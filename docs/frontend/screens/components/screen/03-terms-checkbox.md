# 📘 TermsCheckbox

## 📋 Description

The `TermsCheckbox` component is a reusable checkbox field designed to capture user consent for accepting terms of service, privacy policies, or any legal agreement. It is typically used during registration or in compliance-related prompts.

---

## 🧩 Props

```ts
interface TermsCheckboxProps {
  checked: boolean;
  onChange: (value: boolean) => void;
  label?: string;
  error?: string;
  required?: boolean;
  disabled?: boolean;
}
```

---

## 🎯 States Supported

| State     | Description                                     |
|-----------|-------------------------------------------------|
| Default   | Unchecked checkbox with optional label          |
| Checked   | User has accepted the terms                     |
| Error     | Validation message shown when not accepted      |
| Disabled  | Checkbox is not editable                        |

---

## 🎨 Variants

- Standalone with full terms label
- Inline with summary and link to full terms
- Used inside form or modal

---

## 🧪 Test Strategy

- Test rendering with label and default state
- Simulate toggle and check behavior
- Validate error rendering
- Accessibility: ensure correct label and `aria` attributes
- TDD: tests must be written before component logic

---

## 🔌 Integration Usage

Used in the following components:
- `RegisterForm`
- `CompleteProfileForm`
- `TermsAgreementModal`
