# EP39 — Frazier v. Cupp / 「警察は、取調べであなたに嘘をつけるのか？」— 制作設計書 ＋ Codex引き継ぎプロンプト

- **Episode ID:** `PD-2026-039-frazier` / slug `frazier` / EP39
- **バージョン:** v001（2026-07-19 作成）
- **Status:** 制作基盤 BINDING。**台本本文は別プロセスで並行制作中**。本書は台本に依存しない全工程を確定し、台本依存箇所は「スロット＋機械契約（JSON）」として厳密に定義する。
- **上位正典:** `docs/PD_WINNING_PATTERN.md`（成長・数値ゲート）/ `docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md`（1本の作り方・受入契約）/ `episodes/_planning/VIDEO_RULES.md`。衝突時は v2 のハードGATEが優先。
- **直近テンプレ:** `episodes/_planning/EP37_florence_DESIGN_and_CODEX_PROMPTS.md`（11–12分の構成の型）/ `episodes/_planning/EP38_kidsforcash_DESIGN_and_CODEX_PROMPTS.md`（AE hero-beat 初運用）。

---

## 0. 企画（確定・変更不可）

| 項目 | 確定値 |
|---|---|
| 中心の問い | **「警察は、取調べであなたに嘘をつけるのか？」**（二人称・自分事・司法の線引き＝勝ち型） |
| 答え | **合法**。`Frazier v. Cupp, 394 U.S. 731 (1969)` 以来、警察は**証拠について被疑者に嘘をついてよい**（共犯者が自白した、という虚偽の告知を用いた自白を、最高裁は「状況の総体」から任意と認定）。 |
| 語り口 | 制度解説ではなく**「一人の受難」**。嘘の取調べで、やっていない罪を自白した**実在人物1名**の物語。判例は「その人に何が起きたかを説明する装置」として後段に置く。 |
| 主役候補 | Brendan Dassey / Barry Laughman / Huwe Burton / Central Park Five（研究側で1名に確定。**確定するまで台本もheroビートの数値も埋めない**） |
| リスク区分 | **R2** — 実在私人が主役。**AI肖像禁止・匿名再現のみ・非グラフィック表現のみ**（§9 安全ルール） |
| 尺 | **11–12分**（許容band 11.5–12.5分 = `standard` duration profile） |
| 公開lane | 長尺（16:9）＋ 連動Short（縦9:16・35–45秒）1本 |

### 0.1 実測データ（設計の根拠。2026-07-18時点）

| 指標 | 実測 | 目標（フロア） | 本エピソードでの打ち手 |
|---|---|---|---|
| CTR（サムネ） | **2.31%** | **4.0%**（Good 6%） | §8 サムネ3案。全案「二人称の脅威1アイデア／4語以内／320pxで可読」 |
| 本編 APV | **15–25%** | **35%**（Good 45%） | 「一人の受難」型に振る（下表）＋ 再フック 2–3分毎 ＋ AE heroビートで山場を作る |
| 登録者増 | **+2** | subs/1,000再生 ≥ 5 | earned CTA（感情ペイオフ直後）＋ 終了画面 |
| コメント | **0** | ≥1件/本 | 固定コメントに問いを1つ投下（§11.4） |

**型の実測差（これが本設計の唯一最大の根拠）:**

| 型 | 該当話 | 視聴維持率 |
|---|---|---|
| 判例解説型 | Kelo / Mapp / Gideon | **1.6 – 7.5%** |
| 一人の受難型 | Rodriguez / Hinton / 没収 / Williams | **24 – 42%** |

→ **EP39 は 100% 一人の受難型で書く。** Frazier v. Cupp は「幕3で初めて出る答え」であり、幕1–2に判例名を出さない。冒頭で判例名を出した瞬間に解説型に落ちる（実測1.6–7.5%のレンジに入る）。

---

## 1. 尺と構成（確定・秒数固定）

総尺目標 **11:45（705秒）**、許容 11:30–12:30（690–750秒）。ナレ発話速度は**実測 178.1 wpm**（2026-07-19・31話のTTS実音声から測定）で計算する。

| # | ブロック | 開始 | 終了 | 長さ | 役割 |
|---|---|---|---|---|---|
| 0 | **HOOK** | 0:00 | 0:08 | 8s | 本編の最強ビート3–4本の高速フラッシュフォワード（各約2s）＋ナレ＋語同期字幕。**本編完成後に最後に組む。新規素材を作らない。** |
| 1 | **OPENING** | 0:08 | 0:12 | 3.5s | `BrandOpening`（`remotion/src/components/Bookends.tsx`・`OPENING_SEC=3.5`）。**フックの後**に置く。フォーク禁止（invariant 14）。 |
| 2 | **幕1 — その夜** | 0:12 | 2:50 | 158s | 主役の日常 → 任意同行 → 取調室の扉が閉まる。**まだ嘘は出さない。** |
| 3 | **幕2 — 嘘** | 2:50 | 6:10 | 200s | 警察が提示した「証拠」＝存在しない。反復・時間・孤立。自白へ折れる瞬間。**本編の感情の底。** |
| 4 | **幕3 — それは合法だった** | 6:10 | 9:00 | 170s | 転回。`Frazier v. Cupp (1969)` が初めて画面に出る。「なぜ止められなかったのか」の答え。 |
| 5 | **幕4 — あなたの番** | 9:00 | 11:05 | 125s | 射程の普遍化（虚偽自白の統計）＋ 主役のその後。earned CTA（感情ペイオフ直後・1つだけ）。 |
| 6 | **ENDING / ENDCARD** | 11:05 | 11:45 | 40s | `BrandEndcard`（`ENDCARD_SEC=9`）＋ 次回引き＋終了画面。 |

**再フック（必須・v2 row16）:** 2:45 / 5:20 / 7:40 / 9:50 の4点に「新しい問い or 転回」を置く。20秒以上の低テンションの平坦区間を作らない。
**カット切替:** 平均ショット長 **≤ 6.0秒**、目安 **4.5秒ごと**に別画像へ。単一静止の保持は **≤ 3.0秒**。

### 1.1 台本の語数（機械契約）★2026-07-19 実測にもとづき改訂（旧値は尺不足を再発させる）

**旧記述（1,773語 / band 1,700–1,860 / 173wpm）は使うな。** 2つの欠陥があった:
1. wpm が実測値でなかった。2026-07-19に **31話の実TTS音声**（`H:\pd-media\...\06_voice\draft\VC-*.mp3` の実時間）と台本語数を突き合わせた結果、**実測中央値 = 178.1 wpm**（範囲 163.7–237.4）。
2. 算数のずれ: 705 − (3.5+9+35) = **657.5秒**であって 615秒ではない。

**確定値: 目標 2,140語 / 許容band 2,048 – 2,226語。**

- 判定は `python scripts/check_script_length.py <script>` が唯一の正。自己申告・体感は禁止。
- このゲートは総尺(690–750s)を丸ごとナレ時間として計算する。実測の非ナレ余剰は約20秒（EP38: VO 543.5s → 完成 563.9s）なので、**約60語ぶん厳しめに出る**。尺不足が本チャンネル最大の反復失敗である以上、長い側に倒すのは意図的。
- **根拠**: 過去38話中30話が宣言した目標尺に未達。EP009–015は1,503–1,565語で8.4–8.8分、EP38は1,675語で**9.4分**（ゲートの予測9.4分と実測9.40分が一致）。1,700–1,860語帯で書くと**必ず**10分台前半で終わる。
- **水増し禁止**: 言い換え反復・冗長な接続・無意味な間で語数を稼ぐのは `check_padding` でFAILする。増やすのは中身だけ — 場面のディテール、二つ目の事例、その後の人生、反対意見の論理、制度の仕組み、数字の出所。

---

## 2. 台本スロット契約（台本確定後に機械的に埋まる。ここが本書の核）

台本は別プロセス。**本書は「どのファイルに、どの形で、何が入るか」を先に固定する。** 台本担当は下の契約を満たすファイルを出すだけでよく、Codexは契約が満たされた瞬間に何も相談せず着手できる。

### 2.1 成果物ファイル一覧（パスとバージョンは固定）

| # | ファイル | 生成者 | Codexの依存 |
|---|---|---|---|
| S1 | `episodes/PD-2026-039-frazier/03_script/EP39_FILM_BIBLE.v001.md` | 台本プロセス | 参照のみ |
| S2 | `episodes/PD-2026-039-frazier/03_script/script.en.v001.md` | 台本プロセス | **必須** |
| S3 | `episodes/PD-2026-039-frazier/03_script/script.annotated.v001.json` | 台本プロセス | **必須**（TTS・字幕・shotlistの入力） |
| S4 | `episodes/PD-2026-039-frazier/03_script/fact_recheck.v001.json`（claim台帳） | 台本プロセス | **必須**（heroビート数値の出典） |
| S5 | `episodes/PD-2026-039-frazier/04_scenes/shotlist.v001.json` | Codex（S3から生成） | 生成物 |
| S6 | `episodes/PD-2026-039-frazier/04_scenes/hero_beats.spec.v001.json` | 台本プロセス＋研究 | **必須**（AE heroビートの数値） |
| S7 | `episodes/PD-2026-039-frazier/04_scenes/ai_prompts.v001.md` | **本書 §9 が正典**（もう確定済み） | 依存なし・即着手可 |
| S8 | `episodes/PD-2026-039-frazier/04_scenes/thumb_prompts.v001.md` | **本書 §8 が正典**（もう確定済み） | 依存なし・即着手可 |

### 2.2 `script.annotated.v001.json` の契約（厳密）

```jsonc
{
  "episode_id": "PD-2026-039-frazier",   // 固定文字列。一致しなければFAIL
  "slug": "frazier",
  "target_duration_minutes": 11.75,
  "duration_profile": "standard",         // 11.5-12.5 band
  "wpm_assumed": 178.1,               // 実測中央値(31話)。推定値に戻すな
  "total_words": 2140,                    // 2048 <= x <= 2226 でなければFAIL (check_script_length.py)
  "sections": [
    {
      "role": "hook",                     // enum: hook|opening|body|ending （4つ全部が1回以上必要・この順）
      "act": null,                        // body のとき 1|2|3|4、それ以外 null
      "beats": [
        {
          "beat_id": "B001",              // ^B[0-9]{3}$ 通し・欠番禁止
          "text": "...",                  // ナレ逐語。TTSに渡る唯一の真実。生成後は一字も変えない
          "words": 23,                    // text の語数（半角空白split）。不一致ならFAIL
          "est_sec": 7.75,                // words / 178.1 * 60。±0.05 以内
          "visual_question": "...",       // この文は何を見せるべきか（1文）
          "visual_verb": "...",           // reveal|close|approach|tick|split|collapse|rise|hold のいずれか
          "start_state": "...",           // 画の開始状態（1文）
          "end_state": "...",             // 画の終了状態（1文）
          "eye_target": "...",            // 視線誘導先（画面座標の語: center|lower-left|upper-right 等）
          "sync_words": ["lied", "confessed"],  // 語同期でリビールを合わせる語。0-3語
          "source_type": "ai_still|factory_clip|mg_card|ae_hero|blender",
          "truth_status": "verified|attributed|characterization",  // 3値のみ
          "claim_ids": ["C-039-014"],     // fact_recheck の claim_id。verified の beat は 1個以上必須
          "on_screen_text": null           // 画面テロップ（上部/中央ゾーン）。無ければ null
        }
      ]
    }
  ]
}
```

