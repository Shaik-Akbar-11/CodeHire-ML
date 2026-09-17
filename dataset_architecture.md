# CodeHiring Dataset Architecture

## 1. Folder Structure for Company-wise Dataset Storage

Root folder: `datasets/`

Structure:

- `datasets/companies/`
  - `<company_slug>/`
    - `metadata/`
      - `company_pattern.csv`
      - `topic_taxonomy.csv`
      - `section_definitions.csv`
      - `difficulty_levels.csv`
    - `roles/`
      - `<role_slug>/`
        - `company_pattern.csv`
        - `questions/`
          - `aptitude.csv`
          - `logical_reasoning.csv`
          - `verbal_ability.csv`
          - `coding.csv`
          - `interview_questions.csv`
        - `question_metadata.csv`
        - `student_performance.csv`
- `datasets/global/`
  - `companies.csv`
  - `roles.csv`
  - `questions.csv`
  - `question_metadata.csv`
  - `student_performance.csv`
  - `company_pattern.csv`
  - `topic_taxonomy.csv`
  - `section_definitions.csv`

Notes:
- Company directories isolate company-specific assessment structures.
- Role directories isolate role-level patterns and question banks.
- `datasets/global/` stores normalized master data for platform-wide ML and AI.

## 2. CSV Files Required

### Company-level and Global Metadata

1. `companies.csv`
2. `roles.csv`
3. `topic_taxonomy.csv`
4. `section_definitions.csv`
5. `difficulty_levels.csv`
6. `company_pattern.csv`

### Question Banks by Category

7. `aptitude.csv`
8. `logical_reasoning.csv`
9. `verbal_ability.csv`
10. `coding.csv`
11. `interview_questions.csv`

### AI / Metadata / Student Performance

12. `question_metadata.csv`
13. `student_performance.csv`

## 3. Full CSV Column Designs and Explanations

### 3.1 `companies.csv`
Columns:
- `company_id` (string, UUID or stable slug): unique company identifier.
- `company_name` (string): official company name.
- `company_slug` (string): normalized folder-safe key.
- `industry` (string): tech, consulting, finance, etc.
- `headquarters_country` (string): geographic region for pattern analysis.
- `status` (string): active / archived.
- `created_at` (datetime): record creation timestamp.
- `updated_at` (datetime): last metadata update.

Why:
- Ensures all datasets can reference a stable company entity.
- Enables platform-wide aggregation by company, industry, region, and change tracking.

