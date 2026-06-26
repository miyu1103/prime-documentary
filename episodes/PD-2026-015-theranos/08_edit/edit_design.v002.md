# 第15話 theranos 仕上げ設計書（Edit / Finish Design） v002 — SERIES FINALE

> **v002 改訂点（v001 は不変のまま保存）**: §1 の完成尺を「ふんわり目標」から**拘束力のある秒単位バジェット表**に変更し、**最終尺＝690〜750秒（11.5〜12.5分）を不可侵ゲート化**した。台本・claims・shotlist・AI画像・ナレ音声は**一切変更しない**（録り直し・再生成・追加課金なし）。フックと“ひと呼吸”は**既存の本編映像／既存VO断片／音楽のみ**で構成するため新規制作ゼロ。狙い＝14話で起きた「書き出し直前にフックを引き伸ばして尺を合わせる」やり直しを、設計段階で先回りして潰す（§1.1）。

対象: `PD-2026-015-theranos`（United States v. Holmes / Theranos・詐欺の境界線）。Codex がこの設計に従ってラフカット→仕上げを行う。
入力: `04_scenes/shotlist.v001.json`（24ショット・612.4秒≒10.2分）, `03_script/script.en.v001.md`（`[VO:]`=ナレ本文・**変更禁止**）, `04_scenes/asset_map.v001.md`, AI画像 `H:\pd-media\assets\ai\theranos\SPN-XXXX*.png`（🎨12場面・生成済み前提）, ストック動画（✅7場面・DL済み）, サムネ `H:\pd-media\assets\ai\thumbs\theranos\THUMB-01..06.png`（生成済み前提）。
準拠: `episodes/_planning/VIDEO_RULES.md` §10〜13 / `docs/motion-design-language.md` / `docs/motion-quality-gate.md` / **CLAUDE.md 不変項11（生成映像は記録ではない・実在人物の肖像なし）**。

> **⚠ R3 / 法的高リスク話。公開前に法務レビュー必須（本書 §4・§5）。** 実在人物（Elizabeth Holmes / Ramesh Balwani 等）の**肖像・実写・ディープフェイク・断定的な有罪表現は不可**。表現は象徴的・一般化に徹し、事実は**判決／公開記録ベース**。投資家詐欺の**4件有罪は事実として提示**してよいが、患者関連は「無罪（acquitted）」、3件は「評決不成立（mistrial / no verdict）」であり、**「有罪」と書かない**。意図・認識は**陪審／裁判所に帰属**させ、ナレーター（チャンネル）の断定にしない。台本・claims は一切変更しない。

---

## 1. 完成尺と4部構成（VIDEO_RULES §10 厳守）＝**拘束力のある秒バジェット**

> **不可侵ゲート（最重要）**: 最終書き出しの実尺は **690〜750秒（11.5〜12.5分）に入っていなければならない**。狙い値＝**約706秒（11.8分）**。`scripts/check_runtime_band.py`（v002で新設）でレンダー後に必ず検査し、窓外なら **FAIL（書き出しやり直し）**。`duration_positive` だけのチェックでは**通してはならない**（10.4分でも素通りしてしまうため＝§1.1）。

下表の各セグメントは**目安ではなく組み込み必須項目**。本編(shotlist 612.4s)＋ブランドオープニング(3.5s)＋エンドカード(9s)だけだと **624.9秒＝10.42分** にしかならず窓に**届かない**（現行 review_proxy v003 が実際に624.96秒＝この不足の実例）。**フックは約7秒の短いtease**（オーナー指定・長尺化しない）なので、不足分の約80秒は**主に幕間の“ひと呼吸”と山場の余韻**で**既存素材のみ**から稼ぐ。

| # | セグメント | 内容 | ソース（新規制作なし） | 秒 |
|---|---|---|---|---|
| 1 | **フック** | 本編の山場ハイライト 約3〜4カットの**短いtease**＋riser SFX。**約7秒**（短く punchy・長尺化しない＝オーナー指定）。決め所VO断片は0〜1個だけ | 既存本編映像＋既存VO断片＋音楽 | **7** |
| 2 | ブリッジ | riser の余韻→ブランドスティングへの渡し | 音楽のみ | 1.5 |
| 3 | **オープニング** | 既存 `BrandOpening`（`OPENING_SEC=3.5`） | 既存・作り直さない | 3.5 |
| 4 | **本編** | act1〜act4＋ending本文（SPN-0002〜0022・台本順／§1注記の章順で再配列） | shotlist 24ショット | 612.4 |
| 5 | 幕間“ひと呼吸” ×4 | act1→2 / 2→3 / 3→4 / 4→ending の転換で**ナレなしの held ビジュアル＋音楽スウェル**を各約10秒 | 既存映像＋音楽 | 40 |
| 6 | 山場の余韻 | 評決ボード確定後（SPN-0013→0014）の“ため→開放”の held beat | 既存映像＋SFX | 10 |
| 7 | 主要グラフの間 | 評価額 $9B→$0 崩落の着地／4件 count-up／境界の等式の組み上がりに小さな held | 既存コード演出 | 15 |
| 8 | CTA hold | SPN-0022 Subscribe を少し長く持つ | 既存 | 8 |
| 9 | **エンドカード** | 既存 `BrandEndcard`（`ENDCARD_SEC=9`） | 既存・作り直さない | 9 |
| | **合計** | | | **≈706秒＝11.8分 ✓（窓内・狙い中央寄り）** |

