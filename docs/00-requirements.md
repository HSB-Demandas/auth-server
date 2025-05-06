

# Auth Server — Requirements Documentation

This document consolidates all requirements, risks, and success criteria for the centralized authentication server built with Django.

---

## ✅ Functional Requirements

### 1. User Authentication & Session Management
- Support traditional login via email/username and password.
- Support social login with Google OAuth2.
- Validate credentials and issue JWT (access + refresh) tokens.
- Synchronous session control using HttpOnly and SameSite cookies.

### 2. User Registration
- Manual registration via form.
- Auto-registration via first social login.
- Configurable flag `ALLOW_AUTO_REGISTRATION` to enable/disable.

### 3. Email Verification
- Send verification email on registration.
- Block login for unverified users if `REQUIRE_EMAIL_VERIFICATION` is enabled.

### 4. Multi-Factor Authentication (MFA)
- MFA via Twilio SMS.
- MFA via authenticator apps with QR code.
- Optional MFA enforcement using `ENABLE_MFA` flag.

### 5. Password Management
- Enforce password complexity rules.
- Support password hash rotation and upgrade.
- Enforce password change on next login via `FORCE_PASSWORD_ROTATION`.

### 6. Application Management
- Admin can register applications via Django Admin.
- Each app has its own public key for JWT validation.
- Applications define requested scopes and permissions.

### 7. User Profile
- Profile enrichment after registration.
- Fields include name, avatar, optional fields (e.g., phone).
- User-defined visibility for each profile field (public/private/per-app).

### 8. Permissions & Authorization
- Matrix-based permissions per user/application.
- Permissions included in JWT claims.
- RBAC (Role-Based Access Control) enforcement at API level.

### 9. Token Management
- JWT with expiration and custom claims.
- Refresh token issuance and renewal via secure API.
- Token validation endpoint for async clients.

### 10. Notification System
- Notify users on login from new device/browser.
- Allow users to report unrecognized sessions, triggering forced re-authentication.

### 11. Admin Interface (Django Admin)
- Manage users, sessions, applications, public keys, permissions.
- Visual interface to control MFA flags, auto-registration, and token policies.

---

## 🚫 Non-Functional Requirements

### 1. Security & Compliance
- OWASP-compliant design.
- GDPR/LGPD-aligned data processing and retention.
- Use of secure cookies and encrypted token storage.

### 2. Performance & Scalability
- Stateless JWT-based APIs for high scalability.
- Redis optional for caching sessions and throttling.

### 3. Reliability
- Retry mechanism for external services (e.g., Twilio, email).
- Logging and audit trails for authentication events.

### 4. Maintainability
- Modular Django app structure.
- Django settings for all toggles (e.g., MFA, auto-registration).

### 5. Usability
- Mobile-responsive frontend.
- Fully accessible HTML templates for forms and login.

---

## 🏰 Multitenancy & Realm Support

To support isolated authentication domains (realms), the system must implement a multitenant architecture. Each realm acts as an isolated namespace for:

- Users
- Applications
- Permissions
- Policies
- Tokens

### 🔐 Realm Requirements

- Each user belongs to a single realm
- Each application is registered within a single realm
- Permissions and roles are scoped to a realm
- Tokens must include the realm identifier and cannot be used across realms
- Admin interface must allow managing multiple realms independently
- Realm-based filtering must apply to all API queries (e.g., list users, validate token)
- Realm context is required for all operations, either via:
  - Header (`X-Realm`)
  - JWT claim
  - Context propagation in internal services

> Note: Realm is analogous to a tenant or authentication domain in other systems.

---

## ⚠️ Risks

| Risk | Description | Mitigation |
|------|-------------|------------|
| Email delivery failures | Email provider may fail to send verification or notification emails | Implement retries, use transactional email provider |
| MFA unavailability | Twilio or user device unavailable during login | Allow fallback (if configured), cache previous logins |
| Token compromise | Refresh or access token leaked or stolen | Use short-lived access tokens and track refresh token origin |
| Misconfigured permissions | Applications might request unintended scopes | Explicit admin validation of scopes and claims |
| User confusion on login flow | Redirect chains and MFA may confuse users | Provide clear messaging, fallback and retry support |

---

## 🎯 Success Criteria

- Users can log in using either credentials or Google.
- Tokens include the correct claims and expiration details.
- Email verification and MFA flows work as expected.
- Applications validate tokens using the provided public key.
- Admins can register applications and define their scopes and public keys.
- Sessions behave securely (e.g., no access without verification or MFA).
- All functional flags are configurable and tested.

---
