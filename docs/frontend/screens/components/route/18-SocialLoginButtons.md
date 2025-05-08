# 🔗 SocialLoginButtons

## 📋 Description

The `SocialLoginButtons` component renders a list of buttons for supported social authentication providers (e.g., Google, GitHub). It initiates OAuth flows when clicked and can be reused in registration and login screens.

---

## 🧩 Props

```ts
interface SocialLoginButtonsProps {
  providers: string[];
  onClick: (provider: string) => void;
  loadingProvider?: string;
}
```

---

## 🎯 States Supported

| State     | Description                            |
|-----------|----------------------------------------|
| Default   | All buttons are clickable              |
| Loading   | One button is disabled with a spinner  |

---

## 🎨 Variants

- Horizontal or vertical list
- Icon with label or icon-only button
- Custom styling per provider

---

## 🧪 Test Strategy

- Render all available providers
- Trigger `onClick` correctly
- Show loading state for a provider
- Accessibility: button roles and alt text
- TDD: test coverage for all visual and interaction paths

---

## 🔌 Integration Usage

Used in:
- `LoginScreen`
- `SocialRegistrationForm`
