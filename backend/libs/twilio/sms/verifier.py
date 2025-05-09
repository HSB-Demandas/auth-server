import structlog

import twilio.rest

from .config import TwilioConfig
from .exceptions import InvalidPhoneNumberError, TwilioAPIError, TwilioError
from .types import VerificationChannel, VerificationStatus, VerificationResult

logger = structlog.get_logger()


def start_verification(
    config: TwilioConfig,
    phone_number: str,
    channel: VerificationChannel = VerificationChannel.SMS
) -> VerificationResult:
    """Start a verification process using Twilio Verify
    
    Args:
        config: TwilioConfig instance with account credentials
        phone_number: Recipient phone number (must start with +)
        channel: Verification channel (SMS, call, or email)
        
    Returns:
        VerificationResult with status and metadata
        
    Raises:
        InvalidPhoneNumberError: If phone number format is invalid
        TwilioAPIError: If the Twilio API returns an error
    """
    logger.info("Starting verification", phone_number=phone_number, channel=channel.value)
    # Validate phone number
    if not phone_number.startswith('+'):
        logger.warn("Invalid phone number format", phone_number=phone_number)
        raise InvalidPhoneNumberError(phone_number)  # pragma: no cover

    # Validate service SID
    if not config.service_sid:
        logger.error("Missing service SID in config", config=config)
        raise ValueError("Service SID is required for verification")

    try:
        logger.debug("Initializing Twilio client", account_sid=config.account_sid)
        client = twilio.rest.Client(config.account_sid, config.auth_token)
        service = client.verify.v2.services(config.service_sid)

        logger.debug("Creating verification via Twilio API", to=phone_number, channel=channel.value)
        verification = service.verifications.create(
            to=phone_number, channel=channel.value
        )

        # Map status to enum
        status = _map_verification_status(verification.status)
        logger.info("Verification started", phone_number=phone_number, status=verification.status)

        # Return result
        return VerificationResult(
            success=True,
            to=phone_number,
            status=status
        )

    except TwilioError as e:
        # Handle domain-specific errors
        logger.error("Error starting verification", phone_number=phone_number, error=str(e), code=getattr(e, 'code', None)) # pragma: no cover
        return VerificationResult(
            success=False,
            to=phone_number,
            status=VerificationStatus.FAILED,
            error_code=e.code,
            error_message=str(e)
        )  # pragma: no cover

    except Exception as e:
        # Handle unexpected errors
        logger.error("Unexpected error starting verification", phone_number=phone_number, error=str(e))  # pragma: no cover
        error = TwilioAPIError(str(e), "UNKNOWN")  # pragma: no cover
        return VerificationResult(
            success=False,
            to=phone_number,
            status=VerificationStatus.FAILED,
            error_code=error.code,
            error_message=str(error)
        )


def check_verification(
        config: TwilioConfig,
        phone_number: str,
        code: str
) -> VerificationStatus:
    """Check a verification code using Twilio Verify
    
    Args:
        config: TwilioConfig instance with account credentials
        phone_number: Recipient phone number (must start with +)
        code: Verification code to check
        
    Returns:
        VerificationStatus indicating the result
        
    Raises:
        InvalidPhoneNumberError: If phone number format is invalid
        TwilioAPIError: If the Twilio API returns an error
    """
    logger.info("Checking verification", phone_number=phone_number)
    # Validate phone number
    if not phone_number.startswith('+'):
        logger.warn("Invalid phone number format", phone_number=phone_number)   # pragma: no cover
        raise InvalidPhoneNumberError(phone_number)  # pragma: no cover

    # Validate service SID
    if not config.service_sid:
        logger.error("Missing service SID in config", config=config)
        raise ValueError("Service SID is required for verification")

    try:
        logger.debug("Initializing Twilio client for verification check", account_sid=config.account_sid)
        client = twilio.rest.Client(config.account_sid, config.auth_token)

        logger.debug("Checking verification via Twilio API", to=phone_number, code=code)
        verification_check = client.verify.v2.services(
            config.service_sid).verification_checks.create(
            to=phone_number,
            code=code
        )

        # Map status to enum and return
        logger.info("Verification checked", phone_number=phone_number, status=verification_check.status)
        return _map_verification_status(verification_check.status)

    except Exception as e:
        # Handle errors
        logger.error("Error checking verification", phone_number=phone_number, error=str(e))  # pragma: no cover
        raise TwilioAPIError(str(e), "VERIFICATION_CHECK_ERROR")  # pragma: no cover


def _map_verification_status(status: str) -> VerificationStatus:
    """Map Twilio status string to VerificationStatus enum"""
    status_map = {
        "pending": VerificationStatus.PENDING,
        "approved": VerificationStatus.APPROVED,
        "canceled": VerificationStatus.CANCELED,
        "failed": VerificationStatus.FAILED
    }
    return status_map.get(status, VerificationStatus.FAILED)
