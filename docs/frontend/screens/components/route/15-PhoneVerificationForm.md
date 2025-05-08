# 📱 PhoneVerificationForm

## 📋 Description

The `PhoneVerificationForm` component handles user phone number confirmation. It includes input for the phone number and a code entry field, along with feedback messages and control over when the code is sent or resent.

---

## 🧩 Props

```ts
interface PhoneVerificationFormProps {
  phone: string;
  onPhoneChange: (value: string) => void;
  code: string;
  onCodeChange: (value: string) => void;
  onResendCode: () => void;
  onSubmit: () => void;
  loading?: boolean;
  error?: string;
  resendDisabled?: boolean;
}
```

---

## 🎯 States Supported

| State     | Description                                |
|-----------|--------------------------------------------|
| Default   | Phone + code fields are editable           |
| Loading   | Form is disabled and spinner shown         |
| Error     | Code invalid or phone formatting issue     |

---

## 🎨 Variants

- With or without resend code link
- Combined inline vs stacked layout
- Step-by-step (2-step entry) or combined view

---

## 🧪 Test Strategy

- Simulate phone input, code input, and submit
- Validate `onResendCode` and resend control
- Accessibility on labels, inputs, and feedback
- TDD: all expected behaviors tested before implementation

---

## 🔌 Integration Usage

Used in:
- `PhoneVerificationScreen`
- `MfaPhoneSetupFlow`
