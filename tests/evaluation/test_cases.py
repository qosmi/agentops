from agentops.evaluation.cases import EvaluationCase


def test_evaluation_case() -> None:
    case = EvaluationCase(
        name="resolution_time",
        question="Why did resolution time increase?",
        expected_tools={"get_resolution_time"},
        expected_answer_contains=["payments"],
    )

    assert case.name == "resolution_time"