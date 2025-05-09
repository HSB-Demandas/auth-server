# Twilio SMS Library

A structured, testable wrapper around the Twilio SDK for SMS messaging and verification flows.

## Overview

This library provides a clean abstraction over the Twilio API for sending SMS messages and handling verification flows. It follows a consistent pattern of input validation, error handling, and structured result objects.

## Components

### Configuration (`config.py`)

Centralized configuration management for Twilio credentials:

```python
from backend.libs.twilio.sms.config import TwilioConfig

config = TwilioConfig(
    account_sid="your_account_sid",
    auth_token="your_auth_token",
    from_number="+1234567890",
    service_sid="your_service_sid"  # Optional, required for verification
)
```

### SMS Sender (`sender.py`)

Send SMS messages with proper error handling:

```python
from backend.libs.twilio.sms.config import TwilioConfig
from backend.libs.twilio.sms.sender import send_sms

config = TwilioConfig(
    account_sid="your_account_sid",
    auth_token="your_auth_token",
    from_number="+1234567890"
)

result = send_sms(
    config=config,
    phone_number="+1987654321",
    message="Your verification code is 123456"
)

if result.success:
    print(f"Message sent with SID: {result.message_sid}")
else:
    print(f"Error sending message: {result.error_message}")
```

### Verification (`verifier.py`)

Handle verification flows for phone numbers:

```python
from backend.libs.twilio.sms.config import TwilioConfig
from backend.libs.twilio.sms.verifier import start_verification, check_verification
from backend.libs.twilio.sms.types import VerificationChannel

config = TwilioConfig(
    account_sid="your_account_sid",
    auth_token="your_auth_token",
    from_number="+1234567890",
    service_sid="your_service_sid"  # Required for verification
)

# Start verification
result = start_verification(
    config=config,
    phone_number="+1987654321",
    channel=VerificationChannel.SMS  # Default is SMS
)

if result.success:
    print(f"Verification started with status: {result.status}")
    
    # Later, check the verification code
    status = check_verification(
        config=config,
        phone_number="+1987654321",
        code="123456"
    )
    
    if status == VerificationStatus.APPROVED:
        print("Verification successful!")
    else:
        print(f"Verification failed with status: {status}")
else:
    print(f"Error starting verification: {result.error_message}")
```

## Error Handling

The library provides domain-specific exceptions:

- `InvalidPhoneNumberError`: Raised when a phone number format is invalid
- `TokenExpiredError`: Raised when a verification token has expired
- `VerificationFailedError`: Raised when verification fails
- `TwilioAPIError`: Raised when the Twilio API returns an error
- `RateLimitError`: Raised when rate limits are exceeded

## Testing

The library is fully tested with unit tests. To run the tests:

```bash
python -m pytest backend/libs/twilio/sms/tests/unit/ -v
```

For integration testing with real Twilio credentials:

```bash
python -m pytest backend/libs/twilio/sms/tests/integration/ -v
```
