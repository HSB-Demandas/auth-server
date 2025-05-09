from unittest.mock import patch

import pytest

from libs.twilio.sms.exceptions import InvalidPhoneNumberError
from libs.twilio.sms.types import (
    VerificationChannel, VerificationStatus, VerificationResult,
)
from libs.twilio.sms.verifier import start_verification, check_verification


def test_start_verification_success(mock_twilio_config_with_service, mock_twilio_client):
    """Test that start_verification successfully initiates verification"""
    # Setup mock to return 'pending' status
    mock_instance = mock_twilio_client.return_value
    verification = mock_instance.verify.v2.services.return_value.verifications.create.return_value
    verification.status = "pending"
    with patch('libs.twilio.sms.verifier.twilio.rest.Client', mock_twilio_client):
        result = start_verification(
            config=mock_twilio_config_with_service,
            phone_number="+1987654321"
        )

        # Verify client was initialized with correct credentials
        mock_twilio_client.assert_called_once_with(
            mock_twilio_config_with_service.account_sid,
            mock_twilio_config_with_service.auth_token
        )

        # Verify service was accessed with correct SID
        mock_instance = mock_twilio_client.return_value
        mock_instance.verify.v2.services.assert_called_once_with(
            mock_twilio_config_with_service.service_sid)

        # Verify verification was created with correct parameters
        service = mock_instance.verify.v2.services.return_value
        service.verifications.create.assert_called_once_with(
            to="+1987654321",
            channel="sms"
        )

        # Verify result
        assert isinstance(result, VerificationResult)
        assert result.success is True
        assert result.to == "+1987654321"
        assert result.status == VerificationStatus.PENDING
        assert result.error_code is None
        assert result.error_message is None


def test_start_verification_custom_channel(mock_twilio_config_with_service, mock_twilio_client):
    """Test that start_verification can use a custom channel"""
    with patch('libs.twilio.sms.verifier.twilio.rest.Client', mock_twilio_client):
        result = start_verification(
            config=mock_twilio_config_with_service,
            phone_number="+1987654321",
            channel=VerificationChannel.CALL
        )

        # Verify verification was created with correct channel
        mock_instance = mock_twilio_client.return_value
        service = mock_instance.verify.v2.services.return_value
        service.verifications.create.assert_called_once_with(
            to="+1987654321",
            channel="call"
        )


def test_start_verification_invalid_phone(mock_twilio_config_with_service):
    """Test that start_verification validates phone numbers"""
    with pytest.raises(InvalidPhoneNumberError) as excinfo:
        start_verification(
            config=mock_twilio_config_with_service,
            phone_number="1987654321"  # Missing + prefix
        )
    assert "invalid phone number" in str(excinfo.value).lower()
    assert excinfo.value.phone == "1987654321"


def test_start_verification_missing_service_sid(mock_twilio_config):
    """Test that start_verification raises ValueError if service_sid is missing"""
    with pytest.raises(ValueError) as excinfo:
        start_verification(
            config=mock_twilio_config,  # No service_sid
            phone_number="+1987654321"
        )
    assert "service sid" in str(excinfo.value).lower()


def test_start_verification_twilio_exception(mock_twilio_config_with_service, mock_twilio_client):
    """Test that start_verification handles TwilioRestException (rate limit and other)"""
    from twilio.base.exceptions import TwilioRestException
    # Mock TwilioRestException for rate limit
    rate_limit_exc = TwilioRestException("429 Too Many Requests", 20429)
    mock_instance = mock_twilio_client.return_value
    mock_instance.verify.v2.services.return_value.verifications.create.side_effect = rate_limit_exc
    with patch('libs.twilio.sms.verifier.twilio.rest.Client', mock_twilio_client):
        result = start_verification(
            config=mock_twilio_config_with_service,
            phone_number="+1987654321"
        )
        assert result.success is False
        assert result.error_code == "TWILIO_API_ERROR"

    # Mock TwilioRestException for other error
    other_exc = TwilioRestException("Twilio error", 99999)
    mock_instance.verify.v2.services.return_value.verifications.create.side_effect = other_exc
    with patch('libs.twilio.sms.verifier.twilio.rest.Client', mock_twilio_client):
        result = start_verification(
            config=mock_twilio_config_with_service,
            phone_number="+1987654321"
        )
        assert result.success is False
        assert result.error_code == "TWILIO_API_ERROR"


