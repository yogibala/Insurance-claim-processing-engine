# Domain Model

## Core Entities

### Claim

Represents a reimbursement request submitted by a member.

Attributes:

* id
* member_id
* policy_id
* status
* line_items
* total_requested
* total_payable

---

### Line Item

Represents an individual medical expense within a claim.

Attributes:

* id
* service_type
* amount
* status
* adjudication_result

---

### Policy

Defines coverage rules for services.

Attributes:

* deductible
* service coverage rules
* reimbursement rates
* limits

---

### Usage Tracker

Tracks how much of a policy has been consumed.

Attributes:

* deductible_used
* service_limits_used

---

## Financial Breakdown Model

Each line item produces:

* requested_amount
* allowed_amount
* deductible_applied
* payable_amount
* member_responsibility

---

## State Machines

### Line Item State Machine

PENDING → APPROVED | DENIED | NEEDS_REVIEW

---

### Claim State Machine

SUBMITTED → IN_REVIEW → APPROVED | PARTIAL_APPROVED | DENIED → PAID

---

## Partial Approval Handling

A claim is marked PARTIAL_APPROVED when:

* Some line items are approved
* Some are denied or partially paid

---

## Rule Execution Flow

1. Coverage Check
2. Deductible Application
3. Limit Enforcement
4. Reimbursement Calculation

---

## Explanation System

Each adjudication decision produces:

* decision code
* human-readable explanation

This ensures transparency and auditability.

```
```