**バリデーション（Codexが着手前に必ず実行する自作チェックではなく、既存ゲートに接続する）:**
- `role` は hook→opening→body→ending の順に少なくとも1回ずつ出現（v2 row10 `structure_4part`）。
- hook セクションの `est_sec` 合計 = **6.0–10.0秒**（v2 row9 `hook_added`）。
- hook で teased した reveal が body/ending に必ず出現（promise-payoff）。
- 全 beat の `est_sec` 合計が 600–630秒。
- `truth_status = "verified"` の beat は `claim_ids` 非空。争点は `attributed`（多数意見/反対意見/検察側/弁護側と帰属）。

### 2.3 `fact_recheck.v001.json`（claim台帳）の契約

```jsonc
{
  "episode_id": "PD-2026-039-frazier",
  "risk_tier": "R2",
  "subject_real_person": true,
  "claims": [
    {
      "claim_id": "C-039-001",            // ^C-039-[0-9]{3}$
      "statement": "...",                  // 1文・逐語
      "value": 394,                        // 数値クレームなら数値、それ以外 null
      "unit": "US",                        // "years"|"hours"|"percent"|"USD"|"count"|"US"|null
      "source_title": "Frazier v. Cupp, 394 U.S. 731 (1969)",
      "source_url": "https://...",         // 一次資料優先（判決文・公的統計・報道1次）
      "source_date": "1969-04-22",
      "verified_by": "primary|secondary",  // secondary は2件以上必要
      "disputed": false,
      "attribution": null                  // disputed=true のとき "majority"|"dissent"|"prosecution"|"defense" 必須
    }
  ]
}
```

**固定claim（研究不要・本書で確定済み。台本担当はそのまま台帳に転記せよ）:**

| claim_id | statement | value / unit | source |
|---|---|---|---|
| `C-039-001` | 米最高裁は Frazier v. Cupp において、取調官が「共犯者が既に自白した」と虚偽を告げたうえで得られた自白を、状況の総体から任意であると判断した。 | — | Frazier v. Cupp, 394 U.S. 731 (1969) |
| `C-039-002` | 同判決の合衆国判例集の巻号は 394 U.S. 731、判決年は 1969年。 | 1969 / year | 同上 |

> それ以外の全数値（取調べ時間・年齢・服役年数・虚偽自白率 等）は**主役確定後に研究側が台帳に足す**。本書は数値を書かない（存在しない事実を書かないため）。

### 2.4 差し込みの機械手順（台本確定後、Codexが実行する順）

1. `script.annotated.v001.json` の `text` を連結 → ElevenLabs（`VOICE_ID=nPczCjzI2devNBz1zQrb`, `eleven_multilingual_v2`, stability 0.35 / similarity_boost 0.80 / style 0 / speaker_boost on）でナレ生成。**SAPI/ローカルは出荷禁止。**
2. レンダ済みナレ音声に **forced alignment**（`faster-whisper` 語タイム）→ `04_scenes/captions.final.v001.{srt,json,ass}`。字幕は台本からのコピペ禁止、**発話音声に整列**（v2 row3・トークン一致 ≥99%）。
3. 語タイムから各 `beat_id` の実 `start`/`end`（秒）を確定 → `shotlist.v001.json` を生成。
4. **`hero_beats.spec.v001.json` の `anchor_phrase` を語タイム列に対して逐語一致検索** → 各heroビートの `start` を確定、`end = start + dur`（§3.3のアルゴリズム）。
5. `scripts/ae/build_frazier_hero_jsx.py` → `hero_beats.v001.json`（派生）＋ `frazier_hero.jsx` を生成。
6. Remotion 本編レンダ → 音声mux → **その完成mp4に AE heroビートを ffmpeg overlay**（§3.5）。

---

## 3. After Effects heroビート設計（本エピソードの主要要求）

### 3.1 パイプラインの原則（EP38で実測確立・2026-07-18。これに従う）

1. **Remotion で本編を作り、その完成 mp4 に AE製データカードを ffmpeg で overlay する。Remotion を再レンダしない。**
2. 各beat = **1920x1080 @ 30fps** の AEコンプ。中身（下から順）:
   黒bg → イーズ付きプッシュイン静止画 → クールグレード（multiply 38%）→ 羽根付き楕円ビネット（feather 260 / opacity 62 / SUBTRACTマスク）→ 金グロー（Ramp・ADD）→ ライトスイープ（白ソリッド360×H*1.6・Rotate Z 18°・ADD）→ 上ラベル（Oswald 44 / silver / tracking 340）→ 金アクセントライン（460×6・scaleXワイプ）→ **大数字（Anton 250 / gold / カウントアップ ＋ scaleオーバーシュート ＋ motionBlur）** → 下ラベル（Oswald 64 / white / tracking 120）→ ナレ字幕ロワーサード（暗バー W×130 / opacity 64 ＋ Oswald 42）→ **4フレームの黒シームdip**（head/tail）
3. **不透明フルフレームで書き出し**、ナレ区間に `enable='between(t,start,end)'` で重ねる。**元の図版を完全置換＝二重描画なし。音声は `-c:a copy`。**
4. **Python が .jsx を生成する**（全数値をPython側で制御）。**数値カウントのキーフレーム文字列は Python で全事前計算**（JS側で数値整形しない）。
5. **`hero_beats.v001.json` サイドカーが jsx とコンポジタの両方を駆動する**（単一の真実）。
6. **コンポジタは mp4 が欠損／サイズ違い／短尺の beat を SKIP する**（その区間は元のまま＝作品が壊れない）。
7. **出荷済みファイルを絶対に上書きしない**（`frazier_final_bgm.v002.mp4` → `frazier_final_bgm.v003_ae.mp4`）。

### 3.2 heroビート スロット設計（**8スロット**：必須6＋条件付き2）

数値は台本・研究確定後に `hero_beats.spec.v001.json` に入る。**本書はスロットの「意味・レイアウト・カウント型・区間長・配置」を確定する。**

| slot | 配置(幕) | 見せる数値のカテゴリ | layout | カウント型 | 区間長 | 必須 |
|---|---|---|---|---|---|---|
| `HB1_INTERROGATION_LENGTH` | 幕2 前半 | 取調べの**継続時間**（時間 or 分） | `A_BIG_NUMBER` | 0 → target / ease-out / suffix `" HOURS"` | **6.0s** | ✅必須 |
| `HB2_SUBJECT_VULNERABILITY` | 幕1 後半 | 主役の**年齢**（または該当すれば IQ / 学年） | `A_BIG_NUMBER` | 0 → target / suffix `" YEARS OLD"` | **5.5s** | ✅必須 |
| `HB3_THE_LIE` | 幕2 中盤（本編の底） | 警察が提示した**存在しない証拠の件数**（＝嘘の回数） | `B_SPLIT_RATIO` | 左=提示件数(0→N) / 右=実在件数を `0` に固定表示 | **6.5s** | ✅必須 |
| `HB4_THE_CASE` | 幕3 冒頭（転回点） | **`394 U.S. 731` / `1969`** — Frazier v. Cupp の判例番号と年 | `D_CITATION_STAMP` | 年のみ 0→1969（thousands=false・4桁ロールアップ） | **6.0s** | ✅必須 |
| `HB5_YEARS_LOST` | 幕3 後半 | 主役が**失った年数**（服役年数 or 拘束年数） | `A_BIG_NUMBER` | 0 → target / suffix `" YEARS"` | **6.0s** | ✅必須 |
| `HB6_FALSE_CONFESSION_RATE` | 幕4 前半（普遍化） | DNA免罪事件のうち**虚偽自白が関与した割合** | `C_PERCENT_ARC` | 0 → target% ／ 背後で円弧が同期して伸びる | **6.5s** | ✅必須 |
| `HB7_DECISION_VOTE` | 幕3 中盤 | Frazier判決の**票数**（例 `9–0`） | `E_VOTE_TALLY` | 票マーカーを 0.08s スタッガーで着地 | **5.5s** | ⭕条件付き（台帳で票数が確定した場合のみ） |
| `HB8_EXONERATION_YEAR` | 幕4 後半 | **免罪・釈放の年**（主役に該当する場合） | `D_CITATION_STAMP` | 年のみ 0→YYYY | **5.5s** | ⭕条件付き（主役が免罪済みの場合のみ） |

**合計** 必須6本 = 36.5秒 / 全8本 = 47.5秒（本編705秒の 5.2–6.7%）。

**配置制約（機械チェック可能・違反はFAIL）:**
- `start ≥ 20.0`（HOOK 0–8s と OP 8–11.5s に絶対に置かない）
- `end ≤ (総尺 − 25.0)`（ENDCARD区間に置かない）
- 任意の2ビートの間隔 **≥ 20.0秒**（連続で数字カードが出るのを禁止）
- 各ビートは `truth_status="verified"` かつ `claim_ids` 非空のナレビート上にのみ載る

### 3.3 レイアウト仕様（`layout` enum・数値まで確定）

共通: 1920×1080@30fps / 色 `GOLD=[0.898,0.710,0.227]` `WHITE=[0.961,0.969,0.980]` `SILVER=[0.588,0.627,0.682]` / フォントは実行時に `app.fonts.allFonts` から解決（Anton regular / Oswald medium。**サイレント代替を許さない**）。

**共通タイムライン（コンプローカル秒。`dur` はスロット表の区間長）**

