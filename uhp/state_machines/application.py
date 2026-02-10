from uhp.enums.application_state import ApplicationState
from typing import Dict, Set

class ApplicationStateMachine:
    _VALID_TRANSITIONS: Dict[ApplicationState, Set[ApplicationState]] = {
        ApplicationState.DRAFT: {ApplicationState.SUBMITTED},
        ApplicationState.SUBMITTED: {ApplicationState.SCREENING, ApplicationState.REVIEW, ApplicationState.ACCEPTED, ApplicationState.REJECTED, ApplicationState.WITHDRAWN},
        ApplicationState.SCREENING: {ApplicationState.REVIEW, ApplicationState.REJECTED, ApplicationState.WITHDRAWN},
        ApplicationState.REVIEW: {ApplicationState.ACCEPTED, ApplicationState.REJECTED, ApplicationState.WITHDRAWN},
        ApplicationState.ACCEPTED: {ApplicationState.WITHDRAWN},
        ApplicationState.REJECTED: set(),
        ApplicationState.WITHDRAWN: set()
    }

    @staticmethod
    def can_transition(current_state: ApplicationState, new_state: ApplicationState) -> bool:
        """
        Checks if a transition from current_state to new_state is valid.
        """
        return new_state in ApplicationStateMachine._VALID_TRANSITIONS.get(current_state, set())
