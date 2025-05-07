

# 📘 Documenting User Journeys

This file defines the documentation structure and strategy for mapping user journeys into screen-by-screen UX flows. These flows guide the frontend design and implementation based on the backend capabilities described in this project.

---

## 📌 Purpose

Each user journey defines a real scenario experienced by a user type (persona), including what they see, click, submit, and how they flow through the system. It provides structure for:

- Designing frontend routes and screens
- Mapping endpoints and backend interactions
- Assigning features to personas
- Ensuring feature parity between backend and UI

---

## 🧱 Structure for Each Journey

Each documented journey should include:

### 1. **Title**
A short and clear name, e.g., `Login with Email and Password`.

### 2. **Description**
Briefly describe what this journey allows the user to do, why it exists, and its expected outcome.

### 3. **Personas Involved**
List the system personas (e.g., Anonymous User, Registered User, Admin) that go through this journey.

### 4. **Apps Involved**
Mention the backend apps used to support the flow (e.g., `apps.auth`, `apps.users`, `apps.compliance`).

### 5. **UX Flow: Screen-by-Screen**

Each screen should be described as:

#### 📺 Screen: `<Screen Name>`
- **Route**: `/example/route`
- **Purpose**: Why this screen exists
- **Inputs**: Form fields, buttons, selections
- **Expected Behavior**: Validations, side effects, transitions
- **Backend Endpoints Called**: List of relevant endpoints

Repeat this for every step in the journey.

---

## ✅ Example Journey (Template)

### 🔐 Login with Email and Password

#### Description:
This journey allows a registered user to log into the system using their email and password. MFA, device validation, and policy acceptance may appear based on configuration.

#### Personas:
- Anonymous User
- Registered User

#### Apps:
- `apps.auth`
- `apps.security_events`
- `apps.compliance`

#### UX Flow:

##### 📺 Screen: Login
- **Route**: `/login`
- **Purpose**: Collect user credentials and start login flow
- **Inputs**: Email, Password
- **Expected Behavior**:
  - Validate credentials against backend
  - On success, check if MFA is required
  - On failure, show error message
- **Backend**:
  - `POST /api/auth/login/`

##### 📺 Screen: MFA Challenge (if required)
- **Route**: `/mfa`
- **Purpose**: Enforce second factor authentication
- **Inputs**: SMS code or TOTP code
- **Expected Behavior**:
  - Send code to user (if SMS)
  - Submit token for validation
  - On success, proceed to dashboard
- **Backend**:
  - `POST /api/auth/mfa/verify/`

##### 📺 Screen: Device Confirmation (if needed)
- **Route**: `/device/confirm`
- **Purpose**: Confirm login from an unrecognized device
- **Inputs**: None (passive or confirm button)
- **Expected Behavior**:
  - Show device metadata
  - Let user approve or deny
- **Backend**:
  - `POST /api/security/devices/confirm/`

##### 📺 Screen: Accept Terms (if pending)
- **Route**: `/terms`
- **Purpose**: Show current privacy policy and terms of use
- **Inputs**: Accept checkbox
- **Expected Behavior**:
  - Block navigation until accepted
  - Store consent
- **Backend**:
  - `POST /api/terms/accept/`

---

## 🔄 Next Steps

Use this structure to document all journeys from `README.md > 🧭 User Journeys`.

Each journey should be a separate markdown file in the `/user-journeys/` folder or referenced in sidebar navigation.