| t | 出来事 |
|---|---|
| 0.000 | 黒dip 100% → `head = 4/30 = 0.1333s` で 0%（ease 40） |
| 0.000 → dur | 静止画 scale `fill` → `fill*1.08`（ease 25）／ position `[W/2−18, H/2+10]` → `[W/2+18, H/2−10]`（ease 20） |
| 0.150 | 上ラベル `revealUp`：position y+46 → y（0.5s・ease 80）＋ opacity 0→100（0.4s・ease 70） |
| 0.450 | 大数字 opacity 0 → 100（0.12s） ※`numReveal = t_num0 − 0.10` |
| 0.500 → 1.250 | ライトスイープ position `[-300, H/2]` → `[W+300, H/2]`（ease 45）／ opacity 0→18→0 |
| 0.550 → 1.050 | 金アクセントライン scaleX 0 → 100（ease 90・motionBlur ON） |
| **0.550 → 1.550** | **数値カウントアップ**（18キー・`ease_out_cubic` / hold補間 / +0.02s で target に着地して保持） |
| 0.550 / 0.900 / 1.200 | 数字 scale `42` → `112` → `100`（オーバーシュート・ease 75・motionBlur ON） |
| 0.000 / 0.700 / dur | グロー opacity 0 → 22 → 14（ease 60） |
| 1.150 | 下ラベル `revealUp`（同上） |
| 0.200 / 0.500 / dur−0.4 / dur−0.1 | 字幕バー opacity 0 → 64 → 64 → 0 |
| 0.300 / 0.600 / dur−0.4 / dur−0.12 | 字幕テキスト opacity 0 → 100 → 100 → 0 |
| dur−tail | 黒dip 0% → `tail = 4/30 = 0.1333s` かけて 100%（ease 40） |

**レイアウト別の差分:**

- **`A_BIG_NUMBER`** — 基準形。大数字を `[W/2, H*0.42]`、上ラベル `H*0.205`、アクセント線 `H*0.485`、下ラベル `H*0.60`、字幕バー `H*0.90`。
- **`B_SPLIT_RATIO`** — 大数字を2つ。左 `[W*0.30, H*0.42]`（fontSize 210・GOLD・カウントアップ）／右 `[W*0.70, H*0.42]`（fontSize 210・SILVER・`"0"` 固定）。中央に縦の分割線ソリッド `6×H*0.30` を `[W/2, H*0.42]`、scaleY 0→100（0.40→0.85s・ease 90）。上ラベルは左右それぞれ `H*0.255` に fontSize 36 で配置（左=「CLAIMED」相当、右=「THAT EXISTED」相当。文字列は spec の `top` / `top2`）。
- **`C_PERCENT_ARC`** — 大数字（suffix `"%"`）の背後に円弧。白ソリッド（W×H）＋ `ADBE Vector Group` ではなく**楕円マスク差分は使わず**、`ADBE Radial Wipe`（matchName `ADBE Radial Wipe`）を金ソリッドに適用し `Transition Completion` を `100 → (100 − target)` へ 0.55→1.55s で ease 75。円の中心 `[W/2, H*0.42]`、金ソリッドは `ADBE Ellipse`不使用・**マスク楕円 rx=ry=300・feather 0・SUBTRACTで内側を抜いてリング化**（線幅 = 外径600 / 内径540）。
- **`D_CITATION_STAMP`** — 年を大数字（thousands=false・4桁）。その下 `H*0.545` に fontSize 56 / SILVER / tracking 180 で判例引用文字列（spec の `bottom`）。カウント終了 1.60s で**スタンプ打刻**：引用文字列 scale `130 → 100`（1.60→1.78s・ease 85）＋ opacity 0→100（1.60→1.70s）＋ その瞬間に金アクセント線を再度 scaleX 100→104→100（0.12s）。
- **`E_VOTE_TALLY`** — 数字は `"9–0"` を**文字列固定**（カウントアップしない）。上に票マーカー：金の丸ソリッド（直径 56）を `value` 個、`[W/2 − (n−1)*40 + i*80, H*0.30]` に並べ、i番目を `0.55 + i*0.08` 秒に scale `0 → 118 → 100`（3キー・ease 80・motionBlur ON）で着地。反対票は SILVER 丸で右端に続ける。

### 3.4 `hero_beats.spec.v001.json` の契約（台本側が埋める入力）

```jsonc
{
  "episode_id": "PD-2026-039-frazier",
  "fps": 30,
  "beats": [
    {
      "id": "hb01",                        // ^hb[0-9]{2}$ 通し・欠番禁止
      "slot": "HB1_INTERROGATION_LENGTH",  // §3.2 の slot enum。必須6スロットは全て存在必須
      "layout": "A_BIG_NUMBER",            // A_BIG_NUMBER|B_SPLIT_RATIO|C_PERCENT_ARC|D_CITATION_STAMP|E_VOTE_TALLY
      "dur": 6.0,                          // §3.2 の区間長。5.0 <= dur <= 6.5
      "anchor_phrase": "for forty-eight hours",  // script.annotated の text 内に逐語で1回だけ存在すること
      "anchor_align": "start",             // start|end。start=語の開始でビート開始
      "still": "S07",                      // §9 の SPN-ID。generated_images/<ID>.png が存在すること
      "top": "IN THAT ROOM",               // ASCII大文字・<=18文字
      "top2": null,                        // layout=B のときのみ必須・<=18文字
      "bottom": "NO LAWYER PRESENT",        // ASCII大文字・<=22文字
      "value": 48,                          // number。layout=E のときは反対票数を value2 に
      "value2": null,                       // layout=B/E のとき必須
      "decimals": 0,                        // 0|1
      "thousands": false,                   // bool
      "prefix": "",                         // "" | "$"
      "suffix": " HOURS",                   // <=12文字
      "claim_id": "C-039-014",              // 必須・null禁止。fact_recheck に存在すること
      "start": null,                        // 生成時に anchor から解決。手書き禁止（nullで出す）
      "end": null
    }
  ]
}
```

**アンカー解決アルゴリズム（`build_frazier_hero_jsx.py` が実装）:**
1. `captions.final.v001.json` の語タイム列を連結し、`anchor_phrase` を正規化（小文字化・句読点除去・連続空白1つ）して逐語検索。
2. **ヒット0件 or 2件以上 → そのビートを `unresolved` として出力し FAIL を返す**（推測で置かない）。
3. `anchor_align="start"` → `start = 一致語列の先頭語の開始秒 − 0.25`。`"end"` → `start = 一致語列の末尾語の終了秒 − dur + 0.35`。
4. `end = start + dur`。§3.2 の配置制約（≥20s / ≤総尺−25s / 相互間隔≥20s）を検証。違反は FAIL。
5. 字幕1行は `nearest_caption(start,end)` → `one_line(maxchars=50)`。**改行文字を絶対に含めない**（AEのTextDocumentは `\n` を文字通り描画する）。

### 3.5 実行手順（このマシンの実パス。コマンドは確認済みの実在物のみ）

```bash
# 1) 生成（Python が jsx と派生 json を書く。AEはまだ起動しない）
py -3.11 C:/Users/aab15/Documents/prime-documentary/scripts/ae/build_frazier_hero_jsx.py

# 2) ビルド（AfterFX でコンプ作成 → .aep 保存 → app.quit()）
#    jsx 末尾が render/_build_ok.txt を書く。これをポーリングする。早期killしない。
"/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/AfterFX.com" -noui -r \
  "C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-039-frazier/08_edit/ae_hero/frazier_hero.jsx" &

# 3) 書き出し（レンダーキューを丸ごと）
"/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/aerender.exe" \
  -project "C:/.../08_edit/ae_hero/frazier_hero.aep"

# 4) 合成（完成mp4に overlay。音声は copy。別名出力）
py -3.11 C:/Users/aab15/Documents/prime-documentary/scripts/ae/composite_frazier_hero.py \
  "C:/.../08_edit/frazier_final_bgm.v002.mp4" \
  "C:/.../08_edit/frazier_final_bgm.v003_ae.mp4"
```

**参照する既存実装（実在確認済み・そのまま雛形にする）:**
- `scripts/ae/build_kfc_hero_jsx.py` — jsx生成・`count_keys()`・`ease()`（spatial判定）・フォント解決・OM/RSテンプレ適用・完了マーカー書き出し。
- `scripts/ae/composite_kfc_hero.py` — ffmpeg overlay・SKIPロジック・duration検証。
- `scripts/ae/apply_kfc_fixes.py` / `scripts/ae/plan_kfc_factory_swap.py` — 補助。
- `episodes/_planning/ae_hero/run_hero.sh` / `render_all_heroes.sh` — 起動・ポーリング・taskkill・ffprobe検証の手順（※スクラッチパスは旧いので必ず張り替える）。

### 3.6 このマシン固有の罠（**Codexが踏まないための注意・全部実測**）

| # | 罠 | 対処（そのまま実装せよ） |
|---|---|---|
| 1 | 環境 | AE **2026**・**日本語ロケール**・RTX4090。実行体は `/c/Program Files/Adobe/Adobe After Effects 2026/Support Files/` の `AfterFX.com`（ビルド用）と `aerender.exe`（書き出し用）。 |
| 2 | **イーズが無言で効かず等速になる** | `setTemporalEaseAtKey` は Position など **spatial プロパティでは要素1個の配列**。`var dim = prop.isSpatial ? 1 : (prop.value instanceof Array ? prop.value.length : 1);` で次元を決める。間違えるとエラーも出ずリニアになる。 |
| 3 | **テンプレ名がローカライズ済み** | 有効値は RS `"最良設定"` / OM `"H.264 - レンダリング設定を一致 - 15 Mbps"`。**英語名（"Best Settings" / "H.264 - Match Render Settings - 15 Mbps"）は失敗する**。try/catch で英語名にフォールバックしてよいが、日本語名を先に試すこと。 |
| 4 | **字幕の改行** | AE の `TextDocument` の改行は `\n` **ではない**。**字幕は必ず1行に保つ**（`one_line(maxchars=50)`）。どうしても改行するなら `\r`。 |
| 5 | **`app.newProject()` は headless (`-noui`) でハングする** | 使うな。代わりに既存の同名コンプを防御的に削除する（`for (i=proj.numItems; i>=1; i--) if (item instanceof CompItem && name.indexOf("FRZ_")===0) item.remove();`）。 |
| 6 | **ビルドは遅い / レンダは速い** | ビルド ~100–120秒、レンダは 6コンプ ~21秒。**jsx が書く完了マーカー（`render/_build_ok.txt`）をポーリングせよ。早期killするな。** |
| 7 | 起動方式 | AfterFX / aerender は**デタッチ起動＋出力ファイルのポーリング**。jsx の末尾で必ず `app.quit()`。強制終了後のクラッシュ修復ダイアログが次回起動を全ブロックするので、正常終了させる。 |
| 8 | **モーションブラー** | `layer.motionBlur = true` を**レイヤー個別に**設定する。コンプの `comp.motionBlur = true` だけでは無効。数字レイヤー・アクセント線・票マーカーに必須。 |
| 9 | **2Dレイヤーの回転** | `"ADBE Rotation"` は **null** を返す。`"ADBE Rotate Z"` を使え（ライトスイープの18°）。 |
| 10 | **レイヤーの outPoint** | `inPoint` だけ設定すると `outPoint` がコンプ末尾に残る。**両方設定せよ。** |
| 11 | **画像シーケンスのfps** | AE は画像シーケンスを prefs 既定の 30fps で読む。`item.mainSource.conformFrameRate = FPS` が無いと**全ビートの timing が無言でズレる**。単一 PNG でも明示せよ。 |
| 12 | GPU不安定 | `proj.gpuAccelType = GpuAccelType.SOFTWARE;` / `proj.bitsPerChannel = 8;` を try/catch で設定（EP38で安定確認済み）。 |
| 13 | 残留プロセス | aerender 前に `taskkill //F //IM AfterFX.com` `//IM AfterFX.exe` で残骸を落とす。 |
| 14 | 数値整形 | **JS側で数値を整形しない。** カウントアップの全キー文字列を Python の `fmt_number()` / `count_keys()` で事前計算して jsx に埋め込む。 |
| 15 | 上書き | **出荷済みファイルを絶対に上書きしない。** 出力は必ず `*_v003_ae.mp4` の新規版名。 |

