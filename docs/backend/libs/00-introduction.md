

# 🧱 Library Design Guidelines

This section outlines the design principles and criteria for implementing backend libraries that support the system. These libraries will be consumed by the apps, and must adhere to well-defined engineering standards to ensure consistency, testability, and maintainability.

---

## ✅ Design Criteria

1. **Good Practices**
   - Follow SOLID principles.
   - Prefer composition over inheritance.
   - Use dependency inversion for external services.

2. **Isolated Layers with Single Responsibility**
   - Each library should encapsulate only one concern:
     - e.g., `jwt_signer`, `email_sender`, `twilio_sms_adapter`.
   - No shared state or implicit coupling across libraries.

3. **Well-defined Interfaces**
   - Expose clear contracts via abstract base classes or protocols.
   - Facilitate mocking and swapping in tests or alternate implementations.

4. **Test Coverage**
   - All libraries must include:
     - Unit tests for core logic.
     - Integration tests that connect to real external services (disabled by default).
   - Tests must be isolated from application logic and run independently.

5. **Configurability**
   - External integrations must rely on injected configurations.
   - Do not access `os.environ` directly inside the library; let the application layer handle environment variables.
   - If an environment variable is required, document it clearly in a separate section (e.g., `env.md`), describing:
     - Name
     - Purpose
     - Required or optional
     - Default values (if any)

---

## 🤖 LLM Implementation Instructions

When generating or editing library code:

- Always separate logic into core methods and adapters.
- Respect the principle of single responsibility at the module level.
- Avoid including API-layer logic or Django dependencies inside libraries.
- Provide at least one example usage if creating a new module.
- Default test files should include both `unit/` and `integration/` folders.
- Integration tests must check for a flag like `ENABLE_EXTERNAL_TESTS` to run.
- Use `@dataclass` or config objects for injected settings instead of relying on global state.
- Simplify usage through clear façades (e.g., `EmailSender.send(...)` or `JWTSigner.sign(payload)`).
- Provide example façades that abstract away internal structure while retaining composability.

This ensures that all libraries remain clean, composable, and usable across multiple apps with consistent behavior.

---
