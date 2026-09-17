# CodeHiring Dataset Engine Design

## 1. Project Folder Structure

```
CodeHiring-ML/
├── company_loader.py
├── prompt_builder.py
├── ai_connector.py
├── validator.py
├── classifier.py
├── exporter.py
├── dataset_builder.py
├── config.py
├── models/
│   ├── company.py
│   ├── prompt.py
│   ├── question.py
│   ├── validation.py
│   ├── classification.py
│   └── export.py
├── data/
│   ├── companies/
│   ├── global/
│   └── staging/
├── rules/
│   ├── company_prompt_templates.json
│   ├── difficulty_rules.json
│   ├── question_generation_rules.json
│   ├── validation_rules.json
│   └── topic_templates.json
├── tests/
│   ├── test_company_loader.py
│   ├── test_prompt_builder.py
│   ├── test_ai_connector.py
│   ├── test_validator.py
│   ├── test_classifier.py
│   ├── test_exporter.py
│   └── test_dataset_builder.py
├── docs/
│   ├── ai_dataset_generation_engine.md
│   ├── dataset_architecture.md
│   └── dataset_engine_design.md
└── README.md
```

## 2. Module Responsibilities

### `config.py`
- Central configuration registry for the engine.
- Stores project paths, API keys, AI model settings, retry and rate-limit policy, validation thresholds, export settings, and logging configuration.
- Provides typed configuration objects accessible by all modules.

### `company_loader.py`
- Loads company and role data files.
- Validates schemas and handles missing files.
- Returns typed domain objects for company profiles, pattern metadata, and topic taxonomy.
- Converts raw CSV/JSON into `pydantic` or dataclass models.

### `prompt_builder.py`
- Builds prompts automatically from company, role, topic, difficulty, and rule inputs.
- Produces production-ready AI prompts and structured metadata.
- Applies company style adaptation and template parameters.

### `ai_connector.py`
- Interfaces with external AI providers.
- Supports OpenAI, Gemini, Claude, DeepSeek with provider abstraction.
- Handles retries, rate limiting, streaming, token management, and JSON validation.

### `validator.py`
- Validates generated drafts across grammar, duplicates, correctness, difficulty, topic, explanation, estimated time, and cognitive level.
- Uses rule-driven scoring and structured validation reports.

### `classifier.py`
- Classifies validated questions into topic, subtopic, difficulty, question type, Bloom level, and learning objective.
- Uses deterministic rules and ML-ready model hooks.

### `exporter.py`
- Persists validated questions to CSV, JSON, and MongoDB document formats.
- Supports export schema validation and metadata inclusion.

### `dataset_builder.py`
- Orchestrates the full pipeline.
- Drives load, prompt generation, AI call, validation, classification, and export.
- Supports batch generation, progress tracking, and pipeline recovery.

## 3. Class Diagram

### Core classes
- `Config` (`config.py`)
- `CompanyLoader` (`company_loader.py`)
- `PromptBuilder` (`prompt_builder.py`)
- `AIConnector` (`ai_connector.py`)
- `Validator` (`validator.py`)
- `Classifier` (`classifier.py`)
- `Exporter` (`exporter.py`)
- `DatasetBuilder` (`dataset_builder.py`)

### Data models
- `CompanyProfile`
- `CompanyPattern`
- `TopicDefinition`
- `PromptRequest`
- `PromptResponse`
- `QuestionDraft`
- `ValidationResult`
- `QuestionClassification`
- `ExportRecord`

### Dependencies
- `DatasetBuilder` depends on `CompanyLoader`, `PromptBuilder`, `AIConnector`, `Validator`, `Classifier`, `Exporter`, `Config`
- `PromptBuilder` depends on `CompanyProfile`, topic metadata, and rule templates
- `AIConnector` depends on provider config and response validator
- `Validator` depends on generation and validation rules
- `Classifier` depends on question metadata and classification rules
- `Exporter` depends on export schema and storage config

## 4. Sequence Diagram

