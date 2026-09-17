from pathlib import Path

# ============================
# Project Paths
# ============================

BASE_DIR = Path(__file__).resolve().parent

KNOWLEDGE_DIR = BASE_DIR / "knowledge"

DATASET_DIR = BASE_DIR / "dataset"

OUTPUT_DIR = BASE_DIR / "output"

LOG_DIR = BASE_DIR / "logs"

ENGINE_DIR = BASE_DIR / "engine"

# ============================
# Company
# ============================

COMPANY = "Amazon"

ROLE = "SDE"

# ============================
# Generation
# ============================

QUESTIONS_PER_BATCH = 20

MAX_RETRIES = 3

MODEL_NAME = "gemini"

# ============================
# Output
# ============================

OUTPUT_FILE = OUTPUT_DIR / "amazon_aptitude.csv"