from pydantic import BaseModel
from app.utils.constants import AdjudicationCode
from decimal import Decimal

class FinancialBreakdown(BaseModel):
    requested_amount: Decimal
    allowed_amount: Decimal
    deductible_applied: Decimal
    payable_amount: Decimal
    member_responsibility: Decimal


class AdjudicationResult(BaseModel):
    status: str
    code: AdjudicationCode
    breakdown: FinancialBreakdown
    explanation: str