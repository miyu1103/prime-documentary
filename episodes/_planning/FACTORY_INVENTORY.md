# ファクトリ素材棚 インベントリ＆活用ガイド（2026-06-23 時点）

`assets/asset_manifest.v001.json`（商用OK・DL済み）の現況。設計書・Codex実装はこれを見て**ふんだんに活用**する。
**全件 Pexels / Pixabay（License: Pexels License / Pixabay Content License＝商用OK）**。

## カテゴリ分け＝テーマ（クエリ時に導出・ビルダー非依存）
> 重要：素材ビルダー（ダウンロード/登録）が `asset_manifest.v001.json` を**フラットパスで継続的に上書き**するため、テーマは**マニフェストに保存しない**。`scripts/factory_themes.py` の `theme_of(subtype)` で**抽出時にサブタイプから導出**する（＝ビルダーが何度書き換えても効く・物理移動不要）。
- 実体パス＝**`H:\pd-media\assets\factory\<category>\AF-<CAT>-NNNN__<subtype>.<ext>`**（フラット維持）。
- **backgrounds の14テーマ**：`legal_court / civic_voting / crime_police / forensics_dna / medical_lab / finance_money / property_home / school_youth / surveillance_tech / documents_paper / urban_night / nature_landscape / atmosphere_symbolic / abstract`。light/vfx/particle/texture/loops は各カテゴリ＝1バケット。
- **取り出し方（速い・どの状態でも動く）**：
  - `./.venv/Scripts/python.exe scripts/select_factory_assets.py --themes`（テーマ一覧＋点数）
  - `... --theme legal_court --kind video`（テーマ別b-roll動画）
  - `... --subtype courtroom_interior`（サブタイプ直指定）
  - 抽出後 `remotion/public/<slug>/factory/` へコピーして使用。
- **物理フォルダ整理（factory/<category>/<theme>/）は保留**：DLが完全停止してから `scripts/recategorize_factory.py` を1回実行（実行中はビルダーに上書きされ不整合になるため）。逆操作＝`scripts/revert_factory_reorg.py`。

## 総量
- **総点数 65,543（≈221GB）／ image 53,960・video 11,583。**
- カテゴリ（14分類中6カテゴリが充実、他8は未充填）:

| カテゴリ | 点数 | image | video | 用途 |
|---|---|---|---|---|
| backgrounds | 45,027 | 36,939 | 8,088 | **テーマ別の本格b-roll/確立ショット/背景プレート**（190サブタイプ） |
| light_assets | 6,169 | 5,034 | 1,135 | 光・フレア・リーク（reveal/雰囲気の加飾, screen/add） |
| vfx_overlays | 5,076 | 4,137 | 939 | 煙/水/稲妻/インク/火花（転換・reveal, screen/add） |
| particle_assets | 4,973 | 4,004 | 969 | 塵/雪/灰/火の粉/蛍（奥行き・空気感, screen/add） |
| texture_assets | 3,846 | 3,846 | 0 | 紙/羊皮紙/blueprint/古地図/木/大理石（書類/カード/年表の下地, overlay） |
| loops | 452 | 0 | 452 | 抽象ループ背景（network/data_stream/gradient/light_rays/particles） |

> 未充填（必要なら別途）: parallax_layers, transitions, typography_assets, diagram_assets, sfx, ai_video_shots, lottie_assets, ui_motion_assets。

## backgrounds 190サブタイプ＝テーマ別インデックス（本格活用の核）
※多くが image＋video 両方。**確立ショット・b-roll・カットアウェイ・背景**に使える。

