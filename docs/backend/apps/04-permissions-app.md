# 🛡 Django App: `apps.permissions`

This app defines and manages the role-based access control (RBAC) model for the platform. It scopes permissions by realm and application, enforcing fine-grained control over what users can do. Unlike traditional IAM systems, **users are never granted permissions directly** — instead, they are granted **roles**, and roles encapsulate one or more permissions.

---

## 🎯 Purpose

- Provide a matrix of roles and permissions per app and realm
- Assign users to roles within realms and applications
- Define and enforce advanced assignment conditions based on user validation (email, phone, TOTP)
- Prevent assignment or invalidation of roles when conditions are not met

---

## 📁 App Structure

```
apps/
└── permissions/
    ├── __init__.py
    ├── apps.py
    ├── models.py             # Role, Permission, RoleAssignment
    ├── views.py              # API views to list/query roles/assignments
    ├── urls.py               # REST API routes
    ├── serializers.py        # DRF serializers
    ├── filters.py            # Query filters by realm/app/user
    ├── services.py           # Assignment logic and validation
    ├── admin.py              # Manage roles and permissions
    ├── migrations/
    └── tests/
        ├── unit/
        └── integration/
```

---

## 🧱 Models

### `Permission`

| Field         | Type           | Description                               |
|---------------|----------------|-------------------------------------------|
| `id`          | UUID           | Primary key                               |
| `app`         | FK to Application | Scope permission to app                 |
| `code`        | CharField      | Unique identifier (e.g. `user.update`)    |
| `description` | TextField      | Optional display description              |
| `created_at`  | DateTimeField  |                                           |

### `Role`

| Field         | Type           | Description                               |
|---------------|----------------|-------------------------------------------|
| `id`          | UUID           | Primary key                               |
| `realm`       | FK to Realm    | Scoped to realm                           |
| `app`         | FK to Application |                                         |
| `name`        | CharField      | Display name                              |
| `slug`        | SlugField      | Unique identifier                         |
| `description` | TextField      | Optional description                      |
| `permissions` | M2M to Permission | Roles aggregate permissions             |
| `requires_email_validation` | Boolean | Only assign if user email is verified |
| `requires_phone_validation` | Boolean | Only assign if user phone is verified |
| `requires_totp`             | Boolean | Only assign if user has TOTP enabled   |
| `created_at`  | DateTimeField  |                                           |

### `RoleAssignment`

| Field         | Type           | Description                               |
|---------------|----------------|-------------------------------------------|
| `id`          | UUID           | Primary key                               |
| `user`        | FK to User     | Assigned user                             |
| `role`        | FK to Role     | Assigned role                             |
| `realm`       | FK to Realm    | Redundant for filtering                   |
| `app`         | FK to Application |                                         |
| `is_valid`    | Boolean        | Auto-maintained by signal based on checks |
| `created_at`  | DateTimeField  |                                           |

---

## ⚙️ Validation Logic

- Role assignments are **rejected** at creation if requirements are not met
- A background job or signal can **invalidate existing assignments** if:
  - Email or phone is changed and no longer validated
  - TOTP is removed

> `RoleAssignment.is_valid` flag reflects the current status

---

## 🔗 API Endpoints

### 🔍 Role and Permission Endpoints

| Method | URL                              | Description                                      |
|--------|----------------------------------|--------------------------------------------------|
| GET    | `/api/permissions/roles/`       | List roles for the current realm/app             |
| GET    | `/api/permissions/roles/{id}/`  | Retrieve role details                            |
| POST   | `/api/permissions/roles/`       | Create a new role                                |
| PATCH  | `/api/permissions/roles/{id}/`  | Update role metadata or validation requirements  |
| DELETE | `/api/permissions/roles/{id}/`  | Delete role                                      |

| Method | URL                                    | Description                                  |
|--------|----------------------------------------|----------------------------------------------|
| GET    | `/api/permissions/permissions/`       | List all available permissions               |
| GET    | `/api/permissions/permissions/{id}/`  | Retrieve permission details                  |
| POST   | `/api/permissions/permissions/`       | Create a new permission                      |
| PATCH  | `/api/permissions/permissions/{id}/`  | Update permission description                |
| DELETE | `/api/permissions/permissions/{id}/`  | Delete permission                            |

### 👥 Role Assignment Endpoints

| Method | URL                                           | Description                                |
|--------|-----------------------------------------------|--------------------------------------------|
| GET    | `/api/permissions/assignments/`              | List role assignments for current user     |
| POST   | `/api/permissions/assignments/`              | Assign a role to a user                    |
| DELETE | `/api/permissions/assignments/{id}/`         | Remove a user's role assignment            |

---

## 📣 Webhook Events

The following events may be emitted by this app:

| Event Name                      | Description                                                    |
|--------------------------------|----------------------------------------------------------------|
| `role.created`                 | A new role was created                                         |
| `role.updated`                 | A role was updated (metadata or permission set)               |
| `role.deleted`                 | A role was deleted                                             |
| `permission.created`          | A permission was created                                       |
| `permission.updated`          | A permission was updated                                       |
| `permission.deleted`          | A permission was deleted                                       |
| `role_assignment.created`     | A user was assigned to a role                                  |
| `role_assignment.deleted`     | A role was unassigned from a user                              |
| `role_assignment.invalidated` | An assignment was marked as invalid due to validation failure  |

---

## 🛠 Admin Panel

- Manage roles and permissions per realm/app
- Assign or unassign permissions to roles
- View all role assignments and their validation status

---

## ✅ TDD Strategy

### Unit Tests

- Assignment validation (email, phone, TOTP)
- Permissions aggregation and filtering
- Role lifecycle behavior

### Integration Tests

- Role assignment with validation context
- Role invalidation upon user field change

---

## 🤖 LLM Implementation Guidelines

- Never assign permissions directly to users
- All permission checks must resolve through assigned roles
- Every model must be scoped by `realm` and `app`
- RoleAssignment must validate user context on creation
- Mark assignments as invalid (but do not auto-delete) when requirements fail

---
