# 🧾 SessionCard

## 📋 Description

The `SessionCard` component represents an active or historical user session with metadata such as device, location, and last activity. It includes a revoke action for terminating the session remotely.

---

## 🧩 Props

```ts
interface SessionCardProps {
  sessionId: string;
  device: string;
  ipAddress?: string;
  lastSeen: string;
  isCurrent?: boolean;
  onRevoke?: () => void;
}
```

---

## 🎯 States Supported

| State       | Description                            |
|-------------|----------------------------------------|
| Default     | Session info rendered with actions     |
| Current     | Special styling for active session     |
| Revoking    | Optional visual feedback on revoke     |

---

## 🎨 Variants

- With or without location
- Inline icon for trusted device
- Highlight current session

---

## 🧪 Test Strategy

- Test rendering with metadata and icons
- Validate `onRevoke` click callback
- Test dynamic styles and current session badge
- TDD: test cases before styling and logic

---

## 🔌 Integration Usage

Used in:
- `ActiveSessionsScreen`
- `SecurityDashboard`
