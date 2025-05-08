# 🚨 SuspiciousDeviceAlert

## 📋 Description

The `SuspiciousDeviceAlert` component informs users that a login attempt was made from an unrecognized or potentially suspicious device. It shows device metadata and offers the option to approve or reject the login.

---

## 🧩 Props

```ts
interface SuspiciousDeviceAlertProps {
  browser: string;
  os: string;
  ipAddress?: string;
  lastSeen: string;
  onApprove: () => void;
  onReject: () => void;
  loading?: boolean;
}
```

---

## 🎯 States Supported

| State       | Description                               |
|-------------|-------------------------------------------|
| Default     | Device info shown with action buttons     |
| Loading     | Buttons disabled while processing choice  |

---

## 🎨 Variants

- Card vs modal presentation
- Light or dark alert styling
- Trusted vs unknown device badges

---

## 🧪 Test Strategy

- Render all props correctly
- Simulate approve and reject interactions
- Validate loading and error states
- Accessibility: role alert, keyboard focus, screen reader support
- TDD: define all flows and fallback states in tests before implementation

---

## 🔌 Integration Usage

Used in:
- `LoginSuspiciousCheckpoint`
- `DeviceVerificationFlow`