---

## 4. OPENING（オープニング）設計 — 完全仕様

> **本セクションは Codex がこれだけを読んで実装できる粒度で書かれている。** 正典実装のお手本は `C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx`（読み込み済み）。本設計はその構造を踏襲し、**数値のみ EP39 用に差し替える**。

**重要な境界（invariant 14 との整合）:** 本編タイムライン内の OP/ED は `remotion/src/components/Bookends.tsx` の `BrandOpening` / `BrandEndcard` が引き続き**唯一の正典**であり、フォークしない。本セクションで作る `Frazier39Opening` は **独立した 60fps タイトルカード資産**（サムネ動画・Short用リード・A/B用の別レンダ）であり、`CaseFilm` のタイムラインに差し込まない。よって `op_ed_bookends` ゲートは緑のまま保たれる。

### 4.0 環境・Remotion設定

**Composition 設定（`remotion/src/Root.tsx` に追加。既存 id `Opening` は使用済みのため衝突させない）:**

```tsx
import {Frazier39Opening, frazier39OpeningDurationInFrames} from './compositions/Frazier39Opening';

<Composition
  id="Frazier39Opening"
  component={Frazier39Opening}
  durationInFrames={180}        // = 3.0s @ 60fps
  fps={60}
  width={1920}
  height={1080}
  defaultProps={{
    title: 'THEY CAN LIE',
    subtitle: 'FRAZIER V. CUPP · 1969',
    accent: '#E5B53A',
    hasLogo: true,
  }}
/>
```

- 解像度 **1920×1080** / **fps 60** / **durationInFrames 180**（=3.0秒）/ id **`Frazier39Opening`**
- ファイル: `remotion/src/compositions/Frazier39Opening.tsx`（新規。既存 `compositions/Opening.tsx` を書き換えない）

**必要な依存パッケージ（`remotion/` 直下で実行）:**

```bash
npm i @remotion/motion-blur
```

> 現状 `remotion/package.json` には `@remotion/motion-blur@^4.0.476` が既に入っている。バージョン不整合時のみ上記を実行する（`remotion` 本体と同じメジャー系に揃えること）。

**`remotion/remotion.config.ts` の内容（既に正典値。**変更するな**。以下と一致していることを確認せよ）:**

```ts
import {Config} from '@remotion/cli/config';
import os from 'os';

Config.setVideoImageFormat('png');                 // 中間フレームはロスレスPNG
Config.setCodec('h264');                           // libx264 / CPU（NVENC禁止）
Config.setCrf(16);                                 // CRF 16（視覚的ロスレス）
Config.setX264Preset('slow');
Config.setPixelFormat('yuv420p');
Config.setColorSpace('bt709');
Config.setAudioCodec('aac');
Config.setAudioBitrate('320k');
Config.setConcurrency(os.cpus().length);           // 全コア並列・concurrency最大
Config.setChromiumOpenGlRenderer('angle');         // GPU = angle
Config.setOverwriteOutput(true);
```

### 4.1 秒数ベースのタイムライン（全区間・fps=60 / 総尺 3.0s = 180F）

| 秒 | フレーム | 起きること |
|---|---|---|
| **0.00 – 0.50** | 0–30 | レイヤー1 グラデ背景がフェードイン（opacity 0→1、0.00–0.40s / F0–24）。同時に**背景全体が scale 1.08 → 1.00 へ 3.0秒かけてゆっくり縮む**（`Easing.out(Easing.cubic)`・F0–180）。0.10s（F6）でロゴが scale 0.40→1.00 の spring 開始。0.15s（F9）でレイヤー2グリッドが spring reveal 開始（0.8s=48F）。0.25s（F15）でレイヤー3グローが spring 開始（scale 0.60→1.15 / opacity 0→0.85）。0.30s（F18）で**タイトル1文字目**がマスク下から切れ上がり開始。 |
| **0.50 – 1.00** | 30–60 | タイトルの各文字が **0.04s（=2.4F→切り上げ3F）ごとのスタッガー**で順に切れ上がる（各文字 spring `damping:16, mass:1`、translateY 110%→0%）。`Trail`（layers 6 / lagInFrames 1.2 / trailOpacity 0.45）により速い切れ上がりにモーションブラーが乗る。グリッドは 0→48px の縦ドリフト（`Easing.inOut(Easing.sin)`・F0–180）を継続。 |
| **1.00 – 1.40** | 60–84 | 0.95s（F57）で**金アクセント下線が左から scaleX 0→1 でワイプ**（spring `damping:16, mass:0.8`）。1.10s（F66）で**サブタイトル**が translateY 24px→0px ＋ opacity 0→1（spring `damping:20, mass:1`）。 |
| **1.40 – 2.20** | 84–132 | 全要素が定常。背景 scale と グリッドドリフトだけが動き続ける（画面は一瞬も静止しない）。**1.60s（F96）で背景に薄い紺のフラッシュ（opacity 0→0.10→0、F96–108、`Easing.out(Easing.cubic)`）を1回だけ入れて「取調室の扉が閉まる」拍を作る。** |
| **2.20 – 3.00** | 132–180 | 保持。**2.70s（F162）から全体を scale 1.00→1.02（`Easing.out(Easing.cubic)`・F162–180）で微かに押し込む**＝次カットへの運動量継承（velocity reset を作らない）。opacity は落とさない（本編側のクロスディゾルブ 0.4s が受ける）。 |

### 4.2 各要素のイージング・ディレイ・移動量・damping（確定値）

**タイミング定数（すべて秒。フレーム直書き禁止。`sec(fps,s)=Math.round(fps*s)` で変換）:**

```ts
export const frazier39OpeningDurationInFrames = (fps: number) => Math.round(fps * 3.0); // 180 @60fps

const T = {
  bgIn: 0.00,        // 背景フェード/ズーム開始
  logoIn: 0.10,      // ロゴ
  gridIn: 0.15,      // グリッド出現
  glowIn: 0.25,      // グロー出現
  titleIn: 0.30,     // タイトル切れ上がり開始
  charStagger: 0.04, // 1文字ごとのディレイ（@60fps → 2.4F、Math.max(1,...) で3F）
  accentIn: 0.95,    // アクセント下線ワイプ
  subIn: 1.10,       // サブタイトル
  flashAt: 1.60,     // 紺フラッシュ（EP39固有）
  pushAt: 2.70,      // 終端の押し込み（EP39固有）
} as const;
```

| 要素 | 開始F(@60) | 終了F | 変化量 | イージング |
|---|---|---|---|---|
| 背景 scale | 0 | 180 | `1.08 → 1.00` | `Easing.out(Easing.cubic)` |
| 背景 opacity | 0 | 24 | `0 → 1` | interpolate（**必ず scale と併用。opacity単独禁止**） |
| グリッド translateY | 0 | 180 | `0 → 48px` | `Easing.inOut(Easing.sin)` |
| グリッド reveal | 9 | 57 | `0 → 1`（最終 opacity は `reveal * 0.18`） | `spring{damping:200, mass:1}` / `durationInFrames = sec(fps,0.8)` |
| グロー scale | 15 | — | `0.60 → 1.15` | `spring{damping:18, mass:1.2}` |
| グロー opacity | 15 | — | `0 → 0.85` | 同 spring（scale と同期＝単独禁止） |
| タイトル各文字 translateY | `18 + i*3` | — | `110% → 0%` | `spring{damping:16, mass:1}` |
| タイトル各文字 opacity | `18 + i*3` | +約6F | `0 → 1`（spring値 0→0.25 を 0→1 にマップ・clamp） | 同 spring |
| タイトル Trail | 全域 | — | `layers=6 / lagInFrames=1.2 / trailOpacity=0.45` | — |
| アクセント下線 scaleX | 57 | — | `0 → 1`（`transformOrigin:'left center'`） | `spring{damping:16, mass:0.8}` |
| サブタイトル translateY | 66 | — | `24px → 0px` | `spring{damping:20, mass:1}` |
| サブタイトル opacity | 66 | — | `0 → 1` | 同 spring（translateY と併用） |
| ロゴ scale | 6 | — | `0.40 → 1.00` | `spring{damping:14, mass:0.9}` |
| ロゴ opacity | 6 | — | `0 → 1` | 同 spring |
| 紺フラッシュ opacity | 96 | 108 | `0 → 0.10 → 0` | `Easing.out(Easing.cubic)` |
| 終端押し込み scale | 162 | 180 | `1.00 → 1.02` | `Easing.out(Easing.cubic)` |

**禁止事項の再掲（実装時に自己チェック）:** 等速線形 `interpolate` を**イージング指定なしで**使わない（背景 opacity のような 0→1 の短いフェードも、必ず同時に走る scale/translate と対で成立させる）。`opacity` だけが変化する要素を作らない。複数要素は必ずスタッガー。速い動きには `Trail`。

### 4.3 レイヤー構成（下から上。**主役の裏に最低3レイヤー**）

