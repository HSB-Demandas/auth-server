# 🛡 DeviceConfirmationCard

## 📋 Description

The `DeviceConfirmationCard` component is used to display details about a device that requires user verification after login or during suspicious activity. It includes device metadata, security warnings, and confirmation actions.

---

## 🧩 Props

```ts
interface DeviceConfirmationCardProps {
  browser: string;
  os: string;
  ipAddress?: string;
  lastSeen?: string;
  onConfirm: () => void;
  onReject?: () => void;
}
```

---

## 🎯 States Supported

| State       | Description                                      |
|-------------|--------------------------------------------------|
| Default     | Confirmation prompt with device info             |
| Confirmed   | Confirmation submitted and pending next step     |
| Rejected    | Optionally shows rejection flow or redirect      |

---

## 🎨 Variants

- Vertical card or modal layout
- Button-only vs link + button actions
- Trusted vs untrusted device styling

---

## 🧪 Test Strategy

- Render with and without optional props
- Simulate confirm/reject actions
- Validate visual feedback for trusted/untrusted
- Snapshot tests for UI variants
- Accessibility for actions and metadata
- TDD: test all state transitions before implementation

---

## 🔌 Integration Usage

Used in:
- `DeviceVerificationFlow`
- `SuspiciousLoginScreen`
