# 🏰 Django App: `apps.realms`

This app provides the foundation for multitenancy in the system by introducing the concept of "Realms" — isolated authentication domains. Each realm encapsulates users, applications, permissions, and configuration within its own namespace. This app is foundational and must be installed first in any Django project that uses authentication or user scoping.

---

## 🎯 Purpose

- Represent isolated identity domains (realms) across the platform
- Scope users, applications, permissions, and policies by realm
- Allow realm management via Django Admin and API
- Provide hooks for realm-based filtering and validation
- Support default realm-wide configurations and display metadata

---

## 📁 App Structure

```
apps/
└── realms/
    ├── __init__.py
    ├── apps.py
    ├── models.py             # Realm model definition
    ├── views.py              # API views (optional)
    ├── urls.py               # Routes for APIs (if exposed)
    ├── serializers.py        # DRF serializers
    ├── services.py           # Core logic for realm behavior
    ├── permissions.py        # Realm permission filters
    ├── context.py            # Realm context resolution from headers, JWT
    ├── middleware.py         # Optional realm extraction middleware
    ├── admin.py              # Admin interface for managing realms
    ├── migrations/
    └── tests/
        ├── unit/
        └── integration/
```

---

## 🧱 Model

### `Realm`

| Field             | Type           | Description                              |
|-------------------|----------------|------------------------------------------|
| `id`              | UUID           | Primary key                              |
| `slug`            | CharField      | Unique string identifier (e.g. `myrealm`)|
| `name`            | CharField      | Display name                             |
| `is_active`       | BooleanField   | Whether realm is enabled or blocked      |
| `branding_logo`   | ImageField     | Optional logo for frontend customization |
| `theme`           | JSONField      | Optional theme parameters (colors, etc.) |
| `default_language`| CharField      | Optional default language code           |
| `created_at`      | DateTimeField  | Timestamp                                |
| `updated_at`      | DateTimeField  | Timestamp                                |

---

## 🌐 Realm Context Handling

- All authenticated requests must resolve realm context from:
  - `X-Realm` header
  - JWT `realm` claim
  - Internal execution context (in background jobs or pub/sub)

A dedicated `context.py` module will resolve and expose the current realm to other parts of the system.

---

## 🛠 Admin Panel

The `Realm` model will be fully manageable via Django Admin:
- CRUD support
- Filtering by active/inactive
- Branding/theme customization

---

## 📤 Integration Strategy

All realm-aware models (e.g., User, Application, Permission) must include a `ForeignKey` or `OneToOneField` to `Realm`.

Filtering must be enforced across all endpoints using DRF filters or querysets respecting the current realm context.

---

## ✅ TDD Strategy

### Unit Tests

- Realm creation, validation, deactivation logic
- Context resolution from headers and tokens

### Integration Tests

- Full request flow resolving realm → accessing scoped resource
- Admin CRUD tests
- Middleware detection and context injection

---

## 🤖 LLM Implementation Guidelines

- All users and apps must belong to a realm
- A realm must be explicitly required in all external API calls
- Views must validate that authenticated users operate within the current realm
- Admin access should support listing and switching across realms
- Realm context must be accessible throughout the request lifecycle

---
