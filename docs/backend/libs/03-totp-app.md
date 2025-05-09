# 🔐 MFA Authenticator App — `libs.mfa_authenticator`

A comprehensive TOTP (Time-based One-Time Password) implementation compatible with common MFA applications like Google Authenticator and Authy. Provides secure token generation, verification, and QR code generation for app pairing.

---

## 📋 Table of Contents

- [Architecture](#architecture)
- [Module Structure](#module-structure)
- [Components](#components)
- [Testing Strategy](#testing-strategy)
- [Environment Variables](#environment-variables)
- [Usage Examples](#usage-examples)
- [Security Considerations](#security-considerations)
- [Performance Considerations](#performance-considerations)

## 🏗 Architecture

### Core Principles

1. **Security First**: RFC 6238 compliant implementation
2. **Extensibility**: Flexible configuration options
3. **User Experience**: QR code generation and validation
4. **Error Handling**: Robust error management
5. **Testability**: Mockable interfaces

## 📁 Module Structure

```
libs/
└── totp/
    ├── __init__.py
    ├── config.py            # Configuration and settings
    ├── generator.py         # Token generation
    ├── validator.py         # Token validation
    ├── exceptions.py        # Error handling
    ├── types.py             # Result types and enums
    └── tests/
        ├── unit/
        │   ├── test_generator.py
        │   ├── test_validator.py
        │   └── test_exceptions.py
        └── integration/
            ├── test_user_flow_real.py
```

## ⚙️ Components

### 1. Configuration (`config.py`)

- **Purpose**: MFA settings management
- **Key Components**:
  - `MFAConfig` pydantic model
  - Configuration validation
  - Environment variable mapping

### 2. Generator (`generator.py`)

- **Purpose**: TOTP token generation
- **API**:
  ```python
  def generate_secret(
      length: int = 32,
      chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
  ) -> str
  ```
- **Features**:
  - RFC 6238 compliant secret generation
  - Customizable secret length
  - Base32 encoding
  - QR code generation

### 3. Validator (`validator.py`)

- **Purpose**: Token verification
- **API**:
  ```python
  def verify_token(
      secret: str,
      token: str,
      window: int = 1
  ) -> bool
  ```
- **Features**:
  - Token validation
  - Time drift tolerance
  - Error handling

### 4. Error Handling (`exceptions.py`)

- **Purpose**: Domain-specific error abstraction
- **Exceptions**:
  - `InvalidTokenError`
  - `TokenExpiredError`
  - `InvalidSecretError`
  - `VerificationError`

## ✅ Testing Strategy

### Unit Tests

- **Core Logic**:
  - Token generation
  - Token validation
  - Time drift handling
  - Error scenarios
- **Test Coverage**:
  - 100% statement coverage
  - Edge case handling
  - Error scenarios
  - Time drift testing

### Integration Tests

- **Real Integration**:
  - Full user flow
  - Token validation
  - Error handling
- **Requirements**:
  - Test secrets
  - Mock time sources
  - Test tokens
  - Error scenarios

## 🔐 Environment Variables

No direct environment variable access inside the library. Configuration must be passed through `MFAConfig`.

If required by the consuming app, recommended environment variables:

| Variable Name     | Purpose                      | Required | Default |
|-------------------|------------------------------|----------|---------|
| `MFA_ISSUER`      | App name shown to user       | ✅       | —       |
| `MFA_DRIFT_WINDOW`| Token tolerance window        | ❌       | 1       |
| `MFA_SECRET_LENGTH`| Generated secret length     | ❌       | 32      |
| `MFA_QR_CODE_FORMAT`| QR code format (PNG/SVG)   | ❌       | PNG     |

## 🔄 Usage Examples

### Basic Token Generation

```python
from libs.totp.config import MFAConfig
from libs.totp.generator import generate_secret, generate_provisioning_uri
from libs.totp.validator import verify_token

config = MFAConfig(
    issuer="My App",
    drift_window=1
)

# Generate secret
secret = generate_secret()

# Generate provisioning URI
uri = generate_provisioning_uri(
    secret=secret,
    username="user@example.com"
)

# Verify token
is_valid = verify_token(
    secret=secret,
    token="123456"
)
```

### Advanced Usage with QR Code

```python
from libs.totp.config import MFAConfig
from libs.totp.generator import generate_secret, generate_provisioning_uri, generate_qr_code
from libs.totp.validator import verify_token

config = MFAConfig(
    issuer="My App",
    drift_window=1
)

# Generate secret and QR code
secret = generate_secret()
uri = generate_provisioning_uri(
    secret=secret,
    username="user@example.com"
)
qr_code = generate_qr_code(uri)

# Verify token with time drift
is_valid = verify_token(
    secret=secret,
    token="123456",
    window=2
)
```

## 🛡 Security Considerations

- **Token Validation**: Strict token format validation
- **Time Drift**: Configurable tolerance window
- **Secret Generation**: Cryptographically secure random
- **QR Code**: Secure URI encoding
- **Error Handling**: No sensitive information in errors
- **Rate Limiting**: Built-in rate limiting

## 🚀 Performance Considerations

- **Token Generation**: Efficient secret generation
- **Token Validation**: Fast token verification
- **QR Code**: Optimized image generation
- **Error Handling**: Quick failure paths
- **Caching**: Optional caching strategies
- **Async Operations**: Non-blocking operations

---

> **Note**: This library is designed for production use with MFA applications. For development, use test secrets and mock time sources.

---

## 🤖 LLM Implementation Guidelines

- Use `pyotp` for TOTP generation and validation.
- Never call `os.environ` directly — all values must be injected via config.
- Expose clean façades like `generate_secret()`, `verify_token(...)`.
- Return typed domain exceptions rather than raw SDK errors.
- Integration test must simulate pairing with a real app and token entry.

---
