import json
import re
from pathlib import Path

import pandas as pd


class PatternExtractor:

    def __init__(self, root_path="datasets/external"):

        self.root_path = Path(root_path)

    # --------------------------------------------------
    # Company Path
    # --------------------------------------------------

    def company_path(self, company):

        return self.root_path / company

    # --------------------------------------------------
    # Load All CSV Files
    # --------------------------------------------------

    def load_company(self, company):

        company_path = self.company_path(company)

        if not company_path.exists():

            raise FileNotFoundError(

                f"{company} dataset not found."

            )

        frames = []

        for file in company_path.glob("*.csv"):

            df = pd.read_csv(file)

            df["source_file"] = file.name

            frames.append(df)

        if len(frames) == 0:

            return pd.DataFrame()

        return pd.concat(

            frames,

            ignore_index=True

        )

    # --------------------------------------------------
    # Average Question Length
    # --------------------------------------------------

    def average_question_length(self, df):

        if "question" not in df.columns:

            return 0

        lengths = (

            df["question"]

            .astype(str)

            .apply(

                lambda x: len(x.split())

            )

        )

        return round(

            lengths.mean(),

            2

        )

    # --------------------------------------------------
    # Average Explanation Length
    # --------------------------------------------------

    def average_explanation_length(self, df):

        if "explanation" not in df.columns:

            return 0

        lengths = (

            df["explanation"]

            .astype(str)

            .apply(

                lambda x: len(x.split())

            )

        )

        return round(

            lengths.mean(),

            2

        )

    # --------------------------------------------------
    # Average Option Length
    # --------------------------------------------------

    def average_option_length(self, df):

        if "options" not in df.columns:

            return 0

        total = 0

        count = 0

        for value in df["options"]:

            text = str(value)

            total += len(text.split())

            count += 1

        if count == 0:

            return 0

        return round(

            total / count,

            2

        )

    # --------------------------------------------------
    # Difficulty Distribution
    # --------------------------------------------------

    def difficulty_distribution(self, df):

        if "difficulty" not in df.columns:

            return {}

        return (

            df["difficulty"]

            .value_counts()

            .to_dict()

        )
    # --------------------------------------------------
    # Topic Distribution
    # --------------------------------------------------

    def topic_distribution(self, df):

        if "topic" not in df.columns:

            return {}

        return (

            df["topic"]

            .astype(str)

            .str.strip()

            .value_counts()

            .to_dict()

        )

    # --------------------------------------------------
    # Section Distribution
    # --------------------------------------------------

    def section_distribution(self, df):

        if "section" not in df.columns:

            return {}

        return (

            df["section"]

            .astype(str)

            .str.strip()

            .value_counts()

            .to_dict()

        )

    # --------------------------------------------------
    # Answer Distribution
    # --------------------------------------------------

    def answer_distribution(self, df):

        if "answer" not in df.columns:

            return {}

        return (

            df["answer"]

            .astype(str)

            .str.strip()

            .value_counts()

            .to_dict()

        )

    # --------------------------------------------------
    # Most Common Keywords
    # --------------------------------------------------

    def common_keywords(

        self,

        df,

        top_n=30

    ):

        if "question" not in df.columns:

            return {}

        words = []

        stop_words = {

            "the", "is", "a", "an", "of", "to",

            "and", "or", "in", "on", "at",

            "for", "with", "by", "from",

            "which", "what", "how", "if",

            "then", "find", "calculate"

        }

        for question in df["question"]:

            text = str(question).lower()

            tokens = re.findall(

                r"[a-zA-Z]+",

                text

            )

            for token in tokens:

                if len(token) < 3:

                    continue

                if token in stop_words:

                    continue

                words.append(token)

        return (

            pd.Series(words)

            .value_counts()

            .head(top_n)

            .to_dict()

        )

    # --------------------------------------------------
    # Common Question Openings
    # --------------------------------------------------

    def common_openings(

        self,

        df,

        top_n=15

    ):

        if "question" not in df.columns:

            return {}

        openings = []

        for question in df["question"]:

            words = str(question).split()

            opening = " ".join(

                words[:3]

            ).strip()

            if opening:

                openings.append(opening)

        return (

            pd.Series(openings)

            .value_counts()

            .head(top_n)

            .to_dict()

        )

    # --------------------------------------------------
    # Average Sentence Length
    # --------------------------------------------------

    def average_sentence_length(self, df):

        if "question" not in df.columns:

            return 0

        total = 0

        count = 0

        for question in df["question"]:

            words = len(

                str(question).split()

            )

            total += words

            count += 1

        if count == 0:

            return 0

        return round(

            total / count,

            2

        )
    # --------------------------------------------------
    # Topic Distribution
    # --------------------------------------------------

    def topic_distribution(self, df):

        if "topic" not in df.columns:
            return {}

        return (
            df["topic"]
            .astype(str)
            .str.strip()
            .value_counts()
            .to_dict()
        )

    # --------------------------------------------------
    # Section Distribution
    # --------------------------------------------------

    def section_distribution(self, df):

        if "section" not in df.columns:
            return {}

        return (
            df["section"]
            .astype(str)
            .str.strip()
            .value_counts()
            .to_dict()
        )

    # --------------------------------------------------
    # Answer Distribution
    # --------------------------------------------------

    def answer_distribution(self, df):

        if "answer" not in df.columns:
            return {}

        return (
            df["answer"]
            .astype(str)
            .str.strip()
            .value_counts()
            .to_dict()
        )

    # --------------------------------------------------
    # Common Keywords
    # --------------------------------------------------

    def common_keywords(self, df, top_n=30):

        if "question" not in df.columns:
            return {}

        stop_words = {
            "the", "is", "a", "an", "of", "to",
            "and", "or", "in", "on", "at",
            "for", "with", "by", "from",
            "which", "what", "how", "find",
            "calculate", "determine", "following"
        }

        words = []

        for question in df["question"]:

            tokens = re.findall(
                r"[A-Za-z]+",
                str(question).lower()
            )

            for token in tokens:

                if len(token) < 3:
                    continue

                if token in stop_words:
                    continue

                words.append(token)

        return (
            pd.Series(words)
            .value_counts()
            .head(top_n)
            .to_dict()
        )

    # --------------------------------------------------
    # Common Question Openings
    # --------------------------------------------------

    def common_openings(self, df, top_n=15):

        if "question" not in df.columns:
            return {}

        openings = []

        for question in df["question"]:

            words = str(question).split()

            if len(words) >= 3:
                openings.append(" ".join(words[:3]))
            elif words:
                openings.append(" ".join(words))

        return (
            pd.Series(openings)
            .value_counts()
            .head(top_n)
            .to_dict()
        )

    # --------------------------------------------------
    # Average Sentence Length
    # --------------------------------------------------

    def average_sentence_length(self, df):

        if "question" not in df.columns:
            return 0

        lengths = (
            df["question"]
            .astype(str)
            .apply(lambda x: len(x.split()))
        )

        if len(lengths) == 0:
            return 0

        return round(lengths.mean(), 2)
    # --------------------------------------------------
    # Build Complete Pattern
    # --------------------------------------------------

    def build_pattern(self, company):

        df = self.load_company(company)

        if df.empty:

            raise ValueError(
                "Dataset is empty."
            )

        pattern = {

            "company": company,

            "dataset_size": len(df),

            "average_question_length":
                self.average_question_length(df),

            "average_explanation_length":
                self.average_explanation_length(df),

            "average_option_length":
                self.average_option_length(df),

            "average_sentence_length":
                self.average_sentence_length(df),

            "difficulty_distribution":
                self.difficulty_distribution(df),

            "topic_distribution":
                self.topic_distribution(df),

            "section_distribution":
                self.section_distribution(df),

            "answer_distribution":
                self.answer_distribution(df),

            "common_keywords":
                self.common_keywords(df),

            "common_openings":
                self.common_openings(df)

        }

        return pattern

    # --------------------------------------------------
    # Export Pattern
    # --------------------------------------------------

    def export_pattern(

        self,

        company,

        output_root="knowledge"

    ):

        pattern = self.build_pattern(company)

        output_dir = Path(output_root) / company

        output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        output_file = (

            output_dir /

            "extracted_pattern.json"

        )

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                pattern,

                f,

                indent=4,

                ensure_ascii=False

            )

        print(

            f"Pattern exported : {output_file}"

        )

        return output_file

    # --------------------------------------------------
    # Pattern Statistics
    # --------------------------------------------------

    def print_pattern(self, company):

        pattern = self.build_pattern(company)

        print("\n========== PATTERN SUMMARY ==========")

        print(

            f"Company : {pattern['company']}"

        )

        print(

            f"Dataset Size : {pattern['dataset_size']}"

        )

        print(

            f"Average Question Length : {pattern['average_question_length']} words"

        )

        print(

            f"Average Explanation Length : {pattern['average_explanation_length']} words"

        )

        print(

            f"Average Option Length : {pattern['average_option_length']} words"

        )

        print(

            f"Average Sentence Length : {pattern['average_sentence_length']} words"

        )

        print("\nDifficulty Distribution")

        for k, v in pattern["difficulty_distribution"].items():

            print(f"{k} : {v}")

        print("\nTopic Distribution")

        for k, v in pattern["topic_distribution"].items():

            print(f"{k} : {v}")

        print("\nAnswer Distribution")

        for k, v in pattern["answer_distribution"].items():

            print(f"{k} : {v}")

        print("=====================================\n")

    # --------------------------------------------------
    # Health Check
    # --------------------------------------------------

    def health(self):

        print("\n========== PATTERN EXTRACTOR ==========")

        print(

            f"Dataset Root : {self.root_path}"

        )

        print("Status : Ready")

        print("=======================================\n")