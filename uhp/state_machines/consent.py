from uhp.enums.consent_state import ConsentState
from typing import Dict, Set

class ConsentStateMachine:
    _VALID_TRANSITIONS: Dict[ConsentState, Set[ConsentState]] = {
        ConsentState.GRANTED: {ConsentState.DENIED, ConsentState.REVOKED},
        ConsentState.DENIED: {ConsentState.REVOKED},
        ConsentState.REVOKED: set(),
        ConsentState.PENDING: {ConsentState.GRANTED, ConsentState.DENIED}
    }

    @staticmethod
    def can_transition(current_state: ConsentState, new_state: ConsentState) -> bool:
        """
        Checks if a transition from current_state to new_state is valid.
        """
        return new_state in ConsentStateMachine._VALID_TRANSITIONS.get(current_state, set())
