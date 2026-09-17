"""
engine/batch_engine.py
======================
Generates questions one at a time using single-question prompts
(reliable on Groq free tier) but rotates across topics to keep
the dataset balanced.

Flow per topic:
  build_single_prompt -> generate -> validate -> review -> save
"""

import json
import logging
import time

from engine.exporter import Exporter
from engine.generator import Generator
from engine.prompt_builder import PromptBuilder
from engine.reviewer import Reviewer
from engine.validator import Validator

log = logging.getLogger(__name__)

# Pause between generation call and reviewer call (seconds)
REVIEW_DELAY = 4

# Pause after a successful save (seconds) — keeps us under TPM
POST_SAVE_DELAY = 4

# Max generate+validate+review attempts per question slot
MAX_ATTEMPTS = 10

# How many consecutive failures before skipping a topic
MAX_TOPIC_FAILURES = 8


class BatchEngine:

    def __init__(
        self,
        generator: Generator,
        validator: Validator,
        reviewer:  Reviewer,
    ):
        self.generator = generator
        self.validator = validator
        self.reviewer  = reviewer

    # --------------------------------------------------
    # Generate + validate + review ONE question
    # --------------------------------------------------

    def _generate_one(
        self,
        section: str,
        topic: str,
        difficulty: str,
        builder: PromptBuilder,
    ) -> dict | None:

        for attempt in range(1, MAX_ATTEMPTS + 1):
            log.info(f"    attempt {attempt}/{MAX_ATTEMPTS} | {topic} | {difficulty}")

            prompt = builder.build_prompt(
                section=section,
                topic=topic,
                difficulty=difficulty,
            )

            # --- Generate ---
            try:
                raw      = self.generator.generate(prompt)
                raw      = raw.replace("```json", "").replace("```", "").strip()
                question = json.loads(raw)
            except Exception as e:
                log.warning(f"    generate/parse failed: {e}")
                time.sleep(2)
                continue

            # --- Validate ---
            valid, errors = self.validator.validate(question)
            if not valid:
                log.warning(f"    validation failed: {errors}")
                continue

            # --- Pause before reviewer to avoid back-to-back 429s ---
            delay = 0.05 if getattr(self.generator, "mock", False) else REVIEW_DELAY
            time.sleep(delay)

            # --- Review ---
            try:
                review = self.reviewer.review(json.dumps(question))
            except Exception as e:
                log.warning(f"    reviewer exception: {e}")
                time.sleep(5)
                continue

            if review.get("accepted", False):
                return question

            log.warning(f"    reviewer rejected: {review.get('errors', [])}")

        log.error(f"    gave up: {topic}")
        return None

    # --------------------------------------------------
    # Run until a single topic is complete
    # --------------------------------------------------

    def run_topic(
        self,
        company: str,
        section_name: str,
        topic: str,
        difficulty: str,
        target: int,
        builder: PromptBuilder,
        exporter: Exporter,
        count_fn,
        log_fn=None,
    ) -> int:

        existing = count_fn(exporter, section_name, topic)

        if existing >= target:
            log.info(f"  [SKIP] {topic} complete ({existing}/{target})")
            return 0

        saved        = 0
        failures     = 0
        need         = target - existing

        log.info(f"\n  [{section_name}] {topic} | {difficulty} | need {need} more")

        while existing + saved < target:
            q = self._generate_one(section_name, topic, difficulty, builder)

            if q is None:
                failures += 1
                log.error(f"  failed slot for {topic} (failure {failures}/{MAX_TOPIC_FAILURES})")
                if failures >= MAX_TOPIC_FAILURES:
                    log.error(f"  stopping topic early: {topic}")
                    break
                time.sleep(5)
                continue

            failures = 0   # reset on success
            exporter.save(q)
            saved += 1
            total = existing + saved
            log.info(f"  [SAVED] {topic}: {total}/{target}")

            if log_fn:
                log_fn(company, section_name, topic, total, target)

            save_delay = 0.05 if getattr(self.generator, "mock", False) else POST_SAVE_DELAY
            time.sleep(save_delay)

        return saved

    # --------------------------------------------------
    # Run all topics in a section until complete
    # --------------------------------------------------

    def run_until_complete(
        self,
        company: str,
        section_name: str,
        topics_with_difficulty: list,
        target_per_topic: int,
        builder: PromptBuilder,
        exporter: Exporter,
        count_fn,
        external_sample: str = "None",
        company_pattern_summary: str = "None",
        log_fn=None,
    ) -> int:

        total_saved = 0

        for item in topics_with_difficulty:
            topic      = item["topic"]
            difficulty = item["difficulty"]

            saved = self.run_topic(
                company=company,
                section_name=section_name,
                topic=topic,
                difficulty=difficulty,
                target=target_per_topic,
                builder=builder,
                exporter=exporter,
                count_fn=count_fn,
                log_fn=log_fn,
            )
            total_saved += saved

        return total_saved
