# 📦 Django App: `apps.django_hsb_mailer`

A reusable Django app for email sending with full integration, including persistence, webhook handling, and caching.

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
3. **Distributed Storage**: Redis-based caching
4. **Middleware Integration**: Django/DRF compatibility
5. **Error Handling**: Customizable error responses

## 📁 Module Structure

```
apps/
└── email/
    ├── __init__.py
    ├── admin.py                # Optional: manage logs via admin
    ├── apps.py                 # Django app config
    ├── models.py               # EmailLog model for persistence
    ├── views.py                # API + webhook views
    ├── urls.py                 # Exposes API and webhook routes
    ├── serializers.py          # DRF serializers for validation
    ├── integrations/           # Uses libs.email_sender
    │   ├── sender.py
    │   └── event_parser.py
    ├── services.py             # Email sending / event registration logic
    ├── cache.py                # Local caching logic
    ├── migrations/
    └── tests/
        ├── unit/
        │   ├── test_models.py
        │   ├── test_services.py
        │   └── test_views.py
        └── integration/
            ├── test_provider.py
            └── test_webhook.py
```

## ⚙️ Components

### 1. Models (`models.py`)

- **Purpose**: Email tracking and persistence
- **Key Models**:
  - `EmailLog`: Email tracking with status
  - `EmailTemplate`: Optional template system
  - `EmailEvent`: Delivery events tracking

### 2. Services (`services.py`)

- **Purpose**: Core email logic
- **Features**:
  - Email sending
  - Event handling
  - Retry logic
  - Error handling

### 3. API (`views.py` + `serializers.py`)

- **Purpose**: REST API endpoints
- **Endpoints**:
  - `/api/email/send/` - Send email
  - `/api/email/status/` - Get status
  - `/api/email/events/` - Webhook endpoint

### 4. Caching (`cache.py`)

- **Purpose**: Performance optimization
- **Features**:
  - Event deduplication
  - Rate limiting
  - Retry tracking
  - Status caching

### 5. Error Handling (`exceptions.py`)

- **Purpose**: Domain-specific error abstraction
- **Exceptions**:
  - `EmailSendError`
  - `InvalidEmailError`
  - `ProviderError`
  - `EventProcessingError`

## ✅ Testing Strategy

### Unit Tests

- **Core Logic**:
  - Email sending
  - Event processing
  - Caching logic
  - Validation
- **Test Coverage**:
  - 100% statement coverage
  - Edge case handling
  - Error scenarios
  - Provider-specific tests

### Integration Tests

- **Internal Integration**:
  - Database operations
  - API endpoints
  - Caching behavior
  - Event handling
- **External Integration**:
  - Provider integration
  - Webhook processing
  - Error handling
  - Retry logic

## 🔐 Environment Variables

No direct environment variable access inside the app. All configuration must be passed through Django settings.

If required by the consuming app, recommended settings:

| Setting Name               | Purpose                      | Required | Default |
|----------------------------|------------------------------|----------|---------|
| `EMAIL_PROVIDER`           | Email provider name          | ✅       | —       |
| `EMAIL_FROM`               | Default sender email         | ✅       | —       |
| `EMAIL_PROVIDER_CONFIG`    | Provider-specific settings   | ✅       | —       |
| `EMAIL_EVENT_CACHE_TTL`    | Event cache TTL (seconds)    | ❌       | 3600    |
| `EMAIL_RETRY_DELAY`        | Retry delay (seconds)        | ❌       | 300     |
| `EMAIL_MAX_RETRIES`        | Maximum retry attempts       | ❌       | 3       |

## 🔄 Usage Examples

### Basic Email Sending

```python
from apps.django_hsb_mailer.services import send_email

result = send_email(
    to="user@example.com",
    subject="Welcome",
    template="welcome_email",
    context={
        "name": "John",
        "activation_link": "https://..."
    }
)
```

### Webhook Event Handling

```python
from apps.django_hsb_mailer.integrations.event_parser import parse_webhook

@csrf_exempt
@require_POST
def webhook_view(request):
    event = parse_webhook(request.body)
    if event:
        process_email_event(event)
    return JsonResponse({"status": "ok"})
```

### Caching Usage

