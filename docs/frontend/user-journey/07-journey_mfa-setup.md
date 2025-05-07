

# 📝 Journey: MFA Setup (TOTP or SMS)

## 📌 Description

This journey allows a registered user to activate multi-factor authentication (MFA) on their account, either using a Time-based One-Time Password (TOTP) app (such as Google Authenticator) or via SMS. The system may enforce MFA setup based on role or application configuration.

---

## 👥 Personas

- Registered User

---

## 🧩 Involved Apps

- `apps.users`
- `apps.auth`
- `libs.totp`
- `libs.twilio`

---

## 🧭 UX Flow

### 📺 Screen: MFA Setup Choice

- **Route**: `/mfa/setup`
- **Purpose**: Allow user to choose preferred MFA method
- **Inputs**:
  - Option selector (TOTP / SMS)
  - Continue button
- **Expected Behavior**:
  - Store user preference (optional)
  - Route to appropriate setup screen
- **Backend Endpoints**:
  - `GET /api/users/me/mfa/status/`

---

### 📺 Screen: Setup TOTP (App-Based)

- **Route**: `/mfa/setup/totp`
- **Purpose**: Show QR code to register TOTP in an authenticator app
- **Inputs**:
  - Scannable QR code
  - Manual entry key
  - 6-digit code field
- **Expected Behavior**:
  - Display QR and secret
  - Accept a 6-digit token to verify
  - On success, activate TOTP
- **Backend Endpoints**:
  - `GET /api/mfa/totp/setup/`
  - `POST /api/mfa/totp/verify/`

---

### 📺 Screen: Setup SMS

- **Route**: `/mfa/setup/sms`
- **Purpose**: Send and confirm MFA code via SMS
- **Inputs**:
  - Phone number (if not yet verified)
  - Send button
  - Code input field
- **Expected Behavior**:
  - Send code to phone
  - Validate code
  - On success, enable SMS-based MFA
- **Backend Endpoints**:
  - `POST /api/users/phone/verify/start/`
  - `POST /api/users/phone/verify/`
  - `POST /api/mfa/sms/enable/`

---

### 📺 Screen: MFA Setup Success

- **Route**: `/mfa/setup/success`
- **Purpose**: Confirm MFA is enabled
- **Inputs**: None
- **Expected Behavior**:
  - Show success state and CTA to continue
