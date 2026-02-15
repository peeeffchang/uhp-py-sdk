from uhp.enums.application_state import ApplicationState
from uhp.enums.intent import IntentType
from uhp.state_machines.base import UhpStateMachine

class ApplicationStateMachine(UhpStateMachine):
    """
    Manages the state transitions for a UHP Application.
    Inherits from UhpStateMachine to enforce valid transitions based on defined actions.
    """
    def __init__(self, current_state: ApplicationState = ApplicationState.DRAFT):
        super().__init__()
        self.current_state = current_state
        self.transition_map = {
            ApplicationState.DRAFT: [IntentType.APPLY_FOR_JOB],
            ApplicationState.SUBMITTED: [IntentType.WITHDRAW_APPLICATION],
            ApplicationState.SCREENING: [IntentType.WITHDRAW_APPLICATION],
            ApplicationState.REVIEW: [IntentType.WITHDRAW_APPLICATION],
            ApplicationState.ACCEPTED: [IntentType.WITHDRAW_APPLICATION],
            ApplicationState.REJECTED: [],
            ApplicationState.WITHDRAWN: []
        }

    def apply_for_job(self):
        """
        Attempts to apply for a job.
        Valid only from DRAFT state. Transitions to SUBMITTED.
        """
        self._enforce_transition(IntentType.APPLY_FOR_JOB)
        self.current_state = ApplicationState.SUBMITTED

    def withdraw_application(self):
        """
        Attempts to withdraw an application.
        Valid from SUBMITTED, SCREENING, REVIEW, ACCEPTED states. Transitions to WITHDRAWN.
        """
        self._enforce_transition(IntentType.WITHDRAW_APPLICATION)
        self.current_state = ApplicationState.WITHDRAWN
