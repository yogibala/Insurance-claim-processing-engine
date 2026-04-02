from app.utils.constants import LineItemStatus


class LineItemStateMachine:

    @staticmethod
    def transition(current: LineItemStatus, new: LineItemStatus):
        # simple validation (expand later)
        return new