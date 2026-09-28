from agentops.evaluation.cases import EvaluationCase
from agentops.evaluation.runner import evaluate_answer


def test_evaluate_answer_passes() -> None:
    case = EvaluationCase(
        name="test",
        question="Why?",
        expected_tools=set(),
        expected_answer_contains=["payments"],
    )

    assert evaluate_answer(
        case,
        "The payments product caused the increase.",
    )


def test_evaluate_answer_fails() -> None:
    case = EvaluationCase(
        name="test",
        question="Why?",
        expected_tools=set(),
        expected_answer_contains=["payments"],
    )

    assert not evaluate_answer(
        case,
        "The identity product caused the increase.",
    )