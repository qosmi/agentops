from decimal import Decimal

from agentops.models.llm_pricing import LLMPricing


def test_llm_pricing_calculates_input_and_output_cost() -> None:
    pricing = LLMPricing(
        input_cost_per_million_tokens=Decimal(5),
        output_cost_per_million_tokens=Decimal(15),
    )

    cost = pricing.calculate_cost(
        input_tokens=1000,
        output_tokens=500,
    )

    assert cost == Decimal("0.0125")


def test_llm_pricing_returns_zero_for_zero_tokens() -> None:
    pricing = LLMPricing(
        input_cost_per_million_tokens=Decimal(5),
        output_cost_per_million_tokens=Decimal(15),
    )

    cost = pricing.calculate_cost(
        input_tokens=0,
        output_tokens=0,
    )

    assert cost == Decimal(0)


def test_llm_pricing_rejects_negative_input_price() -> None:
    try:
        LLMPricing(
            input_cost_per_million_tokens=Decimal(-1),
            output_cost_per_million_tokens=Decimal(15),
        )
    except ValueError:
        return

    raise AssertionError(
        "Expected negative input pricing to be rejected"
    )