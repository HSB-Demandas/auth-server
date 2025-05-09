import pytest

from libs.twilio.sms.sender import send_sms
from libs.twilio.sms.types import SMSDeliveryResult
from libs.twilio.sms.exceptions import InvalidPhoneNumberError, TwilioAPIError


def test_send_sms_success(mock_twilio_config, mock_twilio_client_for_sender):
    """Test that send_sms successfully sends an SMS"""
    result = send_sms(
        config=mock_twilio_config,
        phone_number="+1987654321",
        message="Test message"
    )
    
    # Verify client was initialized with config
    mock_twilio_client_for_sender.assert_called_once_with(mock_twilio_config)
    
    # Verify send_message was called with correct parameters
    mock_instance = mock_twilio_client_for_sender.return_value
    mock_instance.send_message.assert_called_once_with(
        to="+1987654321",
        body="Test message",
        from_=mock_twilio_config.from_number
    )
    
    # Verify result
    assert isinstance(result, SMSDeliveryResult)
    assert result.success is True
    assert result.message_sid == "SM123456"
    assert result.to == "+1987654321"
    assert result.error_code is None
    assert result.error_message is None


def test_send_sms_custom_sender(mock_twilio_config, mock_twilio_client_for_sender):
    """Test that send_sms can use a custom sender ID"""
    result = send_sms(
        config=mock_twilio_config,
        phone_number="+1987654321",
        message="Test message",
        sender_id="+1555123456"
    )
    
    # Verify send_message was called with custom sender ID
    mock_instance = mock_twilio_client_for_sender.return_value
    mock_instance.send_message.assert_called_once_with(
        to="+1987654321",
        body="Test message",
        from_="+1555123456"
    )


def test_send_sms_invalid_phone(mock_twilio_config):
    """Test that send_sms validates phone numbers"""
    with pytest.raises(InvalidPhoneNumberError) as excinfo:
        send_sms(
            config=mock_twilio_config,
            phone_number="1987654321",  # Missing + prefix
            message="Test message"
        )
    
    assert "invalid phone number" in str(excinfo.value).lower()
    assert excinfo.value.phone == "1987654321"


def test_send_sms_twilio_api_error(mock_twilio_config, mock_twilio_client_for_sender):
    """Test that send_sms handles TwilioAPIError from client"""
    from libs.twilio.sms.exceptions import TwilioAPIError
    mock_instance = mock_twilio_client_for_sender.return_value
    mock_instance.send_message.side_effect = TwilioAPIError("Twilio error", "30001")
    result = send_sms(
        config=mock_twilio_config,
        phone_number="+1987654321",
        message="Test message"
    )
    assert result.success is False
    assert result.error_code == "TWILIO_API_ERROR"
    assert "twilio error" in (result.error_message or "").lower()


def test_send_sms_generic_exception(mock_twilio_config, mock_twilio_client_for_sender):
    """Test that send_sms handles generic Exception from client"""
    mock_instance = mock_twilio_client_for_sender.return_value
    mock_instance.send_message.side_effect = Exception("Generic error")
    result = send_sms(
        config=mock_twilio_config,
        phone_number="+1987654321",
        message="Test message"
    )
    assert result.success is False
    assert result.error_code == "UNKNOWN_ERROR"
    assert "generic error" in (result.error_message or "").lower()


def test_send_sms_api_error(mock_twilio_config, mock_twilio_client_for_sender):
    """Test that send_sms handles API errors"""
    # Setup mock to raise an exception
    mock_instance = mock_twilio_client_for_sender.return_value
    mock_instance.send_message.side_effect = TwilioAPIError("API Error", "30001")
    
    result = send_sms(
        config=mock_twilio_config,
        phone_number="+1987654321",
        message="Test message"
    )
    
    # Verify error result
    assert isinstance(result, SMSDeliveryResult)
    assert result.success is False
    assert result.to == "+1987654321"
    assert result.message_sid is None
    assert result.error_code == "TWILIO_API_ERROR"
    assert "api error" in result.error_message.lower()
