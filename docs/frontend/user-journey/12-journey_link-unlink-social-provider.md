

# 📝 Journey: Link or Unlink Social Provider

## 📌 Description

This journey allows a registered user to link or unlink external social identity providers (e.g. Google) to their account. Linking allows the user to authenticate using that provider. Unlinking disables login via that provider. At least one login method must remain available.

---

## 👥 Personas

- Registered User

---

## 🧩 Involved Apps

- `apps.users`
- `apps.auth`
- `apps.applications`

---

## 🧭 UX Flow

### 📺 Screen: Manage Linked Accounts

- **Route**: `/settings/providers`
- **Purpose**: Show a list of available and currently linked providers
- **Inputs**:
  - Button to link new provider
  - Button to unlink a currently linked provider
- **Expected Behavior**:
  - Display current linkage status
  - Initiate OAuth flow when linking a provider
  - Allow unlinking only if another valid login method exists
- **Backend Endpoints**:
  - `GET /api/users/me/providers/`
  - `POST /api/auth/social-link/`
  - `DELETE /api/auth/social-unlink/<provider>/`

---

### 📺 Screen: OAuth Authorization Redirect (Linking)

- **Route**: External Provider OAuth URL
- **Purpose**: Redirect user to authenticate with chosen provider
- **Inputs**:
  - Provider-specific login fields
- **Expected Behavior**:
  - Authenticate with provider
  - On return, link identity to existing user account
- **Backend Endpoints**:
  - `POST /api/auth/social-link/`

---

### 📺 Screen: Confirmation Message

- **Route**: `/settings/providers/success`
- **Purpose**: Inform the user of successful link or unlink operation
- **Inputs**: None
- **Expected Behavior**:
  - Display confirmation of change
  - Update visible provider list
