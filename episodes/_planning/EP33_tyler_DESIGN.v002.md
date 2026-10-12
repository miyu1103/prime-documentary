# EP33（tyler）制作設計書 v002 — 3回点検 検証サインオフ層

- **binding正典（不変・invariant6）**: `EP33_tyler_DESIGN.v001.md`（本文はこちらが正典。v002はその上の検証・是正層）
- **超激重アニメ素材（別スレ制作）**: `EP33_tyler_ANIMATION_ASSETS.v001.md` / 引き継ぎ `EP33_tyler_ANIMATION_HANDOFF_PROMPT.md`
- **3回点検（corner-to-corner・実コード実測照合）**: pass別 [{'pass': 1, 'findings': 34, 'majors': 20}, {'pass': 2, 'findings': 31, 'majors': 14}, {'pass': 3, 'findings': 25, 'majors': 9}]
- **正直スコア**: 88/100 ／ **真の未解決BLOCKING**: 1件

---

## A. サインオフ監査（実ゲート実測照合の結論）

## EP33 (slug=tyler) 最終サインオフ監査 — 実ゲート実測照合の結果

正典 `episodes/_planning/EP33_tyler_DESIGN.v001.md` と実ゲート `scripts/check_final_acceptance.py`（配線）・各 `scripts/*.py`（実装）を1対1で突合。ドロップゲート引用ゼロ・水増しゼロを確認。round7サマリは概ね健全だが、**実コード実測で1件の事実誤り（過大なギャップ主張）**を発見したので是正する。

### 是正1（MAJOR・監査官修正）: BLOCKING#2の前提は事実誤り。機能語行末は既に wired hard で塞がれている
設計書 pass3 BLOCKING#2 は「機能語行末0を独立再検査する受領側ゲートが無く、`the/and/to` 終わりが全wiredゲートを素通りしうる」と主張し、`check_caption_dangle` 新設を必須ブロッキングにしている。**実コードはそうではない。** `verify_caption_sync.py`（`evaluate()`）は shipped SRT を独立に読み、`_dangling_end(cue)` で各cue最終行の機能語行末を検出→ L419 `fword_ends`、L434-436 で `problems` に積み、L442 `ok = not problems`。これは `check_final_acceptance.py:1438 check_caption_sync`（`hard: True`, L1464）として配線済み。つまり「字幕が変な所で切れる（機能語行末）」は **既に SOLID（wired・hard）**。同一 `evaluate` が median lag（`FAIL_MEDIAN_LAG=0.10`）・p90 lag・per-minute `FAIL_SEGMENT_DRIFT=0.50` も hard 判定するので「字幕が遅い」「8:45以降ドリフト（字幕）」も同じ関数で SOLID。
- 影響: `check_caption_dangle` 新設は **冗長（defense-in-depth として無害）** であり、これを未解決 BLOCKING として計上するのは誤り。設計書の「全wiredゲートを素通りしうる」文言は撤回すべき。§5.2/§6.1/§7/§12/§14 の該当記述は「既存 `verify_caption_sync._dangling_end` が受領側hard・追加 `check_caption_dangle` は任意の二重化」へ格下げ。
- ただし真の残穴は別にある（是正2）。

### 是正2（残る唯一の真の偽緑穴・要実装）: caption_sync / caption_coverage の skip 経路
`verify_caption_sync.evaluate()` は master mp3 欠落・windowed整列不能・`matched_frac < MIN_MATCHED_FRACTION(0.60)` 等で `{"skipped": True}` を返し、`check_caption_sync` はこれを `ok:True, hard:False`（L1452-1454）に落とす。**skip すると lag・drift・機能語行末の三点が同時に未検査で緑になる。** これが設計書のいう「caption skip=偽緑穴」であり、`check_caption_coverage`（未字幕chunk検出）も同型の skip を持つ。ここは wired ゲートでは閉じておらず、**設計書§13.2の『skip=偽緑穴・要実装』は正しい**。ship前の実効担保は `preflight_owner_review.py`（caption_sync を含む人間試聴 backstop）に依存する。→ 未解決 BLOCKING として1件計上（下記 unresolved_blocking=1）。

### 是正3（据置・実測で確認）: ドロップゲート引用ゼロ
`grep` 実測で `check_music_coverage` / `check_stem_loudness` / `check_motion_bbox_flow` は `scripts/` に実在するが `check_final_acceptance.py` から **0回参照**（NONE 確定）。設計書はこれらを hard 機構として一切引用せず、音は `check_sound_layers`（wired）＋音5本試聴、モーションは `check_motion_energy`（wired・`measure_motion_energy.py`）＋motion-reel に正しく差替済み。**問題なし。**

