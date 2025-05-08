# 🛎 NotificationFeed

## 📋 Description

The `NotificationFeed` component displays a list of in-app notifications for the current user. Each entry contains a title, message, optional timestamp, and an unread indicator. Notifications can be marked as read and may link to related actions or content.

---

## 🧩 Props

```ts
interface NotificationFeedProps {
  notifications: {
    id: string;
    title: string;
    message: string;
    timestamp: string;
    unread: boolean;
    actionLabel?: string;
    onAction?: () => void;
  }[];
  onMarkRead?: (id: string) => void;
}
```

---

## 🎯 States Supported

| State      | Description                            |
|------------|----------------------------------------|
| Default    | Renders full list                      |
| Empty      | No notifications message               |
| Actionable | Includes call-to-action buttons        |

---

## 🎨 Variants

- Scrollable drawer or inline panel
- List view or card layout
- Option to filter unread

---

## 🧪 Test Strategy

- Render list and handle empty state
- Trigger action and mark-as-read callbacks
- Accessibility: list role and item semantics
- TDD: define notification interaction coverage before build

---

## 🔌 Integration Usage

Used in:
- `NotificationsScreen`
- `NotificationPanel`
