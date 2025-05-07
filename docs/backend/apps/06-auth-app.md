# 🔐 Django App: `apps.auth`

This app manages authentication and session-related flows for the platform. Inspired by `django-allauth`, it is designed to support OAuth2-style login workflows, second-factor validation, and active session handling — all scoped per realm and application.

---

## 🎯 Purpose

- Authenticate users via multiple provider types
- Enforce code validation: email, SMS, TOTP
- Issue and manage JWT access and refresh tokens
- Enforce MFA endpoints after primary authentication
- Handle session inspection and revocation

---

## 📁 App Structure

```
apps/
└── auth/
    ├── __init__.py
    ├── apps.py
    ├── models.py             # Track tokens, codes, sessions
    ├── views.py              # Login, logout, token, session APIs
    ├── urls.py               # Expose authentication endpoints
    ├── serializers.py        # DRF serializers
    ├── endpoints/
    │   ├── auth_endpoint.py      # Primary authentication
    │   ├── mfa_endpoint.py       # MFA orchestration
    │   ├── code_endpoint.py      # Code confirmation for email/SMS/TOTP
    │   ├── passkey_endpoint.py       # WebAuthn login support
    ├── sessions/             # Session inspection, cleanup
    ├── tokens.py             # Token issuance and validation
    ├── validators.py         # Access policy and provider checks
    ├── admin.py
    ├── migrations/
    └── tests/
        ├── unit/
        └── integration/
```

---

## 🔐 Authentication Endpoints

- Username/password login
- Social login (Google, Apple, etc.)
- Token issuance: `access_token`, `refresh_token`
- Refresh token handling
- Token revocation
- Passkey login using WebAuthn challenge and response

---

## 🔁 Code Confirmation Endpoints

| Endpoint Type   | Description                               |
|-------------|-------------------------------------------|
| Email Code  | Code sent to verified email               |
| SMS Code    | Code sent via Twilio integration          |
| TOTP        | Code generated via authenticator app      |

Codes are time-limited and rate-limited, and tied to the user's session context.

---

## 🧱 MFA Endpoints

- MFA policies are defined per user or enforced by role
- Configured options include TOTP, email code, or SMS code
- Challenge occurs after initial login and before issuing tokens

---

## 🧭 Session Management

- Active session listing by user
- Logout current session
- Logout all sessions (revoke all tokens and invalidate codes)

---

## 🧠 Design Considerations

- All token activity is scoped by realm and application
- MFA challenge responses must validate code and method
- Session tracking includes IP, user-agent, and timestamp

---

## 🔗 API Endpoints

### 🔐 Authentication Endpoints

| Method | URL                         | Description                                     |
|--------|-----------------------------|-------------------------------------------------|
| POST   | `/api/auth/login/`         | Authenticate user with credentials or provider |
| POST   | `/api/auth/token/refresh/` | Issue new access token via refresh token       |
| POST   | `/api/auth/token/revoke/`  | Revoke current token                           |
| POST   | `/api/auth/passkey/begin/`          | Begin WebAuthn passkey login challenge |
| POST   | `/api/auth/passkey/complete/`       | Complete login with passkey assertion |

### 🔁 Code Confirmation Endpoints

| Method | URL                                 | Description                           |
|--------|-------------------------------------|---------------------------------------|
| POST   | `/api/auth/code/email/`            | Send email confirmation code          |
| POST   | `/api/auth/code/email/verify/`     | Verify code from email                |
| POST   | `/api/auth/code/sms/`              | Send SMS confirmation code            |
| POST   | `/api/auth/code/sms/verify/`       | Verify code from SMS                  |
| POST   | `/api/auth/code/totp/verify/`      | Verify TOTP from authenticator app    |

### 🧱 MFA Challenge Endpoints

| Method | URL                              | Description                             |
|--------|----------------------------------|-----------------------------------------|
| POST   | `/api/auth/mfa/challenge/`      | Request MFA challenge for logged user   |
| POST   | `/api/auth/mfa/verify/`         | Submit MFA verification response        |

