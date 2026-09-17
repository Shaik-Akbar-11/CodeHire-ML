# CodeHire-ML

> **CodeHiring AI Dataset Generation Engine & ML Pipeline**  
> An automated dataset generation and machine learning pipeline for company-specific hiring assessments, technical interview prep, and aptitude question generation across 128+ companies.

---

## 🚀 Features

- **Multi-Company Coverage**: Knowledge base covering 128+ tech and enterprise companies (IT Services, Product, Startups, BFSI, Consulting, Core Engineering, Telecom, and FMCG).
- **Multi-Section Assessments**:
  - Quantitative Aptitude
  - Logical Reasoning
  - Verbal Ability
  - Technical / Coding Assessments
- **AI-Powered Generation & Review**:
  - Batch generation via Groq LLM API (`llama-3.3-70b-versatile`).
  - Strict multi-step validation and programmatic verification.
  - Dedicated Reviewer scoring and quality auditing (`audit.py`).
- **Resumable Execution**: Automatically tracks existing questions per topic and resumes without duplicates.

---

## 🛠 Project Structure

```
CodeHire-ML/
├── datasets/                     # External and generated reference datasets
├── engine/                       # Core generation and validation engine
│   ├── batch_engine.py           # Single/batch question generation runner
│   ├── company_loader.py         # Company knowledge loader
│   ├── dataset_builder.py        # Dataset structuring and assembly
│   ├── exporter.py               # Exporter for CSV and JSON outputs
│   ├── generator.py              # LLM client and prompt completion
│   ├── prompt_builder.py         # Dynamic prompt construction
│   ├── reviewer.py               # Strict assessment question reviewer
│   └── validator.py              # Rule-based question schema validation
├── knowledge/                    # 128+ company-specific knowledge profiles & patterns
├── logs/                         # Execution and audit logs
├── output/                       # Generated assessment datasets
├── .env.example                  # Environment configuration template
├── audit.py                      # Question quality auditing tool
├── config.py                     # Global engine configuration
├── knowledge_seeder.py           # Seeds company patterns & question templates
├── main.py                       # Main generation CLI entry point
├── requirements.txt              # Project dependencies
└── train.py                      # ML training script
```

---

## ⚙️ Setup & Installation

### 1. Install Dependencies
Ensure you have Python 3.10+ installed:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` and configure your API key:

```bash
cp .env.example .env
```

Edit `.env`:
```ini
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🎯 Usage

### 1. Seed Company Knowledge
Generate knowledge patterns and topic configurations for all 128 companies:

```bash
python knowledge_seeder.py
```

### 2. Generate Datasets

- **Generate questions for all companies**:
  ```bash
  python main.py
  ```

- **Generate for a specific company**:
  ```bash
  python main.py --company TCS
  ```

- **Generate for a specific section or topic**:
  ```bash
  python main.py --company Amazon --section quantitative
  python main.py --company Google --topic "Dynamic Programming"
  ```

- **Set a custom target count per topic**:
  ```bash
  python main.py --company Microsoft --target 100
  ```

### 3. Audit and Quality Review
Run the automated reviewer over generated datasets to filter low-quality questions:

```bash
python audit.py
```

---

## 📄 License
This project is licensed under the MIT License.
