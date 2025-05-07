# Functionalities

This document outlines the key functionalities of the Auth Server, grouped by scope and aligned with the needs of the defined personas. Each functionality is a strategic capability that empowers users to achieve their objectives securely and efficiently.

The primary goal of this system is to provide a centralized, secure, and extensible identity and access management platform that supports modern authentication standards while enabling flexible user onboarding, permission control, and session management. Through its design, the system aims to:

- Simplify authentication across multiple applications
- Empower users with control over their identity and privacy
- Enable administrators to enforce strong security policies
- Support developers with seamless integration tools
- Ensure operators can maintain and monitor the infrastructure safely

Each functionality listed below contributes to these goals, mapped to specific personas and evaluated through clear success criteria and possible edge cases.

---

## 📈 Metrics & Observability

| Functionality                         | Personas                          | Description                                                                   | Goals                                                       | Success Criteria                                                               | Edge Cases                                                                           |
|--------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Prometheus-Compatible Metrics        | System Operator                   | Collect metrics for logins, sessions, errors, and events                      | Improve observability and operational visibility            | Metrics accessible at `/metrics/`; exported to Prometheus or other tools       | Misconfigured exporter, metric explosion                                             |
| Realm-Scoped Metrics                 | Admin                             | Metrics are scoped per realm where applicable                                 | Per-tenant visibility for security and operational metrics  | Realm-filtered metrics return accurate counts                                  | Cross-realm leakage, missing tenant isolation                                       |

---

## 🧾 Audit Logging

| Functionality                         | Personas                          | Description                                                                   | Goals                                                       | Success Criteria                                                               | Edge Cases                                                                           |
|--------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Audit Immutable Logs                 | Admin, System Operator            | Records sensitive actions: role changes, logins, user edits, app configs      | Traceability and forensic support                          | Logs are immutable, searchable, scoped to realm                                 | Event loss, excessive noise, storage limits                                         |
| Pub/Sub-Registered Auditable Models  | Developer                         | Models can register themselves to auto-log via signal                          | Decoupled audit integration                                 | Log entries generated on create/update/delete of registered models             | Excess logging, malformed metadata, circular triggers                              |

---

## 📍 Security Events & Device Trust

| Functionality                         | Personas                          | Description                                                                   | Goals                                                       | Success Criteria                                                               | Edge Cases                                                                           |
|--------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Known Device Tracking                | End User, Admin                   | Associates logins with trusted devices (IP + User Agent)                      | Detect unauthorized access attempts                         | Devices logged on first login; shown to user                                     | Legitimate device flagged, user doesn’t remember history                            |
| Suspicious Login Notification        | End User                          | Notifies when login occurs from an unrecognized device                        | Alert on potentially malicious activity                     | Notification sent, user confirms or revokes device                              | Notification skipped, false positive                                                |

---

## 📤 User Data Export

| Functionality                         | Personas                          | Description                                                                   | Goals                                                       | Success Criteria                                                               | Edge Cases                                                                           |
|--------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| GDPR-Compliant Data Export           | End User                          | Authenticated users can export all relevant data (profile, roles, sessions)   | Legal compliance and user transparency                     | JSON export endpoint returns complete and accurate user-related data           | Missing fields, unavailable integrations (e.g., audit missing), export too large    |

---

## ✅ Consent Management

| Functionality                         | Personas                          | Description                                                                   | Goals                                                       | Success Criteria                                                               | Edge Cases                                                                           |
|--------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Granular Consent                     | End User, Admin                   | Tracks explicit user consent for communication types or processing purposes   | Compliance with data regulations                            | User consents saved per type; revocation respected                             | Consent not applied in downstream system, confusion with terms acceptance           |

---

## 🚦 Rate Limiting & Abuse Protection

| Functionality                         | Personas                          | Description                                                                   | Goals                                                       | Success Criteria                                                               | Edge Cases                                                                           |
|--------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Redis-Based Rate Limiting            | System Operator, Developer        | Throttles login, registration, or sensitive endpoints                         | Protect from brute-force and flood attacks                  | Excessive attempts are blocked with 429 response                                | False positives from shared IP, missing reset, race condition                       |
| Scoped Limit Control (IP/User/Realm) | System Operator                   | Limiters apply to IP address, user identity, or realm context                 | Granular and tenant-aware protection                        | Limits can be adjusted and independently applied                                | Missing scope detection, collision of key hashes                                    |

