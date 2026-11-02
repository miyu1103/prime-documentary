# EP63 · CORREA v. HOSPITAL SAN FRANCISCO — 実写素材プラン v001

【対象】`episodes/PD-2026-063-correa` ／ 台本 `EP63_correa_script.en.v002.md` ／
契約 `episodes/PD-2026-063-correa/episode_spec.v001.json`
【作業日】2026-08-10 ／ 記録者 claude
【結果】プール **8本 → 58本**。床は約42本（本編約32分・45秒に1本）なので **+16本（38%超過）**。

---

## 0. 30秒で分かる結論

```
棚（実測 2026-08-10）   151,869点 / うち動画 31,150本
うち EP63 が使える動画   15,427本（1920x1080以上・横位置・商用可・どの話も未使用）
コンタクトシート閲覧     候補218 + 検証146 + 最終プール58 = 全タイル目視
ステージ                 77本 → 19本を撤回 → 58本
撤回の内訳               目視9本（顔2/グリーンバック1/文字2/重複2/その他2）＋ 話またぎ重複10本
```

**`factory_used` の承認済み偏差を「棚が薄いから」という理由で使う必要はもう無い。**
薄かったのは棚ではなく**クエリの書き方**だった（§2）。この偏差は
`episode_spec.v001.json` の `approved_deviations` に残っているが、その根拠は本プランで消えた。

---

## 1. 台本から起こしたレジスター（何を撮り集めるか）

台本 v002 を読んで導出。左が画、右が仕える台詞。

| # | レジスター | 台本の該当箇所 |
|---|---|---|
| R1 | 空席の列・ベンチ | HOOK cut 3「the empty row of waiting chairs」／ACT_1「Then the waiting.」／ACT_3 C138／ACT_4 reset beat |
| R2 | 施設の廊下・通路・エスカレーター | ACT_1「she was inside that emergency room」／ACT_3「the Hospital staff continued blithely to ignore her」 |
| R3 | 扉・非常口・エレベーター | HOOK cut 4「the fogged emergency doors」／ACT_4「Nobody sent her away」 |
| R4 | 番号札・発券機・白紙 | 全編の motif（1 dispenser／2 fan of blanks／3 in the hand …）「a Hospital employee assigned the patient a number, forty-seven」 |
| R5 | 記録・カード目録・書類棚 | ACT_3「the Hospital's utter inability to produce any records」「compilation of a written chart」／motif 6「an empty drawer, an unfilled shelf」 |
| R6 | 時計 | ACT_1「Add up the clock.」 |
| R7 | 雨・窓の雨滴 | 1991年9月のプエルトリコ。ACT_1 の待機、ENDING の静けさ |
| R8 | 熱帯の光と植生 | 事件地はプエルトリコ。本土ではない |
| R9 | 車での移動 | ACT_1「the two women drove to the office of Dr. Acacia Rojas Davis」 |
| R10 | 薬（人物なし） | ACT_1「she had taken a double dose of her high blood pressure medication」「dispensed medicine to control the emesis」 |
| R11 | 電話 | ACT_1／ACT_4「a nurse called from HSF to advise her that the patient would be coming」 |
| R12 | 金銭 | ACT_2「conditioning hospitals' continued participation in the federal Medicare program — a lucrative source of institutional revenue」／ACT_2・ACT_5 の70万ドル |
| R13 | 夜の旧市街・街路 | ACT_5・ENDING の余韻。植民地都市の街並みは旧サンフアンの代替 |
| R14 | 蛍光灯・光と影 | ACT_3「the fluorescent strip」系。無人の施設の空気 |

**契約が禁じるもの**（`forbidden_subjects`）はレジスター設計の段階で外した：
法廷／法槌／判事席、独房／鉄格子／手錠、実在の病院・裁判所、患者・臨床処置・救急ドラマ、
生成画像内の可読文字、そして「ストック的な感情演出（肩に置いた手・涙・**カウントダウンする時計**・落ちる法槌）」。
R6 の時計は、**カウントダウン表現を全部落として**、施設の壁掛け時計 1 本だけに絞った（§4）。

---

## 2. クエリ ― 失敗したものと、何を直したか

