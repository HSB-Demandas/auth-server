
# 🛡️ Auth Server

A centralized, secure, and modular authentication platform built with Django. It supports multi-tenant applications by providing complete Identity and Access Management (IAM) features, including OAuth2 authentication, user and app isolation, session control, multi-factor authentication (MFA), role-based permissions, audit logging, and integrations.

## ✨ Key Features

- Authentication via password or social login (Google)
- Self-registration via form or first-time social login
- Email verification with optional login restriction until confirmed
- Multi-factor authentication (MFA) via Twilio SMS or authenticator apps
- JWT access and refresh token issuance and renewal
- Synchronous session control via secure cookies
- Asynchronous API for token validation and redirection
- Django Admin integration for:
    - Application registration and permission assignment
    - Public key generation and management for JWT verification
    - Password rotation and complexity policy management
- Login notifications for new devices
- Force password change on next login

## 🛠️ Technologies Used

- **Backend**: Django
- **Database**: PostgreSQL
- **Cache / Session**: Redis (optional)
- **MFA**: Twilio
- **Tokens**: JWT
- **Management**: Django Admin

## 🔐 Security

The server follows OWASP best practices and can be configured to meet compliance requirements such as SOC 2, LGPD, and GDPR. Includes:
- Encryption of sensitive data
- Password hashing with support for multiple algorithms
- Password policies (complexity and rotation)
- Event logging and audit trails
- Role-based access control (RBAC)
- Brute-force attack protection

## 🔁 Authentication Flow

1. The user accesses the client application and is redirected to the authentication server.
2. Authentication options:
    - Password login
    - Google account login
3. If enabled, MFA is required.
4. Upon success, the user is redirected back with a valid JWT.
5. The client application can validate and refresh tokens asynchronously.

## ⚙️ Configuration Flags

- `ALLOW_AUTO_REGISTRATION`: enables/disables self-registration
- `REQUIRE_EMAIL_VERIFICATION`: blocks login for unverified users
- `FORCE_PASSWORD_ROTATION`: requires password change on next login
- `ENABLE_MFA`: enables multi-factor authentication

## 📬 Notifications

- Email verification
- Login from a new device
- Suspicious login confirmation

## 📤 API and Session

- Asynchronous refresh token validation
- Secure redirect flow for session renewal
- Secure storage via HttpOnly + SameSite cookies

## 🧩 Extensibility

- Want to add another social network? Add a backend provider.
- New MFA method? Plug it into the pipeline.
- New app? Register it and assign permissions in Django Admin.

---

> This project follows a modern, centralized, and scalable Identity and Access Management (IAM) architecture.

## ✨ Highlights

- 🔐 Password and social login (e.g. Google)
- 🧾 Terms, privacy policies, and granular user consent tracking
- ✅ Multi-Factor Authentication (MFA): SMS (Twilio) and TOTP apps
- 🔄 JWT issuance with refresh and introspection endpoints
- 🧩 Realm and Application isolation for multi-tenant architecture
- 🔁 OAuth2-compatible login and token workflows
- 👤 User registration, provider linking, and profile management
- 🎯 Role-Based Access Control (RBAC) with per-role validation rules
- 🔒 Device-based suspicious login detection
- 📬 In-app and external notifications
- 📤 Webhooks with retries and HMAC signing
- 📈 Prometheus-style metrics for system observability
- 📚 Immutable audit logs for compliance and traceability
- ⚙️ Django Admin interfaces for all resources

---

## 🧱 Architecture Overview

See [01-architecture.md](01-architecture.md) for a full breakdown of layers and responsibilities.

### Main Django Apps

- `apps.auth`: login, token, session, MFA
- `apps.users`: user registration, profile, validation, data export
- `apps.permissions`: role-based permissions and enforcement
- `apps.applications`: app registration and config
- `apps.realms`: multi-tenant realm boundaries
- `apps.notifications`: user-facing notification delivery
- `apps.compliance`: terms, policy, and consent tracking
- `apps.audit`: system action logs
- `apps.security_events`: login/device monitoring
- `apps.webhooks`: event-based external delivery
- `apps.metrics`: login/session/role observability

### Internal Libraries

- `django_hsb_twilio`: Twilio SMS for messaging and verification
- `django_hsb_mailer`: Pluggable multi-provider email system
- `django_hsb_totp`: TOTP-based MFA
- `django_hsb_ratelimit`: Redis-based rate limiting decorators and throttles

---

## 🔐 Security & Compliance

The system supports OWASP guidelines and is aligned with GDPR, LGPD, and SOC 2 readiness. It includes:

- Password policy and enforced rotation
- Multi-layered session and cookie security
- Role validation and MFA requirement enforcement
- Device trust and login history tracking
- Full audit trail of sensitive actions
- User data export endpoint
- Scalable rate limiting for abuse protection

---

## ⚙️ Runtime Flags

| Flag                          | Description                                 |
|-------------------------------|---------------------------------------------|
| `ALLOW_AUTO_REGISTRATION`     | Enable or disable self-registration         |
| `REQUIRE_EMAIL_VERIFICATION`  | Require email validation before login       |
| `FORCE_PASSWORD_ROTATION`     | Enforce password update after login         |
| `ENABLE_MFA`                  | Enable multi-factor authentication globally |

---

## 📚 Documentation Index

- [00-requirements.md](00-requirements.md)
- [01-architecture.md](01-architecture.md)
- [02-functionalities.md](02-functionalities.md)
- [03-security.md](03-security.md)
- [04-users-app.md](04-users-app.md)
- [05-auth-app.md](05-auth-app.md)
- [06-webhooks-app.md](06-webhooks-app.md)
- [07-security-app.md](07-security-app.md)
- [08-metrics-app.md](08-metrics-app.md)
- [05-ratelimit.md](05-ratelimit.md)
