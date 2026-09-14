# EP64 · MEMPHIS LIGHT, GAS & WATER v. CRAFT — FOOTAGE PLAN v001

**Written 2026-08-10.** Pool: `remotion/public/memphis/factory/`.
Verdicts: `runs/qc/memphis_clip_verdicts.v001.json` · staging receipt:
`runs/qc/memphis_title_staging.v001.json` · QC manifest:
`episodes/PD-2026-064-memphis/05_visuals/factory_clip_qc.v001.json`.

## 0. Result

| | |
|---|---:|
| clips in the pool before this pass | 11 |
| floor (32 min ÷ 45 s) | ~43 |
| candidates staged in this pass | 191 |
| dropped by `check_cross_episode_reuse` and `scan_video_shape` | 45 |
| dropped by eye across 9 labelled contact sheets | 100 |
| **accepted and staged** | **57** |
| margin over the floor | +14 |

Nothing from the earlier pass's 65 rejected rows was re-staged. They sit in
`memphis/factory_offtheme` and `memphis/factory_unused`, and `stage_footage_by_title.py`
excludes every `*/factory*` directory, so a rejected clip cannot come back through a query.
The verdict file now carries 210 rejection rows: the original 65, plus 145 from this pass.

## 1. The premise this pass was testing

`episode_spec.v001.json` records an owner-approved deviation on `factory_used` because
"the shelf is thin". Measured on 2026-08-10 the shelf holds **151,869 items, 31,150 of them
video** (`py -3.11 scripts/shelf.py`). Lanes searched — all of them, in one pass over every
ledger: **pixabay 53,760 · pexels 34,905 · pixabay_extra 24,364 · nasa 11,409 ·
wikimedia 5,569 · nara 3,600 · loc 3,092 · mixkit 2,158 · ia 1,422 · unsplash 1,027 ·
smithsonian 751 · noaa 530 · met 328 · coverr 68.** Of these, the video that survives the
licence and size filters is dominated by pexels, pixabay_extra, mixkit and coverr; nara, loc,
wikimedia and ia hold almost only stills for this subject, and nasa / noaa / met / smithsonian
returned nothing on any register in this script.

Two things were true at once, and the earlier pass recorded only the first.

## 2. Where the shelf really is thin, and where the wording was thin

**Genuinely absent: the meter.** Eleven shelf titles contain the word `meter`. Every one is a
speedometer, a countdown counter, a risk-management graphic or a Santa "naughty/nice" scanner.
`electricity meter on wall`, `gas meter`, `utility meter`, `electric meter box` and
`meter reading` each return **0**, and so do their weak-match pools. There is no meter, no meter
box and no meter dial on this shelf. The nearest substitute staged is `AR-31751374`, a weathered
wall-mounted control box with lit buttons — a thing bolted to a wall that a hand reads.
Everything else in that register has to be a commissioned still.

**Not absent, mis-asked: the electricity itself.** This is the finding that matters.

| query written in a director's words | hits | rewritten in the supplier's words | hits |
|---|---:|---|---:|
| `power line`, `electricity pylon` | 0, 0 | `electricity wires` — pixabay_extra tags the same pylon `pylons, electricity, power pylons, energy, voltage` | 3 |
| `fuse box`, `circuit breaker`, `electrical panel switch` | 0, 0, 0 | `control panel` | 3 |
| `transformer substation` | 0 | `power plant` | 3 |
| `electrician working` | 0 | `worker in hardhat` | 1 |
| `hand on light switch`, `lamp switched on in dark room` | 0, 0 | `light is shining in the dark`, `vintage light fixture` | 1, 1 |
| `power outage blackout` | 0 | `snowfall in the dark`, `dimly lit study` | 1, 1 |
| `residential street`, `suburban house`, `aerial view of suburban` | 0, 0, 0 | `vintage 8mm film`, `retro home exterior`, `house with brown roof`, `low angle shot of a house` | 3, 1, 1, 1 |
| `snowy street` | 0 | `road covered with snow`, `street footage with snowfall`, `snowy urban night scene` | 2, 1, 2 |
| `office waiting room` | 0 | `empty waiting area`, `open office space`, `desk in an office`, `modern office interior` | 1, 2, 3, 1 |
| `stack of papers`, `envelope`, `crumpled papers` | 0, 0, 0 | `finding a document`, `paper clips`, `holding a pen`, `filling in a form` | 3, 3, 3, 3 |
| `mailbox` | 0 | nothing fixes it — all 19 envelope/mailbox clips on the shelf are already staged in `postoffice` | 0 |
| `analog clock`, `rusty door handle`, `metal door lock`, `ringing the doorbell` | 0 each | nothing — all four were staged into `greene` earlier the same day | 0 |

The lesson is the one the shelf worklog already records: **a 0 is a fact about the wording.**
`power line` is a director's phrase; `electricity, wires, cables, industrial` is how a pixabay
contributor tags the same pylon. The whole electricity register — the thing this episode is
about — was one query away the entire time.

**Two vocabulary collisions worth writing down**, because they poison whole registers here:

- `bill` matches **bird beaks**. Of 101 shelf titles containing `bill`, most are pelicans,
  spoonbills, geese and ducks; the rest are banknotes. There is no utility bill on this shelf
  under that word, and `invoice` is worse (rhea, coot, pelican).
- `coin`, `stacked coins`, `gold coin on a wooden table` return **bitcoin**, near-exclusively.
  Seven crypto clips were staged and all seven rejected. `a coin on a table with a wooden
  surface` is the one plain-coin title in the set.

## 3. What broke that a query could not see

`stage_footage_by_title.py` de-duplicates across episodes **by clip id**. That is not enough.
`check_cross_episode_reuse.py` keys on content — size plus a hash of the first 256 KB — and it
found **32 of 169** staged clips already burned in another film under a completely different
name, because those episodes took them off the older factory shelf:

```
AR-11008817  a suburban alleyway covered in snow  ->  weimer, as AF-BG-22106__white_picket_fence.mp4
AR-6173646   shadow on a snow covered ground      ->  weimer, as AF-BG-22104__white_picket_fence.mp4
AR-7651532   a document with a graph on a table   ->  flowers, morton, norfolk, postoffice, willingham
AR-8371852   files inside a cardboard box         ->  caniglia, carsearch, katz, kyllo, rodriguez
AR-8731580   a person holding a pen               ->  florence, gardner, king, young, as hand_sign.mp4
```

`scan_video_shape.py` dropped a further 10 clips below 1920×1080 and 1 portrait. Neither defect
is visible on a contact sheet, and neither is in the ledger, which stores no dimensions.
**Run both before looking at anything.**

