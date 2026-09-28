from agentops.models.agent_observation import AgentObservation


def test_agent_observation_stores_tool_execution() -> None:
    observation = AgentObservation(
        iteration=1,
        tool_name="get_resolution_time",
        arguments={"group_by": "product"},
        result={"payments": 6.0},
    )

    assert observation.iteration == 1
    assert observation.tool_name == "get_resolution_time"
    assert observation.arguments["group_by"] == "product"
    assert observation.result == {"payments": 6.0}