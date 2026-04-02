from pydantic import BaseModel
from typing import Dict


class UsageTracker(BaseModel):
    member_id: str
    deductible_used: float = 0
    service_limits_used: Dict[str, float] = {}