And run the content check **again at the end**. `episodes/_planning/measurements/STAGED_CLIP_INDEX.json`
is shared, and another thread rebuilt it mid-session: a `--check` over the second staging round
returned "0/33 already used" at 12:50 and three hits at 12:58 over the same files
(`a person walking through a library` is `AF-BG-0593__law_library_books.mp4` in frazier, gardner
and lech; `person reading handwritten notes` is a byte-identical re-upload of norfolk's
`AR-30998273__close_up_of_person_reading_handwritten_letter.mp4` under a different pexels id).
Those three were accepted on the sheets and then removed, which is why the count is 57 and not 60.

## 4. What a single-frame contact sheet cannot show

The sheet builder extracts one frame at t=1s. Three clips that look faceless on that frame turn
into a clear, centred, identifiable face later:

| clip | on the sheet | at 60–95% of its duration |
|---|---|---|
| `AR-8517529__a_woman_opening_a_curtain` | back of a head at a window | she turns; full profile, sharp |
| `AR-9198046__a_man_turning_pages_of_a_book` | hands and an open book | he lowers the book and smiles to camera |
| `AR-v_40818__corridor_office...` | an empty institutional corridor | two people walk up to lens, faces and a uniform badge |

`AR-8517529` was one of the 11 clips already in the pool — it had passed the earlier review.
This is exactly the EP65 failure (`woman_sitting_on_a_chair_while_reading_a_magazine`), and the
only thing that caught it was sampling extra frames for every clip with a person in the title:
21 clips at 30/60/90% and 11 more at 35/70/95%. That pass also caught two legible-text failures a
single frame hid — `AR-5994030` (the typewriter text resolves to "Fake Ne…") and `AR-5283824`
(the page text resolves to a passage about protein and anatomy).

## 5. Registers, and how the accepted 57 cover the film

| register | script anchor | clips |
|---|---|---:|
| the telephone | HOOK "the handset hanging off its cradle" · ACT_1 state 3 · ACT_5 and ENDING callbacks | 5 |
| the house, the street, the era | ACT_1 "reside on Alaska Street in Memphis" · "the residence had been used previously as a duplex" | 8 |
| winter, night, the light | ACT_4 "the discontinuance of water or heating for even short periods of time may threaten health and safety" | 12 |
| gas and electricity | the service itself — "two separate gas and electric meters" | 6 |
| the machinery of billing | ACT_1 "double computer billings" · ACT_4 "the necessary reliance on computers" | 5 |
| the paper and the record | ACT_2 "no description of a dispute resolution process was ever distributed" · "So where was the ladder written down?" | 3 |
| the office and the counter | ACT_1 the counter beat · ACT_2 the four rungs · ACT_4 "a designated employee" | 6 |
| the city and the utility | ACT_2 "the company sending the bills was the city" | 6 |
| people as shadow and blur | ACT_5 "an employee of uncertain authority" · "thousands of customers" | 6 |

**The weakest register is the paper and the record, at three clips.** That is where the two
mailbox/envelope gaps and the three late duplicate removals all landed, and it is the register
the motif runs on. If any commissioned stills are added for EP64, add them there: the folded
notice, the envelope, the two flyers, the card ledger. The archive cannot supply them.

Deliberately **not** staged, per `forbidden_subjects`: courtroom interiors, gavels, benches;
cells, bars, handcuffs; any depiction of a family; anyone freezing, any house fire, any body; a
utility worker shot as a villain; a hand on a shoulder, a tear, a clock ticking down. No staged
clip shows a street number, a name tag, a badge, an ID card, a readable bill or a meter dial.

## 6. Every clip and its verdict

### accepted (57)

