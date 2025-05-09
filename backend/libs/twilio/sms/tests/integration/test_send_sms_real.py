import os

import pytest
import structlog
from pydantic import BaseModel, Field

from libs.twilio.sms.config import TwilioConfig
from libs.twilio.sms.sender import send_sms

logger = structlog.get_logger()


class IntegrationConfig(BaseModel):
    account_sid: str = Field(...)
    auth_token: str = Field(...)
    from_number: str = Field(...)
    test_phone: str = Field(...)


@pytest.fixture(scope="module")
def integration_config():
    if not os.getenv("TWILIO_INTEGRATION"):
        pytest.skip(
            "Integration tests are disabled. Set TWILIO_INTEGRATION=1 to enable."
        )
    try:
        config = IntegrationConfig(
            account_sid=os.environ["TWILIO_ACCOUNT_SID"],
            auth_token=os.environ["TWILIO_AUTH_TOKEN"],
            from_number=os.environ["TWILIO_FROM_NUMBER"],
            test_phone=os.environ["TWILIO_TEST_PHONE"]
        )
        logger.info("Loaded integration config")
        return config
    except KeyError as e:
        pytest.skip(f"Missing required environment variable: {e}")


@pytest.mark.integration
def test_send_sms_real(integration_config):
    """Send a real SMS using Twilio (costs money!)"""
    config = TwilioConfig(
        account_sid=integration_config.account_sid,
        auth_token=integration_config.auth_token,
        from_number=integration_config.from_number
    )
    logger.info("Sending integration SMS", to=integration_config.test_phone)
    result = send_sms(
        config,
        integration_config.test_phone,
        "Integrations test message from Twilio SMS library."
    )
    logger.info("Integration SMS result", result=result)
    assert result.success is True
    assert result.to == integration_config.test_phone
    assert result.message_sid is not None
