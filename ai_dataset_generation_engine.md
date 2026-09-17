# CodeHiring AI Dataset Generation Engine Architecture

## Overview

This document defines the production-ready architecture for the CodeHiring AI Dataset Generation Engine. It describes modules, responsibilities, data flows, integration points, and scalability requirements. The architecture is designed to support:
- 20+ companies
- 100+ roles
- 100,000+ questions
- AI question generation
- ML training
- Adaptive mock tests
- Student analytics
- Future RAG integration

## High-Level Architecture

The engine is composed of seven core modules:
1. `company_loader.py`
2. `prompt_builder.py`
3. `ai_connector.py`
4. `validator.py`
5. `classifier.py`
6. `exporter.py`
7. `dataset_builder.py`

These components form a pipeline that loads company metadata, builds prompts, generates raw question drafts with AI, validates and classifies them, then exports approved items into structured datasets.

### Textual Architecture Diagram

```
[Company Knowledge Base]     [Question Rules & Templates]
          |                               |
          v                               v
   company_loader.py  ---> prompt_builder.py ---> ai_connector.py
          |                               |                 |
          v                               |                 v
   (metadata objects)                    |         [Generated Draft Questions]
                                          v
                                validator.py ---> classifier.py
                                          |                |
                                          v                v
                                     [Validated Questions] 
                                          |
                                          v
                                    exporter.py
                                          |
                                          v
                           [CSV / JSON / MongoDB Output]
                                          |
                                          v
                                  dataset_builder.py
                                          |
                                          v
                  [Batch orchestration, monitoring, ML logging]
```

## Module Responsibilities

### 1. `company_loader.py`

Purpose: Load and normalize all company-specific knowledge base artifacts required for generation.

Responsibilities:
- Load `company_profile.json` for company/role metadata.
- Load `company_pattern.csv` and topic files (`aptitude_topics.csv`, `logical_topics.csv`, `verbal_topics.csv`, `coding_topics.csv`).
- Load global prompt rules and templates if company-specific overrides exist.
- Normalize data into in-memory models with stable identifiers:
  - company_id, role_id, section_id, topic_id, difficulty_id.
- Validate source file integrity and schema consistency.
- Provide query APIs for:
  - company profiles by company/role
  - topic lists by section and difficulty
  - pattern distributions by round and section
- Implement caching to avoid repeated IO.
- Support loading from multiple dataset sources (local files, shared storage, database bridges).

Why:
- Centralizes company knowledge loading and ensures the rest of the engine receives consistent structured metadata.
- Enables the prompt builder and dataset builder to operate on normalized, queryable objects.

### 2. `prompt_builder.py`

Purpose: Build AI prompts automatically by combining company-specific rules, templates, topic taxonomy, and difficulty constraints.

Responsibilities:
- Accept normalized company profile, topic metadata, difficulty profile, and generation rules.
- Generate prompt payloads that include:
  - company-specific style and expected difficulty
  - topic and subtopic focus
  - learning objective and Bloom level mapping
  - answer format expectations
  - validation requirements
  - constraints for real-world scenario style
- Use `topic_templates.json` to build reusable prompt templates.
- Merge `company_prompt_templates.json` style guidelines for company adaptation.
- Support dynamic prompt composition for:
  - MCQ generation
  - numerical reasoning
  - coding question scaffolding
  - verbal comprehension prompts
- Include metadata fields in the prompt object for later tracking:
  - source_company
  - target_role
  - section
  - topic_id
  - difficulty
  - bloom_level
  - expected_time
  - learning_objective
- Allow prompt variants for batch generation and randomization.
- Export both text prompt and structured prompt metadata.

Why:
- Ensures AI receives consistent, high-quality generation instructions aligned to company and topic requirements.
- Enables reproducible prompt generation and traceability for each generated item.

### 3. `ai_connector.py`

Purpose: Interface with the AI backend to submit prompts, retrieve generated responses, and handle provider-level concerns.

Responsibilities:
- Provide a pluggable connector architecture for multiple AI providers.
- Send prompt payloads in batches or individually.
- Handle API-specific rate limits, backoff strategies, retries, and quota usage.
- Detect and recover from transient failures, timeouts, or throttling.
- Validate response structure and deliver raw AI output to downstream components.
- Log request/response metadata for audit and debugging:
  - prompt_id
  - provider_name
  - tokens_used
  - status_code
  - error_type
  - latency
