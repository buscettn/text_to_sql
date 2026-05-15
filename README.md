# Text-to-SQL Engine

A modular, extensible Text-to-SQL system built with Python, LangGraph, and SqlGlot. The project strictly adheres to Hexagonal Architecture (Ports and Adapters) principles to ensure clear separation of concerns between orchestration, business logic, and external interfaces.

## 🚀 Key Features

- **Semantic Domain Mapping**: Automatically identifies the relevant data domain for a query using LanceDB vector search, grounding the generation process.
- **Entity Resolution (ER)**: Advanced entity extraction using a fine-tuned GLiNER model to resolve specific domain entities (e.g., Financial Institutions).
- **SQL Validation & Transpilation**: Integrated `sqlglot` for ensuring SQL syntax correctness and automatic transpilation to target dialects (e.g., Impala).
- **End-to-End Orchestration**: Managed by LangGraph for robust, state-driven workflows (Pre-generation, Generation, Validation).
- **Evaluation Framework**: Built-in benchmarking tool to run queries against ground truth, calculating Accuracy and BLEU scores, and exporting detailed reports to Excel.
- **Hexagonal Architecture**: Business logic is strictly isolated from the orchestration framework and external entry points.

## 🛠 Architecture

The system is designed with a decoupled architecture to facilitate maintainability and testability:

- **Core Engine (`core/`)**: Provides a framework-agnostic facade (`TextToSQLEngine`) serving as the primary entry point.
- **Orchestration (`graph/`)**: Utilizes LangGraph to manage the workflow and state.
- **Business Logic (`components/`)**: Pure business logic modules (Generator, Validator, etc.) decoupled from orchestration.
- **Semantic Layer (`semantic_layer/`)**: Responsible for domain-specific context retrieval and prompt construction.
- **ER Service (`semantic_layer/er_service/`)**: Named Entity Resolution service using fine-tuned GLiNER models.

## 📋 Prerequisites

- Python 3.10+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Configure environment variables in a `.env` file (see `.env.example` if available).

## ⚙️ Major Setup Steps

### 1. Semantic Domain Data Setup
Initialize the LanceDB table with domain-specific metadata used for semantic mapping:
```bash
python -m semantic_layer.setup.setup_domain_data
```
This script processes the CSV data in `data/semantic_input/domain_data.csv` and generates embeddings to enable vector search.

### 2. Entity Resolution (ER) Service Setup
The ER service identifies domain entities (e.g., banks) to improve query precision.

**Step A: Generate Training Data**
Generate a synthetic dataset based on entity lists and templates:
```bash
python -m semantic_layer.er_service.generate_train_data
```

**Step B: Fine-tune GLiNER Model**
Fine-tune the base GLiNER model on the generated dataset:
```bash
python -m semantic_layer.er_service.fine_tune_gliner
```
*Note: Use the `--test` flag for a quick verification run with a small subset of data.*

## 📊 Evaluation Framework
Benchmark the system against ground truth data (Excel format):
```bash
python -m evaluation.run_eval
```
Results, including Accuracy and BLEU scores, will be saved in `evaluation/results/` as an Excel file.

## 💻 Entry Points

- **Python SDK**: For programmatic integration. See `sdk/` and `tests/test_sdk.py`.
- **CLI**: Command-line interface for local testing.
  ```bash
  python -m cli.main
  ```

## 🧪 Development & Testing

The project uses `pytest` for unit testing.
```bash
pytest
```

## 📚 Dependencies

- `langgraph`: Workflow orchestration.
- `sqlglot`: SQL parsing, validation, and transpilation.
- `lancedb`: Vector database for semantic retrieval.
- `gliner`: Named Entity Recognition.
- `pydantic`: Data validation.
- `pandas` & `openpyxl`: Data processing and Excel reporting.