`docs/PD_ARCHIVE_SHELF_WORKLOG.v001.md` §4 と `docs/PD_CANON.md` §10 の通り、
**0件は棚の事実ではなく自分の語彙の事実**。今回もそのまま再現した。

### 2-1 監督の言葉 → 提供者の語彙

初回に走らせた素朴な語（全部 0 件）と、実際に当たった書き換え：

| 監督の言葉 | 件数 | 提供者の語彙に直す | 件数 |
|---|---:|---|---:|
| `waiting room` | **0** | `waiting` 単独 ＋ テーマ走査 | 10 |
| `hospital corridor` | **0** | `corridor` / `walkway` / `escalator` / `tunnel` | 61 |
| `reception desk` / `reception counter` / `front desk` | **0** | `counter` / `desk` / `clerk` | 53 |
| `rain on window` / `raindrops on window` | **0** | `raindrop` / `rain glass` / `wet glass` | 251 |
| `filing cabinet` / `file cabinet` / `archive shelves` | **0** | `card catalog` / `shelves` / `storage containers` | 199 |
| `double doors` / `automatic door` / `swinging doors` | **0** | `door open` / `glass door` / `entrance` / `exit` | 111 |
| `stretcher` / `gurney` / `hospital bed` | **0** | （代替せず。§4-3 の理由で不採用） | — |
| `paper stack` / `index card` / `archive box` | **0** | `stack books` / `stacks of storage containers` | 26 |
| `ceiling fan` / `water cooler` / `linoleum` | **0** | （棚に無い。小道具か生成の領域） | 0 |
| `number display` | 2 | `ticket machine` | 3 |

### 2-2 もっと効いた発見：**この棚の題名は3種類ある**

`scripts/shelf.py` 経由で全行を読んで初めて分かったこと。

| レーン | 題名の形 | 検索の書き方 |
|---|---|---|
| `pexels` 5,045本 | 自然文（`a card catalog at a library`） | 語をANDで並べる。フレーズでも当たる |
| `pixabay_extra` 6,737本 | **カンマ区切りのタグ列**（`rain, water, floors, wet, drops, moisture, colombia`） | フレーズは絶対に当たらない。**単語をANDする** |
| `pixabay` 2,683本 | **題名が文字列 "id"**（2,672本）または `untitled` | **題名では引けない。テーマでしか届かない** |
| `mixkit` 607本 | 英文（先頭大文字） | 語をANDで並べる |

`pixabay` レーンの 2,672本は題名が丸ごと壊れている。`waiting room` が 0件だった理由の一部はこれで、
**題名検索を使う限りこのレーンは全部見えない**。本プランはここに手を出していない（テーマ×ソースの
コンタクトシートで見るしかない）。棚スレへの申し送り。

### 2-3 テーマで引き直して当たったもの

題名の語彙で届かない先はテーマで走査した。当たり：

- `documents_paper` 304本 → **図書館のカード目録**。ACT_3「記録が一枚も出せなかった」に対する
  最良の対語（引き出しがぎっしり詰まっている画）。プールの中核になった
- `medical_lab` 204本 → 人物なしの錠剤・ブリスターパック。R10 はここだけで足りた
- `money_banking` 859本＋`finance_money` 362本 → R12
- `atmosphere_symbolic` 726本／`light` 794本 → R14

外れ：`bench_to_line` 19本はテーマ名が完全に嘘で、中身はピザ窯・モデル撮影・工場のカプセル充填機。
`civic_voting` 119本は投票所と抗議デモで、`empty polling station` は使えそうに見えて
**VOTE DAY の掲示と星条旗が読める**（§4-2）。

---

## 3. 探した棚（レーン別）

`from shelf import shelf_rows`（`scripts/shelf.py`）で1回だけ棚を読み、
ライセンス・隔離・`unusable` 判定・解像度・話またぎ使用済みを順に引いた実測。

```
棚 全体                       151,869
 └ 動画                        31,150
     ライセンス不可 -1,246
     unusable判定  -3,771
     1920x1080未満 -7,339
     縦位置          -296
     他話で使用済み -2,620 …（作業中に -3,000超まで増えた。§5）
   = EP63が使える動画        15,427
```

