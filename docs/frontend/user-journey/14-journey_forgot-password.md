

# 📝 Journey: Forgot Password

## 📌 Description

This journey allows a user who has forgotten their password to initiate a secure password reset process via their email address. The process includes submitting the email, receiving a reset link with a token, and setting a new password using that token.

---

## 👥 Personas

- Anonymous User
- Registered User

---

## 🧩 Involved Apps

- `apps.auth`
- `apps.users`

---

## 🧭 UX Flow

### 📺 Screen: Forgot Password Request

- **Route**: `/forgot-password`
- **Purpose**: Allow the user to request a password reset
- **Inputs**:
  - Email address
- **Expected Behavior**:
  - Validate email format
  - Submit request to backend
  - Trigger email with password reset link if account exists
  - Show generic success message regardless of account existence
- **Backend Endpoints**:
  - `POST /api/auth/password/reset/request/`

---

### 📺 Screen: Reset Password (via Token)

- **Route**: `/reset-password?token=abc123`
- **Purpose**: Let user enter a new password after following email link
- **Inputs**:
  - New password
  - Confirm new password
- **Expected Behavior**:
  - Validate token on backend
  - Submit new password
  - Show error if token is invalid or expired
- **Backend Endpoints**:
  - `POST /api/auth/password/reset/confirm/`

---

### 📺 Screen: Reset Success

- **Route**: `/reset-password/success`
- **Purpose**: Confirm that the password has been reset
- **Inputs**: None
- **Expected Behavior**:
  - Display success message
  - Suggest login with new credentials
