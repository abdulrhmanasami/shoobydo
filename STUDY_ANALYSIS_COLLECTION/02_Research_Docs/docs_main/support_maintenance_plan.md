# Support & Maintenance Plan

## Post‑Launch Responsibilities
- Uptime monitoring and incident response
- Security updates (dependencies, containers), vulnerability checks
- Database maintenance (vacuum/analyze, indexing reviews)
- Backups verification and periodic restore tests
- User support: triage tickets, SLA responses, feedback loop

## Schedules
- Daily: health checks, error log scans
- Weekly: dependency review, small fixes, report KPIs
- Monthly: backup restore test, security review, capacity check
- Quarterly: policy/legal review, risk tabletop exercises, performance tests

## Points of Contact
- Ops lead: ops@eurodropship.local
- Security: security@eurodropship.local
- Support: support@eurodropship.local

## Tooling
- CI: GitHub Actions (`.github/workflows/ci.yml`)
- Monitoring: health endpoints + log aggregation
- Backup scripts: per `docs/security_plan.md` schedule
