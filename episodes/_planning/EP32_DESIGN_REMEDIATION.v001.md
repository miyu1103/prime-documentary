# EP32 設計 是正台帳（v001 → v002 に向けて）

5人の敵対的批評（事実/リテンション・モーション・音・ゲート/レンダ・失敗モード網羅）の統合結果。
**正直スコア(v001)**: 事実6.5 / リテンション6.5 / モーション5 / 音4 / ゲート6 / レンダ5 / 失敗網羅7.5 / 決定論7。→ **≒60/100。100ではない。**
**根本原因（5人共通）**: 計画(motion budget / sound plan)もゲートも**実レンダに配線されず飾り**＝Goodhart。過去の「緑なのに紙芝居/薄い音/偽の緑」と同じ構造。**直し方＝プロンプト整形でなく"止める機構"をコードで実装**。

## BLOCKING（実装必須）
| ID | 領域 | 欠陥 | 修正（機構） | 担当ファイル |
|---|---|---|---|---|
| B1 | ゲート | 壊れ/未デコードのレンダで black/freeze/resolution/bgm/low_motion が例外時 **fail-open（緑）** | 例外時は **fail-closed(hard)** に統一（motion_energyと同様） | check_final_acceptance.py |
| B2 | ゲート | 「sha≠前回レンダsha」新鮮度が**文章のみ・未実装**＝クラッシュ→古い良品を掴む偽の緑が開いている | 前回sha保存＋**new sha≠prev かつ mp4 mtime≥レンダ開始時刻**でhard fail | check_final_acceptance.py / scheduler |
| B3 | モーション | 知覚予算(depth≥40/図≥6/ヒーロー≥2)は**手打ちJSONでコード検証ゼロ**（grepで参照0）→レンダが自由に乖離 | **pre-renderバリデータ**が remotion_plan＋film.json を読み、床未満でhard fail | 新規 preflight_render_gate.py |
| B4 | モーション | 図・ヒーローが**リビール後±0.5pxで実質フリーズ**（CarKeyLock 34秒静止等）＝コード化された紙芝居 | 各figure/heroにリビール後の**持続的二次モーション**（全体パララックス/ドリフト/スケール、YAVGに乗る振幅） | carsearch/*.tsx |
| B5 | 音 | サウンド計画は**孤児＝muxされず実動画に届かない**／実レンダの層を検査するhardゲート無し | 実ナレ基準の4層mix wavを生成→**最終muxの唯一音源**に配線＋**hard check_sound_layers**（実音のSFXトランジェント＋非音楽アンビ帯を検出） | 新規 build_case_film_audio.py + check_final_acceptance.py |
| B6 | 音 | SFXタイミングが**175wpmの推測**で実ナレ未使用→単語とズレる（invariant14: flashcrash builder再発明） | **narration_index.v001.json の実オフセットで再タイミング**（build_flashcrash_audio_v001.py を拡張/踏襲） | build_case_film_audio.py |

## MAJOR
| ID | 領域 | 欠陥 | 修正 | 担当 |
|---|---|---|---|---|
| M1 | モーション | motion_energyが**カット境界スパイクで嵩上げ**・p10床4.0が紙芝居平均3.5とほぼ同じ・体全体平均のみ | **カット±8フレーム除外の"within-shot"平均**＋**N秒窓の per-segment 床**＋p10床引上げ | check_final_acceptance.py / measure_motion_energy.py |
| M2 | モーション | 実ビルダーは depth **25%**（IMG_TREATで3/12）＝40%床未達・計画を読まない | IMG_TREATのdepth比≥40%化＋**計画のdepth割当を読む**・depthマップ欠落でfail | build_case_film_assets.py |
| M3 | 音 | アンビは**1ファイル全編ループ＆過ダッキングで実質無音**（coverage1.0は幻） | **章ごとにアンビ多様化**＋床≈-18dB＋ダッキング上限（VO下でも可聴）／密度ゲートは"distinctness"も採点 | build_case_film_audio.py |
| M4 | 音 | 台本の環境スウェル("bed/hum/pulse")が**捨てられる**／comma分割で二重ヒット・断片化 | スウェルをL3ゲイン自動化に**ルート**／1括弧=1キュー既定・0.5s内同一de-dup | build_case_film_audio.py |
| M5 | ゲート | 4K/深度の**前提がレンダ後確認**＝重レンダ後に発覚／画像0枚でresolution素通り | **pre-render preflight**で 全参照S0NN存在＋≥3840px＋各depthカットに_depth.png＋0枚→fail | preflight_render_gate.py |
| M6 | ゲート | 60-90秒プローブが**強制されない**（運用者記憶頼み） | `--probe`モードでスライス測定→**プローブ受領書を本レンダが要求** | check_final_acceptance.py / preflight |
| M7 | 事実 | 出典なし断定4件（"家の外で最長"/"毎日膨大"/"lazyback"/McReynolds理由＋Sutherland脱落）＝invariant1違反 | 4件を除去/claim準拠に修正・Sutherland補記 | script.en.v001.md |
| M8 | リテンション | フックが**約14秒(42語)**＝8秒スロット超過・OP遅延 | 冷開を~17語(~6-8s)に圧縮・残りをOPENINGへ | script.en.v001.md |
| M9 | 失敗網羅 | **設計にCAPTIONSセクションが無い**（owner最頻No.1/2の字幕不一致・変な切れ）／annotated要約版desyncの穴 | 設計に字幕章：**ElevenLabsマスターに強制整列・源は逐語narration_index（annotated要約は禁止）・息継ぎ単位・字幕=ナレQCゲート** | DESIGN v002 + gen_captions_forced.py |
| M10 | 素材 | asset_selectionが**S001-S009止まりのスタブ**／画像 40必要 vs 実在29／全参照存在チェック無し | 22 span全てにstill束縛・不足11枚を列挙してCodex生成・**存在preflight**（黒画面防止） | asset_selection.v001.json + preflight |
| M11 | 尺 | ナレ単独 **661s＝11.02分で690s床未満**（pauses依存が未指定） | 台本+60-90語 or **pause/music予算を明記**して床クリア・"~11分"表記を11.5-12.5に修正 | script + DESIGN v002 |

## MINOR（v002で反映）
p10床再較正 / プローブ体窓を本ゲートと一致 / 受領書を immutable v{NNN} / SFX同一多用に変種 / 2-pass loudnorm＆loudness hard化 / cut cadence直接床 or motion_energy代理を明記 / animation_density(=ship-gate床) vs motion_energy の関係明記 / depth%は全カット分母でも併記 / 独立プロース・レビューをゲート化(AI臭さ) / footage実配置数の床。

## 実装フリート（厳格ファイル所有・競合なし）→ 実装後に**再批評で検証（緑≠完了）**
FIX-1 ゲート堅牢化(check_final_acceptance.py, measure_motion_energy.py): B1,B2,M1,M6,MINOR / FIX-2 preflight新規(preflight_render_gate.py): B3,M5,M10,M6 / FIX-3 モーション部品(carsearch/*.tsx): B4 / FIX-4 ビルダーdepth(build_case_film_assets.py): M2 / FIX-5 音再配線(build_case_film_audio.py): B5,B6,M3,M4,MINOR / FIX-6 台本(script.en.v001.md): M7,M8,M11 / FIX-7 素材束縛(asset_selection.v001.json): M10。
最後にClaude: DESIGN v002 + 台本再QC/hash再束縛 + check_sound_layers配線確認 + 再検証。
