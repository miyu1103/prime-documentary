# Motion Design Language（モーション設計言語：30 grammar 定義）

> ステータス: 設計（未実装）。本書は語彙定義のみ。コンポーネント本体は未生成。
> 実装は `docs/remotion-animation-component-roadmap.md` の Phase 順。

## 前提・仮定

- 対象: Remotion v4 / 1920×1080 @ 30fps。尺は frames（30frames = 1.0s）で表記。
- ブランド色/フォントは `remotion/src/brand.ts` `BRAND` を参照（再定義しない）。
- 「推奨コンポーネント」列は `src/motion/*`（=`remotion/src/motion/*`）の新ラッパ、または既存 `remotion/src/components/*` を指す。
- 「既存実装で出来る／要実装」の判定:
  - **出来る（ラップのみ）**: 既存プリミティブをそのまま使える。
  - **要・依存導入**: `@remotion/three|lottie|transitions` / `three` 等の未導入依存が前提（Phase4・導入後）。
  - **要・新規ロジック**: 既存に対応物がなく新規アルゴリズムが要る（依存は不要）。
- SFX 音源・素材は権利クリア済み前提（メモリ feedback_rights_check_before_download）。実パスは episode 側が保持。
- 推奨尺は「単独の効果尺」の目安であり、シーン全体尺ではない。

## 30 motion grammar 概観（実装状態）

