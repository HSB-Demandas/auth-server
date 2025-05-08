# 📦 ExportDataList

## 📋 Description

The `ExportDataList` component renders a visual list or table of user data categories that will be included in a personal data export. It helps users understand what is packaged when initiating a GDPR/LGPD data export.

---

## 🧩 Props

```ts
interface ExportDataListProps {
  items: {
    id: string;
    label: string;
    description?: string;
  }[];
}
```

---

## 🎯 States Supported

| State     | Description                          |
|-----------|--------------------------------------|
| Default   | All categories displayed              |
| Empty     | Shows fallback or "no data" message   |

---

## 🎨 Variants

- List or table layout
- Expandable descriptions
- Download-ready indicator (optional)

---

## 🧪 Test Strategy

- Render with populated and empty `items`
- Snapshot test for layout consistency
- Accessibility checks (headers, list roles)
- TDD: Define all test cases before coding begins

---

## 🔌 Integration Usage

Used in:
- `ExportDataSummary`
