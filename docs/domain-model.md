# Domain Model

## Overview

This system models an insurance claims adjudication workflow where each claim consists of multiple line items that are independently evaluated against policy rules. The system supports partial approvals, financial breakdowns, and transparent explanations.

---

## Core Entities

### Claim

Represents a reimbursement request submitted by a member.

Attributes:
- id
- member_id
- policy_id
- status
- line_items
- total_requested
- total_payable
- total_member_responsibility

Behavior:
- Aggregates line item decisions
- Determines final claim status

---

### LineItem

Represents an individual medical expense within a claim.

Attributes:
- id
- service_type
- amount (Decimal)
- status
- adjudication_result

Behavior:
- Independently adjudicated
- Produces financial breakdown

---

### Policy

Defines coverage rules.

Attributes:
- deductible
- service_coverage (per service type):
  - covered (bool)
  - limit (annual)
  - reimbursement_rate

---

### UsageTracker

Tracks policy usage across claims.

Attributes:
- deductible_used
- service_limits_used (per service)

Purpose:
- Enables accurate limit and deductible enforcement

---

### FinancialBreakdown

Represents monetary outcome of adjudication.

Attributes:
- requested_amount
- allowed_amount
- deductible_applied
- payable_amount
- member_responsibility

All values use **Decimal** for precision.

---

## Adjudication Model

Each LineItem produces:

- status
- adjudication code
- financial breakdown
- explanation

---

## State Machines

### LineItem State Machine

PENDING → APPROVED | DENIED | NEEDS_REVIEW

---

### Claim State Machine

SUBMITTED → IN_REVIEW → APPROVED | PARTIAL_APPROVED | DENIED → PAID

---

## Partial Approval Handling

A claim is marked PARTIAL_APPROVED when:
- At least one line item is approved
- At least one line item is denied or partially paid

---

## Rule Execution Pipeline

Rules are executed in order:

1. CoverageRule → determines if service is covered
2. DeductibleRule → applies remaining deductible
3. LimitRule → enforces service limits
4. ReimbursementRule → calculates payable amount

---

## Rule Precedence Principle

Upstream rules define decision codes. Downstream rules must not override meaningful decisions.

Example:
- DeductibleRule sets `DEDUCTIBLE_APPLIED`
- ReimbursementRule must not override it

---

## Explanation System

Each adjudication produces:
- code (machine-readable)
- explanation (human-readable)

Implemented via ExplanationFactory.

---

## Financial Precision

All monetary values use **Decimal** to:
- Avoid floating point errors
- Ensure deterministic calculations
- Maintain financial correctness