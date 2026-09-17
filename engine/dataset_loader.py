import json
from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd


class DatasetLoader:

    def __init__(self, root_path="datasets/external"):

        self.root_path = Path(root_path)

        self.root_path.mkdir(
            parents=True,
            exist_ok=True
        )

    # --------------------------------------------------
    # Company Folder
    # --------------------------------------------------

    def get_company_path(self, company):

        return self.root_path / company

    # --------------------------------------------------
    # Companies
    # --------------------------------------------------

    def list_companies(self):

        companies = []

        for item in self.root_path.iterdir():

            if item.is_dir():

                companies.append(item.name)

        companies.sort()

        return companies

    # --------------------------------------------------
    # Dataset Files
    # --------------------------------------------------

    def list_dataset_files(self, company):

        company_path = self.get_company_path(company)

        if not company_path.exists():

            raise FileNotFoundError(

                f"Company folder not found : {company}"

            )

        files = []

        for file in company_path.iterdir():

            if file.suffix.lower() in [

                ".csv",

                ".json"

            ]:

                files.append(file)

        files.sort()

        return files

    # --------------------------------------------------
    # Load CSV
    # --------------------------------------------------

    def load_csv(self, file_path):

        return pd.read_csv(file_path)

    # --------------------------------------------------
    # Load JSON
    # --------------------------------------------------

    def load_json(self, file_path):

        with open(

            file_path,

            "r",

            encoding="utf-8"

        ) as f:

            data = json.load(f)

        return pd.DataFrame(data)

    # --------------------------------------------------
    # Load Dataset
    # --------------------------------------------------

    def load_dataset(self, file_path):

        file_path = Path(file_path)

        if not file_path.exists():

            raise FileNotFoundError(

                file_path

            )

        extension = file_path.suffix.lower()

        if extension == ".csv":

            return self.load_csv(file_path)

        if extension == ".json":

            return self.load_json(file_path)

        raise ValueError(

            f"Unsupported file : {extension}"

        )

    # --------------------------------------------------
    # Load All Company Files
    # --------------------------------------------------

    def load_company(self, company):

        datasets = {}

        files = self.list_dataset_files(company)

        for file in files:

            print(

                f"Loading : {file.name}"

            )

            datasets[file.stem] = self.load_dataset(file)

        return datasets
    # --------------------------------------------------
    # Merge Company Datasets
    # --------------------------------------------------

    def merge_company_datasets(self, company):

        datasets = self.load_company(company)

        frames = []

        for name, df in datasets.items():

            if df is None:

                continue

            df = df.copy()

            df["source_file"] = name

            df["company"] = company

            frames.append(df)

        if len(frames) == 0:

            return pd.DataFrame()

        merged = pd.concat(

            frames,

            ignore_index=True

        )

        return merged

    # --------------------------------------------------
    # Normalize Column Names
    # --------------------------------------------------

    def normalize_columns(self, df):

        df = df.copy()

        df.columns = [

            str(col)
            .strip()
            .lower()
            .replace(" ", "_")

            for col in df.columns

        ]

        rename_map = {

            "question_text": "question",

            "questions": "question",

            "correct_answer": "answer",

            "correctoption": "answer",

            "difficulty_level": "difficulty",

            "topic_name": "topic",

            "solution": "explanation"

        }

        df.rename(

            columns=rename_map,

            inplace=True

        )

        return df

    # --------------------------------------------------
    # Remove Empty Rows
    # --------------------------------------------------

    def remove_empty_rows(self, df):

        df = df.dropna(

            how="all"

        )

        return df

    # --------------------------------------------------
    # Remove Duplicate Questions
    # --------------------------------------------------

    def remove_duplicates(self, df):

        if "question" not in df.columns:

            return df

        df = df.drop_duplicates(

            subset=["question"]

        )

        df.reset_index(

            drop=True,

            inplace=True

        )

        return df

    # --------------------------------------------------
    # Validate Required Columns
    # --------------------------------------------------

    def validate_columns(self, df):

        required = [

            "question",

            "answer"

        ]

        missing = []

        for col in required:

            if col not in df.columns:

                missing.append(col)

        if missing:

            raise ValueError(

                f"Missing required columns: {missing}"

            )

        return True

    # --------------------------------------------------
    # Clean Dataset
    # --------------------------------------------------

    def clean_dataset(self, df):

        df = self.normalize_columns(df)

        df = self.remove_empty_rows(df)

        self.validate_columns(df)

        df = self.remove_duplicates(df)

        return df
    # --------------------------------------------------
    # Load, Merge and Clean
    # --------------------------------------------------

    def load_and_clean(self, company):

        df = self.merge_company_datasets(company)

        if df.empty:

            return df

        df = self.clean_dataset(df)

        return df

    # --------------------------------------------------
    # Export Clean Dataset
    # --------------------------------------------------

    def export_clean_dataset(

        self,

        company,

        output_root="datasets/processed"

    ):

        df = self.load_and_clean(company)

        output_root = Path(output_root)

        output_root.mkdir(

            parents=True,

            exist_ok=True

        )

        company_dir = output_root / company

        company_dir.mkdir(

            parents=True,

            exist_ok=True

        )

        output_file = company_dir / f"{company.lower()}_clean.csv"

        df.to_csv(

            output_file,

            index=False

        )

        print(

            f"Clean dataset exported : {output_file}"

        )

        return output_file

    # --------------------------------------------------
    # Dataset Statistics
    # --------------------------------------------------

    def dataset_stats(self, df):

        stats = {

            "rows": len(df),

            "columns": len(df.columns),

            "column_names": list(df.columns)

        }

        if "topic" in df.columns:

            stats["topics"] = (

                df["topic"]

                .value_counts()

                .to_dict()

            )

        if "difficulty" in df.columns:

            stats["difficulty"] = (

                df["difficulty"]

                .value_counts()

                .to_dict()

            )

        return stats

    # --------------------------------------------------
    # Print Statistics
    # --------------------------------------------------

    def print_stats(self, df):

        stats = self.dataset_stats(df)

        print("\n========== DATASET STATS ==========")

        print(

            f"Rows : {stats['rows']}"

        )

        print(

            f"Columns : {stats['columns']}"

        )

        print(

            f"Column Names : {stats['column_names']}"

        )

        if "topics" in stats:

            print("\nTopics")

            for topic, count in stats["topics"].items():

                print(

                    f"{topic} : {count}"

                )

        if "difficulty" in stats:

            print("\nDifficulty")

            for diff, count in stats["difficulty"].items():

                print(

                    f"{diff} : {count}"

                )

        print("===================================\n")

    # --------------------------------------------------
    # Health Check
    # --------------------------------------------------

    def health(self):

        print("\n========== DATASET LOADER ==========")

        print(

            f"Root Path : {self.root_path}"

        )

        print(

            f"Companies : {len(self.list_companies())}"

        )

        print("====================================\n")