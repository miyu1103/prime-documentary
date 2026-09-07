# EP62 · GREENE v. LINDSEY — 素材（アーカイブ映像）計画 v001

**2026-08-10 ・ 台本 `EP62_greene_script.en.v003.md`（v004 は凍結ミスで破棄・v003 が正典）**
**契約 `episodes/PD-2026-062-greene/episode_spec.v001.json`**

---

## 0. 30秒で分かる結論

```
着手時のプール          9 本（床 ≈41 本に対して）
床                     31分 ÷ 45秒 = 約41本
staged（4波・累計）     197 本
accepted（最終）        51 本   ← 床 +10 本（+24%）
rejected                168 本（v001 の 38 本を引き継ぎ ＋ 今回 130 本）
検索した棚              151,869 点（factory 台帳を含む全数）／うち動画 31,150 本
```

The pool was nine clips. `factory_used` was an owner-approved deviation on the grounds that
"the shelf is thin". **The shelf was not thin. The queries were written in a director's
language.** Rewriting them in the supplier's vocabulary took the pool from 9 to 51 without
touching the floor, the resolution rule, or the face rule.

---

## 1. 何を探したか（registers derived from the script）

| # | Register | Script line it serves |
|---|---|---|
| R1 | 紙そのもの — 平らな一枚、めくれた角、ちぎれた角 | HOOK「a piece of paper fixed to a door was service」／ motif 1–7 |
| R2 | ドアと錠・取っ手・敷居 | ACT_1「an officer went to an apartment door in Louisville and knocked」 |
| R3 | ノックする手・呼び鈴・応答のない戸口 | ACT_2「the officer knocks, nobody comes」 |
| R4 | レンガ・コンクリート・塗った壁 | ACT_1「tenants in a Louisville housing project」／ ENDING「an unfaded square where the paper was」 |
| R5 | 外廊下・階段・共用部・エレベーター | HOOK「the walkway of identical doors」／ ENDING「the walkway is empty」 |
| R6 | 天候 — 雨・風・雪・落ち葉 | ACT_3 motif 4「the sheet on concrete under the stair, wet through」／ reset beat「wind lifts the sheet」 |
| R7 | 時間の経過 — 時計 | ACT_1「The clock started」／ ACT_4「the appeal window had closed」 |
| R8 | 記録・証言 — 空の椅子二脚・書類・ページ | ACT_3「the deposition room, two chairs facing each other」 |
| R9 | 留める手段 — 画鋲・コルクボード・釘 | ACT_2 n.1「a thumbtack, adhesive tape, or other means」 |
| R10 | 国家 — 旗・街灯・公共の設え | ACT_1「Every step of what follows was done by the State」 |

**契約で禁じられている register**（`forbidden_subjects`）は最初から検索していない：
法廷内部・法槌・独房・手錠・立ち退きの現場（歩道の家具）・強欲な家主・実在の建物。

---

## 2. 語彙の書き換え — 0件が返ったクエリと、何を直したか

**0件は棚の事実ではなく、こちらの書き方の事実である。** 以下はすべて 151,869 点
（factory 台帳込み）に対する実測。`--weak-ok` 相当（OR一致・一致語数で順位付け）で
目視してから「無い」と判断している。

### 2.1 書き換えて当たったもの

| 監督の言葉 | 実測 | 供給側の言葉 | 実測 |
|---|---:|---|---:|
| `typewriter` | **0** | `old typwriter`（供給側の綴り間違いがそのまま題名） | **1** |
| `apartment door` | **0** | `door handle entry wood` | 1 |
| `front door house` | **0** | `door house old closed padlock` / `doors house old ivy vine building architecture` | 1 / 1 |
| `knocking on door` | **0** | `person ringing the doorbell` | 1 |
| `concrete stairs` / `stairwell` / `handrail` | **0/0/0** | `video of staircase and building` / `close up video of metal railings` | 1 / 1 |
| `empty room` / `empty corridor` | **0/0** | `pan empty room abandoned building steamy steam` / `empty building interior` | 1 / 1 |
| `peeling paint` / `plaster` | **0/0** | `rough cement texture` / `industrial wall installation process` / `person painting a wall` | 1 / 1 / 1 |
| `envelope` | **0** | `writing letter printing document write` / `letter write pen to write office writing record` | 1 / 1 |
| `adhesive tape` / `thumbtack` | **0/0** | `pinning paper on corkboard` | 1 |
| `moving box` | **0** | `labeled boxes of belongings` / `packed boxes and luggage use in transferring house` | 1 / 1 |
| `long shadow` | **0** | `shadow of a person behind the glass door` / `shadow of a person moving on a curtain` | 1 / 1 |
| `balcony` / `hallway` | **0/0** | `pigeon bird courtyard outdoor concrete floor` / `lift open doors closures condominium` | 1 / 1 |
| `post office` / `postal` | **0/0** | `postage stamp collection` | 1（他話で使用済のため不採用） |