> **増やす尺はすべてナレを足さない**（held ビジュアル＋音楽＋既存VO断片のみ）＝**ナレ録り直し・ElevenLabs追加課金・字幕の作り直しは発生しない**。台本／claims／shotlist は **Read専用・不改変**（不変項6・12）。**R3：余韻・間・フックで断定有罪の含意を足さない／患者関連の無罪・評決不成立の区別を崩さない**（GUILTY表記は投資家詐欺4件のみ）。間延びさせず密度で稼ぐ（カット切替は約4.5秒を維持＝§2）。
>
> ### 1.1 なぜ尺が足りなくなるか（14話の教訓・本改訂の理由）
> 14話(lange)は本編ナレ ~10.3分で、**書き出し直前にフックを引き伸ばして 11.5〜12.5分の窓に押し込んだ**（`final.v003.qc.json` ノート「Hook was extended to bring runtime into the requested 11.5–12.5 minute window」）。これが「色々やり直し」の一因。原因は2つ：(a) フックと“ひと呼吸”が**目安**としか書かれず、実装で省略されて本編＋開閉だけの ~10.4分になった。(b) レンダーQCが**尺の窓を検査していない**（`duration_positive` だけ）ので短い尺でも PASS してしまう。15話も現状この穴を抱えたまま（proxy v003＝10.42分）。本v002で (a)を**秒バジェットの必須項目化**、(b)を **`check_runtime_band.py` の不可侵ゲート化**で塞ぐ。
>
> **章順の注意**: shotlist は `span_id` 昇順だが、`chapter_id` は台本の流れ（act1→act2→act3→act4→ending）に従って配置すること。具体的には **SPN-0023(act1) は SPN-0005 と 0006 の間**、**SPN-0024(act3) は SPN-0012 と 0013 の間** に挿入する（asset_map のナレ対応に一致）。台本テキストは変えない。

**フックに使う本編ハイライト候補（priority A 優先・各1〜2秒で速いカット）**:
SPN-0001(一滴の血＋$9B→$0グラフ) / 0008(他社の機械で検査) / 0013(2022・4件有罪の評決ボード) / 0014(患者は無罪・3件評決なし) / 0015(無罪≠潔白／Balwani全12件) / 0016(量刑 約11年3か月) / 0012(詐欺＝欺く意図) / 0024(検察 vs 弁護の二分) / 0002(シリーズ最終回の問い) / 0021(シリーズ総括への引き)。
→ ナレの決め所断片を1〜2個だけ被せ、最後は無音ぎみ→オープニングへブリッジ。**台本テキストは変えない**。

---

## 2. 全ショット モーション設計（Ken Burns 一辺倒にしない＝VIDEO_RULES §12）

凡例: motion は shotlist の値。**「意味のあるアニメ」列が今回の追加指定**。画像は必ず動かす。**実在人物は一切描かない**（象徴・一般化）。出典は判決/記録ベース。

