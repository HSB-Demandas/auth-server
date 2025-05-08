# 🔗 LinkedProvidersManager

## 📋 Description

The `LinkedProvidersManager` component displays and manages the list of external identity providers (e.g. Google, GitHub) linked to a user account. It provides options to link new providers and unlink existing ones with appropriate validation and feedback.

---

## 🧩 Props

```ts
interface LinkedProvidersManagerProps {
  linked: string[];
  available: string[];
  onLink: (provider: string) => void;
  onUnlink: (provider: string) => void;
  loadingProvider?: string;
}
```

---

## 🎯 States Supported

| State     | Description                          |
|-----------|--------------------------------------|
| Default   | List of linked and available shown   |
| Loading   | One provider is actively linking     |
| Empty     | No linked providers                  |

---

## 🎨 Variants

- Horizontal card or vertical list
- Inline icons per provider
- Confirmation modal on unlink

---

## 🧪 Test Strategy

- Render list with linked and available providers
- Trigger `onLink` and `onUnlink` actions
- Simulate loading state
- Accessibility: buttons labeled per provider
- TDD: write test cases for visual and behavior states

---

## 🔌 Integration Usage

Used in:
- `SettingsProvidersScreen`
- `AccountLinkingSection`
