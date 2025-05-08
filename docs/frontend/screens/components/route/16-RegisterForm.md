# 📝 RegisterForm

## 📋 Description

The `RegisterForm` component handles the user interface and validation logic for account registration using email and password. It supports additional optional fields such as name or phone, and integrates with terms of service and consent components.

---

## 🧩 Props

```ts
interface RegisterFormProps {
  onSubmit: (data: { email: string; password: string; name?: string }) => void;
  loading?: boolean;
  error?: string;
}
```

---

## 🎯 States Supported

| State     | Description                              |
|-----------|------------------------------------------|
| Default   | Fields are editable                      |
| Loading   | Form is disabled while submitting        |
| Error     | Validation or backend error is shown     |

---

## 🎨 Variants

- With or without name field
- Full-width layout for modal vs page
- Error inline vs top message

---

## 🧪 Test Strategy

- Simulate valid/invalid submission
- Ensure error and loading states work
- Trigger `onSubmit` with correct data
- Accessibility and label testing
- TDD: define all cases before building

---

## 🔌 Integration Usage

Used in:
- `RegistrationScreen`
- `OnboardingFlow`
