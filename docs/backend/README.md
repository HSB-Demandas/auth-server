# 🛡️ Auth Server Platform - Backend Application

This repository contains the complete backend architecture and implementation plan for the Authentication Server — a modular and scalable authentication and authorization system inspired by Auth0 and AWS IAM principles.

---

## 🧭 Project Overview

The Auth Server is a **multi-tenant identity and access management platform** designed for secure, extensible authentication, authorization, user management, and event-driven communication through webhooks.

The project is implemented in **Django**, with each component encapsulated as a standalone Django app or external library. Each app is reusable, testable, and designed with long-term maintainability in mind.

LLMs and human developers can navigate this repository to scaffold or extend apps based on detailed documentation and strict architectural conventions.

---

## 🧱 Architecture Layers

- **Communication Layer**: All HTTP API endpoints (exposed per app)
- **Application Layer**: Business rules and API orchestration
- **Domain Layer**: Core models and business rules
- **Infra Layer**: Email/SMS sending, TOTP, PubSub via SNS/SQS, external APIs
- **Notification Layer**: Handles delivery of in-app, email, and SMS notifications

---

## 🏗 Architecture Reference

For a detailed explanation of the system layers and their responsibilities, see:

➡️ [System Architecture Overview](01-architecture.md)

---

## 🧩 Core Applications

### 1. `apps.realms`  
- Represents isolated environments (e.g., tenants)  
- Highest-level scoping for users and applications  

### 2. `apps.applications`  
- Manages client app registration, API keys, and JWT public keys  
- Configures enabled providers, MFA policies, and terms versions  

### 3. `apps.users`  
- Manages user profiles, self-registration, password and linked providers  
- Tracks email/phone/TOTP validation and consent to policy/terms  
- Includes user data export endpoint  

### 4. `apps.auth`  
- Handles login, token issuance, MFA and session lifecycle  
- Supports email/SMS/TOTP/passkey challenges  
- Offers token introspection endpoint for external integrations  

### 5. `apps.permissions`  
- Defines and enforces role-based access control per realm/app  
- Roles may require user validations to be active  

### 6. `apps.compliance`  
- Versioned privacy and terms documents with cached endpoints  
- Tracks user acceptance and individual consent preferences  

### 7. `apps.notifications`  
- In-app notification delivery per user  
- Allows configurable icon and action-link metadata  

### 8. `apps.webhooks`  
- App-level webhook registration, retry, and logging  
- HMAC signature and delivery status tracking  

### 9. `apps.audit`  
- Immutable log of sensitive operations for compliance and traceability  
- Logs user, role, permission, and admin actions per realm  

### 10. `apps.security_events`  
- Tracks known devices and detects suspicious login attempts  
- Alerts users on new device activity and allows confirmation  

### 11. `apps.metrics`  
- Exposes Prometheus-style metrics (login success, role usage, webhooks)  
- Enables observability for system operators and realm admins  

### 12. `apps.passkeys`  
- Manages WebAuthn/FIDO2 passkey credentials  
- Allows users to register, label, and revoke passkeys  
- Integrates with login via `apps.auth`  

---

## 📦 Supporting Libraries

All libraries are standalone, testable and include TDD and integration specs:

### ✅ `libs.totp`
- TOTP (RFC 6238) handling for code generation and verification

### ✅ `libs.twilio`
- SMS send and code verification via Twilio

### ✅ `libs.mailer`
- Multi-provider email sender with optional event tracking
- HTML template rendering with unsubscribe support

### ✅ `libs.aws`
- SNS + SQS integration for internal PubSub
- Async consumer with typed payload validation (Pydantic)

### ✅ `django_hsb_ratelimit`  
- Django-integrated Redis-based rate limiting  
- Decorators and DRF-compatible throttling for IP, user, realm, or composite scope  

### ✅ `libs.passkeys`
- Manages FIDO2/WebAuthn challenge generation and verification
- Used for login and credential registration

---

## 🔧 Configuration Guidelines

- All sensitive configurations must be injected via environment variables
- Secrets must be encrypted per deployment
- Each app includes example `.env` variables and documentation

---

## 🧠 LLM Guidelines

- All apps are self-contained and documented in markdown
- Each feature is mapped to endpoints and (where relevant) webhook triggers
- Flows like registration, MFA, session handling, and token issuance are clearly separated between apps
- Test strategies are documented per app: unit and integration
- Passkey-based login is managed by `apps.auth`, while credential lifecycle is handled in `apps.passkeys`
- WebAuthn protocol support uses `python-fido2` internally

---

## 📚 Documentation

Each app is documented individually:

- `01-realms-app.md`
- `02-applications-app.md`
- `03-permissions-app.md`
- `04-users-app.md`
- `05-auth-app.md`
- `06-webhooks-app.md`
- `07-security-app.md`
- `08-metrics-app.md`
- `05-ratelimit.md`
- `django_hsb_mailer.md`
- `django_hsb_twilio.md`
- `django_hsb_totp.md`
- `django_hsb_notifications.md`

---

## ✅ Status

Backend planning is **complete** and ready for implementation. Each app includes:

- Complete models
- Endpoint structure
- Permissions
- Events (where applicable)
- TDD plans

---