| レーン | 使える動画 | 何が出たか |
|---|---:|---|
| `pixabay_extra` | 6,754 | 熱帯の雨（コロンビア）、植民地の街路、走行、廊下。**タグ列題名** |
| `pexels` | 5,045 | カード目録、錠剤、電話、雨、図書館。**プールの大半** |
| `pixabay` | 2,683 | **題名 "id" で到達不能**（§2-2） |
| `mixkit` | 607 | 白紙・壁掛け時計・硬貨・オフィス電話 |
| `nasa` | 314 | 該当なし（宇宙のみ） |
| `coverr` | 48 | 該当なし |
| `ia` | 30 | 該当なし（1080p以上が30本しかない。ia は72.9%がSD） |
| `nara` | 19 | 該当なし（nara は89.3%がSD） |
| `wikimedia` / `loc` | **0** | 動画レーンではない。1920x1080以上の動画は1本も無い |

**wikimedia 5,569点・loc 3,092点・nara 3,600点は静止画の棚**で、
「1920x1080以上の横位置動画」という本話の条件では実質ゼロだった。これは今回測って確定した事実。

---

## 4. 目視 ― 何を見て、何を落としたか

### 4-1 見た枚数

| シート | 枚数 | 目的 |
|---|---:|---|
| `runs/qc/correa_candidates/*_01..11.png` | 218 | 一次選別（1秒地点） |
| `runs/qc/correa_verify35`・`correa_verify75` | 90×2 | **35% と 75% 地点** |
| `runs/qc/correa_verify2_35`・`correa_verify2_75` | 36×2 | 2巡目 |
| `runs/qc/correa_verify3_35`・`correa_verify3_75` | 20×2 | 3巡目 |
| `runs/qc/correa_spot` | 12 | 疑いのある4本を30/60/90%で |
| `runs/qc/correa_factory/*_01..03.png` | 58 | 最終プール全数 |

### 4-2 **1秒地点のシートは嘘をつく**（今回いちばん重要）

`build_footage_contact_sheet.py` は `-ss 1` で1枚抜く。EP65 の事故
（`woman_sitting_on_a_chair_while_reading_a_magazine` という名前の中に、
顔がはっきり中央に写った実在人物がいた）は、**ファイル名だけでなく1枚目のフレームも
何も教えてくれない**という話だった。今回、同じ形の当たりが3本出た：

| クリップ | 1秒地点 | 35% / 75% 地点 |
|---|---|---|
| `pexels 6631722` "woman standing and waiting" | 後ろ手に組んだ手だけ。無人・匿名の待機として理想的 | **眼鏡とサージカルマスクの女性の顔が鮮明。白衣**。臨床スタッフ |
| `pexels 9198046` "a man turning pages of a book" | 縞シャツの手だけ | **若い男性の満面の笑顔が中央に** |
| `pixabay_extra v_95520` "office space, entrance…" | 明るいオフィス廊下の茶色い扉 | **HDR のクリスマス商店街に切り替わる**（モンタージュ素材） |
| `pexels 8524018` "a person sitting on a wheelchair" | 脚だけ・顔なし | 白ホリゾント。**車椅子の広告**だと分かる |
| `pexels v_67483` "elevator, …, green screen, …" | 白いエレベーター扉 | **90%地点で全面グリーンバック**。合成用プレート |

**機構化の提案**：`build_footage_contact_sheet.py` に `--at <fraction>` を足し、
出荷前レビューを 1秒・35%・75% の3枚組にする。今回は ffmpeg で外から抜いて
同じツールに `--from-json` で食わせて代用した（`scratchpad/midframes.py` 相当の手順）。

### 4-3 プールに入れてから撤回した19本

**目視で落とした9本**（`remotion/public/correa/factory_offtheme/` へ移動）

