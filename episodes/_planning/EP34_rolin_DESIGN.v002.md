# EP34（rolin）制作設計書 v002 — 3回点検 検証サインオフ層

- **binding正典（不変・invariant6）**: `EP34_rolin_DESIGN.v001.md`（本文はこちらが正典。v002はその上の検証・是正層）
- **超激重アニメ素材（別スレ制作）**: `EP34_rolin_ANIMATION_ASSETS.v001.md` / 引き継ぎ `EP34_rolin_ANIMATION_HANDOFF_PROMPT.md`
- **3回点検（corner-to-corner・実コード実測照合）**: pass別 [{'pass': 1, 'findings': 33, 'majors': 19}, {'pass': 2, 'findings': 31, 'majors': 11}, {'pass': 3, 'findings': 24, 'majors': 7}]
- **正直スコア**: 81/100 ／ **真の未解決BLOCKING**: 0件

---

## A. サインオフ監査（実ゲート実測照合の結論）

## 最終サインオフ監査結果 — EP34 (slug=rolin)

**判定: サインオフ可（設計として）。未解決 BLOCKING/MAJOR = 0。** ファイル無編集（既存784行が3パス監査を反映済で内部整合・虚偽機構/ドロップゲート引用ゼロを実査で確認したため、無用な改変で整合を壊さない）。

### 実ファイル照合で確認した誠実性（水増し・偽緑なし）
- **ドロップゲート引用ゼロ**: `check_stem_loudness`/`check_motion_bbox_flow`/`check_music_coverage` は設計に一切出現しない（grep 0件）。ファイルは disk 上に残存するが引用されていないため是正不要。
- **`check_arc_nonrepeat.py` は真に basename 一致のみ**（`scripts/check_arc_nonrepeat.py` line91 `os.path.basename(...)`・pHash/CLIP 無し）。設計の「basename一致のみ＝完全同一クリップの話またぎ検出」表記は正確。near-dup(pHash)/CLIP/EP33方向を「要ビルド・当話は`footage_signoff`人手目視のみ」と正直分類済。
- **`check_flat_windows.py` は実在**（469行・EP34仕様床）。設計は「新規16→15本」へ正しく再分類済。
- **`check_ending_sound` を WEAK 表記**、`sound_layers` を #15低域rumberフロアに引用しない、音/象徴ゲートを preflight 人手試聴＋WEAK へ段階化 — GATE REALITY と一致。
- **§13 スコア合計 81 は軸和と厳密一致**（9+8+8+7+8+8+7+8+9+9=81・10点軸ゼロ・最高9）。round4の+2水増しは是正済。

### 全過去失敗（29項）→ 実在機構の被覆
点検表（checklist）参照。**29項すべてが実在機構に紐付き、架空機構・ドロップゲートの引用はゼロ**。ただしオーナー最頻の実害のうち複数（字幕の実音声一致／機能語行末／話またぎnear-dup／終盤低域異音／薄い音／AI臭のリッチ検出）は現状 **SOLID機械ゲートでなく WEAK＋人手preflight＋未ビルドゲート** がフロア。設計はこれを正直に減点している。

### 残す MINOR（BLOCKING/MAJOR には至らず・無編集で記録）
1. **arc の new/modify 二重計上**: §12 step2 の「新規15本」リストと ship-critical 10本に `check_arc_nonrepeat.py(3話統一)` が入るが、同ゲートは §11#27/§13軸7 で「実装済SOLID(basename)」。pHash/3話統一は本来「改修」バケット。実装済かつ新規ビルド対象の二枠に跨がる軽微な内部緊張（誠実表記自体は他所で正しい）。
2. **語数≈3,096は推計・薄いマージン**: pass2機械実カウント3,030語（158wpmで1,151s＝床19s割れ）に「純+66語」で3,096語=1,176s＝床+6sのみ。§2.5本文の機械再カウント未実施＝`check_runtime_band.py`実測が唯一のship-gate。設計は両側リスク（150wpm+8s超／160-165wpm床割れ）を正直明記済だが、再収録リスクは残る。
3. **step0b の EP33 空宇宙前提**: EP33(tyler)資産が `tyler_film.json`/`public/tyler/` 未存在＝EP34↔EP33 arc が恒真PASS。設計は step0b で「EP33資産物理存在」を hard 前提へ昇格済＝適切だが、EP33 側の生成が完了するまで EP34 の arc 緑は出せない外部依存。

