# EPIC-02/TASK-02F — Customers Core

**Summary**
- Add Customer model/schemas/router, secured routes, Alembic migration, and verification artifacts.

**Scope**
- Model: `customers` with unique email, timestamps.
- Routes: 
  - `GET /customers` (user)
  - `POST /customers` (admin|manager)
  - `PUT /customers/{id}` (admin|manager)
  - `DELETE /customers/{id}` (admin)
- Router wiring without double prefix.

**Migrations**
- Created table `customers`. Adjusted enum logic to avoid `userrole` re-creation conflicts.

**Security**
- Guards: `require_user`, `require_any_role("admin","manager")`, `admin` for delete.

**Verification Artifacts**
- reports/EPIC-02/TASK-02F/openapi_paths.txt
- reports/EPIC-02/TASK-02F/curl_00_unauthorized_list.txt
- reports/EPIC-02/TASK-02F/curl_01_create.txt
- reports/EPIC-02/TASK-02F/curl_02_list.txt
- reports/EPIC-02/TASK-02F/curl_03_update.txt
- reports/EPIC-02/TASK-02F/curl_04_delete.txt
- reports/EPIC-02/TASK-02F/curl_05_conflict.txt
- reports/EPIC-02/TASK-02F/curl_06_delete_by_manager_forbidden.txt
- reports/EPIC-02/TASK-02F/psql_describe_customers.txt
- reports/EPIC-02/TASK-02F/DoD_checklist.md
- reports/EPIC-02/TASK-02F/summary.md

**Notes**
- DB started first; created `eurodropship` if missing; admin seeded.
- Aligned with the deep incompatibility report’s core-entities roadmap.

**Acceptance Criteria**
- All artifacts present and readable.
- OpenAPI shows `/customers` paths.
- Unauthorized GET returns 401; duplicate email returns 409.
- Delete forbidden for non-admin roles.
