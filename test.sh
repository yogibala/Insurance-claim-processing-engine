#!/bin/bash

BASE_URL="http://127.0.0.1:8000"

echo "=============================="
echo "1. SUBMIT CLAIM"
echo "=============================="

curl -X POST "$BASE_URL/claims" \
-H "Content-Type: application/json" \
-d '{
  "id": "C100",
  "member_id": "M1",
  "policy_id": "policy_001",
  "line_items": [
    {"id": "L1", "service_type": "CONSULTATION", "amount": 1000},
    {"id": "L2", "service_type": "DENTAL", "amount": 500},
    {"id": "L3", "service_type": "CONSULTATION", "amount": 300}
  ]
}'

echo -e "\n\n=============================="
echo "2. PROCESS CLAIM"
echo "=============================="

curl -X POST "$BASE_URL/claims/C100/process"

echo -e "\n\n=============================="
echo "3. GET CLAIM"
echo "=============================="

curl -X GET "$BASE_URL/claims/C100"