| SPN | 章 | 種別 | テロップ(on_screen_text) | 意味のあるアニメ（指定） |
|---|---|---|---|---|
| 0001 | hook | 図解/graphic_anim | When does selling a dream become a crime? | 一滴の血が落ちる→波紋。**評価額グラフが $9B まで上昇→一気に $0 へ崩落**。雑誌表紙風モンタージュは**人物を出さず**シルエット/空白の表紙で象徴 |
| 0002 | opening | ai/ken_burns | Finale: one person vs. everyone | シリーズで反転したカメラを象徴。**矢印の向きが「国家→個人」から「個人→everyone」へ反転**。寄り＋微パララックス |
| 0003 | act1 | ai/ken_burns | 2003 — a Stanford dropout's startup | 年表が2003へ進む。**創業の象徴（無人のラボ/空席のデスク）**。実在人物なし |
| 0023 | act1 | ai/ken_burns | Prestige became a substitute for scrutiny | **「著名な肩書きカード」が積み上がり、その陰で“検証”の虫眼鏡が縮む**。権威が監視の代替になる対比 |
| 0004 | act1 | 実写/native | The Edison: hundreds of tests, one drop | 指先一滴 vs 採血針・バイアルの対比。**“Edison”は無地の黒い箱として象徴**（実機の写真は使わない） |
| 0005 | act1 | 図解/graphic_anim | ~$9 billion · prominent board · Walgreens (limited) | **評価額グラフが ~$9B へ上昇**＋**ロゴ壁（無名化した抽象ロゴ）**＋Walgreens は「限定」注記。実ロゴ商標は避け一般化 |
| 0006 | act1 | 実写/native | A story powerful enough to stop the questions | 「製品より物語」。落ち着いた寄り、問いが止む静けさ |
| 0007 | act2 | 図解/graphic_anim | 2015: The Wall Street Journal investigates | **年表が2015へ→調査報道のビート**。新聞名はテキストのみ（紙面画像/記者の顔は出さない） |
| 0008 | act2 | ai/ken_burns | Tests run on other companies' machines | **「自社の革新機」から“他社の市販機”へ矢印が差し替わる**暴露の演出。寄り＋微パララックス |
| 0009 | act2 | ai/ken_burns | — | 医療検査の重み。**誤った数値→誤った判断へ**の連鎖を抽象線で。静かな寄り |
| 0010 | act2 | 図解/graphic_anim | 2018: SEC fraud charge (settled, no admission); company dissolves | **年表が2018へ→SEC民事（“認否なし和解”を明記）→会社解散**。$9B が線で 0 へ。断定有罪表現を避ける |
| 0011 | act2 | 実写/native | Failure — or fraud? | **左右に "Failure" と "Fraud" を並置**し中央に問い。act3への橋渡し |
| 0012 | act3 | ai/ken_burns | Fraud = intent to deceive (not just failure) | **法定義カード「詐欺＝欺く意図（単なる失敗ではない）」**を組み上げる。天秤の象徴。長尺なので2バリアント切替 |
| 0024 | act3 | 実写/native | Prosecution: she knew. Defense: a true believer. | **左右対比（検察＝“知っていた” / 弁護＝“真の信奉者”）**のスプリットスクリーン。人物は出さず役割ラベルで |
| 0013 | act3 | **図解/graphic_anim** | 2022 — GUILTY: 4 counts (investor fraud) | **年表が2022/1/3へ→“count by count”の評決ボードが1件ずつ確定→投資家詐欺4件 GUILTY が金ラインで確定**（本話の山場グラフィック）。出典＝記録ベース |
| 0014 | act3 | ai/ken_burns | ACQUITTED: patient counts · NO VERDICT: 3 counts | **評決ボードの続き**：患者関連＝**ACQUITTED（無罪）**、3件＝**NO VERDICT（評決不成立）**を別色で明示。**「有罪」表記を絶対に出さない** |
| 0015 | act3 | 実写/native | Acquittal ≠ exoneration. Balwani: convicted on all 12. | **「無罪 ≠ 潔白」の注記カラム**＋Balwani は別裁判で全12件有罪（テキストで対比）。人物像は出さない |
| 0016 | act3 | ai/ken_burns | Sentenced: ~11 years, 3 months | **量刑の象徴**：時間（年月）が積み上がるカウンタ「~11y 3m」。法廷光の象徴。実在人物なし |
| 0017 | act4 | ai/ken_burns | "Fake it till you make it" — usually legal | **“Fake it till you make it”の標語が浮かび、多くは合法と注記**。スタートアップ behavior の一般化。軽ズーム |
| 0018 | act4 | 実写/native | The line: knowingly false + relied upon = fraud | **境界の等式「knowingly false ＋ relied upon ＝ fraud」が組み上がる**。本話の核（線＝境界線） |
| 0019 | act4 | ai/ken_burns | — | **「失敗したアプリ＝金の損失」vs「誤った血液検査＝診断の損失」の対比**で stakes を可視化。寄りで余白 |
| 0020 | ending | ai/ken_burns | One question, many costumes: where is the line? | **シリーズ総括**：1つの問いが衣装を替える（stop/arrest, identify/investigate, promise/lie の線が次々）。ゆっくり引き |
| 0021 | ending | 実写/native | — | 「線を引き直し続ける」総合。落ち着いた引き |
| 0022 | ending | ai/ken_burns | Subscribe — one line at a time | **CTA**：Subscribe ボタン演出＋「one line at a time」（1.6秒程度） |

> AI画像は1スパンに複数バリアントあり（`SPN-XXXX_02.png`等）。長いスパン（0012=45秒, 0015=43秒, 0002=40秒, 0020=36秒）は**約4.5秒ごとに別カット/別バリアントへ切替**し、静止・長居を避ける。importer が自動で複数取り込み。

---

## 3. テロップ／字幕／出典のレイアウト（被らせない＝VIDEO_RULES §13）

- **字幕（ナレ全文・forced alignment）**: 画面**下部の安全帯**。**ナレと語単位でぴったり同期（ズレ≤約120ms）**・一字一句一致。
- **見やすさ（VIDEO_RULES §13・数値）**: 文字 ≈48〜60px・本文太字・**白文字＋濃い縁取り/影＋半透明黒帯(不透明度~55〜70%)**・最大2行・中央寄せ・1〜2行ずつ送り、読み切れる表示時間（高速点滅切替しない）。
- **テロップ（キーワード＝on_screen_text）**: **上/中央**。短く・大きく。字幕帯と**重ねない**。
- **出典（金ライン）**: 例 `United States v. Holmes (N.D. Cal.) — verdict Jan 3, 2022` / `SEC charges 2018 (settled, no admission)`。**右下など別ポジション**固定。字幕・テロップと別レイヤ・別位置。判決/記録ベースのみ。
- **AI画像には常時 `symbolic reconstruction` ラベル**（`CarpenterPremium` の `ReconLabel` を流用）。生成映像は記録ではない旨を画面で明示（不変項11）。
- 3者＋ラベルを同じ場所に重ねない（読めない/被るのは不可）。

## 4. 品質ゲート（書き出し前チェック＝motion-quality-gate）

