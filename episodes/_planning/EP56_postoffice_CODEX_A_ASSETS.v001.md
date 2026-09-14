# EP56 postoffice — Codex スレッドA「素材生成」引き継ぎプロンプト v001（30分・5幕・payoff 末尾積み上げ・UKパイロット）

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN_ARCHITECTURE）も実装スレッドB（CODEX_B）も**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> ★30分尺。素材点数は EP52 morton / EP55 burge と同スケール。**「だいたい」で決めず §3 の確定値と §3.3 の検算をそのまま使う。**
> ★EP55 の §5.5a 反復禁止ルール（1ビート最大2枚・状態変化つき再登場のみ・one-shot）を**誕生時から**適用済み — 後追い転換はない。

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
担当:       EP56 / Episode ID: PD-2026-056-postoffice / slug: postoffice
Composition id: Ep56Postoffice（B が Root.tsx に登録・A は staging まで）／1920x1080 / fps30 / 30:00
事件:       The UK Post Office Horizon scandal（英国郵便局 Horizon 冤罪事件）
            1999年、英国の Post Office は全支局の会計を Fujitsu 製システム「Horizon」に切り替えた。
            システムのバグが「幻の欠損」を量産し、支局長（sub-postmaster＝村の郵便局を自己資金で
            買って営む自営業者）は契約により欠損の個人弁済を強制された。ヘルプラインは全員に
            「問題はあなただけ（you're the only one）」と告げ続けた。Post Office は英法上誰でも
            使える private prosecution を「被害者・捜査者・訴追者の三役一体＋産業規模」で運用し、
            1999–2015 に約700人を自ら訴追（英全体で約1,000人が Horizon 証拠で有罪・BBC集計で
            236人収監）。Seema Misra は2010年、妊娠8週で息子の10歳の誕生日に収監。Lee Castleton は
            民事で潰され訴訟費用 £321,000 で破産。Martin Griffiths は2013年に自死（★墓場級の抑制・
            映像化厳禁）。内部では 2010 年の Ismay 報告が「システムを疑えば全訴追が止まる」と明記、
            2013 年には自前の法廷弁護士 Clarke が専門家証言の欠陥と「議事録をシュレッダーにかけた」
            事実を記録 — すべて放置・隠蔽。独立調査 Second Sight は 2015 年に解任され資料破棄を指示
            された。Fujitsu の Bracknell 拠点から支局データを遠隔改変できた事実は何年も否定され続け、
            2019-12、Bates v Post Office 群訴訟（原告555人）で Fraser 判事が「remote access は設計上
            存在し実際に使われた」「地球平面説の21世紀版」と認定。2021-04-23、控訴院が39件を破棄
            （"an affront to the conscience of the court"）。2024-01-01、ITVドラマ「Mr Bates vs the
            Post Office」が国民的怒りを点火 → 2024-05-24、前代未聞の一括無罪化法
            Post Office (Horizon System) Offences Act 2024 が成立（s.1(1) "Every conviction to which
            this Act applies is quashed"）。Vennells 元CEOは CBE を剥奪され（Gazette 2024-02-23
            "cancelled and annulled"）、2024-05 の公開インクワイアリで3日間涙の証言。2025-07-08、
            インクワイアリ最終報告 Volume 1（自死13人以上・約1万人が救済対象・"disastrous"）。
            2026-06 時点で賠償 £1,628M / 12,900人超。★しかし個人の刑事訴追はゼロ（2026-05-26 Met
            発表・53人捜査中・起訴判断は2027年末以降）。Horizon は今も稼働中（Fujitsu 契約 2027-03
            まで延長）。インクワイアリの責任認定巻（Volumes 2–5）は 2026-07 時点で未公表。
            ★主題は【機械の言葉が人間の言葉に勝ち続けた — 制度は真実の値段を知っていて払わなかった。
            誰も刑務所に行っていない】。
            ★冤罪被害者は【全員無実】＝断定してよい（控訴院＋議会立法で法的に確定）。
            ★★ほぼ全員が【存命】（Bates/Misra/Hamilton/Castleton/Thomas/Vennells/Jenkins…）＝
              実在人物の顔・肖像・likeness を一切作らない。ITVドラマの俳優（Toby Jones 等）も同様。
              個人を犯罪者と示唆する画像・文言を作らない（起訴者ゼロ）。悪役は常に「制度」。
            ★★★Martin Griffiths の自死は【映像で一切表現しない】＝バス・道路事故・ロープ・薬・
              遺書などの自死表象を全編で禁止。当該ビートの絵は環境のみ（灰色の河口・閉じた
              シャッター）。悲嘆の顔・泣き顔・うずくまりも禁止（尊厳第一）。
            ★★★実在ロゴ禁止＝Post Office / Royal Mail / Fujitsu / ITV / BBC のロゴ・紋章・書体を
              再現しない（generic な赤い看板・generic な赤いポストの「形」のみ可）。
              可読の偽文書・偽帳簿・偽画面を作らない（数字・文字はすべて unreadable smear）。
              時代考証 1999–2026 の英国（米国の街並み・米国ポスト・右側通行を混ぜない）。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ・30分スケール）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**210本の固有プロンプト×1枚＝210枚**・バリエーション0） | `H:\pd-media\assets\ai\postoffice\S<NNN>.png` | 5–8時間（GPU） |
| A-1b | i2v 種画像の生成（**42本の固有プロンプト×1枚＝42枚**・バリエーション0） | `H:\pd-media\assets\ai\postoffice\M<NN>_src.png` | 1.5–2.5時間（GPU） |
| A-1c | サムネ用 emotive-face 静止画（**3枚**・CTR §4A・非実在の illustrative face・§5.12） | `H:\pd-media\assets\ai\postoffice\T<NN>_face.png` | 20分（GPU） |
| A-2 | 静止画のQCと目視（**全255枚を目視必須**＝210 body + 42 i2v種 + 3 thumb_face） | `05_visuals/still_qc.v001.json` + コンタクトシート | 2.5–4時間 |
| A-3 | ~~depth map~~ **不要（本作は depth treatment を使わない・§6.4）** | — | — |
| A-4 | factory 実写クリップ **235本**の選定と**全点目視QC** | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | 4–6時間（うち目視だけで2時間以上） |
| A-5 | i2v モーション化 **42本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\postoffice\M<NN>_rife.mp4` | 18–48時間（GPU・**複数日**） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 **30本** | `05_stock/overlay_selection.v001.json` | 1時間 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 30分 |
| A-8 | Remotion public への staging | `remotion/public/postoffice/{img,factory,motion,overlay,thumb}/` | 40分 |

> **★★ 最重要の前提（EP42–55 から継続）: 1シーン1枚・バリエーション0 ★★**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 210本＝210行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **variants 指定なし（＝1枚）** で回す。**`--variants 3` は使わない。`_02`/`_03` を作らない。**
> **総生成画像 = still 210 + i2v 種 42 + thumb_face 3 = 255枚（各1回）。** factory 235本は生成でなく在庫からの選抜。
> ★**`--only S001` のログで `shots=255` を確認**してから本番を回す（210 body + 42 i2v種 + 3 thumb_face = 255。F-series 12行は base 検証後に追記＝追記後 shots=267 が正・§5.13）。
> ★i2v 42本は**複数日GPU**。**開始前にマシン状態を確認**（heavy-job preflight）。夜間・分割で回す。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

```
episodes/PD-2026-056-postoffice/05_visuals/asset_manifest.v001.json
   ↑ Aが生成（唯一の生産者）        ↓ Bが消費（唯一の消費者・検証者）
```

**Bはこのファイル以外のAの中間生成物を読まない。Aはこのファイル以外のBの成果物に依存しない。** counts / role enum / overlay枚数 / also_thumb集合 / thumb_face枚数 を **A(producer)とB(consumer/validator)で一字一致**で共有する（§4）。

> ★★ **EP45 の事故（本作で必ず回避）:** EP45 は asset_manifest に **stills しか埋めず factory/motion 配列を空のまま**出荷しかけた。**本作の `factory` 配列は 235 エントリ、`motion` 配列は 42 エントリ、`overlay` 配列は 30 エントリを必ず public_path 付きで実体化する**（§4.4／§4.5／§4.6 に全 235 + 42 + 30 を列挙済み。build スクリプトはこの列挙を消費するだけで、空配列を書かない）。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | Aの権限 |
|---|---|---|
| `H:\pd-media\assets\ai\postoffice\**` / `H:\pd-media\assets\ai_video\postoffice\**` | **A** | 読み書き |
| `episodes/PD-2026-056-postoffice/05_visuals/**` / `05_stock/**` | **A** | 読み書き（`mkdir(parents=True, exist_ok=True)` で自作） |
| `episodes/PD-2026-056-postoffice/04_scenes/ai_prompts.v001.md` | **A**（`generate_sdxl_4k.py` の入力） | 読み書き。B は読むだけ |
| `remotion/public/postoffice/{img,factory,motion,overlay,thumb}/**` | **A** | 読み書き |
| `episodes/PD-2026-056-postoffice/manifest.json` `03_script/**` `04_scenes/shotlist*` `08_edit/**` `09_package/**` | **B** | **触るな** |
| `remotion/src/**` `remotion/props/**` `scripts/ae/**` `scripts/build_postoffice_film.py` | **B** | **触るな** |
| `episodes/PD-2026-039-*/**` 〜 `episodes/PD-2026-055-*/**` および EP39〜55 の素材 | 別エージェント | **絶対に触るな。読み取りのみ可** |

## 0.3 A が使う／作るスクリプト

**★既存スクリプトをそのまま使う（新規に作らない）:**

| パス | 役割 | 引数 |
|---|---|---|
| `scripts/generate_sdxl_4k.py`（**既存**） | §5 の SDXL 生成（`04_scenes/ai_prompts.v001.md` を読む） | `PD-2026-056-postoffice`（variants 指定なし） / `56 --only S001` |
| `scripts/build_footage_contact_sheet.py`（**既存**） | §6/§7 の全点目視コンタクトシート | `--ep PD-2026-056-postoffice --media image` / `--media video --dir <staging>` |
| `scripts/select_factory_assets.py`（**既存**） | §7 の factory 候補出し | `--kind video --query <kw> --limit N --exclude-used --ep PD-2026-056-postoffice --json` |
| `scripts/check_visual_asset_qc.py`（**既存**） | §0.4 の factory 全点目視ゲート | `--ep PD-2026-056-postoffice` |

> **★`gen_depth_maps.py` は使わない**（本作は depth treatment を使わない＝depth map 不要・§6.4／DESIGN §1「footage treatment は bleed/parallax/duotone/focus、depth 禁止」）。

**★Aが新規作成するスクリプト（直近既存の複製。実在を `ls scripts/` で確認してから複製。これ以外を新規に作らない）:**

| パス | 役割 | 下敷き（実在確認してから・直近の `*burge*`(EP55) を優先、無ければ `*morton*`(EP52)） |
|---|---|---|
| `scripts/qc_postoffice_stills.py` | §6 の静止画QC＋解像度チェック | `scripts/qc_burge_stills.py`（無ければ `qc_morton_stills.py`） |
| `scripts/select_postoffice_factory.py` | §7 の factory 235本の確定選定・EP39〜55 sha256 除外検証 | `scripts/select_burge_factory.py`（無ければ `select_morton_factory.py`） |
| `scripts/comfy_wan_postoffice.py` | §8 の i2v 42本（Wan 2.2 A14B ドライバ・**パスと SHOTS だけ差し替え**） | `scripts/comfy_wan_burge.py`（実在確認） |
| `scripts/rife_postoffice.py` | §8.4 の RIFE 4x → 48fps | `scripts/rife_burge.py`（実在確認） |
| `scripts/build_postoffice_asset_manifest.py` | §4 の境界契約マニフェストを出力・自己検証 | `scripts/build_burge_asset_manifest.py` |
| `scripts/stage_postoffice_assets.py` | §10 の staging | `scripts/stage_burge_assets.py` |

> **SDXL 生成スクリプトを新規に作らない。** `generate_sdxl_4k.py` が既にある。あなたは **`ai_prompts.v001.md` を §5.9 の2行形式で書く**だけ。**実在しないスクリプトを捏造しない。**
> **正確性ゲートは `check_postoffice_facts.py`（B が clone して実装・DESIGN/A/B で同名）。** A が書く全文字列（プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`）は §1.2 の制約に一致し、`check_postoffice_facts.py` を将来通せる文言でなければならない。

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
cd C:\Users\aab15\Documents\prime-documentary

# [A-DONE-1] 境界契約マニフェストが自己検証を通る
./.venv/Scripts/python.exe scripts/build_postoffice_asset_manifest.py --verify
#   → exit 0。counts が §3/§4 の確定値と一致。全パス実在。sha256 重複ゼロ。
#   → ★factory 配列長==235 / motion 配列長==42 / overlay 配列長==30 が非空で実体化していること（EP45 事故回避の必須不変条件）

# [A-DONE-2] 反復禁止ゲートが素材点数の観点で通る
./.venv/Scripts/python.exe scripts/build_postoffice_asset_manifest.py --reuse-feasibility
#   → still >=210 / motion >=42 / factory >=235 / distinct 合計 >=487 / first-use >=0.70 / avg-uses/source <=1.4

# [A-DONE-3] 静止画の解像度ゲート（長辺 >=3840）
./.venv/Scripts/python.exe scripts/qc_postoffice_stills.py --check-resolution

# [A-DONE-4] factory の視覚QCゲート（★全235本を目で見た記録があること）
./.venv/Scripts/python.exe scripts/check_visual_asset_qc.py --ep PD-2026-056-postoffice

# [A-DONE-5] EP39〜EP55 との素材被りゼロ
./.venv/Scripts/python.exe scripts/select_postoffice_factory.py --verify-no-prior-overlap
#   → 重複 sha256 = 0（EP39〜EP55 のすべてに対して）
```

---

# 1. ★★★ 最優先の絶対条件（正確性制約・ガードレール）★★★

**冤罪被害者（Bates/Misra/Hamilton/Castleton/Thomas ほか）は【無実】＝控訴院（2021-04-23・39件・"an affront to the conscience of the court"）と議会立法（2024 Offences Act s.1(1)）で法的確定＝無実は断定してよい。逆に【個人の刑事訴追はゼロ（2026-05-26 時点・Met 捜査継続中）】＝どの個人（Vennells/Jenkins/investigators…）も犯罪者と示唆する絵・語を作らない。悪役は常に「制度」（Post Office / Fujitsu as institutions — Inquiry Vol 1 §1.9 の adjudicated finding）。ほぼ全principal が存命＝実在人物の顔・肖像・likeness を一切作らない（ITVドラマ俳優も同様）。Martin Griffiths の自死は映像・示唆とも全面禁止（バス・道路・ロープ・薬・遺書・悲嘆顔・うずくまり）＝当該ビートは環境のみ。実在ロゴ（Post Office / Royal Mail / Fujitsu / ITV / BBC / Crown 紋章）を再現しない＝generic な赤看板・赤ポストの形のみ。可読の偽文書・偽帳簿・偽画面・偽新聞を作らない（unreadable smear）。数値は hedged（~1,000 / ~700 / 236=BBC集計 / £1.6B+ / 13+）。exact-of-record（£74,609.84・15 months・£321,000・555・39・2021-04-23・2024-01-01・2024-05-24・£600,000・619〔MoJ MI 2026-06-30・R3で611から更新〕）は断定可。捏造引用禁止。時代考証 1999–2026 の英国。**

## 1.1 R1/R2（生成ビジュアル全般）

1. **★R-FACE: 匿名・非識別の人物は可／実在人物の likeness は不可。** 匿名の一般人（実在の誰にも似せない・非識別のドラマ化スタンドイン）＝顔・身体を出してよい（§5.11 H シリーズ・`[HSTYLE]`/`[HNEG]`・§5.12 thumb_face・§5.13 F シリーズ）。ただし **実在人物の顔・likeness・肖像は作らない**＝Sir Alan Bates・Suzanne Sercombe・Seema Misra・Davinder Misra・Jo Hamilton・Lee Castleton・Noel Thomas・Martin Griffiths・Paula Vennells・Gareth Jenkins・Richard Roll・Ron Warmington・Ian Henderson・Simon Clarke・James Arbuthnot・Nick Wallis・Rebecca Thomson・Fraser 判事・Sir Wyn Williams・Rishi Sunak・Paul Patterson・国王・**ITVドラマの俳優（Toby Jones / Monica Dolan ほか）**を似せて描かない。実在人物が示唆される所（支局長・CEO・判事・弁護士・記者・エンジニア）は非識別（背向き/影/逆光/目から下でクロップ/hands-only）を既定に保つ。
2. **★R-SUICIDE（本作の最重要禁止）: 自死を一切描かない・示唆しない。** Griffiths ビート（および全編）で「バス・バス停・道路に立つ人物・車道・ロープ・薬瓶・遺書・別れの手紙・橋の欄干の人物・線路」を**正プロンプトにもネガにも構図にも作らない**。当該ビートの絵は**無人の環境のみ**（灰色の河口・工業地帯の遠景・閉じたシャッター・空の売場）。**悲嘆の顔・泣き崩れ・うずくまり・絶望ポーズも全編禁止**（被害者は常に upright・still・composed）。
3. **可読の偽公文書・偽画面を再現しない。** 判決文・法律・contract・充当書・Gazette・新聞・請願画面・Horizon の帳簿画面の**可読文字を再現しない**（"blurred into an unreadable smear"）。日付（1999/2010/2013/2019/2021/2024 等）・金額（£74,609.84/£321,000/£1.6B）・件数（555/39/236/619）は**画像に描かない**（AE/figures のタイポで出す＝B の担当）。
4. AI画像は概要欄でAI生成を開示 → マニフェストの `ai_disclosure_required: true` を全静止画・全i2vに立てる。全生成ビジュアル表示中は右下に `AI-assisted visualization` を常時表示（オーバーレイは B が付与）。

## 1.2 ★正確性制約（Aが書く全文字列＝プロンプト・`tags`・`caption_hint`・`eyeballed_content`・`notes`・ファイル名に適用。違反はBLOCKER）

1. **R-INNOCENT:** どの被害者にも "thief / fraudster / criminal / guilty" 側の描写・タグを書かない。無実は断定可（"innocent sub-postmistress"）。
2. **R-NOBODY-CONVICTED:** "Vennells convicted / Jenkins guilty / executives jailed / criminal CEO" 等、個人の刑事責任を既成事実化する語を書かない。制度への認定（"the institution knew" 級）は court/inquiry finding の範囲で可。
3. **R-SUICIDE:** "bus, bus stop, man in the road, rope, noose, pills, farewell note, bridge ledge, railway line, suicide, self-harm" を**正プロンプト・`tags`・`caption_hint`・`eyeballed_content`・ファイル名のどこにも書かない**。悲嘆ポーズ語（"weeping, collapsed, crouching in despair"）も同様。共通ネガ `[NEG]`/`[HNEG]`（ai_prompts.md 内のみ）には抑制目的の該当語が含まれている — それ以外の場所に書いたら BLOCKER（§1.3 の機械ゲートは manifest JSON の全文字列を走査する）。
4. **R-FACE:** 実在人物 likeness ゼロ（§1.1-1）。匿名一般人（"anonymous / generic / non-identifiable person, face turned or in shadow"）は許可。
5. **R-LOGO:** "Post Office logo, Royal Mail logo, Fujitsu logo, ITV logo, royal crest, crown emblem" を書かない。看板・ポストは "generic red post office sign / generic British red pillar box, no readable lettering, no emblem" と書く。
6. **R-READABLE:** 可読の偽文書・偽画面禁止。"legible ledger / readable letter / readable judgment / readable petition" を正プロンプトに書かない。画面・書類は必ず "unreadable smear" を添える。
7. **R-NUM:** hedged 数値（~1,000・~700・236・£1.6B・13+）を画像に可読で描かない・断定文で書かない。exact-of-record は AE/figures（B）へ。
8. **R-DOCHL:** **dochighlight を作らない・言及しない**（grep で 0 を保つ）。
9. **R-QUOTE:** 捏造引用禁止。verbatim は FACTS_LEDGER §VERIFIED-VERBATIM の16系統のみ・AE（B）の担当。画像に可読の引用を描かない。
10. **R-DATE/時代考証:** 1999–2026 の英国。左側通行・英国の街灯/信号/ナンバープレート形状（可読不可）・1999ビートは CRT/ブラウン管・2024ビートは薄型TV。**米国の街並み・黄色いスクールバス・米国ポスト・星条旗を混ぜない。**
11. **R-DIGNITY:** 被害者スタンドインの pose は "dignified, upright, still, composed"。"cowering / broken / sobbing / despairing" を書かない。妊婦シルエット（Misra ビート）は**尊厳最優先**＝直立・横顔シルエット・拘束/手錠/dock（被告人檻）と同一フレーム禁止。

## 1.3 機械ゲート（`build_postoffice_asset_manifest.py --verify` の内部）

A が書いた全JSONの全文字列値に対し、1件でもヒットで exit 1:

```python
import re
# 匿名・非識別の人物は許可。実在人物の likeness だけを弾く。
BANNED_PORTRAIT = re.compile(
    r"likeness of (a )?(real|specific|named) person|real[- ]person likeness|"
    r"face of (alan )?(bates|sercombe|misra|hamilton|castleton|thomas|griffiths|vennells|jenkins|"
    r"roll|warmington|henderson|clarke|arbuthnot|wallis|thomson|fraser|wyn williams|sunak|patterson)|"
    r"likeness of (bates|misra|hamilton|castleton|thomas|griffiths|vennells|jenkins|fraser|sunak|the king)|"
    r"toby jones|monica dolan|recognizable (real person|celebrity|actor)|identifiable real person|"
    r"mugshot of (a )?real person|deepfake|深偽|ディープフェイク",
    re.IGNORECASE)
BANNED_ACCURACY = re.compile(
    r"(vennells|jenkins|executive|ceo) (convicted|guilty|jailed|imprisoned)|criminal ceo|"
    r"(thieving|guilty|fraudster) (postmaster|postmistress|sub-postmaster)|"
    r"suicide|self[- ]harm|noose|rope around|pill bottle|farewell note|man (standing )?in the road|"
    r"bus stop|moving bus|bridge ledge|railway line|"
    r"weeping|sobbing|collapsed in grief|cowering|crouching victim|broken victim pose|"
    r"handcuffed|handcuffs on|restrained (person|prisoner)|prison dock with (a )?person|"
    r"post office logo|royal mail logo|fujitsu logo|itv logo|royal crest|crown emblem|"
    r"legible (ledger|letter|document|report|newspaper|judgment|petition|screen)|"
    r"readable (ledger|letter|document|report|newspaper|judgment|petition)|"
    r"school bus|american flag|us mailbox|dochighlight",
    re.IGNORECASE)
```

> **許容:** "a glowing green ledger screen, its figures an unreadable smear / a generic British red pillar box with no emblem / an anonymized sub-postmistress seen only from behind at her counter / a dignified upright silhouette / innocent sub-postmasters exonerated by the Court of Appeal / an empty inquiry witness chair / grey British drizzle light"。禁止は「自死・悲嘆・拘束の表象」「個人の刑事責任の既成事実化」「被害者の有罪示唆」「実在人物 likeness・実在ロゴ」「可読の偽文書/偽画面」「hedged 数値の断定」「dochighlight」。

---

# 2. 台本の語数と尺の確定値（Aが素材点数を積算する根拠）

```
words_total          = 4,750（LOCKED script・fact-locked・R1/R2/R3済み・オーナー帯 4,600–4,750 内）
narration_seconds    = 1,600.2（= 26.67分 @178.1wpm・provisional・FINAL は measured TTS forced-align で上書き）
wpm_used             = 178.1
★HOOK-AUDIO 標準（owner・EP52〜継続）: Brian の声が 0:00 から鳴る（silent runway なし）。
★OPENING FORMULA v2（EP56 が初のネイティブ適用）: cold open ~33s → BUT-loop → ≤5s sting（0:33–0:38・
  gold Bookends の短縮 cut・audio-continuous）→ post-brand 1文。10秒級のフル BrandOpening は本作では使わない。
designed_gap_seconds = 181.8（幕転換の息・AEカード下の music hold・earned breaths ≤3・OST 着地。
                       finished/speech 比 ≈1.12 ∈ 実測 1.04–1.30。check_padding を通る設計ギャップ＝dead air でない）
total_seconds        = 1,791.0（narration 1600.2 + gaps 181.8 + endcard 9.0）= 29:51（band 1740–1860 内）
durationInFrames     = 53,730（provisional・fps30 = 1791×30・VO onset 0.0。TTS実測後に再ロック＝EP55 実績 +71.2s
                       ドリフトは gap 予算で吸収する）
mean_shot            = 3.166秒/カット（picture 1782.0 / 563 cuts）
視覚 acts             = 5（+ HOOK/OPENING/ENDING は別区）
Act 語数配分（provisional・実測 R3 再計測）: COLD+STING+POST ~154 / ACT1 ~868 / ACT2 ~842 / ACT3 ~928 /
                            ACT4 ~903 / ACT5 ~700 / ENDING ~357（合計 = words_total）
```

**Aにとっての意味は1つ:** > **総カット 563 / distinct 487 / 初出 86.50% = still 210 + factory 235 + motion 42。**（§3 で積算）

> **注意（命名差）:** 視覚 act は **0=HOOK/OPENING, 1..5=ACT I..V, 6=ENDING**（7値）。**still は 210 本の固有プロンプトを持つ**ため、still の資産 ID は **S001..S210**（1プロンプト＝1枚）。`covers_scene_id` は still 資産 ID 空間（S001..S210）を指す（§7.3）。

---

# 3. ★素材構成の確定値（この値で調達する・勝手に変えない）

## 3.1 内訳（★勝手に変えない）

| 種別 | distinct | 担当カット | 使用回数(cap) | 調達方法 |
|---|---|---|---|---|
| **SDXL静止画（本編 body）** | **210枚** | 244カット | 1.162回(≤2) | **210本の固有プロンプトで各1枚**（§5・バリエーション0） |
| **factory 実写クリップ** | **235本** | 235カット | **各1回(1)** | 在庫11,000本超＋stock から選抜（§7）・全点目視・EP39〜55 と sha256 被りゼロ |
| **i2v モーション** | **42本** | 84カット | 各2回(≤2) | 42本の固有種プロンプト→Wan（§8） |
| **合計（カットに出る素材）** | **487点** | **563カット** | | |
| 合成レイヤー（particle/light/vfx） | 30本 | — | 重ね掛け | **distinct 素材に数えない**（§9） |
| サムネ emotive-face（thumb_face） | 3枚 | — | 本編カットに出ない | **distinct/cuts に数えない**（§5.12・thumbnail 専用） |

**SDXL の生成バッチ（本編カットに出ない i2v 種・thumb_face を含む）:**

| 用途 | 点数 | 生成 |
|---|---|---|
| body 静止画（`role:"body"`） | **210枚** | 210プロンプト × 1枚 |
| i2v 種画像（`role:"i2v_source"`・body と別 asset） | **42枚** | 42種プロンプト × 1枚 |
| サムネ face（`role:"thumb_face"`・§5.12） | **3枚** | 3プロンプト × 1枚 |
| **SDXL 生成バッチ合計** | **210 + 42 + 3 = 255枚（各1回）** | **variants 指定なし（＝1枚）** |

> **本編サムネの背景 anchor は body 210枚から4枚を `also_thumb:true` で流用選抜**（§4.3a）。**emotive-face（前景の顔）は §5.12 の thumb_face 3枚**（CTR §4A・B が `PostofficeThumbnails.tsx` で face＋hook text を合成）。**role=thumb / still_thumb を作らない。**

## 3.2 幕別配分（★still は確定・factory/i2v は目安。合計だけが確定）

| 区間(act) | still（S番号・確定） | factory（目安） | i2v（確定合計42） | thumb anchor |
|---|---|---|---|---|
| HOOK+OPENING (0) | **14**（S001–S014） | 12 | 3（M01–M03） | S001 |
| ACT1「The Till That Lied」(1) | **36**（S015–S050） | 36 | 7（M04–M10） | — |
| ACT2「Her Employer, Her Prosecutor」(2) | **38**（S051–S088） | 36 | 7（M11–M17） | S057 |
| ACT3「They Knew」(3)（engine・最密） | **40**（S089–S128） | 38 | 8（M18–M25） | S106 |
| ACT4「The Sub-Postmasters' Army」(4) | **38**（S129–S166） | 36 | 7（M26–M32） | — |
| ACT5「The Drama That Moved a Parliament」(5)（climax・cascade） | **30**（S167–S196） | 30 | 6（M33–M38） | S173 |
| ENDING (6) | **14**（S197–S210） | 14 | 4（M39–M42） | — |
| 繋ぎ（covers_scene_id:null） | — | 33 | — | — |
| **合計** | **210** | **235** | **42** | **4** |

> **still の per-act 数（14/36/38/40/38/30/14＝210）は確定**（§5 の motif ライブラリがこの配分で組まれている）。ACT3（無視された警報の engine）が最厚40、ACT5 は climax cascade。**幕別の factory/i2v 内訳は目安値**（合計 235 / 42 のみ確定）。
> **★human-present(★HP) body = 85枚（40.5%・誕生時から）**: ACT1 **16** ／ ACT2 **16** ／ ACT3 **14** ／ ACT4 **16** ／ ACT5 **20** ／ ENDING **3** ／ ACT0 **0**（象徴のみ）。S番号集合は §5.6 の `★HP` ブロックで確定（§5.7 で検算）。

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 563 = still 244 + factory 235 + i2v 84
[2] 平均ショット長 = picture 1782.0 / 563 = 3.166秒/カット  ✓ (≤7.0)
[3] 静止画占有率(check_animation_mix) = 244/563 = 43.34%  ✓ ≤45%（余裕 1.66%pt）
[4] motion coverage = (235+84)/563 = 319/563 = 56.66%     ✓ ≥45%
[5] per-asset 上限: still 244/210=1.162(≤2) / factory 235/235=1.0(≤1) / motion 84/42=2.0(≤2)  ✓
[6] first-use share = 487/563 = 0.8650                    ✓ ≥0.70
[7] avg uses/source = 563/487 = 1.156                     ✓ ≤1.4（EP49 は 1.8 で flag された）
[8] factory 下限 = 1782/30 = 59.4 → ≥60本。設計値 235本 ✓（still-share≤0.45 を守る）
```

> **[3] の余裕は 1.66%pt。** still が210本を割ったら §6.3 の再生成で回復させ、**still-cut 244 を増やさない**（B側の shotlist が244で固定）。

---

# 4. ★境界契約: `asset_manifest.v001.json`（AとBを繋ぐ唯一のファイル）

**パス:** `episodes/PD-2026-056-postoffice/05_visuals/asset_manifest.v001.json`
**スキーマ版:** `postoffice_assets.v1`（固定文字列）
**生産者:** `scripts/build_postoffice_asset_manifest.py`（**A が実装。他の誰もこのファイルを書かない**）
**★A(producer)とB(consumer/validator)で counts / role enum / overlay枚数 / also_thumb集合 / thumb_face枚数 を一字一致。** role enum は **`body | i2v_source | thumb_face | reject` のみ**。also_thumb は body still **ちょうど4枚**。thumb_face は **ちょうど3枚**。overlay は **ちょうど30本**。

## 4.1 スキーマ（`postoffice_assets.v1`）

```jsonc
{
  "schema_version": "postoffice_assets.v1",
  "episode_id": "PD-2026-056-postoffice",
  "slug": "postoffice",
  "generated_at": "<ISO8601>",
  "producer": "scripts/build_postoffice_asset_manifest.py",
  "is_stub": false,
  "counts": {
    "still_body": 210,        // ==210
    "still_i2v_source": 42,   // ==42
    "motion": 42,             // ==42
    "factory": 235,           // ==235
    "overlay": 30,            // ==30（distinct 素材に数えない）
    "thumb_face": 3           // ==3（thumbnail 専用・distinct/cuts に数えない）
  },
  "stills":  [ /* §4.3: body 210 (POH-S001..S210) + i2v_source 42 (POH-MS01..MS42) + thumb_face 3 (POH-T01..T03) */ ],
  "motion":  [ /* §4.5: POH-M01..M42 全42本・public_path 必須（★非空） */ ],
  "factory": [ /* §4.4: 235本・public_path 必須（★非空・EP45事故回避の核心） */ ],
  "overlay": [ /* §4.6: 30本 */ ]
}
```

### 4.1a stills[] のエントリ形（body 例・★depth_path なし）

```jsonc
{
  "asset_id": "POH-S001",                 // body: ^POH-S\d{3}$（001..210）/ i2v種: ^POH-MS\d{2}$ / thumb: ^POH-T\d{2}$
  "scene_id": "S001",                     // still 資産 ID 空間（§5.9 のプロンプト行に対応・S001..S210）
  "role": "body",                         // body|i2v_source|thumb_face|reject
  "also_thumb": false,                    // body から4枚だけ true（§4.3a・追加生成しない）
  "act": 0,                               // 0=HOOK/OPENING, 1..5=ACT I..V, 6=ENDING
  "path": "H:/pd-media/assets/ai/postoffice/S001.png",
  "public_path": "postoffice/img/S001.png",  // role=="body" のみ非null / i2v種・thumb_face は null
  "width": 3840, "height": 2160,          // 長辺>=3840
  "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 23.0,
  "tags": ["ledger_screen","phantom_glow","phosphor_green","symbolic","no_face","no_readable_text"],
  "caption_hint": "a green-on-black accounting terminal glowing alone in a dark village shop, every figure on the screen blurred into an unreadable smear, the machine speaking to no one, no person, no readable text",
  "seed": 0, "model": "juggernautXL_ragnarokBy",
  "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
  "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
         "has_identifiable_real_person": false, "has_human_body": false,
         "has_identifiable_face": false, "has_suicide_or_grief_imagery": false, "notes": ""}
  // ★depth_path は無い（本作は depth treatment 不使用・§6.4）。
  // ★reject トリガは has_readable_text / has_identifiable_real_person / has_suicide_or_grief_imagery のみ。
  //   匿名人体（has_human_body:true）は reject しない。
}
```

## 4.2 `--verify` の不変条件（BLOCKING・B の validator と一字一致）

1. `schema_version=="postoffice_assets.v1"` / `episode_id`/`slug` 一致 / `is_stub==false`
2. `counts.*` が各配列の実長と完全一致し §4.1 の値（body 210 / i2v_source 42 / motion 42 / factory 235 / overlay 30 / thumb_face 3）に**一致**
3. 全 `path`/`public_path` がディスクに実在（**depth_path は要求しない**）
4. `sha256` が全配列を通して一意（重複ゼロ）
5. `role!="reject"` の全静止画で `max(width,height)>=3840`
6. `role=="body"` は `public_path` が非null かつ実在。`role=="i2v_source"`/`role=="thumb_face"` は `public_path==null`
7. **★reject 条件:** `qc.has_readable_text==true` **または** `qc.has_identifiable_real_person==true` **または** `qc.has_suicide_or_grief_imagery==true` は `role=="reject"`。**`qc.has_human_body==true` は reject 条件ではない**（匿名人体は可）。`qc.has_identifiable_face` は「実在人物として識別可能な顔」を意味する（匿名・非識別の顔は可）。H シリーズ（§5.11）・thumb_face（§5.12）は `has_human_body:true`/`has_identifiable_real_person:false`/`has_readable_text:false`/`has_suicide_or_grief_imagery:false`
8. `role=="i2v_source"` は `role=="body"`/`role=="thumb_face"` と**同一 asset_id を共有しない**（i2v_source は `^POH-MS\d{2}$` / thumb_face は `^POH-T\d{2}$`）
9. 全JSON文字列が §1.3 の `BANNED_PORTRAIT` **および** `BANNED_ACCURACY` に一致しない
10. `factory[].license`/`overlay[].license` が `ALLOWED_LICENSES`（§7.4）に含まれる
11. `factory[].sha256` が **EP39〜EP55 の staged 素材**と1件も衝突しない（§7.7）
12. `factory[].eyeballed_content` が空でない
13. `factory[].qc.label_matches_content==true`
14. `also_thumb==true` の本数が**ちょうど4**、かつ `scene_id` 集合が §4.3a の4枚集合と完全一致（**CODEX_B と一字一致必須の A↔B 契約点**）
15. `role` に `thumb`/`still_thumb` が存在しない（enum は body|i2v_source|thumb_face|reject のみ）
16. `overlay` 配列長が**ちょうど30**
17. ★**`factory` 配列長==235 かつ全エントリ `public_path` が非空**（EP45 事故回避）
18. ★**`motion` 配列長==42 かつ全エントリ `public_path` が非空**（同上）
19. **★どの still/motion にも `depth_path` キーを要求しない・生成しない**（depth treatment 不使用・§6.4）

`--reuse-feasibility` では §3.3 [5][6][7][8] を再計算し、1つでも割ったら exit 1。

## 4.3 `role` の割り当て（機械的に決める）

```
1. body 210枚（S001..S210）= §5.6 の210プロンプトの生成物。各1枚。
2. i2v_source 42枚（MS01..MS42 / 種画像 M01_src..M42_src）= §8.1a の42種プロンプトの生成物。各1枚。body に回さない（不変条件8）。
3. thumb_face 3枚（T01..T03 / T01_face..T03_face）= §5.12 の3プロンプトの生成物。public_path==null。
4. also_thumb : body のうち §4.3a の4枚に true（追加生成しない）
5. reject : QCで落ちたもの（マニフェストに残し理由を qc.notes に）→ 落ちたシーンは §6.3 で同一プロンプト再生成
```

### 4.3a ★also_thumb 集合（ちょうど4枚・CODEX_B と一字一致必須）

```
{ POH-S001 (the glowing phantom-ledger screen in a dark village shop — the hook signature),
  POH-S057 (the generic red post-office sign at night in the rain — warmth turned menacing),
  POH-S106 (the wall of identical green terminal screens in the dark — the multiplied lie),
  POH-S173 (the empty inquiry witness chair under lights — the accountability void) }
