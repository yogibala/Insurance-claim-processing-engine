# Decisions & Trade-offs

## 1. Config-Driven Adjudication

Policies are defined in JSON while the adjudication logic is implemented in deterministic code.

This allows:

* Flexibility in rule updates
* Strong auditability

---

## 2. Claim vs Line Item State Machines

Separate state machines allow:

* Partial approvals
* Accurate lifecycle tracking

---

## 3. Explanation Factory

Decouples:

* Decision logic
* User communication

---

## 4. Financial Breakdown Model

Introduced to handle:

* Partial payments
* Deductible tracking
* Limit enforcement

---

## 5. Usage Tracking

Tracks consumption across claims to ensure:

* Accurate limit enforcement
* Realistic adjudication behavior

---

## Trade-offs

* No database (in-memory store used)
* No concurrency handling
* Limited rule set

```
```