```python
from apps.django_hsb_mailer.cache import EmailCache

cache = EmailCache()

cache.set_event_deduplication("message-id-123")
if cache.check_event_deduplication("message-id-123"):
    # Skip processing
    pass
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
- **Batch Operations**: Optimized sending
- **Caching Strategy**: Event deduplication
- **Error Handling**: Fast failure paths
- **Middleware**: Efficient request processing
- **Template Caching**: Efficient template rendering

## 🤖 LLM Implementation Guidelines

- All actual sending and event parsing must use `libs.django_hsb_mailer.integrations.sender`
- Models must be independent of any specific provider
- Webhook views must normalize all event formats into `EmailEvent`
- Ensure all exceptions are caught and returned as DRF errors
- Follow Django style for views, URLs, models, signals, etc.
- DRF is required for request/response handling

---


---

## 📝 Email Template Management

This app supports storing and rendering reusable email templates with support for both HTML (rich) and plain text content in the same message.

---

### 📁 Template Model: `EmailTemplate`

| Field                | Type           | Description                                      |
|----------------------|----------------|--------------------------------------------------|
| `id`                 | UUID           | Primary key                                      |
| `name`               | CharField      | Unique name used as identifier                  |
| `subject_template`   | TextField      | Subject line with Django-style placeholders      |
| `body_html_template` | TextField      | Rich HTML content (supports placeholders)        |
| `body_text_template` | TextField      | Plain text fallback (optional)                   |
| `description`        | TextField      | Optional description for admin use               |
| `language_code`      | CharField      | Optional, to support multilingual versions       |
| `created_at`         | DateTimeField  | Timestamp                                        |
| `updated_at`         | DateTimeField  | Timestamp                                        |

---

### 🔧 Templating Engine

Templates use Django's templating language. Variables are rendered dynamically using `Context`.

```python
from django.template import Template, Context

def render_email_template(template: EmailTemplate, context: dict) -> tuple[str, str, str]:
    subject = Template(template.subject_template).render(Context(context))
    body_html = Template(template.body_html_template).render(Context(context))
    body_text = Template(template.body_text_template).render(Context(context)) if template.body_text_template else None
    return subject, body_html, body_text
```

---

### 🧪 Example Usage

```python
template = EmailTemplate.objects.get(name="welcome_user")
subject, body_html, body_text = render_email_template(template, {
    "user": {"first_name": "Alice"}
})

email = EmailMessage(
    to="alice@example.com",
    subject=subject,
    html_body=body_html,
    text_body=body_text,
)
EmailRouter(settings.EMAIL_CONFIG).send(email)
```

---

### ✅ API Considerations

Expose endpoints to:
- Create/update templates (admin only)
- Preview rendered template with sample data
- List all templates with metadata

---

### 🧠 Guidelines

- Store templates in DB, not files, to allow dynamic updates
- Always fallback to plain text when available
- Templates are rendered at send-time using current context
- Cache compiled templates optionally for performance

---

### 💡 Rendering Enhancements & Email Standards

To ensure compatibility across email clients, rich HTML templates should be processed using an HTML-to-email converter like **Premailer**, which inlines CSS styles and sanitizes unsupported attributes.

```python
import premailer

def postprocess_email_html(html: str) -> str:
    return premailer.transform(html)
```

This transformation should be applied after the template is rendered but before it is sent.

---

### 📩 Email Best Practices

Every email template **must** include an unsubscribe link in the footer. The app must provide a public unsubscribe endpoint for recipients to opt out of future messages.

#### ✅ Footer Recommendations:

```html
<p style="font-size: 0.8em; color: #888;">
    To stop receiving these emails, <a href="{{ unsubscribe_url }}">unsubscribe here</a>.
</p>
```

#### 🔗 Unsubscribe Endpoint

Expose a route such as:

| Path                               | Method | Description                          |
|------------------------------------|--------|--------------------------------------|
| `/email/unsubscribe/[uuid:token]/` | GET    | Opt out the recipient from future sends |

The `unsubscribe_url` should be generated with a token that maps to the recipient or log.

> Unsubscribed emails must be flagged in the database and suppressed during sends.

---

### ✅ Guidelines Summary

- Rich HTML must be inlined and validated for email clients
- Every email must contain an unsubscribe link
- Emails to unsubscribed addresses must be filtered automatically
- The system must support a secure public unsubscribe endpoint

---
</file>