### 🧭 Session Management Endpoints

| Method | URL                              | Description                             |
|--------|----------------------------------|-----------------------------------------|
| GET    | `/api/auth/sessions/`           | List active sessions                    |
| DELETE | `/api/auth/sessions/current/`   | Terminate current session               |
| DELETE | `/api/auth/sessions/all/`       | Terminate all sessions                  |

---

## 📣 Webhook Events

The following events may be emitted by this app:

| Event Name             | Description                                 |
|------------------------|---------------------------------------------|
| `auth.login.success`   | A user successfully authenticated           |
| `auth.login.failed`    | A failed authentication attempt             |
| `auth.token.issued`    | A token was generated                       |
| `auth.token.revoked`   | A token was revoked                         |
| `auth.mfa.challenge`   | MFA challenge was triggered                 |
| `auth.mfa.verified`    | MFA challenge was successfully completed    |
| `auth.session.created` | A session was created                       |
| `auth.session.revoked` | A session was revoked                       |

---

## 🔍 JWT Introspection Endpoint

To support third-party and external application integration (including OIDC-compatible flows), the `apps.auth` app provides a secure token introspection endpoint.

### 🔗 Endpoint

| Method | URL                          | Description                                         |
|--------|------------------------------|-----------------------------------------------------|
| POST   | `/api/auth/token/introspect/`| Validates a JWT token and returns decoded metadata  |

### 📤 Expected Input

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 📥 Response Format

```json
{
  "active": true,
  "scope": "read write",
  "user_id": "b23f...",
  "username": "john@example.com",
  "exp": 1680000000,
  "iat": 1670000000,
  "aud": "app_id",
  "iss": "https://auth.example.com"
}
```

- If the token is invalid or expired, `"active": false`.

### 🛡 Security

- Requires an API key with access to the application.
- Tokens are validated against:
  - Realm/application signature
  - Audience and expiration
- Prevents local token misuse by enforcing introspection flow.

---

## 🔏 Passkey Login Flow

This flow allows a user to log in using a registered WebAuthn passkey (managed by `apps.passkeys`).

### 🔗 Endpoints

| Method | URL                      | Description                                  |
|--------|--------------------------|----------------------------------------------|
| POST   | `/api/auth/passkey/begin/`    | Initiates login challenge for WebAuthn       |
| POST   | `/api/auth/passkey/complete/` | Completes login using assertion and passkey  |

### 📤 Expected Input (begin)

```json
{
  "username": "john@example.com"
}
```

### 📥 Response (begin)

```json
{
  "challenge": "<base64>",
  "rpId": "example.com",
  "allowCredentials": [...],
  "timeout": 60000
}
```

### 📤 Expected Input (complete)

```json
{
  "id": "...",
  "rawId": "...",
  "type": "public-key",
  "response": {
    "clientDataJSON": "...",
    "authenticatorData": "...",
    "signature": "...",
    "userHandle": "..."
  }
}
```

### 📥 Response (complete)

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "expires_in": 3600,
  "token_type": "bearer"
}
```

### 🛡 Security Considerations

- Challenges are scoped to the realm and expire after a short period.
- Public key validation and signature checks are performed.
- Only passkeys registered via `apps.passkeys` can be used.

---

## ✅ TDD Strategy

### Unit Tests
- Token creation and revocation
- MFA endpoint triggering and resolution
- Code generation, validation, and expiration

### Integration Tests
- Full login + MFA + token endpoint flow
- Session inspection and logout
- Token refresh behavior

---

## 🤖 LLM Implementation Guidelines

- Validate realm and application context in every authentication request
- Respect configured providers per application and user
- Reuse `apps.users` model state (e.g. verified email) for conditional endpoints
- Use standardized JWT claims with expiration, audience, and signature
- Session revocation must invalidate all relevant tokens and codes

---
