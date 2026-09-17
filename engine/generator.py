import os
import time
import json
import logging

from dotenv import load_dotenv
from groq import Groq, RateLimitError

load_dotenv()

log = logging.getLogger(__name__)


class Generator:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment.")

        self.client      = Groq(api_key=api_key)
        self.model            = "llama-3.3-70b-versatile"
        self.max_retries      = 8
        self.temperature      = 0.7
        self.top_p            = 0.9
        self.max_tokens       = 1200  # single question — keep under TPM budget
        self.max_tokens_batch = 1200  # same — batch mode also uses single-q prompt

        self.stats = {
            "generated":   0,
            "success":     0,
            "failed":      0,
            "invalid_json": 0,
            "rate_limits": 0,
        }

    # --------------------------------------------------
    # Clean / Repair
    # --------------------------------------------------

    def clean_response(self, text):
        if not text:
            return ""
        text = text.replace("```json", "").replace("```", "")
        return text.strip()

    def repair_json(self, text):
        text  = self.clean_response(text)
        start = text.find("{")
        end   = text.rfind("}")
        if start != -1 and end != -1:
            text = text[start:end + 1]
        return text

    def is_valid_json(self, text):
        try:
            json.loads(text)
            return True
        except Exception:
            return False

    # --------------------------------------------------
    # Core generate — returns raw string
    # --------------------------------------------------

    def generate(self, prompt: str, max_tokens: int = None) -> str:
        self.stats["generated"] += 1

        system_prompt = (
            "You are a Senior Placement Assessment Architect.\n"
            "Generate company-specific Online Assessment questions.\n\n"
            "Rules:\n"
            "- Return ONLY valid JSON (object or array as instructed).\n"
            "- Never use markdown or ```json.\n"
            "- Never add explanation outside JSON.\n"
            "- Generate ORIGINAL questions only.\n"
            "- Mathematics must be 100% correct.\n"
            "- Explanation must match the selected answer exactly.\n"
            "- Difficulty must match the requested level.\n"
            "- JSON must be parseable by Python json.loads().\n"
        )

        tokens = max_tokens or self.max_tokens
        wait   = 10  # initial rate-limit wait (seconds)

        for attempt in range(1, self.max_retries + 1):
            try:
                log.info(f"Generator attempt {attempt}/{self.max_retries}")

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user",   "content": prompt},
                    ],
                    temperature=self.temperature,
                    top_p=self.top_p,
                    max_completion_tokens=tokens,
                )

                text = response.choices[0].message.content
                text = self.repair_json(text)

                if self.is_valid_json(text):
                    self.stats["success"] += 1
                    return text

                log.warning("Invalid JSON — retrying")
                self.stats["invalid_json"] += 1
                time.sleep(2)

            except RateLimitError:
                self.stats["rate_limits"] += 1
                log.warning(f"Rate limit hit. Waiting {wait}s (attempt {attempt})")
                time.sleep(wait)
                wait = min(wait * 2, 120)   # exponential backoff, cap 120s

            except Exception as e:
                log.error(f"Generator error: {e}")
                time.sleep(5)

        self.stats["failed"] += 1
        raise RuntimeError("Generator: max retries exhausted.")

    # --------------------------------------------------
    # generate_batch — returns raw string (JSON array)
    # --------------------------------------------------

    def generate_batch(self, prompt: str) -> str:
        """Generate a batch prompt expecting a JSON array back."""
        return self.generate(prompt, max_tokens=self.max_tokens_batch)

    # --------------------------------------------------
    # generate_json — returns parsed dict
    # --------------------------------------------------

    def generate_json(self, prompt: str) -> dict:
        raw  = self.generate(prompt)
        raw  = self.repair_json(raw)
        try:
            return json.loads(raw)
        except Exception as e:
            self.stats["invalid_json"] += 1
            log.error(f"JSON parse failed: {e}")
            raise ValueError("Generator returned invalid JSON.")

    # --------------------------------------------------
    # Stats / Health
    # --------------------------------------------------

    def print_stats(self):
        print("\n========== GENERATOR STATS ==========")
        for k, v in self.stats.items():
            print(f"  {k:15} : {v}")
        print("=====================================\n")

    def reset_stats(self):
        self.stats = {k: 0 for k in self.stats}

    def get_stats(self):
        return self.stats.copy()

    def health(self):
        print("\n========== GENERATOR ==========")
        print(f"  Model       : {self.model}")
        print(f"  Temperature : {self.temperature}")
        print(f"  Max Retries : {self.max_retries}")
        print(f"  Max Tokens  : {self.max_tokens}")
        print("================================\n")