## 🔐 Authentication & Session

| Functionality                     | Personas                             | Description                                                                                       | Goals                                                            | Success Criteria                                                                         | Edge Cases                                                                                   |
|----------------------------------|--------------------------------------|---------------------------------------------------------------------------------------------------|------------------------------------------------------------------|------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| Traditional and Social Login     | End User, Client Developer           | Login using email/password or Google OAuth2. May be affected by system states like MFA required. | Provide flexible and secure access methods                      | Login works via both methods; JWT generated with correct claims                          | OAuth failure, unverified email, MFA not completed                                          |
| Session Management via Cookies   | End User, System Operator            | Sessions controlled via HttpOnly cookies and redirect flows                                      | Enable secure, sync sessions across apps                        | Sessions persist and expire properly, redirection works as expected                      | Expired cookies, tampered sessions, concurrent expiration                                   |
| MFA Enforcement                  | End User, Admin                      | Requires second authentication factor (Twilio SMS or Authenticator App). Configurable flag.       | Improve account security                                        | MFA triggered after primary login when enabled                                           | SMS not received, app token expired, device unavailable                                     |
| Forced Password Change           | End User, Admin                      | Enforces password renewal on next login based on system flag or security policy.                  | Ensure account hygiene and response to threats                 | User redirected to change password, blocked until updated                                | Password change skipped, repeated expired tokens                                            |
| Password Rotation & Expiry       | End User, Admin                      | Supports expiry policies and rotation enforcement via settings.                                   | Maintain strong credentials over time                         | Password age tracked, old hashes recognized, prompt on expiry                            | Rotation blocked due to reuse, old hash type rejected                                       |
| Passkey-Based Authentication     | End User, Developer                  | Authenticate using WebAuthn-based passkeys instead of passwords                                  | Provide modern, secure passwordless authentication             | Successful login with registered passkey; proper challenge/response exchange             | Unsupported browser, invalid signature, passkey not found for user                           |

---

## 👤 User Registration & Profile

| Functionality                     | Personas                          | Description                                                                                     | Goals                                                       | Success Criteria                                                             | Edge Cases                                                                 |
|----------------------------------|-----------------------------------|-------------------------------------------------------------------------------------------------|-------------------------------------------------------------|------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| Manual and Auto-Registration     | End User, Authentication Admin    | Supports registration via form or social login. Configurable via `ALLOW_AUTO_REGISTRATION`.     | Easy onboarding, admin control of access                    | Users register through both methods, flag behavior is respected             | Missing social login data, incomplete form, auto-reg disabled              |
| Profile Enrichment & Visibility  | End User                          | Users can update profile and control visibility of each field per app or publicly.              | Personalization and privacy                                | Visibility rules apply, apps only see authorized fields                     | Apps request hidden fields, user edits protected fields                    |
| Profile Schema Enforcement       | End User, Admin                   | Allows admins to define required fields and validations for profile completion.                 | Maintain data quality and personalization                  | Incomplete profiles flagged, required fields enforced                       | Field omitted or invalid during auth-linked registration                   |
| Passkey Credential Management    | End User                          | View, register, label, and revoke FIDO2/WebAuthn credentials                                   | Let users manage trusted devices for login                  | Users can register passkeys and manage them securely                        | Duplicate key ID, user deletes all credentials accidentally                |

---

## 🛡 Identity Verification

| Functionality                        | Personas                          | Description                                                                 | Goals                                                           | Success Criteria                                                                  | Edge Cases                                                                                  |
|-------------------------------------|-----------------------------------|-----------------------------------------------------------------------------|-----------------------------------------------------------------|-----------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Email Verification                  | End User, Authentication Admin    | Sends verification email and blocks login until verified (if configured).   | Ensure valid user identity                                      | Verification emails are sent; status updated; login blocked if required         | Email not delivered, expired/invalid token, user never confirms                              |
| Login Notification & Device Tracking| End User, Admin                   | Notifies user of new device login, allows action and device trust mgmt.     | Improve awareness and account safety                            | Notification sent; trust or re-auth flow triggered if unrecognized              | User ignores alert; legitimate login flagged; forced logout unexpectedly                     |
| New Device Login Recovery Flow      | End User                          | Enables secure reauthentication on unknown devices.                         | Prevent unauthorized access from unknown environments           | User reauthenticates via fallback methods (MFA or password)                     | Device fingerprint mismatch misclassified; user locked out unintentionally                   |

