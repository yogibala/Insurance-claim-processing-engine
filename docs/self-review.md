# Self Review

## What Went Well

- Clean domain separation (Claim vs LineItem)
- Modular rule engine design
- Accurate financial modeling using Decimal
- Strong explanation system
- Handles partial approvals correctly
- Robust error handling in adjudication engine
- Unit tests validate key scenarios

---

## What’s Rough

- In-memory storage (no persistence)
- No concurrency handling
- Limited validation on inputs
- Rule set is simplified
- No API authentication

---

## Key Bug Identified & Fixed

Issue:
- Deductible scenario incorrectly returned VALID instead of DEDUCTIBLE_APPLIED

float vs decimal
- Used Decimal over Float The DECIMAL type is required for financial precision to avoid inaccuracies
Cause:
- ReimbursementRule overwrote upstream decision code

Fix:
- Prevented downstream override of meaningful codes

Learning:
- Rule precedence is critical in decision systems

---

## What I Would Improve

- Add persistent storage (SQLite/Postgres)
- Introduce rule configuration DSL
- Add appeal workflow
- Improve test coverage (edge cases)
- Add structured logging

---

## What I Would Build Next

- Appeals and dispute workflow
- Provider-level coverage rules
- Multi-policy support
- Event-driven processing

---

## Final Reflection

The system prioritizes:
- correctness
- clarity
- explainability

AI was used as a design assistant, but all outputs were reviewed, validated, and refined.

The final system reflects deliberate engineering decisions rather than generated code.