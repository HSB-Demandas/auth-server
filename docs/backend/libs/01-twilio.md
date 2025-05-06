

# 📦 Twilio Library — `libs.twilio_sms`

This module provides a structured, testable wrapper around the Twilio SDK for sending SMS messages and handling token-based verification (e.g., MFA flows).

---

## 📁 Module Structure

```
libs/
└── twilio/
    └── SMS/
        ├── __init__.py
        ├── config.py            # Defines TwilioConfig for injected credentials
        ├── client.py            # Initializes the Twilio REST client
        ├── sender.py            # Sends SMS messages
        ├── verifier.py          # Starts and checks verification flows
        ├── exceptions.py        # Domain-specific error handling
        ├── types.py             # Custom types for results/status
        └── tests/
            ├── unit/
            │   ├── test_sender.py
            │   ├── test_verifier.py
            │   └── test_exceptions.py
            └── integration/
                ├── test_send_sms_real.py
                └── test_validate_token_real.py
```

---

## ⚙️ Components Description

### `config.py`
- Contains `TwilioConfig` dataclass:
  - `account_sid: str`
  - `auth_token: str`
  - `service_sid: str` (used for verification)
- These values must be passed from the application (not read via `os.environ`).

### `client.py`
- Initializes a Twilio client using `TwilioConfig`.
- Exposes the raw client internally to `sender` and `verifier`.

### `sender.py`
- Provides a façade function:
  ```python
  def send_sms(phone_number: str, message: str) -> SMSDeliveryResult
  ```
- Returns a domain object or result type.

### `verifier.py`
- Two façade functions:
  ```python
  def start_verification(phone_number: str) -> VerificationResult
  def check_verification(phone_number: str, code: str) -> VerificationStatus
  ```

### `exceptions.py`
- Maps Twilio errors into project-friendly exceptions like:
  - `InvalidPhoneNumberError`
  - `TokenExpiredError`
  - `VerificationFailedError`

---

## ✅ Testing Strategy (TDD)

### 🔹 Unit Tests

#### `test_sender.py`
- Should successfully send SMS with mocked client
- Should raise domain errors for invalid numbers or SDK failures
- Should simulate retryable exceptions

#### `test_verifier.py`
- Should simulate verification start (mocked)
- Should simulate valid and invalid code checks
- Should handle expired tokens

#### `test_exceptions.py`
- Ensures proper mapping of Twilio exceptions

---

### 🔸 Integration Tests (disabled by default)

#### `test_send_sms_real.py`
- Sends a real SMS using Twilio sandbox/test credentials
- Verifies HTTP 2XX response and valid SID

#### `test_validate_token_real.py`
- Starts and checks verification on a real device (manual test flow)
- Tests both correct and incorrect token input

---

## 🔐 Environment Variables

These variables should be set in the application and passed into the library:

| Variable Name      | Purpose                          | Required | Default |
|--------------------|----------------------------------|----------|---------|
| `TWILIO_ACCOUNT_SID` | Twilio account SID               | ✅       | —       |
| `TWILIO_AUTH_TOKEN`  | Twilio auth token                | ✅       | —       |
| `TWILIO_SERVICE_SID` | Twilio Verify service SID        | ✅       | —       |

Note: These should be injected via `TwilioConfig` and never accessed using `os.environ` inside the library.

---
