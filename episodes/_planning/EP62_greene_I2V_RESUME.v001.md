# EP62 greene — i2v 再開手順 v001

**2026-08-05 停止** · 対象 `PD-2026-062-greene` · **GPUを空けるために意図的に停止した。障害ではない。**

> **一行**：228枚中 **122本が完成済み**。残り **106本**（約10時間のGPU）。
> 再開は §3 のコマンド1本。**§5 の G043 の罠を先に読むこと。**

停止理由：出荷済み10話の再レンダーに4090が必要になった（Remotion WebGL）。
i2vは**中断しても1本も失われない**（フレームディレクトリ単位でレジューム）。

---

## 1. 停止時点の実測（2026-08-05）

| | 実測 |
|---|---|
| 完成クリップ `remotion/public/greene/motion/*.mp4` | **122本**（全て 5.03s / 121フレーム・欠損なし） |
| フレームディレクトリ `C:/Users/aab15/ae-demo/wan_frames_greene_*` | **123個**（うち121フレーム未満＝**0個**。中途半端なものは無い） |
| 中断中だった1本 | **痕跡なし**。`comfy_wan.py` は生成完了後にまとめてコピーするため、途中killでは何も残らない |
| 変換対象の総数 | **228枚**（`mandatory_stills` 224 ＋ サムネ4枚 G220/G221/G222/G240） |
| 残り | **106本** |
| ComfyUI | 停止済み。ポート8188にリスナー無し |
| GPU | `1504 MiB / 24564 MiB · 0%` = 空き |
| ロックファイル | `out_i2v_greene.lock` 削除済み |

**部分ファイルは1つも無い。** manifestスキャナが拾って困るものは残っていない。

---

## 2. 停止した時どのフェーズだったか

3フェーズの自己連鎖構成だった。**プロセスは全て停止済み**（ランチャー2本＋チェーン＋ワーカー＋ComfyUI）。

| フェーズ | 内容 | 状態 |
|---|---|---|
| phase2（人物あり 46枚） | `greene_people.txt` レジーム | ✅ **完了** |
| phase1-after（人物なし 177枚） | `greene_nopeople.txt` レジーム | ⏸ **ここで停止**。target=224 で走行中だった |
| phase3（人物あり 全50枚の取りこぼし回収） | 後から届いた G235/G237/G239/G240 用 | ⏸ **未実行** |

---

## 3. 再開コマンド

**プロンプトは3回改訂した末の確定版。絶対に「動くもの」を名詞で書かないこと（理由は §6）。**

再開スクリプトは下に全文を書く。`scratchpad` は消えている可能性があるので、
**このファイルの内容をそのままコピーして `.sh` を作り直すこと。**

