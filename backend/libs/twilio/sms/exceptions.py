from typing import Optional


class TwilioError(Exception):
    """Base exception for Twilio service errors"""

    def __init__(self, message: str, code: Optional[str] = None):
        self.code = code
        super().__init__(message)


class InvalidPhoneNumberError(TwilioError):
    """Raised when phone number is invalid"""

    def __init__(self, phone: str):
        self.phone = phone
        super().__init__(f"Invalid phone number: {phone}", code="INVALID_PHONE")


class TokenExpiredError(TwilioError):
    """Raised when verification token has expired"""

    def __init__(self):
        super().__init__("Verification token has expired", code="TOKEN_EXPIRED")


class VerificationFailedError(TwilioError):
    """Raised when verification fails"""

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(f"Verification failed: {reason}", code="VERIFICATION_FAILED")


class TwilioAPIError(TwilioError):
    """Raised when Twilio API returns an error"""

    def __init__(self, message: str, twilio_code: str):
        self.twilio_code = twilio_code
        super().__init__(f"Twilio API Error: {message}", code="TWILIO_API_ERROR")


class RateLimitError(TwilioError):
    """Raised when rate limit is exceeded"""

    def __init__(self, message: str, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded: {message}", code="RATE_LIMIT_EXCEEDED")
