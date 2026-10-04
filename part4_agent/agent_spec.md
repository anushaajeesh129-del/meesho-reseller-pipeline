# Part 4 — Agentic Workflow Specification

## 4.1 Agent Specification

### Goal

Keep Meesho category managers informed of categories whose month-on-month revenue movement crosses the 8% threshold, while requiring human approval before any drafted message is considered sent.

### Tools

The monitoring agent uses the following tools and functions:

* `validate_feed()` from Part 2 to validate the monthly revenue feed.
* `mom_growth()` from Part 2 to calculate month-on-month percentage growth.
* `is_flagged()` from Part 2 to determine whether a category is flagged, not flagged, or exactly at the escalation boundary.
* The Part 3 prompt-pack template-fill logic to create a deterministic message draft.

The Part 2 functions are imported and reused without modification.

### Memory / State

Between runs, the agent needs the previous month's revenue for each category.

This previous-month revenue is required to calculate month-on-month growth for the current run.

The runner receives the previous-month CSV explicitly through:

`previous_month_csv`

and the current-month CSV through:

`current_month_csv`.

### Planner

The agent follows these ordered subtasks:

1. Load the monthly revenue feed and run `validate_feed`.
2. If validation fails, perform a Hard Stop and report the validation errors.
3. If validation succeeds, calculate `mom_growth` for every category against the previous month.
4. Run `is_flagged` for every category.
5. Sort flagged categories by absolute month-on-month percentage in descending order.
6. Draft messages for at most the top three flagged categories using the Part 3 template.
7. Record remaining flagged categories as `suppressed, review manually` without drafting a message.
   7b. Record categories whose `is_flagged` result is `escalate_exact_boundary` in `escalated_categories` without drafting a message.
8. Emit one structured JSON object for the run.

### Feedback Loop

Every drafted message is held for human approval.

The mock runner does not send emails or messages.

The output uses:

`action_taken = "drafted_and_held_for_approval"`

to indicate that drafts were created but not sent.

---

## Guardrails

### Input Guardrail

`validate_feed()` must pass before any growth calculation or drafting takes place.

If validation fails, the agent performs a Hard Stop.

### Action Guardrail

No message is automatically sent.

Messages are only drafted and held for human approval.

There is no Gmail, SMTP, API, or network integration.

### Output Guardrail

Every numeric value in a drafted message must trace directly to a verified Part 1 or Part 2 value.

The agent must not invent numerical figures.

---

## Success Condition

A successful run produces:

* `validation_status = "valid"`
* Correct flagged categories and MoM values
* At most three drafted messages
* Remaining flagged categories recorded as suppressed
* Exact-boundary categories recorded separately in `escalated_categories`
* All drafted numbers traceable to Part 1 or Part 2
* `action_taken = "drafted_and_held_for_approval"`

A valid run may also correctly produce zero drafts when no category crosses the threshold.

## Error Condition

If `validate_feed()` returns invalid:

* `validation_status = "invalid"`
* `validation_errors` contains the validation errors
* `flagged_categories = []`
* `suppressed_categories = []`
* No MoM calculation is attempted
* `action_taken = "hard_stop"`

The error must be surfaced rather than silently skipped.

---

## 4.2 Given-When-Then Agent-Level Specifications

### Specification 1 — Significant Positive Growth

**Given** a category's previous revenue and current revenue produce a month-on-month growth of 77.1%

**When** the agent runs `mom_growth()` and then `is_flagged()`

**Then** the category is classified as `flagged` and is eligible for drafting.

### Specification 2 — Growth Below Threshold

**Given** a category's month-on-month growth is 5.67%

**When** the agent evaluates the category using `is_flagged()`

**Then** the category is classified as `not_flagged` and does not appear in `flagged_categories` or `suppressed_categories`.

### Specification 3 — Exact Boundary

**Given** a category's month-on-month growth is exactly 8.0%

**When** the agent evaluates the category using `is_flagged()`

**Then** the result is `escalate_exact_boundary`, and the category is placed in `escalated_categories` without a drafted message.

### Specification 4 — Invalid Feed

**Given** the current monthly feed contains the validation errors defined in Part 2

**When** the agent runs `validate_feed()`

**Then** the agent performs a Hard Stop, surfaces all validation errors, and produces no flagged or suppressed categories.

---

## 4.3 Structured JSON Output

Every run emits one JSON object containing exactly these top-level keys:

* `run_month`
* `validation_status`
* `validation_errors`
* `flagged_categories`
* `suppressed_categories`
* `escalated_categories`
* `action_taken`

Each drafted flagged-category object contains:

* `category`
* `mom_pct`
* `previous_revenue`
* `current_revenue`
* `drafted`
* `message`

---

## 4.4 Mock Agent Runner

The mock agent runner exposes:

```python
run(month: str, previous_month_csv: str, current_month_csv: str) -> dict
```

The runner:

1. Loads the feeds.
2. Validates the current feed.
3. Stops immediately if validation fails.
4. Calculates MoM growth.
5. Applies the Part 2 flagging logic.
6. Sorts flagged categories by absolute MoM percentage.
7. Drafts messages for the top three flagged categories.
8. Suppresses remaining flagged categories.
9. Separately records exact-boundary categories.
10. Returns one structured JSON object.

No real network call, API key, email integration, or message sending is used.