> **【最重要・独立受け入れゲート】QCを“自分で true と書く”のは禁止。** `./.venv/Scripts/python.exe scripts/check_final_acceptance.py 15 --render <final.mp4>` を実行し **RESULT: PASS（exit 0）** を得ること。これは実ファイルを機械測定する独立検証で、14話で起きた**①声がSAPIプロキシ（いつものElevenLabsでない）②最終字幕なし③黒画面=画像なし④尺不足**を自動検出する（14話は手書きQCで全部 true と書いていたが実物は不適合だった＝§1.1の二の舞防止）。下のチェックリストは人手の目視確認用で、**機械ゲートのPASSが最終の必須条件**。
> - `voice_is_master`：ElevenLabs本番ナレ（`06_audio/voice_plan.v001.json` の provider＝elevenlabs）。**SAPI/`review_proxy` 音声を最終に使わない。**
> - `captions_final`：`08_edit/captions.v001.srt`（**`review_proxy` でない**最終字幕）が存在し尺の90%以上をカバー。
> - `images_present`：長い黒画面なし（全カットに画像/実写/図解が出ている）。
> - `bgm_present`：**BGM（音楽の帯）が常時鳴っている**。無音の合計が長い＝ナレだけで音楽が入っていない（14話=109秒・15話proxy=102秒の無音＝音楽なし）。音設計書(`06_audio/audio_cue_sheet.v001.md`)の4層ミックスを必ず適用すること。
> - `runtime_band`：690〜750秒。

- [ ] **【尺・不可侵】最終実尺＝690〜750秒（11.5〜12.5分）に入っている**。`scripts/check_runtime_band.py <render.mp4>` または `check_final_acceptance.py` が PASS（窓外＝書き出しやり直し）。**`duration_positive` だけのPASSでは不可**（§1・§1.1）
- [ ] **【声・不可侵】最終音声＝ElevenLabs本番ナレ**（proxyのWindows SAPI声で書き出さない）。`check_final_acceptance.py` の `voice_is_master` PASS
- [ ] **【字幕・不可侵】最終字幕（非proxy）が焼き込み/サイドカーで存在**し全編同期。`captions_final` PASS
- [ ] **【画像・不可侵】全カットに絵がある**（黒画面/空カードなし）。`images_present` PASS
- [ ] **【BGM・不可侵】音楽の帯が常時鳴っている**（ナレだけにしない・無音帯を作らない）。音設計書の4層(VO/BGM/SFX/ambience)＋ダッキングを適用。`bgm_present` PASS
- [ ] **フックは本編ハイライト約7秒**（短く punchy・長尺化しない＝オーナー指定）＋幕間“ひと呼吸”×4（各約10秒）・山場の余韻が§1バジェット通り組み込まれている（尺は主に幕間と余韻で稼ぐ）
- [ ] フック→オープニング→本編→エンディングの**4部**になっている
- [ ] `coded/cards = 0`（全ショット実素材 or 図解で埋まっている）
- [ ] 全ショットにモーション（静止画ゼロ）／Ken Burns 一辺倒でない
- [ ] 字幕・テロップ・出典が**位置で分離**し被っていない／AI画像に `symbolic reconstruction` ラベル
- [ ] 音4層＋**ダッキング**でナレ最優先（`06_audio/audio_cue_sheet.v001.md`）。**ナレ＝ElevenLabsで生成OK（課金承認待ち不要）**＝−14 LUFS / TP ≤ −1
- [ ] **R3表現チェック**：実在人物の肖像/実写/ディープフェイクなし・断定有罪なし・**患者関連は無罪/評決不成立であり「有罪」表記なし**・意図は陪審/裁判所に帰属
- [ ] **公開前 法務レビュー（R3）を実施・記録**（本書 §5 / EP15 は公開前に法務レビュー必須）
- [ ] 中立・台本/claims 不改変

## 5. この話の編集ポリシー（★R3・最重要）
- **中立**（「失敗 or 詐欺」の問いに肩入れしない）。検察主張・弁護主張・陪審の評決（有罪/無罪/評決不成立）を**公平**に提示。
- **実在人物（Holmes / Balwani 等）の肖像・実写・ディープフェイク不可**。象徴的・一般化した表現のみ。雑誌表紙・記者・実機・実ロゴは出さず抽象化。
- **断定的な有罪表現をしない**。投資家詐欺**4件の有罪は判決事実として提示**してよいが、患者関連＝**無罪**、3件＝**評決不成立**であり「有罪」と書かない。「無罪 ≠ 潔白」を明記。意図/認識は**陪審・裁判所に帰属**させ、ナレーター断定にしない。
- **事実は判決／公開記録ベース**（LLMを出典にしない）。数字（$9B・4件・約11年3か月・全12件）は単位・対象・期間を確認。
- **公開前に法務レビュー必須（R3）**。本動画は法務レビュー記録（exact revision/hash）なしに `publish_approved` へ進めない（CLAUDE.md §3 高リスク承認・§4 不変項2、`.claude/rules/16-approval-boundaries.md`）。
- 台本・claims を一切改変しない（Read専用）。claims 変更時は全依存を stale 化（不変項12）。

---

## 6. 実装方針＝Premium級コード演出（★重要・汎用RoughCutでは出ない）

§2 の「意味あるアニメ」は**汎用 `RoughCut` では描画されない**（RoughCutは Ken Burns＋動画＋テロップ＋グレイン止まり）。
→ EP15は**bespokeな `remotion/src/compositions/TheranosPremium.tsx` を新規作成**し、既存 `CarpenterPremium.tsx`（雛形）／`MadoffPremium.tsx`（金融詐欺・近題材）を参考にする。`RoughCut-theranos` は素材ステージング/下見用に残してよいが、**最終書き出しは `TheranosPremium`**。意味あるアニメはコード演出が主役、**DL済みファクトリ素材は加飾レイヤとして活かす**（§6末尾の加飾レイヤ参照・実在人物想起素材は不可）。

