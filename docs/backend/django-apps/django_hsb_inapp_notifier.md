# 🔔 Django App: `apps.django_hsb_inapp_notifier`

A reusable in-app notification system for Django applications, supporting multiple delivery channels and customizable frontend rendering.

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

1. **Decoupled Delivery**: Supports multiple notification channels (HTTP, pub/sub)
2. **Customizable Rendering**: Flexible metadata for frontend display
3. **Template System**: Optional admin-managed notification templates
4. **User-centric**: Notification lifecycle management per user
5. **Extensible**: Easy to add new notification types and channels

## 📁 Module Structure

```
apps/
└── django_hsb_inapp_notifier/
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
        │   ├── test_models.py
        │   ├── test_services.py
        │   └── test_views.py
        └── integration/
            ├── test_pubsub.py
            └── test_api.py
```

## ⚙️ Components

### 1. Models (`models.py`)

- **Purpose**: Data storage and relationships
- **Key Models**:
  - `Notification`: User notifications with metadata
  - `NotificationTemplate`: Optional template system

### 2. Services (`services.py`)

- **Purpose**: Core notification logic
- **Features**:
  - Template resolution
  - Notification creation
  - Batch operations
  - Error handling

### 3. API (`views.py` + `serializers.py`)

- **Purpose**: REST API endpoints
- **Endpoints**:
  - `/api/notifications/` - List notifications
  - `/api/notifications/unseen/` - Get unseen notifications
  - `/api/notifications/mark-seen/` - Mark notifications as seen
  - `/api/notifications/create/` - Create notifications

### 4. Pub/Sub Integration (`consumers/`)

- **Purpose**: Message handling
- **Features**:
  - AWS SNS/SQS integration
  - Redis pub/sub support
  - Message normalization
  - Error handling

### 5. Error Handling (`exceptions.py`)

- **Purpose**: Domain-specific error abstraction
- **Exceptions**:
  - `NotificationError`
  - `TemplateError`
  - `DeliveryError`
  - `ValidationError`

## ✅ Testing Strategy

### Unit Tests

- **Core Logic**:
  - Model validation
  - Template resolution
  - Notification creation
  - Batch operations
- **Test Coverage**:
  - 100% statement coverage
  - Edge case handling
  - Error scenarios
  - Template rendering

### Integration Tests

- **Internal Integration**:
  - Database operations
  - API endpoints
  - Template system
  - Batch operations
- **External Integration**:
  - Pub/Sub message handling
  - AWS SNS/SQS integration
  - Redis pub/sub
  - Template rendering

## 🔐 Environment Variables

No direct environment variable access inside the app. All configuration must be passed through Django settings.

If required by the consuming app, recommended settings:

| Setting Name               | Purpose                      | Required | Default |
|----------------------------|------------------------------|----------|---------|
| `NOTIFICATIONS_MAX_CONTENT` | Maximum notification content  | ❌       | 1000    |
| `NOTIFICATIONS_PAGINATION`  | API pagination limit         | ❌       | 50      |
| `NOTIFICATIONS_TTL`         | Notification TTL (days)      | ❌       | 30      |

## 🔄 Usage Examples

### Basic Notification Creation

```python
from apps.notifications.services import create_notification

notification = create_notification(
    user=user,
    title="New Message",
    content="You have a new message from John",
    icon="message",
    url="/messages/123"
)
```

### Using Templates

```python
from apps.notifications.services import create_notification_from_template

notification = create_notification_from_template(
    slug="message_received",
    user=user,
    context={
        "sender": "John",
        "message_id": "123"
    }
)
```

### Pub/Sub Integration

```python
from apps.notifications.consumers.aws import SNSConsumer

consumer = SNSConsumer()
consumer.process_message(
    topic="notifications.new",
    message={
        "user_id": "123",
        "event_type": "message_received",
        "data": {...}
    }
)
```

## 🛡 Security Considerations

- **Access Control**: User-specific notifications
- **Content Validation**: Input sanitization
- **Rate Limiting**: API endpoint protection
- **Template Security**: Safe template rendering
- **Error Handling**: No sensitive information

## 🚀 Performance Considerations

- **Database Optimization**: Proper indexes
- **Caching Strategy**: Notification list caching
- **Batch Operations**: Efficient updates
- **Pagination**: API endpoint optimization
- **Error Handling**: Fast failure paths

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
