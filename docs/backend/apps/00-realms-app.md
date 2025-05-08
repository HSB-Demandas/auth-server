# 🏰 Django App: `apps.realms`

A foundational Django app for multitenancy, providing isolated authentication domains (realms) for users, applications, and permissions.

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

1. **Isolation**: Complete realm isolation
2. **Scalability**: Efficient realm switching
3. **Extensibility**: Custom realm behavior
4. **Security**: Strict access control
5. **Configurability**: Flexible realm settings

## 📁 Module Structure

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
        │   ├── test_models.py
        │   ├── test_context.py
        │   └── test_permissions.py
        ├── internal_integration/
        │   ├── test_views.py
        │   └── test_middleware.py
        └── external_integration/
            └── test_auth.py
```

## ⚙️ Components

### 1. Models (`models.py`)

- **Purpose**: Realm definition and configuration
- **Key Models**:
  - `Realm`: Realm definition
  - `RealmConfig`: Optional configuration
  - `RealmTheme`: Optional theming

### 2. Services (`services.py`)

- **Purpose**: Core realm logic
- **Features**:
  - Realm switching
  - Context management
  - Configuration handling
  - Error handling

### 3. Context (`context.py`)

- **Purpose**: Realm context management
- **Features**:
  - Header extraction
  - JWT parsing
  - Context injection
  - Error handling

### 4. Middleware (`middleware.py`)

- **Purpose**: Request context handling
- **Features**:
  - Realm detection
  - Context injection
  - Error handling
  - Performance optimization

### 5. Error Handling (`exceptions.py`)

- **Purpose**: Domain-specific error abstraction
- **Exceptions**:
  - `RealmNotFoundError`
  - `RealmAccessError`
  - `RealmValidationError`
  - `RealmContextError`

## ✅ Testing Strategy

### Unit Tests

- **Core Logic**:
  - Realm creation
  - Context resolution
  - Permission checking
  - Configuration handling
- **Test Coverage**:
  - 100% statement coverage
  - Edge case handling
  - Error scenarios
  - Context testing

### Integration Tests

- **Internal Integration**:
  - Database operations
  - API endpoints
  - Context management
  - Permission checking
- **External Integration**:
  - JWT integration
  - Header handling
  - Middleware testing
  - Error handling

## 🔐 Environment Variables

No direct environment variable access inside the app. All configuration must be passed through Django settings.

If required by the consuming app, recommended settings:

| Setting Name               | Purpose                      | Required | Default |
|----------------------------|------------------------------|----------|---------|
| `REALM_DEFAULT`            | Default realm slug           | ❌       | default |
| `REALM_CONTEXT_HEADERS`    | Headers for realm context    | ❌       | X-Realm |
| `REALM_CACHE_TTL`          | Cache TTL (seconds)          | ❌       | 3600    |
| `REALM_MAX_PER_USER`       | Max realms per user          | ❌       | 10      |

## 🔄 Usage Examples

### Basic Realm Creation

```python
from apps.realms.services import create_realm

# Create new realm
realm = create_realm(
    slug="myrealm",
    name="My Realm",
    theme={
        "primary_color": "#007bff",
        "secondary_color": "#6c757d"
    }
)
```

### Realm Context Usage

```python
from apps.realms.context import get_current_realm

# Get current realm from context
realm = get_current_realm()

# Switch realm context
with switch_realm("otherrealm"):
    # Operations in other realm
    pass
```

### Middleware Integration

```python
from apps.realms.middleware import RealmMiddleware

# Apply middleware
middleware = RealmMiddleware(get_response)
response = middleware(request)
```

## 🛡 Security Considerations

- **Access Control**: Strict realm isolation
- **Context Security**: Secure context management
- **Data Protection**: Realm-scoped data
- **Rate Limiting**: Realm-specific limits
- **Error Handling**: Secure error responses
- **Configuration Security**: Sensitive config handling

## 🚀 Performance Considerations

- **Context Management**: Efficient context switching
- **Caching Strategy**: Realm data caching
- **Middleware**: Efficient request processing
- **Error Handling**: Fast failure paths
- **Query Optimization**: Efficient realm queries
- **Batch Operations**: Efficient bulk operations

## 🤖 LLM Implementation Guidelines

- All users and apps must belong to a realm
- A realm must be explicitly required in all external API calls
- Views must validate that authenticated users operate within the current realm
- Admin access should support listing and switching across realms
- Realm context must be accessible throughout the request lifecycle

---
