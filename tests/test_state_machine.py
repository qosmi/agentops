import pytest

from agentops.models.investigation_state import InvestigationState
from agentops.services.state_machine import InvestigationStateMachine


def test_state_machine_starts_in_created_state() -> None:
    state_machine = InvestigationStateMachine()

    assert (
        state_machine.current_state
        == InvestigationState.CREATED
    )


def test_state_machine_allows_valid_transition() -> None:
    state_machine = InvestigationStateMachine()

    result = state_machine.transition(
        InvestigationState.PLANNING
    )

    assert result == InvestigationState.PLANNING
    assert (
        state_machine.current_state
        == InvestigationState.PLANNING
    )


def test_state_machine_rejects_invalid_transition() -> None:
    state_machine = InvestigationStateMachine()

    with pytest.raises(
        ValueError,
        match="Invalid investigation state transition",
    ):
        state_machine.transition(
            InvestigationState.COMPLETED
        )


def test_state_machine_supports_full_happy_path() -> None:
    state_machine = InvestigationStateMachine()

    state_machine.transition(
        InvestigationState.PLANNING
    )

    state_machine.transition(
        InvestigationState.INVESTIGATING
    )

    state_machine.transition(
        InvestigationState.VERIFYING
    )

    state_machine.transition(
        InvestigationState.COMPLETED
    )

    assert (
        state_machine.current_state
        == InvestigationState.COMPLETED
    )


def test_state_machine_allows_verification_retry() -> None:
    state_machine = InvestigationStateMachine()

    state_machine.transition(
        InvestigationState.PLANNING
    )

    state_machine.transition(
        InvestigationState.INVESTIGATING
    )

    state_machine.transition(
        InvestigationState.VERIFYING
    )

    state_machine.transition(
        InvestigationState.INVESTIGATING
    )

    assert (
        state_machine.current_state
        == InvestigationState.INVESTIGATING
    )


def test_completed_state_cannot_transition() -> None:
    state_machine = InvestigationStateMachine(
        initial_state=InvestigationState.COMPLETED,
    )

    with pytest.raises(
        ValueError,
        match="Invalid investigation state transition",
    ):
        state_machine.transition(
            InvestigationState.INVESTIGATING
        )


def test_failed_state_cannot_transition() -> None:
    state_machine = InvestigationStateMachine(
        initial_state=InvestigationState.FAILED,
    )

    with pytest.raises(
        ValueError,
        match="Invalid investigation state transition",
    ):
        state_machine.transition(
            InvestigationState.INVESTIGATING
        )


def test_investigation_can_fail_from_created() -> None:
    state_machine = InvestigationStateMachine()

    state_machine.transition(
        InvestigationState.FAILED
    )

    assert (
        state_machine.current_state
        == InvestigationState.FAILED
    )


def test_investigation_can_fail_from_planning() -> None:
    state_machine = InvestigationStateMachine()

    state_machine.transition(
        InvestigationState.PLANNING
    )

    state_machine.transition(
        InvestigationState.FAILED
    )

    assert (
        state_machine.current_state
        == InvestigationState.FAILED
    )


def test_investigation_can_fail_from_investigating() -> None:
    state_machine = InvestigationStateMachine()

    state_machine.transition(
        InvestigationState.PLANNING
    )

    state_machine.transition(
        InvestigationState.INVESTIGATING
    )

    state_machine.transition(
        InvestigationState.FAILED
    )

    assert (
        state_machine.current_state
        == InvestigationState.FAILED
    )


def test_investigation_can_fail_from_verifying() -> None:
    state_machine = InvestigationStateMachine()

    state_machine.transition(
        InvestigationState.PLANNING
    )

    state_machine.transition(
        InvestigationState.INVESTIGATING
    )

    state_machine.transition(
        InvestigationState.VERIFYING
    )

    state_machine.transition(
        InvestigationState.FAILED
    )

    assert (
        state_machine.current_state
        == InvestigationState.FAILED
    )