# Meesho Reseller Growth & Alert Intelligence Pipeline

## Project Overview

This project implements a repeatable, deterministic pipeline for monitoring Meesho reseller growth, validating data, detecting significant changes, generating a controlled business narrative, and running a mock agent workflow.

The complete pipeline is designed to run offline using the project's own generated dataset and deterministic logic.

## Project Structure

```text
data/
├── generate_dataset.py
├── resellers.csv
├── orders.csv
└── meesho_reseller.db

part1_sql/
├── queries.sql
└── output/
    └── *.csv

part2_engine/
├── growth_engine.py
├── test_growth_engine.py
└── fixtures/
    ├── corrupted_feed.csv
    └── monthly_category_revenue.csv

part3_narrative/
├── prompt_pack.md
├── narrative_report.md
└── masking.py

part4_agent/
├── agent_spec.md
└── mock_agent_runner.py

README.md
```

## Requirements

* Python 3.x
* SQLite
* pytest

No paid services or external AI APIs are required.

## How to Run the Complete Pipeline

Run the Parts in the following order.

### Part 1 — Generate Dataset and Run SQL

First generate the deterministic dataset:

```bash
python data/generate_dataset.py
```

This creates:

```text
data/resellers.csv
data/orders.csv
data/meesho_reseller.db
```

The dataset is generated using a fixed random seed so that the results are reproducible.

Next, run the SQL queries in:

```text
part1_sql/queries.sql
```

The verified business outputs are stored under:

```text
part1_sql/output/
```

### Part 2 — Growth Detection and Guardrails

Run the unit tests:

```bash
python -m pytest part2_engine/test_growth_engine.py -v
```

Part 2 implements:

* Month-over-month growth calculation
* Growth threshold detection
* Exact-boundary handling
* Input/feed validation
* Guardrails for invalid data

The tests verify that the growth engine behaves consistently for the required business cases.

### Part 3 — Reliable AI Narrative

Part 3 contains:

```text
part3_narrative/prompt_pack.md
part3_narrative/narrative_report.md
part3_narrative/masking.py
```

The prompt pack defines a reusable process for converting verified business numbers into a controlled business narrative.

The narrative is based on verified outputs from the earlier parts and avoids inventing unsupported numbers or exposing information that should be masked.

### Part 4 — Agentic Workflow

Part 4 contains:

```text
part4_agent/agent_spec.md
part4_agent/mock_agent_runner.py
```

Run the mock agent runner with:

```bash
python part4_agent/mock_agent_runner.py
```

The mock agent demonstrates the complete guarded workflow using deterministic offline logic.

## Zero API Keys

The complete project runs with **zero API keys**.

No OpenAI API key, Gemini API key, paid API, or other external AI service is required.

The project uses deterministic local Python, SQL, CSV, SQLite, validation, masking, and mock-agent logic.

## Workflow Mapping

### Part 1 → Part 2

Part 1 computes the real business numbers using SQL first. Part 2 then receives the verified data and applies deterministic growth calculations and guardrails.

This follows the workflow pattern:

```text
Compute real numbers via SQL
        ↓
Verify the results
        ↓
Hand off verified data
        ↓
Apply growth detection and guardrails
```

### Part 3

Part 3 converts verified numerical outputs into a business-readable narrative while applying controlled prompting and masking.

This follows the pattern:

```text
Verified numbers
        ↓
Controlled prompt
        ↓
Business narrative
        ↓
Mask sensitive information
```

### Part 4

Part 4 combines the earlier components into a guarded agentic workflow.

It mirrors the pattern:

```text
Intake
  ↓
Summary
  ↓
Report Draft
  ↓
Validate
  ↓
Final Output
```

The mock runner demonstrates this workflow without requiring an external AI API.

## Reproducibility

The dataset generator uses a fixed random seed. Therefore, the dataset can be regenerated consistently.

To regenerate the dataset, run:

```bash
python data/generate_dataset.py
```

Then execute the Parts in order:

```text
Part 1 → Part 2 → Part 3 → Part 4
```

## Submission

This repository contains the complete implementation of the Meesho Reseller Growth & Alert Intelligence Pipeline, including the generated dataset, SQL business queries, growth engine and tests, narrative prompt pack, masking logic, agent specification, mock agent runner, and documentation.
