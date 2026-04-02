from app.adjudication.engine import AdjudicationEngine
from app.adjudication.context import AdjudicationContext
from app.config.loader import load_policy
from app.domain import claim
from app.domain.usage_tracker import UsageTracker
from app.state_machine.claim_sm import ClaimStateMachine


class ClaimsService:

    def __init__(self):
        self.engine = AdjudicationEngine()

    def process_claim(self, claim):

        policy = load_policy(claim.policy_id)

        usage = UsageTracker(member_id=claim.member_id)

        for line_item in claim.line_items:
            ctx = AdjudicationContext(
                line_item=line_item,
                policy=policy,
                usage=usage
            )

            result = self.engine.adjudicate(ctx)

            line_item.status = result.status
            line_item.adjudication = result

        claim.status = ClaimStateMachine.derive_state(claim.line_items)
        claim.total_requested = sum(li.amount for li in claim.line_items)
        claim.total_payable = sum(
            li.adjudication.breakdown.payable_amount for li in claim.line_items
        )
        claim.total_member_responsibility = (
            claim.total_requested - claim.total_payable
        )       

        return claim