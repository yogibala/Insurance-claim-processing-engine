from app.adjudication.context import AdjudicationContext
from app.adjudication.rules import (
    CoverageRule,
    DeductibleRule,
    LimitRule,
    ReimbursementRule
)
from app.domain.adjudication_result import AdjudicationResult, FinancialBreakdown
from app.adjudication.explanations import ExplanationFactory


class AdjudicationEngine:

    def __init__(self):
        self.rules = [
            CoverageRule(),
            DeductibleRule(),
            LimitRule(),
            ReimbursementRule()
        ]

    def adjudicate(self, ctx: AdjudicationContext) -> AdjudicationResult:

        for rule in self.rules:
            ctx = rule.apply(ctx)

            if ctx.status == "DENIED":
                break

        breakdown = FinancialBreakdown(
            requested_amount=ctx.line_item.amount,
            allowed_amount=ctx.allowed_amount,
            deductible_applied=ctx.deductible_applied,
            payable_amount=ctx.payable_amount,
            member_responsibility=ctx.line_item.amount - ctx.payable_amount
        )

        explanation = ExplanationFactory.get(ctx.code)

        return AdjudicationResult(
            status=ctx.status,
            code=ctx.code,
            breakdown=breakdown,
            explanation=explanation
        )