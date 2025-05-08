# 📘 TermsAgreement

## 📋 Description

The `TermsAgreement` component presents a legal agreement prompt to users such as terms of service and privacy policy. It allows the user to explicitly accept required terms before continuing with registration or usage.

---

## 🧩 Props

```ts
interface TermsAgreementProps {
  accepted: boolean;
  onChange: (value: boolean) => void;
  termsUrl: string;
  privacyUrl: string;
  error?: string;
}
```

---

## 🎯 States Supported

| State     | Description                              |
|-----------|------------------------------------------|
| Default   | Checkbox unchecked with links to terms   |
| Accepted  | Checkbox is marked true                  |
| Error     | Displays error when terms not accepted   |

---

## 🎨 Variants

- Modal version for full-page agreement
- Link styling as inline or below checkbox
- Translated policy names per locale

---

## 🧪 Test Strategy

- Checkbox renders and toggles correctly
- `onChange` callback functions as expected
- URLs open in new tab and are accessible
- TDD: all checkbox + validation flows tested first

---

## 🔌 Integration Usage

Used in:
- `RegisterForm`
- `SocialOnboardingScreen`
