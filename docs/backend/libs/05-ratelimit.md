# 🚦 Django Library: `django_hsb_ratelimit`

## 📌 Purpose

This library provides configurable and extensible rate-limiting functionality for Django projects. It supports per-endpoint, per-user, per-IP, and per-realm throttling strategies using Redis as a backend. The library is integrated with Django and Django REST Framework (DRF) but is designed with clear boundaries between Django integration and the core logic.

---

## 📁 Module Structure

```
django_hsb_ratelimit/
├── decorators.py        # Django view decorators
├── throttles.py         # DRF-compatible throttle classes
├── core.py              # Pure logic: rate calculation, key generation
├── backends/
│   └── redis.py         # Redis-based counter backend
├── exceptions.py        # Custom exceptions (e.g. RateLimitExceeded)
├── utils.py             # IP hashing, fingerprinting, key formatters
├── settings.py          # Configurable settings with defaults
└── tests/
    ├── unit/
    └── integration/
```

---

## 🧠 Rate Limiting Strategy

- Uses Redis with TTL-based keys for fast atomic checks
- Key scopes supported:
  - `ip` (based on request IP)
  - `user` (based on `request.user`)
  - `realm` (if `request.realm` is set)
  - `composite` (e.g., IP + user, app + endpoint)
- Supports multiple limits per route (e.g., `5/m`, `100/day`)

---

## 🧪 Example Usage

### 🎯 With Django View Decorator

```python
from django_hsb_ratelimit.decorators import rate_limit

@rate_limit(key="ip", limit="5/m", scope="auth_login")
def login_view(request):
    ...
```

### 🔄 With DRF Throttle Class

```python
# settings.py

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "django_hsb_ratelimit.throttles.RateScopedThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "auth_login": "5/min",
        "registration": "2/min",
    }
}
```

---

## 🔧 Settings

| Setting                             | Description                                                  |
|-------------------------------------|--------------------------------------------------------------|
| `RATE_LIMIT_REDIS_URL`              | Redis URL to store rate counters                             |
| `RATE_LIMIT_DEFAULT_TTL`            | Default TTL in seconds (used if not derived from rate)       |
| `RATE_LIMIT_NAMESPACE`              | Prefix for Redis keys to isolate environments                |
| `RATE_LIMIT_ENABLED`                | Toggle global rate limiting                                  |

---

## ✅ TDD Strategy

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
