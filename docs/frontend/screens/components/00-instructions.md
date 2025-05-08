


# 🧱 Component Documentation & Implementation Guidelines

This document defines the instructions and standards for implementing and documenting UI components in the project. These guidelines apply to both atomic and macro components.

---

## ✅ General Principles

- All components **must be reusable** and avoid tight coupling with specific screens or flows.
- Components **must not contain mocked data** inside their implementation.
- Components **must be testable** via unit tests and storybook if applicable.
- Components must follow **Next.js and React best practices**, including server/client distinction, hooks usage, file-based organization, and accessibility.
- Use **ShadCN UI** components when available; only build custom components when functionality or design requires it.

---

## 🔁 Component Structure

Each component should follow a consistent structure:

```
/components/
  /<ComponentName>/
    index.tsx            # Main component logic
    types.ts             # Props and types (if necessary)
    hooks.ts             # Custom logic (optional)
    styles.css|ts        # Scoped styles (if needed)
    tests/
      index.test.tsx     # Unit tests
    stories/
      index.stories.tsx  # Storybook stories (if used)
```

---

## 🧪 Test Strategy

Every component must be tested using:

- **Jest** and **React Testing Library** for behavior and DOM rendering
- Edge cases and empty state validation
- Prop validation and conditional rendering paths
- Accessibility compliance (e.g., focus, ARIA labels)
- User interaction: clicks, input, keyboard navigation

> 🔍 Components should not depend on real backend data. Use dependency injection or mock interfaces passed via props.

> **We follow a TDD (Test-Driven Development) approach** — tests must be written **before** the implementation of the component to guide development and ensure behavior is fully defined up front.

---

## 🧩 Component Types

| Type            | Description                                      |
|------------------|--------------------------------------------------|
| Atomic Components | UI-only elements (e.g. input, badge, button)     |
| Composite Components | Multiple atomic components + business logic     |
| Route Components     | Entry components mounted by a route             |
| Utility Components   | Helpers, renderers, or formatting functions    |

---

## 🧭 Naming & Organization

- Use PascalCase for components (e.g. `RegisterForm`, `VerifyCodeInput`)
- Components related to a macro component must live together in folders
- Maintain separation of concerns: UI in JSX, logic in hooks or handlers

---

## 📄 Component Documentation

Each component must have a markdown-based reference stored in `/docs/components/<ComponentName>.md` containing:

- Description and purpose
- Props and types
- States supported
- Variants (if any)
- Testing strategy
- Integration usage
