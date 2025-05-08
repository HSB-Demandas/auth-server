# 💻 DeviceMetadataBox

## 📋 Description

The `DeviceMetadataBox` component displays detailed metadata about a device used during login or session activity. It helps users recognize and manage trusted or suspicious devices by summarizing browser, operating system, IP address, and last seen timestamp. It is typically used in device confirmation or session management flows.

---

## 🧩 Props

```ts
interface DeviceMetadataBoxProps {
  browser: string;
  os: string;
  ipAddress?: string;
  lastSeen?: string;
  isTrusted?: boolean;
}
```

---

## 🎯 States Supported

| State       | Description                                 |
|-------------|---------------------------------------------|
| Default     | Metadata displayed with neutral status      |
| Trusted     | Marked with visual confirmation (badge/icon)|
| Untrusted   | Highlighted as potentially risky            |
| Missing IP  | IP data is unavailable or anonymized        |

---

## 🎨 Variants

- Compact or full layout
- With or without trust badge
- Inline vs card mode

---

## 🧪 Test Strategy

- Render with full and partial props
- Verify visual status for trusted/untrusted
- Validate conditional rendering (e.g. IP missing)
- Snapshot test for layout variants
- Accessibility: verify readable metadata for screen readers
- TDD: all tests written before component logic

---

## 🔌 Integration Usage

Used in the following components:
- `DeviceConfirmationCard`
- `SessionCard`
- `KnownDevicesList`