- **法廷/司法（汎用・全話）**: supreme_court_building / courtroom_interior / courtroom_empty_wide / jury_box_empty / witness_stand_empty / judge_gavel_wooden / courtroom_gavel_block_macro / lady_justice_statue / balance_scale_brass / antique_brass_scales / law_library_books / law_books_spines_macro / us_constitution_document / courthouse_steps / federal_building_columns_night / capitol_dome_dusk / white_house_exterior / bank_building_columns
- **投票/民主主義**: ballot_box_voting / voting_booth_curtain / silhouette_crowd_at_protest / protest_crowd_signs / american_flag_waving
- **犯罪/警察**: police_car_lights_night / ambulance_lights_at_night / police_badge_close_up / police_station_at_night / police_interrogation_room_empty / one_way_mirror_room / crime_scene_tape_night / evidence_bag / evidence_locker_shelves / case_files_stack_desk / handcuffs(関連) / jail_cell_bars / prison_corridor / prison_yard_fence / barbed_wire_fence_sky
- **鑑識/DNA（EP13 King）**: dna_double_helix_render / dna_laboratory_blue / fingerprint_scan_blue / fingerprint_dust_lift / blood_sample_vial / microscope_lab / microscope_slide_macro
- **医療/検査（EP15 Theranos）**: modern_medical_lab / laboratory_glassware / laboratory_centrifuge / test_tubes_rack_lab / blood_vials_in_rack / operating_room / hospital_corridor_night / hospital_waiting_room_empty / ekg_heart_monitor / pills_macro
- **金融/詐欺（EP4 FTX,5 Madoff,15）**: money_cash_counting / cash_stacks_money / stack_of_hundred_dollar_bills / money_counting_machine / open_briefcase_of_cash / gold_bars_stacked / bank_vault_door / safe_deposit_boxes_vault / open_safe_empty / stock_market_screen / stock_ticker_board / stock_chart_crashing_red / stock_chart_rising_green / trading_floor_screens / wall_street_sign / charging_bull_statue / physical_bitcoin_coin / credit_card_macro_chip
- **不動産/家（EP10 Kelo）**: front_door_house / white_picket_fence / for_sale_sign_yard / suburban_house_exterior_night / american_suburb_aerial / moving_truck_loading / moving_boxes_empty_room / broken_house_demolition / small_town_main_street / rural_road_america
- **学校（EP11 Mahanoy）**: school_hallway_empty / school_bus_yellow / graduation_cap_toss / empty_playground_at_dusk
- **監視/テック（EP8 Carpenter,13）**: surveillance_camera_city / city_surveillance_camera_dome / cctv_monitor_grid_wall / security_monitors_wall / cell_tower_silhouette / cell_tower_at_sunset / radio_tower_at_night / smartphone_in_dark / smartphone_notification_glow / mobile_phone_map_location / binary_code_screen_green / circuit_board_macro / circuit_data_flow / fiber_optic_cables_glowing / server_room_blue / data_center / hacker_hoodie_keyboard_dark / satellite_earth_at_night / world_map_dark_glowing / globe_spinning_dark
- **書類/契約（EP12 仲裁ほか）**: contract_paperwork_signing / stacked_legal_documents / documents_on_desk / case_files_stack_desk / wax_seal_on_document / magnifying_glass_on_document / quill_and_ink_pot / vintage_typewriter / newspaper_macro / newspaper_printing_press / shredded_documents_pile / burning_paper_documents
- **象徴/雰囲気（全話の“間”・転換）**: long_shadow_of_a_person / lone_person_silhouette_walking / person_at_window_silhouette_night / shattered_mirror / broken_window_glass_shards / single_chair_empty_room / clock_ticking_macro / candle_in_dark / cemetery_fog / lighthouse_in_storm / storm_clouds_dramatic / ocean_horizon_moody / foggy_forest / lone_tree_in_field / mountain_silhouette_dusk / empty_road_sunset / chess_board_dramatic / padlock_and_chain / chains_and_padlock_rusty / old_keys_on_table / elderly_hands_close_up
- **都市/夜景（確立・転換）**: city_skyline_dusk / drone_city_aerial_night / city_traffic_night_long_exposure / rain_on_city_street_neon / rain_street_reflection_night / city_bridge_night_long_exposure / highway_night_long_exposure / subway_tunnel_empty / train_platform_night / airport_terminal_empty / empty_parking_garage / boardroom_table_dark / office_interior_dark / empty_office_cubicles / warehouse_interior_dark / abandoned_factory_interior

## light / vfx / particle / texture パレット（加飾）
- **light（29）**: god_rays / lens_flare / golden_hour_flare / soft_golden_light / bokeh_lights / light_leak_overlay / light_streaks_motion / neon_glow_abstract / neon_sign_reflection_wet / headlights_in_rain / **police_strobe_red_and_blue** / tv_screen_glow_on_face / projector_beam_dust / flashlight_beam_fog / warm_window_light_rays。→ reveal/山場に光アクセント、夜景・取調べに strobe。
- **vfx（25）**: smoke_on_black / colored_smoke / ink_in_water / ink_drop_in_water_slow_motion / lightning_strike_night / electric_spark / fog_rolling / mist_atmosphere / dust_cloud / shockwave_heat_distortion / paper_burning_edge / explosion_fireball_black。→ 転換・reveal・崩落（screen/add合成）。
- **particle（24）**: dust_motes_sunlight / floating_dust_in_light_beam / embers_floating / sparks_slow_motion / snow_falling_dark / ash_falling / paper_scraps_flying / glitter_particles / fireflies_at_night / bokeh_particles_dark / static_noise_particles / rain_particles_backlit。→ 全編の奥行き・空気感。
- **texture（20）**: old_paper / parchment_texture / aged_document_texture / blueprint_paper / vintage_map_texture / scratched_film / film_grain_texture / dark_wood / dark_marble / leather / canvas / grunge_texture_dark / concrete。→ 書類/カード/年表/地図の下地（overlay）。
- **loops（11・動画）**: abstract_network_nodes_loop / data_stream_loop / looping_gradient_navy / looping_light_rays / looping_particles_blue / atmospheric_loop / slow_gradient_motion。→ 抽象シーン・章扉・データ場面の動く背景。

## 活用方針（VIDEO_RULES §4/§12 準拠・本格活用）
1. **確立ショット/b-roll/カットアウェイ＝backgrounds の動画/静止を本格採用**（establishing・転換・“間”）。AI画像（ヒーロー/象徴）とコード演出（票/年表/図解＝意味）と**三層で構成**。
2. **背景プレート**＝シーン背後に backgrounds/loops を薄く（ベタ塗り回避・被写体くっきり分離）。
3. **オーバーレイ**＝light/vfx/particle を screen/add でreveal・雰囲気に。**山場は光＋vfxでため→開放**。
4. **質感**＝texture を書類/カード/年表/地図の下地に overlay。
5. **編集上の注意（権利/中立）**: これらは**一般ストック**＝「その事件の実物・実在人物そのもの」として提示しない（illustrative/symbolic に使う）。実在人物の肖像なし。トーン/配色（黒/紺/青/金）に合うものを選ぶ。licenseはallowedのみ・出典/sha256記録。
6. **過剰回避**: 加飾を盛りすぎてナレ・字幕・意味グラフィックを邪魔しない。1カット1〜2レイヤを目安。
