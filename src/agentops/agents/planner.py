from pydantic import BaseModel


class InvestigationStep(BaseModel):
    objective: str
    suggested_tool: str | None = None


class InvestigationPlan(BaseModel):
    steps: list[InvestigationStep]


class PlannerAgent:
    def plan(self, question: str) -> InvestigationPlan:
        return InvestigationPlan(
            steps=[
                InvestigationStep(
                    objective=question,
                    suggested_tool="get_resolution_time",
                )
            ]
        )