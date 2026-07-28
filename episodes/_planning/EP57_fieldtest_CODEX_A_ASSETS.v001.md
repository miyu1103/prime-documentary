# EP57 fieldtest — Codex スレッドA「素材生成」引き継ぎプロンプト v001（30分・5幕・reveal ladder・四層素材ドクトリン初号機）

> **このファイルは単体で完結している。他のファイルを読まなくても着手できる。**
> 設計書（DESIGN_ARCHITECTURE）も実装スレッドB（CODEX_B）も**読まなくてよい**（必要な数値はすべて本書に転記済み）。
> ★30分尺。**★★本作から「四層素材ドクトリン」（オーナー指示 2026-07-29）が適用される。** 実写アーカイブが第一層に昇格し、Codex 静止画は「アーカイブで撮れないものを埋める層」になる。**ただし Codex のプロンプト本数は1本も減らない（still 210 + i2v種 42 + thumb 3 + F系 12 = 267 本すべて本書に literal で存在する）。** 変わるのは「カット配分」だけ（§3）。
> **「だいたい」で決めず §3 の確定値と §3.3 の検算をそのまま使う。**

```
あなたは Prime Documentary（YouTubeドキュメンタリーチャンネル）の制作エンジニアです。
リポジトリ: C:\Users\aab15\Documents\prime-documentary
Python:     C:\Users\aab15\Documents\prime-documentary\.venv\Scripts\python.exe
メディア:   H:\pd-media
アーカイブ: H:\pd-media\assets\archive（台帳 H:\pd-media\assets\archive\_ledger\*.jsonl・111,821点）
担当:       EP57 / Episode ID: PD-2026-057-fieldtest / slug: fieldtest
Composition id: Ep57Fieldtest（B が Root.tsx に登録・A は staging まで）／1920x1080 / fps30 / 30:00
出力先:     H:\pd-media\assets\ai\fieldtest\
事件:       The $2 roadside drug test（Amy Albritton と Harris County の「変異」416件）
            2010年8月、テキサス州ヒューストンのストリップモール駐車場。ルイジアナ州モンローで
            アパート管理人をしていた Amy Albritton は、交際1か月の男性が運転する自分の車の
            助手席にいた。車線変更で停められ、警官が車の天井裏に注射針を見たと報告書に記載、
            車内を捜索。床から白い小さな塊、市販頭痛薬 BC Powder、注射針が出た。
            警官はパトカーのトランクから2ドルの携帯試薬キット（プラスチック袋＋ピンク色の
            コバルトチオシアネート溶液のガラスアンプル）を出し、塊のかけらを落とした。
            溶液は青く変わった。警官は証拠提出書に手書きで「.02 grms crack cocaine」と記入。
            秤は現場に無く、これは目視の推定値だった。彼女は逮捕から9時間後の午前3時37分に
            収監され、翌朝には重罪コカイン所持で有罪答弁をした。求刑45日、服役21日。
            仕事（＝住居付き）を失い、家財は路上に出された。
            2011年2月23日、ヒューストン市警犯罪研究所の分析官 Ahtavea Barker が
            ガスクロマトグラフ質量分析計にかけた。白い粉はアスピリンとカフェイン（＝BC Powder）。
            注射針は残渣が少なすぎて検査不能。そして塊は——データベースのどの化合物とも
            一致しなかった。薬物ではなかった。検査票には N.A.M.（一致無し）と
            N.C.S.（規制物質は検出されず）、そして重量【0.0134グラム】、Barker の言葉で
            「ひとつまみの塩と同じくらい」。彼女は既に釈放済み・既に重罪犯だった。
            研究所が偽陽性を警官に通知する仕組みは無く、正しい報告書は誰宛でもなく綴じられた。
            Harris County 地方検事局は自局のファイルを数え直し、2004年1月〜2015年6月に
            未訂正の「変異」416件（全て有罪答弁）を発見。うち251件は単純に「規制物質なし」。
            416件中301件がヒューストン市警の逮捕、その301件中212件が「規制物質でない証拠」に
            基づく有罪。212人全員が答弁し、93%が実刑、50人は薬物前科なし。
            2014年7月29日、元検事 Marie Munier が「Dear Sir or Madam」で始まる定型書簡を
            送付——「あなたは誤って起訴され有罪とされた」。宛先は運転免許証の住所＝
            有罪答弁で失ったあのアパートだった。彼女はそこにいなかった。
            2016年3月、元ヒューストン市警本部長 Charles McClelland は記者に言った——
            「警官は化学者ではない。パトカーのボンネットの上で試薬検査をすべきではない」。
            それでもキットは撤回されなかった。2015年に地検が「研究所報告前の答弁禁止」を導入、
            2016年12月にテキサスの委員会が研究所確認の義務化を勧告、2017年の州法HB34は
            【義務化ではなく「調査」】を命じただけ。2017年7月、ヒューストン市警はキット使用を
            停止したが、公表された理由は精度ではなく【フェンタニル被曝から警官を守るため】。
            2024年1月、ペンシルベニア大 Quattrone センターの調査：全米年150万件超の薬物逮捕の
            うち約77万3千件が呈色試薬を使い、年およそ3万人が偽陽性で嫌疑をかけられている。
            2026年3月26日、コロラド州が全米初の規制法 HB 26-1020 に署名（下院65-0・上院33-0）。
            ★主題は【2ドルの色の変化が重罪を決め、真実は6か月遅れて誰宛でもなく届いた。
              そして機械はいまも動いている】。
            ★Amy Albritton は【存命の私人】。ProPublica/NYT Magazine の調査報道を通じてのみ
              公になった。無実を「主張」する映画ではなく【研究所の結果を報告する】映画。
              尊厳が最優先。likeness 一切禁止。
            ★★逮捕した警官2名は【存命】で【何らの認定も受けていない】。名前を出さない・
              人物として描かない・動機を推測しない。バッジ番号/所属章/車両表記/機関シールなど
              【識別可能な標章を一切描かない】。
            ★★★【「食べ物だった」と断定しない】。研究所の認定は「規制物質は検出されず」
              「データベースのどれとも一致しない」。"food debris, perhaps" は調査報道側の
              留保付き推測であり、留保か帰属を必ず伴う。
            ★★★【薬物使用の描写を一切作らない】——皮膚に刺さる注射針、吸引・服用、
              見せ場としての粉末、いずれも全面禁止。血・傷・遺体・拘束された人物の
              苦悶も全面禁止。実在人物（Albritton/警官/判事/弁護人/分析官/検事/McClelland/
              Acevedo/Scott）の顔・肖像・likeness を一切作らない。匿名・非識別の一般人は可。
              時代考証 1973–2026 のアメリカ（2010年の路上ビートにスマホを混ぜない）。
```

---

# 0. このスレッド（A）の責務・境界・完了条件

## 0.1 責務（GPU律速・目視律速の長時間ジョブ・30分スケール）

本編で使う「絵」を全部そろえ、1本のマニフェストに書き出すところまで。

| # | 作業 | 成果物 | 目安 |
|---|---|---|---|
| A-1 | SDXL静止画のバッチ生成（**210本の固有プロンプト×1枚＝210枚**・バリエーション0） | `H:\pd-media\assets\ai\fieldtest\S<NNN>.png` | 5–8時間（GPU） |
| A-1b | i2v 種画像の生成（**42本の固有プロンプト×1枚＝42枚**・バリエーション0） | `H:\pd-media\assets\ai\fieldtest\M<NN>_src.png` | 1.5–2.5時間（GPU） |
| A-1c | サムネ用 emotive-face 静止画（**3枚**・CTR §4A・非実在の illustrative face・§5.12） | `H:\pd-media\assets\ai\fieldtest\T<NN>_face.png` | 20分（GPU） |
| A-2 | 静止画のQCと目視（**全255枚を目視必須**＝210 body + 42 i2v種 + 3 thumb_face） | `05_visuals/still_qc.v001.json` + コンタクトシート | 2.5–4時間 |
| A-3 | ~~depth map~~ **不要（本作は depth treatment を使わない・§6.4）** | — | — |
| A-4 | **実写アーカイブ 252本**の選定と**全点ラベル付きコンタクトシート目視QC**（★四層ドクトリンで最大層） | `05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json` | 5–8時間（うち目視だけで3時間以上） |
| A-5 | i2v モーション化 **42本**（Wan 2.2 A14B → RIFE 48fps） | `H:\pd-media\assets\ai_video\fieldtest\M<NN>_rife.mp4` | 18–48時間（GPU・**複数日**） |
| A-6 | 合成レイヤー（particle/light/vfx）の選定 **30本** | `05_stock/overlay_selection.v001.json` | 1時間 |
| A-7 | 権利台帳と**境界契約マニフェスト**の出力 | `05_stock/stock_ledger.v001.json` / **`05_visuals/asset_manifest.v001.json`** | 30分 |
| A-8 | Remotion public への staging | `remotion/public/fieldtest/{img,factory,motion,overlay,thumb}/` | 40分 |

> **★★ 最重要の前提（EP42–56 から継続）: 1シーン1枚・バリエーション0 ★★**
> **distinct still を固有プロンプトで各1枚ずつ生成**する（still 210本＝210行の固有プロンプト、各1枚）。
> `generate_sdxl_4k.py` は **variants 指定なし（＝1枚）** で回す。**`--variants 3` は使わない。`_02`/`_03` を作らない。**
> **総生成画像 = still 210 + i2v 種 42 + thumb_face 3 = 255枚（各1回）＋ F系12枚 = 267枚。** アーカイブ252本は生成でなく在庫からの選抜。
> ★**`--only S001` のログで `shots=255` を確認**してから本番を回す。
> ★i2v 42本は**複数日GPU**。開始前にマシン状態を確認し、夜間・分割で回す。

## 0.2 スレッドB（実装）との境界＝接続点はただ1ファイル

`episodes/PD-2026-057-fieldtest/05_visuals/asset_manifest.v001.json` **のみ**。A はこのファイルを書き、B はこのファイルだけを読む。**EP45 の空配列事故**（配列を宣言しただけで実体化せず、B が 0 件で走った）を繰り返さないため、`stills[]` / `factory[]` / `motion[]` / `overlay[]` は**すべて実体化**し、`--verify` が件数を突き合わせる。

### ファイル所有権（破ると並行作業が壊れる）

| パス | 所有 | A の権限 |
|---|---|---|
| `H:\pd-media\assets\ai\fieldtest\**` | A | 作成・上書き可 |
| `H:\pd-media\assets\ai_video\fieldtest\**` | A | 作成・上書き可 |
| `episodes/PD-2026-057-fieldtest/04_scenes/ai_prompts.v001.md` | A | 作成 |
| `episodes/PD-2026-057-fieldtest/05_visuals/**` | A | 作成 |
| `episodes/PD-2026-057-fieldtest/05_stock/**` | A | 作成 |
| `remotion/public/fieldtest/**` | A | 作成（staging のみ） |
| `remotion/src/**` | **B** | **触らない** |
| `episodes/_planning/EP57_*` | 企画 | **触らない** |
| `H:\pd-media\assets\factory\**` / `H:\pd-media\assets\archive\**` | 素材棚 | **読み取り専用。移動・改名・削除禁止** |

## 0.3 A が使う／作るスクリプト

既存をそのまま使う: `generate_sdxl_4k.py`（静止画）· `search_archive.py`（**アーカイブ検索・本作の主力**）· `select_factory_assets.py`（選抜＋ラベル付きコンタクトシート）· `build_footage_contact_sheet.py`（目視シート）· `comfy_wan.py`（i2v）· `rife_*.py`（48fps化）。
clone して作る: `qc_fieldtest_stills.py`（← `qc_burge_stills.py`）· `build_fieldtest_asset_manifest.py`（← `build_burge_asset_manifest.py`）· `stage_fieldtest_assets.py`（← `stage_burge_assets.py`）· `rife_fieldtest.py`（← `rife_burge.py`）。**clone 元を読んでから書く。同名別実装を作らない。**

## 0.4 完了条件（すべて緑で完了。1つでも赤なら未完了）

```bash
# [A-DONE-1] 生成物の実在と枚数
./.venv/Scripts/python.exe scripts/qc_fieldtest_stills.py --ep PD-2026-057-fieldtest --assert-counts 210,42,3
# [A-DONE-2] 全点目視（コンタクトシート消化の記録が入っていること）
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-057-fieldtest --media image
# [A-DONE-3] アーカイブ252本のラベル付きコンタクトシート審査（exit 3 なら未完了）
./.venv/Scripts/python.exe scripts/select_factory_assets.py --ep PD-2026-057-fieldtest --assert-count 252
# [A-DONE-4] 境界契約マニフェストの検証
./.venv/Scripts/python.exe scripts/build_fieldtest_asset_manifest.py --ep PD-2026-057-fieldtest --verify
# [A-DONE-5] staging 後の public 実在確認
./.venv/Scripts/python.exe scripts/stage_fieldtest_assets.py --ep PD-2026-057-fieldtest --verify
```

---

# 1. ★★★ 最優先の絶対条件（正確性制約・ガードレール）★★★

**A が生成する画像・A が書く全文字列（プロンプト・tags・caption_hint・covers・subtype）に適用。違反は BLOCKER であり、後工程では直せない。**

## 1.1 R1/R2（生成ビジュアル全般）

1. **R-FACE**: 実在人物の顔・肖像・likeness を作らない。Albritton、逮捕した警官2名、判事 Velasquez、弁護人 Richardson、分析官 Barker、検事 Anderson/Munier/Chandler、McClelland、Acevedo、L. J. Scott Jr. のいずれにも似た顔を作らない。**匿名・非識別の一般人（後ろ姿・手元・シルエット・目から下でクロップ・浅い被写界深度で溶かした顔）は可。**
2. **R-NO-DRUG-DEPICTION**: 皮膚に刺さる注射針、薬物の吸引・服用・調製、見せ場としての粉末、拘束された人物の苦悶、血・傷・遺体を**一切描かない**。注射針は「報告書の一行」「ピントの外にある物体」までが上限。
3. **R-READABLE**: 読める偽文書を作らない。検査票・答弁書・書簡・特許図面・州法条文・証拠袋のラベルは**すべて判読不能なにじみ**。数字・日付・氏名・機関名が読めてはいけない。
4. **AI 開示**: 全生成画像は `ai_disclosure_required: true`。実在資料として提示しない（invariant 11）。

## 1.2 ★正確性制約（違反は BLOCKER）

- **R-NOT-A-DRUG** — 研究所の認定は「規制物質は検出されず」「一致無し」。**「食べ物だった」と断定する絵・語を作らない**（皿・食卓・パン屑を食品として提示する構図は禁止）。塊は常に「正体不明の白い粒」として撮る。
- **R-OFFICER** — 逮捕した警官を人物として特定しない。**バッジ番号・所属章・肩章・車両ドアの表記・機関シール・制服の識別要素をすべて排除**（無地・影・浅いピント）。悪役として演出しない（見下ろし・威圧構図・暗い顔の逆光ヒーロー構図を使わない）。
- **R-LIVING** — 存命の私人・公人いずれも、記録にある行為の範囲でのみ描く。内心・感情の演出を絵で作らない（泣き崩れる・頭を抱える等は禁止。§5.11 の dignity 規定参照）。
- **R-NO-TEXAS-BAN** — テキサスは「調査」を命じただけ。「禁止」「規制」を示す絵・語（×印・停止標識・封印）をテキサス関連ビートに使わない。
- **R-HOUSTON-REASON** — 2017年7月の使用停止の公表理由は**フェンタニルからの警官保護**。精度是正の勝利として演出しない。
- **R-COLORADO** — 法案番号・票数・署名日・条項のみ。**施行日を描かない・書かない**（`status_as_of` 2026-07-29）。
- **R-RACE** — 人種に関する数字（59% / 24%）は数字のみ。人種を主題化する構図・群衆・対比を作らない。シルエットは尊厳をもって。
- **R-NUM** — ヘッジ表現を絵の中の数値として固定しない。**画面に数字を焼き込まない**（数字は AE と FigureBeats の仕事）。
- **R-LOGO** — Houston PD / Harris County / Scott Company / Sirchie / Safariland / NIK / BC Powder / ProPublica / New York Times の標章を一切描かない。**汎用の形状のみ。**
- **R-DOCHL** — `dochighlight` は**BANNED**（レンダリング不具合に見えるとオーナーが3回指摘）。A はこの語を成果物のどこにも書かない。
- **R-AE-LAYOUT** — `DATE_STAMP` と `SEAM_TRANSITION` は clone 元 JSX に存在せず、使うと**ビルドがクラッシュする＝BANNED**。A は該当する絵を作らない（画面内の日付スタンプ意匠を作らない）。
- **R-DATE/era** — 1973–2026 のアメリカ。2010年の路上ビートにスマートフォン・現行世代の車を混ぜない。1973–78 ビートは当時の実験室・特許事務所の質感で。

## 1.3 機械ゲート（`build_fieldtest_asset_manifest.py --verify` の内部）

> **★★ R3（2026-07-29）BLOCKING 訂正。v001 の正規表現は、本書自身の 267本のプロンプトを 100% 落とす。** 実測した: 全プロンプトが `no readable text` で終わるので `readable` に必ず当たり、`no likeness` / `unreadable as a portrait` を含む行は `likeness` `portrait` にも当たる。**このまま実装すると `--verify` が全件 reject するか、実装者がゲートを緩めることになる（CLAUDE invariant 15 違反）。** 正しい形は「**許容フレーズを先に消してから禁止語を探す**」であり、以下が確定仕様である。

