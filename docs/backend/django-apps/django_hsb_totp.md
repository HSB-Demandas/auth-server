

# 🔐 Django App: `apps.django_hsb_totp`

A reusable Django app for TOTP-based MFA integration, providing secure token generation, validation, and QR code generation for app pairing.

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
2. **Extensible**: Flexible configuration options
3. **User Experience**: QR code generation and validation
4. **Error Handling**: Robust error management
5. **Testable**: Mockable interfaces

## 📁 Module Structure

```
apps/
└── mfa/
    ├── __init__.py
    ├── apps.py
    ├── models.py            # Stores TOTP secrets per user
    ├── views.py             # API: enable MFA, verify token
    ├── urls.py              # Route: /mfa/setup/, /mfa/verify/
    ├── serializers.py       # DRF serializers for validation
    ├── services.py          # Pairing + validation logic
    ├── integrations/        # Calls into libs.mfa_authenticator
    ├── admin.py             # Optional management of MFA
    ├── migrations/
    └── tests/
        ├── unit/
        │   ├── test_models.py
        │   ├── test_services.py
        │   └── test_views.py
        └── integration/
            ├── test_token.py
            └── test_pairing.py
```

## ⚙️ Components

### 1. Models (`models.py`)

- **Purpose**: Secure storage of TOTP secrets
- **Key Models**:
  - `MFASecret`: Encrypted TOTP secrets per user
  - `MFAToken`: Optional token tracking
  - `MFASession`: Optional session tracking

### 2. Services (`services.py`)

- **Purpose**: Core MFA logic
- **Features**:
  - Token generation
  - Token validation
  - QR code generation
  - Session management
  - Error handling

### 3. API (`views.py` + `serializers.py`)

- **Purpose**: REST API endpoints
- **Endpoints**:
  - `/api/mfa/setup/` - Generate QR code
  - `/api/mfa/verify/` - Validate token
  - `/api/mfa/disable/` - Disable MFA

### 4. Integration (`integrations/`)

- **Purpose**: Library integration
- **Features**:
  - TOTP generation
  - Token validation
  - QR code generation
  - Error handling

### 5. Error Handling (`exceptions.py`)

- **Purpose**: Domain-specific error abstraction
- **Exceptions**:
  - `MFATokenError`
  - `MFASecretError`
  - `MFASessionError`
  - `MFAPairingError`

## ✅ Testing Strategy

### Unit Tests

- **Core Logic**:
  - Secret generation
  - Token validation
  - QR code generation
  - Session management
- **Test Coverage**:
  - 100% statement coverage
  - Edge case handling
  - Error scenarios
  - Token drift testing

### Integration Tests

- **Internal Integration**:
  - Database operations
  - API endpoints
  - Session management
  - Error handling
- **External Integration**:
  - TOTP generation
  - Token validation
  - QR code generation
  - Session tracking

## 🔐 Environment Variables

No direct environment variable access inside the app. All configuration must be passed through Django settings.

If required by the consuming app, recommended settings:

| Setting Name               | Purpose                      | Required | Default |
|----------------------------|------------------------------|----------|---------|
| `MFA_SECRET_ENCRYPTION_KEY` | Encryption key for secrets   | ✅       | —       |
| `MFA_TOKEN_VALID_WINDOW`    | Token validation window      | ❌       | 30      |
| `MFA_QR_CODE_FORMAT`        | QR code format (PNG/SVG)    | ❌       | PNG     |
| `MFA_SESSION_TTL`           | Session TTL (seconds)       | ❌       | 3600    |

## 🔄 Usage Examples

### Basic MFA Setup

```python
from apps.mfa.services import setup_mfa

# Generate MFA secret and QR code
result = setup_mfa(user)

# Get QR code for app pairing
qr_code = result.qr_code
```

### Token Validation

```python
from apps.mfa.services import validate_mfa_token

# Validate user-submitted token
is_valid = validate_mfa_token(
    user=user,
    token="123456"
)
```

### Session Management

```python
from apps.mfa.services import create_mfa_session

# Create MFA session
session = create_mfa_session(user)

# Check session status
if session.is_valid:
    # Process valid session
    pass
```

## 🛡 Security Considerations

- **Secret Storage**: Always encrypted
- **Token Validation**: Secure implementation
- **QR Code**: Secure URI generation
- **Error Handling**: No sensitive information
- **Rate Limiting**: Token validation protection
- **Session Security**: Secure session management

## 🚀 Performance Considerations

- **Token Generation**: Efficient secret generation
- **Token Validation**: Fast token verification
- **QR Code**: Optimized image generation
- **Session Management**: Efficient session tracking
- **Error Handling**: Fast failure paths
