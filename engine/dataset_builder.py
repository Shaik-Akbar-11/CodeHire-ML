import pandas as pd


class DatasetBuilder:
    """
    Builds the generation plan for a company.

    Each topic in each section gets `questions_per_topic` questions.
    Topics are ordered by priority (Very High > High > Medium > Low).
    """

    SECTION_KEYS = [
        ("Quantitative Aptitude", "aptitude"),
        ("Logical Reasoning",     "logical"),
        ("Verbal Ability",        "verbal"),
    ]

    PRIORITY_ORDER = {
        "Very High": 0,
        "High":      1,
        "Medium":    2,
        "Low":       3,
    }

    def __init__(self, company_data, questions_per_topic=500):
        self.data               = company_data
        self.questions_per_topic = questions_per_topic

    def _sort_by_priority(self, df):
        df = df.copy()
        df["_order"] = df["priority"].map(self.PRIORITY_ORDER).fillna(9)
        df = df.sort_values("_order").reset_index(drop=True)
        df.drop(columns=["_order"], inplace=True)
        return df

    def build(self):
        """
        Returns a list of dicts:
            { "section", "topic", "difficulty", "target" }

        Each entry = one topic that needs `target` questions generated.
        """
        plan = []

        for section_name, data_key in self.SECTION_KEYS:
            df = self.data.get(data_key)
            if df is None or len(df) == 0:
                continue

            df = self._sort_by_priority(df)

            for _, row in df.iterrows():
                plan.append({
                    "section":    section_name,
                    "topic":      row["topic"],
                    "difficulty": row["difficulty"],
                    "target":     self.questions_per_topic,
                })

        return plan

    def summary(self):
        plan = self.build()
        topics = len(plan)
        total  = topics * self.questions_per_topic
        print(f"Topics: {topics}  |  Questions per topic: {self.questions_per_topic}  |  Total: {total}")
        return plan