### 2.2 書き換えても本当に無いもの（弱一致プールを目視したうえで）

| Register | 弱一致プール | うち使用可 | 目視の結果 |
|---|---:|---:|---|
| `mailbox / mail slot / letterbox` | 111 | 39 | 全部が宅配便・ポスター・スロットマシン。**郵便受けは棚に一本も無い** |
| `peephole / spyhole / door chain` | 72 | 45 | `bolt` が雷、`chain` が鎖・ブロックチェーン。**覗き穴は無い** |
| `public housing block / tenement / estate` | 344 | 65 | `block` が 3D ブロック・blockchain・projector。**団地の外観は無い**（唯一近いのは §5 の title-blind 一本） |
| `exterior walkway / balcony / breezeway` | 206 | 29 | `landing` が飛行機の着陸。**外廊下は無い** |
| `eviction notice on a door` | 1,319 | 473 | 紙は大量にあるが、ドアに留めた告知は無い（棚点検 v001 の結論と一致） |

**この5件はプレート（Codex 生成）で埋めるしかない。** 実在人物も実在建物も写らないので
invariant 11 には触れない。設計書の G001–G241 がすでにその役を負っている。

### 2.3 存在するが他話で焼き済み（＝棚の問題ではない）

語彙を直して初めて見えた、時代設定にぴったりの4本は**すべて他エピソードで使用済み**だった。

```
retro home exterior in winter 1960s footage            -> already used
charming small town street in autumn                   -> already used
scenic twilight view of rural houses and countryside   -> already used
mounted iron grills installed on a house window        -> already used
```

---

## 3. 検索したレーン（全レーン・factory 台帳込み）

`from shelf import shelf_rows`（`scripts/shelf.py`）で数えている。自前 glob はしていない。

| レーン | 棚の総数 | うち動画 | 本話が staged した数 |
|---|---:|---:|---:|
| pixabay | 53,760 | — | — |
| pexels | 34,905 | — | — |
| pixabay_extra | 24,364 | 10,262 | 51 |
| nasa | 11,409 | 630 | 0 |
| freesound | 8,635 | 0（音声） | 0 |
| **wikimedia** | 5,569 | **0** | 0 |
| **nara** | 3,600 | 814（89% が SD） | 0 |
| **loc** | 3,092 | **0** | 0 |
| mixkit | 2,158 | 2,158 | 6 |
| ia | 1,422 | 1,422（73% が SD） | 0 |
| unsplash / smithsonian / noaa / met / sdxl / coverr / oyez / courtlistener | 2,946 | 109 | 0 |
| **合計** | **151,869** | **31,150** | **197** |

- `wikimedia` と `loc` は**動画を1本も持っていない**（静止画・TIF が主）。0本なのは検索漏れではない。
- `nara` は動画 814 本のうち 727 本（89.3%）が 720p 未満。本話は 1920x1080 未満を採らないので
  構造的にほぼ全滅する。SD を採るのは判断であって事故であってはならない、という棚の原則に従った。
- **factory 台帳は最初から検索対象に入っている**（`shelf_rows()` の既定は `include_factory=True`）。
  staged 151 本のうち **91 本**、accepted 51 本のうち **28 本**が `factory.jsonl` 由来。

---

## 4. 使ったクエリと本数（4波・全 135 本）

正典は `config/episode_footage_queries.v001.json` の `episodes.greene.queries`。
各文字列は**書く前に棚に対して数えてある**。`stage_footage_by_title.py` は題名の
AND 部分一致・台帳順に先頭 N 本を採るので、緩いクエリは書いていない。