---

## 🔒 Access Control & Permissions

| Functionality                    | Personas                          | Description                                                                 | Goals                                                       | Success Criteria                                                                 | Edge Cases                                                                      |
|---------------------------------|-----------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Matrix-based Permissions & RBAC | Authentication Admin, Developer   | Uses matrix per user/app and RBAC to include permissions in JWT claims     | Fine-grained control over what users/apps can access        | JWT contains correct permissions; apps enforce access based on roles           | Misassigned permissions, role escalation, app requests unapproved scope        |
| Scoped Claims in JWT            | Client Developer                  | Apps request and receive only specific scopes per token                    | Enforce least-privilege and context-specific access          | Requested scopes match claims; unapproved scopes are denied                     | App requests exceed permissions; user scopes misaligned                        |

---

## 🔁 Token Lifecycle Management

| Functionality                  | Personas                          | Description                                                                 | Goals                                                         | Success Criteria                                                                | Edge Cases                                                                         |
|-------------------------------|-----------------------------------|-----------------------------------------------------------------------------|----------------------------------------------------------------|-----------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| Token Issuance & Validation   | End User, Client Developer        | Issues JWT with expiration, scopes and public key validation                | Provide stateless secure identity for APIs                    | JWT has correct data, validated using stored public key                         | Expired token, old key, invalid claims                                             |
| Refresh Token Flow            | End User, Client Developer        | Allows session renewal via refresh tokens and endpoint                      | Maintain long-lived sessions securely                        | Access token renewed with refresh token when valid                              | Refresh token reuse, revoked token, refresh without session                        |
| Token Revocation & Invalidation| Admin                             | Admins can revoke tokens or force invalidation from dashboard               | Cut off access after compromise or suspicious activity       | Revoked tokens are blocked across all endpoints                                 | Delay in propagation; token misuse before revocation completes                     |

---

## ⚙️ Administration & Config

| Functionality                          | Personas                          | Description                                                                   | Goals                                                         | Success Criteria                                                              | Edge Cases                                                                        |
|---------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|----------------------------------------------------------------|----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Application Registration & Key Mgmt   | Authentication Admin              | Register apps and generate public keys via Django Admin                       | Central control over app identity and access                 | Applications can validate tokens; keys downloadable or rotated                | Missing key, mislinked key, app failure to sync                                    |
| Policy Flags Management               | Authentication Admin              | Enables/disables features like auto-registration, email verification, MFA     | Control global platform behavior                            | Each flag impacts logic and flow as expected                                  | Inconsistency between flags (e.g., MFA required + no second factor configured)     |
| Password Policy Configuration         | Authentication Admin              | Enforces rules on password strength, expiration, reuse, and hashing algorithm | Ensure secure credential hygiene                            | Weak passwords rejected, password age tracked, hash format updated             | Old accounts use unsupported hash, user repeatedly reuses same passwords           |
| State-based Flow Switching            | Authentication Admin              | System flow switches based on user/account state (e.g., force reset, lockout) | Enforce progressive control logic                            | Auth flow changes dynamically based on states                                  | Lockout due to error, states not resetting properly                                |

---

## 📦 Application & Realm Management

| Functionality                         | Personas                          | Description                                                                   | Goals                                                       | Success Criteria                                                               | Edge Cases                                                                           |
|--------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Realm Isolation                      | Admin, System Operator            | Isolates all configurations, users, roles, and policies per realm             | Enable multi-tenancy safely                                 | Data and configurations fully isolated per realm                                 | Realm misconfiguration leaks shared settings                                         |
| Application Configuration            | Admin                             | Configure app details, providers, MFA requirements, terms version, etc.       | App-specific authentication behavior                        | App behaves as configured; only enabled providers available                      | Providers not available, configuration mismatch                                     |
| API Key & Public Key Management      | Admin                             | Generate API keys and public JWT verification keys for each app               | Secure token validation by external consumers               | Keys are downloadable and used for token verification                           | Mismatched keys, keys missing from header                                           |
| Terms Version Enforcement            | Admin                             | Each app can enforce accepted version for privacy and usage terms             | Legal compliance and auditability                           | Users blocked from login until current terms are accepted                        | Versions mismatch, acceptance delay                                                 |

---

## 📄 Terms & Compliance

