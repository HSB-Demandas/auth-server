


# 📧 Email Sender Library — `libs.email_sender`

An extensible email sending interface that supports multiple providers (SMTP, Mailgun, AWS SES, etc.) and handles delivery events through webhooks.

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

1. **Provider Agnostic**: Supports multiple email providers
2. **Event-Driven**: Handles delivery events and webhooks
3. **Extensible**: Easy to add new providers
4. **Type Safe**: Uses Pydantic for validation
5. **Testable**: Mockable interfaces and providers

## 📁 Module Structure

```
libs/
└── mailer/
    ├── __init__.py
    ├── config.py                  # Configuration and settings
    ├── interface.py               # Provider interfaces
    ├── models.py                  # Email message models
    ├── router.py                  # Provider routing
    ├── provider/
    │   ├── smtp_provider.py       # SMTP integration
    │   ├── mailgun_provider.py    # Mailgun integration
    │   ├── ses_provider.py        # AWS SES integration
    │   └── ... (other providers)
    ├── events/
    │   ├── base_event.py          # Event base classes
    │   ├── mailgun_events.py      # Mailgun webhook parsing
    │   └── ... (other providers)
    ├── types.py                   # Result types and enums
    └── tests/
        ├── unit/
        │   ├── test_smtp.py
        │   ├── test_mailgun.py
        │   └── test_ses.py
        └── integration/
            ├── test_send_real.py
            └── test_webhook_real.py
```

## ⚙️ Components

### 1. Configuration (`config.py`)

- **Purpose**: Email service configuration
- **Key Components**:
  - `EmailConfig` pydantic model
  - Provider-specific settings
  - Event handling configuration

### 2. Provider Interface (`interface.py`)

- **Purpose**: Provider contract definition
- **API**:
  ```python
  class EmailProviderInterface:
      def send(self, message: EmailMessage) -> EmailResult
  ```
- **Features**:
  - Standardized message format
  - Unified result handling
  - Error abstraction

### 3. Message Models (`models.py`)

- **Purpose**: Email message representation
- **Models**:
  - `EmailMessage`: Email content and metadata
  - `Attachment`: File attachments
  - `EmailResult`: Send operation result
  - `EmailEvent`: Delivery events

### 4. Router (`router.py`)

- **Purpose**: Provider dispatching
- **Features**:
  - Dynamic provider selection
  - Error handling
  - Retry logic
  - Rate limiting

### 5. Event System (`events/`)

- **Purpose**: Delivery event handling
- **Features**:
  - Webhook parsing
  - Event normalization
  - Event routing
  - Error handling

### 6. Error Handling (`types.py`)

- **Purpose**: Domain-specific error abstraction
- **Exceptions**:
  - `EmailSendError`
  - `InvalidEmailError`
  - `ProviderError`
  - `EventProcessingError`

## ✅ Testing Strategy

### Unit Tests

- **Core Logic**:
  - Message validation
  - Provider routing
  - Event parsing
  - Error handling
- **Test Coverage**:
  - 100% statement coverage
  - Edge case handling
  - Error scenarios
  - Provider-specific tests

### Integration Tests

- **Real Integration**:
  - Email sending
  - Webhook processing
  - Error handling
  - Retry logic
- **Requirements**:
  - Test credentials
  - Test messages
  - Mock providers
  - Event payloads

## 🔐 Environment Variables

No direct environment variable access inside the library. Configuration must be passed through `EmailConfig`.

If required by the consuming app, recommended environment variables:

| Variable Name     | Purpose                      | Required | Default |
|-------------------|------------------------------|----------|---------|
| `EMAIL_PROVIDER`  | Email provider name          | ✅       | —       |
| `EMAIL_FROM`      | Default sender email         | ✅       | —       |
| `SMTP_HOST`       | SMTP server host             | ❌       | —       |
| `SMTP_PORT`       | SMTP server port             | ❌       | 587     |
| `SMTP_USER`       | SMTP username                | ❌       | —       |
| `SMTP_PASS`       | SMTP password                | ❌       | —       |
| `MAILGUN_API_KEY` | Mailgun API key              | ❌       | —       |
| `MAILGUN_DOMAIN`  | Mailgun domain               | ❌       | —       |
| `AWS_ACCESS_KEY`  | AWS access key               | ❌       | —       |
| `AWS_SECRET_KEY`  | AWS secret key               | ❌       | —       |

## 🔄 Usage Examples

### Basic Email Sending

```python
from libs.mailer.config import EmailConfig
from libs.mailer.models import EmailMessage
from libs.mailer.router import EmailRouter

config = EmailConfig(
    provider="smtp",
    from_email="noreply@myapp.com",
    provider_config={
        "host": "smtp.example.com",
        "port": 587,
        "username": "user",
        "password": "pass"
    }
)

message = EmailMessage(
    to="user@example.com",
    subject="Hello",
    html_body="<h1>Hi!</h1>",
    text_body="Hi!"
)

router = EmailRouter(config)
result = router.send(message)
```

### Event Handling

```python
from libs.mailer.events import EventParser
from libs.mailer.models import EmailEvent

async def handle_email_event(event: EmailEvent):
    if event.event_type == EmailEventType.DELIVERED:
        # Handle delivery
        pass
    elif event.event_type == EmailEventType.BOUNCED:
        # Handle bounce
        pass

# Register event handler
parser = EventParser()
parser.register_handler(handle_email_event)
```

## 🛡 Security Considerations

- **Content Security**: Email content sanitization
- **Provider Security**: Credential management
- **Event Security**: Webhook authentication
- **Error Security**: Sensitive information masking
- **Rate Limiting**: Provider-specific limits
- **Connection Security**: TLS/SSL enforcement

## 🚀 Performance Considerations

- **Connection Pooling**: Efficient provider connections
- **Batch Processing**: Optimized sending
- **Async Operations**: Non-blocking I/O
- **Template Caching**: Efficient template rendering
- **Retry Strategy**: Configurable retry logic
- **Error Handling**: Fast failure paths

---

> **Note**: This library is designed for production use with multiple email providers. For development, use test credentials and mock providers.
