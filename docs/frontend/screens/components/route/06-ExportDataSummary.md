# 📦 ExportDataSummary

## 📋 Description

The `ExportDataSummary` component displays a summary interface for personal data export requests. It is used to inform users of the data categories included in their export and provide a trigger for download when the export is ready.

---

## 🧩 Props

```ts
interface ExportDataSummaryProps {
  items: {
    id: string;
    label: string;
    description?: string;
  }[];
  isReady: boolean;
  loading?: boolean;
  onDownload: () => void;
}
```

---

## 🎯 States Supported

| State     | Description                                       |
|-----------|---------------------------------------------------|
| Default   | List is rendered; download not yet available      |
| Ready     | Download button is enabled                        |
| Loading   | Download button shows loading spinner or disabled |

---

## 🎨 Variants

- Vertical or grid layout of export items
- Optional inclusion of descriptions
- Full page or modal context

---

## 🧪 Test Strategy

- Render summary with various list lengths
- Button shows only when `isReady` is true
- Simulate `onDownload` callback
- Visual feedback for loading state
- Accessibility test: role=list, headings, button focus
- TDD: define test cases before coding (no mock data inside)

---

## 🔌 Integration Usage

Used in:
- `ExportPersonalDataScreen`
- `PrivacySettingsPanel`
