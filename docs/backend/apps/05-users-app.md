# 🧍 Django App: `apps.users`

This app manages the core user model and profile metadata across the platform. Inspired by Auth0's user design, it integrates provider tracking, role relationships, validation flags, and legal agreement tracking. It supports flexible identity flows and self-registration, scoped by application settings.

---

## 🎯 Purpose

- Extend the core user model with profile, verification, and identity provider information
- Track terms and privacy policy acceptance per version
- Associate users with roles (and thus applications)
- Respect application-level configuration for registration and access
- Manage password creation and update
- Validate and manage email, phone, and TOTP setups
- Link user accounts to providers on login or registration

---

## 🛠 Account Management Responsibilities

This app is responsible for managing user credential mechanisms and identity association, including:

- **Password management**: setting, updating, and validating hashed passwords
- **Email validation**: sending confirmation tokens and flagging as verified
- **Phone validation**: integrating with SMS provider to verify codes
- **TOTP setup and confirmation**: registering MFA keys and validating codes
- **Provider linking**: When a user logs in or registers using a configured provider, their account is automatically linked to that provider for future logins

---

## 🧱 User Model Fields

| Field                             | Type                 | Description |
|----------------------------------|----------------------|-------------|
| `realm`                          | FK to Realm          | Scope user to a single realm |
| `email`                          | EmailField           | Unique per realm |
| `email_verified`                 | BooleanField         | Flag after confirmation |
| `phone_number`                   | CharField            | Optional |
| `phone_verified`                 | BooleanField         | Flag after SMS token confirmation |
| `avatar_url`                     | URLField             | Custom avatar (overrides gravatar) |
| `use_gravatar`                   | BooleanField         | Enables fallback to gravatar |
| `accepted_terms_version`         | CharField            | Latest accepted `terms_of_use` version |
| `accepted_privacy_version`       | CharField            | Latest accepted `privacy_policy` version |
| `auth_providers`                 | ArrayField (Enum)    | E.g. `["google", "username_password"]` |
| `roles`                          | M2M to Role          | Roles assigned to user (via `apps.permissions`) |
| `is_active`                      | BooleanField         | Enabled or suspended |
| `date_joined`                    | DateTimeField        | Registration timestamp |
| `last_login`                     | DateTimeField        | Optional login tracking |

---

## 📁 App Structure

```
apps/
└── users/
    ├── __init__.py
    ├── apps.py
    ├── models.py             # User model and logic
    ├── views.py              # API views for self-registration, profile
    ├── urls.py               # Routes for public/private API
    ├── serializers.py        # DRF serializers
    ├── validators.py         # Provider and policy logic
    ├── admin.py              # Admin integration
    ├── migrations/
    └── tests/
        ├── unit/
        └── integration/
```

---

## 🔐 Identity Providers

- Stored in `auth_providers` (enum list)
- Examples: `google`, `apple`, `username_password`, `magic_link`, etc.
- Must intersect with the set of providers enabled for the Application(s) linked to the user's roles

---

## 📜 Policy Acceptance

Each user stores the latest accepted version of:
- `terms_of_use`
- `privacy_policy`

Versions are compared to the current active version (from `apps.compliance`) to ensure validity. Enforcement logic is handled on protected endpoints.

---

## 🎛 Self-Registration Configuration

Self-registration is allowed **only if enabled in the related Application**.

### Application Requirement:
| Field                      | Type        | Description |
|----------------------------|-------------|-------------|
| `self_registration_enabled`| Boolean     | If false, `/auth/register/` is not available |

Validation must occur before processing registration requests.

---

## 🔗 API Endpoints

### 👤 User Profile and Identity Endpoints

| Method | URL                                      | Description                                      |
|--------|------------------------------------------|--------------------------------------------------|
| GET    | `/api/users/me/`                        | Retrieve authenticated user profile              |
| PATCH  | `/api/users/me/`                        | Update profile fields                            |
| POST   | `/api/users/validate-email/`            | Send confirmation code to user's email           |
| POST   | `/api/users/confirm-email/`             | Confirm email with a code                        |
| POST   | `/api/users/validate-phone/`            | Send confirmation code to user's phone           |
| POST   | `/api/users/confirm-phone/`             | Confirm phone number with a code                 |
| POST   | `/api/users/setup-totp/`                | Generate TOTP secret for user                    |
| POST   | `/api/users/confirm-totp/`              | Validate TOTP token                              |
| GET    | `/api/users/providers/`                 | List linked authentication providers             |

### 🔐 Self-Registration Endpoints

| Method | URL                                      | Description                                      |
|--------|------------------------------------------|--------------------------------------------------|
| POST   | `/api/users/register/`                  | Register a new user (if enabled for the app)     |

---

## 📣 Webhook Events

The following events may be emitted by this app:

| Event Name                 | Description                                |
|----------------------------|--------------------------------------------|
| `user.created`            | New user was registered                    |
| `user.updated`            | User profile was updated                   |
| `user.deleted`            | User was deleted (soft or hard)            |
| `user.email_verified`     | User confirmed their email address         |
| `user.phone_verified`     | User confirmed their phone number          |
| `user.totp_enabled`       | TOTP setup was successfully completed      |
| `user.provider.linked`    | A provider was linked to an existing user  |

---

## 📤 User Data Export

To support GDPR and LGPD compliance, this app includes functionality for users to export their personal data.

### Included Data

- Profile information (`apps.users`)
- Linked providers
- Roles and associated applications (`apps.permissions`)
- Active sessions (`apps.auth`)
- Activity log entries (if `apps.audit` is installed)

### Endpoint

| Method | URL                    | Description                         |
|--------|------------------------|-------------------------------------|
| GET    | `/api/users/me/export/`| Export user data as a JSON payload  |

### Format

- Returns a JSON document with structured fields (e.g., `profile`, `roles`, `sessions`, `logs`)
- If `apps.audit` is present, includes recent entries scoped to the user

### Security Considerations

- Must be authenticated
- Export includes only the data belonging to the requesting user
- Optionally rate-limited via `django_hsb_ratelimit`

---

## ✅ TDD Strategy

### Unit Tests
- User creation and validation flags
- Role assignment behavior and integrity
- Policy version tracking

### Integration Tests
- Self-registration flow respecting app settings
- Provider matching enforcement
- Terms acceptance and profile access

---

## 🤖 LLM Implementation Guidelines

- Always enforce realm context on user queries and mutations
- Prevent registration when `self_registration_enabled=False`
- Do not assign roles directly in the model — use validated flows from `apps.permissions`
- Avatar priority: `avatar_url` > `gravatar` (if `use_gravatar=True`) > default
- Verify provider access by checking against application's allowed providers

---
