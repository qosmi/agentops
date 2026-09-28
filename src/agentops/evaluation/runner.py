from agentops.evaluation.cases import EvaluationCase


def evaluate_answer(
    case: EvaluationCase,
    answer: str,
) -> bool:
    answer_lower = answer.lower()

    return all(
        expected.lower() in answer_lower
        for expected in case.expected_answer_contains
    )