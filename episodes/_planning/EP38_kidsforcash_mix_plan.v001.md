# EP38 — Kids for Cash — 音の割当表 / Mix Plan v001

> 4層ミックス（VO＋ダッキングBGM＋定常アンビエンス＋SFX）。Florenceの確立手法を踏襲。
> 時間位置はナレ実測（`06_audio/narration_index.v001.json`）。ナレ区間: HOOK 0–27.9 / ACT1 27.9–137.3 / ACT2 137.3–257.6 / ACT3 257.6–335.9 / ACT4 335.9–478.1 / ED 478.1–531.6（計 531.6s＝8.9分）。
> ※完成タイムラインは OP(3.5s) を先頭に被せ、SFXの正確な発火は whisper 語タイミング（`word_timings.v001.json`）で最終ロックする。以下は幕単位の確定分。
> 全素材=権利追跡済みライブラリ（`H:/pd-media/library/`）＋Florence流用SFX（`remotion/public/florence/sfx/`）。読み取り専用参照。

## 1) 全体ミックス方針（Florence踏襲・binding）
- VO=フラット（主役）。BGM=VOでサイドチェイン・ダッキング（GR 9〜12dB、VO無音で回復）。アンビエンス=定常 −18dB（ダッキングしない）。SFX=VOより −5〜−9dB。
- 仕上げ=**2パス loudnorm I=−14 / TP=−1.5 / LRA=11**（配信ラウドネス）。
- ショートと違い**終始一定音量**（中盤ドロップ厳禁）。

## 2) BGM（幕ごと・感情の弧／vol は素材音量）
| 区間 | 秒 | トラック（library/music/…） | vol | 意図 |
|---|---|---|---|---|
| HOOK | 0.0–27.9 | hook/mus_20260614_hook_glass_air_bed_v1.mp3 | 0.30 | 不穏な静けさ・問いの提示 |
| ACT1前半 | 27.9–82.0 | opening/mus_20260614_opening_measured_arpeggio_v1.mp3 | 0.24 | 普通の日常・淡々 |
| ACT1後半 | 82.0–137.3 | tension_build/mus_20260614_tension_build_courtroom_horizon_v1.mp3 | 0.22 | 8.4%/placement で不安が立つ |
| ACT2前半 | 137.3–210.0 | tension_build/…_courtroom_horizon_v2.mp3 | 0.22 | 金の流れ・仕組みの解剖 |
| ACT2後半 | 210.0–257.6 | reveal/mus_20260614_reveal_hidden_system_clicks_v1.mp3 | 0.22 | "inventory/機械" の露見 |
| ACT3 | 257.6–335.9 | somber/mus_20260614_somber_ledger_of_ash_v1.mp3 | 0.18 | **開始はドライ**・喪失・沈黙（最小限） |
| ACT4前半 | 335.9–430.0 | reveal/…_hidden_system_clicks_v2.mp3 | 0.22 | 暴露・追及 |
| ACT4後半 | 430.0–478.1 | reveal/mus_20260614_reveal_verdict_at_dawn_v1.mp3 | 0.24 | 判決・司法が司法を裁く |
| ED | 478.1–531.6+ | outro/mus_20260614_outro_last_frame_v1.mp3 | 0.24 | 余韻・エンドカードを運ぶ（切りよく終える） |
- 各トラック: fade-in 1.5s / fade-out 2.0s。継ぎ目は前トラックのfade-outと次のfade-inを重ねる。

## 3) アンビエンス（定常 −18dB・ダッキングなし）
| 区間 | ファイル（library/ambience/…） | 意図 |
|---|---|---|
| HOOK | amb_tension_drone.mp3 | 冷たい緊張 |
| ACT1 | amb_empty_hallway.mp3 →(115付近) amb_institutional_drone.mp3 | 学校→施設の空気 |
| ACT2 | amb_institutional_drone.mp3 | 制度・建物の冷たさ |
| ACT3 | amb_night_window.mp3 | 家・夜・喪失 |
| ACT4 | amb_courtroom_room_tone.mp3 | 法廷 |
| ED | amb_light_wind.mp3 | 開けた余韻 |
- 22s前後のベッドを `aloop` でループ、各切替で1.0s/1.5sのフェード。

## 4) SFX ワンショット（−5〜−9dB・**発火時刻は語タイミングで最終ロック**）
Florence流用（`remotion/public/florence/sfx/`）を割当。時刻は該当語（whisper）に合わせて後確定。
| 語/ビート（区間） | SFX | 目安gain | メモ |
|---|---|---|---|
| "three months"〔3 MONTHS〕(HOOK) | receiptstamp.wav | −6 | カード打刻 |
| "signature/waiver"〔WAIVER〕(ACT1) | receiptstamp.wav | −6 | 署名＝放棄の打刻 |
| "side door" 連行 (ACT1) | door1.wav | −7 | 側扉が閉まる |
| "for-profit jail" 施設 (ACT2) | door2.wav | −7 | 施設の扉 |
| "two point eight million"〔$2.8M〕(ACT2) | receiptstamp.wav | −6 | 金額カード＋"FINDER'S FEE→BRIBE"打刻 |
| "hundreds/machine"〔MechanismReveal〕(ACT4) | drawer.wav | −9 | 記録を引き出す |
| "vacating thousands"〔THOUSANDS VACATED〕(ACT4) | drawer.wav | −8 | 記録抹消 |
| "twenty-eight" 判決 (ACT4) | verdict_tone.wav | −8 | 判決トーン |
| 判決の決め（ACT4） | verdict_seam.wav | −5 | スラム／転回 |
- **新規SFXが要るもの（未所持・要生成/取得）**: 静かな法廷の木槌（gavel soft）1点あると判決が締まる。無ければ verdict_tone で代替。→ SFX生成リストに1件のみ計上。

## 5) 実装メモ（次工程）
- ミックスは Florence の `build_florence_audio.py` を EP38 用に複製（`build_kidsforcash_audio.py`）＝入力パス・区間・SFX時刻を本表で差し替え。VO=`remotion/public/kidsforcash/narration_master.mp3`。
- SFX時刻は `word_timings.v001.json`（whisper）確定後にロック → G-TIME 系で語同期±1フレーム検算。
- 出力=`08_edit/kidsforcash_audio_mix.v001.wav`（2パスloudnorm）。映像とは別muxで。
- 素材の存在チェック（欠品で停止）→ 全入力の存在を先に assert（docs/42 G-CAP-2 の思想）。
