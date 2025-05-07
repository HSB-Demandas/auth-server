# 📝 Journey: Export Personal Data (LGPD/GDPR)

## 📌 Description

This journey allows a user to export all personal information stored in the system in a structured and readable format, in compliance with privacy regulations such as LGPD and GDPR. Exported data includes user profile, roles, sessions, audit logs, and consent preferences.

---

## 👥 Personas

- Registered User

---

## 🧩 Involved Apps

- `apps.users`
- `apps.permissions`
- `apps.audit`
- `apps.compliance`
- `apps.auth`

---

## 🧭 UX Flow

### 📺 Screen: Export Data Request

- **Route**: `/settings/export`
- **Purpose**: Allow the user to request export of all personal data
- **Inputs**:
  - Export button
- **Expected Behavior**:
  - Confirm intent to export
  - Send export request to backend
  - Display message that data will be downloaded or emailed
- **Backend Endpoints**:
  - `GET /api/users/me/export/`

---

### 📺 Screen: Export Ready (Optional)

- **Route**: `/settings/export/success`
- **Purpose**: Inform user that export is ready
- **Inputs**:
  - Download link (if applicable)
- **Expected Behavior**:
  - Show status of export
  - Allow user to download or receive file via email
  - Optionally indicate when it expires or how to revoke
