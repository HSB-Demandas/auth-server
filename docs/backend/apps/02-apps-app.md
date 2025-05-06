# 🧩 Django App: `apps.application`

This app manages external applications ("apps") that authenticate against the platform using API Keys and JWT. It enables realm-scoped registration and configuration of apps that consume services from the platform. Each app will have access credentials, visual settings, and public keys for token validation.

---

## 🎯 Purpose

- Allow clients (applications) to register and configure their integration
- Generate and expose public keys for JWT validation
- Manage app-level access policies, expiration, secrets, and API keys
- Support realm isolation — each app belongs to a single realm
- Expose app metadata and configuration for client introspection

---

## 📁 App Structure

```
apps/
└── application/
    ├── __init__.py
    ├── apps.py
    ├── models.py             # App definition, API keys, public keys
    ├── views.py              # API views for introspection or registration
    ├── urls.py               # API routes (e.g., /apps/public-key/)
    ├── serializers.py        # DRF serializers
    ├── services.py           # Key generation, API key handling
    ├── admin.py              # Admin UI
    ├── crypto/               # Utilities to manage RSA keys
    ├── migrations/
    └── tests/
        ├── unit/
        └── integration/
```

---

## 🧱 Models

### `Application`

| Field             | Type           | Description                                 |
|------------------|----------------|---------------------------------------------|
| `id`             | UUID           | Primary key                                 |
| `realm`          | FK to Realm    | Application is scoped to one realm          |
| `name`           | CharField      | Display name                                |
| `slug`           | SlugField      | Unique identifier within realm              |
| `description`    | TextField      | Optional long text                          |
| `logo_url`       | URLField       | Used for branding in frontend integrations  |
| `api_key`        | CharField      | Secure random key (hashed in DB)            |
| `public_key`     | TextField      | Public part of key pair (PEM format)        |
| `private_key`    | EncryptedField | Private key for JWT signing (not exposed)   |
| `enabled`        | BooleanField   | Whether app is active                       |
| `providers`      | JSONField      | Optional list of provider identifiers       |
| `created_at`     | DateTimeField  | Timestamp                                   |
| `updated_at`     | DateTimeField  | Timestamp                                   |

---

## 🔐 Key Management

- A key pair (RSA 2048+) is generated for each app upon registration
- Public key is retrievable at `/api/apps/<slug>/jwks/` for JWT verification
- Private key is stored securely and never exposed

---

## 🌐 API Endpoints (Optional)

| Path                             | Method | Purpose                                    |
|----------------------------------|--------|--------------------------------------------|
| `/api/apps/<slug>/jwks/`        | GET    | Returns JWKS (public keys for JWT)         |
| `/api/apps/<slug>/metadata/`    | GET    | Returns app metadata (e.g. logo, name)     |
| `/api/apps/register/`           | POST   | Creates app (admin/internal only)          |
| `/api/apps/<slug>/rotate-keys/` | POST   | Rotates the key pair for the application   |

---

## 🎛 Admin UI Features

- Register apps with branding
- Regenerate API Key or JWT key pair
- Disable or enable app access
- Filter by realm and status

---

## ⚙️ Provider Configuration

- Applications can have one or more **providers** assigned (e.g., `google`, `saml`, `azure_ad`)
- These are stored as a list of strings in the `providers` JSON field
- The list of supported providers is controlled via environment-level configuration and must be validated on app registration
- Providers influence which authentication or integration mechanisms are enabled for a given application

---

## ✅ TDD Strategy

### Unit Tests

- Key generation and validation
- API key validation and hashing
- JWT signing and verification with app keys

### Integration Tests

- Full app registration → token issuance → public key verification
- Key rotation scenarios
- Admin actions and scoping

---

## 🤖 LLM Implementation Guidelines

- Each application must be created within a realm
- Applications must never expose private keys
- Public key should follow JWKS format for compatibility
- Use `libs.jwt` or platform signing service to issue and validate tokens
- Respect app `enabled` flag before processing any auth/issue requests

---
