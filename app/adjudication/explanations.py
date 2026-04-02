from app.utils.constants import AdjudicationCode


class ExplanationFactory:

    MESSAGES = {
        AdjudicationCode.SERVICE_NOT_COVERED: "This service is not covered under your policy.",
        AdjudicationCode.LIMIT_EXCEEDED: "Coverage limit exceeded for this service.",
        AdjudicationCode.DEDUCTIBLE_APPLIED: "Amount applied towards deductible.",
        AdjudicationCode.VALID: "Claim processed successfully.",
        AdjudicationCode.SYSTEM_ERROR: "An error occurred during claim processing. Please contact support. support@company.com"
        
    }

    @staticmethod
    def get(code: AdjudicationCode) -> str:
        return ExplanationFactory.MESSAGES.get(code, "Unknown decision")