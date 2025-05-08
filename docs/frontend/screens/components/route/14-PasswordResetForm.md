# 🔁 PasswordResetForm

## 📋 Description

The `PasswordResetForm` component is used to let users reset their password using a valid password reset token (typically obtained via email). It provides inputs for a new password and confirmation, with validation and error handling.

---

## 🧩 Props

```ts
interface PasswordResetFormProps {
  onSubmit: (data: { password: string; confirmPassword: string }) => void;
  loading?: boolean;
  error?: string;
}
```

---

## 🎯 States Supported

| State     | Description                           |
|-----------|---------------------------------------|
| Default   | Form ready for password input         |
| Loading   | Submit disabled and spinner shown     |
| Error     | Backend or validation error shown     |

---

## 🎨 Variants

- With or without password strength meter
- Auto-focus on first input
- Validation shown inline or on submit

---

## 🧪 Test Strategy

- Render with all prop states
- Simulate valid and invalid submissions
- Validate error and loading behaviors
- Accessibility checks on input labels
- TDD: all tests written before implementation

---

## 🔌 Integration Usage

Used in:
- `ResetPasswordScreen`
