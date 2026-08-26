# i2v レーン 2026-08-26 — EP77 keybridge 納品完了

## LIVE STATE（実測）

    remotion/public/keybridge/motion/           112 mp4
    E:\pd-media\assets\ai_video\keybridge\motion 112 mp4（pub とバイト全数一致）
    *_depth in motion/                          0
    frame dirs (ae-demo/wan_frames_keybridge_*) 全て 81 png
    check_motion_saturation --slug keybridge    exit 0

## 納品

115枚中 **112本**。`img/` と `factory/` は未変更（判定台帳のハッシュは有効）。

落とした3枚 **H062 / H065 / H084**: 色で始まり灰色で終わる（chroma 19.3→7.5 等）。
フレーム81枚に混入なし・再アセンブルでバイト同一 → Wan の生成自体が退色。救済不可。
処置は発注書§5の2手セット済み:
  1. フレームディレクトリを ae-demo の外（runs/qc/keybridge_rejected_frames/）へ移動（改名せず）
  2. config/footage_blocklist.v001.json の blocked に episodes:["keybridge"] で登録

## 踏んだ罠2つ（次に i2v を回す人は必ず読むこと）

**1. i2v は元プレートに無い人物を生成する。112本中30本（27%）。**
無人の会議室にスーツの男／無人の法廷ベンチに2人／コンクリート橋桁だけの絵に男／
設計図のホワイトボードに女性。発注書§4が警告していたとおり。
**check_motion_saturation は緑のまま**（色しか測らない。ツール自身が
"This says nothing about what the clips SHOW" と出力する）。
対処: 人物禁止のネガ＋「新しい被写体は入らない、動くのは空気と光だけ」で30本を再生成し、
全ペアを元プレートと同順のコンタクトシートで目視して解消を確認。
  ネガ: person, people, human, man, woman, figure, crowd, face, hand, hands, arm, arms,
        worker, pedestrian, new object appearing, （以下 既定の static/blurry 系）
  プロンプト: the scene stays exactly as it is and no new subject enters the frame,
        only air and light move: fog drifts slowly, water ripples, reflections shimmer,
        lamps flicker faintly, a very slow subtle camera push

**2. 作り直しが2回とも「成功」を返しながら中身が古いままだった。**
原因が2つ重なっていた:
  - ComfyUI/output/wanout/ に前回のフレームが 11,745枚 残り、frame dir が 81×2=162枚 になって
    組み立てが古い方の81枚を拾っていた
  - E:\pd-media\assets\ai_video\<slug>\motion\ に前回の mp4 が残り、assemble_episode_i2v は
    そこをマスターとして扱うため、新規作成せず古いマスターを render 側へコピーしていた
どちらも「assembled=N / failed=0」と緑を返す。
**気づけたのは出来上がった mp4 のバイトサイズが旧版と完全一致していたから（925117 = 925117）。**
→ 作り直す前に wanout と E: のマスターを両方空にする。完了後に必ず旧版とバイト比較する。

## 限界（正直に）

人物湧きの検出は**目視**。112本を2枚のコンタクトシートで見て30本を挙げた。機械の検出器は無い。
小さく写ったものの見落としはありうる。本編に組んだ後、もう一度誰かの目で見ること。

## 次

1. build_asset_manifest_motionfirst.py --slug keybridge
2. build_case_film_generic.py --config .../EP77_keybridge_filmconfig.v001.json
3. Root.tsx に Ep77KeyBridge 登録
4. check_episode_inputs.py --slug keybridge
動く素材 = 実写42 + motion112 = 154本（発注書の必要数110本を満たす）。

**未着手: H132〜H147 の16枚の i2v。** 設計レーンが4K化＋深度を投入済みで、完了合図待ち。
合図が来たら約55分。最初から上記の人物禁止プロンプトで回すこと。

## EP78-82 レーンへ

EP77 を先に通すため **_chain_i2v_ep78_82.sh と concordia のチェーンを停止した**（オーナー判断）。
concordia は 84/185 でクリーン停止・不完全 frame dir 0・resume 可。
再開手順: runs/qc/EP78_82_QUEUE_PAUSED.md
**再開前に: concordia の既存84本は keybridge と同じ既定プロンプト。keybridge は27%で人物が湧いた。
残り101本を回す前に既存84本を元プレートと突き合わせること（5分で測れる）。**
