from datetime import datetime

class UHPError(Exception):
    """Base exception for all UHP related errors."""
    pass

class InvalidStateTransition(UHPError):
    """
    Exception raised for invalid state transitions.
    Attributes:
        current_state -- current state of the object
        new_state -- attempted new state
        message -- explanation of the error
    """
    def __init__(self, current_state: str, new_state: str, message: str = "Invalid state transition."):
        self.current_state = current_state
        self.new_state = new_state
        self.message = f"{message} Cannot transition from {current_state} to {new_state}."
        super().__init__(self.message)

class InvalidStateTransitionError(UHPError):
    """
    Exception raised for invalid state transitions based on an action.
    Attributes:
        current_state -- current state of the object
        intended_action -- the action that was attempted
        message -- explanation of the error
    """
    def __init__(self, current_state: str, intended_action: str, message: str = "Action not allowed."):
        self.current_state = current_state
        self.intended_action = intended_action
        self.message = f"{message} Cannot perform {intended_action} from state {current_state}."
        super().__init__(self.message)

class PrivacyViolation(UHPError):
    """
    Exception raised for privacy violations.
    Attributes:
        field -- the data field that was accessed or attempted to be accessed
        reason -- why the access was a violation (e.g., "access_without_consent")
        message -- explanation of the error
    """
    def __init__(self, field: str, reason: str, message: str = "Privacy violation detected."):
        self.field = field
        self.reason = reason
        self.message = f"{message} Field '{field}' accessed due to '{reason}'."
        super().__init__(self.message)

class ConsentExpired(UHPError):
    """
    Exception raised when an operation requires consent that has expired.
    Attributes:
        consent_id -- the ID of the expired consent
        expiration_date -- the date/time when the consent expired
        message -- explanation of the error
    """
    def __init__(self, consent_id: str, expiration_date: datetime, message: str = "Consent has expired."):
        self.consent_id = consent_id
        self.expiration_date = expiration_date
        self.message = f"{message} Consent '{consent_id}' expired on {expiration_date.isoformat()}."
        super().__init__(self.message)
