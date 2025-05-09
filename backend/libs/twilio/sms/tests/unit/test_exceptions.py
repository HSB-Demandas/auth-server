import pytest

from libs.twilio.sms.exceptions import (
    TwilioError,
    InvalidPhoneNumberError,
    TokenExpiredError,
    VerificationFailedError,
    TwilioAPIError,
    RateLimitError
)


def test_base_exception():
    """Test the base TwilioError exception"""
    error = TwilioError("An error occurred")
    assert str(error) == "An error occurred"
    assert error.code is None
    
    error_with_code = TwilioError("An error occurred", code="ERROR_CODE")
    assert str(error_with_code) == "An error occurred"
    assert error_with_code.code == "ERROR_CODE"


def test_invalid_phone_number_error():
    """Test the InvalidPhoneNumberError exception"""
    error = InvalidPhoneNumberError("1234567890")
    assert "invalid phone number: 1234567890" in str(error).lower()
    assert error.code == "INVALID_PHONE"
    assert error.phone == "1234567890"


def test_token_expired_error():
    """Test the TokenExpiredError exception"""
    error = TokenExpiredError()
    assert "verification token has expired" in str(error).lower()
    assert error.code == "TOKEN_EXPIRED"


def test_verification_failed_error():
    """Test the VerificationFailedError exception"""
    error = VerificationFailedError("Invalid code")
    assert "verification failed: invalid code" in str(error).lower()
    assert error.code == "VERIFICATION_FAILED"
    assert error.reason == "Invalid code"


def test_twilio_api_error():
    """Test the TwilioAPIError exception"""
    error = TwilioAPIError("API Error", "30001")
    assert "twilio api error: api error" in str(error).lower()
    assert error.code == "TWILIO_API_ERROR"
    assert error.twilio_code == "30001"


def test_rate_limit_error():
    """Test the RateLimitError exception"""
    error = RateLimitError("Too many requests", retry_after=60)
    assert "rate limit exceeded: too many requests" in str(error).lower()
    assert error.code == "RATE_LIMIT_EXCEEDED"
    assert error.retry_after == 60
