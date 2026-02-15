import pytest
from uhp.state_machines.base import UhpStateMachine
from uhp.errors import InvalidStateTransitionError

def test_uhp_state_machine_instantiation():
    """
    Tests that the base UhpStateMachine can be instantiated.
    """
    state_machine = UhpStateMachine()
    assert state_machine is not None

def test_enforce_transition_raises_error_for_invalid_transition():
    """
    Tests that the enforcement logic raises an error for an invalid transition.
    """
    class DummyStateMachine(UhpStateMachine):
        def __init__(self, current_state):
            super().__init__()
            self.current_state = current_state
            self.transition_map = {
                "STATE_A": ["ACTION_B"],
            }

        def perform_action(self, action):
            self._enforce_transition(action)
            # state transition logic would be here
            pass

    state_machine = DummyStateMachine(current_state="STATE_A")

    with pytest.raises(InvalidStateTransitionError) as excinfo:
        state_machine.perform_action("INVALID_ACTION")

    assert "Cannot perform INVALID_ACTION from state STATE_A" in str(excinfo.value)
