# 🔔 Django App: `apps.webhooks`

This app manages webhook subscriptions and dispatching for external systems. Webhooks are scoped to applications and defined by application administrators. They allow external systems to react to internal events via secure and traceable HTTP callbacks.

---

## 🎯 Purpose

- Let applications subscribe to internal events (e.g., `user.created`, `email.verified`, `mfa.failed`)
- Send structured payloads to specified HTTP endpoints
- Support retries with exponential backoff
- Log every delivery attempt for traceability
- Allow flexible extension to future events

---

## 📁 App Structure

```
apps/
└── webhooks/
    ├── __init__.py
    ├── apps.py
    ├── models.py             # Webhook, WebhookLog
    ├── views.py              # API views to manage subscriptions and logs
    ├── urls.py               # Endpoint routes
    ├── serializers.py        # DRF serializers
    ├── dispatcher.py         # Trigger queue, handle retries
    ├── backoff.py            # Retry delay logic
    ├── admin.py              # Manage registered hooks
    ├── migrations/
    └── tests/
        ├── unit/
        └── integration/
```

---

## 🧱 Models

### `Webhook`

| Field           | Type             | Description |
|----------------|------------------|-------------|
| `id`           | UUID             | Primary key |
| `application`  | FK to Application| Webhook belongs to one application |
| `url`          | URLField         | Target endpoint |
| `method`       | CharField        | `POST`, `PUT`, etc. |
| `headers`      | JSONField        | Custom headers (e.g., auth) |
| `events`       | ArrayField       | List of subscribed events |
| `secret`       | CharField        | Used to sign payloads (optional) |
| `is_active`    | BooleanField     | Temporarily enable/disable delivery |
| `created_at`   | DateTimeField    | Timestamp |
| `updated_at`   | DateTimeField    | Timestamp |

### `WebhookLog`

| Field           | Type             | Description |
|----------------|------------------|-------------|
| `webhook`      | FK to Webhook    | Related webhook |
| `payload`      | JSONField        | Sent payload |
| `headers`      | JSONField        | Headers sent |
| `response_status` | IntegerField  | HTTP status received |
| `response_body`  | TextField      | Optional response content |
| `attempt`      | IntegerField     | Current retry count |
| `scheduled_at` | DateTimeField    | When request was (re)attempted |
| `delivered_at` | DateTimeField    | If successful |
| `failed`       | BooleanField     | Final delivery failure |

---

## 📡 Dispatching Logic

- Events are pushed to a queue when triggered
- Initial delivery is attempted immediately
- Failed deliveries are retried with increasing backoff:
  - e.g., 1min → 5min → 15min → 1hr → fail (configurable)
- Signature (HMAC) optionally included via `X-Signature`

---

## 🔐 Access Control

- Only administrators of an application can:
  - Create, update, disable, or delete webhooks
  - View delivery logs for their own app

---

## 🔁 Event Management

- Events are structured as `event.type` (e.g., `user.created`)
- New events can be added to the system without DB migration
- Event payloads follow a versioned schema (future-proof)

---

## ✅ TDD Strategy

### Unit Tests
- Event registration and payload generation
- Retry scheduling logic
- Signature generation

### Integration Tests
- Subscription, delivery, and replay
- Log creation on success/failure
- Disabled webhooks don't trigger dispatch

---

## 🤖 LLM Implementation Guidelines

- Webhooks must always be scoped to an `Application`
- Retry logic must use exponential backoff and persist attempt state
- Log every delivery attempt regardless of outcome
- Delivery jobs must be idempotent (use request IDs)
- Signature is optional per webhook; never hardcoded

---