### 3.2 `roles.csv`
Columns:
- `role_id` (string): unique role identifier.
- `company_id` (string): references `companies.company_id`.
- `role_name` (string): job title.
- `role_level` (string): intern, fresher, entry, experienced, manager.
- `role_category` (string): engineering, product, data, support.
- `primary_skills` (string): comma-separated skill set tags.
- `secondary_skills` (string): comma-separated tags.
- `status` (string): active / retired.
- `created_at` (datetime)`
- `updated_at` (datetime)

Why:
- Normalizes roles across companies.
- Supports filtering and ML models by job level, skill clusters, and active requirements.

### 3.3 `section_definitions.csv`
Columns:
- `section_id` (string): unique section identifier.
- `section_name` (string): 'Aptitude', 'Logical Reasoning', 'Verbal Ability', 'Coding', 'Interview Questions'.
- `section_order` (integer): ordering in a test flow.
- `description` (string): short definition.
- `allowed_question_types` (string): MCQ, coding, subjective, diagram.
- `created_at` (datetime)
- `updated_at` (datetime)

Why:
- Guarantees consistent section naming and helps AI route question generation correctly.

### 3.4 `topic_taxonomy.csv`
Columns:
- `topic_id` (string): unique topic identifier.
- `section_id` (string): reference to `section_definitions.section_id`.
- `topic_name` (string): e.g. 'Probability', 'Graph Theory', 'Reading Comprehension', 'Array Manipulation'.
- `topic_family` (string): broader bucket, e.g. 'Math', 'Data Structures', 'English Grammar'.
- `topic_level` (string): core / advanced / specialized.
- `tags` (string): comma-separated tags for search and AI.
- `created_at` (datetime)
- `updated_at` (datetime)

Why:
- Provides a taxonomy for company patterns, question bank classification, and AI generation prompts.

### 3.5 `difficulty_levels.csv`
Columns:
- `difficulty_id` (string): stable difficulty key.
- `difficulty_name` (string): Easy, Medium, Hard, Very Hard.
- `difficulty_score` (integer): normalized numeric difficulty (e.g. 1-4).
- `description` (string): clarifies grading policy.
- `created_at` (datetime)
- `updated_at` (datetime)

Why:
- Standardizes difficulty mapping across companies and supports ML difficulty modeling.

### 3.6 `company_pattern.csv`
Columns:
- `pattern_id` (string): unique pattern row identifier.
- `company_id` (string): references `companies.company_id`.
- `role_id` (string): references `roles.role_id`.
- `hiring_round` (string): Round 1, Round 2, Technical Interview, HR Round.
- `section_id` (string): references `section_definitions.section_id`.
- `topic_id` (string): references `topic_taxonomy.topic_id`.
- `difficulty_id` (string): references `difficulty_levels.difficulty_id`.
- `question_count` (integer): expected number of questions in that pattern element.
- `time_limit_seconds` (integer): time allocation for that section/topic grouping.
- `weightage_percent` (float): relative score weight.
- `frequency_percent` (float): how often this pattern appears in past hiring cycles.
- `pattern_notes` (string): optional notes on company-specific focus.
- `data_source` (string): internal / external / inferred.
- `created_at` (datetime)
- `updated_at` (datetime)

Why:
- Captures the exact structure expected by requirement #6.
- Enables ML learning of hiring patterns and supports adaptive mock test composition.
- Frequency and weightage support probabilistic pattern generation and effort allocation.

### 3.7 Question bank CSVs
All five category CSVs share a standard core schema.

#### Common columns for `aptitude.csv`, `logical_reasoning.csv`, `verbal_ability.csv`, `coding.csv`, `interview_questions.csv`
- `question_id` (string): unique global identifier.
- `company_id` (string): optional company-specific source reference.
- `role_id` (string): optional role-specific source reference.
- `section_id` (string): section reference from `section_definitions.csv`.
- `topic_id` (string): from `topic_taxonomy.csv`.
- `difficulty_id` (string): from `difficulty_levels.csv`.
- `question_type` (string): MCQ, single-choice, multiple-choice, fill-in-the-blank, coding, subjective, diagram.
- `question_text` (string): question prompt or statement.
- `question_data` (string): structured payload for diagrams, code templates, math notation, or JSON pointer.
- `options` (string): JSON array or CSV list of answer options when applicable.
- `correct_answer` (string): canonical answer key or expected output.
- `explanation` (string): rationale for the correct answer.
- `marks` (float): maximum marks for the question.
- `negative_marks` (float): negative scoring if applicable.
- `time_estimate_seconds` (integer): ideal solve time.
- `is_active` (boolean): active / retired question status.
- `last_used_at` (datetime): last recorded deployment in a test.
- `usage_count` (integer): how many times the question has been used.
- `source` (string): company-provided / generated / curated.
- `created_at` (datetime)
- `updated_at` (datetime)

Why common columns:
- Standardization allows unified querying, AI labeling, and analytics across categories.
- Each field supports test assembly, scoring, usage monitoring, and model training.

#### Additional category-specific columns

`aptitude.csv` and `logical_reasoning.csv` additional fields:
- `problem_style` (string): numeric, verbal, spatial, diagrammatic.
- `concept_tags` (string): comma-separated subskills like 'percentages', 'series', 'logical deduction'.

`verbal_ability.csv` additional fields:
- `language_focus` (string): grammar, vocabulary, comprehension, verbal reasoning.
- `reading_level` (string): beginner / intermediate / expert.
- `passage_id` (string): group identifier for multi-question passages.

`coding.csv` additional fields:
- `programming_language` (string): Python, Java, C++, multi-language.
- `time_complexity_expectation` (string): e.g. O(N), O(N log N).
- `space_complexity_expectation` (string): e.g. O(1), O(N).
- `starter_code` (string): code scaffold if required.
- `input_output_spec` (string): structured I/O contract.
- `test_case_count` (integer): number of evaluation cases.
- `judge_type` (string): deterministic / heuristic / human_review.
- `expected_function_signature` (string): signature or class details.

`interview_questions.csv` additional fields:
- `question_format` (string): technical, behavioral, situational, case-study.
- `competency_tag` (string): leadership, teamwork, problem-solving, culture_fit.
- `preferred_response_style` (string): STAR, narrative, bullet.
- `confidence_score` (float): optional internal estimate of candidate response difficulty.

Why category-specific fields:
- Support specialized assessment logic for each domain.
- Enable AI meta prompts and evaluation of coding/interview response expectations.

### 3.8 `question_metadata.csv`
Columns:
- `metadata_id` (string): unique metadata row identifier.
- `question_id` (string): references question banks.
- `company_id` (string): optional source reference.
- `role_id` (string): optional role reference.
- `section_id` (string)
- `topic_id` (string)
- `difficulty_id` (string)
- `cognitive_skill_level` (string): Bloom's taxonomy level: remember, understand, apply, analyze, evaluate, create.
- `skill_vector` (string): comma-separated skills / subskills.
- `learning_objective` (string): e.g. 'conceptual clarity', 'speed accuracy', 'problem decomposition'.
- `keywords` (string): search tags, NLP prompt anchors.
- `content_source` (string): book, practice set, interview archive, generated.
- `generation_method` (string): manual / curated / ai_generated / hybrid.
- `ai_ready_tags` (string): tags used for automated prompt generation.
- `semantic_embedding_id` (string): optional pointer to precomputed embedding store.
- `question_status` (string): draft, validated, reviewed, approved.
- `reviewer_id` (string): optional reviewer reference.
- `review_notes` (string)
- `created_at` (datetime)
- `updated_at` (datetime)

Why:
- Provides AI with rich metadata required for generation, retrieval, and automated quality control.
- Enables semantic search, embedding mapping, and classification by cognitive level.
- Supports automated question generation and adaptive item selection.

### 3.9 `student_performance.csv`
Columns:
- `student_id` (string): unique candidate identifier.
- `assessment_instance_id` (string): unique test attempt identifier.
- `company_id` (string): target company for this mock or actual attempt.
- `role_id` (string): target role.
- `hiring_round` (string): round being attempted.
- `section_id` (string): section or skill domain.
- `question_id` (string): reference to question.
- `attempted_at` (datetime): timestamp of attempt.
- `response` (string): candidate answer text / code / selected option.
- `is_correct` (boolean): correctness flag.
- `score` (float): points earned.
- `time_spent_seconds` (integer): time spent on the question.
- `attempt_order` (integer): order in which the student attempted questions.
- `hint_used` (boolean): whether hints were used.
- `partial_credit` (float): partial score if applicable.
- `confidence_rating` (integer): candidate self-assessment 1-5.
- `adaptive_level` (string): current difficulty tier in adaptive test.
- `session_id` (string): link to a mock test session.
- `device_type` (string): web, mobile, tablet.
- `browser` (string): optional environment data.
- `created_at` (datetime)
- `updated_at` (datetime)

Why:
- Stores fine-grained performance data for ML models, adaptive algorithms, and student analytics.
- Enables learning curve modeling, skill mastery tracking, and item response theory.
- Supports AI-driven personalization through time, correctness, and confidence features.

## 4. Separation by Dataset Category

### Aptitude
- `datasets/companies/<company>/roles/<role>/questions/aptitude.csv`
- Focus on quantitative ability, number systems, percentages, ratios, probability.
- Uses shared question schema plus `problem_style` and `concept_tags`.

### Logical Reasoning
- `datasets/companies/<company>/roles/<role>/questions/logical_reasoning.csv`
- Focus on puzzles, arrangements, inference, pattern recognition.

### Verbal Ability
- `datasets/companies/<company>/roles/<role>/questions/verbal_ability.csv`
- Focus on grammar, reading comprehension, vocabulary, verbal reasoning.

### Coding
- `datasets/companies/<company>/roles/<role>/questions/coding.csv`
- Focus on algorithm, data structure, systems, code output, debugging.

### Interview Questions
- `datasets/companies/<company>/roles/<role>/questions/interview_questions.csv`
- Focus on behavioral, technical, situational, leadership, domain discussion.

## 5. Company Pattern Dataset Design

`company_pattern.csv` stores the required fields and additional modern metadata:
- `pattern_id`
- `company_id`
- `role_id`
- `hiring_round`
- `section_id`
- `topic_id`
- `difficulty_id`
- `question_count`
- `time_limit_seconds`
- `weightage_percent`
- `frequency_percent`
- `pattern_notes`
- `data_source`
- `created_at`
- `updated_at`

This dataset is the canonical source for how each company/role structures a hiring or mock assessment.

## 6. Student Performance Dataset for Future ML Models

`student_performance.csv` is designed to capture:
- student, session, company, role, round, and section context
- per-question response and correctness
- time and order signals
- hints, partial credit, and confidence
- adaptive path metadata

This allows ML models to predict:
- question difficulty estimations
- student mastery across topics
- optimal adaptive sequencing
- company readiness scores

## 7. Question Metadata Dataset for AI

`question_metadata.csv` supports AI with:
- cognitive taxonomy
- topic and skill vectors
- generation and review provenance
- search/embedding tags
- readiness status
- content source and review notes

This dataset is essential for:
- automated question generation
- semantic retrieval
- quality governance
- category-aware prompt creation

## 8. Relationships Between Datasets

### Core Relationship Graph
- `companies.csv` -> `roles.csv` by `company_id`
- `section_definitions.csv` -> `topic_taxonomy.csv` by `section_id`
- `difficulty_levels.csv` -> `company_pattern.csv` and question banks by `difficulty_id`
- `topic_taxonomy.csv` -> `company_pattern.csv` and question banks by `topic_id`
- `company_pattern.csv` -> `question banks` by `company_id`, `role_id`, `section_id`, `topic_id`
- `question banks` -> `question_metadata.csv` by `question_id`
- `student_performance.csv` -> `question banks` by `question_id`
- `student_performance.csv` -> `company_pattern.csv` by `company_id`, `role_id`, `hiring_round`, `section_id`

### Normalized vs Denormalized Practices
- Keep reference CSVs for taxonomy and normalization.
- Keep role-specific and company-specific banks for direct retrieval.
- Use `question_id` as the global join key for AI and performance analytics.

## 9. Scalable MongoDB Schema Recommendation

### Suggested collections
1. `companies`
2. `roles`
3. `sections`
4. `topics`
5. `difficulties`
6. `companyPatterns`
7. `questions`
8. `questionMetadata`
9. `studentPerformances`
10. `assessmentSessions`
11. `taxonomyTags`

### Example document structure

`companies` document:
- `_id`
- `name`
- `slug`
- `industry`
- `headquartersCountry`
- `status`
- `createdAt`
- `updatedAt`

`roles` document:
- `_id`
- `companyId`
- `name`
- `level`
- `category`
- `primarySkills`
- `secondarySkills`
- `status`
- `createdAt`
- `updatedAt`

`companyPatterns` document:
- `_id`
- `companyId`
- `roleId`
- `hiringRound`
- `sectionId`
- `topicId`
- `difficultyId`
- `questionCount`
- `timeLimitSeconds`
- `weightagePercent`
- `frequencyPercent`
- `notes`
- `dataSource`
- `createdAt`
- `updatedAt`

`questions` document:
- `_id`
- `companyId`
- `roleId`
- `sectionId`
- `topicId`
- `difficultyId`
- `questionType`
- `text`
- `data`
- `options`
- `correctAnswer`
- `explanation`
- `marks`
- `negativeMarks`
- `timeEstimateSeconds`
- `lastUsedAt`
- `usageCount`
- `source`
- `status`
- `createdAt`
- `updatedAt`
- category-specific fields for coding/interview

`questionMetadata` document:
- `_id`
- `questionId`
- `cognitiveSkillLevel`
- `skillVector`
- `learningObjective`
- `keywords`
- `contentSource`
- `generationMethod`
- `aiReadyTags`
- `semanticEmbeddingId`
- `status`
- `reviewerId`
- `reviewNotes`
- `createdAt`
- `updatedAt`

`studentPerformances` document:
- `_id`
- `studentId`
- `assessmentInstanceId`
- `companyId`
- `roleId`
- `hiringRound`
- `sectionId`
- `questionId`
- `attemptedAt`
- `response`
- `isCorrect`
- `score`
- `timeSpentSeconds`
- `attemptOrder`
- `hintUsed`
- `partialCredit`
- `confidenceRating`
- `adaptiveLevel`
- `sessionId`
- `deviceType`
- `browser`
- `createdAt`
- `updatedAt`

### MongoDB scalability notes
- Use indexed fields: `companyId`, `roleId`, `sectionId`, `topicId`, `questionId`, `studentId`, `assessmentInstanceId`.
- Store static taxonomy in separate collections for reference.
- Denormalize only when query performance demands it, e.g. duplicate `topicName` and `difficultyName` in frequently read question documents.
- Keep `questionMetadata` in a separate collection for AI enrichment and embedding lookup.
- Use time-series or bucketed collections for very large performance logs if needed.

## 10. Scalability and Future-readiness

### 20+ companies / 100+ roles / 100,000+ questions
- Use stable unique IDs and slugs.
- Separate master taxonomy from company-specific banks.
- Use category-level CSVs to simplify ingestion and export.
- Keep question metadata separate to scale AI training without bloating raw question banks.
- Keep pattern data normalized so new companies or roles can be added without redesign.

### AI Question Generation
- `question_metadata.csv` enables generation prompts via skill vectors, topics, difficulty, and cognitive taxonomy.
- `topic_taxonomy.csv` and `section_definitions.csv` provide structured generation inputs.
- `source` and `generation_method` let the platform distinguish generated content from curated content.

### ML Pattern Learning
- `company_pattern.csv` provides labeled pattern structure for supervised learning.
- `student_performance.csv` provides response and time-based features for candidate modeling.
- `usage_count`, `last_used_at`, and `frequency_percent` permit drift detection and pattern updating.

### Adaptive Mock Tests
- `student_performance.csv` includes `adaptive_level` and `confidence_rating` for adaptive algorithms.
- Question banks support `difficulty_id`, `time_estimate_seconds`, and `skill_vector` to select adaptive next items.
- Patterns plus candidate performance allow dynamic mock test assembly aligned to company-specific structure.

## 11. Recommended Implementation Notes

- Prefer global question IDs across all categories so AI and analytics can join without category-specific partitioning.
- For company-specific folders, keep only the subset of questions actually used by that company/role to avoid duplication.
- Use `datasets/global/` as the canonical master dataset for training and cross-company insights.
- Use CSV naming conventions consistently: `YYYYMMDD` or `v1` only if versioning is required, otherwise keep stable file names.
- For exports/imports, treat `company_pattern.csv`, `question_metadata.csv`, and `student_performance.csv` as the central datasets for analytics and model building.
