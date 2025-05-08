# 🔐 LoginForm

## 📋 Description

The `LoginForm` component is used for traditional email + password login. It may include “remember me” toggling and links to password recovery. It handles validation, errors, and optional loading state.

---

## 🧩 Props

```ts
interface LoginFormProps {
  onSubmit: (data: { email: string; password: string }) => void;
  loading?: boolean;
  error?: string;
  remember?: boolean;
  onRememberChange?: (checked: boolean) => void;
}
```

---

## 🎯 States Supported

| State     | Description                     |
|-----------|---------------------------------|
| Default   | Normal input flow               |
| Error     | Shows form-level error          |
| Loading   | Disables submit + spinner shown |

---

## 🎨 Variants

- With or without remember me
- Centered vs inline layout
- Autofocus first field

---

## 🧪 Test Strategy

- Validate input value handling
- Simulate submit and callback
- Trigger `onRememberChange`
- Accessibility: proper labels and error semantics
- TDD: define behavior before writing implementation

---

## 🔌 Integration Usage

Used in:
- `LoginScreen`
- `AuthModal`
