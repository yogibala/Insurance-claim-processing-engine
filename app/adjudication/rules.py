from decimal import Decimal

from app.adjudication.context import AdjudicationContext
from app.utils.constants import AdjudicationCode, LineItemStatus


class BaseRule:
    def apply(self, ctx: AdjudicationContext) -> AdjudicationContext:
        raise NotImplementedError


class CoverageRule(BaseRule):

    def apply(self, ctx: AdjudicationContext):

        service = ctx.line_item.service_type
        coverage = ctx.policy.service_coverage.get(service)

        if not coverage or not coverage.get("covered", False):
            ctx.status = LineItemStatus.DENIED
            ctx.code = AdjudicationCode.SERVICE_NOT_COVERED
            ctx.allowed_amount = Decimal("0")
            ctx.payable_amount = Decimal("0")
            return ctx

        # ensure Decimal
        ctx.allowed_amount = Decimal(str(ctx.line_item.amount))

        return ctx


class DeductibleRule(BaseRule):

    def apply(self, ctx: AdjudicationContext):

        deductible = Decimal(str(ctx.policy.deductible))
        used = Decimal(str(ctx.usage.deductible_used or 0))

        remaining_deductible = deductible - used

        if remaining_deductible <= Decimal("0"):
            return ctx

        applied = min(ctx.allowed_amount, remaining_deductible)

        ctx.deductible_applied = applied
        ctx.allowed_amount = ctx.allowed_amount - applied
        ctx.usage.deductible_used = used + applied

        if ctx.allowed_amount == Decimal("0"):
            ctx.status = LineItemStatus.APPROVED
            ctx.code = AdjudicationCode.DEDUCTIBLE_APPLIED

        return ctx


class LimitRule(BaseRule):

    def apply(self, ctx: AdjudicationContext):

        service = ctx.line_item.service_type
        coverage = ctx.policy.service_coverage.get(service, {})

        limit = coverage.get("limit")

        if not limit:
            return ctx

        limit = Decimal(str(limit))
        used = Decimal(str(ctx.usage.service_limits_used.get(service, 0)))

        remaining = limit - used

        if remaining <= Decimal("0"):
            ctx.allowed_amount = Decimal("0")
            ctx.payable_amount = Decimal("0")
            ctx.status = LineItemStatus.DENIED
            ctx.code = AdjudicationCode.LIMIT_EXCEEDED
            return ctx

        if ctx.allowed_amount > remaining:
            ctx.allowed_amount = remaining

        ctx.usage.service_limits_used[service] = used + ctx.allowed_amount

        return ctx


class ReimbursementRule(BaseRule):

    def apply(self, ctx: AdjudicationContext):

        service = ctx.line_item.service_type
        coverage = ctx.policy.service_coverage.get(service, {})

        rate = coverage.get("reimbursement_rate", 1.0)
        rate = Decimal(str(rate))  # safe conversion

        ctx.payable_amount = ctx.allowed_amount * rate

        # do NOT override existing meaningful code
        if ctx.status != LineItemStatus.DENIED:

            ctx.status = LineItemStatus.APPROVED

            # only set VALID if no prior business reason exists
            if ctx.code is None:
                ctx.code = AdjudicationCode.VALID

        return ctx