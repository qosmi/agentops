from agentops.models.agent_observation import AgentObservation


class VerifierAgent:
    def verify(
        self,
        answer: str,
        observations: list[AgentObservation],
    ) -> bool:
        return bool(observations)