

# 📝 Journey: Login with Social Provider

## 📌 Description

This journey allows a user to log in using an external identity provider (e.g. Google). If the user does not exist yet, the backend may auto-register them depending on app configuration. After successful authentication, the system may collect additional data if required, such as phone number or terms acceptance.

---

## 👥 Personas

- Anonymous User
- Registered User

---

## 🧩 Involved Apps

- `apps.auth`
- `apps.users`
- `apps.applications`
- `apps.compliance`
- `apps.security_events`

---

## 🧭 UX Flow

### 📺 Screen: Login with Social

- **Route**: `/login`
- **Purpose**: Let the user select and initiate login via an identity provider
- **Inputs**:
  - Social login buttons (e.g., "Continue with Google")
- **Expected Behavior**:
  - Redirect user to the provider's OAuth consent screen
  - On return, validate the OAuth token and issue login credentials
  - Auto-create user if allowed by application
- **Backend Endpoints**:
  - `POST /api/auth/social-login/`
  - `GET /api/applications/<id>/providers/`

---

### 📺 Screen: Additional Info Required (if profile incomplete)

- **Route**: `/complete-profile`
- **Purpose**: Collect missing fields not provided by the social provider
- **Inputs**:
  - Phone number (if required by app)
  - Accept terms (if not accepted)
- **Expected Behavior**:
  - Display a form with only required missing fields
  - Allow user to complete registration info
- **Backend Endpoints**:
  - `PATCH /api/users/me/`
  - `GET /api/applications/<id>/required_fields/`

---

### 📺 Screen: Accept Terms (if not accepted)

- **Route**: `/terms`
- **Purpose**: Display current policy documents and require acceptance
- **Inputs**: Acceptance checkbox
- **Expected Behavior**:
  - Block access to main app until accepted
- **Backend Endpoints**:
  - `GET /api/terms/`
  - `POST /api/terms/accept/`

---

### 📺 Screen: Device Confirmation (if applicable)

- **Route**: `/device/confirm`
- **Purpose**: Show unrecognized device info and ask for confirmation
- **Inputs**: Confirmation button
- **Expected Behavior**:
  - User sees device info (IP/User-Agent)
  - Can confirm the device or reject the session
- **Backend Endpoints**:
  - `POST /api/security/devices/confirm/`

---

### 📺 Screen: Welcome / Home

- **Route**: `/dashboard`
- **Purpose**: Final step — confirm login and direct user to main app
- **Inputs**: None
- **Expected Behavior**:
  - Show successful login message
  - Redirect to protected area of the app