### 波1（74 クエリ → 104 本）主要なもの

```
R1 紙   close up video of a paper 4 · paper on a table 4 · crumpled paper 7 · folded papers 1
        blank sheet of paper 1 · white paper laid 1 · tearing a paper 1 · pieces of paper falling 1
        pinning paper on corkboard 1 · paper with a message written 1 · person holding papers 1
R2 扉   rusty door handle 1 · metal door lock 1 · door handle entry wood 1 · window knob 1
        door house old closed padlock 1 · key door house to open 1 · metal keys on rings 1
        a woman opening a wooden door 1 · person ringing the doorbell 1
        shadow of a person behind the glass door 1
R4 壁   close up video of a bricks 2 · rough cement texture 1 · cement street granite floor marble city sidewalk 1
        house old ivy vine building architecture door abandoned 4 · footage of an abandoned building 5
        building abandoned derelict pioneer camp 1 · abandoned building deemed unlivable 1
R5 共用 video of staircase and building 1 · empty pedestrian underpass 1 · empty building interior 1
        pigeon bird courtyard outdoor concrete floor 1 · inside of a tunnel 1
R6 天候 rain water yard floors wet drops 2 · black and white yard drops rain 1
        rain fall drops wet water waterdrop raindrop floor 1 · rain weather terrace wood wooden floor housing 1
        raindrops rain droplets evening lights splash 1 · autumn leaves maple leaves windy concrete road 1
        rain drops puddle road weather 1 · water droplets on the window 1
        water droplets sliding down a glass window 1 · rain slow motion drops glass 1
R7 時間 analog clock 3 · clock time watch clock hands time passing 1
R8 記録 flipping pages of an old book 3 · hands opening old book 1 · old typwriter 1
        seal stamps and inks 1 · postage stamp collection 1
        dust particles floating in dim light 1 · motes of dust in the sunlight 1 · dust particles in light beam 1
R8 椅子 room home furniture interior sofa table chair wall house indoors 6 · chairs arranged in a circle 1
        black leather chair 1 · person sitting on sofa chair in a dark room 1
        interior room corner modern furniture home house architecture floor 1
R1 箱   labeled boxes of belongings 1 · a room with many boxes on the floor 1
        packed boxes and luggage use in transferring house 1 · stack of boxes on a wooden flooring 1
R10 国家 usa flag waving against clear sky 1 · street lamp during a snowfall 1 · close up of a lamppost 1
        wire fence with lights on background 1 · lights out of focus through a wire fence 1
```

### 波2（32 クエリ → 27 本）— アメリカの低層住宅・庭・子ども

```
los angeles traffic homes houses south central leimert park 4 · buildings houses street urban city
architecture cityscape scene 1 · narrow alley in city at night 1 · a video footage of an alley at night
with lights 1 · empty swing in slow motion 1 · a footage of a playground swing 1 · a playground with
swings and a tree in the background 1 · dustbin the bags with waste dumpster yard rubbish 1 · a person
walking on the backyard 1 · backyard timelapse 1 · footsteps man people urban 1 · close up video of metal
railings 1 · lift open doors closures condominium 1 · rear view on man walking through door 1 · a man
going out to the exit door 1 · a door made of glass panels 1 · bunker door abandoned war safety shelter 1
· video in an abandoned building 1 · a close up of a puddle 1 · water puddle road reflection feet shoe
leaf autumn rain 1 · raindrops rain water wet liquid droplets close up texture 1 · hand prints on papers
on wall 1 · close up on hand leaving hand prints on papers 1 · letter write pen to write office writing
record paper phone 1
```

波2で **0 を返した8本**（`suburban alleyway covered in snow`, `vintage 8mm film of suburban
neighborhood`, `snow covering the suburb surroundings`, `a house with brown roof`, `black and white
video of a busy street`, `a snow covered roof with a chimney and a snow covered house`, `moody urban
view through window blinds`, `a person magnifying a document`）は、
**波1の実行中に別スレッドが同じクリップを他エピソードへ staged したため**（除外 id が
7,970 → 8,232 に増えていた）。棚に無いのではない。