### 是正4（実測で確認・設計書の別の過小主張を訂正）: music の自動床は存在する
設計書 pass2 で一時「music保証ゲートは皆無」としていたが、pass3 MINOR#23 で `check_sound_layers` の `SOUND_PROV_MIN_MUSIC=1` により music≥1トラックが sha束縛hard床として現に enforce される旨へ訂正済み。実配線と整合。自動床が無いのは「中盤 music drop 等カバレッジ時系列の質」に限定され、そこは人間試聴 backstop。**整合。**

### 是正5（未作成の下流成果物・出荷前ブロッキング前提）: asset_selection.v001.json
`episodes/PD-2026-033-tyler/05_visuals/` は空（`find` 実測: EP006/EP032 には存在、EP033 には無い）。設計書 pass3 MAJOR#18 が正しく「画像生成前の必須成果物」として要求済み。252 still-cut の cut配置・footage突合キー・`check_footage_utilization`/`preflight_render_gate` 起動の唯一の束縛入力なので、**これが無いままの ship は不可**。設計上の指示は正しく、実装は未着手（設計段階として妥当）。

### 是正6（構造ゲートの実契約を確認）: structure_4part は5幕を false-FAIL しない
`check_structure`（L432-471）は body = hook/opening/ending 以外の非空セクション集合を要求するだけで幕数非依存。Act1–Act5 の5幕 body はそのまま受理。設計書§6.1 note#4 の記載は **実コードと一致**。

### サインオフ結論
- BLOCKING（真に未解決）: **1件** = caption skip 偽緑穴（是正2）。wired では閉じず ship前 `preflight_owner_review.py` 人間試聴が唯一の担保。設計書は既にこれを『要実装/本話ブロッキング』と正直計上しており、**新たな隠れ BLOCKING は無い**。
- MAJOR（監査官修正で解消）: BLOCKING#2 の過大ギャップ主張（是正1）→ 冗長化として無害・スコア上は減点対象。
- 実効ゲート点62/設計完全性98 の自己申告は **概ね妥当**（過小・過大の相殺）。ただし機能語行末を「要実装」に数えていた分、実効はやや過小評価だった。
- 水増し・架空機構引用・ドロップゲート引用は **検出されず**。Codex実装粒度（アンカー/語数/tc/イージング数値）は高い。

**この設計書は、是正1（BLOCKING#2の冗長化明記）と是正2（skip偽緑穴を唯一の真ブロッキングとして残置＋人間backstop必須）を反映すれば、round7でサインオフ可。** 正典が immutable（invariant6）のため本監査の是正は remediation ノート／本StructuredOutputに記録し、正典への追記は新revisionで行うこと。

---

## B. 過去失敗 × 塞ぐ実在機構 点検表

## EP33 過去失敗 × 塞ぐ実在機構 点検表（実コード実測照合済）

凡例: SOLID=`check_final_acceptance.py`に配線されhard判定/ WEAK+backstop=自動は限定的で人間試聴等が最終担保/ 要実装=未コード。すべてファイル名は実在を確認済。ドロップゲート（music_coverage/stem_loudness/motion_bbox_flow）は引用していない。