```python
# ① 先に「許容フレーズ」を消す。ここを消さずに ② を当ててはならない。
PERMITTED = re.compile(
    r"no readable text|no legible [a-z ]+|unreadable(?: smear| as a portrait)?|illegible|"
    r"no likeness|not a likeness of [^,]*|resembl\w+ no real individual|no visible face|"
    r"no identifiable face|no face|anonymized|anonymised|non-identifiable|silhouette|"
    r"back of head|hands only|out of focus face|generic unmarked uniform|"
    r"no insignia|no badge number|no precinct number|no agency seal|no department seal|"
    r"no drug use|no restraint|never near skin|no blood|no wound|no corpse|no violence",
    re.I)

# ② 残った文字列にだけ当てる。
BANNED_PORTRAIT = re.compile(
    r"albritton|mcclelland|acevedo|velasquez|richardson|barker|munier|chandler|"
    r"devon anderson|l\.?\s?j\.?\s?scott|likeness|portrait|mugshot|celebrity|deepfake",
    re.I)
BANNED_ACCURACY = re.compile(
    r"it was food|the crumb was food|food on a plate|breadcrumb on a plate|"
    r"needle in (a|the) (arm|skin|vein)|injecting|snorting|smoking (crack|cocaine)|"
    r"blood|wound|corpse|badge number|precinct number|agency seal|department seal|"
    r"texas ban|kits banned|effective date|readable|legible",
    re.I)

def scan(s: str) -> list[str]:
    """s = プロンプト本文 / tags / caption_hint / covers / subtype のいずれか1本。"""
    stripped = PERMITTED.sub(" ", s)
    hits = []
    if BANNED_PORTRAIT.search(stripped): hits.append("BANNED_PORTRAIT")
    if BANNED_ACCURACY.search(stripped): hits.append("BANNED_ACCURACY")
    return hits
```
> **検算（R3 実施済み）:** `scan()` を本書の 267本全部に通すと **hits = 0**。①を外すと **267/267 が hit する**。実装したら必ずこの2通りを走らせて、0 と 267 が出ることを確認してから本番に使うこと。
> **① の [HNEG]/[NEG] 側について:** ネガティブプロンプト（`Avoid:` 以降）は「作らせないものの列挙」なので、**scan の対象外**。`Avoid:` で split した**前半だけ**を渡す。
> 許容: `anonymized`, `non-identifiable`, `silhouette`, `back of head`, `hands only`, `out of focus face`, `unreadable smear`, `generic unmarked uniform`, `food debris perhaps (attributed)` — ただし最後のものはプロンプト本文では使わず、`caption_hint` にのみ書く。

---

# 2. 台本の語数と尺の確定値（Aが素材点数を積算する根拠）

```
narration words (measured, check_script_length PASS)     = 4,673   ★R3 更新（旧 4,750）
provisional wpm (★178.1 ではなく 172.0 — EP55/EP56 で
  実測 +71.2s / +71.8s のドリフトが2話連続で出たため)      = 172.0
narration provisional                                    = 1,630.1 s
designed gap budget (幕転換の息継ぎ・AEカード下の保持)      =   198.9 s  ★R3（旧 172.0）
endcard                                                  =     9.0 s
TOTAL provisional                                        = 1,838.0 s = 30:38  ★不変
picture (TOTAL - endcard)                                = 1,829.0 s          ★不変
durationInFrames                                         = 55,140             ★不変
speech ratio 1838.0/1630.1                               = 1.128  (1.04–1.30 内)
幕別語数: HOOK 114 / OPENING 50 / ACT1 582 / ACT2 667 /
          ACT3 774 / ACT4 1,014 / ACT5 1,105 / ENDING 367 = 4,673
```
> **★R3（2026-07-29・独立レビュー）:** 台本を事実訂正で 77語 削ったが、**TOTAL・picture・durationInFrames は動かしていない**（差分は gap budget に吸収）。したがって **§3 の点数・§3.3 の [1]〜[13] は1つも変わらない。A は従来どおりの本数で調達してよい。**
> ★TTS 実測後に B が `durationInFrames` を再ロックする（DESIGN §5 の手順）。**A の点数は「比」で決まるので再ロックの影響を受けない**（§3.3 の [2] と [8] だけ再導出）。

---

# 3. ★素材構成の確定値（この値で調達する・勝手に変えない）

## 3.1 内訳（★勝手に変えない・★四層ドクトリン適用済み）

| 層 | 種別 | distinct | cuts | **% of 563** | uses上限 | 調達 |
|---|---|---:|---:|---:|---:|---|
| **1** | **実写アーカイブ**（archive + factory 棚） | **252** | **252** | **44.8 %** | 1 | `search_archive.py` → `select_factory_assets.py` → 全点目視 |
| **2** | AE ヒーローカード 17枚 **= 100.5s**（★R3 訂正・旧「≈95s」） | — | *(overlay・cut に数えない)* | *(runtime の 5.5 %)* | — | B が合成 |
| **3** | Codex 静止画 body | **210** | **227** | **40.3 %** | 2 | SDXL 210本×1枚 |
| **4** | i2v モーション | **42** | **84** | **14.9 %** | 2 | 種42枚 → Wan 2.2 → RIFE |
| — | 合成レイヤー（distinct に数えない） | 30 | — | — | — | 在庫 |
| — | i2v 種画像（body には回さない） | 42 | 0 | — | — | SDXL 42本×1枚 |
| — | thumb_face | 3 | 0 | — | — | SDXL 3本×1枚 |
| — | F系 emotive face | 12 | *(採否は B)* | — | — | SDXL 12本×1枚 |
| | **合計 distinct** | **504** | **563** | **100 %** | | |

> **★R3 追記（四層予算のパーセンテージ・DESIGN §1.5 と一字一致）:** 252/563 = **44.76 %**、227/563 = **40.32 %**、84/563 = **14.92 %**、合計 **100 %**。**第一層（実写）が最大層である**という設計の核心が、この表だけで検算できるようにしてある。`archive share ≥ 40 % of cuts` はオーナー指示 2026-07-29 の機械フロア。

## 3.2 幕別配分（★still は確定・archive/i2v は目安。合計だけが確定）

| 幕 | still 枚 | S番号レンジ | ★HP | archive 本 | i2v 種 | thumb anchor |
|---|---:|---|---:|---:|---:|---|
| ACT0 HOOK+OPENING | 15 | S001–S015 | 4 | 14 | 3 | S001 / S006 |
| ACT1 THE CRUMB | 40 | S016–S055 | 16 | 46 | 8 | — |
| ACT2 THE FASTEST WAY OUT | 38 | S056–S093 | 18 | 44 | 8 | S072 |
| ACT3 WHAT IS IN THE VIAL | 34 | S094–S127 | 8 | 40 | 6 | — |
| ACT4 SIX MONTHS LATE | 46 | S128–S173 | 22 | 58 | 9 | S141 |
| ACT5 HOOD OF A PATROL CAR | 27 | S174–S200 | 13 | 38 | 6 | — |
| ENDING | 10 | S201–S210 | 4 | 12 | 2 | — |
| **計** | **210** | | **85** | **252** | **42** | 4 |

## 3.3 全体の検算（★Codex は自分で再計算して一致を確認）

```
[1] 総カット数 563 = archive 252 + still 227 + i2v 84
[2] 平均ショット長 = picture 1829.0 / 563 = 3.249 秒/カット        ✓ ≤7.0
[3] 静止画占有率(check_animation_mix) = 227/563 = 40.32%           ✓ ≤45%（余裕 4.68%pt）
[4] motion coverage = (252+84)/563 = 336/563 = 59.68%              ✓ ≥45%
[5] per-asset 上限: still 227/210=1.081(≤2) / archive 252/252=1.000(≤1) / motion 84/42=2.000(≤2)  ✓
[6] first-use share = 504/563 = 0.8952                              ✓ ≥0.70
[7] avg uses/source = 563/504 = 1.1171                              ✓ ≤1.4（EP49 は 1.8 で flag された）
[8] archive 下限 = picture 1829.0/30 = 60.97 → ≥61本。設計値 252本   ✓ ★R3訂正（旧「61.0→≥62」）
[9] ★HP 比率 = 85/210 = 40.48%                                      ✓ ≥40%（オーナー指示）
[10] 幕別 still 合計 = 15+40+38+34+46+27+10 = 210                    ✓
[11] 幕別 ★HP 合計 = 4+16+18+8+22+13+4 = 85                          ✓
[12] 幕別 archive 合計 = 14+46+44+40+58+38+12 = 252                  ✓
[13] 幕別 i2v 合計 = 3+8+8+6+9+6+2 = 42                              ✓
```
> **★ [3] の余裕は 4.68%pt。** still が210本を割ったら §6.3 の再生成で回復させ、**still-cut 227 を増やさない**（B側の shotlist が227で固定）。
> **★ TTS 再ロック後は [2] と [8] のみ再導出。[1][3][4][5][6][7][9]–[13] は点数の比なので不変。**

---

# 4. ★境界契約: asset_manifest.v001.json（AとBを繋ぐ唯一のファイル）

パス `episodes/PD-2026-057-fieldtest/05_visuals/asset_manifest.v001.json` · `schema_version: "fieldtest_assets.v1"` · `producer: "codex_thread_a"`。**B の validator と一字一致**であること。

## 4.1 スキーマ（fieldtest_assets.v1）

```jsonc
{
  "schema_version": "fieldtest_assets.v1",
  "episode_id": "PD-2026-057-fieldtest",
  "producer": "codex_thread_a",
  "generated_at": "<ISO8601 tz-aware>",
  "counts": { "stills_body": 210, "stills_i2v_source": 42, "stills_thumb_face": 3,
              "archive": 252, "motion": 42, "overlay": 30,
              "distinct": 504, "cuts": 563 },
  "stills": [ /* 255 entries: body 210 + i2v_source 42 + thumb_face 3 */ ],
  "factory": [ /* 252 entries — ★実写アーカイブ層。public_path 非空 */ ],
  "motion":  [ /* 42 entries */ ],
  "overlay": [ /* 30 entries */ ]
}
```

### 4.1a stills[] のエントリ形（body 例・★depth_path なし）

```jsonc
{
  "asset_id": "FDT-S001",                 // body: ^FDT-S\d{3}$（001..210）/ i2v種: ^FDT-MS\d{2}$ / thumb: ^FDT-T\d{2}$
  "scene_id": "S001",                     // §5.9 のプロンプト行に対応（S001..S210）
  "role": "body",                         // body|i2v_source|thumb_face|reject
  "also_thumb": false,                    // body から4枚だけ true（§4.3a・追加生成しない）
  "act": 0,                               // 0=HOOK/OPENING, 1..5=ACT I..V, 6=ENDING
  "path": "H:/pd-media/assets/ai/fieldtest/S001.png",
  "public_path": "fieldtest/img/S001.png",// role=="body" のみ非null / i2v種・thumb_face は null
  "width": 3840, "height": 2160,          // 長辺>=3840
  "sha256": "<64hex>", "phash": "<16hex>", "mean_luma": 23.0,
  "tags": ["white_crumb","dark_floormat","macro","symbolic","no_face","no_readable_text"],
  "caption_hint": "a small white crumb on a dark car floormat under a raking light, unidentified, no person, no readable text",
  "seed": 0, "model": "juggernautXL_ragnarokBy",
  "source": "ai_codex", "commercial_use": "allowed", "ai_disclosure_required": true,
  "qc": {"reviewed": true, "on_theme": true, "has_readable_text": false,
         "has_identifiable_real_person": false, "has_human_body": false,
         "has_identifiable_face": false, "has_drug_use_or_restraint": false,
         "has_identifiable_insignia": false, "notes": ""}
  // ★depth_path は無い（本作は depth treatment 不使用・§6.4）
  // ★reject トリガは has_readable_text / has_identifiable_real_person /
  //   has_drug_use_or_restraint / has_identifiable_insignia のみ。
  //   匿名人体（has_human_body:true）は reject しない。
}
```

## 4.2 --verify の不変条件（BLOCKING・B の validator と一字一致）

1. `counts` の全値が配列長と一致（stills 255 / factory 252 / motion 42 / overlay 30）。
2. `role=="body"` がちょうど 210、`i2v_source` 42、`thumb_face` 3。
3. `also_thumb==true` がちょうど 4、いずれも `role=="body"`。
4. `role=="body"` の `public_path` が非 null、それ以外は null。
5. `factory[].public_path` が全件非空・全件 `fieldtest/factory/` 配下・**全件が異なる**。
6. `motion[].public_path` が `.mp4` で終わり `_rife` を含む。
7. `asset_id` 正規表現が §4.1a どおりで、全件ユニーク。
8. `scene_id` が S001..S210 / MS01..MS42 / T01..T03 を過不足なく被覆。
9. `width`/`height` の長辺 ≥3840（thumb_face のみ 1280×720 を許容）。
10. `sha256` 全件ユニーク（同一画像の二重登録を弾く）。
11. `phash` の全ペア類似度 <0.90（§6.1 Q4）。
12. `qc.reviewed==true` が全件。
13. `qc.has_readable_text` が全件 false。
14. `qc.has_identifiable_real_person` が全件 false。
15. `qc.has_drug_use_or_restraint` が全件 false。
16. `qc.has_identifiable_insignia` が全件 false。
17. `factory[].license` が §7.4 の `ALLOWED_LICENSES` に含まれる（`review_required` は**不可**）。
18. `factory[].eyeballed_content` が全件非空（ラベル付きコンタクトシート審査の記録）。
19. `depth_path` キーがどのエントリにも存在しない。

## 4.3 role の割り当て（機械的に決める）

1. `S001`–`S210` → `role="body"`、`public_path` を `fieldtest/img/S<NNN>.png`。
2. `M01_src`–`M42_src` → `role="i2v_source"`、`scene_id="MS<NN>"`、`public_path=null`。
3. `T01_face`–`T03_face` → `role="thumb_face"`、`public_path=null`（staging 先は `fieldtest/thumb/`）。
4. QC で落ちたものは `role="reject"` にして `rejected/` へ退避し、同一プロンプト・別シードで1枚だけ再生成（§6.3）。
5. F系（F001–F012）は side lane。`stills[]` には入れない。採否は B が決める。

### 4.3a ★also_thumb 集合（ちょうど4枚・CODEX_B と一字一致必須）

- `FDT-S001`（暗いフロアマットの白い粒・マクロ／サムネ左下の物証）
- `FDT-S006`（ピンクから青へ変わる瞬間のアンプル・マクロ／サムネの主役）
- `FDT-S072`（法廷の演台を後ろから・匿名／人の存在を1点だけ入れる）
- `FDT-S141`（研究所の天秤の皿の上の白い粒／「ひとつまみの塩」）

## 4.4 ★archive[] 252エントリの作り方（★ファイル名を先に決めない・全点目視の後に確定する）

**⚠⚠ 本作は EP55 と違い、252行の `public_path` を本書に先に書かない。理由は測定済みの事実：棚のテーマフォルダは約40%が誤ラベルで、フォルダ名から選ぶと必ず場違いな素材が混入する（オーナー指示 2026-07-29 / §7.5）。** 先に名前を決めると「名前があるからそれで良い」ことになり、目視審査が形骸化する。

代わりに **A は §7.3 のクエリ表を実行し、ラベル付きコンタクトシートを審査し、通ったものだけを252行として書き出す。** 出力時の命名規則:

```
fieldtest/factory/AR<NNN>_<subtype_slug>.<ext>     （AR001 … AR252）
```
> **★命名に `F` を使わない（EP55 は `F001_…` だった）。** 理由: `check_prompt_diversity.py` の coverage ゲートは本文全体を `\b[SMTF]\d{2,3}\b` で走査するため、`F013`〜`F252` という文字列があると「literal プロンプトの無い参照ID」として数えられ、**カバレッジが機械的に落ちる**。`AR` 接頭辞はこの衝突を避ける。`check_asset_reuse.kind_of()` はパスに `/factory` が含まれるかで判定するので、ディレクトリ名を `factory` のままにすれば分類は従来どおり動く。

エントリ形（1行1オブジェクト）:
```jsonc
{ "asset_id":"FDT-AR001", "public_path":"fieldtest/factory/AR001_parking_lot_night_aerial.mp4",
  "path":"H:/pd-media/assets/factory/backgrounds/AF-BG-14767__police_station_at_night.mp4",
  "act":0, "covers_scene_id":"S008", "subtype":"parking_lot_night_aerial",
  "source":"pexels", "license":"free_commercial", "sha256":"<64hex>",
  "duration_sec":0.0, "width":0, "height":0, "mean_luma":0.0,
  "eyeballed_content":"aerial night view of an illuminated parking lot; no faces, no plates, no insignia",
  "origin":"archive_ledger", "qc":{"reviewed":true,"on_theme":true,"notes":""} }
```

**幕別の本数（§3.2 と一致・合計252）:** ACT0 14 · ACT1 46 · ACT2 44 · ACT3 40 · ACT4 58 · ACT5 38 · ENDING 12。

## 4.5 ★motion[] 全42エントリ