### 波3（23 クエリ → 37 本）— 質感・天候・同じ扉の連なり

```
dust motes floating 1 · a flying dust at the air 1 · a close up shot of a hand on a wet glass 1
a footage of falling snow during night time 1 · close up shot of snow falling 1 · a road covered in snow 2
heavy rain falling on black background 1 · person painting a wall 1 · geometric pattern wall 2
empty underground escalator in urban setting 1 · empty escalator in a metro station 1
lockers in a locker room as part of the school facility 1 · exterior of a building 2
low angle shot of a building 4 · architectural design of a building exterior 1
inside of commercial building 1 · a low angle shot of a floor 1 · a demolished building 4
silhouette of a person standing 1 · a black and white photo of a person standing in the dark 1
man walking alone 4 · an old portable television 1 · industrial wall installation process 1
```

### 波4（6 クエリ → 6 本）— 監査済み factory テーマを歩いて見つけたもの

`select_factory_assets.py --theme property_home/documents_paper/texture/legal_court --kind video`
で**実題名**を見てから引いた。語を推測したのではない。

```
house framer pulling nails out of board with hammer 1 · a hand touching card catalogs at a library 0
close up of a male hand taking a book from a shelf 0 · video of a parking deck 1
a man is walking bringing document 1 · a person finding a document 0 · man walking alone 3
```

---

## 5. factory 棚（88,659 点・棚の 58%）の点検

コーディネータの指摘を受けて実測した。

```
shelf_rows(include_factory=True)  = 151,869
shelf_rows(include_factory=False) =  63,210
factory.jsonl                     =  88,659（動画 15,681）
```

**本作業は最初から `shelf_rows()` を直接呼んでおり、既定が `include_factory=True` なので
factory 棚は全数が視界に入っていた。** `build_archive_inventory.py` /
`qc_archive_contact_sheets.py` / `qc_audio_stats.py` は一度も経由していない。
検算：staged 151 本のうち 91 本、accepted 51 本のうち **28 本**が `factory.jsonl` 由来。
2.2 の「本当に無い」5件は factory 込みで測った数字であり、変わらない。

### ただし、別の穴が見つかった — 題名が `id` のクリップ 2,643 本

`factory.jsonl` の pixabay 由来行のうち、**供給側の題名が文字列 `"id"` そのもの**のものがある。

```
使用可の棚動画          14,343 本
うち題名が "id"/"untitled"  2,643 本（18.4%）
テーマ内訳  misc_background 319 / nature 253 / light 225 / urban_night 215 / particle 205 /
            atmosphere_symbolic 197 / vfx 189 / legal_court 187 / surveillance_tech 176 /
            crime_police 113 / property_home 111 / finance_money 101 / documents_paper 94 …
```

**この 2,643 本は、本リポジトリのすべての題名ベースのツール（`search_archive.py`、
`stage_footage_by_title.py`、`stage_episode_footage.py`）から到達不能である。**
`--query "id"` は「id を含む題名」全部に当たるので選別にならない。

register 該当テーマから 60 本を抽出してコンタクトシートで目視した
（`runs/qc/greene_titleblind_sheets/`）。中身はグリーンスクリーン・恐竜・マーモット・
蝋燭・チェス・空撮スカイラインが大半で、**本話の register に当たったのは1本だけ**
（`legal_court__pixabay__216021__id.mp4` — モノクロの中低層集合住宅群の広景。
棚全体で「団地の外観」に最も近い一本）。歩留まりは 1/60。

**staged していない。** 題名が `id` のクリップを狙って staged できるツールが存在しないため。
`stage_footage_from_allowlist.py`（AF-ID 指定で staged できる唯一のツール）は
**factory 棚のリネームで壊れている**：`NAME_RE` が `AF-BG-1234__label.mp4` を要求するが、
ディスク上は 38,575 本すべてが `pexels__10000205__bokeh-footage-of-city-lights.mp4` 形式に
改名済みで、`AF-` で始まるファイルは0本。

**棚スレッドへの申し送り（2件）**

1. `factory.jsonl` の `title == "id"` を `source_url`（`https://pixabay.com/videos/id-28860/`）
   か `manifest_id`/`subtype` から埋め戻す。棚の 18% が検索から消えている。
