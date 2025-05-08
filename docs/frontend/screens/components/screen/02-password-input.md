# 🔒 PasswordInput

## 📋 Description

The `PasswordInput` component is a reusable atomic input field for collecting secure password values. It includes support for toggling visibility, enforcing basic security constraints, and displaying error messages. It is used in authentication, password reset, and registration flows.

---

## 🧩 Props

```ts
interface PasswordInputProps {
  value: string;
  onChange: (value: string) => void;
  label?: string;
  placeholder?: string;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  autoFocus?: boolean;
  showStrengthMeter?: boolean;
}
```

---

## 🎯 States Supported

| State     | Description                                 |
|-----------|---------------------------------------------|
| Default   | Editable password field                     |
| Error     | Displays an error when `error` is set       |
| Disabled  | Field is grayed out and not editable        |
| Autofocus | Automatically focused on mount              |
| Visible   | Password text visible when toggled          |

---

## 🎨 Variants

- With or without strength meter
- With or without show/hide toggle
- Embedded in forms or as standalone

---

## 🧪 Test Strategy

- Verify rendering with default and all props
- Simulate typing and visibility toggle
- Display of strength meter if enabled
- Validate accessibility: label, aria attributes
- TDD: All states and edge cases must be tested first

---

## 🔌 Integration Usage

Used in the following components:
- `RegisterForm`
- `LoginForm`
- `ChangePasswordForm`
- `ResetPasswordForm`
