# Security Plan

## Access & Authentication
- Enforce strong passwords and MFA for admin accounts
- Role-based access control; least privilege by default

## Data Protection
- Encrypt sensitive fields at rest (DB level; KMS-managed keys if available)
- TLS 1.2+ in transit; HSTS on public endpoints
- Secrets rotation schedule and vaulting

## Backups & Recovery
- Nightly backups of Postgres and `data/02_Excel` to secure storage
- Retention: 30 days rolling; weekly replicas retained 12 weeks
- Restoration: documented runbook; quarterly restore tests

## Monitoring & Logging
- Application health checks (`/health`, `/reports/summary`)
- Centralized logs with alerts on error spikes and auth anomalies

## Secure Development
- CI checks: tests + lint; dependency scanning monthly
- Regular dependency updates and container rebuilds

## Review Cadence & Ownership
- Security owner: security@eurodropship.local
- Monthly review meeting; quarterly external review; incident postmortems
