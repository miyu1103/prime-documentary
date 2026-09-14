# EP80 concordia — i2v 納品

差出: i2v レーン / 2026-08-27
発注: `docs/handover/EP78_82_TO_I2V.md`

---

## 1. 納品

```
remotion/public/concordia/motion/            181本   ← プールに入れてよい分
remotion/public/concordia/motion/rejected/     1本   ← N001（下記 3.）
motion/ の *_depth                              0本
```

検査:

```
py -3.11 scripts/check_motion_saturation.py --slug concordia
  → 181 clip(s) measured, 0 losing colour, 0 with black    exit 0
```

すべて 1920x1080 / 30fps / 3.4秒。カットが約4.6秒なら1回ループします（EP77 と同じ）。

## 2. 目視QC — 182本すべて、元プレートと1対1で対照しました

**湧いた被写体は0件です。**

`scripts/qc_i2v_tail_vs_plate.py`（今回作成）で、各クリップの終端フレームを元プレートの
真下に貼ったシートを23枚出し、全数を人が見ました。成果物は
`runs/qc/concordia_tail_vs_plate*/`（`index.txt` にセル→stem の対応）。

人が写っている TAIL は N042 / N049 / N062 / N091 / N121 / N130 / N146 / N151 / N152 /
N153 / N155 / N156 ですが、**すべて元プレートに同じ人がいます**。増えたように見えた
N098・N099 は高解像で再確認し、ベンチも人影もプレート由来でした。

## 3. N001 を motion/rejected/ に退避しました

そちらが `img/rejected/` に移した3枚（**N001 / N104 / N141**）のうち、N001 だけ
すでにクリップができていました。`img/rejected/` と同じ約束で
`motion/rejected/N001.mp4` へ移してあります。**削除していません。**
N104 と N141 は動画化前だったので、もともと存在しません。

`img/` と `factory/` には一切触れていません。

## 4. 未納が1枚あります: N093

ComfyUI がプロンプトを受理しながら **`output/wanout` に1ファイルも書かない**板です。
600秒 × 2回を捨てたので `runs/qc/i2v_quarantine_concordia.txt` に隔離しました。
原因は未特定。**残り4話が終わったあと（8/28 夜）に seed を変えて単発で振り直します。**

`i2v_quarantine_concordia.txt` には N122 も載っていますが、**N122 はその後の周回で成功して
おり、クリップは存在しQCも通っています。** 隔離ファイルは「再試行しない」ためのもので、
納品可否の台帳ではありません。納品可否は motion/ の現物で判断してください。

## 5. EP77 の作り直しに効くかもしれない実測

**concordia は既定プロンプトでは生成していません。** 稼働中の `comfy_wan.py` の
コマンドラインを直接読んで確認した実測です。

```
--prompt "the scene stays exactly as it is, only ambient motion: haze and air drift slowly,
          water surface ripples, light flickers gently, a very slow subtle camera push-in,
          archival documentary footage, nothing new enters the frame"
--neg    "new person, people appearing, man appearing, woman appearing, human face, crowd,
          walking figure, silhouette of a person, animal, bird, dog, vehicle entering frame,
          new object appearing, text, lettering, caption, subtitle, watermark, logo,
          signature, readable writing, morphing, warping, deformed, extra limbs, bad anatomy,
          cartoon, illustration, low quality, jitter, scene change, cut to another shot,
          <話数ごとの禁止対象>"
```

話数ごとの追加分は `episode_spec.v001.json` の `forbidden_subjects` から起こしています
（concordia なら capsized ship / listing ship / collision / sinking ship / rescue boat /
person in the water …）。

keybridge は組み込みの `SCENE_PROMPT`（"atmospheric living environment"）＋既定 neg
（"static, motionless" を否定）のままで、人物混入 30/112 = **27%**。
concordia は上記で **0/182**。母数が違うので断定はしませんが、差はここだと見ています。
定義は `scripts/_chain_i2v_ep78_82.sh` の `BASE_PROMPT` / `neg_for()` にあります。
そのまま `I2V_PROMPT` / `I2V_NEG` に渡せます。

## 6. そちらの工程

発注書の手順そのままです。

1. `build_asset_manifest_motionfirst.py --slug concordia`
2. 追加の reject があれば一覧をください。`motion/rejected/` に退避します（N001 と同じ扱い）
3. `build_case_film_generic.py`
4. `remotion/src/Root.tsx` に `Ep80Concordia` を登録
5. `check_episode_inputs.py --slug concordia`

## 7. 残り4話

順に自動で流れています。8/27 09:54 実測で **3.0分/本**。

| slug | 見込み |
|---|---|
| 81 station | 8/27 17:00 |
| 82 valdez | 8/28 02:10 |
| 78 colgan | 8/28 10:30 |
| 79 alaska261 | 8/28 20:20 |

各話とも同じ全数プレート対照QCを通してから出します。
**GPU を使う予定があれば先に言ってください。** ロックは見ていますが、待った時間はそのまま
遅れになります（EP77 で通算10時間ぶん後退しました）。
