from decimal import Decimal

from pydantic import BaseModel, Field


class LLMPricing(BaseModel):
    input_cost_per_million_tokens: Decimal = Field(
        default=Decimal(0),
        ge=0,
    )
    output_cost_per_million_tokens: Decimal = Field(
        default=Decimal(0),
        ge=0,
    )

    def calculate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
    ) -> Decimal:
        input_cost = (
            Decimal(input_tokens)
            / Decimal(1000000)
            * self.input_cost_per_million_tokens
        )

        output_cost = (
            Decimal(output_tokens)
            / Decimal(1000000)
            * self.output_cost_per_million_tokens
        )

        return input_cost + output_cost