| clip | source | query that found it | what it serves |
|---|---|---|---|
| `AR-10599680__hand_putting_handset_on_fixed_phone.mp4` | pexels | `handset on fixed phone` | pale rotary wall phone, a hand replacing the handset -- HOOK 'the handset hanging off its cradle' and ACT_1 motif state 3 |
| `AR-10599685__close_up_on_hand_choosing_number_on_fixed_phone.mp4` | pexels | `hand choosing number on fixed phone` | a hand dialling a fixed phone, no face -- 'she called the defendant's offices' |
| `AR-10709675__house_during_winter.mp4` | pexels | `house during winter` | a single-storey house in snow, no signage and no street number -- the residence in winter |
| `AR-11159656__person_walking_at_sunset_in_winter.mp4` | pexels | `person walking at sunset in winter` | a snowy alley and fence at dusk; the only figure is distant and unrecognisable -- winter exterior |
| `AR-11730362__close_up_of_an_industrial_printing_machine_worki.mp4` | pexels | `industrial printing machine` | a printing machine feeding paper -- 'double computer billings', the machine that made two bills |
| `AR-11792113__a_man_carrying_a_torch_while_walking_in_a_park_o.mp4` | pexels | `carrying a torch` | one lamp and a distant walker on a dark road -- ACT_5 'the meter reader stays' |
| `AR-1721320__a_ringing_vintage_telephone.mp4` | pexels | `ringing vintage telephone` | black rotary desk phone, warm wood -- the telephone motif, ENDING callback |
| `AR-18124607__church_oil_lamp.mp4` | pexels | `(already in the pool before this pass)` | a flame in a metal holder against black; the church is not in frame -- the light that is left |
| `AR-18288122__power_plant.mp4` | pexels | `power plant` | generating plant over a town -- the utility behind the bill (ACT_2 'the company sending the bills was the city') |
| `AR-19010572__a_street_light_is_seen_in_the_dark_with_snow_fal.mp4` | pexels | `street light is seen in the dark with snow falling` | street lamp with snow streaking through it -- winter, ACT_4 'discontinuance of heating may threaten health and safety' |
| `AR-20055095__a_snow_covered_roof_with_a_chimney_and_a_snow_co.mp4` | pexels | `snow covered roof with a chimney` | snow-covered roof and chimney -- the house in winter |
| `AR-29906418__industrial_printing_process_machinery_in_operati.mp4` | pexels | `industrial printing machine` | dark industrial rollers turning -- the billing machinery (family cap: 3 with AR-29975896, AR-30183303) |
| `AR-29975896__industrial_printing_press_machinery_in_operation.mp4` | pexels | `industrial printing press` | second angle on working machinery -- ACT_4 'the necessary reliance on computers' |
| `AR-30148659__heavy_snowfall_during_nighttime_winter_storm.mp4` | pexels | `winter night snowfall` | heavy snow at night, real photography -- winter (preferred over AR-19468012, same shot type) |
| `AR-30183303__white_paper_rolling_through_industrial_machine.mp4` | pexels | `white paper rolling through industrial machine` | white paper rolling through a machine -- the bills being produced |
| `AR-31220606__close_up_of_vintage_car_dashboard.mp4` | pexels | `vintage car dashboard` | period car dashboard and round gauges -- the era, and the meter reader's round |
| `AR-31751374__industrial_machine_control_panel_close_up.mp4` | pexels | `control panel` | weathered wall-mounted control box with lit buttons -- the nearest thing on this shelf to a meter on a house wall |
| `AR-31811337__vintage_8mm_footage_of_window_flower_box.mp4` | pexels | `vintage 8mm footage` | 8mm of a window box on a weatherboard house -- period domestic exterior |
| `AR-31811394__vintage_8mm_film_of_suburban_neighborhood.mp4` | pexels | `vintage 8mm film` | 8mm suburban street with light leak -- ACT_1 'reside on Alaska Street in Memphis' |
| `AR-31966138__vintage_8mm_film_of_person_on_lawn_mower.mp4` | pexels | `vintage 8mm film` | 8mm of a yard, subject back-to-camera -- period domestic, no face |
| `AR-32023790__elegant_fountain_pen_writing_close_up.mp4` | pexels | `fountain pen` | nib writing lorem-ipsum cursive, illegible -- 'the trial judge wrote', 'the Court printed it' |
| `AR-32301726__retro_home_exterior_in_winter_1960s_footage.mp4` | pexels | `retro home exterior` | 1960s colour footage of a single-storey house with awnings -- the hero plate for the residence |
| `AR-32788087__silhouette_of_man_working_in_a_dimly_lit_study.mp4` | pexels | `dimly lit study` | back-lit silhouette at a desk lamp -- the household with the bills at night |
| `AR-32853473__lighting_a_gas_stove_top_burner.mp4` | pexels | `lighting a gas stove` | a gas ring lit in the dark -- the gas in Memphis Light, Gas & Water |
| `AR-33464306__vintage_black_and_white_telephone_focus.mp4` | pexels | `vintage black and white telephone` | black rotary telephone in monochrome -- the motif in period grade |
| `AR-33874629__moody_illumination_with_vintage_light_fixture.mp4` | pexels | `vintage light fixture` | one small warm window in the dark -- the house with the lights still on |
| `AR-34195865__aerial_black_and_white_cityscape_at_night.mp4` | pexels | `black and white cityscape` | monochrome aerial of a city at night -- 'a municipality... subject to the ultimate control of the municipal government' |
| `AR-34750195__snowy_urban_night_scene_with_passing_vehicles.mp4` | pexels | `snowy urban night scene` | snowy street at night with passing vehicles -- winter city |
| `AR-3534898__road_covered_with_snow.mp4` | pexels | `road covered with snow` | snow-covered path and hedge with a lit window behind -- the approach to the door |
| `AR-3573543__street_footage_with_snowfall.mp4` | pexels | `street footage with snowfall` | wide snowy street at night -- winter city |
| `AR-36989632__mysterious_indoor_scene_with_flowing_curtains.mp4` | pexels | `(already in the pool before this pass)` | bare room, white curtains at a window -- the empty room, ⟨HELD⟩ beats |
| `AR-3753693__shadow_footage_of_a_man.mp4` | pexels | `shadow footage of a man` | a head in shadow cast on a wall -- 'an employee of uncertain authority' |
| `AR-37554583__silhouette_hands_on_frosted_glass_at_night.mp4` | pexels | `frosted glass` | a hand pressed on cold glass at night -- the cold from inside |
| `AR-4076116__heavy_snowfall_at_night_in_winter.mp4` | pexels | `heavy snowfall at night` | snow-covered residential street with parked cars under lamps -- the street in winter |
| `AR-4183797__light_and_shadows_time_lapse.mp4` | pexels | `(already in the pool before this pass)` | window-light shadow crossing an empty wall -- time passing, the reset beats |
| `AR-4203360__moving_cars_on_a_winter_weather.mp4` | pexels | `moving cars on a winter weather` | an American street in snow with a municipal truck -- the city at work (use 0-4s; a lit bus destination board appears late) |
| `AR-4553292__a_room_with_many_boxes_stacked_on_top_of_each_ot.mp4` | pexels | `stack of boxes` | boxes stacked in a dim room -- the record, the file that nobody could explain |
| `AR-5483227__reflection_in_the_glass_of_a_man_walking_in_the.mp4` | pexels | `reflection in the glass of a man walking in the office` | empty modern office behind glass, figure unrecognisable -- the Division's offices |
| `AR-5644254__a_house_with_brown_roof.mp4` | pexels | `house with brown roof` | modest single-storey house with a brown roof and chimney -- the residence |
| `AR-5677966__shadow_of_a_person_walking.mp4` | pexels | `shadow of a person walking` | a walker's shadow on tarmac -- the meter reader arriving and leaving |
| `AR-5716999__modern_office_interior.mp4` | pexels | `modern office interior` | an empty meeting room -- 'a meeting with a responsible employee empowered to resolve the dispute' |
| `AR-5844276__low_angle_shot_of_a_house.mp4` | pexels | `low angle shot of a house` | weatherboard house with red frames, low angle -- the exterior register the brief asks for |
| `AR-5976357__a_person_standing_behind_a_glass_wall.mp4` | pexels | `standing behind a glass wall` | a lit glass frontage at night with an indistinct figure -- the office, closed |
| `AR-6540588__drone_footage_of_an_industrial_area.mp4` | pexels | `drone footage of an industrial area` | an industrial plume over a hazy city at dusk -- the utility over the city |
| `AR-6781559__back_view_of_woman_opening_curtain.mp4` | pexels | `(already in the pool before this pass)` | a woman opening a curtain, back to camera throughout -- the house at the window |
| `AR-7255749__a_cup_of_hot_beverage_on_the_table.mp4` | pexels | `cup of hot beverage on the table` | a hand and a cup on a table, someone reading behind, no face -- the kitchen table |
| `AR-7710495__a_person_finding_a_document.mp4` | pexels | `finding a document` | hands turning pages of a document, body copy illegible -- the record that never agreed with itself |
| `AR-8518319__an_industrial_plant_in_the_night_time.mp4` | pexels | `industrial plant in the night time` | an industrial plant lit at night -- the utility that never stops |
| `AR-853844__blurry_footage_of_people_inside_a_office.mp4` | pexels | `blurry footage of people inside a office` | an office of blurred, unrecognisable people -- 'thirty or forty Division employees' |
| `AR-853946__black_and_white_video_of_a_busy_street.mp4` | pexels | `black and white video of a busy street` | a heavily defocused monochrome crowd -- 'thousands of customers of various levels of education' |
| `AR-8706309__close_up_video_of_a_vintage_telephone_dial_pad.mp4` | pexels | `vintage telephone dial pad` | red rotary dial, close -- 'Phone 523-0711, information center' |
| `AR-9792408__worker_in_hardhat_working_on_lift_at_night.mp4` | pexels | `worker in hardhat` | a worker aloft at night, tiny and faceless -- the crew at the end of the thirty-day clock |
| `AR-v_136087__gas_stove_gas_switch_off_energy_crisis_energy_cr.mp4` | pixabay_extra | `gas stove` | a gas ring burning, dark kitchen -- the gas half of the service |
| `AR-v_2151__electricity_wires_time_lapse_sunset_cables_indus.mp4` | pixabay_extra | `electricity wires` | pylons and lines against a sunset -- the electricity half of the service |
| `AR-v_23470__pylons_electricity_power_pylons_energy_voltage_p.mp4` | pixabay_extra | `electricity wires` | a transmission pylon from below -- the network the second meter was wired into |
| `AR-v_23757__stove_fire_gas_kitchen.mp4` | pixabay_extra | `gas stove` | domestic gas hob alight -- the kitchen |
| `AR-v_7087__smoke_chimney_smoking_winter_heat_environmental.mp4` | pixabay_extra | `smoke chimney winter` | a roof plume against a frosted tree -- heating in winter, the house |


