from typing import ClassVar

from agentops.models.investigation_state import InvestigationState


class InvestigationStateMachine:
    _transitions: ClassVar[
        dict[InvestigationState, set[InvestigationState]]
    ] = {
        InvestigationState.CREATED: {
            InvestigationState.PLANNING,
            InvestigationState.FAILED,
        },
        InvestigationState.PLANNING: {
            InvestigationState.INVESTIGATING,
            InvestigationState.FAILED,
        },
        InvestigationState.INVESTIGATING: {
            InvestigationState.VERIFYING,
            InvestigationState.FAILED,
        },
        InvestigationState.VERIFYING: {
            InvestigationState.COMPLETED,
            InvestigationState.INVESTIGATING,
            InvestigationState.FAILED,
        },
        InvestigationState.COMPLETED: set(),
        InvestigationState.FAILED: set(),
    }

    def __init__(
        self,
        initial_state: InvestigationState = InvestigationState.CREATED,
    ) -> None:
        self.current_state = initial_state

    def transition(
        self,
        new_state: InvestigationState,
    ) -> InvestigationState:
        allowed_states = self._transitions[self.current_state]

        if new_state not in allowed_states:
            raise ValueError(
                f"Invalid investigation state transition: "
                f"{self.current_state} -> {new_state}"
            )

        self.current_state = new_state

        return self.current_state