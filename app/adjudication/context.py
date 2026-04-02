from pydantic import BaseModel
from app.domain.line_item import LineItem
from app.domain.policy import Policy
from app.domain.usage_tracker import UsageTracker


class AdjudicationContext(BaseModel):
    line_item: LineItem
    policy: Policy
    usage: UsageTracker

    # working state (mutated by rules)
    allowed_amount: float = 0
    deductible_applied: float = 0
    payable_amount: float = 0

    status: str = "PENDING"
    code: str = "VALID"