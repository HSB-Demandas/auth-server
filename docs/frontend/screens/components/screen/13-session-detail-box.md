

# 🧾 SessionDetailBox

## 📋 Description

The `SessionDetailBox` component displays metadata about an active or historical user session. This includes device, location, last seen timestamp, and session origin. It may include revoke actions and labels to highlight the current session or unrecognized sessions.

---

## 🧩 Props

```ts
interface SessionDetailBoxProps {
  sessionId: string;
  device: string;
  ipAddress?: string;
  location?: string;
  lastSeen: string;
  isCurrent?: boolean;
  isSuspicious?: boolean;
  onRevoke?: () => void;
}
```

---

## 🎯 States Supported

| State         | Description                                  |
|---------------|----------------------------------------------|
| Default       | Shows session details and optional actions   |
| Current       | Tagged or highlighted visually               |
| Suspicious    | May display warning styling or badge         |
| Revocable     | Shows revoke button if `onRevoke` is passed  |

---

## 🎨 Variants

- With or without revoke button
- Current session with subtle highlight
- Suspicious sessions with red alert UI

---

## 🧪 Test Strategy

- Renders full metadata with and without optional props
- Calls `onRevoke` when button is clicked
- Tests for conditional UI based on `isCurrent`, `isSuspicious`
- Accessibility: proper semantic and readable structure
- TDD: define tests for all visual + behavior combinations before coding

---

## 🔌 Integration Usage

Used in:
- `ActiveSessionsScreen`
- `SessionManagementCard`
