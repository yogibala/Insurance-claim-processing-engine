# Decisions & Trade-offs

## 1. Config-Driven Adjudication

Policies are defined in JSON while logic is implemented in deterministic code.

Why:
- Business rules change frequently
- Enables non-code updates
- Ensures auditability

---

## 2. Claim vs LineItem State Machines

Separate state machines were introduced.

Why:
- Enables partial approvals
- Models real-world claim behavior
- Avoids ambiguity in mixed outcomes

---

## 3. Rule Engine Design

A rule pipeline approach was used:
- Coverage → Deductible → Limit → Reimbursement

Why:
- Modular
- Extensible
- Easy to debug

---

## 4. Explanation System

Implemented ExplanationFactory.

Why:
- Separates logic from communication
- Ensures consistent messaging
- Supports transparency

---

## 5. Financial Modeling

Introduced FinancialBreakdown per line item.

Why:
- Required for partial approvals
- Enables detailed visibility
- Reflects real-world adjudication

---

## 6. Decimal for Monetary Values

All financial calculations use Decimal instead of float.

Why:
- Avoid floating-point precision errors
- Ensure correctness in financial systems

---

## 7. Engine Robustness

Added:
- Per-rule try-catch
- Execution trace
- SYSTEM_ERROR handling

Why:
- Prevent system crashes
- Improve debuggability
- Separate business vs system failures

---

## 8. Rule Precedence Fix

Prevented downstream rules from overriding upstream decisions.

Why:
- Ensures explanation correctness
- Preserves decision integrity

---

## 9. API Design

Minimal endpoints:
- POST /claims
- POST /claims/{id}/process
- GET /claims/{id}

Why:
- Meets assignment requirements
- Keeps system simple

---

## 10. Testing Strategy

Added unit tests for:
- Partial approval
- Full denial
- Deductible absorption

Why:
- Validate correctness
- Catch logic bugs (e.g., deductible issue)

---

## Trade-offs

- No database (in-memory store used)
- No concurrency handling
- Limited rule set
- No external integrations

---

## Scope Decisions

Diagnosis codes and provider-level adjudication were intentionally not modeled.

Reason:
- Focus on core adjudication logic
- Maintain clarity within time constraint

In a production system, these would be additional rule dimensions.