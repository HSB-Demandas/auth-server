# 📤 SendCodeButton

## 📋 Description

The `SendCodeButton` component is used to trigger the sending of a verification code (via SMS, email, or other channels). It handles cooldown state, disabling logic, and optional loading indication. It is typically used alongside phone or email verification fields.

---

## 🧩 Props

```ts
interface SendCodeButtonProps {
  onClick: () => void;
  disabled?: boolean;
  loading?: boolean;
  cooldown?: number; // seconds
  lastSentAt?: number; // timestamp
}
```

---

## 🎯 States Supported

| State     | Description                                       |
|-----------|---------------------------------------------------|
| Default   | Button is clickable and ready                     |
| Loading   | Shows spinner or feedback during API call         |
| Cooldown  | Button is disabled with countdown indicator       |
| Disabled  | General disabled state                            |

---

## 🎨 Variants

- Primary or ghost button
- Full-width vs inline
- Cooldown badge vs inline text countdown

---

## 🧪 Test Strategy

- Validate button renders with all prop combinations
- Simulate clicks and ensure `onClick` fires when allowed
- Test cooldown state transitions and timing
- Display of loading indicator when `loading` is true
- Ensure accessible labels and focusability
- TDD: tests must be implemented prior to component logic

---

## 🔌 Integration Usage

Used in the following components:
- `PhoneVerificationForm`
- `MfaSetupForm`
- `ResetPasswordRequestForm`
