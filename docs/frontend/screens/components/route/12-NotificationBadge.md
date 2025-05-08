# 🔔 NotificationBadge

## 📋 Description

The `NotificationBadge` component displays a numeric or dot-style badge in the UI, typically next to a bell icon, representing the number of unread notifications. It can be used in navigation bars or buttons to increase visibility of user alerts.

---

## 🧩 Props

```ts
interface NotificationBadgeProps {
  count: number;
  max?: number;
  showDot?: boolean;
}
```

---

## 🎯 States Supported

| State     | Description                           |
|-----------|---------------------------------------|
| Counted   | Displays number (e.g., 3)             |
| Maxed     | Displays “max+” if count exceeds max  |
| Dot       | Renders small dot when `showDot=true` |

---

## 🎨 Variants

- Dot-only style
- Count with max limit (e.g., "99+")
- Color and size themes

---

## 🧪 Test Strategy

- Render count with and without `max`
- Render dot-only mode
- Validate number formatting and transitions
- Accessibility: `aria-label` for screen readers
- TDD: write interaction and visual state tests prior to implementation

---

## 🔌 Integration Usage

Used in:
- `NavigationHeader`
- `NotificationButton`