| z | レイヤー | 内容 |
|---|---|---|
| 0 | ベース | `AbsoluteFill` `backgroundColor: '#05070d'` |
| **1** | **グラデ背景** | `radial-gradient(120% 120% at 50% 35%, #0E1B33 0%, #0A1020 45%, #05070d 100%)`（PDブランドの navy `#0B1A2B` に寄せた値）。scale 1.08→1.00。 |
| **2** | **グリッド/ライン** | `repeating-linear-gradient` 縦横 1px / 間隔 **64px** / 色 `${accent}22`。全体 opacity = `gridReveal * 0.18`。`maskImage: radial-gradient(120% 90% at 50% 45%, black 35%, transparent 80%)`。translateY 0→48px。 |
| **3** | **グロー** | 中央に `width = W*0.62` `height = H*0.36` の `radial-gradient(closest-side, ${accent}88 0%, ${accent}22 45%, transparent 75%)` ＋ `filter: blur(28px)`。scale 0.60→1.15。 |
| **3.5** | **紺フラッシュ**（EP39固有） | 全面 `#0B1A2B`、F96–108 のみ opacity 0→0.10→0。 |
| **4** | **主役タイトル** | `Trail` 内に `AbsoluteFill`（中央寄せ再指定）→ flex 横並びの1文字 `<span>`。外側 span `overflow:hidden` ＋ `paddingBottom:'0.12em'`、内側 span `transform: translateY(${y}%)`。`fontFamily:'"Oswald","Archivo",Impact,sans-serif'`（BRAND.font.display）/ `fontWeight:800` / `fontSize:132` / `letterSpacing:-2` / `color:#F5F7FA` / `lineHeight:1.05` / `transform:'translateY(-70px)'`。 |
| **5** | **アクセント下線＋サブタイトル** | 縦並び（`gap:18`・`transform:'translateY(55px)'`）。下線＝`240×6`・`borderRadius:3`・`backgroundColor:accent`・`boxShadow:'0 0 24px ' + accent + 'aa'`・`transformOrigin:'left center'`。サブタイトル＝`fontSize:38` / `fontWeight:500` / `letterSpacing:6` / `textTransform:'uppercase'` / `color:'#C8CDD6'`（BRAND.color.silver）。 |
| **6** | **ロゴ**（`hasLogo` のときのみ） | `position:absolute` `top:64` `left:72` `84×84` `borderRadius:20`、`linear-gradient(135deg, ${accent}, #ffffff22)`、`border: 2px solid ${accent}`、`boxShadow: '0 0 30px ' + accent + '66'`。 |

### 4.4 props 定義と型

```ts
export type Frazier39OpeningProps = {
  title: string;      // 主役タイトル。1文字ずつスタッガー。推奨 ≤ 14文字（132px で1行に収まる上限）
  subtitle: string;   // 下段。UPPERCASE前提・推奨 ≤ 32文字
  accent: string;     // アクセントカラー（HEX 6桁・"#" 込み）。既定 '#E5B53A'（BRAND.color.gold）
  hasLogo: boolean;   // 左上のPDロゴマークを出すか
};
```

**EP39 の既定値:** `{ title: 'THEY CAN LIE', subtitle: 'FRAZIER V. CUPP · 1969', accent: '#E5B53A', hasLogo: true }`

**props バリアント（`remotion/props/` に置く。量産用）:**

| ファイル | title | subtitle | accent | hasLogo |
|---|---|---|---|---|
| `props/frazier_op_a.json` | `THEY CAN LIE` | `FRAZIER V. CUPP · 1969` | `#E5B53A` | true |
| `props/frazier_op_b.json` | `IT IS LEGAL` | `POLICE DECEPTION IN THE ROOM` | `#1F6BFF` | true |
| `props/frazier_op_c.json` | `I DID IT` | `A CONFESSION THAT WAS FALSE` | `#E5B53A` | false |

### 4.5 確認方法とレンダリングコマンド

```bash
# プレビュー（Remotion Studio）
cd C:/Users/aab15/Documents/prime-documentary/remotion
npm run studio            # = remotion studio。左のリストから "Frazier39Opening" を選ぶ

# 単発レンダ（既定props）
npx remotion render Frazier39Opening out/frazier_op_a.mp4

# props 差し替えの量産レンダリング
npx remotion render Frazier39Opening out/frazier_op_a.mp4 --props=./props/frazier_op_a.json
npx remotion render Frazier39Opening out/frazier_op_b.mp4 --props=./props/frazier_op_b.json
npx remotion render Frazier39Opening out/frazier_op_c.mp4 --props=./props/frazier_op_c.json

# 型チェック
npm run typecheck
```

**検収（目視・数値）:** 3.0秒ちょうど（180F@60fps）／ 全フレームで何かが動いている（静止フレーム0）／ 文字が1文字ずつ順に立ち上がる／ 切れ上がりの瞬間に残像（Trail）が見える／ 下線が左から伸びる／ 背景・グリッド・グローの3層が識別できる。

---

## 5. Remotion 本編（CaseFilm）側の設計

- エンジン: `remotion/src/compositions/CaseFilm.tsx`（正典・row8実装）。EP39 専用に **新規コンポを作らず**、`remotion/src/data/frazier_film.json` をデータとして与える。
- OP/ED: `components/Bookends.tsx` の `BrandOpening` / `BrandEndcard` を **import して使う**（再実装・フォーク禁止 = `op_ed_bookends` ゲート）。
- 1920×1080 / **30fps** / 全クリップを30fpsに統一。
- トランジション: **0.3–0.5秒のクロスディゾルブ**。Sequence をトランジション長ぶん**オーバーラップ**させる（1フレームの黒/ジャンプを作らない）。カットをまたいで運動方向を継承する（velocity reset = 「かくっ」の原因）。
- `AmbientMotion` オーバーレイを全ビートに載せ、静止フレームを作らない。
- 禁止: 左→右の縦スイープライン／全画面の黄・金ウォッシュ／ズーム/パンのみの演出。

### 5.1 アニメーション密度ゲート（**着手前に閾値を把握せよ。後から直すと作り直しになる**）

`scripts/check_motion_density.py`（実測ハードフロア・AND条件）:
- `MIN_KINETIC_BEATS_PER_MIN = 2.5` — (graphics + figures + heroCuts) / 本編分。**11.75分なら最低 30 本のキネティックビート。**
- `MIN_ANIMATED_COVERAGE = 0.25` — ビート窓の和集合 / 本編秒。**最低 176秒ぶん。**
- `MIN_ANIMATED_VARIETY = 3` — 異なるアニメ形式の種類数（**同じMGの反復は不可**）。

`scripts/check_animation_mix.py`（実測ハードフロア/上限）:
- `MAX_STILL_SHARE = 0.45` — 静止フレーム / 本編フレーム。
- `MIN_MOTION_COVERAGE = 0.45` — (アニメ ∪ 実写フッテージ) / 本編。
- `LONG_HOLD_SECONDS = 5.0` / `MAX_LONG_STILL_HOLDS = 8` — 5秒超の静止保持は**最大8回**まで。
- `MAX_OPENING_SECONDS = 12.0` — `opening` ビートの合計。

→ **EP39 の設計目標（余裕を持たせた値）:** キネティックビート **38本以上**（3.2/分）／ アニメカバレッジ **0.32以上**／ バラエティ **8種以上**（AE heroカード・数値ティッカー・年表・票タリー・引用リビール・地図/経路・図解組み上げ・キネティックタイポ）／ 静止シェア **0.30以下**／ 5秒超の静止保持 **4回以下**。

### 5.2 その他の受入ゲート（全て既存スクリプト・実在確認済み）

```bash
py -3.11 scripts/check_motion_density.py    --ep PD-2026-039-frazier
py -3.11 scripts/check_animation_mix.py     --ep PD-2026-039-frazier
py -3.11 scripts/check_caption_integrity.py --ep PD-2026-039-frazier
py -3.11 scripts/check_visual_asset_qc.py   --ep PD-2026-039-frazier
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 39 --json
```

**最終ゲート（これが緑になるまで "done" と言わない・v2 THE ONE RULE）:**
```bash
./.venv/Scripts/python.exe scripts/check_final_acceptance.py 39 \
  --render episodes/PD-2026-039-frazier/08_edit/frazier_final_bgm.v003_ae.mp4 --emit-receipt
```
→ `09_package/acceptance_receipt.v001.json`（`video_sha256` 付き）。**AE合成後のファイルに対して receipt を発行する**（合成前のv002に対する receipt は無効）。

### 5.3 音（4層・v2 row1）
- ナレ = ElevenLabs（§2.4）。常に最前面・明瞭。
- BGM = 章ごとに1トラック。**ナレ下でも −22 LUFS を下回らない**（無音に落とさない）。無音区間 25秒超は FAIL。
- SFX = カット/リビール/数値出現に短いヒット。heroビートのカウントアップ開始（コンプローカル 0.55s）に tick、着地（1.55s）に impact を同期。
- 環境音 = 取調室（空調のハム・蛍光灯）／夜の街／法廷のざわめき。薄く。
- 総合ラウドネス **−16 … −12 LUFS**。

---

## 6. 字幕（v2 row3/4・VIDEO_RULES §13）
- forced alignment で**語単位**に整列。音と字幕のズレ **≤120ms**。
- 1キュー = **1息継ぎ群**。≤2行 / ≤42文字/行 / 1.0s ≤ キュー ≤ 6.0s / キュー間 ≥2フレーム / 読速 ≤17cps / 単語1個のみのキュー禁止。
- 文字サイズ 48–60px、白＋濃い縁取り、背後に半透明黒帯（不透明度 55–70%）、画面下部の安全帯、中央寄せ。
- **ゾーン分離厳守**: 下＝字幕／上・中央＝テロップ（`on_screen_text`）／出典テロップ（金ライン）は字幕と縦に離す。一度も重ねない。

---

## 7. リスク・安全（R2・厳守）

主役は**実在の私人**。以下は例外なし。

1. **AI肖像の生成・使用を全面禁止。** 主役および関係者の顔・認識可能な特徴を再現しない。
2. 人物表現は**匿名再現のみ**：後ろ姿・シルエット・顔が画角外・肩から下・手元のみ・遠景の小さな人影。
3. **非グラフィック**：暴力・拘束・自傷の直接描写をしない。象徴表現（閉まる鉄扉・空の椅子・置かれた録音機・蛍光灯・時計）に置き換える。
4. **読める判決文・供述調書・実在書式を作らない**（雰囲気のみ・文字は判読不能に）。
5. 争点は中立帰属（「多数意見は」「反対意見は」「検察は」「弁護側は」）。断定しない。
6. 未成年が関与する場合、当時の年齢を明示するが**その人物の少年期の再現画像を作らない**。
7. 生成画像は全点 `05_stock/stock_ledger.v001.json` に `source=ai_codex` / `commercial_use=allowed` / `sha256` を1行記録。
8. **禁止取得元**（YouTube/TikTok/Instagram/X・ニュース番組・TV/映画/アニメ/MV・スポーツ映像・Google画像検索）からの無断取得は使わない。

---

## 8. サムネイル 3案（CTR 2.31% → 目標 4.0%）

共通仕様（v2 row11/12・全案必須）:
- **1280×720**（`BRAND.thumb`）の Remotion `<Still>` として3案すべてレンダ。`09_package/thumbnail.v001-0{1,2,3}.png` ＋ `thumbnail.selected.v001.png`。
- 見出しは **UPPERCASE・4語以内**・自動改行。感情/好奇心のアイデアは**1つだけ**。
- **被写体は巨大**（顔/手/物体が画面高の60%以上）。超高コントラスト。**320pxに縮小しても読める**こと（縮小プレビューで検証）。
- 背景 = 黒 or 濃紺 `#0B1A2B`。アクセント = 金 `#E5B53A` **または** エレクトリックブルー `#1F6BFF`。文字 = 白 `#F5F7FA` / シルバー `#C8CDD6`。**実在人物の肖像は不可。**
- 選定は `thumbnail_visibility` ゲート（選択サムネの輝度平均 ≥33 ＋ コントラスト下限）を通ること。

