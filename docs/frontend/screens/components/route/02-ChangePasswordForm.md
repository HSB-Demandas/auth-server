# 🔒 ChangePasswordForm

## 📋 Description

The `ChangePasswordForm` component provides a secure form for authenticated users to change their current password. It includes fields for current password, new password, and confirmation, along with validation and strength indication.

---

## 🧩 Props

```ts
interface ChangePasswordFormProps {
  onSubmit: (data: { currentPassword: string; newPassword: string }) => void;
  loading?: boolean;
  error?: string;
}
```

---

## 🎯 States Supported

| State     | Description                            |
|-----------|----------------------------------------|
| Default   | Standard input with validation         |
| Error     | Server or client error is shown        |
| Loading   | Disables form and shows spinner        |

---

## 🎨 Variants

- With or without password strength meter
- Show/hide password toggles
- Inline vs stacked layout

---

## 🧪 Test Strategy

- Test rendering with all props
- Validate field input and error display
- Simulate form submit and ensure callback fires
- Password visibility toggle and strength meter logic
- Accessibility coverage for all fields and labels
- TDD: all logic-driven paths tested first

---

## 🔌 Integration Usage

Used in:
- `AccountSettingsScreen`
- `PasswordManagementSection`
