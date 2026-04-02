from decimal import Decimal

from pydantic import BaseModel
from typing import Dict


class UsageTracker(BaseModel):
    member_id: str
    service_limits_used: Dict[str, Decimal] = {}
    deductible_used: Decimal = Decimal("0")