| 案 | 視覚要素（具体） | テキスト（4語以内） | 色/コントラスト方針 |
|---|---|---|---|
| **T1「嘘のファイル」** | 取調室の机の上、**画面いっぱいの手**が「共犯者の自白調書」らしき紙束を被疑者側へ滑らせる。紙は判読不能。紙の上に**赤い「FAKE」スタンプ**が斜めに強く押されている。奥に椅子のシルエット（顔なし）。上からの蛍光灯1灯で紙だけが白く飛ぶ。 | **`POLICE CAN LIE`** | 背景ほぼ黒（輝度10%以下）／紙は純白（輝度90%）で**最大コントラスト**／`FAKE` スタンプのみ赤系→ 金 `#E5B53A` の見出し文字で受ける。赤は1要素のみ。 |
| **T2「言っていない自白」** | **口元のみの超クローズアップ**（目より上は画角外＝肖像回避）。口の前に浮かぶ吹き出しの中に手書き風の `"I DID IT"`。口と吹き出しの間に**細い金の線が切断**されている（＝言葉と真実の断絶）。背景は濃紺のグラデ。 | **`I DIDN'T DO IT`** | 濃紺 `#0B1A2B` 背景 ×  肌のハイライトを強く飛ばす／吹き出しは白／断裂線のみ金／見出しは白＋黒縁。**顔は下1/3のみ＝肖像に該当しない構図**。 |
| **T3「時計と扉」** | 画面左に**巨大な壁時計**（針が異常に多く重なり長時間経過を示す）、右に**閉じた鉄の取調室ドア**。中央に細い光の帯。人物は**ドアの磨りガラス越しの小さなシルエット1つのみ**。 | **`48 HOURS ALONE`**（※時間数は台帳確定後に差し替え。未確定なら `NO ONE COMING`） | 黒背景／時計盤だけエレクトリックブルー `#1F6BFF` で発光／ドアはシルバー質感／見出しは白。青と白の2色に絞って**320pxでの識別性を最大化**。 |

**A/Bの回し方（v2 row13）:** T1 と T2 を**タイトル × サムネの2組**として先に出す。タイトル案（≤60文字・フック前置き）:
- A: `Police Are Allowed to Lie to You in the Interrogation Room`（58字）
- B: `He Confessed to a Crime He Didn't Commit. It Was Legal.`（54字）

---

### 素材の反復禁止（オーナー指示 2026-07-19・機械ゲート）

**「1動画に同じ素材はなるべく繰り返し使用しない」。** 判定は `python scripts/check_asset_reuse.py <film.json>`（`preflight_render_gate.py` に配線済み・レンダー前にブロック）。

| 種別 | 同一素材の使用上限 | 理由 |
|---|---|---|
| factoryクリップ | **1回**（再使用禁止） | `H:/pd-media/assets/factory` に11,623本ある。繰り返す理由が無い |
| i2v モーション | 2回 | 1本あたり24–73 GPU分と高コスト |
| SDXL静止画 | 2回 | 生成コストはあるが安い |

さらに全体条件: **カットの70%以上が「その素材の初出」であること**（first-use share ≥ 0.70）。

**実測した現状（2026-07-19・全13本がこの基準でFAIL）:** rodriguez は62枚を188カットに回して平均3.03回、williams は73素材で344カット＝平均4.71回、EP38は平均2.12回。連続分割はゼロ＝すべて「別の絵を挟んで同じ絵が戻ってくる」真の再登場であり、これが「AIスライドショー感」の正体。最良の rolin は factory 188本を全て1回使用でクリアしており、**この基準は達成可能**（rolin の唯一の違反は静止画の3回使用）。

**設計への含意:** カット数に対して素材点数を積む。12分＝約220カットなら、初出70%＝**約155点の異なる素材**が要る。内訳の確定値は **factory 90本（各1回）＋ 静止画 68枚（平均1.47回）＋ i2v 18本（各2回）= 226カット / distinct 176 / first-use 0.779**。

**注意（私の初期配分は誤りだった）:** 「各素材を上限いっぱいまで使う」設計は原理的に first-use share を下げる。share = distinct/cuts = 1/平均使用回数 なので、**0.70を満たすには平均使用回数を1.43回以下**に抑える必要がある。旧記述の「factory50 + 静止画50×2回 + i2v15×2回」は 180カット / distinct 115 / share **0.639 = FAIL**。上限は「そこまで使ってよい」ではなく「そこが限界」と読むこと。足りなければ factory を増やす（無料・在庫11,623本）のが最も安い解。

### ★素材構成の是正（オーナー指摘「全て画像じゃなくてもいい。大量の素材があるからね」）

SDXL生成に寄せすぎていた。**実測した在庫（2026-07-19・`H:\pd-mediassets`）:**

| カテゴリ | 実測本数 | 使い方 |
|---|---|---|
| `factory/backgrounds` | **11,623** | 実写クリップ。**動いている**ので motion coverage に直接効く |
| `factory/light_assets` | 1,401 | 合成レイヤー（光） |
| `factory/particle_assets` | 1,225 | 合成レイヤー（粒子） |
| `factory/vfx_overlays` | 1,196 | 合成レイヤー |
| `factory/loops` | 454 | ループ素材 |
| `ai`（既存生成物） | 1,287 | 流用可 |
| `stock` | 235 | — |

**空のフォルダ（存在するが中身0）:** `diagram_assets` / `transitions` / `typography_assets` / `parallax_layers` / `lottie_assets` / `ai_video_shots` / `sfx`。図解・トランジション・タイポは**自作が必要**（Remotion/AE側の担当）。

**確定する素材構成（226カット / distinct 約155点）:**

| 種別 | distinct 点数 | 使用回数 | 調達 |
|---|---|---|---|
| SDXL静止画 | **60–70枚** | ≤2回 | 生成。**この作品にしか無い絵**だけに使う（主役の顔が映らない再現、固有の場所、象徴カット） |
| factory backgrounds | **80–90本** | **1回** | 在庫から選抜。空気・情景・質感・繋ぎ |
| i2v モーション | 15–20本 | ≤2回 | 上のSDXLから動きが意味を持つものを選んで生成 |
| 合成レイヤー（light/particle/vfx） | 随時 | — | **distinct素材に数えない。**静止画の上に重ねて「止まっていない」状態を作る |

**要点:** SDXL生成枠は120枚→**60–70枚に半減**させ、その分を無料の実写在庫（11,623本）で埋める。実写は動いているぶん `animation_mix` の motion coverage にも効くので、静止画を増やすより有利。合成レイヤー3,822点は**同じ静止画を別物に見せる**ために使う（反復対策として枚数を増やすより安い）。

**ただし実写選抜には必ず目視QCを通すこと。** EP36で「city_surveillance_camera_dome」という名のクリップが実際にはベオグラードの大聖堂だった、EP38で牛の映像が「documents_on_desk」というラベルで入っていた、という実例がある。**factoryのファイル名とサブタイプは信用できない。** `check_visual_asset_qc` のコンタクトシートで全点を目で見てから使うこと（80–90本ぶんの確認時間を工程に見込め）。

### ★シーン数の是正（オーナー指摘 2026-07-19「20枚じゃ足りない」）— 旧値を上書きする

**旧設計（20–22シーン × 5–6バリエーション）は不足。** 画像は110–132枚あっても、**視聴者が見る「別の被写体」は20種類しかない**。同じ取調室を6アングルで撮っても、観る側には同じ部屋。反復感の原因は総枚数ではなく**シーン数**。

**確定値: 48–50シーン × 2–3バリエーション = 生成プール 120–150枚。本編で使う distinct 静止画 = 約120枚。**

積算（226カット / 静止画が156カットを担当する前提）:

| 静止画 distinct | 1枚あたり使用回数 | 判定 |
|---|---|---|
| 39枚 | 4.0回 | 旧仕様の上限。**反復が露骨に見える** |
| 60枚（旧設計値） | 2.6回 | `check_asset_reuse` の上限2回を**超過＝FAIL** |
| 78枚 | 2.0回 | ゲート最低ライン |
| **120枚** | **1.3回** | **確定値。反復を実感させない水準** |
| 156枚 | 1.0回 | 完全に反復なし（余力があればここへ） |

**バリエーションは「同じ被写体の別アングル」ではなく、別の被写体を増やす方向に使うこと。** 1シーンあたり2–3枚に抑え、浮いた生成枠をシーン数に回す。オーナーはSDXLの大量生成を明示的に許可している（「複数の素材が必要ならSDXLで大量の素材を作って動かすのもあり」）ので、枚数をケチる理由はない。

**生成は冪等に。** 既存ファイルをスキップして再開できるバッチにし、中断しても作り直しにならないこと。強い絵から順に生成し、途中で止まっても使える状態を保て。

## 9. 画像プロンプト群（Codexが即着手できる・台本非依存）

**密度要件（v2 row5/7/8 ＋ VIDEO_RULES §3）:** 11–12分＝**約4.5秒ごとに別画像**。→ **20シーン × 各5〜6バリエーション = 合計 約110枚**。
**各プロンプトを、構図/カメラ/ライティング/被写体位置を変えて 5〜6枚ずつ出力し、`<SPN-ID>.png`, `<SPN-ID>_02.png`, `<SPN-ID>_03.png` … と連番保存する。**

- 保存先: `H:\pd-media\assets\ai\frazier\<SPN-ID>.png` → `import_to_remotion.py` が取り込む。
- 解像度: **長辺 ≥ 3840px**（足りなければアップスケール＋デノイズ＋ブランドLUT）。ブレ・アーティファクト・文字入り・実在人物似は**全部リジェクト**。
- 1点ごとに `05_stock/stock_ledger.v001.json` に1行記録（source=ai_codex / commercial_use=allowed / sha256）。

**共通スタイル接尾（各プロンプト末尾に必ず付ける）:**
```
, cinematic still, dramatic volumetric lighting, moody, deep blacks and navy blue with electric-blue and gold accents, silver highlights, shallow depth of field, ultra-detailed, photoreal, 4K, 16:9, film grain, no text, no watermark, no logo
```

**共通ネガティブ:**
```
text, words, letters, captions, watermark, logo, real celebrity, recognizable real person, identifiable face, cartoon, low quality, deformed, extra limbs, nudity, explicit, gore, blood, violence, restraint, child
```

**S01 — 取調室（無人・本作の主舞台）**
An empty police interrogation room at night, one steel table bolted to the floor, two facing chairs, a single caged ceiling light, a dark one-way mirror on the wall, cold institutional green-grey walls, utterly still and oppressive, no people + [共通スタイル]