| # | grammar | 実装状態 | 主担当コンポーネント |
|---|---------|----------|----------------------|
| 1 | slow_push_in | 出来る（Motion CameraRig） | camera/CameraRig |
| 2 | fast_push_in | 出来る（CameraRig intensity） | camera/CameraRig |
| 3 | pull_out | 出来る（CameraRig 反転） | camera/CameraRig |
| 4 | subtle_shake | 要・新規ロジック（軽微） | camera/CameraRig |
| 5 | impact_zoom | 要・新規ロジック | camera/CameraRig + text/ImpactTitle |
| 6 | parallax_depth | 出来る（Parallax 済） | visual/ParallaxScene |
| 7 | keyword_punch | 出来る（KineticType 活用） | text/KeywordPunch |
| 8 | quote_typewriter | 出来る（OpenCaption 活用） | text/QuoteReveal |
| 9 | number_countup | 要・新規ロジック | text/NumberCounter |
| 10 | evidence_reveal | 出来る（SceneArt+Telop 合成） | layout/EvidenceBoard |
| 11 | timeline_flow | 出来る（SceneArt Timeline 活用） | layout/TimelineReveal |
| 12 | map_focus | 出来る（SceneArt MapUS 活用） | layout/MapFocus |
| 13 | card_stack | 要・新規ロジック | layout/MotionCard |
| 14 | light_sweep | 出来る（Motion LightSweep） | visual/LightSweep |
| 15 | particle_drift | 出来る（Motion Particles） | visual/ParticleField |
| 16 | data_reveal | 要・新規ロジック | layout/DataReveal |
| 17 | hard_cut | 出来る（Series 並置） | transitions/MotionTransition |
| 18 | flash_transition | 出来る（新規だが依存不要） | transitions/FlashTransition |
| 19 | whip_transition | 要・新規ロジック（または @remotion/transitions） | transitions/WhipTransition |
| 20 | glitch_transition | 要・新規ロジック | transitions/GlitchTransition |
| 21 | silent_hold | 出来る（尺と無音のみ） | layout/* + audio/SfxScheduler（無音） |
| 22 | cinematic_drift | 出来る（CameraRig 低 intensity） | camera/CameraRig |
| 23 | foreground_blur_pass | 要・新規ロジック | visual/* + camera/CameraRig |
| 24 | panel_float | 要・依存導入（@remotion/three） | three/FloatingPanels3D |
| 25 | depth_dolly | 要・依存導入（@remotion/three, three） | three/DepthStage |
| 26 | ambient_overlay | 出来る（grade/atmosphere 共通化） | visual/AtmosphereOverlay |
| 27 | diagram_draw | 出来る（DiagramFlow 活用） | layout/* + DiagramFlow |
| 28 | relationship_connect | 要・新規ロジック | layout/RelationshipMap |
| 29 | title_slam | 出来る（KineticType+CameraRig） | text/ImpactTitle |
| 30 | soft_reveal | 出来る（opacity/blur 補間） | text/* + layout/* |

凡例: 難易度 低 / 中 / 高。尺は frames。SFX/VFX/素材は preset 既定の目安。

---

## 1. slow_push_in
| 項目 | 内容 |
|---|---|
| 目的 | 静止素材に生命と没入を与え、語りに引き込む |
| 視聴者の印象 | 落ち着き・重み・「映画を観ている」感 |
| 向く sceneType | explanation, character_profile, place_intro, emotional_pause, quote |
| 向かない sceneType | flash 的な turning_point の瞬間、hard_cut 連打の場面 |
| 推奨尺 | 90–300 frames（連続的、シーン全尺に重ねる） |
| 推奨 SFX | 低音アンビエンス（持続）、ほぼ無音 |
| 推奨 VFX | grain 0.05, vignette, light_sweep 薄め |
| 推奨素材 | 写真・AI 静止画・場面アート |
| 推奨コンポーネント | camera/CameraRig（既存 Motion CameraRig） |
| 実装難易度 | 低 |
| 乱用リスク | 全カット push-in だと単調・眠い |
| 品質基準 | スケール変化が滑らか・端で破綻しない・被写体中心が動かない |

## 2. fast_push_in
| 項目 | 内容 |
|---|---|
| 目的 | 注意を一点に急速集中、緊張を上げる |
| 視聴者の印象 | 緊迫・「来る」予感 |
| 向く sceneType | turning_point, problem_statement, opening_hook |
| 向かない sceneType | emotional_pause, summary |
| 推奨尺 | 12–30 frames |
| 推奨 SFX | riser / impact 直前のスウェル |
| 推奨 VFX | 軽い motion blur 風、vignette 強め |
| 推奨素材 | 顔・象徴オブジェ・新聞見出し |
| 推奨コンポーネント | camera/CameraRig（intensity 高） |
| 実装難易度 | 低 |
| 乱用リスク | 多用で酔う・安っぽい |
| 品質基準 | 終点で完全停止し次カットへ繋がる・行き過ぎない |

## 3. pull_out
| 項目 | 内容 |
|---|---|
| 目的 | 文脈・全体像の開示、関係性の俯瞰 |
| 視聴者の印象 | 納得・俯瞰・解放 |
| 向く sceneType | summary, place_intro, company_profile, ending |
| 向かない sceneType | turning_point の頂点 |
| 推奨尺 | 60–180 frames |
| 推奨 SFX | 解放感のあるアンビエンス、軽い whoosh 開始 |
| 推奨 VFX | vignette 弱め、light_sweep |
| 推奨素材 | 俯瞰写真・地図・建物 |
| 推奨コンポーネント | camera/CameraRig（反転 push） |
| 実装難易度 | 低 |
| 乱用リスク | 引きすぎて被写体が小さく無意味化 |
| 品質基準 | 開始の主題が読める→全体が読める、の順で破綻なし |

## 4. subtle_shake
| 項目 | 内容 |
|---|---|
| 目的 | 手持ち感・現実感・不穏さの付与 |
| 視聴者の印象 | 臨場感・緊張・ドキュメンタリーらしさ |
| 向く sceneType | reenactment, turning_point, problem_statement |
| 向かない sceneType | data_reveal, chapter_title（可読性低下） |
| 推奨尺 | 30–120 frames |
| 推奨 SFX | 環境音・心拍系 |
| 推奨 VFX | grain やや強め |
| 推奨素材 | 写真・AI 動画見せ場 |
| 推奨コンポーネント | camera/CameraRig（seed ノイズ追加・新規ロジック） |
| 実装難易度 | 中 |
| 乱用リスク | 揺れすぎは安っぽく・視聴困難 |
| 品質基準 | 揺れ幅が小（数 px）・決定論的・テキスト可読性を保つ |

## 5. impact_zoom
| 項目 | 内容 |
|---|---|
| 目的 | 衝撃の瞬間を強調、句読点的な強打 |
| 視聴者の印象 | ハッとする・断定 |
| 向く sceneType | turning_point, opening_hook, problem_statement |
| 向かない sceneType | emotional_pause, summary |
| 推奨尺 | 6–18 frames |
| 推奨 SFX | impact hit + 低音ドン |
| 推奨 VFX | 一瞬の vignette 収縮、軽 flash |
| 推奨素材 | キーワード・顔・数字 |
| 推奨コンポーネント | camera/CameraRig + text/ImpactTitle |
| 実装難易度 | 中 |
| 乱用リスク | 連発で陳腐・刺激過多 |
| 品質基準 | SFX とフレーム一致（preset の同一 frame 駆動）・残像なし |

## 6. parallax_depth
| 項目 | 内容 |
|---|---|
| 目的 | 平面素材に 2.5D の奥行きを与える |
| 視聴者の印象 | 立体感・上質さ |
| 向く sceneType | place_intro, explanation, chapter_title, abstract_emotion |
| 向かない sceneType | data_reveal（情報が動きすぎる） |
| 推奨尺 | 90–240 frames |
| 推奨 SFX | アンビエンス |
| 推奨 VFX | light_sweep, particle_drift |
| 推奨素材 | 多層分離した画像・象徴シェイプ |
| 推奨コンポーネント | visual/ParallaxScene（既存 Parallax） |
| 実装難易度 | 低（**Parallax 済**） |
| 乱用リスク | 層が剥離して見える・速すぎ |
| 品質基準 | 層速度が depth に比例・端の隙間が見えない |

## 7. keyword_punch
| 項目 | 内容 |
|---|---|
| 目的 | 重要語を視覚的に強打して記憶に残す |
| 視聴者の印象 | 強調・リズム |
| 向く sceneType | explanation, problem_statement, opening_hook |
| 向かない sceneType | emotional_pause, quote（静かに見せたい時） |
| 推奨尺 | 8–20 frames/語 |
| 推奨 SFX | click / snap / soft impact |
| 推奨 VFX | gold 下線・スケールスナップ |
| 推奨素材 | テキストのみ（背景は素材） |
| 推奨コンポーネント | text/KeywordPunch（既存 KineticType 活用） |
| 実装難易度 | 低 |
| 乱用リスク | 全語強調＝強調なし |
| 品質基準 | 語の出現が SFX と同期・可読・ブランド書体 |

## 8. quote_typewriter
| 項目 | 内容 |
|---|---|
| 目的 | 引用・証言を一語ずつ提示し重みを出す |
| 視聴者の印象 | 信憑性・緊張・傾聴 |
| 向く sceneType | quote, turning_point, evidence_board |
| 向かない sceneType | data_reveal, summary |
| 推奨尺 | 1.5–3.5 frames/文字（文長依存） |
| 推奨 SFX | タイプ音（任意・控えめ）、低音 |
| 推奨 VFX | カーソル点滅、vignette |
| 推奨素材 | 引用テキスト・出典 |
| 推奨コンポーネント | text/QuoteReveal（既存 OpenCaption 活用） |
| 実装難易度 | 低 |
| 乱用リスク | 長文で冗長・遅い |
| 品質基準 | 速度が読みやすい・出典（CitationLowerThird）併記・誤字なし |

## 9. number_countup
| 項目 | 内容 |
|---|---|
| 目的 | 統計・金額・年数を動的に提示し規模を体感させる |
| 視聴者の印象 | 規模感・説得力 |
| 向く sceneType | data_reveal, company_profile, problem_statement |
| 向かない sceneType | quote, emotional_pause |
| 推奨尺 | 20–45 frames |
| 推奨 SFX | tick の連続 + 終端 impact |
| 推奨 VFX | 桁区切り・単位フェード |
| 推奨素材 | 数値・ラベル |
| 推奨コンポーネント | text/NumberCounter（新規ロジック・interpolate+整形） |
| 実装難易度 | 中 |
| 乱用リスク | 桁が多すぎ・速すぎて読めない |
| 品質基準 | 終端値が claim と一致・整形（カンマ/単位）正確・終端で静止 |

## 10. evidence_reveal
| 項目 | 内容 |
|---|---|
| 目的 | 証拠（文書/写真/引用）を順に開示し論証を組む |
| 視聴者の印象 | 説得・「積み上がる」感 |
| 向く sceneType | evidence_board, turning_point, problem_statement |
| 向かない sceneType | emotional_pause, abstract_emotion |
| 推奨尺 | 30–60 frames/要素 |
| 推奨 SFX | 紙/スタンプ/click |
| 推奨 VFX | スポット光・push pin・Telop |
| 推奨素材 | 文書・写真・引用（SceneArt Document/Scales） |
| 推奨コンポーネント | layout/EvidenceBoard（SceneArt+Telop 合成） |
| 実装難易度 | 中 |
| 乱用リスク | 要素過多で散らかる |
| 品質基準 | 開示順が論理に沿う・各要素に出典・最後に全体像が残る |

## 11. timeline_flow
| 項目 | 内容 |
|---|---|
| 目的 | 出来事の時系列を流れとして見せる |
| 視聴者の印象 | 因果・経過の理解 |
| 向く sceneType | timeline, summary, character_profile |
| 向かない sceneType | quote, abstract_emotion |
| 推奨尺 | 30–50 frames/ノード |
| 推奨 SFX | 進行 whoosh・tick |
| 推奨 VFX | 線の描画・年号フェードイン |
| 推奨素材 | 年表データ（SceneArt Timeline） |
| 推奨コンポーネント | layout/TimelineReveal（SceneArt Timeline 活用） |
| 実装難易度 | 中 |
| 乱用リスク | ノード過多で詰まる |
| 品質基準 | 時間軸が一貫・現在位置が明確・年号正確 |

## 12. map_focus
| 項目 | 内容 |
|---|---|
| 目的 | 地理的文脈を示し、対象地点へ寄る |
| 視聴者の印象 | 位置の把握・現実感 |
| 向く sceneType | place_intro, explanation, timeline |
| 向かない sceneType | quote, data_reveal |
| 推奨尺 | 40–90 frames |
| 推奨 SFX | whoosh + ピン着地 click |
| 推奨 VFX | ピン・ハイライト・vignette |
| 推奨素材 | 地図（SceneArt MapUS） |
| 推奨コンポーネント | layout/MapFocus（SceneArt MapUS 活用） |
| 実装難易度 | 中 |
| 乱用リスク | 寄りすぎて文脈喪失 |
| 品質基準 | 地名/位置が正確・寄りが滑らか・ラベル可読 |

## 13. card_stack
| 項目 | 内容 |
|---|---|
| 目的 | 複数の論点/項目をカードで積層提示 |
| 視聴者の印象 | 整理・網羅 |
| 向く sceneType | comparison, summary, explanation |
| 向かない sceneType | emotional_pause, quote |
| 推奨尺 | 18–30 frames/カード |
| 推奨 SFX | カード差し込み swish |
| 推奨 VFX | 影・段差・soft_reveal |
| 推奨素材 | 短文・アイコン |
| 推奨コンポーネント | layout/MotionCard（新規ロジック、MotionCard を再利用） |
| 実装難易度 | 中 |
| 乱用リスク | カード過多で情報飽和 |
| 品質基準 | 重なり順が明快・各カード可読・最終配置が安定 |

## 14. light_sweep
| 項目 | 内容 |
|---|---|
| 目的 | 光の通過で質感と高級感を足す |
| 視聴者の印象 | 上質・映画的 |
| 向く sceneType | chapter_title, opening_hook, ending, abstract_emotion |
| 向かない sceneType | data_reveal（情報の邪魔） |
| 推奨尺 | 連続（シーン全尺に薄く） |
| 推奨 SFX | 不要 or 低音スウェル |
| 推奨 VFX | radial 光（electric/gold 薄） |
| 推奨素材 | 任意（オーバーレイ） |
| 推奨コンポーネント | visual/LightSweep（既存 Motion LightSweep） |
| 実装難易度 | 低 |
| 乱用リスク | 明るすぎて素材が飛ぶ |
| 品質基準 | 透明度が低く下地を壊さない・色が BRAND |

## 15. particle_drift
| 項目 | 内容 |
|---|---|
| 目的 | 塵/光の粒で空気感・奥行きを足す |
| 視聴者の印象 | 没入・静謐 |
| 向く sceneType | emotional_pause, abstract_emotion, chapter_title, opening_hook |
| 向かない sceneType | data_reveal, comparison |
| 推奨尺 | 連続 |
| 推奨 SFX | 環境音 |
| 推奨 VFX | particle 20–40, opacity 低 |
| 推奨素材 | 任意（オーバーレイ） |
| 推奨コンポーネント | visual/ParticleField（既存 Motion Particles） |
| 実装難易度 | 低 |
| 乱用リスク | 粒過多で画面がノイジー |
| 品質基準 | 決定論的・密度が控えめ・可読性維持 |

## 16. data_reveal
| 項目 | 内容 |
|---|---|
| 目的 | グラフ/比率/数値の構造を段階開示 |
| 視聴者の印象 | 理解・納得 |
| 向く sceneType | data_reveal, comparison, company_profile |
| 向かない sceneType | quote, emotional_pause |
| 推奨尺 | 40–80 frames |
| 推奨 SFX | bar 伸長 sweep + 終端 click |
| 推奨 VFX | 軸描画・値ラベル countup（number_countup と連携） |
| 推奨素材 | 構造化データ（数値/比率） |
| 推奨コンポーネント | layout/DataReveal（新規ロジック） |
| 実装難易度 | 高 |
| 乱用リスク | 情報密度過多・誤読を招く図 |
| 品質基準 | 数値が claim と一致・軸/単位明記・読み順が設計される |

## 17. hard_cut
| 項目 | 内容 |
|---|---|
| 目的 | 即時の場面転換、リズムと緊張 |
| 視聴者の印象 | キレ・テンポ |
| 向く sceneType | turning_point, opening_hook, comparison, problem_statement |
| 向かない sceneType | emotional_pause（流れを断つ） |
| 推奨尺 | 0 frames（瞬間） |
| 推奨 SFX | カット音/impact（任意） |
| 推奨 VFX | なし |
| 推奨素材 | 任意 |
| 推奨コンポーネント | transitions/MotionTransition（Series 並置、既定 hard_cut） |
| 実装難易度 | 低 |
| 乱用リスク | 連打で落ち着かない |
| 品質基準 | フレーム境界が正確・音と画の同時切替 |

## 18. flash_transition
| 項目 | 内容 |
|---|---|
| 目的 | 白/光フラッシュで強い場面転換 |
| 視聴者の印象 | 衝撃・記憶の切替 |
| 向く sceneType | turning_point, opening_hook, transition_bridge |
| 向かない sceneType | emotional_pause, summary |
| 推奨尺 | 4–10 frames |
| 推奨 SFX | impact + riser 終端 |
| 推奨 VFX | white フラッシュ（opacity 補間） |
| 推奨素材 | 任意 |
| 推奨コンポーネント | transitions/FlashTransition（新規だが依存不要） |
| 実装難易度 | 低 |
| 乱用リスク | 多用で目に痛い・安っぽい |
| 品質基準 | ピークが短い・点滅過多でない（光感受性配慮） |

## 19. whip_transition
| 項目 | 内容 |
|---|---|
| 目的 | 高速パン風のブラー転換で勢いを出す |
| 視聴者の印象 | スピード・連結 |
| 向く sceneType | transition_bridge, opening_hook, turning_point |
| 向かない sceneType | emotional_pause, quote |
| 推奨尺 | 6–14 frames |
| 推奨 SFX | whoosh |
| 推奨 VFX | 方向性 motion blur |
| 推奨素材 | 任意 |
| 推奨コンポーネント | transitions/WhipTransition（新規ロジック、または @remotion/transitions 導入後） |
| 実装難易度 | 中 |
| 乱用リスク | 酔い・多用で安い |
| 品質基準 | 方向が一貫・前後カットの動線が繋がる |

## 20. glitch_transition
| 項目 | 内容 |
|---|---|
| 目的 | デジタル破綻表現で不穏/技術テーマを示す |
| 視聴者の印象 | 不安・現代性・異常 |
| 向く sceneType | turning_point, problem_statement, transition_bridge |
| 向かない sceneType | emotional_pause, place_intro |
| 推奨尺 | 6–16 frames |
| 推奨 SFX | digital glitch / static |
| 推奨 VFX | RGB ずれ・スキャンライン・ブロックノイズ |
| 推奨素材 | 任意 |
| 推奨コンポーネント | transitions/GlitchTransition（**要実装**・新規ロジック） |
| 実装難易度 | 高 |
| 乱用リスク | 世界観に合わないと安っぽい・多用で陳腐 |
| 品質基準 | テーマ的必然性がある時のみ・短く・可読性を壊さない |

## 21. silent_hold
| 項目 | 内容 |
|---|---|
| 目的 | 無音/静止の「間」で余韻と緊張を作る |
| 視聴者の印象 | 重み・余韻・集中 |
| 向く sceneType | emotional_pause, turning_point, quote, ending |
| 向かない sceneType | data_reveal, comparison |
| 推奨尺 | 30–90 frames |
| 推奨 SFX | 無音 or 微かなアンビエンスのみ |
| 推奨 VFX | 極微の cinematic_drift, vignette |
| 推奨素材 | 顔・象徴・余白 |
| 推奨コンポーネント | layout/* + audio/SfxScheduler（無音管理） |
| 実装難易度 | 低 |
| 乱用リスク | 長すぎると間延び・離脱 |
| 品質基準 | 前後の音圧設計と整合・微動はあるが静止に見える |

## 22. cinematic_drift
| 項目 | 内容 |
|---|---|
| 目的 | 極低速の漂いで「常に生きている画」を保つ |
| 視聴者の印象 | 映画的・自然 |
| 向く sceneType | emotional_pause, quote, place_intro, abstract_emotion |
| 向かない sceneType | turning_point の頂点 |
| 推奨尺 | 連続 |
| 推奨 SFX | アンビエンス |
| 推奨 VFX | grain, vignette |
| 推奨素材 | 任意 |
| 推奨コンポーネント | camera/CameraRig（intensity 低） |
| 実装難易度 | 低 |
| 乱用リスク | ほぼ無し（既定として安全） |
| 品質基準 | 動きが知覚下〜微・端で破綻しない |

## 23. foreground_blur_pass
| 項目 | 内容 |
|---|---|
| 目的 | 前景のボケ要素が横切り、被写界深度と奥行きを出す |
| 視聴者の印象 | 高級・実写的 |
| 向く sceneType | reenactment, place_intro, character_profile, abstract_emotion |
| 向かない sceneType | data_reveal, chapter_title |
| 推奨尺 | 24–60 frames |
| 推奨 SFX | 環境音 |
| 推奨 VFX | blur レイヤの平行移動 |
| 推奨素材 | 前景オブジェ画像 |
| 推奨コンポーネント | visual/*（前景 blur レイヤ）+ camera/CameraRig |
| 実装難易度 | 中 |
| 乱用リスク | 主題を隠しすぎる |
| 品質基準 | 前景が主題を一時的にしか遮らない・blur が自然 |

## 24. panel_float
| 項目 | 内容 |
|---|---|
| 目的 | 複数パネルを 3D 空間に浮遊させ情報を立体配置 |
| 視聴者の印象 | 先進・没入 |
| 向く sceneType | data_reveal, company_profile, summary, abstract_emotion |
| 向かない sceneType | quote, emotional_pause |
| 推奨尺 | 60–150 frames |
| 推奨 SFX | soft whoosh / ambient |
| 推奨 VFX | 3D 透視・被写界深度 |
| 推奨素材 | パネル化した画像/テキスト |
| 推奨コンポーネント | three/FloatingPanels3D（**Phase4・@remotion/three 導入後**） |
| 実装難易度 | 高 |
| 乱用リスク | 3D 酔い・派手すぎてドキュメンタリー性低下 |
| 品質基準 | 導入後実装・パネル可読・動きが上品・$0 代替（2.5D）と切替可 |

## 25. depth_dolly
| 項目 | 内容 |
|---|---|
| 目的 | カメラが Z 軸を進み、真の奥行き移動を作る |
| 視聴者の印象 | 没入・空間の通過 |
| 向く sceneType | opening_hook, transition_bridge, abstract_emotion, place_intro |
| 向かない sceneType | quote, data_reveal |
| 推奨尺 | 45–120 frames |
| 推奨 SFX | 低音 drone / whoosh |
| 推奨 VFX | 3D カメラ移動・depth fog |
| 推奨素材 | 3D シーン/多層画像 |
| 推奨コンポーネント | three/DepthStage（**Phase4・@remotion/three, three 導入後**） |
| 実装難易度 | 高 |
| 乱用リスク | 酔い・処理重・過剰演出 |
| 品質基準 | 導入後実装・2.5D parallax_depth で代替可・移動が滑らか |

## 26. ambient_overlay
| 項目 | 内容 |
|---|---|
| 目的 | グレード/霧/色被りで全カットに統一した空気を与える |
| 視聴者の印象 | 統一感・トーン |
| 向く sceneType | 全般（特に explanation, place_intro, emotional_pause） |
| 向かない sceneType | （無し。強度を下げて常用可） |
| 推奨尺 | 連続 |
| 推奨 SFX | 不要 |
| 推奨 VFX | グラデーション grade（RoughCut の grade を共通化）・色被り |
| 推奨素材 | 任意（オーバーレイ） |
| 推奨コンポーネント | visual/AtmosphereOverlay, visual/ColorGradeOverlay（colorPresets 駆動） |
| 実装難易度 | 低 |
| 乱用リスク | 濃すぎて素材が沈む |
| 品質基準 | 色が BRAND・透明度設計・下地のコントラストを保つ |

## 27. diagram_draw
| 項目 | 内容 |
|---|---|
| 目的 | 図解/フローを描画しながら因果や手順を説明 |
| 視聴者の印象 | 理解・明晰 |
| 向く sceneType | explanation, solution_reveal, summary |
| 向かない sceneType | quote, emotional_pause |
| 推奨尺 | 30–50 frames/ステップ |
| 推奨 SFX | pen / draw tick |
| 推奨 VFX | ストローク描画・矢印フェード |
| 推奨素材 | 手順データ（DiagramFlow steps） |
| 推奨コンポーネント | layout/*（DiagramFlow 活用） |
| 実装難易度 | 中 |
| 乱用リスク | ステップ過多で冗長 |
| 品質基準 | 描画順が論理に沿う・ラベル可読・内容が claim と一致 |

## 28. relationship_connect
| 項目 | 内容 |
|---|---|
| 目的 | 人物/組織/事実の関係をノード＆リンクで可視化 |
| 視聴者の印象 | 構造理解・「繋がった」感 |
| 向く sceneType | character_profile, company_profile, evidence_board, summary |
| 向かない sceneType | quote, emotional_pause |
| 推奨尺 | 30–60 frames/リンク |
| 推奨 SFX | connect click / soft impact |
| 推奨 VFX | リンク描画・ノードのパルス |
| 推奨素材 | 関係データ（ノード/エッジ） |
| 推奨コンポーネント | layout/RelationshipMap（**要実装**・新規ロジック） |
| 実装難易度 | 高 |
| 乱用リスク | ノード過多でスパゲッティ化 |
| 品質基準 | レイアウトが読める・関係が事実と一致・段階開示 |

## 29. title_slam
| 項目 | 内容 |
|---|---|
| 目的 | 章題/タイトルを強く着地させ章の開始を宣言 |
| 視聴者の印象 | 開始の合図・力強さ |
| 向く sceneType | chapter_title, opening_hook |
| 向かない sceneType | emotional_pause, quote |
| 推奨尺 | 12–24 frames |
| 推奨 SFX | impact + 低音ドン |
| 推奨 VFX | スケールスナップ・gold rule・light_sweep |
| 推奨素材 | タイトルテキスト |
| 推奨コンポーネント | text/ImpactTitle（KineticType + CameraRig） |
| 実装難易度 | 中 |
| 乱用リスク | 全章 slam で重い・うるさい |
| 品質基準 | 着地で完全静止・SFX 同期・ブランド書体（Impact） |

## 30. soft_reveal
| 項目 | 内容 |
|---|---|
| 目的 | 穏やかなフェード/ブラー解除で要素を上品に出す |
| 視聴者の印象 | 落ち着き・丁寧 |
| 向く sceneType | emotional_pause, quote, summary, ending, explanation |
| 向かない sceneType | turning_point の頂点, opening_hook の衝撃 |
| 推奨尺 | 18–40 frames |
| 推奨 SFX | 微かな soft swell（任意） |
| 推奨 VFX | opacity + blur 補間 |
| 推奨素材 | テキスト・写真 |
| 推奨コンポーネント | text/* + layout/*（共通 reveal ユーティリティ） |
| 実装難易度 | 低 |
| 乱用リスク | 全要素 soft で締まりがない |
| 品質基準 | 補間が滑らか・終端で完全表示・遅すぎない |

---

## 既存で「もう出来る」 vs 「要・導入/新規」まとめ

- **既存ラップで出来る（依存不要）**: slow_push_in, fast_push_in, pull_out, parallax_depth(**Parallax 済**), keyword_punch, quote_typewriter, evidence_reveal, timeline_flow, map_focus, light_sweep, particle_drift, hard_cut, silent_hold, cinematic_drift, ambient_overlay, diagram_draw, title_slam, soft_reveal。
- **新規ロジックが要る（依存不要）**: subtle_shake, impact_zoom, number_countup, card_stack, data_reveal, flash_transition, whip_transition, glitch_transition(**要実装**), foreground_blur_pass, relationship_connect。
- **依存導入が前提（Phase4・導入後）**: panel_float（@remotion/three）, depth_dolly（@remotion/three, three）。whip_transition は @remotion/transitions を使う場合のみ Phase4 寄り（新規ロジックで Phase3 実装も可）。

## 関連文書
- `docs/code-operable-motion-system.md` — システム思想とアーキテクチャ。
- `docs/remotion-animation-component-roadmap.md` — コンポーネント別 props/Phase/受け入れ基準と preset 設計。