### rejected — 210 rows: 65 from the earlier pass, 145 from this one

| clip | why |
|---|---|
| `AR-10095255__drone_footage_of_an_abandoned_industrial_area.mp4` | duplicates the power-plant register already carried by AR-18288122 |
| `AR-10347787__a_woman_posing_while_holding_a_stack_of_folders.mp4` | check_cross_episode_reuse: identical source already staged in williams (as AF-BG-23691__case_files_stack_desk.mp4) |
| `AR-10692235__cars_on_street_in_winter.mp4` | a foreign street, out of focus |
| `AR-10765696__walking_on_forest_road_in_winter.mp4` | a forest track in snow -- rural register; this case happens on a city street |
| `AR-11008817__a_suburban_alleyway_covered_in_snow.mp4` | check_cross_episode_reuse: identical source already staged in weimer (as AF-BG-22106__white_picket_fence.mp4) |
| `AR-11353677__wood_burning_in_fireplace.mp4` | a cosy fireplace loop -- advertising register, and this episode forbids dramatising warmth as consequence |
| `AR-11543712__close_up_on_fire_in_fireplace.mp4` | a cosy fireplace loop -- advertising register, and this episode forbids dramatising warmth as consequence |
| `AR-11765182__close_up_view_of_antique_books.mp4` | antique library books with gilt spine lettering -- not this record |
| `AR-11798288__video_of_paper_shredding.mp4` | check_cross_episode_reuse: identical source already staged in forfeiture (as AF-BG-23796__shredded_documents_pile.mp4) |
| `AR-11999579__tuning_vintage_radio.mp4` | Zenith radio dial: a legible brand name and dial numerals that read as a meter; no radio in the script |
| `AR-12206553__close_up_of_fire_in_pipe.mp4` | an industrial gas flare -- reads as fire and danger, and the spec forbids harm dramatised as a consequence |
| `AR-12298877__shadow_of_person_with_scythe.mp4` | a hooded figure with a scythe |
| `AR-12405677__hands_taking_telephone.mp4` | hot-pink styled telephone set -- advertising colour, wrong register |
| `AR-12495__smoke_with_fluorescent_particles_on_black_backgr.mp4` | abstract particles |
| `AR-13037020__euro_coins_falling_on_an_orange_surface.mp4` | scan_video_shape: under_hd 1920x1078 -- upscaling into a 1920x1080 film |
| `AR-13081949__burning_logs_in_a_fireplace.mp4` | a cosy fireplace loop -- advertising register, and this episode forbids dramatising warmth as consequence |
| `AR-13244549__people_waiting_at_airport.mp4` | an airport departure lounge |
| `AR-15157535__strobe_led_lights_in_a_dark_room.mp4` | a nightclub strobe |
| `AR-15442472__a_black_and_white_photo_of_people_walking_throug.mp4` | a railway station concourse under a landmark arched roof |
| `AR-15820__desk_view_of_woman_walking_bike_into_modern_offi.mp4` | scan_video_shape: under_hd 1280x720 -- upscaling into a 1920x1080 film |
| `AR-15824279__a_light_is_shining_in_the_dark.mp4` | all but black; there is no picture in it |
| `AR-16943442__a_man_is_standing_in_front_of_a_control_panel.mp4` | garish green and red modern factory panel, with a person in frame whose face is unverified |
| `AR-17151509__a_person_walking_through_a_library_with_books.mp4` | check_cross_episode_reuse (re-run after the shared index was rebuilt mid-session): identical source already staged in frazier, gardner, lech (as AF-BG-0593__law_library_books.mp4) |
| `AR-17670727__lampe_traditionnel_africaine.mp4` | a paraffin storm lantern hung in foliage -- camping register, not a house without power |
| `AR-17807248__telephone_kiosk_booth.mp4` | a British red phone box covered in legible graffiti |
| `AR-1797017__bank_note_and_magnifying_glass.mp4` | dollar-bill macro: legible denomination, and the all-seeing-eye framing is a conspiracy trope |
| `AR-18812653__a_person_is_holding_a_flame_in_the_dark.mp4` | a burning note whose handwriting is fully legible |
| `AR-18969594__a_large_library_with_many_books_on_shelves.mp4` | an identifiable landmark library; grandiose and wrong |
| `AR-19107709__alternative_energy_large_power_plants_drone.mp4` | a modern solar farm |
| `AR-19428465__a_coin_on_a_table_with_a_wooden_surface.mp4` | check_cross_episode_reuse (re-run after the shared index was rebuilt mid-session): identical source already staged in young (as AF-BG-28712__courtroom_gavel_block_macro.mp4) |
| `AR-19468012__real_snow_captured_at_night.mp4` | snow against black -- the same shot type as AR-30148659, which is stronger |
| `AR-19504843__snow_fall_during_a_winter_evening_a_tree_covered.mp4` | bokeh through branches, foreign street behind |
| `AR-19886712__snow_falling_on_the_ground_in_the_woods.mp4` | out-of-focus snow bokeh in woodland; no subject |
| `AR-19887086__snow_falling_on_the_ground_in_the_winter.mp4` | check_cross_episode_reuse: identical source already staged in weimer (as AR-19887086__snow_falling_on_the_ground_in_the_winter.mp4) |
| `AR-20142904__vintage_radio.mp4` | a period tape recorder -- there is no recorder in this record |
| `AR-20563164__guy_sitting_in_dark_room_working_on_his_laptop.mp4` | a modern laptop in a 1978 story |
| `AR-2248637__abandoned_building_in_an_industrial_area.mp4` | a derelict industrial shed -- dereliction implies ruin; this utility functioned |
| `AR-248__phone_on_round_end_table.mp4` | a modern smartphone; the story turns on a 1978 landline |
| `AR-25865440__a_black_and_white_photo_of_people_walking_in_a_s.mp4` | a subway concourse |
| `AR-26085__girl_eating_salad_in_her_kitchen_dining_room.mp4` | advertising kitchen with a face front of frame |
| `AR-26583810__a_fire_is_burning_in_a_fireplace_with_a_black_ba.mp4` | a cosy fireplace loop -- advertising register, and this episode forbids dramatising warmth as consequence |
| `AR-2699388__a_pile_of_burning_firewood_inside_the_fireplace.mp4` | a cosy fireplace loop -- advertising register, and this episode forbids dramatising warmth as consequence |
| `AR-28148270__a_dark_blurry_image_of_a_person_in_a_dark_room.mp4` | an orange blur |
| `AR-2836277__people_waiting_to_cross_the_street_on_the_pedest.mp4` | a city crossing -- identifiable faces, a legible licence plate and shop signage |
| `AR-29193370__snowfall_in_urban_night_landscape.mp4` | check_cross_episode_reuse: identical source already staged in tyler (as AF-BG-10718__snowy_street_night.mp4) |
| `AR-29417147__dramatic_night_scene_through_red_lit_window.mp4` | horror lighting |
| `AR-29562989__cozy_empty_cafe_at_night.mp4` | a modern cafe interior |
| `AR-29570736__adjusting_vintage_radio_dial_tuning_retro_freque.mp4` | retro radio handled with a modern manicure -- anachronism, and radio is not a register here |
| `AR-29633673__winter_night_snowfall_in_silent_darkness.mp4` | near-black; nothing reads |
| `AR-29755925__abstract_shimmering_crystals_in_darkness.mp4` | abstract filler |
| `AR-29906414__industrial_printing_press_operating_in_slow_moti.mp4` | check_cross_episode_reuse: identical source already staged in forfeiture, kyllo, unlock, young (as AF-BG-10313__newspaper_printing_press.mp4) |
| `AR-29906415__industrial_printing_press_in_operation_with_mach.mp4` | check_cross_episode_reuse: identical source already staged in kyllo (as AF-BG-10314__newspaper_printing_press.mp4) |
| `AR-29975898__industrial_printing_press_producing_paper_sheets.mp4` | check_cross_episode_reuse: identical source already staged in kidsforcash (as AF-BG-10315__newspaper_printing_press.mp4) |
| `AR-30814424__outdoor_rainfall_on_empty_wooden_cafe_table.mp4` | an outdoor cafe bench; the table in this script is a kitchen table indoors |
| `AR-30910631__lonely_tree_in_snowy_winter_landscape.mp4` | a lone tree in a field -- rural, and it matches no line in the script |
| `AR-30922271__abstract_dust_particles_in_motion_against_dark_b.mp4` | abstract filler |
| `AR-31012329__person_reading_handwritten_notes_indoors.mp4` | check_cross_episode_reuse (re-run after the shared index was rebuilt mid-session): identical source already staged in norfolk (as AR-30998273__close_up_of_person_reading_handwritten_letter.mp4) |
| `AR-31050550__darkroom_video_editing_studio_with_professionals.mp4` | modern edit-suite monitors |
| `AR-31170350__snowy_night_traffic_scene_in_urban_setting.mp4` | a night street with Chinese shop signage |
| `AR-31220595__classic_car_dashboard_close_up_vintage_vibe.mp4` | the same car shoot as AR-31220606 |
| `AR-31576430__empty_tunnel_at_night_with_curved_roadway.mp4` | a motorway tunnel with green route signs |
| `AR-31750574__close_up_of_hands_handling_stacks_of_currency.mp4` | check_cross_episode_reuse: identical source already staged in hinders (as AF-BG-4125__money_cash_counting.mp4) |
| `AR-31799466__sacred_candles_flickering_in_dark_church.mp4` | a church interior; the register is religious, not domestic |
| `AR-31800816__vintage_film_grain_overlay_effect.mp4` | a flat grey film-grain overlay plate; not a picture |
| `AR-31938875__retro_film_leader_with_flicker_effects.mp4` | near-black film leader |
| `AR-32102723__vintage_golf_swing_on_8mm_film.mp4` | golf |
| `AR-32258717__aerial_view_of_snow_covered_city_statue.mp4` | a foreign city square with legible shop signage |
| `AR-32296437__vintage_reel_to_reel_tape_recorder_in_action.mp4` | a reel-to-reel tape recorder -- not in this record |
| `AR-32308941__silhouette_hand_shadows_creative_art.mp4` | hand-shadow art on a balloon |
| `AR-33145789__abstract_neon_patterns_over_dark_background.mp4` | abstract filler |
| `AR-34279531__mystery_night_scene_with_vintage_car_in_driveway.mp4` | check_cross_episode_reuse: identical source already staged in tyler (as AF-BG-1672__suburban_house_exterior_night.mp4) |
| `AR-34460938__warm_candlelight_ambience_in_dark_setting.mp4` | a bank of votive candles -- ceremonial and religious |
| `AR-34576055__sparse_crowd_at_soccer_stadium_during_match.mp4` | a football stadium |
| `AR-34645464__bright_lens_flare_in_dark_abstract_background.mp4` | abstract filler |
| `AR-34686009__vibrant_soccer_stadium_before_a_match.mp4` | a football stadium |
| `AR-34771084__minimalist_vietnamese_interior_with_lamp.mp4` | check_cross_episode_reuse: already burned in lech |
| `AR-35270173__glowing_green_particles_in_abstract_dark_space.mp4` | abstract filler |
| `AR-35286672__abstract_glittering_particles_dark_background.mp4` | abstract filler |
| `AR-35323521__traditional_south_indian_wedding_lamp_ceremony.mp4` | a wedding ceremony |
| `AR-35342049__soothing_candle_flame_in_dark_room.mp4` | check_cross_episode_reuse: already burned in flowers |
| `AR-3534899__road_covered_with_snow.mp4` | check_cross_episode_reuse: identical source already staged in tyler, young (as AF-BG-10714__snowy_street_night.mp4) |
| `AR-35421265__woman_enjoying_snowfall_in_winter_night.mp4` | a woman's face sharp and centred |
| `AR-35769379__winter_forest_scene_with_snow_covered_gate.mp4` | a woodland gate -- rural |
| `AR-35803533__360_degree_urban_cityscape_black_and_white_view.mp4` | a 360 tiny-planet distortion -- a gimmick alien to this film |
| `AR-35889601__nighttime_view_of_cozy_home_interior.mp4` | check_cross_episode_reuse: identical source already staged in caniglia, tyler (as AF-BG-1668__suburban_house_exterior_night.mp4) |
| `AR-3611037__static_footage_of_black_and_white_in_an_old_film.mp4` | a black frame |
| `AR-36123913__dramatic_black_and_white_oceanfront_cityscape.mp4` | a seafront |
| `AR-36624076__opening_window_blinds_to_view_italian_street.mp4` | the shutters open onto an identifiable Italian street with vehicles and road signs |
| `AR-36746548__moody_urban_view_through_window_blinds.mp4` | check_cross_episode_reuse: identical source already staged in thompson (as AF-BG-51478__window_blinds_shadow_stripes.mp4) |
| `AR-37090524__shadow_play_creates_rabbit_silhouette_on_wall.mp4` | a hand-shadow rabbit -- whimsical; the same family the earlier pass rejected |
| `AR-37165248__aerial_view_of_tennessee_capitol_at_dusk.mp4` | the Tennessee State Capitol, plainly identifiable, and Nashville is not Memphis |
| `AR-3735744__plastic_containers_inside_a_drawer.mp4` | a yellow-gloved hand -- lab or cleaning register |
| `AR-37554585__silhouetted_hands_against_frosted_glass.mp4` | the same shoot as AR-37554583 |
| `AR-37935065__quiet_stroll_past_traditional_homes.mp4` | check_cross_episode_reuse: identical source already staged in rolin (as AF-BG-22891__white_house_exterior.mp4) |
| `AR-37962427__dynamic_trading_terminal_in_dark_room_environmen.mp4` | crypto trading monitors |
| `AR-41359__woman_eating_noodles_in_the_kitchen.mp4` | a vertical phone clip of someone eating |
| `AR-4161816__a_close_up_shot_of_a_stone_wall.mp4` | a featureless wall texture |
| `AR-4252053__the_chimney_of_an_abandoned_manufacturing_plant.mp4` | looking up a derelict chimney -- no line in this script |
| `AR-4320604__close_up_shot_of_smoke_on_a_black_background.mp4` | smoke on black; abstract filler with nothing in it |
| `AR-4320606__close_up_shot_of_smoke_on_a_black_background.mp4` | smoke on black; abstract filler with nothing in it |
| `AR-4320718__close_up_shot_of_smoke_on_a_black_background.mp4` | smoke on black; abstract filler with nothing in it |
| `AR-4519611__snow_falling_on_the_road.mp4` | scan_video_shape: under_hd 1280x720 -- upscaling into a 1920x1080 film |
| `AR-45298__grey_smoke_on_a_black_background.mp4` | smoke on black; abstract filler with nothing in it |
| `AR-4553296__a_room_with_many_boxes_stacked_on_top_of_each_ot.mp4` | check_cross_episode_reuse: identical source already staged in lech (as AF-BG-8915__moving_boxes_empty_room.mp4) |
| `AR-45745__close_up_shot_of_an_office_worker_sipping_on_a_c.mp4` | scan_video_shape: under_hd 1280x720 -- upscaling into a 1920x1080 film |
| `AR-4646330__a_black_and_white_photo_of_a_person_in_a_dark_ro.mp4` | almost entirely black |
| `AR-47013__slow_motion_of_falling_coins.mp4` | scan_video_shape: under_hd 1280x720 -- upscaling into a 1920x1080 film |
| `AR-4848103__a_lit_candle_in_the_dark.mp4` | check_cross_episode_reuse: already burned in flowers |
| `AR-4848379__a_lit_candle_in_the_dark.mp4` | identical red candle to AR-4848103; keeping both would be a repeat |
| `AR-4919561__an_empty_waiting_area_in_the_airport_terminal.mp4` | check_cross_episode_reuse: identical source already staged in rolin (as AF-BG-11394__airport_terminal_empty.mp4) |
| `AR-49256__receptionist_working_at_a_front_desk_in_an_offic.mp4` | scan_video_shape: under_hd 1280x720 -- upscaling into a 1920x1080 film |
| `AR-5072388__a_footage_of_a_beautiful_house.mp4` | an estate-agent hero shot of a large modern house |
| `AR-5155184__shadow_a_man_over_a_wall.mp4` | check_cross_episode_reuse: already burned in young |
| `AR-5228150__people_passing_by_the_bank.mp4` | an HSBC branch -- third-party brand signage, and British |
| `AR-5283818__close_up_of_pages_of_a_book.mp4` | the printed page text is legible |
| `AR-5283824__pages_of_a_book_being_flipped.mp4` | the page text becomes legible and is about protein and anatomy |
| `AR-5651774__us_dollars_on_the_table.mp4` | a banknote with a legible serial number |
| `AR-5767251__candle_in_the_dark.mp4` | check_cross_episode_reuse: already burned in onecoin, thompson, titan |
| `AR-5981608__people_talking_over_cubicle_dividers.mp4` | identifiable face |
| `AR-5981609__a_woman_looking_over_her_cubicle_divider.mp4` | identifiable face |
| `AR-5994030__typing_a_quote_on_a_piece_of_paper.mp4` | the typed text becomes legible and reads 'Fake Ne...' -- wrong meaning and legible document text |
| `AR-6034872__snow_covering_the_suburb_surroundings.mp4` | check_cross_episode_reuse: identical source already staged in tyler, weimer (as AF-BG-1674__suburban_house_exterior_night.mp4) |
| `AR-6101325__a_woman_holding_a_pen.mp4` | a scales-of-justice statuette, the generic symbol the owner has ruled against, plus a face behind it |
| `AR-6173646__shadow_on_a_snow_covered_ground.mp4` | check_cross_episode_reuse: identical source already staged in weimer (as AF-BG-22104__white_picket_fence.mp4) |
| `AR-6177009__paper_clips_falling_in_a_pink_background.mp4` | a flat pink frame |
| `AR-6215354__close_up_view_of_a_genie_lamp.mp4` | a genie lamp |
| `AR-6266257__a_woman_counting_paper_bills.mp4` | check_cross_episode_reuse: identical source already staged in hinders (as AF-BG-23986__money_counting_machine.mp4) |
| `AR-6419222__footage_of_robert_moses_niagara_power_plant.mp4` | a named hydroelectric installation; the power-plant register is already carried by AR-18288122 |
| `AR-6443909__woman_opening_curtain.mp4` | bright modern bedroom with fairy lights, shot like an advert |
| `AR-6446152__a_woman_opening_the_curtain.mp4` | bright modern interior, advertising register |
| `AR-6527125__blizzard_of_snow_in_a_deserted_road.mp4` | a European street with tram rails |
| `AR-6527126__snow_flakes_falling_at_night.mp4` | check_cross_episode_reuse: identical source already staged in weimer (as AFPART-0249__snow_falling_dark.mp4) |
| `AR-6527130__snowfall_in_the_dark.mp4` | near-black |
| `AR-6527472__snow_falling_on_the_road.mp4` | the same European tram street as AR-6527125 |
| `AR-6549976__looking_among_files.mp4` | a card index whose labels are legible Cyrillic -- foreign-language personal records |
| `AR-6646702__volunteer_holding_hands_with_elderly_man.mp4` | VOLUNTEER is legible on the sleeve, and it is the hand-on-hand stock emotion the spec forbids |
| `AR-6721646__view_of_the_snow_covered_street_in_the_city.mp4` | a European boulevard |
| `AR-6777032__cementery_in_winter.mp4` | a cemetery |
| `AR-6825170__person_walking_in_snowy_pathway.mp4` | a park path under autumn foliage; no subject and no season match |
| `AR-6929600__writing_expenses_in_note_pad.mp4` | a modern smartphone is prominent in frame |
| `AR-6929604__a_person_magnifying_a_document.mp4` | check_cross_episode_reuse: identical source already staged in rolin (as AF-BG-15139__magnifying_glass_on_document.mp4) |
| `AR-6964495__person_talking_while_holding_a_binder.mp4` | identifiable face |
| `AR-7033616__faint_smoke_on_a_black_background.mp4` | smoke on black; abstract filler with nothing in it |
| `AR-7088504__the_control_panel_of_an_ultrasound_machine.mp4` | a medical ultrasound console |
| `AR-7344846__seals_and_nibs_on_papers_with_spilled_ink.mp4` | check_cross_episode_reuse: identical source already staged in forfeiture, thompson (as AF-BG-14315__wax_seal_on_document.mp4) |
| `AR-7606613__a_leaflet_spread_over_the_table.mp4` | travel-map set dressing; the 'leaflet' is a map |
| `AR-7606813__light_reflection_over_the_wall.mp4` | world-map wall decor |
| `AR-7651532__close_up_shot_of_a_document_with_graph_on_a_tabl.mp4` | check_cross_episode_reuse: identical source already staged in flowers, morton, norfolk, postoffice, willingham (as AF-BG-30301__documents_on_desk.mp4) |
| `AR-7692021__a_dancing_woman_s_shadow_on_a_wall.mp4` | a dancing silhouette |
| `AR-7710452__a_person_finding_a_document.mp4` | check_cross_episode_reuse: identical source already staged in tyler (as AF-BG-23698__case_files_stack_desk.mp4) |
| `AR-7710453__a_person_finding_a_document.mp4` | check_cross_episode_reuse: identical source already staged in carsearch, cotton (as AF-BG-23802__shredded_documents_pile.mp4) |
| `AR-7744349__high_angle_shot_of_a_fountain_pen.mp4` | a flat-lay still life; near-static |
| `AR-7744350__close_up_video_of_a_fountain_pen.mp4` | a still-life desk flat-lay; near-static |
| `AR-7744415__paper_clips.mp4` | a near-static graphic still |
| `AR-7791919__scattered_paper_clips.mp4` | a near-empty white frame |
| `AR-7822026__a_person_filling_in_a_form.mp4` | check_cross_episode_reuse: identical source already staged in frazier (as AF-BG-8250__contract_paperwork_signing.mp4) |
| `AR-7822031__a_person_filling_up_a_form.mp4` | check_cross_episode_reuse: identical source already staged in rolin (as AF-BG-63123__audit_documents_stack.mp4) | scan_video_shape: under_hd 1280x720 -- upscaling into a 1920x1080 film |
| `AR-7830056__white_painted_wall.mp4` | a featureless white wall |
| `AR-7947425__graphs_printed_on_paper.mp4` | stock-chart printouts -- markets, not a household bill |
| `AR-7947449__graphs_and_charts_printed_on_paper.mp4` | check_cross_episode_reuse: identical source already staged in onecoin (as AF-BG-15132__magnifying_glass_on_document.mp4) |
| `AR-8042899__a_footage_of_a_lamppost.mp4` | check_cross_episode_reuse: already burned in lech |
| `AR-8103486__paper_bills_and_coins_on_a_guitar_case.mp4` | a busker's guitar case |
| `AR-8103504__paper_bills_and_coins_on_the_guitar_case.mp4` | a busker's guitar case |
| `AR-8103666__coins_and_paper_bills_on_a_black_case.mp4` | check_cross_episode_reuse: identical source already staged in rolin (as AF-BG-28943__open_briefcase_of_cash.mp4) |
| `AR-8124298__close_up_of_a_businessperson_s_hands_on_a_table.mp4` | a green-screen backdrop is visible at frame right, and the papers are bright craft card |
| `AR-8135311__a_hand_holding_a_pen.mp4` | scan_video_shape: under_hd 1366x720 -- upscaling into a 1920x1080 film |
| `AR-8269950__a_person_operating_vintage_radio.mp4` | a period radio handled with a modern manicure |
| `AR-8334801__tattooed_woman_behind_a_see_through_curtain.mp4` | scan_video_shape: 1366x720 below 1920x1080 -- upscaling into a 1920x1080 film |
| `AR-8369920__high_angle_shot_of_bitcoins_on_wooden_table.mp4` | bitcoin |
| `AR-8369972__close_up_of_stacked_coins.mp4` | bitcoin |
| `AR-8369977__close_up_of_stacked_coins_in_lined.mp4` | bitcoin |
| `AR-8369987__stacked_of_bitcoins_on_the_table.mp4` | bitcoin |
| `AR-8370146__a_gold_coin_on_a_wooden_table.mp4` | bitcoin |
| `AR-8370538__bitcoins_on_a_wooden_table.mp4` | bitcoin |
| `AR-8371852__person_looking_at_files_inside_a_cardboard_box.mp4` | check_cross_episode_reuse: identical source already staged in caniglia, carsearch, katz, kyllo, rodriguez (as AF-BG-10219__stacked_legal_documents.mp4) |
| `AR-8478747__a_person_filling_up_a_form.mp4` | check_cross_episode_reuse: identical source already staged in rolin (as AF-BG-32810__contract_paperwork_signing.mp4) |
| `AR-8517529__a_woman_opening_a_curtain.mp4` | she turns and her face is fully visible at 60% and 90% of the clip -- invisible on the single-frame sheet |
| `AR-854549__people_waiting.mp4` | an airport lounge with the runway visible behind |
| `AR-855381__fireplace.mp4` | a cosy fireplace loop -- advertising register, and this episode forbids dramatising warmth as consequence |
| `AR-8731580__a_person_holding_a_pen.mp4` | check_cross_episode_reuse: identical source already staged in florence, gardner, king, young (as hand_sign.mp4) |
| `AR-8971157__elderly_couple_holding_hands.mp4` | the hand-on-hand stock emotion the spec forbids by name |
| `AR-914__open_office_space.mp4` | a contemporary open-plan tech office |
| `AR-917__open_office_space_and_staircase.mp4` | the same location as AR-914 |
| `AR-9196613__a_footage_of_a_woman_looking_at_the_lighting_bul.mp4` | staged: a face lit by a prop bulb |
| `AR-9198046__a_man_turning_pages_of_a_book.mp4` | the face is fully visible at 70% and 95% -- invisible on the single-frame sheet |
| `AR-9520__american_dollars_with_coins_falling_on_top.mp4` | scan_video_shape: under_hd 1280x720 -- upscaling into a 1920x1080 film |
| `AR-v_100947__black_lamp_light_spotlight_dark_light_bulb_shutt.mp4` | an abstract white shape on black |
| `AR-v_101451__black_light_dark_light_bulb_smoke_lamp_moon_nigh.mp4` | almost entirely black |
| `AR-v_122354__curtain_wind_window_room_home.mp4` | a saturated magenta curtain -- advertising colour |
| `AR-v_131330__home_wind_furniture_interior_lifestyle_door_curt.mp4` | scan_video_shape: portrait 2160x3840 |
| `AR-v_141854__plate_gas_fire_kitchen_matches_burns_prepare.mp4` | scan_video_shape: portrait / 1080x1920 below 1920x1080 -- upscaling into a 1920x1080 film |
| `AR-v_141924__window_candles_snow_winter_light_trees_night_dar.mp4` | an AI-looking blue window scene |
| `AR-v_143161__man_kitchen_model_dishes.mp4` | a modern kitchen with a face |
| `AR-v_144689__finland_porvoo_borg_old_wooden_warehouse_village.mp4` | a Finnish riverside village |
| `AR-v_151491__board_chips_closer_computer_science_technology_w.mp4` | a modern RGB-lit motherboard |
| `AR-v_153221__room_house_table_furniture_interior_weather_nigh.mp4` | an AI-rendered interior |
| `AR-v_153296__house_room_furniture_interior_night_light_window.mp4` | an AI-rendered log cabin |
| `AR-v_156879__cherry_blossom_living_room_window_night.mp4` | an AI-rendered room with a giant moon |
| `AR-v_186863__table_candles_night_window_curtain_moon_stars.mp4` | an AI-rendered romantic candle scene |
| `AR-v_220153__gas_oil_industry_natural_view_car_trip_vehicle_s.mp4` | a desert flare stack |
| `AR-v_236415__floor_lamp_lamp_ceiling_light_lighting_bulb_arch.mp4` | decorative outdoor lamps |
| `AR-v_2673__fire_flame_gas_gas_fire_warm.mp4` | scan_video_shape: under_hd 1280x720 -- upscaling into a 1920x1080 film |
| `AR-v_2674__fire_flame_gas_gas_fire_coal_warm.mp4` | a gas coal-effect fire -- the cosy-fireplace family this episode already rejected |
| `AR-v_31991__home_kitchen_interior_window_design.mp4` | an estate-agent kitchen |
| `AR-v_341293__book_reading_hands_elderly_old_fingers_pages_lit.mp4` | a face in motion blur; wrong register |
| `AR-v_40818__corridor_office_bank_employees_deposit_money_bus.mp4` | two people walk up to camera with clear faces and a uniform badge at 90% |
| `AR-v_50452__transport_urban_windows_tramway_street_night_tra.mp4` | a tram |
| `AR-v_51919__flame_gas_gas_stove_cooking_appliance.mp4` | a fourth gas-hob clip; the register is already carried by three better ones |
| `AR-v_55206__light_bulb_globe_electric_lamp_planet_lamp_earth.mp4` | a CG globe inside a bulb |
| `AR-v_82015__light_bulbs_lights_decorative_decoration_electri.mp4` | decorative string lights against an advertising sunset |