2. `stage_footage_from_allowlist.py` を改名後のファイル名に合わせる。現状、実行すれば
   「allowlisted clip not in the shelf ledger」で必ず落ちる。

---

## 6. 採用 51 本 — どの台本行に当てるか

| # | clip | Register | Script line |
|---:|---|---|---|
| 1 | `AR-13617608__close_up_view_of_the_flipping_pages_of_an_old_bo` | R8 | ACT_1「section 454.030. It is two sentences long」— 条文を読む3カット |
| 2 | `AR-14744268__a_street_lamp_on_a_snowy_winter_night` | R10 | ACT_2「at whatever hour the one visit happened to fall」 |
| 3 | `AR-20663033__house_framer_pulling_nails_out_of_board_with_ham` | R9 | ACT_2「by use of a thumbtack, adhesive tape, or other means」 |
| 4 | `AR-2618449__a_broken_mesh_wire_on_a_window` | R4 | ACT_1「tenants in a Louisville housing project」 |
| 5 | `AR-28450296__a_playground_with_swings_and_a_tree_in_the_backg` | R5 | ACT_3「children ripping the writs off」— 子どもは映さず、遊具だけ |
| 6 | `AR-32928907__usa_flag_waving_against_clear_sky` | R10 | ACT_1「Every step of what follows was done by the State」 |
| 7 | `AR-34572297__industrial_wall_installation_process` | R4 | ENDING motif 7「an unfaded square where the paper was」 |
| 8 | `AR-36344044__heavy_rain_falling_on_black_background` | R6 | ACT_3 motif 4「the sheet on concrete under the stair, wet through」 |
| 9 | `AR-3813__many_metal_keys_on_rings` | R2 | ACT_4「writs of possession」／ ACT_5「the right to continued residence in their homes」 |
| 10 | `AR-4153743__close_up_shot_of_a_window_knob` | R2 | ACT_2「You watch your own door」 |
| 11 | `AR-4381690__water_droplets_on_the_window` | R6 | reset beat 前後の間 |
| 12 | `AR-5712753__chairs_arranged_in_a_circle` | R8 | HOOK G005「the deposition room, two chairs facing each other」／ ACT_3 冒頭 |
| 13 | `AR-5985192__a_shadow_of_a_person_behind_the_glass_door` | R2/R3 | ACT_2「if no one is at home at the time of that visit」 |
| 14 | `AR-6175388__a_footage_of_an_abandoned_building` | R4 | ACT_1「a Louisville housing project」（低層レンガ・板張りの窓） |
| 15 | `AR-6183926__close_up_of_a_lamppost` | R5/R10 | ACT_2「perhaps at some time of day when the tenant is more likely to be at home」 |
| 16 | `AR-6273545__exterior_of_a_building` | R4/R5 | ACT_1「three doors」（コンクリート躯体に落ち込んだ戸口） |
| 17 | `AR-6473947__person_painting_a_wall` | R4 | ENDING「the paper taped square to the painted door」の下地 |
| 18 | `AR-6474187__close_up_video_of_a_bricks` | R4 | ACT_1「Three names and a housing project」 |
| 19 | `AR-6914692__throwing_crumpled_papers_on_trash_can` | R1 | ACT_3「notices ... were not infrequently removed」 |
| 20 | `AR-6933752__close_up_shot_of_snow_falling` | R6 | ACT_2「Not one at the weekend」— 時間が過ぎる |
| 21 | `AR-7234998__white_paper_laid_on_top_of_other_paper_layer` | R1 | motif 1「the paper taped flat, corners square」 |
| 22 | `AR-7235006__light_and_shadows_on_folded_papers` | R1 | motif 2「one corner lifted from the paint」 |
| 23 | `AR-7533208__a_black_leather_chair` | R8 | ACT_3「under oath, describing their own work」 |
| 24 | `AR-7702049__person_ringing_the_doorbell` | R3 | ACT_1「an officer went to an apartment door in Louisville and knocked」 |
| 25 | `AR-7793217__pedestal_shot_of_a_rough_cement_texture` | R4 | ACT_3 motif 4「on concrete under the stair」 |
| 26 | `AR-8035620__small_pieces_of_paper_falling_on_the_floor` | R1 | motif 5「a torn corner still under the tape」 |
| 27 | `AR-8039468__a_road_covered_in_snow` | R6 | ACT_4「The judgments were final. The appeal window had closed」 |
| 28 | `AR-8516592__shadow_of_a_person_moving_on_a_curtain` | R2/R3 | ACT_2「a conversation on a doorstep, with a person who lives there」— 起きなかった側 |
| 29 | `AR-854693__street_lamp_during_a_snowfall` | R10 | ACT_2「the visit is over」 |
| 30 | `AR-8847832__person_holding_papers` | R8 | ACT_4「filing a class action ... under section 1983」 |
| 31 | `AR-9160919__close_up_of_an_analog_clock` | R7 | ACT_1「The clock started」 |
| 32 | `AR-9306134__person_pinning_paper_on_corkboard` | R9 | ACT_2「a thumbtack」 — **寄りのみ。背景の図表を広く見せない** |
| 33 | `AR-v_114253__lift_open_doors_closures_condominium_technology` | R5 | HOOK G004「the walkway of identical doors」の代替 |
| 34 | `AR-v_114254__door_handle_entry_wood_house_inside_closed_key_w` | R2 | ACT_1「fixed it to the outside of the door」 |
| 35 | `AR-v_127575__pigeon_bird_courtyard_outdoor_concrete_floor_gra` | R5 | ENDING「the hand leaves frame; the walkway is empty」 |
| 36 | `AR-v_141636__house_old_building_brick_building_broken_window` | R4 | ACT_1「Three doors」（同じ開口の連なり） |
| 37 | `AR-v_144780__rain_drops_puddle_road_weather` | R6 | ACT_3「the paper came off」 |
| 38 | `AR-v_16401__pan_empty_room_abandoned_building_steamy_steam` | R5 | ACT_5「It simply stops」 |
| 39 | `AR-v_19316__opening_door_gate_walk_park_old_garden_hand_pass` | R2/R3 | ACT_2「the officer knocks」— 塗った木に手 |
| 40 | `AR-v_215563__rain_raindrops_water_wet_liquid_droplets_close_u` | R6 | reset beat「wind lifts the sheet」の直後 |
| 41 | `AR-v_215607__raindrops_rain_droplets_evening_lights_splash_wa` | R6 | ACT_3「not infrequently removed」 |
| 42 | `AR-v_22694__footsteps_man_people_urban` | R3 | ACT_2「the officer goes to the apartment」 |
| 43 | `AR-v_276__autumn_leaves_maple_leaves_win_fall_windy_concre` | R6 | reset beat「wind lifts the sheet, nobody in frame, 4s」 |
| 44 | `AR-v_27808__rain_slow_motion_drops_glass` | R6 | ACT_2「You will be back」 |
| 45 | `AR-v_31543__water_puddle_road_reflection_feet_shoe_leaf_autu` | R3/R6 | ACT_2「posting follows forthwith」 |
| 46 | `AR-v_326937__clock_time_watch_clock_hands_time_passing_hour_h` | R7 | ACT_4「seventy years earlier」／「That was 1909」 |
| 47 | `AR-v_45471__doors_house_old_ivy_vine_building_architecture_d` | R2 | ACT_5 motif 6「the door, nothing on it」— **冒頭数秒のみ。後半は蔦** |
| 48 | `AR-v_45529__rain_weather_terrace_wood_wooden_floor_housing_b` | R6 | ACT_3「wet through」 |
| 49 | `AR-v_7714__alley_urban_street_lonely_city_town_buildings_ho` | R4/R5 | ACT_1「Somewhere in Louisville in 1975」 |
| 50 | `AR-v_86740__cement_street_granite_floor_marble_city_sidewalk` | R4 | ACT_2「posting a copy thereof in a conspicuous place on the premises」 |
| 51 | `AR-v_9191__rain_fall_drops_wet_water_waterdrop_raindrop_flo` | R6 | ACT_3「before they could have their intended effect」 |

