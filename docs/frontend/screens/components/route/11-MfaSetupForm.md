# 🔐 MfaSetupForm

## 📋 Description

The `MfaSetupForm` component handles the user interface and logic for enabling multi-factor authentication (MFA). It allows the user to choose a method (TOTP or SMS), configure the selected method, and confirm its activation.

---

## 🧩 Props

```ts
interface MfaSetupFormProps {
  method: 'totp' | 'sms';
  onSubmit: (code: string) => void;
  loading?: boolean;
  error?: string;
  onMethodChange?: (method: 'totp' | 'sms') => void;
}
```

---

## 🎯 States Supported

| State       | Description                            |
|-------------|----------------------------------------|
| Default     | Input field and submit button visible  |
| Loading     | Spinner shown and form disabled        |
| Error       | Message for invalid or failed token    |

---

## 🎨 Variants

- TOTP setup with QR code + code entry
- SMS setup with phone input + code

---

## 🧪 Test Strategy

- Test rendering for both methods
- Validate submission flow
- Trigger method change handler
- Accessibility and form semantics
- TDD: all flow logic tested before implementation

---

## 🔌 Integration Usage

Used in:
- `MfaOnboardingScreen`
- `SecuritySettingsPage`