| ファイル | 理由 |
|---|---|
| `AR-6755024__patient_in_a_reception_of_a_clinic` | 白衣の男性と受付の女性、**顔が2つとも識別可能**。実在の臨床シーン。`forbidden_subjects` 直撃。**初回パスから入っていて accept 扱いだった** |
| `AR-6081049__a_couple_talking_on_a_bench_in_a_waiting_area` | **マスク姿の患者2名**の実在クリニック待合。マスクは2020年以降を示し、事件は1991年。**初回パスから入っていた** |
| `AR-v_67483__elevator_lift_green_screen_…` | 90%地点で**全面グリーンバック**。**初回パスから入っていた** |
| `AR-6549272__a_man_looking_at_card_catalogs_in_a_library` | 男性の顔が鮮明。`catalog card library` クエリの相乗り |
| `AR-7252265__…getting_ticket_from…` | `odbierz bilet / collect your ticket` がポーランド語で可読 |
| `AR-5220466__person_buying_a_ticket_from_ticketing_machine` | 印字パネルが可読、自販機に見える |
| `AR-50990__timelapse_of_a_car_driving_through_the_city_at_n` | 光跡タイムラプス。この局が使わない表現 |
| `AR-6745972__a_person_getting_some_books_from_the_shelf` | キリル文字の背表紙 |
| `AR-6550666__a_person_browsing_through_card_catalogs` | 同一撮影の重複（カード目録は6本入ってきたので3本に絞った） |

**話またぎ重複で落とした10本**（`remotion/public/correa/factory_crossused/` へ移動）→ §5-2

### 4-4 ステージ前に落とした主なもの

全49件は `runs/qc/correa_clip_verdicts.v001.json` の
`screened_out_before_staging` に理由つきで記録した。類型：

- **顔** 18件（`5483205` は顔＋**ラニヤードのIDバッジ**。病院ものでバッジは特に警戒した）
- **可読の看板・ロゴ** 9件（Lenovo広告、RESTAURANT、Peugeotのエアバッグ、東京・香港の商店街）
- **CG・イラスト・グリーンバック** 12件（`v_270787`〜`v_270794` の8本は全部「木造酒場のCGレンダ」）
- **禁止レジスター** 4件（救急車、法廷、監房、`bars`）
- **主張の安全性** 2件 — `6549770 burning pages of a diary` と `6550234 burning pages`。
  絵としては強いが、**書類が燃える画は「病院が記録を破棄した」と言ってしまう**。
  判決が言っているのは「一枚も出せなかった」だけで、`forbidden_claims` はそれ以上を許さない。
  これは見た目ではなく事実で落とした唯一のケース。
- **真っ黒／無地** 4件（`12820367 empty building interior` は最初のフレームが黒一色）

**空港の待合は5本まとめて落とした。** 棚の中で「待合室」にいちばん近いのは空港の
出発ロビーだが、飛行機・搭乗ゲート・出発案内板が写る。marmet が同じ理由で
`people_are_sitting_in_chairs_in_an_airport` を落としている。同じ判断を踏襲した。

**映画館も落とした**（初回パスが `AR-7988176 empty red chair in the cinema` を落としているため）。
ただし `AR-29732319 empty theater seats in a quiet cinema` **だけは採った** — 座席の背に
**1・2・3・4 と番号が振られている**フレームで、スクリーンも通路も写らない。番号のついた空席は
この作品の motif そのもの。判断であって事故ではない。

---

## 5. 作業中に起きた2つの事故（次の人が踏まないように）

### 5-1 **棚を他の話と取り合っていた**

12:31 に候補索引を作り、218本をシートで見て65本を選び終えた 12:55 に、
**そのうち23本が既に greene と memphis のプールに入っていた**。13:10 にはさらに6本。
候補は 15,878 → 15,506 → 15,427 と目の前で減った。

- 失った23本には、電話4本すべて、ブラインド2本すべて、壁掛け時計、
  ガラス扉、白紙の一枚、「people waiting」の逆光シルエットが含まれていた
- **教訓：レビューが終わったら即ステージする。** 2巡目のレビューを挟むと持っていかれる

### 5-2 **話またぎ判定がID方式では効かない**

`stage_footage_by_title.py` の重複除外は
`AR-<台帳のid>` と既存ステージ名を突き合わせる。ところが factory 棚は 2026-08-10 に
**提供元のIDへ全面リネームされた**ので、**他の話に旧 `AF-BG-*` 名で入っているクリップは
このガードから完全に見えない**。

