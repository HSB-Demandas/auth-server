# ☎️ PhoneInput

## 📋 Description

The `PhoneInput` component is an atomic form input designed specifically for capturing phone numbers. It may include country code selection, automatic formatting, and validation for international numbers. This component is used in registration, MFA, and profile update flows.

---

## 🧩 Props

```ts
interface PhoneInputProps {
  value: string;
  onChange: (value: string) => void;
  label?: string;
  placeholder?: string;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  autoFocus?: boolean;
}
```

---

## 🎯 States Supported

| State     | Description                          |
|-----------|--------------------------------------|
| Default   | Standard editable input              |
| Error     | Validation or formatting error shown |
| Disabled  | Input disabled from interaction      |
| Autofocus | Input automatically focused          |

---

## 🎨 Variants

- With or without country code dropdown
- Form-integrated vs. standalone
- Full width or constrained

---

## 🧪 Test Strategy

- Renders with default and all props
- Simulates valid and invalid number input
- Verifies formatting behavior
- Validates accessibility (label + screen reader)
- Edge cases: empty string, non-digit input
- TDD: All test cases must be written before implementation

---

## 🔌 Integration Usage

Used in the following components:
- `PhoneVerificationForm`
- `CompleteProfileForm`
- `MfaSetupForm`
