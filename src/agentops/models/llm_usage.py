from decimal import Decimal

from pydantic import BaseModel, Field


class LLMUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: Decimal = Field(
        default=Decimal(0),
        decimal_places=8,
    )

    def add(self, usage: "LLMUsage") -> "LLMUsage":
        return LLMUsage(
            input_tokens=self.input_tokens + usage.input_tokens,
            output_tokens=self.output_tokens + usage.output_tokens,
            total_tokens=self.total_tokens + usage.total_tokens,
            estimated_cost_usd=(
                self.estimated_cost_usd
                + usage.estimated_cost_usd
            ),
        )