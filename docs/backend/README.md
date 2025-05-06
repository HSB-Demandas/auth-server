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
- Registered apps with config like allowed providers, MFA policies
- Generates API keys and JWT public keys

### 3. `apps.users`
- Manages user profile, provider links, password, TOTP/email/phone validation
- Tracks terms and privacy acceptance
- Supports self-registration per app configuration

### 4. `apps.auth`
- Handles login, token issuance, session lifecycle
- Supports email/SMS/TOTP challenges
- Exposes session management and MFA endpoints

### 5. `apps.permissions`
- Role-based access control with permission enforcement
- Roles may require email, phone, or TOTP to be valid

### 6. `apps.compliance`
- Versioned terms and privacy documents
- Cached endpoints for policy fetching

### 7. `apps.notifications`
- In-app notifications per user
- Configurable display icons and action links

### 8. `apps.webhooks`
- Application-level webhook registration
- Supports retries, logs, HMAC signature

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

---

## 📚 Documentation

Each app is documented individually:

- `01-realms-app.md`
- `02-applications-app.md`
- `03-permissions-app.md`
- `04-users-app.md`
- `05-auth-app.md`
- `06-webhooks-app.md`
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
