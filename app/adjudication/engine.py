from decimal import Decimal, ROUND_HALF_UP

from app.adjudication.context import AdjudicationContext
from app.adjudication.rules import (
    CoverageRule,
    DeductibleRule,
    LimitRule,
    ReimbursementRule
)
from app.domain.adjudication_result import AdjudicationResult, FinancialBreakdown
from app.adjudication.explanations import ExplanationFactory
from app.utils.constants import AdjudicationCode, LineItemStatus


# helper for consistent currency rounding
def to_money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class AdjudicationEngine:

    def __init__(self):
        self.rules = [
            CoverageRule(),
            DeductibleRule(),
            LimitRule(),
            ReimbursementRule()
        ]

    def adjudicate(self, ctx: AdjudicationContext) -> AdjudicationResult:

        # ensure safe Decimal initialization
        ctx.allowed_amount = Decimal(ctx.allowed_amount or 0)
        ctx.deductible_applied = Decimal(ctx.deductible_applied or 0)
        ctx.payable_amount = Decimal(ctx.payable_amount or 0)

        for rule in self.rules:
            rule_name = rule.__class__.__name__

            try:
                before = ctx.allowed_amount

                ctx = rule.apply(ctx)

                after = ctx.allowed_amount

                # trace logging (convert to string for JSON safety)
                ctx.trace.append({
                    "rule": rule_name,
                    "before": str(before),
                    "after": str(after),
                    "status": ctx.status,
                    "code": ctx.code
                })

                # business stop condition
                if ctx.status == LineItemStatus.DENIED:
                    break

            except Exception as e:
                # system failure (not business denial)
                ctx.status = LineItemStatus.NEEDS_REVIEW
                ctx.code = AdjudicationCode.SYSTEM_ERROR
                ctx.error = str(e)

                ctx.trace.append({
                    "rule": rule_name,
                    "error": str(e)
                })

                break

        # ✅ ensure all values are properly rounded
        requested_amount = to_money(Decimal(ctx.line_item.amount))
        allowed_amount = to_money(ctx.allowed_amount)
        deductible_applied = to_money(ctx.deductible_applied)
        payable_amount = to_money(ctx.payable_amount)

        member_responsibility = to_money(
            requested_amount - payable_amount
        )

        # explanation mapping
        explanation = ExplanationFactory.get(ctx.code)

        breakdown = FinancialBreakdown(
            requested_amount=requested_amount,
            allowed_amount=allowed_amount,
            deductible_applied=deductible_applied,
            payable_amount=payable_amount,
            member_responsibility=member_responsibility
        )

        return AdjudicationResult(
            status=ctx.status,
            code=ctx.code,
            breakdown=breakdown,
            explanation=explanation
        )