# ⬇️ DownloadButton

## 📋 Description

The `DownloadButton` component provides a reusable interface for initiating the download of a file or export. It supports stateful feedback such as loading indicators, disabled conditions, and download readiness. It can be used with direct download URLs or async callbacks.

---

## 🧩 Props

```ts
interface DownloadButtonProps {
  onClick: () => void;
  disabled?: boolean;
  loading?: boolean;
  label?: string;
}
```

---

## 🎯 States Supported

| State     | Description                            |
|-----------|----------------------------------------|
| Default   | Download available                     |
| Loading   | Button shows loading spinner           |
| Disabled  | Interaction blocked                    |

---

## 🎨 Variants

- Icon + label or icon-only button
- Outlined, solid, or ghost styles
- With or without tooltip for download info

---

## 🧪 Test Strategy

- Simulate click with handler execution
- Display loader during `loading` state
- Ensure button is not clickable when `disabled`
- Validate accessibility labels
- TDD: Write tests for each state before implementation

---

## 🔌 Integration Usage

Used in:
- `ExportDataSummary`
- `DataReportCard`
