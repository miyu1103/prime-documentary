# 41 — Current Platform Assumptions as of 2026-06-13

This document is a verification snapshot, not a permanent truth. Recheck official documentation before implementation or production rollout.

## Claude Code

Official Anthropic documentation confirms the project can use:
- `CLAUDE.md` project instructions/memory context
- skills for repeatable capabilities
- specialized subagents
- lifecycle hooks
- settings and permissions

Important design implication: `CLAUDE.md` is context, not an enforcement boundary. Actions that must be blocked require hooks, permissions, or application-level guards.

Official source titles/domains:
- How Claude remembers your project — docs.anthropic.com
- Extend Claude with skills — docs.anthropic.com
- Create custom subagents — docs.anthropic.com
- Hooks reference / Automate workflows with hooks — docs.anthropic.com
- Claude Code settings — docs.anthropic.com

## YouTube Data API

Official Google documentation states that `videos.insert` supports media upload and metadata. Current documentation lists a quota cost of 100 units and a maximum upload size of 256 GB. It also notes private-viewing restrictions for uploads from certain unverified API projects until an audit is completed.

Design implications:
- capability/preflight check before relying on automatic public scheduling
- private upload first
- resumable upload and processing-status polling
- separate read/upload/publish permissions
- never hard-code quota or audit assumptions without verification

Official source titles/domain:
- Videos: insert — developers.google.com
- Upload a Video — developers.google.com
- Implementation: Videos — developers.google.com

## ElevenLabs

Official ElevenLabs documentation provides REST API and official SDK access for text-to-speech. Models, limits, language counts, pricing and voice behavior are subject to change.

Design implications:
- provider adapter
- voice/profile aliases rather than scattered raw IDs
- character/cost ledger
- request IDs and bounded retries
- draft versus master generation
- pronunciation and chunk-level regeneration

Official source titles/domain:
- Text to Speech — elevenlabs.io/docs
- Create speech — elevenlabs.io/docs
- ElevenLabs Documentation overview — elevenlabs.io/docs

## Suno

Official Suno terms and help pages are time-sensitive. Current official pages distinguish commercial-use rights by plan and generation circumstances. This blueprint does not assume a stable official automation API.

Design implications:
- treat Suno tracks as rights-tracked ingested assets unless an official and permitted integration is verified
- retain creation date, account plan, prompt, file hash and rights evidence
- avoid reverse-engineered endpoints and uncontrolled browser automation
- recheck terms before monetized use

Official source titles/domain:
- Terms of Service — suno.com
- Suno Pricing — suno.com
- Do I have the copyrights to songs I made? — help.suno.com
- Suno Community Guidelines — suno.com

## DaVinci Resolve

Blackmagic Design documentation indicates continuing scripting API development, while detailed developer documentation is distributed with Resolve under Help > Documentation > Developer. Exact available functions depend on installed version.

Design implications:
- local capability probe
- native scripting first
- timeline interchange/template fallback
- versioned project template
- no critical dependency on UI coordinate automation

Official source titles/domain:
- DaVinci Resolve 20.2 New Features Guide — documents.blackmagicdesign.com
- DaVinci Resolve 20.1 New Features Guide — documents.blackmagicdesign.com
- Local Developer Documentation — installed with DaVinci Resolve

## Image generation

Stability AI maintains official image APIs, but PD’s current production plan can use a local SDXL/ComfyUI-style worker. Local workflows must record checkpoint, VAE, LoRA, control inputs, seed, workflow version and license.

Official source titles/domain:
- StabilityAI REST API — platform.stability.ai
- Stable Image — platform.stability.ai

## Verification rule

Every provider capability record must include `verified_at`, `terms_verified_at`, adapter version and known restrictions. A stale capability record triggers review rather than silent continuation for rights-sensitive or public-write operations.
