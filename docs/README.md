# Auth Server

This is a centralized and secure authentication server built with Django, designed to provide authentication and authorization for multiple applications. It includes modern features such as social login, multi-factor authentication (MFA), JWT token issuance, and granular permission control.

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
