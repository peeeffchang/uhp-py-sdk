from uhp.enums.consent_state import ConsentState
from uhp.enums.intent import IntentType
from uhp.state_machines.base import UhpStateMachine
from uhp.errors import InvalidStateTransitionError # Import the new error

class ConsentStateMachine(UhpStateMachine):
    """
    Manages the state transitions for UHP Consent objects.
    Inherits from UhpStateMachine to enforce valid transitions based on defined actions.
    """
    def __init__(self, current_state: ConsentState = ConsentState.PENDING):
        super().__init__()
        self.current_state = current_state
        self.transition_map = {
            ConsentState.PENDING: [IntentType.PROPOSE_CONSENT],
            ConsentState.GRANTED: [IntentType.REVOKE_CONSENT],
            ConsentState.DENIED: [IntentType.REVOKE_CONSENT],
            ConsentState.REVOKED: []
        }

    def propose_consent(self, grant: bool):
        """
        Proposes a consent action, leading to GRANTED or DENIED state from PENDING.
        Args:
            grant (bool): True to grant consent, False to deny.
        """
        self._enforce_transition(IntentType.PROPOSE_CONSENT)
        # The transition map only checks if the action itself is allowed from the current state.
        # The resulting state change is handled within the action method.
        if self.current_state == ConsentState.PENDING:
            if grant:
                self.current_state = ConsentState.GRANTED
            else:
                self.current_state = ConsentState.DENIED
        else:
            # This case should ideally be caught by _enforce_transition, but a defensive check is good
            raise InvalidStateTransitionError(
                current_state=self.current_state,
                intended_action=IntentType.PROPOSE_CONSENT,
                message=f"Cannot propose consent from state {self.current_state}."
            )

    def revoke_consent(self):
        """
        Revokes an existing consent, leading to REVOKED state.
        Valid from GRANTED or DENIED states.
        """
        self._enforce_transition(IntentType.REVOKE_CONSENT)
        self.current_state = ConsentState.REVOKED
