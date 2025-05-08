# ✅ ConsentOptionToggle

## 📋 Description

The `ConsentOptionToggle` component represents a single user consent option that can be toggled on or off. It's commonly used within a list of configurable user consents such as marketing, analytics, or data sharing preferences.

---

## 🧩 Props

```ts
interface ConsentOptionToggleProps {
  id: string;
  label: string;
  description?: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
}
```

---

## 🎯 States Supported

| State     | Description                             |
|-----------|-----------------------------------------|
| Default   | Checkbox or switch is interactive       |
| Checked   | User has opted-in                       |
| Disabled  | Option cannot be toggled                |

---

## 🎨 Variants

- Switch-style toggle or checkbox
- With or without description text
- Disabled visual state (e.g., for required consents)

---

## 🧪 Test Strategy

- Render with label and initial state
- Toggle event calls `onChange`
- Visual changes for disabled and checked
- Accessibility compliance (label + ARIA)
- TDD: tests must be written before implementation

---

## 🔌 Integration Usage

Used in:
- `ConsentToggleList`
