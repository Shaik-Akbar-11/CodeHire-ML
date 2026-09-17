import re
import pandas as pd


class QualityChecker:

    REQUIRED_COLUMNS = [

        "company",

        "role",

        "section",

        "topic",

        "difficulty",

        "question",

        "options",

        "answer",

        "explanation"

    ]

    VALID_DIFFICULTIES = [

        "Easy",

        "Easy-Medium",

        "Medium",

        "Medium-Hard",

        "Hard"

    ]

    VALID_SECTIONS = [

        "Quantitative Aptitude",

        "Logical Reasoning",

        "Verbal Ability",

        "Coding"

    ]

    VALID_ANSWERS = [

        "A",

        "B",

        "C",

        "D"

    ]

    def __init__(self):

        self.total_rows = 0

        self.accepted_rows = 0

        self.rejected_rows = 0

    # --------------------------------------------------
    # Required Columns
    # --------------------------------------------------

    def missing_columns(self, df):

        missing = []

        for col in self.REQUIRED_COLUMNS:

            if col not in df.columns:

                missing.append(col)

        return missing

    # --------------------------------------------------
    # Empty Rows
    # --------------------------------------------------

    def remove_empty_rows(self, df):

        before = len(df)

        df = df.dropna(how="all")

        removed = before - len(df)

        return df, removed

    # --------------------------------------------------
    # Duplicate Questions
    # --------------------------------------------------

    def remove_duplicates(self, df):

        if "question" not in df.columns:

            return df, 0

        before = len(df)

        df = df.drop_duplicates(

            subset=["question"]

        )

        removed = before - len(df)

        df.reset_index(

            drop=True,

            inplace=True

        )

        return df, removed

    # --------------------------------------------------
    # Validate Columns
    # --------------------------------------------------

    def validate_columns(self, df):

        errors = []

        missing = self.missing_columns(df)

        if missing:

            errors.append(

                f"Missing columns : {missing}"

            )

        return errors

    # --------------------------------------------------
    # Validate Section
    # --------------------------------------------------

    def validate_section(self, value):

        return value in self.VALID_SECTIONS

    # --------------------------------------------------
    # Validate Difficulty
    # --------------------------------------------------

    def validate_difficulty(self, value):

        return value in self.VALID_DIFFICULTIES

    # --------------------------------------------------
    # Validate Answer
    # --------------------------------------------------

    def validate_answer(self, value):

        return value in self.VALID_ANSWERS
    # --------------------------------------------------
    # Question Validation
    # --------------------------------------------------

    def validate_question(self, question):

        errors = []

        question = str(question).strip()

        if len(question) < 25:

            errors.append("Question too short.")

        if len(question) > 1500:

            errors.append("Question too long.")

        if "??" in question or ".." in question:

            errors.append("Invalid punctuation.")

        if "  " in question:

            errors.append("Multiple spaces detected.")

        if not re.search(r"[?.!]$", question):

            errors.append("Question should end with punctuation.")

        placeholders = [

            "lorem ipsum",

            "tbd",

            "coming soon",

            "n/a",

            "sample question"

        ]

        q = question.lower()

        for word in placeholders:

            if word in q:

                errors.append(

                    f"Placeholder detected : {word}"

                )

        return errors

    # --------------------------------------------------
    # Explanation Validation
    # --------------------------------------------------

    def validate_explanation(self, explanation):

        errors = []

        explanation = str(explanation).strip()

        if len(explanation) < 40:

            errors.append(

                "Explanation too short."

            )

        if len(explanation) > 2500:

            errors.append(

                "Explanation too long."

            )

        return errors

    # --------------------------------------------------
    # Options Validation
    # --------------------------------------------------

    def validate_options(self, options):

        errors = []

        if isinstance(options, str):

            options = options.strip()

            if len(options) == 0:

                errors.append(

                    "Options empty."

                )

            return errors

        if not isinstance(options, dict):

            errors.append(

                "Options should be dictionary."

            )

            return errors

        if len(options) != 4:

            errors.append(

                "Exactly four options required."

            )

        values = []

        for key in self.VALID_ANSWERS:

            if key not in options:

                errors.append(

                    f"Missing option {key}"

                )

                continue

            value = str(

                options[key]

            ).strip()

            if len(value) == 0:

                errors.append(

                    f"Option {key} empty."

                )

            values.append(

                value.lower()

            )

        if len(values) != len(set(values)):

            errors.append(

                "Duplicate options detected."

            )

        return errors

    # --------------------------------------------------
    # Grammar Validation
    # --------------------------------------------------

    def grammar_check(self, text):

        errors = []

        text = str(text)

        if "  " in text:

            errors.append(

                "Multiple spaces."

            )

        if text.count("(") != text.count(")"):

            errors.append(

                "Bracket mismatch."

            )

        if text.count('"') % 2 != 0:

            errors.append(

                "Quotation mismatch."

            )

        return errors
    # --------------------------------------------------
    # Validate Single Row
    # --------------------------------------------------

    def validate_row(self, row):

        errors = []

        errors.extend(
            self.validate_question(
                row["question"]
            )
        )

        errors.extend(
            self.validate_explanation(
                row["explanation"]
            )
        )

        errors.extend(
            self.validate_options(
                row["options"]
            )
        )

        if not self.validate_section(
            row["section"]
        ):

            errors.append(
                "Invalid section."
            )

        if not self.validate_difficulty(
            row["difficulty"]
        ):

            errors.append(
                "Invalid difficulty."
            )

        if not self.validate_answer(
            row["answer"]
        ):

            errors.append(
                "Invalid answer."
            )

        errors.extend(
            self.grammar_check(
                row["question"]
            )
        )

        return errors

    # --------------------------------------------------
    # Check Dataset
    # --------------------------------------------------

    def check_dataset(self, df):

        self.total_rows = len(df)

        accepted = []

        rejected = []

        for _, row in df.iterrows():

            errors = self.validate_row(row)

            if len(errors) == 0:

                accepted.append(row)

            else:

                row = row.copy()

                row["errors"] = "; ".join(errors)

                rejected.append(row)

        accepted_df = pd.DataFrame(accepted)

        rejected_df = pd.DataFrame(rejected)

        self.accepted_rows = len(accepted_df)

        self.rejected_rows = len(rejected_df)

        return accepted_df, rejected_df

    # --------------------------------------------------
    # Quality Score
    # --------------------------------------------------

    def quality_score(self):

        if self.total_rows == 0:

            return 0

        return round(

            (self.accepted_rows / self.total_rows) * 100,

            2

        )

    # --------------------------------------------------
    # Print Statistics
    # --------------------------------------------------

    def print_stats(self):

        print("\n========== QUALITY CHECKER ==========")

        print(

            f"Total Rows     : {self.total_rows}"

        )

        print(

            f"Accepted Rows  : {self.accepted_rows}"

        )

        print(

            f"Rejected Rows  : {self.rejected_rows}"

        )

        print(

            f"Quality Score  : {self.quality_score()}%"

        )

        print("=====================================\n")

    # --------------------------------------------------
    # Export Rejected Dataset
    # --------------------------------------------------

    def export_rejected(

        self,

        rejected_df,

        output_file="rejected_dataset.csv"

    ):

        rejected_df.to_csv(

            output_file,

            index=False

        )

        print(

            f"Rejected dataset saved to {output_file}"

        )

    # --------------------------------------------------
    # Reset Statistics
    # --------------------------------------------------

    def reset_stats(self):

        self.total_rows = 0

        self.accepted_rows = 0

        self.rejected_rows = 0

    # --------------------------------------------------
    # Health Check
    # --------------------------------------------------

    def health(self):

        print("\n========== QUALITY CHECKER ==========")

        print(

            f"Required Columns : {len(self.REQUIRED_COLUMNS)}"

        )

        print(

            f"Valid Sections   : {len(self.VALID_SECTIONS)}"

        )

        print(

            f"Valid Difficulty : {len(self.VALID_DIFFICULTIES)}"

        )

        print(

            f"Valid Answers    : {len(self.VALID_ANSWERS)}"

        )

        print("=====================================\n")