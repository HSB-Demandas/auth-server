# 🔔 NotificationItem

## 📋 Description

The `NotificationItem` component represents a single in-app notification entry in a user's feed. It may include a title, message, timestamp, icon, and optional action link or button. It supports read/unread states and lightweight interactions.

---

## 🧩 Props

```ts
interface NotificationItemProps {
  id: string;
  title: string;
  message: string;
  timestamp: string;
  unread: boolean;
  onClick?: () => void;
  icon?: React.ReactNode;
  actionLabel?: string;
  onAction?: () => void;
}
```

---

## 🎯 States Supported

| State     | Description                              |
|-----------|------------------------------------------|
| Unread    | Highlighted visually                     |
| Read      | Normal visual styling                    |
| Actionable| Contains a button or link                |

---

## 🎨 Variants

- With or without icon
- With action (e.g. “View”, “Acknowledge”)
- Dense or standard layout

---

## 🧪 Test Strategy

- Render with and without icon and actions
- Simulate `onClick` and `onAction` handlers
- State-based style testing (`unread`, `read`)
- Accessibility: roles, labels, keyboard interaction
- TDD: define visual and interactive tests before coding

---

## 🔌 Integration Usage

Used in:
- `NotificationFeed`
- `NotificationCenter`
