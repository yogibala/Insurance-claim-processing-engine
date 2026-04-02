from app.utils.constants import ClaimStatus, LineItemStatus


class ClaimStateMachine:

    @staticmethod
    def derive_state(line_items):
        statuses = [li.status for li in line_items]

        if all(s == LineItemStatus.DENIED for s in statuses):
            return ClaimStatus.DENIED

        if all(s == LineItemStatus.APPROVED for s in statuses):
            return ClaimStatus.APPROVED

        return ClaimStatus.PARTIAL_APPROVED