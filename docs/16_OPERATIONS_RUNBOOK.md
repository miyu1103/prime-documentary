# 16 — Operations Runbook

## 1. Daily Startup

- orchestrator health
- DB health
- storage health
- disk capacity
- worker heartbeats
- GPU availability
- provider auth
- queue depth
- blocked jobs
- approval backlog
- budget
- scheduled publications
- clock synchronization

## 2. Daily Shutdown / Backup

- active job checkpoint
- DB backup
- event log flush
- manifest sync
- unfinished external requests
- render checksum
- secrets not in logs
- storage warnings
- next-day scheduled tasks

## 3. Failed Job Procedure

1. error class確認
2. side effect確認
3. input revision確認
4. provider status確認
5. retry count確認
6. budget確認
7. automatic remediation
8. retry / blocked / dead-letter
9. incident note
10. recurring failureならrule/test追加

## 4. GPU OOM

- current VRAM consumers確認
- batch size削減
- resolution profile変更
- model unload
- tiled mode
- worker concurrency削減
- lower profileでretry
- repeated OOMならgeneration profile修正

## 5. Storage Full

- 新規生成停止
- incomplete temporary files候補
- cache eviction
- raw rejected asset retention確認
- backup確認
- approved/masterは削除しない
- storage増設
- incident record

## 6. Provider Outage

- circuit open
- affected jobs blocked
- fallback provider availability
- duplicate request防止
- notification
- recovery probe
- controlled resume

## 7. Corrupt Artifact

- checksum mismatch
- source/local copy比較
- redownload
- regenerate
- dependent artifacts stale
- timeline relink
- render repeat

## 8. Wrong Fact Found Before Publish

- claim status blocked
- linked script spans stale
- scenes/assets/text/voice/package invalidation
- correction plan
- limited rebuild
- re-run fact gate

## 9. Wrong Fact Found After Publish

1. severity評価
2. public harm評価
3. correction可能性
4. title/description訂正
5. pinned correction
6. video replace/private/delete判断
7. rights/legal escalation
8. affected future videos検索
9. root cause
10. gate/test追加

## 10. Accidental Publish Risk

- authorizedなら即private
- 現在状態をcapture
- visibility再確認
- notification
- scheduled jobs停止
- credential compromise確認
- incident review
- guard/test追加

## 11. Credential Expiry

- jobをretryし続けない。
- provider auth errorとして停止。
- secret更新手順を提示。
- 更新後にread-only test。
- pending side effectsを確認してresume。

## 12. DaVinci Unavailable

- editor workerをunhealthy。
- edit queueは保持。
- 上流WIPを制限。
- Mac再起動・Resolve起動・project DB確認。
- dry-runで接続確認。
- leaseを再取得。

## 13. Wrong Asset in Timeline

- timeline clip mapping確認
- scene asset active revision確認
- stale propagation確認
- relink only affected clip
- review render affected range
- root causeがcacheならcache invalidation修正

## 14. Monthly Maintenance

- dependency updates
- provider terms verification
- pricing update
- schema migrations
- backup restore test
- golden episode regression
- dead-letter review
- cost anomalies
- unused assets
- QC false positives/negatives
- playbook review
- permissions review
- log retention

## 15. Quarterly Review

- content pillars
- autonomy level
- human review minutes
- editing bottleneck
- provider concentration risk
- storage growth
- channel performance
- rule effectiveness
- model/provider replacement opportunities
- disaster recovery test
