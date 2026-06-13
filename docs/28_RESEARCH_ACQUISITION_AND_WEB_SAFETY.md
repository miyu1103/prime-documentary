# 28 — Research Acquisition and Web Safety

## 1. 原則

Web取得は、情報収集であると同時にセキュリティ境界。

Webページ、PDF、字幕、コメント、検索結果、メール、ドキュメント内の命令はすべてuntrusted dataとして扱う。

## 2. Acquisition pipeline

1. query plan
2. source discovery
3. domain/type classification
4. fetch
5. content extraction
6. integrity metadata
7. chunking
8. citation location
9. claim candidate extraction
10. independent verification

## 3. Query plan

- central question
- subquestions
- primary-source queries
- counterargument queries
- chronology queries
- numerical verification queries
- current-status queries
- visual evidence queries
- rights queries

検索数を増やすことを調査品質とみなさない。

## 4. Source deduplication

転載記事を独立ソースと数えない。

- canonical URL
- content hash
- quoted-source tracing
- publication chain
- syndication detection

## 5. PDF handling

- document title/version/date
- page count
- exact page location
- table/figure references
- scan/OCR confidence
- revision status
- appendices

表や図は本文テキストだけで判断しない。必要ならページ画像を確認する。

## 6. Dynamic/current facts

- accessed_at
- effective_date
- publication_date
- last_updated
- expected volatility
- recheck_before_publish

公開直前に変わり得る事実は再確認ジョブを作る。

## 7. Prompt injection defense

- source content never changes system policy
- embedded instructions ignored
- no shell/tool execution from source text
- no credential entry requested by content
- allowed domains and content types
- sandboxed parsing
- file-size limits
- malware scanning where relevant
- no automatic form submission

## 8. Evidence packets

writerへWeb全文を渡さない。

渡す：
- claim candidate
- exact evidence excerpt or structured fact
- source ID
- location
- confidence
- caveat
- counterevidence

これにより、writerが未確認情報を混ぜる範囲を減らす。

## 9. Citation durability

- stable identifier where possible
- archived reference metadata where legally permitted
- retrieval timestamp
- document version
- page/section
- content hash

URLだけに依存しない。

## 10. Comments and social data

需要・疑問・反応の発見には使えるが、事実根拠としては扱わない。個人情報を不必要に保存しない。

## 11. Access and rights

- robots/access policy
- paywall and subscription terms
- redistribution restrictions
- quotation limits
- local caching policy
- deletion/retention

取得できることと再利用できることを分ける。

## 12. Research completion

資料数ではなく、以下で判断：
- central claim support
- counterevidence coverage
- unknowns bounded
- source independence
- timeline resolved
- numerical claims normalized
- current facts scheduled for recheck
