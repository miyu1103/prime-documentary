# Archive shelf — what it can actually supply (2026-08-09 21:39)

63,180 items / 1,552 GB across 62 themes, 16 sources.

**Read this before writing shot specs.** A theme name is the download query, not a subject — asking a shot spec for `weather_disasters` gets 358 GB of one flood survey. Search by SUBJECT (section 2), and only from rows section 1 marks `good`/`mixed`.

```
python scripts/search_archive.py --shot "courthouse exterior dusk" --kind video
python scripts/search_archive.py --shot "prison corridor" --md    # paste-ready rows
python scripts/qc_archive_contact_sheets.py --theme <theme>          # look before you trust
```

Filenames are `<source>__<id>__<title-slug>.<ext>` and 53,333/53,567 conform, but a name is NOT evidence: NOAA titles are survey codes and 27k NYPL scans all read `new-york-city-directory`. The verdicts below come from eyeballing the labeled sheets in `H:\pd-media\assets\archive\_qc\<theme>\`.

## 1. Supply and verdicts (theme x source)

| theme | source | items | GB | video/image/audio | verdict | real titles |
|---|---|---:|---:|---|---|---|
| ambience_beds | freesound | 1,067 | 4.4 | 0/0/1067 | good (8 faults in 60: six mono beds (no width under a stereo mix), one clipped, one at 22 kHz. Median 74 s. Usable with the mono ones kept for spot use) | Roomtone Bedroom Yew; Room Tone Stairs.wav; Empty Office Ambience |
| americana_1930s_1970s | met | 305 | 0.9 | 0/305/0 | unusable (all 24 tiles are Renaissance and Baroque allegory engravings. Allegory of America matched americana. The theme is US life 1930-1970; this is 16th-18th century Europe) | Allegory; Allegory of the Planets and Continents; Allegory of Virtues and Vices at the Court of Charle |
| americana_1930s_1970s | loc | 243 | 11.6 | 0/243/0 | good (American storefront, main-street and railroad photographs - strongest still source) | Main street storefronts. Edwards, Mississippi; Storefront Transom, angle 1, Main Street, Chinook, M; Storefront Transom, angle 2, Main Street, Chinook, M |
| americana_1930s_1970s | smithsonian | 19 | 0.1 | 0/19/0 | mixed (19th-c mural studies; only the Justice/Courage allegories fit) | New England Factory Life--"Bell-Time", from Harper's; New England Factory Life – "Bell-Time"; Factory at the shore. |
| americana_1930s_1970s | nara | 12 | 1.5 | 11/1/0 | good (mid-century street, railroad and civic-life motion footage) | Main Street U.S.A.; Footage of Olympic Stadium in Berlin; Bomb Damage to; [LAKE SHORE COUNTY FAIR] |
| americana_1930s_1970s | ia | 9 | 0.9 | 9/0/0 | good (period educational films and home movies; several underexposed) | Dynamic American City, The (Part II); Dynamic American City, The (Part I); [Home movie: 098550: Sausage factory in Michigan] |
| atmosphere_symbolic | pexels | 5 | 0.0 | 0/5/0 | good (clock macros, handshakes, hands - generic symbolic inserts, which is what the theme is for) | close up on hands of clock; professional handshake in business meeting; macro shot of a clock |
| audio | oyez | 5 | 0.1 | 0/0/5 | good (Supreme Court oral argument in Terry, Kelo, Carpenter, Riley and Timbs - primary source audio for cases this channel covers. The measurement tool first graded it unusable at 100% by applying a music-bed floor: 22 kHz mono is how the Court itself distributes these. Three of the five do exceed 0 dBFS and need a limiter) | Carpenter oral argument; Kelo oral argument; Riley oral argument |
| bank_and_branch | wikimedia | 474 | 3.6 | 0/474/0 | good (bank buildings, branch facades and one historic teller hall - the only source actually supplying banks) | File:HK WTSD 樂富廣場 Lok Fu Place mall shop Standard Ch; File:HK SKD TKO Po Lam Tsui Lam Estate Square Shoppi; File:HK 港島 南區 Southern District 黃竹坑 Wong Chuk Hang 香 |
| bank_and_branch | coverr | 2 | 0.0 | 2/0/0 | good (2 items only, cafe cash-handling close-ups; generic transaction inserts, not bank interiors) | premium a customer pays barista with cash; close up of barista taking money from a customer |
| bench_to_line | mixkit | 45 | 1.3 | 45/0/0 | mixed (a real spine of welding, robotics and packaging diluted by fashion, fitness and motivational-businessman stock) | Metal drawer in a garage with tools; Model turns to pose as a photographer takes photos i; White flowers in the breeze |
| bench_to_line | ia | 2 | 0.3 | 2/0/0 | good (2 items, both the 1936 Chevrolet plant film Master Hands - best-matched material but corporate-attributable) | Master Hands |
| bench_to_line | coverr | 1 | 0.0 | 1/0/0 | good (1 item, gloved hands grinding metal; carries a legible metabo tool brand) | angle grinder on metal |
| bgm_general | freesound | 381 | 1.8 | 0/0/381 | good (1 fault in 60 (a mono pad). Median 91 s, all CC0. The cleanest audio block on the shelf) | Eerie Horror Nature Atmosphere SFX; Granular Dark and Brilliant Ambient Background Textu; Relax Dark Wind Ambient Background.wav |
| business_corporate | pixabay_extra | 766 | 4.5 | 236/530/0 | mixed (architecture tiles are fine, polluted with 3D icon art and animal wallpapers; 4 of 9 missing on disk) | discussion, desk, people, office, team, meeting, bus; handshake, greeting, deal, hello, thanks, trust, wel; design, marketing, business |
| business_corporate | mixkit | 88 | 1.7 | 88/0/0 | mixed (competent but heavily acted handshakes and meeting reenactments; a quarter is lifestyle filler) | Business people at work meeting; Men in black shirts shake hands at business meetng; A man is presenting a business report |
| business_corporate | unsplash | 50 | 0.1 | 0/50/0 | good (empty, unbranded, well-lit boardrooms and towers that carry narration without asserting a specific company) | oval brown wooden conference table and chairs inside; long table with Eiffel chair inside room; beige wooden conference table |
| business_corporate | coverr | 3 | 0.0 | 3/0/0 | good (3 items, two of them the same Lisbon facade - effectively two distinct shots) | premium skyscrapers viewed through a glass roof; a glass building in lisbon; a glass building on lisbon street |
| chicago_city | nara | 18 | 1.5 | 9/9/0 | good (skyline stills, lakefront aerials, parade and explosion-damage newsreel) | Chicago riots, Chicago, Illinois; FIRST DIVISION CIRCUS AT CHICAGO; Apollo 11 Chicago Parade and Ceremony in Civic Cente |
| chicago_city | ia | 2 | 0.4 | 2/0/0 | good (2 items: World's Fair home movie and 1968 riot footage) | [Home Movies: Chicago World's Fair]; Chicago riots, Chicago, Illinois (1968) |
| civic_voting | pexels | 3 | 0.0 | 0/3/0 | mixed (three items: two US flags and a street protest. Usable, but nothing depicting voting) | protesters on the street; us a flag on pole under blue sky; flag blowing in the wind |
| courtroom_justice | pixabay_extra | 1,550 | 17.2 | 624/926/0 | unusable (bench collides with PARK BENCH - 11 of 24 tiles are park benches; the rest is a wolf, a cartoon dog on green screen, roses, a fan and hand cream. Zero courtroom material) | courthouse, building, government, architecture, law,; belgium, castle, architecture, palace, building, for; judge, 2d character, gavel, law, justice, vector art |
| courtroom_justice | loc | 1,144 | 47.0 | 0/1144/0 | good (HABS/GSA courthouse exteriors, lobbies, empty courtrooms - instantly cuttable) | [Orange County Government Center, Goshen, New York. ; [Orange County Government Center, Goshen, New York. ; Interior courtroom, William J. Nealon Federal Buildi |
| courtroom_justice | nara | 173 | 20.7 | 127/46/0 | mixed (WWII war-crimes tribunal reels, diluted by leaders and document cards) | British Courtroom; Black Panther; Crown Prince Olaf and Princess Martha of Norway at R |
| courtroom_justice | mixkit | 159 | 3.1 | 159/0/0 | unusable (walking and library dominate: 9 tiles of people walking on beaches, pavements and campuses, 8 of general (not law) libraries, and a green-lit ghost nun. Two tiles are legal - a lawyers' meeting and a contract signature) | Judge Shows Money on Table; The scales of justice; Judge pronounces sentence in court |
| courtroom_justice | ia | 109 | 31.9 | 109/0/0 | mixed (mostly talking-head public-access programs; only the Nuremberg reels are cuttable) | Disorder in the Court; Cross Examination; WITNESS FOR THE PROSECUTION trailer |
| courtroom_justice | unsplash | 50 | 0.3 | 0/50/0 | good (22 of 24 tiles are American courthouses - historic clock towers, classical porticos, federal buildings - and one is a real empty courtroom in wood panelling at 14467x5736. Prime PD material) | Ornate courtroom with gilded decorations and chandel; Empty ornate courtroom interior with wooden paneling; Empty courtroom featuring rich wooden paneling and a |
| courtroom_justice | coverr | 1 | 0.0 | 1/0/0 | unusable (one item, titled walking to the mountain top, and it is a mountain) | walking to the mountain top |
| crime_police | pexels | 7 | 0.0 | 0/7/0 | good (police car at night, jail interior, a prisoner walking into a cell, handcuffs under blue light. Note legible force liveries - NYPD and Royal Newfoundland Constabulary) | police car on the street; interior of jail; prisoner walking into cell |
| decision_rooms | wikimedia | 159 | 1.6 | 0/159/0 | good (real company offices and period labour photography, though it skews to unions and strikes rather than boardrooms) | File:JB Pritker on labor unions DBqb3aoWAAAANlo.jpg; File:Emblem of Guild of Trade Unions of Afghanistan ; File:RMT (trade union) logo.png |
| decision_rooms | unsplash | 50 | 0.1 | 0/50/0 | mixed (document-and-desk tiles are useful; failures are word-game and gavel novelty shots) | Petition to File For Bankruptcy; gray scale photography of Lawyer Bankruptcy scrabble; Membership Certificate paper |
| decision_rooms | ia | 1 | 0.2 | 1/0/0 | good (1 item, a mid-century office training film - dramatised acting, never cut as actuality) | New Girl in the Office, The |
| depression_hardship | wikimedia | 183 | 1.7 | 0/183/0 | mixed (1,598 of 1,688 items yet 6 of 9 sampled tiles missing on disk; the two that render are paper scans) | File:Bowery bread line LCCN2014683026.jpg; File:Bowery men waiting for bread in bread line, (Ne; File:Bowery men waiting for bread in bread line, New |
| depression_hardship | loc | 85 | 1.9 | 0/85/0 | mixed (the backbone - FSA sharecropper cabins, porches, relief scenes - but four in ten tiles are book covers, charts or drawings) | Free coffee at Bowery Mission for unemployed; The problem of the unemployed.; Swollen fortunes and the problems of the unemployed |
| depression_hardship | nara | 5 | 0.5 | 4/1/0 | mixed (five tiles, four carrying the identical CCC title - one programme reel sliced up, low diversity) | Civilian Conservation Corps; AN Army relief team carries an Army tent in a box to |
| documents_paper | pexels | 4 | 0.0 | 0/4/0 | good (library shelves and hands signing documents, including a divorce decree and a contract) | cozy library bookshelves with ladder; person signing in documentation paper; a person signing divorce documents |
| economy_crisis | pixabay_extra | 695 | 4.7 | 205/490/0 | mixed (4 of 7 tiles missing on disk and a Dubai waterfront pulled in on the word mall - the visual opposite of crisis) | mall, shop, store, department store, people, busy, b; online, shopping, cart, mobile, digital, internet, s; supermarket, cart, market, mall, buy, retail, buyer, |
| economy_crisis | wikimedia | 122 | 1.2 | 0/122/0 | good (highest-yield source, but six of eleven tiles are the same Slovakian plant - repeat-footage hazard) | File:Abandoned factory interior (31260792602).jpg; File:Alliance Brick abandoned factory, Darlington.jp; File:Research Of An Abandoned Factory (232886655).jp |
| economy_crisis | mixkit | 56 | 1.4 | 56/0/0 | mixed (half usable crowds and malls; a missile launch and abstract renders are off-theme) | Pairs of shoes in a department store display; Busy mall escalator timelapse; Young woman browsing at clothes in a store |
| economy_crisis | unsplash | 50 | 0.2 | 0/50/0 | good (every tile a real storefront or sign, roughly half literal closure notices - the most directly on-theme cluster reviewed) | a store front with a variety of items in the window; brown and red wooden store; Corbett building supply store with boarded windows |
| economy_crisis | ia | 1 | 0.1 | 1/0/0 | good (1 item, period industrial actuality; it is editorial film, so avoid producer captions) | America Marching On: A Screen Editorial With Lowell |
| factory_manufacturing | wikimedia | 2,197 | 30.0 | 0/2197/0 | good (HABS/HAER survey photography of mills, foundries and works; 5 of 14 sampled tiles missing on disk) | File:Assembly line) Vicker Sons & Maxim Gun Factory ; File:Ford assembly line in Copenhagen 1923.jpg; File:Underwood Typewriter Assembly 1962.jpg |
| factory_manufacturing | loc | 167 | 3.6 | 0/167/0 | mixed (barely clears mixed: dominated by digitised trade-book covers, union newspaper pages and expense tables) | United automobile worker (Detroit, Mich.), June 5, 1; United automobile worker (Detroit, Mich.), January 2; United automobile worker (Detroit, Mich.), October 3 |
| factory_manufacturing | nara | 38 | 5.1 | 35/3/0 | good (period industrial reels of the Rouge, foundries and steel - the strongest source here) | [FORD MOTOR COMPANY AUTOMOBILE ASSEMBLY LINES]; Ford Automobile Assembly Line / Ford Automobile Serv; [FORD ASSEMBLY LINES AND AUTOMOBILE TESTING] |
| finance_money | pexels | 3 | 0.0 | 0/3/0 | good (banknotes of several denominations, dollar bills, hands exchanging cash - exactly the currency inserts Prime Finance asks for) | banknotes of different denominations cash dolors; paper dollar bills; hands exchanging dollars |
| finance_money | wikimedia | 1 | 0.0 | 0/1/0 | good (one item, a clean scan of a US one-dollar bill) | US one-dollar bill |
| forensics_dna | pexels | 1 | 0.0 | 0/1/0 | good (one item, a modern fingerprint access-control terminal) | modern fingerprint access control system |
| goods_in_motion | pixabay_extra | 845 | 13.0 | 357/488/0 | mixed (largest source at 3,145 items and only 40%: loading returned a loading bar, shipping returned a cruise ship) | warehouse, bogota, colombia; finland, porvoo, borg, old, wooden warehouse, villag; containers, cargo, shipping shipping, freight, port, |
| goods_in_motion | wikimedia | 597 | 5.9 | 0/597/0 | good (grain handling and rail survey photography; one WWII internment-camp file shows the category is broader than the theme) | File:Camouflage Design for Cargo Ship - NARA - 69971; File:Cargo ship 2.png; File:Cargo ship 3.png |
| goods_in_motion | mixkit | 72 | 1.6 | 72/0/0 | good (cleanest source: ports, trucks, cranes and delivery, only two lifestyle clips out of place) | View of a forklift driver operating in a warehouse; A large warehouse stored with wheat ready for shipme; Warehouse area on a coastline in a general shot |
| goods_in_motion | unsplash | 50 | 0.2 | 0/50/0 | mixed (splits into genuine warehouse footage and a block of blank-paper desk flat-lays) | a computer keyboard sitting on top of a wooden table; A receipt sitting on top of a wooden table; white printer paper on brown wooden table |
| government_buildings | pixabay_extra | 2,252 | 29.4 | 923/1329/0 | unusable (4 animated national-flag wallpapers, a football stadium, an aquatic seal (the word seal), a hiking signpost (courts); the real architecture is European and Middle Eastern, almost no US civic building) | austin, capitol, building, texas, architecture, usa,; austin, capitol, building, texas, architecture, usa,; austin, capitol, building, texas, architecture, usa, |
| government_buildings | nara | 618 | 4.1 | 15/603/0 | mixed (large slice is Federal Hall planning paperwork and microfilm cards) | DAWN STRIKES THE CAPITOL DOME; WEAVING STRAW, SEOUL ; SEOUL ; CAPITOL BUILDING, PYO; National Aeronautics and Space Administration-Astron |
| government_buildings | ia | 280 | 137.6 | 280/0/0 | mixed (half genuine mid-century film, half partisan citizen-journalist uploads) | Government Workers; [Home Movies: Kansas City to Natchez]; [Home Movies: Washington & Gettysburg] |
| government_buildings | loc | 123 | 1.1 | 0/123/0 | good (high-res Supreme Court and Capitol exteriors plus period prints) | Supreme Court Building, Washington, D.C.; U.S. Supreme Court building, Washington, D.C.; United States Capitol |
| government_buildings | unsplash | 50 | 0.2 | 0/50/0 | good (23 of 24 are the US Capitol, state capitols, the National Archives, the Statue of Freedom and a rotunda interior, up to 9324x6216. One foreign (Serbian constitutional court)) | the dome of the u s capitol building with a statue o; the ceiling of the dome of the us capitol building; United states capitol building under dramatic sky |
| government_buildings | mixkit | 42 | 1.0 | 42/0/0 | unusable (12 of 24 tiles are national FLAGS - Colombia, Brazil, Thailand, the Philippines, China, India, Spain, a pirate flag - and 6 more are generic city skylines. Three tiles are on theme) | Corporate and business buildings in the city.; Buildings under construction, aerial view; Panoramic view of Manhattan buildings |
| government_buildings | coverr | 1 | 0.0 | 1/0/0 | mixed (one item, flags on a skyscraper - a flag shot, not a government building) | flags on a skyscraper |
| hands_and_transactions | mixkit | 597 | 14.2 | 597/0/0 | mixed (only 5 of 16 tiles show work or money changing hands; the rest is coffee-shop lifestyle, sport and gaming) | Silhouette of a hand being held up in front of the s; Hand touching wheat in golden sunset; Electronics assembly line |
| household_loss | unsplash | 50 | 0.2 | 0/50/0 | good (real doors, windows, notices and ordinary houses that cut straight into a foreclosure sequence) | Teal double doors with "bonjour" sign above; A metal door covered in various posters and notices.; Illuminated "exit to the city" sign above a brown do |
| household_loss | wikimedia | 14 | 0.1 | 0/14/0 | mixed (archival boarded-up and foreclosure-sale material is excellent; six tiles are press-conference photography) | File:VIEW DOWN RIVER STREET TO THE EAST FROM THE INT; File:Cash payment timeline on foreclosures.jpg; File:Enright foreclosure notice in The Jersey Journa |
| household_loss | coverr | 1 | 0.0 | 1/0/0 | good (1 item only - provisional verdict, an old man at a window, restrained and on-theme) | an old man looking out of the window |
| japan | pixabay_extra | 1,620 | 24.1 | 476/1144/0 | good (genuine Japan temples, streets and Fuji with some foreign mountain leakage) | shrine, torii, japan, fushimi, nature, temple, kyoto; kyoto, japan, statue, jizo, buddha purnima, japanese; street, puddles, rain, pubs, lights, night, tokyo, j |
| japan | nara | 530 | 11.0 | 53/477/0 | mixed (genuine WWII Japan archival plus unrelated modern US Marine photos) | Physical Damage, Okayama, Japan; Japanese aggression in China and activities in Japan; News Events, Japan 1946 |
| japan | mixkit | 89 | 1.1 | 89/0/0 | good (Japanese motion footage; temple keyword dragged in Turkey, Malaysia and Egypt) | Time lapse of a street and mount Fuji; Tokyo Night street with fast traffic and tower; Tokyo cityscape at night |
| japan | unsplash | 50 | 0.3 | 0/50/0 | good (temples, pagodas and neon streets - cleanest source in this theme) | narrow japanese street at night; people near pagoda under white and blue sky; red temple near body of water |
| japan | ia | 16 | 1.9 | 16/0/0 | mixed (genuine WWII-era US government film on Japan - Tokyo ruins 1945, Kyoto damage, kamikaze ceremony, Japanese newsreels. But The Enemy Japan is wartime propaganda, one carries a Prelinger card, and several sampled frames are title cards) | The Enemy Japan--The People; Children of Japan; News Events, Japan 1946: November 1945 - June 1, 194 |
| japan | loc | 15 | 0.7 | 0/15/0 | good (high-resolution archival plates, readable only since the TIF fix: USS West Virginia burning at Pearl Harbor, San Pedro California April 1942, Yokohama woodblock prints, a map of Japan. Two need framing - Enemy Japan is an Office of War Information pamphlet, and the San Pedro photographs document Japanese-American exclusion) | [Untitled photo, possibly related to: Corner of Mont; Pearl Harbor, Hawaii. USS West Virginia aflame.  Dis; Japan, |
| laboratory_forensics | noaa | 9 | 0.0 | 0/9/0 | unusable (laboratory matched the Aquarius UNDERSEA HABITAT: divers, reef structures, a NOAA logo PNG, lenticular clouds and a staff portrait. No forensic laboratory at all) | NOAA Earth System Research Laboratory aircraft; Lenticular clouds in Boulder CO - NOAA Earth System ; National Severe Storms Laboratory logo mid-90s |
| laboratory_forensics | ia | 5 | 0.6 | 5/0/0 | unusable (two of the seven items are COVID conspiracy broadcasts (Stew Peters / Carrie Madej, a test kit under a microscope) and are now quarantined. The five that remain are a Yucca Mountain film, a chemistry series, an antibiotics reel, a sonic boom test and a 1945 Navy mess hall - none is forensics) | Yucca Mountain: The Making of an Underground Laborat; Chemistry - Challenges and Solutions ★ "Lost" Annenb; Science in Action: Antibiotics |
| laboratory_forensics | smithsonian | 1 | 0.0 | 0/1/0 | unusable (one item, a museum model of the Mars Science Laboratory rover) | Model, Mars Science Laboratory, Mars Rover Curiosity |
| landscapes_timelapse | pixabay_extra | 1,766 | 29.0 | 667/1099/0 | good (waterfalls, peaks and skies - on-theme but visually interchangeable) | dolomites, mountains, snow, time lapse, clouds, wint; sunrise, fog, clouds, landscape, mountain range, alp; clouds, stars, full moon, night sky, light, mood, la |
| landscapes_timelapse | mixkit | 123 | 4.9 | 123/0/0 | good (aerials and cloud or valley timelapses) | Fog on the heights of the snowy mountains; Flying over an arid land with the sun shining over t; Flying over a landscape of sun soaked desert land wi |
| landscapes_timelapse | nasa | 67 | 0.2 | 0/67/0 | mixed (glacier collided with GLACIER, the ISS freezer locker: seven of 24 tiles are astronauts working a rack inside the station. The other 17 are real satellite landscape stills - Lena Delta, Malaspina, Pine Island, the Namib. No timelapse in it) | Earth observation taken by the Expedition 28 crew; Two-Orbit Time Lapse Earth Observation taken with a ; Earth from Orbit 2014 |
| landscapes_timelapse | unsplash | 50 | 0.2 | 0/50/0 | good (high-res landscape stills, heavy on mountains) | aerial photo of mountains during daytime; a person standing on top of a mountain at sunset; Snow-capped mountains bathed in golden sunlight |
| landscapes_timelapse | coverr | 9 | 0.1 | 9/0/0 | good (most PD-relevant: Manhattan and Washington DC timelapses) | timelapse of a house in the mountains; pink sunset timelapse; timelapse of a sunset |
| landscapes_timelapse | ia | 6 | 0.5 | 6/0/0 | good (2 items, clean low-res timelapses) | Timelapse sky; Timelapse of pasture at sunset; Juuson Turha Video Diary - Clouds 26h timelapse |
| legal_court | pexels | 10 | 0.0 | 0/10/0 | good (the Capitol, the Supreme Court facade and frieze, a Lady Justice statue and a wooden courthouse interior - small but every tile on brief) | wooden interior of a courthouse; corner of capitol in washington dc; us capitol in washington dc |
| legal_court | wikimedia | 2 | 0.1 | 0/2/0 | good (seen in full: a judge's gavel and page 1 of the US Constitution. Both on brief - supersedes an earlier mixed call made before the tiles were rendered) | judge's gavel; US Constitution page 1 |
| market_machinery | mixkit | 52 | 1.1 | 52/0/0 | mixed (half real mechanisms and infrastructure, half keyword collisions on machinery plus staged corporate performance) | Woman scrolling the web on a tablet; A man lying on the bed scrolling on his phone; Investor scrolling through an investment app on a ta |
| market_machinery | unsplash | 50 | 0.2 | 0/50/0 | good (real mechanical calculating hardware, punch cards, split-flap clocks and numeral displays) | Rows of vintage punched cards with data; a large number of numbers are arranged in rows; Antique dark green mechanical calculating machine on |
| market_machinery | coverr | 8 | 0.1 | 8/0/0 | good (8 items, tightly on-brief: trading desks, phones and chart screens) | a trader making a call with his smartphone; financial analysis of cryptocurrency; crypto wallet |
| medical_lab | pexels | 2 | 0.0 | 0/2/0 | good (two items, both real laboratory hardware: a centrifuge loaded by gloved hands and a sample rack in an XN-1000 analyser) | laboratory worker using modern hospital equipment; test tubes in a medical equipment |
| misc | pixabay | 106 | 0.3 | 35/71/0 | good (Capitol, Supreme Court, cash, cuffs; a few non-US police clips) | untitled |
| misc | pexels | 57 | 0.5 | 36/21/0 | good (clean modern b-roll: money, justice props, jail bars - interchangeable stock) | black cars on road; people walking at the park during sunset; yellow and white currency strap |
| misc | wikimedia | 3 | 0.1 | 0/3/0 | good (3 items, all core: RBG and Roberts portraits, Bill of Rights parchment) | Bill of Rights parchment; RBG official portrait; CJ Roberts official portrait |
| money_banking | pixabay_extra | 1,490 | 20.4 | 953/537/0 | mixed (generic money stills diluted by wildlife, green screens and lifestyle) | currency, dollars, euro, money, symbol, commerce, ba; cards, coins, gambling, game, money, currency, finan; board, chalk, finance, graphic, diagram, training, s |
| money_banking | wikimedia | 435 | 6.7 | 0/435/0 | mixed (strong US Treasury Building record and colonial paper money, but 9 of 24 tiles are GOLD MINING - placer claims, mining-company share certificates, a route map to the Colorado gold region. That is the word gold, not banking) | File:Chip gold bullion bar.jpg; File:Gold bullion 1.jpg; File:Gold bullion bars.jpg |
| money_banking | nara | 211 | 3.1 | 3/208/0 | mixed (Treasury Relief Art Project interiors plus bank false positives such as lighting rigs) | [STOCK NEWSREEL EXCERPTS]; Looking West at Conduit Bank North of Service Equipm; LOAD BANK |
| money_banking | mixkit | 134 | 2.3 | 134/0/0 | good (clean modern money and finance motion - most directly droppable) | Money counting machine counting up money; Close up to a counting money machine; Man counting a wad of bills seen very closely |
| money_banking | loc | 117 | 3.5 | 0/117/0 | good (19 of 24 tiles are real bank buildings - Freedman's Bank, Dime Bank Detroit, the 1900 Burlington Savings Bank, an abandoned 1915 branch, the US Treasury - at up to 13150x10199. This is the bank exterior material Prime Finance was recorded as lacking) | The old Central Gas Station building in Donaldsonvil; P.S. Duval's Lithographic Establishment and Office o; The neoclassical-style, onetime First National Bank |
| money_banking | unsplash | 50 | 0.2 | 0/50/0 | good (high-res currency stills, very repetitive) | a lot of money sitting on top of a green surface; 1 US dollar banknote; 100 us dollar bill |
| money_banking | ia | 10 | 1.2 | 10/0/0 | good (mid-century educational banking films - strong period b-roll) | Using the Bank; Two Dollar Bettor; What Is Money? |
| money_banking | coverr | 6 | 0.1 | 6/0/0 | mixed (four trading-screen clips are exactly what Prime Finance wants; the other two are supermarket aisles, and one carries a large coverr watermark) | a screen showing financial analysis of a cryptocurre; a broker working with a candlestick chart; a broker works with a cryptocurrency candlestick cha |
| music_performance_pd_era | ia | 2 | 0.7 | 2/0/0 | unusable (six of eight items are actively owned and were tagged pd or cc0 in the ledger: two Wiggles TV episodes, three ABC For Kids concerts and a Nintendo compilation. All six quarantined. Two possibly-genuine PD films remain) | Command Performance; Music In Motion |
| nature_landscape | pexels | 1 | 0.0 | 0/1/0 | unusable (one item, and it is people rallying in the street - filed under nature) | people rallying on the street |
| navy_harbor | nara | 478 | 26.8 | 194/284/0 | good (ship decks, harbors, Pearl Harbor damage, crew activity - directly cuttable) | FRENCH SHIPS IN HARBOR & UNDERWAY; JAPANESE SHIPS AWAIT "PEARL HARBOR"; Japanese SHIPS AT KURE HARBOR |
| navy_harbor | loc | 144 | 1.5 | 0/144/0 | mixed (harbor pulled in an entire run of The Islander, a Friday Harbor local paper - 16 of 24 tiles are newspaper pages and congressional letters. Four real naval-yard photographs (Philadelphia, Pearl Harbor) are worth reaching by direct search) | The islander (Friday Harbor, Wash.), June 17, 1897; The San Juan islander (Friday Harbor, Wash.), August; The San Juan islander (Friday Harbor, Wash.), August |
| navy_harbor | ia | 88 | 5.9 | 88/0/0 | good (real newsreel harbor footage, diluted by the Don Winslow fiction serial) | Don Winslow of the Navy: Chapter 1 - The Human Torpe; Don Winslow of the Navy: Chapter 2 - Flaming Death; 1942 Captured Japanese Newsreel: Pearl Harbor, Hong |
| newspapers_printing | pixabay_extra | 1,007 | 9.5 | 399/608/0 | unusable (press collides with hay baler, bench press, coffee press, excavator and bulldozer; about 5 of 24 usable (typewriters, one old press) plus a CGI figure and an AI anime illustration) | press ups, boy, sports, sweating, crunches, leisure,; hang clean, kettlebell press, kettlebell, kettlebell; newspaper, cat, bird, peace, tolerance, information, |
| newspapers_printing | loc | 164 | 3.6 | 0/164/0 | mixed (excellent pressroom, linotype and newsboy photography plus dead-weight book covers and page scans) | Paul and the printing press,; Specimens of druggists' labels...letter-press printi; The Centennial -- wall paper printing press, Machine |
| newspapers_printing | unsplash | 50 | 0.2 | 0/50/0 | good (old flatbed presses, newspaper stacks, ink on plates, industrial print halls. Watch the mastheads: several are legible and foreign - Klettgauer Bote, Evening Standard, Irish Examiner, Persian dailies) | Antique printing press machine on a white background; Vintage printing press in a factory setting.; Antique linotype printing machine on a white backgro |
| newspapers_printing | mixkit | 46 | 0.9 | 46/0/0 | unusable (running (as in the press runs) collides with PEOPLE RUNNING - 12 of 24 are joggers, running tracks and athletes; 8 more are typing on laptops. Two tiles are on theme) | Burning a newspaper in a campfire; Young adult reading the newspaper; Person reading the newspaper in a park outdoors |
| newspapers_printing | ia | 11 | 1.1 | 11/0/0 | mixed (tiny pool of mid-century industrial films; modern uploads out of focus) | Printing; ADVANCED NEWSPAPER TECHNOLOGY; Media Smart - Part 12 - Roll the Presses! Newspaper |
| newspapers_printing | nara | 6 | 0.6 | 6/0/0 | unusable (8 items, essentially none show printing - keyword false positives) | SOME OF UNCLE SAM"S WORKSHOPS [U.S. POST OFFICE DEPA; FORD RIVER ROUGE PLANT; [PLANT SAFETY] |
| ocean_nature | pixabay_extra | 2,110 | 72.3 | 969/1141/0 | good (reef life and coastline stills; reef shots repetitive) | beach, ocean, sea, summer, holiday, wave, nature, be; waves, water, sea, ocean, landscape, nature, sunset,; wave, sea, water, sky, power, ocean waves |
| ocean_nature | noaa | 148 | 0.6 | 1/147/0 | good (genuine underwater reef and diver photography, unlike the satellite plates elsewhere) | Mimic goatfish coral reef Howland Island 2023; NOAA diver lays transect on reef Tutuila 2023; NOAA diver measures coral Rose Atoll 2023 |
| ocean_nature | nasa | 132 | 0.6 | 0/132/0 | mixed (about 40% is genuine ocean and ice - the Larsen Ice Shelf, phytoplankton blooms, the Great Barrier Reef, a Coast Guard cutter in pack ice. The rest is six Artemis-1 motor arrivals in a Kennedy Space Center assembly hall and five data charts) | KENNEDY SPACE CENTER, FLA.  -   Purple flowers flow ; Ocean Inside Saturn Moon Enceladus; Typhoon Neoguri is pictured in the Pacific Ocean |
| ocean_nature | mixkit | 56 | 1.9 | 56/0/0 | good (ocean motion: surf, reef fish, coastal boats) | Sea waves breaking on the rocks, front view; Aerial view of long running wave crashing onto shore; Waves reaching the shore |
| ocean_nature | unsplash | 50 | 0.2 | 0/50/0 | good (high-res underwater and open-water stills) | bird's-eye view of sea waves; aerial photography of large body of water and shorel; sea waves during daytime photo |
| ocean_nature | coverr | 24 | 0.2 | 24/0/0 | good (coastal aerials, but 5 of 8 are the same Praia do Pinhao location) | the incoming waves of the ocean gently splash onto t; premium couple observes ocean waves; sandstone cliffs |
| ocean_nature | ia | 14 | 0.9 | 14/0/0 | mixed (2 items; one carries a clideo.com watermark) | Hills and the Sea; Ocean Wave; Venice Beach Ocean Waves Ashley Gershoony Video |
| pd_feature_films | ia | 277 | 137.5 | 277/0/0 | mixed (PD-claimed noir features with the right period texture, but each needs shot-logging and title-by-title rights clearance; several are not actually PD) | The Killers (1946) Burt Lancaster, Ava Gardner, Edmo; Spellbound (1945) Director: Alfred Hitchcock Starrin; Kiss Me Deadly (1955, ) Dir: Robert Aldrich Featurin |
| period_telephone_tech | loc | 57 | 0.2 | 0/57/0 | unusable (telegraph matched the newspaper NAMES Washington Telegraph and American Telegraph - 23 of 24 tiles are their pages, plus rate tables and book covers. One real photograph: a Spanish-American war telegraph room) | Masters of space: Morse and the telegraph; Thompson ; Letter from J. Sitzenstatter to Alexander Graham Bel; Investigation of telephone companies. Letter from th |
| period_telephone_tech | ia | 15 | 2.1 | 15/0/0 | mixed (Bell-style instructional films; a third land on intertitles or notice cards) | Town and the Telephone, The; Communication: A Film Lesson in General Science / De; Operator Toll Dialing: Teamwork |
| period_telephone_tech | nara | 15 | 1.5 | 10/5/0 | good (genuine switchboard and operator photographs - most on-theme in the set) | Number Please (Telephone Switchboard) / Lumbering; THE TELEPHONE SECTION; [TELEPHONE AND TELEGRAPH COMMUNICATIONS] |
| police_modern | pixabay_extra | 1,442 | 22.1 | 600/842/0 | mixed (real cruisers mixed with Lego toys, AI renders, generic night wallpaper) | night, city, cars, road, lights; futuristic, robots, android, guardian, police, patro; steampunk, guardian, police, patrol, vehicle, futuri |
| police_modern | mixkit | 86 | 2.1 | 86/0/0 | good (staged crime-scene and forensic clips that cut as narrative b-roll) | Police barricade tape at a crime scene; Handcuffed man walking to a police car; Blurry lights form a police car |
| police_modern | unsplash | 50 | 0.2 | 0/50/0 | good (modern patrol-car photography, night and rain - ideal establishing b-roll) | Police cars parked with flashing lights at night.; A police car with its lights on at night; a police car driving down a street at night |
| police_modern | ia | 3 | 0.0 | 3/0/0 | unusable (4 items, none belong: classic features and a screen-recorded agenda) | Monday, 2nd June 1913 Frank Asked Room to Conceal Bo; Monday, 28th April 1913 Police Think Negro Watchman ; Tuesday, 3rd June 1913 Grand Jury Calls for Thos. Fe |
| police_modern | coverr | 1 | 0.0 | 1/0/0 | mixed (one item, a traffic light timer. Usable as a city insert, not as policing) | traffic light timer |
| police_period | loc | 194 | 5.4 | 0/194/0 | good (pre-war police stations, squad cars, troop portraits, station interiors) | Police station, Belle Isle; [The Imperial Police Station, Papasköprüsü]; [The Imperial Police Station, Nişantaşı] |
| police_period | nara | 69 | 2.1 | 18/51/0 | unusable (almost entirely 2006 Iraq police-training and 2012 FEMA photos mislabeled as period) | RADIO TRAFFIC & SAFETY PATROLS (JOINT PATROLS AMERIC; [YOUR STATE POLICE]; PATROL IN LEIPZIG RR STATION, GERMANY ; US 26TH DIVI |
| police_period | ia | 2 | 0.3 | 2/0/0 | mixed (2 items only: one period educational film, one unrelated TV comedy) | Youth and the Law; 56 11 18 The Jack Benny Program S 07e 05 Beverly Hil |
| prison_jail | pixabay_extra | 1,489 | 13.2 | 416/1073/0 | unusable (a laid dinner table, a neon heart, a mussel dish, a girl in daffodils, the Doge's Palace; roughly 6 of 24 usable (razor wire, barred window, handcuffs) and one tile is tagged ai generated) | fence, thorny, razor blade, sharp, barrier, anger, m; attorney, justice, law, legal, face, cell, arrested,; watchtower, guarding, prison, fence, barbedwire, war |
| prison_jail | ia | 114 | 26.0 | 114/0/0 | mixed (half genuine prison film; rest screen recordings, cartoons, game capture) | Prison Mutiny; Prison Shadows; Back Door to Heaven |
| prison_jail | loc | 79 | 0.1 | 0/79/0 | unusable (dominated by scanned Prison Mirror newspaper pages and government letters) | Cell blocks at Occoquan [Workhouse]; Prisons and prison systems of the United States. Let; Military prisons. Letter from the Secretary of War, |
| prison_jail | unsplash | 27 | 0.1 | 0/27/0 | good (18 of 20 are real prisons - cell blocks, spiral staircases, Alcatraz, barred windows, abandoned brick wings. Among the strongest PD material on the shelf) | Long row of weathered prison cell bars in a corridor; Dark, narrow hallway with bright, barred skylights.; A long hallway with prison cells on the left |
| prison_jail | nara | 20 | 2.0 | 17/3/0 | unusable (Leavenworth inmate case files: forms and mugshots of named prisoners) | JAPANESE PRISON CAMPS (273-X); Prison Ship is Wrecked / Laying Lighthouse Cornersto; Rioting Felons Damage Prison in 8-Hour Row |
| prison_jail | mixkit | 18 | 0.3 | 18/0/0 | unusable (seen in full on the shared sheet: about 6 of 20 are usable and four of those are the same man-behind-a-wire-fence setup. The rest is 3D blood-cell animation, solar panels, a birthday cake, a metal furnace door and boats in Saint Petersburg. Supersedes an earlier mixed call made from two tiles) | A shirtless man with metal chain behind the fence; Angry prisoner behind a wire fence; Hand on a wire fence by night |
| property_home | pexels | 5 | 0.0 | 1/4/0 | good (suburban houses, one with a FOR SALE sign, and a demolition site. One tile is a remote worker and is mislabelled) | suburban house for sale; brown and white wooden house; suburban house with double garage and greenery |
| retail_commerce | wikimedia | 930 | 10.8 | 0/930/0 | mixed (half the sample is bare department-store logo files; the real photographs nearly all carry a legible shop name) | File:Edward's Department Store Logo.png; File:Forbes & Wallace Department Store Final Logo.pn; File:Frederick & Nelson Department Store Final Logo. |
| retail_commerce | nara | 13 | 0.2 | 1/12/0 | mixed (a few excellent period window displays against Independence NHP paperwork and repeated off-theme naval frames) | Futuristic Department Store; Civil Defense Window Display at Sage Allen Departmen; American Red Cross - War Work - War Activities in Du |
| retail_commerce | loc | 5 | 0.0 | 0/5/0 | unusable (almost entirely paper: regulations, annual reports and book pages, one usable building photograph) | Annual reports of the Post-Office Department for the; Rules and regulations governing the Department of th; Rules and regulations governing the Department of th |
| school_youth | pexels | 2 | 0.0 | 0/2/0 | mixed (two items; usable, but the classroom tile shows students in hoodies branded for a named international school) | students attending class at international school; students walking in school corridor |
| science_tech | nasa | 1,562 | 8.1 | 0/1562/0 | good (mission control rooms, wind tunnel consoles, ISS interiors, launch control, all public domain and 2048x1536 to 8256x5504. Note it is aerospace, not general science, and several tiles are portraits of named NASA staff) | Wind Tunnel Test of Stoppable Rotors in Ames 40x80ft; AVROCAR tested in the NASA Ames 40x80ft Wind Tunnel; Nacelles and props in 40x80 foot wind tunnel at Ames |
| science_tech | pixabay_extra | 1,382 | 14.7 | 683/699/0 | good (circuit-board macros, telescopes, retro computers, office clips) | television, monitor, telecommunication system, scree; anime, coding, programmer, desk, computer, technolog; robot, artificial intelligence, technology, develope |
| science_tech | mixkit | 99 | 1.6 | 99/0/0 | good (data centers, robots, labs; three green-screen or screen-capture plates) | Close up of electronic circuit board; Automated machine places parts on circuit boards; Robot working in an electronics manufacturing facili |
| science_tech | unsplash | 50 | 0.2 | 0/50/0 | good (high-res circuit-board macros and vintage computers) | close up of dark blue circuit board; a close-up of a circuit board; tilt-shift photography of green computer motherboard |
| science_tech | smithsonian | 45 | 0.1 | 0/45/0 | good (19th-c telegraph and instrument artifacts - narrow but excellent) | Microscope; Microscope, Lerebours; Microscope Case |
| science_tech | noaa | 7 | 0.5 | 0/7/0 | mixed (good field and instrument photography plus near-duplicate satellite frames) | PHOTO-IMETs-launch-weather-balloon-2023-IMET-trainin; Weather Balloon release; Smoke Balloons from Chemical Fire in Southeast Texas |
| science_tech | ia | 4 | 0.5 | 4/0/0 | mixed (1 item: UNIVAC commercial, advertising rights unverified) | Classic TV Commercial for a UNIVAC computer; UNIVAC Computer Commercials in 3D; Threads of Technology |
| science_tech | met | 1 | 0.0 | 0/1/0 | good (1 item: celestial globe) | Celestial globe with clockwork |
| selling_floor | pixabay_extra | 537 | 5.3 | 228/309/0 | mixed (largest source and least verifiable: 6 of 9 sampled tiles missing on disk, two carrying pure landscape keywords) | tailor, clothing, fashion designer, tailor shop; tailor, clothing, folding, shirt, shop, textiles, cl; kid, teenager, shopping, 3d, sale, cartoon, boy, man |
| selling_floor | unsplash | 50 | 0.2 | 0/50/0 | good (strong and low-risk closure signage, but 13 of 14 tiles are a CLOSED or SALE sign - no more than two per film) | Busy shopping arcade with escalators and people.; Grand interior of a department store with multiple l; Mannequins display clothing in a well-lit retail sto |
| selling_floor | mixkit | 44 | 0.9 | 44/0/0 | mixed (good unbranded merchandise close-ups alongside fog, football, models and staged retail actors) | T-shirts on hangers at fashion store; Clothing store panning; Sweaters hanging on the coat rack of a clothing stor |
| selling_floor | coverr | 3 | 0.0 | 3/0/0 | good (3 items, real observational queue footage; every one contains a live shop fascia and pedestrian faces) | socially distanced queue; queue to carrefour market in paris; queue to a newspaper store |
| sfx_environment | freesound | 2,819 | 14.9 | 0/0/2819 | mixed (12 in 60: eight are mono, which is the wrong shape for an ambience bed, and three exceed full scale (fire crackle peaks at +3.6 dBFS). Median 128 s) | Distant Thunder and Rain from Half Open Window 2.aif; Distant Thunder and Rain from Half Open Window 1.aif; thunder.rumble.ogg |
| sfx_human_movement | freesound | 2,739 | 1.9 | 0/0/2739 | good (7 in 60, all marginal clipping (peak -0.08 to +0.36 dBFS). Median 18 s. Footsteps, doors, cloth) | Footsteps in Factory Hall on Wood and Concrete.wav; Footsteps on concrete; footsteps boots int walk through melted ice on concr |
| sfx_mechanical | freesound | 1,629 | 2.1 | 0/0/1629 | mixed (15 in 60, thirteen of them clipped - a camera click and a metal lid both peak above 0 dBFS. Short transients clip easily; check before laying under narration) | Creaking Door #3; Creaking Door #2; DOOR CREAKS CLOSES 2.wav |
| small_town | pixabay_extra | 1,177 | 19.7 | 473/704/0 | mixed (town-square scraping filled it with European and Latin American squares) | san antonio, urban, pedestrians, riverwalk, people, ; broadway, street, new york, crossing, usa, america, ; las vegas, usa, america, vegas, nevada, street, city |
| small_town | loc | 404 | 23.7 | 0/404/0 | good (large-format main-street and courthouse-square photographs - exactly what PD needs) | Main street of Bourne, ghost mining town. Oregon; Main street of old mining town. Leadville, Colorado; Building on main street, Halifax, North Carolina |
| small_town | unsplash | 50 | 0.2 | 0/50/0 | good (modern American small-town streets and aerials) | Small building with trees and cloudy sky; Sunny covered walkway with pillars, storefronts, and; Quiet town street with buildings, traffic signals, a |
| small_town | nara | 49 | 1.0 | 6/43/0 | unusable (park-service survey paperwork and microfilm catalogue cards) | Mine Town / Freighter / Child Playing; INFANTRY MOVES, HAULOVICE (?) CZECHOSLOVAKIA ; 105MM; New York City Harbor and Bridges / Buffalo Bill Cody |
| small_town | ia | 24 | 4.3 | 24/0/0 | good (mid-century social and educational films giving period Americana) | Social Class in America; Poverty in Rural America; America's Funniest Home Videos - Season 19 |
| space_nasa | nasa | 9,449 | 362.4 | 630/8819/0 | good (orbital Earth-observation stills plus launch, pad and hardware photography) | Weighing in on the Dumbbell Nebula; Planetary Nebula; Trifid Nebula |
| space_nasa | ia | 66 | 9.3 | 66/0/0 | unusable (2 items, both fiction entertainment mislabeled pd) | Teenagers from Outer Space; Evil Brain From Outer Space; Attack from Space |
| space_nasa | smithsonian | 12 | 0.0 | 0/12/0 | good (rocket-hardware artifact stills, all one visual register) | Spacecraft, New Horizons, Mock-up, model; Rocket Engine, Liquid Fuel, Navajo Missile; Rocket Engine, Liquid Fuel, Apollo Lunar Module Asce |
| stock_market_exchange | wikimedia | 452 | 4.7 | 0/452/0 | mixed (excellent exchange buildings and period Wall Street against an equal pile of scanned share certificates; 10 of 35 sampled tiles missing on disk) | File:Brussels Stock Exchange (1).jpg; File:Brussels Stock Exchange (2).jpg; File:Brussels Stock Exchange (3).jpg |
| stock_market_exchange | nara | 1 | 0.2 | 1/0/0 | unusable (single item, sampled frame is pure black, license review_required) | [STOCK NEWSREEL EXCERPTS] |
| surveillance_tech | pexels | 11 | 0.0 | 2/9/0 | mixed (the CCTV masts, data-centre racks and cell tower are good; the phone-screen tiles carry legible Instagram, Twitter, Pinterest and Snapchat marks) | social media apps on smartphone; man holding a smart phone with a photo; surveillance cameras in city |
| textures_backgrounds | smithsonian | 575 | 1.6 | 0/575/0 | good (pattern engravings and porcelain; some frames show page edges) | Repeating Pattern Designs for Borders; Design for Embroidery Pattern; Design for Emrboidery Pattern |
| textures_backgrounds | pixabay_extra | 461 | 15.2 | 461/0/0 | good (smoke, bokeh, fluid-ink and abstract light loops - overlay grade) | slow, beautiful wallpaper, yellow, abstract, macro, ; ink, abstract, art, wave, fog, smoke, blue, pink, wa; paints, water, watercolor, painting, ink, texture, l |
| textures_backgrounds | mixkit | 148 | 6.0 | 148/0/0 | good (smoke, ink and bokeh motion textures; two stylized character clips) | Black ink on white background; Black background with smoke foreground; White smoke with black background |
| textures_backgrounds | unsplash | 50 | 0.3 | 0/50/0 | good (large-format concrete, paper and parchment grounds - best behaved source) | white and black marble surface; weathered teal concrete wall texture; a close up of a black marble surface |
| textures_backgrounds | met | 19 | 0.1 | 0/19/0 | good (textile and object scans; one frame has a colour chart) | Embroidery Pattern with Seven Six-pointed Stars and ; Nose ornament in the shape of a head; Pectoral Disc Ornament |
| textures_backgrounds | coverr | 2 | 0.0 | 2/0/0 | good (2 items, both bokeh light loops) | blurred christmas lights; hookah lights |
| textures_backgrounds | ia | 1 | 0.1 | 1/0/0 | good (1 item: 1950s industrial film) | Industry on Parade: Paperman's Paper, Ink Inc., Use |
| uk_highstreet_postoffice | loc | 73 | 1.0 | 0/73/0 | unusable (London matched the Madison County Democrat of LONDON, OHIO - 11 of 24 tiles are that newspaper. 23 of 24 are printed pages; the one photograph is a street in Woodstock, Vermont) | Possibilities of the Post Office. February 23, 1901.; Post-office appropriation bill. May 2, 1898. -- Orde; Pacific Mail Steamship Company. May 19, 1874. -- Rec |
| uk_period | loc | 76 | 0.4 | 0/76/0 | unusable (the same London/Ohio collision - 13 of 24 tiles are the Madison County Democrat of London, OHIO. The rest are blank book spines. No British period photography at all) | Madison County Democrat (London, Ohio), March 13, 19; Madison County Democrat (London, Ohio), October 16, ; Madison County Democrat (London, Ohio), July 31, 195 |
| uk_period | nara | 41 | 2.5 | 17/24/0 | unusable (only 23% genuine British; rest is New England Bowling League newsletters and French/Belgian cards) | THE BOMBING OF LONDON; V-E Day, Paris and London, 1945; MISC SCENES, LONDON, ENGLAND, WALES |
| uk_period | ia | 1 | 0.4 | 1/0/0 | good (1 item: steam-railway film, sample too small for confidence) | ' Reflections On Western Steam Vol 2. Through The Ch |
| urban_night | pexels | 5 | 0.0 | 0/5/0 | good (city streets at night, a Miami highway, a crowded crossing. One office-meeting tile is mislabelled) | street in toyohashi city japan at night; crowded city street with diverse group of people; cars on miami highway during daytime |
| vintage_ads_cartoons | ia | 104 | 16.3 | 104/0/0 | unusable (about three quarters is ripped third-party studio animation and off-air 1990s breaks; only ~9 tiles are genuine period live-action ads) | Fifties Advertising: UNIVAC Computer Commercial (5 F; Classic Commercial for Du Mont Laboratories Televisi; A 5th Classic Commercial for Coca-Cola (20/January/1 |
| war_history | nara | 1,227 | 43.9 | 263/964/0 | mixed (genuine WWII/Korea/Vietnam combat film; a third is caption cards and near-black leader) | USS TIRANTE COMBAT FILM; USS TIRANTE (SS-420) COMBAT FILM; GSAP Combat Film |
| war_history | ia | 229 | 19.9 | 229/0/0 | mixed (genuine WWII newsreel and War Department film, on subject - but nearly every item is 640x360 and licensed review_required (Universal, Movietone, UFA). Usable only where SD is an accepted look; check rights per item) | Why We Fight: Prelude to War; Universal Newsreel Volume 35, Release 2, 01/01/1962; Universal Newsreel Volume 36, Release 96, 11/24/1963 |
| war_history | loc | 2 | 0.2 | 0/2/0 | good (2 items, both large clean archival stills) | Troops of the 185th Inf., 40th Div., take cover behi; Production. M-4 tanks. Hull members of an M-4 tank o |
| weather_disasters | nasa | 199 | 1.6 | 0/199/0 | mixed (about half is genuine hurricane satellite imagery (Typhoon Maysak, Irma, Matthew); the rest is Kennedy Space Center facility work filed under the storm's name, plus two press briefings with named NASA staff) | Hurricane Matthew from Space; A view of Hurricane Hilary from space; RapidScat and Hurricane Patricia |
| weather_disasters | noaa | 39 | 0.2 | 39/0/0 | unusable (32/44 tiles are featureless top-down flood-survey plates; 85-90% dead weight as b-roll) | Clear skies reveal tornado scar in Mississippi (CIRA; Destructive Tornado in Southern Michigan (CIRA 2026-; Destructive Tornado in Southern Michigan (CIRA 2026- |
| weather_disasters | ia | 21 | 1.9 | 21/0/0 | good (4 items, all shootable: archival disaster films and 8K GOES timelapses) | Satellite time lapse, GOES-E 2021-07 8K UHD, Hurrica; Satellite time lapse, GOES-E 2021-08 8K UHD, Hurrica; Shock Troops of Disaster: The Story of the New Engla |
| wildlife_animals | pixabay_extra | 2,439 | 47.9 | 1019/1420/0 | mixed (technically clean but 1280x853 - too low-res for the 4K pipeline, heavy deer duplication) | cranes, flock of birds, nature, animals, birds, wild; birds, nest, flock, forest, wildlife, animals, natur; crows, beautiful wallpaper, birds, wildlife, animal, |
| wildlife_animals | noaa | 327 | 1.3 | 1/326/0 | good (public-domain marine-sanctuary photography, archival grade) | Humpback whale Fournier Bay Robert Pitman NOAA PS9; North Pacific right whale (Eubalaena japonica) - Joh; Rice's whale close to surface |
| wildlife_animals | smithsonian | 99 | 0.1 | 0/99/0 | mixed (two-thirds contamination from butterfly matching non-animals) | The Butterfly; Butterfly over Water; Butterfly |
| wildlife_animals | mixkit | 76 | 1.3 | 76/0/0 | good (real animal motion, but most clips are 1280x720) | Deer looking at the camera in the forest; Herd of deer in the forest; Pair of brown bears in the field |
| wildlife_animals | unsplash | 50 | 0.2 | 0/50/0 | good (highest-res stills on the shelf, but 8 of 9 tiles are the same deer) | brown deer under tree; red and gray deer; deer on grass field photography |
| wildlife_animals | met | 3 | 0.0 | 0/3/0 | mixed (3 items, two are antiquities that matched on horse) | Study of a Bird; Horses Harnessed to a Chariot; Tympanum with a Horse and Rider |
| wildlife_animals | ia | 2 | 0.2 | 2/0/0 | mixed (two items: a spruce hen film and a title card reading OUR WILDLIFE RESOURCES. Genuine but peripheral to all three channels) | King Spruce Hen puts on a show for the largest flock; OUR WILDLIFE RESOURCES |
| world_cities | pixabay_extra | 1,336 | 20.8 | 573/763/0 | good (clean city stills and skylines from many countries) | dubai, architecture, city, building, uae, tourism, t; blood moon, lunar eclipse, hyperlapse, seoul citysca; night, harbour, people, car, automobile, city, urban |
| world_cities | mixkit | 128 | 5.3 | 128/0/0 | good (aerials, traffic plates and city timelapses - the motion supply) | Side by side aerial view of a city at night; Aerial view of the glass corporate buildings of a bi; Quiet Tokyo street at night |
| world_cities | nara | 76 | 3.0 | 24/52/0 | mixed (half archival city film, half scanned park-service paperwork) | [TRAFFIC]; MERRILY WE ROLL ALONG [COUNTRY AND CITY SCENES]; Automobile-Train Wreck / Parkway Traffic / Automobil |
| world_cities | unsplash | 50 | 0.2 | 0/50/0 | good (night skylines and street-level views; several very dark) | aerial city view; full moon over city skyline during night time; a city skyline at night |
| world_cities | coverr | 6 | 0.1 | 6/0/0 | good (street-level video: pedestrians, signals, US road plates) | cars in the city at night; street in mexico city; timelapse of buenos aires |
| world_cities | ia | 3 | 0.4 | 3/0/0 | good (1 item: sepia period film) | Wonderful World; Big City, 1958; New York City Scenics |

## 2a. MOVING FOOTAGE by subject — 350 subjects with >= 3 clips

This is the scarce resource. Take stills only when no clip exists.

| subject | clips | top themes (clips only) | example clip |
|---|---:|---|---|
| nature | 1643 | wildlife_animals:454, landscapes_timelapse:382 | `mixkit__41575__traveling-on-a-nature-road-at-dusk.mp4` |
| sea | 1061 | ocean_nature:746, landscapes_timelapse:88 | `ia__0991-hills-and-the-sea-01-19-57-20__hills-and-the-sea.mp4` |
| city | 1015 | world_cities:491, government_buildings:228 | `coverr__5837__cars-in-the-city-at-night.mp4` |
| ocean | 963 | ocean_nature:816, landscapes_timelapse:42 | `coverr__3079__the-incoming-waves-of-the-ocean-gently-splash-onto-the-shore.mp4` |
| landscape | 914 | landscapes_timelapse:408, japan:176 | `mixkit__52012__flying-over-a-landscape-of-sun-soaked-desert-land-with-majes.mp4` |
| water | 909 | ocean_nature:394, wildlife_animals:204 | `mixkit__45611__ocean-water-moving-calmly.mp4` |
| wildlife | 830 | wildlife_animals:773, ocean_nature:25 | `ia__33-451-r-1-2__our-wildlife-resources.mp4` |
| road | 684 | small_town:285, police_modern:169 | `ia__on-the-road-istanbul-sringar__on-the-road-istanbul-sringar.mp4` |
| sky | 553 | landscapes_timelapse:258, ocean_nature:52 | `ia__timelapsesky__timelapse-sky.mp4` |
| beach | 551 | ocean_nature:388, landscapes_timelapse:58 | `coverr__9330__eroded-cliffs-on-praia-do-pinh-o-beach.mp4` |
| sunset | 544 | landscapes_timelapse:308, ocean_nature:108 | `coverr__4178__pink-sunset-timelapse.mp4` |
| aerial | 539 | landscapes_timelapse:240, ocean_nature:92 | `ia__npc-5630__aerial-views-ww2-new-ireland-island-simpson-harbor-rapapo-ta.mp4` |
| traffic | 522 | world_cities:234, police_modern:172 | `coverr__9024__pedestrian-traffic-light.mp4` |
| forest | 510 | wildlife_animals:212, landscapes_timelapse:78 | `mixkit__10076__deer-looking-at-the-camera-in-the-forest.mp4` |
| drone | 505 | landscapes_timelapse:199, world_cities:72 | `mixkit__23688__man-working-on-repairing-drone-circuits.mp4` |
| animal | 498 | wildlife_animals:378, ocean_nature:69 | `mixkit__22013__3d-printing-a-cartoon-animal.mp4` |
| space | 493 | space_nasa:412, police_modern:21 | `ia__plan-9-from-outer-space-202009__plan-9-from-outer-space-full-movie.mp4` |
| clouds | 463 | landscapes_timelapse:328, small_town:23 | `ia__juusonturhavideodiary-clouds26htimelapse__juuson-turha-video-diary-clouds-26h-timelapse-3.mp4` |
| background | 420 | textures_backgrounds:164, money_banking:69 | `mixkit__489__black-ink-on-white-background.mp4` |
| bird | 409 | wildlife_animals:350, small_town:16 | `pixabay_extra__v_30448__hummingbird-feeder-backyard-flock-anna-s-flying-bird-wildlif.mp4` |
| money | 405 | money_banking:399, hands_and_transactions:2 | `ia__whatismo1947__what-is-money.mp4` |
| waves | 403 | ocean_nature:284, textures_backgrounds:51 | `coverr__3079__the-incoming-waves-of-the-ocean-gently-splash-onto-the-shore.mp4` |
| technology | 389 | science_tech:302, police_modern:22 | `ia__0559-threads-of-technology__threads-of-technology.mp4` |
| business | 370 | money_banking:156, business_corporate:99 | `ia__37600-201704__in-us-town-that-embraces-refugees-auto-shop-business-flouris.mp4` |
| night | 356 | world_cities:111, police_modern:58 | `coverr__5837__cars-in-the-city-at-night.mp4` |
| underwater | 356 | ocean_nature:322, textures_backgrounds:29 | `mixkit__43088__woman-swimming-underwater.mp4` |
| japan | 353 | japan:292, courtroom_justice:38 | `ia__children1941__children-of-japan.mp4` |
| street | 351 | world_cities:211, small_town:32 | `coverr__3879__street-in-mexico-city.mp4` |
| beautiful | 340 | textures_backgrounds:113, ocean_nature:87 | `mixkit__4034__beautiful-northern-lights-of-yellow-and-pink-tones.mp4` |
| coast | 331 | ocean_nature:230, landscapes_timelapse:18 | `mixkit__4078__ocean-waves-bursting-on-the-shore-of-the-coast.mp4` |
| green | 331 | money_banking:92, economy_crisis:70 | `ia__green-archer-ep1__green-archer-the-chapter-1-prison-bars-beckon.mp4` |
| abstract | 331 | textures_backgrounds:201, money_banking:64 | `mixkit__44818__abstract-video-of-a-liquid-with-dark-ink-flowing.mp4` |
| mountains | 315 | landscapes_timelapse:194, small_town:33 | `coverr__4021__timelapse-of-a-house-in-the-mountains.mp4` |
| lights | 314 | textures_backgrounds:165, police_modern:66 | `coverr__284__blurred-christmas-lights.mp4` |
| car | 304 | police_modern:175, small_town:47 | `mixkit__49329__handcuffed-man-walking-to-a-police-car.mp4` |
| computer | 302 | science_tech:258, business_corporate:24 | `ia__univac-commercial-classic-old-vintage__classic-tv-commercial-for-a-univac-computer.mp4` |
| trees | 291 | wildlife_animals:65, landscapes_timelapse:61 | `pixabay_extra__v_311415__nature-pond-lake-water-forest-trees-geese-swimming-bird-wild.mp4` |
| wallpaper | 283 | textures_backgrounds:98, ocean_nature:60 | `ia__the-lazarus-man-s-1-e-09-the-wallpaper-prison__the-lazarus-man-s1e09-the-wallpaper-prison.mp4` |
| cars | 275 | world_cities:94, police_modern:85 | `coverr__5837__cars-in-the-city-at-night.mp4` |
| travel | 274 | world_cities:61, ocean_nature:56 | `mixkit__41540__aerial-travel-above-a-highway-in-the-city.mp4` |
| wave | 271 | ocean_nature:226, textures_backgrounds:12 | `ia__ocean-wave__ocean-wave.mp4` |
| screen | 267 | money_banking:91, economy_crisis:76 | `coverr__3490__a-screen-showing-financial-analysis-of-a-cryptocurrency.mp4` |
| urban | 264 | world_cities:185, japan:14 | `mixkit__3516__urban-view-from-a-rooftop-and-the-sunset.mp4` |
| woman | 263 | hands_and_transactions:95, police_modern:38 | `ia__thewomaninthewindow1944__the-woman-in-the-window-1944-fritz-lang-edward-g-robinson-jo.mp4` |
| people | 258 | selling_floor:64, economy_crisis:47 | `coverr__9463__timelapse-of-people-near-a-cathedral.mp4` |
| mountain | 256 | landscapes_timelapse:128, japan:43 | `mixkit__52426__an-arid-natural-landscape-with-a-mountain-in-the-distance-an.mp4` |
| finance | 251 | money_banking:238, business_corporate:8 | `pixabay_extra__v_91678__cards-coins-gambling-game-money-currency-finance-casino-happ.mp4` |
| nature landscape | 251 | landscapes_timelapse:134, ocean_nature:27 | `pixabay_extra__v_198549__sky-clouds-mountains-cloudscape-drone-aerial-nature-landscap.mp4` |
| highway | 250 | small_town:131, world_cities:42 | `ia__freedomh1956__freedom-highway-part-i.mp4` |
| river | 250 | landscapes_timelapse:52, world_cities:41 | `mixkit__8097__shallow-river-flowing-through-a-canyon.mp4` |
| man | 243 | hands_and_transactions:61, business_corporate:33 | `coverr__4931__an-old-man-looking-out-of-the-window.mp4` |
| beautiful wallpaper | 237 | textures_backgrounds:93, ocean_nature:54 | `pixabay_extra__v_22909__slow-beautiful-wallpaper-yellow-abstract-macro-paint-ink-liq.mp4` |
| sea ocean | 235 | ocean_nature:186, landscapes_timelapse:19 | `pixabay_extra__v_22183__waves-water-sea-ocean-landscape-nature-sunset-coast.mp4` |
| council | 229 | government_buildings:226, small_town:1 | `ia__city-council-05-21-2019__city-council-05-21-2019.mp4` |
| blue | 226 | ocean_nature:91, textures_backgrounds:29 | `ia__thebluegardenia1953__the-blue-gardenia-1953-dir-fritz-lang-featuring-anne-baxter.mp4` |
| bokeh | 219 | textures_backgrounds:196, world_cities:11 | `mixkit__45355__bokeh-lights-on-a-black-background.mp4` |
| sun | 218 | landscapes_timelapse:109, ocean_nature:41 | `mixkit__52009__flying-over-an-arid-land-with-the-sun-shining-over-the-mesme.mp4` |
| smoke | 218 | textures_backgrounds:200, money_banking:8 | `mixkit__1968__black-background-with-smoke-foreground.mp4` |
| ground | 217 | space_nasa:205, wildlife_animals:2 | `nasa__jsc2020m000053_Space_to_Ground_352_201223__space-to-ground-the-year-that-was-12-23-2020.mp4` |
| wild | 217 | wildlife_animals:179, ocean_nature:10 | `mixkit__11059__a-herd-of-elephants-grazing-in-the-wild.mp4` |
| plumage | 216 | wildlife_animals:204, small_town:4 | `pixabay_extra__v_191159__gull-bird-snow-plumage-sitting-winter-wildlife.mp4` |
| light | 215 | textures_backgrounds:60, police_modern:32 | `mixkit__50948__a-light-trail-of-smoke-twirls-and-unfurls-over-a-dark-backgr.mp4` |
| fish | 215 | ocean_nature:190, wildlife_animals:8 | `mixkit__44868__beautiful-coral-reef-with-exotic-reef-fish.mp4` |
| ocean sea | 211 | ocean_nature:173, wildlife_animals:16 | `pixabay_extra__v_218714__beach-ocean-sea-summer-holiday-wave-nature-beautiful-beautif.mp4` |
| harbor | 209 | navy_harbor:187, goods_in_motion:9 | `ia__npc-10134__1942-captured-japanese-newsreel-pearl-harbor-hong-kong.mp4` |
| architecture | 207 | world_cities:129, japan:26 | `mixkit__3510__urban-architecture-of-a-tourist-street.mp4` |
| space ground | 204 | space_nasa:204 | `nasa__jsc2020m000053_Space_to_Ground_352_201223__space-to-ground-the-year-that-was-12-23-2020.mp4` |
| building | 203 | world_cities:71, japan:29 | `mixkit__2017__classic-old-building-in-a-city.mp4` |
| currency | 202 | money_banking:202 | `pixabay_extra__v_5433__currency-dollars-euro-money-symbol-commerce-bank-business-in.mp4` |
| reef | 201 | ocean_nature:200, wildlife_animals:1 | `ia__scuba-dive-the-coral-sea-great-barrier-reef-1989__scuba-dive-the-coral-sea-great-barrier-reef-1989.mp4` |
| motion | 199 | wildlife_animals:63, textures_backgrounds:42 | `mixkit__27133__flock-of-pigeons-on-the-street-slow-motion.mp4` |
| ink | 195 | textures_backgrounds:173, police_modern:6 | `ia__papermans-paper__industry-on-parade-paperman-s-paper-ink-inc-use-and-discard.mp4` |
| vehicle | 193 | police_modern:140, world_cities:22 | `ia__louisianasupremecourtallowsvehiclesearchesonahunch__louisiana-supreme-court-allows-vehicle-searches-on-a-hunch.mp4` |
| coral | 192 | ocean_nature:190, war_history:1 | `ia__0436-coral-wonderland-01-00-02-00__coral-wonderland.mp4` |
| city council | 191 | government_buildings:191 | `ia__city-council-05-21-2019__city-council-05-21-2019.mp4` |
| science | 190 | science_tech:126, space_nasa:32 | `ia__gov-ntis-ava20966vnb1-2__science-in-the-courtroom-program-5-basic-principles-of-epide.mp4` |
| summer | 183 | ocean_nature:63, landscapes_timelapse:33 | `pixabay_extra__v_218714__beach-ocean-sea-summer-holiday-wave-nature-beautiful-beautif.mp4` |
| office | 183 | business_corporate:78, science_tech:52 | `mixkit__914__open-office-space.mp4` |
| launch | 182 | space_nasa:180, war_history:1 | `nasa__ksc-20230507-mh-rls01-tropics-rocket-launch-rocket-lab-won-3__tropics-rocket-launch.mp4` |
| green screen | 182 | money_banking:71, economy_crisis:59 | `mixkit__48285__laptop-with-a-green-screen-slide-in.mp4` |
| sunrise | 178 | landscapes_timelapse:88, ocean_nature:30 | `coverr__9808__sunrise-at-the-beach-dock.mp4` |
| cash | 174 | money_banking:171, bank_and_branch:1 | `mixkit__47005__a-lot-of-cash-over-a-rotating-background.mp4` |
| temple | 174 | japan:173, landscapes_timelapse:1 | `mixkit__20072__kyoto-historic-temple-with-tourism.mp4` |
| time | 173 | landscapes_timelapse:74, world_cities:25 | `ia__goes-e-2021-07-8k__satellite-time-lapse-goes-e-2021-07-8k-uhd-hurricane-elsa.mp4` |
| drone aerial | 168 | landscapes_timelapse:141, ocean_nature:7 | `pixabay_extra__v_198549__sky-clouds-mountains-cloudscape-drone-aerial-nature-landscap.mp4` |
| lake | 164 | wildlife_animals:60, japan:31 | `mixkit__41398__touring-a-lake-in-nature-from-the-top.mp4` |
| deer | 164 | wildlife_animals:163, economy_crisis:1 | `mixkit__10076__deer-looking-at-the-camera-in-the-forest.mp4` |
| robot | 161 | science_tech:154, police_modern:4 | `ia__gov-ntis-ava19272__robot-reality.mp4` |
| transport | 159 | police_modern:49, small_town:38 | `ia__npc-4420__invasion-of-france-barges-landing-craft-in-transport-area-ca.mp4` |
| station | 157 | space_nasa:122, japan:8 | `ia__561118thejackbennyprograms07e05beverlyhillspolicestation__56-11-18-the-jack-benny-program-s-07e-05-beverly-hills-polic.mp4` |
| newsreel | 157 | war_history:145, navy_harbor:3 | `ia__universalnewsreelvolume35release201-01-1962__universal-newsreel-volume-35-release-2-01-01-1962.mp4` |
| netherlands | 156 | police_modern:65, small_town:50 | `nara__77741-219251798__princess-juliana-of-the-netherlands-christens-ss-jan-pieters.mp4` |
| buildings | 152 | world_cities:112, business_corporate:7 | `mixkit__49845__aerial-view-of-the-glass-corporate-buildings-of-a-big-city-a.mp4` |
| war | 151 | courtroom_justice:90, war_history:47 | `ia__adc-10018__sentencing-of-nazi-war-leaders-at-nuremberg-10-1946.mp4` |
| ship | 149 | goods_in_motion:101, ocean_nature:17 | `coverr__2381__view-of-the-ocean-from-a-cruise-ship.mp4` |
| winter | 148 | wildlife_animals:28, landscapes_timelapse:24 | `pixabay_extra__v_191159__gull-bird-snow-plumage-sitting-winter-wildlife.mp4` |
| bank | 145 | money_banking:144, ocean_nature:1 | `ia__usingthe1947__using-the-bank.mp4` |
| coffee | 145 | hands_and_transactions:93, business_corporate:16 | `mixkit__45745__close-up-shot-of-an-office-worker-sipping-on-a-coffee-at-the.mp4` |
| invasion | 145 | war_history:135, navy_harbor:9 | `ia__arc-38987__november-1943-newsreel-usmc-invasion-capture-of-tarawa-cairo.mp4` |
| snow | 144 | wildlife_animals:32, landscapes_timelapse:29 | `mixkit__7311__eagle-in-the-snow-closeup-facing-the-camera.mp4` |
| animals | 144 | wildlife_animals:84, ocean_nature:46 | `mixkit__11239__herds-of-african-animals-on-a-vast-plain.mp4` |
| opening | 138 | money_banking:79, hands_and_transactions:46 | `ia__200333-panama-pacific-international-exposition-opening-parad__panama-pacific-international-exposition-opening-parade.mp4` |
| transportation | 137 | police_modern:52, world_cities:33 | `ia__usaf-11069__japanese-transportation-equipment-04-14-1946-06-01-1946.mp4` |
| sky clouds | 136 | landscapes_timelapse:121, small_town:5 | `pixabay_extra__v_198549__sky-clouds-mountains-cloudscape-drone-aerial-nature-landscap.mp4` |
| tree | 135 | wildlife_animals:34, landscapes_timelapse:22 | `mixkit__4027__huge-argan-tree-in-the-savanna.mp4` |
| driving | 134 | police_modern:88, small_town:19 | `mixkit__4521__blonde-woman-driving-on-road.mp4` |
| futuristic | 134 | science_tech:94, police_modern:11 | `mixkit__5579__futuristic-diagrams-of-dna-scans-in-modern-lab.mp4` |
| lapse | 134 | landscapes_timelapse:70, world_cities:26 | `mixkit__4070__time-lapse-of-a-green-meadow.mp4` |
| coastline | 133 | ocean_nature:128, japan:2 | `coverr__6947__praia-do-pinh-o-coastline.mp4` |
| black | 133 | textures_backgrounds:38, hands_and_transactions:22 | `mixkit__489__black-ink-on-white-background.mp4` |
| japanese | 132 | japan:73, navy_harbor:27 | `ia__npc-10134__1942-captured-japanese-newsreel-pearl-harbor-hong-kong.mp4` |
| time lapse | 132 | landscapes_timelapse:69, world_cities:25 | `mixkit__4070__time-lapse-of-a-green-meadow.mp4` |
| skyline | 129 | world_cities:111, business_corporate:8 | `mixkit__27095__frankfurt-city-skyline-in-the-morning-aerial-view.mp4` |
| mammal | 129 | wildlife_animals:120, small_town:5 | `pixabay_extra__v_260654__zebra-nature-animal-wildlife-mammal-safari-africa-fauna-spec.mp4` |
| hands | 127 | hands_and_transactions:68, money_banking:17 | `ia__0555-master-hands-18-27-28-00__master-hands.mp4` |
| autumn | 125 | japan:32, small_town:25 | `pixabay_extra__v_82366__mountain-volcano-snow-sunset-tokyo-fuji-lake-asian-autumn-tr.mp4` |
| red | 124 | wildlife_animals:27, textures_backgrounds:18 | `ia__the-red-house__the-red-house-full-film-4k-a-haunting-1940s-thriller-with-ed.mp4` |
| timelapse | 123 | landscapes_timelapse:84, world_cities:34 | `coverr__4021__timelapse-of-a-house-in-the-mountains.mp4` |
| house | 123 | economy_crisis:47, small_town:17 | `coverr__4021__timelapse-of-a-house-in-the-mountains.mp4` |
| work | 123 | science_tech:49, business_corporate:26 | `ia__arc-38908__june-1942-newsreel-molotov-lend-lease-bomber-ferry-war-work.mp4` |
| network | 123 | science_tech:109, police_modern:6 | `mixkit__32989__virtual-network-representation.mp4` |
| white | 122 | wildlife_animals:48, textures_backgrounds:18 | `ia__gov-gsa-historic-denver__a-poem-in-marble-a-place-on-the-map-byron-r-white-u-s-courth.mp4` |
| bridge | 122 | world_cities:44, small_town:23 | `mixkit__1606__city-train-driving-under-a-bridge.mp4` |
| birds | 120 | wildlife_animals:86, landscapes_timelapse:8 | `mixkit__11120__a-flock-of-cockatoo-birds-flying-away.mp4` |
| space station | 119 | space_nasa:116, weather_disasters:2 | `nasa__Earth_Views_from_the_International_Space_Station__earth-views-from-the-international-space-station.mp4` |
| aquarium | 119 | ocean_nature:108, textures_backgrounds:5 | `pixabay_extra__v_85674__fish-aquarium-underwater-ocean-marine-coral-dive-reef-deep-s.mp4` |
| water bird | 118 | wildlife_animals:115, money_banking:2 | `pixabay_extra__v_265493__fauna-duck-water-bird-floating-splashing-swim-wing-lake-wild.mp4` |
| tropical | 117 | ocean_nature:108, money_banking:3 | `mixkit__44973__big-tropical-fish-swimming-gracefully-along-a-coral-sea-bed.mp4` |
| noir | 117 | pd_feature_films:117 | `ia__thekillers1946usafeaturingburtlancasteravagardneredmondobrie__the-killers-1946-burt-lancaster-ava-gardner-edmond-o-brien-f.mp4` |
| tokyo | 115 | japan:71, courtroom_justice:36 | `ia__kamikazeceremony__kamikaze-ceremony-pd-tokyo-way-of-life-tokyo-1945.mp4` |
| design | 115 | textures_backgrounds:33, science_tech:28 | `pixabay_extra__v_101446__art-black-light-pattern-smoke-curve-motion-texture-design-co.mp4` |
| rocks | 113 | ocean_nature:76, landscapes_timelapse:12 | `mixkit__9294__sea-waves-breaking-on-the-rocks-front-view.mp4` |
| young | 113 | hands_and_transactions:37, wildlife_animals:13 | `ia__citythatneversleeps1953usafeaturinggigyoungwilliamtalmanfilm__city-that-never-sleeps-1953-gig-young-william-talman-film-no.mp4` |
| shopping | 112 | economy_crisis:43, selling_floor:38 | `mixkit__6302__women-walking-with-shopping-bags.mp4` |
| cliff | 111 | ocean_nature:96, landscapes_timelapse:6 | `ia__cliff-erosion-threatens-to-push-california-homes-into-sea__cliff-erosion-threatens-to-push-california-homes-into-sea.mp4` |
| pattern | 111 | textures_backgrounds:84, science_tech:9 | `pixabay_extra__v_127164__pattern-smoke-liquid-black-and-white-texture-background-cove.mp4` |
| shore | 110 | ocean_nature:89, war_history:5 | `coverr__3079__the-incoming-waves-of-the-ocean-gently-splash-onto-the-shore.mp4` |
| small | 110 | small_town:59, hands_and_transactions:38 | `ia__npc-4954__huge-gasoline-fire-japanese-ships-small-craft-burn-in-harbor.mp4` |
| slow | 110 | wildlife_animals:77, money_banking:6 | `mixkit__27133__flock-of-pigeons-on-the-street-slow-motion.mp4` |
| camera | 109 | police_modern:67, ocean_nature:9 | `mixkit__1512__professional-video-camera-on-a-tripod-recording-a-talk.mp4` |
| dollar | 109 | money_banking:103, hands_and_transactions:4 | `ia__two-dollar-bettor-movie__two-dollar-bettor.mp4` |
| texture | 108 | textures_backgrounds:83, money_banking:7 | `mixkit__1205__blue-ink-texture-underwater-with-a-mirror.mp4` |
| town | 108 | world_cities:42, small_town:19 | `ia__townofthetimes__town-of-the-times.mp4` |
| marine | 108 | ocean_nature:87, goods_in_motion:7 | `ia__npc-11306__marine-naval-civilian-activities-on-okinawa-04-03-1945.mp4` |
| loop | 107 | money_banking:49, science_tech:31 | `mixkit__31534__futuristic-virtual-city-highway-loop-video.mp4` |
| nasa | 107 | space_nasa:107 | `nasa__Safe_Return_to_Earth_from_the_Space_Station_on_This_Week_NAS__safe-return-to-earth-from-the-space-station-on-this-week-nas.mp4` |
| movie | 106 | pd_feature_films:81, money_banking:9 | `ia__thekillers1946usafeaturingburtlancasteravagardneredmondobrie__the-killers-1946-burt-lancaster-ava-gardner-edmond-o-brien-f.mp4` |
| fog | 106 | landscapes_timelapse:41, textures_backgrounds:16 | `mixkit__4396__fog-on-the-heights-of-the-snowy-mountains.mp4` |
| island | 105 | ocean_nature:52, war_history:14 | `ia__npc-10988__spectators-watch-u-s-fleet-entering-harbor-aboard-ship-attac.mp4` |
| market | 104 | selling_floor:43, money_banking:41 | `coverr__3150__queue-to-carrefour-market-in-paris.mp4` |
| evening | 104 | landscapes_timelapse:37, police_modern:22 | `pixabay_extra__v_366661__drone-aerial-drone-footage-nature-landscape-summer-evening-s.mp4` |
| train | 104 | japan:40, goods_in_motion:19 | `ia__6335stopmotiontrainfilm01154900__stop-motion-train-film.mp4` |
| dark | 103 | textures_backgrounds:46, police_modern:10 | `mixkit__44818__abstract-video-of-a-liquid-with-dark-ink-flowing.mp4` |
| fire | 102 | textures_backgrounds:32, navy_harbor:10 | `ia__npc-4954__huge-gasoline-fire-japanese-ships-small-craft-burn-in-harbor.mp4` |
| flying | 102 | police_modern:27, wildlife_animals:19 | `ia__the-flying-ace-part-1__the-flying-ace-part-1-1920-all-black-cast-silent-film-1-05-5.mp4` |
| animal wildlife | 102 | wildlife_animals:95, small_town:3 | `pixabay_extra__v_12793__birds-starlings-flock-flock-of-birds-nature-animal-wildlife.mp4` |
| lion | 100 | wildlife_animals:97, world_cities:2 | `mixkit__11035__male-lion-walking-in-the-savanna.mp4` |
| holiday | 100 | ocean_nature:65, textures_backgrounds:9 | `pixabay_extra__v_218714__beach-ocean-sea-summer-holiday-wave-nature-beautiful-beautif.mp4` |
| table | 99 | science_tech:33, business_corporate:30 | `mixkit__31135__man-picking-up-100-bills-from-the-table.mp4` |
| sand | 99 | ocean_nature:63, landscapes_timelapse:7 | `pixabay_extra__v_133508__ocean-wave-sand-sea-lake-water-sky-nature.mp4` |
| desk | 99 | hands_and_transactions:36, science_tech:32 | `mixkit__47415__accountant-working-at-her-desk-with-a-calculator.mp4` |
| rain | 98 | money_banking:22, police_modern:13 | `mixkit__18218__young-woman-in-a-park-opening-her-umbrella-to-cover-herself.mp4` |
| flow | 97 | textures_backgrounds:51, goods_in_motion:10 | `mixkit__44791__abstract-flow-of-a-drop-of-pink-ink-in-a-thick-liquid.mp4` |
| coins | 97 | money_banking:64, hands_and_transactions:32 | `mixkit__33358__gray-haired-old-man-counting-a-few-coins.mp4` |
| shop | 96 | selling_floor:36, hands_and_transactions:32 | `ia__37600-201704__in-us-town-that-embraces-refugees-auto-shop-business-flouris.mp4` |
| christmas | 95 | textures_backgrounds:36, money_banking:13 | `coverr__284__blurred-christmas-lights.mp4` |
| internet | 95 | science_tech:76, business_corporate:9 | `pixabay_extra__v_17085__technology-computer-computer-science-network-internet.mp4` |
| old | 94 | world_cities:26, goods_in_motion:12 | `mixkit__4206__walking-through-ibiza-old-town.mp4` |
| wind | 93 | japan:23, landscapes_timelapse:18 | `mixkit__13293__closeup-of-japan-flag-waving-in-wind.mp4` |
| rock | 93 | ocean_nature:46, landscapes_timelapse:13 | `ia__pacific-ocean-waves-crashing-against-rock-formation__pacific-ocean-waves-crashing-against-rock-formation.mp4` |
| predator | 93 | wildlife_animals:83, world_cities:6 | `pixabay_extra__v_296464__lion-animal-wild-predator-king-majestic-powerful-wildlife-na.mp4` |
| morning | 92 | selling_floor:14, japan:12 | `ia__1913-07-27-all-in-readiness-for-franks-trial-monday-morning__sunday-27th-july-1913-all-in-readiness-for-leo-franks-trial.mp4` |
| germany | 92 | courtroom_justice:57, war_history:8 | `ia__adc-6491__munich-no-541-buchenwald-trial-dachau-germany-04-12-1947.mp4` |
| cityscape | 91 | world_cities:71, japan:6 | `mixkit__31005__beach-in-dubai-with-cityscape-in-the-background.mp4` |
| coral reef | 91 | ocean_nature:91 | `mixkit__44868__beautiful-coral-reef-with-exotic-reef-fish.mp4` |
| flock | 91 | wildlife_animals:89, landscapes_timelapse:1 | `ia__kingsprucehenputsonashowforthelargestflockweeversaw__king-spruce-hen-puts-on-a-show-for-the-largest-flock-we-ever-3.mp4` |
| artemis | 91 | space_nasa:90, japan:1 | `nasa__KSC-20221116-MH-NAS01-0001-Artemis_I_Orion_First_Imagery_of___artemis-i-orion-first-imagery-of-earth.mp4` |
| walking | 90 | wildlife_animals:33, world_cities:13 | `mixkit__11054__a-herd-of-lions-walking.mp4` |
| grass | 90 | wildlife_animals:32, landscapes_timelapse:17 | `mixkit__11053__male-lions-resting-on-the-grass.mp4` |
| port | 90 | goods_in_motion:33, government_buildings:30 | `ia__npc-4814__damage-caused-by-explosion-of-ammunition-ships-port-chicago.mp4` |
| flowers | 90 | japan:27, landscapes_timelapse:18 | `mixkit__4484__lilies-flowers-on-its-stem-slowly-opening.mp4` |
| prison | 89 | prison_jail:89 | `ia__prison-mutiny-ipod__prison-mutiny.mp4` |
| pearl | 89 | navy_harbor:87, war_history:1 | `ia__npc-10134__1942-captured-japanese-newsreel-pearl-harbor-hong-kong.mp4` |
| rocket | 88 | space_nasa:77, war_history:8 | `nara__77338-14911517__invasion-of-southern-france-landing-lcs-fires-rocket-barrage.mp4` |
| hand | 88 | hands_and_transactions:57, science_tech:7 | `mixkit__46762__silhouette-of-a-hand-being-held-up-in-front-of-the-sunlight.mp4` |
| trials | 88 | courtroom_justice:88 | `ia__adc-9927__nuremberg-trials-11-21-1945.mp4` |
| pearl harbor | 88 | navy_harbor:87, war_history:1 | `ia__npc-10134__1942-captured-japanese-newsreel-pearl-harbor-hong-kong.mp4` |
| particles | 88 | textures_backgrounds:68, science_tech:10 | `mixkit__12495__smoke-with-fluorescent-particles-on-black-background.mp4` |
| wealth | 87 | money_banking:87 | `pixabay_extra__v_122881__market-economy-trading-graph-finance-money-business-wealth-i.mp4` |
| speed | 86 | police_modern:38, world_cities:16 | `mixkit__2160__man-hitting-a-speed-ball.mp4` |
| trip | 86 | ocean_nature:39, goods_in_motion:10 | `ia__000437-202005__home-movie-000437-1940s-western-train-trip.mp4` |
| crimes | 86 | courtroom_justice:85, government_buildings:1 | `nara__20795-75843019__war-crimes-atrocity-trials-yokohama-japan.mp4` |
| field | 85 | small_town:23, landscapes_timelapse:15 | `mixkit__4071__pair-of-brown-bears-in-the-field.mp4` |
| tourism | 85 | ocean_nature:25, world_cities:20 | `pixabay_extra__v_232793__ocean-sea-waves-horizon-sky-coast-tropical-wave-kennedy-isla.mp4` |
| cute | 85 | wildlife_animals:54, small_town:18 | `pixabay_extra__v_308428__lion-cub-baby-lion-lion-cubs-playing-play-fight-wildlife-cut.mp4` |
| war crimes | 85 | courtroom_justice:85 | `nara__20795-75843019__war-crimes-atrocity-trials-yokohama-japan.mp4` |
| drenthe | 85 | police_modern:35, small_town:33 | `pixabay_extra__v_231773__deer-trees-alone-sunset-forest-woods-netherlands-drenthe-bea.mp4` |
| calm | 84 | ocean_nature:56, landscapes_timelapse:8 | `coverr__4513__calm-waves-in-an-ocean-gulf.mp4` |
| home | 84 | small_town:14, money_banking:13 | `ia__america-s-funniest-home-videos-s-19-e-01-a-musical-tribute-t__america-s-funniest-home-videos-season-19.mp4` |
| slow motion | 84 | wildlife_animals:62, hands_and_transactions:5 | `mixkit__27133__flock-of-pigeons-on-the-street-slow-motion.mp4` |
| ocean waves | 83 | ocean_nature:75, landscapes_timelapse:5 | `coverr__coverr-premium-couple-observes-ocean-waves__premium-couple-observes-ocean-waves.mp4` |
| park | 83 | world_cities:25, wildlife_animals:10 | `mixkit__16582__timelapse-of-hikers-in-a-national-park.mp4` |
| moon | 83 | space_nasa:28, world_cities:8 | `nasa__jsc2020m001449_Down_to_Earth_To_the_Moon_and_Beyond-SOCIAL__down-to-earth-to-the-moon-and-beyond.mp4` |
| art | 82 | textures_backgrounds:39, japan:9 | `pixabay_extra__v_23730__ink-abstract-art-wave-fog-smoke-blue-pink-water-paint-colors.mp4` |
| close | 81 | hands_and_transactions:21, money_banking:17 | `coverr__3270__close-up-of-barista-taking-money-from-a-customer.mp4` |
| life | 81 | ocean_nature:41, wildlife_animals:17 | `ia__010058-001__home-movie-010058-001-1931-upstate-new-york-town-life-with-f.mp4` |
| uss | 81 | navy_harbor:47, war_history:33 | `ia__npc-1126__night-action-battle-of-kula-gulf-uss-honolulu-cl-48-damage-c.mp4` |
| colorful | 81 | textures_backgrounds:30, ocean_nature:11 | `mixkit__47176__colorful-ink-swirling-through-water-against-a-dark-backgroun.mp4` |
| trees forest | 80 | landscapes_timelapse:25, small_town:21 | `pixabay_extra__v_171531__trees-forest-river-canyon-town-drone-beach-sea-water-lake-tr.mp4` |
| bombardment | 80 | war_history:79, navy_harbor:1 | `ia__arc-39003__february-march-1944-newsreel-new-air-bases-in-south-pacific.mp4` |
| phone | 79 | business_corporate:48, market_machinery:6 | `mixkit__4801__young-man-sitting-scrolling-on-his-cell-phone.mp4` |
| sea beach | 79 | ocean_nature:63, landscapes_timelapse:10 | `pixabay_extra__v_70796__waves-ocean-sea-beach-byron-bay-4k-australia-live-wallpaper.mp4` |
| data | 79 | science_tech:40, business_corporate:20 | `mixkit__23219__long-hallway-in-data-center.mp4` |
| crimes trials | 79 | courtroom_justice:79 | `nara__19879-75842785__munich-nos-211-222-war-crimes-trials-nuremberg-germany.mp4` |
| laptop | 78 | science_tech:33, hands_and_transactions:19 | `mixkit__50766__a-young-man-on-the-couch-using-the-laptop-computer.mp4` |
| rural | 78 | japan:41, small_town:26 | `mixkit__25096__rural-landscape-in-the-hills-and-a-village.mp4` |
| store | 77 | hands_and_transactions:33, money_banking:16 | `coverr__coverr-premium-shopping-for-meat-at-the-grocery-store__premium-shopping-for-meat-at-the-grocery-store.mp4` |
| cloud | 77 | landscapes_timelapse:38, japan:14 | `mixkit__48482__aerial-footage-of-cloud-topped-mountains-at-sunset.mp4` |
| working | 76 | science_tech:27, hands_and_transactions:24 | `mixkit__47258__robot-working-in-an-electronics-manufacturing-facility.mp4` |
| door | 76 | economy_crisis:36, money_banking:24 | `ia__backdoortoheaven__back-door-to-heaven.mp4` |
| international | 76 | space_nasa:66, money_banking:2 | `nasa__Earth_Views_from_the_International_Space_Station__earth-views-from-the-international-space-station.mp4` |
| training | 76 | war_history:46, business_corporate:12 | `ia__gov-archives-arc-645746__hallucination-training-film-counterguerrilla-training.mp4` |
| investment | 76 | money_banking:70, business_corporate:5 | `pixabay_extra__v_308078__stock-market-finance-trading-investment-economy-business-mon.mp4` |
| aerial drone | 76 | landscapes_timelapse:30, world_cities:18 | `pixabay_extra__v_189269__clouds-sunset-sky-nature-mountains-golden-sky-landscape-aeri.mp4` |
| outdoors | 75 | wildlife_animals:24, landscapes_timelapse:14 | `pixabay_extra__v_12793__birds-starlings-flock-flock-of-birds-nature-animal-wildlife.mp4` |
| food | 75 | selling_floor:28, textures_backgrounds:14 | `ia__arc-39115__may-1946-newsreel-uscg-postwar-food-crisis-40-wall-st-plane.mp4` |
| economy | 75 | money_banking:72, world_cities:1 | `pixabay_extra__v_308078__stock-market-finance-trading-investment-economy-business-mon.mp4` |
| cloudscape | 75 | landscapes_timelapse:74, world_cities:1 | `pixabay_extra__v_198549__sky-clouds-mountains-cloudscape-drone-aerial-nature-landscap.mp4` |
| spring | 74 | japan:25, landscapes_timelapse:10 | `mixkit__26999__mountainous-landscape-in-spring-with-cloudy-sky.mp4` |
| natural | 74 | japan:43, landscapes_timelapse:8 | `pixabay_extra__v_236928__waterfall-water-flow-japan-natural-landscape.mp4` |
| sea waves | 74 | ocean_nature:66, money_banking:2 | `mixkit__9294__sea-waves-breaking-on-the-rocks-front-view.mp4` |
| flight | 74 | wildlife_animals:25, space_nasa:10 | `mixkit__22598__passenger-waiting-for-a-flight.mp4` |
| flower | 73 | landscapes_timelapse:14, money_banking:11 | `mixkit__28834__peony-pink-flower-opening.mp4` |
| live | 72 | space_nasa:44, police_modern:7 | `nasa__KSC-20220628-VP-MMS01-0001-RocketLab_Capstone_Live_Launch_Co__rocket-lab-capstone-live-launch-coverage-rocket-views.mp4` |
| card | 72 | money_banking:43, police_modern:13 | `mixkit__42606__girl-opening-an-envelope-from-a-valentine-s-day-card.mp4` |
| automobile | 72 | police_modern:46, world_cities:9 | `ia__0960runninggearanddifferential__elements-of-the-automobile-part-i-running-gear-and-different.mp4` |
| liquid | 72 | textures_backgrounds:46, science_tech:8 | `mixkit__44818__abstract-video-of-a-liquid-with-dark-ink-flowing.mp4` |
| leaves | 71 | money_banking:21, japan:16 | `pixabay_extra__v_171978__waterfall-stream-forest-stock-trees-water-rain-leaves-bugs-b.mp4` |
| ships | 71 | navy_harbor:45, goods_in_motion:13 | `ia__npc-1733__over-turned-wrecked-ships-others-afire-pearl-harbor-12-07-19.mp4` |
| france | 71 | war_history:29, navy_harbor:13 | `ia__adc-1324a__trial-of-nazi-spies-cherbourg-france-7-8-44.mp4` |
| cartoon | 71 | selling_floor:13, science_tech:11 | `mixkit__22013__3d-printing-a-cartoon-animal.mp4` |
| landscape nature | 71 | landscapes_timelapse:32, small_town:10 | `mixkit__43161__couple-looking-at-a-landscape-in-nature.mp4` |
| big | 70 | wildlife_animals:26, world_cities:17 | `ia__gov-archives-arc-2569601__big-picture-military-justice.mp4` |
| road traffic | 70 | world_cities:28, police_modern:28 | `pixabay_extra__v_188591__street-road-traffic-night-motorcycles-cars-buses-travel-trip.mp4` |
| scenery | 70 | landscapes_timelapse:21, small_town:13 | `mixkit__15625__canyon-scenery.mp4` |
| ocean water | 70 | ocean_nature:63, landscapes_timelapse:2 | `mixkit__45611__ocean-water-moving-calmly.mp4` |
| netherlands drenthe | 70 | police_modern:31, small_town:22 | `pixabay_extra__v_231773__deer-trees-alone-sunset-forest-woods-netherlands-drenthe-bea.mp4` |
| falling | 69 | money_banking:30, economy_crisis:12 | `mixkit__47013__slow-motion-of-falling-coins.mp4` |
| boat | 69 | goods_in_motion:37, ocean_nature:12 | `mixkit__11939__harbour-pilot-boat-following-a-cargo-ship.mp4` |
| italy | 69 | war_history:18, world_cities:18 | `ia__npc-10398__giornale-luce-no-2-fascist-italy-newsreel.mp4` |
| seascape | 69 | ocean_nature:64, landscapes_timelapse:3 | `pixabay_extra__v_223461__bird-seagull-boat-ocean-sea-wildlife-water-beach-waves-seasc.mp4` |
| girl | 69 | hands_and_transactions:18, police_modern:11 | `ia__the-patchwork-girl-of-oz-1914-silent-film-noir-drama__the-patchwork-girl-of-oz-1914-silent-film-film-noir-drama.mp4` |
| counting | 69 | money_banking:65, hands_and_transactions:2 | `mixkit__45703__money-counting-machine-counting-up-money.mp4` |
| aerial landscape | 69 | landscapes_timelapse:61, japan:4 | `mixkit__1566__aerial-view-of-landscape-of-a-calm-sea-at-sunset.mp4` |
| bird plumage | 69 | wildlife_animals:66, money_banking:2 | `pixabay_extra__v_174537__gull-bird-water-bird-plumage-sitting-wildlife.mp4` |
| future | 68 | science_tech:53, space_nasa:7 | `ia__hrs14edw2175-090616__the-future-of-learning-how-technology-is-transforming-public.mp4` |
| europe | 68 | world_cities:35, money_banking:10 | `pixabay_extra__v_34309__france-paris-lion-statue-center-city-marble-metal-old-antiqu.mp4` |
| plant | 68 | factory_manufacturing:15, landscapes_timelapse:9 | `mixkit__4362__smoke-from-power-plant.mp4` |
| nuremberg | 67 | courtroom_justice:66, war_history:1 | `ia__adc-9927__nuremberg-trials-11-21-1945.mp4` |
| earth | 67 | space_nasa:30, small_town:13 | `nasa__Earth_Views_from_the_International_Space_Station__earth-views-from-the-international-space-station.mp4` |
| floor | 66 | money_banking:64, business_corporate:2 | `pixabay_extra__v_111293__meerkat-take-floor-equal-young-sweet-dirt.mp4` |
| machine | 66 | science_tech:28, money_banking:7 | `mixkit__47266__automated-machine-places-parts-on-circuit-boards.mp4` |
| dusk | 66 | landscapes_timelapse:47, world_cities:5 | `pixabay_extra__v_197802__sky-nature-sunset-clouds-landscape-mountains-dusk-drone-aeri.mp4` |
| america | 66 | small_town:54, space_nasa:3 | `ia__socialcl1957__social-class-in-america.mp4` |
| asia | 66 | japan:27, world_cities:17 | `pixabay_extra__v_44622__japan-street-tokyo-city-night-asia-japanese-travel-building.mp4` |
| dollars | 66 | money_banking:64, hands_and_transactions:2 | `ia__doubtful-dollars__doubtful-dollars.mp4` |
| electronics | 66 | science_tech:65, hands_and_transactions:1 | `mixkit__47258__robot-working-in-an-electronics-manufacturing-facility.mp4` |
| diving | 65 | ocean_nature:64, wildlife_animals:1 | `pixabay_extra__v_5270__coral-ocean-underwater-diving-scuba-reef-travel-water-tropic.mp4` |
| international space | 65 | space_nasa:65 | `nasa__Earth_Views_from_the_International_Space_Station__earth-views-from-the-international-space-station.mp4` |
| center | 64 | space_nasa:14, world_cities:11 | `mixkit__23219__long-hallway-in-data-center.mp4` |
| body | 64 | police_modern:53, hands_and_transactions:3 | `mixkit__49442__detective-examining-a-body-at-a-crime-scene.mp4` |
| landing | 64 | war_history:44, space_nasa:7 | `ia__npc-8345d__newsreel-marines-landing-ww2.mp4` |
| paint | 64 | textures_backgrounds:55, money_banking:7 | `mixkit__51424__extreme-close-up-of-the-texture-of-bright-paint-drops-on-gre.mp4` |
| blur | 64 | textures_backgrounds:32, world_cities:10 | `pixabay_extra__v_4382__liquid-lights-intro-blue-blur-beautiful-wallpaper-bokeh-abst.mp4` |
| atmosphere | 63 | landscapes_timelapse:44, space_nasa:5 | `pixabay_extra__v_236027__mountains-clouds-snow-panorama-alps-timelapse-sky-atmosphere.mp4` |
| feathers | 63 | wildlife_animals:58, small_town:3 | `pixabay_extra__v_37220__geese-animals-birds-feed-meal-feathers-nature-poultry-wing-b.mp4` |
| key | 62 | money_banking:23, economy_crisis:11 | `mixkit__21812__opening-a-door-with-a-hanging-key.mp4` |
| world | 62 | war_history:13, small_town:12 | `ia__sekigunpflpsekaisensosengentheredarmypflpdeclarationofworldw__sekigun-pflp-sekai-senso-sengen-the-red-army-pflp-declaratio.mp4` |
| gold | 62 | money_banking:39, textures_backgrounds:13 | `mixkit__30772__titan-bitcoin-gold-coins-on-a-white-background.mp4` |
| eating | 61 | hands_and_transactions:41, wildlife_animals:17 | `mixkit__26087__young-woman-eating-healthy.mp4` |
| intro | 61 | money_banking:35, textures_backgrounds:10 | `pixabay_extra__v_17531__stock-footage-stock-intro-intro-template-design-square-squar.mp4` |
| golden | 61 | landscapes_timelapse:24, hands_and_transactions:11 | `ia__themanwiththegoldenarm1955-202001__the-man-with-the-golden-arm-1955-frank-sinatra-kim-novak-fil.mp4` |
| sunlight | 61 | landscapes_timelapse:22, ocean_nature:19 | `pixabay_extra__v_189264__clouds-sky-nature-mountains-sun-sunlight-calm-sunset-landsca.mp4` |
| financial | 60 | money_banking:49, business_corporate:7 | `coverr__3490__a-screen-showing-financial-analysis-of-a-cryptocurrency.mp4` |
| modern | 60 | science_tech:12, world_cities:10 | `mixkit__5644__doctor-and-scientist-look-at-3d-brain-models-in-modern-lab.mp4` |
| scenic | 60 | landscapes_timelapse:28, small_town:9 | `pixabay_extra__v_198786__sky-clouds-cloudscape-mountains-scenic-drone-aerial-nature-l.mp4` |
| communication | 60 | science_tech:38, business_corporate:7 | `pixabay_extra__v_212818__robot-brain-computer-science-head-face-digital-communication.mp4` |
| meeting | 60 | government_buildings:44, business_corporate:5 | `ia__cityofportorfordoregon-councilmeetingapril7th2011__city-of-port-orford-oregon-council-meeting-april-7th-2011.mp4` |
| beach sea | 60 | ocean_nature:40, landscapes_timelapse:13 | `mixkit__1087__aerial-shot-of-a-beach-with-sea-waves.mp4` |
| fuji | 59 | japan:58, police_modern:1 | `mixkit__30148__time-lapse-of-a-street-and-mount-fuji.mp4` |
| animation | 59 | money_banking:16, selling_floor:8 | `mixkit__26759__negative-stock-market-indicators-3d-animation.mp4` |
| laboratory | 59 | science_tech:56, space_nasa:2 | `mixkit__4765__scientist-adjusting-equipment-in-a-laboratory.mp4` |
| swim | 59 | ocean_nature:48, wildlife_animals:8 | `mixkit__8540__clown-fish-swim-among-corals-and-seaweed.mp4` |
| reflection | 59 | ocean_nature:18, landscapes_timelapse:10 | `pixabay_extra__v_330216__ocean-sea-tropical-waves-water-sunlight-sun-reflection-under.mp4` |
| nature wildlife | 59 | wildlife_animals:53, small_town:2 | `pixabay_extra__v_67623__birds-seagull-ocean-sea-water-nature-wildlife-freedom-waves.mp4` |
| day | 58 | war_history:9, landscapes_timelapse:7 | `ia__newsoftheday1943__newsreels-news-of-the-day-1943.mp4` |
| waterfall | 58 | landscapes_timelapse:20, japan:20 | `mixkit__30502__waterfall-of-a-river-in-winter-falling-into-a-canyon.mp4` |
| abandoned | 58 | economy_crisis:49, landscapes_timelapse:2 | `mixkit__2632__abandoned-house-in-a-forest.mp4` |
| room | 57 | money_banking:13, police_modern:10 | `ia__powder-room-prison__powder-room-prison.mp4` |
| auto | 57 | police_modern:29, small_town:10 | `pixabay_extra__v_114432__auto-police-inside-patrolling-night-night-scene-city-securit.mp4` |
| construction | 57 | goods_in_motion:27, prison_jail:4 | `ia__car-000180__california-new-prison-construction-shots.mp4` |
| dna | 57 | science_tech:54, space_nasa:2 | `mixkit__5579__futuristic-diagrams-of-dna-scans-in-modern-lab.mp4` |
| sea water | 57 | ocean_nature:41, goods_in_motion:5 | `pixabay_extra__v_42543__wave-sea-water-sky-power-ocean-waves.mp4` |
| aerial nature | 57 | landscapes_timelapse:51, ocean_nature:5 | `pixabay_extra__v_198549__sky-clouds-mountains-cloudscape-drone-aerial-nature-landscap.mp4` |
| wildlife slow | 57 | wildlife_animals:56, small_town:1 | `pixabay_extra__v_126680__lioness-predator-big-cat-lion-female-dangerous-wildlife-slow.mp4` |
| air | 56 | war_history:26, landscapes_timelapse:7 | `ia__1945-04-05-air-army-invades-germany__air-army-invades-germany-1945-04-05.mp4` |
| country | 56 | small_town:25, wildlife_animals:9 | `pixabay_extra__v_177035__honduras-flag-country-symbol-latin-america-nation.mp4` |
| animal nature | 56 | wildlife_animals:48, ocean_nature:6 | `pixabay_extra__v_249466__lion-forest-trees-wilderness-outdoors-wildlife-animal-nature.mp4` |
| truck | 55 | goods_in_motion:35, small_town:6 | `mixkit__45816__yellow-dump-truck-at-a-mining-site-removing-rubble.mp4` |
| effect | 55 | textures_backgrounds:22, economy_crisis:10 | `mixkit__30__blurred-abstract-cars-lights-at-night-with-bokeh-effect.mp4` |
| group | 55 | wildlife_animals:38, hands_and_transactions:4 | `mixkit__11238__group-of-ostrich-on-a-sunny-savanna.mp4` |
| moving | 55 | hands_and_transactions:10, selling_floor:9 | `mixkit__20961__robot-with-moving-eyes.mp4` |
| public | 55 | government_buildings:40, police_modern:6 | `ia__npc-2762__1940-s-public-buildings-washington-d-c-general-scenes-ww2.mp4` |
| stars | 55 | police_modern:20, textures_backgrounds:10 | `ia__stars-in-your-eyes-1956__jimmy-clitheroe-film-stars-in-your-eyes-1956.mp4` |
| mount | 55 | japan:51, police_modern:2 | `mixkit__30148__time-lapse-of-a-street-and-mount-fuji.mp4` |
| sign | 55 | money_banking:18, small_town:9 | `pixabay_extra__v_208312__man-piggy-bank-middle-ages-3d-history-fun-sign-marketing-fin.mp4` |
| glow | 55 | textures_backgrounds:22, science_tech:9 | `pixabay_extra__v_199549__glitter-particles-glow-abstract-bokeh-bright-concept-design.mp4` |
| artificial | 55 | science_tech:47, navy_harbor:3 | `pixabay_extra__v_174086__robot-artificial-intelligence-technology-developer-tech-comp.mp4` |
| bokeh lights | 55 | textures_backgrounds:51, world_cities:3 | `mixkit__45355__bokeh-lights-on-a-black-background.mp4` |
| water nature | 55 | ocean_nature:37, wildlife_animals:5 | `pixabay_extra__v_191093__sea-storm-ocean-beach-pier-wave-sky-rain-water-nature.mp4` |
| nature animal | 55 | wildlife_animals:48, ocean_nature:4 | `pixabay_extra__v_12793__birds-starlings-flock-flock-of-birds-nature-animal-wildlife.mp4` |
| through | 54 | science_tech:6, world_cities:5 | `coverr__4214__surfing-through-the-ocean-waves.mp4` |
| dawn | 54 | landscapes_timelapse:22, world_cities:11 | `ia__dawnstrikesthecapitoldomecirca1936__dawn-strikes-the-capitol-dome-circa-1936.mp4` |
| free | 54 | money_banking:42, prison_jail:3 | `pixabay_extra__v_32345__kaleidoscope-background-loop-abstract-stock-footage-video-fr.mp4` |
| pond | 54 | wildlife_animals:33, japan:9 | `mixkit__10998__herd-of-african-elephants-in-a-pond.mp4` |
| circuit | 54 | science_tech:52, small_town:1 | `mixkit__47048__close-up-of-electronic-circuit-board.mp4` |
| worker | 54 | goods_in_motion:30, hands_and_transactions:19 | `mixkit__4705__young-worker-doing-inventory.mp4` |
| dangerous | 54 | wildlife_animals:44, world_cities:6 | `pixabay_extra__v_210072__puma-predator-dangerous-mountain-lion-wildlife.mp4` |
| bills | 54 | money_banking:41, hands_and_transactions:11 | `mixkit__18296__man-counting-a-wad-of-bills-seen-very-closely.mp4` |
| horizon | 54 | ocean_nature:25, landscapes_timelapse:17 | `pixabay_extra__v_232793__ocean-sea-waves-horizon-sky-coast-tropical-wave-kennedy-isla.mp4` |
| bitcoin | 54 | money_banking:47, hands_and_transactions:6 | `mixkit__31349__golden-bitcoin-rotating-over-dollar-bills.mp4` |
| beak | 54 | wildlife_animals:51, small_town:1 | `pixabay_extra__v_209413__birds-pigeons-flock-animals-wildlife-swarm-feed-ornithology.mp4` |
| cryptocurrency | 53 | money_banking:42, market_machinery:7 | `coverr__3490__a-screen-showing-financial-analysis-of-a-cryptocurrency.mp4` |
| storm | 53 | ocean_nature:14, weather_disasters:10 | `ia__1955-08-15-storm-havoc__storm-havoc-hurricane-kills-43-damage-15-millions-1955-08-15.mp4` |
| writing | 53 | hands_and_transactions:35, science_tech:5 | `mixkit__39855__hand-of-a-man-writing-on-a-sheet-on-a-desk.mp4` |
| railway | 53 | japan:22, goods_in_motion:19 | `mixkit__20047__tokyo-railway-station-time-lapse.mp4` |
| head | 53 | wildlife_animals:30, textures_backgrounds:5 | `pixabay_extra__v_167882__lion-predator-masculine-cats-mane-head-wildlife-big-cat.mp4` |
| cargo | 53 | goods_in_motion:35, space_nasa:10 | `mixkit__39462__warehouse-port-for-cargo-ships.mp4` |
| vietnam | 53 | world_cities:14, japan:7 | `pixabay_extra__v_211662__old-town-hoi-an-vietnam-drone-landscape.mp4` |
| road highway | 52 | small_town:39, world_cities:5 | `pixabay_extra__v_42483__road-highway-car-mountain-landscape-asphalt-sky-travel-natur.mp4` |
| tokyo japan | 52 | courtroom_justice:36, japan:16 | `nara__19941-75842799__war-crimes-trials-tokyo-japan.mp4` |
| chroma | 52 | money_banking:24, economy_crisis:11 | `pixabay_extra__v_180016__money-dollars-falling-rain-income-profit-stock-chroma-key.mp4` |
| android | 52 | science_tech:48, police_modern:3 | `pixabay_extra__v_295578__robot-technology-automation-robotics-future-android-machine.mp4` |
| bright | 51 | textures_backgrounds:32, police_modern:8 | `mixkit__51424__extreme-close-up-of-the-texture-of-bright-paint-drops-on-gre.mp4` |
| path | 51 | small_town:21, landscapes_timelapse:7 | `mixkit__32622__walking-of-a-person-on-the-path-of-a-forest.mp4` |
| etc | 51 | war_history:47, prison_jail:1 | `ia__cb-48__combat-bulletin-48-air-support-on-western-front-etc-1945.mp4` |
| board | 51 | science_tech:31, war_history:5 | `mixkit__47048__close-up-of-electronic-circuit-board.mp4` |
| person | 51 | hands_and_transactions:21, money_banking:8 | `mixkit__23168__counting-money-and-giving-it-to-another-person.mp4` |
| mount fuji | 51 | japan:50, police_modern:1 | `mixkit__30148__time-lapse-of-a-street-and-mount-fuji.mp4` |
| sale | 51 | selling_floor:36, money_banking:10 | `mixkit__25437__birds-for-sale-in-thailand.mp4` |

## 2b. Everything by subject — 350 subjects with >= 6 items

Search these words, not theme names. `themes` tells you which shelf folder holds them; `example` is a representative real file.

| subject | items | video | image | audio | top themes | example |
|---|---:|---:|---:|---:|---|---|
| file | 5,620 | 13 | 5605 | 2 | factory_manufacturing:2197, retail_commerce:930 | `loc__mss6557000804__naacp-legal-defense-and-educational-fund-records-subject-fil.jpg` |
| nature | 5,545 | 1643 | 3870 | 32 | wildlife_animals:1441, landscapes_timelapse:1247 | `pixabay_extra__i_9348003__shrine-torii-japan-fushimi-nature-temple-kyoto-fushimi-inari.jpg` |
| space | 3,462 | 493 | 2927 | 42 | space_nasa:2767, science_tech:504 | `nasa__carina-nebula__james-webb-space-telescope-nircam-image-of-the-cosmic-cliffs.png` |
| launch | 3,434 | 182 | 3251 | 1 | space_nasa:3260, science_tech:139 | `nara__45493301-45493302__liberty-bonds-public-gatherings-new-york-4th-campaign-naval.jpg` |
| city | 2,676 | 1015 | 1538 | 123 | world_cities:1149, government_buildings:288 | `loc__2006678356__photographs-of-the-federal-building-and-courthouse-in-oklaho.tif` |
| sea | 2,452 | 1061 | 1315 | 76 | ocean_nature:1716, goods_in_motion:156 | `nara__86712054-86712055__launching-an-observation-balloon-at-sea-observation-balloon.jpg` |
| water | 2,413 | 909 | 1332 | 172 | ocean_nature:889, landscapes_timelapse:301 | `loc__2021758099__an-old-tractor-sits-below-the-town-water-tower-in-funk-nebra.tif` |
| landscape | 2,313 | 914 | 1399 | 0 | landscapes_timelapse:1093, japan:440 | `nara__6516701-13311198__left-side-rear-view-medium-shot-of-a-us-marine-m198-155mm-ho.jpeg` |
| building | 2,297 | 203 | 2087 | 7 | courtroom_justice:479, money_banking:355 | `loc__2010719020__interior-courtroom-william-j-nealon-federal-building-and-u-s.jpg` |
| earth | 2,180 | 67 | 2113 | 0 | space_nasa:2125, small_town:14 | `nasa__sl4-143-4707__view-of-skylab-space-station-cluster-in-earth-orbit-from-csm.jpg` |
| ocean | 2,087 | 963 | 1007 | 117 | ocean_nature:1685, sfx_environment:115 | `loc__2017669628__they-know-much-of-the-great-land-seas-of-russia-siberia-but.tif` |
| station | 1,927 | 157 | 1752 | 18 | space_nasa:1407, small_town:118 | `loc__2016799032__police-station-belle-isle.tif` |
| street | 1,741 | 351 | 1340 | 50 | world_cities:499, small_town:220 | `loc__nc0306__polk-county-courthouse-courthouse-street-columbus-polk-count.tif` |
| forest | 1,736 | 510 | 1035 | 191 | wildlife_animals:703, landscapes_timelapse:483 | `nara__55182035-55182036__111-sc-10870-an-artilleryman-s-bunk-in-the-forest-battery-al.jpg` |
| nasa | 1,685 | 107 | 1578 | 0 | space_nasa:1449, science_tech:215 | `nasa__GSFC_20171208_Archive_e002093__nasa-explores-the-carina-nebula-by-touch.jpg` |
| expedition | 1,656 | 22 | 1634 | 0 | space_nasa:1631, science_tech:13 | `nasa__iss043e003041__earth-observation-taken-by-the-expedition-43-crew.jpg` |
| wildlife | 1,586 | 830 | 756 | 0 | wildlife_animals:1454, ocean_nature:70 | `ia__33-451-r-1-2__our-wildlife-resources.mp4` |
| night | 1,491 | 356 | 604 | 531 | sfx_environment:412, world_cities:395 | `loc__2017810669__two-policemen-on-the-main-street-saturday-night-when-all-the.tif` |
| center | 1,485 | 64 | 1419 | 2 | space_nasa:853, science_tech:355 | `loc__2009632448__orange-county-government-center-goshen-new-york-interior-cou.tif` |
| during | 1,451 | 26 | 1410 | 15 | space_nasa:401, war_history:373 | `loc__2004676670__african-american-woman-juanita-sealy-being-carried-to-police.tif` |
| animal | 1,443 | 498 | 943 | 2 | wildlife_animals:1182, ocean_nature:167 | `pixabay_extra__i_1586373__deer-fawn-young-deer-wild-bambi-fallow-deer-cub-forest-anima.jpg` |
| road | 1,356 | 684 | 621 | 51 | small_town:615, police_modern:200 | `ia__on-the-road-istanbul-sringar__on-the-road-istanbul-sringar.mp4` |
| mission | 1,307 | 49 | 1258 | 0 | space_nasa:857, science_tech:386 | `loc__98502779__free-coffee-at-bowery-mission-for-unemployed.tif` |
| international | 1,293 | 76 | 1217 | 0 | space_nasa:1211, war_history:29 | `loc__2005676128__international-exhibition-phila-pa-walter-printing-press-mach.tif` |
| space station | 1,270 | 119 | 1151 | 0 | space_nasa:1203, science_tech:58 | `nasa__sl4-143-4707__view-of-skylab-space-station-cluster-in-earth-orbit-from-csm.jpg` |
| door | 1,252 | 76 | 95 | 1081 | sfx_human_movement:1011, sfx_mechanical:62 | `freesound__407205__room-tone-small-with-door-and-window-open-to-wall-with-dista.mp3` |
| sky | 1,244 | 553 | 690 | 1 | landscapes_timelapse:379, japan:157 | `loc__2017871934__pearl-harbor-hawaii-uss-west-virginia-aflame-disregarding-th.tif` |
| county | 1,187 | 13 | 1174 | 0 | courtroom_justice:458, factory_manufacturing:357 | `loc__2009632448__orange-county-government-center-goshen-new-york-interior-cou.tif` |
| japan | 1,163 | 353 | 785 | 25 | japan:786, space_nasa:131 | `loc__18009096__japan.jpg` |
| rocket | 1,150 | 88 | 1061 | 1 | space_nasa:1087, war_history:30 | `nara__17446367-17459867__acton-air-conveying-bank-and-piping-outside-cell-13-in-the-o.jpg` |
| international space | 1,150 | 65 | 1085 | 0 | space_nasa:1150 | `nasa__iss045e013851__earth-observation-from-the-international-space-station.jpg` |
| beach | 1,108 | 551 | 417 | 140 | ocean_nature:664, sfx_environment:135 | `coverr__9330__eroded-cliffs-on-praia-do-pinh-o-beach.mp4` |
| observations | 1,070 | 2 | 1068 | 0 | space_nasa:1064, science_tech:5 | `nasa__sts075-722-013__earth-observations-taken-during-sts-75.jpg` |
| earth observations | 1,060 | 1 | 1059 | 0 | space_nasa:1059, ocean_nature:1 | `nasa__sts075-722-013__earth-observations-taken-during-sts-75.jpg` |
| river | 1,055 | 250 | 634 | 171 | factory_manufacturing:247, landscapes_timelapse:225 | `loc__pa3339__u-s-steel-duquesne-works-blast-furnace-plant-along-monongahe.tif` |
| architecture | 1,048 | 207 | 841 | 0 | world_cities:462, business_corporate:179 | `pixabay_extra__i_10333720__catania-cathedral-city-landmark-narrow-street-historic-archi.jpg` |
| store | 1,043 | 77 | 963 | 3 | retail_commerce:646, selling_floor:152 | `loc__2012645659__view-of-store-fronts-along-main-street-in-benson-arizona.tif` |
| old | 1,035 | 94 | 804 | 137 | world_cities:209, economy_crisis:181 | `loc__2019691079__one-of-dozens-of-examples-of-exemplary-public-art-and-archit.tif` |
| mountain | 1,019 | 256 | 738 | 25 | landscapes_timelapse:542, japan:275 | `loc__2005693170__barbourville-ky-knox-county-court-house-a-mountain-county-co.tif` |
| sts- | 1,004 | 1 | 1003 | 0 | space_nasa:830, science_tech:169 | `nasa__sts075-722-013__earth-observations-taken-during-sts-75.jpg` |
| observations expedition | 975 | 0 | 975 | 0 | space_nasa:975 | `nasa__iss034e039331__earth-observations-taken-by-expedition-34-crewmember.jpg` |
| bank | 967 | 145 | 820 | 2 | money_banking:514, bank_and_branch:370 | `loc__2021755736__the-old-central-gas-station-building-in-donaldsonville-a-his.tif` |
| waves | 919 | 403 | 271 | 245 | ocean_nature:533, sfx_environment:245 | `coverr__3079__the-incoming-waves-of-the-ocean-gently-splash-onto-the-shore.mp4` |
| courthouse | 908 | 14 | 894 | 0 | courtroom_justice:886, americana_1930s_1970s:13 | `loc__2010719020__interior-courtroom-william-j-nealon-federal-building-and-u-s.jpg` |
| bird | 904 | 409 | 426 | 69 | wildlife_animals:750, sfx_environment:66 | `met__453250__study-of-a-bird.jpg` |
| car | 903 | 304 | 318 | 281 | police_modern:405, sfx_mechanical:199 | `loc__2020635830__police-car-police-officers-and-onlookers.tif` |
| japanese | 898 | 132 | 764 | 2 | japan:596, space_nasa:150 | `loc__2017821634__untitled-photo-possibly-related-to-corner-of-montgomery-and.tif` |
| travel | 898 | 274 | 621 | 3 | world_cities:191, japan:130 | `loc__2020742585__the-1937-vintage-western-view-diner-and-steak-house-on-histo.tif` |
| artemis | 898 | 91 | 807 | 0 | space_nasa:851, science_tech:45 | `nasa__art002e000192__earth-from-the-perspective-of-artemis-ii.jpg` |
| office | 897 | 183 | 668 | 46 | business_corporate:343, courtroom_justice:81 | `loc__al0898__greene-county-courthouse-probate-judge-s-office-courthouse-s.tif` |
| factory | 882 | 44 | 827 | 11 | factory_manufacturing:452, economy_crisis:294 | `loc__08011463__profit-making-in-shop-and-factory-management.jpg` |
| coast | 874 | 331 | 531 | 12 | ocean_nature:637, war_history:35 | `loc__2026583309__coast-guard-national-defense-and-maritime-police-functions-m.jpg` |
| kennedy | 872 | 35 | 837 | 0 | space_nasa:654, science_tech:168 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| close | 858 | 81 | 158 | 619 | sfx_human_movement:520, sfx_environment:81 | `freesound__657357__fire-near-open-close-wav.mp3` |
| space center | 857 | 9 | 848 | 0 | space_nasa:670, science_tech:167 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| sunset | 843 | 544 | 293 | 6 | landscapes_timelapse:365, ocean_nature:142 | `coverr__4178__pink-sunset-timelapse.mp4` |
| crew | 841 | 27 | 814 | 0 | space_nasa:705, science_tech:50 | `nara__6421230-13148181__crew-members-aboard-a-foreign-warship-man-the-rails-during-t.jpeg` |
| works | 837 | 6 | 831 | 0 | factory_manufacturing:750, space_nasa:36 | `loc__pa3339__u-s-steel-duquesne-works-blast-furnace-plant-along-monongahe.tif` |
| business | 831 | 370 | 461 | 0 | business_corporate:320, money_banking:264 | `loc__afcwip001417__view-down-east-main-street-near-the-corner-of-east-main-and.jpg` |
| kennedy space | 831 | 9 | 822 | 0 | space_nasa:644, science_tech:167 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| shuttle | 827 | 1 | 826 | 0 | space_nasa:728, science_tech:86 | `nasa__sts093-704-087__earth-observations-taken-from-space-shuttle-columbia-during.jpg` |
| telescope | 814 | 9 | 805 | 0 | science_tech:704, space_nasa:103 | `nara__6374210-14831496__a-member-of-the-9th-division-artillery-uses-a-m-65-battery-c.jpeg` |
| aerial | 813 | 539 | 274 | 0 | landscapes_timelapse:243, ocean_nature:233 | `ia__npc-5630__aerial-views-ww2-new-ireland-island-simpson-harbor-rapapo-ta.mp4` |
| air | 807 | 56 | 736 | 15 | space_nasa:254, war_history:244 | `loc__ca4313__ss-keystone-state-national-defense-reserve-fleet-alameda-nav.tif` |
| artillery | 801 | 7 | 793 | 1 | war_history:790, japan:3 | `nara__789238-502238326__australia-divider-4-artillery.jpg` |
| will | 798 | 3 | 795 | 0 | space_nasa:528, science_tech:113 | `loc__2021641653__lone-pine-calif-may-1942-a-soldier-of-army-military-police-a.tif` |
| mountains | 793 | 315 | 470 | 8 | landscapes_timelapse:494, japan:106 | `loc__2021756510__a-streetside-stand-selling-mouth-watering-but-fattening-food.tif` |
| traffic | 778 | 522 | 121 | 135 | world_cities:247, police_modern:193 | `coverr__9024__pedestrian-traffic-light.mp4` |
| money | 776 | 405 | 371 | 0 | money_banking:738, bank_and_branch:21 | `ia__whatismo1947__what-is-money.mp4` |
| underwater | 775 | 356 | 414 | 5 | ocean_nature:713, textures_backgrounds:29 | `nasa__KSC-03pd2367__kennedy-space-center-fla-justin-manley-of-the-national-ocean.jpg` |
| trees | 774 | 291 | 395 | 88 | landscapes_timelapse:206, small_town:158 | `pixabay_extra__i_2897227__dolomites-mountains-alps-alpine-trees-conifers-coniferous-fo.jpg` |
| observation | 770 | 3 | 767 | 0 | space_nasa:731, science_tech:27 | `nasa__iss045e013851__earth-observation-from-the-international-space-station.jpg` |
| clouds | 766 | 463 | 303 | 0 | landscapes_timelapse:445, japan:79 | `ia__juusonturhavideodiary-clouds26htimelapse__juuson-turha-video-diary-clouds-26h-timelapse-3.mp4` |
| crewmember | 756 | 0 | 756 | 0 | space_nasa:756 | `nasa__iss034e039331__earth-observations-taken-by-expedition-34-crewmember.jpg` |
| deer | 751 | 164 | 586 | 1 | wildlife_animals:743, americana_1930s_1970s:3 | `pixabay_extra__i_1586373__deer-fawn-young-deer-wild-bambi-fallow-deer-cub-forest-anima.jpg` |
| haer | 746 | 0 | 746 | 0 | factory_manufacturing:619, goods_in_motion:105 | `wikimedia__File_PHOTOCOPY_OF_CA._1934_VIEW_OF_AUTOS_COMING_OFF_ASSEMBLY__file-photocopy-of-ca-1934-view-of-autos-coming-off-assembly.tif` |
| fla | 740 | 1 | 739 | 0 | space_nasa:569, science_tech:161 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| center fla | 734 | 0 | 734 | 0 | space_nasa:568, science_tech:160 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| expedition crewmember | 733 | 0 | 733 | 0 | space_nasa:733 | `nasa__iss034e039331__earth-observations-taken-by-expedition-34-crewmember.jpg` |
| drone | 726 | 505 | 18 | 203 | landscapes_timelapse:199, ambience_beds:172 | `mixkit__23688__man-working-on-repairing-drone-circuits.mp4` |
| earth observation | 724 | 1 | 723 | 0 | space_nasa:721, landscapes_timelapse:3 | `nasa__iss045e013851__earth-observation-from-the-international-space-station.jpg` |
| battery | 720 | 3 | 716 | 1 | war_history:690, japan:17 | `nara__6471418-12947993__an-iraqi-artillery-battery-abandoned-during-operation-desert.jpeg` |
| national | 713 | 16 | 694 | 3 | government_buildings:200, money_banking:58 | `loc__ca10005037__rules-and-regulations-for-the-government-of-the-preventive-f.jpg` |
| ship | 712 | 149 | 554 | 9 | goods_in_motion:441, japan:97 | `loc__2017692837__production-m-4-tanks-hull-members-of-an-m-4-tank-on-a-positi.tif` |
| field | 709 | 85 | 582 | 42 | war_history:459, small_town:60 | `nara__6373154-14831058__sergeant-1st-class-michael-vinson-chief-of-firing-battery-fo.jpeg` |
| background | 700 | 420 | 228 | 52 | textures_backgrounds:167, money_banking:79 | `mixkit__489__black-ink-on-white-background.mp4` |
| harbor | 699 | 209 | 489 | 1 | navy_harbor:317, japan:316 | `loc__ed-1__the-islander-friday-harbor-wash-june-17-1897.jpg` |
| blue | 691 | 226 | 459 | 6 | ocean_nature:214, money_banking:47 | `loc__2020724560__the-now-as-of-2019-blue-star-diner-along-old-u-s-highway-60.tif` |
| urban | 678 | 264 | 397 | 17 | world_cities:389, business_corporate:84 | `pixabay_extra__i_4472321__street-tower-krakow-poland-tourism-europe-urban-travel-krako.jpg` |
| town | 654 | 108 | 519 | 27 | small_town:285, world_cities:183 | `loc__2017789244__main-street-of-bourne-ghost-mining-town-oregon.tif` |
| computer | 652 | 302 | 302 | 48 | science_tech:498, business_corporate:72 | `ia__univac-commercial-classic-old-vintage__classic-tv-commercial-for-a-univac-computer.mp4` |
| coral | 650 | 192 | 457 | 1 | ocean_nature:644, navy_harbor:2 | `nasa__PIA25861__study-uses-modis-data-to-determine-belize-coral-reef-risk.jpg` |
| spacex | 649 | 34 | 615 | 0 | space_nasa:648, science_tech:1 | `nasa__iss074e0723937__a-spacex-dragon-cargo-spacecraft-departs-from-the-internatio.jpg` |
| house | 648 | 123 | 503 | 22 | police_modern:83, courtroom_justice:78 | `loc__2024785551__letter-from-the-secretary-of-war-transmitting-a-system-of-fi.jpg` |
| force | 647 | 24 | 619 | 4 | space_nasa:245, japan:132 | `loc__11003805__historical-sketch-of-the-police-service-of-hartford-from-163.jpg` |
| vehicle | 646 | 193 | 449 | 4 | police_modern:250, space_nasa:249 | `nara__6418527-13170342__a-pioneer-i-remotely-piloted-vehicle-rpv-is-readied-for-flig.jpeg` |
| interior | 639 | 16 | 570 | 53 | courtroom_justice:187, police_modern:108 | `loc__2009632448__orange-county-government-center-goshen-new-york-interior-cou.tif` |
| mill | 639 | 1 | 633 | 5 | factory_manufacturing:606, stock_market_exchange:19 | `loc__2017810761__pouring-water-on-hot-ashes-from-the-blast-furnace-bethlehem.tif` |
| open | 637 | 33 | 58 | 546 | sfx_human_movement:514, goods_in_motion:17 | `freesound__158691__distant-thunder-and-rain-from-half-open-window-2-aif.mp3` |
| day | 626 | 58 | 522 | 46 | space_nasa:290, government_buildings:64 | `loc__2017802009__interior-of-courtroom-during-trial-of-automobile-accident-ca.tif` |
| reef | 624 | 201 | 422 | 1 | ocean_nature:610, money_banking:10 | `nasa__PIA25861__study-uses-modis-data-to-determine-belize-coral-reef-risk.jpg` |
| buildings | 622 | 152 | 470 | 0 | world_cities:302, business_corporate:77 | `loc__afcwip004231__three-buildings-on-the-west-side-of-main-street-north-of-gra.jpg` |
| wood | 615 | 42 | 130 | 443 | sfx_human_movement:421, goods_in_motion:31 | `freesound__155858__footsteps-in-factory-hall-on-wood-and-concrete-wav.mp3` |
| wild | 614 | 217 | 396 | 1 | wildlife_animals:551, landscapes_timelapse:15 | `pixabay_extra__i_1586373__deer-fawn-young-deer-wild-bambi-fallow-deer-cub-forest-anima.jpg` |
| federal | 607 | 8 | 599 | 0 | courtroom_justice:428, government_buildings:87 | `loc__2010719020__interior-courtroom-william-j-nealon-federal-building-and-u-s.jpg` |
| wind | 605 | 93 | 309 | 203 | science_tech:259, sfx_environment:166 | `nara__17443346-17453348__sb-switch-in-capacitor-bank-control-in-the-10x10-foot-wind-t.jpg` |
| flight | 603 | 74 | 529 | 0 | space_nasa:300, science_tech:169 | `nara__6421353-13158235__crewmen-stand-by-on-the-flight-deck-aboard-the-battleship-us.jpeg` |
| room | 584 | 57 | 461 | 66 | police_modern:191, science_tech:112 | `loc__93515056__supreme-court-room.tif` |
| space shuttle | 584 | 1 | 583 | 0 | space_nasa:548, science_tech:25 | `nasa__sts093-704-087__earth-observations-taken-from-space-shuttle-columbia-during.jpg` |
| first | 580 | 29 | 550 | 1 | space_nasa:241, science_tech:111 | `loc__10022234__our-police-a-history-of-the-baltimore-force-from-the-first-w.jpg` |
| technology | 578 | 389 | 189 | 0 | science_tech:423, business_corporate:62 | `ia__0559-threads-of-technology__threads-of-technology.mp4` |
| temple | 569 | 174 | 376 | 19 | japan:538, ambience_beds:18 | `pixabay_extra__i_9348003__shrine-torii-japan-fushimi-nature-temple-kyoto-fushimi-inari.jpg` |
| steel | 566 | 5 | 560 | 1 | factory_manufacturing:528, business_corporate:6 | `loc__pa3339__u-s-steel-duquesne-works-blast-furnace-plant-along-monongahe.tif` |
| mount | 563 | 55 | 505 | 3 | japan:516, landscapes_timelapse:11 | `nara__6480382-13053086__the-site-of-the-new-armory-being-constructed-by-naval-mobile.jpeg` |
| washington | 560 | 15 | 545 | 0 | government_buildings:189, money_banking:144 | `loc__2011632073__supreme-court-building-washington-d-c.jpg` |
| nara | 560 | 4 | 556 | 0 | factory_manufacturing:418, depression_hardship:30 | `pixabay_extra__i_6963458__temple-night-view-yakushiji-temple-world-cultural-heritage-n.jpg` |
| green | 558 | 331 | 227 | 0 | money_banking:100, economy_crisis:73 | `ia__green-archer-ep1__green-archer-the-chapter-1-prison-bars-beckon.mp4` |
| table | 549 | 99 | 446 | 4 | police_modern:247, business_corporate:111 | `loc__2025864573__letter-of-the-secretary-of-the-interior-in-answer-to-a-resol.jpg` |
| aircraft | 546 | 18 | 528 | 0 | factory_manufacturing:333, space_nasa:45 | `loc__2017691815__women-aircraft-workers-women-man-america-s-machines-in-a-wes.tif` |
| spacecraft | 546 | 11 | 535 | 0 | space_nasa:491, science_tech:53 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| mars | 541 | 6 | 535 | 0 | space_nasa:531, science_tech:6 | `nasa__KSC-03pp2101__kennedy-space-center-fla-from-a-burst-of-fire-and-smoke-the.jpg` |
| keyboard | 537 | 38 | 78 | 421 | sfx_mechanical:421, science_tech:78 | `freesound__437631__keyboard.mp3` |
| waterfall | 537 | 58 | 427 | 52 | landscapes_timelapse:440, sfx_environment:52 | `pixabay_extra__i_5312692__waterfall-sweden-water-nature-landscape-flow-forest-bach-fjl.jpg` |
| design | 532 | 115 | 416 | 1 | textures_backgrounds:337, police_modern:67 | `met__452365__velvet-fragment-with-bird-and-flower-design.jpg` |
| red | 529 | 124 | 402 | 3 | wildlife_animals:167, space_nasa:59 | `loc__ia0068__montgomery-county-courthouse-courthouse-square-red-oak-montg.tif` |
| marine | 528 | 108 | 420 | 0 | ocean_nature:254, war_history:148 | `loc__2025876483__alaska-seal-and-fur-company-letter-from-the-secretary-of-the.jpg` |
| lights | 524 | 314 | 209 | 1 | textures_backgrounds:165, world_cities:135 | `coverr__284__blurred-christmas-lights.mp4` |
| skyline | 522 | 129 | 385 | 8 | world_cities:351, business_corporate:113 | `nara__6490754-13178018__an-aerial-port-side-view-of-the-nuclear-powered-aircraft-car.jpeg` |
| shop | 516 | 96 | 419 | 1 | retail_commerce:127, factory_manufacturing:109 | `loc__2018700911__assuming-this-streetcorner-emergency-call-box-outside-a-wig.tif` |
| nature landscape | 513 | 251 | 262 | 0 | landscapes_timelapse:283, ocean_nature:72 | `pixabay_extra__i_9247234__mountain-nature-landscape-peak-travel-forest-outdoors-summit.jpg` |
| fish | 511 | 215 | 295 | 1 | ocean_nature:438, science_tech:24 | `nasa__KSC-03pd2367__kennedy-space-center-fla-justin-manley-of-the-national-ocean.jpg` |
| uss | 507 | 81 | 426 | 0 | navy_harbor:284, japan:151 | `nara__6455958-13543540__navy-musicians-play-at-a-colors-ceremony-aboard-the-guided-m.jpeg` |
| facility | 506 | 8 | 497 | 1 | space_nasa:358, science_tech:124 | `nasa__KSC-03pd2314__kennedy-space-center-fla-viewed-from-below-the-space-infrare.jpg` |
| capitol | 505 | 6 | 499 | 0 | government_buildings:490, courtroom_justice:8 | `loc__2005684916__united-states-capitol.tif` |
| white | 498 | 122 | 372 | 4 | wildlife_animals:78, textures_backgrounds:34 | `loc__2012645740__supreme-court-part-i-white-plains-new-york.tif` |
| control | 497 | 18 | 478 | 1 | science_tech:305, space_nasa:133 | `loc__14020358__the-police-control-of-the-slave-in-south-carolina.jpg` |
| people | 490 | 258 | 194 | 38 | selling_floor:78, economy_crisis:75 | `coverr__9463__timelapse-of-people-near-a-cathedral.mp4` |
| department | 488 | 6 | 482 | 0 | retail_commerce:290, selling_floor:88 | `loc__24006610__history-of-the-seattle-police-department-1912.jpg` |
| science | 486 | 190 | 295 | 1 | science_tech:284, space_nasa:162 | `nasa__MSFC-202100043__a-look-inside-the-international-space-station-payload-operat.jpg` |
| air force | 484 | 8 | 476 | 0 | space_nasa:242, japan:70 | `loc__sd0059__ellsworth-air-force-base-group-administration-secure-storage.tif` |
| stage | 481 | 40 | 441 | 0 | space_nasa:459, goods_in_motion:5 | `nasa__sl3-114-1625__view-of-the-expended-s-ivb-second-stage-of-skylab-3-space-ve.jpg` |
| snow | 480 | 144 | 324 | 12 | landscapes_timelapse:198, japan:120 | `loc__2018663275__neon-rich-nightime-view-of-the-snow-cap-diner-near-seligman.tif` |
| park | 479 | 83 | 354 | 42 | wildlife_animals:97, japan:51 | `loc__ca09005868__official-souvenir-book-and-program-of-the-athletic-events-of.jpg` |
| pad | 478 | 14 | 431 | 33 | space_nasa:394, science_tech:47 | `nasa__KSC-03pd2314__kennedy-space-center-fla-viewed-from-below-the-space-infrare.jpg` |
| police | 478 | 50 | 425 | 3 | police_modern:258, police_period:187 | `loc__2016799032__police-station-belle-isle.tif` |
| nasa's | 476 | 23 | 453 | 0 | space_nasa:386, science_tech:77 | `nasa__GSFC_20171208_Archive_e000273__nasa-s-hubble-captures-the-beating-heart-of-the-crab-nebula.jpg` |
| lake | 475 | 164 | 292 | 19 | japan:107, wildlife_animals:81 | `loc__wi0580__town-of-lake-water-tower-municipal-building-4001-south-sixth.tif` |
| light | 473 | 215 | 175 | 83 | textures_backgrounds:60, police_modern:50 | `mixkit__50948__a-light-trail-of-smoke-twirls-and-unfurls-over-a-dark-backgr.mp4` |
| sea ocean | 467 | 235 | 232 | 0 | ocean_nature:395, goods_in_motion:24 | `pixabay_extra__v_22183__waves-water-sea-ocean-landscape-nature-sunset-coast.mp4` |
| training | 465 | 76 | 389 | 0 | war_history:207, space_nasa:151 | `loc__23010642__the-police-recruit-police-manual-of-physical-training.jpg` |
| north | 461 | 40 | 413 | 8 | factory_manufacturing:119, war_history:45 | `loc__2010642234__historic-police-call-boxes-painted-in-stricking-colors-north.jpg` |
| united | 460 | 25 | 435 | 0 | government_buildings:139, money_banking:62 | `loc__2005684916__united-states-capitol.tif` |
| elephant | 459 | 11 | 448 | 0 | wildlife_animals:455, courtroom_justice:2 | `noaa__An_elephant_seal_from_NOAA__an-elephant-seal-from-noaa.jpg` |
| two | 456 | 31 | 410 | 15 | space_nasa:209, science_tech:46 | `loc__2020635862__composite-photograph-of-two-images-police-officers-standing.tif` |
| mammal | 451 | 129 | 322 | 0 | wildlife_animals:434, small_town:9 | `pixabay_extra__i_9372866__fallow-deer-deer-nature-forest-wild-mammal-wildlife-animal-f.jpg` |
| typing | 449 | 35 | 12 | 402 | sfx_mechanical:401, science_tech:21 | `freesound__801120__typewriter-typing-03.mp3` |
| currency | 447 | 202 | 245 | 0 | money_banking:444, newspapers_printing:2 | `loc__2025848106__reimbursement-for-currency-destroyed-by-fire-may-31-1916-com.jpg` |
| time | 443 | 173 | 246 | 24 | space_nasa:158, landscapes_timelapse:75 | `loc__2013650116__there-was-time-for-fun-and-games-last-night-near-w-123rd-pol.tif` |
| open close | 438 | 0 | 1 | 437 | sfx_human_movement:427, sfx_mechanical:8 | `freesound__395648__open-close-door-quietly-1-mp3.mp3` |
| dark | 438 | 103 | 80 | 255 | ambience_beds:138, bgm_general:117 | `freesound__614546__myst-dark-drone-synth-female-vocal-choir-atmo-ambience-cinem.mp3` |
| iss | 436 | 17 | 419 | 0 | space_nasa:402, science_tech:32 | `nasa__sts111-373-018__zenith-view-of-the-iss-silhouetted-against-earth-s-limb-take.jpg` |
| woman | 435 | 263 | 171 | 1 | hands_and_transactions:95, police_modern:68 | `ia__thewomaninthewindow1944__the-woman-in-the-window-1944-fritz-lang-edward-g-robinson-jo.mp4` |
| floor | 431 | 66 | 172 | 193 | sfx_human_movement:185, money_banking:69 | `freesound__451862__footsteps-shoes-dirty-concrete-unfinished-basement-floor-fla.mp3` |
| field artillery | 429 | 0 | 429 | 0 | war_history:429 | `nara__6373154-14831058__sergeant-1st-class-michael-vinson-chief-of-firing-battery-fo.jpeg` |
| paper | 428 | 34 | 268 | 126 | sfx_human_movement:125, money_banking:112 | `loc__2024851477__letter-from-the-secretary-of-the-treasury-transmitting-a-com.jpg` |
| pennsylvania | 428 | 4 | 424 | 0 | factory_manufacturing:216, americana_1930s_1970s:114 | `loc__2010719020__interior-courtroom-william-j-nealon-federal-building-and-u-s.jpg` |
| transport | 428 | 159 | 269 | 0 | goods_in_motion:126, police_modern:73 | `nara__204839921-204839922__a-large-group-of-the-nine-hundred-7th-air-force-men-bound-fo.jpg` |
| man | 427 | 243 | 175 | 9 | hands_and_transactions:61, business_corporate:41 | `coverr__4931__an-old-man-looking-out-of-the-window.mp4` |
| one | 422 | 23 | 392 | 7 | space_nasa:224, money_banking:40 | `loc__2019691079__one-of-dozens-of-examples-of-exemplary-public-art-and-archit.tif` |
| sand | 422 | 99 | 281 | 42 | landscapes_timelapse:193, ocean_nature:132 | `nara__6509148-13020915__an-american-landing-craft-air-cushion-lcac-amphibious-vehicl.jpeg` |
| army | 420 | 25 | 394 | 1 | war_history:311, government_buildings:45 | `nara__36213493-40939197__aerial-photographs-with-interpretations-taking-of-cantigny-o.jpg` |
| beautiful | 418 | 340 | 78 | 0 | textures_backgrounds:113, ocean_nature:98 | `mixkit__4034__beautiful-northern-lights-of-yellow-and-pink-tones.mp4` |
| after | 418 | 12 | 402 | 4 | space_nasa:165, navy_harbor:62 | `loc__2017802277__corner-of-main-street-center-of-town-after-blizzard-brattleb.tif` |
| tower | 417 | 37 | 376 | 4 | space_nasa:109, small_town:100 | `loc__2021758099__an-old-tractor-sits-below-the-town-water-tower-in-funk-nebra.tif` |
| system | 417 | 50 | 365 | 2 | space_nasa:233, science_tech:76 | `loc__2024785551__letter-from-the-secretary-of-war-transmitting-a-system-of-fi.jpg` |
| front | 416 | 24 | 345 | 47 | factory_manufacturing:87, sfx_human_movement:41 | `loc__2010718821__historic-courthouse-front-door-federal-building-and-u-s-cour.jpg` |
| wave | 416 | 271 | 121 | 24 | ocean_nature:337, sfx_environment:22 | `ia__ocean-wave__ocean-wave.mp4` |
| naval | 415 | 27 | 388 | 0 | factory_manufacturing:224, navy_harbor:86 | `loc__2024798807__rifled-cannon-c-letter-from-the-secretary-of-the-navy-transm.jpg` |
| small | 412 | 110 | 178 | 124 | small_town:125, sfx_environment:85 | `loc__2020723796__water-towers-are-a-common-and-readily-available-place-marke.tif` |
| test | 412 | 38 | 366 | 8 | space_nasa:245, science_tech:110 | `nara__6371796-14771933__preparations-are-made-to-test-fire-the-16-inch-50-cal-guns-o.jpeg` |
| moon | 411 | 83 | 328 | 0 | space_nasa:311, world_cities:19 | `nasa__S92-52043__galileo-view-of-moon-orbiting-the-earth-taken-from-3-9-milli.jpg` |
| looking | 410 | 31 | 379 | 0 | factory_manufacturing:205, goods_in_motion:40 | `loc__afcwip004234__the-southwest-corner-of-grand-and-main-streets-looking-west.jpg` |
| summer | 410 | 183 | 141 | 86 | ocean_nature:113, sfx_environment:63 | `pixabay_extra__v_218714__beach-ocean-sea-summer-holiday-wave-nature-beautiful-beautif.mp4` |
| finance | 407 | 251 | 156 | 0 | money_banking:386, business_corporate:13 | `pixabay_extra__v_91678__cards-coins-gambling-game-money-currency-finance-casino-happ.mp4` |
| footsteps | 406 | 1 | 0 | 405 | sfx_human_movement:397, sfx_environment:8 | `freesound__155858__footsteps-in-factory-hall-on-wood-and-concrete-wav.mp3` |
| battalion | 406 | 6 | 400 | 0 | war_history:375, japan:25 | `nara__6480382-13053086__the-site-of-the-new-armory-being-constructed-by-naval-mobile.jpeg` |
| june | 405 | 29 | 373 | 3 | space_nasa:276, government_buildings:30 | `loc__ed-1__the-interior-journal-stanford-ky-june-6-1879.jpg` |
| south | 405 | 32 | 360 | 13 | factory_manufacturing:95, wildlife_animals:33 | `loc__2006678359__photographs-of-the-strom-thurmond-federal-building-and-u-s-c.tif` |
| cliff | 404 | 111 | 291 | 2 | ocean_nature:366, landscapes_timelapse:20 | `pixabay_extra__i_3749383__ocean-cliff-sea-nature-aerial-view-mountain-cliff-cliff-sea.jpg` |
| market | 403 | 104 | 295 | 4 | world_cities:106, retail_commerce:103 | `loc__2017703204__tile-storefront-market-street-new-sharon-iowa.tif` |
| west | 401 | 20 | 379 | 2 | factory_manufacturing:145, goods_in_motion:65 | `loc__2010718820__new-courthouse-federal-building-and-u-s-courthouse-wheeling.jpg` |
| abandoned | 401 | 58 | 340 | 3 | economy_crisis:351, small_town:11 | `loc__2014631684__abandoned-buildings-and-water-tower-in-what-is-now-a-ghost-t.jpg` |
| research | 401 | 31 | 370 | 0 | science_tech:300, space_nasa:63 | `nara__183510546-603086873__federal-hall-national-memorial-feha-manhattan-sites-masi-the.jpg` |
| left | 398 | 3 | 380 | 15 | space_nasa:187, war_history:40 | `loc__2018702648__what-s-left-of-an-old-silo-or-water-tower-now-a-graffiti-cov.tif` |
| desert | 397 | 40 | 337 | 20 | landscapes_timelapse:250, war_history:52 | `loc__2018703101__the-round-cooling-towers-shown-in-the-distance-are-used-to-r.tif` |
| sign | 397 | 55 | 341 | 1 | economy_crisis:136, small_town:74 | `loc__2017881793__neon-sign-for-pink-cadillac-diner-wildwood-new-jersey.jpg` |
| cargo | 395 | 53 | 341 | 1 | goods_in_motion:279, space_nasa:83 | `nara__204951332-204951333__troops-reporting-at-the-22nd-replacement-depot-located-in-ma.jpg` |
| county haer | 395 | 0 | 395 | 0 | factory_manufacturing:304, goods_in_motion:70 | `wikimedia__File_PHOTOCOPY_OF_CA._1934_VIEW_OF_AUTOS_COMING_OFF_ASSEMBLY__file-photocopy-of-ca-1934-view-of-autos-coming-off-assembly.tif` |
| company | 394 | 15 | 379 | 0 | factory_manufacturing:158, stock_market_exchange:47 | `loc__2020781976__to-the-public-in-embarking-in-the-enterprise-of-furnishing-p.jpg` |
| dpla | 392 | 0 | 392 | 0 | retail_commerce:94, stock_market_exchange:67 | `noaa__Assignment-_NOAA_2006_3137_48_National_Oceanic_and_Atmospher__assignment-noaa-2006-3137-48-national-oceanic-and-atmospheri.jpg` |
| rocks | 390 | 113 | 226 | 51 | ocean_nature:178, landscapes_timelapse:87 | `nasa__KSC-03pd1877__kennedy-space-center-fla-on-launch-complex-17-a-cape-canaver.jpg` |
| walking | 389 | 90 | 60 | 239 | sfx_human_movement:228, wildlife_animals:36 | `freesound__383672__footsteps-walking-on-sandy-concrete.mp3` |
| navy | 387 | 44 | 343 | 0 | factory_manufacturing:109, navy_harbor:94 | `loc__2024798807__rifled-cannon-c-letter-from-the-secretary-of-the-navy-transm.jpg` |
| states | 385 | 19 | 366 | 0 | government_buildings:139, money_banking:62 | `loc__2005684916__united-states-capitol.tif` |
| sls | 385 | 21 | 364 | 0 | space_nasa:385 | `nasa__B1B_Crew_Night_Launch__nasas-evolved-sls-block-1b-crew-rocket-night-launch.jpg` |
| work | 384 | 123 | 255 | 6 | science_tech:123, business_corporate:81 | `loc__19013898__practical-police-work-what-to-do-and-how-to-do-it.jpg` |
| united states | 380 | 17 | 363 | 0 | government_buildings:138, money_banking:61 | `loc__2005684916__united-states-capitol.tif` |
| laboratory | 380 | 59 | 321 | 0 | science_tech:254, space_nasa:99 | `loc__hi0722__u-s-naval-base-pearl-harbor-hospital-laboratory-hospital-way.tif` |
| landing | 379 | 64 | 315 | 0 | war_history:179, space_nasa:162 | `nara__74241518-74241519__general-tanks-landing-craft-heavy-equipment-composite.jpg` |
| live | 377 | 72 | 304 | 1 | space_nasa:285, war_history:47 | `nara__6510134-13130600__marines-from-india-battery-3rd-battalion-12th-marines-twenty.jpeg` |
| york | 374 | 46 | 326 | 2 | stock_market_exchange:73, world_cities:57 | `loc__2009632448__orange-county-government-center-goshen-new-york-interior-cou.tif` |
| fire | 372 | 102 | 207 | 63 | war_history:122, sfx_environment:61 | `loc__2022673071__trademark-registration-by-a-g-davis-for-police-special-mess.tif` |
| three | 371 | 5 | 364 | 2 | space_nasa:256, science_tech:53 | `loc__2019691079__one-of-dozens-of-examples-of-exemplary-public-art-and-archit.tif` |
| glass | 370 | 49 | 293 | 28 | factory_manufacturing:154, business_corporate:104 | `loc__2025871752__report-on-the-manufactures-of-the-united-states-at-the-tenth.jpg` |
| winter | 370 | 148 | 205 | 17 | landscapes_timelapse:98, japan:73 | `loc__2016630949__circus-elephant-figure-one-of-several-along-with-circus-hors.jpg` |
| federal building | 367 | 0 | 367 | 0 | courtroom_justice:367 | `loc__2010719020__interior-courtroom-william-j-nealon-federal-building-and-u-s.jpg` |
| wallpaper | 365 | 283 | 82 | 0 | textures_backgrounds:100, ocean_nature:71 | `ia__the-lazarus-man-s-1-e-09-the-wallpaper-prison__the-lazarus-man-s1e09-the-wallpaper-prison.mp4` |
| exploration | 364 | 5 | 359 | 0 | space_nasa:303, science_tech:25 | `nasa__MSFC-202100043__a-look-inside-the-international-space-station-payload-operat.jpg` |
| africa | 363 | 41 | 302 | 20 | wildlife_animals:237, landscapes_timelapse:67 | `loc__2021645979__an-auction-sale-parade-market-square-cape-town-south-africa.tif` |
| crew- | 361 | 33 | 328 | 0 | space_nasa:360, science_tech:1 | `nasa__KSC-20240928-PH-JBS01_0031__nasa-s-spacex-crew-9-live-launch-coverage.jpg` |
| cars | 360 | 275 | 55 | 30 | police_modern:100, world_cities:99 | `coverr__5837__cars-in-the-city-at-night.mp4` |
| along | 359 | 11 | 345 | 3 | factory_manufacturing:251, war_history:34 | `loc__2012645659__view-of-store-fronts-along-main-street-in-benson-arizona.tif` |
| expedition crew | 359 | 5 | 354 | 0 | space_nasa:354, landscapes_timelapse:2 | `nasa__iss043e003041__earth-observation-taken-by-the-expedition-43-crew.jpg` |
| crickets | 355 | 0 | 0 | 355 | sfx_environment:339, ambience_beds:13 | `freesound__637565__forest-boreal-steady-light-wind-breeze-through-trees-bird-cr.mp3` |
| near | 353 | 12 | 305 | 36 | science_tech:52, space_nasa:51 | `loc__2010641511__historic-police-call-box-sheridan-kalorama-call-box-restorat.jpg` |
| launch pad | 353 | 10 | 343 | 0 | space_nasa:316, science_tech:35 | `nasa__KSC-03pd2314__kennedy-space-center-fla-viewed-from-below-the-space-infrare.jpg` |
| spacex crew- | 349 | 25 | 324 | 0 | space_nasa:349 | `nasa__KSC-20240928-PH-JBS01_0031__nasa-s-spacex-crew-9-live-launch-coverage.jpg` |
| black | 348 | 133 | 200 | 15 | textures_backgrounds:51, wildlife_animals:33 | `loc__2020744163__a-vintage-metal-water-tower-in-grambling-louisiana-near-the.tif` |
| department store | 348 | 5 | 343 | 0 | retail_commerce:287, selling_floor:57 | `nara__7385143-16038921__civil-defense-window-display-at-sage-allen-department-store.jpg` |
| apollo | 348 | 3 | 345 | 0 | space_nasa:292, science_tech:51 | `nasa__GSFC_20171208_Archive_e001282__nasa-google-hangout-earthrise-a-new-visualization-45th-anniv.jpg` |
| right | 347 | 4 | 326 | 17 | space_nasa:146, factory_manufacturing:44 | `loc__afcwip001417__view-down-east-main-street-near-the-corner-of-east-main-and.jpg` |
| pearl | 347 | 89 | 258 | 0 | japan:232, navy_harbor:103 | `loc__2017821634__untitled-photo-possibly-related-to-corner-of-montgomery-and.tif` |
| birds | 346 | 120 | 41 | 185 | sfx_environment:155, wildlife_animals:109 | `freesound__513251__spring-distant-thunderstorm-suburban-birds-wind-rumble-ambie.mp3` |
| second | 346 | 7 | 338 | 1 | space_nasa:217, science_tech:22 | `loc__2006675203__photographs-of-the-old-post-office-and-u-s-courthouse-300-we.tif` |
| lccn | 346 | 0 | 346 | 0 | money_banking:95, factory_manufacturing:52 | `wikimedia__File_Bowery_bread_line_LCCN2014683026.jpg__file-bowery-bread-line-lccn2014683026-jpg.jpg` |
| abstract | 345 | 331 | 14 | 0 | textures_backgrounds:204, money_banking:65 | `mixkit__44818__abstract-video-of-a-liquid-with-dark-ink-flowing.mp4` |
| rural | 344 | 78 | 249 | 17 | small_town:261, japan:47 | `loc__2017763330__rural-types-on-main-street-of-ames-iowa.tif` |
| sun | 344 | 218 | 126 | 0 | landscapes_timelapse:134, ocean_nature:46 | `mixkit__52009__flying-over-an-arid-land-with-the-sun-shining-over-the-mesme.mp4` |
| home | 343 | 84 | 250 | 9 | factory_manufacturing:104, police_modern:32 | `loc__18010549__police-reserve-and-home-defense-guard-manual.jpg` |
| port | 343 | 90 | 252 | 1 | goods_in_motion:147, japan:56 | `loc__2017707160__storefront-rock-port-missouri.tif` |
| treasury | 342 | 1 | 341 | 0 | money_banking:321, courtroom_justice:13 | `loc__2024862449__metropolitan-police-district-of-columbia-letter-from-the-sec.jpg` |
| engine | 341 | 12 | 212 | 117 | sfx_mechanical:112, space_nasa:90 | `loc__2017686449__a-water-tower-steam-engine-and-tender-at-tiny-osier-colorado.jpg` |
| county courthouse | 341 | 2 | 339 | 0 | courtroom_justice:323, americana_1930s_1970s:10 | `loc__nc0306__polk-county-courthouse-courthouse-street-columbus-polk-count.tif` |
| ocean sea | 340 | 211 | 129 | 0 | ocean_nature:293, wildlife_animals:18 | `pixabay_extra__v_218714__beach-ocean-sea-summer-holiday-wave-nature-beautiful-beautif.mp4` |
| pearl harbor | 339 | 88 | 251 | 0 | japan:232, navy_harbor:103 | `loc__2017821634__untitled-photo-possibly-related-to-corner-of-montgomery-and.tif` |
| sls rocket | 339 | 13 | 326 | 0 | space_nasa:339 | `nasa__KSC-01172026-Artemis_II_Rollout-27__nasa-s-sls-rocket-and-orion-spacecraft-rollout-to-launch-pad.jpg` |
| ground | 336 | 217 | 112 | 7 | space_nasa:256, war_history:29 | `nasa__jsc2020m000053_Space_to_Ground_352_201223__space-to-ground-the-year-that-was-12-23-2020.mp4` |
| peak | 336 | 9 | 327 | 0 | landscapes_timelapse:291, japan:38 | `pixabay_extra__i_9247234__mountain-nature-landscape-peak-travel-forest-outdoors-summit.jpg` |
| highway | 335 | 250 | 73 | 12 | small_town:165, police_modern:44 | `ia__freedomh1956__freedom-highway-part-i.mp4` |
| hall | 335 | 9 | 318 | 8 | government_buildings:134, economy_crisis:77 | `loc__2022650295__city-hall-and-police-station-east-st-louis.tif` |
| shipping | 335 | 37 | 297 | 1 | goods_in_motion:280, factory_manufacturing:28 | `nara__204953486-204953487__bombing-of-japanese-merchant-shipping-simpson-harbor-rabaul.jpg` |
| tunnel | 334 | 21 | 305 | 8 | science_tech:266, space_nasa:27 | `loc__99614948__main-street-entrance-to-the-tunnel.tif` |
| cash | 333 | 174 | 159 | 0 | money_banking:319, retail_commerce:6 | `mixkit__47005__a-lot-of-cash-over-a-rotating-background.mp4` |
| main | 332 | 5 | 322 | 5 | small_town:124, americana_1930s_1970s:63 | `loc__az0060__police-station-south-main-street-tucson-pima-county-az.tif` |
| distant | 330 | 3 | 73 | 254 | sfx_environment:179, ambience_beds:67 | `freesound__158691__distant-thunder-and-rain-from-half-open-window-2-aif.mp3` |
| tokyo | 330 | 115 | 214 | 1 | japan:196, science_tech:40 | `nara__134403789-134403790__suburban-tokyo-street.jpg` |
| wall | 328 | 33 | 271 | 24 | stock_market_exchange:99, textures_backgrounds:35 | `loc__93509655__the-centennial-wall-paper-printing-press-machinery-hall.tif` |
| complex | 327 | 2 | 323 | 2 | space_nasa:174, science_tech:95 | `nasa__KSC-03pd2879__vandenberg-afb-calif-the-mobile-service-tower-on-space-launc.jpg` |
| fuji | 327 | 59 | 267 | 1 | japan:314, war_history:9 | `nara__6480382-13053086__the-site-of-the-new-armory-being-constructed-by-naval-mobile.jpeg` |
| dollar | 327 | 109 | 218 | 0 | money_banking:305, bank_and_branch:9 | `pixabay_extra__i_1974694__dollar-money-currency-trade-poverty-paper-bill-bank-note-fin.jpg` |
| outdoors | 326 | 75 | 240 | 11 | landscapes_timelapse:107, small_town:57 | `pixabay_extra__i_9247234__mountain-nature-landscape-peak-travel-forest-outdoors-summit.jpg` |
| exercise | 323 | 13 | 310 | 0 | war_history:238, japan:37 | `nara__6350917-14698438__navy-and-marine-corps-troops-aboard-the-utility-landing-craf.jpeg` |
| ksc | 322 | 1 | 321 | 0 | space_nasa:258, science_tech:59 | `nasa__KSC-20240402-PH-KLS02_0143__earth-day-at-ksc.jpg` |
| cotton | 321 | 0 | 318 | 3 | factory_manufacturing:309, sfx_human_movement:3 | `loc__2018674972__it-seems-a-pity-that-some-of-the-spinning-frames-are-so-larg.tif` |
| workers | 321 | 47 | 273 | 1 | factory_manufacturing:97, space_nasa:82 | `loc__2018676631__group-of-workers-at-sagamore-mills-1-some-of-these-were-boys.tif` |
| space telescope | 321 | 4 | 317 | 0 | science_tech:268, space_nasa:53 | `nasa__carina-nebula__james-webb-space-telescope-nircam-image-of-the-cosmic-cliffs.png` |
| agency | 320 | 3 | 317 | 0 | space_nasa:237, science_tech:55 | `loc__ca10005037__rules-and-regulations-for-the-government-of-the-preventive-f.jpg` |
| desk | 318 | 99 | 215 | 4 | business_corporate:178, science_tech:73 | `loc__98000434__a-desk-book-of-printing-types-to-which-is-appended-a-condens.jpg` |
| railroad | 318 | 32 | 286 | 0 | americana_1930s_1970s:128, goods_in_motion:103 | `loc__2025169042__pennsylvania-railroad-locomotive-prr-937.tif` |
| plumage | 318 | 216 | 102 | 0 | wildlife_animals:305, money_banking:5 | `pixabay_extra__v_191159__gull-bird-snow-plumage-sitting-winter-wildlife.mp4` |
| building courthouse | 315 | 0 | 315 | 0 | courtroom_justice:315 | `loc__2010719020__interior-courtroom-william-j-nealon-federal-building-and-u-s.jpg` |
| cityscape | 314 | 91 | 221 | 2 | world_cities:206, business_corporate:63 | `pixabay_extra__i_2945920__medieval-town-night-architecture-city-cityscape-europe-old-b.jpg` |
| support | 314 | 4 | 310 | 0 | war_history:153, science_tech:52 | `nara__6637256-13169765__advancing-us-marine-corps-usmc-personnel-from-charlie-compan.jpeg` |
| aircraft factory | 313 | 0 | 313 | 0 | factory_manufacturing:313 | `loc__2017691821__women-aircraft-workers-nice-work-if-you-can-get-it-a-leadman.tif` |
| coral reef | 312 | 91 | 220 | 1 | ocean_nature:311, sfx_environment:1 | `nasa__PIA25861__study-uses-modis-data-to-determine-belize-coral-reef-risk.jpg` |
| hardware | 311 | 15 | 296 | 0 | retail_commerce:137, space_nasa:102 | `loc__2025871752__report-on-the-manufactures-of-the-united-states-at-the-tenth.jpg` |
| atlantis | 311 | 0 | 311 | 0 | space_nasa:296, science_tech:13 | `nasa__sts076-370-020__view-of-the-shuttle-orbiter-atlantis-from-the-mir-space-stat.jpg` |
| aboard | 310 | 29 | 281 | 0 | space_nasa:103, navy_harbor:95 | `nara__204839927-204839928__a-large-group-of-gis-of-the-7th-air-force-bound-for-the-unit.jpg` |
| equipment | 310 | 40 | 270 | 0 | space_nasa:86, war_history:70 | `loc__11003805__historical-sketch-of-the-police-service-of-hartford-from-163.jpg` |
| screen | 309 | 267 | 20 | 22 | money_banking:91, economy_crisis:77 | `coverr__3490__a-screen-showing-financial-analysis-of-a-cryptocurrency.mp4` |
| shopping | 309 | 112 | 197 | 0 | economy_crisis:128, selling_floor:92 | `pixabay_extra__i_1180397__akihabara-tokyo-night-japan-japanese-shopping-asian-technolo.jpg` |
| astronaut | 308 | 7 | 301 | 0 | space_nasa:223, science_tech:85 | `nasa__41G-11-027__astronaut-kathryn-sullivan-using-binoculars-for-magnifed-vie.jpg` |
| island | 306 | 105 | 196 | 5 | ocean_nature:106, japan:44 | `loc__94501754__troops-of-the-185th-inf-40th-div-take-cover-behind-advancing.tif` |
| opening | 303 | 138 | 39 | 126 | sfx_human_movement:118, money_banking:81 | `ia__200333-panama-pacific-international-exposition-opening-parad__panama-pacific-international-exposition-opening-parade.mp4` |
| bridge | 303 | 122 | 175 | 6 | world_cities:88, factory_manufacturing:46 | `loc__pa3386__bethlehem-steel-corporation-south-bethlehem-works-along-lehi.tif` |
| atmosphere | 302 | 63 | 156 | 83 | space_nasa:132, landscapes_timelapse:46 | `nasa__iss035e014335__earth-atmosphere-observations-taken-by-the-expedition-35-cre.jpg` |
| window | 298 | 18 | 263 | 17 | retail_commerce:72, selling_floor:56 | `loc__2010718829__historic-courthouse-window-detail-federal-building-and-u-s-c.jpg` |
| war | 298 | 151 | 145 | 2 | courtroom_justice:97, factory_manufacturing:60 | `ia__adc-10018__sentencing-of-nazi-war-leaders-at-nuremberg-10-1946.mp4` |
| surface | 298 | 27 | 267 | 4 | space_nasa:234, ocean_nature:14 | `nasa__STS053-105-002__sts-53-view-of-ov-103-s-payload-bay-plb-the-moon-and-earth-s.jpg` |
| processing | 298 | 4 | 294 | 0 | space_nasa:192, science_tech:99 | `nasa__KSC-03pd3282__vandenberg-afb-calif-in-the-nasa-spacecraft-processing-facil.jpg` |
| ambience | 297 | 0 | 1 | 296 | ambience_beds:152, sfx_environment:112 | `freesound__750799__empty-office-ambience.mp3` |
| east | 297 | 14 | 279 | 4 | factory_manufacturing:83, government_buildings:43 | `loc__afcwip001417__view-down-east-main-street-near-the-corner-of-east-main-and.jpg` |
| wooden | 297 | 35 | 166 | 96 | sfx_human_movement:94, goods_in_motion:49 | `nara__6489223-13220985__a-crewman-repairs-wooden-planking-on-the-weather-deck-of-the.jpeg` |
| european | 297 | 42 | 253 | 2 | space_nasa:159, world_cities:77 | `nasa__jsc2015e106168__in-the-integration-facility-at-the-baikonur-cosmodrome-in-ka.jpg` |
| plant | 297 | 68 | 229 | 0 | factory_manufacturing:178, economy_crisis:17 | `loc__pa3339__u-s-steel-duquesne-works-blast-furnace-plant-along-monongahe.tif` |
| rock | 295 | 93 | 196 | 6 | ocean_nature:157, landscapes_timelapse:56 | `loc__2006675203__photographs-of-the-old-post-office-and-u-s-courthouse-300-we.tif` |
| artemis launch | 295 | 8 | 287 | 0 | space_nasa:274, science_tech:21 | `nasa__KSC_20221115_Artemis_I_Launch-1__artemis-i-launch.jpg` |
| side | 294 | 9 | 258 | 27 | factory_manufacturing:65, japan:36 | `loc__afcwip004231__three-buildings-on-the-west-side-of-main-street-north-of-gra.jpg` |
| battleship | 294 | 2 | 292 | 0 | navy_harbor:245, japan:49 | `nara__45511570-45511571__navy-naval-operations-mine-laying-mines-on-track-launching-d.jpg` |
| sunrise | 293 | 178 | 110 | 5 | landscapes_timelapse:121, ocean_nature:39 | `coverr__9808__sunrise-at-the-beach-dock.mp4` |
| animals | 293 | 144 | 148 | 1 | wildlife_animals:205, ocean_nature:59 | `pixabay_extra__i_1482712__roe-deer-kitz-wild-forest-red-deer-fawn-young-animals-young.jpg` |
| environment | 293 | 20 | 273 | 0 | space_nasa:182, science_tech:57 | `loc__2018673748__113-indianapolis-newsboys-waiting-for-the-base-ball-edition.tif` |
| tree | 289 | 135 | 137 | 17 | wildlife_animals:67, landscapes_timelapse:51 | `loc__2017807299__hotel-on-main-street-of-town-lone-tree-north-dakota.tif` |
| delta | 289 | 2 | 287 | 0 | space_nasa:253, war_history:26 | `nara__6498576-12759139__spc-chris-laury-left-and-pfc-earl-walker-delta-battery-3rd-b.jpeg` |
| stream | 288 | 42 | 109 | 137 | sfx_environment:135, landscapes_timelapse:104 | `freesound__165286__nolde-forest-small-stream-wind-in-trees-wav.mp3` |
| final | 287 | 12 | 275 | 0 | space_nasa:118, retail_commerce:101 | `nara__6654454-13519048__a-hikers-view-looking-upwards-to-the-final-station-at-mt-fuj.jpeg` |
| station iss | 287 | 14 | 273 | 0 | space_nasa:287 | `nasa__0701890__international-space-station-iss.jpg` |
| laptop | 286 | 78 | 168 | 40 | science_tech:129, business_corporate:57 | `nasa__KSC-03pd2375__kennedy-space-center-fla-dr-grant-gilmore-dynamac-corp-utili.jpg` |
| deck | 286 | 6 | 278 | 2 | navy_harbor:232, science_tech:21 | `nara__6444709-13464048__at-parade-rest-on-the-deck-of-a-us-7th-fleet-warship-paying.jpeg` |
| hands | 284 | 127 | 157 | 0 | space_nasa:128, hands_and_transactions:68 | `nasa__KSC-03pd1617__kennedy-space-center-fla-the-delta-ii-rocket-on-launch-compl.jpg` |
| battery battalion | 284 | 0 | 284 | 0 | war_history:267, japan:17 | `nara__6653796-13544966__us-marine-corps-usmc-marines-gun-one-kilo-battery-3rd-battal.jpeg` |
| operations | 283 | 48 | 235 | 0 | space_nasa:98, war_history:94 | `loc__2025876483__alaska-seal-and-fur-company-letter-from-the-secretary-of-the.jpg` |
| module | 282 | 4 | 278 | 0 | space_nasa:197, science_tech:84 | `nasa__KSC-03pd2322__kennedy-space-center-fla-the-sts-114-crew-is-welcomed-to-han.jpg` |
| square | 281 | 8 | 266 | 7 | small_town:166, courtroom_justice:30 | `loc__sd0013__union-county-courthouse-courthouse-square-elk-point-union-co.tif` |
| pattern | 281 | 111 | 170 | 0 | textures_backgrounds:234, factory_manufacturing:9 | `met__388376__embroidery-pattern-with-seven-six-pointed-stars-and-four-cor.jpg` |
| area | 280 | 31 | 244 | 5 | war_history:144, space_nasa:40 | `loc__2023630509__gas-station-attendant-filling-a-car-tank-with-custom-blend-g.tif` |
| through | 279 | 54 | 115 | 110 | sfx_environment:86, war_history:35 | `nara__12008267-15829962__photograph-of-american-troops-marching-through-the-streets-o.jpg` |
| shore | 278 | 110 | 134 | 34 | ocean_nature:169, war_history:36 | `loc__2019691079__one-of-dozens-of-examples-of-exemplary-public-art-and-archit.tif` |
| inside | 278 | 12 | 215 | 51 | space_nasa:64, science_tech:45 | `loc__2020742211__one-rarely-sees-two-town-water-towers-close-together-such-as.tif` |
| district | 278 | 21 | 254 | 3 | business_corporate:67, courtroom_justice:44 | `loc__2024862449__metropolitan-police-district-of-columbia-letter-from-the-sec.jpg` |
| regiment | 278 | 4 | 274 | 0 | war_history:265, japan:6 | `nara__36213493-40939197__aerial-photographs-with-interpretations-taking-of-cantigny-o.jpg` |
| coverage | 276 | 48 | 228 | 0 | space_nasa:256, science_tech:19 | `nasa__KSC-20240601-PH-GEB01_0033__nasas-boeing-crew-flight-test-live-launch-coverage.jpg` |
| metal | 275 | 22 | 77 | 176 | sfx_human_movement:107, sfx_mechanical:60 | `freesound__637990__wind-gusty-through-quiet-studio-full-of-junk-wood-rattle-met.mp3` |
| morning | 274 | 92 | 68 | 114 | sfx_environment:104, japan:32 | `freesound__514682__morning-stream-1-stereo.mp3` |
| operation | 274 | 19 | 254 | 1 | war_history:193, navy_harbor:31 | `nara__6637256-13169765__advancing-us-marine-corps-usmc-personnel-from-charlie-compan.jpeg` |
| may | 273 | 32 | 232 | 9 | space_nasa:80, government_buildings:27 | `loc__99614110__illinois-the-anarchist-labor-troubles-in-chicago-a-police-pa.tif` |
| cape | 273 | 2 | 270 | 1 | space_nasa:198, science_tech:42 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| service | 273 | 19 | 254 | 0 | space_nasa:54, science_tech:50 | `loc__11003805__historical-sketch-of-the-police-service-of-hartford-from-163.jpg` |
| smoke | 272 | 218 | 54 | 0 | textures_backgrounds:200, factory_manufacturing:16 | `mixkit__1968__black-background-with-smoke-foreground.mp4` |
| young | 271 | 113 | 157 | 1 | wildlife_animals:75, hands_and_transactions:37 | `loc__2018676094__another-young-newsboy-in-hartford-conn-august-26-1924-locati.tif` |
| landscape nature | 271 | 71 | 200 | 0 | landscapes_timelapse:136, small_town:45 | `pixabay_extra__i_3019429__matterhorn-summit-mountains-snow-winter-landscape-nature-ice.jpg` |
| base | 270 | 14 | 255 | 1 | space_nasa:77, war_history:70 | `loc__2018673748__113-indianapolis-newsboys-waiting-for-the-base-ball-edition.tif` |
| kyoto | 269 | 28 | 241 | 0 | japan:268, retail_commerce:1 | `pixabay_extra__i_9348003__shrine-torii-japan-fushimi-nature-temple-kyoto-fushimi-inari.jpg` |
| gravel | 268 | 1 | 12 | 255 | sfx_human_movement:253, small_town:9 | `freesound__537835__two-footsteps-on-gravel.mp3` |
| wind tunnel | 267 | 0 | 266 | 1 | science_tech:243, space_nasa:22 | `nara__17443346-17453348__sb-switch-in-capacitor-bank-control-in-the-10x10-foot-wind-t.jpg` |
| division | 267 | 13 | 254 | 0 | war_history:226, courtroom_justice:11 | `loc__2025845069__new-machinery-for-treasury-bindery-letter-from-the-acting-se.jpg` |
| soyuz | 265 | 7 | 258 | 0 | space_nasa:265 | `nasa__iss009e05034__soyuz-tma-3-separates-from-the-space-station-after-undocking.jpg` |
| tropical | 264 | 117 | 140 | 7 | ocean_nature:212, weather_disasters:11 | `loc__2023696450__sculpture-flotilla-of-kayaks-in-a-tropical-storm-in-the-silv.tif` |
| usa | 264 | 48 | 202 | 14 | war_history:101, small_town:34 | `nara__6628231-12912625__us-army-usa-soldiers-from-the-95th-chemical-company-special.jpeg` |
| historic | 264 | 14 | 250 | 0 | world_cities:50, courtroom_justice:46 | `loc__2010718822__historic-courthouse-federal-building-and-u-s-courthouse-whee.jpg` |
| sts- mission | 264 | 0 | 264 | 0 | space_nasa:213, science_tech:50 | `nasa__sts093-704-087__earth-observations-taken-from-space-shuttle-columbia-during.jpg` |
| american | 260 | 41 | 218 | 1 | money_banking:66, war_history:35 | `loc__2022637908__an-american-police-station-in-peking-china.tif` |
| exchange | 260 | 21 | 239 | 0 | stock_market_exchange:226, money_banking:25 | `loc__35030001__tables-of-sterling-exchange-for-converting-sterling-into-cur.jpg` |
| which | 257 | 2 | 254 | 1 | space_nasa:93, japan:38 | `loc__2017770144__main-street-storefront-chickasaw-oklahoma-this-is-a-region-f.tif` |
| aquarium | 257 | 119 | 138 | 0 | ocean_nature:244, textures_backgrounds:5 | `pixabay_extra__i_4482131__lionfish-fish-sea-underwater-aquarius-coral-zodiac-capricorn.jpg` |
| ambient | 256 | 1 | 0 | 255 | bgm_general:118, ambience_beds:116 | `freesound__612591__night-ambient-with-crickets-rumble-and-baby-48000-hz-24-bit.mp3` |
| california | 256 | 50 | 197 | 9 | japan:25, money_banking:25 | `loc__2013631471__neon-sign-for-mel-s-drive-in-and-celebrity-bar-in-the-hollyw.jpg` |
| canaveral | 255 | 0 | 255 | 0 | space_nasa:204, science_tech:49 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| members | 254 | 0 | 254 | 0 | war_history:73, space_nasa:66 | `loc__2017692837__production-m-4-tanks-hull-members-of-an-m-4-tank-on-a-positi.tif` |
| locomotive | 253 | 8 | 244 | 1 | americana_1930s_1970s:117, factory_manufacturing:114 | `loc__2025169042__pennsylvania-railroad-locomotive-prr-937.tif` |

## 3. Known name-vs-content traps

| source | trap |
|---|---|
| noaa | Titles are survey codes (`20260130aC0894545w340345n`). Nothing about the frame is knowable from the name — must be eyeballed. |
| nypl | 27k scans share the title `new-york-city-directory`; the subject index cannot separate them. Treat as page scans, not footage. |
| ia | Real titles, but talking-head lectures/podcasts pass the relevance gate (measured 4/24 on the courtroom_justice sheet). Check before staging. |
| factory (older shelf) | Filenames are the SEARCH QUERY, verified ~50% wrong. Use `select_factory_assets.py` + FACTORY_SUBTYPE_INVENTORY.v001.md, never the name. |