```
AR-11769112__close_up_of_a_male_hand_taking_a_book…  = kyllo の AF-BG-63059__old_ledger_book.mp4
AR-4169122__close_up_shot_of_a_moving_pendulum       = caniglia/unlock の AF-BG-14187__antique_brass_scales.mp4
AR-6538597__a_woman_getting_a_file                   = caniglia/dbcooper の AF-BG-1279__documents_on_desk.mp4
AR-6549279__a_person_using_a_library_catalog         = frazier/lech の AF-BG-10147__old_library_archive.mp4
AR-6550655__man_picking_up_a_book_from_the_shelf     = frazier の AF-BG-33692__old_library_archive.mp4
AR-6781564__a_person_holding_a_business_summary      = frazier の AF-BG-4522__documents_on_desk.mp4
```

内容ハッシュで測る `check_cross_episode_reuse.py`（size + 先頭256KBのsha1）だけが見つけた。
`AF-BG-14187` が「天秤」として3話で使われていたのも、これで初めて分かった
（オーナーの「天秤クリップ多用しすぎ」はまだ生きている）。

**残り4本**は §5-1 の競合で、同じ AR- 名が greene / forfeiture / gardner / frazier にも入った。
10本すべて撤回。最終プールの話またぎ重複は **0件**（再ビルド後に再測定）。

**次の人へ：ステージのたびに `check_cross_episode_reuse.py --build --check` を回す。**
ID一致は当てにならない。

### 5-3 その他の罠

- `stage_footage_by_title.py` は**実行のたびに受領書 `runs/qc/<slug>_title_staging.v001.json` を
  上書きする**。5回に分けて流したので4回分が消えた。`write_factory_clip_qc.py` は
  この受領書からクリップ毎の証拠（題名・出典・ライセンス）を読むので、消えた分は
  「証拠なし」になる。**プール全体を台帳から引き直して再構成した**
- 同ツールは**題名が一意でないクリップを指定できない**。「people waiting」を題名に含む動画は
  棚に49本あり、狙った1本は9番目。`--per-query` は先頭からN本しか取れないので到達できない。
  3本（`854549 people waiting`／`v_136286 hand writing`／`18302 counting money`）を
  この理由だけで諦めた。ツールに `--id` を足せば解決する
- `--min-mb 1.0` の既定値で `6006383 person moving her wheelchair`（0.93MB）が黙って落ちた
- 4K の pixabay_extra は既定の `--max-mb 120` を超える。`--max-mb 400` で流した

**目視で合格したのにステージできなかった5本**（プール58本には入っていない）:
`854549 people waiting`（棚に「people waiting」を含む題名が49本、狙いは9番目）／
`v_136286 hand writing on a notepad`（10本中7番目）／`18302 counting money`（34本中31番目）／
`5014476 heavy rain footage`（23本中8番目）／`26746388 rain`（1,081本中198番目）。
**全部「題名が一意でない」という同じ理由**で、素材の問題ではなくツールの問題。§8-2 参照。

---

## 6. 最終プール58本 ― どの台詞に仕えるか

`remotion/public/correa/factory/`。すべて **1920x1080以上・横位置・商用可・他話未使用**を機械で確認済み。

### R1 空席・待機 — HOOK cut 3／ACT_1「Then the waiting.」／ACT_3 C138／ACT_4 reset beat
| クリップ | 画 |
|---|---|
| `AR-29732319` empty theater seats in a quiet cinema | **背番号1〜4の空席の列**。motif（47番）の直接の対応物 |
| `AR-6284510` a pan shot of white benches | 明るい室内の白いベンチ列をパン |
| `AR-34580818` cozy sunlit corner with yellow armchair | ブラインド越しの光と誰も座っていない椅子。ENDING の余韻 |

### R2 廊下・通路 — ACT_1／ACT_3「continued blithely to ignore her」
| クリップ | 画 |
|---|---|
| `AR-35039967` modern melbourne metro walkway | **無人のタイル張り通路が消失点まで**。R2の中心 |
| `AR-35273413` modern underground tunnel with escalators | リブ天井のトンネル、無人 |
| `AR-28829130` moody underground tunnel walk with neon lights | 長い地下通路に人影ひとつ |
| `AR-34576517` lonely man walking on covered bridge tunnel | 背中だけの人物が歩き去る。ACT_1「she got up and left」 |
| `AR-8772864` an escalator is moving down in a subway station | 下りエスカレーター、暗い |
| `AR-5968236` top view of escalator in a building | 手すりの金属だけ。抽象だが動いている |
| `AR-v_130783` elevator, door, open, waiting elevator, sliding door | 無人のエレベーター扉 |

