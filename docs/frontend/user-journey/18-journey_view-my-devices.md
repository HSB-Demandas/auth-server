

# 📝 Journey: View My Devices

## 📌 Description

This journey allows a logged-in user to see all known and active devices associated with their account. Devices are identified based on login metadata such as User-Agent and IP fingerprint. This feature improves transparency and security, enabling users to recognize unauthorized access.

---

## 👥 Personas

- Registered User

---

## 🧩 Involved Apps

- `apps.security_events`
- `apps.auth`
- `apps.users`

---

## 🧭 UX Flow

### 📺 Screen: Known Devices

- **Route**: `/settings/devices`
- **Purpose**: Display all devices that have accessed the user’s account
- **Inputs**:
  - Device list (browser, location, last seen)
  - Actions: Trust, Revoke, or Mark Suspicious
- **Expected Behavior**:
  - Show trusted vs unconfirmed devices
  - Allow user to remove or mark devices manually
  - Clearly label current session
- **Backend Endpoints**:
  - `GET /api/security/devices/`
  - `POST /api/security/devices/<id>/trust/`
  - `DELETE /api/security/devices/<id>/`

---

### 📺 Screen: Revoke Confirmation (Optional)

- **Route**: Modal or inline
- **Purpose**: Confirm revoking or marking a device as untrusted
- **Inputs**:
  - Confirm / Cancel
- **Expected Behavior**:
  - On confirmation, device is flagged or removed
  - Optionally log out associated session (if active)