```jsonc
{ "asset_id":"FDT-M01", "source_scene_id":"MS01", "source_still":"H:/pd-media/assets/ai/fieldtest/M01_src.png", "path":"H:/pd-media/assets/ai_video/fieldtest/M01_rife.mp4", "public_path":"fieldtest/motion/M01_rife.mp4", "act":0, "storyboard":"hook", "tags":["pouch_torn_open"] }
{ "asset_id":"FDT-M02", "source_scene_id":"MS02", "source_still":"H:/pd-media/assets/ai/fieldtest/M02_src.png", "path":"H:/pd-media/assets/ai_video/fieldtest/M02_rife.mp4", "public_path":"fieldtest/motion/M02_rife.mp4", "act":0, "storyboard":"hook", "tags":["liquid_turning_blue"] }
{ "asset_id":"FDT-M42", "source_scene_id":"MS42", "source_still":"H:/pd-media/assets/ai/fieldtest/M42_src.png", "path":"H:/pd-media/assets/ai_video/fieldtest/M42_rife.mp4", "public_path":"fieldtest/motion/M42_rife.mp4", "act":6, "storyboard":"ending", "tags":["unopened_pouch_on_car_seat"] }
```
**残り39件も同型で書き出す。** 幕別内数: ACT0 = M01–M03 · ACT1 = M04–M11 · ACT2 = M12–M19 · ACT3 = M20–M25 · ACT4 = M26–M34 · ACT5 = M35–M40 · ENDING = M41–M42。**検算 3+8+8+6+9+6+2 = 42 ✓**
**人物種（H001–H018 のラベルが割り当たる18本）** = M04 M06 M07 M09 · M12 M14 M15 M17 M18 · M22 · M27 M29 M30 M32 M33 · M35 M37 M39。**検算 4+5+1+5+3 = 18 ✓**

## 4.6 overlay[] 30エントリ（distinct 素材に数えない・15 particle / 10 light / 5 vfx）

```jsonc
{ "public_path":"fieldtest/overlay/P01_rain_on_asphalt_fine.mp4", "type":"particle_assets", "subtype":"rain_on_asphalt_fine", "blend_hint":"screen" }
{ "public_path":"fieldtest/overlay/L01_sodium_lamp_haze_shaft.mp4", "type":"light_assets", "subtype":"sodium_lamp_haze_shaft", "blend_hint":"screen" }
{ "public_path":"fieldtest/overlay/V01_film_grain_fine.mp4", "type":"vfx_overlays", "subtype":"film_grain_fine", "blend_hint":"overlay" }
```
命名 `P01..P15` / `L01..L10` / `V01..V05`。**色レーン制限: light は sodium orange と fluorescent green-white のみ。cobalt blue の light overlay を作らない**（青は必ず「液体」であって「光」ではない — 一度でも青い光を撒くと SIGNATURE A の意味が壊れる）。overlay は `cuts[].src` に出さない。

---

# 5. A-1: SDXL 静止画のバッチ生成（210本 × 1枚・バリエーション0）— ★motif ライブラリ方式

## 5.1 生成環境
`generate_sdxl_4k.py` をそのまま使う。model `juggernautXL_ragnarokBy`、2段（base → hires）、出力 `H:\pd-media\assets\ai\fieldtest\`、プロンプト源は本書 §5.6 を `04_scenes/ai_prompts.v001.md` へ転記したもの。

## 5.2 ★210本の作り方＝「motif ライブラリ」テンプレート方式
幕ごとに motif ブロックを置き、各ブロックに **枚数** と **S番号レンジ** と **literal プロンプト** を書く。**2レーン**に分かれる: object/symbolic レーン（`[STYLE]`/`[NEG]`・125枚）と ★human-present レーン（`[HSTYLE]`/`[HNEG]`・85枚）。**HARD BAN: レーンを跨いだスタイルトークンの混用**（object 行に `[HSTYLE]` を付けない）。

## 5.3 共通スタイル [STYLE]（DESIGN §1 と一字一致）

```
, cinematic still, somber documentary grade, sodium-vapor orange as the one recurring night note and flat green-tinged institutional fluorescent as the one recurring day note, near-black ink gravity, a small glass ampoule of liquid as the film's dread object shown only as an object and never touching a person, the liquid reading pink for nothing-has-happened and a single deep cobalt blue reserved for the moment a two-dollar reagent has decided something, paper rendered with all type blurred into an unreadable smear, one warm late-paper amber note reserved only for the examination sheet, the form letter and the statute page, restrained dignified symbolism, telephoto compression and frontal composition, shallow depth of field, low-key deep-shadow lighting, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, no insignia, symbolic still-life, no visible face, no drug use, no restraint, no violence, empty rooms as aftermath, objects and shadows only
```
> **★過去話の色語 BAN（EP39–EP56 と混ざらないこと）:** `electric blue`（EP36）・`steel-cyan`（EP32）・`evidence-blue bandana`（EP54）・`sodium prison gold`（EP41）・`porch amber`（EP43）・`teal-green hospital`・`crimson kitchen`（EP45）・`forest-green`・`civil-violet`・`somber-plum`・`interrogation fluorescent green-gray`（EP55）・`post-office signage red`／`phantom-ledger phosphor green`（EP56）。**EP57 の色は `false-positive cobalt blue #2A57C4` ＋ `reagent pink #E0708C` ＋ 環境の sodium/fluorescent ＋ 末端のみ `late-paper amber #E8D6A8`。**

## 5.4 共通ネガティブ [NEG]（各 Avoid: の後に全文付ける・A/B 同一）

```
text, words, letters, numbers, captions, watermark, logo, badge number, precinct number, agency seal, department seal, unit patch, shoulder flash, vehicle door lettering, readable document, legible report, legible letter, legible court record, legible examination sheet, legible patent drawing, legible statute, legible date, license plate, real celebrity, recognizable real person, identifiable face, portrait, mugshot, likeness of a specific person, Amy Albritton, Charles McClelland, needle in an arm, needle in skin, injecting, snorting, smoking crack, drug use, drug paraphernalia in use, pills spilled as spectacle, blood, wound, injury, corpse, handcuffed person in distress, cowering figure, screaming face, crying face, child, food on a plate, dinner table, bread roll, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, steel-cyan, sodium prison gold, porch amber, crimson kitchen, teal-green hospital, forest-green, civil-violet, somber-plum, interrogation fluorescent green-gray, post-office signage red, phantom-ledger phosphor green, milky haze, foggy wash, scanline, CRT texture, vignette wash
```

## 5.5 プロンプトの絶対ルール（210本すべてに適用）

1. **レーンを守る** — object 行は `[STYLE] Avoid: [NEG]`、★HP 行は `[HSTYLE] Avoid: [HNEG]` で終わる。
2. **読める文字を作らない** — 書類は必ず `unreadable smear` と明記する。
3. **薬物使用・拘束・受傷を描かない** — 注射針は「ピントの外の物体」まで。
4. **R-OFFICER** — 制服は無地、標章なし、顔なし。威圧構図を作らない。
5. **R-NOT-A-DRUG** — 塊は常に「正体不明の白い粒」。食品として提示しない。
6. **色の体系を守る** — 青は液体の中だけ。ピンクは液体と figures だけ。amber は3ビートだけ。
7. **時代考証** — 2010年の路上にスマホを出さない。1973–78 は当時の質感。
8. **treatment** — `depth` を前提にした絵を作らない（§6.4）。

## 5.5a ★反復禁止ルール（BINDING・本作は誕生時から適用）

1. **1ビート内は同一 motif のバリエーション最大2枚。** 3枚目が欲しくなったら、そのビートのナレーション（script.en の該当段落）に合致する**別の distinct シーン**へ転換する。
2. **幕をまたぐ motif の再登場は「目に見える状態変化」必須。同状態の撮り直しは禁止。** spine motif の状態連鎖（各状態1–2枚まで・状態語を各プロンプト本文に内蔵済み）:
   - **vial** = sealed in a dark trunk(S002) → open and pink in a gloved hand(S004) → **turning blue**(S005–S006) → held at eye level, blue(S007) → discarded blue in a roadside bin at dawn(S060) → **a wall of identical unopened pouches on a supply shelf**(S112) → one vial beside a bench instrument under laboratory white(S133) → **an unopened pouch on a patrol-car seat, present day**(S208)。**この8状態以外の vial 行を作らない。**
   - **paper** = a blank examination sheet on a bench(S138) → the same sheet face-down in a filing tray(S147) → a form letter on a sorting belt(S162) → **the envelope uncollected in an outdoor mailbox bank**(S165) → a bound statute page under a signing pen(S196)。**この5状態のみ。**
   - **the two weights** = a hand-written figure on a form at a car hood(S013) → a digital laboratory balance reading(S140–S141)。**2状態のみ。**
   - **empty passenger seat** = door open at night(S010) → the same seat empty in daylight, impound(S055) → a different car's seat, present day(S207)。**3状態のみ。**
3. **Codex one-shot 原則:** 各行1枚・一発で決める。再生成は §6 の QC fail 時のみ（同一プロンプト・別シード1枚・§6.3）。**「複数枚から選ぶ」ためのバリエーション生成は禁止**（variants 0・§5.10 と同義）。
4. **DRUG/OFFICER GATE 不変:** 上記の再構成で §1.1-2 / §1.2 R-OFFICER / R-NO-DRUG-DEPICTION を1文字も緩めない。

## 5.6 ★motif ライブラリ（幕別・distinct 数確定・S番号レンジ・全210本の literal プロンプト）

> **★HP anti-samey 変化マトリクス（85枚全体に適用）:**
> - **軸を必ず散らす:** 距離（hands macro／medium／wide／far-wide）×角度（背後正対／後方斜め／low angle／over-the-shoulder）×年代 wardrobe（1970s／1980s／2000s／2010s／2020s）×光（sodium night／institutional fluorescent／north-window laboratory white／overcast daylight／late-paper amber）×setting（roadside／car interior／booking corridor／courtroom／records room／laboratory／convenience store／bar／stairwell／mailbox bank／capitol chamber／supply room）×人数（solo／2–3人／列／小群衆）×姿勢（座って待つ／立つ／歩く／手元作業／書く／運ぶ）。
> - **HARD: どの2枚の ★HP も「被写体タイプ＋構図＋光」の3要素同時一致を禁止。** 85行を書き終えたら軸表で自己監査してから生成に入る。
> - **クラスタは §6.1 Q4 phash watch-list に反映済み。同状態ペアが phash で衝突したら「削る」でなく §5.5a のルールで作り直す。**

### ACT 0 — HOOK + OPENING（15枚・S001–S015・★HP 4）

- **crumb_and_pouch — 6 — S001–S006**（cold open の物証連鎖・vial 状態1–3）
```
- `S001.png`
Extreme macro of a single small white crumb lying on the dark ribbed rubber floormat of a car at night, raking light from outside the open door picking out its rough edges, unidentified and utterly ordinary, no person, no readable text [STYLE] Avoid: [NEG]
- `S002.png`
A small sealed plastic pouch containing a glass ampoule lying among jumper cables and a folded blanket in the dark trunk of a sedan, lit only by a weak boot lamp, sealed and waiting, no person, no readable text [STYLE] Avoid: [NEG]
- `S003.png`
Close macro of the foil corner of a plastic test pouch being torn open, the serrated edge peeling back, sodium street light behind it dissolving into orange bokeh, no person visible beyond the tear itself, no readable text [STYLE] Avoid: [NEG]
- `S004.png`
Macro of a slim glass ampoule of clear pink liquid standing upright inside its opened plastic sleeve on a car roof, the pink reading calm and inert, condensation on the paint around it, no person, no readable text [STYLE] Avoid: [NEG]
- `S005.png`
Ultra macro of a crumb falling into pink liquid inside a narrow glass tube, the surface tension dimpling around it, the fluid still entirely pink and undecided, shallow focus, no person, no readable text [STYLE] Avoid: [NEG]
- `S006.png`
Ultra macro of pink liquid in a narrow glass tube blooming into a deep cobalt blue from the bottom upward, a soft plume of colour spreading through the fluid, the single most saturated frame in the film, no person, no readable text [STYLE] Avoid: [NEG]
```
- **roadside_night — 5 — S007–S011**（★HP 2・停止現場の環境）
```
- `S007.png`
A gloved hand raised at eye level holding a small glass tube of deep blue liquid, the hand cropped at the wrist and the sleeve deliberately plain with no marking of any kind, orange streetlight flaring behind, the gesture of a verdict, no face, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
- `S008.png`
Wide night view across an empty American strip-mall parking lot, painted bays glossy with recent rain, shuttered storefront awnings along the far edge, two tall lamp standards burning orange, no cars in the foreground, no person, no readable text [STYLE] Avoid: [NEG]
- `S009.png`
A bar of alternating red and blue emergency light sweeping across the open passenger door of a pale sedan at night, the beam catching the rubber weatherstrip and the door card, the vehicle itself unmarked and generic, no person, no readable text [STYLE] Avoid: [NEG]
- `S010.png`
A woman seen only as a dark silhouette seated motionless in a car passenger seat at night, shoulders squared, head turned toward the open door, dome light behind her so nothing of her face reads, an ordinary handbag on her lap, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S011.png`
A distant Houston skyline at night compressed by a long lens, freeway light trails smeared across the foreground overpass, humid haze softening the towers, an enormous indifferent city, no person, no readable text [STYLE] Avoid: [NEG]
```
- **first_paper_and_custody — 4 — S012–S015**（★HP 2・書類と拘束の抽象化）
```
- `S012.png`
A clipboard resting on the warm hood of a sedan at night, a ballpoint pen laid across a printed form whose every line of type is blurred into an unreadable smear, orange lamp light raking across the paper, no person, no readable text [STYLE] Avoid: [NEG]
- `S013.png`
Close on a pair of anonymous hands filling a short handwritten figure into a box on a printed form laid on a car hood, only the cuff and the fingers in frame, the writing itself an illegible scrawl, orange night light, no face, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
- `S014.png`
The rear side window of a plain sedan photographed from outside at night, a steel mesh divider visible beyond the glass, orange lamplight sliding down the wet pane, the interior in near darkness, no person, no readable text [STYLE] Avoid: [NEG]
- `S015.png`
A woman's shape walking away from camera along an outdoor apartment-complex walkway at night, keys in one hand, a bank of metal mailboxes glowing under a single bulb ahead of her, back turned, no face, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 1 — THE CRUMB（40枚・S016–S055・★HP 16）

