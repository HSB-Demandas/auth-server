
## 4. Tenant-Specific Admin UI Panel

- Realm admins should manage users/roles/apps in isolation.
- Django Admin is global; requires override or separate admin dashboard.
- Suggested app: `apps.dashboard` or extend existing views with tenant scope.

---

## 5. Password Policy Enforcement

- Enforce complexity, history, expiration, and rotation per realm.
- Optional: per-role policies.
- Suggested app/extension: Extend `apps.users` or add `apps.policies`.