## 7. Cut caveats the builder must honour

- `AR-4203360` — use the first four seconds. A lit bus destination board comes into frame later.
- `AR-32023790` — the handwriting under the nib is lorem ipsum and stays illegible; safe throughout.
- `AR-7710495`, `AR-31012329` — keep the document at the scale shown on the sheet. Both are body
  copy at that size; push in and they become readable.
- Family caps, or `footage_diversity` will bite: telephone ≤6, snow-at-night ≤5, house exterior
  ≤5, industrial machinery ≤3, gas hob ≤3.

## 8. How to reproduce or extend this

```bash
py -3.11 scripts/shelf.py                                   # what the shelf holds, by source
py -3.11 scripts/search_archive.py --shot "<shot>" --kind video --md --sheet [--weak-ok]
py -3.11 scripts/stage_footage_by_title.py --slug memphis --per-query 3 --query "<title terms>" ...
py -3.11 scripts/scan_video_shape.py --root remotion/public/memphis/factory --stage both
py -3.11 scripts/check_cross_episode_reuse.py --check remotion/public/memphis/factory/*.mp4
py -3.11 scripts/build_footage_contact_sheet.py --dir remotion/public/memphis/factory \
        --media video --out-dir runs/qc/memphis_factory
py -3.11 scripts/write_factory_clip_qc.py --slug memphis
```

`stage_footage_by_title.py` writes `runs/qc/<slug>_title_staging.v001.json` on **every** run and
overwrites it. Two rounds were staged here, so the receipt was rebuilt from the archive ledger
afterwards to cover both rounds and both pools; if you stage again, copy the receipt first.

The full query list used in this pass is stored in that receipt under `queries`.
