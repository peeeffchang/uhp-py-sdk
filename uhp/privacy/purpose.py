from uhp.models.consent import Consent
from uhp.enums.consent_state import ConsentState
from uhp.errors import PrivacyViolation

def assert_purpose_allowed(consent: Consent, purpose: str) -> bool:
    """
    Asserts if the given purpose is allowed based on the consent.
    Raises a PrivacyViolation if the purpose is not allowed.
    """
    if consent.state != ConsentState.GRANTED:
        raise PrivacyViolation(field="consent_state", reason=f"Consent '{consent.consent_id}' is not granted.")

    if not consent.purpose or purpose not in consent.purpose:
        raise PrivacyViolation(field="purpose", reason=f"Purpose '{purpose}' not granted in consent {consent.consent_id}")

    return True
