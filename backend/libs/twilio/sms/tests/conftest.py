import pytest
from unittest.mock import patch, MagicMock

from libs.twilio.sms.config import TwilioConfig
from libs.twilio.sms.exceptions import TwilioAPIError


@pytest.fixture
def mock_twilio_config():
    """Common fixture for TwilioConfig instance"""
    return TwilioConfig(
        account_sid="AC123456789",
        auth_token="auth_token_123",
        from_number="+1234567890"
    )


@pytest.fixture
def mock_twilio_config_with_service():
    """TwilioConfig instance with service_sid for verification tests"""
    return TwilioConfig(
        account_sid="AC123456789",
        auth_token="auth_token_123",
        from_number="+1234567890",
        service_sid="VA123456789"
    )


@pytest.fixture
def mock_twilio_client():
    """Mock for twilio.rest.Client used in client.py"""
    with patch('twilio.rest.Client') as mock_client:
        # Setup mock client instance
        instance = mock_client.return_value
        instance.messages = MagicMock()
        instance.verify = MagicMock()
        instance.verify.v2 = MagicMock()
        instance.verify.v2.services = MagicMock()
        yield mock_client


@pytest.fixture
def mock_twilio_client_for_sender():
    """Mock for TwilioClient used in sender.py"""
    with patch('libs.twilio.sms.sender.TwilioClient') as mock_client_class:
        mock_instance = mock_client_class.return_value
        mock_instance.send_message.return_value = {
            "sid": "SM123456",
            "status": "queued",
            "to": "+1987654321"
        }
        yield mock_client_class


@pytest.fixture
def mock_twilio_client_for_verifier():
    """Mock for twilio.rest.Client used in verifier.py"""
    with patch('libs.twilio.sms.verifier.twilio.rest.Client') as mock_client:
        # Setup mock client instance
        instance = mock_client.return_value
        
        # Mock verify service
        verify_service = MagicMock()
        instance.verify.v2.services.return_value = verify_service
        
        # Mock verification creation
        verification_creation = MagicMock()
        verify_service.verifications.create.return_value = verification_creation
        verification_creation.status = "pending"
        
        # Mock verification check
        verification_check = MagicMock()
        verify_service.verification_checks.create.return_value = verification_check
        verification_check.status = "approved"
        
        yield mock_client