def test_start_verification_generic_exception(mock_twilio_config_with_service, mock_twilio_client):
    """Test that start_verification handles unexpected exceptions"""
    mock_instance = mock_twilio_client.return_value
    mock_instance.verify.v2.services.return_value.verifications.create.side_effect = Exception("Generic error")
    with patch('libs.twilio.sms.verifier.twilio.rest.Client', mock_twilio_client):
        result = start_verification(
            config=mock_twilio_config_with_service,
            phone_number="+1987654321"
        )
        assert result.success is False
        assert result.error_code == "TWILIO_API_ERROR"


def test_check_verification_success(mock_twilio_config_with_service, mock_twilio_client):
    """Test that check_verification successfully validates a code"""
    # Setup mock to return 'approved' status
    mock_instance = mock_twilio_client.return_value
    verification_check = mock_instance.verify.v2.services.return_value.verification_checks.create.return_value
    verification_check.status = "approved"
    with patch('libs.twilio.sms.verifier.twilio.rest.Client', mock_twilio_client):
        status = check_verification(
            config=mock_twilio_config_with_service,
            phone_number="+1987654321",
            code="123456"
        )

        # Verify verification check was created with correct parameters
        mock_instance = mock_twilio_client.return_value
        service = mock_instance.verify.v2.services.return_value
        service.verification_checks.create.assert_called_once_with(
            to="+1987654321",
            code="123456"
        )

        # Verify status
        assert status == VerificationStatus.APPROVED


def test_check_verification_missing_service_sid(mock_twilio_config):
    """Test that check_verification raises ValueError if service_sid is missing"""
    with pytest.raises(ValueError) as excinfo:
        check_verification(
            config=mock_twilio_config,  # No service_sid
            phone_number="+1987654321",
            code="123456"
        )
    assert "service sid" in str(excinfo.value).lower()


def test_check_verification_twilio_exception(mock_twilio_config_with_service, mock_twilio_client):
    """Test that check_verification handles TwilioRestException (rate limit and other)"""
    from twilio.base.exceptions import TwilioRestException
    # Mock TwilioRestException for rate limit
    rate_limit_exc = TwilioRestException("429 Too Many Requests", 20429)
    mock_instance = mock_twilio_client.return_value
    mock_instance.verify.v2.services.return_value.verification_checks.create.side_effect = rate_limit_exc
    with patch('libs.twilio.sms.verifier.twilio.rest.Client', mock_twilio_client):
        with pytest.raises(Exception) as excinfo:
            check_verification(
                config=mock_twilio_config_with_service,
                phone_number="+1987654321",
                code="123456"
            )
        assert "429" in str(excinfo.value) or "rate limit" in str(excinfo.value).lower()

    # Mock TwilioRestException for other error
    other_exc = TwilioRestException("Twilio error", 99999)
    mock_instance.verify.v2.services.return_value.verification_checks.create.side_effect = other_exc
    with patch('libs.twilio.sms.verifier.twilio.rest.Client', mock_twilio_client):
        with pytest.raises(Exception) as excinfo:
            check_verification(
                config=mock_twilio_config_with_service,
                phone_number="+1987654321",
                code="123456"
            )
        assert "twilio error" in str(excinfo.value).lower()


def test_check_verification_generic_exception(mock_twilio_config_with_service, mock_twilio_client):
    """Test that check_verification handles unexpected exceptions and raises TwilioAPIError with code VERIFICATION_CHECK_ERROR"""
    from libs.twilio.sms.exceptions import TwilioAPIError
    mock_instance = mock_twilio_client.return_value
    mock_instance.verify.v2.services.return_value.verification_checks.create.side_effect = Exception("Generic error")
    with patch('libs.twilio.sms.verifier.twilio.rest.Client', mock_twilio_client):
        with pytest.raises(TwilioAPIError) as excinfo:
            check_verification(
                config=mock_twilio_config_with_service,
                phone_number="+1987654321",
                code="123456"
            )
        assert excinfo.value.code == "TWILIO_API_ERROR"
        assert "generic error" in str(excinfo.value).lower()


def test_check_verification_failed(mock_twilio_config_with_service, mock_twilio_client):
    """Test that check_verification handles failed verification"""
    # Setup mock to return failed status
    mock_instance = mock_twilio_client.return_value
    verification_check = mock_instance.verify.v2.services.return_value.verification_checks.create.return_value
    verification_check.status = "canceled"

    with patch('libs.twilio.sms.verifier.twilio.rest.Client', mock_twilio_client):
        status = check_verification(
            config=mock_twilio_config_with_service,
            phone_number="+1987654321",
            code="123456"
        )

        # Verify status
        assert status == VerificationStatus.CANCELED
