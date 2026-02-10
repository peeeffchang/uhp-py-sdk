from uhp.models.consent import Consent
from uhp.enums.consent_state import ConsentState

def assert_purpose_allowed(consent: Consent, purpose: str) -> bool:
    """
    Asserts if the given purpose is allowed based on the consent.
    This is a placeholder implementation.
    """
    if consent.state == ConsentState.GRANTED:
        return True
    return False # Fail closed by default
