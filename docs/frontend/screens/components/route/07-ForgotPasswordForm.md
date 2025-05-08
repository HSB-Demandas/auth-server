# 🔁 ForgotPasswordForm

## 📋 Description

The `ForgotPasswordForm` component provides a form for users to request a password reset via their email. It captures the user's email and triggers the reset request process while providing appropriate feedback.

---

## 🧩 Props

```ts
interface ForgotPasswordFormProps {
  onSubmit: (email: string) => void;
  loading?: boolean;
  error?: string;
}
```

---

## 🎯 States Supported

| State     | Description                        |
|-----------|------------------------------------|
| Default   | Input form for email entry         |
| Error     | Email not found or API error       |
| Loading   | Form disabled, spinner shown       |

---

## 🎨 Variants

- Inline or full-page form
- Optional success message placeholder

---

## 🧪 Test Strategy

- Validate email input and submission
- Trigger `onSubmit` correctly
- Display error when `error` prop is set
- Accessibility: focus management, label
- TDD: tests before form logic begins

---

## 🔌 Integration Usage

Used in:
- `ForgotPasswordScreen`
- `ResetRequestFlow`
