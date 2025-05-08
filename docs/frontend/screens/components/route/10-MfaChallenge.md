# 🧪 MfaChallenge

## 📋 Description

The `MfaChallenge` component handles MFA validation during login. It provides an input for a 6-digit token (TOTP or SMS), handles state transitions, and optionally allows code resend or fallback options.

---

## 🧩 Props

```ts
interface MfaChallengeProps {
  onSubmit: (code: string) => void;
  loading?: boolean;
  error?: string;
  onResend?: () => void;
  method?: 'totp' | 'sms';
}
```

---

## 🎯 States Supported

| State     | Description                        |
|-----------|------------------------------------|
| Default   | Code input and submit enabled      |
| Loading   | Input and button disabled          |
| Error     | Invalid or expired token shown     |

---

## 🎨 Variants

- With resend link (for SMS)
- TOTP or SMS variant
- With countdown (future enhancement)

---

## 🧪 Test Strategy

- Simulate code input and submit
- Trigger resend callback
- Validate loading and error states
- TDD: define full interaction before implementing

---

## 🔌 Integration Usage

Used in:
- `LoginMfaStep`
- `SecureFlowCheckpoint`
