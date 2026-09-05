# EP33 tyler — アニメ成果物 出力マニフェスト（統合用・turnkey）

- **Episode:** PD-2026-033-tyler
- **担当:** アニメスレ（本話 = tyler のみ。EP34 rolin / EP35 hinders は別スレ。共有 `FigureBeats.tsx`/`Root.tsx` は両スレが編集するので pull→push 運用）
- **正典:** `EP33_tyler_ANIMATION_ASSETS.v001.md`（数値・tc・シーン帯の確定値）／`EP33_tyler_DESIGN.v001.md`
- **状態(2026-07-09):** ヒーロー6面 実レンダ完了・Remotion図5種 実装+検証完了。**上流(台本=別スレ / 画像=Codex)待ちで depth配線・本編統合は未着手。**
- **provenance:** Blender 5.1 / **EEVEE Next**（§2.2公認フォールバック・オーナー選択）/ レンダ 4K(3840×2160)→**1080p supersample** / row-6 `libx264 crf16 yuv420p bt709` / 決定論 `random.seed(1234)` / fps30 / invariant11（実在肖像なし・自案件データ数値のみ・生成物は再現で記録でない）。scripts commit=`579763d6`。

---

## 1. ヒーロー6面（Blender mp4 プレート・`OffthreadVideo` で差込）

出力先: `remotion/public/tyler/hero/<name>.mp4`（**public=gitignore のメディア**・リポジトリ非コミット）。
束ねレビュー: `remotion/public/tyler/hero/_ALL6_heroes_reel.mp4`（幕順・24.5s・映像のみ）。

| # | mp4 | 図の意味（入力データ/CLM） | 尺 | 差込tc / シーン帯 / シーン |
|---|---|---|---|---|
| 1 | `taxdebtmeter.mp4` | 税債務メーター `$15,000`（T5・CLM-0004）1:50 slam | 3.5s | T5 1:20登場/1:50 slam・Act1帯 0:24–3:40・S003–S009 |
| 2 | `equitybar.mp4` | 三段 `DEBT $15,000`/`SALE $40,000`/`SURPLUS $25,000`（T7・CLM-0004/0005）赤余剰4:50着弾 | 3.5s | T7 4:50・Act2帯 3:40–6:35・S010–S016 |
| 3 | `equitytheft_map.mp4` | 全米 home equity theft 集積（約8,000発光点=PLF"Est."規模の視覚表現・断定しない）（T11・CLM-0017） | 4.5s | T11 9:00・Act3帯 6:35–10:20・S017–S024 |
| 4 | `govtargument_fracture.mp4` | 郡の余剰保持論が物理崩壊（OL4・CLM-0006関連） | 4.5s | 13:20・Act4帯 10:20–14:20・S025–S031 |
| 5 | `magnacarta_scroll.mp4` | 余剰返還原則の源流・巻物unfurl（Magna Carta 1215・T15・CLM-0014A） | 4.5s | T15 14:40・Act5帯 14:20–19:00・S032–S038 |
| 6 | `votetally_bench.mp4` | 9–0 全員一致・9席同時発火（T18・CLM-0010・`598 U.S. 631`） | 4.0s | T18 ~18:15・Act5帯・S032–S038 |

**差込方針:** 各ヒーローは掴み/ペイオフの大きい一撃。`OffthreadVideo` で該当シーンの背景プレートとして、または `BrandOpening` 裏のコールドオープンに配置（invariant11=抽象生成映像）。数値グリフ（`$15,000`等）はヒーロー内に3D押し出しで焼込済＝図データ扱いで可。逐語テキスト/ロゴ/実在肖像は無し。

**再レンダ手順（1本）:** `blender -b -P remotion/src/blender/tyler_<name>.py -- <OUTDIR> 3840 2160 1 <frames> 64` → `npx remotion ffmpeg -framerate 30 -i <OUTDIR>/f_%04d.png -vf scale=1920:1080:flags=lanczos -c:v libx264 -crf 16 -pix_fmt yuv420p -colorspace bt709 -y public/tyler/hero/<name>.mp4`。frames: #1/#2=105・#3/#4/#5=135・#6=120。**EEVEEで各~6–15分。** ※`taskkill //IM blender.exe` は他スレのレンダを巻き込むので禁止（PID指定で個別kill）。※blender.exe/ffmpeg に MSYS `/c/` パスは通らない（`C:/` 形式必須）。

---

## 2. Remotion bespoke図 5種（`FigureBeats` の `kind` で差込・§5新規）

実装: `remotion/src/components/tyler/`（自スレ専用ディレクトリ）。配線: `FigureBeats.tsx` の union+dispatch（**共有ファイル**・EP34/EP35と同居・追加のみ）。プレビュー: `Root` の `TylerFigures` 合成。

| コンポーネント | FigureBeats kind | 入力/CLM | 差込tc / シーン |
|---|---|---|---|
| `EquityTheftTally`(2D companion) | `equitytheft` | `$780,000,000+`＋Est.PLF（CLM-0017） | T11 9:00・S017–S024（走行カウンタは2D側の役割） |
| `GovtArgumentCard` | `govtargument`{mode:'stack'\|'collapse'} | 郡の主張（CLM-0006関連） | 13:20・S025–S031 |
| `HallEquityLadder` | `hallladder`{showAmounts} | Hall `$1`→`$308k`→債務`$22,600`（CLM-0021） | Act3・S017–S024。**★裏取りゲート: CLM-0021 grade-A まで `showAmounts=false`（金額withheld・`verify_onscreen_text`照合対象）** |
| `SplitLadder` | `splitladder` | District→8th Cir→SCOTUS（CLM-0008） | 11:15再フック・S025–S031 |
| `OralArgQuestionTally` | `oralargtally` | 弁論の質問往復（CLM-0009関連） | 16:40・S025–S031 |

**残り13図**は `motionkit`/`carsearch` 既存部品を組立時に配線（`tax_debt_meter`→`RadialGauge`、EquityBar→`ComparisonBars` 等・§5再利用リスト）。二重実装しない。

---

## 3. まだ出来ないこと（依存ブロック・別スレ/Codex待ち）

- **depth実配線**: `asset_selection.v001.json`（68行台帳）と Codex画像68枚が未生成（画像はCodex担当）。生成後、depth対象238/539カットに `DepthStillHi` を付与。
- **本編統合・尺・最終受領**: 台本（別スレ）→シーン→画像 が揃ってから。`check_final_acceptance.py` は組立mp4を測定するので今は対象なし（自己申告完了は禁止）。
- **hero統合の実配線**: 上記が揃い次第、本マニフェストの tc に沿って `OffthreadVideo` 差込＋FigureBeats の `beats` 追記（機械的）。

---

## 4. スレ間の非干渉メモ
- 本話(tyler)アニメ = 本スレ専用。EP34(rolin/aircash)・EP35(hinders) = 別スレ。同じ題材の別話で**重複なし**。
- 共有 `FigureBeats.tsx`/`Root.tsx` は両スレが追記するため、**push前に必ず pull**。競合しやすいのはこの2ファイルのみ（各話のコンポーネントは別ディレクトリで衝突しない）。
