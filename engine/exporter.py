import csv
import os


class Exporter:

    def __init__(self, company):

        self.output_root = f"output/{company}"

        os.makedirs(
            self.output_root,
            exist_ok=True
        )

        self.headers = [
            "Company",
            "Role",
            "Section",
            "Topic",
            "Difficulty",
            "Question",
            "Option A",
            "Option B",
            "Option C",
            "Option D",
            "Answer",
            "Explanation"
        ]

    def get_filename(self, section):

        section = section.lower()

        if "quantitative" in section:
            return "quantitative.csv"

        elif "logical" in section:
            return "logical.csv"

        elif "verbal" in section:
            return "verbal.csv"

        elif "coding" in section:
            return "coding.csv"

        else:
            return "others.csv"

    def save(self, question):

        filename = self.get_filename(
            question.get("section", "")
        )

        filepath = os.path.join(
            self.output_root,
            filename
        )

        file_exists = os.path.exists(filepath)

        with open(
            filepath,
            "a",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.writer(csvfile)

            if not file_exists:
                writer.writerow(self.headers)

            options = question.get("options", {})

            writer.writerow([
                question.get("company", ""),
                question.get("role", ""),
                question.get("section", ""),
                question.get("topic", ""),
                question.get("difficulty", ""),
                question.get("question", ""),
                options.get("A", ""),
                options.get("B", ""),
                options.get("C", ""),
                options.get("D", ""),
                question.get("answer", ""),
                question.get("explanation", "")
            ])

        print(f"[SAVED] {filename}")