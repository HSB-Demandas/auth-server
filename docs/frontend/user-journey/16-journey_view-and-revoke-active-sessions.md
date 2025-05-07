

# 📝 Journey: View and Revoke Active Sessions

## 📌 Description

This journey allows an authenticated user to see all of their active sessions across devices and revoke any of them manually. This is useful for managing security, identifying unauthorized access, or terminating forgotten logins from other browsers.

---

## 👥 Personas

- Registered User

---

## 🧩 Involved Apps

- `apps.auth`
- `apps.users`
- `apps.security_events`

---

## 🧭 UX Flow

### 📺 Screen: Active Sessions

- **Route**: `/settings/sessions`
- **Purpose**: Show a list of the user's active sessions
- **Inputs**:
  - Session metadata (device, IP, browser, timestamp)
  - Revoke (terminate) button per session
- **Expected Behavior**:
  - List current and past sessions associated with the user
  - Identify current session clearly
  - Allow user to revoke any session except the current
- **Backend Endpoints**:
  - `GET /api/auth/sessions/`
  - `DELETE /api/auth/sessions/<session_id>/`

---

### 📺 Screen: Revoke Confirmation (Optional Modal)

- **Route**: Inline modal
- **Purpose**: Confirm user's intention to revoke a session
- **Inputs**:
  - Confirm and Cancel buttons
- **Expected Behavior**:
  - On confirm, send DELETE request
  - Show success or error toast
- **Backend Endpoints**:
  - `DELETE /api/auth/sessions/<session_id>/`

---

### 📺 Screen: Session Revoked

- **Route**: `/settings/sessions`
- **Purpose**: Return to updated session list view
- **Inputs**: None
- **Expected Behavior**:
  - Updated list without revoked session
  - Optionally notify the user that the session has been removed
