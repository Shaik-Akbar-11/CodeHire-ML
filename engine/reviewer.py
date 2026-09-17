import json
import logging
import time

from engine.generator import Generator

log = logging.getLogger(__name__)


class Reviewer:

    ACCEPT_SCORE = 85   # slightly relaxed to reduce unnecessary rejections

    CRITICAL_CHECKS = [
        "mathematics_correct",
        "answer_correct",
        "explanation_correct",
        "single_correct_answer",
        "topic_match",
        "grammar_correct",
    ]

    def __init__(self):
        self.generator      = Generator()
        self.total_reviewed = 0
        self.total_accepted = 0
        self.total_rejected = 0

    # --------------------------------------------------
    # Build reviewer prompt
    # --------------------------------------------------

    def _build_prompt(self, question_json: str) -> str:
        return f"""You are a STRICT Senior Assessment Reviewer.
You are ONLY reviewing — NOT generating.

Review the question below using these steps:

STEP 1: Solve the question yourself completely. Ignore the provided answer.
STEP 2: Compare your answer with the marked answer. Reject if different.
STEP 3: Verify the explanation leads to the marked answer. Reject if not.
STEP 4: Verify all arithmetic. Reject any mistake.
STEP 5: Verify the topic label matches the question content.
STEP 6: Verify grammar and clarity. Reject if ambiguous.
STEP 7: Verify exactly ONE option is correct.

SCORING (out of 100):
Mathematics        /20
Answer Correct     /20
Explanation        /15
Topic Match        /15
Grammar            /15
Single Answer      /15

Return ONLY valid JSON — no markdown, no explanation outside JSON:

{{
    "accepted": true,
    "overall_score": 95,
    "checks": {{
        "mathematics_correct": true,
        "answer_correct": true,
        "explanation_correct": true,
        "single_correct_answer": true,
        "topic_match": true,
        "grammar_correct": true
    }},
    "errors": []
}}

QUESTION TO REVIEW:
{question_json}"""

    # --------------------------------------------------
    # Review
    # --------------------------------------------------

    def review(self, question_json: str) -> dict:
        self.total_reviewed += 1

        FAIL = {
            "accepted":      False,
            "overall_score": 0,
            "checks": {c: False for c in self.CRITICAL_CHECKS},
            "errors": ["Reviewer failed to produce a valid response."],
        }

        try:
            prompt   = self._build_prompt(question_json)
            raw      = self.generator.generate(prompt)
            raw      = raw.replace("```json", "").replace("```", "").strip()
            result   = json.loads(raw)
        except Exception as e:
            log.warning(f"Reviewer error: {e}")
            self.total_rejected += 1
            return FAIL

        score  = result.get("overall_score", 0)
        checks = result.get("checks", {})
        errors = list(result.get("errors", []))

        accepted = True

        if score < self.ACCEPT_SCORE:
            accepted = False
            errors.append(f"Score {score} below threshold {self.ACCEPT_SCORE}")

        for check in self.CRITICAL_CHECKS:
            if not checks.get(check, False):
                accepted = False
                errors.append(f"Failed: {check}")

        result["accepted"] = accepted
        result["errors"]   = list(dict.fromkeys(errors))

        if accepted:
            self.total_accepted += 1
            log.info(f"Review PASSED | score={score}")
        else:
            self.total_rejected += 1
            log.warning(f"Review FAILED | score={score} | {result['errors']}")

        return result

    # --------------------------------------------------
    # Stats
    # --------------------------------------------------

    def get_success_rate(self):
        if self.total_reviewed == 0:
            return 0.0
        return round(self.total_accepted / self.total_reviewed * 100, 2)

    def print_stats(self):
        print("\n========== REVIEWER STATS ==========")
        print(f"  Reviewed        : {self.total_reviewed}")
        print(f"  Accepted        : {self.total_accepted}")
        print(f"  Rejected        : {self.total_rejected}")
        print(f"  Acceptance Rate : {self.get_success_rate()}%")
        print("=====================================\n")

    def reset_stats(self):
        self.total_reviewed = 0
        self.total_accepted = 0
        self.total_rejected = 0

    def health(self):
        print(f"\nReviewer | Min Score: {self.ACCEPT_SCORE} | "
              f"Critical checks: {len(self.CRITICAL_CHECKS)}\n")