### Codex 実装粒度
画像68枚は正典 `EP34_rolin_ai_prompts.v001.md`（S001-S068・実在確認）が1枚=1 image-span で被写体/構図/匿名化/治療別YAVG下限まで確定。§10.1幕別配分(HOOK1/OP3/幕1 18/幕2 12/幕3 13/幕4 11/幕5 8/ED2=68)を正典へ一致させ「厳密一致」偽自認を削除済。**Codex=画像のみ／Claude=7TSX+新規15ゲート+改修5+fixture回帰** の分業も MEMORY/CLAUDE.md と整合。

### 完成条件（設計の Done 定義を追認）
必須ゲート・レジストリ緑（fail-closed＋負のフィクスチャ検証）＋機械ゲート全hard緑（新規はビルド後計上）＋`preflight_owner_review` 実物提示（音5本試聴・話またぎnear-dup目視・左右見切れ・画面内テキスト整合サインオフ）＋オーナーGO。自己申告完了禁止。この定義は妥当。

---

## B. 過去失敗 × 塞ぐ実在機構 点検表

## EP34 点検表 — 過去失敗 → 塞ぐ実在機構

凡例: **SOLID**=`check_final_acceptance`配線済・実データ検証済 / **WEAK+backstop**=機能するが偽装耐性限界・人間試聴で担保 / **HUMAN**=専用機械ゲート無し・preflight目視/試聴のみ / **BUILD-PENDING**=当話ビルド予定(未実装) / **RULE**=運用/設計規律。ドロップゲート(`check_stem_loudness`/`check_motion_bbox_flow`/`check_music_coverage`)引用は設計に無し(照合済)。

