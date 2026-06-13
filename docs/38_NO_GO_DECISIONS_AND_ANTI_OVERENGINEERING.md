# 38 — No-go Decisions and Anti-overengineering

## 1. 初期にやらない

- Kubernetes
- microservices per stage
- custom vector database before retrieval need is proven
- multi-region deployment
- fully autonomous public publishing
- custom video editor replacing DaVinci
- proprietary model training before evaluation data exists
- mass scraping without source policy
- 10,000 music tracks without coverage taxonomy
- many channels on an unstable pipeline
- complex web UI before CLI vertical slice works

## 2. Avoided abstractions

- generic “AI task” table with no domain type
- one universal JSON blob
- provider IDs inside core objects
- status strings without transition rules
- manual folder naming as database
- arbitrary retry count
- “confidence” without action threshold
- one score combining blockers and preferences

## 3. Build versus buy

Build:
- PD domain model
- claim lineage
- episode orchestration
- approval boundaries
- artifact registry
- analytics-to-scene learning

Buy/use:
- TTS
- image generation engine
- video editor
- object storage
- observability libraries
- OAuth client

## 4. Trigger for additional infrastructure

Add complexity only when measured constraints exist.

Examples：
- PostgreSQL when concurrency/reliability exceeds SQLite use case
- Redis/queue when local job runner is insufficient
- web dashboard when CLI review creates measurable bottleneck
- second GPU when queue utilization justifies it
- dedicated server when node availability causes delays

## 5. Technical debt register

Every shortcut records:
- reason
- scope
- risk
- expiry/review date
- removal condition

## 6. Completion bias

Do not create placeholder modules for every future concept. Finish one vertical slice, prove it, then extend.