### R3 扉・非常口 — HOOK cut 4／ACT_4「Nobody sent her away」
| クリップ | 画 |
|---|---|
| `AR-7644222` an exit signage at the building | 緑の非常口サイン |
| `AR-9945020` video of a fluorescent lights | 蛍光灯の管（R14と兼務） |

### R4 番号札・発券機・白紙 — 全編の motif
| クリップ | 画 |
|---|---|
| `AR-7252272` close up video of a ticket machine | **発券口から白い紙が出る**。motif 状態1（dispenser） |

### R5 記録・カード目録 — ACT_3「utter inability to produce any records」／motif 6
| クリップ | 画 |
|---|---|
| `AR-6550428` a card catalog at a library | **カード目録の引き出しが両側に延びる廊下**。ACT_3 の中心画 |
| `AR-6550424` a person browsing through card catalogs | 引き出しを開けるとカードがぎっしり |
| `AR-6550134` a hand touching card catalogs at a library | 引き出しの面に手が触れる |
| `AR-4941466` stacks of storage containers | 灰色の整理棚が壁一面 |
| `AR-5095967` a person is holding an open book with a pen | 手書きの記録帳をめくる手 |
| `AR-5283825` macro shot of a book page | 活字のマクロ。ACT_3 の四原則の読み上げに |
| `AR-3009534` stack of books | 積み上がった古い本（スペイン語背表紙） |
| `AR-6550418` books on a table | テーブルに積まれた本 |
| `AR-8870088` a man walking inside the library | 暗い書庫、人影は小さく顔は読めない |

### R6 時計 — ACT_1「Add up the clock.」
| クリップ | 画 |
|---|---|
| `AR-28897` Slowly approaching a clock on a black background | **無地の壁掛け時計1本だけ**。カウントダウン系は全部落とした |

### R7 雨 — 1991年9月・プエルトリコ
| クリップ | 画 |
|---|---|
| `AR-9945249` raindrops falling on glass | 青いガラスの雨滴 |
| `AR-7681518` raindrops pouring on a glass surface | 灰色の濡れガラス |
| `AR-32086252` raindrops on umbrella calm weather scene | 傘の布に落ちる雨 |
| `AR-7843122` heavy raindrops falling | 緑を背にした豪雨 |
| `AR-7949070` slow motion video of raindrops | 濡れた縁石 |
| `AR-1727802` rain with thunder and lightning | 夜の雨の街路、街灯ひとつ |
| `AR-6804244` black and white footage of raining | モノクロ、傘の下の後ろ姿 |
| `AR-32161267` nighttime rain walk on city sidewalk | 雨の歩道を歩く後ろ姿 |
| `AR-v_42899` rain, water, floors, wet, drops, moisture, colombia | **熱帯の濡れた葉** |
| `AR-v_29584` nature, floors, trees, rain, colombia | **熱帯の雨に打たれる緑** |

### R8 熱帯の光と植生 — 事件地はプエルトリコ
| `AR-7318024` palm leaves swaying in the wind | 白空を背にした椰子の葉 |
| `AR-37218119` sunlight filtering through lush green jungle canopy | 樹冠を抜ける光条 |
| `AR-36022925` serene tropical waterfall with lush greenery | シダと水しぶき |

### R9 車での移動 — ACT_1「the two women drove to the office of Dr. Rojas」
| `AR-v_8735` car, rain, driving, hail, storm | **ワイパー越しの雨の走行**。この一本が「病院を出て走った」を担う |
| `AR-13643105` car driving at night | ヘッドライトが向かってくる |
| `AR-9977360` view from car driving on highway | 高速の車内視点 |
| `AR-v_120266` motoring, road, car, traffic, vehicle, driving | 荒れた空の下の空いた道路 |
| `AR-31940806` moody night drive in rainy urban setting | 雨の夜の路面 |
| `AR-33743353` nighttime rainy urban traffic scene | 雨のヘッドライト列 |
| `AR-5879298` pedestrians crossing the road | モノクロの道路と柵 |

