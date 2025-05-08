

# 📦 Twilio Library — `libs.twilio_sms`

A structured, testable wrapper around the Twilio SDK for SMS messaging and verification flows.

---

## 📋 Table of Contents

- [Architecture](#architecture)
- [Module Structure](#module-structure)
- [Components](#components)
- [Testing Strategy](#testing-strategy)
- [Environment Variables](#environment-variables)
- [Usage Examples](#usage-examples)
- [Security Considerations](#security-considerations)

## 🏗 Architecture

### Core Principles

1. **Isolation**: No direct SDK access from application code
2. **Abstraction**: Clear façades for SMS and verification
3. **Error Handling**: Domain-specific exceptions
4. **Testability**: Mockable interfaces and integration points

## 📁 Module Structure

```
libs/
└── twilio/
    ├── __init__.py
    ├── config.py            # Configuration and settings
    ├── client.py            # SDK wrapper
    ├── sender.py            # SMS functionality
    ├── verifier.py          # Verification flows
    ├── exceptions.py        # Error handling
    ├── types.py             # Result types and enums
    └── tests/
        ├── unit/
        │   ├── test_sender.py
        │   ├── test_verifier.py
        │   └── test_exceptions.py
        └── integration/
            ├── test_send_sms_real.py
            └── test_validate_token_real.py
```

## ⚙️ Components

### 1. Configuration (`config.py`)

- **Purpose**: Centralized configuration management
- **Key Components**:
  - `TwilioConfig` dataclass
  - Configuration validation
  - Environment variable mapping

### 2. Client (`client.py`)

- **Purpose**: SDK wrapper with error handling
- **Features**:
  - Twilio REST client initialization
  - Request retry logic
  - Error translation

### 3. SMS Sender (`sender.py`)

- **Purpose**: SMS message handling
- **API**:
  ```python
  def send_sms(
      phone_number: str,
      message: str,
      sender_id: Optional[str] = None
  ) -> SMSDeliveryResult
  ```
- **Returns**: Result object with status and metadata

### 4. Verifier (`verifier.py`)

- **Purpose**: Token-based verification
- **API**:
  ```python
  def start_verification(
      phone_number: str,
      channel: VerificationChannel = VerificationChannel.SMS
  ) -> VerificationResult

  def check_verification(
      phone_number: str,
      code: str
  ) -> VerificationStatus
  ```

### 5. Error Handling (`exceptions.py`)

- **Purpose**: Domain-specific error abstraction
- **Exceptions**:
  - `InvalidPhoneNumberError`
  - `TokenExpiredError`
  - `VerificationFailedError`
  - `TwilioAPIError`
  - `RateLimitError`

## ✅ Testing Strategy

### Unit Tests

- **Core Logic**:
  - SMS sending flows
  - Verification workflows
  - Error handling
- **Test Coverage**:
  - 100% statement coverage
  - Edge case handling
  - Error scenarios

### Integration Tests

- **Real Integration**:
  - SMS sending
  - Token verification
  - Error handling
- **Requirements**:
  - Test credentials
  - Sandbox environment
  - Manual verification steps

## 🔐 Environment Variables

No direct environment variable access inside the library. Configuration must be passed through `TwilioConfig`.

If required by the consuming app, recommended environment variables:

| Variable Name     | Purpose                      | Required | Default |
|-------------------|------------------------------|----------|---------|
| `TWILIO_ACCOUNT_SID`  | Twilio account SID           | ✅       | —       |
| `TWILIO_AUTH_TOKEN`   | Twilio auth token            | ✅       | —       |
| `TWILIO_SERVICE_SID`  | Twilio verification service  | ❌       | —       |
| `TWILIO_SENDER_ID`    | Custom sender ID             | ❌       | —       |

## 🔄 Usage Examples

### Basic SMS Sending

```python
from libs.twilio.config import TwilioConfig
from libs.twilio.sender import send_sms

config = TwilioConfig(
    account_sid="your_account_sid",
    auth_token="your_auth_token"
)

result = send_sms(
    config=config,
    phone_number="+1234567890",
    message="Your verification code is 123456"
)
```

### Verification Flow

```python
from libs.twilio.config import TwilioConfig
from libs.twilio.verifier import start_verification, check_verification

config = TwilioConfig(
    account_sid="your_account_sid",
    auth_token="your_auth_token",
    service_sid="your_service_sid"
)

# Start verification
result = start_verification(
    config=config,
    phone_number="+1234567890",
    channel=VerificationChannel.SMS
)

# Check code
status = check_verification(
    config=config,
    phone_number="+1234567890",
    code="123456"
)
```

## 🛡 Security Considerations

- **Rate Limiting**: Built-in rate limiting for SMS and verification
- **Error Masking**: No sensitive information in error messages
- **Validation**: Strict phone number and token validation
- **Timeouts**: Secure timeouts for verification attempts
- **Logging**: Secure audit logging of all operations

---