**S02 — 閉まる扉**
A heavy steel interrogation-room door caught in the act of closing, seen from inside the room, a narrowing blade of corridor light on the floor, cold blue outside and warm dead fluorescent inside, symbolic of the world shutting out + [共通スタイル]

**S03 — 主役（匿名・後ろ姿）**
A lone anonymous figure seen from behind, seated small at a steel table in a vast dark room, shoulders low, head slightly bowed, face entirely out of frame, one hard overhead light, overwhelming institutional emptiness around them + [共通スタイル]

**S04 — 取調官（匿名・シルエット）**
The silhouette of a standing investigator leaning over a table, seen from behind and below, faceless and backlit, one hand flat on a stack of papers, looming and authoritative, cold blue rim light, no identifiable features + [共通スタイル]

**S05 — 「証拠」の紙束（＝嘘）**
A thick stack of official-looking papers pushed across a steel table under a hard overhead lamp, the top page deliberately blurred and illegible, a faint red stamp impression, symbolic of evidence that does not exist + [共通スタイル]

**S06 — 空の証拠袋**
An empty clear evidence bag lying open on a dark table, its label blank and illegible, a single cold spotlight, dust in the air, deeply symbolic of nothing inside, minimal and stark + [共通スタイル]

**S07 — 時間の経過**
A plain institutional wall clock in a dark room, its hands smeared into a long motion-blurred arc implying many hours passing, cold blue light, a lone empty chair below it, exhaustion and duration made visible + [共通スタイル]

**S08 — 蛍光灯と疲弊**
A close-up of a flickering caged fluorescent tube on a stained ceiling, harsh glare blooming into the lens, moths of light, seen from the point of view of someone lying back exhausted, disorienting and relentless + [共通スタイル]

**S09 — 録音機/テープ**
An old reel-to-reel or cassette recorder on a steel table, its red record light glowing in the dark, tape turning, one shaft of light, symbolic of words being captured forever + [共通スタイル]

**S10 — 署名の手**
Anonymous hands holding a pen above a document at the moment before signing, the paper deliberately illegible, hands trembling slightly, one warm lamp against cold darkness, no face, the weight of an irreversible act + [共通スタイル]

**S11 — 独房の夜**
A bare holding cell at night, a thin mattress on a metal bunk, a small barred window casting a cold blue grid across the floor, completely empty of people, lonely and still + [共通スタイル]

**S12 — 家族の不在（象徴）**
An ordinary family kitchen at night with one chair pulled out and empty, a cold dinner still on the table, a hallway light left on, no people, aching absence, warm domestic tones against a cold blue window + [共通スタイル]

**S13 — 最高裁 外観**
The U.S. Supreme Court building at dusk, dramatic low angle, marble columns lit gold against a deep navy sky, solemn and monumental, cinematic + [共通スタイル]

**S14 — 法廷内（無人・象徴）**
An empty grand courtroom interior, the raised judicial bench in shadow, one beam of light across nine empty high-backed chairs, dust motes suspended, solemn, no people + [共通スタイル]

**S15 — 1969年（時代）**
A dim 1960s American police station interior, period rotary telephone, metal filing cabinets, venetian-blind light stripes across the wall, muted period colour palette, no people, archival and historical + [共通スタイル]

**S16 — 判例集の書架**
Rows of heavy bound law reports on a dark library shelf, gold lettering catching a single warm light, one volume pulled slightly forward, reverent and institutional, lettering unreadable + [共通スタイル]

**S17 — 嘘という道具（象徴）**
An abstract symbolic image of a polished tool laid on black velvet under a single spotlight, ordinary and clinical yet sinister, implying a permitted instrument, cold metal and gold light, minimal + [共通スタイル]

**S18 — 「あなた」への射程**
A long line of anonymous silhouetted people waiting under harsh institutional lights, each faceless and interchangeable, implying any one of us, cold blue tone with one warm light + [共通スタイル]

**S19 — 平穏な日常が一変**
A calm ordinary suburban American street in soft morning light, warm and safe, a single distant police car turning onto it far down the road, cinematic contrast of safety and threat + [共通スタイル]

**S20 — 権利の線 / ED**
A single stark line of golden light drawn across a dark marble floor, a lone figure standing just behind it seen from far away and from behind, symbolic of the constitutional limit, minimal, contemplative, open-ended epilogue mood + [共通スタイル]

*(S01–S20 を各 5〜6 枚ずつ ＝ 合計 約110枚。)*

### 9.1 heroビートに使う静止画の割り当て（`still` フィールドの既定値）

| slot | 既定 still | 理由 |
|---|---|---|
| `HB1_INTERROGATION_LENGTH` | `S07` | 時間の経過そのもの |
| `HB2_SUBJECT_VULNERABILITY` | `S03` | 主役の匿名後ろ姿 |
| `HB3_THE_LIE` | `S05` | 存在しない「証拠」の紙束 |
| `HB4_THE_CASE` | `S16` | 判例集の書架 |
| `HB5_YEARS_LOST` | `S11` | 独房の夜 |
| `HB6_FALSE_CONFESSION_RATE` | `S18` | 匿名の列＝普遍化 |
| `HB7_DECISION_VOTE` | `S14` | 無人の法廷 |
| `HB8_EXONERATION_YEAR` | `S20` | 光の線／解放 |

---

## 10. 工程分担（誰が何をやるか・明示）

### 10.1 Codex が単体で実装可能（**台本を待たずに今すぐ着手可能**）

| # | タスク | 成果物 |
|---|---|---|
| C1 | エピソード雛形の作成 | `episodes/PD-2026-039-frazier/{03_script,04_scenes,05_stock,06_audio,08_edit,09_package,approvals,events}/` |
| C2 | **§4 の `Frazier39Opening.tsx` 実装＋Root登録＋props3種** | `remotion/src/compositions/Frazier39Opening.tsx` / `remotion/props/frazier_op_{a,b,c}.json` / `out/frazier_op_{a,b,c}.mp4` |
| C3 | **§9 の画像110枚を事前生成**（S01–S20 × 5–6） | `H:\pd-media\assets\ai\frazier\S**.png` ＋ `05_stock/stock_ledger.v001.json` |
| C4 | **§8 のサムネ3案を Remotion `<Still>` でレンダ** | `09_package/thumbnail.v001-0{1,2,3}.png` ＋ `thumbnail.selected.v001.png` |
| C5 | **§3 の AEスクリプト2本を EP39 用に新規作成**（EP38版を雛形に、§3.3の5レイアウトを実装） | `scripts/ae/build_frazier_hero_jsx.py` / `scripts/ae/composite_frazier_hero.py` |
| C6 | **AEスモークテスト**（ダミー数値の1ビートをビルド→aerender→ffprobeで1920x1080/30fps/尺を検証） | `08_edit/ae_hero/render/_smoke.mp4` ＋ ffprobe出力 |
| C7 | 画像QC（長辺≥3840・シャープネス・NEG違反0・肖像違反0） | `04_scenes/image_ledger.v001.json` |
| C8 | ファクトリ素材の候補選定（`scripts/select_factory_assets.py`）。取調室/夜/法廷/時計/光のトーンで抽出 | 候補リスト |

### 10.2 台本確定を待つ（Codex・台本到着後に自動で進む）

| # | タスク | 依存 |
|---|---|---|
| D1 | ElevenLabs ナレ生成 | S3 `script.annotated.v001.json` |
| D2 | forced alignment → 字幕3形式 | D1 |
| D3 | `shotlist.v001.json` 生成・画像割当 | D2 |
| D4 | `frazier_film.json` 生成 → `CaseFilm` レンダ | D3 |
| D5 | BGM/SFX/環境音の4層ミックス → `frazier_final_bgm.v002.mp4` | D4 |
| D6 | **heroビートの anchor 解決 → jsx生成 → AEビルド/レンダ → overlay合成** → `frazier_final_bgm.v003_ae.mp4` | S6 `hero_beats.spec.v001.json` ＋ D2 ＋ D5 |
| D7 | フック（0–8s）を本編素材から組む（**最後**） | D6 |
| D8 | 全ゲート実行 → `--emit-receipt` | D7 |

### 10.3 Claude 側（別工程・Codexはやらない）

| # | タスク |
|---|---|
| E1 | **主役1名の確定**（Dassey / Laughman / Burton / CP5 から）＋ 一次資料の収集 |
| E2 | **claim台帳 `fact_recheck.v001.json` の作成**（§2.3の全数値の出典固定・R2判定） |
| E3 | **台本（FILM BIBLE ＋ script.en ＋ script.annotated）**：初稿→批評→改稿の3回。語数 2,048–2,226（目標2,140）。`check_script_length.py` PASS が完了条件。 |
| E4 | **`hero_beats.spec.v001.json` の数値・`anchor_phrase`・ラベル文字列の記入**（§3.4の契約に厳密準拠） |
| E5 | DSPゲート系の事前レビュー（motion_density / animation_mix の設計値がフロアを超えるか、beatsheet 設計段階で試算） |
| E6 | 法務・安全レビュー（R2 肖像・非グラフィック・中立帰属の最終確認） |
| E7 | 連動Short（35–45秒）の台本＋固定コメント文＋概要欄1行目の本編リンク |
| E8 | 公開後 72h / 7d / 28d の北極星4指標の記録（`yt_analytics_probe.py` ＋ `yt_studio_ctr.py`） |

### 10.4 オーナー専管
- **YouTube アップロード・公開予約は必ずオーナー操作**（invariant 2）。Codex/Claudeは完成物とパッケージを用意して停止する。

---

## 11. 受入チェックリスト（EP39・全部緑で package_ready）

- [ ] `structure_4part`：hook / opening / body / ending が順に存在。hook = 6–10秒。
- [ ] `hook_added` ＋ promise-payoff：hookで提示した reveal が本編に出る。
- [ ] `runtime_band`：11.5–12.5分（standard profile）。
- [ ] `voice_is_master`：narration provider に `eleven` を含む。sapi/local を含まない。
- [ ] `caption_narration_match ≥ 99%` / `captions_final` が runtime の ≥95% をカバー / キューQC 0違反。
- [ ] `bgm_present`：無音25秒超なし・VO下でも −22 LUFS を下回らない。ラウドネス −16…−12 LUFS。
- [ ] `image_resolution`：全使用静止画の長辺 ≥3840。
- [ ] `footage_diversity`：distinct/total ≥0.40・同一クリップ4回超なし・汎用シンボル（天秤/gavel）2回まで。
- [ ] `motion_density`：≥2.5 beats/min ＋ coverage ≥0.25 ＋ variety ≥3（設計目標 3.2 / 0.32 / 8）。
- [ ] `animation_mix`：still share ≤0.45 ／ motion coverage ≥0.45 ／ 5秒超静止保持 ≤8 ／ opening合計 ≤12秒。
- [ ] `op_ed_bookends`：`BrandOpening`/`BrandEndcard` を import（フォークしていない）。
- [ ] `thumbnail_present`：1280×720 PNG が3枚以上＋selected 1枚。`thumbnail_visibility`：selected の輝度平均 ≥33。
- [ ] タイトル ≤60字・A/B 2案。
- [ ] **AE heroビート：6本以上が SKIP されずに合成された**（コンポジタのログで確認）。SKIPが1本でもあれば原因を潰して再合成。
- [ ] **合成後の `v003_ae.mp4` に対して** `check_final_acceptance.py 39 --emit-receipt` が exit 0。
- [ ] R2安全：AI肖像0件・グラフィック表現0件・読める偽書類0件。