### R10 薬 — ACT_1「a double dose of her high blood pressure medication」
| `AR-34380553` close up of white tablets on reflective surface | 白い錠剤2粒 |
| `AR-13048933` pills in blisters | ブリスターパック |
| `AR-5453774` view of medicines on a wooden table | 木のテーブルに散った錠剤 |

### R11 電話 — ACT_1／ACT_4「a nurse called from HSF」
| `AR-234` Hand dialing a phone | 事務用電話を押す手 |
| `AR-v_39249` telephone, booth, old, call | 公衆電話の受話器 |

（回転式ダイヤルの黒電話3本は §5-1 で memphis に取られた。この2本が残り）

### R12 金銭 — ACT_2「a lucrative source of institutional revenue」／70万ドル
| `AR-7735914` person counting banknotes | 紙幣を数える手 |
| `AR-18263` Hands of a man counting coins close up view | 手のひらに硬貨を落とす |
| `AR-31750576` a pile of assorted shiny coins | 硬貨の山 |
| `AR-18248` Scrambled American coins and bills seen very close | 米硬貨と紙幣のマクロ |
| `AR-5024` One dollar bill in detail | 1ドル札の彫刻 |

### R13 夜の旧市街 — ACT_5・ENDING
| `AR-v_24745` colonial, street, colombia, architecture, old, historic, town, latin | **ラテンアメリカの植民地都市の夜**。旧サンフアンの代替 |
| `AR-30339959` moody foggy night in cobblestone alley | 霧の石畳、無人 |
| `AR-19712943` a street with lights hanging from the ceiling | 灯りを渡した無人の路地 |
| `AR-v_49321` street, building, path, europe, barcelona, narrow | 花のバルコニーの細い路地 |
| `AR-4206` Walking through ibiza old town | 白壁の路地、陽光 |

> 注：R13 は地中海・ラテンアメリカの旧市街で、プエルトリコそのものではない。
> 棚に `san juan` は0件、`puerto rico` は1件（使えず）。**建物で場所を特定させない切り方**を
> 組み立て側に申し送る。看板が読めるカットは全部落としてある。

---

## 7. 組み立て側への申し送り

1. **`AR-35039967` に広告ディスプレイが写る。** 通路の壁に小さなデジタル看板があり、
   内容は判読できない。寄るなら左寄りを避けること
2. **R13 は「熱帯の旧市街らしさ」で使い、建物を主役にしない。** 実在の街が特定できる引きは避ける
3. **`AR-29732319` は劇場の座席**である。番号が見えるタイトなフレーミングだけを使い、
   通路や段差が入る引きは使わない
4. **カード目録3本は同一撮影**。1カットに続けて並べない（`footage_diversity` の再利用上限）
5. `factory_offtheme/` 55本と `factory_crossused/` 10本は**戻さない**。
   `stage_footage_by_title.py` は `factory*` 配下を全部除外するので、
   次に誰かがプールを足しても復活しない

## 8. 棚スレへの申し送り

1. **`pixabay` レーン2,672本は題名が文字列 `"id"`。** 題名検索の全ツールから見えない。
   `ia`/`nara` と違いこれはHDが多いレーンなので、埋め戻す価値がある
2. **`stage_footage_by_title.py` に `--id` が要る。** 題名が一意でないクリップは指定できず、
   今回3本を取り逃した
3. **同ツールの受領書は上書きされる。** 追記かマージにすべき
4. **`build_footage_contact_sheet.py` に `--at <fraction>` が要る。** §4-2
5. **ID方式の話またぎ判定は factory リネーム後は無効。** §5-2

---

## 9. 再現コマンド

```bash
# 棚を数え直す
py -3.11 scripts/shelf.py

# プールのコンタクトシート（全数目視の入口）
py -3.11 scripts/build_footage_contact_sheet.py --dir remotion/public/correa/factory --media video --out-dir runs/qc/correa_factory

# 話またぎ重複（内容ハッシュ。ID一致は当てにならない）
py -3.11 scripts/check_cross_episode_reuse.py --build --workers 12
py -3.11 scripts/check_cross_episode_reuse.py --check remotion/public/correa/factory/*.mp4

# クリップ毎のQC記録を manifest 側へ書く
py -3.11 scripts/write_factory_clip_qc.py --slug correa
```

**このプランでは manifest も film.json も再構築していないし、レンダーもしていない。**
