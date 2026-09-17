"""
audit.py  —  Re-reviews every saved question through the strict Reviewer.
Bad questions are removed from the CSV so they get regenerated on next run.
"""

import json
import time
import pandas as pd
from engine.reviewer import Reviewer

COMPANY = "Amazon"

SECTIONS = [
    ("quantitative", f"output/{COMPANY}/quantitative.csv"),
    ("logical",      f"output/{COMPANY}/logical.csv"),
    ("verbal",       f"output/{COMPANY}/verbal.csv"),
    ("coding",       f"output/{COMPANY}/coding.csv"),
]

def row_to_question(row):
    return {
        "company":     row.get("Company", ""),
        "role":        row.get("Role", ""),
        "section":     row.get("Section", ""),
        "topic":       row.get("Topic", ""),
        "difficulty":  row.get("Difficulty", ""),
        "question":    row.get("Question", ""),
        "options": {
            "A": row.get("Option A", ""),
            "B": row.get("Option B", ""),
            "C": row.get("Option C", ""),
            "D": row.get("Option D", ""),
        },
        "answer":      row.get("Answer", ""),
        "explanation": row.get("Explanation", ""),
    }


def audit():
    reviewer = Reviewer()
    total_removed = 0

    for sec, filepath in SECTIONS:
        try:
            df = pd.read_csv(filepath)
        except FileNotFoundError:
            print(f"⚠  {filepath} not found — skipping.")
            continue

        print(f"\n{'='*60}")
        print(f"AUDITING: {sec.upper()}  ({len(df)} questions)")
        print(f"{'='*60}")

        keep_indices = []

        for i, row in df.iterrows():
            topic = row.get("Topic", "?")
            question_json = json.dumps(row_to_question(row))

            print(f"  [{i+1}/{len(df)}] {topic} ...", end=" ", flush=True)

            review = reviewer.review(question_json)
            time.sleep(2)  # rate limit buffer

            if review.get("accepted", False):
                score = review.get("overall_score", 0)
                print(f"✅ score={score}")
                keep_indices.append(i)
            else:
                errors = review.get("errors", [])
                score  = review.get("overall_score", 0)
                print(f"❌ score={score}  errors={errors}")
                total_removed += 1

        cleaned = df.loc[keep_indices].reset_index(drop=True)
        cleaned.to_csv(filepath, index=False)
        removed = len(df) - len(cleaned)
        print(f"\n  Kept {len(cleaned)}, removed {removed} from {sec}")

    print(f"\n{'='*60}")
    print(f"AUDIT COMPLETE — {total_removed} bad questions removed.")
    print(f"Run main.py to regenerate the removed questions.")
    print(f"{'='*60}")


if __name__ == "__main__":
    audit()
