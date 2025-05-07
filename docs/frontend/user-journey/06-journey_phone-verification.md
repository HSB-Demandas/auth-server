

# 📝 Journey: Phone Verification

## 📌 Description

This journey allows a user to verify their phone number using a token (usually a numeric code) sent via SMS. It is commonly used for account validation during registration, profile updates, or before assigning roles that require phone confirmation. The verification may use Twilio or similar services behind the scenes.

---

## 👥 Personas

- Registered User

---

## 🧩 Involved Apps

- `apps.users`
- `apps.auth`
- `libs.twilio`
- `django_hsb_twilio`

---

## 🧭 UX Flow

### 📺 Screen: Enter Phone Number

- **Route**: `/verify/phone`
- **Purpose**: Collect the user’s phone number to initiate verification
- **Inputs**:
  - Phone number input field
  - Submit button
- **Expected Behavior**:
  - Validate phone number format
  - Trigger backend to send verification code via SMS
  - Proceed to code input screen
- **Backend Endpoints**:
  - `POST /api/users/phone/verify/start/`

---

### 📺 Screen: Enter Verification Code

- **Route**: `/verify/phone/code`
- **Purpose**: Accept and validate the code sent to the user’s phone
- **Inputs**:
  - 6-digit verification code
  - Submit button
- **Expected Behavior**:
  - Match code with backend using Twilio (or other)
  - On success, mark phone as verified
  - On failure, show retry or resend option
- **Backend Endpoints**:
  - `POST /api/users/phone/verify/`

---

### 📺 Screen: Verification Success

- **Route**: `/verify/phone/success`
- **Purpose**: Confirm that the phone number is verified
- **Inputs**: None
- **Expected Behavior**:
  - Display confirmation and continue navigation
  - May return user to profile or registration flow

---

### 📺 Screen: Verification Failure

- **Route**: `/verify/phone/failed`
- **Purpose**: Inform the user that verification failed
- **Inputs**:
  - Resend button
  - Retry input
- **Expected Behavior**:
  - Offer to restart the flow or resend code
- **Backend Endpoints**:
  - `POST /api/users/phone/verify/start/`
