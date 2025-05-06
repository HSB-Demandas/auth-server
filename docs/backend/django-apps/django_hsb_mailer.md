# 📦 Django App: `apps.email`

This app wraps the generic email sending library (`libs.email_sender`) with full Django integration, including persistence of email records, webhook event handling, API endpoints, and caching. It is a reusable Django app that can be installed across projects and configured via standard Django settings.

---

## 🎯 Purpose

- Send emails through configurable providers using the `libs.email_sender` library
- Track delivery lifecycle via webhook events (delivered, opened, bounced, etc.)
- Expose RESTful endpoints for sending and querying emails
- Enable retries, caching, and deduplication
- Allow reusability across multiple Django projects

---

## 📁 App Structure

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
        └── integration/
```

---

## 🧱 Models

### `EmailLog`
Tracks every email and its state.

| Field              | Type           | Description                                |
|--------------------|----------------|--------------------------------------------|
| `id`               | UUID           | Primary key                                |
| `provider`         | CharField      | E.g., `smtp`, `mailgun`, `ses`             |
| `provider_msg_id`  | CharField      | ID returned by the provider                |
| `from_email`       | EmailField     | Sender                                     |
| `to_email`         | EmailField     | Recipient                                  |
| `subject`          | TextField      | Optional                                   |
| `status`           | CharField      | `PENDING`, `SENT`, `FAILED`, etc.          |
| `last_event`       | CharField      | `DELIVERED`, `OPENED`, `BOUNCED`, etc.     |
| `last_event_time`  | DateTimeField  | Timestamp of last event                    |
| `created_at`       | DateTimeField  | Timestamp                                  |
| `updated_at`       | DateTimeField  | Timestamp                                  |

---

## ⚙️ Configuration via Settings

```python
EMAIL_PROVIDER = "mailgun"
EMAIL_FROM = "noreply@myapp.com"
EMAIL_PROVIDER_CONFIG = {
    "api_key": "...",
    "domain": "...",
}
EMAIL_EVENT_CACHE_TTL = 3600  # 1 hour
```

---

## 🧠 Caching Strategy

| Use Case              | Cache Key Example                   | Purpose                          |
|------------------------|-------------------------------------|----------------------------------|
| Deduplicate events     | `email:event:<provider_msg_id>`     | Prevent duplicate updates        |
| Block re-send flood    | `email:send:<to>:<subject>`         | Prevent immediate re-send        |
| Retry flag             | `email:retry:<email_id>`            | Delayed retry support            |

---

## ✅ TDD Strategy

### Unit Tests

- Email log creation on successful send
- Webhook parsing and model updates
- Validation and serialization

### Integration Tests

- Send real email and log result
- Simulate webhook event POST
- Query status endpoint

---

## 🤖 LLM Implementation Guidelines

- All actual sending and event parsing must use `libs.email_sender`
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
