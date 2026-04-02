from app.adjudication.context import AdjudicationContext


class BaseRule:
    def apply(self, ctx: AdjudicationContext) -> AdjudicationContext:
        raise NotImplementedError

class CoverageRule(BaseRule):

    def apply(self, ctx: AdjudicationContext):
        service = ctx.line_item.service_type
        coverage = ctx.policy.service_coverage.get(service)

        if not coverage or not coverage.get("covered", False):
            ctx.status = "DENIED"
            ctx.code = "SERVICE_NOT_COVERED"
            ctx.allowed_amount = 0
            ctx.payable_amount = 0
            return ctx

        ctx.allowed_amount = ctx.line_item.amount
        return ctx

class DeductibleRule(BaseRule):

    def apply(self, ctx: AdjudicationContext):
        remaining_deductible = ctx.policy.deductible - ctx.usage.deductible_used

        if remaining_deductible <= 0:
            return ctx

        applied = min(ctx.allowed_amount, remaining_deductible)

        ctx.deductible_applied = applied
        ctx.allowed_amount -= applied
        ctx.usage.deductible_used += applied

        if ctx.allowed_amount == 0:
            ctx.status = "APPROVED"
            ctx.code = "DEDUCTIBLE_APPLIED"

        return ctx

class LimitRule(BaseRule):

    def apply(self, ctx: AdjudicationContext):
        service = ctx.line_item.service_type
        coverage = ctx.policy.service_coverage.get(service, {})

        limit = coverage.get("limit")
        used = ctx.usage.service_limits_used.get(service, 0)

        if not limit:
            return ctx

        remaining = limit - used

        if remaining <= 0:
            ctx.allowed_amount = 0
            ctx.payable_amount = 0
            ctx.status = "DENIED"
            ctx.code = "LIMIT_EXCEEDED"
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

        ctx.payable_amount = ctx.allowed_amount * rate

        if ctx.payable_amount == 0 and ctx.status != "DENIED":
            ctx.status = "APPROVED"
            ctx.code = "VALID"

        else:
            ctx.status = "APPROVED"

        return ctx