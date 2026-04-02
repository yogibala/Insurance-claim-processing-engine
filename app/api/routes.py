from fastapi import APIRouter, HTTPException

router = APIRouter()




@router.get("/")
def health():
    return {"status": "ok"}


