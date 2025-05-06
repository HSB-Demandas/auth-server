# 🛡️ Security Events App — `apps.security_events`

## 📌 Purpose

This app provides support for **device tracking** and **suspicious login detection**. It protects user accounts by identifying unknown login origins and alerting users when new or risky devices are used.

---

## 📐 Models

### `KnownDevice`

| Field             | Type             | Description                                 |
|------------------|------------------|---------------------------------------------|
| `id`             | UUIDField        | Primary key                                 |
| `user`           | FK to `User`     | Owner of the device                         |
| `realm`          | FK to `Realm`    | Realm scope of the login                    |
| `user_agent`     | CharField        | Parsed user-agent string                    |
| `ip_hash`        | CharField        | Hashed representation of IP or fingerprint  |
| `last_seen`      | DateTimeField    | Last time the device was used               |
| `confirmed`      | BooleanField     | True if the user has confirmed the device   |
| `created_at`     | DateTimeField    | First usage                                 |

---

## 🧠 Detection Strategy

- Every login event triggers device fingerprint evaluation.
- If the device is not recognized (user-agent + IP hash), a `KnownDevice` is created as unconfirmed.
- Unconfirmed devices trigger an alert (e.g. in-app or email).
- The user can confirm or delete devices from their account.
- Admins may audit or revoke devices from other users within the same realm.

---

## 🌐 API Endpoints

| Method | URL                                | Description                                     |
|--------|------------------------------------|-------------------------------------------------|
| GET    | `/api/security/devices/`           | List known devices for the current user         |
| POST   | `/api/security/devices/confirm/`   | Confirm a known device as trusted               |
| DELETE | `/api/security/devices/[uuid:id]/` | Revoke (delete) a known device                  |

---

## 🛡️ Security

- Only users can manage their own devices.
- Admins with proper permissions can manage devices across users in the same realm.
- Logs for all device-related events are stored in the `apps.audit` log system.

---

## 🔔 Integration Points

- Triggers `security.device.new` event on new device detection.
- Optionally notifies via `apps.notifications` or `libs.mailer`.
- Logs to `apps.audit` for compliance and monitoring.

---

## ✅ TDD Strategy

- Verify detection of new vs. known devices.
- Test IP/user-agent hashing logic.
- Test device confirmation flow.
- Ensure endpoint authorization rules are enforced.
- Validate integration with audit and notification systems.

---

## 🔧 Configuration via Settings

| Setting                            | Description                                                  |
|-----------------------------------|--------------------------------------------------------------|
| `DEVICE_HASH_SALT`                | Salt used to hash IP/fingerprint for privacy and uniqueness |
| `NOTIFY_ON_NEW_DEVICE`            | Enable/disable alerting when unknown device is detected      |
| `DEVICE_EXPIRATION_DAYS`          | Automatically remove stale devices after given days          |

---

## 🧭 Use Case Overview

This app integrates with the login process (via signal from `apps.auth`) to evaluate whether the current login originates from a previously known device. A known device is identified by its combination of user-agent string and a hashed IP or fingerprint.

### 🔄 Typical Flow:
1. User logs in through any supported method.
2. The login event triggers a signal.
3. `apps.security_events` checks whether the device is known.
4. If unknown:
    - A `KnownDevice` is registered.
    - The user is alerted (via email or in-app notification).
    - Optionally, a webhook or audit log entry is generated.
5. The user may confirm or revoke the device from their account.
6. Admins may list or revoke devices within their realm for audit and security purposes.

This enables early detection of suspicious activity and provides auditability and user control over active devices.
