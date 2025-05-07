


# 🧩 Django App: apps.passkeys

## 📌 Purpose

The `apps.passkeys` application is responsible for managing user WebAuthn passkeys used for passwordless authentication. It allows users to register, view, label, and revoke their own passkeys and stores public key credentials securely.

This app does not perform authentication itself — authentication using passkeys is handled by `apps.auth`.

---

## 🧩 Features

- Passkey (FIDO2/WebAuthn) registration flow
- List and revoke passkeys
- Support for labeling user devices
- Audit logging on credential changes
- Admin support via Django Admin

---

## 🧱 Models

### `PasskeyCredential`

| Field             | Type                  | Description |
|------------------|-----------------------|-------------|
| `user`           | FK to user            | Owner of the passkey |
| `credential_id`  | CharField (unique)    | Credential ID (base64-encoded) |
| `public_key`     | TextField             | Public key used to verify assertions |
| `sign_count`     | BigIntegerField       | Replay protection counter |
| `transports`     | ArrayField            | Supported transports (e.g., `usb`, `ble`, `internal`) |
| `label`          | CharField             | Optional user-provided label for the passkey |
| `last_used_at`   | DateTimeField         | Timestamp of last usage |
| `created_at`     | DateTimeField         | Timestamp of registration |

---

## 🌐 API Endpoints

| Method | Endpoint                             | Description |
|--------|--------------------------------------|-------------|
| GET    | `/api/passkeys/`                     | List all registered passkeys for the logged-in user |
| POST   | `/api/passkeys/register/begin/`      | Start WebAuthn registration process, returns challenge |
| POST   | `/api/passkeys/register/complete/`   | Complete registration with browser-signed data |
| DELETE | `/api/passkeys/<id>/`                | Revoke a specific passkey credential |

---

## 🛡 Security Considerations

- All operations are scoped to the authenticated user.
- Credential registration must validate challenges using the FIDO2/WebAuthn protocol.
- Credential revocation must log the action and require CSRF protection.

---

## 🧪 Testing Strategy

- Unit tests for all endpoints and model logic
- Integration tests simulating registration and revocation using a mocked WebAuthn client
- Optional: browser-based E2E tests to simulate QR code and device setup

---

## 🧩 Admin

- Admin support to view all passkeys in the system
- Optional filtering by user or device label

---

## 🧩 Integration with Other Apps

- `apps.auth`: handles passkey login (challenge + verify)
- `apps.audit`: records creation, usage, and revocation of passkeys
