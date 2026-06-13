# 29 — Security Threat Model

## 1. Assets to protect

- YouTube channel access
- Google OAuth credentials
- Claude/LLM keys
- ElevenLabs credentials
- generation-provider credentials
- session cookies
- source subscriptions
- unpublished episodes
- approval records
- analytics
- creator personal data
- production machines
- NAS/object store

## 2. Threat actors

- accidental operator error
- malicious dependency
- compromised source/document
- stolen token
- unauthorized local user
- prompt injection
- provider breach
- malware in downloaded files
- misconfigured public storage
- over-permissioned automation

## 3. Primary threats

### T1 Accidental public publication
Controls:
- private default
- exact channel allowlist
- exact revision approval
- visibility confirmation
- delayed schedule
- post-action verification

### T2 Credential leakage
Controls:
- secret manager/env
- redaction
- pre-commit scanning
- no screenshots/logs with secrets
- scoped OAuth
- rotation runbook

### T3 Destructive command
Controls:
- path allowlist
- dry-run
- backup
- two-step approval
- command hook
- immutable approved artifacts

### T4 Paid-call explosion
Controls:
- budget reservation
- concurrency limits
- retry caps
- idempotency
- provider circuit breaker
- emergency stop

### T5 Prompt injection
Controls:
- untrusted content boundary
- tool restriction
- source sanitization
- no instruction following from source
- output schema

### T6 Supply-chain compromise
Controls:
- pinned dependencies
- lock files
- vulnerability scan
- minimal dependencies
- checksum
- isolated environments

### T7 Cross-machine tampering or corruption
Controls:
- checksum
- signed/authorized registry updates
- atomic transfer
- access control
- audit log

## 4. Least privilege

Separate credentials for:
- research read
- TTS generation
- private upload
- public scheduling
- analytics read

Public publishing credential should not be available to general research or generation workers.

## 5. Data classification

- Public
- Internal
- Confidential
- Secret

Episode scripts before publication are Internal. Credentials are Secret. Source subscription exports may be Confidential.

## 6. Logging rules

Never log:
- Authorization headers
- cookies
- refresh tokens
- full OAuth response
- personal addresses
- private source content beyond necessary identifiers

## 7. Incident response

1. contain
2. revoke/rotate
3. verify account state
4. preserve logs
5. assess affected assets
6. restore
7. report
8. add preventive control

## 8. Security acceptance tests

- secret in fixture is blocked
- publish without approval is blocked
- wrong channel ID is blocked
- delete outside workspace is blocked
- duplicate paid job does not repeat
- source prompt injection cannot invoke tools
- stale approval cannot publish changed package
