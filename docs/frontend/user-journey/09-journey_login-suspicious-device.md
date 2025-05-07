

# 📝 Journey: Login with Suspicious or New Device

## 📌 Description

This journey is triggered when a user logs in from a new or unrecognized device (based on IP and User-Agent fingerprint). The system alerts the user and optionally requires confirmation of the device before granting full access. This is part of the platform’s security event monitoring and user protection strategy.

---

## 👥 Personas

- Registered User

---

## 🧩 Involved Apps

- `apps.auth`
- `apps.security_events`
- `apps.notifications`
- `apps.audit`

---

## 🧭 UX Flow

### 📺 Screen: Device Alert

- **Route**: `/device/alert`
- **Purpose**: Inform the user they are logging in from an unrecognized device
- **Inputs**:
  - Acknowledge or confirm device button
- **Expected Behavior**:
  - Device fingerprint is shown (e.g., browser, platform, partial IP)
  - User can choose to trust or deny access
  - On confirmation, device is stored and marked trusted
  - On denial, session is invalidated or user logged out
- **Backend Endpoints**:
  - `GET /api/security/devices/unconfirmed/`
  - `POST /api/security/devices/confirm/`
  - `DELETE /api/auth/sessions/current/` (if rejected)

---

### 📺 Screen: Device Confirmation Success

- **Route**: `/device/confirmed`
- **Purpose**: Notify user that the device is now trusted
- **Inputs**: None
- **Expected Behavior**:
  - Confirmation message shown
  - Redirect to dashboard or intended resource

---

### 📺 Screen: Device Confirmation Failure

- **Route**: `/device/failed`
- **Purpose**: Indicate failure to confirm device
- **Inputs**:
  - Retry or cancel option
- **Expected Behavior**:
  - Show error if token is invalid or expired
  - Allow user to retry or trigger support
