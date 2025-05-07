

# 📝 Journey: User Registration with Social Login

## 📌 Description

This journey allows a user to register by signing in with an external social provider (e.g. Google). Upon first login, the system may create the user automatically and collect additional information if required by the application configuration (e.g., phone number, MFA setup, or terms acceptance).

---

## 👥 Personas

- Anonymous User

---

## 🧩 Involved Apps

- `apps.auth`
- `apps.users`
- `apps.applications`
- `apps.compliance`
- `apps.permissions`

---

## 🧭 UX Flow

### 📺 Screen: Choose Social Provider

- **Route**: `/login`
- **Purpose**: Allow user to initiate login using an external provider
- **Inputs**: Social login button(s)
- **Expected Behavior**:
  - Redirect to provider’s OAuth2 login
  - On return, process authentication token
  - Backend creates or finds user and issues session/token
- **Backend Endpoints**:
  - `POST /api/auth/social-login/`
  - `GET /api/applications/<id>/providers/`

---

### 📺 Screen: Additional Info Required (Post-login)

- **Route**: `/complete-profile`
- **Purpose**: Collect additional user information required by app
- **Inputs**:
  - Phone number (if not provided by provider)
  - Name (if missing)
  - Accept Terms (if not accepted)
- **Expected Behavior**:
  - Validate form inputs
  - Store user info via PATCH
  - Check if profile is complete per app config
- **Backend Endpoints**:
  - `PATCH /api/users/me/`
  - `GET /api/applications/<id>/required_fields/`

---

### 📺 Screen: Accept Terms (if required)

- **Route**: `/terms`
- **Purpose**: Enforce terms and privacy acceptance for app
- **Inputs**: Accept checkbox
- **Expected Behavior**:
  - Block further use until accepted
  - Store acceptance with timestamp
- **Backend Endpoints**:
  - `GET /api/terms/`
  - `POST /api/terms/accept/`

---

### 📺 Screen: Registration Complete

- **Route**: `/welcome`
- **Purpose**: Show confirmation that the user is registered and ready
- **Inputs**: None
- **Expected Behavior**:
  - Inform user of successful login/registration
  - Provide links to dashboard or additional setup (e.g., MFA)
