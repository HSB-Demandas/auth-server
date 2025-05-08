# 🛡️ Auth Server Platform - Backend Architecture

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture Overview](#architecture-overview)
- [Core Applications](#core-applications)
  - [Realms](#realms)
  - [Applications](#applications)
  - [Users](#users)
  - [Authentication](#authentication)
  - [Permissions](#permissions)
  - [Compliance](#compliance)
  - [Notifications](#notifications)
  - [Webhooks](#webhooks)
  - [Audit](#audit)
  - [Security Events](#security-events)
  - [Metrics](#metrics)
  - [Passkeys](#passkeys)
- [Supporting Libraries](#supporting-libraries)
- [Architecture Layers](#architecture-layers)
- [LLM Integration Guidelines](#llm-integration-guidelines)
- [Documentation](#documentation)
- [Status](#status)

## 🧭 Project Overview

The Auth Server is a multi-tenant Identity and Access Management (IAM) platform built with Django, designed to provide enterprise-grade authentication, authorization, and user management capabilities. The system is inspired by best practices from providers like Auth0 and AWS IAM while maintaining full extensibility and customization.

### Key Principles

1. **Modularity**: Each feature is encapsulated in a standalone Django app
2. **Reusability**: Core functionality is abstracted into reusable libraries
3. **Security First**: OWASP-compliant architecture with built-in compliance features
4. **Scalability**: Designed for multi-tenant operation with proper isolation
5. **Extensibility**: Easy to add new authentication methods, providers, and integrations

## 🏗 Architecture Overview

The backend is organized into two main categories:

1. **Core Applications**: Django apps that implement specific business domains
2. **Supporting Libraries**: Reusable components that provide common functionality

### Core Applications vs Supporting Libraries

- **Core Applications** (`apps.*`): Implement business logic and domain rules

  - Have their own models, views, serializers, and permissions
  - Contain business-specific logic and workflows
  - Are tightly coupled to the IAM domain
- **Supporting Libraries** (`libs.*`): Provide reusable technical components

  - Are decoupled from business logic
  - Can be used in other projects
  - Focus on technical implementation details

## 🧩 Core Applications

### 1. `apps.realms`

**Purpose**: Tenant isolation and scoping

- **Key Features**:
  - Realm-based isolation for multi-tenant operation
  - Configuration management per realm
  - Resource scoping and isolation
  - Custom branding and settings per realm

### 2. `apps.applications`

**Purpose**: Client application management and registration

- **Key Features**:
  - OAuth2 client registration
  - API key management
  - JWT configuration and public key management
  - Provider configuration
  - MFA policy management
  - Terms and conditions versioning

### 3. `apps.users`

**Purpose**: User management and profile handling

- **Key Features**:
  - User registration and profile management
  - Provider linking (password, social, passkeys)
  - Email/phone verification
  - TOTP device management
  - Consent tracking
  - Data export compliance

### 4. `apps.auth`

**Purpose**: Authentication workflow and session management

- **Key Features**:
  - Multi-factor authentication workflow
  - JWT token issuance and validation
  - Session management
  - Passkey authentication
  - Rate limiting
  - Login flow orchestration

### 5. `apps.permissions`

**Purpose**: Role-based access control and authorization

- **Key Features**:
  - Role definition and management
  - Permission assignment
  - Role validation rules
  - Policy enforcement
  - Access control lists

### 6. `apps.compliance`

**Purpose**: Legal and regulatory compliance

- **Key Features**:
  - Terms and conditions management
  - Privacy policy versioning
  - User consent tracking
  - Data export endpoints
  - Compliance reporting

### 7. `apps.notifications`

**Purpose**: User communication and alerts

- **Key Features**:
  - In-app notification delivery
  - Actionable notifications
  - Notification preferences
  - Event-driven notifications
  - Delivery tracking

### 8. `apps.webhooks`

**Purpose**: Event-driven integration

- **Key Features**:
  - Webhook registration and management
  - Event delivery with retry logic
  - HMAC signature validation
  - Delivery status tracking
  - Rate limiting

### 9. `apps.audit`

**Purpose**: System observability and compliance

- **Key Features**:
  - Immutable audit logging
  - Action tracking per realm
  - User activity monitoring
  - Compliance reporting
  - Event correlation

### 10. `apps.security_events`

**Purpose**: Security monitoring and alerting

- **Key Features**:
  - Device tracking and trust
  - Suspicious activity detection
  - Login attempt monitoring
  - Security event correlation
  - User notification

### 11. `apps.metrics`

**Purpose**: System monitoring and observability

- **Key Features**:
  - Prometheus-style metrics
  - Login success/failure tracking
  - Role usage metrics
  - Webhook delivery statistics
  - System health monitoring

### 12. `apps.passkeys`

**Purpose**: WebAuthn/FIDO2 credential management

- **Key Features**:
  - Passkey registration
  - Credential management
  - Passkey verification
  - Integration with authentication flow
  - Security policy enforcement

## 📦 Supporting Libraries

### 1. `libs.totp`

**Purpose**: Time-based One-Time Password implementation

- **Features**:
  - RFC 6238 compliant TOTP generation
  - QR code generation for app setup
  - Code verification
  - Recovery code management

### 2. `libs.twilio`

**Purpose**: SMS integration and verification

- **Features**:
  - SMS message sending
  - Code verification
  - Message templating
  - Rate limiting
  - Error handling

### 3. `libs.mailer`

**Purpose**: Email notification system

- **Features**:
  - Multi-provider email sending
  - HTML template rendering
  - Event tracking
  - Bounce handling
  - Unsubscribe management

### 4. `libs.aws`

**Purpose**: AWS service integration

- **Features**:
  - SNS + SQS integration
  - Async message processing
  - Payload validation
  - Error handling
  - Retry logic

### 5. `django_hsb_ratelimit`

**Purpose**: Rate limiting and throttling

- **Features**:
  - Redis-based rate limiting
  - DRF-compatible throttling
  - Multiple scope support
  - Custom rate limit definitions
  - Real-time monitoring

### 6. `libs.passkeys`

**Purpose**: WebAuthn protocol implementation

- **Features**:
  - FIDO2 protocol support
  - Challenge generation
  - Credential verification
  - Security policy enforcement
  - Error handling

## 🏗 Architecture Layers

The system is organized into distinct architectural layers:

1. **Communication Layer**

   - REST API endpoints
   - GraphQL API (planned)
   - WebSocket connections
   - Protocol handling
2. **Application Layer**

   - Business logic orchestration
   - Workflow management
   - Cross-app coordination
   - Event handling
3. **Domain Layer**

   - Business entities
   - Domain rules
   - Value objects
   - Domain events
4. **Infrastructure Layer**

   - Database access
   - External service integration
   - Message queue handling
   - Caching
   - Storage
5. **Notification Layer**

   - Event-driven notifications
   - Delivery channels
   - Retry mechanisms
   - Status tracking

## 🧠 LLM Integration Guidelines

### App Structure

Each app follows a consistent structure:

```
apps/<app_name>/
├── models/          # Domain models
├── services/        # Business logic
├── tasks/          # Async tasks
├── serializers/     # Data serialization
├── views/          # API endpoints
├── permissions/    # Access control
├── events/         # Event handling
├── docs/           # Documentation
└── tests/          # Test suite
```

### Integration Points

1. **Data Flow**

   - Clear input/output specifications
   - Well-defined data models
   - Standardized error handling
2. **Authentication Flow**

   - Step-by-step process documentation
   - Required permissions
   - Error scenarios
   - Success criteria
3. **Event System**

   - Available events
   - Event payloads
   - Event triggers
   - Event consumers

### Best Practices

1. **Documentation**

   - Maintain API documentation
   - Keep examples up-to-date
   - Document integration points
   - Update error codes
2. **Testing**

   - Unit tests for core functionality
   - Integration tests for workflows
   - Performance benchmarks
   - Security testing
3. **Security**

   - Input validation
   - Rate limiting
   - Error masking
   - Audit logging
   - Compliance checks

## 📚 Documentation

Each component is documented in its own file:

- Core Applications:

  - [01-realms-app.md](01-realms-app.md)
  - [02-applications-app.md](02-applications-app.md)
  - [03-permissions-app.md](03-permissions-app.md)
  - [04-users-app.md](04-users-app.md)
  - [05-auth-app.md](05-auth-app.md)
  - [06-webhooks-app.md](06-webhooks-app.md)
  - [07-security-app.md](07-security-app.md)
  - [08-metrics-app.md](08-metrics-app.md)
- Supporting Libraries:

  - [django_hsb_ratelimit.md](django_hsb_ratelimit.md)
  - [django_hsb_mailer.md](django_hsb_mailer.md)
  - [django_hsb_twilio.md](django_hsb_twilio.md)
  - [django_hsb_totp.md](django_hsb_totp.md)
  - [django_hsb_notifications.md](django_hsb_notifications.md)

## ✅ Status

The backend architecture is fully planned and ready for implementation. Each component includes:

- Complete data models
- Defined API endpoints
- Permission structures
- Event definitions
- Test plans
- Integration guidelines
- Security considerations
- Performance requirements

The system is designed to be extensible, allowing for:

- New authentication methods
- Additional compliance features
- Custom notification channels
- Extended audit capabilities
- New security controls
- Additional monitoring metrics

---

> **Note**: This README serves as the main entry point for understanding the backend architecture. Each component has its own detailed documentation that should be consulted for implementation details.