```bash
#!/bin/bash
set -u
cd /c/Users/aab15/Documents/prime-documentary

# --- 変換対象リストを再生成（scratchpadが消えていても復元できる） ---
.venv/Scripts/python.exe - <<'PY'
import json, re, pathlib
img = {p.stem for p in pathlib.Path('remotion/public/greene/img').glob('G*.png')}
t = pathlib.Path('episodes/_planning/EP62_greene_CODEX_BATCH_A.v002.md').read_text(encoding='utf-8')
lines = t.splitlines(); briefs = {}
for i, l in enumerate(lines):
    m = re.match(r'^- .(G\d{3})\.png.\s*$', l)
    if m and i + 1 < len(lines): briefs[m.group(1)] = lines[i + 1]
PEOPLE = re.compile(r'\b(hand|hands|child|children|kid|boy|girl|man|men|woman|women|person|people|'
                    r'figure|silhouette|shoulder|arm|finger|clerk|officer|worker|tenant|resident|'
                    r'crowd|passer|walking|someone|his |her |their )', re.I)
ppl, nop = [], []
for g in sorted(img):
    if g == 'G043': continue                      # 恒久除外。§5 を読むこと
    b = briefs.get(g, '')
    (ppl if (b and PEOPLE.search(b)) else nop).append(g)
pathlib.Path('greene_people.txt').write_text(','.join(ppl))
pathlib.Path('greene_nopeople.txt').write_text(','.join(nop))
print('people', len(ppl), 'nopeople', len(nop))
PY

BASE_NEG="new object appearing, object entering frame, object flying into frame, something entering from the edge of frame, sudden appearance, text, lettering, words, writing, numerals, signage, logo, watermark, caption, subtitles, morphing, warping, deformed, extra limbs, bad anatomy, flickering, jitter, low quality, blurry, cartoon, illustration"

# 人物なしレジーム（G006/G008/G064 で検証済み）
P1="nothing enters the frame and nothing new appears in it, only what is already visible moves and it moves only slightly, light and shadow shift across the surfaces, the air stirs whatever is already there, the camera drifts almost imperceptibly, still-life documentary photography, natural available light, an empty place with no one in it"
N1="person, people, man, woman, child, human, face, head, hand, arm, finger, body, figure, silhouette, crowd, pedestrian, animal, dog, cat, bird, car, vehicle, bicycle, camera, lens, tripod, tool, equipment, $BASE_NEG"

# 人物ありレジーム（G002/G212/G213 で検証済み）
P2="nothing enters the frame and nothing new appears in it, only what is already visible moves and it moves only slightly, light and shadow shift across the surfaces, the air stirs whatever is already there, any person already in frame stays turned away from the camera and only breathes and shifts weight, the camera drifts almost imperceptibly, documentary photography, natural available light"
N2="person entering frame, new person, extra people, additional person, second figure, crowd, pedestrian walking, face turning toward camera, visible facial features, recognisable face, animal, dog, cat, bird, car, vehicle, bicycle, camera, lens, tripod, $BASE_NEG"

count_done(){ local n=0; for d in /c/Users/aab15/ae-demo/wan_frames_greene_*; do [ -d "$d" ] || continue
  [ "$(ls "$d"/*.png 2>/dev/null | wc -l)" -ge 40 ] && n=$((n+1)); done; echo "$n"; }

# --- phase A: 人物なしの残り ---
TA=$(.venv/Scripts/python.exe -c "
import glob,os
done={os.path.basename(d).replace('wan_frames_greene_','') for d in glob.glob('C:/Users/aab15/ae-demo/wan_frames_greene_*') if os.path.isdir(d) and len(glob.glob(d+'/*.png'))>=40}
want=set(open('greene_nopeople.txt').read().split(','))
print(len(done|want))")
I2V_PROMPT="$P1" I2V_NEG="$N1" I2V_SEED_BASE=5100 \
  bash scripts/_chain_i2v_robust.sh greene "$TA" G 12 "$(cat greene_nopeople.txt)" 121

# --- phase B: 人物ありの取りこぼし（G235/G237/G239/G240 など） ---
TB=$(.venv/Scripts/python.exe -c "
import glob,os
img={os.path.basename(p)[:-4] for p in glob.glob('remotion/public/greene/img/G*.png')}
print(len(img)-1)")   # -1 = G043 は恒久除外
I2V_PROMPT="$P2" I2V_NEG="$N2" I2V_SEED_BASE=7300 \
  bash scripts/_chain_i2v_robust.sh greene "$TB" G 12 "$(cat greene_people.txt)" 121

py -3.11 scripts/assemble_episode_i2v.py --slug greene
# ★ manifest を作る前に §5 を実行すること
```

**必ず `--length 121`。** 81フレーム(3.37s)だと平均4.6秒のカットの中で `<Loop>` が
巻き戻り、全モーションカットに毎回ジャンプが出る（`CaseFilm.tsx` L116-120）。

**ディスク**：1本あたり約136MB（`wan_frames`）＋同量の一時ファイル。
残り106本で約15GB。`ComfyUI/output/wanout` を定期的に掃除しないと詰まる
（フレームは `ae-demo/wan_frames_*` にコピー済みなので消して安全）。

---

## 4. 再開前の確認

```bash
nvidia-smi                                    # 4090が空いていること。Remotionレンダーと同時に走らせない
ls remotion/public/greene/motion/*.mp4 | wc -l  # 122 のはず
ls out_i2v_greene.lock                        # 無いこと（あれば古い残骸なので消す）
```

