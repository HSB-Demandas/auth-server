# Personas — Auth Server

This document defines the key personas interacting with the centralized authentication system.

---

## 👤 1. Anonymous User

### Description
An unauthenticated visitor attempting to register or log in to an application.

### Responsibilities
- Access registration and login interfaces.
- Submit credentials or use social login to authenticate.
- Accept terms and privacy policy when required.

### Functional Access
- `apps.auth` endpoints for login/token
- `apps.users` for registration (if enabled)
- `apps.compliance` for reading terms

### Security Scope
- Blocked from accessing user resources until authenticated.
- Cannot bypass terms acceptance enforcement.

---

## 👤 2. Registered End User

### Description
An authenticated individual who uses applications integrated with the identity platform.

### Responsibilities
- Log in using password, social auth, or MFA.
- Manage their personal profile and linked providers.
- Complete validation flows (email, phone, TOTP).
- Accept required legal terms.

### Functional Access
- `apps.users`: profile, MFA setup, validation
- `apps.auth`: session and token flows
- `apps.notifications`: view in-app messages
- `apps.compliance`: read and accept terms

### Security Scope
- MFA may be required based on role/app.
- Blocked from specific role permissions until validation is complete.

---

## 🛡️ 3. Realm Administrator

### Description
Responsible for managing tenants (realms), including their apps, users, roles, policies, and webhook integrations.

### Responsibilities
- Define realms and isolate configurations.
- Register new applications.
- Configure webhook endpoints and provider availability.

### Functional Access
- `apps.realms`, `apps.applications`, `apps.webhooks`, `apps.compliance`

### Security Scope
- Elevated permission over realm data and applications.
- Cannot manage data outside their realm.

---

## 🧩 4. Application Administrator

### Description
Manages a specific application registered in a realm.

### Responsibilities
- Configure app settings (MFA, providers, terms enforcement).
- Manage users and assign roles within the app.
- Subscribe webhooks and view app-specific logs.

### Functional Access
- `apps.applications`, `apps.users`, `apps.permissions`, `apps.webhooks`

### Security Scope
- Limited to apps they control within the realm.

---

## 👷 5. Developer / Integrator

### Description
A technical user integrating client applications using the platform's authentication system.

### Responsibilities
- Authenticate via OAuth2.
- Validate JWTs using provided keys.
- Use API keys for app-to-app authentication.
- Track token usage, scopes, and permissions.

### Functional Access
- `apps.auth`, `apps.applications`

### Security Scope
- Limited to keys and scopes authorized for their app.

---

## 🧑‍🔧 6. System Operator / DevOps

### Description
Deploys and manages the infrastructure where the platform runs.

### Responsibilities
- Configure environment variables and rotate secrets.
- Monitor queues, email/SMS delivery, and system health.
- Enable or disable integrations like AWS, Twilio, SMTP.

### Functional Access
- Environment settings, logging systems, infrastructure

### Security Scope
- Full access to backend internals but no access to user data through APIs.

---
