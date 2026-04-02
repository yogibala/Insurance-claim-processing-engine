import json
from pathlib import Path
from app.domain.policy import Policy


def load_policy(policy_id: str) -> Policy:
    path = Path(f"app/config/{policy_id.lower()}.json")

    with open(path) as f:
        data = json.load(f)

    return Policy(**data)