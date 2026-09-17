import re


class Validator:

    REQUIRED_FIELDS = [
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

    REQUIRED_OPTIONS = [
        "A",
        "B",
        "C",
        "D"
    ]

    VALID_SECTIONS = [
        "Quantitative Aptitude",
        "Logical Reasoning",
        "Verbal Ability",
        "Coding"
    ]

    VALID_DIFFICULTIES = [
        "Easy",
        "Easy-Medium",
        "Medium",
        "Medium-Hard",
        "Hard"
    ]

    def __init__(self):

        self.total_checked = 0
        self.total_passed = 0
        self.total_failed = 0

    # ---------------------------------------------------
    # Validate
    # ---------------------------------------------------

    def validate(self, question):

        self.total_checked += 1

        errors = []

        # ---------------------------------------------
        # Required Fields
        # ---------------------------------------------

        for field in self.REQUIRED_FIELDS:

            if field not in question:

                errors.append(
                    f"Missing field : {field}"
                )

        if errors:

            self.total_failed += 1

            return False, errors

        # ---------------------------------------------
        # Validate String Fields
        # ---------------------------------------------

        string_fields = [

            "company",
            "role",
            "section",
            "topic",
            "difficulty",
            "question",
            "answer",
            "explanation"

        ]

        for field in string_fields:

            value = question[field]

            if not isinstance(value, str):

                errors.append(
                    f"{field} must be a string."
                )

                continue

            if len(value.strip()) == 0:

                errors.append(
                    f"{field} cannot be empty."
                )

        # ---------------------------------------------
        # Section Validation
        # ---------------------------------------------

        if question["section"] not in self.VALID_SECTIONS:

            errors.append(
                "Invalid section."
            )

        # ---------------------------------------------
        # Difficulty Validation
        # ---------------------------------------------

        if question["difficulty"] not in self.VALID_DIFFICULTIES:

            errors.append(
                "Invalid difficulty."
            )

        # ---------------------------------------------
        # Company Validation
        # ---------------------------------------------

        if len(question["company"]) < 2:

            errors.append(
                "Invalid company."
            )

        # ---------------------------------------------
        # Role Validation
        # ---------------------------------------------

        if len(question["role"]) < 3:

            errors.append(
                "Invalid role."
            )
        # ---------------------------------------------
        # Question Validation
        # ---------------------------------------------

        q = question["question"].strip()

        if len(q) < 25:

            errors.append(
                "Question is too short."
            )

        if len(q) > 1500:

            errors.append(
                "Question is too long."
            )

        if not re.search(r"[?.!]$", q):

            errors.append(
                "Question should end with punctuation."
            )

        # ---------------------------------------------
        # Options Validation
        # ---------------------------------------------

        options = question["options"]

        if not isinstance(options, dict):

            errors.append(
                "Options must be a dictionary."
            )

        else:

            if len(options) != 4:

                errors.append(
                    "Exactly four options are required."
                )

            for opt in self.REQUIRED_OPTIONS:

                if opt not in options:

                    errors.append(
                        f"Missing option {opt}"
                    )

                    continue

                value = str(
                    options[opt]
                ).strip()

                if len(value) == 0:

                    errors.append(
                        f"Option {opt} is empty."
                    )

        # ---------------------------------------------
        # Duplicate Options
        # ---------------------------------------------

        if isinstance(options, dict):

            values = [

                str(v).strip().lower()

                for v in options.values()

            ]

            if len(values) != len(set(values)):

                errors.append(
                    "Duplicate options detected."
                )

        # ---------------------------------------------
        # Answer Validation
        # ---------------------------------------------

        answer = question["answer"]

        if answer not in self.REQUIRED_OPTIONS:

            errors.append(
                "Answer must be A, B, C or D."
            )

        elif (
            isinstance(options, dict)
            and answer in options
        ):

            answer_text = str(
                options[answer]
            ).strip()

            if len(answer_text) == 0:

                errors.append(
                    "Correct answer is empty."
                )

        # ---------------------------------------------
        # Explanation Validation
        # ---------------------------------------------

        explanation = question[
            "explanation"
        ].strip()

        if len(explanation) < 40:

            errors.append(
                "Explanation is too short."
            )

        if len(explanation) > 2500:

            errors.append(
                "Explanation is too long."
            )

        # ---------------------------------------------
        # Basic Grammar Checks
        # ---------------------------------------------

        if "  " in q:

            errors.append(
                "Multiple spaces detected."
            )

        if "??" in q or ".." in q:

            errors.append(
                "Invalid punctuation."
            )

        if q.count("(") != q.count(")"):

            errors.append(
                "Unbalanced brackets."
            )
        # ---------------------------------------------
        # Final Validation Result
        # ---------------------------------------------

        if errors:

            self.total_failed += 1

            return False, errors

        self.total_passed += 1

        return True, []

    # ---------------------------------------------------
    # Validation Score
    # ---------------------------------------------------

    def get_validation_score(self):

        if self.total_checked == 0:

            return 0.0

        return round(

            (self.total_passed / self.total_checked) * 100,

            2

        )

    # ---------------------------------------------------
    # Print Statistics
    # ---------------------------------------------------

    def print_stats(self):

        print("\n========== VALIDATOR STATS ==========")

        print(f"Total Checked : {self.total_checked}")

        print(f"Passed        : {self.total_passed}")

        print(f"Failed        : {self.total_failed}")

        print(

            f"Success Rate  : {self.get_validation_score()}%"

        )

        print("=====================================\n")

    # ---------------------------------------------------
    # Reset Statistics
    # ---------------------------------------------------

    def reset_stats(self):

        self.total_checked = 0

        self.total_passed = 0

        self.total_failed = 0

    # ---------------------------------------------------
    # Quick Check
    # ---------------------------------------------------

    def health(self):

        print("\n========== VALIDATOR ==========")

        print("Required Fields :", len(self.REQUIRED_FIELDS))

        print("Required Options:", len(self.REQUIRED_OPTIONS))

        print("Valid Sections  :", len(self.VALID_SECTIONS))

        print("Valid Difficulty:", len(self.VALID_DIFFICULTIES))

        print("================================\n")