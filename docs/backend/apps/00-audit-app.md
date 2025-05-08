# 🧾 Audit App — `apps.audit`

A centralized audit logging system for tracking administrative and user-related actions across realms and applications, ensuring traceability and accountability.

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

1. **Immutability**: Audit logs cannot be modified
2. **Traceability**: Complete action tracking
3. **Scalability**: Efficient querying and storage
4. **Security**: Role-based access control
5. **Extensibility**: Pub/Sub event system

## 📁 Module Structure

```
apps/
└── audit/
    ├── __init__.py
    ├── apps.py
    ├── models.py              # AuditLogEntry model
    ├── views.py               # API views
    ├── urls.py                # REST API routes
    ├── serializers.py         # DRF serializers
    ├── services.py            # Core audit logic
    ├── signals.py             # Signal handlers
    ├── integrations/          # External service wrappers
    │   ├── base.py
    │   └── pubsub.py
    ├── admin.py               # Optional admin integration
    ├── migrations/
    └── tests/
        ├── unit/
        │   ├── test_models.py
        │   ├── test_services.py
        │   └── test_signals.py
        ├── internal_integration/
        │   ├── test_views.py
        │   └── test_queries.py
        └── external_integration/
            └── test_pubsub.py
```

## ⚙️ Components

### 1. Models (`models.py`)

- **Purpose**: Immutable audit log storage
- **Key Models**:
  - `AuditLogEntry`: Immutable log entries
  - `AuditSubscription`: Optional event subscriptions
  - `AuditConfig`: Optional configuration model

### 2. Services (`services.py`)

- **Purpose**: Core audit logic
- **Features**:
  - Log creation
  - Event handling
  - Query optimization
  - Error handling

### 3. API (`views.py` + `serializers.py`)

- **Purpose**: REST API endpoints
- **Endpoints**:
  - `/api/audit/` - List audit entries
  - `/api/audit/<uuid:id>/` - Get audit entry

### 4. Integration (`integrations/`)

- **Purpose**: External service integration
- **Features**:
  - Pub/Sub event handling
  - Signal processing
  - Error handling

### 5. Error Handling (`exceptions.py`)

- **Purpose**: Domain-specific error abstraction
- **Exceptions**:
  - `AuditError`
  - `ImmutableError`
  - `AccessError`
  - `ValidationError`

## ✅ Testing Strategy

### Unit Tests

- **Core Logic**:
  - Log creation
  - Event handling
  - Query optimization
  - Signal processing
- **Test Coverage**:
  - 100% statement coverage
  - Edge case handling
  - Error scenarios
  - Immutability testing

### Integration Tests

- **Internal Integration**:
  - Database operations
  - API endpoints
  - Signal processing
  - Query optimization
- **External Integration**:
  - Pub/Sub event handling
  - Signal processing
  - Error handling
  - Performance testing

## 🔐 Environment Variables

No direct environment variable access inside the app. All configuration must be passed through Django settings.

If required by the consuming app, recommended settings:

| Setting Name               | Purpose                      | Required | Default |
|----------------------------|------------------------------|----------|---------|
| `AUDIT_LOG_RETENTION_DAYS` | Log retention period (days)  | ❌       | 365     |
| `AUDIT_PUBSUB_TOPIC`       | Pub/Sub topic name           | ❌       | audit   |
| `AUDIT_MAX_QUERY_SIZE`     | Max query size               | ❌       | 1000    |
| `AUDIT_QUERY_TIMEOUT`      | Query timeout (seconds)      | ❌       | 30      |

## 🔄 Usage Examples

### Basic Log Creation

```python
from apps.audit.services import create_audit_log

# Create audit log
log = create_audit_log(
    actor_user=user,
    realm=realm,
    action="user.created",
    target_model="User",
    target_object_id=user.id,
    metadata={
        "ip_address": "127.0.0.1",
        "user_agent": "Mozilla/..."
    }
)
```

### Signal-Based Logging

```python
from apps.audit.signals import audit_log

@audit_log("user.updated")
def user_updated(sender, instance, **kwargs):
    return {
        "target_model": "User",
        "target_object_id": instance.id,
        "changes": kwargs.get("changes", {})
    }
```

### Querying Logs

```python
from apps.audit.models import AuditLogEntry

# Query logs for specific user
logs = AuditLogEntry.objects.filter(
    actor_user=user,
    realm=realm
).order_by("-timestamp")[:100]
```

## 🛡 Security Considerations

- **Access Control**: Realm-scoped access
- **Immutability**: Log entries cannot be modified
- **Data Protection**: Sensitive data handling
- **Rate Limiting**: API endpoint protection
- **Error Handling**: Secure error responses
- **Audit Trail**: Self-auditing capabilities

## 🚀 Performance Considerations

- **Query Optimization**: Efficient database queries
- **Indexing Strategy**: Proper database indexes
- **Caching Strategy**: Query result caching
- **Batch Operations**: Efficient bulk operations
- **Error Handling**: Fast failure paths
- **Pagination**: Efficient result pagination
