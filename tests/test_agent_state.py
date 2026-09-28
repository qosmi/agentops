from agentops.models.agent_state import AgentState


def test_agent_state_has_defaults() -> None:
    state = AgentState(
        system_prompt="You are a business analyst."
    )

    assert state.messages == []
    assert state.iteration == 0
    assert state.final_answer is None


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
        final_answer="Resolution time increased because of payment tickets.",
    )

    assert state.iteration == 2
    assert (
        state.final_answer
        == "Resolution time increased because of payment tickets."
    )