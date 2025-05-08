

# 📝 Journey: Terms, Privacy, and User Consent Acceptance

**## 📌 Description**

This journey ensures users explicitly accept the most recent versions of the system's terms of use, privacy policy, and any additional consent requirements (e.g., for marketing or analytics). Acceptance may be required during registration, first login, or after a new version is published. The journey adapts based on application settings.

---

## 👥 Personas

- Anonymous User
- Registered User

---

## 🧩 Involved Apps

- `apps.compliance`
- `apps.users`

---

## 🧭 UX Flow

### 📺 Screen: Accept Terms & Privacy Policy

- **Route**: `/terms`
- **Purpose**: Present current legal documents to the user for acceptance
- **Inputs**:
  - Viewable terms and privacy content (versioned)
  - Checkboxes for acceptance
- **Expected Behavior**:
  - Block access to system if required terms are not accepted
  - Require all checkboxes (if configured)
  - Save acceptance to user profile
- **Backend Endpoints**:
  - `GET /api/terms/` — fetch current terms and privacy policy
  - `POST /api/terms/accept/` — accept both documents

---

### 📺 Screen: Granular Consent (Optional)

- **Route**: `/consent`
- **Purpose**: Let user opt-in or out of specific data usage purposes
- **Inputs**:
  - Toggle switches or checkboxes per consent type (e.g., marketing_emails, analytics)
- **Expected Behavior**:
  - Store consent preferences per user
  - Persist consent at realm level
- **Backend Endpoints**:
  - `GET /api/consent/` — retrieve existing consent preferences
  - `POST /api/consent/<type>/` — update single consent

---

### 📺 Screen: Confirmation

- **Route**: `/terms/success`
- **Purpose**: Confirm acceptance and proceed to application
- **Inputs**: None
- **Expected Behavior**:
  - Redirect to dashboard or continue login/registration flow
