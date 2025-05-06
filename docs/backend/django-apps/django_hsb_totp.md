

# 🔐 Django App: `apps.mfa`

This app provides a full TOTP integration into the Django ecosystem by wrapping the `libs.mfa_authenticator` library and exposing endpoints for pairing and token validation. It is reusable, installable in any Django project, and integrates seamlessly with frontend flows.

---

## 🎯 Purpose

- Expose endpoints to enable/disable MFA and validate tokens
- Store and manage per-user TOTP configuration securely
- Provide QR code-based app pairing
- Validate user-submitted tokens
- Support secure and configurable flows

---

## 📁 App Structure

```
apps/
└── mfa/
    ├── __init__.py
    ├── apps.py
    ├── models.py            # Stores TOTP secrets per user
    ├── views.py             # API: enable MFA, verify token
    ├── urls.py              # Route: /mfa/setup/, /mfa/verify/
    ├── serializers.py       # DRF serializers for validation
    ├── services.py          # Pairing + validation logic
    ├── integrations/        # Calls into libs.mfa_authenticator
    ├── admin.py             # Optional management of MFA
    ├── migrations/
    └── tests/
        ├── unit/
        └── integration/
```

---

## 🔐 Model

### `MFASecret`

| Field          | Type           | Description                            |
|----------------|----------------|----------------------------------------|
| `id`           | UUID           | Primary key                            |
| `user`         | FK to User     | One-to-one with user                   |
| `secret`       | EncryptedField | Base32 secret for TOTP                 |
| `enabled`      | BooleanField   | Is MFA enabled for this user?          |
| `created_at`   | DateTimeField  | Timestamp                              |
| `updated_at`   | DateTimeField  | Timestamp                              |

> All secrets must be encrypted at rest using a proper encryption strategy.

---

## 🌐 API Endpoints

### 🔐 TOTP Management Endpoints

| Method | URL                    | Description                                 |
|--------|------------------------|---------------------------------------------|
| GET    | `/api/mfa/setup/`      | Returns pairing QR code and URI             |
| POST   | `/api/mfa/verify/`     | Validates submitted TOTP token              |
| POST   | `/api/mfa/disable/`    | Disables MFA for the authenticated user <br>_Planned feature_ |

---

## 🔐 Setup Flow

1. User initiates MFA pairing
2. App generates secret + QR code via `libs.mfa_authenticator`
3. Returns base64 QR image or URI
4. User scans and enters token
5. Backend verifies token → enables MFA

---

## ✅ TDD Strategy

### Unit Tests
- Secret creation and encryption
- Token validation logic
- View serialization and error handling

### Integration Tests
- End-to-end: generate → pair → validate
- Token expiration / drift window edge cases

---

## 🤖 LLM Implementation Guidelines

- Do not store plain secrets — always encrypt in `MFASecret`
- Use `libs.mfa_authenticator` internally for pairing and validation
- Provide clean views with DRF serializers
- Do not expose token content or secret
- Frontend must submit token via `/mfa/verify/` for validation

---
