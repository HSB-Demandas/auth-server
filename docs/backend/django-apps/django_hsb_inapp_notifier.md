# 🔔 Django App: `apps.notifications`

This app provides a reusable, decoupled in-app notification system for Django applications. It allows backend services to create user-facing notifications delivered via multiple channels (HTTP, pub/sub, internal signals), which can be queried and marked as seen by authenticated users. The app supports customizable metadata for rendering in the frontend (icons, links, content) and provides an optional admin-managed notification template system.

---

## 🎯 Purpose

- Store notifications targeted to specific users
- Display and manage them in the frontend (unseen/seen state)
- Allow custom metadata per notification (e.g. icon, link, etc.)
- Receive notification triggers from HTTP endpoints or pub/sub consumers
- Optionally configure templates/presets for standardized rendering
- Be installable and reusable across Django projects

---

## 📁 App Structure

```
apps/
└── notifications/
    ├── __init__.py
    ├── apps.py
    ├── models.py             # Notification + NotificationTemplate
    ├── views.py              # API views for listing, creating, updating
    ├── urls.py               # REST API routes
    ├── serializers.py        # DRF serializers for input/output
    ├── consumers/            # Optional pub/sub consumers (SNS/SQS/Redis)
    ├── services.py           # Core logic for creation, template resolution
    ├── admin.py              # Admin panel for template config
    ├── migrations/
    └── tests/
        ├── unit/
        └── integration/
```

---

## 🧱 Models

### `Notification`

| Field        | Type           | Description                                  |
|--------------|----------------|----------------------------------------------|
| `id`         | UUID           | Primary key                                  |
| `user`       | FK to User     | Recipient                                    |
| `title`      | CharField      | Optional short title                         |
| `content`    | TextField      | Max 1000 chars (configurable)                |
| `url`        | CharField      | Optional frontend-controlled navigation link |
| `icon`       | CharField      | Icon ID or class (frontend-controlled)       |
| `seen`       | Boolean        | If user has seen this notification           |
| `created_at` | DateTimeField  | Auto timestamp                               |
| `updated_at` | DateTimeField  | Auto timestamp                               |

### `NotificationTemplate` (optional)

| Field        | Type           | Description                                  |
|--------------|----------------|----------------------------------------------|
| `slug`       | CharField      | Unique identifier (e.g. `payment_failed`)     |
| `title`      | CharField      | Optional default title                       |
| `icon`       | CharField      | Icon string                                  |
| `url`        | CharField      | Default target (optional template format)     |
| `default_content` | TextField | Default content (template renderable)         |
| `created_at` | DateTimeField  | Auto timestamp                               |
| `updated_at` | DateTimeField  | Auto timestamp                               |

---

## 🌐 API Endpoints

| Path                                  | Method | Purpose                                      |
|---------------------------------------|--------|----------------------------------------------|
| `/api/notifications/`                | GET    | List notifications for authenticated user   |
| `/api/notifications/unseen/`         | GET    | Fetch only unseen notifications             |
| `/api/notifications/mark-seen/`      | POST   | Mark one or more notifications as seen      |
| `/api/notifications/create/`         | POST   | Create a notification (internal/manual use) |

---

## ⚙️ Template Usage and Dynamic Resolution

- Templates can be selected by `slug`
- Messages can be generated dynamically using `.format(**data)`
- Useful for rendering `content`, `title`, or `url` with placeholders

---

## 📤 Pub/Sub Integration

This app can receive messages from:
- AWS SNS/SQS (via `libs.aws_messaging`)
- Redis pub/sub (optional)
- Kafka (future)

Use `NotificationTemplate.slug` to resolve frontend style (icon, title, etc.).

Each consumer must normalize incoming data and call:

```python
create_notification_from_template(slug="event_type", user_id=..., context={...})
```

---

## ✅ TDD Strategy

### Unit Tests

- Notification creation and template usage
- User-based filtering and marking seen
- Serializer validations

### Integration Tests

- Pub/sub consumption via simulated queue message
- Full frontend flow (create → list → mark seen)

---

## 🤖 LLM Implementation Guidelines

- Use `Notification.objects.filter(user=request.user)` in all views
- Always validate `content` length and icon string format
- Allow slug-based lookup via templates
- Add configurable limits for unseen notification polling
- No hardcoding icons/titles — allow full frontend control or template fallback
- Integrate signal or service call into external systems (ex: `notify_user(user, slug, context)`)

---
