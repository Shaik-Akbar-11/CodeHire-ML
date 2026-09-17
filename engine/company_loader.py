import json
from pathlib import Path
import pandas as pd


class CompanyLoader:

    def __init__(self, knowledge_path):
        self.knowledge_path = Path(knowledge_path)

    def load_json(self, filename):
        file = self.knowledge_path / filename

        if not file.exists():
            raise FileNotFoundError(f"{filename} not found.")

        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_json_optional(self, filename):
        file = self.knowledge_path / filename

        if not file.exists():
            return None

        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_csv(self, filename):
        file = self.knowledge_path / filename

        if not file.exists():
            raise FileNotFoundError(f"{filename} not found.")

        return pd.read_csv(file)

    def load_csv_optional(self, filename):
        file = self.knowledge_path / filename

        if not file.exists():
            return None

        return pd.read_csv(file)

    def load_all(self):

        data = {

            # ==========================
            # Company Information (required)
            # ==========================
            "profile": self.load_json("company_profile.json"),
            "pattern": self.load_json("pattern.json"),

            # ==========================
            # Company Information (optional)
            # ==========================
            "preferences": self.load_json_optional("company_preferences.json"),
            "insights": self.load_json_optional("company_insights.json"),
            "metadata": self.load_json_optional("metadata.json"),

            # ==========================
            # Assessment Structure (optional)
            # ==========================
            "oa_rounds": self.load_json_optional("oa_rounds.json"),
            "oa_platforms": self.load_json_optional("oa_platforms.json"),
            "section_distribution": self.load_json_optional("section_distribution.json"),
            "scoring_rules": self.load_json_optional("scoring_rules.json"),
            "previous_patterns": self.load_json_optional("previous_patterns.json"),
            "interview_pattern": self.load_json_optional("interview_pattern.json"),
            "hiring_statistics": self.load_json_optional("hiring_statistics.json"),

            # ==========================
            # Generation Rules (optional)
            # ==========================
            "question_generation_rules": self.load_json_optional("question_generation_rules.json"),
            "validation_rules": self.load_json_optional("validation_rules.json"),
            "constraints": self.load_json_optional("constraints.json"),
            "coding_constraints": self.load_json_optional("coding_constraints.json"),
            "difficulty_rules": self.load_json_optional("difficulty_rules.json"),
            "prompt_templates": self.load_json_optional("company_prompt_templates.json"),

            # ==========================
            # Question Templates (optional)
            # ==========================
            "topic_templates": self.load_json_optional("topic_templates.json"),

            # ==========================
            # Topic CSVs (required)
            # ==========================
            "aptitude": self.load_csv("aptitude_topics.csv"),
            "logical": self.load_csv("logical_topics.csv"),
            "verbal": self.load_csv("verbal_topics.csv"),
            "company_pattern": self.load_csv("company_pattern.csv"),
        }

        # Coding topics are optional — not all companies have them
        coding = self.load_csv_optional("coding_topics.csv")
        if coding is not None:
            data["coding"] = coding

        return data