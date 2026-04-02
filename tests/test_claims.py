from decimal import Decimal

from app.services.claims_service import ClaimsService
from app.domain.claim import Claim
from app.domain.line_item import LineItem


def build_claim():
    return Claim(
        id="C_TEST",
        member_id="M1",
        policy_id="policy_001",
        line_items=[
            LineItem(id="L1", service_type="CONSULTATION", amount=Decimal("1000")),
            LineItem(id="L2", service_type="DENTAL", amount=Decimal("500")),
            LineItem(id="L3", service_type="CONSULTATION", amount=Decimal("300")),
        ],
    )


def test_partial_approval():
    service = ClaimsService()
    claim = build_claim()

    result = service.process_claim(claim)

    assert result.status == "PARTIAL_APPROVED"

    # L2 should be denied
    assert result.line_items[1].status == "DENIED"

    # payable should match expected
    assert result.total_payable == Decimal("640.00")


def test_fully_denied():
    service = ClaimsService()

    claim = Claim(
        id="C_DENY",
        member_id="M1",
        policy_id="policy_001",
        line_items=[
            LineItem(id="L1", service_type="DENTAL", amount=Decimal("500"))
        ],
    )

    result = service.process_claim(claim)

    assert result.status == "DENIED"
    assert result.total_payable == Decimal("0.00")


def test_deductible_absorption():
    service = ClaimsService()

    claim = Claim(
        id="C_DEDUCT",
        member_id="M1",
        policy_id="policy_001",
        line_items=[
            LineItem(id="L1", service_type="CONSULTATION", amount=Decimal("200"))
        ],
    )

    result = service.process_claim(claim)

    line = result.line_items[0]

    assert line.adjudication.breakdown.payable_amount == Decimal("0.00")
    assert "deductible" in line.adjudication.explanation.lower()