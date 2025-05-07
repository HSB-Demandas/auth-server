

# 📝 Journey: Password Reset (Logged-in User)

## 📌 Description

This journey allows an authenticated user to initiate a password reset process for security or credential refresh purposes. It differs from the "forgot password" flow by being accessible from within the user's session and does not require email verification.

---

## 👥 Personas

- Registered User

---

## 🧩 Involved Apps

- `apps.users`
- `apps.auth`

---

## 🧭 UX Flow

### 📺 Screen: Reset Password Form (User-Initiated)

- **Route**: `/settings/password/reset`
- **Purpose**: Allow logged-in user to reset password without knowing current one (if session is already trusted)
- **Inputs**:
  - New password
  - Confirm new password
- **Expected Behavior**:
  - Validate new password strength and confirmation match
  - Immediately update user credentials
  - Invalidate old sessions if required
- **Backend Endpoints**:
  - `POST /api/users/password/reset/`

---

### 📺 Screen: Password Reset Success

- **Route**: `/settings/password/reset/success`
- **Purpose**: Show confirmation that password was updated
- **Inputs**: None
- **Expected Behavior**:
  - Display success message
  - Suggest logout and re-authentication (optional)
