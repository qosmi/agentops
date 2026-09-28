from agentops.agents.analyst import AnalystAgent
from agentops.agents.loop import AgentLoop
from agentops.llm.fake import FakeLLMProvider
from agentops.models.agent_config import AgentConfig
from agentops.models.agent_response import AgentResponse
from agentops.tools.registry import ToolRegistry


def test_analyst_agent_uses_llm() -> None:
    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="The data indicates resolution time increased."
            )
        ]
    )

    agent_loop = AgentLoop(
        llm=llm,
        tools=ToolRegistry(),
        config=AgentConfig(
            max_iterations=5,
            allowed_tools=set(),
        ),
    )

    agent = AnalystAgent(
        agent_loop=agent_loop,
    )

    result = agent.analyze(
        "Why did resolution time increase?"
    )

    assert result == "The data indicates resolution time increased."
    assert llm.call_count == 1