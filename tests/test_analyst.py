from agentops.agents.analyst import AnalystAgent
from agentops.llm.fake import FakeLLMProvider
from agentops.models.agent_response import AgentResponse


def test_analyst_agent_uses_llm() -> None:
    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="The data indicates resolution time increased."
            )
        ]
    )

    agent = AnalystAgent(llm=llm)

    result = agent.analyze(
        "Why did resolution time increase?"
    )

    assert "resolution time increased" in result
    assert llm.call_count == 1