

# 📝 Journey: View and Interact with In-App Notifications

## 📌 Description

This journey allows a registered user to view, mark as read, or interact with in-app notifications delivered to them. Notifications may contain contextual messages, action links, and custom icons. This improves engagement and visibility of security events, account updates, or administrative messages.

---

## 👥 Personas

- Registered User

---

## 🧩 Involved Apps

- `apps.notifications`
- `apps.security_events`
- `apps.audit`

---

## 🧭 UX Flow

### 📺 Screen: Notification Center

- **Route**: `/notifications`
- **Purpose**: Display all unread and historical in-app notifications
- **Inputs**:
  - List of notification cards (title, content, icon, timestamp)
  - Buttons: Mark as Read, Dismiss, View More
- **Expected Behavior**:
  - Unread notifications shown prominently
  - Allow individual or bulk "mark as read"
  - Action link opens appropriate route (if configured)
- **Backend Endpoints**:
  - `GET /api/notifications/`
  - `POST /api/notifications/<id>/read/`
  - `DELETE /api/notifications/<id>/` (optional)

---

### 📺 Inline Widget: Notification Badge

- **Route**: UI Component (Header/Nav)
- **Purpose**: Show badge with count of unread notifications
- **Inputs**:
  - Notification icon + count
- **Expected Behavior**:
  - Poll or receive via WebSocket (if configured)
  - Redirect or open dropdown for recent activity
