import pytest

from agentops.tools.base import Tool
from agentops.tools.registry import ToolRegistry


class FakeTool(Tool):
    name = "fake_tool"
    description = "A fake tool"

    def execute(self, arguments):
        return {"ok": True}


def test_tool_can_be_registered() -> None:
    registry = ToolRegistry()

    tool = FakeTool()

    registry.register(tool)

    assert registry.get("fake_tool") is tool


def test_unknown_tool_fails() -> None:
    registry = ToolRegistry()

    with pytest.raises(ValueError):
        registry.get("does_not_exist")