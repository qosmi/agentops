from pydantic import BaseModel


class EvaluationCase(BaseModel):
    name: str
    question: str
    expected_tools: set[str]
    expected_answer_contains: list[str]