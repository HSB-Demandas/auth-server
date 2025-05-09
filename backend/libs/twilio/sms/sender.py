from typing import Optional
import structlog

# Use absolute imports to match the test mocking pattern
from .config import TwilioConfig
from .client import TwilioClient
from .types import SMSDeliveryResult
from .exceptions import InvalidPhoneNumberError, TwilioError

logger = structlog.get_logger()


def send_sms(
    config: TwilioConfig,
    phone_number: str,
    message: str,
    sender_id: Optional[str] = None
) -> SMSDeliveryResult:
    """Send an SMS message using Twilio
    
    Args:
        config: TwilioConfig instance with account credentials
        phone_number: Recipient phone number (must start with +)
        message: SMS message content
        sender_id: Optional custom sender ID (must start with +)
        
    Returns:
        SMSDeliveryResult with status and metadata
        
    Raises:
        InvalidPhoneNumberError: If phone number format is invalid
    """
    logger.info("Sending SMS", phone_number=phone_number, sender_id=sender_id)
    # Validate phone number
    if not phone_number.startswith('+'):
        logger.warn("Invalid phone number format", phone_number=phone_number)
        raise InvalidPhoneNumberError(phone_number)
    
    try:
        logger.debug("Initializing TwilioClient for SMS sending", account_sid=config.account_sid)
        client = TwilioClient(config)
        
        logger.debug("Sending message via TwilioClient", to=phone_number, sender=sender_id or config.from_number)
        response = client.send_message(
            to=phone_number,
            body=message,
            from_=sender_id or config.from_number
        )
        logger.info("SMS sent successfully", phone_number=phone_number, sid=response.get('sid'))
        
        # Return success result
        return SMSDeliveryResult(
            success=True,
            message_sid=response.get('sid'),
            to=phone_number
        )
        
    except TwilioError as e:
        # Handle domain-specific errors
        logger.error("Error sending SMS", phone_number=phone_number, error=str(e), code=getattr(e, 'code', None))
        return SMSDeliveryResult(
            success=False,
            to=phone_number,
            error_code=e.code,
            error_message=str(e)
        )
        
    except Exception as e:
        # Handle unexpected errors
        logger.error("Unexpected error sending SMS", phone_number=phone_number, error=str(e))
        return SMSDeliveryResult(
            success=False,
            to=phone_number,
            error_code="UNKNOWN_ERROR",
            error_message=str(e)
        )