### 使う既存コード部品（再利用・新規実装を最小化／実在確認済み）
- `components/Motion.tsx`: `MovingStage`（カメラ＋粒子＋光）, `Particles`, `LightSweep`, `Vignette`, `CameraRig`。
- `components/Grain.tsx`: `Grain`（フィルムグレイン）。
- `components/Bookends.tsx`: `BrandOpening`（`seriesLabel`/`title`/`subtitle`）／`BrandEndcard`（固定エンドカード・`OPENING_SEC=3.5` / `ENDCARD_SEC=9`）。
- `components/SceneArt.tsx`: `SceneArt`（props=`visualMode`/`motifHint`/`onScreenText`/`seed`）で **小槌(gavel)/天秤(scales)/年表(timeline)/USマップ(map)/書類＋印章(document)/法廷(courtroom)/取調室ランプ(room)** を自動選択（`pickArt`）。
- `CarpenterPremium.tsx` の流用可能なビズ（同ファイル内 export 前提でコピー/移植）：`Vote`(5–4票・**本話は使わず代わりに評決ボードへ改変**)、`MapGrid`、`TwoColumn`(左右対比)、`Doors`(アイコン/ラベル列)、`BigNumber`、`CourtColumns`、`Boundary`(境界線)、`Triptych`、`SceneShell`(多画像Ken Burns＋光＋粒子＋`ReconLabel`＋`Lower`)。

### ショット→実装の割り当て（§2の演出をコードに対応）
| SPN | 演出（§2） | 実装（部品） |
|---|---|---|
| 0001 | 一滴の血＋$9B→$0崩落グラフ | 手組み**ValuationGraph**（上昇→崩落・新規小コンポ）＋`Particles`。雑誌表紙は人物なしの抽象板 |
| 0002 | 矢印が「国家→個人」へ反転 | AI画像＋`MovingStage`＋手組み矢印（反転） |
| 0003 | 2003年表・創業の象徴 | `SceneArt visualMode="timeline"`（2003マーカー）＋AI画像（無人ラボ） |
| 0023 | 権威カードが積み“検証”が縮む | `Doors`（著名肩書きラベル列）＋手組み虫眼鏡縮小 |
| 0004 | 一滴 vs 採血針・黒い箱 | `<Video>`（ストック）＋`Vignette`/`Grain`。Edison は無地黒箱の手組み |
| 0005 | ~$9B 上昇＋ロゴ壁＋Walgreens限定 | **ValuationGraph**（~$9Bへ）＋`Doors`（抽象ロゴ壁）＋注記 |
| 0006 | 物語が問いを止める | `<Video>`＋`Vignette`/`Grain` |
| 0007 | 2015 調査報道 | `SceneArt visualMode="timeline"`（2015マーカー）。新聞名はテキストのみ |
| 0008 | 自社機→他社市販機へ差替 | AI画像＋`TwoColumn`(left="own device" / right="others' machines")＋差替アニメ |
| 0009 | 誤数値→誤判断の連鎖 | AI画像＋`SceneShell`相当（多画像Ken Burns）＋細線アニメ |
| 0010 | 2018 SEC和解→解散・$9B→0 | `SceneArt visualMode="timeline"`（2018）＋**ValuationGraph**（0へ）＋“no admission”注記 |
| 0011 | Failure vs Fraud 並置 | `<Video>`＋`TwoColumn`(left="Failure" / right="Fraud") |
| 0012 | 法定義「詐欺＝欺く意図」 | `SceneArt motifHint="scales"`（天秤）＋手組み定義カード |
| 0024 | 検察 vs 弁護の二分 | `<Video>`＋`TwoColumn`(left="Prosecution: she knew" / right="Defense: true believer") |
| 0013 | **2022→count by count 評決ボード（山場）** | `SceneArt visualMode="timeline"`（2022/1/3）＋**VerdictBoard**（`Vote` を改変：4件 GUILTY を1件ずつ確定）＋`SceneArt motifHint="document"`（記録確定）。`LightSweep`色=GOLD |
| 0014 | 患者=無罪・3件=評決なし | **VerdictBoard** 続き（ACQUITTED/NO VERDICT を別色・**GUILTY表記なし**）＋AI画像 |
| 0015 | 無罪≠潔白／Balwani全12件 | `<Video>`＋`TwoColumn`(left="Acquittal ≠ exoneration" / right="Balwani: all 12") |
| 0016 | 量刑 約11年3か月 | AI画像＋`BigNumber`(top="~11y 3m" bottom="sentenced")＋`SceneArt motifHint="court"`光 |
| 0017 | “Fake it till you make it”標語 | AI画像＋手組みタイポ＋注記「usually legal」 |
| 0018 | 境界の等式 | 手組み等式（knowingly false ＋ relied upon ＝ fraud）／`Boundary`（線） |
| 0019 | アプリ損失 vs 検査の損失 | AI画像＋`TwoColumn`(left="a failed app: money" / right="a wrong test: a diagnosis") |
| 0020 | シリーズ総括「many costumes」 | AI画像＋`Triptych`相当（stop/arrest・identify/investigate・promise/lie の線） |
| 0021 | 線を引き直し続ける | `<Video>`＋`Vignette`/`Grain` |
| 0022 | CTA Subscribe | 手組みSubscribeボタン＋`soft_impact`（`BrandEndcard` 直前） |
| その他のai_image | 寄り/引き＋微パララックス | `SceneShell`相当（多画像Ken Burns＋`Particles`/`Vignette`/`Grain`＋`ReconLabel`） |
| stock_video | 実写再生 | `<Video>`＋`Vignette`/`Grain` |

