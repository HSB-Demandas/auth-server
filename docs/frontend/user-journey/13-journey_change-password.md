

# 📝 Journey: Change Password

## 📌 Description

This journey enables a registered and authenticated user to change their password manually. It is accessible through their account settings and requires the current password for security confirmation. The user must meet password strength requirements and confirm the new password before submission.

---

## 👥 Personas

- Registered User

---

## 🧩 Involved Apps

- `apps.users`
- `apps.auth`

---

## 🧭 UX Flow

### 📺 Screen: Change Password Form

- **Route**: `/settings/password`
- **Purpose**: Allow the user to update their password securely
- **Inputs**:
  - Current password
  - New password
  - Confirm new password
- **Expected Behavior**:
  - Validate that current password is correct
  - Validate new password strength
  - Check that new and confirm match
  - Update password and invalidate other sessions if configured
  - Notify user of successful change
- **Backend Endpoints**:
  - `POST /api/users/change-password/`

---

### 📺 Screen: Password Changed Confirmation

- **Route**: `/settings/password/success`
- **Purpose**: Show a confirmation that the password was updated
- **Inputs**: None
- **Expected Behavior**:
  - Display success message
  - Suggest user logs out of other sessions if relevant
