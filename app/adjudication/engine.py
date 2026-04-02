from app.adjudication.context import AdjudicationContext
from app.adjudication.rules import (
    CoverageRule,
    DeductibleRule,
    LimitRule,
    ReimbursementRule
)
from app.domain.adjudication_result import AdjudicationResult, FinancialBreakdown
from app.adjudication.explanations import ExplanationFactory
from app.utils.constants import AdjudicationCode


class AdjudicationEngine:

    def __init__(self):
        self.rules = [
            CoverageRule(),
            DeductibleRule(),
            LimitRule(),
            ReimbursementRule()
        ]

   def adjudicate(self, ctx: AdjudicationContext):

    for rule in self.rules:
        rule_name = rule.__class__.__name__

        try:
            before = ctx.allowed_amount

            ctx = rule.apply(ctx)

            after = ctx.allowed_amount

            # trace logging
            ctx.trace.append({
                "rule": rule_name,
                "before": before,
                "after": after,
                "status": ctx.status,
                "code": ctx.code
            })

            # business stop condition
            if ctx.status == "DENIED":
                break

        except Exception as e:
            # system failure (not business denial)
            ctx.status = "NEEDS_REVIEW"
            ctx.code = AdjudicationCode.SYSTEM_ERROR
            ctx.error = str(e)

            ctx.trace.append({
                "rule": rule_name,
                "error": str(e)
            })

            break