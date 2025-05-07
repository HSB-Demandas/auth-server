

# 📝 Journey: Email Verification

## 📌 Description

This journey allows a user to confirm ownership of their email address by validating a token sent to their inbox. Email verification is typically triggered after user registration or when a user changes their email address. It ensures that only users with access to a valid email can complete registration or update their profile.

---

## 👥 Personas

- Registered User
- Anonymous User (after self-registration)

---

## 🧩 Involved Apps

- `apps.users`
- `apps.auth`
- `apps.compliance`
- `apps.notifications`

---

## 🧭 UX Flow

### 📺 Screen: Prompt to Verify Email

- **Route**: `/verify/email`
- **Purpose**: Inform the user that a verification email has been sent
- **Inputs**:
  - Resend button
- **Expected Behavior**:
  - Display masked email address used
  - Offer resend link with rate limit enforced
- **Backend Endpoints**:
  - `POST /api/users/resend-verification/`

---

### 📺 Screen: Deep Link with Token

- **Route**: `/verify/email?token=abc123`
- **Purpose**: Accept the token from the email and verify the user
- **Inputs**: Token (via URL param)
- **Expected Behavior**:
  - Automatically verify user using token
  - On success, redirect to login or dashboard
  - On failure, show option to resend or contact support
- **Backend Endpoints**:
  - `POST /api/users/verify-email/`

---

### 📺 Screen: Verification Success

- **Route**: `/verify/email/success`
- **Purpose**: Show confirmation of successful verification
- **Inputs**: None
- **Expected Behavior**:
  - Display "Email Verified!" confirmation
  - Offer link to log in or continue session

---

### 📺 Screen: Verification Failure

- **Route**: `/verify/email/failed`
- **Purpose**: Handle invalid or expired token
- **Inputs**: None
- **Expected Behavior**:
  - Display error message
  - Allow user to resend email or retry
- **Backend Endpoints**:
  - `POST /api/users/resend-verification/`
