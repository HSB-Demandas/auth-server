# 🧾 Audit App — `apps.audit`

## 📌 Purpose

This app provides a centralized audit logging system to track administrative and user-related actions across all realms and applications.

It supports traceability and accountability for operations such as user management, permission updates, role assignments, app configurations, and other sensitive actions.

---

## 📐 Models

### `AuditLogEntry`

| Field              | Type              | Description                                      |
|-------------------|-------------------|--------------------------------------------------|
| `id`              | UUIDField         | Primary key                                      |
| `actor_user`      | FK to `User`      | User who performed the action                    |
| `actor_app`       | FK to `Application` | App (if system initiated via API key)           |
| `realm`           | FK to `Realm`     | Realm context in which the action happened       |
| `action`          | CharField         | A codified string of the action performed        |
| `target_model`    | CharField         | The model class of the affected object           |
| `target_object_id`| CharField         | The object ID of the affected record             |
| `timestamp`       | DateTimeField     | When the action occurred                         |
| `metadata`        | JSONField         | Additional optional metadata (e.g., IP, diff)    |

---

## 🧠 Audit Strategy

- All logs must be immutable.
- Loggable actions include:
    - Creation, update, deletion of users, roles, apps, permissions
    - Security events such as MFA setup, provider linking
    - Admin API or dashboard operations
- Triggered via signals or explicit service layer calls
- Audit actions can be subscribed using a Pub/Sub signal-based system. Models or events can register themselves via decorators or a registry to automatically emit logs when watched fields change.

---

## 🌐 API Endpoints

| Method | URL                             | Description                          |
|--------|----------------------------------|--------------------------------------|
| GET    | `/api/audit/`                  | List entries (admin scoped per realm) |
| GET    | `/api/audit/<uuid:id>/`        | View specific audit entry             |

*Filtering by `actor`, `target_model`, `action`, and `date` is supported.*

---

## 🛡️ Security

- Only realm admins or auditors can view logs for their realm.
- All access is read-only via API.
- Endpoint is paginated and filterable, never editable.

---

## 💾 Persistence & Retention

- Retention policy configurable via settings.
- Archival can be optionally supported via async job or cron.

---

## ✅ TDD Strategy

- Log creation is triggered from representative backend operations.
- Validate immutability of logs.
- Validate filtering and pagination API responses.
- Validate access restrictions per realm.

---

## 🔧 Configuration via Settings

| Setting                         | Description                                     |
|----------------------------------|-------------------------------------------------|
| `AUDIT_LOG_RETENTION_DAYS`      | How long logs are stored before optional purge |
