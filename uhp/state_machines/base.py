from uhp.errors import InvalidStateTransitionError

class UhpStateMachine:
    """
    Base class for all UHP state machines.
    """
    def __init__(self):
        self.transition_map = {}
        self.current_state = None

    def _enforce_transition(self, action: str):
        """
        Checks if a transition is valid and raises an error if not.
        """
        allowed_actions = self.transition_map.get(self.current_state, [])
        if action not in allowed_actions:
            raise InvalidStateTransitionError(
                current_state=self.current_state,
                intended_action=action,
                message=f"Action '{action}' is not allowed from state '{self.current_state}'."
            )
