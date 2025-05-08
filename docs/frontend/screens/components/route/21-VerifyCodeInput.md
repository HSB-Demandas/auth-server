# 🔢 VerifyCodeInput

## 📋 Description

The `VerifyCodeInput` component provides a segmented input interface for users to enter one-time passcodes (OTPs) such as TOTP or SMS verification codes. It manages focus, formatting, and error states internally.

---

## 🧩 Props

```ts
interface VerifyCodeInputProps {
  value: string;
  onChange: (value: string) => void;
  length?: number;
  disabled?: boolean;
  error?: string;
}
```

---

## 🎯 States Supported

| State     | Description                             |
|-----------|-----------------------------------------|
| Default   | Fields accept numeric input              |
| Error     | Fields are styled to indicate failure    |
| Disabled  | Input fields are locked                  |

---

## 🎨 Variants

- 4 or 6-digit code entry
- Box or underline style per digit
- Combined input vs individual fields

---

## 🧪 Test Strategy

- Render segments based on `length` prop
- Handle keyboard input and backspace
- Validate onChange propagation
- Accessibility: labeled fields and tab order
- TDD: verify component behavior before implementing

---

## 🔌 Integration Usage

Used in:
- `MfaChallenge`
- `PhoneVerificationForm`
- `EmailCodeVerificationScreen`
