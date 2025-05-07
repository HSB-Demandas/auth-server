

# 📝 Journey: MFA Login Challenge

## 📌 Description

This journey occurs after a user has successfully entered their primary login credentials (email/password or social login) and MFA is required. It prompts the user to complete a second authentication step using TOTP or SMS. The method depends on the user’s active MFA configuration.

---

## 👥 Personas

- Registered User (with MFA enabled)

---

## 🧩 Involved Apps

- `apps.auth`
- `libs.totp`
- `libs.twilio`
- `apps.users`

---

## 🧭 UX Flow

### 📺 Screen: MFA Challenge Prompt

- **Route**: `/mfa`
- **Purpose**: Prompt user to complete second authentication factor
- **Inputs**:
  - 6-digit TOTP code or SMS code
- **Expected Behavior**:
  - Display hint of method used (SMS or Authenticator App)
  - Submit code to backend for verification
  - On success, grant session and continue login
  - On failure, show error or retry prompt
- **Backend Endpoints**:
  - `POST /api/auth/mfa/verify/`

---

### 📺 Screen: Resend MFA Code (SMS only)

- **Route**: `/mfa?resend=sms`
- **Purpose**: Allow user to request a new SMS verification code
- **Inputs**:
  - Button to resend SMS
- **Expected Behavior**:
  - Trigger re-send of MFA SMS code
  - Show cooldown message if recently triggered
- **Backend Endpoints**:
  - `POST /api/mfa/sms/resend/`

---

### 📺 Screen: MFA Challenge Success

- **Route**: `/dashboard` (or app landing route)
- **Purpose**: Finalize login process
- **Inputs**: None
- **Expected Behavior**:
  - Redirect user to protected content or app dashboard