---

## Codex引き継ぎプロンプト（そのまま貼る）

```
あなたは Prime Documentary EP39 の実装担当です。リポジトリは
C:\Users\aab15\Documents\prime-documentary です。

# 受入契約（最初に読む・これを満たさない限り "done" と言わない）
本作業は docs/PD_ONE_PASS_PRODUCTION_SPEC.v2.md の以下の行を満たさなければならない:
row1(BGM) row2(ElevenLabs音声) row3/4(字幕) row5(画像長辺>=3840) row6(libx264 preset slow /
crf16 / yuv420p / bt709 / aac320k / NVENC禁止) row7(素材多様性) row8(アニメ密度・紙芝居禁止)
row9(フック8秒) row10(4部構成+earned CTA) row11/12/13(サムネ3案・4語以内・A/B)
row14(OP/EDはBookendsをimport・フォーク禁止) row15/16(台本・リテンション設計)。
最終検証コマンド（必ず自分で実行し exit 0 を確認する）:
  ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 39 --json
  ./.venv/Scripts/python.exe scripts/check_final_acceptance.py 39 \
    --render episodes/PD-2026-039-frazier/08_edit/frazier_final_bgm.v003_ae.mp4 --emit-receipt

# 設計書（唯一の仕様）
episodes/_planning/EP39_frazier_DESIGN_and_CODEX_PROMPTS.v001.md
全ての数値・レイアウト・イージング・パス・契約はこの設計書に書いてある。書いていないことを
推測で決めない。曖昧だと感じた箇所は「推測して進める」のではなく、その場で停止して報告する。

# 重要な前提
台本は別プロセスで並行制作中。よってタスクは2群に分かれる。
【今すぐ着手する（台本非依存）】
 1. episodes/PD-2026-039-frazier/ に 03_script,04_scenes,05_stock,06_audio,08_edit,
    09_package,approvals,events を作成。
 2. 設計書 §4 のとおり remotion/src/compositions/Frazier39Opening.tsx を新規実装。
    - Composition id="Frazier39Opening" / 1920x1080 / fps=60 / durationInFrames=180(=3.0s)
    - props: {title:string, subtitle:string, accent:string, hasLogo:boolean}
    - 既存の remotion/src/compositions/Opening.tsx（id="Opening"）は書き換えない。
    - 既存の components/Bookends.tsx もフォークしない（本編OP/EDはBookendsのまま）。
    - お手本は C:\Users\aab15\Documents\pino-channel\remotion\src\Opening.tsx。構造を踏襲し
      数値だけ設計書 §4.2 の表どおりに差し替える。
    - 全モーションにイージング必須（spring{damping,mass} または Easing.out(Easing.cubic)）。
      等速線形禁止。opacity単独の演出禁止（必ず translateY/scale と併用）。
      文字は1文字ずつ 0.04秒スタッガー。切れ上がりは overflow:hidden + translateY(110%→0%)。
      速い動きには @remotion/motion-blur の Trail(layers=6, lagInFrames=1.2, trailOpacity=0.45)。
      主役タイトルの裏に最低3レイヤー（グラデ背景・グリッド・グロー）。
      秒数は fps から算出（フレーム直書き禁止）、タイミングは定数 T にまとめる。
    - remotion/props/frazier_op_{a,b,c}.json を設計書 §4.4 の表のとおり作成。
    - 検証: cd remotion && npm run typecheck && npm run studio で目視、
      npx remotion render Frazier39Opening out/frazier_op_a.mp4 --props=./props/frazier_op_a.json
      で3案ともレンダできること。remotion.config.ts は既に正典値なので変更しない。
 3. 設計書 §9 の画像プロンプト S01〜S20 を、構図/カメラ/ライティング/被写体位置を変えて
    各5〜6枚ずつ生成（合計 約110枚）。長辺>=3840px。
    保存: H:\pd-media\assets\ai\frazier\S01.png, S01_02.png, ... の連番。
    共通スタイル接尾と共通ネガティブを必ず付ける。
    ★R2安全（絶対）: 実在人物の肖像・認識可能な顔を作らない。人物は後ろ姿/シルエット/
      顔が画角外のみ。暴力・拘束・自傷の直接描写禁止。読める書類・判決文を作らない。
    生成後 05_stock/stock_ledger.v001.json に1点1行（source=ai_codex, commercial_use=allowed,
    sha256）を記録し、画像QC（長辺/シャープネス/NEG違反0）を通す。
 4. 設計書 §8 のサムネ3案を Remotion <Still> 1280x720 でレンダし
    09_package/thumbnail.v001-01.png ... -03.png ＋ thumbnail.selected.v001.png を出す。
    見出しは UPPERCASE 4語以内、被写体は巨大、320pxに縮小しても読めることを実際に縮小して確認。
 5. 設計書 §3 の After Effects パイプラインを EP39 用に実装:
    scripts/ae/build_frazier_hero_jsx.py と scripts/ae/composite_frazier_hero.py を新規作成。
    雛形は実在する scripts/ae/build_kfc_hero_jsx.py と scripts/ae/composite_kfc_hero.py。
    必ず先にこの2ファイルを読んでから書くこと。
    - 5つのレイアウト A_BIG_NUMBER / B_SPLIT_RATIO / C_PERCENT_ARC / D_CITATION_STAMP /
      E_VOTE_TALLY を設計書 §3.3 の数値どおりに実装する。
    - 数値カウントアップのキーフレーム文字列は Python 側で全事前計算する（JS側で整形しない）。
    - サイドカー hero_beats.v001.json が jsx とコンポジタの両方を駆動する。
    - コンポジタは mp4 が欠損/サイズ違い/短尺の beat を SKIP する（その区間は元のまま）。
    - 出荷済みファイルを絶対に上書きしない（出力は *_v003_ae.mp4）。音声は -c:a copy。
 6. AEスモークテスト: ダミー数値1ビートをビルド→aerender→ffprobe で
    1920x1080 / 30fps / 尺が spec どおりであることを実測確認する。
    ★ここで必ず実挙動を確認してから本番へ進む。

【台本確定後に着手する（待ち）】
 03_script/script.annotated.v001.json, 03_script/fact_recheck.v001.json,
 04_scenes/hero_beats.spec.v001.json の3ファイルが揃ったら、設計書 §2.4 の手順1〜6を順に実行:
 ElevenLabsナレ生成 → forced alignment字幕 → shotlist → frazier_film.json → CaseFilmレンダ →
 4層ミックス(v002) → heroビートanchor解決/AEビルド/overlay合成(v003_ae) → フックを最後に組む →
 全ゲート → receipt発行。
 ★ hero_beats.spec の anchor_phrase が語タイム列に0件または2件以上ヒットした場合は
   推測で配置せず FAIL を返して停止すること。

# このマシン固有の罠（AE。これを踏むと無言で壊れる。設計書 §3.6 の全項目を守れ）
 - AE 2026・日本語ロケール・RTX4090。実行体は
   /c/Program Files/Adobe/Adobe After Effects 2026/Support Files/ の AfterFX.com と aerender.exe。
 - setTemporalEaseAtKey は Position など spatial プロパティでは要素1個の配列。
   dim = prop.isSpatial ? 1 : (value.length||1)。間違えるとイーズが無言で効かず等速になる。
 - RS/OMテンプレ名はローカライズ済み。有効値は RS "最良設定" /
   OM "H.264 - レンダリング設定を一致 - 15 Mbps"。英語名は失敗する。
 - AE の TextDocument の改行は \n ではない。字幕は必ず1行に保つ（または \r）。
 - app.newProject() は headless(-noui) でハングする。使うな。既存の同名コンプを防御的に削除する。
 - ビルドは遅い(~100-120秒)がレンダは速い(6コンプ~21秒)。jsx が書く完了マーカーファイルを
   ポーリングせよ。早期killするな。
 - AfterFX/aerender はデタッチ起動＋出力ファイルのポーリング。jsx の末尾で app.quit()。
 - layer.motionBlur はレイヤー個別に設定が必要（コンプのスイッチだけでは無効）。
 - 2Dレイヤーの "ADBE Rotation" は null。"ADBE Rotate Z" を使え。
 - レイヤーは inPoint だけ設定すると outPoint がコンプ末尾に残る。両方設定せよ。
 - AE は画像シーケンスを prefs 既定の30fpsで読む。item.mainSource.conformFrameRate = FPS が
   無いと全ビートの timing が無言でズレる。
 - proj.gpuAccelType = GpuAccelType.SOFTWARE / proj.bitsPerChannel = 8 を try/catch で設定。
 - aerender の前に taskkill //F //IM AfterFX.com と //IM AfterFX.exe で残骸を落とす。

# アニメーション密度（後から直すと作り直しになる。設計段階で超えておけ）
 check_motion_density: >=2.5 kinetic beats/分 AND coverage>=0.25 AND variety>=3
 check_animation_mix : still share<=0.45 AND motion coverage>=0.45 AND 5秒超の静止保持<=8
                        AND opening合計<=12秒
 EP39 設計目標: 3.2 beats/分 / coverage 0.32 / variety 8 / still share 0.30 / 長保持 4回以下。

# 禁止
 - YouTube へのアップロード・公開予約をしない（オーナー専管）。完成物を用意して停止する。
 - 出荷済み mp4 を上書きしない。
 - 実在しないスクリプト名・テンプレ名を使わない。使う前に必ずファイルを読んで実在を確認する。
 - 自作の品質ゲートを書いて「合格」と宣言しない。既存の check_*.py の測定結果のみが合否。
 - 実在人物の肖像を生成しない。

# 完了報告に必ず含めること
 1. 作成/変更したファイルの絶対パス一覧
 2. Frazier39Opening の3案レンダ結果（ffprobe: 1920x1080 / 60fps / 3.00s）
 3. 生成画像の枚数・長辺の最小値・QC違反件数
 4. サムネ3案のパスと320px縮小での可読性確認結果
 5. AEスモークテストの ffprobe 実出力
 6. 台本待ちで着手できなかった項目の一覧
```
