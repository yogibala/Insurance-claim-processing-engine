from decimal import Decimal
from pydantic import BaseModel
from app.domain.line_item import LineItem
from app.domain.policy import Policy
from app.domain.usage_tracker import UsageTracker

class AdjudicationContext(BaseModel):
    line_item: LineItem
    policy: Policy
    usage: UsageTracker
    allowed_amount: Decimal = Decimal("0")
    deductible_applied: Decimal = Decimal("0")
    payable_amount: Decimal = Decimal("0")
    status: str = "PENDING"
    code: str = "VALID"
    trace: list = []
    error: str | None = None