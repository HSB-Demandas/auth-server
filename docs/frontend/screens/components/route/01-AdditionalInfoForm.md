# 👤 AdditionalInfoForm

## 📋 Description

The `AdditionalInfoForm` component is a form that captures required user profile fields that may not be provided by social login providers. It is used after registration or login when additional information (like phone number or policy consent) is needed to complete the account setup.

---

## 🧩 Props

```ts
interface AdditionalInfoFormProps {
  defaultValues: {
    phone?: string;
    country?: string;
  };
  onSubmit: (data: { phone: string; country: string }) => void;
  loading?: boolean;
  error?: string;
}
```

---

## 🎯 States Supported

| State     | Description                              |
|-----------|------------------------------------------|
| Default   | Standard form entry                      |
| Error     | Backend or validation error is shown     |
| Loading   | Submit button disabled and spinner active|

---

## 🎨 Variants

- With or without country selector
- Responsive layout (1-column mobile, 2-column desktop)

---

## 🧪 Test Strategy

- Validate input and submission logic
- Check initial values are populated correctly
- Submit event triggers `onSubmit` with expected values
- Verify accessibility (form labels and tab order)
- TDD: All edge cases and state transitions tested before implementation

---

## 🔌 Integration Usage

Used in:
- `CompleteProfileScreen`
- `SocialRegistrationFlow`
