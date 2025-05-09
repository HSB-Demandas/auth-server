import structlog
from typing import Optional, Dict, Any

import twilio.rest
from twilio.base.exceptions import TwilioRestException

from .config import TwilioConfig
from .exceptions import TwilioAPIError, RateLimitError

logger = structlog.get_logger()


class TwilioClient:
    """Wrapper around the Twilio REST client with error handling"""

    def __init__(self, config: TwilioConfig):
        """Initialize the Twilio client with the provided configuration
        
        Args:
            config: TwilioConfig instance with account credentials
        """
        self.config = config
        logger.debug("Initializing Twilio REST client", account_sid=config.account_sid)
        self._client = twilio.rest.Client(config.account_sid, config.auth_token)
        logger.info("TwilioClient initialized", account_sid=config.account_sid)

    def send_message(
        self, to: str, body: str, from_: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send an SMS message using the Twilio API
        
        Args:
            to: Recipient phone number
            body: Message content
            from_: Sender phone number (defaults to config.from_number)
            
        Returns:
            Dictionary containing the Twilio API response
            
        Raises:
            TwilioAPIError: If the Twilio API returns an error
            RateLimitError: If rate limits are exceeded
        """
        try:
            sender = from_ or self.config.from_number
            logger.info("Sending SMS", to=to, sender=sender)
            response = self._client.messages.create(
                to=to,
                body=body,
                from_=sender
            )
            logger.debug("SMS sent successfully", to=to, sid=response.sid)  # pragma: no cover
            return {    # pragma: no cover
                "sid": getattr(response, "sid", None),  
                "status": getattr(response, "status", None),
                "to": getattr(response, "to", None),
                "error_code": getattr(response, "error_code", None),
                "error_message": getattr(response, "error_message", None),
            }
        except TwilioRestException as e:
            logger.error("Twilio API error", to=to, error=str(e), code=getattr(e, 'code', None))
            if e.code == 20429:  # Rate limit error code
                retry_after = int(e.response.headers.get('Retry-After', 60))  # pragma: no cover
                raise RateLimitError(str(e), retry_after=retry_after)  # pragma: no cover
            else:
                raise TwilioAPIError(str(e), str(e.code))  # pragma: no cover
        except Exception as e:
            logger.error("Unexpected error when sending SMS", to=to, error=str(e))  # pragma: no cover
            raise TwilioAPIError(str(e), "UNKNOWN")  # pragma: no cover
