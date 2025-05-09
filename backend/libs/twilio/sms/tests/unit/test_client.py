import pytest

from libs.twilio.sms.client import TwilioClient
from libs.twilio.sms.exceptions import TwilioAPIError


def test_client_initialization(mock_twilio_config, mock_twilio_client):
    """Test that TwilioClient is properly initialized"""
    client = TwilioClient(mock_twilio_config)

    # Verify Twilio client was initialized with correct credentials
    mock_twilio_client.assert_called_once_with(
        mock_twilio_config.account_sid,
        mock_twilio_config.auth_token
    )

    # Verify client properties
    assert client.config == mock_twilio_config
    assert client._client is not None


def test_client_error_handling(mock_twilio_config, mock_twilio_client):
    """Test that TwilioClient handles API errors properly"""
    # Setup mock to raise an exception
    mock_instance = mock_twilio_client.return_value
    mock_instance.messages.create.side_effect = Exception("API Error")

    client = TwilioClient(mock_twilio_config)

    # Test that API errors are properly translated to our domain exceptions
    with pytest.raises(TwilioAPIError) as excinfo:
        client.send_message(
            to="+1234567890",
            body="Test message",
            from_=mock_twilio_config.from_number
        )
    assert "api error" in str(excinfo.value).lower()


def test_client_twilio_rest_exception_rate_limit(mock_twilio_config, mock_twilio_client):
    """Test that TwilioClient handles TwilioRestException with rate limit code"""
    from twilio.base.exceptions import TwilioRestException
    from libs.twilio.sms.exceptions import RateLimitError
    # Simulate a TwilioRestException with code 20429 and a mock response with Retry-After
    class DummyResponse:
        headers = {"Retry-After": "42"}
    exc = TwilioRestException("429 Too Many Requests", 20429)
    exc.response = DummyResponse()
    mock_instance = mock_twilio_client.return_value
    mock_instance.messages.create.side_effect = exc

    client = TwilioClient(mock_twilio_config)
    with pytest.raises(TwilioAPIError) as excinfo:
        client.send_message(
            to="+1234567890",
            body="Test message",
            from_=mock_twilio_config.from_number
        )
    assert excinfo.value.code == "TWILIO_API_ERROR"
    assert "429" in str(excinfo.value).lower() or "too many requests" in str(excinfo.value).lower()


def test_client_unexpected_exception(mock_twilio_config, mock_twilio_client):
    """Test that TwilioClient handles unexpected exceptions and raises TwilioAPIError with code UNKNOWN"""
    mock_instance = mock_twilio_client.return_value
    mock_instance.messages.create.side_effect = Exception("Totally unexpected!")

    client = TwilioClient(mock_twilio_config)
    with pytest.raises(TwilioAPIError) as excinfo:
        client.send_message(
            to="+1234567890",
            body="Test message",
            from_=mock_twilio_config.from_number
        )
    assert excinfo.value.code == "TWILIO_API_ERROR"
    assert "unexpected" in str(excinfo.value).lower()


def test_client_twilio_rest_exception_other_code(mock_twilio_config, mock_twilio_client):
    """Test that TwilioClient handles TwilioRestException with other code"""
    from twilio.base.exceptions import TwilioRestException
    exc = TwilioRestException("Twilio error", 99999)
    mock_instance = mock_twilio_client.return_value
    mock_instance.messages.create.side_effect = exc

    client = TwilioClient(mock_twilio_config)
    with pytest.raises(TwilioAPIError) as excinfo:
        client.send_message(
            to="+1234567890",
            body="Test message",
            from_=mock_twilio_config.from_number
        )
    assert "twilio error" in str(excinfo.value).lower() or "99999" in str(excinfo.value)
