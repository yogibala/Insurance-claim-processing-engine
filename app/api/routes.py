from fastapi import APIRouter, HTTPException
from app.domain.claim import Claim
from app.services.claims_service import ClaimsService

router = APIRouter()

claims_db = {}  # in-memory store
service = ClaimsService()


@router.get("/")
def health():
    return {"status": "ok"}


# 1. Submit Claim
@router.post("/claims")
def submit_claim(claim: Claim):
    claims_db[claim.id] = claim
    return {"message": "Claim submitted", "claim_id": claim.id}


# 2. Process Claim
@router.post("/claims/{claim_id}/process")
def process_claim(claim_id: str):
    claim = claims_db.get(claim_id)

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    processed = service.process_claim(claim)

    claims_db[claim_id] = processed

    return processed


# 3. Get Claim
@router.get("/claims/{claim_id}")
def get_claim(claim_id: str):
    claim = claims_db.get(claim_id)

    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    return claim