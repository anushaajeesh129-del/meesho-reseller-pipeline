# Part 2: Growth Engine & Guardrails

This folder contains the deterministic growth detection logic and input validation.

## Files
- growth_engine.py: Contains mom_growth(), is_flagged(), and validate_feed().
- test_growth_engine.py: Given-When-Then unit tests for the engine.
- fixtures/: Contains the corrupted feed test file and a copy of the Part 1 output.

## How to Run Tests
From the root directory, run:
```bash
pytest part2_engine/test_growth_engine.py