> **VerdictBoard / ValuationGraph は新規小コンポ**（`Vote` と `BigNumber` を改変・流用）。実在人物を描かない・断定有罪表記を避けるための専用ビズ。SVG/CSS・$0。

### 実装ステップ
1. `TheranosPremium.tsx` を作成（`scenes[]` に24スパン＋hook/opening/ending を `kind` 付きで定義。**章順は §1 の注記どおり台本順に並べる**。AI画像は `remotion/public/theranos/SPN-XXXX*.png` を参照）。
2. `Root.tsx` に `TheranosPremium`（`id="TheranosPremium"`・ハイフンのみ）を `<Composition>` 登録（`MadoffPremium` 等と同形・`durationInFrames={theranosPremiumDurationInFrames(BRAND.video.fps)}`）。`THERANOS_ROUGHCUT` のRoughCut登録は残してよい。
3. `npm run studio` で `TheranosPremium` を確認 → §2の各演出が出ているか／4部構成か／**R3表現チェック（§4）**をチェック。
4. 書き出しは `TheranosPremium`（quality-first CPU/libx264）。**公開前に法務レビュー（§5）を通すまで `publish_approved` に進めない。**

> **加飾レイヤ（VIDEO_RULES §4/§12）＝DL済みファクトリ素材を活かす**: `assets/asset_manifest.v001.json`（商用OK・DL済み）から**トーンの合うものだけ**を `scripts/select_factory_assets.py` で選び `remotion/public/theranos/factory/` へコピー → `TheranosPremium` に **背景プレート(下地)＋light/particle/vfxオーバーレイ(screen/add)＋texture(overlay)** の3層で重ね、奥行きと光で美しくダイナミックに。**意味あるアニメはコード演出が主役・factoryは加飾**（過剰にしない・合わない素材は使わない・licenseはallowedのみ）。**実在人物を想起させる素材は使わない（R3）。** **美しくダイナミックに**＝映画的カメラ（`MovingStage`/`CameraRig` で全カットに寄り/引き/パララックス＋イージング、spring/ease＝リニア禁止）＋ファクトリ三層加飾（§7）＋**山場 SPN-0013 は“ため→開放”でSFX同期**。トランジションは上品・速め（光ワイプ/クロスディゾルブ）。**ただしR3＝実在人物想起素材なし・断定有罪の演出なし・無罪/評決不成立の区別を崩さない。** 詳細割り当ては **§7** を参照。

---

## 7. ファクトリ素材の本格活用（テーマ別b-roll/背景/オーバーレイ）

