


---

## 🧭 User Journeys

This system supports a wide set of user journeys based on the features implemented across its apps:

| #  | Journey                                                                                      | Persona(s)             | Involved Apps                                       |
|----|----------------------------------------------------------------------------------------------|------------------------|------------------------------------------------------|
| 1  | [User Registration (Email)](01-journey_user-registration-email.md)                           | Anonymous              | `apps.users`, `apps.compliance`                     |
| 2  | [User Registration (Social Provider)](02-journey_user-registration-social.md)                | Anonymous              | `apps.auth`, `apps.users`, `apps.applications`      |
| 3  | Self-Registration Flow Check (App Config)                                                    | Anonymous              | `apps.applications`, `apps.users`                   |
| 4  | [Login (Email/Password)](03-journey_login-email-pass.md)                                     | Registered User        | `apps.auth`, `apps.security_events`                 |
| 5  | [Login (Social)](04-journey_login-social.md)                                                 | Registered User        | `apps.auth`, `apps.security_events`                 |
| 6  | [Email Verification Flow](05-journey_email-verification.md)                                  | Registered User        | `apps.users`, `apps.auth`, `apps.compliance`        |
| 7  | [Phone Verification Flow (SMS)](06-journey_phone-verification.md)                            | Registered User        | `apps.users`, `apps.auth`                           |
| 8  | [MFA Setup (TOTP or SMS)](07-journey_mfa-setup.md)                                           | Registered User        | `apps.users`, `apps.auth`                           |
| 9  | [MFA Login Challenge Flow](08-journey_mfa-login-challenge.md)                                | Registered User        | `apps.auth`, `apps.security_events`                 |
| 10 | [Suspicious Login Notification + Device Confirmation](09-journey_login-suspicious-device.md) | Registered User        | `apps.security_events`, `apps.notifications`        |
| 11 | [Accept Terms and Privacy Policy](10-journey_terms-accept.md)                                | Anonymous / Registered | `apps.compliance`, `apps.users`                     |
| 12 | Granular Consent Management (Marketing, Data Use)                                            | Registered User        | `apps.compliance`                                   |
| 13 | Edit Profile (Avatar, Phone, Name)                                                           | Registered User        | `apps.users`                                        |
| 14 | [Link/Unlink Social or Auth Providers](12-journey_link-unlink-social-provider.md)            | Registered User        | `apps.users`                                        |
| 15 | [Change Password](13-journey_change-password.md)                                             | Registered User        | `apps.users`                                        |
| 16 | [Forgot Password / Reset Password Flow](14-journey_forgot-password.md)                       | Anonymous / Registered | `apps.users`, `apps.auth`                           |
| 17 | [View and Revoke Active Sessions](16-journey_view-and-revoke-active-sessions.md)             | Registered User        | `apps.auth`                                         |
| 18 | [Export Personal Data (LGPD/GDPR)](17-journey_export-personal-data.md)                       | Registered User        | `apps.users`, `apps.permissions`, `apps.audit`      |
| 19 | [View My Devices (Trusted Login Sources)](18-journey_view-my-devices.md)                     | Registered User        | `apps.security_events`                              |
| 20 | Revoke Device / Mark Unrecognized                                                            | Registered User        | `apps.security_events`                              |
| 21 | [View In-App Notifications](19-journey_view-inapp-notifications.md)                          | Registered User        | `apps.notifications`                                |
| 22 | Admin: Create Application                                                                    | Realm Admin            | `apps.applications`, `apps.realms`                  |
| 23 | Admin: Configure Providers for App                                                           | Realm Admin            | `apps.applications`                                 |
| 24 | Admin: Manage Terms and Privacy Policy                                                       | Realm Admin            | `apps.compliance`                                   |
| 25 | Admin: Manage Roles and Permissions Matrix                                                   | Realm Admin            | `apps.permissions`                                  |
| 26 | Admin: Assign Roles to Users                                                                 | Realm Admin            | `apps.permissions`, `apps.users`                    |
| 27 | Admin: Manage Webhook Subscriptions                                                          | Realm Admin            | `apps.webhooks`                                     |
| 28 | Admin: View Webhook Deliveries & Logs                                                        | Realm Admin            | `apps.webhooks`                                     |
| 29 | Admin: View Metrics Dashboard                                                                | Realm Admin / Operator | `apps.metrics`                                      |
| 30 | Admin: View Audit Log for Realm Activities                                                   | Realm Admin / Operator | `apps.audit`                                        |
| 31 | Admin: Set Rate Limiting Rules (Config)                                                      | Operator               | `django_hsb_ratelimit`, `apps.auth`, `apps.users`   |
| 32 | JWT Token Introspection API Usage                                                            | External Integrator    | `apps.auth`                                         |
| 33 | Admin: Manage Realm-Wide Settings (e.g. MFA, policies)                                       | Realm Admin            | `apps.realms`, `apps.compliance`, `apps.auth`       |
