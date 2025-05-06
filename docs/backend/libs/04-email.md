


# 📧 Email Sender Library — `libs.email_sender`

This module provides an extensible, provider-agnostic email sending interface that allows the system to support multiple third-party email services like SMTP, Mailgun, AWS SES, and others. It also supports parsing event notifications (when available) from these providers, such as delivery confirmations, opens, bounces, and spam reports.

---

## 📁 Module Structure

```
libs/
└── mailer/
    ├── __init__.py
    ├── config.py                  # Global EmailConfig dataclass
    ├── interface.py               # EmailProviderInterface (abstract contract)
    ├── models.py                  # EmailMessage, Attachment, EmailResult
    ├── router.py                  # Main entrypoint and dynamic dispatcher
    ├── provider/
    │   ├── smtp_provider.py       # SMTP integration
    │   ├── mailgun_provider.py    # Mailgun integration
    │   ├── ses_provider.py        # AWS SES integration
    │   └── ... (other providers)
    ├── events/
    │   ├── base_event.py          # EmailEvent base class + enums
    │   ├── mailgun_events.py      # Parses Mailgun webhooks
    │   └── ... (others)
    └── tests/
        ├── unit/
        └── integration/
```

---

## ⚙️ Provider Abstraction

Each provider must implement:

```python
class EmailProviderInterface:
    def send(self, message: EmailMessage) -> EmailResult
```

- `EmailMessage`: unified structure with subject, body, recipients, etc.
- `EmailResult`: normalized result (success/failure + metadata)

The active provider is selected by the router dynamically based on `EmailConfig`.

---

## 📬 Event Support

Some providers offer delivery events (via webhooks). When supported, each event parser must implement:

```python
class EventParserInterface:
    def parse_event(self, payload: dict) -> EmailEvent
```

The parsed `EmailEvent` structure contains:
- `event_type`: Enum (`DELIVERED`, `OPENED`, `BOUNCED`, etc.)
- `timestamp`
- `recipient`
- `provider_message_id`

The system can consume these events and store or react accordingly.

---

## 🔐 Configuration

```python
@dataclass
class EmailConfig:
    provider: Literal["smtp", "mailgun", "ses", ...]
    from_email: str
    provider_config: dict  # credentials and API keys per provider
```

All configuration must be passed from the consuming app. The library does not access `os.environ`.

---

## ✅ Usage Example

```python
config = EmailConfig(provider="smtp", from_email="noreply@myapp.com", provider_config={...})
email = EmailMessage(to="user@example.com", subject="Hello", html_body="<h1>Hi!</h1>")
result = EmailRouter(config).send(email)
```

---

## ✅ Testing Strategy (TDD)

### Unit Tests
- Each provider is mocked and tested independently
- Verify correct routing and standardization

### Integration Tests (disabled by default)
- SMTP or Mailgun real tests using test accounts

---

## 🤖 LLM Guidelines

- Do not access environment variables inside the library.
- Use clean façades like `EmailRouter.send(...)`.
- Each provider must follow the same interface.
- Add new integrations in `provider/`, and register in `router.py`.
- Events should be parsed into `EmailEvent` with a common structure.

---
