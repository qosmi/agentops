from agentops.models.agent_state import AgentState
from agentops.models.evidence import Evidence


def test_agent_state_has_defaults() -> None:
    state = AgentState(
        system_prompt="You are a business analyst."
    )

    assert state.messages == []
    assert state.iteration == 0
    assert state.final_answer is None
    assert state.observations == []
    assert state.evidence == []


def test_agent_state_stores_messages() -> None:
    state = AgentState(
        system_prompt="You are a business analyst.",
        messages=[
            {
                "role": "user",
                "content": "Why did resolution time increase?",
            }
        ],
    )

    assert len(state.messages) == 1
    assert state.messages[0]["role"] == "user"


def test_agent_state_can_store_final_answer() -> None:
    state = AgentState(
        system_prompt="You are a business analyst.",
        iteration=2,
        final_answer=(
            "Resolution time increased because of payment tickets."
        ),
    )

    assert state.iteration == 2
    assert (
        state.final_answer
        == "Resolution time increased because of payment tickets."
    )


def test_agent_state_can_store_evidence() -> None:
    evidence = Evidence(
        source="get_resolution_time",
        value={"payments": 6.0},
    )

    state = AgentState(
        system_prompt="You are a business analyst.",
        evidence=[evidence],
    )

    assert len(state.evidence) == 1
    assert state.evidence[0].source == "get_resolution_time"
    assert state.evidence[0].value == {"payments": 6.0}