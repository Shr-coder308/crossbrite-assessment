# Assessment Note

## 1. Schema Design and Normalization

The schema separates users, sessions, parent-child relationships, and evaluations into dedicated tables. Users store identity, authentication, and role information, while sessions reference the teacher who owns them through a foreign key. Evaluations reference both a session and a student, which avoids duplicating session or user information.

The parent-child relationship is represented separately using the `parent_children` table. This keeps the relationship normalized and allows a parent to have multiple children and a child to be associated with a parent without duplicating user records. Foreign keys also provide clear ownership boundaries between related records.

This design favors normalization and data consistency over denormalizing frequently accessed information. For a small assessment service, additional joins are acceptable and make updates safer because user information is stored in one place. In a larger production system, selected read-heavy paths could be optimized with indexes, caching, or carefully chosen denormalized read models without changing the source-of-truth schema.

## 2. RBAC, Additional Roles, and Organizations

The current implementation uses a role field on the user and dependency-based authorization for admin, teacher, parent, and student access. This is sufficient for the current scope, but a larger platform should avoid hard-coding every role directly into application logic.

To support a fourth role or more flexible permissions, roles and permissions could be moved into separate tables such as `roles`, `permissions`, and `role_permissions`. User-role assignments could then be represented through a relationship table. This would allow new roles to be introduced without changing the database schema or duplicating authorization code.

For nested organizations, I would introduce `organizations` and an organization hierarchy using a self-referencing parent organization ID. Users could belong to organizations through an `organization_memberships` table containing the user's organization, role, and membership status. Authorization would then check both the user's permissions and the organization scope of the requested resource. This would provide tenant isolation and support organization-level administrators.

## 3. Production Safety Gaps

The assessment uses environment-based configuration and Alembic migrations, but production deployment would require additional controls. Secrets such as the JWT signing key and database credentials should come from a managed secret store rather than source code or committed environment files. The JWT implementation should also use a strong rotated secret or asymmetric signing keys with appropriate key rotation.

Production would additionally require HTTPS, secure authentication flows, rate limiting, request validation, structured logging, monitoring, health checks, database connection pooling, and centralized error handling. Database migrations should be reviewed and applied through a controlled deployment process with backups and rollback procedures.

The Redis evaluation queue would also need a real worker, retry handling, job idempotency, dead-letter handling, and monitoring. Finally, authorization should be covered by comprehensive integration tests to prevent cross-user or cross-organization data access.