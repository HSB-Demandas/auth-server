

# 📝 Journey: Login with Email and Password

## 📌 Description

This journey allows a registered user to log in using their email and password credentials. It does not include multi-factor authentication (MFA), which is documented in a separate journey. Upon successful authentication, the system may trigger additional checks such as terms acceptance or device validation, based on app configuration.

---

## 👥 Personas

- Registered User

---

## 🧩 Involved Apps

- `apps.auth`
- `apps.security_events`
- `apps.compliance`
- `django_hsb_ratelimit`

---

## 🧭 UX Flow

### 📺 Screen: Login Form

- **Route**: `/login`
- **Purpose**: Allow user to authenticate using email and password
- **Inputs**:
  - Email
  - Password
- **Expected Behavior**:
  - Validate credentials against backend
  - On success, issue session or token
  - On failure, show error message
- **Backend Endpoints**:
  - `POST /api/auth/login/`

---

### 📺 Screen: Device Confirmation (if applicable)

- **Route**: `/device/confirm`
- **Purpose**: Confirm login from new or unrecognized device
- **Inputs**: None (or confirm button)
- **Expected Behavior**:
  - Show device info (browser, IP hash)
  - Confirm or mark as suspicious
- **Backend Endpoints**:
  - `POST /api/security/devices/confirm/`

---

### 📺 Screen: Accept Terms (if not accepted yet)

- **Route**: `/terms`
- **Purpose**: Present current terms and privacy policy
- **Inputs**: Accept checkbox
- **Expected Behavior**:
  - Block access until terms are accepted
  - Store acceptance for user profile
- **Backend Endpoints**:
  - `GET /api/terms/`
  - `POST /api/terms/accept/`

---

### 📺 Screen: Dashboard (Post-Login)

- **Route**: `/dashboard`
- **Purpose**: Landing screen after successful login and validation
- **Inputs**: None
- **Expected Behavior**:
  - Display welcome or account overview