| Functionality                         | Personas                          | Description                                                                   | Goals                                                       | Success Criteria                                                               | Edge Cases                                                                           |
|--------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Terms Versioning                     | Admin                             | Policy and privacy documents are versioned with public access endpoints       | Track historical acceptance                                | Correct versions published; metadata stored                                     | Version rollback, corrupted document                                                |
| Terms Acceptance Tracking            | End User                          | Acceptance of specific terms version is tracked and enforced per user         | Legal proof and flow control                               | User can't proceed until they accept the latest version                         | Incomplete acceptance, duplicate acceptances                                        |
| Cached Terms Endpoints               | Client Developer                  | Serve the latest terms via cached endpoints                                   | Improve performance and stability                          | Content loads from cache; expires properly                                       | Cache invalidation delay, wrong cache hit                                           |

---

## 📬 Notifications

| Functionality                         | Personas                          | Description                                                                   | Goals                                                       | Success Criteria                                                               | Edge Cases                                                                           |
|--------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| In-app Notifications                 | End User                          | Display notifications for user-specific events with icon and action link      | Improve UX and engagement                                  | User sees relevant messages; actionable if needed                               | Wrong recipient, link expiration                                                    |
| Notification Rendering               | Client Developer                  | Icons and links are determined by frontend app and passed with notification   | UI control and extensibility                               | Frontend interprets icon field and URL as intended                              | Icon mismatch, user confusion                                                       |
| Notification Ingestion (PubSub/API) | System Integrator                 | Notifications can be created via PubSub topic or internal API                 | Allow event-based delivery                                 | Notifications created from multiple sources                                     | Duplicates, failure to ingest from malformed source                                |

---

## 📨 Email Communication

| Functionality                         | Personas                          | Description                                                                   | Goals                                                       | Success Criteria                                                               | Edge Cases                                                                           |
|--------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Email Delivery with Multi-provider   | Admin, System Operator            | Send emails using SMTP, SES, Mailgun, etc. with pluggable backend             | Adapt to customer infra and reliability                     | Emails sent successfully via selected provider                                  | Provider outage, formatting issues                                                  |
| Email Template Management            | Admin, Developer                  | Define rich and plain templates with variable substitution                    | Consistent branding and dynamic content                     | Template renders correctly with data populated                                  | Missing placeholder, unsafe HTML                                                    |
| Email Events Support                 | System Operator                   | Support event feedback (delivered, opened, bounced, spam) from providers      | Visibility and monitoring                                  | Events received and processed; status reflected                                 | Event loss, webhook failure                                                         |
| Unsubscribe & Footer Enforcement     | End User                          | Templates include opt-out links and comply with best practices                | Compliance and transparency                                | Unsubscribe works; footer present                                               | Link disabled, user confusion                                                       |

---

## 🔢 MFA and TOTP

| Functionality                         | Personas                          | Description                                                                   | Goals                                                       | Success Criteria                                                               | Edge Cases                                                                           |
|--------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| TOTP Setup and Verification          | End User                          | Generate and verify time-based one-time passwords                             | Enable strong 2FA                                          | QR Code / URI provided; token validated                                          | Clock drift, token reused, TOTP lost                                                |
| TOTP Disable Flow                    | End User                          | Allow user to disable TOTP from their profile                                 | User control and flexibility                              | TOTP disabled upon valid request                                                | Token hijack, forced disable from other session                                     |
| Role-based MFA Requirement           | Admin                             | Role assignments may require TOTP or validated email/phone                    | Granular security enforcement                             | Role blocked until requirements fulfilled                                      | Role inaccessible, validation delay                                                 |

---

## 🔄 Webhooks

| Functionality                         | Personas                          | Description                                                                   | Goals                                                       | Success Criteria                                                               | Edge Cases                                                                           |
|--------------------------------------|-----------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Webhook Subscriptions per App        | Admin                             | Each app can define HTTP endpoints to receive event payloads                  | Integrate with external systems                           | Events sent to correct endpoint with HMAC signature if enabled                 | Endpoint down, retries fail                                                         |
| Retry with Backoff                   | System Operator                   | Retry failed deliveries with exponential backoff and log all attempts         | Reliability and traceability                              | Retries happen at increasing intervals                                          | Retry storm, skipped interval                                                       |
| Delivery Logging                     | Admin                             | Every webhook call attempt is logged with payload, response, and status       | Auditable and debug-friendly                              | Admins can view log and reason for failure                                     | Storage overload, sensitive data logged                                             |

---
