import json


class PromptBuilder:

    # Difficulty distribution targets (for 10k per company)
    DIFFICULTY_DIST = {
        "Easy":        0.15,
        "Easy-Medium": 0.25,
        "Medium":      0.30,
        "Medium-Hard": 0.20,
        "Hard":        0.10,
    }

    def __init__(self, profile, pattern):
        self.profile = profile
        self.pattern = pattern

    # --------------------------------------------------
    # Difficulty mapper — handles missing keys in pattern
    # --------------------------------------------------

    def _map_difficulty(self, difficulty):
        if difficulty in self.pattern["difficulty"]:
            return difficulty
        mapping = {
            "Easy-Medium": "Medium",
            "Medium-Hard": "Hard",
            "Easy-Hard":   "Hard",
            "Very Easy":   "Easy",
            "Very Hard":   "Hard",
        }
        return mapping.get(difficulty, "Medium")

    # --------------------------------------------------
    # Shared field extraction
    # --------------------------------------------------

    def _base_fields(self):
        company = self.profile.get("company", "")

        role_field = self.profile.get(
            "role",
            self.profile.get("primary_hiring_roles", ["Software Engineer"])
        )
        role = role_field[0] if isinstance(role_field, list) else role_field

        question_style = self.pattern.get("question_style", "Scenario Based")
        real_world     = self.pattern.get("real_world_context", True)
        reasoning      = self.pattern.get("multi_step_reasoning", True)
        calculator     = self.pattern.get("calculator_allowed", False)
        rules          = self.pattern.get("generation_rules", self.pattern.get("rules", []))

        return company, role, question_style, real_world, reasoning, calculator, rules

    # --------------------------------------------------
    # Single-question prompt (used by legacy flow)
    # --------------------------------------------------

    def build_prompt(self, section, topic, difficulty):
        company, role, question_style, real_world, reasoning, calculator, rules = self._base_fields()

        diff_key = self._map_difficulty(difficulty)
        diff     = self.pattern["difficulty"][diff_key]
        steps    = diff.get("steps", 2)
        time_val = diff.get("time_minutes", diff.get("time", 2))

        prompt = f"""You are a Senior Placement Assessment Architect, Mathematics Expert, and Quality Reviewer.
Your task is to generate ONE ORIGINAL, HIGH-QUALITY multiple-choice aptitude question for a company placement assessment.

==================================================
INPUT
==================================================
Company      : {company}
Role         : {role}
Section      : {section}
Topic        : {topic}
Difficulty   : {difficulty}
Question Style        : {question_style}
Real-World Context    : {real_world}
Multi-Step Reasoning  : {reasoning}
Calculator Allowed    : {calculator}
Expected Reasoning Steps : {steps}
Expected Solving Time    : {time_val} minutes

==================================================
GENERATION RULES
==================================================
{chr(10).join(f'- {r}' for r in rules)}

==================================================
INTERNAL PROCESS (do this before outputting)
==================================================
STEP 1 - Design one clear problem for {section} / {topic} / {difficulty}.
STEP 2 - Solve it completely. Verify all arithmetic twice.
STEP 3 - Determine the exact correct answer independently.
STEP 4 - Create four distinct options (A/B/C/D). Exactly ONE correct.
         Distractors = realistic mistakes (arithmetic, formula misuse, incomplete reasoning).
STEP 5 - Verify all four options. If >1 correct: regenerate.
STEP 6 - Select the answer letter only after full verification.
STEP 7 - Write explanation (40-100 words) showing key steps. End with the exact final answer.
STEP 8 - Quality gate: math correct, one answer, original, unambiguous, matches difficulty.

==================================================
DIFFICULTY: {difficulty}
==================================================
EASY          : 1-2 steps, direct formula, 30-60 sec
EASY-MEDIUM   : 2-3 steps, one twist, 60-90 sec
MEDIUM        : 3-4 steps, careful calculation, 90-150 sec
MEDIUM-HARD   : 4-5 steps, multi-condition, 2-3 min
HARD          : 5+ steps, interacting constraints, 3-5 min

==================================================
MATHEMATICAL SAFETY
==================================================
- Successive %: apply sequentially, never add/subtract directly
- Profit/Loss %: always over Cost Price
- Average speed: total distance / total time
- Compound interest: verify formula and period
- Probability: 0<=P<=1, verify sample space
- Permutation/Combination: verify whether order matters

==================================================
OUTPUT
==================================================
Return ONLY ONE valid JSON object. No markdown. No ```json. Parseable by json.loads().

{{"company":"{company}","role":"{role}","section":"{section}","topic":"{topic}","difficulty":"{difficulty}","question":"","options":{{"A":"","B":"","C":"","D":""}},"answer":"A","explanation":""}}"""

        return prompt.strip()

    # --------------------------------------------------
    # Batch prompt — generates `batch_size` questions in
    # one LLM call. Returns a JSON ARRAY.
    # --------------------------------------------------

    def build_batch_prompt(
        self,
        section: str,
        topics_with_difficulty: list,   # [{"topic": ..., "difficulty": ...}, ...]
        batch_size: int,
        external_sample: str = "None",
        company_pattern_summary: str = "None",
    ) -> str:

        company, role, question_style, real_world, reasoning, calculator, _ = self._base_fields()

        # Pick up to 8 pending topics to keep prompt small
        topics_subset = topics_with_difficulty[:8]
        topics_str = ", ".join(
            f"{t['topic']}({t['difficulty']})"
            for t in topics_subset
        )

        # Difficulty distribution for this batch
        dist = self._batch_difficulty_plan(batch_size)
        dist_str = " | ".join(f"{d}:{n}" for d, n in dist.items() if n > 0)

        prompt = f"""You are a Senior Assessment Architect generating placement questions for {company}.

TASK: Generate exactly {batch_size} ORIGINAL MCQ questions for section "{section}".

COMPANY: {company} | ROLE: {role} | STYLE: {question_style} | CALCULATOR: {calculator}

TOPICS (pick from these): {topics_str}

DIFFICULTY TARGETS FOR THIS BATCH: {dist_str}

RULES:
1. Each question: 4 options (A/B/C/D), exactly 1 correct, 3 plausible distractors.
2. Solve every question internally before writing options. Verify arithmetic twice.
3. Explanation: 40-80 words, show key steps, end with exact final answer.
4. Difficulty from reasoning depth, NOT confusing wording or huge numbers.
5. EASY=1-2 steps | EASY-MEDIUM=2-3 | MEDIUM=3-4 | MEDIUM-HARD=4-5 | HARD=5+
6. Math rules: Profit%=Profit/CP*100 | AvgSpeed=TotalDist/TotalTime | SI/CI use correct formula | P(A) in [0,1].
7. All questions original. Different numbers, scenarios, reasoning paths per question.

OUTPUT: Return ONLY a valid JSON array. No markdown. No text outside JSON.
Format per element:
{{"company":"{company}","role":"{role}","section":"{section}","topic":"TOPIC","difficulty":"DIFFICULTY","question":"","options":{{"A":"","B":"","C":"","D":""}},"answer":"A","explanation":""}}

Generate {batch_size} questions now:"""

        return prompt.strip()

    def _batch_difficulty_plan(self, batch_size: int) -> dict:
        """Return how many questions of each difficulty to generate in a batch."""
        dist = {
            "Easy":        0.15,
            "Easy-Medium": 0.25,
            "Medium":      0.30,
            "Medium-Hard": 0.20,
            "Hard":        0.10,
        }
        plan = {}
        remaining = batch_size
        keys = list(dist.keys())
        for i, k in enumerate(keys):
            if i == len(keys) - 1:
                plan[k] = remaining
            else:
                n = round(dist[k] * batch_size)
                plan[k] = n
                remaining -= n
        return plan
