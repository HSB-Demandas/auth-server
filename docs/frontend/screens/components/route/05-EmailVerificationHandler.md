# 📧 EmailVerificationHandler

## 📋 Description

The `EmailVerificationHandler` component handles the processing of email verification tokens from a URL and provides visual feedback about the verification result. It is commonly used in account confirmation, registration, and email update workflows.

---

## 🧩 Props

```ts
interface EmailVerificationHandlerProps {
  token: string;
  onSuccess: () => void;
  onFailure?: () => void;
  loading?: boolean;
}
```

---

## 🎯 States Supported

| State     | Description                       |
|-----------|-----------------------------------|
| Loading   | Token being processed             |
| Success   | Email verified successfully       |
| Failure   | Token invalid or expired          |

---

## 🎨 Variants

- Message-only or full page
- Auto-redirect vs manual continue

---

## 🧪 Test Strategy

- Render loading, success, and failure states
- Simulate valid and invalid token paths
- Mock API integration for token status
- Accessibility: live region for feedback
- TDD: define test paths for full lifecycle

---

## 🔌 Integration Usage

Used in:
- `VerifyEmailScreen`