DL済みファクトリ棚（`assets/asset_manifest.v001.json`・全件 Pexels/Pixabay＝**商用OK**・`H:\pd-media\assets\factory\`）を、§6の「コード演出が主役」を崩さずに**ふんだんに**活かす。実体は `FACTORY_INVENTORY.md` のテーマ別インデックスに準拠し、**実在サブタイプ名のみ**を指定する（新規名を作らない）。**本話はR3**：実在人物（Holmes / Balwani）を**想起させる素材は使わない**。一般的な研究室・抽象・象徴のみ。実機（Edison）・実ロゴ・雑誌表紙・記者・実写の人物は出さない。一般ストックは**「その事件の実物そのもの」として提示しない**（illustrative/symbolic）。

### 7.1 三層構成（主役＝コード演出 / 象徴＝AI / 加飾＝ファクトリ）

| 層 | 役割 | 主な担い手 | 本話での扱い |
|---|---|---|---|
| **① コード演出（主役）** | 意味のあるアニメ＝票/年表/評決ボード/評価額グラフ/境界の等式/定義カード | §6の手組みコンポ（`VerdictBoard`/`ValuationGraph`/`TwoColumn`/`Boundary`/`BigNumber`/`SceneArt`） | **意味は必ずコードで描く。ファクトリで意味を代替しない。** |
| **② AI画像（象徴）** | ヒーロー/象徴ショット（**人物なし**・無人ラボ・抽象） | `remotion/public/theranos/SPN-XXXX*.png`＋`SceneShell`（多画像Ken Burns） | 実在人物の肖像なし（不変項11）・`symbolic reconstruction` ラベル常時。 |
| **③ ファクトリ（加飾）** | **確立ショット・b-roll・カットアウェイ・背景プレート・overlay・texture** | `backgrounds`（b-roll/establishing/背景）＋`light/vfx/particle`（screen/add）＋`texture`（overlay）＋`loops`（動く抽象背景） | トーン（黒/紺/青/金）に合うものだけ薄く。1カット1〜2レイヤ。**意味は持たせない。** |

### 7.2 SPN→ファクトリ割り当て表（theme・subtype は実在名のみ）

凡例 — **層**: BG=背景/b-roll、OVL=オーバーレイ（light/vfx/particle, screen/add）、TEX=質感（overlay）、LOOP=動く抽象背景。**kind**: video / image。subtypeは複数候補から**トーン適合の1点**を選ぶ。

| SPN | 章 | theme | subtype（実在・候補） | 層 | kind |
|---|---|---|---|---|---|
| 0001 | hook | finance_money / atmosphere_symbolic | stock_chart_crashing_red, shattered_mirror | BG下地＋OVL | video |
| 0002 | opening | atmosphere_symbolic / loops | empty_road_sunset, looping_gradient_navy | BG/LOOP | video |
| 0003 | act1 | medical_lab | modern_medical_lab, laboratory_glassware | BG（establishing・無人ラボ） | video |
| 0023 | act1 | documents_paper / texture | documents_on_desk, aged_document_texture | BG＋TEX（肩書きカード下地） | image |
| 0004 | act1 | medical_lab | test_tubes_rack_lab, blood_vials_in_rack, laboratory_centrifuge | BG（b-roll・指先一滴の文脈） | video |
| 0005 | act1 | finance_money | stock_market_screen, stock_chart_rising_green | BG（評価額上昇の背後） | video |
| 0006 | act1 | atmosphere_symbolic | single_chair_empty_room, clock_ticking_macro | BG（“間”・静けさ） | video |
| 0007 | act2 | documents_paper | newspaper_macro, newspaper_printing_press | BG（調査報道の象徴・紙面のみ） | video |
| 0008 | act2 | medical_lab | laboratory_centrifuge, microscope_lab | BG（市販機への差替の文脈） | video |
| 0009 | act2 | medical_lab | microscope_lab, test_tubes_rack_lab | BG（誤数値→誤判断の連鎖） | video |
| 0010 | act2 | finance_money / documents_paper | stock_chart_crashing_red, documents_on_desk | BG（解散・$9B→0の背後） | video |
| 0011 | act2 | atmosphere_symbolic | shattered_mirror, clock_ticking_macro | OVL/BG（Failure vs Fraud の橋渡し） | video |
| 0012 | act3 | legal_court | balance_scale_brass, judge_gavel_wooden | BG（天秤＝詐欺の法定義） | video |
| 0024 | act3 | legal_court | courtroom_interior | BG（検察 vs 弁護の二分） | video |
| **0013** | **act3** | **legal_court ＋ light/vfx** | **courtroom_interior, judge_gavel_wooden ＋ god_rays + smoke_on_black** | **BG＋OVL（山場・評決ボードに光＋vfxで“ため→開放”）** | **video** |
| 0014 | act3 | legal_court | balance_scale_brass | BG（無罪/評決不成立の続き・別色） | video |
| 0015 | act3 | legal_court / documents_paper | courtroom_interior, documents_on_desk | BG（無罪≠潔白／Balwani全12件） | video |
| 0016 | act3 | atmosphere_symbolic / legal_court | clock_ticking_macro, balance_scale_brass | BG＋OVL（量刑＝時間が積む象徴） | video |
| 0017 | act4 | atmosphere_symbolic | empty_road_sunset | BG（“Fake it…”標語の一般化） | video |
| 0018 | act4 | atmosphere_symbolic | shattered_mirror | OVL（境界の等式の背後・薄く） | video |
| 0019 | act4 | medical_lab / finance_money | blood_vials_in_rack, money_cash_counting | BG（検査の損失 vs 金の損失の対比） | video |
| 0020 | ending | urban_night / atmosphere_symbolic | abandoned_factory_interior, single_chair_empty_room | BG（シリーズ総括の引き） | video |
| 0021 | ending | atmosphere_symbolic / loops | clock_ticking_macro, atmospheric_loop | BG/LOOP（線を引き直し続ける） | video |
| 0022 | ending | atmosphere_symbolic | single_chair_empty_room | BG（CTA下地・控えめ） | image |

> 全編共通の**空気感レイヤ（薄く）**: `particle`＝dust_motes_sunlight / floating_dust_in_light_beam（screen/add）、`texture`＝aged_document_texture / film_grain_texture（書類・カードの下地, overlay）、`light`＝soft_golden_light / bokeh_lights（reveal・山場のアクセント）。`loops`＝looping_gradient_navy / atmospheric_loop は章扉・抽象場面の動く背景。

### 7.3 取り込み例（select_factory_assets.py → factory/ へコピー）

```sh
# テーマ別b-roll動画（医療/検査）
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme medical_lab --kind video
# 金融（評価額崩落）
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme finance_money --kind video
# 書類/暴露
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme documents_paper --kind video
# 司法（山場SPN-0013）
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme legal_court --kind video
# 崩落/空虚の象徴
./.venv/Scripts/python.exe scripts/select_factory_assets.py --theme atmosphere_symbolic --kind video
# サブタイプ直指定の例
./.venv/Scripts/python.exe scripts/select_factory_assets.py --subtype stock_chart_crashing_red
./.venv/Scripts/python.exe scripts/select_factory_assets.py --subtype abandoned_factory_interior
```

抽出後 → `remotion/public/theranos/factory/` へコピーして `TheranosPremium` から参照。**`license` が allowed のものだけ**・出典/作者/sha256を `05_stock/stock_ledger.v001.json` に記録（VIDEO_RULES §5）。

### 7.4 合成指針（中立・R3・過剰回避）

1. **背景プレートは薄く**: backgrounds/loops を下地に置き、被写体（コード演出・テロップ・字幕）と**くっきり分離**（ベタ塗り回避）。意味グラフィックを邪魔しない。
2. **オーバーレイは screen/add**: light/vfx/particle を reveal・空気感に。**山場 SPN-0013（評決ボード）は `god_rays`＋`smoke_on_black` で“ため→開放”**、`LightSweep` 色＝GOLD と同期（§6）。1カット1〜2レイヤを目安・盛りすぎない。
3. **質感は overlay**: texture（aged_document_texture / film_grain_texture / blueprint_paper）を肩書きカード（0023）・書類（0007/0015）・等式（0018）の下地に薄く。
4. **R3＝実在人物想起素材は不可**: 実機（Edison）・実ロゴ・雑誌表紙・記者の顔・実写の人物・特定の本社/施設を想起させる素材は使わない。一般的な研究室（modern_medical_lab 等）・抽象・象徴のみ。**一般ストックを「その事件の実物」として提示しない**（illustrative/symbolic）。`symbolic reconstruction` ラベルはAI画像に常時。
5. **評決の区別を侵さない**: 投資家詐欺**4件＝GUILTY（事実として提示可）**／患者関連＝**ACQUITTED（無罪）**／3件＝**NO VERDICT（評決不成立）**。ファクトリの加飾（光・天秤・法廷b-roll）は**どの区別にも有罪のニュアンスを足さない**（0014は別色・GUILTY表記なし）。意図/認識は陪審・裁判所に帰属させ、加飾で断定有罪を演出しない。
6. **中立**: 「失敗 or 詐欺」に肩入れする加飾（崩落・破壊の過剰演出で詐欺側に寄せる等）をしない。崩落系（stock_chart_crashing_red / shattered_mirror）は記録事実（評価額の下落・解散）に対応する箇所のみ・象徴の範囲で。

---

## 完成定義（書き出し前に全✓・＋公開前法務レビュー）

書き出し前に**以下を全て満たす**こと（§4 品質ゲートと併用・本話はR3＝法務レビューを追加の最終ゲートとする）。

- [ ] **4部構成**：フック → オープニング → 本編（act1〜act4・台本順に再配列） → エンディングになっている（§1）。
- [ ] **coded/cards = 0**：全ショットが実素材／AI画像／コード演出（図解）で埋まり、空カード・プレースホルダがない（§4）。
- [ ] **全カットが動いている**：静止画ゼロ・Ken Burns 一辺倒でない・全カットに映画的カメラ（寄り/引き/パララックス＋spring/ease、リニア禁止）（§2・§6末尾）。
- [ ] **字幕がナレと語単位同期（ズレ≤約120ms）＆一字一句一致**、字幕／テロップ／出典／`symbolic reconstruction` ラベルが**位置で分離**し非重複（§3）。
- [ ] **音4層（VO/BGM/SFX/ambience）＋ダッキング**でナレ最優先・**−14 LUFS / true peak ≤ −1 dBTP**。**ナレ＝ElevenLabsで生成OK（課金承認待ち不要）**（§4・`06_audio/audio_cue_sheet.v001.md`）。
- [ ] **評決の区別を侵さない**：投資家詐欺**4件＝GUILTY（事実として提示可）**／患者関連＝**ACQUITTED（無罪）**／3件＝**NO VERDICT（評決不成立）**。「無罪 ≠ 潔白／技術が機能した」とは言わない。意図/認識は陪審・裁判所に帰属（§4・§5・§7.4）。
- [ ] **実在人物（Holmes / Balwani 等）を想起させる素材なし**：肖像・実写・ディープフェイク・実機（Edison）・実ロゴ・雑誌表紙・記者・特定の本社/施設を出さない。AI画像に `symbolic reconstruction` ラベル常時（§3・§5・§7.4）。
- [ ] **factory三層加飾**：①コード演出（主役・意味）／②AI画像（象徴・人物なし）／③ファクトリ（加飾・薄く1カット1〜2レイヤ）。license=allowed のみ・出典/sha256を `05_stock/stock_ledger.v001.json` に記録（§7・VIDEO_RULES §5）。
- [ ] **山場 SPN-0013** が“ため→開放”でSFX（gavel_knock＋low_boom）・`god_rays`＋`smoke_on_black`・`LightSweep`色=GOLD と同期（§6・§7.4）。
- [ ] **【不可侵】最終実尺＝690〜750秒（11.5〜12.5分・狙い約706秒）**。`scripts/check_runtime_band.py` が PASS（§1 秒バジェット通り：フック7＋ブリッジ1.5＋OP3.5＋本編612.4＋幕間40＋山場余韻10＋グラフの間15＋CTA8＋エンドカード9 ≈706秒）。フックは本編ハイライト約7秒（短く）。中立・台本/claims/shotlist 不改変（Read専用）。
- [ ] **公開前 法務レビュー（R3）を実施・記録（exact revision/hash）**。**法務レビュー記録なしに `publish_approved` へ進めない**（CLAUDE.md invariant 2、`.claude/rules/16-approval-boundaries.md`、VIDEO_RULES §6・§8）。← 本話の最終・不可侵ゲート。
