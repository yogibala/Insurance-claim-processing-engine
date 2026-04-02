from pydantic import BaseModel
from typing import Dict


class Policy(BaseModel):
    policy_id: str
    deductible: float
    service_coverage: Dict[str, object]  # flexible for config-driven rules