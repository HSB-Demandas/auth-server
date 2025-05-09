import os

import pytest
import structlog
from pydantic import BaseModel, Field

from libs.twilio.sms.config import TwilioConfig
from libs.twilio.sms.types import VerificationStatus
from libs.twilio.sms.verifier import start_verification, check_verification

logger = structlog.get_logger()


class IntegrationConfig(BaseModel):
    account_sid: str = Field(...)
    auth_token: str = Field(...)
    from_number: str = Field(...)
    service_sid: str = Field(...)
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
            service_sid=os.environ["TWILIO_SERVICE_SID"],
            test_phone=os.environ["TWILIO_TEST_PHONE"]
        )
        logger.info("Loaded integration config")
        return config
    except KeyError as e:
        pytest.skip(f"Missing required environment variable: {e}")


@pytest.mark.integration
def test_verification_start_real(integration_config):
    """Start a verification and assert it is pending."""
    config = TwilioConfig(
        account_sid=integration_config.account_sid,
        auth_token=integration_config.auth_token,
        from_number=integration_config.from_number,
        service_sid=integration_config.service_sid
    )
    logger.info("Starting integration verification", to=integration_config.test_phone)
    start_result = start_verification(config, integration_config.test_phone)
    logger.info("Started verification", result=start_result)
    assert start_result.success is True
    assert start_result.status == VerificationStatus.PENDING

@pytest.mark.integration
def test_verification_check_real(integration_config):
    """Check a verification code and assert the result is terminal (not pending)."""
    config = TwilioConfig(
        account_sid=integration_config.account_sid,
        auth_token=integration_config.auth_token,
        from_number=integration_config.from_number,
        service_sid=integration_config.service_sid
    )
    code = os.getenv("TWILIO_TEST_CODE")
    if not code:
        pytest.skip(
            "No verification code provided via TWILIO_TEST_CODE env var. Check your phone and set the code."
        )
    logger.info("Checking verification with code", code=code)
    status = check_verification(config, integration_config.test_phone, code)
    logger.info("Verification check result", status=status)
    assert status in {VerificationStatus.APPROVED, VerificationStatus.FAILED, VerificationStatus.CANCELED}
