

# 📊 Metrics & Observability App — `apps.metrics`

## 📌 Purpose

This app collects internal metrics to support observability across authentication, authorization, and user activity. It provides structured insights to system operators and realm administrators for monitoring usage patterns, diagnosing failures, and enforcing security policies.

---

## 📈 Metric Types

| Metric Name                  | Description                                        |
|------------------------------|----------------------------------------------------|
| `login_success_total`        | Number of successful login attempts                |
| `login_failure_total`        | Number of failed login attempts                    |
| `registration_total`         | Number of completed user registrations             |
| `role_assignments_total`     | Role assignments performed                         |
| `mfa_challenge_total`        | Number of MFA challenges triggered                 |
| `user_consent_granted_total`| Count of user consents granted                     |
| `webhook_delivery_success`   | Successful webhook deliveries                      |
| `webhook_delivery_failure`   | Failed webhook deliveries                          |

---

## 🔍 Data Collection Strategy

- Middleware and signals collect data during request or event flow.
- Metrics may be stored in:
  - Prometheus-compatible endpoint
  - Internal log aggregator
  - Cached counters or external time-series DB (optional)

---

## 🌐 API Endpoints (Optional)

| Method | URL                  | Description                             |
|--------|----------------------|-----------------------------------------|
| GET    | `/metrics/`          | Prometheus-compatible metrics endpoint  |

---

## 🛡️ Access Control

- The metrics endpoint is secured and accessible only to internal services or authenticated admins/operators.
- Optional: expose scoped metrics per realm with query filters.

---

## ✅ TDD Strategy

- Simulate login, registration, and consent actions
- Confirm metric counters are incremented appropriately
- Validate access control for metrics endpoint

---

## 🔧 Settings

| Setting                            | Description                                   |
|------------------------------------|-----------------------------------------------|
| `METRICS_ENABLED`                  | Global flag to enable/disable metrics         |
| `METRICS_EXPORT_PROMETHEUS`        | Toggle Prometheus endpoint export             |
| `METRICS_STORAGE_BACKEND`          | Backend used (e.g., `memory`, `prometheus`)   |

---

## 🤖 LLM Implementation Guidelines

- Metrics must be incremented via signal listeners or explicit calls
- Avoid business logic coupling — metrics are side effects
- Decorators can wrap API or service methods to count usage
