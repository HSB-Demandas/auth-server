# 📥 EmailInput

## 📋 Description

The `EmailInput` component is an atomic input field used to collect email addresses across various forms such as registration, login, password recovery, and profile updates. It ensures accessibility and supports basic format validation.

---

## 🧩 Props

```ts
interface EmailInputProps {
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

| State     | Description                             |
|-----------|-----------------------------------------|
| Default   | Normal editable email input             |
| Error     | Shows validation or external error text |
| Disabled  | Field is non-interactive                |

---

## 🎨 Variants

- With or without label
- Full-width layout
- Autofocused on render

---

## 🧪 Test Strategy

- Render with all supported props
- Simulate `onChange` input behavior
- Display of error message when `error` prop is set
- Field disabled state behaves correctly
- Autofocus is applied when specified
- Accessibility tested with screen readers and labels

> 💡 TDD Approach: All test cases above must be written before implementing the component logic.

---

## 🔌 Integration Usage

Used in the following components:
- `RegisterForm`
- `LoginForm`
- `ForgotPasswordForm`
- `CompleteProfileForm`
