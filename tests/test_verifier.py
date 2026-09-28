from agentops.agents.verifier import VerifierAgent
from agentops.models.agent_observation import AgentObservation


def test_verifier_accepts_answer_with_observations() -> None:
    verifier = VerifierAgent()

    observations = [
        AgentObservation(
            iteration=1,
            tool_name="get_resolution_time",
            arguments={"group_by": "product"},
            result={"payments": 6.0},
        )
    ]

    assert verifier.verify(
        "Payments increased.",
        observations,
    )