- Support safe prompt replay with consistent prompts.
- Enforce provider-specific content policies if needed.
- Optionally store raw AI outputs in a staging area for RAG and review.

Why:
- Abstracts the AI service layer and provides robust, production-grade handling of external dependencies.
- Enables scaling across large generation volumes with systematic retry and rate-limit management.

### 4. `validator.py`

Purpose: Validate every generated question draft according to grammar, duplication, correctness, topic, and difficulty rules.

Responsibilities:
- Implement validation pipelines using the rule sets from `validation_rules.json`, `question_generation_rules.json`, and `difficulty_rules.json`.
- Validate grammar and readability using NLP grammar checks.
- Detect duplicates and near-duplicates against existing question banks and current batch.
- Validate answer correctness logically and mathematically.
- Check topic consistency by verifying that prompt metadata and generated content align.
- Check difficulty consistency by comparing structure, step count, and reasoning demand to declared difficulty.
- Provide pass/fail status and error categories for each draft.
- Support partial scoring or quality scoring for review thresholds.
- Emit structured validation reports:
  - grammarScore
  - duplicateScore
  - correctnessScore
  - topicMatchScore
  - difficultyMatchScore
  - overallQualityScore
- Support manual override or review queue integration for uncertain cases.
- Use data versioning to store validation history and improvement feedback.

Why:
- Ensures only high-quality question drafts progress to classification and export.
- Protects the platform from poor AI output and supports continuous improvement. 

### 5. `classifier.py`

Purpose: Automatically classify validated generated questions along key educational dimensions.

Responsibilities:
- Assign canonical `Topic` and `Subtopic` based on content and prompt metadata.
- Assign `Difficulty` using a combination of prompt metadata, validation scores, and trained models.
- Assign `Bloom Level` based on question complexity, verb usage, and inferred cognitive demand.
- Estimate solving time based on topic, difficulty, option count, complexity, and historical data.
- Produce classification metadata fields:
  - topic_id
  - subtopic
  - difficulty_id
  - bloom_level
  - estimated_time_seconds
  - learning_objective
  - question_type
- Use rule-based mapping for deterministic classification when possible.
- Incorporate ML models for classification when scaling to 100k+ questions.
- Support calibration using historical student analytics and performance data.
- Emit classification confidence scores and labeling rationale.

Why:
- Provides normalized labels required for indexing, adaptive engines, and analytics.
- Enables consistent topic/difficulty assignment across generated content.

### 6. `exporter.py`

Purpose: Save validated and classified questions into structured dataset formats for downstream usage.

Responsibilities:
- Export questions into CSV with column schemas matching dataset architecture.
- Export JSON for flexible consumption by AI, ML, and RAG systems.
- Export MongoDB-ready documents for ingestion into document stores.
- Support both normalized and denormalized export forms:
  - normalized: question metadata + classification identifiers
  - denormalized: full question text, options, explanation, and company labels
- Validate export schema compliance before writing files.
- Support incremental exports and batch appends.
- Track export metadata and file versions.
- Support multiple storage targets:
  - local filesystem
  - shared network storage
  - cloud blob storage
  - database import staging directories
- Provide hooks for export-level metadata enrichment such as:
  - generation_date
  - provider_name
  - validation_results
  - classification_confidence

Why:
- Ensures generated items are persisted in machine-readable formats suitable for training, testing, and production consumption.
- Makes the dataset usable by analytics pipelines and adaptive engines.

### 7. `dataset_builder.py`

Purpose: Orchestrate the end-to-end generation pipeline and manage large-scale dataset creation.

Responsibilities:
- Control generation workflows for companies, roles, and topic segments.
- Create batches of prompt generation tasks using `company_loader` and `prompt_builder`.
- Submit prompts to `ai_connector` and route AI drafts to `validator` and `classifier`.
- Implement concurrency and batching strategies for scale.
- Manage retry policies, failure handling, and backpressure.
- Maintain progress tracking and observability:
  - total prompts generated
  - validation pass rate
  - export counts
  - throughput per hour
- Support both full pipeline runs and incremental refresh runs.
- Enable generation modes:
  - exploratory draft generation
  - production-ready dataset creation
  - targeted role/topic augmentation
- Integrate logging and metrics for ML and analytics feedback.
- Emit pipeline artifacts for RAG integration:
  - prompt history
  - AI response metadata
  - validation reports
