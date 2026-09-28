from decimal import Decimal

from agentops.models.llm_usage import LLMUsage


def test_llm_usage_defaults_to_zero() -> None:
    usage = LLMUsage()

    assert usage.input_tokens == 0
    assert usage.output_tokens == 0
    assert usage.total_tokens == 0
    assert usage.estimated_cost_usd == Decimal(0)


def test_llm_usage_stores_token_counts() -> None:
    usage = LLMUsage(
        input_tokens=1000,
        output_tokens=500,
        total_tokens=1500,
    )

    assert usage.input_tokens == 1000
    assert usage.output_tokens == 500
    assert usage.total_tokens == 1500


def test_llm_usage_accumulates_usage() -> None:
    first = LLMUsage(
        input_tokens=1000,
        output_tokens=500,
        total_tokens=1500,
        estimated_cost_usd=Decimal("0.01"),
    )

    second = LLMUsage(
        input_tokens=2000,
        output_tokens=1000,
        total_tokens=3000,
        estimated_cost_usd=Decimal("0.02"),
    )

    total = first.add(second)

    assert total.input_tokens == 3000
    assert total.output_tokens == 1500
    assert total.total_tokens == 4500
    assert total.estimated_cost_usd == Decimal("0.03")


def test_llm_usage_add_does_not_mutate_original() -> None:
    first = LLMUsage(
        input_tokens=1000,
        output_tokens=500,
        total_tokens=1500,
    )

    second = LLMUsage(
        input_tokens=2000,
        output_tokens=1000,
        total_tokens=3000,
    )

    first.add(second)

    assert first.input_tokens == 1000
    assert first.output_tokens == 500
    assert first.total_tokens == 1500