- **her_working_world — 9 — S016–S024**（★HP 5・住居＝仕事だった世界）
```
- `S016.png`
A two-storey red-brick apartment complex in a small Louisiana town photographed in flat overcast morning light, exterior stairwells, window air-conditioning units, a mown strip of grass, entirely ordinary and well kept, no person, no readable text [STYLE] Avoid: [NEG]
- `S017.png`
A woman seen from behind over her own shoulder at the counter of a cluttered on-site letting office, a ring binder open in front of her and a wall board of numbered key fobs beyond, a desk fan turning and a half-drunk coffee at her elbow, morning light striped across her back through vertical blinds, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S018.png`
A woman's hands sorting a fan of brass apartment keys on a counter, sleeves pushed to the elbow, a spiral notebook open beside them, warm daylight from a window out of frame, hands only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S019.png`
A vacant ground-floor apartment interior mid-turnover, bare beige carpet with vacuum tracks, a stepladder folded against the wall, a paint tin on a dust sheet, light flooding through an uncurtained sliding door, no person, no readable text [STYLE] Avoid: [NEG]
- `S020.png`
A woman in a plain polo shirt seen from behind carrying a plastic caddy of cleaning bottles up an outdoor concrete stairwell, shoulders working, midday shadow hard on the risers, back turned, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S021.png`
A domestic living room in the on-site manager's apartment: a worn sofa with a folded throw, a child's game controller on the arm, a wheelchair-accessible doorway widened at the frame, late afternoon sun in bands across the floor, no person, no readable text [STYLE] Avoid: [NEG]
- `S022.png`
A woman's silhouette standing at a kitchen sink in a modest apartment at dusk, one hand resting on the edge of the counter, dishes stacked on the drainer, the window beyond her already dark, back three-quarters, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S023.png`
A small-town Louisiana main street in humid late-summer light, a hardware store awning, angled parking, a pharmacy sign shape with its lettering deliberately illegible, heat shimmer above the asphalt, no person, no readable text [STYLE] Avoid: [NEG]
- `S024.png`
An adult and a teenager seen from behind as two shapes on a sofa in a dim living room, television glow washing over the backs of their heads, an ordinary evening, neither face visible, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_drive — 7 — S025–S031**（★HP 3・移動）
```
- `S025.png`
An interstate highway seen through a windscreen at speed in the late afternoon, oncoming pale-gold light, a chip in the glass catching the sun, wiper streaks fanning across the view, no person, no readable text [STYLE] Avoid: [NEG]
- `S026.png`
A woman's hands resting loosely in her lap in a car passenger seat, seatbelt diagonal across a plain blouse, the door card and window crank beside her, afternoon light moving across her knees, cropped below the shoulders, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S027.png`
The dashboard of an ageing full-size American sedan photographed from the passenger side, an analogue instrument cluster with unreadable dials, a cassette-era radio fascia, a cracked vinyl top, no person, no readable text [STYLE] Avoid: [NEG]
- `S028.png`
A driver's hands on a worn steering wheel at ten and two, forearms tanned, the windscreen ahead filled with flat Texan sky, hands only and no shoulder or head in frame, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S029.png`
A wing mirror filling the frame, reflecting an empty stretch of freeway behind and a low sun, the mirror housing scuffed, the road beyond compressed by a long lens, no person, no readable text [STYLE] Avoid: [NEG]
- `S030.png`
A row of interchangeable roadside businesses along a Texas arterial in the last hour of daylight, a tyre shop, a taqueria awning, a laundromat, all signage reduced to illegible shapes, power lines cutting the sky, no person, no readable text [STYLE] Avoid: [NEG]
- `S031.png`
A woman's shape reflected faintly in a passenger window against the blur of passing storefronts, the reflection broken and doubled by the glass, unreadable as a portrait, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_stop — 8 — S032–S039**（★HP 3・停止と接触）
```
- `S032.png`
A single indicator lamp on the rear quarter of a pale sedan blinking amber at dusk, the paint dulled and the trim pitted, shot tight so the vehicle remains anonymous, no person, no readable text [STYLE] Avoid: [NEG]
- `S033.png`
A plain patrol-style vehicle stopped behind a civilian car on the shoulder, seen from far behind through heat haze, both vehicles reduced to dark shapes under a wide dusk sky, all markings and lettering absent, no person, no readable text [STYLE] Avoid: [NEG]
- `S034.png`
An open driver's door of a sedan with the interior dome light on, seen from outside at dusk, the seat empty, the key still in the column, a jacket left folded on the console, no person, no readable text [STYLE] Avoid: [NEG]
- `S035.png`
A pair of dark uniform trouser legs and duty boots standing on wet asphalt beside a car sill, framed from the knee down, the fabric deliberately plain with no stripe or marking, orange lamplight pooling around the boots, no face, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
- `S036.png`
The interior headliner of a car photographed from below, a corner of the fabric sagging away from the roof panel, shadow in the cavity behind it, an ordinary decade of wear, no person, no readable text [STYLE] Avoid: [NEG]
- `S037.png`
A gloved hand sweeping a flashlight beam low across a car footwell, the beam catching dust and grit in the carpet pile, the glove plain black nitrile, wrist only, no face, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
- `S038.png`
A woman standing at the kerb with her back to camera and her arms folded, seen past the rear wing of her own car, the tail light throwing red across her sleeve, waiting without motion, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S039.png`
A car's glove compartment hanging open with an owner's manual, a tyre gauge and a wad of paper napkins spilling toward the footwell, torch light from outside grazing the contents, no person, no readable text [STYLE] Avoid: [NEG]
```
- **what_the_search_found — 7 — S040–S046**（★HP 1・対象物 3点の抽象化）
```
- `S040.png`
A small unbranded paper sachet of headache powder lying creased on a car seat, the printing on it reduced to an unreadable blur, a corner already torn and re-folded, ordinary drugstore ephemera, no person, no readable text [STYLE] Avoid: [NEG]
- `S041.png`
A disposable syringe lying capped and thrown badly out of focus in the deep background of a dark car footwell, present only as a soft grey shape, never a subject, never near skin, no person, no readable text [STYLE] Avoid: [NEG]
- `S042.png`
A wide low-angle view along a car floor at night, the seat rails and the carpet grain running away from the lens, a single pale speck sitting in the middle distance, everything else in shadow, no person, no readable text [STYLE] Avoid: [NEG]
- `S043.png`
A gloved fingertip and a folded paper card lifting a pale speck from carpet pile, macro, the card's printed side turned away, the movement precise and clinical, fingers only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S044.png`
A transparent evidence sleeve lying flat on a car boot lid with a single pale fragment inside it, the printed panel of the sleeve blurred to illegibility, night air condensing on the plastic, no person, no readable text [STYLE] Avoid: [NEG]
- `S045.png`
Macro of a printed colour comparison strip on a test pouch, a graded band running from pale pink through violet to deep blue, the reference legend deliberately unreadable, the whole apparatus of proof in one printed strip, no person, no readable text [STYLE] Avoid: [NEG]
- `S046.png`
A discarded pouch wrapper and a snapped glass tip lying together on wet asphalt beside a kerb, orange lamplight reflected in the puddle around them, the aftermath of a ninety-second procedure, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_verdict_moment — 9 — S047–S055**（★HP 4・青が決めた後）
```
- `S047.png`
A wide shot of a parking lot at night from a raised angle, two vehicles small in the frame and the vast empty asphalt around them, one pool of orange light containing everything that mattered, no person, no readable text [STYLE] Avoid: [NEG]
- `S048.png`
A woman's wrists held together low behind her back, framed tightly from the mid-forearm down so that no restraint hardware, no injury and no distress is visible, sleeves plain, orange light on skin, dignified and still, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S049.png`
The open rear door of a plain sedan with a moulded bench seat inside, seen from the kerb, a dark cavity waiting, the vehicle stripped of all markings, no person, no readable text [STYLE] Avoid: [NEG]
- `S050.png`
A woman's shape seated behind a mesh partition seen from outside through a rear window at night, reduced to a dark outline against the far window, streetlight sliding across the glass between camera and subject, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S051.png`
A tow hook and chain being made fast to the front subframe of a sedan on a night street, macro on the steel and the paint chips, the recovery truck beyond it out of focus, no person, no readable text [STYLE] Avoid: [NEG]
- `S052.png`
Two dark uniformed shapes standing several paces apart on an empty lot conferring, seen from a great distance with a long lens so both are unidentifiable smudges under a lamp standard, no faces, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
- `S053.png`
A woman's handbag left open on a car seat with a purse, a phone of the correct 2010 era face-down and a folded receipt spilling out, the personal contents of an interrupted afternoon, no person, no readable text [STYLE] Avoid: [NEG]
- `S054.png`
A pair of hands signing a property receipt on a metal counter under hard overhead light, the pen mid-stroke, the form's type an unreadable smear, wrists and cuffs only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S055.png`
The same passenger seat photographed empty in flat daylight inside a fenced impound yard, dust settled on the vinyl, the door standing open on nothing, no person, no readable text [STYLE] Avoid: [NEG]
```

### ACT 2 — THE FASTEST WAY OUT（38枚・S056–S093・★HP 18）

- **booking_night — 8 — S056–S063**（★HP 3・vial 状態4を含む）
```
- `S056.png`
A long county booking corridor at night lit by unshaded fluorescent tubes, painted cinder-block walls, a bench bolted to one side, the far end dissolving into glare, empty, no person, no readable text [STYLE] Avoid: [NEG]
- `S057.png`
A woman sitting alone on a bolted steel bench at the end of a fluorescent corridor, seen from far behind, small in the frame, hands in her lap, an entire institution around one person, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S058.png`
A wall-mounted clock in an institutional corridor reading somewhere in the small hours, its numerals deliberately blurred beyond reading, the second hand caught mid-sweep, fluorescent light flattening the plastic, no person, no readable text [STYLE] Avoid: [NEG]
- `S059.png`
A grey painted steel door closed flush in a tiled institutional wall, a plain handle and no window, harsh overhead light and no shadow anywhere, the whole beat carried by a shut door and nothing else, no person, no readable text [STYLE] Avoid: [NEG]
- `S060.png`
A discarded plastic pouch with a snapped ampoule of blue liquid inside, lying among grit at the bottom of a roadside litter bin photographed at dawn, the blue already dulled and irrelevant, no person, no readable text [STYLE] Avoid: [NEG]
- `S061.png`
A woman's hands holding a paper cup of water in a holding area, knuckles pale, the cup's rim slightly crushed, hard overhead light, hands and forearms only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S062.png`
A row of narrow personal-effects lockers with numbered doors in an intake area, the numbers blurred to unreadable shapes, one door hanging open on an empty compartment, no person, no readable text [STYLE] Avoid: [NEG]
- `S063.png`
Several seated figures spaced along a wall bench in a night intake area, all seen from behind as dark shoulder shapes against pale tile, none identifiable, an ordinary queue of an ordinary night, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_lawyer_and_the_offer — 8 — S064–S071**（★HP 5）
```
- `S064.png`
A courthouse corridor in the early morning, terrazzo floor, wooden benches along one wall, tall sash windows throwing long parallelograms of light, entirely empty before the day begins, no person, no readable text [STYLE] Avoid: [NEG]
- `S065.png`
A man's hands resting on a thin manila case file balanced on his knee in a corridor, one thumb holding the folder shut, a wristwatch at the cuff, the tab label an unreadable smear, hands only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S066.png`
A clerk's shape pushing a trolley stacked with dozens of identical thin case folders along a corridor wall, seen from a low angle from behind so only the back and the working forearms read, each spine bearing an illegible label, the stack taller than the trolley rail, an ordinary morning's caseload, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S067.png`
Two figures standing close together in a corridor alcove, one leaning in to speak, both seen from behind and slightly below so neither face is visible, midday window light behind them, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S068.png`
A wall-mounted bail schedule board in a courthouse hallway, its printed rows reduced entirely to unreadable grey ruling, a scuff of hands at the lower edge, cold fluorescent overhead, no person, no readable text [STYLE] Avoid: [NEG]
- `S069.png`
A woman standing very still in a corridor with her back to camera, facing a closed set of double doors, one hand gripping the opposite elbow, the corridor stretching away behind her, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S070.png`
A payphone alcove in an older county building, the handset resting off its cradle on the shelf, a coiled steel cord, laminate walls scarred by decades of use, no person, no readable text [STYLE] Avoid: [NEG]
- `S071.png`
A woman's hands accepting a ballpoint pen held out by another pair of hands over a plain counter, the exchange caught mid-air, both faces out of frame entirely, hard overhead light, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_plea — 9 — S072–S080**（★HP 4・法廷・also_thumb S072）
```
- `S072.png`
A lectern in an American courtroom photographed from directly behind a single standing figure, the figure a dark shape occupying the lower third, the bench beyond in soft focus, all seals and lettering absent from the woodwork, no face, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
- `S073.png`
An empty American courtroom photographed from the back row, wooden pews receding, a raised bench at the far end, high windows throwing dusty light down the aisle, all heraldry and lettering removed, no person, no readable text [STYLE] Avoid: [NEG]
- `S074.png`
A close view of the polished top rail of a courtroom bar, a shallow shelf worn smooth by decades of hands, one deep gouge in the varnish, shallow focus running off into the room, no person, no readable text [STYLE] Avoid: [NEG]
- `S075.png`
A woman's hands flat on a lectern shelf, fingers spread, a folded tissue crumpled beside them, sleeve cuffs plain, cool courtroom light from above, hands only and no face anywhere in frame, no readable text [HSTYLE] Avoid: [HNEG]
- `S076.png`
A typed plea form lying on a table with a signature line at the foot, every line of type dissolved into an unreadable smear, a pen resting diagonally across it, cool north light, no person, no readable text [STYLE] Avoid: [NEG]
- `S077.png`
A court reporter's stenotype machine on its tripod stand in an otherwise empty courtroom, keys catching a hard sidelight, the paper tape feeding blankly into the tray, no person, no readable text [STYLE] Avoid: [NEG]
- `S078.png`
The dark shape of a seated figure in a robe on a raised bench, backlit by a high window so nothing but an outline reads, the bench face plain and unmarked, seen from the well of the court, no likeness, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
- `S079.png`
A wooden gallery pew photographed empty from the side, hymn-board-shaped notice frame on the wall behind it holding nothing, afternoon light sliding along the seat, no person, no readable text [STYLE] Avoid: [NEG]
- `S080.png`
A woman's shape walking away down the centre aisle of a courtroom toward a set of doors, seen from behind at some distance, a bailiff-shaped figure standing motionless to one side, neither identifiable, no readable text [HSTYLE] Avoid: [HNEG]
```
- **twenty_one_days — 6 — S081–S086**（★HP 4・服役の抽象化）
```
- `S081.png`
A narrow institutional dormitory corridor with painted breeze-block walls and a strip of skylight, bunk frames visible through an open doorway, everything scrubbed and colourless, empty, no person, no readable text [STYLE] Avoid: [NEG]
- `S082.png`
A stack of folded county-issue clothing and a pair of canvas slip-on shoes on a bare mattress, the fabric bleached by industrial laundering, hard overhead light, no person, no readable text [STYLE] Avoid: [NEG]
- `S083.png`
A woman's shape standing at a narrow reinforced window looking out at a car park, seen from behind and slightly to one side, daylight flattening her into a silhouette, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S084.png`
A woman's hand drawing a biro through one more square on a wall calendar page in an institutional day room, the grid of dates deliberately unreadable, two squares already scored through, the paper curling at one corner, flat day-room light, hand and cuff only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S085.png`
Several figures queueing along a painted line on a polished floor, seen from behind as a receding row of shoulders under identical overhead lights, none identifiable, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S086.png`
A woman's hands returning a plastic property tray across a counter, a wristwatch and a purse inside it, the counter's laminate worn through to chipboard at the edge, hands only, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **what_was_waiting — 7 — S087–S093**（★HP 2・出所後の喪失）
```
- `S087.png`
A pile of household furniture stacked at a kerb outside an apartment block in flat daylight, a sofa on its end, a lamp with a bent shade, cardboard boxes going soft in the damp, no person, no readable text [STYLE] Avoid: [NEG]
- `S088.png`
A door lock cylinder being changed on an apartment door, macro on the fresh brass barrel against weathered paint, the old cylinder lying on the threshold, no person, no readable text [STYLE] Avoid: [NEG]
- `S089.png`
A woman standing at the foot of an outdoor apartment stairwell looking up at a first-floor door, seen from behind, a single plastic bag of belongings by her feet, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S090.png`
A dew-soaked cardboard box of kitchenware left on grass beside a kerb, a colander and a stack of mismatched plates visible at the top, morning light, no person, no readable text [STYLE] Avoid: [NEG]
- `S091.png`
A greyhound-style intercity bus station waiting hall in the small hours, moulded plastic seats in rows, a vending machine glowing at the far wall, one bag on a seat, no person, no readable text [STYLE] Avoid: [NEG]
- `S092.png`
A woman's shape asleep sitting upright in a waiting-hall chair, jacket pulled around her, seen from a distance and from behind, the terminal lights hard and unforgiving, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S093.png`
A rental application form on a kitchen table with a background-check consent box at the bottom, all wording blurred to an unreadable smear, a pen resting unused beside it, overcast daylight, no person, no readable text [STYLE] Avoid: [NEG]
```

### ACT 3 — WHAT IS ACTUALLY IN THE VIAL（34枚・S094–S127・★HP 8）

- **the_1973_object — 8 — S094–S101**（★HP 2・特許と誕生）
```
- `S094.png`
A 1970s patent draughtsman's board with a technical drawing of a small sealed pouch and vial assembly, every annotation and dimension reduced to unreadable graphite scratching, an adjustable lamp raking across the paper, no person, no readable text [STYLE] Avoid: [NEG]
- `S095.png`
A mid-1970s American government laboratory bench with a rotary vacuum pump, a wooden reagent rack and a bakelite switch panel, tungsten light warming the enamel surfaces, period-correct and unpeopled, no person, no readable text [STYLE] Avoid: [NEG]
- `S096.png`
Macro of a hand-blown glass ampoule being sealed in a small flame, the neck drawing out into a thread, the flame reflected in the glass wall, a manufacturing detail from another era, no person, no readable text [STYLE] Avoid: [NEG]
- `S097.png`
A pair of hands in a 1970s lab coat cuff assembling a sealed pouch on a bench jig, the motion practised and repetitive, sleeves and hands only in frame, tungsten work light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S098.png`
A cardboard shipping carton of unmarked pouches with its flaps open on a stockroom floor, packing straw around the contents, a shipping label whose printing is an unreadable blur, no person, no readable text [STYLE] Avoid: [NEG]
- `S099.png`
The open glove box of a 1970s American patrol vehicle with a handful of sealed pouches wedged in beside a torch and a folded map, vinyl dashboard cracked by sun, no person, no readable text [STYLE] Avoid: [NEG]
- `S100.png`
A figure in a plain period uniform seen only from the shoulder blades down, standing at the open door of a vehicle in daylight with one pouch in hand, deliberately without any marking on the cloth, no face, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
- `S101.png`
A 1970s federal office corridor with pebbled glass doors and a terrazzo floor, an ashtray stand between two doorways, tungsten ceiling fittings, the architecture of a policy nobody will revisit, no person, no readable text [STYLE] Avoid: [NEG]
```
- **the_warnings_on_file — 6 — S102–S107**（1974/1978 の警告）
```
- `S102.png`
A bound government technical report lying closed on a metal shelf under fluorescent light, its cover printing dissolved into an unreadable smear, a decade of dust in the top edge of the pages, no person, no readable text [STYLE] Avoid: [NEG]
- `S103.png`
A drawer of buff suspension files pulled halfway open in a records room, tabs standing in a row with every label illegible, the drawer's runners worn bright, no person, no readable text [STYLE] Avoid: [NEG]
- `S104.png`
A microfiche reader glowing in a dim archive alcove, a blank illuminated screen and a carousel of film jackets beside it, no legible frame anywhere on the display, no person, no readable text [STYLE] Avoid: [NEG]
- `S105.png`
A wall of grey federal filing cabinets photographed head-on under flat ceiling light, every drawer identical and closed, one handle polished by use, no person, no readable text [STYLE] Avoid: [NEG]
- `S106.png`
A single typed page pinned to a corkboard among older curling notices, the type a soft unreadable grey, a rusted drawing pin at its corner, north light from a high window, no person, no readable text [STYLE] Avoid: [NEG]
- `S107.png`
A stack of departmental circulars slumped in an unemptied in-tray on a metal desk, the topmost sheet gone brittle and yellow, all wording blurred, afternoon light across the desk, no person, no readable text [STYLE] Avoid: [NEG]
```
- **why_the_colour_lies — 8 — S108–S115**（★HP 2・偽陽性の物たち・vial 状態6）
```
- `S108.png`
A macro row of five identical glass tubes on a white surface, each holding liquid at a slightly different stage between pink and cobalt blue, a graded sequence that proves nothing, cold even light, no person, no readable text [STYLE] Avoid: [NEG]
- `S109.png`
A tight still life of ordinary household cleaning bottles grouped on a kitchen counter, labels blurred into unreadable colour fields, morning light through a window blind, the mundane sources of a false positive, no person, no readable text [STYLE] Avoid: [NEG]
- `S110.png`
A bathroom cabinet shelf holding a blister strip, a tube of skin treatment and a small brown pharmacy bottle, all wording illegible, harsh mirror light bouncing off the tiles, no person, no readable text [STYLE] Avoid: [NEG]
- `S111.png`
A single square of dark chocolate on a white saucer beside a glass tube of blue liquid, the improbable pairing lit like a laboratory exhibit rather than a plate of food, cold overhead light, no person, no readable text [STYLE] Avoid: [NEG]
- `S112.png`
A deep supply-room shelf packed end to end with hundreds of identical sealed test pouches in stacked cardboard trays, receding into shadow, an industrial quantity of certainty, no person, no readable text [STYLE] Avoid: [NEG]
- `S113.png`
A pair of hands lifting a tray of sealed pouches from a supply shelf, forearms braced under the weight, storeroom fluorescents overhead, hands and sleeves only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S114.png`
A cheap moulded plastic training chair in a bare briefing room facing a blank wall-mounted screen, one folding table, the room set up for instruction nobody attended, no person, no readable text [STYLE] Avoid: [NEG]
- `S115.png`
Several seated figures seen from the back row of a fluorescent briefing room, shoulders and the backs of heads only, a blank projection rectangle on the far wall, none identifiable, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_chemist_and_his_choice — 7 — S116–S122**（★HP 2・三段→一段）
```
- `S116.png`
A private workshop bench with three glass reagent steps laid out in sequence on a felt mat, a small notebook of illegible calculations beside them, a single anglepoise lamp, no person, no readable text [STYLE] Avoid: [NEG]
- `S117.png`
Macro of two liquid layers separating cleanly in a test tube, a dense blue below and a clear pink above with a knife-sharp meniscus between them, backlit against black, no person, no readable text [STYLE] Avoid: [NEG]
- `S118.png`
The same workshop bench photographed after two of the three glass steps have been cleared away, only one tube left on the felt with two empty rings in the dust where the others stood, no person, no readable text [STYLE] Avoid: [NEG]
- `S119.png`
An older man's hands closing a hinged wooden sample case on a workshop bench, the fingers thick and careful, the catch half-turned, sleeves rolled, hands only and no face in frame, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S120.png`
A small independent manufacturing unit seen from the car park at dusk, a roller shutter half down, a single office window lit, a nondescript industrial building with all signage absent, no person, no readable text [STYLE] Avoid: [NEG]
- `S121.png`
A packing table with a heat sealer, a reel of clear film and a shallow bin of loose glass ampoules waiting to be sleeved, work light hard from above, no person, no readable text [STYLE] Avoid: [NEG]
- `S122.png`
A figure in a plain work coat seen from behind at the end of a small production line, one hand on a bench edge, the line's rollers running away toward a shuttered doorway, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_room_nobody_reaches — 5 — S123–S127**（★HP 2・不採用の法廷）
```
- `S123.png`
An empty jury box in an American courtroom photographed from the witness position, fourteen vacant chairs in two tiers, cold north light through a high window, the seats that were never filled, no person, no readable text [STYLE] Avoid: [NEG]
- `S124.png`
A witness stand with a small shelf, a brass microphone gooseneck and a carafe of water on a coaster, all lettering absent from the woodwork, seen empty from the jury side, no person, no readable text [STYLE] Avoid: [NEG]
- `S125.png`
A wheeled exhibit table in a courtroom well with nothing on it but a single numbered card whose figure is illegible, hard light from above, the emptiness deliberate, no person, no readable text [STYLE] Avoid: [NEG]
- `S126.png`
A figure in a plain suit standing alone in the well of an empty courtroom seen from the gallery, hands clasped behind the back, entirely anonymous at that distance, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S127.png`
Two figures seen from behind at a long table stacked with identical folders in a plea-negotiation room, both reduced to shoulder shapes under a low pendant lamp, neither identifiable, no faces, no readable text [HSTYLE] Avoid: [HNEG]
```

### ACT 4 — SIX MONTHS LATE（46枚・S128–S173・★HP 22・engine・最密）

- **the_laboratory — 12 — S128–S139**（★HP 5・vial 状態7）
```
- `S128.png`
A municipal crime laboratory bench under cold north-facing window light, stainless surfaces, a fume hood at the far end, everything ordered and unglamorous, empty of people, no person, no readable text [STYLE] Avoid: [NEG]
- `S129.png`
A gas chromatograph mass spectrometer standing against a laboratory wall, its cabinet doors closed, a bundle of tubing looping to a gas cylinder behind it, indicator lamps steady, no person, no readable text [STYLE] Avoid: [NEG]
- `S130.png`
Macro of a fine capillary column coiled inside a heated oven compartment, the metal glowing faintly with residual heat, the geometry precise and beautiful, no person, no readable text [STYLE] Avoid: [NEG]
- `S131.png`
A gloved hand loading a small glass vial into an autosampler tray of numbered wells, the numerals deliberately illegible, laboratory white light, hand and cuff only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S132.png`
An analyst's shoulder and tied-back hair thrown soft in the near foreground, a laboratory monitor beyond her in focus displaying an abstract spectral trace of peaks against a pale grid, all axis labelling reduced to unreadable marks, over-the-shoulder, cold room light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S133.png`
A single small glass tube of pale liquid standing on a laboratory bench beside the housing of a bench instrument, isolated in a pool of cold white light, the object at the centre of everything finally in the right room, no person, no readable text [STYLE] Avoid: [NEG]
- `S134.png`
An analyst seen from behind seated at a laboratory workstation, lab-coat shoulders and a tied-back head, one hand on a mouse and one on a keyboard, the screen glow the only warm thing in frame, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S135.png`
A rack of sealed evidence envelopes standing on end in a laboratory intake tray, each bearing a printed panel blurred beyond reading, cold light from a high window, no person, no readable text [STYLE] Avoid: [NEG]
- `S136.png`
Gloved hands slitting the sealed edge of an evidence envelope with a scalpel over a clean bench mat, the cut precise, the contents not yet visible, hands only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S137.png`
Macro of a laboratory spatula tip touching a pale granular sample on a weighing paper, the grain structure enormous at this magnification, cold even light, no person, no readable text [STYLE] Avoid: [NEG]
- `S138.png`
A blank printed examination sheet lying on a laboratory bench under a warm desk lamp, all of its ruled fields empty and its printed headings blurred into an unreadable smear, the first appearance of the paper that will arrive too late, no person, no readable text [STYLE] Avoid: [NEG]
- `S139.png`
An analyst's hand writing a short entry into a ruled field on a bench form with a fine pen, the writing an illegible scrawl, the lamp throwing a warm amber pool across the paper, hand only, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_two_weights — 5 — S140–S144**（★HP 2・also_thumb S141・macro loop の payoff）
```
- `S140.png`
A precision laboratory balance in its glass draught shield, the pan empty and the display showing an abstract row of characters too soft to read, cold white light, the instrument that will settle the question, no person, no readable text [STYLE] Avoid: [NEG]
- `S141.png`
Extreme macro of a single pale crumb sitting alone in the centre of a polished balance pan, dwarfed by the pan itself, the draught shield glass throwing a faint reflection, the entire case for a felony weighed in one frame, no person, no readable text [STYLE] Avoid: [NEG]
- `S142.png`
A pinch of ordinary table salt resting on a black slate surface beside a stainless spatula, lit hard from the side so every grain casts a shadow, a domestic measure standing in for a legal one, no person, no readable text [STYLE] Avoid: [NEG]
- `S143.png`
Gloved fingertips easing the glass draught-shield door of a balance closed, the movement slow and deliberate, the pan and its contents just out of focus behind the glass, hands only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S144.png`
A split composition of a handwritten figure on a paper form on the left and the softly glowing display of a laboratory balance on the right, both sets of characters deliberately unreadable, the gap between them the point, no person, no readable text [HSTYLE] Avoid: [HNEG]
```
- **filed_and_addressed_to_nobody — 6 — S145–S150**（★HP 2・paper 状態2）
```
- `S145.png`
A laboratory results printer feeding a continuous sheet into a wire catch tray, the printed rows an unreadable grey wash, the mechanism mid-cycle, cold ceiling light, no person, no readable text [STYLE] Avoid: [NEG]
- `S146.png`
A wall of pigeonhole trays in a records annexe, each slot holding a thin sheaf of paper, one slot conspicuously fuller than the rest, flat institutional light, no person, no readable text [STYLE] Avoid: [NEG]
- `S147.png`
A completed examination sheet lying face-down in a shallow steel filing tray with three other sheets on top of it, only the blank reverse visible, a warm desk lamp at the frame edge, the correct answer already buried, no person, no readable text [STYLE] Avoid: [NEG]
- `S148.png`
A telephone handset resting undisturbed in its cradle on a cluttered institutional desk, a coiled cord, a message pad with nothing written on it, cold light from a strip fitting, no person, no readable text [STYLE] Avoid: [NEG]
- `S149.png`
A pair of hands sliding a manila folder into a densely packed filing drawer and pushing it shut, the runners taking the weight, hands and cuffs only, fluorescent light overhead, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S150.png`
A figure walking away down a long records aisle between towering shelving units, seen from behind and reduced to a small dark shape by the perspective, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **her_working_years — 8 — S151–S158**（★HP 6・唯一の tonal reset）
```
- `S151.png`
A woman in a shop tabard standing far down the aisle of an all-night convenience store at three in the morning, small in a very wide frame under hard white ceiling light, shelves of packaged goods running away on both sides and the door chime unit above the entrance behind her, back turned, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S152.png`
A woman's hands counting a shallow drawer of banknotes and coins into stacks on a shop counter, the notes worn soft, a fluorescent tube reflected in the glass top, hands only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S153.png`
A woman in a shop tabard seen from behind restocking a chilled cabinet, arm extended into the cold light of the case, breath faintly visible, back turned, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S154.png`
A neighbourhood bar interior after closing time, stools inverted on the counter, a single pendant left burning over the till, the floor still wet from a mop, no person, no readable text [STYLE] Avoid: [NEG]
- `S155.png`
A woman's hands wiping down a bar counter with a folded cloth in long even strokes, a tray of upturned glasses beside her, warm low light from the back bar, hands and forearms only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S156.png`
A tired stairwell in a low-rise rental block in Baton Rouge, chipped paint on the risers, a bare bulb in a wire cage, a plastic bucket left on a landing, no person, no readable text [STYLE] Avoid: [NEG]
- `S157.png`
A woman seen from behind climbing an exterior rental stairwell carrying a tool bag and a bundle of paperwork under one arm, morning light hard on the concrete, back turned, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S158.png`
A woman's shape at a laundromat window seen from the street at night, silhouetted against the row of machine doors behind her, the glass reflecting passing headlights, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_county_counts_itself — 9 — S159–S167**（★HP 4・416/251/212 と paper 状態3–4）
```
- `S159.png`
A district attorney's records room stacked floor to ceiling with archive boxes on steel racking, an aisle running away under strip lights, a decade of closed cases in cardboard, no person, no readable text [STYLE] Avoid: [NEG]
- `S160.png`
A single archive box open on a trestle table with a dense block of thin case files inside it, the tabs a row of unreadable smudges, a desk lamp pulled low over the work, no person, no readable text [STYLE] Avoid: [NEG]
- `S161.png`
A pair of hands walking two fingers along the tops of packed file tabs in a drawer, pausing at one, sleeves pushed back, hands only under a low lamp, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S162.png`
A mail sorting belt in a county facility carrying a stream of identical windowed envelopes past camera, all address panels blurred beyond reading, industrial light overhead, no person, no readable text [STYLE] Avoid: [NEG]
- `S163.png`
A franking machine stamping a mark onto an envelope at speed, macro on the impression roller, the printed mark itself an unreadable blur, no person, no readable text [STYLE] Avoid: [NEG]
- `S164.png`
A woman's hands squaring a thick stack of identical form letters against a desk before sleeving them, the paper edges catching the light, hands only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S165.png`
A weathered outdoor bank of apartment mailboxes at dusk, one door standing slightly ajar with a single windowed envelope wedged in the slot and rain-spotted, nobody has collected it, no person, no readable text [STYLE] Avoid: [NEG]
- `S166.png`
Two figures conferring across a desk stacked with case folders in a prosecutor's office, both seen from behind and above so neither face reads, evening light through vertical blinds, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S167.png`
A figure standing alone at the end of a records aisle with a single thin folder held open in both hands, seen from far behind, the shelving towering on either side, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_scale_of_it — 6 — S168–S173**（★HP 3・n=many）
```
- `S168.png`
A dense grid of identical closed manila folders laid edge to edge across a large table, filling the frame corner to corner, every tab blurred, flat overhead light, no person, no readable text [STYLE] Avoid: [NEG]
- `S169.png`
A courthouse docket hall at mid-morning with benches full of waiting shapes seen from a high rear angle, everyone reduced to anonymous crowns and shoulders, institutional light, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S170.png`
A long queue of figures shuffling through a metal detector arch at a courthouse entrance, seen from behind at a low angle, bags on the belt, all identities lost in the backlight, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S171.png`
An aerial view at dusk of a sprawling county justice complex, car parks and low blocks and a raised walkway, the scale of the machine visible only from above, no person, no readable text [STYLE] Avoid: [NEG]
- `S172.png`
A figure standing alone in a courthouse lobby looking up at a blank directory board whose lettering is illegible, seen from behind, cold light from the glazed frontage, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S173.png`
A row of empty plastic waiting chairs bolted together in a county corridor, one seat cushion split and taped, a strip light humming above, no person, no readable text [STYLE] Avoid: [NEG]
```

### ACT 5 — THE HOOD OF A PATROL CAR（27枚・S174–S200・★HP 13）

- **the_chief_and_the_hood — 7 — S174–S180**（★HP 4・primary reveal）
```
- `S174.png`
The flat expanse of a patrol vehicle's bonnet photographed close and low in the morning, dust and pollen across the paint, a faint ring where something was once set down, the working surface of a laboratory that never was, no person, no readable text [STYLE] Avoid: [NEG]
- `S175.png`
A man's hands resting still on a table in an interview setting, fingers laced, the cuffs of a plain jacket, a glass of water beside them, soft key light from a window, hands only and no face in frame, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `S176.png`
A tripod-mounted camera and a small lighting stand set up facing an empty chair in a bare office, the interview about to happen or just finished, daylight through a slatted blind, no person, no readable text [STYLE] Avoid: [NEG]
- `S177.png`
A figure in a plain dark suit standing at a window with hands behind his back, seen entirely from behind and silhouetted against a bright city view, an authority looking out at what he ran, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S178.png`
An empty command office with a broad desk, a wall of framed rectangles whose contents are blank, a swivel chair pushed back, late light across the carpet, no person, no readable text [STYLE] Avoid: [NEG]
- `S179.png`
An anonymous shape seated at the far end of a long conference table in an unlit meeting room, the near chairs empty and receding toward camera, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S180.png`
A figure in a plain uniform seen from behind at a supply-room counter accepting a stacked tray of sealed pouches, the counter's edge worn, strip lights overhead, no face, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
```
- **the_reforms_that_werent — 8 — S181–S188**（★HP 3・closingdoor 三態）
```
- `S181.png`
A prosecutor's desk diary open at a working week with every written entry reduced to unreadable pen strokes, a phone and a stapler at the frame edge, morning light, no person, no readable text [STYLE] Avoid: [NEG]
- `S182.png`
A two-week desk calendar block sitting beside a three-day court schedule card on a laminate surface, both sets of print illegible, the mismatch between them the entire beat, no person, no readable text [STYLE] Avoid: [NEG]
- `S183.png`
A committee room in a state capitol building with a horseshoe of empty members' seats and a lectern facing them, brass fittings and heavy drapes, entirely unoccupied, no person, no readable text [STYLE] Avoid: [NEG]
- `S184.png`
A thick bound commission report standing upright between two heavy bookends on an office shelf, its spine lettering an unreadable smear, dust visible on the top edge, no person, no readable text [STYLE] Avoid: [NEG]
- `S185.png`
Several figures seated along a committee bench seen from the public gallery behind them, only the backs of heads and shoulders visible against a bright panelled wall, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S186.png`
A heavy panelled door in a state building swinging closed on a lit corridor, the gap narrowing to a bright vertical line, brass kickplate scuffed, no person, no readable text [STYLE] Avoid: [NEG]
- `S187.png`
A figure in a plain jacket walking away along a marble capitol corridor carrying a document wallet, seen from far behind, the vaulted ceiling swallowing the footsteps, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S188.png`
A pair of hands lifting a stack of unopened pouch trays into a wheeled bin marked only by its shape, a store-room roller shutter half closed behind, hands only, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **courts_and_national_scale — 6 — S189–S194**（★HP 3）
```
- `S189.png`
A judge's raised bench photographed empty and head-on in a modern American courtroom, pale wood, a blank nameplate rebate with nothing in it, cool ceiling light, no person, no readable text [STYLE] Avoid: [NEG]
- `S190.png`
A prison mail-room table strewn with opened correspondence and a small test kit tray, envelopes flattened and stacked, every hand-written address blurred to illegibility, hard overhead light, no person, no readable text [STYLE] Avoid: [NEG]
- `S191.png`
A figure in a plain uniform seen from behind sorting envelopes into pigeonholes in a facility mail room, shoulders working steadily, strip lighting, no face, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
- `S192.png`
A night aerial of an American interstate interchange, ribbons of white and red light braiding through the frame, the whole country's traffic reduced to a circulatory diagram, no person, no readable text [STYLE] Avoid: [NEG]
- `S193.png`
A hard-shoulder stop at night seen from a great distance across open ground, two small vehicle shapes and one cone of headlight, the scene anonymous at that range, no faces, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
- `S194.png`
A figure standing beside an open car door on a dark verge with hazard lights pulsing, seen from behind and far away, the whole encounter rendered small and routine, no face, no readable text [HSTYLE] Avoid: [HNEG]
```
- **one_state — 6 — S195–S200**（★HP 3・paper 状態5・amber）
```
- `S195.png`
The columned portico of a western American state capitol photographed against a clear high-altitude sky, deep shadow between the pillars, snow still on the distant range beyond, no person, no readable text [STYLE] Avoid: [NEG]
- `S196.png`
A bound statute page open on a desk beneath a heavy fountain pen mid-signature, the printed clauses blurred into an unreadable smear, warm amber lamplight pooled on the paper, no person, no readable text [STYLE] Avoid: [NEG]
- `S197.png`
A hand laying a signed sheet onto a small stack on a desk blotter, the pen still in the fingers, a warm lamp raking across the paper, hand and cuff only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S198.png`
A legislative chamber photographed from the rear gallery with rows of desks and a presiding rostrum, every seat empty, daylight from a domed skylight, no person, no readable text [STYLE] Avoid: [NEG]
- `S199.png`
Rows of legislators seen only as the backs of heads and shoulders at their chamber desks, arms raised in a vote, the tally board on the far wall deliberately blank, no faces, no readable text [HSTYLE] Avoid: [HNEG]
- `S200.png`
A figure standing alone at the top of a capitol's exterior steps at dusk looking out over a city, seen from behind and below, the building's mass filling the top of the frame, no face, no readable text [HSTYLE] Avoid: [HNEG]
```

### ENDING（10枚・S201–S210・★HP 4・vial 状態8・strip to essentials）

```
- `S201.png`
A courthouse door photographed closed from the outside in flat evening light, its brass handle worn bright by decades of hands, the building beyond it silent, no person, no readable text [STYLE] Avoid: [NEG]
- `S202.png`
A woman's shape standing at a bus stop at dusk with a shoulder bag, seen from across the road and slightly behind, traffic passing between camera and subject, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S203.png`
A woman seated at a kitchen table in the evening with an unopened residential background-check letter and a set of keys in front of her, seen from behind and slightly above so nothing of her face reads, the envelope's printed panel blurred beyond reading, the window beyond her already gone blue, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S204.png`
A woman's hands folding a work tabard into a bag on a bed at the end of a shift, the movements economical, low bedside light, hands only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S205.png`
Extreme macro of a single pale crumb on a black surface, isolated and enormous, every irregularity of its edge visible, nothing else in the frame at all, no person, no readable text [STYLE] Avoid: [NEG]
- `S206.png`
A laboratory balance pan photographed empty and immaculate under cold light, the draught shield open, the instrument at rest after the answer it gave, no person, no readable text [STYLE] Avoid: [NEG]
- `S207.png`
A different car's empty passenger seat photographed in flat present-day daylight, seatbelt retracted, a coffee cup in the door pocket, an ordinary vehicle belonging to nobody in this story, no person, no readable text [STYLE] Avoid: [NEG]
- `S208.png`
A sealed unopened test pouch lying on the vinyl bench seat of a patrol vehicle at dusk, the ampoule inside still perfectly pink, the interior otherwise stripped of every marking, no person, no readable text [STYLE] Avoid: [NEG]
- `S209.png`
A woman's shape walking away from camera along a lit residential street at dusk, growing smaller between parked cars, an ordinary evening in an ordinary town, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `S210.png`
A wide dusk view of an American arterial road with a single vehicle's tail lights receding toward a low horizon, sodium lamps just coming on down the length of it, the machine still running, no person, no readable text [STYLE] Avoid: [NEG]
```

## 5.7 幕別 motif 枚数の検算（★Codex は書き終えたら足して確認）

```
ACT0  : 6+5+4 = 15
ACT1  : 9+7+8+7+9 = 40
ACT2  : 8+8+9+6+7 = 38
ACT3  : 8+6+8+7+5 = 34
ACT4  : 12+5+6+8+9+6 = 46
ACT5  : 7+8+6+6 = 27
ENDING: 10
合計   : 15+40+38+34+46+27+10 = 210 ✓
★human-present(★HP) body: 4(ACT0)+16(ACT1)+18(ACT2)+8(ACT3)+22(ACT4)+13(ACT5)+4(ENDING) = 85 / 210 = 40.5% ✓
（残り125は object/symbolic レーン）
```

> **★★ R3（2026-07-29）で実測して直した最大の欠陥。** v001 は「★HP 85枚 / 40.5%」と3か所（§3.2・§3.3 [9][11]・本節）で宣言していたが、**§5.6 の 210行を機械で数えると `[HSTYLE]` は 79行しかなく、実測は 79/210 = 37.62%** だった。**オーナーの常設指示は「誕生時から ★HP ≥40%」であり、37.62% は不合格。** 宣言と実体がずれたまま生成に入っていたら、210枚焼き終わってから発覚し、GPU 5〜8時間の焼き直しになっていた。
> **6行を object レーンから ★HP レーンへ転換して 85 に合わせた（総枚数・幕別枚数・cuts 563 は1つも動かしていない）:**
> **S017**（ACT1・letting office → 肩越しの女性）· **S066**（ACT2・書類台車 → ローアングル背後の事務員）· **S084**（ACT2・壁掛けカレンダー → 日付を消す手）· **S132**（ACT4・スペクトル画面 → 分析官の肩越し）· **S151**（ACT4・コンビニ内観 → 遠景の店員）· **S203**（ENDING・封筒 → 食卓に座る女性の後ろ姿）。
> 転換先はすべて **§5.6 冒頭の anti-samey 変化マトリクス**（距離×角度×光×setting×姿勢）で既存85枚と衝突しない軸を選んである（S017=肩越し/朝ブラインド, S066=ローアングル/歩行, S084=手/day-room光, S132=over-the-shoulder, S151=far-wide, S203=座位/背後やや上）。
> **加えて S048 の本文の "wound" を "injury" に変えた** — §1.3 の `BANNED_ACCURACY` に `wound` があり、許容フレーズを剥がしたあとも唯一残る誤検知だったため。
> **ブロック見出しの ★HP 数も実体に合わせて訂正した**（what_the_search_found 0→1 / the_verdict_moment 5→4 / booking_night 4→3 / the_lawyer_and_the_offer 4→5 / twenty_one_days 3→4 / what_was_waiting 3→2）。**幕別合計は 4/16/18/8/22/13/4 = 85 で §3.2 と一致する。**

## 5.7a ★R3 REGEN LIST（Codex が既に生成を始めている場合、この7枚だけ焼き直す）

| ファイル | 旧レーン | 新レーン | 理由 |
|---|---|---|---|
| `S017.png` | object | **★HP** | ★HP 85枚に合わせる（ACT1 +1） |
| `S048.png` | ★HP | ★HP（本文のみ変更） | `wound` → `injury`（§1.3 誤検知の解消） |
| `S066.png` | object | **★HP** | ★HP 85枚に合わせる（ACT2 +1） |
| `S084.png` | object | **★HP** | ★HP 85枚に合わせる（ACT2 +1） |
| `S132.png` | object | **★HP** | ★HP 85枚に合わせる（ACT4 +1） |
| `S151.png` | object | **★HP** | ★HP 85枚に合わせる（ACT4 +1） |
| `S203.png` | object | **★HP** | ★HP 85枚に合わせる（ENDING +1） |

> **他の 203 枚のプロンプトは1文字も変えていない。** 焼き直しはこの7枚だけでよい。`[STYLE]/[NEG]` から `[HSTYLE]/[HNEG]` へレーンが変わる6枚は、**必ず新しいレーンのスタイル文字列で焼く**（§5.5-1 のレーン厳守）。QC フラグは `has_human_body:true` になるが、それ単独では reject しない（§4.1a）。

## 5.8 メタJSON
画像ごとの meta JSON は作らない。`qc_fieldtest_stills.py` が sha256 / phash / mean_luma を `still_qc.v001.json` に記録する。

## 5.9 パーサ契約（`read_prompts()` はこの2行形式しか読まない）

```
- `S###.png`
<positive prompt を1行で> Avoid: <negative を同じ行に>
```
1行目はバッククォートで囲んだファイル名のみ。2行目に本文を1行で書く（改行しない）。**この形式を崩すと `check_prompt_diversity.py` がプロンプトを抽出できず、coverage ゲートで FAIL する。**

> **★R3（2026-07-29）BLOCKING な罠を1つ潰した。** v001 のこの見本は実在IDの **`S001.png`** を使っていた。`generate_sdxl_4k.py` の `read_prompts()` は「バッククォートのファイル名行 → 次の `Avoid:` を含む行」をそのまま拾い、**同名IDを2件目として append する**（重複排除しない）。本書を丸ごとパーサに通すと **S001 が `<positive prompt>` という中身で二重登録され、`shots=255` の確認も 256 になる**。ID を `S###` に変えたので `^-\s*`?[SMTF]\d{2,3}` にも `\b[SMTF]\d{2,3}\b` にも当たらない。
> **さらに:** **§5.9 のこの見本行は書式説明であって素材ではない。`04_scenes/ai_prompts.v001.md` に転記しない。** 転記するのは §5.6（S001–S210）・§8.1a（M01–M42）・§5.12（T01–T03）・§5.13（F001–F012）の合計 **267行だけ**。