**同一 register の重複対策**：雨/濡れた地面が 11 本と多い。台本上は
「紙が剥がれる」が中心主題なので意味のある反復だが、
`footage_diversity`（distinct≥0.40／再利用≤4）に当てて組むこと。同じ雨を4回以上使わない。

---

## 7. 却下 — 6つの型（全 168 件・`runs/qc/greene_clip_verdicts.v001.json` に全件理由付き）

| 型 | 件数 | 代表例 |
|---|---:|---|
| **実在人物の顔が識別できる** | 6 | `AR-52230`（母と子の顔）／ **`AR-6944084`「a man closing the curtain」・`AR-8909763`「a person looking at the window」は v001 レビューが採用していた2本**。前者は照明の当たった男性の顔、後者は横顔の女性と乳児。今回撤回した |
| **読める文字・姓・ブランド** | 7 | `AR-18330534`（手書きの本文が全部読める）／`AR-7463988`（引越箱に姓 FLETCHER）／`AR-39849`（Apple のモニタが画面を占める）／`AR-7685810`（コワーキングの館内表示） |
| **この作品が使わない register** | 58 | 落書き・廃墟趣味（`AR-10900588`, `AR-13633629`, `AR-9724319`）／解体現場（`AR-4876779` ほか3本）／金（`AR-8369985`, `AR-7580445`）／ガラスの超高層（`AR-15191845` ほか3本）／ドローン（`AR-12567706`, `AR-14047047`, `AR-v_82637`）／自然（`AR-1899746`, `AR-5234909` ほか） |
| **3D レンダー・アニメ** | 9 | `AR-v_270787..794`（ゲームエンジンの山小屋内装6本）／`AR-v_49280`（平面ベクター）／`AR-v_90559`（金貨） |
| **他話で焼き済み**（`check_cross_episode_reuse`・内容ハッシュ） | 26 | `AR-2750099`→hinders／`AR-4553301`→forfeiture（別名 `AF-BG-8913__moving_boxes_empty_room`）／`AR-4018217`→thompson+williams ほか |
| **縦位置 or 1920x1080 未満**（`scan_video_shape`） | 4 | `AR-16156321` 1280x720／`AR-v_245583`, `AR-v_177081`, `AR-v_210786` は 1080x1920 |
| （うち v001 レビューからの引き継ぎ） | 38 | 東京・京都・浜辺・鹿・ピエロ・トイレットペーパー — 語だけ当たった典型 |

