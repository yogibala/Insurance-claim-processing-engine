from pydantic import BaseModel
from typing import List
from app.utils.constants import ClaimStatus
from app.domain.line_item import LineItem


class Claim(BaseModel):
    id: str
    member_id: str
    policy_id: str

    line_items: List[LineItem]

    status: ClaimStatus = ClaimStatus.SUBMITTED

    total_requested: float = 0
    total_payable: float = 0
    total_member_responsibility: float = 0