```

> ★この4集合は §5 の該当 S番号に必ず該当 motif を置くこと（§5 の motif ライブラリで anchor 指定済み）。**前景の emotive face は §5.12 の thumb_face（T01–T03）＝これらは背景 anchor。**

## 4.4 ★`factory[]` 全235エントリ（★必ず実体化・public_path 非空。EP45事故回避の核心）

> `select_postoffice_factory.py` が下表の **public_path / act / covers_scene_id / subtype を pre-assign 済み**として消費し、`asset_id`（棚 id）/`path`（`H:/pd-media/assets/factory/...` or `H:/pd-media/assets/stock/...`）/`sha256`/`duration_sec`/`width`/`height`/`mean_luma`/`license`/`eyeballed_content`/`origin`(`factory`|`stock`)/`qc` を選抜・目視時に埋める（§7）。**空配列を書かない。** 各 public_path は `postoffice/factory/F0NN_<subtype>.mp4`。`type:"backgrounds"`, `kind:"video"`。**subtype の `_02`/`_03` は「同一検索テーマの別クリップ」の意で、別 sha256・別素材（同一ファイルの重複ではない）。**

```jsonc
// HOOK+OPENING (act 0) — 12
{ "public_path":"postoffice/factory/F001_village_high_street_rain_night.mp4", "act":0, "covers_scene_id":"S006", "subtype":"village_high_street_rain_night" }
{ "public_path":"postoffice/factory/F002_red_pillar_box_drizzle.mp4", "act":0, "covers_scene_id":"S008", "subtype":"red_pillar_box_drizzle" }
{ "public_path":"postoffice/factory/F003_dark_shop_interior_counter.mp4", "act":0, "covers_scene_id":null, "subtype":"dark_shop_interior_counter" }
{ "public_path":"postoffice/factory/F004_wet_slate_rooftops_dusk.mp4", "act":0, "covers_scene_id":null, "subtype":"wet_slate_rooftops_dusk" }
{ "public_path":"postoffice/factory/F005_crt_screen_glow_macro.mp4", "act":0, "covers_scene_id":"S011", "subtype":"crt_screen_glow_macro" }
{ "public_path":"postoffice/factory/F006_letterbox_door_mat.mp4", "act":0, "covers_scene_id":null, "subtype":"letterbox_door_mat" }
{ "public_path":"postoffice/factory/F007_uk_country_lane_grey.mp4", "act":0, "covers_scene_id":null, "subtype":"uk_country_lane_grey" }
{ "public_path":"postoffice/factory/F008_low_cloud_hills_grey.mp4", "act":0, "covers_scene_id":null, "subtype":"low_cloud_hills_grey" }
{ "public_path":"postoffice/factory/F009_shop_window_night_light.mp4", "act":0, "covers_scene_id":null, "subtype":"shop_window_night_light" }
{ "public_path":"postoffice/factory/F010_rain_on_window_night.mp4", "act":0, "covers_scene_id":null, "subtype":"rain_on_window_night" }
{ "public_path":"postoffice/factory/F011_village_high_street_rain_night_02.mp4", "act":0, "covers_scene_id":null, "subtype":"village_high_street_rain_night_02" }
{ "public_path":"postoffice/factory/F012_red_pillar_box_drizzle_02.mp4", "act":0, "covers_scene_id":null, "subtype":"red_pillar_box_drizzle_02" }
// ACT1 The Till That Lied (act 1) — 42
{ "public_path":"postoffice/factory/F013_village_shop_exterior_morning.mp4", "act":1, "covers_scene_id":"S015", "subtype":"village_shop_exterior_morning" }
{ "public_path":"postoffice/factory/F014_shop_interior_shelves_warm.mp4", "act":1, "covers_scene_id":"S016", "subtype":"shop_interior_shelves_warm" }
{ "public_path":"postoffice/factory/F015_post_office_counter_brass.mp4", "act":1, "covers_scene_id":"S017", "subtype":"post_office_counter_brass" }
{ "public_path":"postoffice/factory/F016_elderly_queue_high_street.mp4", "act":1, "covers_scene_id":"S036", "subtype":"elderly_queue_high_street" }
{ "public_path":"postoffice/factory/F017_welsh_seafront_grey.mp4", "act":1, "covers_scene_id":"S019", "subtype":"welsh_seafront_grey" }
{ "public_path":"postoffice/factory/F018_welsh_town_street.mp4", "act":1, "covers_scene_id":null, "subtype":"welsh_town_street" }
{ "public_path":"postoffice/factory/F019_cash_till_drawer_macro.mp4", "act":1, "covers_scene_id":"S026", "subtype":"cash_till_drawer_macro" }
{ "public_path":"postoffice/factory/F020_counting_banknotes_hands.mp4", "act":1, "covers_scene_id":"S041", "subtype":"counting_banknotes_hands" }
{ "public_path":"postoffice/factory/F021_paper_ledger_pen_macro.mp4", "act":1, "covers_scene_id":"S023", "subtype":"paper_ledger_pen_macro" }
{ "public_path":"postoffice/factory/F022_crt_terminal_office_1990s.mp4", "act":1, "covers_scene_id":"S022", "subtype":"crt_terminal_office_1990s" }
{ "public_path":"postoffice/factory/F023_delivery_van_village.mp4", "act":1, "covers_scene_id":null, "subtype":"delivery_van_village" }
{ "public_path":"postoffice/factory/F024_telephone_handset_macro.mp4", "act":1, "covers_scene_id":"S027", "subtype":"telephone_handset_macro" }
{ "public_path":"postoffice/factory/F025_kitchen_table_paperwork_night.mp4", "act":1, "covers_scene_id":"S040", "subtype":"kitchen_table_paperwork_night" }
{ "public_path":"postoffice/factory/F026_savings_jar_coins.mp4", "act":1, "covers_scene_id":"S030", "subtype":"savings_jar_coins" }
{ "public_path":"postoffice/factory/F027_british_terraced_street_day.mp4", "act":1, "covers_scene_id":null, "subtype":"british_terraced_street_day" }
{ "public_path":"postoffice/factory/F028_church_and_green_village.mp4", "act":1, "covers_scene_id":null, "subtype":"church_and_green_village" }
{ "public_path":"postoffice/factory/F029_tea_pot_kitchen_warm.mp4", "act":1, "covers_scene_id":null, "subtype":"tea_pot_kitchen_warm" }
{ "public_path":"postoffice/factory/F030_shop_bell_door_macro.mp4", "act":1, "covers_scene_id":null, "subtype":"shop_bell_door_macro" }
{ "public_path":"postoffice/factory/F031_morning_light_shop_window.mp4", "act":1, "covers_scene_id":null, "subtype":"morning_light_shop_window" }
{ "public_path":"postoffice/factory/F032_rainy_village_lane.mp4", "act":1, "covers_scene_id":null, "subtype":"rainy_village_lane" }
{ "public_path":"postoffice/factory/F033_grey_estuary_wales.mp4", "act":1, "covers_scene_id":null, "subtype":"grey_estuary_wales" }
{ "public_path":"postoffice/factory/F034_stone_cottages_hill.mp4", "act":1, "covers_scene_id":null, "subtype":"stone_cottages_hill" }
{ "public_path":"postoffice/factory/F035_quiet_high_street_day.mp4", "act":1, "covers_scene_id":null, "subtype":"quiet_high_street_day" }
{ "public_path":"postoffice/factory/F036_postbox_letters_hand.mp4", "act":1, "covers_scene_id":null, "subtype":"postbox_letters_hand" }
{ "public_path":"postoffice/factory/F037_shopkeeper_shelf_stocking_backs.mp4", "act":1, "covers_scene_id":null, "subtype":"shopkeeper_shelf_stocking_backs" }
{ "public_path":"postoffice/factory/F038_closed_sign_door_macro.mp4", "act":1, "covers_scene_id":null, "subtype":"closed_sign_door_macro" }
{ "public_path":"postoffice/factory/F039_box_files_shelf.mp4", "act":1, "covers_scene_id":"S034", "subtype":"box_files_shelf" }
{ "public_path":"postoffice/factory/F040_receipt_paper_roll_macro.mp4", "act":1, "covers_scene_id":null, "subtype":"receipt_paper_roll_macro" }
{ "public_path":"postoffice/factory/F041_uk_suburban_parade.mp4", "act":1, "covers_scene_id":null, "subtype":"uk_suburban_parade" }
{ "public_path":"postoffice/factory/F042_night_village_one_window.mp4", "act":1, "covers_scene_id":"S033", "subtype":"night_village_one_window" }
{ "public_path":"postoffice/factory/F043_village_shop_exterior_morning_02.mp4", "act":1, "covers_scene_id":null, "subtype":"village_shop_exterior_morning_02" }
{ "public_path":"postoffice/factory/F044_shop_interior_shelves_warm_02.mp4", "act":1, "covers_scene_id":null, "subtype":"shop_interior_shelves_warm_02" }
{ "public_path":"postoffice/factory/F045_cash_till_drawer_macro_02.mp4", "act":1, "covers_scene_id":null, "subtype":"cash_till_drawer_macro_02" }
{ "public_path":"postoffice/factory/F046_kitchen_table_paperwork_night_02.mp4", "act":1, "covers_scene_id":null, "subtype":"kitchen_table_paperwork_night_02" }
{ "public_path":"postoffice/factory/F047_welsh_seafront_grey_02.mp4", "act":1, "covers_scene_id":null, "subtype":"welsh_seafront_grey_02" }
{ "public_path":"postoffice/factory/F048_rainy_village_lane_02.mp4", "act":1, "covers_scene_id":null, "subtype":"rainy_village_lane_02" }
{ "public_path":"postoffice/factory/F049_paper_ledger_pen_macro_02.mp4", "act":1, "covers_scene_id":null, "subtype":"paper_ledger_pen_macro_02" }
{ "public_path":"postoffice/factory/F050_telephone_handset_macro_02.mp4", "act":1, "covers_scene_id":null, "subtype":"telephone_handset_macro_02" }
{ "public_path":"postoffice/factory/F051_british_terraced_street_day_02.mp4", "act":1, "covers_scene_id":null, "subtype":"british_terraced_street_day_02" }
{ "public_path":"postoffice/factory/F052_counting_banknotes_hands_02.mp4", "act":1, "covers_scene_id":null, "subtype":"counting_banknotes_hands_02" }
{ "public_path":"postoffice/factory/F053_stone_cottages_hill_02.mp4", "act":1, "covers_scene_id":null, "subtype":"stone_cottages_hill_02" }
{ "public_path":"postoffice/factory/F054_morning_light_shop_window_02.mp4", "act":1, "covers_scene_id":null, "subtype":"morning_light_shop_window_02" }
// ACT2 Her Employer, Her Prosecutor (act 2) — 42
{ "public_path":"postoffice/factory/F055_dark_saloon_car_street_dawn.mp4", "act":2, "covers_scene_id":"S051", "subtype":"dark_saloon_car_street_dawn" }
{ "public_path":"postoffice/factory/F056_briefcase_documents_table.mp4", "act":2, "covers_scene_id":"S052", "subtype":"briefcase_documents_table" }
{ "public_path":"postoffice/factory/F057_uk_courtroom_empty.mp4", "act":2, "covers_scene_id":"S058", "subtype":"uk_courtroom_empty" }
{ "public_path":"postoffice/factory/F058_court_exterior_stone_grey.mp4", "act":2, "covers_scene_id":"S067", "subtype":"court_exterior_stone_grey" }
{ "public_path":"postoffice/factory/F059_barrister_wig_gown_detail.mp4", "act":2, "covers_scene_id":"S059", "subtype":"barrister_wig_gown_detail" }
{ "public_path":"postoffice/factory/F060_legal_files_stack_red_tape.mp4", "act":2, "covers_scene_id":"S055", "subtype":"legal_files_stack_red_tape" }
{ "public_path":"postoffice/factory/F061_yorkshire_harbour_trawlers.mp4", "act":2, "covers_scene_id":"S060", "subtype":"yorkshire_harbour_trawlers" }
{ "public_path":"postoffice/factory/F062_seaside_town_grey_front.mp4", "act":2, "covers_scene_id":"S061", "subtype":"seaside_town_grey_front" }
{ "public_path":"postoffice/factory/F063_for_sale_sign_street.mp4", "act":2, "covers_scene_id":"S063", "subtype":"for_sale_sign_street" }
{ "public_path":"postoffice/factory/F064_empty_living_room_boxes.mp4", "act":2, "covers_scene_id":"S064", "subtype":"empty_living_room_boxes" }
{ "public_path":"postoffice/factory/F065_suburban_rail_station_parade.mp4", "act":2, "covers_scene_id":"S065", "subtype":"suburban_rail_station_parade" }
{ "public_path":"postoffice/factory/F066_prison_wall_long_grey.mp4", "act":2, "covers_scene_id":"S068", "subtype":"prison_wall_long_grey" }
{ "public_path":"postoffice/factory/F067_high_window_light_shaft.mp4", "act":2, "covers_scene_id":"S069", "subtype":"high_window_light_shaft" }
{ "public_path":"postoffice/factory/F068_birthday_candles_dim.mp4", "act":2, "covers_scene_id":"S071", "subtype":"birthday_candles_dim" }
{ "public_path":"postoffice/factory/F069_envelope_stack_rubber_band.mp4", "act":2, "covers_scene_id":"S072", "subtype":"envelope_stack_rubber_band" }
{ "public_path":"postoffice/factory/F070_court_corridor_benches.mp4", "act":2, "covers_scene_id":null, "subtype":"court_corridor_benches" }
{ "public_path":"postoffice/factory/F071_solicitor_office_desk.mp4", "act":2, "covers_scene_id":null, "subtype":"solicitor_office_desk" }
{ "public_path":"postoffice/factory/F072_family_photos_hall_blur.mp4", "act":2, "covers_scene_id":null, "subtype":"family_photos_hall_blur" }
{ "public_path":"postoffice/factory/F073_school_gates_afternoon.mp4", "act":2, "covers_scene_id":null, "subtype":"school_gates_afternoon" }
{ "public_path":"postoffice/factory/F074_rainy_town_square.mp4", "act":2, "covers_scene_id":null, "subtype":"rainy_town_square" }
{ "public_path":"postoffice/factory/F075_hospital_corridor_dim.mp4", "act":2, "covers_scene_id":null, "subtype":"hospital_corridor_dim" }
{ "public_path":"postoffice/factory/F076_removal_van_street.mp4", "act":2, "covers_scene_id":null, "subtype":"removal_van_street" }
{ "public_path":"postoffice/factory/F077_auction_house_interior.mp4", "act":2, "covers_scene_id":null, "subtype":"auction_house_interior" }
{ "public_path":"postoffice/factory/F078_bank_counter_1990s.mp4", "act":2, "covers_scene_id":null, "subtype":"bank_counter_1990s" }
{ "public_path":"postoffice/factory/F079_court_steps_grey.mp4", "act":2, "covers_scene_id":null, "subtype":"court_steps_grey" }
{ "public_path":"postoffice/factory/F080_street_lamp_rain_halo.mp4", "act":2, "covers_scene_id":null, "subtype":"street_lamp_rain_halo" }
{ "public_path":"postoffice/factory/F081_uk_courtroom_empty_02.mp4", "act":2, "covers_scene_id":null, "subtype":"uk_courtroom_empty_02" }
{ "public_path":"postoffice/factory/F082_prison_wall_long_grey_02.mp4", "act":2, "covers_scene_id":null, "subtype":"prison_wall_long_grey_02" }
{ "public_path":"postoffice/factory/F083_legal_files_stack_red_tape_02.mp4", "act":2, "covers_scene_id":null, "subtype":"legal_files_stack_red_tape_02" }
{ "public_path":"postoffice/factory/F084_dark_saloon_car_street_dawn_02.mp4", "act":2, "covers_scene_id":null, "subtype":"dark_saloon_car_street_dawn_02" }
{ "public_path":"postoffice/factory/F085_yorkshire_harbour_trawlers_02.mp4", "act":2, "covers_scene_id":null, "subtype":"yorkshire_harbour_trawlers_02" }
{ "public_path":"postoffice/factory/F086_empty_living_room_boxes_02.mp4", "act":2, "covers_scene_id":null, "subtype":"empty_living_room_boxes_02" }
{ "public_path":"postoffice/factory/F087_court_exterior_stone_grey_02.mp4", "act":2, "covers_scene_id":null, "subtype":"court_exterior_stone_grey_02" }
{ "public_path":"postoffice/factory/F088_envelope_stack_rubber_band_02.mp4", "act":2, "covers_scene_id":null, "subtype":"envelope_stack_rubber_band_02" }
{ "public_path":"postoffice/factory/F089_rainy_town_square_02.mp4", "act":2, "covers_scene_id":null, "subtype":"rainy_town_square_02" }
{ "public_path":"postoffice/factory/F090_court_corridor_benches_02.mp4", "act":2, "covers_scene_id":null, "subtype":"court_corridor_benches_02" }
{ "public_path":"postoffice/factory/F091_high_window_light_shaft_02.mp4", "act":2, "covers_scene_id":null, "subtype":"high_window_light_shaft_02" }
{ "public_path":"postoffice/factory/F092_seaside_town_grey_front_02.mp4", "act":2, "covers_scene_id":null, "subtype":"seaside_town_grey_front_02" }
{ "public_path":"postoffice/factory/F093_street_lamp_rain_halo_02.mp4", "act":2, "covers_scene_id":null, "subtype":"street_lamp_rain_halo_02" }
{ "public_path":"postoffice/factory/F094_suburban_rail_station_parade_02.mp4", "act":2, "covers_scene_id":null, "subtype":"suburban_rail_station_parade_02" }
{ "public_path":"postoffice/factory/F095_briefcase_documents_table_02.mp4", "act":2, "covers_scene_id":null, "subtype":"briefcase_documents_table_02" }
{ "public_path":"postoffice/factory/F096_solicitor_office_desk_02.mp4", "act":2, "covers_scene_id":null, "subtype":"solicitor_office_desk_02" }
// ACT3 They Knew (act 3) — 44
{ "public_path":"postoffice/factory/F097_server_room_racks_green.mp4", "act":3, "covers_scene_id":"S091", "subtype":"server_room_racks_green" }
{ "public_path":"postoffice/factory/F098_data_centre_corridor.mp4", "act":3, "covers_scene_id":null, "subtype":"data_centre_corridor" }
{ "public_path":"postoffice/factory/F099_office_park_night_one_floor.mp4", "act":3, "covers_scene_id":"S094", "subtype":"office_park_night_one_floor" }
{ "public_path":"postoffice/factory/F100_error_log_screen_blur.mp4", "act":3, "covers_scene_id":"S092", "subtype":"error_log_screen_blur" }
{ "public_path":"postoffice/factory/F101_call_centre_night_rows.mp4", "act":3, "covers_scene_id":"S122", "subtype":"call_centre_night_rows" }
{ "public_path":"postoffice/factory/F102_headset_desk_night.mp4", "act":3, "covers_scene_id":"S093", "subtype":"headset_desk_night" }
{ "public_path":"postoffice/factory/F103_accountants_office_files.mp4", "act":3, "covers_scene_id":"S098", "subtype":"accountants_office_files" }
{ "public_path":"postoffice/factory/F104_magnifier_ledger_printout.mp4", "act":3, "covers_scene_id":"S099", "subtype":"magnifier_ledger_printout" }
{ "public_path":"postoffice/factory/F105_meeting_table_empty_long.mp4", "act":3, "covers_scene_id":"S101", "subtype":"meeting_table_empty_long" }
{ "public_path":"postoffice/factory/F106_legal_brief_pink_ribbon.mp4", "act":3, "covers_scene_id":"S102", "subtype":"legal_brief_pink_ribbon" }
{ "public_path":"postoffice/factory/F107_office_shredder_basket.mp4", "act":3, "covers_scene_id":"S104", "subtype":"office_shredder_basket" }
{ "public_path":"postoffice/factory/F108_shredded_paper_strips_macro.mp4", "act":3, "covers_scene_id":"S105", "subtype":"shredded_paper_strips_macro" }
{ "public_path":"postoffice/factory/F109_filing_drawer_closing_dim.mp4", "act":3, "covers_scene_id":"S107", "subtype":"filing_drawer_closing_dim" }
{ "public_path":"postoffice/factory/F110_grey_estuary_industrial_far.mp4", "act":3, "covers_scene_id":"S108", "subtype":"grey_estuary_industrial_far" }
{ "public_path":"postoffice/factory/F111_closed_shop_shutter_grey.mp4", "act":3, "covers_scene_id":"S109", "subtype":"closed_shop_shutter_grey" }
{ "public_path":"postoffice/factory/F112_bankers_boxes_taped.mp4", "act":3, "covers_scene_id":"S111", "subtype":"bankers_boxes_taped" }
{ "public_path":"postoffice/factory/F113_tv_studio_dark_rig.mp4", "act":3, "covers_scene_id":"S112", "subtype":"tv_studio_dark_rig" }
{ "public_path":"postoffice/factory/F114_tv_glow_living_room.mp4", "act":3, "covers_scene_id":"S113", "subtype":"tv_glow_living_room" }
{ "public_path":"postoffice/factory/F115_corporate_letterhead_blur.mp4", "act":3, "covers_scene_id":"S114", "subtype":"corporate_letterhead_blur" }
{ "public_path":"postoffice/factory/F116_westminster_hall_interior.mp4", "act":3, "covers_scene_id":"S120", "subtype":"westminster_hall_interior" }
{ "public_path":"postoffice/factory/F117_committee_room_green_leather.mp4", "act":3, "covers_scene_id":"S121", "subtype":"committee_room_green_leather" }
{ "public_path":"postoffice/factory/F118_boardroom_glass_night.mp4", "act":3, "covers_scene_id":"S123", "subtype":"boardroom_glass_night" }
{ "public_path":"postoffice/factory/F119_office_desks_late_night.mp4", "act":3, "covers_scene_id":"S124", "subtype":"office_desks_late_night" }
{ "public_path":"postoffice/factory/F120_frosted_glass_door_office.mp4", "act":3, "covers_scene_id":null, "subtype":"frosted_glass_door_office" }
{ "public_path":"postoffice/factory/F121_keyboard_hands_dark_macro.mp4", "act":3, "covers_scene_id":null, "subtype":"keyboard_hands_dark_macro" }
{ "public_path":"postoffice/factory/F122_mainframe_tape_reels_90s.mp4", "act":3, "covers_scene_id":null, "subtype":"mainframe_tape_reels_90s" }
{ "public_path":"postoffice/factory/F123_document_boxes_corridor.mp4", "act":3, "covers_scene_id":null, "subtype":"document_boxes_corridor" }
{ "public_path":"postoffice/factory/F124_microfilm_reader_glow.mp4", "act":3, "covers_scene_id":null, "subtype":"microfilm_reader_glow" }
{ "public_path":"postoffice/factory/F125_london_office_towers_dusk.mp4", "act":3, "covers_scene_id":null, "subtype":"london_office_towers_dusk" }
{ "public_path":"postoffice/factory/F126_rain_window_office_night.mp4", "act":3, "covers_scene_id":null, "subtype":"rain_window_office_night" }
{ "public_path":"postoffice/factory/F127_fluorescent_stairwell_dim.mp4", "act":3, "covers_scene_id":null, "subtype":"fluorescent_stairwell_dim" }
{ "public_path":"postoffice/factory/F128_archive_shelves_dim.mp4", "act":3, "covers_scene_id":null, "subtype":"archive_shelves_dim" }
{ "public_path":"postoffice/factory/F129_server_room_racks_green_02.mp4", "act":3, "covers_scene_id":null, "subtype":"server_room_racks_green_02" }
{ "public_path":"postoffice/factory/F130_call_centre_night_rows_02.mp4", "act":3, "covers_scene_id":null, "subtype":"call_centre_night_rows_02" }
{ "public_path":"postoffice/factory/F131_office_park_night_one_floor_02.mp4", "act":3, "covers_scene_id":null, "subtype":"office_park_night_one_floor_02" }
{ "public_path":"postoffice/factory/F132_meeting_table_empty_long_02.mp4", "act":3, "covers_scene_id":null, "subtype":"meeting_table_empty_long_02" }
{ "public_path":"postoffice/factory/F133_filing_drawer_closing_dim_02.mp4", "act":3, "covers_scene_id":null, "subtype":"filing_drawer_closing_dim_02" }
{ "public_path":"postoffice/factory/F134_tv_glow_living_room_02.mp4", "act":3, "covers_scene_id":null, "subtype":"tv_glow_living_room_02" }
{ "public_path":"postoffice/factory/F135_committee_room_green_leather_02.mp4", "act":3, "covers_scene_id":null, "subtype":"committee_room_green_leather_02" }
{ "public_path":"postoffice/factory/F136_archive_shelves_dim_02.mp4", "act":3, "covers_scene_id":null, "subtype":"archive_shelves_dim_02" }
{ "public_path":"postoffice/factory/F137_rain_window_office_night_02.mp4", "act":3, "covers_scene_id":null, "subtype":"rain_window_office_night_02" }
{ "public_path":"postoffice/factory/F138_document_boxes_corridor_02.mp4", "act":3, "covers_scene_id":null, "subtype":"document_boxes_corridor_02" }
{ "public_path":"postoffice/factory/F139_grey_estuary_industrial_far_02.mp4", "act":3, "covers_scene_id":null, "subtype":"grey_estuary_industrial_far_02" }
{ "public_path":"postoffice/factory/F140_keyboard_hands_dark_macro_02.mp4", "act":3, "covers_scene_id":null, "subtype":"keyboard_hands_dark_macro_02" }
// ACT4 The Sub-Postmasters' Army (act 4) — 42
{ "public_path":"postoffice/factory/F141_printing_press_rolls.mp4", "act":4, "covers_scene_id":"S129", "subtype":"printing_press_rolls" }
{ "public_path":"postoffice/factory/F142_newsstand_magazines_blur.mp4", "act":4, "covers_scene_id":"S130", "subtype":"newsstand_magazines_blur" }
{ "public_path":"postoffice/factory/F143_village_hall_exterior_dusk.mp4", "act":4, "covers_scene_id":"S131", "subtype":"village_hall_exterior_dusk" }
{ "public_path":"postoffice/factory/F144_village_hall_interior_chairs.mp4", "act":4, "covers_scene_id":"S132", "subtype":"village_hall_interior_chairs" }
{ "public_path":"postoffice/factory/F145_tea_urn_trestle_table.mp4", "act":4, "covers_scene_id":null, "subtype":"tea_urn_trestle_table" }
{ "public_path":"postoffice/factory/F146_laptop_kitchen_table_night.mp4", "act":4, "covers_scene_id":"S133", "subtype":"laptop_kitchen_table_night" }
{ "public_path":"postoffice/factory/F147_uk_map_pins_wall.mp4", "act":4, "covers_scene_id":"S134", "subtype":"uk_map_pins_wall" }
{ "public_path":"postoffice/factory/F148_lever_arch_files_trolley.mp4", "act":4, "covers_scene_id":"S135", "subtype":"lever_arch_files_trolley" }
{ "public_path":"postoffice/factory/F149_royal_courts_gothic_exterior.mp4", "act":4, "covers_scene_id":"S137", "subtype":"royal_courts_gothic_exterior" }
{ "public_path":"postoffice/factory/F150_modern_glass_court_building.mp4", "act":4, "covers_scene_id":"S138", "subtype":"modern_glass_court_building" }
{ "public_path":"postoffice/factory/F151_modern_courtroom_empty.mp4", "act":4, "covers_scene_id":"S139", "subtype":"modern_courtroom_empty" }
{ "public_path":"postoffice/factory/F152_judges_bench_red_chair.mp4", "act":4, "covers_scene_id":"S140", "subtype":"judges_bench_red_chair" }
{ "public_path":"postoffice/factory/F153_bound_judgment_volume.mp4", "act":4, "covers_scene_id":"S141", "subtype":"bound_judgment_volume" }
{ "public_path":"postoffice/factory/F154_court_boxes_rain_pavement.mp4", "act":4, "covers_scene_id":"S142", "subtype":"court_boxes_rain_pavement" }
{ "public_path":"postoffice/factory/F155_boardroom_dusk_papers.mp4", "act":4, "covers_scene_id":"S143", "subtype":"boardroom_dusk_papers" }
{ "public_path":"postoffice/factory/F156_invoices_stack_macro.mp4", "act":4, "covers_scene_id":"S144", "subtype":"invoices_stack_macro" }
{ "public_path":"postoffice/factory/F157_referral_tags_case_files.mp4", "act":4, "covers_scene_id":"S145", "subtype":"referral_tags_case_files" }
{ "public_path":"postoffice/factory/F158_court_steps_wide_grey.mp4", "act":4, "covers_scene_id":"S146", "subtype":"court_steps_wide_grey" }
{ "public_path":"postoffice/factory/F159_press_microphones_cluster.mp4", "act":4, "covers_scene_id":"S147", "subtype":"press_microphones_cluster" }
{ "public_path":"postoffice/factory/F160_shop_counter_relit_warm.mp4", "act":4, "covers_scene_id":"S148", "subtype":"shop_counter_relit_warm" }
{ "public_path":"postoffice/factory/F161_boarded_shopfront_sign.mp4", "act":4, "covers_scene_id":"S149", "subtype":"boarded_shopfront_sign" }
{ "public_path":"postoffice/factory/F162_newspaper_stack_blur.mp4", "act":4, "covers_scene_id":"S150", "subtype":"newspaper_stack_blur" }
{ "public_path":"postoffice/factory/F163_umbrella_crowd_street_rain.mp4", "act":4, "covers_scene_id":null, "subtype":"umbrella_crowd_street_rain" }
{ "public_path":"postoffice/factory/F164_camera_flashes_night_blur.mp4", "act":4, "covers_scene_id":null, "subtype":"camera_flashes_night_blur" }
{ "public_path":"postoffice/factory/F165_london_taxi_rain_street.mp4", "act":4, "covers_scene_id":null, "subtype":"london_taxi_rain_street" }
{ "public_path":"postoffice/factory/F166_thames_grey_morning.mp4", "act":4, "covers_scene_id":null, "subtype":"thames_grey_morning" }
{ "public_path":"postoffice/factory/F167_city_of_london_dusk.mp4", "act":4, "covers_scene_id":null, "subtype":"city_of_london_dusk" }
{ "public_path":"postoffice/factory/F168_gothic_stone_arch_detail.mp4", "act":4, "covers_scene_id":null, "subtype":"gothic_stone_arch_detail" }
{ "public_path":"postoffice/factory/F169_village_hall_exterior_dusk_02.mp4", "act":4, "covers_scene_id":null, "subtype":"village_hall_exterior_dusk_02" }
{ "public_path":"postoffice/factory/F170_laptop_kitchen_table_night_02.mp4", "act":4, "covers_scene_id":null, "subtype":"laptop_kitchen_table_night_02" }
{ "public_path":"postoffice/factory/F171_royal_courts_gothic_exterior_02.mp4", "act":4, "covers_scene_id":null, "subtype":"royal_courts_gothic_exterior_02" }
{ "public_path":"postoffice/factory/F172_court_steps_wide_grey_02.mp4", "act":4, "covers_scene_id":null, "subtype":"court_steps_wide_grey_02" }
{ "public_path":"postoffice/factory/F173_press_microphones_cluster_02.mp4", "act":4, "covers_scene_id":null, "subtype":"press_microphones_cluster_02" }
{ "public_path":"postoffice/factory/F174_umbrella_crowd_street_rain_02.mp4", "act":4, "covers_scene_id":null, "subtype":"umbrella_crowd_street_rain_02" }
{ "public_path":"postoffice/factory/F175_lever_arch_files_trolley_02.mp4", "act":4, "covers_scene_id":null, "subtype":"lever_arch_files_trolley_02" }
{ "public_path":"postoffice/factory/F176_bound_judgment_volume_02.mp4", "act":4, "covers_scene_id":null, "subtype":"bound_judgment_volume_02" }
{ "public_path":"postoffice/factory/F177_newspaper_stack_blur_02.mp4", "act":4, "covers_scene_id":null, "subtype":"newspaper_stack_blur_02" }
{ "public_path":"postoffice/factory/F178_thames_grey_morning_02.mp4", "act":4, "covers_scene_id":null, "subtype":"thames_grey_morning_02" }
{ "public_path":"postoffice/factory/F179_modern_courtroom_empty_02.mp4", "act":4, "covers_scene_id":null, "subtype":"modern_courtroom_empty_02" }
{ "public_path":"postoffice/factory/F180_uk_map_pins_wall_02.mp4", "act":4, "covers_scene_id":null, "subtype":"uk_map_pins_wall_02" }
{ "public_path":"postoffice/factory/F181_camera_flashes_night_blur_02.mp4", "act":4, "covers_scene_id":null, "subtype":"camera_flashes_night_blur_02" }
{ "public_path":"postoffice/factory/F182_printing_press_rolls_02.mp4", "act":4, "covers_scene_id":null, "subtype":"printing_press_rolls_02" }
// ACT5 The Drama That Moved a Parliament (act 5) — 36
{ "public_path":"postoffice/factory/F183_terraced_street_tv_glow_night.mp4", "act":5, "covers_scene_id":"S167", "subtype":"terraced_street_tv_glow_night" }
{ "public_path":"postoffice/factory/F184_living_room_tv_side_table.mp4", "act":5, "covers_scene_id":"S168", "subtype":"living_room_tv_side_table" }
{ "public_path":"postoffice/factory/F185_parliament_night_river.mp4", "act":5, "covers_scene_id":"S169", "subtype":"parliament_night_river" }
{ "public_path":"postoffice/factory/F186_westminster_clock_dawn.mp4", "act":5, "covers_scene_id":"S170", "subtype":"westminster_clock_dawn" }
{ "public_path":"postoffice/factory/F187_parchment_ribbon_macro.mp4", "act":5, "covers_scene_id":"S171", "subtype":"parchment_ribbon_macro" }
{ "public_path":"postoffice/factory/F188_statute_volume_macro.mp4", "act":5, "covers_scene_id":"S172", "subtype":"statute_volume_macro" }
{ "public_path":"postoffice/factory/F189_hearing_room_empty_wide.mp4", "act":5, "covers_scene_id":"S174", "subtype":"hearing_room_empty_wide" }
{ "public_path":"postoffice/factory/F190_medal_case_dark_cloth.mp4", "act":5, "covers_scene_id":"S175", "subtype":"medal_case_dark_cloth" }
{ "public_path":"postoffice/factory/F191_official_page_macro_blur.mp4", "act":5, "covers_scene_id":"S176", "subtype":"official_page_macro_blur" }
{ "public_path":"postoffice/factory/F192_phone_screen_scroll_blur.mp4", "act":5, "covers_scene_id":"S183", "subtype":"phone_screen_scroll_blur" }
{ "public_path":"postoffice/factory/F193_commuter_train_interior_backs.mp4", "act":5, "covers_scene_id":"S181", "subtype":"commuter_train_interior_backs" }
{ "public_path":"postoffice/factory/F194_office_kitchenette_two_backs.mp4", "act":5, "covers_scene_id":null, "subtype":"office_kitchenette_two_backs" }
{ "public_path":"postoffice/factory/F195_parliament_lobby_walk_backs.mp4", "act":5, "covers_scene_id":null, "subtype":"parliament_lobby_walk_backs" }
{ "public_path":"postoffice/factory/F196_red_dispatch_boxes_carry.mp4", "act":5, "covers_scene_id":null, "subtype":"red_dispatch_boxes_carry" }
{ "public_path":"postoffice/factory/F197_queue_umbrellas_city_street.mp4", "act":5, "covers_scene_id":"S187", "subtype":"queue_umbrellas_city_street" }
{ "public_path":"postoffice/factory/F198_press_annex_laptops_backs.mp4", "act":5, "covers_scene_id":"S188", "subtype":"press_annex_laptops_backs" }
{ "public_path":"postoffice/factory/F199_postman_village_round_back.mp4", "act":5, "covers_scene_id":"S192", "subtype":"postman_village_round_back" }
{ "public_path":"postoffice/factory/F200_envelope_opening_hands_macro.mp4", "act":5, "covers_scene_id":"S193", "subtype":"envelope_opening_hands_macro" }
{ "public_path":"postoffice/factory/F201_solicitors_desk_couple_backs.mp4", "act":5, "covers_scene_id":"S195", "subtype":"solicitors_desk_couple_backs" }
{ "public_path":"postoffice/factory/F202_palace_forecourt_gravel_far.mp4", "act":5, "covers_scene_id":"S196", "subtype":"palace_forecourt_gravel_far" }
{ "public_path":"postoffice/factory/F203_big_ben_clear_day.mp4", "act":5, "covers_scene_id":null, "subtype":"big_ben_clear_day" }
{ "public_path":"postoffice/factory/F204_whitehall_street_grey.mp4", "act":5, "covers_scene_id":null, "subtype":"whitehall_street_grey" }
{ "public_path":"postoffice/factory/F205_tv_studio_lights_warm.mp4", "act":5, "covers_scene_id":null, "subtype":"tv_studio_lights_warm" }
{ "public_path":"postoffice/factory/F206_pub_interior_wall_tv.mp4", "act":5, "covers_scene_id":null, "subtype":"pub_interior_wall_tv" }
{ "public_path":"postoffice/factory/F207_terraced_street_tv_glow_night_02.mp4", "act":5, "covers_scene_id":null, "subtype":"terraced_street_tv_glow_night_02" }
{ "public_path":"postoffice/factory/F208_parliament_night_river_02.mp4", "act":5, "covers_scene_id":null, "subtype":"parliament_night_river_02" }
{ "public_path":"postoffice/factory/F209_hearing_room_empty_wide_02.mp4", "act":5, "covers_scene_id":null, "subtype":"hearing_room_empty_wide_02" }
{ "public_path":"postoffice/factory/F210_queue_umbrellas_city_street_02.mp4", "act":5, "covers_scene_id":null, "subtype":"queue_umbrellas_city_street_02" }
{ "public_path":"postoffice/factory/F211_envelope_opening_hands_macro_02.mp4", "act":5, "covers_scene_id":null, "subtype":"envelope_opening_hands_macro_02" }
{ "public_path":"postoffice/factory/F212_commuter_train_interior_backs_02.mp4", "act":5, "covers_scene_id":null, "subtype":"commuter_train_interior_backs_02" }
{ "public_path":"postoffice/factory/F213_whitehall_street_grey_02.mp4", "act":5, "covers_scene_id":null, "subtype":"whitehall_street_grey_02" }
{ "public_path":"postoffice/factory/F214_postman_village_round_back_02.mp4", "act":5, "covers_scene_id":null, "subtype":"postman_village_round_back_02" }
{ "public_path":"postoffice/factory/F215_phone_screen_scroll_blur_02.mp4", "act":5, "covers_scene_id":null, "subtype":"phone_screen_scroll_blur_02" }
{ "public_path":"postoffice/factory/F216_westminster_clock_dawn_02.mp4", "act":5, "covers_scene_id":null, "subtype":"westminster_clock_dawn_02" }
{ "public_path":"postoffice/factory/F217_official_page_macro_blur_02.mp4", "act":5, "covers_scene_id":null, "subtype":"official_page_macro_blur_02" }
{ "public_path":"postoffice/factory/F218_pub_interior_wall_tv_02.mp4", "act":5, "covers_scene_id":null, "subtype":"pub_interior_wall_tv_02" }
// ENDING (act 6) — 17
{ "public_path":"postoffice/factory/F219_dark_terminal_off_reflection.mp4", "act":6, "covers_scene_id":"S197", "subtype":"dark_terminal_off_reflection" }
{ "public_path":"postoffice/factory/F220_pillar_box_grey_dawn.mp4", "act":6, "covers_scene_id":"S198", "subtype":"pillar_box_grey_dawn" }
{ "public_path":"postoffice/factory/F221_shuttered_branch_faded_sign.mp4", "act":6, "covers_scene_id":"S199", "subtype":"shuttered_branch_faded_sign" }
{ "public_path":"postoffice/factory/F222_corner_shop_open_drizzle.mp4", "act":6, "covers_scene_id":"S200", "subtype":"corner_shop_open_drizzle" }
{ "public_path":"postoffice/factory/F223_draft_volumes_stack_blur.mp4", "act":6, "covers_scene_id":"S201", "subtype":"draft_volumes_stack_blur" }
{ "public_path":"postoffice/factory/F224_hearing_room_half_dark.mp4", "act":6, "covers_scene_id":"S202", "subtype":"hearing_room_half_dark" }
{ "public_path":"postoffice/factory/F225_police_archive_aisle_boxes.mp4", "act":6, "covers_scene_id":"S203", "subtype":"police_archive_aisle_boxes" }
{ "public_path":"postoffice/factory/F226_laptop_closed_dawn_table.mp4", "act":6, "covers_scene_id":"S204", "subtype":"laptop_closed_dawn_table" }
{ "public_path":"postoffice/factory/F227_village_street_first_light.mp4", "act":6, "covers_scene_id":"S205", "subtype":"village_street_first_light" }
{ "public_path":"postoffice/factory/F228_grey_coast_first_light.mp4", "act":6, "covers_scene_id":"S206", "subtype":"grey_coast_first_light" }
{ "public_path":"postoffice/factory/F229_shutter_unlocking_dawn_back.mp4", "act":6, "covers_scene_id":"S208", "subtype":"shutter_unlocking_dawn_back" }
{ "public_path":"postoffice/factory/F230_morning_queue_outside_backs.mp4", "act":6, "covers_scene_id":"S209", "subtype":"morning_queue_outside_backs" }
{ "public_path":"postoffice/factory/F231_sea_rail_figure_backlit.mp4", "act":6, "covers_scene_id":"S210", "subtype":"sea_rail_figure_backlit" }
{ "public_path":"postoffice/factory/F232_dawn_mist_fields_uk.mp4", "act":6, "covers_scene_id":null, "subtype":"dawn_mist_fields_uk" }
{ "public_path":"postoffice/factory/F233_pillar_box_grey_dawn_02.mp4", "act":6, "covers_scene_id":null, "subtype":"pillar_box_grey_dawn_02" }
{ "public_path":"postoffice/factory/F234_village_street_first_light_02.mp4", "act":6, "covers_scene_id":null, "subtype":"village_street_first_light_02" }
{ "public_path":"postoffice/factory/F235_grey_coast_first_light_02.mp4", "act":6, "covers_scene_id":null, "subtype":"grey_coast_first_light_02" }
```

**検算:** 12 + 42 + 42 + 44 + 42 + 36 + 17 = 235 ✓（covers 付き 105本＝ナレの意味に接着・covers null の繋ぎ/情景 130本を act 配分に内包。意味一致 directive[[visual-narration-meaning-match]]のため covers を EP55 比で厚くしてある — B は covers を該当ビートに優先配置する）。

## 4.5 ★`motion[]` 全42エントリ（★必ず実体化・public_path 非空）

> エントリ形は §4.1a 準拠 + 動画フィールド。`asset_id ^POH-M\d{2}$`。`source_still` は §8.1a の種画像、`source_scene_id`=`MS<NN>`。runtime で `sha256`/`width 1280`/`height 720`/`fps 48`/`frames`/`duration_sec`/`qc` を埋める（§8.4）。**空配列を書かない。**

```jsonc
{ "asset_id":"POH-M01", "source_scene_id":"MS01", "source_still":"H:/pd-media/assets/ai/postoffice/M01_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M01_rife.mp4", "public_path":"postoffice/motion/M01_rife.mp4", "act":0, "storyboard":"hook", "tags":["ledger_screen_phantom_glow"] }
{ "asset_id":"POH-M02", "source_scene_id":"MS02", "source_still":"H:/pd-media/assets/ai/postoffice/M02_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M02_rife.mp4", "public_path":"postoffice/motion/M02_rife.mp4", "act":0, "storyboard":"A0-02", "tags":["envelope_on_mat_shadow"] }
{ "asset_id":"POH-M03", "source_scene_id":"MS03", "source_still":"H:/pd-media/assets/ai/postoffice/M03_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M03_rife.mp4", "public_path":"postoffice/motion/M03_rife.mp4", "act":0, "storyboard":"A0-03", "tags":["village_street_night_rain_drift"] }
{ "asset_id":"POH-M04", "source_scene_id":"MS04", "source_still":"H:/pd-media/assets/ai/postoffice/M04_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M04_rife.mp4", "public_path":"postoffice/motion/M04_rife.mp4", "act":1, "storyboard":"A1-01", "tags":["postmistress_serving_warm_back","H01_anon"] }
{ "asset_id":"POH-M05", "source_scene_id":"MS05", "source_still":"H:/pd-media/assets/ai/postoffice/M05_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M05_rife.mp4", "public_path":"postoffice/motion/M05_rife.mp4", "act":1, "storyboard":"A1-02", "tags":["ledger_screen_turns_wrong"] }
{ "asset_id":"POH-M06", "source_scene_id":"MS06", "source_still":"H:/pd-media/assets/ai/postoffice/M06_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M06_rife.mp4", "public_path":"postoffice/motion/M06_rife.mp4", "act":1, "storyboard":"A1-03", "tags":["couple_kitchen_receipts_night","H02_anon"] }
{ "asset_id":"POH-M07", "source_scene_id":"MS07", "source_still":"H:/pd-media/assets/ai/postoffice/M07_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M07_rife.mp4", "public_path":"postoffice/motion/M07_rife.mp4", "act":1, "storyboard":"A1-04", "tags":["till_drawer_slides_open"] }
{ "asset_id":"POH-M08", "source_scene_id":"MS08", "source_still":"H:/pd-media/assets/ai/postoffice/M08_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M08_rife.mp4", "public_path":"postoffice/motion/M08_rife.mp4", "act":1, "storyboard":"A1-05", "tags":["woman_on_helpline_night_back","H03_anon"] }
{ "asset_id":"POH-M09", "source_scene_id":"MS09", "source_still":"H:/pd-media/assets/ai/postoffice/M09_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M09_rife.mp4", "public_path":"postoffice/motion/M09_rife.mp4", "act":1, "storyboard":"A1-06", "tags":["envelope_through_letterbox"] }
{ "asset_id":"POH-M10", "source_scene_id":"MS10", "source_still":"H:/pd-media/assets/ai/postoffice/M10_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M10_rife.mp4", "public_path":"postoffice/motion/M10_rife.mp4", "act":1, "storyboard":"A1-07", "tags":["red_sign_warm_morning_light"] }
{ "asset_id":"POH-M11", "source_scene_id":"MS11", "source_still":"H:/pd-media/assets/ai/postoffice/M11_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M11_rife.mp4", "public_path":"postoffice/motion/M11_rife.mp4", "act":2, "storyboard":"A2-01", "tags":["investigators_approach_dawn_backs","H04_anon"] }
{ "asset_id":"POH-M12", "source_scene_id":"MS12", "source_still":"H:/pd-media/assets/ai/postoffice/M12_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M12_rife.mp4", "public_path":"postoffice/motion/M12_rife.mp4", "act":2, "storyboard":"A2-02", "tags":["charge_sheet_settles_on_desk"] }
{ "asset_id":"POH-M13", "source_scene_id":"MS13", "source_still":"H:/pd-media/assets/ai/postoffice/M13_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M13_rife.mp4", "public_path":"postoffice/motion/M13_rife.mp4", "act":2, "storyboard":"A2-03", "tags":["pregnant_silhouette_corridor_dignified","H05_anon"] }
{ "asset_id":"POH-M14", "source_scene_id":"MS14", "source_still":"H:/pd-media/assets/ai/postoffice/M14_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M14_rife.mp4", "public_path":"postoffice/motion/M14_rife.mp4", "act":2, "storyboard":"A2-04", "tags":["gallery_backs_lean_forward","H06_anon"] }
{ "asset_id":"POH-M15", "source_scene_id":"MS15", "source_still":"H:/pd-media/assets/ai/postoffice/M15_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M15_rife.mp4", "public_path":"postoffice/motion/M15_rife.mp4", "act":2, "storyboard":"A2-05", "tags":["prison_wall_light_shift"] }
{ "asset_id":"POH-M16", "source_scene_id":"MS16", "source_still":"H:/pd-media/assets/ai/postoffice/M16_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M16_rife.mp4", "public_path":"postoffice/motion/M16_rife.mp4", "act":2, "storyboard":"A2-06", "tags":["man_files_court_doors_back","H07_anon"] }
{ "asset_id":"POH-M17", "source_scene_id":"MS17", "source_still":"H:/pd-media/assets/ai/postoffice/M17_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M17_rife.mp4", "public_path":"postoffice/motion/M17_rife.mp4", "act":2, "storyboard":"A2-07", "tags":["envelope_stack_topples_slow"] }
{ "asset_id":"POH-M18", "source_scene_id":"MS18", "source_still":"H:/pd-media/assets/ai/postoffice/M18_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M18_rife.mp4", "public_path":"postoffice/motion/M18_rife.mp4", "act":3, "storyboard":"A3-01", "tags":["report_pages_riffle_cold_light"] }
{ "asset_id":"POH-M19", "source_scene_id":"MS19", "source_still":"H:/pd-media/assets/ai/postoffice/M19_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M19_rife.mp4", "public_path":"postoffice/motion/M19_rife.mp4", "act":3, "storyboard":"A3-02", "tags":["engineer_server_aisle_back","H08_anon"] }
{ "asset_id":"POH-M20", "source_scene_id":"MS20", "source_still":"H:/pd-media/assets/ai/postoffice/M20_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M20_rife.mp4", "public_path":"postoffice/motion/M20_rife.mp4", "act":3, "storyboard":"A3-03", "tags":["cursor_moves_alone_no_hand"] }
{ "asset_id":"POH-M21", "source_scene_id":"MS21", "source_still":"H:/pd-media/assets/ai/postoffice/M21_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M21_rife.mp4", "public_path":"postoffice/motion/M21_rife.mp4", "act":3, "storyboard":"A3-04", "tags":["shredded_strips_fall_basket"] }
{ "asset_id":"POH-M22", "source_scene_id":"MS22", "source_still":"H:/pd-media/assets/ai/postoffice/M22_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M22_rife.mp4", "public_path":"postoffice/motion/M22_rife.mp4", "act":3, "storyboard":"A3-05", "tags":["accountants_pass_page_backs","H09_anon"] }
{ "asset_id":"POH-M23", "source_scene_id":"MS23", "source_still":"H:/pd-media/assets/ai/postoffice/M23_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M23_rife.mp4", "public_path":"postoffice/motion/M23_rife.mp4", "act":3, "storyboard":"A3-06", "tags":["drawer_shuts_over_advice"] }
{ "asset_id":"POH-M24", "source_scene_id":"MS24", "source_still":"H:/pd-media/assets/ai/postoffice/M24_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M24_rife.mp4", "public_path":"postoffice/motion/M24_rife.mp4", "act":3, "storyboard":"A3-07", "tags":["executive_boardroom_window_back","H10_anon"] }
{ "asset_id":"POH-M25", "source_scene_id":"MS25", "source_still":"H:/pd-media/assets/ai/postoffice/M25_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M25_rife.mp4", "public_path":"postoffice/motion/M25_rife.mp4", "act":3, "storyboard":"A3-08", "tags":["grey_estuary_slow_drift_environmental"] }
{ "asset_id":"POH-M26", "source_scene_id":"MS26", "source_still":"H:/pd-media/assets/ai/postoffice/M26_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M26_rife.mp4", "public_path":"postoffice/motion/M26_rife.mp4", "act":4, "storyboard":"A4-01", "tags":["press_rolls_running_blur"] }
{ "asset_id":"POH-M27", "source_scene_id":"MS27", "source_still":"H:/pd-media/assets/ai/postoffice/M27_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M27_rife.mp4", "public_path":"postoffice/motion/M27_rife.mp4", "act":4, "storyboard":"A4-02", "tags":["village_hall_filing_in_backs","H11_anon"] }
{ "asset_id":"POH-M28", "source_scene_id":"MS28", "source_still":"H:/pd-media/assets/ai/postoffice/M28_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M28_rife.mp4", "public_path":"postoffice/motion/M28_rife.mp4", "act":4, "storyboard":"A4-03", "tags":["kitchen_table_laptop_night_back","H12_anon"] }
{ "asset_id":"POH-M29", "source_scene_id":"MS29", "source_still":"H:/pd-media/assets/ai/postoffice/M29_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M29_rife.mp4", "public_path":"postoffice/motion/M29_rife.mp4", "act":4, "storyboard":"A4-04", "tags":["royal_courts_rain_drift"] }
{ "asset_id":"POH-M30", "source_scene_id":"MS30", "source_still":"H:/pd-media/assets/ai/postoffice/M30_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M30_rife.mp4", "public_path":"postoffice/motion/M30_rife.mp4", "act":4, "storyboard":"A4-05", "tags":["claimant_queue_umbrellas_backs","H13_anon"] }
{ "asset_id":"POH-M31", "source_scene_id":"MS31", "source_still":"H:/pd-media/assets/ai/postoffice/M31_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M31_rife.mp4", "public_path":"postoffice/motion/M31_rife.mp4", "act":4, "storyboard":"A4-06", "tags":["court_steps_arms_lift_backs","H14_anon"] }
{ "asset_id":"POH-M32", "source_scene_id":"MS32", "source_still":"H:/pd-media/assets/ai/postoffice/M32_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M32_rife.mp4", "public_path":"postoffice/motion/M32_rife.mp4", "act":4, "storyboard":"A4-07", "tags":["judgment_volume_pages_settle"] }
{ "asset_id":"POH-M33", "source_scene_id":"MS33", "source_still":"H:/pd-media/assets/ai/postoffice/M33_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M33_rife.mp4", "public_path":"postoffice/motion/M33_rife.mp4", "act":5, "storyboard":"A5-01", "tags":["family_sofa_tv_flicker_backs","H15_anon"] }
{ "asset_id":"POH-M34", "source_scene_id":"MS34", "source_still":"H:/pd-media/assets/ai/postoffice/M34_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M34_rife.mp4", "public_path":"postoffice/motion/M34_rife.mp4", "act":5, "storyboard":"A5-02", "tags":["gallery_before_empty_chair_breathing","H16_anon"] }
{ "asset_id":"POH-M35", "source_scene_id":"MS35", "source_still":"H:/pd-media/assets/ai/postoffice/M35_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M35_rife.mp4", "public_path":"postoffice/motion/M35_rife.mp4", "act":5, "storyboard":"A5-03", "tags":["assent_parchment_ribbon_stirs"] }
{ "asset_id":"POH-M36", "source_scene_id":"MS36", "source_still":"H:/pd-media/assets/ai/postoffice/M36_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M36_rife.mp4", "public_path":"postoffice/motion/M36_rife.mp4", "act":5, "storyboard":"A5-04", "tags":["postman_village_street_back","H17_anon"] }
{ "asset_id":"POH-M37", "source_scene_id":"MS37", "source_still":"H:/pd-media/assets/ai/postoffice/M37_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M37_rife.mp4", "public_path":"postoffice/motion/M37_rife.mp4", "act":5, "storyboard":"A5-05", "tags":["hands_open_official_envelope","H18_anon"] }
{ "asset_id":"POH-M38", "source_scene_id":"MS38", "source_still":"H:/pd-media/assets/ai/postoffice/M38_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M38_rife.mp4", "public_path":"postoffice/motion/M38_rife.mp4", "act":5, "storyboard":"A5-06", "tags":["westminster_night_river_light"] }
{ "asset_id":"POH-M39", "source_scene_id":"MS39", "source_still":"H:/pd-media/assets/ai/postoffice/M39_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M39_rife.mp4", "public_path":"postoffice/motion/M39_rife.mp4", "act":6, "storyboard":"A6-01", "tags":["dark_terminal_window_reflection"] }
{ "asset_id":"POH-M40", "source_scene_id":"MS40", "source_still":"H:/pd-media/assets/ai/postoffice/M40_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M40_rife.mp4", "public_path":"postoffice/motion/M40_rife.mp4", "act":6, "storyboard":"A6-02", "tags":["pillar_box_dawn_light_rises"] }
{ "asset_id":"POH-M41", "source_scene_id":"MS41", "source_still":"H:/pd-media/assets/ai/postoffice/M41_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M41_rife.mp4", "public_path":"postoffice/motion/M41_rife.mp4", "act":6, "storyboard":"A6-03", "tags":["village_street_first_light_drizzle"] }
{ "asset_id":"POH-M42", "source_scene_id":"MS42", "source_still":"H:/pd-media/assets/ai/postoffice/M42_src.png", "path":"H:/pd-media/assets/ai_video/postoffice/M42_rife.mp4", "public_path":"postoffice/motion/M42_rife.mp4", "act":6, "storyboard":"A6-04", "tags":["phosphor_dies_to_red_ember"] }
```

**検算:** 42エントリ ✓・全 public_path 非空 ✓（不変条件18）・`^POH-M\d{2}$` ✓・**★H01–H18（匿名人物・18本）は M04/M06/M08・M11/M13/M14/M16・M19/M22/M24・M27/M28/M30/M31・M33/M34/M36/M37 の内数 ✓**（＝42 motion のうち 18 が人物・84 cuts のうち最大36が人物）。残り24本が抽象/象徴。**★どの motion にも「自死・悲嘆・拘束の表象」「実在 likeness」「可読文字」なし（R-SUICIDE/R-FACE/R-READABLE）。**

## 4.6 `overlay[]` 30エントリ（distinct 素材に数えない・15 particle / 10 light / 5 vfx）

```jsonc
{ "public_path":"postoffice/overlay/P01_shop_dust_warm.mp4", "type":"particle_assets", "subtype":"shop_dust_warm", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P02_drizzle_drift_fine.mp4", "type":"particle_assets", "subtype":"drizzle_drift_fine", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P03_rain_on_glass_bokeh.mp4", "type":"particle_assets", "subtype":"rain_on_glass_bokeh", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P04_archive_dust_cold.mp4", "type":"particle_assets", "subtype":"archive_dust_cold", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P05_paper_fiber_drift.mp4", "type":"particle_assets", "subtype":"paper_fiber_drift", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P06_courtroom_dust_shaft.mp4", "type":"particle_assets", "subtype":"courtroom_dust_shaft", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P07_server_room_dust_green.mp4", "type":"particle_assets", "subtype":"server_room_dust_green", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P08_night_air_drift_dark.mp4", "type":"particle_assets", "subtype":"night_air_drift_dark", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P09_morning_dust_grey.mp4", "type":"particle_assets", "subtype":"morning_dust_grey", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P10_fine_grain_dust.mp4", "type":"particle_assets", "subtype":"fine_grain_dust", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P11_drizzle_drift_fine_02.mp4", "type":"particle_assets", "subtype":"drizzle_drift_fine_02", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P12_rain_on_glass_bokeh_02.mp4", "type":"particle_assets", "subtype":"rain_on_glass_bokeh_02", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P13_archive_dust_cold_02.mp4", "type":"particle_assets", "subtype":"archive_dust_cold_02", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P14_paper_fiber_drift_02.mp4", "type":"particle_assets", "subtype":"paper_fiber_drift_02", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/P15_shop_dust_warm_02.mp4", "type":"particle_assets", "subtype":"shop_dust_warm_02", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/L01_phosphor_green_glow.mp4", "type":"light_assets", "subtype":"phosphor_green_glow", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/L02_cold_window_light_bar.mp4", "type":"light_assets", "subtype":"cold_window_light_bar", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/L03_shop_lamp_amber_glow.mp4", "type":"light_assets", "subtype":"shop_lamp_amber_glow", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/L04_tv_flicker_blue_night.mp4", "type":"light_assets", "subtype":"tv_flicker_blue_night", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/L05_grey_overcast_soft_key.mp4", "type":"light_assets", "subtype":"grey_overcast_soft_key", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/L06_fluorescent_flicker_soft.mp4", "type":"light_assets", "subtype":"fluorescent_flicker_soft", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/L07_dawn_light_sweep_grey.mp4", "type":"light_assets", "subtype":"dawn_light_sweep_grey", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/L08_phosphor_green_glow_02.mp4", "type":"light_assets", "subtype":"phosphor_green_glow_02", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/L09_shop_lamp_amber_glow_02.mp4", "type":"light_assets", "subtype":"shop_lamp_amber_glow_02", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/L10_cold_window_light_bar_02.mp4", "type":"light_assets", "subtype":"cold_window_light_bar_02", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/V01_film_grain_fine.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine", "blend_hint":"overlay" }
{ "public_path":"postoffice/overlay/V02_cold_light_noise.mp4", "type":"vfx_overlays", "subtype":"cold_light_noise", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/V03_film_grain_fine_02.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine_02", "blend_hint":"overlay" }
{ "public_path":"postoffice/overlay/V04_green_glitch_min.mp4", "type":"vfx_overlays", "subtype":"green_glitch_min", "blend_hint":"screen" }
{ "public_path":"postoffice/overlay/V05_cold_light_noise_02.mp4", "type":"vfx_overlays", "subtype":"cold_light_noise_02", "blend_hint":"screen" }
```

**検算:** 15 + 10 + 5 = 30 ✓。runtime で `asset_id`/`path`/`sha256`/`license`/`eyeballed_content`/`qc` を埋める。**overlay は `cuts[].src` に出さない。★per-beat の疎なアクセントのみ＝全編常駐の持続レイヤーにしない（DESIGN §1・screen-wash ≤0.07）。scanline/CRT full-frame texture/vignette-wash の overlay を選ばない（CRT の glow は ledger-screen オブジェクト内のみ）。** 発色は B が accent `#C8102E`（signage red）／ledger 系のみ `#3FA66A`（phosphor green）に寄せる想定。**shop-lamp amber（L03/L09）は ACT1 の warm world ＋ ACT4 の resurrection beat 用のみ・tv_flicker（L04）は ACT5 の一夜のみ。** 他話色（electric blue/prison gold/porch amber/teal/crimson/forest-green/violet/plum/steel-cyan/evidence-blue/green-gray #7C9082）を選ばない。

---

# 5. A-1: SDXL 静止画のバッチ生成（210本 × 1枚・バリエーション0）— ★motif ライブラリ方式

## 5.1 生成環境（★既存の `generate_sdxl_4k.py` を使う）

```
API:   http://127.0.0.1:7860（ローカル AUTOMATIC1111・課金なし）
モデル: juggernautXL_ragnarokBy（generate_sdxl_4k.py が自動で set_model）
プロンプト元: episodes/PD-2026-056-postoffice/04_scenes/ai_prompts.v001.md   ← A が §5.9 の形式で書く
出力:  H:\pd-media\assets\ai\postoffice\S<NNN>.png（+ remotion/public/postoffice/ に自動コピー）
2段パイプライン: txt2img 1536x864 → hires 3072x1728 → extras R-ESRGAN 4x+ → 3840x2160（長辺≥3840・冪等スキップ）
```

**ローカルGPU生成に課金は発生しない。** 禁止は ElevenLabs TTS / 課金画像API / アップロードのみ（§12）。

## 5.2 ★210本の作り方＝「motif ライブラリ」テンプレート方式

210 の固有プロンプトを**幕×motifで体系化**する。各 motif に (a) **確定 distinct 枚数**、(b) **S番号レンジ**、(c) **literal プロンプト（全210行 literal 化済み — そのまま転記）** を与える。**S001–S210 の全210行を `ai_prompts.v001.md` にそのまま転記する（変奏を新たに書かない・行を増減しない・S番号を並べ替えない）。** motif 合計が幕の確定 still 数（§3.2）に一致し、全幕合計 210 になることを §5.7 で検算。

> ★**1シーン1枚・variants 0。** 各プロンプト末尾に §5.3 の `[STYLE]`（人物なし象徴 still）**または** §5.11 の `[HSTYLE]`（匿名人物 still）を**全文連結**、`Avoid:` の後に §5.4 `[NEG]`（象徴）**または** §5.11 `[HNEG]`（匿名人物）を**全文連結**。
> **★2レーン構成: 210 body = object/symbolic 125枚（`[STYLE]`+`[NEG]`・人物なし）＋ ★human-present 85枚（40.5%・`[HSTYLE]`+`[HNEG]`・匿名/非識別・背向き/影/silhouette/hands・adults only）。** 該当 S-range は §5.6 で `★HP` と明記。**（誕生時から 85枚＝40.5% — EP52/EP55 の owner directive「人間が映った画像は結構必要」を初期設計に内蔵。）**
> **HARD BAN（不変・両レーン共通）: 自死・悲嘆・拘束の表象なし・実在人物 likeness なし・実在ロゴなし・可読テキストなし・識別可能な子供顔なし。被害者スタンドインは尊厳第一（直立・静・composed）。**

## 5.3 共通スタイル `[STYLE]`（body 125 の象徴 still ＋ 抽象 i2v 種に連結・DESIGN §1 と一字一致）

```
, cinematic still, somber documentary grade, grey British overcast light as the base register, drizzle-flat daylight and soft net-curtain interiors, a generic post-office signage red on street furniture as the one recurring warm-turned-cold note with no readable lettering and no emblem, phosphor green reserved strictly for glowing ledger screens whose figures are always an unreadable smear, a single warm shop-lamp amber note reserved for the world-before beats and one act of restoration only, period-correct United Kingdom 1999 to 2026 with left-side traffic and British street furniture where streets appear, restrained dignified symbolism, telephoto compression and frontal composition, shallow depth of field, low-key soft-shadow lighting, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, symbolic still-life, no people, no visible face, no violence, empty rooms as aftermath, objects and weather as witnesses
```

> **EP39〜EP55 の色語（1語も含めない）:** electric blue / sodium prison gold（EP41）/ porch-amber（EP43・**本作の shop-lamp amber は Act I の「世界の温もり」＋Act IV の1点復活のみ＝accent ではない**）/ teal-green hospital / crimson kitchen（EP45・**本作の red は屋外の看板・ポスト・書類タブのみ＝domestic interior に赤を置かない**）/ forest-green / civil-violet / somber-plum / steel-cyan（EP50）/ evidence-blue #3F5E8C（EP52）/ **interrogation green-gray #7C9082（EP55・本作の phosphor green #3FA66A は「光る画面の中」限定＝部屋の照明色にしない）**。**EP56 の色 = grey British light（基調）＋ signage red `#C8102E`（街路・書類の институт note）＋ phosphor green `#3FA66A`（ledger 画面内のみ）＋ shop-lamp amber `#E4B96B`（Act I ＋ Act IV 復活1点のみ）。INK `#0B0C0D`。**

## 5.4 共通ネガティブ `[NEG]`（各 `Avoid:` の後に全文付ける・A/B 同一）

```
text, words, letters, numbers, captions, watermark, logo, readable document, legible ledger, legible letter, legible newspaper, legible court record, legible screen, post office logo, royal mail logo, fujitsu logo, itv logo, royal crest, crown emblem, license plate, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, human face, front-facing person, Alan Bates, Paula Vennells, Seema Misra, Toby Jones, bus, double-decker bus, person standing in a road, rope, pills, farewell note, weeping face, crying face, cowering figure, collapsed figure, handcuffs, restrained person, prison dock cage with a person, blood, gore, injury, corpse, violence, re-enactment, american street, yellow school bus, us mailbox, stars and stripes, right-side traffic, child, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, evidence-blue bandana, interrogation green-gray, milky haze, foggy wash, scanline, CRT texture overlay, vignette wash
```

> 文字/紙面/画面が必要な絵は「blurred into an unreadable smear」で判読不能に。**自死表象・悲嘆ポーズ・拘束・実在ロゴ・可読の偽公文書を NEG で明示抑制。** この `[NEG]` は象徴 body ＋ 抽象 i2v 種にのみ使う。**人物ビート（§5.11 H シリーズ・§5.12 thumb_face・§5.13 F シリーズ）には使わない**（人物を弾くため）。H/thumb/F は `[HNEG]`/`[TNEG]`/`[FNEG]` を使う。

## 5.5 プロンプトの絶対ルール（210本すべてに適用）

- **body 210 は2レーン（§5.2）:** object/symbolic 125枚＝§5.3/§5.4（人物なし）、**human-present 85枚（40.5%）＝§5.11 `[HSTYLE]`/`[HNEG]`**。
- **可読文字なし。** ledger/letter/newspaper/判決/法/Gazette/請願/画面の可読文字を描かない。画面・書類には必ず "unreadable smear" を添える。
- **自死・悲嘆・拘束・実在ロゴを一切描かない（§1.1-2/§1.2-3/-5）。** Griffiths ビート（S108–S109）は無人の環境のみ。
- **R-INNOCENT/R-NOBODY-CONVICTED:** 被害者を犯罪者に見せる絵・語、個人を有罪に見せる絵・語を作らない。
- **被害者の尊厳（R-DIGNITY）:** スタンドインは upright/still/composed。妊婦シルエット（S075/M13）は直立・横顔・尊厳最優先。
- **grey British light 基調。signage red は街路/書類の note のみ。phosphor green `#3FA66A` は「光る画面の中」のみ。shop-lamp amber `#E4B96B` は ACT1 の world-before ＋ ACT4 の S148 復活1点のみ**（§5.6 の per-act motif で指定）。
- **時代考証:** 1999–2026 の英国。1999–2005 ビートは CRT・ブラウン管・紙台帳の残滓／2024 ビートは薄型TV・スマホ。米国モチーフ禁止。
- **★footage treatment は bleed/parallax/duotone/focus（DESIGN §1）。depth 前提の絵作りをしない。**
- **dochighlight を作らない・書かない。** milky wash / scanline を描かない。

## 5.5a ★反復禁止ルール（EP55 R3++++ で確立・EP56 は誕生時から BINDING）

1. **1ビート内は同一 motif のバリエーション最大2枚。** 同一被写体ブロックの3枚以上量産は禁止（§5.6 は最初からこの制約で組んである — 勝手に増やさない）。
2. **幕をまたぐ motif の再登場は「目に見える状態変化」必須。同状態の撮り直しは禁止。** spine motif の状態連鎖（各状態1–2枚まで・状態語を各プロンプト本文に内蔵済み）:
   - **ledger screen（SIGNATURE A）** = hook flash(S001–S002 のみ) → balanced in a warm shop(S024) → the impossible hole at dawn(S025–S026) → **multiplied into a wall of screens(S106)** → dark, switched off(S197)。**この5状態以外の ledger-screen 行を作らない。**
   - **branch red sign（SIGNATURE B）** = warm village morning(S015) → night rain, cold(S057) → boarded(S149) → （現在形は pillar box が引き取る）。**pillar box** = hook drizzle(S008) → a letter posted into it(S155・★HP) → grey dawn, present day(S198)。
   - **envelope** = on the doormat(S005 hook / S029 昼・別構図) → the stack(S072) → the buried advice(S103/S107) → the state writes back(S171/S176) → the exoneration letter opened(S193–S194)。
   - **counter** = warm and busy(S016) → cold strip-light(S066) → re-lit amber(S148) → unlocked at dawn(S208・★HP)。
   - **kitchen table** = the night search(S040) → the careful man filing(S046) → the parents' repayment(S088) → the campaign(S133/S154) → the laptop closed at dawn(S204)。
3. **Codex one-shot 原則:** 各行1枚・一発で決める。再生成は §6 の QC fail 時のみ（同一プロンプト・別シード1枚・§6.3）。**「複数枚から選ぶ」ためのバリエーション生成は禁止**（variants 0・§5.10 と同義）。
4. **SUICIDE/DIGNITY GATE 不変:** S108–S109（Griffiths 環境）は無人・バスなし・道路の人物なし。全★HP は composed。**§1.1-2/§1.2 R-SUICIDE/R-DIGNITY はどの再構成でも1文字も緩めない。**

## 5.6 ★motif ライブラリ（幕別・distinct 数確定・S番号レンジ・literal 全210行）

> 各 motif ブロックは `motif名 — 枚数 — S番号レンジ`。**全210行 literal 化済み。Codex は各行をそのまま `ai_prompts.v001.md` に転記する（変奏を新たに書かない・行を増減しない・S番号を並べ替えない）。**
> **★`[STYLE]`/`[NEG]`＝人物なし象徴。`★HP`＝§5.11 `[HSTYLE]`/`[HNEG]`（匿名・非識別の人物）。** ★HP 合計 = **85枚（40.5%）**:
> ACT1 **16**（S035–S050）／ACT2 **16**（S073–S088）／ACT3 **14**（S115–S128）／ACT4 **16**（S151–S166）／ACT5 **20**（S177–S196）／ENDING **3**（S208–S210）。**ACT0 は象徴のまま（0）。**
> **★HP anti-samey 変化マトリクス（85枚全体に適用）:** 距離（hands macro／medium／wide／far-wide）×角度（背後正対／後方斜め／over-the-shoulder／high window）×年代 wardrobe（1999／2000s／2010s／2024–26）×光（warm shop lamp／cold strip light／grey daylight／TV glow／phosphor glow／dawn）×setting（shop／kitchen／court／prison visit／village hall／Westminster／inquiry／train／street）×人数（solo／couple／2–4人／queue／gallery crowd）×姿勢（serving／counting／waiting／walking／rising／watching／opening）。**HARD: どの2枚の ★HP も「被写体タイプ＋構図＋光」の3要素同時一致を禁止。** 85行を書き終えたら軸の表で自己監査してから生成に入る。クラスタは §6.1 Q4 phash watch-list に反映済み。

### ACT 0 — HOOK + OPENING（14枚・S001–S014・全て象徴）
- **ledger_screen_hook — 2 — S001–S002**（S001 は also_thumb・**hook signature**・ledger の hook flash はこの2枚だけ）
```
- `S001.png`
A green-on-black accounting terminal glowing alone on the counter of a dark village shop before dawn, every figure on the screen blurred into an unreadable smear, phosphor light pooling on worn wood, the machine speaking to no one, no person, no readable text [STYLE] Avoid: [NEG]
- `S002.png`
A wide view down the dark aisle of a small village shop at night, shelves in shadow on both sides, one distant terminal screen burning green at the post-office counter at the far end, an island of wrong light in a warm world gone dark, no person, no readable text [STYLE] Avoid: [NEG]
```
- **dark_shop_before_dawn — 2 — S003–S004**（無人の売場と入口 — 寄り/引きで差別化）
```
- `S003.png`
A village shop counter in near-darkness before opening, biscuit tins and a till in silhouette, thin grey first light through the blinds striping the floor, the quiet before the number, no person, no readable text [STYLE] Avoid: [NEG]
- `S004.png`
The inside of a village shop door at night, a small brass bell above it and a CLOSED sign turned inward with its lettering an unreadable smear, rain tapping the glass beyond, no person, no readable text [STYLE] Avoid: [NEG]
```
- **envelope_on_mat_hook — 1 — S005**（envelope 連鎖の hook 状態）
```
- `S005.png`
A single brown window envelope lying face-up on a coir doormat inside a dark hallway, the address panel an unreadable smear, cold light from the door glass falling across it like a blade, no person, no readable text [STYLE] Avoid: [NEG]
```
- **village_street_rain — 2 — S006–S007**（夜の高街と屋根 — 別ロケーション・別高度）
```
- `S006.png`
A narrow British village high street at night in steady drizzle, dark shopfronts and one amber window, wet tarmac mirroring a generic red shop sign with no readable lettering, empty and hushed, no people, no readable text [STYLE] Avoid: [NEG]
- `S007.png`
Wet slate rooftops and brick chimneys of an English village at dusk seen from above, drizzle drifting in sheets, one street lamp warming a corner below, grey cloud pressing low, no people, no readable text [STYLE] Avoid: [NEG]
```
- **pillar_box_hook — 1 — S008**（pillar box 連鎖①・hook 状態）
```
- `S008.png`
A generic British red pillar box standing alone on a rainy village corner at first light, no emblem and no readable lettering on its face, paint worn at the slot, drizzle beading on the dome, the state in walking distance, no person, no readable text [STYLE] Avoid: [NEG]
```
- **title_abstract — 2 — S009–S010**（タイトル下地・別テクスチャ）
```
- `S009.png`
An abstract near-black field with soft drifting bands of grey overcast light, like cloud shadow moving over slate, fine grain texture, a title bed of pure weather, no objects, no people, no readable text [STYLE] Avoid: [NEG]
- `S010.png`
An abstract near-black field with a faint horizontal breath of phosphor green light low in the frame, like the afterglow of a switched-off screen, everything else ink dark, no objects, no people, no readable text [STYLE] Avoid: [NEG]
```
- **terminal_cursor_macro — 1 — S011**
```
- `S011.png`
Extreme macro of a single green cursor block glowing on dark curved glass, the surrounding characters dissolved into an unreadable smear, scanless and silent, the machine mid-sentence, no person, no readable text [STYLE] Avoid: [NEG]
```
- **receipts_shoebox — 1 — S012**（object plant・Act IV payoff の種）
```
- `S012.png`
An old shoebox packed tight with years of paper receipts on a kitchen table under lamplight, every slip an unreadable smear, edges soft with handling, a careful life kept in paper, no person, no readable text [STYLE] Avoid: [NEG]
```
- **welsh_coast_grey — 1 — S013**（Bates の海岸のテーゼ）
```
- `S013.png`
A grey Welsh headland meeting a flat silver sea under low cloud, a small seaside town's rooftops huddled at the shore far below, drizzle hanging in the air, patient and unmoved, no people, no readable text [STYLE] Avoid: [NEG]
```
- **village_silhouette_negative_space — 1 — S014**（タイトル用 negative space）
```
- `S014.png`
An English village skyline as a low black silhouette of chimneys and a church tower under a vast ceiling of grey night cloud, one window of warm light, enormous negative space above for type, no people, no readable text [STYLE] Avoid: [NEG]
```

### ACT 1 — THE TILL THAT LIED（36枚・S015–S050 ＝ object 20 + ★HP 16）
- **village_shop_warm — 3 — S015–S017**（S015 = branch red sign 状態①warm・世界の温もり・shop-lamp amber 帯）
```
- `S015.png`
A village corner shop on a bright damp morning, a generic red post-office sign over the door with no readable lettering and no emblem, produce crates and a leaning bicycle outside, warm lamplight inside the glass, the heart of the high street, no people, no readable text [STYLE] Avoid: [NEG]
- `S016.png`
Inside a warm village shop, shelves of sweet jars and tinned goods glowing under a single shop-lamp amber light, the post-office counter at the back with its brass grille, dust motes in the warmth, no people, no readable text [STYLE] Avoid: [NEG]
- `S017.png`
Close still-life on a post-office counter: a worn date stamp and ink pad, a ball of twine, brown paper parcels tied and waiting, coins in a wooden bowl, warm lamplight, the tools of a trusted trade, no person, no readable text [STYLE] Avoid: [NEG]
```
- **pension_day_till — 1 — S018**
```
- `S018.png`
An open till drawer with neat bundled banknotes and sorted coins in warm morning light, a handwritten tally slip beside it blurred to a smear, everything counted and everything correct, no person, no readable text [STYLE] Avoid: [NEG]
```
- **wool_post_wales — 2 — S019–S020**（Craig-y-Don 級の海辺町・別構図）
```
- `S019.png`
A grey North Wales seafront promenade in the late 1990s, painted guesthouse terraces facing a flat pewter sea, a small shop's red sign glowing halfway down the parade, drizzle softening the headland beyond, no people, no readable text [STYLE] Avoid: [NEG]
- `S020.png`
A small Welsh corner shop photographed square-on, wool skeins and postcards in one window and post-office notices in the other, all lettering an unreadable smear, slate hills rising close behind the roofline, no people, no readable text [STYLE] Avoid: [NEG]
```
- **horizon_arrives_1999 — 3 — S021–S023**（進歩として来る機械・搬入/開梱/紙台帳の退場）
```
- `S021.png`
Cardboard equipment boxes stacked on a village shop floor in 1999, printed labels blurred to smears, bubble wrap spilling out, a beige CRT monitor half unpacked, the future arriving by van, no person, no readable text [STYLE] Avoid: [NEG]
- `S022.png`
A beige late-1990s computer terminal newly installed on a scuffed wooden post-office counter, its screen dark and waiting, cables still zip-tied, an old receipt spike beside it, two eras sharing one desk, no person, no readable text [STYLE] Avoid: [NEG]
- `S023.png`
A thick handwritten paper ledger being retired into an archive box, its ruled columns of figures blurred to smears, a pencil laid diagonally across the cover, decades of Wednesday-night arithmetic closed for good, no person, no readable text [STYLE] Avoid: [NEG]
```
- **ledger_balanced_state — 1 — S024**（SIGNATURE A 状態②）
```
- `S024.png`
The green-on-black terminal on a warm shop counter at closing time, its columns aligned and quiet, figures an unreadable smear, lamplight and phosphor sharing the wood amicably, the machine still a servant, no person, no readable text [STYLE] Avoid: [NEG]
```
- **first_shortfall — 2 — S025–S026**（SIGNATURE A 状態③・寄り/引き）
```
- `S025.png`
The same class of green terminal screen now cold in a dark shop at dawn, one impossible total glowing at the foot of a smeared column, phosphor light gone hostile, the first hole in the world, no person, no readable text [STYLE] Avoid: [NEG]
- `S026.png`
An open till drawer with carefully counted stacks of notes and coins laid out in rows beside a glowing green screen, the two totals irreconcilable, cold pre-dawn light through the blind, arithmetic against a wall, no person, no readable text [STYLE] Avoid: [NEG]
```
- **helpline_phone — 1 — S027**
```
- `S027.png`
A 1990s telephone handset lying off its cradle on a dark shop counter, coiled cord hanging to the floor, the green glow of a terminal reflected along the plastic, a call that changed nothing, no person, no readable text [STYLE] Avoid: [NEG]
```
- **contract_clause — 1 — S028**
```
- `S028.png`
A thick printed contract open on a desk under a single cold lamp, one dense clause caught in the light while the rest falls into shadow, every word an unreadable smear, a signature line waiting below, no person, no readable text [STYLE] Avoid: [NEG]
```
- **demand_envelope — 1 — S029**（envelope 連鎖・昼の状態＝S005 と別構図/別光）
```
- `S029.png`
A brown window envelope on a doormat in flat grey daylight, seen from standing height with the shop door and its brass bell above, the address panel a smear, the institution communicating by post, no person, no readable text [STYLE] Avoid: [NEG]
```
- **repayment — 2 — S030–S031**
```
- `S030.png`
A tin savings box open on a kitchen table, emptied, coins and a few folded notes beside a handwritten sum blurred to a smear, tea gone cold in a floral cup, the family absorbing the machine's mistake, no person, no readable text [STYLE] Avoid: [NEG]
- `S031.png`
A set of house keys resting on a stack of remortgage papers on a solicitor's leather desk, the print an unreadable smear, grey window light, a home converted into a debt that never existed, no person, no readable text [STYLE] Avoid: [NEG]
```
- **false_accounting_key — 1 — S032**
```
- `S032.png`
Extreme macro of a single worn ENTER key on a beige keyboard lit only by green screen glow, the legend polished off by use, the most expensive button in England, shallow focus into darkness, no person, no readable text [STYLE] Avoid: [NEG]
```
- **night_village_one_window — 1 — S033**
```
- `S033.png`
A village street at midnight, every window dark except the post-office shop where a pale green light still burns behind the blind, drizzle drifting under one street lamp, someone in there is counting again, no visible person, no readable text [STYLE] Avoid: [NEG]
```
- **bates_records_plant — 1 — S034**（shoebox S012 と対の「几帳面」plant・kitchen-table 連鎖の起点隣接）
```
- `S034.png`
A neat wall of labelled box files and lever-arch folders on home shelves, every spine label an unreadable smear, one folder pulled halfway out, the archive of a man who kept everything, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP postmistress_at_work — 2 — S035–S036**（温かい勤めの背中 — 距離/人数で差別化）
```
- `S035.png`
An anonymized sub-postmistress seen only from behind at her counter, handing a pension book across the brass grille to a customer seen as a soft shape beyond, warm shop-lamp light, wool cardigan and neat bun, the trusted morning ritual, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S036.png`
A far-wide view of elderly customers queueing quietly outside a village shop in morning light, walking sticks and shopping trolleys, seen from across the street so no face reads, a community arranged around one red-signed door, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP family_shop_life — 2 — S037–S038**
```
- `S037.png`
An anonymized couple stocking shelves together in their warm shop after hours, both seen from behind in aprons, one passing tins up to the other, lamplight and easy domesticity, the business that was also a home, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S038.png`
A shopkeeper couple seen from behind in their open doorway at dawn, mugs of tea in hand, looking out at a wet empty village street going silver with first light, unhurried and unafraid, the world before, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP balancing_night — 3 — S039–S041**（探索の夜 — wide/medium/macro）
```
- `S039.png`
An anonymized woman at a shop counter at midnight seen from behind, lit only by the green glow of the terminal she is leaning toward, shoulders set, recounting a till that will not agree, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S040.png`
A husband and wife at a kitchen table late at night seen from behind, a shoebox of receipts open between them, papers sorted into careful piles, one bare bulb overhead, checking each other's arithmetic against a machine, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S041.png`
Macro of work-worn hands recounting a stack of banknotes over a shop counter in cold light, a smeared tally slip pinned under a thumb, the third count of the same money, no face in frame, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP helpline_call — 2 — S042–S043**（電話の孤独 — medium/macro）
```
- `S042.png`
An anonymized woman standing in a dark shop with a telephone receiver to her ear, seen from behind against the green glow of the terminal, cord stretched taut, the loneliest call in England, composed and still, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S043.png`
Macro of a hand gripping a telephone receiver hard enough to whiten the knuckles, green screen light catching the wedding ring, held steady, no face in frame, no distress pose, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP paying_it_back — 2 — S044–S045**
```
- `S044.png`
Hands tipping a jar of saved coins onto a shop counter in flat morning light, coins spreading across the wood, macro from a low angle, the family's rainy-day money meeting the machine's invented rain, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S045.png`
An anonymized man at a 2000s bank counter seen from behind at medium distance, one hand flat on a withdrawal slip whose print is a smear, grey institutional light, emptying an account to pay a fiction, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP the_careful_man — 2 — S046–S047**（Bates lane 起点 — kitchen-table 連鎖状態②）
```
- `S046.png`
A methodical anonymized man at a kitchen table at night seen from behind, filing papers into labelled folders by lamplight, spine straight, a wall calendar beyond blurred to a smear, a man building an archive instead of an apology, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S047.png`
The same class of man seen from behind carrying two heavy box files out of a shop door into grey daylight, shoulders squared, a red-signed frontage above him with lettering smeared, leaving with the evidence, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP terminated — 1 — S048**
```
- `S048.png`
A man and a woman standing close together before their own shuttered shopfront in flat grey light, seen from behind at a respectful distance, her hand through his arm, upright and very still, reading the end of a life they bought, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP village_watches — 2 — S049–S050**
```
- `S049.png`
Neighbours gathered in twos on the far pavement of a village street, seen from far behind under umbrellas, all turned toward a closed shop with a red sign, the quiet arithmetic of gossip, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S050.png`
Two customers seen from behind reading a typed notice taped inside a shop's glass door, its text an unreadable smear, one holding a shopping bag gone slack, grey afternoon, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 2 — HER EMPLOYER, HER PROSECUTOR（38枚・S051–S088 ＝ object 22 + ★HP 16）
- **investigators_arrive — 2 — S051–S052**（到着の環境と道具 — 人は §HP 側）
```
- `S051.png`
A dark saloon car parked outside a village shop at dawn, engine ticking, doors just closed, grey light on wet paint, the shop's warm window suddenly small behind it, no people, no readable text [STYLE] Avoid: [NEG]
- `S052.png`
An official briefcase open on a shop counter, printed forms fanned out with every line a smear, a capped fountain pen laid across them at a precise angle, procedure arriving in leather, no person, no readable text [STYLE] Avoid: [NEG]
```
- **suspension_notice — 1 — S053**
```
- `S053.png`
A typed notice taped inside the glass of a shop door, photographed from the street side, its text an unreadable smear, the warm interior behind it gone dark for the first time in years, drizzle on the glass, no person, no readable text [STYLE] Avoid: [NEG]
```
- **charge_sheet — 2 — S054–S055**（紙のハンマー — macro/引き）
```
- `S054.png`
Macro of a charge sheet's heading block in cold light, two numbered counts visible as smeared lines of type, a stamp mark bleeding through from the reverse, paper with the weight of a cell door, no person, no readable text [STYLE] Avoid: [NEG]
- `S055.png`
A manila prosecution file thick with papers, closed with red legal tape, resting alone in the centre of a wide dark desk, one cold window bar of light across it, no person, no readable text [STYLE] Avoid: [NEG]
```
- **plea_pen — 1 — S056**
```
- `S056.png`
A fountain pen poised a breath above the signature line of a plea form, the form's text an unreadable smear, cold institutional light, the trade offered in ink, no person, no readable text [STYLE] Avoid: [NEG]
```
- **red_sign_state2_night — 1 — S057**（SIGNATURE B 状態②・★also_thumb）
```
- `S057.png`
The same class of generic red post-office sign over a dark village shopfront, now at night in hard rain, lit coldly from a street lamp so the red reads like a warning, no readable lettering, no emblem, windows black behind it, no people, no readable text [STYLE] Avoid: [NEG]
```
- **uk_courtroom — 2 — S058–S059**（無人の法廷・法服の道具）
```
- `S058.png`
An empty British courtroom in wood panelling, tiered benches and a high canopied bench, the royal arms above rendered as an indistinct carved shape, cold daylight through leaded glass, justice as furniture, no people, no readable text [STYLE] Avoid: [NEG]
- `S059.png`
A barrister's white horsehair wig resting on a ribboned brief on a scarred oak table, black gown draped over the chair behind, every page edge a smear, the costume of consequence, no person, no readable text [STYLE] Avoid: [NEG]
```
- **castleton_bridlington — 2 — S060–S061**（ヨークシャー海辺の生活圏）
```
- `S060.png`
A grey Yorkshire harbour at low tide, fishing trawlers leaning on their keels in the mud, gulls hunched on wet rails, a cold wind you can see in the rigging, no people, no readable text [STYLE] Avoid: [NEG]
- `S061.png`
A small seaside-town shopping street out of season, shuttered kiosks and one lit café window, drizzle blowing sideways past a generic red sign with smeared lettering, no people, no readable text [STYLE] Avoid: [NEG]
```
- **costs_ruin — 2 — S062–S063**（£321,000 の物象化）
```
- `S062.png`
Macro of a legal bill of costs, columns of figures cascading down the page as unreadable smears, the final total boxed at the foot and smeared darkest of all, cold white light, arithmetic as a weapon, no person, no readable text [STYLE] Avoid: [NEG]
- `S063.png`
A generic estate agent's sale board wired to a gatepost outside a modest brick house in drizzle, its lettering an unreadable smear, curtains half gone from the windows behind, no people, no readable text [STYLE] Avoid: [NEG]
```
- **bankruptcy_empty_room — 1 — S064**
```
- `S064.png`
An emptied family living room, pale rectangles on the wallpaper where pictures hung, cardboard boxes taped and stacked by the door, one child's drawing pinned low on the wall blurred to coloured smears, grey window light, no people, no readable text [STYLE] Avoid: [NEG]
```
- **westbyfleet_parade — 2 — S065–S066**（Surrey 郊外と冷えた売場 — counter 連鎖状態②）
```
- `S065.png`
A 2000s Surrey suburban parade of shops beneath a brick railway bridge, a small post-office frontage among them with smeared signage, commuter morning light flat and pale, no people, no readable text [STYLE] Avoid: [NEG]
- `S066.png`
Inside a small suburban post office under cold strip light, the counter bare and clinical, security glass smudged, the warmth of the village original entirely absent, a queue barrier standing in an empty room, no people, no readable text [STYLE] Avoid: [NEG]
```
- **crown_court_exterior — 1 — S067**
```
- `S067.png`
A modern British crown court building in pale stone and dark glass under an overcast sky, its name band over the doors an unreadable smear, wet paving reflecting the mass of it, no people, no readable text [STYLE] Avoid: [NEG]
```
- **prison_environment — 2 — S068–S069**（無人・非扇情）
```
- `S068.png`
A long high prison wall in weathered grey brick running the full width of the frame under white sky, a single line of wire along its top, drizzle darkening the pavement below, scale without spectacle, no people, no readable text [STYLE] Avoid: [NEG]
- `S069.png`
A small high window in an institutional wall throwing one narrow shaft of daylight into a bare room, dust drifting through the beam, the world reduced to a rectangle, no person, no readable text [STYLE] Avoid: [NEG]
```
- **tag_object — 1 — S070**
```
- `S070.png`
An electronic monitoring ankle tag lying inert on a bare table in flat grey light, strap open, attached to nothing and no one, a bracelet the state issues, clinical still-life, no person, no readable text [STYLE] Avoid: [NEG]
```
- **birthday_absence — 1 — S071**
```
- `S071.png`
A homemade birthday cake with ten unlit candles waiting on a kitchen table in a dim room, one place set, party napkins folded, the light going grey outside the window, an absence shaped like a mother, no person, no readable text [STYLE] Avoid: [NEG]
```
- **envelope_stack_state — 1 — S072**（envelope 連鎖状態③）
```
- `S072.png`
A thick stack of brown window envelopes bound with a rubber band on a hallway table, address panels all smears, the earliest at the bottom yellowing with age, the institution's patience in paper form, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP investigators_pair — 2 — S073–S074**
```
- `S073.png`
Two anonymized men in dark suits seen only from behind at a village shop's open door at dawn, one holding a briefcase, the shopkeeper beyond reduced to a soft warm-lit shape, cold light on their shoulders, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S074.png`
An over-the-shoulder view from behind an anonymized official across a bare table, a composed interviewee's folded hands and cardigan sleeve visible opposite, papers between them all smears, quiet and procedural, faces never in frame, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP misra_dignity — 2 — S075–S076**（妊婦シルエットの尊厳 — 直立/静・拘束なし・dock なし）
```
- `S075.png`
A pregnant anonymized woman standing upright in profile silhouette in a long corridor of cold institutional light, coat closed over her bump, head level, perfectly still and composed, carried with dignity, no face readable, no restraint, no readable text [HSTYLE] Avoid: [HNEG]
- `S076.png`
An anonymized woman seated alone on a bench seen squarely from behind, hands folded in her lap, hair pinned neatly, a tall cold window far ahead of her, waiting with a straight back, no face, no distress pose, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP family_left_behind — 2 — S077–S078**
```
- `S077.png`
An anonymized man holding a small child's hand at a rain-flecked window, both seen from behind as soft dark shapes against grey light, the child only an out-of-focus outline, a house gone quiet, no faces, no identifiable child, no readable text [HSTYLE] Avoid: [HNEG]
- `S078.png`
A husband alone behind a shop counter seen from behind at medium distance, serving no one, the queue barrier empty, cold strip light on his shoulders, keeping the shop alive for someone absent, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP court_gallery_2000s — 2 — S079–S080**
```
- `S079.png`
A public gallery of anonymized figures seen from directly behind, 2000s coats and scarves, all facing the well of a wood-panelled courtroom below, shoulders tight with listening, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S080.png`
A solicitor and client seen from behind at a table stacked with ring binders, the solicitor's arm extended over one open page smeared white, cold fluorescent light, the arithmetic of a defence, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP self_represented — 2 — S081–S082**（Castleton の孤独 — 移動/対峙）
```
- `S081.png`
An anonymized man alone on a train with an armful of folders on his lap, seen from behind across the carriage, grey towns sliding past the window, a litigant carrying his own case to London, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S082.png`
A wide courtroom view from the rear: one anonymized man standing alone at a lectern facing the high empty bench, no counsel beside him, his files squared in front of him, small and upright in a large room, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP village_judgment — 2 — S083–S084**
```
- `S083.png`
Two neighbours in headscarves seen from far behind, paused mid-conversation on a village pavement, both turned toward a shuttered shop across the road, shopping bags at their feet, the trial before the trial, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S084.png`
An anonymized woman walking briskly past her own former shop, seen from behind under an umbrella, head held level, not looking at the dark window, grey rain light, dignity in motion, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP prison_visit — 2 — S085–S086**
```
- `S085.png`
A wide prison visiting hall seen from the back wall: rows of small tables, visitors seen only as backs in winter coats leaning slightly forward, strip light flattening everything, love conducted across formica, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S086.png`
An anonymized woman at a visitors' reception desk seen from behind, signing a smeared register with one hand and holding a clear bag of coins in the other, institutional signage above her blurred, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP repayment_generation — 2 — S087–S088**（kitchen-table 連鎖状態③＝両親の世代）
```
- `S087.png`
Elderly hands counting folded banknotes into a neat pile on a lace tablecloth, a teapot and a smeared building-society book beside them, macro in soft grey window light, a lifetime's caution changing hands, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S088.png`
An elderly couple seated side by side at their kitchen table seen from behind, papers arranged before them, his hand flat on the table and hers over it, still and resolved, giving their savings to a child's invented debt, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 3 — THEY KNEW（40枚・S089–S128・engine・最密 ＝ object 26 + ★HP 14）
- **ismay_report_2010 — 2 — S089–S090**（「正直さの値段」の文書 — 引き/寄り）
```
- `S089.png`
A bound internal report lying square on a polished executive desk, its title block an unreadable smear, a single cold desk lamp burning above it in a dark office, the price of honesty calculated and filed, no person, no readable text [STYLE] Avoid: [NEG]
- `S090.png`
Macro of one paragraph of a typed corporate report caught in a bar of cold light, the surrounding page falling to black, every word a smear but the shape of a warning unmistakable, no person, no readable text [STYLE] Avoid: [NEG]
```
- **bugs_have_names — 3 — S091–S093**（ベンダー側の壁の向こう）
```
- `S091.png`
A data-centre aisle at night, tall server racks with constellations of small green LEDs receding into darkness, cold air shimmering faintly at the vents, the machine's real home, no people, no readable text [STYLE] Avoid: [NEG]
- `S092.png`
A dark monitor filled with scrolling error-log lines rendered as stuttering smears of green text, one line frozen mid-screen brighter than the rest, a fault with a name nobody outside will hear, no person, no readable text [STYLE] Avoid: [NEG]
- `S093.png`
A support-desk headset abandoned on a desk beside a cold coffee mug at night, three dark monitors behind it, the queue of unheard callers implied by a blinking light, no person, no readable text [STYLE] Avoid: [NEG]
```
- **bracknell_campus — 2 — S094–S095**
```
- `S094.png`
A 1990s-built British office park at night, one floor of one block still lit white against wet trees and empty car parks, the room where branch accounts could be reached, no people, no readable text [STYLE] Avoid: [NEG]
- `S095.png`
A frosted-glass office door with a department name etched as an unreadable smear, cold corridor light behind it, a swipe-card reader glowing one small red point, access most people never knew existed, no person, no readable text [STYLE] Avoid: [NEG]
```
- **remote_reach — 2 — S096–S097**（無人で動く数字）
```
- `S096.png`
A branch terminal in a closed dark shop, its green cursor advancing alone across a smeared line of figures with no hand at the keyboard, phosphor light flickering on the empty chair, no person, no readable text [STYLE] Avoid: [NEG]
- `S097.png`
Two identical green terminal screens side by side in the dark showing the same smeared branch figures, one subtly brighter where a value differs, the double ledger nobody was told about, no person, no readable text [STYLE] Avoid: [NEG]
```
- **second_sight_arrives — 3 — S098–S100**（外からの目）
```
- `S098.png`
A small accountants' office overwhelmed by evidence: banker's boxes stacked to the sill, lever-arch files open on every surface, a desk lamp burning at midday against the grey window, outsiders doing the reading, no people, no readable text [STYLE] Avoid: [NEG]
- `S099.png`
A magnifying glass lying across a fanfold computer printout of branch figures, the columns beneath the lens swelling into larger smears, pencil ticks in the margin, the first honest audit, no person, no readable text [STYLE] Avoid: [NEG]
- `S100.png`
A spiral-bound interim report on a meeting table, cover title a smear, two paper flags marking two pages deep inside, morning light flat across it, two bugs with names now on the record, no person, no readable text [STYLE] Avoid: [NEG]
```
- **mediation_stall — 1 — S101**
```
- `S101.png`
A very long mahogany meeting table set with smeared name cards and untouched water glasses, chairs pushed back at angles as after an ended argument, grey afternoon light down its length, a scheme designed to exhaust, no people, no readable text [STYLE] Avoid: [NEG]
```
- **clarke_advice — 2 — S102–S103**（自前の法廷弁護士の結論 — envelope/advice 連鎖状態④前段）
```
- `S102.png`
A barrister's brief tied in faded pink ribbon on a chambers desk, candle-warm lamp against dark shelves of law reports, the bundle's label an unreadable smear, an opinion nobody upstairs wants, no person, no readable text [STYLE] Avoid: [NEG]
- `S103.png`
Macro of the first page of a typed legal advice, the chambers letterhead shape blurred, dense numbered paragraphs descending as smears, one short final paragraph sitting alone at the foot like a verdict, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_shredding — 2 — S104–S105**（記録の消え方 — 装置/断片）
```
- `S104.png`
An office paper shredder standing beside an executive desk, its bin filled to the brim with fine white strips, a last sheet resting in the feed slot, cold light from a window blind, minutes becoming confetti, no person, no readable text [STYLE] Avoid: [NEG]
- `S105.png`
Extreme macro of shredded paper strips tangled in the bin, fragments of typed characters reduced to meaningless flecks, shallow depth of field, what disclosure looks like after the instruction, no person, no readable text [STYLE] Avoid: [NEG]
```
- **wall_of_screens — 1 — S106**（SIGNATURE A 状態④・★also_thumb）
```
- `S106.png`
A dark space filled with a receding grid of identical green-glowing terminal screens, every screen carrying the same smeared columns, one lie multiplied into an institution, phosphor haze rising off the wall of glass, no people, no readable text [STYLE] Avoid: [NEG]
```
- **advice_buried — 1 — S107**（advice 連鎖状態④・closingdoor）
```
- `S107.png`
A deep file drawer sliding shut over a ribboned legal advice, the pink ribbon's tail the last thing in the light, institutional grey cabinets receding beyond, the conclusion filed where conclusions go to die, no person, no readable text [STYLE] Avoid: [NEG]
```
- **griffiths_environmental — 2 — S108–S109**（⚠⚠ 無人環境のみ・自死表象なし・バスなし・道路の人物なし）
```
- `S108.png`
A wide grey estuary at low tide under a heavy sky, mudflats and still water fading toward a distant industrial horizon, one gull motionless on a post, an enormous quiet, no people, no vehicles, no readable text [STYLE] Avoid: [NEG]
- `S109.png`
A closed village-branch shopfront in early grey morning, shutter down and streaked with old rain, the generic red sign above drained of warmth in the flat light, milk crate empty by the step, no people, no readable text [STYLE] Avoid: [NEG]
```
- **prosecutions_stop — 1 — S110**
```
- `S110.png`
An office out-tray labelled with a smeared strip sitting completely empty on a dark desk, dust settled undisturbed across its base, beside it an in-tray still stacked high, the machine quietly switched off with no announcement, no person, no readable text [STYLE] Avoid: [NEG]
```
- **second_sight_sacked — 1 — S111**
```
- `S111.png`
Banker's boxes sealed with brown tape and stacked by an office door for collection, each side labelled with a smeared marker scrawl, a bare desk and unplugged lamp behind, the investigation packed up mid-sentence, no people, no readable text [STYLE] Avoid: [NEG]
```
- **panorama_2015 — 2 — S112–S113**（放送の光 — スタジオ/居間）
```
- `S112.png`
A dark television studio between recordings, a single interview chair under a switched-off softbox, cables coiled on black floor, the question waiting for airtime, no people, no readable text [STYLE] Avoid: [NEG]
- `S113.png`
A 2015 living room at night lit only by a television's cold flicker, the screen itself out of frame, the glow trembling over an empty armchair and a mug on the arm, a nation half-listening, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_denial — 1 — S114**
```
- `S114.png`
A typed corporate statement on headed paper lying in a pool of cold light, the letterhead reduced to a grey shape and every line a smear, one sentence's underline pressing through the paper, absolute language on thin stock, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP engineer_lane — 2 — S115–S116**
```
- `S115.png`
An anonymized engineer in a lanyard seen only from behind, walking a server aisle at night with a clipboard under one arm, green LEDs streaking both sides, custodian of a machine the country trusts, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S116.png`
Over-the-shoulder view of anonymized hands typing at a dark terminal, the screen's smeared figures reflected in spectacles' edge only as light, cuffs rolled, the reach into a faraway branch, face never in frame, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP outside_examiners — 2 — S117–S118**
```
- `S117.png`
Two anonymized forensic accountants seen from behind at a table drowning in folders, one passing a single page to the other, sleeves rolled, a kettle steaming on a filing cabinet behind, patient outsiders, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S118.png`
An anonymized man carrying an armload of lever-arch files down a long institutional corridor, seen from far behind, strip lights ticking away overhead into darkness, evidence in transit, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP whistleblower — 1 — S119**
```
- `S119.png`
A man's composed silhouette by a window with half-open venetian blinds, seen from behind in three-quarter, daylight striping his shoulders, a man deciding to say on camera what he knows, still and resolved, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP westminster_asks — 2 — S120–S121**
```
- `S120.png`
Suited figures walking away down a vast vaulted Westminster hall, seen from far behind, their footsteps implied in the polished stone, small under the architecture that is supposed to hold power to account, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S121.png`
A committee room seen from the rear public seats: green leather benches, anonymized officials' backs at the witness table, microphones craned toward them, cold daylight through high windows, questions about to be answered carefully, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP helpline_floor — 1 — S122**
```
- `S122.png`
A call-centre floor at night seen from behind the back row: headsetted operators as dark shapes against cubicle glow, dozens of small screens smeared bright, the place where "you're the only one" was said a thousand times, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP executive_floor — 2 — S123–S124**
```
- `S123.png`
An anonymized executive seen only from behind at a floor-to-ceiling boardroom window at night, city lights smeared below, one hand holding printed pages loosely at the thigh, the view from the top of a machine, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S124.png`
Assistants at open-plan desks late at night seen from behind, screens glowing with smeared documents, one desk lamp among the monitors, jackets on chair-backs, an institution drafting its answers, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP savings_book — 1 — S125**（両親の £62,000 の手 — 手元のみ・非悲嘆）
```
- `S125.png`
Elderly hands resting on a closed building-society passbook on a kitchen table, thumb moving over the worn cover, its lettering a smear, steady grey window light, a lifetime of small deposits about to be given away, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP waiting_for_mediation — 1 — S126**
```
- `S126.png`
Former postmasters waiting on a row of corridor chairs seen from behind, coats folded on laps, one leaning to another to murmur, a frosted meeting-room door glowing ahead of them, patience wearing thin, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP mediation_table — 1 — S127**
```
- `S127.png`
A wide mediation room seen from the back corner: two sides of anonymized backs facing each other across a long table, files squared like fortifications, an empty chair at the head, grey light, talks going nowhere slowly, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP reporter_lane — 1 — S128**
```
- `S128.png`
An anonymized reporter typing at a cluttered desk at night seen from behind, one desk lamp, printouts taped to the wall edge-lit and smeared, a story nobody upstairs wants to run, no face, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 4 — THE SUB-POSTMASTERS' ARMY（38枚・S129–S166 ＝ object 22 + ★HP 16）
- **computer_weekly_2009 — 2 — S129–S130**（最初の亀裂）
```
- `S129.png`
Newspaper press rolls thundering in a print hall, a river of pages blurring through the rollers, ink mist in the work lights, seven names about to reach the world, no people, no readable text [STYLE] Avoid: [NEG]
- `S130.png`
A trade magazine on a station newsstand rack among dailies, its cover headline and masthead smeared, one copy turned face-out under fluorescent light, the first crack in a national wall, no people, no readable text [STYLE] Avoid: [NEG]
```
- **fenny_compton_hall — 2 — S131–S132**（真ん中の村の集会所）
```
- `S131.png`
A red-brick village hall at dusk with its windows lit warm yellow, bicycles and a few parked cars outside on the gravel, flat Warwickshire fields fading behind, a meeting about to start in the middle of England, no people, no readable text [STYLE] Avoid: [NEG]
- `S132.png`
Inside an empty village hall before a meeting: stacked chairs part-unstacked, two trestle tables end to end, a tea urn steaming beside cups on a tray, a notice board of smeared flyers, strip light and lino, no people, no readable text [STYLE] Avoid: [NEG]
```
- **campaign_hq_kitchen — 2 — S133–S134**（kitchen-table 連鎖状態④）
```
- `S133.png`
A kitchen table converted to a campaign office at night: an open laptop's glow over stacked box files and highlighted printouts all smeared, a phone face-down, tea going cold, twenty years of evenings looking like this, no person, no readable text [STYLE] Avoid: [NEG]
- `S134.png`
A wall map of Britain bristling with dozens of small pins from Cornwall to the Highlands, threads of shadow under a desk lamp's raking light, no labels readable, the only-ones plotted as a country, no person, no readable text [STYLE] Avoid: [NEG]
```
- **group_litigation — 2 — S135–S136**
```
- `S135.png`
A porter's trolley stacked with lever-arch files being wheeled down a court corridor, ribbons and tab flags trailing, marble floor reflecting the load, a case measured in metres of paper, no visible person, no readable text [STYLE] Avoid: [NEG]
- `S136.png`
A schedule of claimants running down a legal document in a dense column, every name blurred to an even smear, page numbers deep in the hundreds implied by the thickness beneath, five hundred and fifty-five lives in a list, no person, no readable text [STYLE] Avoid: [NEG]
```
- **high_court — 3 — S137–S139**（ゴシック外観/ガラスの新館/無人法廷）
```
- `S137.png`
The Victorian gothic stone facade of London's law courts rising pale against a wet grey sky, arches and spires streaked dark with rain, pavement shining below, the building where the machine finally lost, no people, no readable text [STYLE] Avoid: [NEG]
- `S138.png`
A modern glass-and-steel court building at dawn, its atrium lights cold behind rain-flecked panels, a revolving door motionless, twenty-first-century justice with the heating off, no people, no readable text [STYLE] Avoid: [NEG]
- `S139.png`
A modern British courtroom empty before sitting: pale wood, dark dormant monitors at every desk, water carafes set, the managed hush of a room where evidence wins, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_judge_reads — 1 — S140**
```
- `S140.png`
A high judge's bench with an empty red leather chair, a carafe and a single thick bundle squared on the blotter, cold daylight from tall windows, the seat of a man who read every page, no person, no readable text [STYLE] Avoid: [NEG]
```
- **horizon_issues_judgment — 2 — S141–S142**
```
- `S141.png`
A bound High Court judgment as thick as a novel standing upright on a desk, its spine title a smear, edges dense with paper flags, December light low across it, three hundred pages of demolition, no person, no readable text [STYLE] Avoid: [NEG]
- `S142.png`
Barristers' wheeled document boxes lined up on wet pavement outside a court entrance in the rain, lids beaded with drizzle, a verdict day's luggage, no people, no readable text [STYLE] Avoid: [NEG]
```
- **settlement_pyrrhic — 2 — S143–S144**（勝利の請求書）
```
- `S143.png`
A long boardroom at dusk after a signing: chairs askew, a settlement bundle left squared at the table's head, pens abandoned, city light dying in the glass, a victory that cost the winners everything, no people, no readable text [STYLE] Avoid: [NEG]
- `S144.png`
Two towers of stacked invoices and fee notes beside a small single cheque-sized slip, all figures smeared, cold accountant's light, the arithmetic of who really won, no person, no readable text [STYLE] Avoid: [NEG]
```
- **ccrc_referrals — 1 — S145**
```
- `S145.png`
A row of old case files each newly flagged with a bright red referral tab, standing in a records box like teeth, one pulled a few centimetres proud of the rest, convictions coming back up for air, no person, no readable text [STYLE] Avoid: [NEG]
```
- **royal_courts_2021 — 2 — S146–S147**（4月23日の朝の舞台）
```
- `S146.png`
The wide stone steps and gothic doorway of the Royal Courts of Justice on a cold bright April morning, wet stone drying in patches, barriers set out for a crowd not yet arrived, no people, no readable text [STYLE] Avoid: [NEG]
- `S147.png`
A cluster of press microphones taped to a single stand on court steps, cables snaking away, channel flashes and logos all smeared, waiting for someone exonerated to speak, no people, no readable text [STYLE] Avoid: [NEG]
```
- **counter_relit_amber — 1 — S148**（counter 連鎖状態③・★本作唯一の ACT4 amber 復活ビート）
```
- `S148.png`
A village post-office counter warm again under a shop-lamp amber glow, the brass grille polished and the date stamp back on its pad, dust gone, one narrow warmth returning to a cold film, no people, no readable text [STYLE] Avoid: [NEG]
```
- **boarded_branch_state — 1 — S149**（SIGNATURE B 状態③）
```
- `S149.png`
A generic red post-office sign above a shopfront boarded with weathered plywood, the red faded toward rust at the edges, no readable lettering, weeds in the doorstep crack, what the years of the fight cost the high street, no people, no readable text [STYLE] Avoid: [NEG]
```
- **front_pages — 1 — S150**
```
- `S150.png`
A stack of fresh newspapers bound in twine on a dark pavement before dawn, the top front page dominated by one huge smeared headline and a photograph blurred beyond identity, ink still sharp-smelling, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP fenny_meeting — 3 — S151–S153**（only-ones の合流 — 入場/全景/手元）
```
- `S151.png`
People filing into a lit village hall at dusk seen from far behind, coats and flat caps, pausing at the door as strangers do, each of them told for years they were the only one, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S152.png`
A village-hall meeting seen from the very back of the room: two dozen anonymized backs on folding chairs facing a trestle table, one figure standing to speak, tea steam rising, an army discovering itself, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S153.png`
Two men's hands at a trestle table comparing two smeared branch printouts side by side, fingers tracing the same impossible pattern in both, tea mugs at their elbows, the moment the lie breaks, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP the_campaigner — 2 — S154–S155**（kitchen-table 状態④の人物・pillar box 連鎖②）
```
- `S154.png`
A methodical anonymized man at his kitchen-table laptop at night seen from behind, older now, the box files around him doubled since the shop, reading-glasses folded by the keyboard, the long game in progress, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S155.png`
An anonymized man posting a thick envelope into a generic red pillar box on a village corner, seen from behind in drizzle, the envelope halfway into the slot, the campaign sent by the very network that wronged him, no face, no emblem, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP litigation_army — 3 — S156–S158**
```
- `S156.png`
Claimants queueing outside a London court under umbrellas seen from far behind, a line of ordinary coats stretching along the wet railings, provincial and patient in the capital, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S157.png`
A legal team wheeling document trolleys toward court doors seen from behind, gowns over arms, boxes swaying, the paper artillery of the 555 going in, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S158.png`
A packed public gallery rising to its feet as one, seen from directly behind, coats and grey heads lifting together, a judgment landing below, restrained thunder, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP trial_witness — 2 — S159–S160**
```
- `S159.png`
An anonymized witness standing at a modern court lectern seen from behind, a calm upright silhouette against tall cold windows, giving the evidence of an ordinary working life, still and composed, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S160.png`
Rows of barristers seen from directly behind, white wigs in ordered ranks against black gowns, one head inclined to a neighbour, the machinery of the law finally pointed the right way, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP steps_2021 — 3 — S161–S163**（4月23日・抑制された歓喜）
```
- `S161.png`
A crowd on the Royal Courts steps seen from behind at the moment of release, arms lifting, a cheer made visible in shoulders rather than faces, April light hard and clean on the stone, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S162.png`
An anonymized woman on court steps holding a sheet of paper high over her head with both hands, seen from directly behind, coat lifting in the wind, eighteen years answered in one page, its text a smear, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S163.png`
Two people embracing outside a court seen from a long way off, small against the gothic doorway, one hat knocked slightly askew, held still, dignity in joy as in everything, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP press_witness — 2 — S164–S165**
```
- `S164.png`
A wall of press photographers seen from behind, cameras raised in a single motion toward court doors, elbows interlocked, long lenses like artillery, the country finally looking, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S165.png`
Reporters under umbrellas doing pieces to camera on a wet pavement, seen from behind the camera line, lit faces turned away from us into their own lights, satellite van cables underfoot, no identifiable faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP walking_away_free — 1 — S166**
```
- `S166.png`
An elderly couple walking away from a court hand in hand seen from far behind, his stick in his free hand, her head leaning to his shoulder, the pavement long and bright ahead of them, upright to the end of the frame, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 5 — THE DRAMA THAT MOVED A PARLIAMENT（30枚・S167–S196・climax cascade ＝ object 10 + ★HP 20）
- **one_night_in_january — 2 — S167–S168**（2024-01-01 の夜）
```
- `S167.png`
A terraced British street on a cold January night, rows of front-room windows all glowing the same television blue, one upstairs light amber, a nation watching the same story at the same time, no people, no readable text [STYLE] Avoid: [NEG]
- `S168.png`
A living-room side table lit by an off-screen television's flicker: a mug of tea, a remote control, reading glasses folded on a smeared listings magazine, the sofa cushion still dented, no person, no readable text [STYLE] Avoid: [NEG]
```
- **westminster — 2 — S169–S170**
```
- `S169.png`
The Houses of Parliament seen across the black river at night, gothic ranks of lit windows doubled in the water, rain just ending, the building about to do something it has never done, no people, no readable text [STYLE] Avoid: [NEG]
- `S170.png`
The Westminster clock tower against a flat grey dawn sky, gilt details dulled by drizzle, its face a pale disc with the time unreadable, London traffic lights smeared far below, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_act_2024 — 2 — S171–S172**（envelope 連鎖状態⑤=国家が書き返す）
```
- `S171.png`
A formal parchment document with a ribbon and wax-adjacent seal shape lying on a green leather desk, its engrossed text an elegant unreadable smear, cold chandelier light, a law that erases convictions by its own first sentence, no person, no readable text [STYLE] Avoid: [NEG]
- `S172.png`
Macro of a bound statute volume open at a fresh page, section numbering visible only as smeared marginalia, the paper bright white against dark binding, one short subsection carrying hundreds of lives, no person, no readable text [STYLE] Avoid: [NEG]
```
- **inquiry_room — 2 — S173–S174**（S173 = ★also_thumb・説明責任の空白）
```
- `S173.png`
An empty witness chair at a white inquiry desk under cool even lights, a microphone angled toward the vacant seat, a water glass full and untouched, screens dark behind, the chair where the answers were supposed to be, no person, no readable text [STYLE] Avoid: [NEG]
- `S174.png`
A wide modern inquiry hearing room, rows of empty desks with dead monitors, cable runs taped to carpet, one wall of frosted glass glowing grey, institutional truth-finding between sessions, no people, no readable text [STYLE] Avoid: [NEG]
```
- **the_erasure — 2 — S175–S176**（honour の取り消し）
```
- `S175.png`
A dark presentation case closing over a generic neck-ribbon honour medal on black velvet, the lid's descent caught halfway, no royal emblem and no readable engraving, an award on its way back, no person, no readable text [STYLE] Avoid: [NEG]
- `S176.png`
Macro of an official register page where one entry line has been struck through into an unreadable smear among other smeared lines, the strike ruler-straight, ink still wet-black, a name erased from an order, no person, no readable text [STYLE] Avoid: [NEG]
```
- **★HP nation_watching — 4 — S177–S180**（同じ夜の別の部屋 — 家族/パブ/独り/老夫婦）
```
- `S177.png`
A family of anonymized figures on a sofa seen from directly behind, silhouetted against a bright television's smeared glow in a dark room, one small out-of-focus child shape leaning on a shoulder, nobody reaching for the remote, no faces, no identifiable child, no readable text [HSTYLE] Avoid: [HNEG]
- `S178.png`
A crowded pub seen from the back of the room, drinkers' backs turned to the bar and every head angled up at a wall-mounted television with a smeared bright screen, pints untouched, the ordinary noise gone, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S179.png`
A woman alone in an armchair seen from behind, television light flickering over her still shoulders in a dark front room, a cooling cup on the arm, watching her own story happen to someone else, composed, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S180.png`
An elderly couple side by side on a settee seen from behind, his arm along the back cushion behind her, both silhouetted against the television's smeared glow, a reading lamp making one warm pool beside the cold light, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP the_morning_after — 2 — S181–S182**
```
- `S181.png`
Commuters packed in a morning train carriage seen from behind, a dozen phone screens all glowing with the same smeared story, heads bowed in unison, fury travelling at network speed, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S182.png`
Two colleagues at an office kitchenette seen from behind, kettle steaming unattended between them, one gesturing with a teaspoon mid-sentence, the conversation every workplace had that week, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP petition_million — 1 — S183**
```
- `S183.png`
Macro of anonymized thumbs signing a petition on a phone screen, the page a bright smear with one button shape glowing, a train window's grey blur beyond, one signature of more than a million, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP westminster_moves — 3 — S184–S186**
```
- `S184.png`
Members walking a parliamentary lobby seen from far behind, dark suits on chequered marble under high gothic ribs, folders under arms, unusual speed in the stride, a law being hurried for once, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S185.png`
A wide chamber view from behind the back benches: an anonymized figure standing at a despatch-box distance below, ranks of green leather and dark shoulders between, an announcement without precedent mid-sentence, no faces, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S186.png`
Civil servants carrying red despatch boxes across a courtyard seen from behind, coats snapping in wind, wet cobbles, the machinery of state jogging to catch up with a television drama, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP inquiry_reckoning — 5 — S187–S191**（行列/記者/尋問者/満員の傍聴/静かに見守る当事者）
```
- `S187.png`
A queue under umbrellas outside a glass-fronted hearing venue at early morning, seen from far behind along the wet pavement, lanyards and thermos flasks, people who waited twenty years waiting two more hours, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S188.png`
A press annex seen from the back: journalists' backs at trestle desks, laptops open with smeared live-feeds, cabled monitors relaying an empty witness desk, the country taking notes, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S189.png`
A barrister at a lectern seen from behind in silhouette against the hearing room's cool light, one hand resting on a thick bundle, the pause before a question that took a decade to ask, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S190.png`
A packed public gallery seen from its own back row, every seat filled with anonymized shoulders and grey heads, all facing the small bright empty witness chair far below, silence with weight, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S191.png`
A single row of exonerated former postmasters seated together in a hearing-room gallery, seen from behind, hands in laps, utterly still while the room murmurs around them, composure as testimony, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP the_state_writes_back — 3 — S192–S194**（envelope 連鎖の反転）
```
- `S192.png`
A postman with a shoulder bag delivering along a village street at morning, seen from behind in drizzle, one white official envelope bright in his hand against the grey, the network carrying the apology it owes, no face, no emblem, no readable text [HSTYLE] Avoid: [HNEG]
- `S193.png`
Hands opening a thick white official envelope at a kitchen table, the letter half unfolded and its text a smear, a teapot and two cups waiting, macro in soft morning light, twenty years arriving by post, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S194.png`
Elderly hands holding an official payment letter flat on a table, one thumb pressed on the smeared figure line as if to hold it down, reading glasses beside, money that buys back nothing and matters anyway, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP redress_office — 1 — S195**
```
- `S195.png`
A couple seated before a solicitor's desk seen from behind, a claim bundle open between the three, the solicitor beyond only a dark shape and folded hands, filing for what was taken, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP the_knighthood — 1 — S196**
```
- `S196.png`
A man in a morning suit walking alone across a palace forecourt's raked gravel, seen from far behind, railings and sentry boxes softened by mist, a campaigner arriving where campaigns end, no face, no emblem, no readable text [HSTYLE] Avoid: [HNEG]
```

### ENDING（14枚・S197–S210・the honest grey present ＝ object 11 + ★HP 3）
- **ledger_dark_state — 1 — S197**（SIGNATURE A 状態⑤・終端）
```
- `S197.png`
A branch terminal switched off on a counter, its dead glass reflecting only a grey window and rain, no phosphor anywhere, the machine silent but still present, dust along the keyboard seam, no person, no readable text [STYLE] Avoid: [NEG]
```
- **pillar_box_dawn_state — 1 — S198**（pillar box 連鎖③・現在形）
```
- `S198.png`
The generic red pillar box on its village corner at grey first light, present day, paint recently renewed but the kerb around it patched and old, drizzle starting, the state still in walking distance, still red, no people, no readable text [STYLE] Avoid: [NEG]
```
- **two_branches_now — 2 — S199–S200**
```
- `S199.png`
A permanently shuttered village branch in dawn light, the red sign sun-faded to dusty rose, a dead notice curled in the door glass as a smear, one of the ones that never came back, no people, no readable text [STYLE] Avoid: [NEG]
- `S200.png`
A small corner shop open at dawn in drizzle, door propped, warm light spilling onto wet pavement, crates of milk stacked outside, life continuing next to everything unfinished, no people, no readable text [STYLE] Avoid: [NEG]
```
- **volumes_unwritten — 2 — S201–S202**
```
- `S201.png`
Four thick unbound draft volumes stacked on an office desk, pages clipped with bulldog grips, every cover sheet a smear, a lamp left on over them at night, the chapters that will name the culpable still in proof, no person, no readable text [STYLE] Avoid: [NEG]
- `S202.png`
The inquiry hearing room in half-darkness after hours, chairs pushed in, one strip of security lighting along the floor, the witness chair a pale shape in the gloom, adjourned but not finished, no people, no readable text [STYLE] Avoid: [NEG]
```
- **police_files — 1 — S203**
```
- `S203.png`
A police evidence archive aisle receding into darkness, ranks of boxed files on industrial shelving, one bay tagged with smeared labels newer than the rest, eight million documents waiting for 2027, no people, no readable text [STYLE] Avoid: [NEG]
```
- **laptop_closed — 1 — S204**（kitchen-table 連鎖状態⑤・終端）
```
- `S204.png`
A laptop closed on a tidy kitchen table at dawn, box files squared beside it, a single mug washed and upturned on the drainer beyond, grey light strengthening, the campaign paused but not surrendered, no person, no readable text [STYLE] Avoid: [NEG]
```
- **grey_morning_britain — 2 — S205–S206**
```
- `S205.png`
A village high street at first light, wide and empty, wet tarmac silvering, a milk crate on one step and a red sign dark down the parade, the ordinary country this happened to, no people, no readable text [STYLE] Avoid: [NEG]
- `S206.png`
A grey British coastline at first light, long flat waves under a lid of cloud, one break of paler sky far out over the water, patience the size of weather, no people, no readable text [STYLE] Avoid: [NEG]
```
- **title_out_texture — 1 — S207**
```
- `S207.png`
An abstract near-black closing field where a last breath of phosphor green fades low in the frame beside a dying ember of signage red, both dissolving into grain, the two lights of the story going out together, no objects, no people, no readable text [STYLE] Avoid: [NEG]
```
- **★HP morning_shutter — 2 — S208–S209**（counter 連鎖状態④・現在の営み）
```
- `S208.png`
An anonymized postmistress unlocking her shop shutter at dawn seen from behind, the metal half-raised showing the warm interior, keys in hand, cardigan against the cold, the trade continuing in spite of everything, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S209.png`
Elderly customers waiting outside a village shop in morning light seen from far behind, a small patient cluster with shopping bags, exactly as they waited in 1999, the community still arranged around the red door, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **★HP survivor_dignity_close — 1 — S210**
```
- `S210.png`
An older man standing at a seafront rail seen from behind, backlit by flat grey light off the water, coat buttoned, hands on the rail, upright and unbroken, looking a long way out, no face, no readable text [HSTYLE] Avoid: [HNEG]
```

## 5.7 幕別 motif 枚数の検算（★Codex は書き終えたら足して確認）

```
ACT0  : 2+2+1+2+1+2+1+1+1+1 = 14
ACT1  : object 3+1+2+3+1+2+1+1+1+2+1+1+1 = 20 ／ ★HP 2+2+3+2+2+2+1+2 = 16 → 36
ACT2  : object 2+1+2+1+1+2+2+2+1+2+1+2+1+1+1 = 22 ／ ★HP 2+2+2+2+2+2+2+2 = 16 → 38
ACT3  : object 2+3+2+2+3+1+2+2+1+1+2+1+1+2+1 = 26 ／ ★HP 2+2+1+2+1+2+1+1+1+1 = 14 → 40
ACT4  : object 2+2+2+2+3+1+2+2+1+2+1+1+1 = 22 ／ ★HP 3+2+3+2+3+2+1 = 16 → 38
ACT5  : object 2+2+2+2+2 = 10 ／ ★HP 4+2+1+3+5+3+1+1 = 20 → 30
ENDING: object 1+1+2+2+1+1+2+1 = 11 ／ ★HP 2+1 = 3 → 14
合計   : 14+36+38+40+38+30+14 = 210 ✓
★human-present(★HP) body: 16+16+14+16+20+3 = 85 / 210 = 40.5%（残り125は object/symbolic）
★HP の S番号集合: S035–S050 / S073–S088 / S115–S128 / S151–S166 / S177–S196 / S208–S210（連続レンジ・穴なし）
★also_thumb 4枚 = S001 / S057 / S106 / S173（§4.3a と一字一致）✓
```
> **S001..S210 の連番が穴なく210行**そろっていることを `--only S001` の `shots=255`（210 body + 42 i2v種 + 3 thumb_face）で確認する。

## 5.8 メタJSON

`generate_sdxl_4k.py` は per-image メタJSONを書かない。**A は QC 時に `qc_postoffice_stills.py` で各画像の `sha256`/`phash`/`mean_luma`/`long_edge` を測り `still_qc.v001.json` に記録する**（§6.2）。

## 5.9 パーサ契約（`read_prompts()` はこの2行形式しか読まない）

```
- `S001.png`
<positive prompt> Avoid: <negative>
```
- **1行目:** `` - `S001.png` ``（バッククォート囲み・行末は `.png` の直後）
- **2行目:** 正プロンプト → `Avoid:` → 負プロンプト
- `ai_prompts.v001.md` は **body 210行（S001..S210）＋ i2v 種 42行（M01_src..M42_src、§8.1a）＋ thumb_face 3行（T01_face..T03_face、§5.12）＝ 255 エントリ**を書く。すべて1枚生成。

## 5.10 生成コマンド（★variants 指定なし。`--variants 3` は使わない）

```bash
# まず1枚だけ回して読める行数を確認（★shots=255 でなければ形式が壊れている）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 56 --only S001
#   → ログ "episode=... shots=255 ... -> N images" の shots が 255 であること（210 body + 42 i2v種 + 3 thumb_face）

# 全255枚（body 210 + i2v種 42 + thumb_face 3・冪等・長辺>=3840 の既存はスキップ）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py PD-2026-056-postoffice
```
> QC で落ちたシーンの再生成は `--only S###`（同じプロンプトで別シードを1枚）。**基準を下げない・水増ししない。**

## 5.11 ★人物画像（匿名・ドラマ化スタンドイン）— HUMAN-FIGURE prompts（★18本・i2v 種の内数）＋ ★HP body still の style

> **owner directive（EP48/49「空/寂しい」却下の恒久対策・EP52/EP55 継続）: 匿名・非識別の人物を増やし、動かす。** 実在人物（Bates/Sercombe/Misra夫妻/Hamilton/Castleton/Thomas/Griffiths/Vennells/Jenkins/Roll/Warmington/Henderson/Clarke/Arbuthnot/Wallis/Thomson/Fraser/Wyn Williams/Sunak/Patterson/国王/ITV俳優）の **likeness を作らない**。顔は非識別（背向き/影の横顔/逆光 silhouette/目から下クロップ/浅い被写界深度・**adults only**）。**自死・悲嘆・拘束の表象を絶対に作らない（R-SUICIDE/R-DIGNITY 継続）。被害者スタンドインは尊厳第一（upright・still・composed）。識別可能な子供の顔なし（家族ビートは out-of-focus の輪郭のみ）。**
> **★この `[HSTYLE]`/`[HNEG]` は (a) 18本の i2v 人物種、(b) §5.6 の ★HP body still 85枚、の両方に使う。**

### ★lane 定義（人物は動かす＝紙芝居にしない → H は motion レーンへ・locked counts 不変）

**H01–H18 は「新規の静止カット」ではなく、既存 42本の i2v 種のうち 18本の中身（＝人物ビート）として作る。additive にしない。**
- **role = `i2v_source`**（body には回さない）。**42本の i2v 種のうち ★18本を人物ビート**に充て、残り **24本を抽象/象徴種**（§8.1a）。per-act の内数: **ACT1×3・ACT2×4・ACT3×3・ACT4×4・ACT5×4 ＝18**（§4.5 の M04/M06/M08・M11/M13/M14/M16・M19/M22/M24・M27/M28/M30/M31・M33/M34/M36/M37）。ACT0/ENDING は象徴のまま。
- **asset_id は既存の i2v 種 ID 空間（`^POH-MS\d{2}$`）の 18本を占有**（H01–H18 は本書内のラベル）。種画像ファイルは `M<NN>_src.png`。`public_path==null`。
- 各人物種は **Wan → RIFE（§8）で motion 化**され、**42本の motion のうち 18本**になり、**84 motion カットのうち最大 36カット**に出る＝**人物が動く**。
- **QC フラグ:** `has_human_body:true`（許可）・`has_identifiable_real_person:false`（必須）・`has_readable_text:false`（必須）・`has_suicide_or_grief_imagery:false`（必須）。
- **★locked counts は1つも変わらない:** still_body **210**（＝object 125 ＋ ★HP 85）/ still_i2v_source **42**（＝抽象 24 ＋ 人物 18）/ motion **42** / factory **235** / overlay **30** / thumb_face **3**；cuts **244/235/84 = 563**；still-share **0.4334**；first-use **0.8650**；avg-uses **1.156**。

**共通スタイル `[HSTYLE]`（各 H プロンプト・★HP body 行の末尾に全文連結・匿名/非識別/photoreal/grey-British）:**
```
, cinematic photoreal still, documentary reenactment stand-in, a generic anonymized person who resembles no real individual, face kept non-identifiable — turned away, in profile lost to shadow, back-lit to a silhouette, cropped below the eyes, or thrown soft in shallow focus, grey British overcast light as the base register with warm shop-lamp amber only in the world-before and restoration beats and phosphor green only as screen glow, period-correct United Kingdom 1999 to 2026, wronged sub-postmaster figures always upright and composed and never in distress poses, low-key soft-shadow lighting, telephoto compression, shallow depth of field, restrained dignified framing, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, no readable documents, no real-institution branding, adults only
```
**共通ネガティブ `[HNEG]`（各 `Avoid:` の後に全文連結・匿名人体は許可、実在 likeness/自死悲嘆/拘束/可読テキスト/ロゴは禁止）:**
```
recognizable real person, likeness of a specific person, Alan Bates, Suzanne Sercombe, Seema Misra, Jo Hamilton, Lee Castleton, Noel Thomas, Martin Griffiths, Paula Vennells, Gareth Jenkins, Richard Roll, Nick Wallis, James Arbuthnot, Mr Justice Fraser, Sir Wyn Williams, Rishi Sunak, the King, Toby Jones, Monica Dolan, any real judge or executive, celebrity, mugshot, deepfake, text, words, letters, numbers, captions, watermark, logo, readable document, legible letter, legible ledger, legible screen, post office logo, royal mail logo, fujitsu logo, itv logo, royal crest, license plate, bus, double-decker bus, person standing in a road, rope, pills, farewell note, weeping face, crying face, sobbing, collapsed figure, cowering figure, crouching victim, despair pose, handcuffs, restrained person, prison dock cage with a person, wounds, blood, gore, injury, corpse, identifiable child face, american street, yellow school bus, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, sodium prison gold, porch amber, teal-green hospital, crimson kitchen, forest-green, civil-violet, somber-plum, steel-cyan, evidence-blue bandana, interrogation green-gray, milky haze, scanline
```

### 人物ビート（★18本・全て匿名・非識別・実在 likeness なし・adults only・i2v 種として motion 化）
```
- `H01.png`  (= M04_src.png · ACT1 · the trusted morning)
An anonymized sub-postmistress seen only from behind at her warm counter, mid-motion passing a pension book under the brass grille to a soft customer shape beyond, shop-lamp amber light, poised in the easy rhythm of a trusted trade, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H02.png`  (= M06_src.png · ACT1 · the night search)
A husband and wife at a kitchen table at night seen from behind, hands paused over sorted piles of smeared receipts, one bare bulb swaying almost imperceptibly above, the recount poised to start again, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H03.png`  (= M08_src.png · ACT1 · the only-one call)
An anonymized woman on a telephone in a dark shop seen from behind against green screen glow, cord swaying gently, shoulders squared, poised between the question and the answer that never changed, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `H04.png`  (= M11_src.png · ACT2 · the machine arrives)
Two anonymized suited investigators seen from behind mid-stride toward a village shop's door at dawn, briefcase swinging slightly, cold light along their shoulders, procedure in motion, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H05.png`  (= M13_src.png · ACT2 · carried with dignity)
A pregnant anonymized woman walking upright down a long corridor of cold institutional light, seen from behind in silhouette, coat closed, pace even and unhurried, composed the whole length of the frame, no face, no restraint, no readable text [HSTYLE] Avoid: [HNEG]
- `H06.png`  (= M14_src.png · ACT2 · the gallery leans)
A public gallery of anonymized backs caught leaning forward as one at a verdict's approach, coats shifting slightly, wood panelling beyond, restrained collective breath, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H07.png`  (= M16_src.png · ACT2 · alone against it)
An anonymized man with an armful of folders seen from behind, mid-step through tall court doors alone, his reflection sliding in the polished stone floor, one man carrying his own defence, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `H08.png`  (= M19_src.png · ACT3 · custodian of the machine)
An anonymized engineer seen from behind walking a dark server aisle, rack LEDs blinking green along both sides, lanyard swinging, poised mid-patrol through the country's most trusted liar, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `H09.png`  (= M22_src.png · ACT3 · the outsiders read everything)
Two anonymized forensic accountants seen from behind at a file-drowned table, one page passing between their hands in mid-air, lamplight over the exchange, the honest audit in motion, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H10.png`  (= M24_src.png · ACT3 · the view from the top)
An anonymized executive seen only from behind at a night boardroom window, city light shifting slowly across the glass, printed pages held loosely at the thigh, stillness with everything underneath it, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `H11.png`  (= M27_src.png · ACT4 · the only-ones arrive)
People filing into a lit village hall at dusk seen from far behind, coats and caps bobbing through the doorway's warm rectangle, gravel underfoot, strangers about to become an army, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H12.png`  (= M28_src.png · ACT4 · the long game)
A methodical anonymized man at his kitchen-table laptop at night seen from behind, hands poised over the keys, box files walling the lamplight, the campaign's ten-thousandth evening in progress, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `H13.png`  (= M30_src.png · ACT4 · the 555 go in)
Claimants queueing outside a London court under umbrellas seen from far behind, the line shuffling one place forward, drizzle drifting through streetlight, patience advancing, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H14.png`  (= M31_src.png · ACT4 · the steps, April 2021)
A crowd on court steps seen from behind at the instant of release, arms beginning to lift, one sheet of smeared paper rising above the shoulders, April light hard on the stone, joy with its back turned, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H15.png`  (= M33_src.png · ACT5 · the night the country watched)
A family of anonymized figures on a sofa seen from directly behind, silhouetted against a television's bright smeared glow, the light flickering over their stillness, nobody moving to change the channel, no faces, no identifiable child, no readable text [HSTYLE] Avoid: [HNEG]
- `H16.png`  (= M34_src.png · ACT5 · facing the empty chair)
A packed hearing-room gallery seen from its back row, anonymized shoulders and grey heads utterly still, the small bright empty witness chair far below them, the room breathing as one, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `H17.png`  (= M36_src.png · ACT5 · the network delivers the answer)
A postman with a shoulder bag seen from behind walking a village street at morning, one white official envelope bright in his hand, drizzle silvering the air ahead of him, the state finally writing back, no face, no emblem, no readable text [HSTYLE] Avoid: [HNEG]
- `H18.png`  (= M37_src.png · ACT5 · twenty years, unfolded)
Anonymized hands at a kitchen table opening a thick white official envelope, the letter half-unfolded and poised, its text a smear, morning light warming the wood grain, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
> **★H↔M 対応（§4.5 と一致・18本）:** H01=M04 · H02=M06 · H03=M08 · H04=M11 · H05=M13 · H06=M14 · H07=M16 · H08=M19 · H09=M22 · H10=M24 · H11=M27 · H12=M28 · H13=M30 · H14=M31 · H15=M33 · H16=M34 · H17=M36 · H18=M37。`ai_prompts.v001.md` では**新規行を足さず**、該当する 18本の `M<NN>_src.png` 行を上記の人物内容＋`[HSTYLE]`/`[HNEG]` で書く（`shots=255` 維持）。§8.5 で目視確認（adults only・子供顔なし・自死/悲嘆/拘束表象なし・実在 likeness なし・スタンドインの尊厳）。

## 5.12 ★サムネ用 emotive-face 静止画（3枚・CTR §4A・thumb_face）

> **owner directive（CTR_PLAYBOOK §4A・emotive face が lane の #1 CTR driver）:** サムネは **単一の AI 生成・非実在・illustrative/dramatized な顔**を peak emotion で。**実在人物（Bates/Misra/Hamilton/Vennells/俳優）の likeness を作らない**＝clearly illustrative（semi-painterly, cinematic-render）にして実写に読ませない＝likeness firewall。**悲嘆の泣き顔・自死表象・子供の顔を作らない**（感情は「不屈の凝視」「不信の驚き」「静かな解放」の3系統＝grief でなく defiance/shock/release）。これらは **本編カットに出ない thumbnail 専用**（role=thumb_face・public_path null・distinct/cuts に数えない・§3.1）。B が `PostofficeThumbnails.tsx` で face＋2–4語 hook text を合成。

**共通スタイル `[TSTYLE]`:**
```
, thumbnail key art, a single non-real dramatized generic human character rendered in a clearly illustrative semi-painterly cinematic style so it never reads as a real photograph of a real person, face occupying 50 to 65 percent of frame height with eyes on the upper third, bright key light on the face and a rim light separating it from a dark desaturated blurred British background, skin warm, background cool grey with one note of signage red or phosphor green, high contrast and vivid, one clean quadrant of negative space for text, 1280x720, ultra-detailed
```
**共通ネガティブ `[TNEG]`:**
```
photoreal photograph of a real person, likeness of Alan Bates or Seema Misra or Jo Hamilton or Paula Vennells or any real postmaster or judge or executive, Toby Jones, Monica Dolan, recognizable real celebrity, deepfake, a child, wounds, blood, gore, weeping, sobbing, despair pose, handcuffs, restraint, violence, weapon, text, words, letters, numbers, watermark, logo, post office logo, royal crest, two faces, tiny face, neutral expression, dark muddy low-contrast mush, cartoon flatness, extra limbs, deformed, warped
```
```
- `T01_face.png`
A non-real dramatized generic middle-aged British shopkeeper woman's face in an illustrative cinematic style at peak emotion — a steady, wounded, unbroken stare directly at the viewer, the look of an honest woman branded a thief by a machine, pushed to the right third over a dark blurred village post-office background at night with one cold green screen glow, warm rim light, clean negative space on the left [TSTYLE] Avoid: [TNEG]
- `T02_face.png`
A non-real dramatized generic middle-aged woman's face in an illustrative cinematic style lit from below by phosphor green screen light, eyes widening in stunned disbelief at something just off-frame, one hand's fingertips at her jaw, the instant the till invents a debt, pushed to the left third over a deep black background with a faint red sign bokeh, clean negative space on the right [TSTYLE] Avoid: [TNEG]
- `T03_face.png`
A non-real dramatized generic older working man's face in an illustrative cinematic style with eyes lifting and jaw unclenching in quiet hard-won release, twenty years of fight resolving into daylight, pushed to the right third over a dark blurred gothic court-steps background with a band of cold morning light, warm key, clean negative space on the left [TSTYLE] Avoid: [TNEG]
```
> ★これら3枚は `role:"thumb_face"`・`public_path:null`・`has_human_body:true`・`has_identifiable_real_person:false`。§6 の目視で「実在 likeness でない・illustrative・悲嘆/自死表象なし・子供なし」を確認。B のサムネ案は T01–T03 を前景に、§4.3a の also_thumb body（背景）＋ 2–4語 hook（CTR §4A・stakes-gap 例 "236 JAILED" / "THE COMPUTER LIED" / "ONE BUG, 236 PRISONERS"）で組む。

## 5.13 ★EMOTIVE FACES — VISIBLE faces（F-series 12枚・per owner 2026-07-25 standard）

匿名図だけでは「顔がほぼ無い」状態になる。オーナー方針＝**見える感情的な顔**を織り込む（顔は維持率・CTRを上げる）。F-series（見える顔）を既存の匿名図に**加えて**生成する（★distinct/cuts に数えない補助レーンとして B が挿し込み判断・迷ったら生成だけして staging し、cuts への採用は B に委ねる）。

**2レーン、いずれも「実在の誰にも似せない・非実在の人物」:**
- **(a) generic-photoreal** — 特定の実在人物に紐づかない役（客・陪審員・記者・エンジニア・会計士・郵便配達員）。
- **(b) dramatized-illustrative** — 中心的実在人物に隣接するビート（postmistress everyman・campaigner archetype・executive archetype）は**明らかにイラスト調・半絵画的**で写真に見えないスタイルに。実在人物として名指し/キャプションしない。

**HARD BANS（不変）:** Bates・Misra・Hamilton・Castleton・Thomas・Griffiths・Vennells・Jenkins・俳優の**肖像を作らない**；**識別可能な子供の顔は不可**；悲嘆の泣き顔・自死表象・拘束・傷なし；可読テキストなし。QCフラグ: `has_human_body:true`・`has_identifiable_real_person:false`・`has_identifiable_face:false`（=実在として識別可能でない）・`has_suicide_or_grief_imagery:false`・`has_readable_text:false`。

**★ FACE 標準（data-driven・owner choice A）:** 全F画像は**LIGHT + EXPRESSION で目立つ顔**（サイズで盛らない）— **medium-close-up ~30–45% of frame height, eyes on the upper third, front or slight three-quarter, one strong unmistakable emotion, dramatic key + rim light against a DARK moody restrained background**。60%超の顔面充填・背向き・影に沈む・hands-only は不可。

`[FSTYLE]` = `a clearly-visible emotive human face in a strong medium-close-up filling ~30-45 percent of the frame, eyes on the upper third, front or slight three-quarter view looking near camera, one strong unmistakable {EXPRESSION}, dramatic key light plus rim light on the face against a dark moody background, restrained saturation, a generic anonymized non-real person resembling no real individual, cinematic documentary grade, grey British light with signage red or phosphor green only as environmental notes, ultra-detailed skin and eyes, high contrast, {photoreal | clearly illustrative semi-painterly non-photographic}, 16:9, adults only, no text, no watermark, no logo`
`[FNEG]` = `likeness of a real or named person, Alan Bates, Seema Misra, Jo Hamilton, Lee Castleton, Noel Thomas, Martin Griffiths, Paula Vennells, Gareth Jenkins, Toby Jones, Monica Dolan, recognizable real person, mugshot, deepfake, child, toddler, weeping, sobbing, despair, wounds, blood, injury, restraint, handcuffs, weapon, readable text, document, caption, post office logo, royal crest`

**★F001–F012 の literal 12行（そのまま `ai_prompts.v001.md` 末尾へ追記する。lane (a)=photoreal / (b)=clearly illustrative は各プロンプト本文に内蔵済み）:**
```
- `F001.png`
A village postmistress everyman's face rendered clearly illustrative and semi-painterly, a middle-aged woman in medium-close-up behind her counter, eyes on the upper third warm and open, the trusted face of a high street before the machine, shop-lamp amber key and soft grey rim, dark shop bokeh, not a likeness of any real postmistress [FSTYLE] Avoid: [FNEG]
- `F002.png`
Photoreal medium-close-up of a generic elderly customer's trusting face at a post-office counter, cap pushed back, small smile of long acquaintance, warm counter light against dark shelves, the community the trust was borrowed from, generic anonymized adult [FSTYLE] Avoid: [FNEG]
- `F003.png`
A clearly illustrative semi-painterly face of a generic wrongly accused shopkeeper, a middle-aged woman with quiet defiance set in her jaw and hurt held behind steady eyes, upright posture, cold strip-light key with a warm rim, dark interview-room bokeh, dignity under accusation, not a likeness of any real person [FSTYLE] Avoid: [FNEG]
- `F004.png`
Photoreal medium-close-up of a generic juror's uncertain face in a 2000s courtroom, three-quarter view, doubt creasing the brow as testimony lands, cold window key light, dark wood bokeh, generic anonymized adult [FSTYLE] Avoid: [FNEG]
- `F005.png`
A clearly illustrative semi-painterly face of a generic young British-Asian woman, composed and unbowed under cold institutional light, eyes steady on the upper third, carrying herself with deliberate dignity, dark corridor bokeh, not a likeness of any real person [FSTYLE] Avoid: [FNEG]
- `F006.png`
Photoreal medium-close-up of a generic engineer's uneasy face lit by green rack LEDs in a dark server aisle, eyes flicking off-camera, knowledge he cannot say out loud written in the set of his mouth, generic anonymized adult [FSTYLE] Avoid: [FNEG]
- `F007.png`
Photoreal medium-close-up of a generic forensic accountant's grim discovering face over an open file, desk-lamp key from below the eyeline, the moment a professional realises what the numbers mean, dark office bokeh, generic anonymized adult [FSTYLE] Avoid: [FNEG]
- `F008.png`
A clearly illustrative semi-painterly face of a generic institutional-executive archetype, composed and unreachable, chin slightly lifted, cold boardroom key light and glass reflections ghosting the cheek, denial worn as calm, no glorification, not a likeness of any real executive or any real person [FSTYLE] Avoid: [FNEG]
- `F009.png`
A clearly illustrative semi-painterly face of a generic weathered campaigner, an older man at a lamplit kitchen table, patient unyielding resolve in the eyes and twenty years of paper in the lines of his face, warm lamp key against cold blue night bokeh, not a likeness of any real campaigner [FSTYLE] Avoid: [FNEG]
- `F010.png`
Photoreal faces of a generic older woman and man in a court gallery at the instant of a verdict, stunned joy breaking as widened eyes and parted lips, hands rising into frame's edge, cold courtroom key with warm rim, generic anonymized adults [FSTYLE] Avoid: [FNEG]
- `F011.png`
Photoreal medium-close-up of a generic viewer's face lit only by television flicker in a dark living room, dawning outrage hardening the brow, screen light trembling on the skin, dark sofa bokeh, generic anonymized adult [FSTYLE] Avoid: [FNEG]
- `F012.png`
Photoreal medium-close-up of a generic old postmaster's face at a grey seafront, wind moving his coat collar, endurance and salt light in the eyes on the upper third, flat silver sea bokeh behind, generic anonymized adult [FSTYLE] Avoid: [FNEG]
```

Generate all 12; QC each visually (visible emotive face · non-real · no likeness/child/grief-weeping/text) before manifest.

> **★shots カウントとの整合:** F001–F012 の12行は、**base 255 行（S001..S210 + M01_src..M42_src + T01_face..T03_face）の `shots=255` 検証が通った後に** `ai_prompts.v001.md` の末尾へ追記して生成する。**追記後の `shots=267`（255+12）が正**。§5.9/§5.10 の「255」は F-series 追記前の base セットの検算値であり、形式破損の判定はその時点で行う。F-series は distinct/cuts に数えない（§5.13 冒頭のとおり）。

---

# 6. A-2/A-3: 静止画のQC・目視（★depth map なし）

## 6.1 機械QC（body 210 + i2v種 42 + thumb_face 3 = 全255枚・`qc_postoffice_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `18.0<=mean_luma<=225.0`（grey British light 基調＝中間傾向。ACT0/夜ビートの黒潰れ・ACT1 warm/ENDING dawn の白飛びに注意） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject。**watch-list（状態連鎖が正・同状態化したら reject）: ledger 5状態(S001–S002/S024/S025–S026/S106/S197)・branch sign 3状態(S015/S057/S149)・pillar box 3状態(S008/S155/S198)・envelope 連鎖(S005/S029/S072/S103/S107/S171/S176/S193–S194)・counter 4状態(S016/S066/S148/S208)・kitchen-table 5状態(S040/S046/S088/S133/S154/S204)・courtroom/gallery 群(S058/S079/S139/S158/S190–S191)・queue 線(S036/S126/S156/S187/S209)・hands-macro 群(S041/S043/S044/S087/S116/S125/S153/S183/S193–S194)・TV-watching 4連(S177–S180・部屋/人数/光で分離)・umbrella 群(S049/S084/S156/S165/S187)・shop 外観群(S015/S020/S061/S109/S149/S199–S200)・法廷外観(S067/S137–S138/S146)。★R3 注記: prompt-diversity の残存 ~0.35 ペア S016↔S148（counter 連鎖の状態①warm→状態③re-lit amber＝設計どおりの復活 bookend）と S036↔S209（queue 線の Act I 朝→ENDING「exactly as they waited in 1999」＝意図した首尾 bookend、prompt に状態語内蔵済み）は**設計上のペア＝正**。生成後 phash が >=0.90 に接近した場合のみ構図/距離で作り直す** | 片方 reject＋プロンプト見直し（削るのではなく §5.5a のルールで作り直す） |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・日付(1999/2010/2021/2024)・金額(£74,609.84/£321,000)・件数(555/39/236)・実在ロゴ（Post Office/Royal Mail/Fujitsu/ITV/crown crest）・新聞/判決/法/Gazette の可読紙面 | `has_readable_text=true`→reject |
| Q6 | **実在人物**の顔の混入 | **目視。** 実在人物として識別可能な顔（Bates/Misra/Hamilton/Castleton/Thomas/Griffiths/Vennells/Jenkins/Fraser/Sunak/国王/ITV俳優 に**似た**顔）。**匿名・非識別の顔（H/F/thumb_face）は OK。** | `has_identifiable_real_person=true`→reject |
| Q7 | 自死表象/悲嘆/拘束/子供 | **目視。** バス・道路の人物・ロープ・薬・遺書・橋/線路の人物・泣き顔・泣き崩れ・うずくまり・手錠・拘束・dock 内の人物・**識別可能な子供の顔**。**★匿名の人体は OK（`has_human_body=true` 単独では reject しない）。** | `has_suicide_or_grief_imagery=true`（または子供顔）→reject |

**Q5/Q6/Q7 は機械で判定しない。全255枚を実際に目視:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-056-postoffice --media image
#   → runs/qc/postoffice_footage_contact_NN.png（20枚/シート・約13シート）。全シートを開いて1枚ずつ見る
```

> **EP38/EP39-55 の教訓: ファイル名・プロンプトを信じるな。生成物を実際に見ろ。** 特に **S108–S109（Griffiths 環境）にバス・車両・道路の人物・花束/メモリアル的要素が出ていないこと、S075/M13（妊婦シルエット）が dignified upright で拘束/distress に転じていないこと、S070（tag）が人体に装着されていないこと、S177（家族TV）と S077（父子）の子供が out-of-focus 輪郭のみであること、S015/S057/S149/S198/S008/S155 の看板/ポストに実在の Post Office/Royal Mail ロゴ・紋章・可読文字が出ていないこと、S171/S172/S176（法・Gazette）と S141（判決）の紙面が可読になっていないこと、S185（despatch box）が実在政治家に似ていないこと、T01–T03/F001–F012 が実在人物・ITV俳優に似ていないこと、を必ず目で確認する。**

## 6.2 出力
```
episodes/PD-2026-056-postoffice/05_visuals/still_qc.v001.json     # 255枚全部の行（reject も残す）
```

## 6.3 accepted が (body210 / i2v42 / thumb3) に届かなかったとき
```bash
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py 56 --only S###   # 落ちたシーンだけ同一プロンプトで別シード1枚
./.venv/Scripts/python.exe scripts/qc_postoffice_stills.py
```
accepted body >= 210 かつ i2v_source >= 42 かつ thumb_face >= 3 になるまで繰り返す。**基準を下げない・水増ししない。**

## 6.4 ★depth map は生成しない（本作は depth treatment 不使用）
**DESIGN §1 の hard rule により footage/still treatment は `bleed`/`parallax`/`duotone`/`focus` のみ・`depth` を使わない**（depth displacement は被写体を melt/warp させる＝EP48/49 の warp 欠陥）。したがって **`gen_depth_maps.py` を回さない・`<stem>_depth.png` を作らない・マニフェストに `depth_path` を持たせない**（§4.1a/§4.2-19）。

---

# 7. A-4: factory 実写クリップ 235本の選定と全点目視QC

## 7.1 在庫の実態
```
H:\pd-media\assets\factory\   フラット構成（backgrounds 11,000本超・light_assets・particle_assets・vfx_overlays・texture_assets・loops）
ファイル名規約: AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext>
棚レジストリ: C:\Users\aab15\Documents\prime-documentary\assets\asset_manifest.v001.json（★必ず encoding="utf-8" で開く）
★既知の障害: factory 棚のラベルは全面的に信用できない（evidence_bag=カートゥーン事故の実績）。§7.5 の全点目視が生命線。
ストックライブラリ: H:\pd-media\assets\stock（STOCK_MANIFEST.json・pexels/pixabay・商用可）— §7.4a
```

## 7.2 選定条件
- **`kind=="video"` のみ。** 静止画 factory は使わない
- **235本ちょうど**（§3.3[8] より still-share≤0.45 を守る設計値）
- **各1回しか使わない**（`MAX_USES_FACTORY=1`）
- 幕別割り当て（§4.4）: HOOK+OPENING=12 / ACT1=42 / ACT2=42 / ACT3=44 / ACT4=42 / ACT5=36 / ENDING=17 ＝ 235（covers 105・繋ぎ130を内包）
- **EP39〜EP55 の絵柄を選ばない（§7.7 の分離語）。** EP56 は 英国の村・高街・雨・赤ポスト・海辺町（Wales/Yorkshire）・郊外 parade・法廷/裁判所（gothic+modern）・Westminster・server room・call centre・village hall・TV glow の居間・通勤電車・グレーの海岸・dawn。**実在の顔が写るニュース/デモ映像・実在ロゴ（Post Office/Royal Mail/Fujitsu/ITV）が読める映像・バス主体の映像（R-SUICIDE 隣接回避・映り込み程度は §7.5 目視で当該ビート外へ）・泣く人・葬列・手錠/拘束・米国の街並みを選ばない。EP41 sodium prison corridor・EP44 病院 teal・EP47 two-lane/pickup・EP49 Utah・EP50 cyan・EP52 Texas suburb/bandana・EP55 Chicago night/el train を選ばない。**

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py \
    --kind video --query village_high_street --limit 60 --exclude-used --ep PD-2026-056-postoffice --json
```
`--exclude-used` は出荷ゲート `arc_nonrepeat` と同じ指紋集合を使う。**必ず付ける。**

## 7.3 実写在庫でカバーする代表シーン（`covers_scene_id` を付ける・§4.4 に pre-assign 済み）
> **★`covers_scene_id` は still 資産 ID 空間（S001..S210）を指す。** §4.4 の各エントリに pre-assign 済み（**105本が covers 付き**・意味一致 directive のため厚め・残り130は null の繋ぎ/情景）。

| covers（例） | 内容 | `--query` 例 | 幕(act) |
|---|---|---|---|
| S006/S008/S011 | 村の高街夜雨・赤ポスト・CRT glow | `village_street_rain` / `red_pillar_box` / `crt_screen` | 0 |
| S015/S022/S026/S036/S040 | 村の店・90s端末・till・年金の列・夜の帳簿 | `village_shop` / `crt_terminal` / `cash_till` / `queue_elderly` / `kitchen_paperwork` | 1 |
| S051/S058/S060/S068/S071 | 捜査の車・法廷・港・prison wall・誕生日 | `saloon_car_dawn` / `uk_courtroom` / `harbour_trawlers` / `prison_wall` / `birthday_cake` | 2 |
| S091/S094/S101/S104/S113/S122 | server room・office park・mediation・shredder・TV glow・call centre | `server_room` / `office_park_night` / `meeting_table` / `paper_shredder` / `tv_glow_room` / `call_centre` | 3 |
| S129/S131/S137/S141/S146/S148 | 輪転機・village hall・RCJ・判決・court steps・counter 復活 | `printing_press` / `village_hall` / `royal_courts` / `bound_judgment` / `court_steps` / `shop_counter_warm` | 4 |
| S167/S169/S173/S181/S187/S192 | TV夜の街・国会夜景・witness chair・通勤電車・行列・postman | `terraced_street_night` / `parliament_night` / `hearing_room` / `commuter_train` / `queue_umbrellas` / `postman_delivery` | 5 |
| S197/S198/S203/S205 | 消えた画面・dawn のポスト・警察アーカイブ・村の朝 | `dark_screen` / `pillar_box_dawn` / `police_archive` / `village_dawn` | 6 |

**残りは covers を持たない繋ぎ・情景**（institutional 廊下・rain window・grey sky・texture・dust shaft）。**暗いクリップに偏りすぎない**（暗側は約78本まで＝1/3・grey daylight・warm shop・morning を混ぜる）。

## 7.4 ライセンス（`ALLOWED_LICENSES` — これ以外選ばない）
```python
ALLOWED_LICENSES = {"cc0","royalty_free","generated_owned","Pexels License","Pixabay Content License"}
```

## 7.4a ★★★ 実写ストックライブラリを必ず使う（EP48/49 の burned lesson＝実写0本を潰す）★★★
- **ストックライブラリ:** `H:\pd-media\assets\stock`（`STOCK_MANIFEST.json`・動画74本＋静止155本・pexels/pixabay・商用可）。
- **調達方針（★counts は固定・factory 235 を変えない。レーン内の調達源を広げるだけ）:**
  1. `STOCK_MANIFEST.json` を読み、**意味（§7.3 の covers カテゴリ）に一致し §7.5 の全点目視 QC と R-FACE/R-SUICIDE/R-LOGO を通る実写動画を優先採用**（英国的な村・雨・海岸・ロンドンは stock に強い）。
  2. 残り枠を `H:\pd-media\assets\factory` 在庫で埋める。
  3. 各エントリの出所（`origin`: `stock` or `factory`）を `factory_selection.v001.json`（§7.6）と `stock_ledger.v001.json`（§10.2）に記録。
  4. **ストック静止155本は本編 body still（AI 210）レーンに混ぜない。**
- **★R-FACE/R-SUICIDE/R-LOGO を絶対順守:** 実在人物の顔が識別できるニュース映像・実在ロゴが読める映像・バス主体/自死連想の映像・泣く人を含むクリップは**ストックでも使わない**。EP39〜55 との sha256 被りゼロ（§7.7）はストック由来にも適用。
- **★カラーマッチは B が担当:** pexels/pixabay の発色バラつきは B が grey-British neutral グレードで AI still に合わせる（**milky wash にしない**）。

## 7.5 ★★★ factory のファイル名とサブタイプは信用できない ★★★
> **実際に起きた事故（EP36 大聖堂・EP38 牛・factory 棚ラベル全面破損）。** `subtype` は「その検索語で取った」記録であって中身の保証ではない。**235本は分割して全点見る。**

**選抜235本は例外なく次を経る:**
```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py \
    --ep PD-2026-056-postoffice --media video --dir "<235本の staging フォルダ>"
```
1. コンタクトシートを開き **235本すべてを1本ずつ見る**
2. 各本について `asset_manifest.v001.json` の **`eyeballed_content` に「実際に見た内容」を1文の英語で書く**（ファイル名の言い換え禁止）。`subtype` と食い違ったら `label_matches_content:false` を立てて選定から外す（差替え）
3. 実写シネマティックB-roll・EP56テーマ（英国・1999–2026）・ウォーターマークなし・識別可能な実在人物なしを確認
4. **★制約の目視:** 人物が写るクリップは後ろ姿/遠景/顔外しのみ。**実在ロゴ（Post Office/Royal Mail/Fujitsu/ITV/BBC）が読めるクリップ・米国街並み/右側通行・バス主体のクリップ・泣く人・手錠/拘束・法廷内の実在人物を使わない。時代錯誤（1999ビートに現代スマホ/薄型モニタ）を使わない。**
5. `05_visuals/factory_clip_qc.v001.json` を固定タイムスタンプで原子的に書く（冪等）

閾値（`check_visual_asset_qc.py`）: `DARK_LUMA_FLOOR=42.0` / `MAX_DARK_FRACTION=0.40` / `NEARDUP_SIM=0.90` / `MIN_VARIETY=0.60`。**暗いクリップは約78本（1/3）までに抑える。**

## 7.6 出力
```
episodes/PD-2026-056-postoffice/05_stock/factory_selection.v001.json   # 選定理由・幕割り当て・origin
episodes/PD-2026-056-postoffice/05_visuals/factory_clip_qc.v001.json   # ゲートが読む reviewed マニフェスト
```

## 7.7 EP39〜EP55 との重複ゼロ（BLOCKING）
```bash
./.venv/Scripts/python.exe scripts/select_postoffice_factory.py --verify-no-prior-overlap
```
`episodes/PD-2026-039-*/` 〜 `episodes/PD-2026-055-*/` の `05_stock/stock_ledger*.json`（および `05_visuals/asset_manifest*.json` があれば）を**読み取り専用で**開き、`sha256` 集合と EP56 の235本の積集合が**空**であることを確認。1件でも exit 1。**EP39〜EP55 のファイルは読むだけ。**

**分離レーン（色・素材・語）:** EP41 gold（監獄）／EP42 blue／EP43 amber／EP44 teal（病院）／EP45 crimson（domestic）／EP46 green／EP47 civil-violet（Texas road）／EP48 glover／EP49 somber-plum（Utah）／EP50 steel-cyan／EP52 evidence-blue（Texas suburb/bandana）／EP55 green-gray #7C9082（Chicago night/el train/interrogation）。**EP56 = grey British light（基調）＋ signage red `#C8102E`＋ phosphor green `#3FA66A`（画面内のみ）＋ shop-lamp amber `#E4B96B`（ACT1＋ACT4 復活1点のみ）。INK `#0B0C0D`。** これら他話の絵柄・色・被写体を1本も選ばない。

---

# 8. A-5: i2v モーション化 42本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする42本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）
種画像は §5 と同じ `generate_sdxl_4k.py`（variants なし）で `M<NN>_src.png` として生成（`ai_prompts.v001.md` に §8.1a の42行を追加）。**`role:"i2v_source"` として専用確保し body に回さない**（§4.2 不変条件8）。i2v_source の asset_id は `POH-MS01..MS42`、モーション成果物は `POH-M01..M42`。**幕別配分は §4.5 に pre-assign 済み**（ACT0 3 / ACT1 7 / ACT2 7 / ACT3 8 / ACT4 7 / ACT5 6 / ENDING 4 = 42）。
> **★このうち ★18本は §5.11 の匿名人物ビート（H01–H18）＝42本の内数**。**残り 24本が抽象/象徴種。**

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの42行を追加・各1枚・**poised-still の source**）
> 各種プロンプトは §5.6/§4.5 の対応 tag の「動く直前の poised-still」版。**動きが意味を持つ絵**（envelope が letterbox を抜ける直前・drawer が advice の上に閉じる直前・court steps で腕が上がる直前・page がめくれる直前 等）。末尾に §5.3 `[STYLE]` ＋ `Avoid:` §5.4 `[NEG]`（人物種は `[HSTYLE]`/`[HNEG]`）を全文連結。**★M01_src..M42_src の全42行 literal 化済み（穴なし）。★18本の人物種（M04/M06/M08/M11/M13/M14/M16/M19/M22/M24/M27/M28/M30/M31/M33/M34/M36/M37＝§5.11 H01–H18 の poised 版）は `[HSTYLE]`/`[HNEG]`、残り24本の抽象/象徴種は `[STYLE]`/`[NEG]`。そのまま転記する。**

```
- `M01_src.png`
The green-on-black ledger terminal alone in a dark shop, its phosphor glow held at the edge of a flicker, smeared figures poised to change by themselves, worn counter wood drinking the light, no person, no readable text [STYLE] Avoid: [NEG]
- `M02_src.png`
A brown window envelope on a coir doormat in a dark hallway, a shadow from the door glass beginning to slide across it, address panel a smear, the institution one breath from arriving, no person, no readable text [STYLE] Avoid: [NEG]
- `M03_src.png`
A village high street at night in steady drizzle, rain drifting through one street lamp's cone, a red sign's wet reflection trembling on the tarmac, the town holding its breath, no people, no readable text [STYLE] Avoid: [NEG]
- `M04_src.png`
An anonymized sub-postmistress seen only from behind at her warm counter, mid-motion passing a pension book under the brass grille to a soft customer shape beyond, shop-lamp amber light, poised in the easy rhythm of a trusted trade, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M05_src.png`
A green terminal screen on a shop counter, its smeared balanced columns poised at the instant one total begins to brighten wrongly, phosphor light starting to harden, the servant turning, no person, no readable text [STYLE] Avoid: [NEG]
- `M06_src.png`
A husband and wife at a kitchen table at night seen from behind, hands paused over sorted piles of smeared receipts, one bare bulb swaying almost imperceptibly above, the recount poised to start again, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M07_src.png`
An open till drawer at dawn, banknotes lifting at one corner in a draught, the counted stacks beside a cold green glow poised to be counted a fourth time, no person, no readable text [STYLE] Avoid: [NEG]
- `M08_src.png`
An anonymized woman on a telephone in a dark shop seen from behind against green screen glow, cord swaying gently, shoulders squared, poised between the question and the answer that never changed, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M09_src.png`
A brown envelope frozen halfway through a brass letterbox slot in a panelled front door, hallway dark beyond, its shadow already on the mat, the demand mid-delivery, no person, no readable text [STYLE] Avoid: [NEG]
- `M10_src.png`
A generic red post-office sign over a village shop doorway in warm morning light, bunting-free and emblem-free, the light poised to shift as a cloud crosses, warmth with a countdown on it, no people, no readable text [STYLE] Avoid: [NEG]
- `M11_src.png`
Two anonymized suited investigators seen from behind mid-stride toward a village shop's door at dawn, briefcase swinging slightly, cold light along their shoulders, procedure in motion, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M12_src.png`
A charge sheet caught in mid-air a hand's width above a dark desk, its two smeared counts angled toward the lens, cold light through blinds, paper about to land with the weight of a door, no person, no readable text [STYLE] Avoid: [NEG]
- `M13_src.png`
A pregnant anonymized woman walking upright down a long corridor of cold institutional light, seen from behind in silhouette, coat closed, pace even and unhurried, composed the whole length of the frame, no face, no restraint, no readable text [HSTYLE] Avoid: [HNEG]
- `M14_src.png`
A public gallery of anonymized backs caught leaning forward as one at a verdict's approach, coats shifting slightly, wood panelling beyond, restrained collective breath, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M15_src.png`
A long grey prison wall under white sky, a cloud shadow poised at its far end about to travel the whole length, drizzle darkening the pavement, time doing its arithmetic, no people, no readable text [STYLE] Avoid: [NEG]
- `M16_src.png`
An anonymized man with an armful of folders seen from behind, mid-step through tall court doors alone, his reflection sliding in the polished stone floor, one man carrying his own defence, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M17_src.png`
A rubber-banded stack of brown envelopes on a hallway table, the top one poised at a slide, the band strained, years of demands about to spill, address panels all smears, no person, no readable text [STYLE] Avoid: [NEG]
- `M18_src.png`
The pages of a bound internal report caught mid-riffle under one cold lamp, each leaf a smear frozen in the air, the paragraph that priced honesty about to fall shut, no person, no readable text [STYLE] Avoid: [NEG]
- `M19_src.png`
An anonymized engineer seen from behind walking a dark server aisle, rack LEDs blinking green along both sides, lanyard swinging, poised mid-patrol through the country's most trusted liar, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M20_src.png`
A branch terminal in a closed dark shop, its green cursor poised at the head of a smeared line with no hand at the keyboard, the empty chair's shadow long across the floor, a correction about to happen by itself, no person, no readable text [STYLE] Avoid: [NEG]
- `M21_src.png`
Fine white shredded strips poised in mid-fall between a shredder's teeth and a brimming basket, typed characters reduced to flecks, cold blind-light striping the scene, the minutes on their way out of history, no person, no readable text [STYLE] Avoid: [NEG]
- `M22_src.png`
Two anonymized forensic accountants seen from behind at a file-drowned table, one page passing between their hands in mid-air, lamplight over the exchange, the honest audit in motion, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M23_src.png`
A deep file drawer a finger's width from closed over a ribboned legal advice, the pink ribbon's tail still catching the light, the burial one breath from complete, grey cabinets beyond, no person, no readable text [STYLE] Avoid: [NEG]
- `M24_src.png`
An anonymized executive seen only from behind at a night boardroom window, city light shifting slowly across the glass, printed pages held loosely at the thigh, stillness with everything underneath it, no face, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M25_src.png`
A wide grey estuary at low tide, still water and mudflats, one slow band of brighter sky poised to open at the horizon, an enormous quiet breathing once, no people, no vehicles, no readable text [STYLE] Avoid: [NEG]
- `M26_src.png`
Newspaper press rolls at the instant of start-up, the paper river taut and beginning to blur, ink mist rising into the work lights, seven names about to reach the country, no people, no readable text [STYLE] Avoid: [NEG]
- `M27_src.png`
People filing into a lit village hall at dusk seen from far behind, coats and caps bobbing through the doorway's warm rectangle, gravel underfoot, strangers about to become an army, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M28_src.png`
A methodical anonymized man at his kitchen-table laptop at night seen from behind, hands poised over the keys, box files walling the lamplight, the campaign's ten-thousandth evening in progress, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M29_src.png`
The gothic stone face of London's law courts in rain, drizzle drifting through the arches' shadow, a pigeon lifting from a ledge, wet pavement mirroring the mass about to be shaken, no people, no readable text [STYLE] Avoid: [NEG]
- `M30_src.png`
Claimants queueing outside a London court under umbrellas seen from far behind, the line shuffling one place forward, drizzle drifting through streetlight, patience advancing, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M31_src.png`
A crowd on court steps seen from behind at the instant of release, arms beginning to lift, one sheet of smeared paper rising above the shoulders, April light hard on the stone, joy with its back turned, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M32_src.png`
A thick bound judgment volume poised in the last centimetre of falling closed, pages fanning air, paper flags trembling, three hundred pages of demolition about to become law's memory, no person, no readable text [STYLE] Avoid: [NEG]
- `M33_src.png`
A family of anonymized figures on a sofa seen from directly behind, silhouetted against a television's bright smeared glow, the light flickering over their stillness, nobody moving to change the channel, no faces, no identifiable child, no readable text [HSTYLE] Avoid: [HNEG]
- `M34_src.png`
A packed hearing-room gallery seen from its back row, anonymized shoulders and grey heads utterly still, the small bright empty witness chair far below them, the room breathing as one, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `M35_src.png`
A formal parchment on green leather, its ribbon's tail stirring in a draught, engrossed smeared text catching chandelier light, a law one signature old, no person, no readable text [STYLE] Avoid: [NEG]
- `M36_src.png`
A postman with a shoulder bag seen from behind walking a village street at morning, one white official envelope bright in his hand, drizzle silvering the air ahead of him, the state finally writing back, no face, no emblem, no readable text [HSTYLE] Avoid: [HNEG]
- `M37_src.png`
Anonymized hands at a kitchen table opening a thick white official envelope, the letter half-unfolded and poised, its text a smear, morning light warming the wood grain, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M38_src.png`
The Houses of Parliament across the black river at night, lit windows doubled and trembling in the water, the last rain moving off downstream, the building poised over its own precedent, no people, no readable text [STYLE] Avoid: [NEG]
- `M39_src.png`
A switched-off branch terminal's dead glass reflecting a grey window, rain shadows poised to crawl across the dark screen, dust along the keyboard seam, the machine outliving its verdicts, no person, no readable text [STYLE] Avoid: [NEG]
- `M40_src.png`
The generic red pillar box on its village corner at first light, drizzle beginning, the grey dawn poised to strengthen along the wet kerb, the state still in walking distance, no emblem, no people, no readable text [STYLE] Avoid: [NEG]
- `M41_src.png`
A village high street at first light, wide and empty, drizzle drifting slowly through the frame, wet tarmac silvering toward the far red sign, the ordinary country waking, no people, no readable text [STYLE] Avoid: [NEG]
- `M42_src.png`
An abstract near-black field, a last low breath of phosphor green fading beside a dying ember of signage red, both poised at the edge of going out, fine grain drifting, no objects, no people, no readable text [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな。`comfy_wan_burge.py` を下敷きにパスと SHOTS だけ差し替え）
```python
HOST = "http://127.0.0.1:8188"
HIGH = "wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors"
LOW  = "wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors"
VAE  = "wan_2.1_vae.safetensors"       # ★2.1（2.2 ではない）
CLIP = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
WIDTH, HEIGHT = 1280, 720
FRAMES = 41
STEPS = 40 / SPLIT = 20 / SHIFT = 5.0   # ★SHIFT 5.0（8.0 はバグ）
CFG = 3.5 / SAMPLER,SCHEDULER = "euler","simple" / FPS = 16
STILL_DIR     = H:\pd-media\assets\ai\postoffice
VIDEO_OUT_DIR = H:\pd-media\assets\ai_video\postoffice
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = "static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, morphing face, flickering, jitter, warping, melting, text, watermark, identifiable face, real person likeness, child face, crying person, weeping, corpse, handcuffs, restrained person, bus, vehicle striking, logo"
```
**ゲート:** `dry_validate`（length=5）/ `assert_loaded_completely` / `assert_frame_math`。`--run` パスにだけ配線。

## 8.3 実行手順（まず1本で通す・★42本は複数日）
```bash
py -3.11 scripts/comfy_wan_postoffice.py --build
py -3.11 scripts/comfy_wan_postoffice.py --run --shot M01
py -3.11 scripts/comfy_wan_postoffice.py --run-all
```
1本 24–73 GPU分・42本で 18–48時間。**夜間分割で回す。開始前にマシン状態を確認（A1111 との VRAM 競合は unload-checkpoint で解放）。**

## 8.4 RIFE で 48fps 化（`rife_postoffice.py`・`rife_burge.py` と同手順）
```
RIFE = D:/AI/tools/rife-ncnn-vulkan-20221029-windows/rife-ncnn-vulkan.exe / モデル rife-v4.6
```
1. Wan 出力先頭 **5フレームは検証プローブなので捨てる**（`DROP_VALIDATE=5`）
2. 残り41を `f0001.png` 連番 → RIFE 2x を2回（=4x）→ **164フレーム**
3. 164/48fps = **3.417秒** → `ffmpeg -framerate 48 -i f%04d.png -c:v libx264 -pix_fmt yuv420p` で `M<NN>_rife.mp4`
4. フレーム数検証 `n2 >= 4*n0 - 8` でなければ `SHORT?` で記録し reject

## 8.5 i2v の QC
- **自死表象・悲嘆・拘束・実在ロゴ・可読文字が生成されていないこと**（必ず目視・特に M13 の妊婦シルエットの尊厳・M25 の無人保証・M40/M41 に車両/バスが湧いていないこと）
- モーフィング/ちらつき/ワープ/melt が無いこと → あれば別シードで再生成
- H シリーズが**識別可能な実在 likeness**に転じていないこと・**識別可能な子供顔**が出ていないこと（M33 の子影は out-of-focus のみ）・スタンドインが尊厳を失う動き（泣き崩れ・うずくまり等）をしていないこと
- ledger 系（M01/M05/M20/M39）の画面に**可読の数字/文字が出ないこと**／sign/pillar box 系（M10/M40）に**実在ロゴ・紋章が出ないこと**
- 3.417秒あるので B のカット設計では 3.0–3.4秒で使う想定（42本 × 2回 = 84カット）

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど30本）

| 種別 | 選定 | 用途 |
|---|---|---|
| `particle_assets` | **15本** | shop dust warm（ACT1）・drizzle drift・rain on glass・archive dust・paper fiber・courtroom dust shaft・server room dust・morning grey dust |
| `light_assets` | **10本** | phosphor green glow（ledger ビートのみ）・cold window bar・**shop-lamp amber glow（ACT1＋ACT4 復活のみ=L03/L09）**・**tv flicker blue（ACT5 の一夜のみ=L04）**・grey overcast key・dawn sweep |
| `vfx_overlays` | **5本** | 微細な grain・cold light noise・green glitch min |
| **合計** | **30本** | |

**ルール:** 合成レイヤーは `check_asset_reuse` の distinct に数えない → `remotion/public/postoffice/overlay/` に置き、`postoffice_film.json` の `cuts[].src` には**出さない**。**★per-beat の疎なアクセントのみ＝全編常駐の持続レイヤーにしない・scanline/CRT full-frame/vignette-wash を選ばない（DESIGN §1・screen-wash ≤0.07）。** 黒背景でループするものを選び `blend_hint` を書く。他話色を選ばない。§7.5 の目視QC対象（30本）。

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_postoffice_assets.py`）
```
remotion/public/postoffice/img/     ← role=body の静止画210枚（★depth なし）
remotion/public/postoffice/factory/ ← 選定 factory .mp4 235本（§4.4 の F001..F235 名で）
remotion/public/postoffice/motion/  ← i2v M<NN>_rife.mp4 42本
remotion/public/postoffice/overlay/ ← 合成レイヤー 30本（§4.6 の P/L/V 名で）
remotion/public/postoffice/thumb/   ← thumb_face T01..T03（B の PostofficeThumbnails が参照）
```
- `public_path` はマニフェストの値（§4.4/§4.5/§4.6）と実ファイルが一致すること
- factory 動画は `libx264 crf 16 preset medium -an` で **30fps に conform** してコピー
- i2v は 48fps のまま置く
- 既存 sha256 一致ならコピーをスキップ（冪等）
- **★depth の同名ペアは作らない・置かない**（§6.4）

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する）:**
- factory の `public_path` は必ず `postoffice/factory/` の下（`/factory` を含む）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も含めない
- 合成レイヤーは `postoffice/overlay/` に置き `cuts[].src` に出さない

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`
全静止画・i2v・factory・overlay・thumb_face を1行ずつ: `asset_id`/`path`/`source`(`ai_codex`|`factory`|`stock`)/`origin`/`license`/`commercial_use`/`sha256`/`ai_disclosure_required`/`generated_at`。

## 10.3 境界契約マニフェストの出力
```bash
./.venv/Scripts/python.exe scripts/build_postoffice_asset_manifest.py
./.venv/Scripts/python.exe scripts/build_postoffice_asset_manifest.py --verify
./.venv/Scripts/python.exe scripts/build_postoffice_asset_manifest.py --reuse-feasibility
```
この3つが exit 0 で「マニフェストが本番になった」。**★factory 235 / motion 42 / overlay 30 が非空で実体化しているか（不変条件17/18/16）を必ず確認。**

---

# 11. 素材反復禁止ゲートの実仕様（`check_asset_reuse.py`）
```python
MAX_USES_FACTORY = 1
MAX_USES_MOTION  = 2
MAX_USES_STILL   = 2
MIN_FIRST_USE_SHARE = 0.70
MAX_AVG_USES_PER_SOURCE = 1.4   # ★EP49 は 1.8 で flag された
```
種別判定は**パス文字列**（`kind_of()`）。§10.1 の命名規則を守る。
EP56 の設計値: still 244/210=1.162(≤2) / factory 235/235=1.0(≤1) / motion 84/42=2.0(≤2) / first-use 487/563=0.8650(≥0.70) / avg-uses 563/487=1.156(≤1.4)。**全て達成可能。**

---

# 12. 絶対にやらないこと
- **EP39〜EP55 のファイル・素材に触らない。** 読み取りのみ可。素材・色・音のレーンも分離（§7.7）。
- **スレッドBの所有ファイル（§0.2）に触らない**。ただし `04_scenes/ai_prompts.v001.md` は A が書く。
- **課金ジョブを起動しない**（ElevenLabs TTS / 課金画像API / アップロード）。
- **公開済み・出荷済み mp4 を上書き・再レンダしない。**
- **実在人物の肖像・likeness をどこにも作らない**（Bates/Sercombe/Misra夫妻/Hamilton/Castleton/Thomas/Griffiths/Vennells/Jenkins/Roll/Warmington/Henderson/Clarke/Arbuthnot/Wallis/Thomson/Fraser/Wyn Williams/Sunak/Patterson/国王/**ITV俳優 Toby Jones・Monica Dolan**）。**匿名・非識別の一般人は可。**
- **★自死・悲嘆・拘束の表象を一切作らない**（R-SUICIDE/R-DIGNITY・本作の最重要禁止）。Griffiths ビートは無人環境のみ・バス/道路の人物/ロープ/薬/遺書ゼロ・泣き顔/うずくまりゼロ。
- **★実在ロゴ（Post Office/Royal Mail/Fujitsu/ITV/BBC/crown crest）を再現しない。** generic な赤看板・赤ポストの形のみ。
- **制約に反する文言・絵を作らない**（§1.2/§1.3）: 被害者の有罪示唆／個人の刑事責任の既成事実化／hedged 数値の断定／可読の偽公文書・偽帳簿・偽画面／実在人物 likeness／dochighlight／捏造・可読引用／milky wash/scanline／時代錯誤（米国モチーフ含む）。
- **バリエーション（`_02`/`_03`）を作らない・`--variants 3` を使わない。** 1シーン1枚。（factory の subtype `_02` は別素材の意・混同しない。）
- **role=thumb / still_thumb を作らない・overlay を30本以外にしない・thumb_face を3枚以外にしない。** also_thumb は body 4枚（§4.3a＝S001/S057/S106/S173）。
- **★factory 235 / motion 42 / overlay 30 の配列を空・stub のまま出荷しない**（EP45/EP38 事故）。
- **★depth map を生成しない・`depth_path` を持たせない**（§6.4）。
- **★dochighlight figure を作らない・言及しない**（grep で 0）。
- **枚数を「だいたい」で決めない。** §3 の確定値（still 210 / factory 235 / i2v 42 / thumb_face 3 / distinct 487 / first-use 0.8650 / still-share 0.4334 / avg-uses 1.156 / overlay 30）と §3.3 の検算をそのまま使う。合わなければ本書を疑って報告。
- **★ファイル名・subtype・プロンプトを根拠に「大丈夫」と判断しない。** 生成物・在庫クリップを実際に見る。

---

# 13. 完了報告に含めるもの
```
1. accepted 静止画の枚数と内訳（body 210 [＝object 125 ＋ ★HP human-present 85 = 40.5%] / i2v_source 42 [＝抽象 24 ＋ ★人物 18] / thumb_face 3 / F-series 12 / also_thumb 4 [§4.3a＝S001/S057/S106/S173] / reject N）
2. factory 選定 235本のリスト（asset_id / subtype / origin / eyeballed_content）と、subtype と食い違って外した本数、
   sign/pillar box/court/screen クリップの「no readable text / no real logo / no identifiable face / no suicide-adjacent imagery」確認、stock 由来の本数
3. EP39〜EP55 重複ゼロの確認結果
4. i2v 42本の frames / duration_sec と、SHORT? の有無、★H01–H18（18本）の匿名・非識別・adults-only・尊厳確認、
   ★HP body 85枚が匿名・非識別・実在 likeness なし・識別可能子供顔なし・自死/悲嘆/拘束表象ゼロ・
   可読文字/実在ロゴなし・★変化マトリクス（§5.6・被写体+構図+光の3要素同時一致ゼロ）の確認
5. 合成レイヤー30本のリスト
6. §0.4 の [A-DONE-1]〜[A-DONE-5] の実行結果（exit code）＋ factory 235/motion 42/overlay 30 が非空で実体化した確認 ＋ depth_path をどこにも生成していない確認
7. §3.3 の検算 [1]〜[8] を自分で再計算した結果（avg-uses/source 1.156≤1.4 を含む）
8. asset_manifest.v001.json の counts ブロック（still_body 210 / still_i2v_source 42 / motion 42 / factory 235 / overlay 30 / thumb_face 3）
9. 制約・1枚前提の自己申告（被害者の有罪示唆なし・個人の刑事責任既成事実化なし・自死/悲嘆/拘束表象ゼロ・
   実在の顔/likeness ゼロ・実在ロゴゼロを目視確認・hedged 数値の可読断定なし・dochighlight 文字列ゼロ・
   捏造/可読引用なし・milky wash/scanline なし・depth なし・バリエーション0・時代錯誤なし・A↔B同一スキーマ
   [schema postoffice_assets.v1 / role enum body|i2v_source|thumb_face|reject / counts / also_thumb 集合 4 / overlay 30 / thumb_face 3]）
```

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
