"""
main.py  -  CodeHiring Dataset Engine
======================================
Generates questions per topic per company across all 128 companies.
Uses BATCH generation: 5 questions per LLM call for efficiency.
Fully resumable: skips topics already at target count.

Usage:
    python main.py                                   # all companies
    python main.py --company TCS                     # one company
    python main.py --company TCS --section verbal    # one section
    python main.py --company TCS --topic Percentages # one topic
    python main.py --target 10000                    # custom per-company target
"""

import argparse
import logging
import os
import sys

import pandas as pd

from engine.batch_engine import BatchEngine
from engine.company_loader import CompanyLoader
from engine.dataset_builder import DatasetBuilder
from engine.exporter import Exporter
from engine.generator import Generator
from engine.prompt_builder import PromptBuilder
from engine.reviewer import Reviewer
from engine.validator import Validator

# ======================================================
# CONFIGURATION
# ======================================================

DEFAULT_TARGET_PER_TOPIC = 500   # questions per topic per company

ALL_COMPANIES = [
    # IT Services (23)
    "TCS", "Infosys", "Wipro", "Cognizant", "Capgemini",
    "Accenture", "HCL Technologies", "Tech Mahindra", "Mphasis",
    "Hexaware", "LTIMindtree", "Zensar", "Persistent Systems",
    "Cyient", "Birlasoft", "Sonata Software", "Tata Elxsi",
    "Nisum", "Xoriant", "Mastech Digital", "3i Infotech",
    "Info Edge", "NIIT Technologies",
    # Product (23)
    "Amazon", "Microsoft", "Google", "Meta", "Apple",
    "Adobe", "Oracle", "Atlassian", "Salesforce", "Qualcomm",
    "NVIDIA", "Intel", "Intuit", "Cisco", "Samsung RnD",
    "Palo Alto Networks", "ServiceNow", "LinkedIn", "Uber",
    "Stripe", "Snowflake", "Databricks", "ThoughtWorks",
    # Startups (24)
    "Flipkart", "Swiggy", "Zomato", "Paytm", "PhonePe",
    "Razorpay", "Groww", "Meesho", "Myntra", "Ola",
    "Freshworks", "Zoho", "BrowserStack", "Dream11", "CRED",
    "Zepto", "BYJUS", "Unacademy", "MakeMyTrip", "ShareChat",
    "Zerodha", "Postman", "Urban Company", "ClearTax",
    # Consulting (15)
    "Deloitte", "PwC", "KPMG", "EY", "McKinsey",
    "BCG", "Bain", "Oliver Wyman", "Genpact",
    "Fractal Analytics", "Mu Sigma", "Tiger Analytics",
    "LatentView", "WNS", "EXL",
    # BFSI (15)
    "JP Morgan", "Goldman Sachs", "Morgan Stanley", "Deutsche Bank",
    "Barclays", "HSBC", "Citi", "Nomura", "American Express",
    "Mastercard", "Visa", "ICICI", "HDFC", "Axis", "SBI",
    # Core Engineering (18)
    "Tata Motors", "LnT", "BHEL", "ONGC", "NTPC",
    "IOCL", "GAIL", "BPCL", "Maruti Suzuki", "Mahindra",
    "Bosch", "Siemens", "Honeywell", "GE Digital", "Caterpillar",
    "Cummins", "Hero MotoCorp", "Bajaj Auto",
    # Telecom (5)
    "Ericsson", "Nokia", "Airtel", "Jio", "BSNL",
    # FMCG (5)
    "HUL", "Nestle", "ITC", "PnG", "Marico",
]

SECTIONS = [
    ("Quantitative Aptitude", "aptitude"),
    ("Logical Reasoning",     "logical"),
    ("Verbal Ability",        "verbal"),
]

# ======================================================
# LOGGING
# ======================================================

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/generation.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

# ======================================================
# HELPERS
# ======================================================

def count_existing(exporter: Exporter, section_name: str, topic: str) -> int:
    """Count accepted questions already on disk for this topic."""
    filename = exporter.get_filename(section_name)
    filepath = os.path.join(exporter.output_root, filename)
    if not os.path.exists(filepath):
        return 0
    try:
        df = pd.read_csv(filepath)
        return int((df.get("Topic", pd.Series(dtype=str)) == topic).sum())
    except Exception:
        return 0


