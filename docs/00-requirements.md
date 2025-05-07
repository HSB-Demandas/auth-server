

# Auth Server — Requirements Documentation

This document consolidates all requirements, risks, and success criteria for the centralized authentication server built with Django.

---

## ✅ Functional Requirements

### 1. User Authentication & Session Management
- Support traditional login via email/username and password.
- Support social login (Google, others via extensible provider support).
- Validate credentials and issue JWT (access + refresh) tokens.
- JWT introspection endpoint for external systems.
- Synchronous session control using HttpOnly and SameSite cookies.
- Session revocation and listing.
- Detect and handle suspicious device logins.

### 2. User Registration & Profile
- Manual registration via form.
- Auto-registration via first social login.
- Configurable flag `ALLOW_AUTO_REGISTRATION`.
- Profile enrichment with optional fields (name, avatar, phone).
- Per-field visibility (public/private/per-app).
- User data export endpoint (`/me/export/`).

### 3. Email & Phone Verification
- Send verification email and/or SMS on registration or request.
- Block login if not verified (controlled via flags).
- TOTP support via authenticator apps with QR code.

### 4. Multi-Factor Authentication (MFA)
- Support MFA via SMS (Twilio) or TOTP.
- Optional MFA enforcement via role or application.
- MFA challenge endpoints.
- Track MFA events and logins.

### 5. Password & Provider Management
- Enforce password complexity and rotation.
- Provider linking and unlinking (social + password-based).
- Password change and recovery flows.
- Require email/phone verification before role assignment (configurable).

### 6. Application Management
- Admins can register and manage apps (with JWT keys, provider options).
- Apps have API keys and JWT public keys.
- Define allowed login methods, consent requirements, and policy versions.

### 7. Roles, Permissions & Authorization
- RBAC with roles scoped to realm + application.
- Matrix-based permission enforcement.
- Role assignment policies (MFA, email, phone required).
- Roles included in JWT claims.

### 8. Token Management
- Short-lived access tokens + refresh tokens.
- Token introspection endpoint for verification (`/token/introspect/`).
- Revocation support.

### 9. Notification System
- Notify on login from new device/browser.
- In-app notifications per user.
- Frontend-defined icon + action links.
- Supports ingestion via API or PubSub.

### 10. Webhooks & Integrations
- App-level webhook registration.
- Configurable URL, headers, and subscribed events.
- Retries with backoff and delivery logs.
- HMAC signing support.

### 11. Admin Interface
- Django Admin support for users, apps, sessions, and configuration.
- Role and permission assignment with validation controls.
- Terms/policy enforcement configuration.

### 12. Terms, Policies & Consent
- Versioned privacy and usage terms.
- Terms acceptance blocking login if required.
- User-level consent for specific data uses (e.g. marketing, analytics).
- Consent APIs per realm.

### 13. Observability & Metrics
- Metrics for login success/failure, sessions, registrations, etc.
- Exposed via Prometheus-style endpoint for scraping.

### 17. Passkey (WebAuthn) Support
- Users can register passkeys (FIDO2/WebAuthn) and associate them with their account.
- Login is supported via WebAuthn-based passkeys (challenge/response).
- Passkey management interface for users (list, label, revoke).
- Secure challenge validation using public-key cryptography.
- Admin view of registered passkeys.

### 18. User Consent Management
- Users can manage granular consent types (e.g., analytics, marketing).
- Consent acceptance stored per realm and exposed via API.
- Consent enforced on authentication flows as configured.

### 19. Personal Data Export
- Authenticated users can export their profile, sessions, roles, audit log.
- Export formatted in JSON and optionally sent via email.
- LGPD/GDPR compliant export mechanism.

### 20. Observability & Metrics Enhancements
- Track usage of login methods (password, social, passkey).
- Per-realm metrics for logins, registration, role usage.
- Prometheus-compatible endpoint.

### 14. Audit Logging
- Logs user and admin actions per realm.
- Includes app config, permissions, login, role assignment.
- Immutable and filterable.

### 15. Security Events
- Track login attempts from new or suspicious devices.
- Device confirmation and revocation per user.
- Admins can monitor and revoke unknown devices.

### 16. Rate Limiting & Abuse Protection
- Protect login, registration, and sensitive flows.
- Redis-backed rate limit library (`django_hsb_ratelimit`) with decorators and DRF support.
- Supports user, IP, realm, and composite scopes.

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
