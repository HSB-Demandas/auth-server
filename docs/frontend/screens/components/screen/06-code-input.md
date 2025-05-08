

# 🔢 CodeInput

## 📋 Description

The `CodeInput` component is used to capture a short numeric or alphanumeric verification code, such as those used in two-factor authentication (2FA), phone/email confirmation, or device validation. It typically renders a segmented input interface and manages focus automatically between fields.

---

## 🧩 Props

```ts
interface CodeInputProps {
  value: string;
  onChange: (value: string) => void;
  length?: number; // number of code digits (default: 6)
  autoFocus?: boolean;
  disabled?: boolean;
  error?: string;
}
```

---

## 🎯 States Supported

| State     | Description                             |
|-----------|-----------------------------------------|
| Default   | Editable segmented inputs               |
| Error     | Input is marked invalid                 |
| Disabled  | All input fields disabled               |
| Autofocus | Focus starts at the first segment       |

---

## 🎨 Variants

- 4-digit or 6-digit input length
- Alphanumeric vs numeric only
- Boxed style or underlined input segments

---

## 🧪 Test Strategy

- Render with default and edge case props
- Simulate input typing and backspace navigation
- Test focus behavior across segments
- Validate error rendering and disabled state
- Accessibility: test screen reader compatibility
- TDD: define expected behaviors for each state before implementation

---

## 🔌 Integration Usage

Used in the following components:
- `MfaChallenge`
- `PhoneVerificationForm`
- `ResetPasswordVerification`
