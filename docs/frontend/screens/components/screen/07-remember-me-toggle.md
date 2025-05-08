# 🗂 RememberMeToggle

## 📋 Description

The `RememberMeToggle` component is a reusable checkbox element that allows users to request persistent login sessions. When enabled, this setting informs the authentication system to issue longer-lived tokens or persistent cookies.

---

## 🧩 Props

```ts
interface RememberMeToggleProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
  disabled?: boolean;
}
```

---

## 🎯 States Supported

| State     | Description                            |
|-----------|----------------------------------------|
| Default   | Standard unchecked checkbox            |
| Checked   | Persistent login requested             |
| Disabled  | Checkbox is non-interactive            |

---

## 🎨 Variants

- Custom label (e.g., “Keep me signed in”)
- Small or large size
- Inline within form or standalone block

---

## 🧪 Test Strategy

- Render with all combinations of props
- Simulate toggle interaction and validate `onChange` callback
- Validate disabled behavior
- Accessibility: proper labeling and screen reader support
- TDD: all logic and edge cases must be covered in tests first

---

## 🔌 Integration Usage

Used in the following components:
- `LoginForm`
