# 📦 Django App: `apps.django_hsb_twilio`

A reusable Django app for Twilio integration, supporting SMS delivery, verification, and webhook handling with proper error handling and rate limiting.

---

## 📋 Table of Contents

- [Architecture](#architecture)
- [Module Structure](#module-structure)
- [Components](#components)
- [Testing Strategy](#testing-strategy)
- [Environment Variables](#environment-variables)
- [Usage Examples](#usage-examples)
- [Security Considerations](#security-considerations)
- [Performance Considerations](#performance-considerations)

## 🏗 Architecture

### Core Principles

1. **Provider Integration**: Twilio SMS and verification services
2. **Event-Driven**: Webhook handling for status updates
3. **Rate Limiting**: Built-in protection
4. **Extensible**: Future service integration
5. **Error Handling**: Robust error management

## 📁 Module Structure

```
apps/
└── twilio/
    ├── __init__.py
    ├── apps.py
    ├── models.py              # SMSLog model for tracking messages
    ├── views.py               # API views for sending and receiving updates
    ├── urls.py                # Routes for endpoints and webhooks
    ├── serializers.py         # DRF serializers for validation
    ├── integrations/          # Uses libs.twilio_sms
    │   └── sender.py
    ├── services.py            # Core business logic
    ├── cache.py               # Optional cache handling for rate limit, retry
    ├── admin.py               # Admin integration (optional)
    ├── migrations/
    └── tests/
        ├── unit/
        │   ├── test_models.py
        │   ├── test_services.py
        │   └── test_views.py
        └── integration/
            ├── test_webhook.py
            └── test_verification.py
```

## ⚙️ Components

### 1. Models (`models.py`)

- **Purpose**: SMS tracking and persistence
- **Key Models**:
  - `SMSLog`: SMS delivery tracking
  - `VerificationSession`: Optional verification tracking
  - `WebhookEvent`: Optional webhook tracking

### 2. Services (`services.py`)

- **Purpose**: Core Twilio integration
- **Features**:
  - SMS sending
  - Verification flow
  - Webhook processing
  - Rate limiting
  - Error handling

### 3. API (`views.py` + `serializers.py`)

- **Purpose**: REST API endpoints
- **Endpoints**:
  - `/api/sms/send/` - Send SMS
  - `/api/sms/status/` - Get status
  - `/api/sms/verify/` - Verification endpoints
  - `/webhooks/sms/` - Webhook endpoint

### 4. Integration (`integrations/`)

- **Purpose**: Twilio library integration
- **Features**:
  - SMS sending
  - Verification
  - Status updates
  - Error handling

### 5. Error Handling (`exceptions.py`)

- **Purpose**: Domain-specific error abstraction
- **Exceptions**:
  - `TwilioError`
  - `VerificationError`
  - `RateLimitError`
  - `WebhookError`

## ✅ Testing Strategy

### Unit Tests

- **Core Logic**:
  - SMS sending
  - Verification flow
  - Webhook processing
  - Rate limiting
- **Test Coverage**:
  - 100% statement coverage
  - Edge case handling
  - Error scenarios
  - Rate limit testing

### Integration Tests

- **Internal Integration**:
  - Database operations
  - API endpoints
  - Webhook processing
  - Verification flow
- **External Integration**:
  - Twilio SMS integration
  - Webhook handling
  - Rate limiting
  - Error handling

## 🔐 Environment Variables

No direct environment variable access inside the app. All configuration must be passed through Django settings.

If required by the consuming app, recommended settings:

| Setting Name               | Purpose                      | Required | Default |
|----------------------------|------------------------------|----------|---------|
| `TWILIO_ACCOUNT_SID`       | Twilio account SID           | ✅       | —       |
| `TWILIO_AUTH_TOKEN`        | Twilio auth token            | ✅       | —       |
| `TWILIO_PHONE_NUMBER`      | Twilio phone number          | ✅       | —       |
| `TWILIO_RATE_LIMIT`        | SMS rate limit (per minute)  | ❌       | 60      |
| `TWILIO_RETRY_DELAY`       | Retry delay (seconds)        | ❌       | 300     |
| `TWILIO_WEBHOOK_SECRET`    | Webhook validation secret    | ❌       | —       |

## 🔄 Usage Examples

### Basic SMS Sending

```python
from apps.twilio.services import send_sms

# Send SMS
result = send_sms(
    to_phone="+1234567890",
    message="Your verification code is 123456",
    from_phone="+0987654321"
)
```

### SMS Verification

```python
from apps.twilio.services import start_verification, check_verification

# Start verification
session = start_verification(
    phone_number="+1234567890",
    channel="sms"
)

# Check verification
is_valid = check_verification(
    session_id=session.id,
    code="123456"
)
```

### Webhook Processing

```python
from apps.twilio.integrations.sender import process_webhook

@csrf_exempt
@require_POST
def webhook_view(request):
    event = process_webhook(request.body)
    if event:
        update_sms_status(event)
    return JsonResponse({"status": "ok"})
```

## 🛡 Security Considerations

- **Credential Security**: Twilio credentials management
- **Webhook Security**: Request validation
- **Rate Limiting**: SMS sending protection
- **Error Security**: Sensitive information masking
- **Session Security**: Verification session management
- **Connection Security**: TLS/SSL enforcement

## 🚀 Performance Considerations

- **Connection Pooling**: Efficient Twilio connections
- **Batch Operations**: Optimized sending
- **Caching Strategy**: Rate limit tracking
- **Error Handling**: Fast failure paths
- **Middleware**: Efficient request processing
- **Webhook Processing**: Efficient event handlingAll you need are the following:

- `/api/sms/verify/start/` — to initiate token delivery
- `/api/sms/verify/check/` — to validate submitted token

No database model is required for token tracking when using Twilio Verify.

---

### 🧪 Token Verification Flow

1. Frontend sends phone number to `/verify/start/`
2. Backend triggers `libs.twilio_sms.send_token(to_number)`
3. User enters received code in frontend
4. Code is sent to `/verify/check/`
5. Backend validates via `libs.twilio_sms.verify_token(...)`
6. Response confirms or denies validation

---

### ✅ TDD Strategy (Extension)

- Test token generation rate limit
- Verify token lifecycle: send → validate → expire
- Mock successful and failed validations
- Handle edge cases: expired, reused, throttled codes

---

### 🤖 LLM Implementation Guidelines

- Token lifecycle must be abstracted inside services
- Integrate `libs.twilio_sms` for both sending and checking codes
- Allow retry/resend under configurable throttling policies
- Return normalized responses for all verification outcomes

---

## 🔐 Configuration via Settings

```python
TWILIO_SMS_CONFIG = {
    "account_sid": "...",
    "auth_token": "...",
    "default_from": "+11234567890",
}
```

All settings must be injected externally — no direct use of `os.environ`.

---

## 🧠 Caching Strategy (optional)

| Use Case              | Cache Key                      | Purpose                                |
|------------------------|-------------------------------|----------------------------------------|
| Deduplication          | `sms:msg:<provider_msg_id>`    | Prevent multiple webhook updates       |
| Retry throttling       | `sms:retry:<to_phone>`         | Avoid spam/resend flooding             |

---

## ✅ TDD Strategy

### Unit Tests

- SMSLog creation, status update
- Serializer and payload validation
- Webhook integrity

### Integration Tests

- Full send flow via test Twilio account
- Receive simulated webhook and update SMSLog

---

## 🤖 LLM Implementation Guidelines

- All delivery logic must use `libs.twilio_sms`
- Provider-specific responses must be normalized internally
- Use DRF serializers for input and response
- Ensure webhook events are authenticated (e.g., Twilio signature)
- Views must return structured errors for invalid inputs

---
</file>