### Full generation flow
1. `DatasetBuilder` loads `Config`.
2. `DatasetBuilder` calls `CompanyLoader.load_company(company, role)`.
3. `CompanyLoader` loads and validates company profile, patterns, and topics.
4. `DatasetBuilder` calls `PromptBuilder.build_prompt(...)`.
5. `PromptBuilder` constructs AI input using templates and rules.
6. `DatasetBuilder` sends prompt to `AIConnector.generate(prompt)`.
7. `AIConnector` submits request to provider and returns raw draft.
8. `DatasetBuilder` sends draft to `Validator.validate(draft)`.
9. `Validator` returns validation result.
10. If valid, `DatasetBuilder` sends draft to `Classifier.classify(draft)`.
11. `Classifier` returns classification metadata.
12. `DatasetBuilder` sends final item to `Exporter.export(item)`.
13. `Exporter` persists the item in CSV/JSON/MongoDB-ready form.

## 5. Design Patterns Used

- Dependency Injection: modules receive dependencies through constructors.
- Factory Pattern: create AI provider clients and configuration objects.
- Strategy Pattern: validation and classification strategies can be swapped.
- Adapter Pattern: AI provider adapters normalize API interaction.
- Template Method: prompt building pipeline structure.
- Repository Pattern: export persistence abstraction.

## 6. File-by-file Implementation Plan

### `config.py`
- Implement `Config` loader from YAML/JSON environment files.
- Define typed config models: `PathsConfig`, `AIConfig`, `RetryConfig`, `ValidationConfig`, `ExportConfig`, `LoggingConfig`.
- Add helper methods for environment overrides.

### `company_loader.py`
- Implement `CompanyLoader` with `load_company_profile`, `load_company_pattern`, `load_topic_files`.
- Use `pydantic` models for schema validation.
- Add file existence and schema validation logic.

### `prompt_builder.py`
- Implement `PromptBuilder` with `build_prompt` and `build_batch_prompts`.
- Load templates from JSON and merge with company style rules.
- Create `PromptRequest` dataclass.

### `ai_connector.py`
- Implement provider base class and adapters for OpenAI/Gemini/Claude/DeepSeek.
- Add retry and rate limiter using token bucket or backoff.
- Implement JSON schema validation for provider output.

### `validator.py`
- Implement `Validator` with rule engine.
- Define `ValidationResult` and scoring metrics.
- Add duplicate detection and grammar validation hooks.

### `classifier.py`
- Implement `Classifier` with classification methods.
- Add rule-based mappings and ML model integration points.
- Expose `classify_question`.

### `exporter.py`
- Implement CSV, JSON, and MongoDB export methods.
- Add schema validation, metadata stamping, and file writing.

### `dataset_builder.py`
- Implement pipeline orchestration, batch management, and progress logging.
- Add retry/resume behavior and error handling.
- Expose CLI or runner method.

## 7. Best Practices

- Use typed models for all domain entities.
- Keep modules small and single-responsibility.
- Use dependency injection for testability.
- Log structured events, not plain strings.
- Fail fast on schema or config errors.
- Use config files and environment variables for deploy flexibility.
- Keep AI prompt composition separate from provider integration.
- Store raw prompt and response artifacts for RAG provenance.
- Use incremental exports and checkpointing for large runs.

## 8. Coding Standards

- Follow PEP 8 for formatting.
- Use `typing` and `pydantic` for strong typing.
- Use `dataclasses` or `pydantic.BaseModel` for domain objects.
- Prefer composition over inheritance for module collaboration.
- Use Python logging with named loggers: `codehiring.company_loader`, `codehiring.prompt_builder`, etc.
- Use exceptions for validation and loading failures.
- Document public classes and methods with docstrings.
- Keep module-level functions minimal.
- Use consistent naming: `load_*`, `build_*`, `validate_*`, `classify_*`, `export_*`.

---

## Next Step

Ready to implement the first module: `config.py`.
Please approve and I will generate the production-ready `config.py` module.