**コンタクトシートの1秒目は clip ではない。** 採用に回した全クリップを、尺全体に散らした
4フレームで見直した（`runs/qc/greene_facecheck/`）。それで3本が落ちた。

- `AR-1277675「video of staircase and building」` — 1秒目は摩耗した石段。後半で
  **デリーのジャーマー・マスジドと群衆**が現れる。識別可能な建造物＋人物。
- `AR-12820367「empty building interior」` — 1秒目は真っ黒。中身は現代の
  ガラス張りロビーと新築マンション。
- `AR-8909763` — 1秒目は後頭部だけ。他フレームで女性の横顔と乳児が正面に来る。

---

## 8. 機械ゲートの通過状況（本文書の時点）

```
scan_video_shape        51/51 ok（portrait 0・under_hd 0・pillarbox 0）
check_cross_episode_reuse  51 本すべて他話と content hash 不一致
check_pool_faces        検出器が飽和して 101/101 を flag（街灯 31%・鍵 38%・水たまり 10.7%）。
                        Haar は本件では判別力を持たない。**目視4フレームで代替した**
write_factory_clip_qc   51 clip(s) recorded / accept 51 / unreviewed 0
```

`check_pool_faces.py` の結果を「顔なし」の証拠として使ってはいけない。
本件では偽陽性率が事実上 100% だった。証拠は `runs/qc/greene_facecheck/*.png` の目視である。

---

## 9. 次にやること（本スレッドの担当外）

1. **manifest / film.json の再構築とレンダーはしていない。** 3話ぶん出そろってから一度で行う。
2. `episode_spec.v001.json` の `approved_deviations: ["factory_used"]` は
   **根拠が消えた**（棚は薄くなかった）。組み立て側でこの deviation を落とせるか確認すること。
3. 2.2 の5 register（郵便受け・覗き穴・団地外観・外廊下・ドアに留めた告知）は
   棚に無い。Codex プレート G001–G241 で必ず埋めること。
4. §5 の棚スレッド申し送り2件。
