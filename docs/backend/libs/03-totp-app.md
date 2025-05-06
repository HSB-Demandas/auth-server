# 🔐 MFA Authenticator App — `libs.mfa_authenticator`

This module provides a full TOTP (Time-based One-Time Password) integration compatible with common MFA applications such as Google Authenticator, Authy, and others. It allows the platform to generate shared secrets, encode them into QR codes for app pairing, and verify time-based tokens submitted by users.

---

## 📁 Module Structure

```
libs/
└── totp/
    ├── __init__.py
    ├── config.py            # MFA issuer and token window configuration
    ├── generator.py         # Generates TOTP secrets and provisioning URIs
    ├── validator.py         # Validates user-submitted TOTP tokens
    ├── exceptions.py        # Domain-level errors for invalid/expired tokens
    └── tests/
        ├── unit/
        │   ├── test_generator.py
        │   ├── test_validator.py
        │   └── test_exceptions.py
        └── integration/
            ├── test_user_flow_real.py
```

---

## ⚙️ Components Description

### `config.py`
- `MFAConfig` dataclass:
  - `issuer: str` — shown in the Authenticator app UI
  - `token_valid_window: int` — tolerance window for time drift (default: ±1 step)

### `generator.py`
- `generate_secret() -> str`  
  - Generates a new base32-encoded TOTP secret

- `generate_provisioning_uri(secret: str, username: str) -> str`  
  - Returns a URI that can be encoded into a QR code:
    ```
    otpauth://totp/{issuer}:{username}?secret={secret}&issuer={issuer}
    ```

- `generate_qr_code(uri: str) -> bytes`  
  - Returns a QR code image (PNG or SVG format)

### `validator.py`
- `verify_token(secret: str, token: str) -> bool`  
  - Validates a TOTP token using `pyotp`

- Accepts optional window/tolerance

### `exceptions.py`
- `InvalidTokenError`
- `TokenExpiredError`

---

## ✅ Testing Strategy (TDD)

### 🔹 Unit Tests

#### `test_generator.py`
- Generates valid base32 secrets
- Produces well-formed URIs
- Successfully generates QR code image bytes

#### `test_validator.py`
- Validates correct token
- Rejects expired/invalid tokens
- Handles optional window configuration

#### `test_exceptions.py`
- Raises and identifies expected exception types

---

### 🔸 Integration Tests (disabled by default)

#### `test_user_flow_real.py`
- Simulates end-to-end flow:
  - Generate secret
  - Scan in Google Authenticator
  - Input token and validate
- Used for manual pairing confirmation

---

## 🔐 Environment Variables

No direct access to environment variables inside the library.

All configuration (like issuer name or drift window) must be injected through `MFAConfig`.

If required by the consuming app, recommended environment variable names:

| Variable Name     | Purpose                      | Required | Default |
|-------------------|------------------------------|----------|---------|
| `MFA_ISSUER`      | App name shown to user       | ✅       | —       |
| `MFA_DRIFT_WINDOW`| Token tolerance window        | ❌       | 1       |

---

## 🤖 LLM Implementation Guidelines

- Use `pyotp` for TOTP generation and validation.
- Never call `os.environ` directly — all values must be injected via config.
- Expose clean façades like `generate_secret()`, `verify_token(...)`.
- Return typed domain exceptions rather than raw SDK errors.
- Integration test must simulate pairing with a real app and token entry.

---