## 5.10 生成コマンド（★variants 指定なし。`--variants 3` は使わない）

```bash
# スモーク（shots=255 を必ず目視確認してから本番）
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py --ep PD-2026-057-fieldtest --only S001
# 本番
./.venv/Scripts/python.exe scripts/generate_sdxl_4k.py --ep PD-2026-057-fieldtest
```

## 5.11 ★人物画像（匿名・ドラマ化スタンドイン）— HUMAN-FIGURE prompts（★18本・i2v 種の内数）＋ ★HP body still の style

### ★lane 定義（人物は動かす＝紙芝居にしない → H は motion レーンへ・locked counts 不変）

**H001–H018 は「新規の静止カット」ではなく、既存 42本の i2v 種のうち 18本の中身（＝人物ビート）として作る。additive にしない（object 種を人物種に転換）。**
- **role = `i2v_source`**（body には回さない）。per-act 内数: **ACT1×4・ACT2×5・ACT3×1・ACT4×5・ACT5×3 ＝18**（§4.5 の M04 M06 M07 M09・M12 M14 M15 M17 M18・M22・M27 M29 M30 M32 M33・M35 M37 M39）。ACT0/ENDING は象徴のまま。
- **asset_id は既存の i2v 種 ID 空間（`^FDT-MS\d{2}$`）の18本を占有**（H001–H018 は本書内のラベル）。種画像ファイルは `M<NN>_src.png`。`public_path==null`。
- 各人物種は **Wan → RIFE（§8）で motion 化**され、**42本の motion のうち18本**になり、**84 motion カットのうち最大36カット**に出る＝**人物が動く**。
- **QC フラグ:** `has_human_body:true`（許可）・`has_identifiable_real_person:false`（必須）・`has_readable_text:false`（必須）・`has_drug_use_or_restraint:false`（必須）・`has_identifiable_insignia:false`（必須）。
- **★locked counts は1つも変わらない:** still_body **210**（object 125 ＋ ★HP 85）/ still_i2v_source **42**（象徴 24 ＋ 人物 18）/ motion **42** / archive **252** / overlay **30** / thumb_face **3**；cuts **252/227/84 = 563**；still-share **0.4032**；first-use **0.8952**；avg-uses **1.1171**。

