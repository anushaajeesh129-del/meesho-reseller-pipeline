# Prompt Pack

## 1. Trigger

This prompt is triggered when:

is_flagged(mom_pct) == "flagged"

---

## 2. Input Variables

- {category}
- {previous_revenue}
- {current_revenue}
- {mom_pct}
- {month}
- {prev_month}

---

## 3. Prompt

Generate a stakeholder-ready business narrative using:

### CONTEXT
Describe:
- category
- previous month
- current month
- previous revenue
- current revenue

### INSIGHT (FACT)
State:
- exact MoM percentage
- mention FACT explicitly

Example:
"Ethnic Wear revenue grew 77.1% MoM — FACT"

### IMPLICATION (HYPOTHESIS)

Suggest:
- action items
- unproven reasons must be labeled HYPOTHESIS

Example:
"Investigate promotional campaigns — HYPOTHESIS"

Rules:
- Use only supplied placeholders
- Do not invent numbers
- Do not mention reseller names

---

## 4. Checklist

✓ Correct category name

✓ Correct revenue values

✓ FACT label included

✓ HYPOTHESIS label included

✓ Actionable recommendation

✓ No raw reseller names