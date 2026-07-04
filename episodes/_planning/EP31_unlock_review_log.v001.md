# EP31 `review_log.v001` — 台本3パスレビュー記録（DESIGN §10a）

**Subject:** `EP31_unlock_script.annotated.v001.json` / `script.en.v001.md`（~1,760語）
**Reviewer:** Claude（左工程）  ·  **Date:** 2026-07-05  ·  **Result:** 3パス通過（v001 は script_verified 相当）
**根拠:** `PD_ONE_PASS_PRODUCTION_SPEC.v2.md` rows 15/16、DESIGN §10a、`fact_recheck.v001`（MYTHS/GUARDRAILS）。

## Pass 1 — 事実 / 因果（R2）
- 全法律主張が `fact_recheck` の FR ラベルに対応（各 span の `claim_ids`）。判例名・裁判所・年は逐語ロック済（Valdez 上告不受理2024/6/24・Smith 673 F. Supp. 3d 381 を一次確認）。
- **MYTHS チェック（全て回避を確認）**：
  - ❌「最高裁が決めた」→ 本文「the Supreme Court keeps refusing to answer」「It has never decided」で**未判断**を明示。✓
  - ❌「暗証番号は常に守られる」→「a passcode **may** be protected」「**many courts**」「**Not everywhere. Not guaranteed.**」✓
  - ❌「生体は絶対守られない」→ Payne(許可) と Brown(禁止) を**両方**提示し「**opposite answer**」。✓
  - ❌ 捜索(Riley)と強制解除(第5)の混同 → 「A warrant lets them LOOK … a completely different question … the Fifth」で明確分離。✓
- **GUARDRAILS**：被告の犯罪内容は全カット（"a man"/"officers took a man's phone" 止め）。二人称"you"と法理のみ。Payne は 9th Cir. の一判決として提示し全国ルール化しない。✓
- 判定：**PASS**（捏造ゼロ・断定は事実のみ）。

## Pass 2 — ドラマ / クラフト（row15）
- コールドオープンの問い（開けさせられるのか／なぜ顔と番号で違うのか）→ 三幕の上げ（人生＝スマホ → 心 vs 体 → 割れる国と沈黙 → 未決の一線）→ フック回収、が通っている。✓
- **「普通の情報提供（法解説）」回避**：全法理を"あなたの車内"の場面＋**金庫/鍵**の比喩＋**割れる地図**＋**閉じる扉**で"見せて"進行。Wikipedia調・箇条書き調なし。✓
- **要注意点（motion パスへ申し送り）**：`SPN-0018`（foregone conclusion の核心・~31s）が唯一"講義"に寄る危険区間。**フォーク型キネティック図＋"your privacy stands or falls"の緊張**で必ず動かす（静止解説にしない）。row8 motion 実装時に最優先で作り込む。
- 判定：**PASS**（1箇所を motion で救済する条件付き）。

## Pass 3 — リテンション / 字幕（row16）
- **再フック**：`SPN-0005`(ACT I転換)／`SPN-0014`(ACT II ボタン"Except it wasn't that simple")／`SPN-0020`(ACT III ボタン"patchwork")＝**~2.5分ごと**。✓
- **オープンループ**：「開けさせられるのか／最後に守られるものは何か」を全編保持→ACT IVで回収。ACT II末で明示的に開く。✓
- **平坦区間**：20秒超の無変化な説明なし（唯一の長尺 SPN-0018 は Pass2 の申し送りで担保）。✓
- **語数**：~1,760語 @~173wpm ≈ 610s（+音楽ビートで ~700–710s、band 690–750 内）。✓
- **息継ぎ字幕**：短文中心で1息継ぎ=1cueに割りやすい。長文（SPN-0018）は複数cueに自然分割可。✓
- 判定：**PASS**。

## 修正（本レビューで実施）
- 章参照の不整合を修正：`act3` の存在しない `SPN-0021` を除去、CTA を独立 `ending` 章へ（`qc_status: pass1_2_3_done`）。

## 申し送り（次工程 = Claude 組み立て）
1. ElevenLabs マスター生成（`VOICE_ID=nPczCjzI2devNBz1zQrb`）→ 強制アライメントで**息継ぎ単位字幕**。※外部課金＝実行はオーナー承認/予算確認後。
2. Codex へ `ai_prompts.v001` の40枚を発注（≥3840・匿名・実機ロゴ/OS UIなし）。
3. `shotlist.v001` に従い `CaseFilm.tsx`＋`data/unlock_film.json` で組み立て（`SPN-0018` の motion 最優先）。
4. `check_final_acceptance.py 31 --json` → exit0 → 目視で失敗1〜9＋MYTHS点検 → オーナーゲート。
