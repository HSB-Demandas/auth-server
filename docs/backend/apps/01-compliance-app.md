# 📄 Django App: `apps.compliance`

This app manages versioned policy documents and terms of service agreements for end users. Each document (e.g., Privacy Policy, Terms of Use) is stored in a versioned format and associated with a realm. It exposes public API endpoints for users to retrieve the current policy content.

---

## 🎯 Purpose

- Store and version legal policy documents (e.g., terms and privacy)
- Support per-realm policies (optional)
- Expose publicly accessible, cached endpoints to retrieve current versions
- Support granular user consents beyond general terms (e.g., marketing, analytics)

---

## 📁 App Structure

```
apps/
└── compliance/
    ├── __init__.py
    ├── apps.py
    ├── models.py             # Policy, Acceptance
    ├── views.py              # Public views to serve content
    ├── urls.py               # Exposed API routes
    ├── serializers.py        # DRF serializers
    ├── cache.py              # Caching layer for content responses
    ├── admin.py              # Manage versioned documents
    ├── migrations/
    └── tests/
        ├── unit/
        └── integration/
```

---

## 🧱 Models

### `PolicyDocument`

| Field         | Type           | Description                                |
|---------------|----------------|--------------------------------------------|
| `id`          | UUID           | Primary key                                |
| `realm`       | FK to Realm    | Optional — can be global or per realm      |
| `type`        | CharField      | `terms_of_use`, `privacy_policy`, etc.     |
| `version`     | CharField      | Semantic version or timestamped            |
| `content`     | TextField      | Markdown or rich-text version of the policy|
| `is_active`   | Boolean        | Marks the current version                  |
| `created_at`  | DateTimeField  |                                            |

### `UserConsent`

| Field         | Type             | Description                                                      |
|---------------|------------------|------------------------------------------------------------------|
| `id`          | UUID             | Primary key                                                      |
| `user`        | FK to User       | The user granting or revoking consent                            |
| `realm`       | FK to Realm      | Realm scope of the consent                                       |
| `consent_type`| CharField        | The type of consent (e.g. `marketing_emails`, `data_sharing`)    |
| `granted`     | BooleanField     | Whether the user has granted or revoked this consent             |
| `granted_at`  | DateTimeField    | Timestamp of the most recent change to this consent              |

---

## 🌐 API Endpoints

| Path                                  | Method | Purpose                                       |
|---------------------------------------|--------|-----------------------------------------------|
| `/api/policy/<type>/`                | GET    | Return the current active document (cached)   |
| `/api/consent/<type>/`                | GET    | Return current consent status for the user            |
| `/api/consent/<type>/`                | POST   | Update consent status for the user                    |

> Supported `<type>`: `terms_of_use`, `privacy_policy`, etc.

---

## 🧠 Caching Strategy

- Use `cache.get_or_set(...)` to cache policy responses by:
  - `type`
  - `realm` (if scoped)
- Cache invalidates when a new version is marked active
- TTL can be configured via settings

---

## ✅ TDD Strategy

### Unit Tests

- Document creation/versioning
- Caching behavior validation

### Integration Tests

- Public access to current policy

---

## 🤖 LLM Implementation Guidelines

- Only one `is_active=True` version per realm/type at a time
- Automatically deactivate older versions on new activation
- Cache must respect realm scoping if applicable
- `UserConsent` entries should be updated via explicit user action.
- Consent types must be predefined or registered in code/config (not arbitrary).
