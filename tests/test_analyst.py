from agentops.agents.analyst import AnalystAgent
from agentops.llm.fake import FakeLLMProvider


def test_analyst_agent_uses_llm() -> None:
    llm = FakeLLMProvider(
        response="The data indicates resolution time increased."
    )

    agent = AnalystAgent(llm)

    result = agent.analyze(
        "Why did resolution time increase?"
    )

    assert "resolution time increased" in result