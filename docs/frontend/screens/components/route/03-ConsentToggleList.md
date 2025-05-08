# ✅ ConsentToggleList

## 📋 Description

The `ConsentToggleList` component presents a list of user consent options (like marketing or analytics permissions) that users can toggle on or off. Each toggle is rendered using the `ConsentOptionToggle` component and managed in a form context.

---

## 🧩 Props

```ts
interface ConsentToggleListProps {
  options: {
    id: string;
    label: string;
    description?: string;
    required?: boolean;
  }[];
  values: Record<string, boolean>;
  onChange: (id: string, value: boolean) => void;
  disabled?: boolean;
}
```

---

## 🎯 States Supported

| State     | Description                             |
|-----------|-----------------------------------------|
| Default   | Toggle list is fully interactive        |
| Disabled  | Entire list is locked                   |
| Required  | Required toggles are fixed and labeled  |

---

## 🎨 Variants

- Inline or stacked layout
- Optional grouping by category
- ShadCN switch vs checkbox mode

---

## 🧪 Test Strategy

- Render list with multiple toggles
- Toggle state reflects `values` map
- Callback fires on user interaction
- Accessibility: labels, roles, focusable elements
- TDD: write all validation and interaction cases before implementation

---

## 🔌 Integration Usage

Used in:
- `ConsentScreen`
- `CompleteProfileForm`