### `[HSTYLE]`

```
, cinematic photoreal still, documentary reenactment stand-in, a generic anonymized person who resembles no real individual, face kept non-identifiable — turned away, in profile lost to shadow, back-lit to a silhouette, cropped below the eyes, or thrown soft in shallow focus, sodium-vapor orange as the one recurring night note and flat green-tinged institutional fluorescent as the one recurring day note, near-black ink gravity, period-correct American clothing for the decade named in the line, low-key deep-shadow lighting, telephoto compression, shallow depth of field, restrained dignified framing, figures always upright and composed and never in distress poses, uniforms and workwear entirely plain with no marking of any kind, clear and high-contrast never milky, ultra-detailed, photoreal, 4K, 16:9, fine film grain, no text, no watermark, no logo, no insignia, no readable documents, no drug use, no restraint hardware in frame, one warm late-paper amber note only where the beat is the examination sheet, the letter or the statute
```

### `[HNEG]`

```
recognizable real person, likeness of a specific person, Amy Albritton, Charles McClelland, Art Acevedo, Vanessa Velasquez, Dan Richardson, Ahtavea Barker, Devon Anderson, Marie Munier, Inger Chandler, L. J. Scott, any real judge or officer or analyst, celebrity, mugshot, deepfake, text, words, letters, numbers, captions, watermark, logo, badge number, precinct number, agency seal, department seal, unit patch, shoulder flash, name tape, vehicle door lettering, readable document, legible report, legible letter, legible date, license plate, needle in an arm, needle in skin, injecting, snorting, drug use, pills as spectacle, blood, wound, injury, corpse, handcuffs on a person, restrained person in distress, cowering figure, screaming face, crying face, hands over the face, identifiable child face, cartoon, illustration, anime, 3d render, low quality, blurry, jpeg artifacts, deformed, extra limbs, warped, melting, electric blue, steel-cyan, sodium prison gold, porch amber, crimson kitchen, teal-green hospital, forest-green, civil-violet, somber-plum, interrogation fluorescent green-gray, post-office signage red, phantom-ledger phosphor green, milky haze, scanline
```

### 人物ビート（★18本・全て匿名・非識別・実在 likeness なし・adults only）

- **H001** (ACT1 · M04) a passenger's hands in her lap as the car slows — the last ordinary moment.
- **H002** (ACT1 · M06) a driver's hands leaving the wheel and reaching for the door handle.
- **H003** (ACT1 · M07) a gloved hand sweeping a torch beam across a footwell.
- **H004** (ACT1 · M09) a gloved hand raising a tube of blue liquid to eye level.
- **H005** (ACT2 · M12) a woman seated alone on a bench at the end of a corridor.
- **H006** (ACT2 · M14) hands passing a pen across a counter.
- **H007** (ACT2 · M15) a standing figure at a courtroom lectern, from behind.
- **H008** (ACT2 · M17) hands flat on a lectern shelf beginning to tremble and then stilling.
- **H009** (ACT2 · M18) a figure walking away down a courtroom aisle.
- **H010** (ACT3 · M22) hands closing a hinged wooden sample case.
- **H011** (ACT4 · M27) a gloved hand loading a vial into an autosampler tray.
- **H012** (ACT4 · M29) an analyst at a workstation, from behind, as a trace resolves.
- **H013** (ACT4 · M30) a hand writing a short entry into a ruled field under a warm lamp.
- **H014** (ACT4 · M32) hands squaring a stack of identical letters.
- **H015** (ACT4 · M33) a woman restocking a chilled cabinet on a night shift.
- **H016** (ACT5 · M35) a man's laced hands still on an interview table.
- **H017** (ACT5 · M37) a figure at a window with hands behind his back.
- **H018** (ACT5 · M39) a hand laying a signed sheet onto a stack under amber lamplight.

## 5.12 ★サムネ用 emotive-face 静止画（3枚・CTR §4A・`thumb_face`）

### `[TSTYLE]`
```
, thumbnail key art, a single non-real dramatized generic human character rendered in a clearly illustrative semi-painterly cinematic style so it never reads as a real photograph of a real person, face occupying 50 to 65 percent of frame height with eyes on the upper third, bright key light on the face and a rim light separating it from a dark desaturated blurred American night background, skin warm, background cool, high contrast and vivid, one clean quadrant of negative space for text, 1280x720, ultra-detailed
```
### `[TNEG]`
```
photoreal photograph of a real person, likeness of Amy Albritton or any real officer or judge or analyst, recognizable real celebrity, deepfake, a child, wounds, blood, gore, needle in skin, drug use, restraint, weapon, badge number, agency seal, text, words, letters, numbers, watermark, logo, two faces, tiny face, neutral expression, dark muddy low-contrast mush, cartoon flatness, extra limbs, deformed, warped
```
```
- `T01_face.png`
A non-real dramatized generic white woman's face in her early forties in an illustrative cinematic style at peak emotion — stunned open-eyed disbelief looking slightly past the viewer, the look of someone hearing a number that cannot be right, pushed to the right third over a dark blurred parking lot at night with one orange lamp flare, warm rim light, clean negative space on the left [TSTYLE] Avoid: [TNEG]
- `T02_face.png`
A non-real dramatized generic older man's face in an illustrative cinematic style with a grave, unguarded, faintly ashamed expression looking directly at the viewer, the look of an official admitting his own institution was wrong, pushed to the left third over a dark blurred city skyline with a faint cool haze, hard rim light, clean negative space on the right [TSTYLE] Avoid: [TNEG]
- `T03_face.png`
A non-real dramatized generic woman's face in an illustrative cinematic style in profile at three-quarters turned down toward something in her hands, exhausted and utterly composed, lit by a single warm lamp from below the frame line, over a dark blurred kitchen interior, clean negative space upper right [TSTYLE] Avoid: [TNEG]
```

## 5.13 ★EMOTIVE FACES — VISIBLE faces（F系12枚・per owner 2026-07-25 standard）

**★ FACE 標準（data-driven・owner choice A）:** 全F画像は**LIGHT + EXPRESSION で目立つ顔**（サイズで盛らない）— **medium-close-up ~30–45% of frame height, eyes on the upper third, front or slight three-quarter, one strong unmistakable emotion, dramatic key + rim light against a DARK moody restrained background**。60%超の顔面充填・背向き・影に沈む・hands-only は不可。**F系は side lane（distinct/cuts に数えない）。採否は B が決める。**