| # | 過去失敗 | 塞ぐ実在機構（ファイル名） | 設計§ | 状態 |
|---|---|---|---|---|
| 1 | 字幕がナレと不一致 | `caption_narration_match`＋`verify_caption_sync`(exact帯)／実音声ASR差分・vo_stem onset・WhisperX conf は改修要 | §5/§11#1 | **SOLID**(帰属/exact)＋BUILD-PENDING(実音声一致) |
| 2 | 字幕が遅い | `verify_caption_sync`(exact帯・リード0.12s) | §5/§11#1 | **SOLID** |
| 3 | 字幕が変な所で切れる(機能語行末) | 専用ゲート無し＝S3決定論規則分割(生成時)＋preflight readability目視 | §5.3/§11#2 | **HUMAN**＋生成規則 |
| 4 | 8:45以降ドリフト | `verify_caption_sync`(exact帯=粗ドリフト捕捉)／20分区間slope・章境界7点jumpは改修要 | §5.4/§11#3 | **SOLID**(粗)＋BUILD-PENDING(区間) |
| 5 | 字幕が飛ぶ(未字幕chunk) | `caption_coverage`(全chunk→cue被覆・欠落0) | §5.1/§11#1b | **SOLID** |
| 6 | DL素材が1つも使われない | `footage_utilization`(未使用検出)／`footage_usage_count`・`footage_inventory`は要ビルド | §3.5/§11#4 | **SOLID**フロア＋BUILD-PENDING(充足) |
| 7 | 素材の話またぎ&話内被り | `arc_nonrepeat`(basename一致=完全同一クリップのみ)＋`footage_diversity`(話内reuse≤4)／near-dup(pHash)/CLIP/EP33方向は要ビルド・人手目視 | §3.5/§11#27/step0b | **SOLID**(basename/話内)＋**HUMAN**(near-dup/EP33方向) |
| 8 | 天秤等の汎用象徴の乱用 | `footage_diversity`(rule19＝汎用象徴≤2)／拡張語彙`check_generic_symbols`は要ビルド・人手 | §11#16 | **SOLID**(基本)＋**HUMAN**(拡張) |
| 9 | factory棚ラベル破損で場違い素材 | `footage_signoff`署名artifact(カートゥーン検出FAIL)＋evidence bagはCodex専用＋生サムネ目視 | §3.5/§11#17 | hard＋**HUMAN**目視 |
| 10 | 構成(8s hook→OP→本編→ED)でない | `structure_4part`＋`op_ed_bookends`(※本話5幕＝step12でハードコード4固定でないか要コード確認/パラメータ化) | §11#5 | **SOLID**(要parameterize確認) |
| 11 | OP/EDがいつものテイストでない | `op_ed_bookends`＋既存テイスト軸＋owner | §9.1/§11#6 | **SOLID**＋owner |
| 12 | アニメが無く紙芝居 | `motion_energy`(within≥12/p10≥9)＋`check_flat_windows`(実装済469行=EP34床・fixture検証)／p50・12秒窓加算は改修要 | §3.7/§11#7 | **SOLID**＋fixture検証 |
| 13 | 図が少ない/疎(2点地図) | 専用ゲート無し＝設計固定 PinDropMap 15空港＋流量ライン | §3.3/§11#10 | **RULE**(設計固定) |
| 14 | 周回する淡い光がうざい | 設計禁止(周回/lissajous)＋`motion_energy`(走光を分子外) | §3.2/§11#8 | 設計禁止＋**SOLID** |
| 15 | 図/lowerthird左見切れ | 専用ゲート無し＝bbox決定論アサート(レンダ前)＋preflight「左右見切れ」目視 | §3.6/§11#9/§6.3⑪ | **HUMAN**＋アサート |
| 16 | 図背景が暗い | `image_cut_luma`(全カット拡張)＋SceneBed地色Rec709≥48 | §3.1/§11#11 | **SOLID** |
| 17 | 画面が暗くて画像が見えない | `body_luma`＋`image_cut_luma`(per-cut・前景ROI床)＋暗frame≤15% | §3.1/§11#12 | **SOLID** |
| 18 | 効果音が無意味なフィラー | SFX cut_id束縛検査(`check_sfx_distribution`要ビルド)＋`verify_sfx_manifest`(WEAK)＋preflight試聴 | §4.2/§11#13 | **WEAK+backstop**＋BUILD-PENDING |
| 19 | SFX種類少ない/違和感 | `sound_layers`(distinct SFX≥12/beds≥4)／SFX床≥18・`sfx_inventory`・`check_sfx_distribution`は要ビルド | §4.2/§11#14 | **SOLID**(distinct床)＋BUILD-PENDING(充足) |
| 20 | 終盤の飛行機みたいな変な音 | `check_ending_sound`(WEAK)＋`preflight_owner_review`音5本実試聴(省略不可)／`check_lowfreq_rumble`は次話以降。※`sound_layers`は<160Hz非検出のため引用せず | §4.1/§11#15/§6.3⑩ | **WEAK+backstop**(人手試聴) |
| 21 | サムネが地味でCTR低い | `thumbnail_visibility`(≥42)＋`thumb_subject_luma`／`check_thumbnail_saliency`(面積/色数/文字bbox)は要ビルド＋owner QC | §9.2/§11#18 | **SOLID**フロア＋BUILD-PENDING＋owner |
| 22 | AI臭い(定型句/固有名詰め/出典なし断定) | `script_lint`(AI臭/カデンツ)＋`verify_onscreen_text`(数値/引用/判例/人名帰属照合)＋§1/§6.2事実ゲート(facts_review)／`check_rhetoric_counts`加算は要ビルド | §2.3/§1/§11#19/#28/#29 | **SOLID**(script_lint/onscreen数値)＋BUILD-PENDING(修辞加算) |
| 23 | SDXLを勝手に起動 | 運用規律＝画像はCodexのみ(SDXL/A1111/ComfyUI勝手起動禁止) | §10/§11#20 | **RULE** |
| 24 | 緑なのに完成でない(自己申告) | 必須ゲート・レジストリ(fail-closed)＋`preflight_owner_review`(実物提示)＋オーナーGO | §6.0/§6.3/§11#21 | **owner-gate** |
| 25 | 偽の緑(古い良品/スタブ) | `freshness`(sha≠前回＋mtime)＋レジストリ負のフィクスチャFAIL実証＋回帰コーパス固定commit | §7/§6.0/§11#22 | **SOLID**(freshness)＋設計(neg-fixture) |
| 26 | 薄い音で緑 | `check_audible_floor`(相対−28全窓・要ビルド)＋2-pass I=−14＋preflight音5本試聴。※`sound_layers`はloudness床非測定 | §4.5/§11#23 | BUILD-PENDING＋**WEAK+backstop**(試聴) |
| 27 | 尺外れ | `check_runtime_band`(1,170-1,230s＝唯一のオーナー承認偏差) | §8/§11#24 | **SOLID** |
| 28 | 20分を間・水増しで稼ぐ | `check_padding`(沈黙尾/言い換え反復)＋`check_flat_windows`(実装済)／`check_content_density`(絶対床133語/60s)・`check_audible_floor`は要ビルド | §8/§11#26 | **SOLID**(padding/flat)＋BUILD-PENDING(密度) |
| 29 | ゲート最適化(グッドハート) | owner-gate＝intent是正・実物確認・未実装ゲート援用禁止・新規はビルド後のみ緑 | §6.4/§11#25 | **owner-gate** |

