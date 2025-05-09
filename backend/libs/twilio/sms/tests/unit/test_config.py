import pytest
from pydantic import ValidationError

from libs.twilio.sms.config import TwilioConfig


def test_twilio_config_creation():
    """Test that TwilioConfig can be created with valid parameters"""
    # Create with required parameters
    config = TwilioConfig(
        account_sid="AC123456789",
        auth_token="auth_token_123",
        from_number="+1234567890"
    )
    
    assert config.account_sid == "AC123456789"
    assert config.auth_token == "auth_token_123"
    assert config.from_number == "+1234567890"
    assert config.service_sid is None

    # Create with optional parameters
    config_with_optional = TwilioConfig(
        account_sid="AC123456789",
        auth_token="auth_token_123",
        from_number="+1234567890",
        service_sid="VA123456789"
    )
    
    assert config_with_optional.account_sid == "AC123456789"
    assert config_with_optional.auth_token == "auth_token_123"
    assert config_with_optional.from_number == "+1234567890"
    assert config_with_optional.service_sid == "VA123456789"


def test_twilio_config_validation():
    """Test that TwilioConfig validates input parameters"""
    # Test invalid phone number format
    with pytest.raises(ValidationError) as excinfo:
        TwilioConfig(
            account_sid="AC123456789",
            auth_token="auth_token_123",
            from_number="1234567890"  # Missing + prefix
        )
    assert "phone number must start with +" in str(excinfo.value).lower()
    
    # Test missing required fields
    with pytest.raises(ValidationError):
        TwilioConfig(
            account_sid="AC123456789",
            auth_token="auth_token_123"
            # Missing from_number
        )
    
    with pytest.raises(ValidationError):
        TwilioConfig(
            account_sid="AC123456789",
            # Missing auth_token
            from_number="+1234567890"
        )
    
    with pytest.raises(ValidationError):
        TwilioConfig(
            # Missing account_sid
            auth_token="auth_token_123",
            from_number="+1234567890"
        )
