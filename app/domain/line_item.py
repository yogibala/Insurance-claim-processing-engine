from pydantic import BaseModel
from typing import Optional
from app.utils.constants import LineItemStatus
from app.domain.adjudication_result import AdjudicationResult


class LineItem(BaseModel):
    id: str
    service_type: str
    amount: float

    status: LineItemStatus = LineItemStatus.PENDING

    adjudication: Optional[AdjudicationResult] = None