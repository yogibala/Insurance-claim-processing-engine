from pydantic import BaseModel
from app.utils.constants import AdjudicationCode


class FinancialBreakdown(BaseModel):
    requested_amount: float
    allowed_amount: float
    deductible_applied: float
    payable_amount: float
    member_responsibility: float


class AdjudicationResult(BaseModel):
    status: str
    code: AdjudicationCode
    breakdown: FinancialBreakdown
    explanation: str