| # | 過去失敗 | 塞ぐ実在機構（ファイル名・関数） | 設計書§ | 状態 |
|---|---|---|---|---|
| 1 | 字幕がナレと不一致 | `check_final_acceptance.py:check_caption_narration_match`(L410, token match≥`CAPTION_MATCH_MIN`) ＋ `verify_caption_coverage.py` | §5.2/§6.1 | **SOLID** |
| 2 | 字幕が遅い | `verify_caption_sync.py:evaluate`(`FAIL_MEDIAN_LAG=0.10`/p90/LATE_TOL) ←`check_caption_sync`(hard,L1438) | §5.2/§6.1 | **SOLID** |
| 3 | 字幕が変な所で切れる(機能語行末) | `verify_caption_sync.py:_dangling_end`→`function_word_line_ends`(L419/434, hard) ←`check_caption_sync`。**既にwired**（設計書のBLOCKING#2「素通り」は誤り／`check_caption_dangle`は冗長二重化） | §5.2/§6.1(是正1) | **SOLID**（+任意二重化） |
| 4 | 8:45以降ドリフト | `verify_caption_sync.py` per-minute `FAIL_SEGMENT_DRIFT=0.50`(hard)。字幕以外のドリフトは`check_longform_drift`が**要実装** | §13.2 | **SOLID(字幕)** / 要実装(音映像) |
| 5 | 字幕が飛ぶ(未字幕chunk) | `verify_caption_coverage.py`(全chunk字幕化,wired)。**skip経路で偽緑化**→skip-hardening要実装 | §5.6/§13.2 | **WEAK+backstop**(`preflight_owner_review.py`) |
| 6 | DL素材が1つも使われない | `check_footage_utilization.py`(未使用candidate≤20%,wired) | §3.6/§6.1 | **SOLID** |
| 7 | 素材の話またぎ&話内被り | `check_arc_nonrepeat.py`(他話cut basename交差=0,hard) ＋ `check_footage_diversity`(distinct≥0.40/再利用≤4) | §12step7 | **SOLID**（3話分distinct生存はコンタクトシート先行QC=§12step7） |
| 8 | 天秤等の汎用象徴の乱用 | `check_footage_diversity`(汎用象徴≤2,rule19)。意味は人間 | §3.6 | **SOLID(数)+backstop**(`build_footage_contact_sheet.py`目視) |
| 9 | factory棚ラベル破損で場違い素材 | **自動不能**（ラベル破損でゲート検出不可）→`build_footage_contact_sheet.py`+`preflight_owner_review.py`目視QC | §12step7/§3.6 | **backstopのみ**（正直降格） |
| 10 | 8s→OP→本編4幕→EDでない | `check_final_acceptance.py:check_structure`(structure_4part,L432,hard)＋`check_bookends`(op_ed_bookends)＋`check_hook` | §6.1 | **SOLID**（5幕body受理も確認） |
| 11 | OP/EDがいつものテイストでない | `op_ed_bookends`(存在/構造,wired)。テイストは人間 | §6.1 | **SOLID(存在)+backstop**(owner review) |
| 12 | アニメが無く紙芝居 | `check_motion_energy`←`measure_motion_energy.py`(body mean≥12/p10≥9,wired) | §3.8/§6.1 | **SOLID+backstop**(motion-reel) |
| 13 | 図が少ない/疎(2点地図) | preflight マップノード≥6/StateMap≥12（`preflight_render_gate.py`に**要実装**）＋`verify_onscreen_text.py` | §3.10 | **WEAK/要実装+backstop** |
| 14 | 周回する淡い光がうざい | **自動ゲート無し**→`preflight_owner_review.py`(motion-reel人間承認) | §6.3 | **backstopのみ** |
| 15 | 図/lowerthird左見切れ | preflight safe-rect x∈[160,1760]/safeInset96（`preflight_render_gate.py`に**要実装**） | §3.10 | **WEAK/要実装+backstop** |
| 16 | 図背景が暗い | `check_image_cut_luma.py`(カット毎輝度,wired) | §3.0/§6.1 | **SOLID** |
| 17 | 画面が暗くて画像が見えない | `check_body_luma`(median≥48/暗率≤0.22)＋`check_image_cut_luma.py`＋`check_black`(wired) | §6.1 | **SOLID** |
| 18 | 効果音が無意味なフィラー | `check_sound_layers`(distinct SFX≥12/beds≥4/mux sha,wired)。意味は人間 | §4/§6.2 | **SOLID(数)+backstop**(音5本試聴) |
| 19 | SFX種類少ない/違和感 | `check_sound_layers`(distinct≥12,wired) | §4.4 | **SOLID+backstop** |
| 20 | 終盤の飛行機みたいな変な音 | `check_ending_sound.py`(WEAK)＋`preflight_owner_review.py`音5本試聴 | §4.2/§6.2 | **WEAK+backstop** |
| 21 | サムネが地味でCTR低い | `check_thumb_subject_luma.py`＋`check_thumbnail_visibility`(可読,wired)。CTRは非ゲート | §6.1 | **SOLID(可読)+backstop** |
| 22 | AI臭い(定型句/固有名詞/無出典断定) | `verify_script_lint.py`(カデンツ/固有名詞密度>4文,wired)＋`review_facts.md`人手 | §12step3 | **SOLID+backstop**(オーナー台本ロック) |
| 23 | SDXLを勝手に起動 | **ゲート無し**＝方針(rule19/pd-division-of-labor)＋provenance追跡 | §10 | **backstop/方針** |
| 24 | 緑なのに完成でない(自己申告) | `preflight_owner_review.py`(16枚コンタクト+luma+caption_sync+音5本+SUMMARY) | §6.2 | **backstop**（これが機構） |
| 25 | 偽の緑(古い良品) | `check_freshness`(wired)＋rule19 ship-gate `video_sha256`受領書照合＋`check_sound_layers` mux sha | §6.2 | **SOLID** |
| 26 | 薄い音で緑 | `check_loudness`/`check_bgm`(wired)＋`check_sound_layers` beds≥4＋2-pass静的-14(`build_short_mix.py`) | §4.2 | **SOLID+backstop**(音5本) |
| 27 | 尺外れ | `check_runtime_band.py`(19.5–20.5分,wired・唯一の承認偏差) | §0/§8 | **SOLID** |
| 28 | 20分を間/水増しで稼ぐ | `check_padding.py`(沈黙尾/同義反復/水増し検出,wired) | §0/§14 | **SOLID** |
| 29 | ゲート最適化(グッドハート) | `preflight_owner_review.py`人間試聴＋知覚モーション予算(depth/FigureBeats/ヒーロー面) | §6.2/§13 | **backstop**（構造的緩和） |