### `[FSTYLE]`
```
, a clearly-visible emotive human face in a strong medium-close-up filling about thirty to forty-five percent of the frame, eyes on the upper third, front or slight three-quarter view looking near camera, one strong unmistakable expression, dramatic key light plus rim light on the face against a dark moody background, restrained saturation, a generic anonymized non-real person resembling no real individual, cinematic documentary grade, sodium night or institutional fluorescent as the ambient note with one warm amber accent only on paper beats, ultra-detailed skin and eyes, high contrast, 16:9, adults only, no text, no watermark, no logo, no insignia
```
### `[FNEG]`
```
likeness of a real or named person, Amy Albritton, Charles McClelland, Art Acevedo, Vanessa Velasquez, Dan Richardson, Ahtavea Barker, Devon Anderson, L. J. Scott, recognizable real person, mugshot, deepfake, child, toddler, wounds, blood, injury, needle in skin, drug use, restraint, weapon, badge number, agency seal, unit patch, readable text, document, caption
```
```
- `F001.png`
A generic anonymized white woman in her early forties in medium-close-up, photoreal, her expression a flat exhausted disbelief with the jaw set and the eyes slightly too wide, orange street light as the key from camera left and a cold rim from behind, dark blurred parking lot bokeh, not a likeness of any real person [FSTYLE] Avoid: [FNEG]
- `F002.png`
A generic anonymized man in a plain dark uniform shirt in medium-close-up, photoreal, his expression the blank procedural neutrality of someone performing a routine task, hard fluorescent key from above and a weak cool rim, dark vehicle interior behind him, collar entirely unmarked, not a likeness of any real officer [FSTYLE] Avoid: [FNEG]
- `F003.png`
A clearly illustrative semi-painterly face of a generic middle-aged court-appointed lawyer, brow tight in the resigned impatience of a man with forty files and one morning, corridor window light as the key, dark panelled background, not a likeness of any real attorney [FSTYLE] Avoid: [FNEG]
- `F004.png`
A generic anonymized woman in medium-close-up mid-sentence with her mouth open on a word she cannot finish and her eyes brimming but not spilling, cold courtroom light from a high window as the key, dark wooden background, restrained and never lurid, not a likeness of any real person [FSTYLE] Avoid: [FNEG]
- `F005.png`
A clearly illustrative semi-painterly face of a generic robed judge in three-quarter view, expression neutral to the point of absence, cool overhead key and a faint warm rim, dark bench woodwork behind, no nameplate and no heraldry anywhere, not a likeness of any real judge [FSTYLE] Avoid: [FNEG]
- `F006.png`
A generic anonymized older male chemist in medium-close-up in a private workshop, expression thoughtful and slightly evasive as if asked a question he has answered honestly and does not enjoy, warm anglepoise key from below left, dark bench background, not a likeness of any real inventor [FSTYLE] Avoid: [FNEG]
- `F007.png`
A generic anonymized female laboratory analyst in medium-close-up in safety glasses pushed up on her head, expression absorbed and precise as she reads something off frame, cold north-window key and a faint instrument glow as rim, dark laboratory background, not a likeness of any real analyst [FSTYLE] Avoid: [FNEG]
- `F008.png`
A generic anonymized female prosecutor in medium-close-up, expression a controlled dismay as she registers the size of what she is counting, desk-lamp key warm from the right and a cool ceiling rim, dark shelving of archive boxes behind, not a likeness of any real prosecutor [FSTYLE] Avoid: [FNEG]
- `F009.png`
A generic anonymized woman in a shop tabard in medium-close-up under a convenience-store ceiling tube, expression a tired ordinary alertness at three in the morning, hard cold key from directly above and a weak warm rim from a cooler, dark aisle behind, not a likeness of any real person [FSTYLE] Avoid: [FNEG]
- `F010.png`
A clearly illustrative semi-painterly face of a generic retired police commander in medium-close-up, expression grave and unguarded with the eyes lowered a fraction, warm window key from camera right and a cold rim, dark office background, not a likeness of any real chief [FSTYLE] Avoid: [FNEG]
- `F011.png`
A generic anonymized male state legislator in medium-close-up at a chamber desk, expression the mild civic satisfaction of a unanimous vote, cool daylight key from a skylight and a warm rim from a desk lamp, dark panelled chamber behind, not a likeness of any real legislator [FSTYLE] Avoid: [FNEG]
- `F012.png`
A generic anonymized woman in her mid-forties in medium-close-up at a kitchen table in the evening, expression settled and unsentimental with the faintest hardness around the mouth, a single warm lamp as key from below the frame line and a cold window rim, dark domestic background, not a likeness of any real person [FSTYLE] Avoid: [FNEG]
```

---

# 6. A-2/A-3: 静止画のQC・目視（★depth map なし）

## 6.1 機械QC（body 210 + i2v種 42 + thumb_face 3 = 全255枚・`qc_fieldtest_stills.py`）

| # | 検査 | 判定 | 落ちたら |
|---|---|---|---|
| Q1 | 解像度 | `max(w,h)>=3840` | reject |
| Q2 | サイズ/開ける | `>1024 bytes` かつ PIL で開ける | reject |
| Q3 | 平均輝度 | `18.0<=mean_luma<=225.0`（sodium night と near-black が多い→黒潰れ注意。ACT3 の研究所・ACT5 の capitol は明側） | reject |
| Q4 | 近似重複 | 全ペア phash。類似度 `>=0.90` は片方 reject。**watch-list（§5.5a の状態連鎖が正）: vial 8状態(S002/S004/S005–S006/S007/S060/S112/S133/S208＝各状態1–2枚のみ)・paper 5状態(S138/S147/S162/S165/S196)・two-weights 2状態(S013/S140–S141/S144)・empty passenger seat 3状態(S010/S055/S207)・corridor 群(S056/S064/S081/S173)・courtroom 群(S073/S079/S123/S124/S189)・records/filing 群(S103/S105/S146/S159/S160/S168)・laboratory bench 群(S128/S129/S135/S137/S206)・★HP waiting 群(S057/S063/S069/S085/S169/S173)・★HP hands-macro 群(S018/S037/S043/S061/S075/S131/S136/S139/S152/S155/S161/S164/S197)・★HP walking-away 群(S015/S020/S080/S150/S157/S187/S200/S209)・capitol/chamber 群(S183/S195/S198/S199) の被りに注意** | 片方 reject＋プロンプト見直し（**削るのではなく §5.5a のルールで作り直す**） |
| Q5 | 文字の混入 | **目視。** 読める英字・数字・日付(1973/1974/1978/2010/2011/2014/2016/2017/2024/2026)・重量(.02 / 0.0134)・件数(416/251/212/119/172)・機関名・書類ロゴ | `has_readable_text=true`→reject |
| Q6 | **実在人物**の顔の混入 | **目視。** 実在人物として識別可能な顔（Albritton/McClelland/Acevedo/Velasquez/Richardson/Barker/Anderson/Munier/Chandler/Scott に**似た**顔）。**匿名・非識別の顔（H/F/thumb_face）は OK。** | `has_identifiable_real_person=true`→reject |
| Q7 | 薬物使用・拘束・受傷・標章・子供 | **目視。** 皮膚に刺さる注射針・服用/吸引・見せ場の粉末・手錠が写る拘束・傷/血・苦悶/泣き顔・**バッジ番号/所属章/機関シール/車両表記**・**識別可能な子供の顔**。**★匿名の人体は OK（`has_human_body=true` 単独では reject しない）。** | あれば reject |

**Q5/Q6/Q7 は機械で判定しない。全255枚を実際に目視:**

```bash
./.venv/Scripts/python.exe scripts/build_footage_contact_sheet.py --ep PD-2026-057-fieldtest --media image
#   → runs/qc/fieldtest_footage_contact_NN.png（20枚/シート・約13シート）。全シートを開いて1枚ずつ見る
```

## 6.2 出力
`episodes/PD-2026-057-fieldtest/05_visuals/still_qc.v001.json`（sha256 / phash / mean_luma / qc フラグ / reject 理由）。

## 6.3 accepted が (body210 / i2v種42 / thumb3) に届かなかったとき
**同一プロンプト・別シードで1枚だけ**再生成する。プロンプトを弱めて通さない。Q4 で落ちた場合のみ §5.5a に従いプロンプトを作り直す（状態語を変える）。**still 210本を割ったまま先へ進まない**（§3.3 [3] の余裕を食い潰す）。

## 6.4 ★depth map は生成しない（本作は depth treatment 不使用）
`depth`-displacement は被写体を溶かす（EP48/49 の warp 欠陥）。**BANNED。`depth_path` をマニフェストに書かない**（§4.2-19 が機械で弾く）。

---

# 7. A-4: 実写アーカイブ 252本の選定と全点目視QC（★四層ドクトリンの第一層）

## 7.1 在庫の実態

- **アーカイブ本体:** `H:\pd-media\assets\archive\`（一部は `E:\pd-archive\` と `H:\pd-media\assets\archive\_quarantine\` に分散）。台帳 `H:\pd-media\assets\archive\_ledger\*.jsonl`。
- **factory 棚:** `H:\pd-media\assets\factory\{backgrounds,light_assets,particle_assets,vfx_overlays}\`。命名 `AF-<TYPECODE>-<4桁>__<subtype_slug>.<ext>`。
- **索引:** `./.venv/Scripts/python.exe scripts/search_archive.py --stats` → 本パスの実行時点で **112,678 件**。ソース内訳（同実行）: pixabay 53,836 / pexels 34,911 / nypl 9,391 / nasa 6,411 / freesound 2,143 / pixabay_extra 1,793 / nara 1,319 / noaa 978 / loc 611 / smithsonian 412 / ia 347 / sdxl 216 / mixkit 178 / unsplash 91。
- **参照ブラウズツリー（補正済み）:** `D:\pd-media-browse\factory_browse\<theme>\`。
- **ファイル名は自己記述的**（`source__id__title-slug.ext`）で、台帳の各行が **licence decision** を持つ。

## 7.2 選定条件

- **本数 252**（幕別 §4.4）。`uses` は **1**（同一素材の再利用禁止）。
- **kind:** video を優先（`kind:video` は索引に 17,834 件）。static image は「動かす前提」で `parallax`/`bleed` 処理する場合に限る。
- **EP39–EP56 で使った sha256 と交差ゼロ**（§7.7）。
- **licence:** `pd` / `cc0` / `free_commercial` のみ（§7.4）。
- **generic symbol cap:** `check_footage_diversity` が **汎用象徴 ≤2** を機械で見る。⚠ **本作は法廷＋研究所の話なので、棚は真鍮の天秤とガベルを大量に出してくる。`balance_scale_brass` 系は「文字どおり物を量る秤」としてのみ採る（S140–S142 のカバー）。正義の寓意としては採らない。**

## 7.3 ★実行済みクエリ表（2026-07-29 に本パスが実際に走らせた結果・ここから始める）

```bash
./.venv/Scripts/python.exe scripts/search_archive.py <keywords> [--theme X] [--source Y] [--limit N]
```

| クエリ | 幕 | covers | 代表ヒット（実測・台帳行そのまま） |
|---|---|---|---|
| `parking lot` | 0 | S008 | `H:\pd-media\assets\factory\backgrounds\AF-BG-14767__police_station_at_night.mp4`（pexels・free_commercial・11.2MB・"aerial night view of illuminated parking lot"） |
| `patrol car night` | 0,1 | S033 | `AF-BG-1908__police_car_lights_night.mp4`（pexels・26.5MB・"police patrols in the street"） |
| `police lights` | 0,1 | S009 | `AF-BG-1844__police_car_lights_night.jpg`・`AF-BG-1845__police_car_lights_night.jpg` |
| `highway night road` | 1,5 | S025,S192 | `AF-BG-1528__highway_night_long_exposure.jpg`・`AF-BG-1532__highway_night_long_exposure.jpg` |
| `city traffic night` | 0,5 | S011,S192 | `AF-BG-0369__blurred_city_night_bokeh.mp4`（54.6MB）・`AF-BG-0373__blurred_city_night_bokeh.mp4` |
| `texas houston` | 0 | S011 | `AF-BG-7558__city_traffic_night_long_exposure.jpg`（"houston texas city urban skyline"）・`AF-BG-30505__suburban_house_exterior_night.jpg`・`AF-LIGHT-5491__police_strobe_red_and_blue.jpg` |
| `jail cell` / `prison corridor` | 2 | S056,S081 | `AF-BG-1762__prison_corridor.jpg`（"empty prison corridor"）・`AF-BG-1793__prison_corridor.jpg`・`AF-BG-1765__prison_corridor.jpg` |
| `courthouse corridor` | 2 | S064 | `E:\pd-archive\courtroom_justice\loc__2017661063__corridor-federal-building-and-u-s-courthouse-phoenix-arizona.jpg`（**loc**・free_commercial・**索引中ただ1件**） |
| `courtroom` | 2,3 | S073,S123 | `AF-BG-0466__courtroom_interior.jpg`（"courtroom with american flags in usa"）・`AF-BG-0463__courtroom_interior.jpg` |
| `case files stack desk` / `file cabinet documents` | 3,4 | S103,S159 | `AF-BG-23581__case_files_stack_desk.jpg`・`AF-BG-23582__case_files_stack_desk.jpg`・`AF-BG-23642__case_files_stack_desk.jpg`（"records filing cabinet files pen"） |
| `laboratory glassware` | 3,4 | S108,S128 | `AF-BG-2000__laboratory_glassware.jpg`（"vials with liquids in holder"）・`AF-BG-2003__laboratory_glassware.jpg` |
| `test tube liquid` | 3 | S108 | `AF-BG-5111__laboratory_glassware.mp4`（7.5MB）・`AF-BG-5076__laboratory_glassware.jpg` |
| `microscope lab` | 4 | S129 | `AF-BG-2086__modern_medical_lab.jpg`・`AF-BG-5068__laboratory_glassware.jpg` |
| `laboratory technician` | 4 | S134 | `AF-BG-7109__dna_laboratory_blue.mp4`（5.8MB・"a laboratory technician putting samples in a machine" — **mid reveal の実写アンカー**）・`AF-BG-5121__modern_medical_lab.jpg` |
| `evidence bag` | 1,4 | S044,S135 | `AF-BG-6865__evidence_bag.jpg`・`AF-BG-6868__evidence_bag.jpg` |
| `weighing scale balance` | 4 | S140–S142 | `AF-BG-9919__balance_scale_brass.jpg`（"a weighing scale on white surface"）⚠**寓意の天秤は採らない** |
| `government building columns` | 5 | S195 | `AF-BG-0620__government_building_exterior.jpg`（"columns in california state capitol museum building"） |
| `police badge` | 5 | S180 | `AF-BG-6627__police_badge_close_up.jpg`（"a police office holding black radio"）⚠**バッジが読める向きは不可・装備の質感としてのみ** |
| `police station` | 2,5 | S056 | `AF-BG-14700__police_station_at_night.jpg`・`AF-BG-14702__police_station_at_night.jpg` |
| `chemistry chemical reaction` | 3 | — | `AF-BG-5085__laboratory_glassware.jpg` — **ヒット1件のみ。これが「呈色反応そのものは実写で撮れない」という測定結果であり、vial 連鎖を Codex（第三層）に置く根拠。** |

**⚠ この表は出発点であって完成ではない。252本に届かせるには各行を `--limit 60` で掘り下げ、`--theme documents_paper` `--theme urban_night` `--theme property_home` `--theme civic_voting` `--theme americana_1930s_1970s` などで補う。**

## 7.4 ライセンス（ALLOWED_LICENSES — これ以外選ばない）

```python
ALLOWED_LICENSES = {"pd", "cc0", "free_commercial", "royalty_free",
                    "generated_owned", "Pexels License", "Pixabay Content License"}
