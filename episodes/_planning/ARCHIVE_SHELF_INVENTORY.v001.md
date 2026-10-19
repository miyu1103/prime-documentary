# Archive shelf — what it can actually supply (2026-08-21 00:15)

61,556 items / 1,219 GB across 47 themes, 15 sources.

**Read this before writing shot specs.** A theme name is the download query, not a subject — asking a shot spec for `weather_disasters` gets 358 GB of one flood survey. Search by SUBJECT (section 2), and only from rows section 1 marks `good`/`mixed`.

```
python scripts/search_archive.py --shot "courthouse exterior dusk" --kind video
python scripts/search_archive.py --shot "prison corridor" --md    # paste-ready rows
python scripts/qc_archive_contact_sheets.py --theme <theme>          # look before you trust
```

Filenames are `<source>__<id>__<title-slug>.<ext>` and 53,333/53,567 conform, but a name is NOT evidence: NOAA titles are survey codes and 27k NYPL scans all read `new-york-city-directory`. The verdicts below come from eyeballing the labeled sheets in `H:\pd-media\assets\archive\_qc\<theme>\`.

## 1. Supply and verdicts (theme x source)

> No verdicts recorded yet — run the contact sheets, fill `_qc\verdicts.template.jsonl`, save it as `_qc\archive_verdicts.jsonl`. Until then every row is UNJUDGED and must not be trusted blind.

| theme | source | items | GB | video/image/audio | verdict | real titles |
|---|---|---:|---:|---|---|---|
| ambience_beds | freesound | 1,067 | 4.4 | 0/0/1067 | — | crickets wav; alien facility c2 wav; the curtain closed e1 wav |
| americana_1930s_1970s | met | 305 | 0.9 | 0/305/0 | — | seated woman holding baby ionic porch and balustrade; allegory of rhetoric; overdoor panel with allegory of justice one of a pai |
| americana_1930s_1970s | loc | 220 | 11.6 | 0/220/0 | — | main street in philadelphia pennsylvania; view of store fronts along main street in benson ari; neon sign for mel s drive in and celebrity bar in th |
| americana_1930s_1970s | smithsonian | 19 | 0.1 | 0/19/0 | — | hampton county courthouse; new england factory life bell time from harper s wee; courthouse steps |
| americana_1930s_1970s | nara | 2 | 0.1 | 1/1/0 | — | industries of war railroad material forge shop forgi; downtown san francisco |
| bank_and_branch | wikimedia | 474 | 3.6 | 0/474/0 | — | file 10 dollars national commercial savings bank ltd; file 300 ashland and williamsburgh savings bank towe; file affaire de faux documents from a pawn shop 1 jp |
| bank_and_branch | coverr | 1 | 0.0 | 1/0/0 | — | close up of barista taking money from a customer |
| bench_to_line | mixkit | 45 | 1.3 | 45/0/0 | — | hand of a person squeezing an orange on a light back; white flowers in the breeze; scissors cutting a blue fabric |
| bench_to_line | ia | 2 | 0.3 | 2/0/0 | — | master hands |
| bench_to_line | coverr | 1 | 0.0 | 1/0/0 | — | angle grinder on metal |
| bgm_general | freesound | 381 | 1.8 | 0/0/381 | — | ambient sounds 13 mp3; ambient sounds 14 mp3; ambient sounds 006 |
| business_corporate | pixabay_extra | 766 | 4.5 | 236/530/0 | — | office office complex glass facade building city win; business professional office workplace corporate wom; writing hands pen paper desk office document work fo |
| business_corporate | mixkit | 88 | 1.7 | 88/0/0 | — | presentation of many fruits and vegetables; presentation of watermelon slices; worried man on phone call stares at laptop |
| business_corporate | unsplash | 50 | 0.1 | 0/50/0 | — | modern glass building with a flag; orange chairs around a wooden conference table; brown wooden 9 piece office table and chairs |
| business_corporate | coverr | 2 | 0.0 | 2/0/0 | — | a glass building on lisbon street; a glass building in lisbon |
| chicago_city | nara | 12 | 1.0 | 5/7/0 | — | illinois chicago; chicago riots chicago illinois; first division circus at chicago |
| courtroom_justice | pixabay_extra | 1,590 | 18.4 | 664/926/0 | — | couple on bench samsung wallpaper autumn romance bea; dark grim books pages paper read a book bound browse; high seat outlook hunting stand hunt hunting seat hu |
| courtroom_justice | loc | 1,077 | 45.6 | 0/1077/0 | — | plymouth county court house plymouth mass; worcester county court house fitchburg mass; monroe county court house monroe mich |
| courtroom_justice | mixkit | 178 | 3.5 | 178/0/0 | — | rinsing strawberries apples and grapes holding hands; man walking on large boulders; lady of justice at the dublin castle in ireland |
| courtroom_justice | nara | 51 | 4.6 | 29/22/0 | — | tablet on courthouse on u s route 40 at vandalia ill; trial of nazi spies cherbourg france trial of nazi s; first shot into germany theding france artillery 90t |
| courtroom_justice | unsplash | 50 | 0.3 | 0/50/0 | — | classical building with columns street lamp and dram; red courthouse with white columns under blue sky; a building with columns and snow on the ground |
| courtroom_justice | oyez | 31 | 0.5 | 0/0/31 | — | gideon v wainwright supreme court oral argument janu; gideon v wainwright supreme court oral argument janu; mapp v ohio supreme court oral argument march 29 196 |
| courtroom_justice | courtlistener | 9 | 0.3 | 0/0/9 | — | rodriguez v united states supreme court oral argumen; carpenter v united states supreme court oral argumen; timbs v indiana supreme court oral argument 2018 11 |
| courtroom_justice | coverr | 1 | 0.0 | 1/0/0 | — | walking to the mountain top |
| decision_rooms | wikimedia | 159 | 1.6 | 0/159/0 | — | file 1st international congress of working women cal; file 317 tb patients typing pool 1964 dpla 185cd8b58; file activities at the american federation of labor |
| decision_rooms | unsplash | 50 | 0.1 | 0/50/0 | — | white printer paper on black and brown granite table; a close up of a menu on a table; a drawing of a building on a piece of paper |
| decision_rooms | ia | 1 | 0.2 | 1/0/0 | — | new girl in the office the |
| depression_hardship | wikimedia | 173 | 1.7 | 0/173/0 | — | file 689 chapel chaplin soup kitchen dpla 0b45bedeeb; file 689 chapel chaplin soup kitchen dpla 0b45bedeeb; file 689 chapel chaplin soup kitchen dpla 0b45bedeeb |
| depression_hardship | loc | 79 | 1.9 | 0/79/0 | — | towards pretoria a record of the war between briton ; report of war emergency relief board cleveland ohio ; field genealogy being the record of all the field fa |
| depression_hardship | nara | 1 | 0.0 | 0/1/0 | — | an army relief team carries an army tent in a box to |
| economy_crisis | pixabay_extra | 695 | 4.7 | 205/490/0 | — | fence electric caution warning sign sign; europe italy storefront fruit food italian store sho; open shop inside street sell trade sign urban gray s |
| economy_crisis | wikimedia | 122 | 1.2 | 0/122/0 | — | file mypubliclandsroadtrip 2016 step back in time ga; file mypubliclandsroadtrip 2016 step back in time ga; file mypubliclandsroadtrip 2016 step back in time ga |
| economy_crisis | mixkit | 56 | 1.4 | 56/0/0 | — | waves crash on the shore; waves crash on the rocks; waves crash on a shore with boulders |
| economy_crisis | unsplash | 50 | 0.2 | 0/50/0 | — | closed sign on string; charming teal storefront with decorative lights and ; protestor holds a sign about due process |
| economy_crisis | ia | 1 | 0.1 | 1/0/0 | — | america marching on a screen editorial with lowell t |
| factory_manufacturing | wikimedia | 2,194 | 29.9 | 0/2194/0 | — | file 81 typical night scene in an indiana glass work; file 81 typical night scene in an indiana glass work; file 95 a glass works boy waiting for the night shif |
| factory_manufacturing | loc | 157 | 3.6 | 0/157/0 | — | west s moulders text book being pt ii of american fo; cotton mill processes and calculations an elementary; carding and spinning a book for practical mill men |
| factory_manufacturing | nara | 3 | 0.0 | 0/3/0 | — | annotated photo of anshan steel works anshan manchur; annotated photo of anshan steel works anshan manchur; stereos of anshan steel works anshan manchuria taken |
| goods_in_motion | pixabay_extra | 845 | 13.0 | 357/488/0 | — | ship sea water sight transport cargo ship nature tan; firewood woodpile wood pile stack timber cut lumber ; trailer old cargo to drag transport shipping trailer |
| goods_in_motion | wikimedia | 597 | 5.9 | 0/597/0 | — | file 111 sc 6343 quartermaster depot near railroad f; file 125 pennsylvania railroad freight depot west st; file 19th century wagon grain elevator dodge city jp |
| goods_in_motion | mixkit | 72 | 1.6 | 72/0/0 | — | cargo ship under the sun; cargo ship turning; drone flying past a cargo ship |
| goods_in_motion | unsplash | 50 | 0.2 | 0/50/0 | — | men in blue uniforms sorting fish in orange crates; a laptop computer sitting on top of a wooden table; black plastic containers on green plastic crate |
| government_buildings | pixabay_extra | 2,412 | 32.7 | 1028/1384/0 | — | mosque architecture islam arabic dome emirates relig; architecture buildings netherlands government buildi; basel switzerland modern architecture architectural |
| government_buildings | nara | 389 | 1.0 | 1/388/0 | — | george washington delivering his inaugural address a; entering old santa fe dome of the capitol building s; capitol |
| government_buildings | loc | 116 | 0.8 | 0/116/0 | — | the history of the raising of the first american fla; united states capitol; state capitol montgomery alabama |
| government_buildings | mixkit | 62 | 1.4 | 62/0/0 | — | philippine flag waving in the sky; the washington monument; american flags at the washington monument |
| government_buildings | unsplash | 50 | 0.2 | 0/50/0 | — | grand capitol building with a dome and columns; classical building facade with columns against cloud; the united states capitol building dome against blue |
| government_buildings | coverr | 1 | 0.0 | 1/0/0 | — | flags on a skyscraper |
| hands_and_transactions | mixkit | 597 | 14.2 | 597/0/0 | — | agricultural workers harvesting the field; dachshund dog while hands caress it; couple holding hands on the beach |
| household_loss | pixabay_extra | 160 | 3.5 | 160/0/0 | — | ruins, house, burnt, burned, building, door, windows; curtains, door, window, patio, movement, air, wind, ; chromakey, door, exit, outdoors, green screen, male, |
| household_loss | mixkit | 64 | 1.7 | 64/0/0 | — | Woman looking at nature through the window; Heavy rain from an open window; Young woman looking for discounts at the supermarket |
| household_loss | unsplash | 50 | 0.2 | 0/50/0 | — | a wooden door with a sign on it; aerial view of a suburban neighborhood with houses a; a dense suburban neighborhood with many houses |
| household_loss | wikimedia | 14 | 0.1 | 0/14/0 | — | file boarded up 50575803283 jpg; file boarded up 50576531891 jpg; file cash payment timeline on foreclosures jpg |
| household_loss | coverr | 1 | 0.0 | 1/0/0 | — | an old man looking out of the window |
| japan | pixabay_extra | 1,620 | 24.1 | 476/1144/0 | — | fuji japan sakura spring landscape girl kimono mount; heaven gate china temple roof architecture monastery; japan tokyo asia paper umbrellas japan tokyo tokyo t |
| japan | nara | 482 | 5.2 | 27/455/0 | — | mary galaktinoff and her family return to dutch harb; photograph of a navy scout observation plane wrecked; photograph of uss arizona on fire after attack on pe |
| japan | mixkit | 89 | 1.1 | 89/0/0 | — | ancient temple time lapse; japan flag waves gently in the wind; closeup of japan flag waving in wind |
| japan | unsplash | 50 | 0.3 | 0/50/0 | — | a city street filled with lots of neon signs; a tree branch with white flowers in front of a pagod; a busy city street at night with neon lights |
| japan | loc | 15 | 0.7 | 0/15/0 | — | a japanese and english dictionary with an english an; japan and japanese american relations; japan |
| japan | ia | 9 | 1.5 | 9/0/0 | — | children of japan; the enemy japan the people 2; the enemy japan the people |
| laboratory_forensics | noaa | 9 | 0.0 | 0/9/0 | — | aquarius laboratory; catlin seaview survey team at aquarius laboratory; david johnson appointed chief of the weather bureau |
| laboratory_forensics | smithsonian | 1 | 0.0 | 0/1/0 | — | model mars science laboratory mars rover curiosity |
| landscapes_timelapse | pixabay_extra | 1,886 | 32.4 | 736/1150/0 | — | patagonia argentina nature glacier summer cerro torr; mountains landscape painting dawn snowy peak nature ; desert landscape north of chile valley of the moon l |
| landscapes_timelapse | mixkit | 123 | 4.9 | 123/0/0 | — | grand canyon time lapse; a rancher riding a horse at sunset; heart shape in the snow mountains at sunset |
| landscapes_timelapse | nasa | 67 | 0.2 | 0/67/0 | — | malaspina glacier alaska; earth from orbit 2014; preparing for antarctic flights in the california de |
| landscapes_timelapse | unsplash | 50 | 0.2 | 0/50/0 | — | landscape photography of mountain ranges under purpl; a group of sand dunes with a blue sky in the backgro; green trees and snow covered mountains during daytim |
| landscapes_timelapse | coverr | 9 | 0.1 | 9/0/0 | — | timelapse of manhattan at sunset; timelapse of hot air balloons; timelapse of a house in the mountains |
| landscapes_timelapse | ia | 7 | 0.5 | 7/0/0 | — | juuson turha video diary clouds 26h timelapse 2; juuson turha video diary clouds 26h timelapse; blender sunset time lapse test1 |
| market_machinery | mixkit | 52 | 1.1 | 52/0/0 | — | green code scrolling on a monitor; a man lying on the bed scrolling on his phone; screen information reflects on a woman s glasses |
| market_machinery | unsplash | 50 | 0.2 | 0/50/0 | — | a close up of a clock on a metal surface; digital clock display with wires and tools; a group of numbers that are in the dark |
| market_machinery | coverr | 7 | 0.1 | 7/0/0 | — | a trader making a call with his smartphone; a trader analysing the cryptocurrency market; cryptocurrency trade platform |
| money_banking | pixabay_extra | 1,490 | 20.4 | 953/537/0 | — | bethlehem city houses hill view west bank bethlehem ; money finance house mortgage investment banking curr; classical dance bharatanatyam indian dance tradition |
| money_banking | wikimedia | 433 | 6.6 | 0/433/0 | — | file 081 first paper money of people s republic of c; file aerial view of the u s treasury building washin; file aerial view of u s treasury department building |
| money_banking | nara | 136 | 1.8 | 0/136/0 | — | u s mint building new philadelphia pa from north wes; u s mint building new philadelphia pa from south eas; u s mint building new philadelphia pa from south eas |
| money_banking | mixkit | 134 | 2.3 | 134/0/0 | — | casino poker table full of dice dollars and chips; closeup of hand using atm touchscreen; 3d moving gold coins |
| money_banking | loc | 88 | 3.4 | 0/88/0 | — | the bank and treasury bank capitalization and the pr; memory keys a table top treatise on unlocking the mi; washington loan trust company bank building washingt |
| money_banking | unsplash | 50 | 0.2 | 0/50/0 | — | a pile of one hundred dollar bills laying on top of ; close up photography of 1 u s dollar banknote lot; a pile of one hundred dollar bills |
| money_banking | coverr | 5 | 0.0 | 5/0/0 | — | a screen showing financial analysis of a cryptocurre; a businessman working on a stock market trading plat; a broker working with a candlestick chart |
| music_performance_pd_era | ia | 2 | 0.7 | 2/0/0 | — | command performance; music in motion |
| navy_harbor | nara | 443 | 22.6 | 168/275/0 | — | air attack on warships a gaping hole in the deck of ; air attack on warships a gaping hole in the deck of ; commission from foreign nations france arrival of th |
| navy_harbor | loc | 112 | 1.4 | 0/112/0 | — | the story of our navy; ship launching in portland maine the men behind the ; ss keystone state national defense reserve fleet ala |
| newspapers_printing | pixabay_extra | 1,007 | 9.5 | 399/608/0 | — | garlic garlic press pressed garlic extruded garlic c; hugs to press mortgage bottles business recycling; printing press antique printing press printing press |
| newspapers_printing | loc | 151 | 3.6 | 0/151/0 | — | printing and writing materials their evolution; printing in relation to graphic art; gutenberg and the art of printing |
| newspapers_printing | unsplash | 50 | 0.2 | 0/50/0 | — | the united states of america newspaper; a colorful print rests on an old printing press; the klettgauer bote newspaper is visible |
| newspapers_printing | mixkit | 46 | 0.9 | 46/0/0 | — | close up view of a typewriter while a man works on i; operation of a typewriter viewed in detail; hands of a person typing on a typewriter |
| ocean_nature | pixabay_extra | 2,110 | 72.3 | 969/1141/0 | — | currumbin beach aerial aerial photography beach wave; aquarium fish nature jellyfish coral sea animal wate; etretat nature france cliff normandy sea landscape b |
| ocean_nature | noaa | 148 | 0.6 | 1/147/0 | — | acropora coral ffs; anchor on reef tinian 2022; anthomastus coral |
| ocean_nature | nasa | 132 | 0.6 | 0/132/0 | — | space shuttle projects; ice bridge antarctic sea ice; the x 43a pegasus combination dropped into the pacif |
| ocean_nature | mixkit | 56 | 1.9 | 56/0/0 | — | surfer walking toward the ocean at sunset; sunrise on the ocean; aerial shot of a beach with sea waves |
| ocean_nature | unsplash | 50 | 0.2 | 0/50/0 | — | an underwater view of a seaweed in the ocean; a large group of fish swimming over a coral reef; a group of fish swimming over a coral reef |
| ocean_nature | coverr | 22 | 0.2 | 22/0/0 | — | the praia do pinh o coastline; foamy ocean waves at night; sandstone cliffs |
| ocean_nature | ia | 12 | 0.9 | 12/0/0 | — | coral wonderland; hills and the sea; beautiful ocean waves view for relaxation |
| pd_feature_films | ia | 178 | 87.1 | 178/0/0 | — | home movie 000416 1951 detroit area family; home movie 000419 1960s pennsylvania farm; home movie 000427 1944 fairview poultry farm il |
| period_telephone_tech | loc | 47 | 0.2 | 0/47/0 | — | a hand book of the electro magnetic telegraph; public ownership and the telephone in great britain ; lincoln in the telegraph office recollections of the |
| period_telephone_tech | nara | 8 | 0.5 | 3/5/0 | — | telephone operators on v e day; airplanes radio equipment navy s latest flying boat ; company e first telegraph battalion signal corps |
| police_modern | pixabay_extra | 1,602 | 25.5 | 739/863/0 | — | cop policewoman colleagues fun figure police funny l; cop policewoman colleagues fun figure police funny l; cop policewoman colleagues fun figure police funny l |
| police_modern | mixkit | 114 | 3.2 | 114/0/0 | — | a man in the dressing room putting on the armor iron; police lights in a dark background; online shoping with credit card |
| police_modern | unsplash | 50 | 0.2 | 0/50/0 | — | a police car parked on the side of the road; a police car parked in a parking lot at night; a police car stopped at an intersection at night |
| police_modern | coverr | 1 | 0.0 | 1/0/0 | — | traffic light timer |
| police_period | loc | 153 | 4.9 | 0/153/0 | — | hendricks collection no 30 police entering patrol wa; police gazette sporting annual; police record of the spies smugglers and rebel emiss |
| police_period | nara | 2 | 0.0 | 0/2/0 | — | u s navy master at arms 3rd class jacob faulkner and; a u s navy military police boat from naval station p |
| prison_jail | pixabay_extra | 1,489 | 13.2 | 416/1073/0 | — | fence pattern wire fence fence fence fence fence wir; electric fence wire tensioner rope tensioner wire me; electric fence wire tensioner rope tensioner wire me |
| prison_jail | unsplash | 27 | 0.1 | 0/27/0 | — | alcatraz island prison under a cloudy sky; alcatraz island in san francisco bay on a foggy day; alcatraz island with lighthouse and buildings by the |
| prison_jail | mixkit | 18 | 0.3 | 18/0/0 | — | hand on a wire fence by night; scary woman seeing through the window; on the phone by a window |
| retail_commerce | wikimedia | 922 | 10.8 | 0/922/0 | — | file 2024 photo of shopping walking women on the sun; file 024 02 free download photo of people shopping a; file 10th street market breads of india oakland jpg |
| retail_commerce | nara | 7 | 0.1 | 0/7/0 | — | american red cross classes in red cross work women s; american red cross war work war activities in duluth; a female naval officer speaks with a young girl in f |
| science_tech | nasa | 1,562 | 8.1 | 0/1562/0 | — | research technology; history of hubble space telescope hst; russian mission control center |
| science_tech | pixabay_extra | 1,382 | 14.7 | 683/699/0 | — | forest bench nature park tree walk wooden bench land; viewpoint telescope distance view riverbank outlook ; viewpoint telescope distance view riverbank outlook |
| science_tech | mixkit | 99 | 1.6 | 99/0/0 | — | computer code running on a screen; macro closeup video of microchips; video with digital trade network concept |
| science_tech | unsplash | 50 | 0.2 | 0/50/0 | — | close up of a dirty electronic circuit board; a close up of a printed circuit board; green circuit board |
| science_tech | smithsonian | 45 | 0.1 | 0/45/0 | — | microscope; microscope lerebours; what hath god wrought telegraph message |
| science_tech | noaa | 7 | 0.5 | 0/7/0 | — | advanced technology demonstrator radar dome installa; advanced technology demonstrator radar tower and dom; photo imets launch weather balloon 2023 imet trainin |
| science_tech | ia | 4 | 0.4 | 4/0/0 | — | threads of technology; classic tv commercial for a univac computer; univac computer commercials in 3d 2 |
| science_tech | met | 1 | 0.0 | 0/1/0 | — | celestial globe with clockwork |
| selling_floor | pixabay_extra | 537 | 5.3 | 228/309/0 | — | kenya africa the interior of the store souvenir shop; thumb hand human gesture sign language bad negative ; small business e commerce order packing business own |
| selling_floor | unsplash | 50 | 0.2 | 0/50/0 | — | a closed sign hanging from a glass door; sorry we re closed signboard hanging on glass door; a closed sign hangs on a glass door |
| selling_floor | mixkit | 44 | 0.9 | 44/0/0 | — | men discuss business sale on deck of yacht; escalators of a shopping center; cashiers smile at customer paying in fashion store |
| selling_floor | coverr | 3 | 0.0 | 3/0/0 | — | queue to carrefour market in paris; queue to a newspaper store; socially distanced queue |
| sfx_environment | freesound | 2,819 | 14.9 | 0/0/2819 | — | windynight wav; driving away at night mp3; walking at night mp3 |
| sfx_human_movement | freesound | 2,739 | 1.9 | 0/0/2739 | — | door handle close aif; door handle open aif; class 166 165 networker journey farnborough north as |
| sfx_mechanical | freesound | 1,629 | 2.1 | 0/0/1629 | — | car crash edit two aif; keyboard wav; keyboard writing wav |
| small_town | pixabay_extra | 1,337 | 23.9 | 564/773/0 | — | urban black and white elderly woman road puddle rain; road desert highway black and white nature road mark; mailbox postbox country side usa mail box postal let |
| small_town | loc | 384 | 23.5 | 0/384/0 | — | the custom house and main street; main street; water works systems for small towns cities etc |
| small_town | mixkit | 53 | 2.4 | 53/0/0 | — | Person watering a small plant by hand; Small boat heading out for the night; Small shark swimming |
| small_town | unsplash | 50 | 0.2 | 0/50/0 | — | blackfoot water tower against a cloudy sky; a water tower with the name linden on it; american flag reflected in a storefront window |
| space_nasa | nasa | 9,450 | 364.2 | 631/8819/0 | — | international space station iss; advanced space transportation program astp; early rockets |
| space_nasa | smithsonian | 12 | 0.0 | 0/12/0 | — | flow regulator liquid oxygen rocket engine r h godda; safety valve rocket engine liquid fuel r h goddard; rocket liquid fuel hoopskirt r h goddard |
| space_nasa | ia | 8 | 0.8 | 8/0/0 | — | moon landing hoax apollo 16 astronauts hooked themse; moon landing hoax apollo 16 astronauts hooked themse; earthrise the 45th anniversary scientific visualizat |
| stock_market_exchange | wikimedia | 452 | 4.7 | 0/452/0 | — | file 17 william england wall street new york jpg; file 1 wall street 001 jpg; file 1 wall street 002 jpg |
| textures_backgrounds | smithsonian | 575 | 1.6 | 0/575/0 | — | origami crane with bold designs; handmade basket with purple design and handle; rectangular shaped basket with woven purple design |
| textures_backgrounds | pixabay_extra | 461 | 15.2 | 461/0/0 | — | bokeh light background to dye red move waves drops a; star sparkles window twinkles christmas beautiful wa; glass sphere crystal ball bullet fortune tellers eso |
| textures_backgrounds | mixkit | 148 | 6.0 | 148/0/0 | — | exploding ink underwater; blurred pink circular lights; blurred multicolor lights bokeh |
| textures_backgrounds | unsplash | 50 | 0.3 | 0/50/0 | — | brown and gray concrete wall; crumpled blank paper texture; old creased blank paper texture |
| textures_backgrounds | met | 19 | 0.1 | 0/19/0 | — | textile with crowned double headed eagles; fragments of a textile with medici emblems; gold finger ring engraved with an image of hermes |
| textures_backgrounds | coverr | 2 | 0.0 | 2/0/0 | — | blurred christmas lights; hookah lights |
| textures_backgrounds | ia | 1 | 0.1 | 1/0/0 | — | industry on parade paperman s paper ink inc use and |
| uk_highstreet_postoffice | loc | 51 | 1.0 | 0/51/0 | — | the new england gazetteer comprising a concise descr; the queens of england abridged and adapted from stri; roster of all regimental surgeons and assistant surg |
| uk_period | loc | 72 | 0.4 | 0/72/0 | — | summer homes and rambles along the erie railway; california and alaska and over the canadian pacific ; history of british columbia |
| vintage_ads_cartoons | ia | 30 | 4.2 | 30/0/0 | — | 26 may 2014 nbn 3 newcastle commercial break 2; 26 may 2014 nbn 3 newcastle commercial break; animated floating clouds |
| war_history | nara | 1,131 | 30.9 | 178/953/0 | — | 1st cavalry division artillery fires a 105mm towed h; approved pension application file for matilda butz n; approved pension application file for matilda butz n |
| war_history | ia | 72 | 10.9 | 72/0/0 | — | home movie 010126 1940s world war ii navy film about; stanford documents of world war ii and red revolutio; u s faces war says roosevelt 1937 10 06 |
| war_history | loc | 2 | 0.2 | 0/2/0 | — | production m 4 tanks hull members of an m 4 tank on ; troops of the 185th inf 40th div take cover behind a |
| weather_disasters | nasa | 199 | 1.6 | 0/199/0 | — | a view of hurricane hilary from space; nasa sees smoke from californias long valley wildfir; satellites see major winter storm marching toward th |
| weather_disasters | ia | 13 | 1.5 | 13/0/0 | — | storm havoc hurricane kills 43 damage 15 millions 19; trauma talks hurricane safety; satellite time lapse goes e 2021 07 8k uhd hurricane |
| weather_disasters | noaa | 1 | 0.0 | 1/0/0 | — | clear skies reveal tornado scar in mississippi cira |
| wildlife_animals | pixabay_extra | 2,439 | 47.9 | 1019/1420/0 | — | bird nature animal wildlife plumage avian birdwatchi; beautiful beauty bird colorful nature marco peacock ; elephant animal wildlife mammal africa safari nature |
| wildlife_animals | noaa | 327 | 1.3 | 1/326/0 | — | 3008x2000 ribbon seal; adult false killer whale off guam photographed prior; adult male elephant seals battling |
| wildlife_animals | smithsonian | 99 | 0.1 | 0/99/0 | — | i bouquet holder butterfly motif i; butterfly pea clitoria mariana; butterfly violet viola papilionacea |
| wildlife_animals | mixkit | 76 | 1.3 | 76/0/0 | — | seagulls in nature; deer looking at the camera in the forest; deer family walking in the mountain |
| wildlife_animals | unsplash | 50 | 0.2 | 0/50/0 | — | a deer is standing in the tall grass; brown deer on forest during daytime; a couple deer in the woods |
| wildlife_animals | ia | 3 | 0.3 | 3/0/0 | — | our wildlife resources; king spruce hen puts on a show for the largest flock; king spruce hen puts on a show for the largest flock |
| wildlife_animals | met | 3 | 0.0 | 0/3/0 | — | tympanum with a horse and rider; study of a bird; horses harnessed to a chariot |
| world_cities | pixabay_extra | 1,336 | 20.8 | 573/763/0 | — | porto old town wet street cobblestone sunset backlig; warsaw night poland city europe travel architecture ; bangkok thailand floating market boats river travel |
| world_cities | mixkit | 128 | 5.3 | 128/0/0 | — | aerial view of city traffic at night; a man being followed walking in a city; city traffic on a bridge |
| world_cities | unsplash | 50 | 0.2 | 0/50/0 | — | black city bike parked beside white concrete wall; cityscape at night; a view of a city at night from the water |
| world_cities | nara | 27 | 0.1 | 0/27/0 | — | boulevards from city walls; second street north from market street showing chris; high street from the country marketplace with the pr |
| world_cities | coverr | 6 | 0.1 | 6/0/0 | — | a guy crosses a road in a city; street in mexico city; cars in the city at night |
| world_cities | ia | 4 | 0.4 | 4/0/0 | — | wonderful world; new york city scenics; big city 1958 2 |

## 2a. MOVING FOOTAGE by subject — 350 subjects with >= 3 clips

This is the scarce resource. Take stills only when no clip exists.

| subject | clips | top themes (clips only) | example clip |
|---|---:|---|---|
| nature | 1721 | wildlife_animals:390, landscapes_timelapse:373 | `ia__0033-day-at-the-river-a-film-lesson-in-nature-study-a-09-44__day-at-the-river-a-film-lesson-in-nature-study-a.mp4` |
| sea | 1083 | ocean_nature:706, landscapes_timelapse:93 | `ia__0991-hills-and-the-sea-01-19-57-20__hills-and-the-sea.mp4` |
| city | 1062 | world_cities:426, government_buildings:245 | `coverr__1246__a-guy-crosses-a-road-in-a-city.mp4` |
| water | 995 | ocean_nature:344, wildlife_animals:197 | `ia__water-friend-or-enemy__water-friend-or-enemy-disney-educational-film-2.mp4` |
| ocean | 972 | ocean_nature:772, landscapes_timelapse:48 | `coverr__2122__foamy-ocean-waves-at-night.mp4` |
| landscape | 855 | landscapes_timelapse:347, japan:154 | `mixkit__20148__shenzhen-city-landscape-and-skyscrapers.mp4` |
| road | 803 | small_town:355, police_modern:178 | `coverr__1246__a-guy-crosses-a-road-in-a-city.mp4` |
| wildlife | 727 | wildlife_animals:666, ocean_nature:17 | `ia__33-451-r-1-2__our-wildlife-resources.mp4` |
| beach | 592 | ocean_nature:372, landscapes_timelapse:58 | `coverr__6079__cliffs-on-praia-do-pinh-o-beach.mp4` |
| sky | 587 | landscapes_timelapse:257, ocean_nature:49 | `ia__timelapsesky__timelapse-sky.mp4` |
| sunset | 585 | landscapes_timelapse:290, ocean_nature:103 | `coverr__1213__timelapse-of-manhattan-at-sunset.mp4` |
| forest | 576 | wildlife_animals:185, landscapes_timelapse:88 | `mixkit__14620__man-walking-through-the-path-in-a-green-forest.mp4` |
| traffic | 563 | world_cities:219, police_modern:191 | `coverr__8472__midwest-traffic.mp4` |
| flag | 529 | government_buildings:475, small_town:19 | `mixkit__11026__philippine-flag-waving-in-the-sky.mp4` |
| aerial | 523 | landscapes_timelapse:230, ocean_nature:86 | `mixkit__31688__empty-street-in-berlin-aerial-shot.mp4` |
| architecture | 523 | government_buildings:309, world_cities:108 | `mixkit__3510__urban-architecture-of-a-tourist-street.mp4` |
| animal | 521 | wildlife_animals:349, ocean_nature:56 | `mixkit__22013__3d-printing-a-cartoon-animal.mp4` |
| drone | 519 | landscapes_timelapse:198, world_cities:70 | `mixkit__11937__drone-flying-past-a-cargo-ship.mp4` |
| clouds | 494 | landscapes_timelapse:337, small_town:21 | `ia__juusonturhavideodiary-clouds26htimelapse__juuson-turha-video-diary-clouds-26h-timelapse-2.mp4` |
| beautiful | 491 | government_buildings:173, textures_backgrounds:100 | `coverr__8352__beautiful-rocky-shoreline.mp4` |
| man | 490 | courtroom_justice:133, hands_and_transactions:65 | `coverr__4931__an-old-man-looking-out-of-the-window.mp4` |
| space | 473 | space_nasa:359, police_modern:21 | `ia__teenagers-from-outerspace__teenagers-from-outer-space-2.mp4` |
| background | 473 | textures_backgrounds:131, money_banking:64 | `mixkit__10435__hand-of-a-person-squeezing-an-orange-on-a-light-background.mp4` |
| bird | 464 | wildlife_animals:350, courtroom_justice:19 | `nasa__jsc2021m000152_Space_Station_Images_Trace_Bird_Migrations-MP__space-station-images-trace-bird-migrations.mp4` |
| night | 420 | world_cities:105, police_modern:94 | `coverr__5837__cars-in-the-city-at-night.mp4` |
| waves | 419 | ocean_nature:271, textures_backgrounds:51 | `coverr__2122__foamy-ocean-waves-at-night.mp4` |
| street | 418 | world_cities:190, small_town:50 | `coverr__3879__street-in-mexico-city.mp4` |
| wallpaper | 399 | government_buildings:148, textures_backgrounds:80 | `pixabay_extra__v_154833__woman-phone-business-casual-cheerful-beautiful-wallpaper-cus.mp4` |
| business | 397 | money_banking:136, business_corporate:89 | `mixkit__15716__men-in-black-shirts-shake-hands-at-business-meetng.mp4` |
| money | 381 | money_banking:373, hands_and_transactions:2 | `mixkit__14007__counting-euro-paper-money-on-the-table.mp4` |
| abstract | 379 | textures_backgrounds:186, money_banking:58 | `mixkit__30__blurred-abstract-cars-lights-at-night-with-bokeh-effect.mp4` |
| woman | 375 | hands_and_transactions:100, courtroom_justice:54 | `ia__the-second-woman-1950-202602__the-second-woman-1950-cc-film-noir-mystery-1-30-49.mp4` |
| walking | 374 | courtroom_justice:265, wildlife_animals:33 | `coverr__8360__walking-to-the-mountain-top.mp4` |
| building | 372 | government_buildings:155, world_cities:55 | `coverr__645__a-glass-building-on-lisbon-street.mp4` |
| car | 368 | police_modern:214, small_town:54 | `mixkit__24481__car-driving-away.mp4` |
| lights | 365 | textures_backgrounds:160, police_modern:100 | `coverr__284__blurred-christmas-lights.mp4` |
| technology | 359 | science_tech:240, police_modern:29 | `ia__0559-threads-of-technology__threads-of-technology.mp4` |
| urban | 358 | world_cities:160, government_buildings:71 | `mixkit__31089__shanghai-urban-city-scape-time-lapse.mp4` |
| trees | 355 | landscapes_timelapse:66, wildlife_animals:59 | `mixkit__30472__empty-avenue-surrounded-by-trees.mp4` |
| beautiful wallpaper | 351 | government_buildings:145, textures_backgrounds:76 | `pixabay_extra__v_154833__woman-phone-business-casual-cheerful-beautiful-wallpaper-cus.mp4` |
| green | 350 | economy_crisis:67, money_banking:59 | `mixkit__28384__golden-falling-bullets-with-green-background.mp4` |
| people | 346 | courtroom_justice:69, selling_floor:60 | `mixkit__15997__people-feet-walking.mp4` |
| underwater | 343 | ocean_nature:310, textures_backgrounds:28 | `mixkit__12715__underwater-shot-form-a-diver-of-penguins-swimming.mp4` |
| mountains | 338 | landscapes_timelapse:206, small_town:36 | `coverr__4021__timelapse-of-a-house-in-the-mountains.mp4` |
| coast | 336 | ocean_nature:220, landscapes_timelapse:18 | `mixkit__13000__aerial-view-of-high-cliffs-on-indonesian-coast-and-ocean-wav.mp4` |
| symbol | 323 | government_buildings:270, money_banking:17 | `pixabay_extra__v_109053__ukraine-flag-ukraine-flag-kiev-nation-symbol.mp4` |
| computer | 318 | science_tech:227, newspapers_printing:29 | `ia__univac-commercial-classic-old-vintage__classic-tv-commercial-for-a-univac-computer.mp4` |
| country | 312 | government_buildings:247, small_town:28 | `mixkit__19157__indonesia-flag-asian-country.mp4` |
| cars | 308 | police_modern:99, world_cities:87 | `mixkit__28092__cars-driving-through-rainfall.mp4` |
| river | 303 | landscapes_timelapse:56, world_cities:40 | `mixkit__15919__aerial-view-of-lush-river-valley-and-snowy-mountains.mp4` |
| buildings | 294 | government_buildings:133, world_cities:105 | `mixkit__2028__city-buildings-lit-up-at-night.mp4` |
| highway | 289 | small_town:166, police_modern:41 | `mixkit__49147__trailer-crash-on-a-highway.mp4` |
| travel | 282 | small_town:55, world_cities:45 | `mixkit__27691__travel-stamps-in-a-passport.mp4` |
| mountain | 279 | landscapes_timelapse:128, japan:41 | `mixkit__28844__sunset-over-a-snowy-winter-mountain.mp4` |
| screen | 276 | economy_crisis:71, money_banking:64 | `ia__0723-america-marching-on-a-screen-editorial-with-lowell-thom__america-marching-on-a-screen-editorial-with-lowell-thomas.mp4` |
| japan | 261 | japan:239, landscapes_timelapse:5 | `ia__0043-children-of-japan-19-20-39-00__children-of-japan.mp4` |
| light | 260 | textures_backgrounds:55, police_modern:45 | `coverr__7318__traffic-light-timer.mp4` |
| wave | 259 | ocean_nature:211, money_banking:12 | `ia__ocean-wave__ocean-wave.mp4` |
| running | 248 | newspapers_printing:229, wildlife_animals:6 | `mixkit__11187__guy-running-at-the-beach-during-sunset.mp4` |
| sea ocean | 243 | ocean_nature:184, landscapes_timelapse:22 | `pixabay_extra__v_102706__people-shore-sea-ocean-water-waves-beach-walk-walking-holida.mp4` |
| sun | 242 | landscapes_timelapse:108, ocean_nature:29 | `mixkit__4113__sun-rays-pass-through-the-clouds-in-the-mountains.mp4` |
| office | 237 | business_corporate:72, science_tech:48 | `mixkit__914__open-office-space.mp4` |
| plumage | 237 | wildlife_animals:201, courtroom_justice:12 | `pixabay_extra__v_63338__swan-bird-plumage-elegant-nature-pen-aquatic-majestic-the-wa.mp4` |
| blue | 226 | ocean_nature:67, textures_backgrounds:29 | `mixkit__14776__scissors-cutting-a-blue-fabric.mp4` |
| vehicle | 221 | police_modern:168, world_cities:19 | `mixkit__10160__vehicle-driving-through-the-rocky-mountain-road.mp4` |
| sunrise | 219 | landscapes_timelapse:93, courtroom_justice:27 | `coverr__9808__sunrise-at-the-beach-dock.mp4` |
| wild | 219 | wildlife_animals:171, courtroom_justice:8 | `mixkit__11018__african-elephant-walking-in-the-wild.mp4` |
| ground | 217 | space_nasa:206, science_tech:2 | `nasa__jcs2022m000004_Space_to_Ground_404_220114__space-to-ground-spacewalks-and-research-01-14-2022.mp4` |
| bokeh | 217 | textures_backgrounds:178, world_cities:11 | `mixkit__1177__blurred-multicolor-lights-bokeh.mp4` |
| finance | 215 | money_banking:204, business_corporate:4 | `pixabay_extra__v_102779__money-online-earn-business-cartoon-fund-finance-paid-profit.mp4` |
| smoke | 213 | textures_backgrounds:190, money_banking:8 | `mixkit__12495__smoke-with-fluorescent-particles-on-black-background.mp4` |
| fish | 213 | ocean_nature:185, wildlife_animals:8 | `mixkit__44868__beautiful-coral-reef-with-exotic-reef-fish.mp4` |
| design | 212 | prison_jail:56, government_buildings:40 | `pixabay_extra__v_138422__design-marketing-business.mp4` |
| ocean sea | 212 | ocean_nature:160, wildlife_animals:15 | `pixabay_extra__v_146632__couple-beach-ocean-sea-walking-calm-travel-honeymoon-love-to.mp4` |
| winter | 208 | landscapes_timelapse:29, wildlife_animals:25 | `ia__timelapseofanorangesunsetinwinter__timelapse-of-an-orange-sunset-in-winter.mp4` |
| motion | 207 | prison_jail:45, money_banking:31 | `ia__rpmusicinmotion__music-in-motion.mp4` |
| space ground | 204 | space_nasa:204 | `nasa__jcs2022m000004_Space_to_Ground_404_220114__space-to-ground-spacewalks-and-research-01-14-2022.mp4` |
| time | 201 | landscapes_timelapse:74, money_banking:28 | `ia__timelapse-teste1__blender-sunset-time-lapse-test1.mp4` |
| nature landscape | 199 | landscapes_timelapse:98, wildlife_animals:25 | `pixabay_extra__v_98384__nature-landscape-pine-tree-night-forest-tree-lights-twinkle.mp4` |
| currency | 195 | money_banking:194, household_loss:1 | `pixabay_extra__v_103707__bitcoin-crypto-cryptocurrency-blockchain-currency-money-cash.mp4` |
| snow | 192 | landscapes_timelapse:31, wildlife_animals:29 | `mixkit__13916__heart-shape-in-the-snow-mountains-at-sunset.mp4` |
| ink | 189 | textures_backgrounds:162, police_modern:12 | `ia__papermans-paper__industry-on-parade-paperman-s-paper-ink-inc-use-and-discard.mp4` |
| rain | 186 | household_loss:40, prison_jail:23 | `mixkit__28085__heavy-rain-from-an-open-window.mp4` |
| reef | 186 | ocean_nature:185, wildlife_animals:1 | `mixkit__11179__snorkeling-at-the-coral-reef.mp4` |
| green screen | 185 | economy_crisis:53, money_banking:44 | `mixkit__48285__laptop-with-a-green-screen-slide-in.mp4` |
| netherlands | 183 | police_modern:63, small_town:42 | `nara__77741-219251798__princess-juliana-of-the-netherlands-christens-ss-jan-pieters.mp4` |
| house | 182 | economy_crisis:47, government_buildings:19 | `mixkit__2632__abandoned-house-in-a-forest.mp4` |
| science | 182 | science_tech:117, space_nasa:30 | `nasa__321_SS101-PlantGrowth-03__nasa-sciencecasts-station-science-101-advancing-plant-scienc.mp4` |
| launch | 181 | space_nasa:178, newspapers_printing:2 | `nasa__1511201_JWST_L-D_Apvd_Final__webb-telescope-launch-and-deploy-12-minute.mp4` |
| hands | 178 | hands_and_transactions:61, courtroom_justice:42 | `ia__0555-master-hands-18-27-28-00__master-hands.mp4` |
| lake | 177 | wildlife_animals:58, japan:31 | `mixkit__11100__eagle-eats-a-fish-in-the-lake.mp4` |
| coral | 175 | ocean_nature:174, wildlife_animals:1 | `ia__0436-coral-wonderland-01-00-02-00__coral-wonderland.mp4` |
| state | 174 | government_buildings:163, small_town:8 | `pixabay_extra__v_110268__ukraine-flag-symbol-sky-city-country-state-symbols-symbol-of.mp4` |
| wind | 173 | government_buildings:51, japan:21 | `mixkit__13129__international-flags-waving-in-the-wind.mp4` |
| bridge | 166 | world_cities:39, government_buildings:35 | `mixkit__13__city-traffic-on-a-bridge.mp4` |
| tree | 166 | wildlife_animals:31, landscapes_timelapse:22 | `mixkit__34016__dry-tree-leaves-falling-into-the-water-from-a-pond.mp4` |
| animals | 166 | wildlife_animals:84, ocean_nature:43 | `mixkit__11239__herds-of-african-animals-on-a-vast-plain.mp4` |
| deer | 166 | wildlife_animals:162, newspapers_printing:2 | `mixkit__10076__deer-looking-at-the-camera-in-the-forest.mp4` |
| cartoon | 166 | government_buildings:44, newspapers_printing:20 | `ia__bosko5491soundcartoon1932hughharmanrudolfisingc__bosko-5491-sound-cartoon-1932-hugh-harman-rudolf-ising-2.mp4` |
| cash | 166 | money_banking:164, market_machinery:1 | `mixkit__23725__female-hands-counting-cash.mp4` |
| temple | 163 | japan:161, courtroom_justice:1 | `mixkit__11072__ancient-temple-time-lapse.mp4` |
| robot | 161 | science_tech:152, police_modern:5 | `mixkit__20961__robot-with-moving-eyes.mp4` |
| black | 158 | textures_backgrounds:37, wildlife_animals:22 | `ia__black-angel-1946-202406__black-angel-1946-12-cc-crime-film-noir-1-20-33-dan-duryea-ju.mp4` |
| coffee | 158 | hands_and_transactions:92, business_corporate:16 | `mixkit__1323__couple-drinking-coffee-close-up.mp4` |
| young | 156 | hands_and_transactions:37, courtroom_justice:25 | `mixkit__50814__a-young-man-streaching-his-arms-against-the-blue-sky.mp4` |
| work | 154 | science_tech:44, business_corporate:26 | `mixkit__4809__business-people-at-work-meeting.mp4` |
| summer | 152 | ocean_nature:44, landscapes_timelapse:34 | `mixkit__7879__man-running-during-summer.mp4` |
| autumn | 152 | japan:29, small_town:26 | `mixkit__25043__flying-over-an-autumn-forest-and-a-empty-road.mp4` |
| white | 151 | wildlife_animals:48, textures_backgrounds:18 | `mixkit__1187__white-flowers-in-the-breeze.mp4` |
| old | 150 | courtroom_justice:33, government_buildings:24 | `mixkit__12533__old-man-walking-through-green-fields.mp4` |
| red | 150 | wildlife_animals:27, textures_backgrounds:18 | `ia__the-red-house__the-red-house-full-film-4k-a-haunting-1940s-thriller-with-ed.mp4` |
| drone aerial | 147 | landscapes_timelapse:124, ocean_nature:7 | `pixabay_extra__v_110594__waterfall-cliff-jungle-drone-aerial-view-nature-sunrise-pano.mp4` |
| ship | 145 | goods_in_motion:99, ocean_nature:17 | `mixkit__11935__cargo-ship-under-the-sun.mp4` |
| close | 143 | wildlife_animals:29, hands_and_transactions:21 | `coverr__3270__close-up-of-barista-taking-money-from-a-customer.mp4` |
| fog | 143 | landscapes_timelapse:53, courtroom_justice:24 | `mixkit__4396__fog-on-the-heights-of-the-snowy-mountains.mp4` |
| sky clouds | 143 | landscapes_timelapse:124, small_town:5 | `pixabay_extra__v_107211__nature-landscape-cross-sky-clouds-light-effects-mountain-sum.mp4` |
| transport | 142 | police_modern:47, small_town:34 | `mixkit__2741__orange-heavy-cargo-transport-moving-on-the-road.mp4` |
| empty | 140 | courtroom_justice:121, household_loss:7 | `mixkit__1930__waves-at-an-empty-beach.mp4` |
| driving | 139 | police_modern:86, small_town:25 | `mixkit__21084__driving-through-a-long-tunnel.mp4` |
| construction | 136 | government_buildings:83, goods_in_motion:27 | `mixkit__4010__buildings-under-construction-aerial-view.mp4` |
| opening | 135 | money_banking:74, hands_and_transactions:46 | `mixkit__11518__opening-her-eyes-and-smiling.mp4` |
| harbor | 135 | navy_harbor:120, goods_in_motion:9 | `nara__75302-14908202__uss-argonaut-returns-to-pearl-harbor-with-usmc-raiders-from.mp4` |
| small | 134 | small_town:83, hands_and_transactions:38 | `mixkit__1520__stalk-of-small-bananas-over-a-wooden-base.mp4` |
| rocks | 134 | ocean_nature:72, newspapers_printing:16 | `mixkit__9294__sea-waves-breaking-on-the-rocks-front-view.mp4` |
| skyline | 134 | world_cities:103, government_buildings:13 | `mixkit__26872__downtown-los-angeles-skyline-in-california.mp4` |
| room | 132 | prison_jail:33, police_modern:27 | `mixkit__23040__a-woman-working-with-a-computer-in-the-server-room.mp4` |
| birds | 132 | wildlife_animals:82, prison_jail:9 | `mixkit__11120__a-flock-of-cockatoo-birds-flying-away.mp4` |
| lapse | 131 | landscapes_timelapse:61, world_cities:26 | `ia__timelapse-teste1__blender-sunset-time-lapse-test1.mp4` |
| park | 130 | courtroom_justice:28, world_cities:24 | `mixkit__17901__park-and-a-bench-with-fallen-leaves.mp4` |
| futuristic | 130 | science_tech:79, police_modern:17 | `mixkit__9082__woman-opens-video-call-on-futuristic-hologram-panel-in-bed.mp4` |
| time lapse | 130 | landscapes_timelapse:61, world_cities:25 | `ia__timelapse-teste1__blender-sunset-time-lapse-test1.mp4` |
| mammal | 130 | wildlife_animals:113, courtroom_justice:4 | `pixabay_extra__v_110527__peccary-boar-pig-collared-animal-zoo-wildlife-hog-mammal-wal.mp4` |
| hand | 129 | hands_and_transactions:56, household_loss:19 | `mixkit__12524__top-view-of-a-tailor-s-hand-sewing-a-shirt.mp4` |
| shopping | 128 | economy_crisis:41, selling_floor:35 | `mixkit__31086__busy-shopping-mall-time-lapse.mp4` |
| symbol state | 127 | government_buildings:123, small_town:4 | `pixabay_extra__v_130269__flag-finland-country-beautiful-wallpaper-symbol-state-backgr.mp4` |
| nation | 126 | government_buildings:114, small_town:7 | `pixabay_extra__v_109053__ukraine-flag-ukraine-flag-kiev-nation-symbol.mp4` |
| morning | 125 | courtroom_justice:27, landscapes_timelapse:16 | `ia__what-happened-to-saturday-morning-cartoons__what-happened-to-saturday-morning-cartoons-2.mp4` |
| loop | 124 | money_banking:49, science_tech:28 | `mixkit__31534__futuristic-virtual-city-highway-loop-video.mp4` |
| table | 124 | business_corporate:27, science_tech:26 | `mixkit__23222__signing-on-a-contract-on-a-wooden-table.mp4` |
| desk | 124 | hands_and_transactions:35, science_tech:28 | `mixkit__13339__creative-girl-sketches-on-desk-in-art-studio.mp4` |
| cityscape | 123 | world_cities:59, government_buildings:41 | `mixkit__31005__beach-in-dubai-with-cityscape-in-the-background.mp4` |
| window | 122 | household_loss:67, prison_jail:27 | `coverr__4931__an-old-man-looking-out-of-the-window.mp4` |
| dark | 122 | textures_backgrounds:38, courtroom_justice:11 | `ia__the-dark-corner-1946-202405__the-dark-corner-1946-cc-crime-film-noir-1-35-11-lucille-ball.mp4` |
| town | 122 | world_cities:35, small_town:24 | `mixkit__29336__clouds-above-a-town-skyline.mp4` |
| person | 121 | prison_jail:29, hands_and_transactions:23 | `mixkit__10435__hand-of-a-person-squeezing-an-orange-on-a-light-background.mp4` |
| coastline | 119 | ocean_nature:113, japan:2 | `coverr__1523__the-praia-do-pinh-o-coastline.mp4` |
| colombia | 118 | prison_jail:67, courtroom_justice:6 | `mixkit__18090__colombia-flag-render.mp4` |
| water bird | 118 | wildlife_animals:113, government_buildings:2 | `pixabay_extra__v_102630__goose-greylag-goose-winter-snow-water-bird-cold-plumage-bird.mp4` |
| aquarium | 116 | ocean_nature:106, textures_backgrounds:5 | `pixabay_extra__v_100438__aquarium-fishes-water-underwater-bullet-glass-sphere-fishbow.mp4` |
| bank | 115 | money_banking:109, courtroom_justice:3 | `mixkit__24584__counting-bank-notes.mp4` |
| evening | 114 | landscapes_timelapse:36, police_modern:24 | `mixkit__15858__lawyers-talk-with-client-in-late-evening-office.mp4` |
| girl | 114 | courtroom_justice:26, hands_and_transactions:20 | `mixkit__18240__little-girl-walking-in-the-valley-at-sunset.mp4` |
| sport | 114 | newspapers_printing:45, government_buildings:29 | `pixabay_extra__v_12609__basketball-ball-sport-basket-court-game-competition-play-act.mp4` |
| invasion | 113 | war_history:107, navy_harbor:6 | `ia__npc-4912__invasion-of-france-german-newsreel.mp4` |
| transportation | 113 | police_modern:45, small_town:30 | `pixabay_extra__v_125556__train-rails-time-transportation-train-passing-locomotive-spe.mp4` |
| yard | 112 | prison_jail:94, economy_crisis:7 | `nara__76128-14909731__activities-in-landing-craft-maintenance-repair-yard-salcombe.mp4` |
| home | 111 | prison_jail:18, money_banking:13 | `ia__000416-202005__home-movie-000416-1951-detroit-area-family.mp4` |
| flowers | 111 | japan:27, landscapes_timelapse:17 | `mixkit__1187__white-flowers-in-the-breeze.mp4` |
| train | 110 | japan:39, goods_in_motion:18 | `mixkit__20066__tokyo-train-station-traffic.mp4` |
| station | 110 | space_nasa:74, japan:8 | `nasa__15_Benefits_of_Space_Station_Research__15-benefits-of-space-station-research.mp4` |
| flying | 109 | police_modern:27, wildlife_animals:18 | `ia__the-flying-ace-part-1__the-flying-ace-part-1-1920-all-black-cast-silent-film-1-05-5.mp4` |
| sand | 108 | ocean_nature:51, courtroom_justice:11 | `mixkit__26017__friday-written-in-sand.mp4` |
| cliff | 108 | ocean_nature:87, landscapes_timelapse:8 | `mixkit__51454__aerial-view-of-waves-hitting-a-small-cliff-in-the-sea.mp4` |
| camera | 108 | police_modern:69, ocean_nature:9 | `mixkit__49603__a-woman-in-a-pink-suit-points-a-firearm-to-the-camera.mp4` |
| shop | 106 | hands_and_transactions:32, selling_floor:31 | `mixkit__13878__delicious-desserts-in-the-counter-shop.mp4` |
| europe | 106 | government_buildings:48, world_cities:28 | `pixabay_extra__v_122869__flag-eu-europe-union-europe.mp4` |
| market | 105 | selling_floor:41, money_banking:39 | `coverr__3150__queue-to-carrefour-market-in-paris.mp4` |
| field | 105 | small_town:20, landscapes_timelapse:16 | `mixkit__23320__soldiers-walking-through-the-field.mp4` |
| laptop | 105 | science_tech:32, newspapers_printing:20 | `mixkit__12964__worried-man-on-phone-call-stares-at-laptop.mp4` |
| dollar | 105 | money_banking:99, hands_and_transactions:4 | `mixkit__18259__detailed-shot-of-pictures-for-a-dollar-bill.mp4` |
| shore | 104 | ocean_nature:82, wildlife_animals:4 | `coverr__3079__the-incoming-waves-of-the-ocean-gently-splash-onto-the-shore.mp4` |
| africa | 104 | government_buildings:64, wildlife_animals:19 | `pixabay_extra__v_133538__ceuta-spanish-africa-north-africa-flag-symbol-state-beautifu.mp4` |
| christmas | 103 | textures_backgrounds:29, police_modern:16 | `coverr__284__blurred-christmas-lights.mp4` |
| door | 103 | economy_crisis:36, money_banking:24 | `mixkit__35896__man-tries-to-open-a-padlocked-wooden-door.mp4` |
| texture | 102 | textures_backgrounds:72, money_banking:6 | `mixkit__1205__blue-ink-texture-underwater-with-a-mirror.mp4` |
| sign | 102 | household_loss:22, government_buildings:18 | `mixkit__31698__flying-towards-the-hollywood-sign-in-california.mp4` |
| fire | 101 | textures_backgrounds:31, money_banking:11 | `mixkit__32360__fire-in-the-woods-with-a-lot-of-smoke.mp4` |
| lion | 101 | wildlife_animals:96, world_cities:2 | `mixkit__11035__male-lion-walking-in-the-savanna.mp4` |
| flow | 100 | textures_backgrounds:46, landscapes_timelapse:9 | `mixkit__44791__abstract-flow-of-a-drop-of-pink-ink-in-a-thick-liquid.mp4` |
| cute | 100 | wildlife_animals:53, small_town:18 | `mixkit__25003__cute-little-empty-town.mp4` |
| speed | 99 | police_modern:40, newspapers_printing:16 | `mixkit__17613__car-speed-dashboard.mp4` |
| grass | 99 | wildlife_animals:27, landscapes_timelapse:12 | `mixkit__11053__male-lions-resting-on-the-grass.mp4` |
| contemporary | 99 | government_buildings:53, science_tech:26 | `pixabay_extra__v_141186__architecture-construction-kiev-structure-contemporary-design.mp4` |
| tropical | 98 | ocean_nature:89, landscapes_timelapse:2 | `mixkit__44870__tropical-sea-life-swimming-gently-along-a-coral-reef-bank.mp4` |
| network | 98 | science_tech:83, police_modern:6 | `mixkit__14142__video-with-digital-trade-network-concept.mp4` |
| nasa | 98 | space_nasa:97, newspapers_printing:1 | `nasa__297_ISS-Cement__nasa-sciencecasts-cementing-our-place-in-space.mp4` |
| predator | 97 | wildlife_animals:83, world_cities:6 | `pixabay_extra__v_258584__spotted-hyena-animal-mammal-nature-wild-wildlife-predator-wa.mp4` |
| animal wildlife | 97 | wildlife_animals:91, newspapers_printing:2 | `pixabay_extra__v_120283__zebra-striped-animal-wildlife.mp4` |
| japanese | 96 | japan:52, navy_harbor:20 | `ia__misc-1057__geography-of-the-japanese-empire-1945.mp4` |
| pattern | 95 | textures_backgrounds:59, science_tech:7 | `pixabay_extra__v_17446__abstract-fractal-psychedelic-fractals-pattern-digital-projec.mp4` |
| leaves | 94 | money_banking:20, courtroom_justice:14 | `mixkit__17901__park-and-a-bench-with-fallen-leaves.mp4` |
| holiday | 94 | ocean_nature:56, textures_backgrounds:8 | `mixkit__13208__gold-holiday-ornaments-and-champagne-glasses-on-green-bokeh.mp4` |
| food | 93 | selling_floor:25, textures_backgrounds:14 | `mixkit__48931__cat-eating-dry-cat-food-in-its-plate.mp4` |
| tourism | 93 | government_buildings:21, ocean_nature:17 | `ia__000541-202005__home-movie-000541-1940s-tourism-to-mountain-provinces-catche.mp4` |
| abandoned | 92 | economy_crisis:45, courtroom_justice:30 | `mixkit__17408__flying-through-an-abandoned-place.mp4` |
| coins | 92 | money_banking:59, hands_and_transactions:32 | `mixkit__13259__hands-full-of-coins.mp4` |
| flower | 92 | landscapes_timelapse:17, prison_jail:14 | `mixkit__43178__fashion-model-with-sunglasses-and-a-flower.mp4` |
| slow | 91 | wildlife_animals:49, government_buildings:7 | `mixkit__32532__sewing-machine-in-slow-motion.mp4` |
| trees forest | 91 | landscapes_timelapse:28, small_town:23 | `pixabay_extra__v_203665__man-walking-trees-forest-sunrise-netherlands-drenthe-nationa.mp4` |
| flock | 91 | wildlife_animals:83, courtroom_justice:6 | `ia__kingsprucehenputsonashowforthelargestflockweeversaw__king-spruce-hen-puts-on-a-show-for-the-largest-flock-we-ever-2.mp4` |
| drenthe | 91 | police_modern:32, small_town:27 | `pixabay_extra__v_178715__man-walking-hiking-forest-netherlands-drenthe-sunset-afterno.mp4` |
| working | 90 | science_tech:27, hands_and_transactions:25 | `coverr__4862__a-businessman-working-on-a-stock-market-trading-platform.mp4` |
| rock | 90 | ocean_nature:40, landscapes_timelapse:12 | `ia__pacific-ocean-waves-crashing-against-rock-formation__pacific-ocean-waves-crashing-against-rock-formation.mp4` |
| moon | 90 | space_nasa:29, police_modern:10 | `ia__moonlandinghoaxapollo16astronautshookedthemselvesupinsidethe__moon-landing-hoax-apollo-16-astronauts-hooked-themselves-up-2.mp4` |
| artemis | 90 | space_nasa:89, japan:1 | `nasa__Around_the_Moon_for_All_Humanity_Artemis_II_Official_Launch___around-the-moon-for-all-humanity-artemis-ii-official-launch.mp4` |
| art | 89 | textures_backgrounds:34, japan:8 | `mixkit__13339__creative-girl-sketches-on-desk-in-art-studio.mp4` |
| marine | 89 | ocean_nature:74, goods_in_motion:7 | `nara__76047-14908572__marine-landing-operations-invasion-of-eniwetok-is-marshall-i.mp4` |
| particles | 89 | textures_backgrounds:64, science_tech:9 | `mixkit__12494__light-particles-reflected-in-a-traffic-bokeh.mp4` |
| internet | 88 | science_tech:64, business_corporate:9 | `mixkit__13189__closeup-of-surfing-internet-reflected-in-glasses.mp4` |
| rural | 87 | small_town:41, japan:27 | `mixkit__26563__rural-roads-between-farm-buildings.mp4` |
| structure | 87 | government_buildings:64, courtroom_justice:7 | `pixabay_extra__v_34317__hong-kong-sunset-sky-structure-office-city-skyscrapers-dawn.mp4` |
| state country | 87 | government_buildings:84, small_town:3 | `pixabay_extra__v_131017__greece-flag-state-country-patriotism-beautiful-wallpaper-bac.mp4` |
| island | 86 | ocean_nature:40, landscapes_timelapse:11 | `mixkit__34004__small-island-paradise-made-in-3d-on-a-sunny-day.mp4` |
| book | 86 | courtroom_justice:62, hands_and_transactions:6 | `mixkit__14791__man-looking-for-a-book-in-the-library.mp4` |
| ocean waves | 85 | ocean_nature:73, landscapes_timelapse:6 | `coverr__2122__foamy-ocean-waves-at-night.mp4` |
| off | 85 | newspapers_printing:64, war_history:7 | `mixkit__20932__taking-off-a-bolt.mp4` |
| timelapse | 84 | landscapes_timelapse:58, world_cities:19 | `coverr__1213__timelapse-of-manhattan-at-sunset.mp4` |
| cloud | 84 | landscapes_timelapse:39, textures_backgrounds:13 | `mixkit__48482__aerial-footage-of-cloud-topped-mountains-at-sunset.mp4` |
| walk | 83 | courtroom_justice:40, household_loss:10 | `pixabay_extra__v_1010__hiker-nature-lake-calm-walking-hiking-walk-mountains-alone-t.mp4` |
| italy | 83 | government_buildings:28, world_cities:17 | `ia__adc-1780__newsreel-fire-power-u-s-guns-open-upon-nazis-in-italy.mp4` |
| phone | 82 | business_corporate:47, hands_and_transactions:6 | `mixkit__12964__worried-man-on-phone-call-stares-at-laptop.mp4` |
| coral reef | 81 | ocean_nature:81 | `mixkit__11179__snorkeling-at-the-coral-reef.mp4` |
| colorful | 81 | textures_backgrounds:21, ocean_nature:10 | `mixkit__42002__shooting-colorful-underwater-inks.mp4` |
| police | 80 | police_modern:75, courtroom_justice:2 | `mixkit__14004__police-lights-in-a-dark-background.mp4` |
| boat | 80 | goods_in_motion:35, ocean_nature:11 | `mixkit__11939__harbour-pilot-boat-following-a-cargo-ship.mp4` |
| sea beach | 80 | ocean_nature:60, landscapes_timelapse:10 | `pixabay_extra__v_189214__sea-beach-woman-walking-ice-winter-iceland-nature.mp4` |
| fence | 80 | prison_jail:74, textures_backgrounds:3 | `mixkit__17536__hand-on-a-wire-fence-by-night.mp4` |
| typing | 79 | newspapers_printing:46, science_tech:14 | `mixkit__4837__young-man-on-the-street-typing-on-his-cell-phone.mp4` |
| sea waves | 79 | ocean_nature:66, courtroom_justice:3 | `mixkit__1087__aerial-shot-of-a-beach-with-sea-waves.mp4` |
| path | 78 | courtroom_justice:23, small_town:21 | `mixkit__14697__woman-walking-on-a-wooden-path-in-the-swamp.mp4` |
| asia | 78 | japan:26, world_cities:15 | `ia__npc-10127__the-great-asia-war-01-1942.mp4` |
| national | 78 | government_buildings:65, small_town:5 | `pixabay_extra__v_117755__flag-indian-flag-india-indian-national-flag-shiva-flying-tri.mp4` |
| rocket | 78 | space_nasa:66, war_history:8 | `ia__trailoft1951-2__trail-of-the-rocket-part-ii-2.mp4` |
| trip | 78 | ocean_nature:33, police_modern:10 | `ia__000437-202005__home-movie-000437-1940s-western-train-trip.mp4` |
| abstract background | 77 | prison_jail:44, textures_backgrounds:25 | `pixabay_extra__v_270877__abstract-background-calming-geometric-design-graphic-motion.mp4` |
| cloudscape | 77 | landscapes_timelapse:75, government_buildings:1 | `pixabay_extra__v_17243__sunset-pink-yellow-clouds-cloudscape-trees-nature-landscape.mp4` |
| calm | 76 | ocean_nature:40, courtroom_justice:8 | `coverr__4513__calm-waves-in-an-ocean-gulf.mp4` |
| future | 76 | science_tech:50, space_nasa:7 | `nasa__jcs2023m000010_Space_to_Ground_460_230217__space-to-ground-a-grip-on-the-future-feb-17-2023.mp4` |
| card | 76 | money_banking:40, police_modern:18 | `mixkit__21780__using-a-card-machine-at-the-counter.mp4` |
| insect | 75 | prison_jail:43, wildlife_animals:14 | `pixabay_extra__v_160123__ants-trunk-insect-walking-nature-environment.mp4` |
| earth | 75 | space_nasa:32, small_town:14 | `nasa__308_ISS-EyeOnEarth__nasa-sciencecasts-keeping-an-eye-on-earth.mp4` |
| graphic | 75 | prison_jail:46, science_tech:6 | `mixkit__47016__close-up-of-a-stock-market-graphic.mp4` |
| flight | 75 | wildlife_animals:23, police_modern:9 | `mixkit__22598__passenger-waiting-for-a-flight.mp4` |
| city urban | 75 | world_cities:28, government_buildings:20 | `pixabay_extra__v_299548__city-urban-center-avenue-traffic-buildings-shops-the-busines.mp4` |
| through | 74 | courtroom_justice:12, police_modern:6 | `mixkit__12533__old-man-walking-through-green-fields.mp4` |
| falling | 74 | money_banking:30, economy_crisis:12 | `mixkit__28125__snow-falling-in-an-empty-woodland.mp4` |
| alone | 74 | courtroom_justice:59, japan:3 | `pixabay_extra__v_100583__papers-wind-alone-pen-beautyshot-beaty-shot-home-interior-so.mp4` |
| automobile | 74 | police_modern:57, world_cities:6 | `pixabay_extra__v_111956__harley-davidson-motorcycle-biker-rider-automobile-car-self-v.mp4` |
| sunlight | 74 | landscapes_timelapse:19, ocean_nature:17 | `mixkit__46762__silhouette-of-a-hand-being-held-up-in-front-of-the-sunlight.mp4` |
| bird plumage | 74 | wildlife_animals:65, courtroom_justice:5 | `pixabay_extra__v_63338__swan-bird-plumage-elegant-nature-pen-aquatic-majestic-the-wa.mp4` |
| tokyo | 73 | japan:61, world_cities:6 | `ia__kamikazeceremony__kamikaze-ceremony-pd-tokyo-way-of-life-tokyo-1945.mp4` |
| outdoors | 73 | wildlife_animals:17, landscapes_timelapse:10 | `mixkit__46359__lovely-couple-enjoying-walking-outdoors.mp4` |
| modern | 73 | government_buildings:18, science_tech:10 | `ia__the-capture-1950-202604__the-capture-1950-cc-drama-modern-western-01-30-18.mp4` |
| liquid | 73 | textures_backgrounds:39, science_tech:6 | `mixkit__44791__abstract-flow-of-a-drop-of-pink-ink-in-a-thick-liquid.mp4` |
| kiev | 73 | government_buildings:63, world_cities:6 | `pixabay_extra__v_109053__ukraine-flag-ukraine-flag-kiev-nation-symbol.mp4` |
| store | 72 | hands_and_transactions:32, selling_floor:13 | `mixkit__12531__grandmother-shopping-in-a-clothing-store.mp4` |
| natural | 72 | japan:42, landscapes_timelapse:8 | `mixkit__50201__natural-landscape-with-a-lake-in-an-aerial-view.mp4` |
| live | 72 | space_nasa:45, police_modern:8 | `nasa__KSC-20200209-VP-CDC01-0001-Solar_Orbiter_Live_Launch_Coverag__solar-orbiter-live-launch-coverage-launch-isos.mp4` |
| waterfall | 72 | landscapes_timelapse:22, japan:20 | `mixkit__30502__waterfall-of-a-river-in-winter-falling-into-a-canyon.mp4` |
| bombardment | 72 | war_history:71, navy_harbor:1 | `nara__75421-183895408__bombardment-by-missouri-unloading-oprns-of-bataan.mp4` |
| communication | 72 | science_tech:33, government_buildings:12 | `pixabay_extra__v_116453__cloud-3d-cartoon-smartphone-phone-communication-data-technol.mp4` |
| aerial drone | 71 | landscapes_timelapse:31, world_cities:17 | `pixabay_extra__v_134555__mountains-forest-nature-aerial-drone.mp4` |
| netherlands drenthe | 71 | police_modern:28, small_town:16 | `pixabay_extra__v_178715__man-walking-hiking-forest-netherlands-drenthe-sunset-afterno.mp4` |
| fall | 70 | money_banking:13, courtroom_justice:10 | `mixkit__18262__surface-while-100-dollar-bills-fall-messily.mp4` |
| road traffic | 70 | police_modern:28, world_cities:26 | `pixabay_extra__v_113420__vehicles-road-traffic-bus-vehicle-transport-asia-thailand-ba.mp4` |
| noir | 70 | pd_feature_films:69, police_modern:1 | `ia__a-life-at-stake-1955-202512__a-life-at-stake-1955-film-noir-drama-1-15-52-angela-lansbury.mp4` |
| space station | 70 | space_nasa:67, weather_disasters:2 | `nasa__15_Benefits_of_Space_Station_Research__15-benefits-of-space-station-research.mp4` |
| books | 70 | courtroom_justice:66, science_tech:2 | `mixkit__12277__shelves-full-of-books-3d-animation.mp4` |
| tower | 69 | government_buildings:31, japan:13 | `mixkit__21598__detailed-view-of-a-disarranged-tower-of-books.mp4` |
| data | 69 | science_tech:36, business_corporate:17 | `mixkit__21053__colorful-data-scrolling.mp4` |
| stream | 68 | newspapers_printing:26, wildlife_animals:14 | `mixkit__26989__small-stream-in-a-forest-in-spring-slow-motion.mp4` |
| cold | 68 | household_loss:25, prison_jail:9 | `mixkit__42510__guy-puts-his-shirt-on-his-girlfriend-when-it-s-cold.mp4` |
| plant | 68 | prison_jail:13, landscapes_timelapse:9 | `mixkit__23493__electrical-workers-in-power-plant.mp4` |
| animation | 68 | money_banking:15, selling_floor:8 | `mixkit__5404__marketing-infographic-data-charts-animation.mp4` |
| blur | 68 | textures_backgrounds:30, police_modern:12 | `pixabay_extra__v_201__people-crow-blur-bokeh-out-of-focus-men-women-walking-statio.mp4` |
| glass | 67 | business_corporate:23, household_loss:13 | `coverr__645__a-glass-building-on-lisbon-street.mp4` |
| run | 67 | newspapers_printing:42, courtroom_justice:9 | `ia__woman-on-the-run-1950-202509__woman-on-the-run-1950-12-cc-crime-film-noir-1-18-31.mp4` |
| tunnel | 67 | government_buildings:32, police_modern:7 | `pixabay_extra__v_160715__tunnel-passage-corridor-the-loop-infinity-intro-3d.mp4` |
| farm | 67 | prison_jail:26, wildlife_animals:12 | `ia__000419-202005__home-movie-000419-1960s-pennsylvania-farm.mp4` |
| key | 67 | money_banking:21, hands_and_transactions:10 | `mixkit__12877__slow-motion-offer-of-house-key-and-handshake.mp4` |
| reading | 67 | courtroom_justice:56, hands_and_transactions:4 | `mixkit__14725__student-reading-on-the-library-corridor.mp4` |
| wealth | 67 | money_banking:66, prison_jail:1 | `pixabay_extra__v_105802__dollar-money-coin-gold-wealth-cash.mp4` |
| machine | 66 | science_tech:26, money_banking:7 | `mixkit__32432__close-up-of-a-sewing-machine-needle-emotion.mp4` |
| life | 66 | ocean_nature:37, wildlife_animals:16 | `mixkit__44870__tropical-sea-life-swimming-gently-along-a-coral-reef-bank.mp4` |
| france | 65 | war_history:16, government_buildings:16 | `ia__npc-4912__invasion-of-france-german-newsreel.mp4` |
| dusk | 65 | landscapes_timelapse:42, world_cities:5 | `mixkit__3428__street-with-people-walking-at-dusk.mp4` |
| hiking | 65 | courtroom_justice:49, landscapes_timelapse:7 | `pixabay_extra__v_1010__hiker-nature-lake-calm-walking-hiking-walk-mountains-alone-t.mp4` |
| restaurant | 65 | selling_floor:34, government_buildings:15 | `mixkit__24405__waiter-taking-customer-order-in-the-restaurant.mp4` |
| writing | 65 | hands_and_transactions:35, newspapers_printing:10 | `mixkit__14604__young-woman-writing-on-a-notebook-in-the-kitchen.mp4` |
| ocean water | 65 | ocean_nature:56, courtroom_justice:2 | `mixkit__45611__ocean-water-moving-calmly.mp4` |
| feathers | 65 | wildlife_animals:54, prison_jail:4 | `pixabay_extra__v_161942__bird-heron-flight-pond-feathers-lift-off-fauna-wings-nature.mp4` |
| road highway | 65 | small_town:52, police_modern:5 | `pixabay_extra__v_123433__road-highway-car-vehicle-mountains-nature.mp4` |
| big | 64 | wildlife_animals:23, world_cities:18 | `ia__the-big-clock-1948-202412__the-big-clock-1948-cc-film-noir-thriller-1-35-25.mp4` |
| eating | 64 | hands_and_transactions:41, wildlife_animals:17 | `mixkit__11156__barbary-ape-eating-fruit-on-a-tree.mp4` |
| paper | 64 | courtroom_justice:19, money_banking:16 | `ia__papermans-paper__industry-on-parade-paperman-s-paper-ink-inc-use-and-discard.mp4` |
| counting | 64 | money_banking:60, hands_and_transactions:2 | `mixkit__14007__counting-euro-paper-money-on-the-table.mp4` |
| sale | 63 | selling_floor:35, household_loss:11 | `mixkit__12944__men-discuss-business-sale-on-deck-of-yacht.mp4` |
| scenery | 63 | landscapes_timelapse:18, ocean_nature:11 | `mixkit__15625__canyon-scenery.mp4` |
| landscape nature | 63 | landscapes_timelapse:32, small_town:7 | `mixkit__43161__couple-looking-at-a-landscape-in-nature.mp4` |
| beach sea | 63 | ocean_nature:40, landscapes_timelapse:13 | `mixkit__1087__aerial-shot-of-a-beach-with-sea-waves.mp4` |
| economy | 63 | money_banking:59, world_cities:1 | `pixabay_extra__v_108778__investment-success-finance-currency-money-economy-publicity.mp4` |
| flag symbol | 63 | government_buildings:63 | `pixabay_extra__v_110268__ukraine-flag-symbol-sky-city-country-state-symbols-symbol-of.mp4` |
| stars | 62 | police_modern:21, textures_backgrounds:10 | `mixkit__19353__christmas-hanging-stars-with-pink-bokeh-background.mp4` |
| intro | 62 | money_banking:33, business_corporate:5 | `pixabay_extra__v_241982__intro-introduction-colorful-graphic-business-advertising-web.mp4` |
| spring | 62 | japan:20, landscapes_timelapse:9 | `mixkit__26999__mountainous-landscape-in-spring-with-cloudy-sky.mp4` |
| world | 62 | small_town:12, government_buildings:10 | `ia__world-for-ransom-1954-202603__world-for-ransom-1954-drama-film-noir-1-22-18.mp4` |
| female | 62 | wildlife_animals:18, police_modern:13 | `mixkit__28293__female-reporter-reporting-with-microphone-in-hand-on-a-chrom.mp4` |
| couple | 62 | hands_and_transactions:19, courtroom_justice:18 | `mixkit__32616__feet-of-a-couple-of-people-walking-in-a-park.mp4` |
| auto | 62 | police_modern:36, small_town:8 | `pixabay_extra__v_104135__highway-traffic-automobiles-auto-car-rome-italy-speed-street.mp4` |
| body | 62 | police_modern:51, hands_and_transactions:3 | `mixkit__17107__model-of-the-human-body.mp4` |
| woods | 61 | courtroom_justice:21, wildlife_animals:20 | `mixkit__6845__couple-walking-in-the-woods.mp4` |
| meadow | 61 | wildlife_animals:22, landscapes_timelapse:9 | `mixkit__3661__big-elephant-walking-in-a-meadow.mp4` |
| worker | 61 | goods_in_motion:29, hands_and_transactions:19 | `mixkit__4705__young-worker-doing-inventory.mp4` |
| reflection | 61 | ocean_nature:12, landscapes_timelapse:10 | `mixkit__221__reflection-of-a-screen-in-glasses.mp4` |
| dollars | 61 | money_banking:59, hands_and_transactions:2 | `mixkit__12510__casino-poker-table-full-of-dice-dollars-and-chips.mp4` |
| paint | 61 | textures_backgrounds:52, money_banking:7 | `mixkit__51409__colorful-ink-drops-on-pink-paint.mp4` |
| water nature | 61 | ocean_nature:34, newspapers_printing:8 | `pixabay_extra__v_214806__stream-water-nature-walk-countryside-rural-scene-people-walk.mp4` |
| city night | 60 | world_cities:33, police_modern:13 | `coverr__5837__cars-in-the-city-at-night.mp4` |
| keyboard | 60 | newspapers_printing:23, science_tech:22 | `mixkit__17695__hands-typing-on-computer-keyboard.mp4` |
| gold | 60 | money_banking:36, textures_backgrounds:12 | `mixkit__13925__3d-moving-gold-coins.mp4` |
| day | 59 | small_town:7, landscapes_timelapse:6 | `coverr__7560__timelapse-from-day-to-night.mp4` |
| down | 59 | space_nasa:8, money_banking:8 | `mixkit__21069__looking-down-over-skyscrapers-and-pools.mp4` |
| port | 59 | goods_in_motion:33, world_cities:7 | `mixkit__20179__singapore-trading-port-and-cranes-time-lapse.mp4` |
| weather | 59 | landscapes_timelapse:25, household_loss:8 | `pixabay_extra__v_106617__sunset-sun-clouds-trees-golden-weather-fluffy-gold-sky-cloud.mp4` |
| man walking | 59 | courtroom_justice:51, prison_jail:3 | `mixkit__1062__man-walking-on-large-boulders.mp4` |
| diving | 59 | ocean_nature:57, courtroom_justice:1 | `pixabay_extra__v_1084__diving-scuba-diving-underwater-fish-ocean-sea-marine-diver-a.mp4` |
| geometric | 59 | prison_jail:46, science_tech:4 | `pixabay_extra__v_270877__abstract-background-calming-geometric-design-graphic-motion.mp4` |
| wood | 58 | courtroom_justice:15, money_banking:8 | `pixabay_extra__v_183009__woman-path-road-trees-walking-person-autumn-fall-forest-wood.mp4` |
| sheep | 58 | wildlife_animals:36, courtroom_justice:7 | `pixabay_extra__v_156929__sheep-lamb-wool-animal-livestock-walking-flock-cute-nature.mp4` |
| pearl | 58 | navy_harbor:57, goods_in_motion:1 | `nara__75302-14908202__uss-argonaut-returns-to-pearl-harbor-with-usmc-raiders-from.mp4` |
| city architecture | 58 | world_cities:30, government_buildings:25 | `pixabay_extra__v_28883__albert-dock-li-liverpool-city-architecture-england-travel-bu.mp4` |
| architecture construction | 58 | government_buildings:57, world_cities:1 | `pixabay_extra__v_138603__buildings-architecture-construction-city-urban-properties-ap.mp4` |
| daylight | 58 | police_modern:18, courtroom_justice:15 | `pixabay_extra__v_136463__crab-seafood-animal-sea-ocean-rocks-walking-water-daylight-s.mp4` |
| car vehicle | 58 | police_modern:53, small_town:2 | `pixabay_extra__v_1134__drift-car-vehicle-parking-lot-tires-tuning-sport-ride-event.mp4` |
| pond | 57 | wildlife_animals:32, japan:9 | `mixkit__10998__herd-of-african-elephants-in-a-pond.mp4` |
| moving | 57 | selling_floor:9, hands_and_transactions:7 | `mixkit__40228__bright-fabric-texture-moving-with-the-wind.mp4` |
| fuji | 57 | japan:56, police_modern:1 | `mixkit__28665__mount-fuji-and-houses-landscape.mp4` |
| education | 57 | courtroom_justice:35, small_town:13 | `mixkit__9000__girl-studies-high-school-education-in-library.mp4` |
| web | 57 | prison_jail:24, science_tech:18 | `mixkit__28737__woman-scrolling-the-web-on-a-tablet.mp4` |
| floor | 56 | money_banking:51, business_corporate:2 | `pixabay_extra__v_1081__underwater-sea-floor-rocks-wreck-ship-sunken-corals-sea-ocea.mp4` |
| truck | 56 | goods_in_motion:32, small_town:11 | `mixkit__25444__excavator-loading-up-a-truck.mp4` |
| mount | 56 | japan:51, landscapes_timelapse:2 | `mixkit__28665__mount-fuji-and-houses-landscape.mp4` |
| seascape | 56 | ocean_nature:53, landscapes_timelapse:2 | `pixabay_extra__v_10287__nature-seascape-tide-cove-blue-north-landing-flamborough-bri.mp4` |
| pearl harbor | 56 | navy_harbor:56 | `nara__75302-14908202__uss-argonaut-returns-to-pearl-harbor-with-usmc-raiders-from.mp4` |
| laboratory | 56 | science_tech:53, space_nasa:2 | `mixkit__21454__laboratory-worker-looking-at-a-test-tube.mp4` |
| international | 56 | space_nasa:49, government_buildings:2 | `nasa__2022_ISS_Results_Highlights-MP4__2022-annual-highlights-of-results-from-the-international-spa.mp4` |
| skyscrapers | 56 | government_buildings:23, world_cities:22 | `mixkit__30386__zoom-out-shot-of-buildings-and-skyscrapers-in-nyc.mp4` |
| electronics | 56 | science_tech:55, hands_and_transactions:1 | `mixkit__47258__robot-working-in-an-electronics-manufacturing-facility.mp4` |
| swim | 56 | ocean_nature:44, wildlife_animals:8 | `mixkit__44978__a-school-of-colourful-reef-fish-swim-in-the-shallows-of-a-co.mp4` |
| nature wildlife | 56 | wildlife_animals:49, courtroom_justice:2 | `pixabay_extra__v_104040__deer-mammal-ruminant-wild-nature-wildlife-cub-antler.mp4` |

## 2b. Everything by subject — 350 subjects with >= 6 items

Search these words, not theme names. `themes` tells you which shelf folder holds them; `example` is a representative real file.

| subject | items | video | image | audio | top themes | example |
|---|---:|---:|---:|---:|---|---|
| nature | 5,929 | 1721 | 4179 | 29 | wildlife_animals:1279, landscapes_timelapse:1168 | `pixabay_extra__i_10133004__wooden-table-top-wood-table-background-blurred-nature-backgr.jpg` |
| file | 5,570 | 16 | 5554 | 0 | factory_manufacturing:2194, retail_commerce:922 | `nara__116008446-116008447__approved-pension-application-file-for-matilda-butz-nicholson.jpg` |
| space | 2,933 | 473 | 2418 | 42 | space_nasa:2221, science_tech:488 | `loc__17007207__masters-of-space-morse-and-the-telegraph-thompson-and-the-ca.jpg` |
| launch | 2,807 | 181 | 2625 | 1 | space_nasa:2712, science_tech:82 | `nara__6386305-14136708__an-m270-227-mm-multiple-launch-rocket-system-from-b-battery.jpeg` |
| city | 2,585 | 1062 | 1404 | 119 | world_cities:1011, government_buildings:411 | `loc__2017703170__golden-rule-storefront-federal-avenue-mason-city-iowa.tif` |
| sea | 2,501 | 1083 | 1344 | 74 | ocean_nature:1640, goods_in_motion:151 | `nara__6423394-13248799__a-helicopter-anti-submarine-squadron-2-hs-2-sh-3h-sea-king-h.jpeg` |
| building | 2,354 | 372 | 1976 | 6 | government_buildings:556, courtroom_justice:489 | `loc__ga0485__3818-east-main-street-commercial-building-college-park-fulto.tif` |
| water | 2,342 | 995 | 1179 | 168 | ocean_nature:798, landscapes_timelapse:275 | `loc__2013634223__view-across-water-toward-the-alton-lennon-federal-building-a.jpg` |
| earth | 2,207 | 75 | 2132 | 0 | space_nasa:2140, small_town:15 | `met__337551__allegory-of-earth.jpg` |
| landscape | 2,099 | 855 | 1244 | 0 | landscapes_timelapse:944, japan:365 | `nasa__GSFC_20171208_Archive_e002076__hubble-captures-spectacular-landscape-in-the-carina-nebula.jpg` |
| architecture | 2,064 | 523 | 1541 | 0 | government_buildings:815, world_cities:395 | `pixabay_extra__i_1011876__building-cologne-facade-architecture-house-facade-modern-gla.jpg` |
| ocean | 2,032 | 972 | 935 | 125 | ocean_nature:1577, sfx_environment:123 | `coverr__2122__foamy-ocean-waves-at-night.mp4` |
| forest | 1,731 | 576 | 973 | 182 | wildlife_animals:632, landscapes_timelapse:440 | `nara__55182035-55182036__111-sc-10870-an-artilleryman-s-bunk-in-the-forest-battery-al.jpg` |
| animal | 1,567 | 521 | 1045 | 1 | wildlife_animals:1090, government_buildings:155 | `pixabay_extra__i_2557294__cat-kitten-animal-pet-desk-office-notepad-nature-papers.jpg` |
| expedition | 1,528 | 23 | 1505 | 0 | space_nasa:1508, science_tech:12 | `loc__05039718__report-of-board-of-officers-to-consider-an-expedition-for-th.jpg` |
| night | 1,515 | 420 | 558 | 537 | sfx_environment:416, world_cities:363 | `loc__2017810669__two-policemen-on-the-main-street-saturday-night-when-all-the.tif` |
| street | 1,484 | 418 | 1019 | 47 | world_cities:416, small_town:254 | `loc__2011632219__main-street-in-philadelphia-pennsylvania.jpg` |
| road | 1,434 | 803 | 596 | 35 | small_town:716, police_modern:210 | `coverr__1246__a-guy-crosses-a-road-in-a-city.mp4` |
| wildlife | 1,417 | 727 | 690 | 0 | wildlife_animals:1222, government_buildings:80 | `ia__33-451-r-1-2__our-wildlife-resources.mp4` |
| door | 1,336 | 103 | 132 | 1101 | sfx_human_movement:1031, sfx_mechanical:61 | `freesound__213345__stove-door-open-interior-ambience-door-close.mp3` |
| sky | 1,266 | 587 | 677 | 2 | landscapes_timelapse:362, japan:137 | `nara__6476470-12968270__a-rainbow-highlights-the-sky-in-the-background-as-the-battle.jpeg` |
| center | 1,196 | 49 | 1146 | 1 | space_nasa:695, science_tech:318 | `loc__2017702492__laundry-center-main-street-binghampton-new-york.tif` |
| nasa | 1,191 | 98 | 1093 | 0 | space_nasa:983, science_tech:171 | `nasa__PIA15077__nasa-spacecraft-images-massive-crack-in-antarctica-pine-isla.jpg` |
| old | 1,181 | 150 | 897 | 134 | world_cities:172, economy_crisis:169 | `loc__2020724560__the-now-as-of-2019-blue-star-diner-along-old-u-s-highway-60.tif` |
| beach | 1,166 | 592 | 427 | 147 | ocean_nature:634, sfx_environment:142 | `coverr__6079__cliffs-on-praia-do-pinh-o-beach.mp4` |
| observations | 1,062 | 2 | 1060 | 0 | space_nasa:1061, ocean_nature:1 | `nasa__61a-52-0049__sts-61a-earth-observations.jpg` |
| earth observations | 1,058 | 1 | 1057 | 0 | space_nasa:1057, ocean_nature:1 | `nasa__61a-52-0049__sts-61a-earth-observations.jpg` |
| crew | 1,027 | 53 | 974 | 0 | space_nasa:928, science_tech:35 | `nara__6421148-13153338__crew-members-aboard-the-japanese-training-ship-katori-tv-350.jpeg` |
| mountain | 994 | 279 | 692 | 23 | landscapes_timelapse:528, japan:245 | `loc__2005693170__barbourville-ky-knox-county-court-house-a-mountain-county-co.tif` |
| bird | 994 | 464 | 470 | 60 | wildlife_animals:745, sfx_environment:58 | `met__453250__study-of-a-bird.jpg` |
| car | 987 | 368 | 336 | 283 | police_modern:457, sfx_mechanical:204 | `mixkit__24481__car-driving-away.mp4` |
| observations expedition | 975 | 0 | 975 | 0 | space_nasa:975 | `nasa__iss007e07306__earth-observations-taken-by-the-expedition-seven-crew.jpg` |
| station | 947 | 110 | 823 | 14 | space_nasa:578, small_town:110 | `loc__2022632569__man-on-motorcyle-stopping-at-a-gas-station-jugopetrol-belgra.tif` |
| close | 946 | 143 | 203 | 600 | sfx_human_movement:509, sfx_environment:72 | `freesound__517456__city-night-side-street-delivery-scooter-close-seat-engine-cl.mp3` |
| store | 942 | 72 | 867 | 3 | retail_commerce:580, selling_floor:130 | `loc__2012645659__view-of-store-fronts-along-main-street-in-benson-arizona.tif` |
| waves | 915 | 419 | 245 | 251 | ocean_nature:496, sfx_environment:251 | `coverr__2122__foamy-ocean-waves-at-night.mp4` |
| bank | 911 | 115 | 794 | 2 | money_banking:432, bank_and_branch:344 | `loc__wv0038__bank-of-wheeling-1229-main-street-wheeling-ohio-county-wv.tif` |
| sunset | 907 | 585 | 316 | 6 | landscapes_timelapse:351, ocean_nature:135 | `coverr__1213__timelapse-of-manhattan-at-sunset.mp4` |
| artemis | 900 | 90 | 810 | 0 | space_nasa:850, science_tech:35 | `nasa__KSC-20190606-PH_JBS01_0014__artemis-1-motor-arrival-at-kennedy-space-center.jpg` |
| river | 873 | 303 | 403 | 167 | landscapes_timelapse:224, sfx_environment:161 | `loc__mn0399__sherburne-county-courthouse-320-lowell-avenue-elk-river-sher.tif` |
| rocket | 840 | 78 | 761 | 1 | space_nasa:799, science_tech:18 | `nara__6386305-14136708__an-m270-227-mm-multiple-launch-rocket-system-from-b-battery.jpeg` |
| office | 830 | 237 | 547 | 46 | business_corporate:311, courtroom_justice:75 | `loc__2006675203__photographs-of-the-old-post-office-and-u-s-courthouse-300-we.tif` |
| trees | 828 | 355 | 399 | 74 | landscapes_timelapse:193, small_town:164 | `nara__6664202-13636279__yellow-ribbons-adorn-the-tree-trunks-of-all-of-the-trees-at.jpeg` |
| kennedy | 818 | 26 | 792 | 0 | space_nasa:605, science_tech:167 | `loc__va0138__kennedy-buildings-416-418-king-street-alexandria-independent.tif` |
| mountains | 815 | 338 | 469 | 8 | landscapes_timelapse:519, japan:91 | `nasa__STS106-705-009__glaciers-in-the-himalayan-mountains-taken-from-atlantis-duri.jpg` |
| coast | 803 | 336 | 455 | 12 | ocean_nature:600, japan:21 | `loc__2017691820__women-aircraft-workers-precision-assembly-at-a-west-coast-ai.tif` |
| space center | 798 | 1 | 797 | 0 | space_nasa:611, science_tech:167 | `nasa__KSC-03pd2367__kennedy-space-center-fla-justin-manley-of-the-national-ocean.jpg` |
| kennedy space | 787 | 2 | 785 | 0 | space_nasa:600, science_tech:167 | `nasa__KSC-03pd2367__kennedy-space-center-fla-justin-manley-of-the-national-ocean.jpg` |
| clouds | 786 | 494 | 292 | 0 | landscapes_timelapse:452, japan:63 | `ia__juusonturhavideodiary-clouds26htimelapse__juuson-turha-video-diary-clouds-26h-timelapse-2.mp4` |
| business | 777 | 397 | 380 | 0 | business_corporate:270, money_banking:222 | `mixkit__15716__men-in-black-shirts-shake-hands-at-business-meetng.mp4` |
| sts | 777 | 0 | 777 | 0 | space_nasa:622, science_tech:148 | `loc__99402715__bank-of-america-wall-wm-sts.tif` |
| travel | 773 | 282 | 488 | 3 | world_cities:159, japan:110 | `loc__22005246__travel-orders-press-on-the-note-book-of-a-war-relief-worker.jpg` |
| observation | 766 | 4 | 762 | 0 | space_nasa:731, science_tech:25 | `nasa__41g-120-056__earth-observation-taken-during-the-41g-mission.jpg` |
| aerial | 764 | 523 | 241 | 0 | landscapes_timelapse:234, ocean_nature:205 | `mixkit__31688__empty-street-in-berlin-aerial-shot.mp4` |
| traffic | 753 | 563 | 110 | 80 | world_cities:230, police_modern:214 | `coverr__8472__midwest-traffic.mp4` |
| deer | 753 | 166 | 586 | 1 | wildlife_animals:743, newspapers_printing:3 | `pixabay_extra__i_10012863__nature-deer-roe-deer-wildflowers-forest-wild-summer-antlers.jpg` |
| japan | 749 | 261 | 464 | 24 | japan:663, ambience_beds:11 | `loc__13005426__japan-and-japanese-american-relations.jpg` |
| fla | 748 | 4 | 740 | 4 | space_nasa:570, science_tech:161 | `loc__2016794750__duval-county-court-house-jacksonville-fla.tif` |
| money | 746 | 381 | 365 | 0 | money_banking:706, bank_and_branch:23 | `mixkit__14007__counting-euro-paper-money-on-the-table.mp4` |
| man | 742 | 490 | 243 | 9 | courtroom_justice:164, newspapers_printing:72 | `coverr__4931__an-old-man-looking-out-of-the-window.mp4` |
| drone | 735 | 519 | 14 | 202 | landscapes_timelapse:198, ambience_beds:172 | `mixkit__11937__drone-flying-past-a-cargo-ship.mp4` |
| urban | 735 | 358 | 361 | 16 | world_cities:327, government_buildings:93 | `loc__2020724792__shop-in-clarendon-a-lively-unincorporated-urban-neighborhood.tif` |
| center fla | 734 | 0 | 734 | 0 | space_nasa:568, science_tech:160 | `nasa__KSC-03pd2367__kennedy-space-center-fla-justin-manley-of-the-national-ocean.jpg` |
| earth observation | 725 | 1 | 724 | 0 | space_nasa:722, landscapes_timelapse:3 | `nasa__41g-120-056__earth-observation-taken-during-the-41g-mission.jpg` |
| courthouse | 723 | 4 | 719 | 0 | courtroom_justice:705, americana_1930s_1970s:11 | `loc__2003669822__court-square-vance-monument-courthouse-city-hall-palmetto-bu.tif` |
| underwater | 722 | 343 | 374 | 5 | ocean_nature:677, textures_backgrounds:28 | `pixabay_extra__i_101373__underwater-anemone-diving-reef-tropical-marine-coral-life-di.jpg` |
| wood | 708 | 58 | 210 | 440 | sfx_human_movement:418, courtroom_justice:79 | `freesound__152989__morning-atmo-june-wood-garden-mp3.mp3` |
| international | 705 | 56 | 649 | 0 | space_nasa:686, japan:4 | `nasa__0000552__international-space-station-iss.jpg` |
| buildings | 704 | 294 | 410 | 0 | world_cities:264, government_buildings:170 | `loc__ia0330__commercial-industrial-buildings-bishop-s-block-90-main-stree.tif` |
| crewmember | 699 | 0 | 699 | 0 | space_nasa:699 | `nasa__iss026e008222__earth-observations-taken-by-expedition-26-crewmember.jpg` |
| house | 695 | 182 | 493 | 20 | government_buildings:109, police_modern:77 | `loc__2020742585__the-1937-vintage-western-view-diner-and-steak-house-on-histo.tif` |
| expedition crewmember | 695 | 0 | 695 | 0 | space_nasa:695 | `nasa__iss026e008222__earth-observations-taken-by-expedition-26-crewmember.jpg` |
| factory | 680 | 41 | 628 | 11 | economy_crisis:278, factory_manufacturing:269 | `loc__05019050__organizing-a-factory-an-analysis-of-the-elements-in-factory.jpg` |
| mission | 666 | 42 | 624 | 0 | space_nasa:335, science_tech:314 | `nasa__20040421_exp9_01__russian-mission-control-center.jpg` |
| computer | 663 | 318 | 297 | 48 | science_tech:462, business_corporate:67 | `ia__univac-commercial-classic-old-vintage__classic-tv-commercial-for-a-univac-computer.mp4` |
| design | 659 | 212 | 446 | 1 | textures_backgrounds:333, prison_jail:69 | `loc__13017645__rogers-drawing-and-design-an-educational-treatise-relating-t.jpg` |
| walking | 657 | 374 | 47 | 236 | courtroom_justice:272, sfx_human_movement:226 | `coverr__8360__walking-to-the-mountain-top.mp4` |
| open | 651 | 41 | 67 | 543 | sfx_human_movement:512, goods_in_motion:17 | `freesound__427860__roomtone-house-open-lite-birds-fridge.mp3` |
| table | 651 | 124 | 523 | 4 | police_modern:241, prison_jail:126 | `loc__19010074__memory-keys-a-table-top-treatise-on-unlocking-the-mind-s-tre.jpg` |
| spacex | 645 | 42 | 603 | 0 | space_nasa:641, science_tech:4 | `nasa__iss040e000399__spacex-dragon-undocking-from-the-international-space-station.jpg` |
| blue | 638 | 226 | 406 | 6 | ocean_nature:176, landscapes_timelapse:39 | `nasa__GSFC_20171208_Archive_e001527__blue-beaufort-sea-ice-from-operation-icebridge.jpg` |
| interior | 636 | 46 | 538 | 52 | courtroom_justice:213, police_modern:105 | `loc__2010718859__interior-detail-james-t-foley-u-s-post-office-and-courthouse.jpg` |
| woman | 628 | 375 | 252 | 1 | hands_and_transactions:100, courtroom_justice:94 | `ia__the-second-woman-1950-202602__the-second-woman-1950-cc-film-noir-mystery-1-30-49.mp4` |
| light | 626 | 260 | 291 | 75 | prison_jail:161, police_modern:64 | `loc__mt0107__anaconda-historic-district-electric-light-building-101-103-m.tif` |
| telescope | 623 | 7 | 616 | 0 | science_tech:574, space_nasa:45 | `nasa__0400393__history-of-hubble-space-telescope-hst.jpg` |
| window | 622 | 122 | 485 | 15 | prison_jail:270, household_loss:71 | `loc__2010718829__historic-courthouse-window-detail-federal-building-and-u-s-c.jpg` |
| background | 620 | 473 | 101 | 46 | textures_backgrounds:134, money_banking:72 | `mixkit__10435__hand-of-a-person-squeezing-an-orange-on-a-light-background.mp4` |
| town | 617 | 122 | 468 | 27 | small_town:259, world_cities:161 | `loc__2006683803__view-of-13th-century-church-and-16th-century-town-square-and.tif` |
| flag | 615 | 529 | 86 | 0 | government_buildings:528, small_town:22 | `mixkit__11026__philippine-flag-waving-in-the-sky.mp4` |
| keyboard | 598 | 60 | 111 | 427 | sfx_mechanical:427, science_tech:73 | `freesound__108477__keyboard-wav.mp3` |
| wind | 597 | 173 | 242 | 182 | science_tech:187, sfx_environment:149 | `nasa__A-12700__mcdonald-xp-85-airplane-in-40x80-foot-wind-tunnel.jpg` |
| space station | 594 | 70 | 524 | 0 | space_nasa:560, science_tech:27 | `nasa__iss071e047733__the-space-station-soars-into-orbital-daytime.jpg` |
| green | 594 | 350 | 244 | 0 | economy_crisis:70, money_banking:66 | `mixkit__28384__golden-falling-bullets-with-green-background.mp4` |
| room | 590 | 132 | 393 | 65 | police_modern:196, science_tech:68 | `loc__2005683575__supreme-court-room-in-the-capitol-chair-of-the-chief-of-just.tif` |
| beautiful | 578 | 491 | 87 | 0 | government_buildings:174, textures_backgrounds:100 | `coverr__8352__beautiful-rocky-shoreline.mp4` |
| temple | 577 | 163 | 395 | 19 | japan:513, government_buildings:25 | `pixabay_extra__i_1751558__paestum-salerno-italy-greek-temple-columns-temple-of-neptune.jpg` |
| wild | 576 | 219 | 356 | 1 | wildlife_animals:495, landscapes_timelapse:14 | `met__338735__an-allegory-male-nude-in-a-stable-with-four-wild-horses.jpg` |
| white | 574 | 151 | 419 | 4 | wildlife_animals:85, prison_jail:48 | `loc__2012645740__supreme-court-part-i-white-plains-new-york.tif` |
| people | 567 | 346 | 206 | 15 | courtroom_justice:84, selling_floor:70 | `mixkit__15997__people-feet-walking.mp4` |
| lights | 566 | 365 | 200 | 1 | textures_backgrounds:160, police_modern:134 | `coverr__284__blurred-christmas-lights.mp4` |
| coral | 566 | 175 | 390 | 1 | ocean_nature:563, wildlife_animals:2 | `nasa__PIA25861__study-uses-modis-data-to-determine-belize-coral-reef-risk.jpg` |
| ship | 557 | 145 | 405 | 7 | goods_in_motion:438, japan:38 | `loc__2017693922__ship-launching-in-portland-maine-the-men-behind-the-launchin.tif` |
| park | 551 | 130 | 380 | 41 | courtroom_justice:194, wildlife_animals:74 | `loc__oh0277__sandusky-county-courthouse-south-park-street-fremont-sandusk.tif` |
| snow | 548 | 192 | 345 | 11 | landscapes_timelapse:207, japan:103 | `loc__2018663275__neon-rich-nightime-view-of-the-snow-cap-diner-near-seligman.tif` |
| reef | 546 | 186 | 359 | 1 | ocean_nature:527, money_banking:10 | `nasa__GSFC_20171208_Archive_e001931__great-barrier-reef.jpg` |
| shuttle | 546 | 1 | 545 | 0 | space_nasa:511, science_tech:27 | `nasa__0400207__space-shuttle-projects.jpg` |
| county | 545 | 2 | 541 | 2 | courtroom_justice:339, uk_highstreet_postoffice:39 | `loc__2003669769__plymouth-county-court-house-plymouth-mass.tif` |
| vehicle | 544 | 221 | 320 | 3 | police_modern:264, space_nasa:140 | `nara__6418527-13170342__a-pioneer-i-remotely-piloted-vehicle-rpv-is-readied-for-flig.jpeg` |
| waterfall | 542 | 72 | 419 | 51 | landscapes_timelapse:433, sfx_environment:51 | `pixabay_extra__i_10094940__beskid-waterfall-water-nature-landscape-poland-mountains.jpg` |
| red | 541 | 150 | 388 | 3 | wildlife_animals:160, space_nasa:45 | `loc__2010720364__untitled-sculpture-with-green-and-red-fluorescent-lights-ent.jpg` |
| technology | 533 | 359 | 174 | 0 | science_tech:324, business_corporate:53 | `ia__0559-threads-of-technology__threads-of-technology.mp4` |
| during | 530 | 29 | 486 | 15 | space_nasa:256, science_tech:114 | `loc__2017802009__interior-of-courtroom-during-trial-of-automobile-accident-ca.tif` |
| mount | 512 | 56 | 452 | 4 | japan:465, landscapes_timelapse:13 | `nara__6348731-14703641__from-the-marine-camp-the-famous-mount-fuji-can-be-seen-in-th.jpeg` |
| mammal | 507 | 130 | 377 | 0 | wildlife_animals:390, government_buildings:93 | `pixabay_extra__i_1596703__seal-closeup-wildlife-mammal-nature-beach-fur.jpg` |
| glass | 506 | 67 | 407 | 32 | factory_manufacturing:147, business_corporate:92 | `loc__2014650024__glass-enclosed-lobby-wayne-n-aspinall-federal-building-and-u.jpg` |
| wallpaper | 502 | 399 | 103 | 0 | government_buildings:156, textures_backgrounds:82 | `pixabay_extra__v_154833__woman-phone-business-casual-cheerful-beautiful-wallpaper-cus.mp4` |
| typing | 499 | 79 | 18 | 402 | sfx_mechanical:401, newspapers_printing:54 | `freesound__118817__25-typing-wav.mp3` |
| international space | 499 | 39 | 460 | 0 | space_nasa:499 | `nasa__0000552__international-space-station-iss.jpg` |
| field | 490 | 105 | 341 | 44 | war_history:179, small_town:64 | `nara__148727112-148727113__photograph-of-battery-c-599th-field-artillery-battalion.jpg` |
| mill | 487 | 2 | 480 | 5 | factory_manufacturing:454, stock_market_exchange:16 | `loc__03011171__cotton-mill-processes-and-calculations-an-elementary-text-bo.jpg` |
| paper | 485 | 64 | 294 | 127 | sfx_human_movement:126, money_banking:104 | `loc__07039114__shop-management-a-paper-read-before-the-american-society-of.jpg` |
| sea ocean | 482 | 243 | 239 | 0 | ocean_nature:387, landscapes_timelapse:22 | `pixabay_extra__v_102706__people-shore-sea-ocean-water-waves-beach-walk-walking-holida.mp4` |
| fish | 480 | 213 | 267 | 0 | ocean_nature:423, wildlife_animals:15 | `noaa__CINMS_fish_in_kelp_forest_50199042878__cinms-fish-in-kelp-forest-50199042878.jpg` |
| country | 475 | 312 | 131 | 32 | government_buildings:254, small_town:112 | `mixkit__19157__indonesia-flag-asian-country.mp4` |
| skyline | 474 | 134 | 338 | 2 | world_cities:303, business_corporate:104 | `nasa__sts119-s-025__sts-119-launch-skyline.jpg` |
| lake | 473 | 177 | 278 | 18 | japan:104, landscapes_timelapse:76 | `loc__2017703250__storefront-lake-city-way-73rd-avenue-kenmore-washington.tif` |
| space shuttle | 469 | 1 | 468 | 0 | space_nasa:445, science_tech:18 | `nasa__0400207__space-shuttle-projects.jpg` |
| dark | 467 | 122 | 87 | 258 | ambience_beds:141, bgm_general:117 | `freesound__176395__dark-soundscape-138bpm-loop-wav.mp3` |
| sand | 457 | 108 | 308 | 41 | landscapes_timelapse:195, ocean_nature:114 | `nasa__KSC-03pd2389__kennedy-space-center-fla-purple-flowers-flow-across-the-sand.jpg` |
| elephant | 456 | 13 | 443 | 0 | wildlife_animals:446, courtroom_justice:4 | `noaa__Adult_Male_Elephant_Seals_Battling__adult-male-elephant-seals-battling.jpg` |
| shop | 452 | 106 | 345 | 1 | retail_commerce:107, selling_floor:85 | `loc__va0733__main-street-shop-main-street-waterford-loudoun-county-va.tif` |
| winter | 448 | 208 | 224 | 16 | landscapes_timelapse:98, japan:67 | `nasa__PIA17924__nasa-radar-maps-the-winter-pace-of-iceland-glaciers.jpg` |
| police | 448 | 80 | 366 | 2 | police_modern:299, police_period:133 | `loc__00694282__hendricks-collection-no-30-police-entering-patrol-wagon-unid.jpg` |
| abandoned | 441 | 92 | 346 | 3 | economy_crisis:331, courtroom_justice:33 | `loc__2020722592__abandoned-bank-building-in-delray-an-industrial-neighborhood.tif` |
| sign | 436 | 102 | 333 | 1 | economy_crisis:135, small_town:69 | `loc__2013631471__neon-sign-for-mel-s-drive-in-and-celebrity-bar-in-the-hollyw.jpg` |
| nature landscape | 432 | 199 | 233 | 0 | landscapes_timelapse:224, ocean_nature:52 | `pixabay_extra__i_3575198__england-lake-district-nature-landscape-trees.jpg` |
| federal | 431 | 0 | 431 | 0 | courtroom_justice:383, government_buildings:27 | `loc__2006675200__photographs-of-the-harold-d-donohue-federal-building-and-cou.tif` |
| aircraft | 430 | 13 | 416 | 1 | factory_manufacturing:280, science_tech:42 | `loc__2017691815__women-aircraft-workers-women-man-america-s-machines-in-a-wes.tif` |
| open close | 428 | 0 | 1 | 427 | sfx_human_movement:418, sfx_mechanical:7 | `freesound__125958__wooden-door-open-close.mp3` |
| bench | 426 | 18 | 407 | 1 | courtroom_justice:349, science_tech:38 | `pixabay_extra__i_10140688__couple-on-bench-samsung-wallpaper-autumn-romance-beautiful-w.jpg` |
| marine | 422 | 89 | 333 | 0 | ocean_nature:218, war_history:74 | `loc__or0607__astoria-marine-construction-company-92134-front-road-astoria.tif` |
| black | 416 | 158 | 243 | 15 | textures_backgrounds:50, wildlife_animals:36 | `nara__6462948-12753076__a-uh-60-black-hawk-helicopter-follows-various-other-helicopt.jpeg` |
| nasas | 416 | 21 | 395 | 0 | space_nasa:409, science_tech:7 | `nasa__Artemis_1B_Crew_InFLight__nasas-evolved-sls-block-1b-crew-rocket-in-flight.jpg` |
| works | 412 | 5 | 407 | 0 | factory_manufacturing:355, space_nasa:30 | `loc__pa2223__u-s-steel-homestead-works-along-monongahela-river-north-of-e.tif` |
| small | 411 | 134 | 155 | 122 | small_town:157, sfx_environment:84 | `loc__05014219__water-works-systems-for-small-towns-cities-etc.jpg` |
| footsteps | 409 | 2 | 0 | 407 | sfx_human_movement:401, sfx_environment:6 | `freesound__117627__footsteps-gravel-pavement-wav.mp3` |
| tower | 406 | 69 | 333 | 4 | small_town:92, government_buildings:59 | `loc__2006679711__lima-the-public-square-municipality-and-tower-of-st-domingo.tif` |
| abstract | 405 | 379 | 26 | 0 | textures_backgrounds:189, money_banking:58 | `mixkit__30__blurred-abstract-cars-lights-at-night-with-bokeh-effect.mp4` |
| department | 402 | 3 | 399 | 0 | retail_commerce:270, selling_floor:80 | `loc__2004672464__treasury-department-procurement-division-public-buildings-br.tif` |
| mars | 402 | 5 | 397 | 0 | space_nasa:391, science_tech:6 | `nasa__201303120003HQ__mars-rock-analysis-briefing.jpg` |
| metal | 398 | 35 | 185 | 178 | sfx_human_movement:110, prison_jail:109 | `loc__2015631610__this-still-standing-granite-block-carrying-a-metal-tablet-sy.jpg` |
| africa | 398 | 104 | 291 | 3 | wildlife_animals:226, government_buildings:65 | `loc__05008818__my-personal-experiences-in-equatorial-africa-as-medical-offi.jpg` |
| moon | 398 | 90 | 308 | 0 | space_nasa:293, world_cities:19 | `nasa__09_24_24_First_steps_Axiom_suits__artists-concepts-depict-spacexs-starship-hls-on-the-moon-for.jpg` |
| wall | 394 | 44 | 327 | 23 | stock_market_exchange:98, prison_jail:50 | `loc__2016645845__courtroom-wall-detail-federal-building-u-s-courthouse-annist.jpg` |
| wooden | 393 | 55 | 240 | 98 | courtroom_justice:102, sfx_human_movement:96 | `nara__6464448-12760571__sailors-swab-the-wooden-deck-near-the-no-2-gun-turret-aboard.jpeg` |
| japanese | 393 | 96 | 295 | 2 | japan:311, navy_harbor:21 | `loc__11004068__a-japanese-and-english-dictionary-with-an-english-and-japane.jpg` |
| wave | 389 | 259 | 106 | 24 | ocean_nature:310, sfx_environment:22 | `ia__ocean-wave__ocean-wave.mp4` |
| cliff | 385 | 108 | 276 | 1 | ocean_nature:341, landscapes_timelapse:22 | `nara__6436800-13432843__carved-out-of-a-sandstone-cliff-the-alkhazneh-the-treasury-r.jpeg` |
| dome | 381 | 3 | 377 | 1 | government_buildings:359, courtroom_justice:7 | `nara__135801384-135801385__entering-old-santa-fe-dome-of-the-capitol-building-seen-at-t.jpg` |
| seal | 379 | 8 | 367 | 4 | government_buildings:306, wildlife_animals:62 | `noaa__3008x2000_ribbon_seal__3008x2000-ribbon-seal.jpg` |
| currency | 379 | 195 | 184 | 0 | money_banking:376, uk_period:1 | `pixabay_extra__v_103707__bitcoin-crypto-cryptocurrency-blockchain-currency-money-cash.mp4` |
| sls | 377 | 19 | 358 | 0 | space_nasa:377 | `nasa__Artemis_1B_Crew_InFLight__nasas-evolved-sls-block-1b-crew-rocket-in-flight.jpg` |
| rocks | 374 | 134 | 187 | 53 | ocean_nature:168, landscapes_timelapse:79 | `nasa__PIA19817__rocks-here-sequester-some-of-mars-early-atmosphere.jpg` |
| sun | 371 | 242 | 129 | 0 | landscapes_timelapse:127, ocean_nature:36 | `mixkit__4113__sun-rays-pass-through-the-clouds-in-the-mountains.mp4` |
| flight | 369 | 75 | 294 | 0 | science_tech:141, space_nasa:118 | `met__399885__an-allegory-of-the-rest-on-the-flight-into-egypt.jpg` |
| battery | 368 | 3 | 364 | 1 | war_history:348, japan:10 | `nara__6510124-13126931__lcpl-sheldon-of-india-battery-3rd-battalion-12th-marines-twe.jpeg` |
| beautiful wallpaper | 366 | 351 | 15 | 0 | government_buildings:145, textures_backgrounds:76 | `pixabay_extra__v_154833__woman-phone-business-casual-cheerful-beautiful-wallpaper-cus.mp4` |
| cars | 365 | 308 | 42 | 15 | police_modern:113, small_town:93 | `mixkit__28092__cars-driving-through-rainfall.mp4` |
| summer | 363 | 152 | 120 | 91 | ocean_nature:81, sfx_environment:68 | `mixkit__7879__man-running-during-summer.mp4` |
| symbol | 363 | 323 | 40 | 0 | government_buildings:275, money_banking:24 | `pixabay_extra__v_109053__ukraine-flag-ukraine-flag-kiev-nation-symbol.mp4` |
| fence | 362 | 80 | 282 | 0 | prison_jail:333, small_town:6 | `pixabay_extra__i_440804__wooden-fence-fence-wood-bench-garden-bank-garden-bench-outdo.jpg` |
| birds | 360 | 132 | 52 | 176 | sfx_environment:152, wildlife_animals:104 | `freesound__353559__japan-kashiwa-town-walking-light-traffic-cars-motors-birds-c.mp3` |
| floor | 360 | 56 | 113 | 191 | sfx_human_movement:183, money_banking:55 | `freesound__108850__wood-floor-wav.mp3` |
| highway | 359 | 289 | 59 | 11 | small_town:198, police_modern:48 | `mixkit__49147__trailer-crash-on-a-highway.mp4` |
| outdoors | 357 | 73 | 273 | 11 | landscapes_timelapse:90, courtroom_justice:57 | `pixabay_extra__i_165692__table-picnic-park-nature-lunch-empty-summer-scenic-outdoors.jpg` |
| rural | 356 | 87 | 252 | 17 | small_town:266, japan:32 | `loc__2017763330__rural-types-on-main-street-of-ames-iowa.tif` |
| day | 355 | 59 | 254 | 42 | space_nasa:131, science_tech:55 | `loc__2017801933__court-day-in-a-county-seat-second-day-of-superior-court-gran.tif` |
| stage | 353 | 29 | 324 | 0 | space_nasa:331, goods_in_motion:5 | `nasa__as11-44-6626__apollo-11-lunar-module-ascent-stage-photographed-from-comman.jpg` |
| time | 351 | 201 | 125 | 25 | landscapes_timelapse:75, space_nasa:61 | `ia__timelapse-teste1__blender-sunset-time-lapse-test1.mp4` |
| spacex crew | 350 | 25 | 325 | 0 | space_nasa:350 | `nasa__iss072e742584__the-four-spacex-crew-9-members-aboard-the-international-spac.jpg` |
| expedition crew | 349 | 5 | 344 | 0 | space_nasa:344, landscapes_timelapse:2 | `nasa__201205150002HQ__expedition-31-crew-prepares-for-launch.jpg` |
| market | 348 | 105 | 239 | 4 | retail_commerce:100, world_cities:69 | `loc__2017702486__victory-market-main-street-margaretville-new-york.tif` |
| court | 347 | 20 | 288 | 39 | government_buildings:180, courtroom_justice:156 | `loc__2003669769__plymouth-county-court-house-plymouth-mass.tif` |
| tree | 346 | 166 | 163 | 17 | wildlife_animals:60, landscapes_timelapse:52 | `mixkit__34016__dry-tree-leaves-falling-into-the-water-from-a-pond.mp4` |
| national | 346 | 78 | 265 | 3 | government_buildings:88, bank_and_branch:53 | `loc__tn0403__national-home-for-disabled-volunteer-soldiers-mountain-branc.tif` |
| cargo | 346 | 52 | 293 | 1 | goods_in_motion:258, space_nasa:73 | `nara__6516204-13237442__greek-air-force-captain-tsamidis-nektarios-photographs-cargo.jpeg` |
| crickets | 344 | 0 | 0 | 344 | sfx_environment:330, ambience_beds:12 | `freesound__118419__crickets-wav.mp3` |
| desk | 344 | 124 | 216 | 4 | business_corporate:170, science_tech:64 | `pixabay_extra__i_10107599__writing-hands-pen-paper-desk-office-document-work-focused-si.jpg` |
| federal building | 343 | 0 | 343 | 0 | courtroom_justice:343 | `loc__2006675200__photographs-of-the-harold-d-donohue-federal-building-and-cou.tif` |
| finance | 343 | 215 | 128 | 0 | money_banking:325, business_corporate:9 | `pixabay_extra__v_102779__money-online-earn-business-cartoon-fund-finance-paid-profit.mp4` |
| ocean sea | 339 | 212 | 127 | 0 | ocean_nature:272, wildlife_animals:17 | `pixabay_extra__v_146632__couple-beach-ocean-sea-walking-calm-travel-honeymoon-love-to.mp4` |
| washington | 336 | 11 | 325 | 0 | government_buildings:110, newspapers_printing:58 | `loc__2017703249__storefront-1st-street-mount-vernon-washington.tif` |
| apollo | 336 | 2 | 334 | 0 | space_nasa:281, science_tech:51 | `met__392659__apollo-standing-a-beside-a-woman-representing-an-allegory-of.jpg` |
| sls rocket | 336 | 11 | 325 | 0 | space_nasa:336 | `nasa__DSC00134__space-launch-system-sls-rocket-and-orion-spacecraft-rollout.jpg` |
| front | 334 | 22 | 266 | 46 | newspapers_printing:64, sfx_human_movement:40 | `loc__va0525__donnan-asher-iron-front-building-1207-1211-east-main-street.tif` |
| harbor | 333 | 135 | 197 | 1 | navy_harbor:225, japan:55 | `loc__ed-1__fairport-beacon-fairport-harbor-ohio-april-14-1950.jpg` |
| sunrise | 332 | 219 | 108 | 5 | landscapes_timelapse:124, ocean_nature:34 | `coverr__9808__sunrise-at-the-beach-dock.mp4` |
| iss | 330 | 4 | 326 | 0 | space_nasa:323, science_tech:4 | `nasa__0000552__international-space-station-iss.jpg` |
| looking | 329 | 36 | 293 | 0 | factory_manufacturing:166, goods_in_motion:24 | `loc__2020635655__bdwy-looking-south-from-129th-st-here-on-bdwy-126th-is-on-op.tif` |
| work | 329 | 154 | 169 | 6 | business_corporate:82, science_tech:80 | `loc__18021646__four-years-of-relief-and-war-work-by-the-jews-of-america-191.jpg` |
| cityscape | 325 | 123 | 201 | 1 | world_cities:172, government_buildings:55 | `pixabay_extra__i_102822__hong-kong-skyscrapers-buildings-city-skyline-cityscape-urban.jpg` |
| running | 325 | 248 | 9 | 68 | newspapers_printing:229, sfx_human_movement:41 | `mixkit__11187__guy-running-at-the-beach-during-sunset.mp4` |
| desert | 324 | 54 | 264 | 6 | landscapes_timelapse:261, small_town:13 | `nasa__GSFC_20171208_Archive_e000959__preparing-for-antarctic-flights-in-the-california-desert.jpg` |
| church | 323 | 54 | 261 | 8 | government_buildings:146, prison_jail:46 | `loc__2017879402__the-courtroom-which-at-first-glance-resembles-a-church-sanct.jpg` |
| bridge | 322 | 166 | 150 | 6 | world_cities:81, small_town:46 | `mixkit__13__city-traffic-on-a-bridge.mp4` |
| peak | 321 | 10 | 311 | 0 | landscapes_timelapse:280, japan:32 | `nara__6346140-14589518__two-c-130e-hercules-aircraft-fly-in-formation-past-the-peak.jpeg` |
| state | 320 | 174 | 144 | 2 | government_buildings:254, bank_and_branch:10 | `pixabay_extra__v_110268__ukraine-flag-symbol-sky-city-country-state-symbols-symbol-of.mp4` |
| control | 320 | 11 | 309 | 0 | science_tech:274, space_nasa:18 | `loc__17014072__shop-expense-analysis-and-control.jpg` |
| live | 319 | 72 | 246 | 1 | space_nasa:285, police_modern:10 | `nasa__200910210001HQ__nasa-live-tweetup-event-with-international-space-station.jpg` |
| engine | 318 | 10 | 195 | 113 | sfx_mechanical:109, space_nasa:81 | `loc__2020743340__a-steam-engine-is-adorned-in-christmas-lights-on-the-courtho.tif` |
| screen | 317 | 276 | 19 | 22 | economy_crisis:72, money_banking:64 | `ia__0723-america-marching-on-a-screen-editorial-with-lowell-thom__america-marching-on-a-screen-editorial-with-lowell-thomas.mp4` |
| autumn | 317 | 152 | 157 | 8 | courtroom_justice:63, small_town:47 | `pixabay_extra__i_10140688__couple-on-bench-samsung-wallpaper-autumn-romance-beautiful-w.jpg` |
| south | 316 | 35 | 269 | 12 | factory_manufacturing:75, goods_in_motion:28 | `loc__2017707189__storefronts-chester-south-carolina.tif` |
| transport | 316 | 142 | 174 | 0 | goods_in_motion:103, police_modern:65 | `nara__6350923-14699086__two-marine-corps-ch-53-sea-stallion-helicopters-transport-tr.jpeg` |
| wire | 316 | 44 | 272 | 0 | prison_jail:309, government_buildings:2 | `pixabay_extra__i_1003664__fence-pattern-wire-fence-fence-fence-fence-fence-wire-wire-w.jpg` |
| dollar | 315 | 105 | 210 | 0 | money_banking:295, bank_and_branch:9 | `pixabay_extra__i_1095903__money-euro-banknotes-currency-seem-finance-dollar-bill-europ.jpg` |
| plumage | 315 | 237 | 78 | 0 | wildlife_animals:276, courtroom_justice:12 | `pixabay_extra__v_63338__swan-bird-plumage-elegant-nature-pen-aquatic-majestic-the-wa.mp4` |
| first | 314 | 23 | 290 | 1 | space_nasa:127, science_tech:57 | `loc__co0318__american-house-hotel-northwest-corner-first-main-streets-sai.tif` |
| north | 313 | 31 | 274 | 8 | government_buildings:47, factory_manufacturing:43 | `loc__2017707115__earnhardt-s-storefront-salisbury-north-carolina.tif` |
| animals | 312 | 166 | 145 | 1 | wildlife_animals:180, ocean_nature:53 | `mixkit__11239__herds-of-african-animals-on-a-vast-plain.mp4` |
| shopping | 312 | 128 | 184 | 0 | economy_crisis:116, selling_floor:78 | `pixabay_extra__i_4181395__girl-shop-souvenirs-woman-shelf-work-shopping-spain-searchin.jpg` |
| department store | 307 | 3 | 304 | 0 | retail_commerce:267, selling_floor:37 | `nara__86722158-86722159__window-display-of-l-blumstein-department-store-151st-street.jpg` |
| laptop | 306 | 105 | 160 | 41 | science_tech:122, business_corporate:49 | `pixabay_extra__i_1035345__laptop-mockup-business-office-iphone-macbook-pro-lense-custo.jpg` |
| spacecraft | 306 | 10 | 296 | 0 | space_nasa:261, science_tech:43 | `nasa__PIA15077__nasa-spacecraft-images-massive-crack-in-antarctica-pine-isla.jpg` |
| rain | 305 | 186 | 24 | 95 | sfx_environment:63, household_loss:40 | `mixkit__28085__heavy-rain-from-an-open-window.mp4` |
| artemis launch | 304 | 8 | 296 | 0 | space_nasa:283, science_tech:21 | `nasa__KSC-20220829-PH-KLS01_0007__artemis-i-launch-control-center-activities.jpg` |
| stream | 301 | 68 | 95 | 138 | sfx_environment:136, landscapes_timelapse:99 | `freesound__165286__nolde-forest-small-stream-wind-in-trees-wav.mp3` |
| rock | 300 | 90 | 204 | 6 | ocean_nature:147, landscapes_timelapse:49 | `loc__2017707160__storefront-rock-port-missouri.tif` |
| young | 298 | 156 | 141 | 1 | wildlife_animals:71, hands_and_transactions:37 | `mixkit__50814__a-young-man-streaching-his-arms-against-the-blue-sky.mp4` |
| cash | 293 | 166 | 127 | 0 | money_banking:282, retail_commerce:6 | `mixkit__23725__female-hands-counting-cash.mp4` |
| astronaut | 293 | 17 | 276 | 0 | space_nasa:199, science_tech:84 | `nasa__ast-008-499__astronaut-vance-brand-at-controls-of-apollo-command-module.jpg` |
| allegory | 292 | 0 | 292 | 0 | americana_1930s_1970s:292 | `met__17546__allegory-of-rhetoric.jpg` |
| morning | 290 | 125 | 50 | 115 | sfx_environment:105, courtroom_justice:32 | `ia__what-happened-to-saturday-morning-cartoons__what-happened-to-saturday-morning-cartoons-2.mp4` |
| county courthouse | 288 | 0 | 288 | 0 | courtroom_justice:271, americana_1930s_1970s:10 | `loc__2003675167__hamilton-county-courthouse-chattanooga.tif` |
| air | 287 | 44 | 231 | 12 | war_history:82, space_nasa:50 | `loc__sd0059__ellsworth-air-force-base-group-administration-secure-storage.tif` |
| science | 287 | 182 | 104 | 1 | science_tech:178, space_nasa:61 | `nasa__321_SS101-PlantGrowth-03__nasa-sciencecasts-station-science-101-advancing-plant-scienc.mp4` |
| artillery | 287 | 4 | 282 | 1 | war_history:280, stock_market_exchange:2 | `nara__100310266-100310267__1st-cavalry-division-artillery-fires-a-105mm-towed-howitzer.jpg` |
| ambience | 286 | 2 | 1 | 283 | ambience_beds:146, sfx_environment:106 | `freesound__177648__thailand-hotel-hallway-ambience-bassy-heavy-some-ventilation.mp3` |
| pad | 282 | 11 | 239 | 32 | space_nasa:246, ambience_beds:25 | `nasa__200907100001HQ__space-shuttle-endeavour-on-pad-39a.jpg` |
| opening | 282 | 135 | 14 | 133 | sfx_human_movement:123, money_banking:76 | `mixkit__11518__opening-her-eyes-and-smiling.mp4` |
| tunnel | 282 | 67 | 207 | 8 | science_tech:165, government_buildings:33 | `nasa__A-12700__mcdonald-xp-85-airplane-in-40x80-foot-wind-tunnel.jpg` |
| empty | 280 | 140 | 132 | 8 | courtroom_justice:144, prison_jail:42 | `mixkit__1930__waves-at-an-empty-beach.mp4` |
| coverage | 278 | 46 | 232 | 0 | space_nasa:254, science_tech:19 | `nasa__jsc2001e25103__sts-105-coverage-of-mission-control-center-employees-in-the.jpg` |
| jupiter | 276 | 0 | 276 | 0 | space_nasa:276 | `nasa__GSFC_20171208_Archive_e000036__a-whole-new-jupiter.jpg` |
| gravel | 275 | 3 | 15 | 257 | sfx_human_movement:255, small_town:9 | `freesound__117627__footsteps-gravel-pavement-wav.mp3` |
| modern | 275 | 73 | 197 | 5 | business_corporate:87, government_buildings:43 | `loc__2020723975__a-mid-century-modern-landmark-with-a-storied-history-the-joh.tif` |
| europe | 273 | 106 | 167 | 0 | world_cities:139, government_buildings:61 | `met__334877__allegory-of-europe-from-the-four-continents.jpg` |
| test | 272 | 35 | 227 | 10 | space_nasa:184, science_tech:73 | `nara__6367711-14795033__col-jack-r-lousma-commander-third-test-mission-of-the-space.jpeg` |
| usa | 272 | 54 | 205 | 13 | war_history:95, government_buildings:55 | `nara__6507901-13052103__gen-george-a-joulwan-usa-supreme-allied-commander-europe-sac.jpeg` |
| student | 272 | 45 | 227 | 0 | space_nasa:219, courtroom_justice:38 | `nasa__20240413-MIC_8508__2024-student-launch.jpg` |
| station iss | 272 | 1 | 271 | 0 | space_nasa:272 | `nasa__0000552__international-space-station-iss.jpg` |
| machine | 271 | 66 | 193 | 12 | newspapers_printing:115, factory_manufacturing:49 | `loc__11006971__machine-shop-mechanics-the-why-of-things-in-the-shop.jpg` |
| square | 271 | 17 | 248 | 6 | small_town:153, courtroom_justice:31 | `loc__2003669822__court-square-vance-monument-courthouse-city-hall-palmetto-bu.tif` |
| army | 271 | 10 | 260 | 1 | war_history:201, government_buildings:29 | `loc__2024639942__u-s-army-trucks-and-jeeps-waiting-at-the-port-of-baltimore-m.tif` |
| facade | 270 | 15 | 255 | 0 | government_buildings:106, business_corporate:65 | `loc__2008675041__public-building-i-e-courthouse-new-haven-connecticut-facade.tif` |
| steel | 269 | 5 | 263 | 1 | factory_manufacturing:222, prison_jail:12 | `loc__15001289__cinders-the-young-apprentice-of-the-steel-mills.jpg` |
| pattern | 267 | 95 | 172 | 0 | textures_backgrounds:202, prison_jail:14 | `met__388162__embroidery-pattern-with-seven-six-pointed-stars-and-four-cor.jpg` |
| hall | 266 | 22 | 236 | 8 | economy_crisis:74, government_buildings:63 | `loc__ga0483__old-college-park-city-hall-3814-east-main-street-college-par.tif` |
| construction | 266 | 136 | 127 | 3 | government_buildings:85, newspapers_printing:40 | `mixkit__4010__buildings-under-construction-aerial-view.mp4` |
| book | 266 | 86 | 177 | 3 | courtroom_justice:142, newspapers_printing:33 | `loc__22005246__travel-orders-press-on-the-note-book-of-a-war-relief-worker.jpg` |
| fuji | 262 | 57 | 204 | 1 | japan:257, space_nasa:2 | `nara__6348731-14703641__from-the-marine-camp-the-famous-mount-fuji-can-be-seen-in-th.jpeg` |
| ambient | 258 | 2 | 0 | 256 | ambience_beds:118, bgm_general:118 | `freesound__346114__low-ambient.mp3` |
| flow | 258 | 100 | 114 | 44 | landscapes_timelapse:69, textures_backgrounds:46 | `nasa__iss074e0603582__glaciers-flow-downhill-from-the-himalayas-northern-slopes-on.jpg` |
| port | 258 | 59 | 197 | 2 | goods_in_motion:136, japan:36 | `loc__2017707160__storefront-rock-port-missouri.tif` |
| smoke | 258 | 213 | 45 | 0 | textures_backgrounds:190, factory_manufacturing:14 | `mixkit__12495__smoke-with-fluorescent-particles-on-black-background.mp4` |
| york | 256 | 38 | 214 | 4 | stock_market_exchange:64, world_cities:42 | `loc__2017702486__victory-market-main-street-margaretville-new-york.tif` |
| main | 255 | 4 | 246 | 5 | small_town:124, americana_1930s_1970s:40 | `loc__2011632219__main-street-in-philadelphia-pennsylvania.jpg` |
| fire | 255 | 101 | 89 | 65 | sfx_environment:63, textures_backgrounds:31 | `mixkit__32360__fire-in-the-woods-with-a-lot-of-smoke.mp4` |
| coral reef | 255 | 81 | 173 | 1 | ocean_nature:254, sfx_environment:1 | `nasa__PIA25861__study-uses-modis-data-to-determine-belize-coral-reef-risk.jpg` |
| gold | 255 | 60 | 195 | 0 | money_banking:184, textures_backgrounds:17 | `met__256193__gold-finger-ring-engraved-with-an-image-of-hermes.jpg` |
| shipping | 254 | 32 | 221 | 1 | goods_in_motion:232, science_tech:4 | `pixabay_extra__i_1007245__trailer-old-cargo-to-drag-transport-shipping-trailer-trailer.jpg` |
| capitol | 254 | 15 | 239 | 0 | government_buildings:244, courtroom_justice:9 | `loc__2005683575__supreme-court-room-in-the-capitol-chair-of-the-chief-of-just.tif` |
| expedition launch | 252 | 0 | 252 | 0 | space_nasa:252 | `nasa__20030426_4_launch__expedition-7-launch.tif` |
| kyoto | 251 | 23 | 228 | 0 | japan:250, retail_commerce:1 | `pixabay_extra__i_10145816__kiyomizu-temple-japanese-temple-kyoto-architecture-culture-a.jpg` |
| ground | 250 | 217 | 27 | 6 | space_nasa:206, war_history:9 | `nasa__jcs2022m000004_Space_to_Ground_404_220114__space-to-ground-spacewalks-and-research-01-14-2022.mp4` |
| tourism | 250 | 93 | 157 | 0 | world_cities:71, government_buildings:45 | `loc__2019639074__mural-tourism-at-the-golden-collum-memorial-federal-building.tif` |
| island | 248 | 86 | 157 | 5 | ocean_nature:89, prison_jail:30 | `loc__ny1601__ellis-island-kitchen-laundry-building-new-york-harbor-new-yo.tif` |
| workers | 248 | 48 | 199 | 1 | factory_manufacturing:78, goods_in_motion:52 | `loc__2017691815__women-aircraft-workers-women-man-america-s-machines-in-a-wes.tif` |
| landscape nature | 248 | 63 | 185 | 0 | landscapes_timelapse:125, small_town:40 | `pixabay_extra__i_2699359__garden-museum-gray-scale-landscape-nature-architecture-city.jpg` |
| space telescope | 247 | 2 | 245 | 0 | science_tech:209, space_nasa:38 | `nasa__0400393__history-of-hubble-space-telescope-hst.jpg` |
| atlantis | 246 | 0 | 246 | 0 | space_nasa:240, science_tech:4 | `nasa__200911150015HQ__sts-129-shuttle-atlantis-on-pad-39a.jpg` |
| evening | 245 | 114 | 91 | 40 | landscapes_timelapse:39, world_cities:38 | `mixkit__15858__lawyers-talk-with-client-in-late-evening-office.mp4` |
| distant | 244 | 3 | 49 | 192 | sfx_environment:131, ambience_beds:53 | `freesound__197706__distant-booming-traffic.mp3` |
| italy | 244 | 83 | 158 | 3 | world_cities:71, government_buildings:53 | `loc__2011660861__in-italy-the-trains-stop-at-the-stations-and-the-passengers.tif` |
| train | 242 | 110 | 72 | 60 | japan:47, sfx_mechanical:40 | `mixkit__20066__tokyo-train-station-traffic.mp4` |
| uss | 242 | 49 | 193 | 0 | navy_harbor:121, japan:88 | `loc__2017871934__pearl-harbor-hawaii-uss-west-virginia-aflame-disregarding-th.tif` |
| surface | 241 | 31 | 206 | 4 | space_nasa:176, ocean_nature:11 | `nasa__art001e002157__the-lunar-surface.jpg` |
| brown | 240 | 28 | 207 | 5 | wildlife_animals:34, landscapes_timelapse:23 | `loc__2014631502__the-brown-county-courthouse-in-brownwood-texas.jpg` |
| tokyo | 238 | 73 | 164 | 1 | japan:178, stock_market_exchange:33 | `nara__134403789-134403790__suburban-tokyo-street.jpg` |
| aquarium | 238 | 116 | 122 | 0 | ocean_nature:214, government_buildings:12 | `pixabay_extra__i_2469301__seal-aquarium-water-seal-station-ecomare-texel-mammal-aquati.jpg` |
| door open | 237 | 6 | 1 | 230 | sfx_human_movement:222, sfx_mechanical:6 | `freesound__107640__door-open-wav.mp3` |
| coffee | 236 | 158 | 77 | 1 | hands_and_transactions:92, business_corporate:31 | `mixkit__1323__couple-drinking-coffee-close-up.mp4` |
| cotton | 235 | 0 | 232 | 3 | factory_manufacturing:226, sfx_human_movement:3 | `loc__03011171__cotton-mill-processes-and-calculations-an-elementary-text-bo.jpg` |
| building courthouse | 235 | 0 | 235 | 0 | courtroom_justice:235 | `loc__2006675208__photographs-of-the-federal-building-and-u-s-courthouse-in-du.tif` |
| loop | 234 | 124 | 11 | 99 | money_banking:49, sfx_environment:38 | `mixkit__31534__futuristic-virtual-city-highway-loop-video.mp4` |
| sound | 234 | 14 | 19 | 201 | bgm_general:80, sfx_mechanical:54 | `freesound__515240__ambient-sound-1.mp3` |
| company | 234 | 12 | 222 | 0 | factory_manufacturing:83, decision_rooms:39 | `loc__2017865849__columbia-steel-company-at-geneva-utah-the-erecting-crane-is.tif` |
| path | 233 | 78 | 132 | 23 | small_town:92, courtroom_justice:32 | `nara__6462201-13580138__airmen-position-plywood-planks-along-the-path-of-an-m-270-mu.jpeg` |
| railroad | 233 | 19 | 214 | 0 | americana_1930s_1970s:119, goods_in_motion:43 | `loc__2017658617__steam-locomotive-number-4-of-the-illinois-central-railroad-c.tif` |
| grass | 230 | 99 | 120 | 11 | wildlife_animals:64, small_town:22 | `loc__ed-1__grass-valley-telegraph-grass-valley-calif-march-4-1856.jpg` |
| bokeh | 229 | 217 | 12 | 0 | textures_backgrounds:178, police_modern:11 | `mixkit__1177__blurred-multicolor-lights-bokeh.mp4` |
| exchange | 228 | 15 | 213 | 0 | stock_market_exchange:205, money_banking:17 | `loc__35030001__tables-of-sterling-exchange-for-converting-sterling-into-cur.jpg` |
| fog | 227 | 143 | 83 | 1 | landscapes_timelapse:86, courtroom_justice:30 | `mixkit__4396__fog-on-the-heights-of-the-snowy-mountains.mp4` |
| west | 227 | 10 | 215 | 2 | factory_manufacturing:66, goods_in_motion:39 | `loc__2017707099__storefront-west-union-west-virginia.tif` |
| motion | 226 | 207 | 19 | 0 | prison_jail:46, money_banking:31 | `ia__rpmusicinmotion__music-in-motion.mp4` |
| skyscraper | 224 | 50 | 172 | 2 | business_corporate:121, world_cities:40 | `pixabay_extra__i_1028965__facade-glass-facade-skyscraper-reflection-glass-stained-glas.jpg` |
| model | 223 | 43 | 177 | 3 | science_tech:96, factory_manufacturing:25 | `nasa__A-15938__delta-wing-test-model-in-ames-40x80-foot-wind-tunnel.jpg` |
| home | 222 | 111 | 103 | 8 | police_modern:30, prison_jail:21 | `ia__000416-202005__home-movie-000416-1951-detroit-area-family.mp4` |
| united | 221 | 36 | 180 | 5 | government_buildings:66, money_banking:48 | `loc__2014630544__the-united-states-federal-building-and-courthouse-in-laredo.jpg` |
| asia | 221 | 78 | 142 | 1 | japan:107, world_cities:34 | `loc__44030446__russia-central-asia-and-british-india.jpg` |
| shore | 220 | 104 | 82 | 34 | ocean_nature:143, sfx_environment:34 | `coverr__3079__the-incoming-waves-of-the-ocean-gently-splash-onto-the-shore.mp4` |
| camera | 220 | 108 | 55 | 57 | police_modern:79, sfx_mechanical:57 | `mixkit__49603__a-woman-in-a-pink-suit-points-a-firearm-to-the-camera.mp4` |
| logo | 220 | 12 | 208 | 0 | retail_commerce:167, police_modern:25 | `nasa__S89-20024__logo-for-the-20th-anniversary-of-the-apollo-11-mission.jpg` |
| heavy | 218 | 13 | 96 | 109 | sfx_human_movement:70, newspapers_printing:57 | `freesound__177648__thailand-hotel-hallway-ambience-bassy-heavy-some-ventilation.mp3` |
| dpla | 217 | 0 | 217 | 0 | retail_commerce:68, bank_and_branch:31 | `noaa__Events--Seal_Plant_Display_2006_-_DPLA_-_338838fcefbd697efef__events-seal-plant-display-2006-dpla-338838fcefbd697efef87bcd.jpg` |
| inside | 216 | 16 | 152 | 48 | factory_manufacturing:37, space_nasa:36 | `loc__2020723410__portions-of-wrought-iron-staircases-inside-the-minneapolis-c.tif` |
| animal wildlife | 216 | 97 | 119 | 0 | wildlife_animals:193, government_buildings:12 | `pixabay_extra__i_349598__fur-seal-seal-mammal-animal-wildlife-arctic-sea-nature-marin.jpg` |
| girl | 215 | 114 | 101 | 0 | courtroom_justice:38, prison_jail:22 | `mixkit__18240__little-girl-walking-in-the-valley-at-sunset.mp4` |
| savings | 215 | 22 | 193 | 0 | bank_and_branch:162, money_banking:52 | `loc__2003675527__bank-building-chevy-chase-savings-bank-connecticut-avenue-an.tif` |
| architecture building | 215 | 41 | 174 | 0 | government_buildings:100, world_cities:36 | `pixabay_extra__i_1508086__architecture-building-glass-nature-windows-business-blue-bus.jpg` |
| high | 213 | 38 | 149 | 26 | space_nasa:29, courtroom_justice:27 | `loc__2019631132__corridor-dennis-chavez-federal-building-a-high-rise-federal.tif` |
| navy | 212 | 4 | 208 | 0 | factory_manufacturing:87, japan:35 | `loc__14018565__the-story-of-our-navy.jpg` |
| leaves | 210 | 94 | 89 | 27 | courtroom_justice:37, japan:26 | `mixkit__17901__park-and-a-bench-with-fallen-leaves.mp4` |
| tropical | 210 | 98 | 105 | 7 | ocean_nature:171, weather_disasters:11 | `nasa__GSFC_20171208_Archive_e000780__tropical-cyclone-glenda-in-the-indian-ocean.jpg` |
| bag | 210 | 42 | 152 | 16 | police_modern:164, sfx_human_movement:16 | `pixabay_extra__i_1022327__bag-pink-fashion-style-beauty-ornament-ms-woman-bag-bag-bag.png` |
| hands | 210 | 178 | 32 | 0 | hands_and_transactions:61, courtroom_justice:47 | `ia__0555-master-hands-18-27-28-00__master-hands.mp4` |
| sky clouds | 210 | 143 | 67 | 0 | landscapes_timelapse:139, small_town:20 | `pixabay_extra__v_107211__nature-landscape-cross-sky-clouds-light-effects-mountain-sum.mp4` |
| post | 209 | 11 | 195 | 3 | space_nasa:54, small_town:51 | `loc__2006675203__photographs-of-the-old-post-office-and-u-s-courthouse-300-we.tif` |
| netherlands | 209 | 183 | 26 | 0 | police_modern:63, small_town:43 | `nara__77741-219251798__princess-juliana-of-the-netherlands-christens-ss-jan-pieters.mp4` |
| research | 209 | 24 | 185 | 0 | science_tech:170, space_nasa:13 | `nasa__0202598__research-technology.jpg` |
| locomotive | 208 | 5 | 201 | 2 | americana_1930s_1970s:115, factory_manufacturing:67 | `loc__2017658617__steam-locomotive-number-4-of-the-illinois-central-railroad-c.tif` |
| orion | 207 | 6 | 201 | 0 | space_nasa:181, science_tech:24 | `nara__6487875-13191173__a-high-angle-right-side-view-of-a-p-3-orion-aircraft-in-flig.jpeg` |
| off | 206 | 85 | 101 | 20 | newspapers_printing:68, space_nasa:21 | `loc__2019631137__lobby-dennis-chavez-federal-building-a-high-rise-federal-off.tif` |
| system | 206 | 41 | 165 | 0 | space_nasa:140, science_tech:24 | `loc__08009481__a-system-of-estmating-for-foundry-work.jpg` |
| machinery | 206 | 12 | 194 | 0 | newspapers_printing:182, factory_manufacturing:14 | `loc__2006677406__wall-paper-printing-press-machinery-hall-at-the-centennial-1.tif` |
| nature animal | 206 | 51 | 155 | 0 | wildlife_animals:142, government_buildings:43 | `pixabay_extra__i_7271441__cat-park-bench-pet-nature-animal-iran-tehran-persian-cat-ben.jpg` |
| london | 205 | 34 | 164 | 7 | uk_period:39, uk_highstreet_postoffice:38 | `loc__2015646750__federal-building-and-u-s-courthouse-and-annex-london-kentuck.jpg` |
| walk | 205 | 83 | 26 | 96 | sfx_human_movement:84, courtroom_justice:47 | `freesound__558272__walk-in-dark-wind.mp3` |
| germany | 205 | 53 | 149 | 3 | government_buildings:93, courtroom_justice:14 | `loc__16002885__germany-and-england-the-real-issue.jpg` |
| hardware | 205 | 15 | 190 | 0 | retail_commerce:108, space_nasa:53 | `nasa__iss069e008883__astronaut-sultan-alneyadi-removes-physics-research-hardware.jpg` |
| fall | 204 | 70 | 130 | 4 | courtroom_justice:43, landscapes_timelapse:30 | `pixabay_extra__i_1094794__forest-bank-bench-nature-fall-leaves-resting-place-bank-tree.jpg` |
| art | 204 | 89 | 115 | 0 | textures_backgrounds:34, government_buildings:31 | `loc__2010720548__art-at-federal-building-u-s-courthouse-binghamton-new-york.jpg` |
| space ground | 204 | 204 | 0 | 0 | space_nasa:204 | `nasa__jcs2022m000004_Space_to_Ground_404_220114__space-to-ground-spacewalks-and-research-01-14-2022.mp4` |
| side | 203 | 10 | 172 | 21 | factory_manufacturing:27, japan:24 | `loc__2010718828__side-view-of-historic-courthouse-federal-building-and-u-s-co.jpg` |
| concrete | 203 | 19 | 36 | 148 | sfx_human_movement:146, textures_backgrounds:25 | `freesound__118041__concrete-stairs-wav.mp3` |
| lunar | 202 | 2 | 200 | 0 | space_nasa:186, science_tech:13 | `nasa__jsc2026e020501__lunar-flyby-in-mission-control.jpg` |
| fallow | 202 | 10 | 192 | 0 | wildlife_animals:202 | `pixabay_extra__i_1092458__white-fallow-deer-antler-nature-forest-fallow-deer-lying.jpg` |
| summit | 201 | 5 | 196 | 0 | landscapes_timelapse:172, japan:21 | `loc__2019690539__customers-arrive-at-the-summit-diner-in-the-borough-as-penns.tif` |
| government | 201 | 28 | 173 | 0 | government_buildings:171, factory_manufacturing:7 | `loc__26026104__courses-for-the-training-of-apprentices-in-the-government-pr.jpg` |
| training | 200 | 51 | 149 | 0 | space_nasa:100, war_history:20 | `loc__15017063__wage-worth-of-school-training-an-analytical-study-of-six-hun.jpg` |

## 3. Known name-vs-content traps

| source | trap |
|---|---|
| noaa | Titles are survey codes (`20260130aC0894545w340345n`). Nothing about the frame is knowable from the name — must be eyeballed. |
| nypl | 27k scans share the title `new-york-city-directory`; the subject index cannot separate them. Treat as page scans, not footage. |
| ia | Real titles, but talking-head lectures/podcasts pass the relevance gate (measured 4/24 on the courtroom_justice sheet). Check before staging. |
| factory (older shelf) | Filenames are the SEARCH QUERY, verified ~50% wrong. Use `select_factory_assets.py` + FACTORY_SUBTYPE_INVENTORY.v001.md, never the name. |