def build_external_sample(company: str) -> str:
    """Load up to 3 example questions from external dataset for style reference."""
    paths = [
        f"datasets/external/{company}/{company.lower()}_aptitude.csv",
        f"datasets/external/{company}/{company.lower()}_oa.csv",
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                if "question" in df.columns or "Question" in df.columns:
                    col = "question" if "question" in df.columns else "Question"
                    sample = df[col].dropna().head(3).tolist()
                    return "\n".join(f"- {q}" for q in sample)
            except Exception:
                pass
    return "None"


def build_pattern_summary(data: dict) -> str:
    """Build a short company pattern summary for the batch prompt."""
    profile = data.get("profile", {})
    pattern = data.get("pattern", {})
    lines = [
        f"Industry: {profile.get('industry', 'N/A')}",
        f"Overall Difficulty: {profile.get('overall_difficulty', 'N/A')}",
        f"Question Style: {pattern.get('question_style', 'N/A')}",
        f"Calculator: {pattern.get('calculator_allowed', False)}",
        f"Real World Context: {pattern.get('real_world_context', True)}",
    ]
    return " | ".join(lines)


def log_progress(company: str, section: str, topic: str, saved: int, target: int):
    with open("logs/progress.log", "a", encoding="utf-8") as f:
        f.write(f"{company} | {section} | {topic} | {saved}/{target}\n")

# ======================================================
# SECTION RUNNER
# ======================================================

def run_section(
    company: str,
    section_name: str,
    topics_df,
    target_per_topic: int,
    builder: PromptBuilder,
    batch_engine: BatchEngine,
    exporter: Exporter,
    external_sample: str,
    pattern_summary: str,
    topic_filter: str | None = None,
) -> int:

    if topics_df is None or len(topics_df) == 0:
        log.warning(f"  No topics for section: {section_name}")
        return 0

    # Build topic list, apply filter
    topics_with_difficulty = []
    for _, row in topics_df.iterrows():
        topic = row["topic"]
        if topic_filter and topic_filter.lower() not in topic.lower():
            continue
        topics_with_difficulty.append({
            "topic":      topic,
            "difficulty": row["difficulty"],
        })

    if not topics_with_difficulty:
        return 0

    # Log section plan
    log.info(f"\n  Section: {section_name} | {len(topics_with_difficulty)} topics | target={target_per_topic}/topic")
    for t in topics_with_difficulty:
        existing = count_existing(exporter, section_name, t["topic"])
        log.info(f"    {t['topic']:35} {t['difficulty']:12} existing={existing}/{target_per_topic}")

    saved = batch_engine.run_until_complete(
        company=company,
        section_name=section_name,
        topics_with_difficulty=topics_with_difficulty,
        target_per_topic=target_per_topic,
        builder=builder,
        exporter=exporter,
        count_fn=count_existing,
        external_sample=external_sample,
        company_pattern_summary=pattern_summary,
    )

    return saved

# ======================================================
# COMPANY RUNNER
# ======================================================

def run_company(
    company: str,
    batch_engine: BatchEngine,
    target_per_topic: int,
    section_filter: str | None = None,
    topic_filter:   str | None = None,
) -> int:

    print("\n" + "=" * 70)
    print(f"  COMPANY: {company}")
    print("=" * 70)

    knowledge_path = f"knowledge/{company}"
    if not os.path.exists(knowledge_path):
        log.error(f"Knowledge missing: {knowledge_path} - run: python knowledge_seeder.py")
        return 0

    try:
        loader = CompanyLoader(knowledge_path)
        data   = loader.load_all()
    except Exception as e:
        log.error(f"Failed to load {company}: {e}")
        return 0

    builder         = PromptBuilder(data["profile"], data["pattern"])
    exporter        = Exporter(company)
    external_sample = build_external_sample(company)
    pattern_summary = build_pattern_summary(data)
    grand           = 0

    for section_name, data_key in SECTIONS:
        if section_filter and section_filter.lower() not in section_name.lower():
            continue

        topics_df = data.get(data_key)

        try:
            saved = run_section(
                company=company,
                section_name=section_name,
                topics_df=topics_df,
                target_per_topic=target_per_topic,
                builder=builder,
                batch_engine=batch_engine,
                exporter=exporter,
                external_sample=external_sample,
                pattern_summary=pattern_summary,
                topic_filter=topic_filter,
            )
            grand += saved
        except KeyboardInterrupt:
            raise
        except Exception as e:
            log.error(f"Section error [{section_name}]: {e}")
            continue

    print(f"\n  Done: {company} | saved this run: {grand}")
    return grand

# ======================================================
# MAIN
# ======================================================

def main():
    parser = argparse.ArgumentParser(description="CodeHiring Dataset Engine")
    parser.add_argument("--company",  type=str,  default=None,
                        help="Single company (default: all)")
    parser.add_argument("--section",  type=str,  default=None,
                        help="Section filter: quantitative / logical / verbal")
    parser.add_argument("--topic",    type=str,  default=None,
                        help="Topic filter (partial match)")
    parser.add_argument("--target",   type=int,  default=DEFAULT_TARGET_PER_TOPIC,
                        help=f"Questions per topic (default: {DEFAULT_TARGET_PER_TOPIC})")
    parser.add_argument("--mock",     action="store_true",
                        help="Run in mock/offline mode for testing without an API key")
    args = parser.parse_args()

    companies = [args.company] if args.company else ALL_COMPANIES

    is_mock = args.mock or not os.getenv("GROQ_API_KEY")
    if not os.getenv("GROQ_API_KEY") and not args.mock:
        print("\n[INFO] GROQ_API_KEY not detected in .env or environment.")
        print("Running in test mode (mock LLM).")
        print("To generate real questions, add GROQ_API_KEY to your .env file.\n")
        is_mock = True

    print("\n" + "=" * 70)
    print(f"  CODEHIRING AI DATASET ENGINE  [{'MOCK MODE' if is_mock else 'LIVE BATCH MODE'}]")
    print(f"  Companies      : {len(companies)}")
    print(f"  Per topic      : {args.target} questions")
    print(f"  Section filter : {args.section or 'All'}")
    print(f"  Topic filter   : {args.topic or 'All'}")
    print("=" * 70)

    generator    = Generator(mock=is_mock)
    validator    = Validator()
    reviewer     = Reviewer(generator=generator)
    batch_engine = BatchEngine(generator, validator, reviewer)

    grand_total = 0

    for company in companies:
        try:
            saved = run_company(
                company=company,
                batch_engine=batch_engine,
                target_per_topic=args.target,
                section_filter=args.section,
                topic_filter=args.topic,
            )
            grand_total += saved
        except KeyboardInterrupt:
            print("\n\nInterrupted. Progress is saved — resume anytime with python main.py")
            break
        except Exception as e:
            log.error(f"Company error [{company}]: {e}")
            continue

    print("\n" + "=" * 70)
    print("  GENERATION COMPLETE")
    print(f"  Total questions saved : {grand_total}")
    print("=" * 70)

    generator.print_stats()
    validator.print_stats()
    reviewer.print_stats()


if __name__ == "__main__":
    main()