```
> **⚠ `review_required` は採らない（索引に789件・とくに `nara` 動画の多くは `_quarantine` 配下で `review_required`）。オーナーの明示的な権利判断なしに staging しない。** `pd_expired_owner_approved` / `pd_allied_coproduction_owner_approved` も同様に**個別承認済みの既決ぶんだけ**であり、新規には使わない。

## 7.5 ★★★ 棚のラベルとフォルダは信用できない ★★★

> **オーナー指示（2026-07-29）そのまま:** *「the shelf's own theme folders are 40% mislabeled (measured; a court folder contained a Christmas dinner). NEVER select by raw folder.」*

**本パスが実際に踏んだ実例（そのまま記録する）:** `--source nara` を `theme:courtroom_justice` で見ると、**"British Courtroom"** の隣に **"Crown Prince Olaf and Princess Martha of Norway at River Rouge"** と **"[STOCK NEWSREEL EXCERPTS]"** が同居している。アメリカの法廷でないどころか王族の訪問記録である。**フォルダ名から選べば必ず混入する。**

**手順（省略禁止）:**
1. **`search_archive.py` で選ぶ**（復元済みのプロバイダ由来タイトルに対して照合される）。または補正済みブラウズツリー `D:\pd-media-browse\factory_browse\<theme>\` を使う。**生のフォルダ一覧から選ばない。**
2. 候補を `select_factory_assets.py` に渡す。**このツールはラベル付きコンタクトシートを出力し、出せなければ exit 3 で止まる。**
3. **全シートを開いて1枚ずつ見る。** タイル下のラベルは「唯一の正直な説明」であって、テーマ名ではない。
4. 場違い・被り・人物識別可能・標章可読・年代不整合を落とす。**落とした分は §7.3 のクエリを掘って補充する。**
5. 通ったものだけを `factory_selection.v001.json` に書き、各行の `eyeballed_content` に**自分が見たものを書く**（テーマ名の転記は不可）。

```bash
./.venv/Scripts/python.exe scripts/select_factory_assets.py --ep PD-2026-057-fieldtest --assert-count 252
# exit 3 = コンタクトシートを出せなかった → 未完了。ここを飛ばして staging しない。
```

## 7.6 出力
`05_stock/factory_selection.v001.json` / `05_visuals/factory_clip_qc.v001.json`。

## 7.7 EP39〜EP56 との重複ゼロ（BLOCKING）
既出話の `factory_selection` / `asset_manifest` から sha256 集合を作り、**交差が空であることを確認**してから確定する。色レーンでも分離する: EP32 の steel-cyan 路上素材、EP36 の electric-blue 監視素材、EP55 の fluorescent green-gray 取調素材、EP56 の signage-red 商店素材は**同じ画でも別の色で使われているため、EP57 では採らない**（見た人が「前に見た」と感じる）。

---

# 8. A-5: i2v モーション化 42本（Wan 2.2 A14B → RIFE 48fps）

## 8.1 i2v にする42本（動きが意味を持つ絵・各1枚の種プロンプト・バリエーション0）

幕別 §4.5。**24本が象徴、18本が人物（H001–H018）。** 種画像は `M<NN>_src.png`、`role="i2v_source"`、`public_path=null`。

### 8.1a i2v 種プロンプト（★`ai_prompts.v001.md` の末尾にこの42行を追加・各1枚・poised-still の source）

```
- `M01_src.png`
A sealed plastic test pouch lying in a dark car trunk, held perfectly still a breath before a gloved hand enters frame to lift it, weak boot lamp, no person, no readable text [STYLE] Avoid: [NEG]
- `M02_src.png`
Ultra macro of pink liquid in a narrow glass tube poised motionless an instant before the first thread of cobalt blue begins to climb through it, backlit against black, no person, no readable text [STYLE] Avoid: [NEG]
- `M03_src.png`
A wet strip-mall parking lot at night with two lamp standards burning orange, the whole lot held still a moment before a light bar begins to strobe across the frame, no person, no readable text [STYLE] Avoid: [NEG]
- `M04_src.png`
A passenger's hands resting loosely in her lap in a moving car, poised in the last quiet second before the body tilts with a deceleration, sleeve cuffs plain, afternoon light across the knees, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M05_src.png`
An amber indicator lamp on the rear quarter of a pale sedan at dusk, held motionless a beat before it flashes, paint dulled and trim pitted, no person, no readable text [STYLE] Avoid: [NEG]
- `M06_src.png`
A driver's hands poised leaving a worn steering wheel and reaching toward the door handle, forearms tanned, the windscreen ahead filled with flat sky, hands only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M07_src.png`
A gloved hand poised at the edge of a dark car footwell an instant before a torch beam sweeps across the carpet pile, black nitrile, wrist only, no face, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
- `M08_src.png`
The sagging corner of a car headliner photographed from below, held still a moment before a hand presses the fabric back toward the roof panel, shadow in the cavity, no person, no readable text [STYLE] Avoid: [NEG]
- `M09_src.png`
A gloved hand holding a small glass tube of deep blue liquid at chest height, poised motionless a breath before it rises to eye level, orange streetlight flaring behind, no face, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
- `M10_src.png`
A transparent evidence sleeve lying flat on a car boot lid at night, held still an instant before a hand seals its adhesive strip, night air condensing on the plastic, no person, no readable text [STYLE] Avoid: [NEG]
- `M11_src.png`
A tow chain hanging slack from a recovery hook beside a sedan's front subframe on a night street, poised in the second before it snaps taut, macro on the steel, no person, no readable text [STYLE] Avoid: [NEG]
- `M12_src.png`
A woman seated alone on a bolted steel bench at the far end of a fluorescent corridor, held perfectly still a moment before she shifts her weight, small in a very large frame, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M13_src.png`
A grey painted steel door closed flush in a tiled institutional wall, held motionless a breath before the handle begins to turn, harsh overhead light and no shadow, no person, no readable text [STYLE] Avoid: [NEG]
- `M14_src.png`
A woman's hands poised to accept a ballpoint pen being held out across a plain counter, the exchange caught an instant before contact, hard overhead light, both faces out of frame, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M15_src.png`
A single standing figure at a courtroom lectern seen directly from behind, held motionless a beat before the shoulders drop on an exhale, the bench beyond in soft focus, no face, no insignia, no readable text [HSTYLE] Avoid: [HNEG]
- `M16_src.png`
A typed plea form on a table with a pen resting diagonally across it, poised an instant before a hand lifts the pen, every line of type an unreadable smear, cool north light, no person, no readable text [STYLE] Avoid: [NEG]
- `M17_src.png`
A woman's hands laid flat on a lectern shelf with the fingers spread, held perfectly still a moment before the smallest tremor passes through them, a crumpled tissue beside, hands only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M18_src.png`
A figure poised at the head of a courtroom centre aisle facing a set of doors, motionless a breath before the first step, a bailiff-shaped shape to one side, neither identifiable, no readable text [HSTYLE] Avoid: [HNEG]
- `M19_src.png`
A stack of household furniture at a kerb outside an apartment block, held still an instant before a gust lifts the corner of a dust sheet, cardboard going soft in the damp, no person, no readable text [STYLE] Avoid: [NEG]
- `M20_src.png`
A 1970s patent draughtsman's board with a technical drawing held under a hot lamp, poised a moment before the lamp arm swings and the shadows travel, annotations illegible, no person, no readable text [STYLE] Avoid: [NEG]
- `M21_src.png`
Macro of a hand-blown glass ampoule in a small flame, poised in the second before the neck begins to draw out into a thread, the flame reflected in the glass wall, no person, no readable text [STYLE] Avoid: [NEG]
- `M22_src.png`
An older man's hands on the lid of a hinged wooden sample case, poised motionless a breath before the catch turns and the lid comes down, sleeves rolled, hands only, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M23_src.png`
Macro of two liquid layers separating in a test tube, blue below and pink above, held perfectly still an instant before the meniscus between them settles into a knife edge, backlit against black, no person, no readable text [STYLE] Avoid: [NEG]
- `M24_src.png`
A deep supply-room shelf of hundreds of identical sealed pouches receding into shadow, poised a moment before a tray is drawn out from the middle of the stack, no person, no readable text [STYLE] Avoid: [NEG]
- `M25_src.png`
A heat sealer poised open above a strip of clear film on a packing table, the jaw an instant from closing, a bin of loose glass ampoules beside it, no person, no readable text [STYLE] Avoid: [NEG]
- `M26_src.png`
A gas chromatograph mass spectrometer standing against a laboratory wall, held still a beat before an indicator lamp changes state and the cooling fan spins up, no person, no readable text [STYLE] Avoid: [NEG]
- `M27_src.png`
A gloved hand poised above an autosampler tray of numbered wells with a small vial pinched between finger and thumb, an instant before it is seated, laboratory white light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M28_src.png`
A laboratory monitor showing a flat baseline trace on a pale grid, held motionless a breath before the first peak begins to rise out of it, all labelling illegible, no person, no readable text [STYLE] Avoid: [NEG]
- `M29_src.png`
An analyst seen from behind at a laboratory workstation, lab-coat shoulders motionless a moment before she leans in toward the screen, the monitor the only warm light, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M30_src.png`
A hand holding a fine pen a millimetre above a ruled field on a bench form, poised before the first stroke, a warm amber lamp pooling on the paper, hand only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M31_src.png`
A precision balance with its glass draught shield open and a single pale crumb on the pan, held perfectly still an instant before the display settles, cold white light, no person, no readable text [STYLE] Avoid: [NEG]
- `M32_src.png`
A woman's hands squaring a thick stack of identical form letters against a desk, poised a beat before the stack is tapped level, paper edges catching the light, hands only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M33_src.png`
A woman in a shop tabard seen from behind at an open chilled cabinet, held motionless a moment before she reaches in, cold light spilling onto her sleeve, back turned, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M34_src.png`
An outdoor bank of apartment mailboxes at dusk with one windowed envelope wedged in a slot, poised an instant before rain begins to spot the paper, nobody approaching, no person, no readable text [STYLE] Avoid: [NEG]
- `M35_src.png`
A man's laced hands resting still on an interview table beside a glass of water, poised a breath before the fingers unlace, plain jacket cuffs, soft window key, hands only, no likeness, no readable text [HSTYLE] Avoid: [HNEG]
- `M36_src.png`
The flat bonnet of a patrol vehicle in low morning light with dust across the paint, held still a moment before a shadow crosses it, a faint ring where something was set down, no person, no readable text [STYLE] Avoid: [NEG]
- `M37_src.png`
A figure at a window with hands clasped behind his back, silhouetted against a bright city view, held motionless a beat before the shoulders turn a few degrees, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M38_src.png`
A heavy panelled door in a state building standing a hand's width open onto a lit corridor, poised an instant before it swings closed, brass kickplate scuffed, no person, no readable text [STYLE] Avoid: [NEG]
- `M39_src.png`
A hand holding a signed sheet an inch above a small stack on a desk blotter, poised before it is laid down, the pen still in the fingers, warm amber lamplight, hand only, no face, no readable text [HSTYLE] Avoid: [HNEG]
- `M40_src.png`
A legislative chamber seen from the rear gallery with rows of empty desks, held still a beat before the overhead lights step up to full, daylight from a domed skylight, no person, no readable text [STYLE] Avoid: [NEG]
- `M41_src.png`
Extreme macro of a single pale crumb on a black surface, held perfectly still an instant before a breath of air stirs it a fraction, nothing else in frame, no person, no readable text [STYLE] Avoid: [NEG]
- `M42_src.png`
A sealed unopened test pouch on the vinyl bench seat of a patrol vehicle at dusk, the ampoule inside still pink, held motionless a moment before the door light dims, no marking anywhere, no person, no readable text [STYLE] Avoid: [NEG]
```

## 8.2 Wan 2.2 A14B の設定（★Known-good・この値を変えるな）

```python
POS_PREFIX = "cinematic documentary shot, subtle natural motion, "
POS_SUFFIX = ", slow deliberate camera move, shallow depth of field, film grain, photoreal, consistent lighting, no sudden changes"
NEG_PROMPT = ("static, motionless, blurry, low quality, distorted, deformed, extra limbs, bad anatomy, "
              "morphing face, flickering, jitter, warping, melting, text, watermark, identifiable face, "
              "real person likeness, child face, crying person, needle in skin, drug use, blood, wound, "
              "handcuffs, restrained person, badge number, agency seal")
```

## 8.3 実行手順（まず1本で通す・★42本は複数日）

```bash
./.venv/Scripts/python.exe ae-demo/comfy_wan.py --ep PD-2026-057-fieldtest --build
./.venv/Scripts/python.exe ae-demo/comfy_wan.py --ep PD-2026-057-fieldtest --run --shot M01
./.venv/Scripts/python.exe ae-demo/comfy_wan.py --ep PD-2026-057-fieldtest --run-all
```
> ★A1111 が起動していると VRAM を食う。`unload-checkpoint` で解放してから回す。**prefix の使い回しで出力が累積する罠**に注意（既存出力を必ず確認）。

## 8.4 RIFE で 48fps 化（`rife_fieldtest.py`・`rife_burge.py` と同手順）
先頭5フレームを落とし、41→164 フレーム（3.417秒）へ。**フレーム数のアサートを必ず入れる**（無言で短くなる事故が起きる）。

## 8.5 i2v の QC（目視5点）
1. 顔が生成されていないか（人物種でも顔は出さない）。2. 手指の破綻。3. 溶け・モーフィング。4. **標章が湧いていないか**（Wan は制服に勝手に記章を描くことがある）。5. **青い光が湧いていないか**（青は液体の中だけ・§4.6）。

---

# 9. A-6: 合成レイヤー（distinct 素材に数えない・ちょうど30本）

| type | 本数 | 採るもの |
|---|---:|---|
| `particle_assets` | 15 | 雨・アスファルトの飛沫・埃・紙の繊維・蒸気 |
| `light_assets` | 10 | sodium lamp haze・fluorescent flicker・torch beam・window shaft・headlight sweep |
| `vfx_overlays` | 5 | film grain fine／medium・halation soft・gate weave・dust on glass |

**規則:** overlay は `cuts[].src` に出さない。`blend_hint` は screen（particle/light）・overlay（vfx）。**cobalt blue の light を作らない**（§4.6）。強度は控えめ（screen-wash ≤0.07 を壊さない）。

---

# 10. A-7/A-8: staging とマニフェスト出力

## 10.1 Remotion public への staging（`scripts/stage_fieldtest_assets.py`）

```
remotion/public/fieldtest/img/     ← role=body の静止画210枚（★depth なし）
remotion/public/fieldtest/factory/ ← 選定アーカイブ .mp4/.jpg 252本（§4.4 の AR001..AR252 名で）
remotion/public/fieldtest/motion/  ← i2v M<NN>_rife.mp4 42本
remotion/public/fieldtest/overlay/ ← 合成レイヤー 30本（§4.6 の P/L/V 名で）
remotion/public/fieldtest/thumb/   ← thumb_face T01..T03（B の FieldtestThumbnails が参照）
```

**★命名規則（`check_asset_reuse.kind_of()` がパス文字列で分類する）:**
- アーカイブの `public_path` は必ず `fieldtest/factory/` の下（`/factory` を含む）— **ディレクトリ名は `factory` のまま、ファイル名の接頭辞だけ `AR`**（§4.4 の理由）
- i2v の `public_path` は必ず `.mp4` で終わり `_rife` を含む
- 静止画の `public_path` は `.png` で `/factory` も `ai_video` も `_rife` も含めない
- 合成レイヤーは `fieldtest/overlay/` に置き `cuts[].src` に出さない

## 10.2 権利台帳 `05_stock/stock_ledger.v001.json`
1行1素材で `asset_id` / `origin`（archive_ledger | ai_codex | i2v）/ `source` / `license` / `license_source_url_or_ledger_row` / `sha256` / `commercial_use` / `ai_disclosure_required` / `eyeballed_content` / `reviewed_at`。

## 10.3 境界契約マニフェストの出力
```bash
./.venv/Scripts/python.exe scripts/build_fieldtest_asset_manifest.py --ep PD-2026-057-fieldtest --build
./.venv/Scripts/python.exe scripts/build_fieldtest_asset_manifest.py --ep PD-2026-057-fieldtest --verify
./.venv/Scripts/python.exe scripts/stage_fieldtest_assets.py --ep PD-2026-057-fieldtest --verify
```

---

# 11. 素材反復禁止ゲートの実仕様（`check_asset_reuse.py`）

```python
MAX_USES_FACTORY = 1       # 設計 1.000
MAX_USES_MOTION  = 2       # 設計 2.000
MAX_USES_STILL   = 2       # 設計 1.081
MIN_FIRST_USE_SHARE   = 0.70   # 設計 0.8952
MAX_AVG_USES_PER_SOURCE = 1.4  # 設計 1.1171
```
加えて `check_footage_diversity`: distinct ≥0.40 / 同一素材の再利用 ≤4 / **汎用象徴 ≤2**（⚠ 天秤・ガベル・法典。§7.2 参照）。

---

# 12. 絶対にやらないこと

1. 実在人物の顔・肖像・likeness を作る。
2. 読める偽文書（検査票・答弁書・書簡・特許・州法・証拠袋ラベル）を作る。
3. 薬物使用（皮膚に刺さる注射針・吸引・服用・見せ場の粉末）を描く。
4. 血・傷・遺体・拘束された人物の苦悶を描く。
5. バッジ番号・所属章・機関シール・車両表記など**識別可能な標章**を描く。
6. 逮捕した警官を「悪役」として演出する（見下ろし・威圧・逆光ヒーロー構図）。
7. 塊を**食品として**提示する（皿・食卓・パン）。
8. テキサスが「禁止した」ように見える絵（×印・封印・停止標識）を作る。
9. コロラド法の**施行日**を絵にも文字にも出す。
10. `--variants 3` を使う／`_02` `_03` を作る／「複数枚から選ぶ」ために増産する。
11. `depth` map を作る／`depth_path` をマニフェストに書く。
12. `dochighlight` を成果物のどこかに書く。
13. `DATE_STAMP` / `SEAM_TRANSITION` を前提にした絵や指定を作る。
14. **生のフォルダ名でアーカイブを選ぶ**（40%誤ラベル・§7.5）／コンタクトシートを見ずに staging する。
15. `review_required` ライセンスの素材を staging する。
16. 素材棚のファイルを移動・改名・削除する。
17. QC 基準を自分で書き換えて通す。
18. 幕別の枚数・★HP 85枚・cuts 563 を独断で変える。

---

# 13. 完了報告に含めるもの

1. 生成枚数の実測（body / i2v種 / thumb_face / F系）と reject 件数・理由の内訳。
2. §3.3 の [1]–[13] を**自分で再計算した結果**（一致しなければ何が食い違ったか）。
3. アーカイブ252本の**幕別内訳**と、**コンタクトシートを何枚見たか**、落とした件数と落とした理由の上位5つ。
4. `search_archive.py` で実際に走らせたクエリの一覧（§7.3 に無いものを含む）。
5. EP39–EP56 との sha256 交差がゼロであることの出力。
6. i2v 42本の生成所要時間と失敗・再試行の記録。
7. `--verify` の出力（19不変条件すべて）。
8. staging 後の `remotion/public/fieldtest/**` の実ファイル数。
9. **未解決の懸念**（あれば正直に。無ければ「無し」と書く）。

**「動いたと思う」は完了ではない。ゲートが exit 0 を返して初めて完了。自分でQC基準を書き換えて通すのは禁止。**
