<file name=0 path=django_hsb_twilio.md># 📦 Django App: `apps.twilio`

This app provides a Django-native integration with the `libs.twilio_sms` library, enabling SMS delivery via Twilio with future extensibility for other Twilio services (voice, WhatsApp, video, etc.). The app is fully installable, supports DRF endpoints, persistence, and clean configuration through Django settings.

---

## 🎯 Purpose

- Send SMS via Twilio using `libs.twilio_sms`
- Track SMS delivery logs and status
- Expose HTTP endpoints for sending SMS
- Receive delivery status updates via webhook
- Prepare for future Twilio service integrations

---

## 📁 App Structure

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
        └── integration/
```

---

## 🧱 Model

### `SMSLog`

| Field           | Type           | Description                             |
|------------------|----------------|-----------------------------------------|
| `id`             | UUID           | Primary key                             |
| `to_phone`       | CharField      | Recipient phone number                  |
| `from_phone`     | CharField      | Sender number (Twilio-registered)       |
| `message`        | TextField      | Body of the SMS                         |
| `status`         | CharField      | `QUEUED`, `SENT`, `FAILED`, `DELIVERED`, etc. |
| `provider_msg_id`| CharField      | Twilio SID for tracking                 |
| `last_event_time`| DateTimeField  | Last event update timestamp             |
| `created_at`     | DateTimeField  |                                         |
| `updated_at`     | DateTimeField  |                                         |

---

## 🌐 API Endpoints

### 📤 SMS Sending and Tracking

| Path                             | Method | Purpose                                |
|----------------------------------|--------|----------------------------------------|
| `/api/sms/send/`                | POST   | Send SMS via Twilio                    |
| `/api/sms/<uuid:id>/status/`    | GET    | Query status of a specific SMS         |

### 📡 Webhook Receiver

| Path                             | Method | Purpose                                |
|----------------------------------|--------|----------------------------------------|
| `/webhooks/sms/twilio/`         | POST   | Receive delivery status updates from Twilio |

### 🔐 Verification Code API

| Path                                  | Method | Purpose                                      |
|---------------------------------------|--------|----------------------------------------------|
| `/api/sms/verify/start/`             | POST   | Initiate verification code via SMS           |
| `/api/sms/verify/check/`             | POST   | Validate submitted verification code         |

---

## 🔑 Verification Code Support

This app also supports sending and validating time-limited SMS verification codes using Twilio's verification services or a custom implementation based on `libs.twilio_sms`.

---

### 🌐 Verification API Endpoints

| Path                                  | Method | Purpose                                      |
|---------------------------------------|--------|----------------------------------------------|
| `/api/sms/verify/start/`             | POST   | Initiates SMS verification code to a number |
| `/api/sms/verify/check/`             | POST   | Validates submitted SMS verification code   |

---

### 🧱 Token Storage Note

When using Twilio Verify, you do **not need to store verification tokens**. Twilio manages the entire lifecycle of code generation, delivery, expiration, and validation. Your backend simply delegates to Twilio for sending and verifying tokens.

All you need are the following:

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
