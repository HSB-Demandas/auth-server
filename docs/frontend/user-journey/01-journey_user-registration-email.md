

# 📝 Journey: User Registration with Email

## 📌 Description

This journey enables a new user to register for an account using their email address and password. The registration flow includes validating input, submitting registration data, confirming email, and optionally accepting terms of use and privacy policy. Depending on app configuration, certain screens may be conditionally shown.

---

## 👥 Personas

- Anonymous User

---

## 🧩 Involved Apps

- `apps.users`
- `apps.compliance`
- `apps.auth`
- `django_hsb_ratelimit` (optional, for abuse protection)

---

## 🧭 UX Flow

### 📺 Screen: Registration Form

- **Route**: `/register`
- **Purpose**: Allow a new user to create an account using their email address
- **Inputs**:
  - Email
  - Password
  - Confirm Password
  - (Optional) Full Name
  - Accept Terms (Checkbox)
- **Expected Behavior**:
  - Validate inputs client-side (required fields, password match)
  - Submit data to backend
  - Display error if account exists or validation fails
  - Redirect to confirmation screen on success
- **Backend Endpoints**:
  - `POST /api/users/register/`

---

### 📺 Screen: Email Confirmation Sent

- **Route**: `/register/confirm-email`
- **Purpose**: Inform the user that a confirmation email has been sent
- **Inputs**: None
- **Expected Behavior**:
  - Inform the user to check their email
  - Provide link to resend confirmation
- **Backend Endpoints**:
  - `POST /api/users/resend-confirmation/` (optional)

---

### 📺 Screen: Email Confirmation Clicked (Deep Link)

- **Route**: `/verify/email?token=...`
- **Purpose**: Validate the token received by email and activate the account
- **Inputs**: Token via URL
- **Expected Behavior**:
  - On success, activate user and redirect to login or next step
  - On failure, show error and option to resend email
- **Backend Endpoints**:
  - `POST /api/users/verify-email/`

---

### 📺 Screen: Terms Acceptance (if required post-registration)

- **Route**: `/terms`
- **Purpose**: Present the latest terms and require acceptance
- **Inputs**: Accept checkbox
- **Expected Behavior**:
  - Display most recent terms and privacy policy
  - Submit acceptance
- **Backend Endpoints**:
  - `GET /api/terms/`
  - `POST /api/terms/accept/`

---

### 📺 Screen: Registration Complete

- **Route**: `/register/success`
- **Purpose**: Confirm account creation is complete
- **Inputs**: None
- **Expected Behavior**:
  - Provide CTA to login
  - Optionally show dashboard preview
