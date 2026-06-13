# 20 — Provider Adapters and External Integrations

## 1. Adapter Principle

コアdomainはprovider固有JSONやIDへ依存しない。

```python
class ImageProvider:
    def generate(self, request, idempotency_key): ...
    def get_status(self, external_request_id): ...
    def download(self, result_ref): ...
```

## 2. Common Adapter Result

- provider
- provider_request_id
- status
- outputs
- usage
- estimated_cost
- actual_cost
- raw_metadata_ref
- retry_after
- error_class
- terms_snapshot

## 3. LLM Gateway

責務：

- model routing
- prompt version
- structured output
- retries
- token/cost logging
- fallback
- safety filters
- response hash
- caching where appropriate

タスク別routing：

- cheap model：分類、整形、lint
- strong model：thesis、複雑な構成、architecture
- independent model/pass：fact/style review

具体モデル名をdomainへ直書きしない。

## 4. SDXL Adapter

- local endpoint or process
- model/checkpoint profile
- LoRA/control references
- seed
- dimensions
- sampler/steps
- batch
- GPU selection
- timeout
- output metadata
- safety scan

## 5. ElevenLabs Adapter

- voice profile alias
- text/spoken text
- model profile
- output format
- pronunciation dictionaries
- seed where supported
- request ID
- character usage
- rate-limit handling
- partial retry

API仕様は実装時に公式文書で再確認する。

## 6. Music Provider Adapter

優先順：

1. 公式API
2. 承認済みintegration
3. 人間が生成し監視フォルダへ保存→自動ingest
4. 規約確認済みの限定UI automation

非公式APIや認証Cookie抽出を既定で使わない。

## 7. DaVinci Adapter

- connection health
- project template
- media import
- bin creation
- timeline creation
- clip placement
- marker placement
- subtitle import
- render job
- status polling
- output validation

未対応操作はimport formatまたはmanual instructionへfallback。

## 8. YouTube Publisher Adapter

- channel allowlist
- upload
- resumable status
- duplicate detection
- privacy default
- metadata
- thumbnail
- subtitles
- playlist
- schedule
- processing status
- final video ID
- analytics job registration

public化はapproval tokenが必要。

## 9. Provider Health

- auth test
- read-only test
- latency
- error rate
- quota
- pricing snapshot
- terms verification date
- circuit status

## 10. Fallback Policy

provider failure時に勝手に品質・権利の異なるproviderへ切り替えない。

fallback profileに：

- allowed task
- quality difference
- rights difference
- cost difference
- human review requirement

を持つ。