### 集計
- **SOLID（wired hard）: 15件**（#1,2,3,4字幕,6,7,10,12,16,17,25,27,28 ＋ 数量部#18,19,21,26）
- **要実装（本話ブロッキング/未コード）: 3系統**（#5 caption skip-hardening／#13 map-node preflight／#15 safe-rect preflight）＋補助的 `check_longform_drift`・`test_gate_fixtures`・`asset_selection.v001.json`未作成
- **backstopのみ（自動不能・人間試聴が最終担保）: #9, #14, #23, #24, #29** ＝ 正直に降格記載済
- **ドロップゲート引用: 0件**（music_coverage/stem_loudness/motion_bbox_flow を hard 機構として不使用＝実測NONE確認）

---

## C. 残課題（性質別分類・**どれも設計本文の穴ではない**）

### 下流成果物（制作段/別スレで作る・設計の穴でない）
- asset_selection.v001.json が episodes/PD-2026-033-tyler/05_visuals/ に未作成（実測で空・EP006/EP032には存在）。252 still-cut のcut配置・footage_utilization/preflight_render_gate 起動の唯一の束縛入力であり、これが無いままの ship は不可。設計指示は正しいが実装は未着手。
- 図の疎密（map-node≥6/StateMap≥12）と lower-third 左見切れ（safe-rect x∈[160,1760]）の preflight 実強制は preflight_render_gate.py に未実装。散文約束段階で、赤フィクスチャ(test_gate_fixtures.py)も未作成のため false-green を機械検出できない。

### 要実装ゲート（コード・別track）
- check_longform_drift は未実装。字幕ドリフトは verify_caption_sync の per-minute FAIL_SEGMENT_DRIFT=0.50 でカバーされるが、音声↔映像の長尺ドリフトは wired ゲートで測定されていない。

### 人間backstopのみ（自動ゲート原理的に不能）
- caption_sync/caption_coverage の skip 経路（master mp3欠落・matched_frac<0.60・整列不能）が発火すると、lag・per-minute drift・機能語行末・未字幕chunkの4検査が同時に未検査のまま ok:True/hard:False で緑化する（偽緑穴・要実装 skip-hardening）。ship前 preflight_owner_review.py の人間試聴が唯一の担保で、自動閉塞は未実装＝unresolved BLOCKING 1件。
- 『周回する淡い光』『OP/EDテイスト』『SDXL勝手起動』『ゲート最適化(グッドハート)』は自動ゲートが原理的に存在せず、preflight_owner_review.py の人間承認のみが担保。人間 backstop を省略すると全て素通りする（正直に backstop-only と降格済）。

### その他（記述精度）
- 3話アーク(EP33/34/35)の法廷/連邦庁舎 b-roll 共有について、check_arc_nonrepeat は basename交差=0 を無条件hardで強制する一方、MEMORYの『factory棚ラベル全面破損』下で各話distinct生存clip≥3×が実データ未検証。§12step7の出荷前コンタクトシートQCで先行実測しないと、レーン非重複は『計画上OK・未検証』のまま。
- 設計書 pass3 BLOCKING#2 は『機能語行末が全wiredゲートを素通りしうる』と過大主張していたが、実コードでは verify_caption_sync._dangling_end が既に受領側hardで塞いでいる。新設 check_caption_dangle は冗長。実効ゲート62の自己採点はこの分だけ過小評価（無害だが記述精度の欠陥）。
