from agentops.agents.loop import AgentLoop


class AnalystAgent:
    def __init__(self, agent_loop: AgentLoop) -> None:
        self.agent_loop = agent_loop

    def analyze(self, question: str) -> str:
        return self.agent_loop.run(
            system_prompt=(
                "You are a business analyst. "
                "Use the available analytical tools to investigate "
                "the user's question and provide a concise evidence-based answer."
            ),
            user_message=question,
        )