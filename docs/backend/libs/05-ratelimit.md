# 🔄 Rate Limit Library — `django_hsb_ratelimit`

A flexible rate limiting system for Django and DRF endpoints, supporting various key types (IP, user, etc.) and configurable time windows.

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

1. **Flexible Keying**: Multiple key types (IP, user, etc.)
2. **Configurable Limits**: Customizable rate limits
3. **Distributed Storage**: Redis-based implementation
4. **Middleware Integration**: Django/DRF compatibility
5. **Error Handling**: Customizable error responses

## 📁 Module Structure

```
libs/
└── ratelimit/
    ├── __init__.py
    ├── config.py            # Configuration and settings
    ├── decorators.py        # Rate limit decorator
    ├── storage.py           # Redis storage
    ├── middleware.py        # Django middleware
    ├── exceptions.py        # Error handling
    ├── types.py             # Result types and enums
    └── tests/
        ├── unit/
        │   ├── test_decorator.py
        │   ├── test_storage.py
        │   └── test_middleware.py
        └── integration/
            ├── test_redis_real.py
            └── test_http_real.py
```

## ⚙️ Components

### 1. Configuration (`config.py`)

- **Purpose**: Rate limit settings
- **Key Components**:
  - `RateLimitConfig` dataclass
  - Redis connection settings
  - Default limits and windows
  - Error message customization

### 2. Decorator (`decorators.py`)

- **Purpose**: Rate limit application
- **API**:
  ```python
  def rate_limit(
      key: str = "ip",  # or "user", "path", etc.
      limit: str = "100/m",  # e.g. "100/m", "500/h", "1000/d"
      scope: str = None  # optional scope name
  ) -> Callable
  ```
- **Features**:
  - Flexible key types
  - Customizable limits
  - Multiple scopes
  - Error handling

### 3. Storage (`storage.py`)

- **Purpose**: Rate limit tracking
- **Features**:
  - Redis implementation
  - Automatic cleanup
  - Concurrent access
  - Multiple scopes

### 4. Middleware (`middleware.py`)

- **Purpose**: Request handling
- **Features**:
  - Rate limit enforcement
  - Error responses
  - Custom error messages
  - Request logging

### 5. Error Handling (`exceptions.py`)

- **Purpose**: Domain-specific error abstraction
- **Exceptions**:
  - `RateLimitExceeded`
  - `InvalidRateLimit`
  - `StorageError`
  - `ConfigurationError`

## ✅ Testing Strategy

### Unit Tests
- Token bucket counter math and key resolution
- TTL enforcement and bucket reset
- Key strategy combinations (IP, user, realm, etc.)

### Integration Tests
- View-level and DRF-based rate limiting
- Enforcement of limits with blocking and reset
- Middleware compatibility and exception response

---

## 🛡 Security Notes

- Rate limit responses never leak sensitive state.
- Throttling applies equally to valid and invalid credentials.
- Composite keys prevent shared IP abuse.

---

## 🤖 LLM Implementation Guidelines

- Import decorators or throttle classes directly from the package
- Use DRF `scope` strings to differentiate throttle purposes
- Do not include the rate limit state in user-facing error messages

---

## 🚀 Example: Using in a Django Project

Below is a full example of how to integrate `django_hsb_ratelimit` in a Django project:

### 1. Install Redis and Configure Settings

```python
# settings.py

RATE_LIMIT_ENABLED = True
RATE_LIMIT_REDIS_URL = "redis://localhost:6379/0"
RATE_LIMIT_NAMESPACE = "ratelimit"
RATE_LIMIT_DEFAULT_TTL = 60  # default 60 seconds

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "django_hsb_ratelimit.throttles.RateScopedThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "auth_login": "5/min",
        "registration": "3/min",
    }
}
```

---

### 2. Protect a Django View

```python
# views.py

from django_hsb_ratelimit.decorators import rate_limit
from django.http import JsonResponse

@rate_limit(key="ip", limit="5/m", scope="auth_login")
def login_view(request):
    return JsonResponse({"message": "Login attempt successful."})
```

---

### 3. Protect a DRF ViewSet or APIView

```python
# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

class RegistrationView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "registration"

    def post(self, request):
        return Response({"message": "Registered successfully."})
```

---

### 4. Optional: Custom Throttle Key Generator

```python
# Use a composite key like realm + IP
@rate_limit(key="realm:ip", limit="10/min", scope="custom_scope")
def sensitive_view(request):
    ...
```

This setup protects your endpoints from abusive or brute-force access patterns by enforcing consistent rate limits across Django and DRF layers.
