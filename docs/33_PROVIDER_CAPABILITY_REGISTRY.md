# 33 — Provider Capability Registry

## 1. 目的

外部サービスは仕様、料金、モデル、利用規約、制限が変わる。コードに固定的な前提を書かず、provider capability registryで管理する。

## 2. Provider record

- provider_id
- service_type
- official_name
- adapter_version
- verified_at
- verified_by
- terms_verified_at
- commercial_use_status
- API availability
- authentication type
- rate limits
- concurrency limits
- input limits
- output formats
- idempotency support
- async/polling behavior
- webhook support
- cost model
- data retention
- training/data-use setting
- regional constraints
- known failure modes
- fallback providers
- disabled reasons

## 3. Capability discovery

アプリ起動時に毎回外部へ問い合わせる必要はない。

- scheduled verification
- manual override
- cached capability snapshot
- adapter compatibility check
- stale-warning threshold

## 4. Suno handling

Suno-origin audio is treated as an ingested asset unless a currently supported and permitted official integration is explicitly verified.

Do not build the core pipeline around browser-coordinate automation or reverse-engineered endpoints.

Ingestion records:
- creation account/plan
- creation date
- prompt
- downloaded file hash
- commercial-use evidence
- rights note
- model/version if known
- track metadata

## 5. ElevenLabs handling

Adapter separates:
- draft TTS
- master TTS
- voice profile
- pronunciation dictionary
- request/character usage
- streaming versus file generation
- retry and output validation

## 6. YouTube handling

Separate scopes and credentials:
- analytics read
- private upload
- metadata update
- public scheduling

Capability registry records audit/private-mode restrictions and quota assumptions. Preflight verifies the actual account/project state before writes.

## 7. DaVinci handling

Resolve capabilities vary by version and local developer documentation. Adapter performs local capability probing and supports fallbacks:
- native scripting
- timeline interchange
- generated project template
- operator checklist

## 8. SDXL/local generation

Registry includes:
- checkpoint
- VAE
- LoRA
- ControlNet
- workflow version
- required VRAM
- deterministic seed behavior
- license
- intended visual modes
- known failure patterns

## 9. Provider deprecation

When provider/model is deprecated:
- mark new requests disabled
- list affected profiles
- retain past provenance
- test replacement on golden set
- migrate configuration
- do not rewrite historical metadata