---

## 5. ★ G043 の罠（必ず読む）

`G043` = 床板の上に置かれた紙を**真上から**撮ったプレート。
**2回連続で「左から腕と手が伸びてきて紙を拾う」** 映像になった（人物禁止のネガティブを効かせても）。
構図そのものが「誰かが拾おうとしている」画の事前分布を持っているためで、プロンプトでは直らない。

**判断：G043 は静止画のまま使う。**`mandatory_stills` には残る（PNGがカットに出れば
`check_spec_satisfied.py` の stem 照合を満たす）。予算も足りる：

> 227 motion ＋ 9 factory = **236** ≥ 契約の `distinct_video_assets` **234**（あと2枚まで同様に諦められる）

**やること：**

1. §3 のリスト生成スクリプトは **G043 を除外済み**なので、再開しても再生成されない。
2. **停止時点で `G043` のフレームディレクトリだけが残っている**
   （`C:/Users/aab15/ae-demo/wan_frames_greene_G043`・121フレーム）。
   `G043.mp4` は既に削除済みだが、**`assemble_episode_i2v.py` を実行すると
   このフレームから G043.mp4 が再生成される。**
3. したがって **最後の assemble の後・manifest を作る前に必ず：**

```bash
rm -f remotion/public/greene/motion/G043.mp4 "H:/pd-media/assets/ai_video/greene/motion/G043.mp4"
py -3.11 scripts/build_asset_manifest_motionfirst.py --slug greene
```

フレームディレクトリ自体は「消すな」と指示されているので残してある。
消さない限りこの再生成は毎回起きる。**assemble のたびに上の rm を打つこと。**

---

## 6. プロンプトを勝手に変えないこと（3回失敗した記録）

| 版 | 変更点 | 結果 |
|---|---|---|
| v1 | *"paper lifts and settles, dust turns, fabric and foliage stir"* と**動くものを名詞で列挙** | 13本中2本が**被写体を捏造**。G006(コンクリ壁)に女性の頭が4.09秒に出現、G008(レンガ壁)にカメラと手が4.72秒に出現 |
| v2 | v1＋人物禁止の強いネガティブ | 人は消えたが、G006/G008/G003 が揃って**大きな白い紙を捏造して飛ばした**。禁止しても**捏造先が移っただけ** |
| **v3（確定）** | **物の名前を一切書かない。「どう動くか」だけ書く** | G006/G008 が清潔になり、しかも**動き量は増えた**（2.08/1.99）。紙が実在する G064 は紙を保ったまま清潔 |

**原因は発注側（プロンプト）にあった。**名詞を書くと、その物が写っていないプレートに
モデルがそれを**生成してしまう**。v3は名詞を1つも含まない。

**捏造は必ずクリップの最後の1〜3秒に出る。**中間1フレームのサムネでは100%見逃す。

---

## 7. 残っている必須作業（GPU不要）

- **全224本の目視レビューが出荷前の必須ゲート。** 自動化は試して**失敗した**：
  肌色検出のスクリーナーを書いたが、実物の腕侵入(G043)を92本中76位・スコア0.00で**見逃し**、
  目視で清潔と確認済みのレンガ壁(G008)を1位に**誤検出**した。
  この映画の色調（暗く彩度の低い1970年代の内装）ではレンガも床板も肌色と区別できない。
  **動き量スコアは内容の正しさを一切予測しない**（G043=0.29「低」で侵入あり／G223=3.30「高」で完全に清潔）。
- 1クリップあたり**8フレームを1枚のシートに並べて**見ること（`i2v_qc.py` 方式）。
- 既知の判定：**清潔 30本（目視済み）／却下 4本（G003,G006,G008 は再生成して解決・G043 は静止画へ退避）／
  動き量が低い 26本**（内容は正しい。最後にまとめて別シードで振り直す候補）。

---

*v001 · 2026-08-05 · GPU解放のため停止。この文書に書いていない数字は測っていない数字。*
