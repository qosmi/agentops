from agentops.llm.fake import FakeLLMProvider
from agentops.models.agent_response import AgentResponse


def test_fake_llm_returns_response() -> None:
    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="This is a test response."
            )
        ]
    )

    result = llm.generate(
        system_prompt="You are a test assistant.",
        messages=[],
    )

    assert result.message == "This is a test response."