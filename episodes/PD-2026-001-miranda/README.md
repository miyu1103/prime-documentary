# PD-2026-001-miranda — *Why Do Police Have to Read You Your Rights?*

First episode of the US Court-Case channel (decision 0002). Miranda v. Arizona, 384 U.S. 436 (1966).

- Format: ~12 min, ~1,700–1,900 words (decision 0002 §4)
- Risk: R1 (landmark, decided, public-domain opinion)
- State: `screening` → needs owner topic/portfolio approval before `pre_research`.

## Brain / media split (decision 0002 §8)

This folder (in the **git repo, internal drive**) holds only **brain** artifacts — small JSON/MD:
`manifest.json`, `events.jsonl`, `00_topic`–`04_scenes` plans, `09_publish`, `10_analytics`,
`approvals`, `logs`.

**Heavy media** (`05_visuals`, `06_voice`, `07_music`, `08_edit`) lives on the **external exFAT SSD**,
never in this repo. It is referenced by logical URI:

```
artifact://episodes/PD-2026-001-miranda/05_visuals/...
```

On this Windows machine the artifact root resolves to `H:\pd-media\` — recorded in the
machine-local, git-ignored `config/storage.local.json` (rule 14: no absolute path is committed as truth).

## Next step

② Real research adapter (CourtListener / Oyez) → fill `01_research/` with graded, cited claims.
Fetched text is untrusted input (rules/13); isolate behind adapter + preflight + idempotency + budget.