- Manage seed and randomization state for reproducibility.
- Coordinate with `exporter` to persist validated datasets.
- Support dynamic scaling strategies such as prioritizing high-demand companies, roles, or topics.
- Provide configuration options for:
  - question volume targets
  - difficulty mixes
  - company-specific style adherence
  - use of updated prompt templates or rules

Why:
- Creates a single orchestration layer that can manage production dataset generation end-to-end.
- Enables the platform to generate thousands of questions reliably and consistently.

## Data Flow and Integration

### Pipeline Flow

1. `company_loader.py` reads the knowledge base and produces normalized company/topic metadata.
2. `dataset_builder.py` requests prompt batches from `prompt_builder.py`.
3. `prompt_builder.py` constructs AI prompts using the loaded metadata and rule templates.
4. `ai_connector.py` sends prompts to the AI provider and returns raw generated drafts.
5. `validator.py` applies quality checks, filters invalid output, and tags issues.
6. `classifier.py` labels successful drafts with topic, difficulty, Bloom level, and time.
7. `exporter.py` writes the approved questions to persistent outputs.
8. `dataset_builder.py` logs metrics and controls iterative scaling.

### Data Products

- Raw prompts and prompt metadata
- AI-generated drafts and raw responses
- Validation reports and quality scores
- Classification labels and confidence metrics
- Exported CSV, JSON, and MongoDB-ready documents
- Pipeline telemetry for batching and throughput

## Scaling Considerations

### Performance and Parallelism

- Use batched prompt generation and asynchronous AI calls for high throughput.
- Partition generation by company, role, section, or topic to parallelize work.
- Cache loaded metadata to avoid repeated IO.
- Use a queue or task orchestration engine for large-scale production runs.

### Data Volume

- Maintain stable unique IDs across companies and questions.
- Store generation metadata separately from final exported content.
- Keep raw AI outputs in a staging layer for audit and retraining.

### Reproducibility

- Seed randomization for prompt variants.
- Version rules, templates, and difficulty profiles.
- Persist prompt definitions and generation parameters.

### RAG Integration

- Preserve prompt text, AI output, validation results, and classification metadata.
- Store these artifacts in JSON forms suitable for retrieval augmentation.
- Tag generated items with provenance metadata.

### ML Training and Analytics

- Save validation feature vectors and quality scores.
- Export classification labels for supervised model training.
- Record question metadata for adaptive mock test sequencing.
- Track performance signals and difficulty calibration metrics.

## Module Interfaces and Collaboration

### `company_loader.py` interface
- `load_company_profile(company_slug, role_slug)`
- `load_company_patterns(company_slug, role_slug)`
- `load_topic_taxonomy(section)`
- `list_available_companies()`

### `prompt_builder.py` interface
- `build_prompt(context)`
- `build_batch_prompts(company_id, role_id, section_id, topic_id, difficulty, count)`

### `ai_connector.py` interface
- `generate(prompt)`
- `generate_batch(prompts)`
- `health_check()`
- `provider_status()`

### `validator.py` interface
- `validate_question(draft)`
- `validate_batch(drafts)`
- `get_validation_report(draft_id)`

### `classifier.py` interface
- `classify_question(validated_item)`
- `predict_metadata(text)`
- `calibrate_model(training_data)`

### `exporter.py` interface
- `export_csv(items, destination)`
- `export_json(items, destination)`
- `export_mongodb(items, connection_string, collection)`
- `export_batch(items, config)`

### `dataset_builder.py` interface
- `run_generation(config)`
- `generate_for_company(company_slug, role_slug, target_count)`
- `resume_pipeline(run_id)`
- `report_progress()`

## Production Readiness Features

- Schema validation for all inputs and outputs
- Fault-tolerant retry handling in AI connector
- Comprehensive logging and auditability
- Rule-driven validation and classification
- Modular design for company-specific adaptation
- Export formats aligned with dataset architecture
- Support for future storage and retrieval systems

## Recommended Output Structure

- `company_loader.py` — metadata ingestion and normalization
- `prompt_builder.py` — AI prompt composition
- `ai_connector.py` — provider integration and reliability
- `validator.py` — quality filtering and rule enforcement
- `classifier.py` — label assignment and metadata enrichment
- `exporter.py` — dataset persistence and format conversion
- `dataset_builder.py` — pipeline orchestration and scaling

## Summary

This architecture defines a production-ready AI Dataset Generation Engine for CodeHiring. It is designed to support large-scale question generation and dataset creation while preserving data quality, company-specific style, and future extensibility for RAG, ML, and adaptive testing.
