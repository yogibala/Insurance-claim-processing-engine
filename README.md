# Claims Processing System

## Overview

This system processes insurance claims by adjudicating each line item against policy coverage rules. It supports partial approvals, detailed financial breakdowns, and transparent explanations for decisions.

---

## Features

* Config-driven policy rules (JSON-based)
* Deterministic adjudication engine
* Line item level decisions
* Partial claim approvals
* Financial breakdown (deductible, limits, payable)
* Explanation system for every decision

---

## Architecture

* Domain-driven design
* Rule-based adjudication pipeline
* Separate state machines for Claim and LineItem

---

## Setup

```bash
conda activate claims-engine
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## API Docs

http://127.0.0.1:8000/docs

---

## Demo Flow

### 1. Submit Claim

POST /claims

### 2. Process Claim

POST /claims/{claim_id}/process

### 3. Get Claim

GET /claims/{claim_id}

---

## Example Input

```json
{
  "id": "C1",
  "member_id": "M1",
  "policy_id": "policy_001",
  "line_items": [
    {"id": "L1", "service_type": "CONSULTATION", "amount": 1000},
    {"id": "L2", "service_type": "DENTAL", "amount": 500}
  ]
}
```

---

## Output Highlights

* Line item level approval/denial
* Partial approvals supported
* Explanation for every decision
* Financial breakdown per line item

```
```