**被覆総括**: 29/29 が実在機構に紐付け・架空/ドロップ引用ゼロ。うち **SOLID機械フロア=約15項**、**WEAK+人手試聴=3項(#18/#20/#26)**、**専用ゲート無しHUMAN=3項(#3/#15/#7 near-dup)**、**設計/運用RULE=3項(#13/#14一部/#23)**、**owner-gate=3項(#24/#25一部/#29)**。オーナー最頻実害の一部が SOLID でなく人手/未ビルド依存＝これが 81/100 の天井。

---

## C. 残課題（性質別分類・**どれも設計本文の穴ではない**）

### 下流成果物（制作段/別スレで作る・設計の穴でない）
- EP33(tyler)資産(tyler_film.json/public/tyler/)未存在＝arc比較宇宙が空でEP34↔EP33が恒真PASS。step0bで hard前提化済だがEP33生成完了までEP34のarc緑を出せない外部依存。EP33方向の話またぎ被りは現状footage_signoff人手目視のみ。
- verify_onscreen_text の実スコープは数値/引用/判例/人名の帰属照合のみ。非数値(帰属チップ存在・ILLUSTRATIVEラベル・条文チップ・'TIP'不在・'>50%'illustrative表記)は§6.3⑫の人間backstop依存＝OCR/文字列照合の改修が済むまで機械保証なし。

### 要実装ゲート（コード・別track）
- §12 step2で check_arc_nonrepeat.py が『新規15本ビルド』リストと ship-critical 10本に入るが同ゲートは実装済SOLID(basename)。pHash/3話統一は本来『改修』枠＝new/modify二重計上の軽微な内部緊張(誠実表記自体は§11#27/§13軸7で正しい)。
- structure_4part が本編を4固定セグメントにハードコードしている場合、本話5幕でbookend境界検証が誤動作しうる。step12でコード確認しパラメータ化する前提(未確認)。

### 人間backstopのみ（自動ゲート原理的に不能）
- 新規15本＋改修5本のゲートが未ビルド。オーナー最頻実害の複数（字幕の実音声一致=改修要／機能語行末=機械ゲート無し／話またぎnear-dup=basename一致のみ＋人手／終盤低域異音=WEAK+人手試聴／薄い音=check_audible_floor未ビルド／AI臭リッチ検出=check_rhetoric_counts未ビルド）が現状 SOLID機械ゲートでなく人手preflight/WEAK/未ビルドに依存。
- CTR6%・30s残存70%・APV45%・知覚モーションの豊かさは公開後実測でのみ確定。機械ゲートは『凍っていない』を測るが『見ごたえ』は保証しない(feedback_animation_still_too_little)。

### その他（記述精度）
- 台本語数≈3,096は§2.5本文の機械再カウント未実施の推計。pass2実カウント3,030語(158wpmで床19s割れ)＋純+66語で床+6sのみの薄いマージン。速端160-165wpmで床割れ・遅端150wpmで上限+8s超の両側リスク→check_runtime_band実測次第で再収録の可能性。
