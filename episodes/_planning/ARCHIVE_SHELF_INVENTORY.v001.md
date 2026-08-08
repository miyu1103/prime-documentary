# Archive shelf — what it can actually supply (2026-08-09 05:44)

64,040 items / 1,842 GB across 62 themes, 16 sources.

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
| ambience_beds | freesound | 1,067 | 4.4 | 0/0/1067 | — | Roomtone Bedroom Yew; Room Tone Stairs.wav; Empty Office Ambience |
| americana_1930s_1970s | met | 305 | 0.9 | 0/305/0 | — | Allegory; Allegory of the Planets and Continents; Allegory of Virtues and Vices at the Court of Charle |
| americana_1930s_1970s | loc | 243 | 11.6 | 0/243/0 | good (American storefront, main-street and railroad photographs - strongest still source) | Main street storefronts. Edwards, Mississippi; Storefront Transom, angle 1, Main Street, Chinook, M; Storefront Transom, angle 2, Main Street, Chinook, M |
| americana_1930s_1970s | smithsonian | 19 | 0.1 | 0/19/0 | mixed (19th-c mural studies; only the Justice/Courage allegories fit) | New England Factory Life--"Bell-Time", from Harper's; New England Factory Life – "Bell-Time"; Factory at the shore. |
| americana_1930s_1970s | nara | 12 | 1.5 | 11/1/0 | good (mid-century street, railroad and civic-life motion footage) | Main Street U.S.A.; Footage of Olympic Stadium in Berlin; Bomb Damage to; [LAKE SHORE COUNTY FAIR] |
| americana_1930s_1970s | ia | 9 | 0.9 | 9/0/0 | good (period educational films and home movies; several underexposed) | Dynamic American City, The (Part II); Dynamic American City, The (Part I); [Home movie: 098550: Sausage factory in Michigan] |
| atmosphere_symbolic | pexels | 5 | 0.0 | 0/5/0 | — | close up on hands of clock; professional handshake in business meeting; macro shot of a clock |
| audio | oyez | 5 | 0.1 | 0/0/5 | — | Carpenter oral argument; Kelo oral argument; Riley oral argument |
| bank_and_branch | wikimedia | 474 | 3.6 | 0/474/0 | good (bank buildings, branch facades and one historic teller hall - the only source actually supplying banks) | File:HK WTSD 樂富廣場 Lok Fu Place mall shop Standard Ch; File:HK SKD TKO Po Lam Tsui Lam Estate Square Shoppi; File:HK 港島 南區 Southern District 黃竹坑 Wong Chuk Hang 香 |
| bank_and_branch | coverr | 2 | 0.0 | 2/0/0 | good (2 items only, cafe cash-handling close-ups; generic transaction inserts, not bank interiors) | premium a customer pays barista with cash; close up of barista taking money from a customer |
| bench_to_line | mixkit | 45 | 1.3 | 45/0/0 | mixed (a real spine of welding, robotics and packaging diluted by fashion, fitness and motivational-businessman stock) | Metal drawer in a garage with tools; Model turns to pose as a photographer takes photos i; White flowers in the breeze |
| bench_to_line | ia | 2 | 0.3 | 2/0/0 | good (2 items, both the 1936 Chevrolet plant film Master Hands - best-matched material but corporate-attributable) | Master Hands |
| bench_to_line | coverr | 1 | 0.0 | 1/0/0 | good (1 item, gloved hands grinding metal; carries a legible metabo tool brand) | angle grinder on metal |
| bgm_general | freesound | 381 | 1.8 | 0/0/381 | — | Eerie Horror Nature Atmosphere SFX; Granular Dark and Brilliant Ambient Background Textu; Relax Dark Wind Ambient Background.wav |
| business_corporate | pixabay_extra | 781 | 4.6 | 247/534/0 | mixed (architecture tiles are fine, polluted with 3D icon art and animal wallpapers; 4 of 9 missing on disk) | discussion, desk, people, office, team, meeting, bus; handshake, greeting, deal, hello, thanks, trust, wel; design, marketing, business |
| business_corporate | mixkit | 88 | 1.7 | 88/0/0 | mixed (competent but heavily acted handshakes and meeting reenactments; a quarter is lifestyle filler) | Business people at work meeting; Men in black shirts shake hands at business meetng; A man is presenting a business report |
| business_corporate | unsplash | 50 | 0.1 | 0/50/0 | good (empty, unbranded, well-lit boardrooms and towers that carry narration without asserting a specific company) | oval brown wooden conference table and chairs inside; long table with Eiffel chair inside room; beige wooden conference table |
| business_corporate | coverr | 3 | 0.0 | 3/0/0 | good (3 items, two of them the same Lisbon facade - effectively two distinct shots) | premium skyscrapers viewed through a glass roof; a glass building in lisbon; a glass building on lisbon street |
| chicago_city | nara | 18 | 1.5 | 9/9/0 | good (skyline stills, lakefront aerials, parade and explosion-damage newsreel) | Chicago riots, Chicago, Illinois; FIRST DIVISION CIRCUS AT CHICAGO; Apollo 11 Chicago Parade and Ceremony in Civic Cente |
| chicago_city | ia | 2 | 0.4 | 2/0/0 | good (2 items: World's Fair home movie and 1968 riot footage) | [Home Movies: Chicago World's Fair]; Chicago riots, Chicago, Illinois (1968) |
| civic_voting | pexels | 3 | 0.0 | 0/3/0 | — | protesters on the street; us a flag on pole under blue sky; flag blowing in the wind |
| courtroom_justice | pixabay_extra | 1,589 | 17.8 | 663/926/0 | — | courthouse, building, government, architecture, law,; belgium, castle, architecture, palace, building, for; judge, 2d character, gavel, law, justice, vector art |
| courtroom_justice | loc | 1,145 | 47.2 | 0/1145/0 | good (HABS/GSA courthouse exteriors, lobbies, empty courtrooms - instantly cuttable) | [Orange County Government Center, Goshen, New York. ; [Orange County Government Center, Goshen, New York. ; Interior courtroom, William J. Nealon Federal Buildi |
| courtroom_justice | nara | 174 | 20.8 | 128/46/0 | mixed (WWII war-crimes tribunal reels, diluted by leaders and document cards) | British Courtroom; Black Panther; Crown Prince Olaf and Princess Martha of Norway at R |
| courtroom_justice | mixkit | 159 | 3.1 | 159/0/0 | — | Judge Shows Money on Table; The scales of justice; Judge pronounces sentence in court |
| courtroom_justice | ia | 111 | 32.4 | 111/0/0 | mixed (mostly talking-head public-access programs; only the Nuremberg reels are cuttable) | Disorder in the Court; Cross Examination; WITNESS FOR THE PROSECUTION trailer |
| courtroom_justice | unsplash | 50 | 0.3 | 0/50/0 | — | Ornate courtroom with gilded decorations and chandel; Empty ornate courtroom interior with wooden paneling; Empty courtroom featuring rich wooden paneling and a |
| courtroom_justice | coverr | 1 | 0.0 | 1/0/0 | — | walking to the mountain top |
| crime_police | pexels | 7 | 0.0 | 0/7/0 | — | police car on the street; interior of jail; prisoner walking into cell |
| decision_rooms | wikimedia | 163 | 1.6 | 0/163/0 | good (real company offices and period labour photography, though it skews to unions and strikes rather than boardrooms) | File:JB Pritker on labor unions DBqb3aoWAAAANlo.jpg; File:Emblem of Guild of Trade Unions of Afghanistan ; File:RMT (trade union) logo.png |
| decision_rooms | unsplash | 50 | 0.1 | 0/50/0 | mixed (document-and-desk tiles are useful; failures are word-game and gavel novelty shots) | Petition to File For Bankruptcy; gray scale photography of Lawyer Bankruptcy scrabble; Membership Certificate paper |
| decision_rooms | ia | 1 | 0.2 | 1/0/0 | good (1 item, a mid-century office training film - dramatised acting, never cut as actuality) | New Girl in the Office, The |
| depression_hardship | wikimedia | 183 | 1.7 | 0/183/0 | mixed (1,598 of 1,688 items yet 6 of 9 sampled tiles missing on disk; the two that render are paper scans) | File:Bowery bread line LCCN2014683026.jpg; File:Bowery men waiting for bread in bread line, (Ne; File:Bowery men waiting for bread in bread line, New |
| depression_hardship | loc | 85 | 1.9 | 0/85/0 | mixed (the backbone - FSA sharecropper cabins, porches, relief scenes - but four in ten tiles are book covers, charts or drawings) | Free coffee at Bowery Mission for unemployed; The problem of the unemployed.; Swollen fortunes and the problems of the unemployed |
| depression_hardship | nara | 5 | 0.5 | 4/1/0 | mixed (five tiles, four carrying the identical CCC title - one programme reel sliced up, low diversity) | Civilian Conservation Corps; AN Army relief team carries an Army tent in a box to |
| documents_paper | pexels | 4 | 0.0 | 0/4/0 | — | cozy library bookshelves with ladder; person signing in documentation paper; a person signing divorce documents |
| economy_crisis | pixabay_extra | 699 | 4.8 | 208/491/0 | mixed (4 of 7 tiles missing on disk and a Dubai waterfront pulled in on the word mall - the visual opposite of crisis) | mall, shop, store, department store, people, busy, b; online, shopping, cart, mobile, digital, internet, s; supermarket, cart, market, mall, buy, retail, buyer, |
| economy_crisis | wikimedia | 122 | 1.2 | 0/122/0 | good (highest-yield source, but six of eleven tiles are the same Slovakian plant - repeat-footage hazard) | File:Abandoned factory interior (31260792602).jpg; File:Alliance Brick abandoned factory, Darlington.jp; File:Research Of An Abandoned Factory (232886655).jp |
| economy_crisis | mixkit | 56 | 1.4 | 56/0/0 | mixed (half usable crowds and malls; a missile launch and abstract renders are off-theme) | Pairs of shoes in a department store display; Busy mall escalator timelapse; Young woman browsing at clothes in a store |
| economy_crisis | unsplash | 50 | 0.2 | 0/50/0 | good (every tile a real storefront or sign, roughly half literal closure notices - the most directly on-theme cluster reviewed) | a store front with a variety of items in the window; brown and red wooden store; Corbett building supply store with boarded windows |
| economy_crisis | ia | 1 | 0.1 | 1/0/0 | good (1 item, period industrial actuality; it is editorial film, so avoid producer captions) | America Marching On: A Screen Editorial With Lowell |
| factory_manufacturing | wikimedia | 2,197 | 30.0 | 0/2197/0 | good (HABS/HAER survey photography of mills, foundries and works; 5 of 14 sampled tiles missing on disk) | File:Assembly line) Vicker Sons & Maxim Gun Factory ; File:Ford assembly line in Copenhagen 1923.jpg; File:Underwood Typewriter Assembly 1962.jpg |
| factory_manufacturing | loc | 167 | 3.6 | 0/167/0 | mixed (barely clears mixed: dominated by digitised trade-book covers, union newspaper pages and expense tables) | United automobile worker (Detroit, Mich.), June 5, 1; United automobile worker (Detroit, Mich.), January 2; United automobile worker (Detroit, Mich.), October 3 |
| factory_manufacturing | nara | 38 | 5.1 | 35/3/0 | good (period industrial reels of the Rouge, foundries and steel - the strongest source here) | [FORD MOTOR COMPANY AUTOMOBILE ASSEMBLY LINES]; Ford Automobile Assembly Line / Ford Automobile Serv; [FORD ASSEMBLY LINES AND AUTOMOBILE TESTING] |
| finance_money | pexels | 3 | 0.0 | 0/3/0 | — | banknotes of different denominations cash dolors; paper dollar bills; hands exchanging dollars |
| finance_money | wikimedia | 1 | 0.0 | 0/1/0 | — | US one-dollar bill |
| forensics_dna | pexels | 1 | 0.0 | 0/1/0 | — | modern fingerprint access control system |
| goods_in_motion | pixabay_extra | 855 | 13.2 | 367/488/0 | mixed (largest source at 3,145 items and only 40%: loading returned a loading bar, shipping returned a cruise ship) | warehouse, bogota, colombia; finland, porvoo, borg, old, wooden warehouse, villag; containers, cargo, shipping shipping, freight, port, |
| goods_in_motion | wikimedia | 597 | 5.9 | 0/597/0 | good (grain handling and rail survey photography; one WWII internment-camp file shows the category is broader than the theme) | File:Camouflage Design for Cargo Ship - NARA - 69971; File:Cargo ship 2.png; File:Cargo ship 3.png |
| goods_in_motion | mixkit | 72 | 1.6 | 72/0/0 | good (cleanest source: ports, trucks, cranes and delivery, only two lifestyle clips out of place) | View of a forklift driver operating in a warehouse; A large warehouse stored with wheat ready for shipme; Warehouse area on a coastline in a general shot |
| goods_in_motion | unsplash | 50 | 0.2 | 0/50/0 | mixed (splits into genuine warehouse footage and a block of blank-paper desk flat-lays) | a computer keyboard sitting on top of a wooden table; A receipt sitting on top of a wooden table; white printer paper on brown wooden table |
| government_buildings | pixabay_extra | 2,265 | 29.7 | 933/1332/0 | — | austin, capitol, building, texas, architecture, usa,; austin, capitol, building, texas, architecture, usa,; austin, capitol, building, texas, architecture, usa, |
| government_buildings | ia | 704 | 415.7 | 704/0/0 | mixed (half genuine mid-century film, half partisan citizen-journalist uploads) | Government Workers; [Home Movies: Kansas City to Natchez]; [Home Movies: Washington & Gettysburg] |
| government_buildings | nara | 618 | 4.1 | 15/603/0 | mixed (large slice is Federal Hall planning paperwork and microfilm cards) | DAWN STRIKES THE CAPITOL DOME; WEAVING STRAW, SEOUL ; SEOUL ; CAPITOL BUILDING, PYO; National Aeronautics and Space Administration-Astron |
| government_buildings | loc | 123 | 1.1 | 0/123/0 | good (high-res Supreme Court and Capitol exteriors plus period prints) | Supreme Court Building, Washington, D.C.; U.S. Supreme Court building, Washington, D.C.; United States Capitol |
| government_buildings | unsplash | 50 | 0.2 | 0/50/0 | — | the dome of the u s capitol building with a statue o; the ceiling of the dome of the us capitol building; United states capitol building under dramatic sky |
| government_buildings | mixkit | 42 | 1.0 | 42/0/0 | — | Corporate and business buildings in the city.; Buildings under construction, aerial view; Panoramic view of Manhattan buildings |
| government_buildings | coverr | 1 | 0.0 | 1/0/0 | — | flags on a skyscraper |
| hands_and_transactions | mixkit | 597 | 14.2 | 597/0/0 | mixed (only 5 of 16 tiles show work or money changing hands; the rest is coffee-shop lifestyle, sport and gaming) | Silhouette of a hand being held up in front of the s; Hand touching wheat in golden sunset; Electronics assembly line |
| household_loss | unsplash | 50 | 0.2 | 0/50/0 | good (real doors, windows, notices and ordinary houses that cut straight into a foreclosure sequence) | Teal double doors with "bonjour" sign above; A metal door covered in various posters and notices.; Illuminated "exit to the city" sign above a brown do |
| household_loss | wikimedia | 20 | 0.1 | 0/20/0 | mixed (archival boarded-up and foreclosure-sale material is excellent; six tiles are press-conference photography) | File:VIEW DOWN RIVER STREET TO THE EAST FROM THE INT; File:Cash payment timeline on foreclosures.jpg; File:Enright foreclosure notice in The Jersey Journa |
| household_loss | coverr | 1 | 0.0 | 1/0/0 | good (1 item only - provisional verdict, an old man at a window, restrained and on-theme) | an old man looking out of the window |
| japan | pixabay_extra | 1,651 | 25.1 | 507/1144/0 | good (genuine Japan temples, streets and Fuji with some foreign mountain leakage) | shrine, torii, japan, fushimi, nature, temple, kyoto; kyoto, japan, statue, jizo, buddha purnima, japanese; ai generated, lost in tokyo, anime tokyo street, ani |
| japan | nara | 530 | 11.0 | 53/477/0 | mixed (genuine WWII Japan archival plus unrelated modern US Marine photos) | Physical Damage, Okayama, Japan; Japanese aggression in China and activities in Japan; News Events, Japan 1946 |
| japan | mixkit | 89 | 1.1 | 89/0/0 | good (Japanese motion footage; temple keyword dragged in Turkey, Malaysia and Egypt) | Time lapse of a street and mount Fuji; Tokyo Night street with fast traffic and tower; Tokyo cityscape at night |
| japan | unsplash | 50 | 0.3 | 0/50/0 | good (temples, pagodas and neon streets - cleanest source in this theme) | narrow japanese street at night; people near pagoda under white and blue sky; red temple near body of water |
| japan | ia | 16 | 1.9 | 16/0/0 | — | The Enemy Japan--The People; Children of Japan; News Events, Japan 1946: November 1945 - June 1, 194 |
| japan | loc | 15 | 0.7 | 0/15/0 | — | [Untitled photo, possibly related to: Corner of Mont; Pearl Harbor, Hawaii. USS West Virginia aflame.  Dis; Japan, |
| laboratory_forensics | noaa | 9 | 0.0 | 0/9/0 | — | NOAA Earth System Research Laboratory aircraft; Lenticular clouds in Boulder CO - NOAA Earth System ; National Severe Storms Laboratory logo mid-90s |
| laboratory_forensics | ia | 7 | 0.8 | 7/0/0 | — | Yucca Mountain: The Making of an Underground Laborat; Chemistry - Challenges and Solutions ★ "Lost" Annenb; Science in Action: Antibiotics |
| laboratory_forensics | smithsonian | 1 | 0.0 | 0/1/0 | — | Model, Mars Science Laboratory, Mars Rover Curiosity |
| landscapes_timelapse | pixabay_extra | 1,807 | 29.1 | 673/1134/0 | good (waterfalls, peaks and skies - on-theme but visually interchangeable) | dolomites, mountains, snow, time lapse, clouds, wint; sunrise, fog, clouds, landscape, mountain range, alp; clouds, stars, full moon, night sky, light, mood, la |
| landscapes_timelapse | mixkit | 123 | 4.9 | 123/0/0 | good (aerials and cloud or valley timelapses) | Fog on the heights of the snowy mountains; Flying over an arid land with the sun shining over t; Flying over a landscape of sun soaked desert land wi |
| landscapes_timelapse | nasa | 67 | 0.2 | 0/67/0 | — | Earth observation taken by the Expedition 28 crew; Two-Orbit Time Lapse Earth Observation taken with a ; Earth from Orbit 2014 |
| landscapes_timelapse | unsplash | 50 | 0.2 | 0/50/0 | good (high-res landscape stills, heavy on mountains) | aerial photo of mountains during daytime; a person standing on top of a mountain at sunset; Snow-capped mountains bathed in golden sunlight |
| landscapes_timelapse | coverr | 9 | 0.1 | 9/0/0 | good (most PD-relevant: Manhattan and Washington DC timelapses) | timelapse of a house in the mountains; pink sunset timelapse; timelapse of a sunset |
| landscapes_timelapse | ia | 6 | 0.5 | 6/0/0 | good (2 items, clean low-res timelapses) | Timelapse sky; Timelapse of pasture at sunset; Juuson Turha Video Diary - Clouds 26h timelapse |
| legal_court | pexels | 10 | 0.0 | 0/10/0 | — | wooden interior of a courthouse; corner of capitol in washington dc; us capitol in washington dc |
| legal_court | wikimedia | 2 | 0.1 | 0/2/0 | — | judge's gavel; US Constitution page 1 |
| market_machinery | mixkit | 52 | 1.1 | 52/0/0 | mixed (half real mechanisms and infrastructure, half keyword collisions on machinery plus staged corporate performance) | Woman scrolling the web on a tablet; A man lying on the bed scrolling on his phone; Investor scrolling through an investment app on a ta |
| market_machinery | unsplash | 50 | 0.2 | 0/50/0 | good (real mechanical calculating hardware, punch cards, split-flap clocks and numeral displays) | Rows of vintage punched cards with data; a large number of numbers are arranged in rows; Antique dark green mechanical calculating machine on |
| market_machinery | coverr | 8 | 0.1 | 8/0/0 | good (8 items, tightly on-brief: trading desks, phones and chart screens) | a trader making a call with his smartphone; financial analysis of cryptocurrency; crypto wallet |
| medical_lab | pexels | 2 | 0.0 | 0/2/0 | — | laboratory worker using modern hospital equipment; test tubes in a medical equipment |
| misc | pixabay | 107 | 0.3 | 35/72/0 | good (Capitol, Supreme Court, cash, cuffs; a few non-US police clips) | untitled |
| misc | pexels | 57 | 0.5 | 36/21/0 | good (clean modern b-roll: money, justice props, jail bars - interchangeable stock) | black cars on road; people walking at the park during sunset; yellow and white currency strap |
| misc | wikimedia | 3 | 0.1 | 0/3/0 | good (3 items, all core: RBG and Roberts portraits, Bill of Rights parchment) | Bill of Rights parchment; RBG official portrait; CJ Roberts official portrait |
| money_banking | pixabay_extra | 1,501 | 20.7 | 964/537/0 | mixed (generic money stills diluted by wildlife, green screens and lifestyle) | currency, dollars, euro, money, symbol, commerce, ba; cards, coins, gambling, game, money, currency, finan; board, chalk, finance, graphic, diagram, training, s |
| money_banking | wikimedia | 435 | 6.7 | 0/435/0 | — | File:Chip gold bullion bar.jpg; File:Gold bullion 1.jpg; File:Gold bullion bars.jpg |
| money_banking | nara | 211 | 3.1 | 3/208/0 | mixed (Treasury Relief Art Project interiors plus bank false positives such as lighting rigs) | [STOCK NEWSREEL EXCERPTS]; Looking West at Conduit Bank North of Service Equipm; LOAD BANK |
| money_banking | mixkit | 134 | 2.3 | 134/0/0 | good (clean modern money and finance motion - most directly droppable) | Money counting machine counting up money; Close up to a counting money machine; Man counting a wad of bills seen very closely |
| money_banking | loc | 117 | 3.5 | 0/117/0 | — | The old Central Gas Station building in Donaldsonvil; P.S. Duval's Lithographic Establishment and Office o; The neoclassical-style, onetime First National Bank |
| money_banking | unsplash | 50 | 0.2 | 0/50/0 | good (high-res currency stills, very repetitive) | a lot of money sitting on top of a green surface; 1 US dollar banknote; 100 us dollar bill |
| money_banking | ia | 10 | 1.2 | 10/0/0 | good (mid-century educational banking films - strong period b-roll) | Using the Bank; Two Dollar Bettor; What Is Money? |
| money_banking | coverr | 6 | 0.1 | 6/0/0 | — | a screen showing financial analysis of a cryptocurre; a broker working with a candlestick chart; a broker works with a cryptocurrency candlestick cha |
| music_performance_pd_era | ia | 8 | 3.2 | 8/0/0 | — | Command Performance; Music In Motion; The Wiggles - TV Series 1 Episode 14 (Wiggly Concert |
| nature_landscape | pexels | 1 | 0.0 | 0/1/0 | — | people rallying on the street |
| navy_harbor | nara | 478 | 26.8 | 194/284/0 | good (ship decks, harbors, Pearl Harbor damage, crew activity - directly cuttable) | FRENCH SHIPS IN HARBOR & UNDERWAY; JAPANESE SHIPS AWAIT "PEARL HARBOR"; Japanese SHIPS AT KURE HARBOR |
| navy_harbor | loc | 144 | 1.5 | 0/144/0 | — | The islander (Friday Harbor, Wash.), June 17, 1897; The San Juan islander (Friday Harbor, Wash.), August; The San Juan islander (Friday Harbor, Wash.), August |
| navy_harbor | ia | 88 | 5.9 | 88/0/0 | good (real newsreel harbor footage, diluted by the Don Winslow fiction serial) | Don Winslow of the Navy: Chapter 1 - The Human Torpe; Don Winslow of the Navy: Chapter 2 - Flaming Death; 1942 Captured Japanese Newsreel: Pearl Harbor, Hong |
| newspapers_printing | pixabay_extra | 1,020 | 9.7 | 412/608/0 | — | press ups, boy, sports, sweating, crunches, leisure,; hang clean, kettlebell press, kettlebell, kettlebell; newspaper, cat, bird, peace, tolerance, information, |
| newspapers_printing | loc | 164 | 3.6 | 0/164/0 | mixed (excellent pressroom, linotype and newsboy photography plus dead-weight book covers and page scans) | Paul and the printing press,; Specimens of druggists' labels...letter-press printi; The Centennial -- wall paper printing press, Machine |
| newspapers_printing | unsplash | 50 | 0.2 | 0/50/0 | — | Antique printing press machine on a white background; Vintage printing press in a factory setting.; Antique linotype printing machine on a white backgro |
| newspapers_printing | mixkit | 46 | 0.9 | 46/0/0 | — | Burning a newspaper in a campfire; Young adult reading the newspaper; Person reading the newspaper in a park outdoors |
| newspapers_printing | ia | 11 | 1.1 | 11/0/0 | mixed (tiny pool of mid-century industrial films; modern uploads out of focus) | Printing; ADVANCED NEWSPAPER TECHNOLOGY; Media Smart - Part 12 - Roll the Presses! Newspaper |
| newspapers_printing | nara | 6 | 0.6 | 6/0/0 | unusable (8 items, essentially none show printing - keyword false positives) | SOME OF UNCLE SAM"S WORKSHOPS [U.S. POST OFFICE DEPA; FORD RIVER ROUGE PLANT; [PLANT SAFETY] |
| ocean_nature | pixabay_extra | 2,153 | 73.4 | 1010/1143/0 | good (reef life and coastline stills; reef shots repetitive) | beach, ocean, sea, summer, holiday, wave, nature, be; waves, water, sea, ocean, landscape, nature, sunset,; wave, sea, water, sky, power, ocean waves |
| ocean_nature | noaa | 148 | 0.6 | 1/147/0 | good (genuine underwater reef and diver photography, unlike the satellite plates elsewhere) | Mimic goatfish coral reef Howland Island 2023; NOAA diver lays transect on reef Tutuila 2023; NOAA diver measures coral Rose Atoll 2023 |
| ocean_nature | nasa | 132 | 0.6 | 0/132/0 | — | KENNEDY SPACE CENTER, FLA.  -   Purple flowers flow ; Ocean Inside Saturn Moon Enceladus; Typhoon Neoguri is pictured in the Pacific Ocean |
| ocean_nature | mixkit | 56 | 1.9 | 56/0/0 | good (ocean motion: surf, reef fish, coastal boats) | Sea waves breaking on the rocks, front view; Aerial view of long running wave crashing onto shore; Waves reaching the shore |
| ocean_nature | unsplash | 50 | 0.2 | 0/50/0 | good (high-res underwater and open-water stills) | bird's-eye view of sea waves; aerial photography of large body of water and shorel; sea waves during daytime photo |
| ocean_nature | coverr | 24 | 0.2 | 24/0/0 | good (coastal aerials, but 5 of 8 are the same Praia do Pinhao location) | the incoming waves of the ocean gently splash onto t; premium couple observes ocean waves; sandstone cliffs |
| ocean_nature | ia | 14 | 0.9 | 14/0/0 | mixed (2 items; one carries a clideo.com watermark) | Hills and the Sea; Ocean Wave; Venice Beach Ocean Waves Ashley Gershoony Video |
| pd_feature_films | ia | 277 | 137.5 | 277/0/0 | mixed (PD-claimed noir features with the right period texture, but each needs shot-logging and title-by-title rights clearance; several are not actually PD) | The Killers (1946) Burt Lancaster, Ava Gardner, Edmo; Spellbound (1945) Director: Alfred Hitchcock Starrin; Kiss Me Deadly (1955, ) Dir: Robert Aldrich Featurin |
| period_telephone_tech | loc | 57 | 0.2 | 0/57/0 | — | Masters of space: Morse and the telegraph; Thompson ; Letter from J. Sitzenstatter to Alexander Graham Bel; Investigation of telephone companies. Letter from th |
| period_telephone_tech | ia | 15 | 2.1 | 15/0/0 | mixed (Bell-style instructional films; a third land on intertitles or notice cards) | Town and the Telephone, The; Communication: A Film Lesson in General Science / De; Operator Toll Dialing: Teamwork |
| period_telephone_tech | nara | 15 | 1.5 | 10/5/0 | good (genuine switchboard and operator photographs - most on-theme in the set) | Number Please (Telephone Switchboard) / Lumbering; THE TELEPHONE SECTION; [TELEPHONE AND TELEGRAPH COMMUNICATIONS] |
| police_modern | pixabay_extra | 1,466 | 22.5 | 624/842/0 | mixed (real cruisers mixed with Lego toys, AI renders, generic night wallpaper) | night, city, cars, road, lights; futuristic, robots, android, guardian, police, patro; steampunk, guardian, police, patrol, vehicle, futuri |
| police_modern | mixkit | 86 | 2.1 | 86/0/0 | good (staged crime-scene and forensic clips that cut as narrative b-roll) | Police barricade tape at a crime scene; Handcuffed man walking to a police car; Blurry lights form a police car |
| police_modern | unsplash | 50 | 0.2 | 0/50/0 | good (modern patrol-car photography, night and rain - ideal establishing b-roll) | Police cars parked with flashing lights at night.; A police car with its lights on at night; a police car driving down a street at night |
| police_modern | ia | 3 | 0.0 | 3/0/0 | unusable (4 items, none belong: classic features and a screen-recorded agenda) | Monday, 2nd June 1913 Frank Asked Room to Conceal Bo; Monday, 28th April 1913 Police Think Negro Watchman ; Tuesday, 3rd June 1913 Grand Jury Calls for Thos. Fe |
| police_modern | coverr | 1 | 0.0 | 1/0/0 | — | traffic light timer |
| police_period | loc | 194 | 5.4 | 0/194/0 | good (pre-war police stations, squad cars, troop portraits, station interiors) | Police station, Belle Isle; [The Imperial Police Station, Papasköprüsü]; [The Imperial Police Station, Nişantaşı] |
| police_period | nara | 67 | 2.1 | 18/49/0 | unusable (almost entirely 2006 Iraq police-training and 2012 FEMA photos mislabeled as period) | RADIO TRAFFIC & SAFETY PATROLS (JOINT PATROLS AMERIC; [YOUR STATE POLICE]; PATROL IN LEIPZIG RR STATION, GERMANY ; US 26TH DIVI |
| police_period | ia | 2 | 0.3 | 2/0/0 | mixed (2 items only: one period educational film, one unrelated TV comedy) | Youth and the Law; 56 11 18 The Jack Benny Program S 07e 05 Beverly Hil |
| prison_jail | pixabay_extra | 1,531 | 14.4 | 457/1074/0 | — | fence, thorny, razor blade, sharp, barrier, anger, m; attorney, justice, law, legal, face, cell, arrested,; watchtower, guarding, prison, fence, barbedwire, war |
| prison_jail | ia | 115 | 26.1 | 115/0/0 | mixed (half genuine prison film; rest screen recordings, cartoons, game capture) | Prison Mutiny; Prison Shadows; Back Door to Heaven |
| prison_jail | loc | 79 | 0.1 | 0/79/0 | unusable (dominated by scanned Prison Mirror newspaper pages and government letters) | Cell blocks at Occoquan [Workhouse]; Prisons and prison systems of the United States. Let; Military prisons. Letter from the Secretary of War, |
| prison_jail | unsplash | 27 | 0.1 | 0/27/0 | — | Long row of weathered prison cell bars in a corridor; Dark, narrow hallway with bright, barred skylights.; A long hallway with prison cells on the left |
| prison_jail | nara | 20 | 2.0 | 17/3/0 | unusable (Leavenworth inmate case files: forms and mugshots of named prisoners) | JAPANESE PRISON CAMPS (273-X); Prison Ship is Wrecked / Laying Lighthouse Cornersto; Rioting Felons Damage Prison in 8-Hour Row |
| prison_jail | mixkit | 18 | 0.3 | 18/0/0 | — | A shirtless man with metal chain behind the fence; Angry prisoner behind a wire fence; Hand on a wire fence by night |
| property_home | pexels | 5 | 0.0 | 1/4/0 | — | suburban house for sale; brown and white wooden house; suburban house with double garage and greenery |
| retail_commerce | wikimedia | 930 | 10.8 | 0/930/0 | mixed (half the sample is bare department-store logo files; the real photographs nearly all carry a legible shop name) | File:Edward's Department Store Logo.png; File:Forbes & Wallace Department Store Final Logo.pn; File:Frederick & Nelson Department Store Final Logo. |
| retail_commerce | nara | 13 | 0.2 | 1/12/0 | mixed (a few excellent period window displays against Independence NHP paperwork and repeated off-theme naval frames) | Futuristic Department Store; Civil Defense Window Display at Sage Allen Departmen; American Red Cross - War Work - War Activities in Du |
| retail_commerce | loc | 5 | 0.0 | 0/5/0 | unusable (almost entirely paper: regulations, annual reports and book pages, one usable building photograph) | Annual reports of the Post-Office Department for the; Rules and regulations governing the Department of th; Rules and regulations governing the Department of th |
| school_youth | pexels | 2 | 0.0 | 0/2/0 | — | students attending class at international school; students walking in school corridor |
| science_tech | nasa | 1,577 | 8.3 | 0/1577/0 | — | Wind Tunnel Test of Stoppable Rotors in Ames 40x80ft; AVROCAR tested in the NASA Ames 40x80ft Wind Tunnel; Nacelles and props in 40x80 foot wind tunnel at Ames |
| science_tech | pixabay_extra | 1,432 | 15.5 | 730/702/0 | good (circuit-board macros, telescopes, retro computers, office clips) | television, monitor, telecommunication system, scree; anime, coding, programmer, desk, computer, technolog; robot, artificial intelligence, technology, develope |
| science_tech | mixkit | 99 | 1.6 | 99/0/0 | good (data centers, robots, labs; three green-screen or screen-capture plates) | Close up of electronic circuit board; Automated machine places parts on circuit boards; Robot working in an electronics manufacturing facili |
| science_tech | unsplash | 50 | 0.2 | 0/50/0 | good (high-res circuit-board macros and vintage computers) | close up of dark blue circuit board; a close-up of a circuit board; tilt-shift photography of green computer motherboard |
| science_tech | smithsonian | 45 | 0.1 | 0/45/0 | good (19th-c telegraph and instrument artifacts - narrow but excellent) | Microscope; Microscope, Lerebours; Microscope Case |
| science_tech | noaa | 7 | 0.5 | 0/7/0 | mixed (good field and instrument photography plus near-duplicate satellite frames) | PHOTO-IMETs-launch-weather-balloon-2023-IMET-trainin; Weather Balloon release; Smoke Balloons from Chemical Fire in Southeast Texas |
| science_tech | ia | 4 | 0.5 | 4/0/0 | mixed (1 item: UNIVAC commercial, advertising rights unverified) | Classic TV Commercial for a UNIVAC computer; UNIVAC Computer Commercials in 3D; Threads of Technology |
| science_tech | met | 1 | 0.0 | 0/1/0 | good (1 item: celestial globe) | Celestial globe with clockwork |
| selling_floor | pixabay_extra | 551 | 5.6 | 242/309/0 | mixed (largest source and least verifiable: 6 of 9 sampled tiles missing on disk, two carrying pure landscape keywords) | tailor, clothing, fashion designer, tailor shop; tailor, clothing, folding, shirt, shop, textiles, cl; kid, teenager, shopping, 3d, sale, cartoon, boy, man |
| selling_floor | unsplash | 50 | 0.2 | 0/50/0 | good (strong and low-risk closure signage, but 13 of 14 tiles are a CLOSED or SALE sign - no more than two per film) | Busy shopping arcade with escalators and people.; Grand interior of a department store with multiple l; Mannequins display clothing in a well-lit retail sto |
| selling_floor | mixkit | 44 | 0.9 | 44/0/0 | mixed (good unbranded merchandise close-ups alongside fog, football, models and staged retail actors) | T-shirts on hangers at fashion store; Clothing store panning; Sweaters hanging on the coat rack of a clothing stor |
| selling_floor | coverr | 3 | 0.0 | 3/0/0 | good (3 items, real observational queue footage; every one contains a live shop fascia and pedestrian faces) | socially distanced queue; queue to carrefour market in paris; queue to a newspaper store |
| sfx_environment | freesound | 2,819 | 14.9 | 0/0/2819 | — | Distant Thunder and Rain from Half Open Window 2.aif; Distant Thunder and Rain from Half Open Window 1.aif; thunder.rumble.ogg |
| sfx_human_movement | freesound | 2,739 | 1.9 | 0/0/2739 | — | Footsteps in Factory Hall on Wood and Concrete.wav; Footsteps on concrete; footsteps boots int walk through melted ice on concr |
| sfx_mechanical | freesound | 1,629 | 2.1 | 0/0/1629 | — | Creaking Door #3; Creaking Door #2; DOOR CREAKS CLOSES 2.wav |
| small_town | pixabay_extra | 1,196 | 20.0 | 491/705/0 | mixed (town-square scraping filled it with European and Latin American squares) | san antonio, urban, pedestrians, riverwalk, people, ; broadway, street, new york, crossing, usa, america, ; las vegas, usa, america, vegas, nevada, street, city |
| small_town | loc | 404 | 23.7 | 0/404/0 | good (large-format main-street and courthouse-square photographs - exactly what PD needs) | Main street of Bourne, ghost mining town. Oregon; Main street of old mining town. Leadville, Colorado; Building on main street, Halifax, North Carolina |
| small_town | unsplash | 50 | 0.2 | 0/50/0 | good (modern American small-town streets and aerials) | Small building with trees and cloudy sky; Sunny covered walkway with pillars, storefronts, and; Quiet town street with buildings, traffic signals, a |
| small_town | nara | 49 | 1.0 | 6/43/0 | unusable (park-service survey paperwork and microfilm catalogue cards) | Mine Town / Freighter / Child Playing; INFANTRY MOVES, HAULOVICE (?) CZECHOSLOVAKIA ; 105MM; New York City Harbor and Bridges / Buffalo Bill Cody |
| small_town | ia | 24 | 4.3 | 24/0/0 | good (mid-century social and educational films giving period Americana) | Social Class in America; Poverty in Rural America; America's Funniest Home Videos - Season 19 |
| space_nasa | nasa | 9,453 | 362.4 | 630/8823/0 | good (orbital Earth-observation stills plus launch, pad and hardware photography) | Weighing in on the Dumbbell Nebula; Planetary Nebula; Trifid Nebula |
| space_nasa | ia | 66 | 9.3 | 66/0/0 | unusable (2 items, both fiction entertainment mislabeled pd) | Teenagers from Outer Space; Evil Brain From Outer Space; Attack from Space |
| space_nasa | smithsonian | 12 | 0.0 | 0/12/0 | good (rocket-hardware artifact stills, all one visual register) | Spacecraft, New Horizons, Mock-up, model; Rocket Engine, Liquid Fuel, Navajo Missile; Rocket Engine, Liquid Fuel, Apollo Lunar Module Asce |
| stock_market_exchange | wikimedia | 454 | 5.0 | 0/454/0 | mixed (excellent exchange buildings and period Wall Street against an equal pile of scanned share certificates; 10 of 35 sampled tiles missing on disk) | File:Brussels Stock Exchange (1).jpg; File:Brussels Stock Exchange (2).jpg; File:Brussels Stock Exchange (3).jpg |
| stock_market_exchange | nara | 1 | 0.2 | 1/0/0 | unusable (single item, sampled frame is pure black, license review_required) | [STOCK NEWSREEL EXCERPTS] |
| surveillance_tech | pexels | 11 | 0.0 | 2/9/0 | — | social media apps on smartphone; man holding a smart phone with a photo; surveillance cameras in city |
| textures_backgrounds | smithsonian | 575 | 1.6 | 0/575/0 | good (pattern engravings and porcelain; some frames show page edges) | Repeating Pattern Designs for Borders; Design for Embroidery Pattern; Design for Emrboidery Pattern |
| textures_backgrounds | pixabay_extra | 469 | 15.4 | 469/0/0 | good (smoke, bokeh, fluid-ink and abstract light loops - overlay grade) | slow, beautiful wallpaper, yellow, abstract, macro, ; ink, abstract, art, wave, fog, smoke, blue, pink, wa; paints, water, watercolor, painting, ink, texture, l |
| textures_backgrounds | mixkit | 148 | 6.0 | 148/0/0 | good (smoke, ink and bokeh motion textures; two stylized character clips) | Black ink on white background; Black background with smoke foreground; White smoke with black background |
| textures_backgrounds | unsplash | 50 | 0.3 | 0/50/0 | good (large-format concrete, paper and parchment grounds - best behaved source) | white and black marble surface; weathered teal concrete wall texture; a close up of a black marble surface |
| textures_backgrounds | met | 19 | 0.1 | 0/19/0 | good (textile and object scans; one frame has a colour chart) | Embroidery Pattern with Seven Six-pointed Stars and ; Nose ornament in the shape of a head; Pectoral Disc Ornament |
| textures_backgrounds | coverr | 2 | 0.0 | 2/0/0 | good (2 items, both bokeh light loops) | blurred christmas lights; hookah lights |
| textures_backgrounds | ia | 1 | 0.1 | 1/0/0 | good (1 item: 1950s industrial film) | Industry on Parade: Paperman's Paper, Ink Inc., Use |
| uk_highstreet_postoffice | loc | 73 | 1.0 | 0/73/0 | — | Possibilities of the Post Office. February 23, 1901.; Post-office appropriation bill. May 2, 1898. -- Orde; Pacific Mail Steamship Company. May 19, 1874. -- Rec |
| uk_period | loc | 76 | 0.4 | 0/76/0 | — | Madison County Democrat (London, Ohio), March 13, 19; Madison County Democrat (London, Ohio), October 16, ; Madison County Democrat (London, Ohio), July 31, 195 |
| uk_period | nara | 41 | 2.5 | 17/24/0 | unusable (only 23% genuine British; rest is New England Bowling League newsletters and French/Belgian cards) | THE BOMBING OF LONDON; V-E Day, Paris and London, 1945; MISC SCENES, LONDON, ENGLAND, WALES |
| uk_period | ia | 1 | 0.4 | 1/0/0 | good (1 item: steam-railway film, sample too small for confidence) | ' Reflections On Western Steam Vol 2. Through The Ch |
| urban_night | pexels | 5 | 0.0 | 0/5/0 | — | street in toyohashi city japan at night; crowded city street with diverse group of people; cars on miami highway during daytime |
| vintage_ads_cartoons | ia | 104 | 16.3 | 104/0/0 | unusable (about three quarters is ripped third-party studio animation and off-air 1990s breaks; only ~9 tiles are genuine period live-action ads) | Fifties Advertising: UNIVAC Computer Commercial (5 F; Classic Commercial for Du Mont Laboratories Televisi; A 5th Classic Commercial for Coca-Cola (20/January/1 |
| war_history | nara | 1,228 | 44.0 | 264/964/0 | mixed (genuine WWII/Korea/Vietnam combat film; a third is caption cards and near-black leader) | USS TIRANTE COMBAT FILM; USS TIRANTE (SS-420) COMBAT FILM; GSAP Combat Film |
| war_history | ia | 229 | 19.9 | 229/0/0 | — | Why We Fight: Prelude to War; Universal Newsreel Volume 35, Release 2, 01/01/1962; Universal Newsreel Volume 36, Release 96, 11/24/1963 |
| war_history | loc | 2 | 0.2 | 0/2/0 | good (2 items, both large clean archival stills) | Troops of the 185th Inf., 40th Div., take cover behi; Production. M-4 tanks. Hull members of an M-4 tank o |
| weather_disasters | nasa | 199 | 1.6 | 0/199/0 | — | Hurricane Matthew from Space; A view of Hurricane Hilary from space; RapidScat and Hurricane Patricia |
| weather_disasters | noaa | 39 | 0.2 | 39/0/0 | unusable (32/44 tiles are featureless top-down flood-survey plates; 85-90% dead weight as b-roll) | Clear skies reveal tornado scar in Mississippi (CIRA; Destructive Tornado in Southern Michigan (CIRA 2026-; Destructive Tornado in Southern Michigan (CIRA 2026- |
| weather_disasters | ia | 21 | 1.9 | 21/0/0 | good (4 items, all shootable: archival disaster films and 8K GOES timelapses) | Satellite time lapse, GOES-E 2021-07 8K UHD, Hurrica; Satellite time lapse, GOES-E 2021-08 8K UHD, Hurrica; Shock Troops of Disaster: The Story of the New Engla |
| wildlife_animals | pixabay_extra | 2,452 | 48.0 | 1031/1421/0 | mixed (technically clean but 1280x853 - too low-res for the 4K pipeline, heavy deer duplication) | cranes, flock of birds, nature, animals, birds, wild; birds, nest, flock, forest, wildlife, animals, natur; crows, beautiful wallpaper, birds, wildlife, animal, |
| wildlife_animals | noaa | 322 | 1.3 | 1/321/0 | good (public-domain marine-sanctuary photography, archival grade) | Humpback whale Fournier Bay Robert Pitman NOAA PS9; North Pacific right whale (Eubalaena japonica) - Joh; Rice's whale close to surface |
| wildlife_animals | smithsonian | 99 | 0.1 | 0/99/0 | mixed (two-thirds contamination from butterfly matching non-animals) | The Butterfly; Butterfly over Water; Butterfly |
| wildlife_animals | mixkit | 76 | 1.3 | 76/0/0 | good (real animal motion, but most clips are 1280x720) | Deer looking at the camera in the forest; Herd of deer in the forest; Pair of brown bears in the field |
| wildlife_animals | unsplash | 50 | 0.2 | 0/50/0 | good (highest-res stills on the shelf, but 8 of 9 tiles are the same deer) | brown deer under tree; red and gray deer; deer on grass field photography |
| wildlife_animals | met | 3 | 0.0 | 0/3/0 | mixed (3 items, two are antiquities that matched on horse) | Study of a Bird; Horses Harnessed to a Chariot; Tympanum with a Horse and Rider |
| wildlife_animals | ia | 2 | 0.2 | 2/0/0 | — | King Spruce Hen puts on a show for the largest flock; OUR WILDLIFE RESOURCES |
| world_cities | pixabay_extra | 1,341 | 20.9 | 578/763/0 | good (clean city stills and skylines from many countries) | dubai, architecture, city, building, uae, tourism, t; blood moon, lunar eclipse, hyperlapse, seoul citysca; night, harbour, people, car, automobile, city, urban |
| world_cities | mixkit | 128 | 5.3 | 128/0/0 | good (aerials, traffic plates and city timelapses - the motion supply) | Side by side aerial view of a city at night; Aerial view of the glass corporate buildings of a bi; Quiet Tokyo street at night |
| world_cities | nara | 78 | 3.3 | 26/52/0 | mixed (half archival city film, half scanned park-service paperwork) | Harvard-Cambridge City Council; [TRAFFIC]; MERRILY WE ROLL ALONG [COUNTRY AND CITY SCENES] |
| world_cities | unsplash | 50 | 0.2 | 0/50/0 | good (night skylines and street-level views; several very dark) | aerial city view; full moon over city skyline during night time; a city skyline at night |
| world_cities | coverr | 6 | 0.1 | 6/0/0 | good (street-level video: pedestrians, signals, US road plates) | cars in the city at night; street in mexico city; timelapse of buenos aires |
| world_cities | ia | 3 | 0.4 | 3/0/0 | good (1 item: sepia period film) | Wonderful World; Big City, 1958; New York City Scenics |

## 2a. MOVING FOOTAGE by subject — 350 subjects with >= 3 clips

This is the scarce resource. Take stills only when no clip exists.

| subject | clips | top themes (clips only) | example clip |
|---|---:|---|---|
| nature | 1952 | wildlife_animals:463, ocean_nature:387 | `mixkit__41575__traveling-on-a-nature-road-at-dusk.mp4` |
| city | 1723 | government_buildings:850, world_cities:498 | `coverr__5837__cars-in-the-city-at-night.mp4` |
| sea | 1158 | ocean_nature:763, landscapes_timelapse:89 | `ia__0991-hills-and-the-sea-01-19-57-20__hills-and-the-sea.mp4` |
| water | 1068 | ocean_nature:398, wildlife_animals:205 | `mixkit__45611__ocean-water-moving-calmly.mp4` |
| ocean | 1059 | ocean_nature:848, landscapes_timelapse:43 | `coverr__3079__the-incoming-waves-of-the-ocean-gently-splash-onto-the-shore.mp4` |
| landscape | 1013 | landscapes_timelapse:411, japan:178 | `mixkit__52012__flying-over-a-landscape-of-sun-soaked-desert-land-with-majes.mp4` |
| wildlife | 864 | wildlife_animals:782, ocean_nature:25 | `ia__33-451-r-1-2__our-wildlife-resources.mp4` |
| road | 752 | small_town:288, police_modern:173 | `ia__on-the-road-istanbul-sringar__on-the-road-istanbul-sringar.mp4` |
| council | 648 | government_buildings:642, world_cities:2 | `ia__committee-04-02-2012__city-council-committee-meeting-april-2nd-2012.mp4` |
| sky | 640 | landscapes_timelapse:260, ocean_nature:52 | `ia__timelapsesky__timelapse-sky.mp4` |
| beach | 632 | ocean_nature:391, landscapes_timelapse:58 | `coverr__9330__eroded-cliffs-on-praia-do-pinh-o-beach.mp4` |
| sunset | 622 | landscapes_timelapse:313, ocean_nature:118 | `coverr__4178__pink-sunset-timelapse.mp4` |
| forest | 622 | wildlife_animals:218, courtroom_justice:82 | `mixkit__10076__deer-looking-at-the-camera-in-the-forest.mp4` |
| animal | 592 | wildlife_animals:386, ocean_nature:69 | `mixkit__22013__3d-printing-a-cartoon-animal.mp4` |
| background | 580 | textures_backgrounds:168, government_buildings:73 | `mixkit__489__black-ink-on-white-background.mp4` |
| architecture | 568 | government_buildings:307, world_cities:131 | `ia__gov-gsa-historic-portland-1__at-the-forefront-of-adventure-and-architecture-pioneer-court.mp4` |
| aerial | 564 | landscapes_timelapse:240, ocean_nature:93 | `ia__npc-5630__aerial-views-ww2-new-ireland-island-simpson-harbor-rapapo-ta.mp4` |
| drone | 552 | landscapes_timelapse:199, world_cities:72 | `ia__20130206seattlecitycouncildrones__seattle-city-council-public-safety-civil-rights-and-technolo.mp4` |
| beautiful | 541 | government_buildings:187, textures_backgrounds:114 | `coverr__8352__beautiful-rocky-shoreline.mp4` |
| traffic | 537 | world_cities:234, police_modern:173 | `coverr__9024__pedestrian-traffic-light.mp4` |
| flag | 532 | government_buildings:476, small_town:19 | `mixkit__13312__flag-of-china-waving-in-the-wind.mp4` |
| space | 531 | space_nasa:412, science_tech:21 | `ia__plan-9-from-outer-space-202009__plan-9-from-outer-space-full-movie.mp4` |
| city council | 529 | government_buildings:527, world_cities:2 | `ia__committee-04-02-2012__city-council-committee-meeting-april-2nd-2012.mp4` |
| clouds | 502 | landscapes_timelapse:329, ocean_nature:23 | `ia__juusonturhavideodiary-clouds26htimelapse__juuson-turha-video-diary-clouds-26h-timelapse-3.mp4` |
| man | 496 | courtroom_justice:154, hands_and_transactions:61 | `coverr__4931__an-old-man-looking-out-of-the-window.mp4` |
| wallpaper | 475 | government_buildings:176, textures_backgrounds:99 | `ia__the-lazarus-man-s-1-e-09-the-wallpaper-prison__the-lazarus-man-s1e09-the-wallpaper-prison.mp4` |
| bird | 466 | wildlife_animals:353, prison_jail:21 | `pixabay_extra__v_30448__hummingbird-feeder-backyard-flock-anna-s-flying-bird-wildlif.mp4` |
| technology | 449 | science_tech:320, police_modern:22 | `ia__0559-threads-of-technology__threads-of-technology.mp4` |
| waves | 442 | ocean_nature:289, textures_backgrounds:51 | `coverr__3079__the-incoming-waves-of-the-ocean-gently-splash-onto-the-shore.mp4` |
| business | 421 | money_banking:157, business_corporate:100 | `ia__37600-201704__in-us-town-that-embraces-refugees-auto-shop-business-flouris.mp4` |
| beautiful wallpaper | 421 | government_buildings:174, textures_backgrounds:94 | `pixabay_extra__v_218714__beach-ocean-sea-summer-holiday-wave-nature-beautiful-beautif.mp4` |
| street | 415 | world_cities:211, courtroom_justice:35 | `coverr__3879__street-in-mexico-city.mp4` |
| meeting | 415 | government_buildings:397, business_corporate:5 | `ia__committee-04-02-2012__city-council-committee-meeting-april-2nd-2012.mp4` |
| night | 411 | world_cities:113, police_modern:64 | `coverr__5837__cars-in-the-city-at-night.mp4` |
| money | 410 | money_banking:403, hands_and_transactions:2 | `ia__whatismo1947__what-is-money.mp4` |
| abstract | 410 | textures_backgrounds:205, money_banking:64 | `mixkit__44818__abstract-video-of-a-liquid-with-dark-ink-flowing.mp4` |
| green | 409 | money_banking:92, economy_crisis:70 | `ia__green-archer-ep1__green-archer-the-chapter-1-prison-bars-beckon.mp4` |
| building | 407 | government_buildings:162, world_cities:71 | `coverr__6636__a-glass-building-in-lisbon.mp4` |
| walking | 403 | courtroom_justice:295, wildlife_animals:33 | `coverr__8360__walking-to-the-mountain-top.mp4` |
| underwater | 387 | ocean_nature:352, textures_backgrounds:29 | `mixkit__43088__woman-swimming-underwater.mp4` |
| people | 372 | courtroom_justice:73, selling_floor:66 | `mixkit__23042__business-people-signing-contracts.mp4` |
| trees | 369 | wildlife_animals:65, landscapes_timelapse:62 | `pixabay_extra__v_311415__nature-pond-lake-water-forest-trees-geese-swimming-bird-wild.mp4` |
| japan | 366 | japan:303, courtroom_justice:38 | `ia__children1941__children-of-japan.mp4` |
| woman | 364 | hands_and_transactions:95, courtroom_justice:56 | `ia__thewomaninthewindow1944__the-woman-in-the-window-1944-fritz-lang-edward-g-robinson-jo.mp4` |
| coast | 363 | ocean_nature:231, landscapes_timelapse:18 | `mixkit__4078__ocean-waves-bursting-on-the-shore-of-the-coast.mp4` |
| urban | 360 | world_cities:186, government_buildings:65 | `mixkit__3516__urban-view-from-a-rooftop-and-the-sunset.mp4` |
| computer | 355 | science_tech:265, newspapers_printing:31 | `ia__univac-commercial-classic-old-vintage__classic-tv-commercial-for-a-univac-computer.mp4` |
| generated | 347 | science_tech:46, prison_jail:42 | `pixabay_extra__v_365918__ai-generated-steampunk-robot-vintage-car-driver-vehicle-retr.mp4` |
| country | 344 | government_buildings:282, small_town:25 | `ia__germany-country-under-the-rule-of-law-role-model-or-illusion__germany-country-under-the-rule-of-law-role-model-or-illusion.mp4` |
| lights | 337 | textures_backgrounds:167, police_modern:70 | `coverr__284__blurred-christmas-lights.mp4` |
| mountains | 335 | landscapes_timelapse:195, small_town:33 | `coverr__4021__timelapse-of-a-house-in-the-mountains.mp4` |
| car | 333 | police_modern:182, small_town:47 | `mixkit__49329__handcuffed-man-walking-to-a-police-car.mp4` |
| symbol | 333 | government_buildings:277, money_banking:21 | `pixabay_extra__v_5433__currency-dollars-euro-money-symbol-commerce-bank-business-in.mp4` |
| travel | 331 | world_cities:61, ocean_nature:56 | `mixkit__41540__aerial-travel-above-a-highway-in-the-city.mp4` |
| screen | 321 | money_banking:91, economy_crisis:76 | `coverr__3490__a-screen-showing-financial-analysis-of-a-cryptocurrency.mp4` |
| river | 316 | landscapes_timelapse:52, world_cities:41 | `mixkit__8097__shallow-river-flowing-through-a-canyon.mp4` |
| cars | 290 | world_cities:95, police_modern:85 | `coverr__5837__cars-in-the-city-at-night.mp4` |
| wave | 283 | ocean_nature:227, textures_backgrounds:12 | `ia__ocean-wave__ocean-wave.mp4` |
| running | 276 | newspapers_printing:256, wildlife_animals:6 | `mixkit__719__man-running-on-trail-in-the-park.mp4` |
| mountain | 275 | landscapes_timelapse:129, japan:44 | `mixkit__52426__an-arid-natural-landscape-with-a-mountain-in-the-distance-an.mp4` |
| nature landscape | 273 | landscapes_timelapse:136, ocean_nature:27 | `pixabay_extra__v_198549__sky-clouds-mountains-cloudscape-drone-aerial-nature-landscap.mp4` |
| buildings | 271 | world_cities:112, government_buildings:108 | `mixkit__49845__aerial-view-of-the-glass-corporate-buildings-of-a-big-city-a.mp4` |
| motion | 270 | wildlife_animals:63, prison_jail:45 | `mixkit__27133__flock-of-pigeons-on-the-street-slow-motion.mp4` |
| light | 269 | textures_backgrounds:61, police_modern:32 | `mixkit__50948__a-light-trail-of-smoke-twirls-and-unfurls-over-a-dark-backgr.mp4` |
| sun | 258 | landscapes_timelapse:110, ocean_nature:42 | `mixkit__52009__flying-over-an-arid-land-with-the-sun-shining-over-the-mesme.mp4` |
| design | 256 | prison_jail:60, government_buildings:60 | `pixabay_extra__v_101446__art-black-light-pattern-smoke-curve-motion-texture-design-co.mp4` |
| finance | 256 | money_banking:241, business_corporate:8 | `pixabay_extra__v_91678__cards-coins-gambling-game-money-currency-finance-casino-happ.mp4` |
| highway | 255 | small_town:131, world_cities:42 | `ia__freedomh1956__freedom-highway-part-i.mp4` |
| blue | 254 | ocean_nature:93, textures_backgrounds:29 | `ia__thebluegardenia1953__the-blue-gardenia-1953-dir-fritz-lang-featuring-anne-baxter.mp4` |
| sea ocean | 246 | ocean_nature:187, landscapes_timelapse:20 | `pixabay_extra__v_22183__waves-water-sea-ocean-landscape-nature-sunset-coast.mp4` |
| plumage | 239 | wildlife_animals:204, courtroom_justice:12 | `pixabay_extra__v_191159__gull-bird-snow-plumage-sitting-winter-wildlife.mp4` |
| wild | 236 | wildlife_animals:181, ocean_nature:10 | `mixkit__11059__a-herd-of-elephants-grazing-in-the-wild.mp4` |
| ocean sea | 233 | ocean_nature:182, wildlife_animals:16 | `pixabay_extra__v_218714__beach-ocean-sea-summer-holiday-wave-nature-beautiful-beautif.mp4` |
| bokeh | 232 | textures_backgrounds:199, world_cities:11 | `mixkit__45355__bokeh-lights-on-a-black-background.mp4` |
| office | 230 | business_corporate:79, science_tech:52 | `ia__gov-gsa-historic-pittsburgh__a-monument-reborn-u-s-post-office-courthouse-pittsburgh-pa.mp4` |
| fish | 230 | ocean_nature:199, wildlife_animals:8 | `mixkit__44868__beautiful-coral-reef-with-exotic-reef-fish.mp4` |
| smoke | 226 | textures_backgrounds:205, money_banking:8 | `mixkit__1968__black-background-with-smoke-foreground.mp4` |
| reef | 225 | ocean_nature:224, wildlife_animals:1 | `ia__scuba-dive-the-coral-sea-great-barrier-reef-1989__scuba-dive-the-coral-sea-great-barrier-reef-1989.mp4` |
| sunrise | 224 | landscapes_timelapse:88, ocean_nature:30 | `coverr__9808__sunrise-at-the-beach-dock.mp4` |
| green screen | 223 | money_banking:71, economy_crisis:59 | `mixkit__52076__on-a-round-table-the-hands-of-a-young-man-start-typing-on-a.mp4` |
| council meeting | 221 | government_buildings:219, small_town:1 | `ia__council-08-08-2011__city-council-meeting-august-8th-2011.mp4` |
| ground | 218 | space_nasa:205, wildlife_animals:2 | `nasa__jsc2020m000053_Space_to_Ground_352_201223__space-to-ground-the-year-that-was-12-23-2020.mp4` |
| coral | 212 | ocean_nature:210, war_history:1 | `ia__0436-coral-wonderland-01-00-02-00__coral-wonderland.mp4` |
| science | 211 | science_tech:128, space_nasa:32 | `ia__gov-ntis-ava20966vnb1-2__science-in-the-courtroom-program-5-basic-principles-of-epide.mp4` |
| harbor | 211 | navy_harbor:187, goods_in_motion:11 | `ia__npc-10134__1942-captured-japanese-newsreel-pearl-harbor-hong-kong.mp4` |
| summer | 210 | ocean_nature:63, landscapes_timelapse:34 | `pixabay_extra__v_218714__beach-ocean-sea-summer-holiday-wave-nature-beautiful-beautif.mp4` |
| currency | 204 | money_banking:204 | `pixabay_extra__v_5433__currency-dollars-euro-money-symbol-commerce-bank-business-in.mp4` |
| space ground | 204 | space_nasa:204 | `nasa__jsc2020m000053_Space_to_Ground_352_201223__space-to-ground-the-year-that-was-12-23-2020.mp4` |
| house | 202 | economy_crisis:47, prison_jail:34 | `coverr__4021__timelapse-of-a-house-in-the-mountains.mp4` |
| vehicle | 202 | police_modern:146, world_cities:22 | `ia__louisianasupremecourtallowsvehiclesearchesonahunch__louisiana-supreme-court-allows-vehicle-searches-on-a-hunch.mp4` |
| nation | 202 | government_buildings:186, small_town:10 | `ia__house-hbs-blur-06-e__advancing-public-alert-and-warning-systems-to-build-a-more-r.mp4` |
| winter | 200 | wildlife_animals:28, landscapes_timelapse:24 | `pixabay_extra__v_191159__gull-bird-snow-plumage-sitting-winter-wildlife.mp4` |
| state | 197 | government_buildings:182, small_town:9 | `ia__soc2017a__east-grand-forks-state-of-the-city-2017.mp4` |
| ink | 196 | textures_backgrounds:174, police_modern:6 | `ia__papermans-paper__industry-on-parade-paperman-s-paper-ink-inc-use-and-discard.mp4` |
| netherlands | 194 | police_modern:65, small_town:50 | `nara__77741-219251798__princess-juliana-of-the-netherlands-christens-ss-jan-pieters.mp4` |
| temple | 193 | japan:191, landscapes_timelapse:1 | `mixkit__20072__kyoto-historic-temple-with-tourism.mp4` |
| snow | 190 | wildlife_animals:32, landscapes_timelapse:29 | `mixkit__7311__eagle-in-the-snow-closeup-facing-the-camera.mp4` |
| lake | 189 | wildlife_animals:60, japan:31 | `mixkit__41398__touring-a-lake-in-nature-from-the-top.mp4` |
| time | 185 | landscapes_timelapse:74, world_cities:25 | `ia__goes-e-2021-07-8k__satellite-time-lapse-goes-e-2021-07-8k-uhd-hurricane-elsa.mp4` |
| launch | 184 | space_nasa:180, newspapers_printing:2 | `nasa__ksc-20230507-mh-rls01-tropics-rocket-launch-rocket-lab-won-3__tropics-rocket-launch.mp4` |
| hands | 180 | hands_and_transactions:68, courtroom_justice:43 | `ia__0555-master-hands-18-27-28-00__master-hands.mp4` |
| port | 178 | government_buildings:114, goods_in_motion:36 | `ia__cityofportorfordoregon-councilmeetingapril7th2011__city-of-port-orford-oregon-council-meeting-april-7th-2011.mp4` |
| cash | 175 | money_banking:172, bank_and_branch:1 | `mixkit__47005__a-lot-of-cash-over-a-rotating-background.mp4` |
| robot | 175 | science_tech:168, police_modern:4 | `ia__gov-ntis-ava19272__robot-reality.mp4` |
| animals | 175 | wildlife_animals:85, ocean_nature:50 | `mixkit__11239__herds-of-african-animals-on-a-vast-plain.mp4` |
| deer | 173 | wildlife_animals:169, newspapers_printing:2 | `mixkit__10076__deer-looking-at-the-camera-in-the-forest.mp4` |
| tree | 170 | wildlife_animals:34, landscapes_timelapse:23 | `mixkit__4027__huge-argan-tree-in-the-savanna.mp4` |
| drone aerial | 169 | landscapes_timelapse:141, ocean_nature:7 | `pixabay_extra__v_198549__sky-clouds-mountains-cloudscape-drone-aerial-nature-landscap.mp4` |
| transport | 168 | police_modern:50, small_town:38 | `ia__npc-4420__invasion-of-france-barges-landing-craft-in-transport-area-ca.mp4` |
| wind | 167 | government_buildings:51, japan:23 | `mixkit__13312__flag-of-china-waving-in-the-wind.mp4` |
| station | 167 | space_nasa:122, japan:10 | `ia__561118thejackbennyprograms07e05beverlyhillspolicestation__56-11-18-the-jack-benny-program-s-07e-05-beverly-hills-polic.mp4` |
| black | 165 | textures_backgrounds:38, hands_and_transactions:22 | `mixkit__489__black-ink-on-white-background.mp4` |
| red | 165 | wildlife_animals:27, textures_backgrounds:20 | `ia__the-red-house__the-red-house-full-film-4k-a-haunting-1940s-thriller-with-ed.mp4` |
| coffee | 165 | hands_and_transactions:93, selling_floor:21 | `mixkit__45745__close-up-shot-of-an-office-worker-sipping-on-a-coffee-at-the.mp4` |
| ship | 164 | goods_in_motion:106, ocean_nature:17 | `coverr__2381__view-of-the-ocean-from-a-cruise-ship.mp4` |
| work | 162 | science_tech:49, business_corporate:26 | `ia__arc-38908__june-1942-newsreel-molotov-lend-lease-bomber-ferry-war-work.mp4` |
| futuristic | 162 | science_tech:103, police_modern:12 | `mixkit__5579__futuristic-diagrams-of-dna-scans-in-modern-lab.mp4` |
| bridge | 159 | world_cities:44, government_buildings:30 | `mixkit__1606__city-train-driving-under-a-bridge.mp4` |
| rain | 157 | prison_jail:27, money_banking:22 | `ia__esolany-ii__seth-f-henriett-fajcsak-henrietta-esolany-ii-rain-girl-2-tel.mp4` |
| autumn | 157 | japan:32, small_town:25 | `pixabay_extra__v_82366__mountain-volcano-snow-sunset-tokyo-fuji-lake-asian-autumn-tr.mp4` |
| newsreel | 157 | war_history:145, navy_harbor:3 | `ia__universalnewsreelvolume35release201-01-1962__universal-newsreel-volume-35-release-2-01-01-1962.mp4` |
| cartoon | 157 | government_buildings:47, newspapers_printing:23 | `mixkit__22013__3d-printing-a-cartoon-animal.mp4` |
| war | 155 | courtroom_justice:91, war_history:47 | `ia__adc-10018__sentencing-of-nazi-war-leaders-at-nuremberg-10-1946.mp4` |
| room | 152 | prison_jail:70, courtroom_justice:15 | `ia__powder-room-prison__powder-room-prison.mp4` |
| empty | 152 | courtroom_justice:141, prison_jail:6 | `ia__adl-anti-defamation-league-behind-the-mask-of-respectability__adl-behind-the-empty-mask-of-respectability.mp4` |
| white | 151 | wildlife_animals:48, textures_backgrounds:18 | `ia__gov-gsa-historic-denver__a-poem-in-marble-a-place-on-the-map-byron-r-white-u-s-courth.mp4` |
| old | 150 | courtroom_justice:36, world_cities:26 | `ia__castaoca-000170__old-orange-county-courthouse-ceremony.mp4` |
| home | 150 | prison_jail:33, courtroom_justice:20 | `ia__098550__home-movie-098550-sausage-factory-in-michigan.mp4` |
| loop | 149 | money_banking:49, science_tech:34 | `mixkit__31534__futuristic-virtual-city-highway-loop-video.mp4` |
| young | 149 | hands_and_transactions:37, courtroom_justice:24 | `ia__citythatneversleeps1953usafeaturinggigyoungwilliamtalmanfilm__city-that-never-sleeps-1953-gig-young-william-talman-film-no.mp4` |
| bank | 147 | money_banking:146, ocean_nature:1 | `ia__usingthe1947__using-the-bank.mp4` |
| rocks | 146 | ocean_nature:78, newspapers_printing:17 | `mixkit__9294__sea-waves-breaking-on-the-rocks-front-view.mp4` |
| invasion | 146 | war_history:136, navy_harbor:9 | `ia__arc-38987__november-1943-newsreel-usmc-invasion-capture-of-tarawa-cairo.mp4` |
| construction | 145 | government_buildings:86, goods_in_motion:27 | `mixkit__4010__buildings-under-construction-aerial-view.mp4` |
| sky clouds | 144 | landscapes_timelapse:122, small_town:5 | `pixabay_extra__v_198549__sky-clouds-mountains-cloudscape-drone-aerial-nature-landscap.mp4` |
| mammal | 143 | wildlife_animals:124, small_town:5 | `pixabay_extra__v_260654__zebra-nature-animal-wildlife-mammal-safari-africa-fauna-spec.mp4` |
| park | 142 | courtroom_justice:34, world_cities:25 | `mixkit__17901__park-and-a-bench-with-fallen-leaves.mp4` |
| japanese | 142 | japan:79, navy_harbor:27 | `ia__npc-10134__1942-captured-japanese-newsreel-pearl-harbor-hong-kong.mp4` |
| opening | 142 | money_banking:80, hands_and_transactions:46 | `ia__200333-panama-pacific-international-exposition-opening-parad__panama-pacific-international-exposition-opening-parade.mp4` |
| fog | 142 | landscapes_timelapse:41, courtroom_justice:30 | `mixkit__4396__fog-on-the-heights-of-the-snowy-mountains.mp4` |
| transportation | 142 | police_modern:54, world_cities:33 | `ia__usaf-11069__japanese-transportation-equipment-04-14-1946-06-01-1946.mp4` |
| birds | 139 | wildlife_animals:86, prison_jail:10 | `mixkit__11120__a-flock-of-cockatoo-birds-flying-away.mp4` |
| driving | 137 | police_modern:90, small_town:19 | `mixkit__4521__blonde-woman-driving-on-road.mp4` |
| coastline | 136 | ocean_nature:130, japan:2 | `coverr__6947__praia-do-pinh-o-coastline.mp4` |
| skyline | 136 | world_cities:113, business_corporate:8 | `mixkit__27095__frankfurt-city-skyline-in-the-morning-aerial-view.mp4` |
| lapse | 136 | landscapes_timelapse:70, world_cities:26 | `mixkit__4070__time-lapse-of-a-green-meadow.mp4` |
| tropical | 135 | ocean_nature:124, money_banking:3 | `mixkit__44973__big-tropical-fish-swimming-gracefully-along-a-coral-sea-bed.mp4` |
| time lapse | 134 | landscapes_timelapse:69, world_cities:25 | `mixkit__4070__time-lapse-of-a-green-meadow.mp4` |
| symbol state | 134 | government_buildings:129, small_town:5 | `pixabay_extra__v_136170__burundi-flag-beautiful-wallpaper-africa-symbol-state-country.mp4` |
| pattern | 131 | textures_backgrounds:84, science_tech:9 | `pixabay_extra__v_127164__pattern-smoke-liquid-black-and-white-texture-background-cove.mp4` |
| dark | 130 | textures_backgrounds:48, courtroom_justice:12 | `mixkit__44818__abstract-video-of-a-liquid-with-dark-ink-flowing.mp4` |
| network | 129 | science_tech:110, police_modern:6 | `mixkit__32989__virtual-network-representation.mp4` |
| morning | 126 | courtroom_justice:28, selling_floor:14 | `ia__1913-07-27-all-in-readiness-for-franks-trial-monday-morning__sunday-27th-july-1913-all-in-readiness-for-leo-franks-trial.mp4` |
| table | 126 | business_corporate:35, science_tech:34 | `mixkit__31135__man-picking-up-100-bills-from-the-table.mp4` |
| timelapse | 124 | landscapes_timelapse:84, world_cities:34 | `coverr__4021__timelapse-of-a-house-in-the-mountains.mp4` |
| sand | 124 | ocean_nature:63, newspapers_printing:13 | `mixkit__28901__sand-falling-from-an-hourglass-on-a-black-background.mp4` |
| town | 124 | world_cities:43, small_town:20 | `ia__townofthetimes__town-of-the-times.mp4` |
| slow | 122 | wildlife_animals:77, money_banking:6 | `mixkit__27133__flock-of-pigeons-on-the-street-slow-motion.mp4` |
| tokyo | 122 | japan:74, courtroom_justice:37 | `ia__kamikazeceremony__kamikaze-ceremony-pd-tokyo-way-of-life-tokyo-1945.mp4` |
| yard | 122 | prison_jail:99, economy_crisis:7 | `ia__npc-3527__launching-uss-alabama-bb-60-norfolk-navy-yard-02-16-1942.mp4` |
| aquarium | 122 | ocean_nature:111, textures_backgrounds:5 | `pixabay_extra__v_85674__fish-aquarium-underwater-ocean-marine-coral-dive-reef-deep-s.mp4` |
| shopping | 121 | economy_crisis:44, selling_floor:38 | `mixkit__6302__women-walking-with-shopping-bags.mp4` |
| texture | 121 | textures_backgrounds:83, money_banking:7 | `mixkit__1205__blue-ink-texture-underwater-with-a-mirror.mp4` |
| europe | 121 | government_buildings:52, world_cities:35 | `ia__1939-09-04-special-release-europe-at-war__special-release-europe-at-war-1939-09-04.mp4` |
| sport | 121 | newspapers_printing:52, government_buildings:29 | `pixabay_extra__v_158088__mountains-waterfall-cascade-rocks-canyon-drone-crystal-water.mp4` |
| person | 120 | prison_jail:30, hands_and_transactions:21 | `mixkit__23168__counting-money-and-giving-it-to-another-person.mp4` |
| cityscape | 119 | world_cities:72, government_buildings:24 | `mixkit__31005__beach-in-dubai-with-cityscape-in-the-background.mp4` |
| oregon | 119 | government_buildings:109, ocean_nature:3 | `ia__cityofportorfordoregon-councilmeetingapril7th2011__city-of-port-orford-oregon-council-meeting-april-7th-2011.mp4` |
| space station | 119 | space_nasa:116, weather_disasters:2 | `nasa__Earth_Views_from_the_International_Space_Station__earth-views-from-the-international-space-station.mp4` |
| water bird | 119 | wildlife_animals:115, money_banking:2 | `pixabay_extra__v_265493__fauna-duck-water-bird-floating-splashing-swim-wing-lake-wild.mp4` |
| evening | 118 | landscapes_timelapse:37, police_modern:22 | `pixabay_extra__v_366661__drone-aerial-drone-footage-nature-landscape-summer-evening-s.mp4` |
| field | 118 | small_town:23, landscapes_timelapse:15 | `mixkit__4071__pair-of-brown-bears-in-the-field.mp4` |
| noir | 118 | pd_feature_films:117, police_modern:1 | `ia__thekillers1946usafeaturingburtlancasteravagardneredmondobrie__the-killers-1946-burt-lancaster-ava-gardner-edmond-o-brien-f.mp4` |
| shore | 117 | ocean_nature:89, war_history:5 | `coverr__3079__the-incoming-waves-of-the-ocean-gently-splash-onto-the-shore.mp4` |
| marine | 117 | ocean_nature:92, goods_in_motion:7 | `ia__npc-11306__marine-naval-civilian-activities-on-okinawa-04-03-1945.mp4` |
| flow | 116 | textures_backgrounds:52, newspapers_printing:10 | `mixkit__44791__abstract-flow-of-a-drop-of-pink-ink-in-a-thick-liquid.mp4` |
| colombia | 116 | prison_jail:67, world_cities:6 | `mixkit__18090__colombia-flag-render.mp4` |
| cliff | 116 | ocean_nature:97, landscapes_timelapse:7 | `ia__cliff-erosion-threatens-to-push-california-homes-into-sea__cliff-erosion-threatens-to-push-california-homes-into-sea.mp4` |
| desk | 116 | hands_and_transactions:36, science_tech:32 | `mixkit__47415__accountant-working-at-her-desk-with-a-calculator.mp4` |
| tourism | 116 | government_buildings:29, ocean_nature:25 | `ia__000541-202005__home-movie-000541-1940s-tourism-to-mountain-provinces-catche.mp4` |
| fire | 115 | textures_backgrounds:33, navy_harbor:10 | `ia__npc-4954__huge-gasoline-fire-japanese-ships-small-craft-burn-in-harbor.mp4` |
| train | 115 | japan:42, goods_in_motion:19 | `ia__6335stopmotiontrainfilm01154900__stop-motion-train-film.mp4` |
| small | 114 | small_town:59, hands_and_transactions:38 | `ia__npc-4954__huge-gasoline-fire-japanese-ships-small-craft-burn-in-harbor.mp4` |
| camera | 114 | police_modern:68, ocean_nature:9 | `ia__npc-10241__navy-world-war-ii-combat-gun-camera-gsap.mp4` |
| flying | 114 | police_modern:27, wildlife_animals:19 | `ia__the-flying-ace-part-1__the-flying-ace-part-1-1920-all-black-cast-silent-film-1-05-5.mp4` |
| island | 114 | ocean_nature:53, war_history:14 | `ia__npc-10988__spectators-watch-u-s-fleet-entering-harbor-aboard-ship-attac.mp4` |
| africa | 113 | government_buildings:64, wildlife_animals:23 | `ia__arc-38932__november-1942-newsreel-marines-on-guadalcanal-uss-boise-cl-4.mp4` |
| germany | 112 | courtroom_justice:58, government_buildings:19 | `ia__adc-6491__munich-no-541-buchenwald-trial-dachau-germany-04-12-1947.mp4` |
| market | 111 | selling_floor:43, money_banking:42 | `coverr__3150__queue-to-carrefour-market-in-paris.mp4` |
| laptop | 111 | science_tech:33, newspapers_printing:23 | `mixkit__50766__a-young-man-on-the-couch-using-the-laptop-computer.mp4` |
| port orford | 111 | government_buildings:111 | `ia__cityofportorfordoregon-councilmeetingapril7th2011__city-of-port-orford-oregon-council-meeting-april-7th-2011.mp4` |
| orford | 111 | government_buildings:111 | `ia__cityofportorfordoregon-councilmeetingapril7th2011__city-of-port-orford-oregon-council-meeting-april-7th-2011.mp4` |
| hand | 110 | hands_and_transactions:57, courtroom_justice:13 | `mixkit__3916__hand-of-a-person-in-the-dark-through-colored-lights.mp4` |
| cute | 110 | wildlife_animals:54, small_town:18 | `pixabay_extra__v_308428__lion-cub-baby-lion-lion-cubs-playing-play-fight-wildlife-cut.mp4` |
| holiday | 110 | ocean_nature:65, textures_backgrounds:9 | `pixabay_extra__v_218714__beach-ocean-sea-summer-holiday-wave-nature-beautiful-beautif.mp4` |
| movie | 109 | pd_feature_films:81, money_banking:9 | `ia__thekillers1946usafeaturingburtlancasteravagardneredmondobrie__the-killers-1946-burt-lancaster-ava-gardner-edmond-o-brien-f.mp4` |
| grass | 109 | wildlife_animals:32, landscapes_timelapse:17 | `mixkit__11053__male-lions-resting-on-the-grass.mp4` |
| dollar | 109 | money_banking:103, hands_and_transactions:4 | `ia__two-dollar-bettor-movie__two-dollar-bettor.mp4` |
| orford oregon | 109 | government_buildings:109 | `ia__cityofportorfordoregon-councilmeetingapril7th2011__city-of-port-orford-oregon-council-meeting-april-7th-2011.mp4` |
| flowers | 109 | japan:28, landscapes_timelapse:18 | `mixkit__4484__lilies-flowers-on-its-stem-slowly-opening.mp4` |
| nasa | 108 | space_nasa:107, newspapers_printing:1 | `nasa__Safe_Return_to_Earth_from_the_Space_Station_on_This_Week_NAS__safe-return-to-earth-from-the-space-station-on-this-week-nas.mp4` |
| girl | 107 | courtroom_justice:27, hands_and_transactions:18 | `ia__the-patchwork-girl-of-oz-1914-silent-film-noir-drama__the-patchwork-girl-of-oz-1914-silent-film-film-noir-drama.mp4` |
| art | 107 | textures_backgrounds:39, japan:11 | `pixabay_extra__v_23730__ink-abstract-art-wave-fog-smoke-blue-pink-water-paint-colors.mp4` |
| city port | 107 | government_buildings:107 | `ia__cityofportorfordoregon-councilmeetingapril7th2011__city-of-port-orford-oregon-council-meeting-april-7th-2011.mp4` |
| speed | 106 | police_modern:41, newspapers_printing:17 | `mixkit__2160__man-hitting-a-speed-ball.mp4` |
| italy | 106 | government_buildings:28, war_history:18 | `ia__npc-4281__wreckage-in-city-harbor-of-civitavecchia-italy-06-09-1944.mp4` |
| animal wildlife | 106 | wildlife_animals:96, small_town:3 | `pixabay_extra__v_12793__birds-starlings-flock-flock-of-birds-nature-animal-wildlife.mp4` |
| state country | 106 | government_buildings:100, small_town:6 | `pixabay_extra__v_136170__burundi-flag-beautiful-wallpaper-africa-symbol-state-country.mp4` |
| christmas | 105 | textures_backgrounds:36, money_banking:13 | `coverr__284__blurred-christmas-lights.mp4` |
| shop | 105 | selling_floor:42, hands_and_transactions:32 | `ia__37600-201704__in-us-town-that-embraces-refugees-auto-shop-business-flouris.mp4` |
| predator | 105 | wildlife_animals:87, world_cities:6 | `pixabay_extra__v_296464__lion-animal-wild-predator-king-majestic-powerful-wildlife-na.mp4` |
| close | 104 | hands_and_transactions:21, money_banking:17 | `coverr__3270__close-up-of-barista-taking-money-from-a-customer.mp4` |
| internet | 104 | science_tech:77, business_corporate:9 | `pixabay_extra__v_17085__technology-computer-computer-science-network-internet.mp4` |
| calm | 103 | ocean_nature:56, courtroom_justice:10 | `coverr__4513__calm-waves-in-an-ocean-gulf.mp4` |
| lion | 102 | wildlife_animals:98, world_cities:2 | `mixkit__11035__male-lion-walking-in-the-savanna.mp4` |
| country nation | 102 | government_buildings:96, small_town:5 | `pixabay_extra__v_136170__burundi-flag-beautiful-wallpaper-africa-symbol-state-country.mp4` |
| drenthe | 102 | police_modern:35, small_town:33 | `pixabay_extra__v_231773__deer-trees-alone-sunset-forest-woods-netherlands-drenthe-bea.mp4` |
| moving | 101 | prison_jail:44, hands_and_transactions:10 | `mixkit__20961__robot-with-moving-eyes.mp4` |
| rock | 101 | ocean_nature:46, landscapes_timelapse:13 | `ia__pacific-ocean-waves-crashing-against-rock-formation__pacific-ocean-waves-crashing-against-rock-formation.mp4` |
| national | 101 | government_buildings:83, small_town:5 | `ia__house-hbs-blur-05-x__subcommittee-on-national-parks-forests-and-public-lands-legi.mp4` |
| oregon council | 101 | government_buildings:101 | `ia__cityofportorfordoregon-councilmeetingapril7th2011__city-of-port-orford-oregon-council-meeting-april-7th-2011.mp4` |
| leaves | 100 | money_banking:21, japan:16 | `pixabay_extra__v_171978__waterfall-stream-forest-stock-trees-water-rain-leaves-bugs-b.mp4` |
| committee | 100 | government_buildings:99, prison_jail:1 | `ia__committee-04-02-2012__city-council-committee-meeting-april-2nd-2012.mp4` |
| coins | 99 | money_banking:66, hands_and_transactions:32 | `mixkit__33358__gray-haired-old-man-counting-a-few-coins.mp4` |
| food | 99 | selling_floor:28, textures_backgrounds:14 | `ia__arc-39115__may-1946-newsreel-uscg-postwar-food-crisis-40-wall-st-plane.mp4` |
| prison | 99 | prison_jail:99 | `ia__prison-mutiny-ipod__prison-mutiny.mp4` |
| coral reef | 99 | ocean_nature:99 | `mixkit__44868__beautiful-coral-reef-with-exotic-reef-fish.mp4` |
| abandoned | 98 | economy_crisis:49, courtroom_justice:33 | `mixkit__2632__abandoned-house-in-a-forest.mp4` |
| door | 97 | economy_crisis:36, money_banking:24 | `ia__backdoortoheaven__back-door-to-heaven.mp4` |
| outdoors | 97 | wildlife_animals:24, ocean_nature:16 | `pixabay_extra__v_12793__birds-starlings-flock-flock-of-birds-nature-animal-wildlife.mp4` |
| flock | 97 | wildlife_animals:89, courtroom_justice:6 | `ia__kingsprucehenputsonashowforthelargestflockweeversaw__king-spruce-hen-puts-on-a-show-for-the-largest-flock-we-ever-3.mp4` |
| structure | 97 | government_buildings:61, science_tech:15 | `pixabay_extra__v_20273__window-ruins-house-burnt-burned-building-structure-architect.mp4` |
| rural | 96 | japan:43, small_town:26 | `mixkit__25096__rural-landscape-in-the-hills-and-a-village.mp4` |
| particles | 96 | textures_backgrounds:69, science_tech:10 | `mixkit__12495__smoke-with-fluorescent-particles-on-black-background.mp4` |
| council committee | 94 | government_buildings:94 | `ia__committee-04-02-2012__city-council-committee-meeting-april-2nd-2012.mp4` |
| colorful | 94 | textures_backgrounds:30, ocean_nature:12 | `mixkit__47176__colorful-ink-swirling-through-water-against-a-dark-backgroun.mp4` |
| fence | 94 | prison_jail:89, textures_backgrounds:3 | `mixkit__24179__a-shirtless-man-with-metal-chain-behind-the-fence.mp4` |
| modern | 93 | courtroom_justice:14, science_tech:12 | `mixkit__8846__lawyer-puts-on-sunglasses-in-front-of-modern-building.mp4` |
| france | 92 | war_history:30, government_buildings:17 | `ia__adc-1324a__trial-of-nazi-spies-cherbourg-france-7-8-44.mp4` |
| flower | 92 | landscapes_timelapse:14, prison_jail:14 | `mixkit__28834__peony-pink-flower-opening.mp4` |
| working | 91 | science_tech:27, hands_and_transactions:24 | `mixkit__47258__robot-working-in-an-electronics-manufacturing-facility.mp4` |
| regular | 91 | government_buildings:91 | `ia__bartletttexasregularcitycouncilmeetingjan192010__bartlett-texas-regular-city-council-meeting-jan-19-2010.mp4` |
| moon | 91 | space_nasa:28, japan:10 | `nasa__jsc2020m001449_Down_to_Earth_To_the_Moon_and_Beyond-SOCIAL__down-to-earth-to-the-moon-and-beyond.mp4` |
| enumclaw city | 91 | government_buildings:91 | `ia__160222council__enumclaw-city-council-regular-meeting-february-22-2016.mp4` |
| enumclaw | 91 | government_buildings:91 | `ia__160222council__enumclaw-city-council-regular-meeting-february-22-2016.mp4` |
| artemis | 91 | space_nasa:90, japan:1 | `nasa__KSC-20221116-MH-NAS01-0001-Artemis_I_Orion_First_Imagery_of___artemis-i-orion-first-imagery-of-earth.mp4` |
| rocket | 90 | space_nasa:77, war_history:8 | `nara__77338-14911517__invasion-of-southern-france-landing-lcs-fires-rocket-barrage.mp4` |
| pearl | 90 | navy_harbor:87, war_history:1 | `ia__npc-10134__1942-captured-japanese-newsreel-pearl-harbor-hong-kong.mp4` |
| regular meeting | 90 | government_buildings:90 | `ia__160222council__enumclaw-city-council-regular-meeting-february-22-2016.mp4` |
| wealth | 90 | money_banking:89, prison_jail:1 | `pixabay_extra__v_122881__market-economy-trading-graph-finance-money-business-wealth-i.mp4` |
| trees forest | 89 | landscapes_timelapse:25, small_town:21 | `pixabay_extra__v_171531__trees-forest-river-canyon-town-drone-beach-sea-water-lake-tr.mp4` |
| trials | 89 | courtroom_justice:89 | `ia__adc-9927__nuremberg-trials-11-21-1945.mp4` |
| life | 89 | ocean_nature:42, wildlife_animals:17 | `ia__010058-001__home-movie-010058-001-1931-upstate-new-york-town-life-with-f.mp4` |
| trip | 89 | ocean_nature:39, goods_in_motion:10 | `ia__000437-202005__home-movie-000437-1940s-western-train-trip.mp4` |
| slow motion | 89 | wildlife_animals:62, government_buildings:5 | `mixkit__27133__flock-of-pigeons-on-the-street-slow-motion.mp4` |
| phone | 88 | business_corporate:49, market_machinery:6 | `coverr__9327__a-trader-performing-financial-analysis-of-cryptocurrency-usi.mp4` |
| typing | 88 | newspapers_printing:55, science_tech:15 | `ia__basic-typing-2__basic-typing-part-i-methods-part-ii.mp4` |
| asia | 88 | japan:28, government_buildings:20 | `pixabay_extra__v_44622__japan-street-tokyo-city-night-asia-japanese-travel-building.mp4` |
| pearl harbor | 88 | navy_harbor:87, war_history:1 | `ia__npc-10134__1942-captured-japanese-newsreel-pearl-harbor-hong-kong.mp4` |
| council regular | 88 | government_buildings:88 | `ia__160222council__enumclaw-city-council-regular-meeting-february-22-2016.mp4` |
| ocean waves | 87 | ocean_nature:76, landscapes_timelapse:5 | `coverr__coverr-premium-couple-observes-ocean-waves__premium-couple-observes-ocean-waves.mp4` |
| future | 87 | science_tech:60, government_buildings:9 | `ia__hrs14edw2175-090616__the-future-of-learning-how-technology-is-transforming-public.mp4` |
| training | 87 | war_history:46, business_corporate:12 | `ia__gov-archives-arc-645746__hallucination-training-film-counterguerrilla-training.mp4` |
| crimes | 87 | courtroom_justice:86, government_buildings:1 | `nara__20795-75843019__war-crimes-atrocity-trials-yokohama-japan.mp4` |
| plant | 87 | factory_manufacturing:15, prison_jail:14 | `mixkit__4362__smoke-from-power-plant.mp4` |
| walk | 86 | courtroom_justice:44, world_cities:8 | `ia__walkacrookedmile1948-202002__walk-a-crooked-mile-1948-usa-louis-hayward-dennis-o-keefe-fi.mp4` |
| war crimes | 86 | courtroom_justice:86 | `nara__20795-75843019__war-crimes-atrocity-trials-yokohama-japan.mp4` |
| spring | 85 | japan:25, landscapes_timelapse:10 | `mixkit__26999__mountainous-landscape-in-spring-with-cloudy-sky.mp4` |
| netherlands drenthe | 85 | police_modern:31, small_town:22 | `pixabay_extra__v_231773__deer-trees-alone-sunset-forest-woods-netherlands-drenthe-bea.mp4` |
| store | 84 | hands_and_transactions:33, money_banking:17 | `coverr__coverr-premium-shopping-for-meat-at-the-grocery-store__premium-shopping-for-meat-at-the-grocery-store.mp4` |
| path | 84 | courtroom_justice:24, small_town:21 | `mixkit__23818__young-man-walking-in-a-rural-path.mp4` |
| sea beach | 84 | ocean_nature:63, landscapes_timelapse:10 | `pixabay_extra__v_70796__waves-ocean-sea-beach-byron-bay-4k-australia-live-wallpaper.mp4` |
| data | 84 | science_tech:44, business_corporate:20 | `mixkit__23219__long-hallway-in-data-center.mp4` |
| contemporary | 84 | government_buildings:50, science_tech:26 | `mixkit__40946__contemporary-dancers-hands-on-a-light-background.mp4` |
| flight | 84 | wildlife_animals:25, space_nasa:10 | `mixkit__22598__passenger-waiting-for-a-flight.mp4` |
| sign | 83 | government_buildings:20, money_banking:18 | `ia__arc-39079__september-1945-newsreel-japanese-sign-final-surrender.mp4` |
| daylight | 83 | police_modern:22, courtroom_justice:15 | `ia__arc-39002__newsreel-january-february-1944-u-s-bombers-in-first-daylight.mp4` |
| liquid | 83 | textures_backgrounds:47, science_tech:10 | `mixkit__44818__abstract-video-of-a-liquid-with-dark-ink-flowing.mp4` |
| sea waves | 82 | ocean_nature:69, courtroom_justice:3 | `mixkit__9294__sea-waves-breaking-on-the-rocks-front-view.mp4` |
| cloud | 82 | landscapes_timelapse:38, japan:14 | `mixkit__48482__aerial-footage-of-cloud-topped-mountains-at-sunset.mp4` |
| natural | 81 | japan:45, landscapes_timelapse:8 | `pixabay_extra__v_236928__waterfall-water-flow-japan-natural-landscape.mp4` |
| boat | 81 | goods_in_motion:38, ocean_nature:12 | `mixkit__11939__harbour-pilot-boat-following-a-cargo-ship.mp4` |
| uss | 81 | navy_harbor:47, war_history:33 | `ia__npc-1126__night-action-battle-of-kula-gulf-uss-honolulu-cl-48-damage-c.mp4` |
| communication | 81 | science_tech:38, government_buildings:11 | `pixabay_extra__v_212818__robot-brain-computer-science-head-face-digital-communication.mp4` |
| cells | 81 | prison_jail:77, science_tech:4 | `mixkit__3958__viruses-absorbing-cells-floating-in-a-liquid.mp4` |
| graphic | 81 | prison_jail:46, textures_backgrounds:8 | `mixkit__47016__close-up-of-a-stock-market-graphic.mp4` |
| abstract background | 81 | prison_jail:44, textures_backgrounds:28 | `pixabay_extra__v_134822__sea-waves-blue-abstract-background-nature-ocean-daytime-beau.mp4` |
| off | 80 | newspapers_printing:56, war_history:9 | `mixkit__20932__taking-off-a-bolt.mp4` |
| world | 80 | war_history:13, ocean_nature:12 | `ia__sekigunpflpsekaisensosengentheredarmypflpdeclarationofworldw__sekigun-pflp-sekai-senso-sengen-the-red-army-pflp-declaratio.mp4` |
| international | 80 | space_nasa:66, courtroom_justice:3 | `ia__img-4983-202108-sauhx1fvhjzo__nintendo-music-records-true-quality-international-awards-col.mp4` |
| bombardment | 80 | war_history:79, navy_harbor:1 | `ia__arc-39003__february-march-1944-newsreel-new-air-bases-in-south-pacific.mp4` |
| crimes trials | 80 | courtroom_justice:80 | `nara__19879-75842785__munich-nos-211-222-war-crimes-trials-nuremberg-germany.mp4` |
| window | 79 | prison_jail:44, government_buildings:7 | `ia__green-archer-ep2__green-archer-the-chapter-2-the-face-at-the-window.mp4` |
| live | 79 | space_nasa:44, police_modern:7 | `nasa__KSC-20220628-VP-MMS01-0001-RocketLab_Capstone_Live_Launch_Co__rocket-lab-capstone-live-launch-coverage-rocket-views.mp4` |
| sunlight | 79 | landscapes_timelapse:22, ocean_nature:20 | `pixabay_extra__v_189264__clouds-sky-nature-mountains-sun-sunlight-calm-sunset-landsca.mp4` |
| patriotism | 79 | government_buildings:76, small_town:2 | `pixabay_extra__v_135801__angola-flag-africa-symbol-state-country-nation-patriotism-be.mp4` |
| restaurant | 78 | selling_floor:45, government_buildings:15 | `mixkit__4672__waiter-serving-meat-stew-in-a-restaurant.mp4` |
| alone | 78 | courtroom_justice:63, japan:3 | `ia__alone-short-film__alone-short-film.mp4` |
| economy | 78 | money_banking:74, world_cities:1 | `pixabay_extra__v_308078__stock-market-finance-trading-investment-economy-business-mon.mp4` |
| aerial drone | 78 | landscapes_timelapse:30, world_cities:18 | `pixabay_extra__v_189269__clouds-sunset-sky-nature-mountains-golden-sky-landscape-aeri.mp4` |
| america | 77 | small_town:56, government_buildings:8 | `ia__socialcl1957__social-class-in-america.mp4` |
| book | 76 | courtroom_justice:50, hands_and_transactions:6 | `mixkit__45831__woman-walking-through-a-row-of-tall-book-shelves-filled-with.mp4` |
| investment | 76 | money_banking:70, business_corporate:5 | `pixabay_extra__v_308078__stock-market-finance-trading-investment-economy-business-mon.mp4` |
| cloudscape | 76 | landscapes_timelapse:74, world_cities:1 | `pixabay_extra__v_198549__sky-clouds-mountains-cloudscape-drone-aerial-nature-landscap.mp4` |
| big | 75 | wildlife_animals:26, world_cities:17 | `ia__gov-archives-arc-2569601__big-picture-military-justice.mp4` |
| insect | 75 | prison_jail:43, wildlife_animals:14 | `pixabay_extra__v_345137__butterfly-nature-insect-fauna-animal-lepidoptera-wildlife-po.mp4` |
| automobile | 75 | police_modern:48, world_cities:9 | `ia__0960runninggearanddifferential__elements-of-the-automobile-part-i-running-gear-and-different.mp4` |
| scenery | 75 | landscapes_timelapse:21, small_town:13 | `mixkit__15625__canyon-scenery.mp4` |
| ocean water | 75 | ocean_nature:63, goods_in_motion:3 | `mixkit__45611__ocean-water-moving-calmly.mp4` |
| blur | 75 | textures_backgrounds:32, world_cities:10 | `pixabay_extra__v_4382__liquid-lights-intro-blue-blur-beautiful-wallpaper-bokeh-abst.mp4` |
| bird plumage | 75 | wildlife_animals:66, courtroom_justice:5 | `pixabay_extra__v_174537__gull-bird-water-bird-plumage-sitting-wildlife.mp4` |
| card | 74 | money_banking:43, police_modern:13 | `mixkit__42606__girl-opening-an-envelope-from-a-valentine-s-day-card.mp4` |
| animation | 74 | money_banking:16, selling_floor:8 | `mixkit__26759__negative-stock-market-indicators-3d-animation.mp4` |
| landscape nature | 74 | landscapes_timelapse:32, small_town:10 | `mixkit__43161__couple-looking-at-a-landscape-in-nature.mp4` |
| city urban | 74 | world_cities:31, government_buildings:17 | `pixabay_extra__v_338628__night-harbour-people-car-automobile-city-urban-cityscape-bui.mp4` |
| falling | 73 | money_banking:30, economy_crisis:12 | `mixkit__47013__slow-motion-of-falling-coins.mp4` |
| stream | 73 | newspapers_printing:27, wildlife_animals:16 | `mixkit__31563__platelets-and-red-blood-cells-in-the-blood-stream.mp4` |
| dusk | 73 | landscapes_timelapse:48, world_cities:5 | `pixabay_extra__v_197802__sky-nature-sunset-clouds-landscape-mountains-dusk-drone-aeri.mp4` |
| books | 73 | courtroom_justice:63, prison_jail:4 | `mixkit__45831__woman-walking-through-a-row-of-tall-book-shelves-filled-with.mp4` |
| day | 72 | courtroom_justice:11, war_history:9 | `ia__trump-fraud-trial-day-2-10-03-2023__trump-s-fraud-trial-day-2.mp4` |
| center | 72 | space_nasa:14, world_cities:11 | `mixkit__23219__long-hallway-in-data-center.mp4` |
| ships | 72 | navy_harbor:45, goods_in_motion:13 | `ia__npc-1733__over-turned-wrecked-ships-others-afire-pearl-harbor-12-07-19.mp4` |
| usa | 72 | small_town:25, government_buildings:18 | `ia__alonzo-mann-sworn-in-for-the-defendant-68th-to-testify-at-th__alonzo-mann-sworn-in-for-the-defendant-68th-to-testify-at-th.mp4` |
| stars | 72 | police_modern:22, textures_backgrounds:10 | `ia__stars-in-your-eyes-1956__jimmy-clitheroe-film-stars-in-your-eyes-1956.mp4` |
| earth | 72 | space_nasa:30, small_town:13 | `nasa__Earth_Views_from_the_International_Space_Station__earth-views-from-the-international-space-station.mp4` |
| fall | 71 | money_banking:13, wildlife_animals:10 | `mixkit__18262__surface-while-100-dollar-bills-fall-messily.mp4` |
| road traffic | 71 | world_cities:28, police_modern:28 | `pixabay_extra__v_188591__street-road-traffic-night-motorcycles-cars-buses-travel-trip.mp4` |
| tower | 71 | government_buildings:29, japan:13 | `mixkit__20077__tokyo-night-street-with-fast-traffic-and-tower.mp4` |
| waterfall | 71 | japan:21, landscapes_timelapse:20 | `pixabay_extra__v_236928__waterfall-water-flow-japan-natural-landscape.mp4` |
| committee meeting | 71 | government_buildings:71 | `ia__committee-04-02-2012__city-council-committee-meeting-april-2nd-2012.mp4` |
| diving | 71 | ocean_nature:69, wildlife_animals:1 | `pixabay_extra__v_5270__coral-ocean-underwater-diving-scuba-reef-travel-water-tropic.mp4` |
| through | 70 | courtroom_justice:12, science_tech:6 | `coverr__4214__surfing-through-the-ocean-waves.mp4` |
| machine | 70 | science_tech:29, money_banking:7 | `mixkit__47266__automated-machine-places-parts-on-circuit-boards.mp4` |
| fantasy | 70 | science_tech:13, courtroom_justice:12 | `pixabay_extra__v_231873__robot-science-fiction-futuristic-skyline-loop-fantasy.mp4` |
| woods | 70 | courtroom_justice:21, wildlife_animals:21 | `mixkit__6845__couple-walking-in-the-woods.mp4` |
| hiking | 70 | courtroom_justice:51, landscapes_timelapse:11 | `pixabay_extra__v_232696__mountains-japan-northern-alps-climber-hiking-japan-landscape.mp4` |
| public | 70 | government_buildings:52, police_modern:6 | `ia__npc-2762__1940-s-public-buildings-washington-d-c-general-scenes-ww2.mp4` |
| scenic | 70 | landscapes_timelapse:29, small_town:9 | `pixabay_extra__v_198786__sky-clouds-cloudscape-mountains-scenic-drone-aerial-nature-l.mp4` |
| april | 69 | government_buildings:44, space_nasa:17 | `ia__committee-04-02-2012__city-council-committee-meeting-april-2nd-2012.mp4` |
| seascape | 69 | ocean_nature:64, landscapes_timelapse:3 | `pixabay_extra__v_223461__bird-seagull-boat-ocean-sea-wildlife-water-beach-waves-seasc.mp4` |
| electronics | 69 | science_tech:68, hands_and_transactions:1 | `mixkit__47258__robot-working-in-an-electronics-manufacturing-facility.mp4` |
| counting | 69 | money_banking:65, hands_and_transactions:2 | `mixkit__45703__money-counting-machine-counting-up-money.mp4` |
| aerial landscape | 69 | landscapes_timelapse:61, japan:4 | `mixkit__1566__aerial-view-of-landscape-of-a-calm-sea-at-sunset.mp4` |
| reflection | 69 | ocean_nature:18, landscapes_timelapse:10 | `pixabay_extra__v_330216__ocean-sea-tropical-waves-water-sunlight-sun-reflection-under.mp4` |
| feathers | 69 | wildlife_animals:58, prison_jail:4 | `pixabay_extra__v_37220__geese-animals-birds-feed-meal-feathers-nature-poultry-wing-b.mp4` |
| kiev | 69 | government_buildings:59, world_cities:6 | `pixabay_extra__v_132880__church-building-architecture-kiev-capital.mp4` |
| floor | 68 | money_banking:65, business_corporate:2 | `pixabay_extra__v_111293__meerkat-take-floor-equal-young-sweet-dirt.mp4` |
| fireplace | 68 | small_town:24, courtroom_justice:19 | `pixabay_extra__v_210707__ai-generated-fireplace-porch-cozy-chill-relax-lofi-jazz-outs.mp4` |
| atmosphere | 68 | landscapes_timelapse:44, space_nasa:5 | `pixabay_extra__v_236027__mountains-clouds-snow-panorama-alps-timelapse-sky-atmosphere.mp4` |
| key | 68 | money_banking:23, economy_crisis:11 | `mixkit__21812__opening-a-door-with-a-hanging-key.mp4` |

## 2b. Everything by subject — 350 subjects with >= 6 items

Search these words, not theme names. `themes` tells you which shelf folder holds them; `example` is a representative real file.

| subject | items | video | image | audio | top themes | example |
|---|---:|---:|---:|---:|---|---|
| nature | 6,709 | 1952 | 4725 | 32 | wildlife_animals:1450, landscapes_timelapse:1277 | `pixabay_extra__i_9348003__shrine-torii-japan-fushimi-nature-temple-kyoto-fushimi-inari.jpg` |
| file | 5,634 | 15 | 5617 | 2 | factory_manufacturing:2197, retail_commerce:930 | `loc__mss6557000804__naacp-legal-defense-and-educational-fund-records-subject-fil.jpg` |
| city | 3,620 | 1723 | 1774 | 123 | world_cities:1156, government_buildings:1078 | `loc__2006678356__photographs-of-the-federal-building-and-courthouse-in-oklaho.tif` |
| space | 3,533 | 531 | 2960 | 42 | space_nasa:2771, science_tech:521 | `nasa__carina-nebula__james-webb-space-telescope-nircam-image-of-the-cosmic-cliffs.png` |
| launch | 3,437 | 184 | 3252 | 1 | space_nasa:3260, science_tech:139 | `nara__45493301-45493302__liberty-bonds-public-gatherings-new-york-4th-campaign-naval.jpg` |
| building | 3,044 | 407 | 2630 | 7 | government_buildings:653, courtroom_justice:567 | `loc__2010719020__interior-courtroom-william-j-nealon-federal-building-and-u-s.jpg` |
| sea | 2,733 | 1158 | 1499 | 76 | ocean_nature:1734, goods_in_motion:158 | `nara__86712054-86712055__launching-an-observation-balloon-at-sea-observation-balloon.jpg` |
| water | 2,702 | 1068 | 1462 | 172 | ocean_nature:893, landscapes_timelapse:312 | `loc__2021758099__an-old-tractor-sits-below-the-town-water-tower-in-funk-nebra.tif` |
| landscape | 2,490 | 1013 | 1477 | 0 | landscapes_timelapse:1100, japan:442 | `met__342648__an-allegory-of-peace-peace-personified-as-a-woman-standing-i.jpg` |
| architecture | 2,326 | 568 | 1758 | 0 | government_buildings:848, world_cities:464 | `loc__2019691079__one-of-dozens-of-examples-of-exemplary-public-art-and-archit.tif` |
| ocean | 2,236 | 1059 | 1060 | 117 | ocean_nature:1719, sfx_environment:115 | `loc__2025868584__ocean-mail-steamship-service-between-the-united-states-and-b.jpg` |
| earth | 2,194 | 72 | 2122 | 0 | space_nasa:2125, science_tech:14 | `nasa__sl4-143-4707__view-of-skylab-space-station-cluster-in-earth-orbit-from-csm.jpg` |
| station | 1,956 | 167 | 1771 | 18 | space_nasa:1409, small_town:118 | `loc__2016799032__police-station-belle-isle.tif` |
| forest | 1,930 | 622 | 1117 | 191 | wildlife_animals:709, landscapes_timelapse:515 | `nara__55182035-55182036__111-sc-10870-an-artilleryman-s-bunk-in-the-forest-battery-al.jpg` |
| street | 1,856 | 415 | 1391 | 50 | world_cities:499, small_town:223 | `loc__nc0306__polk-county-courthouse-courthouse-street-columbus-polk-count.tif` |
| wildlife | 1,760 | 864 | 896 | 0 | wildlife_animals:1464, government_buildings:115 | `nara__7722786-15405834__wetlands-and-wildlife-scenic-byway-barton-county-courthouse.jpg` |
| animal | 1,738 | 592 | 1144 | 2 | wildlife_animals:1190, ocean_nature:167 | `pixabay_extra__i_1586373__deer-fawn-young-deer-wild-bambi-fallow-deer-cub-forest-anima.jpg` |
| nasa | 1,686 | 108 | 1578 | 0 | space_nasa:1449, science_tech:215 | `nasa__GSFC_20171208_Archive_e002093__nasa-explores-the-carina-nebula-by-touch.jpg` |
| expedition | 1,658 | 22 | 1636 | 0 | space_nasa:1631, science_tech:13 | `nasa__iss043e003041__earth-observation-taken-by-the-expedition-43-crew.jpg` |
| night | 1,566 | 411 | 624 | 531 | sfx_environment:412, world_cities:397 | `loc__2017802628__untitled-photo-possibly-related-to-a-new-england-housewife-f.tif` |
| center | 1,515 | 72 | 1441 | 2 | space_nasa:855, science_tech:355 | `loc__2009632448__orange-county-government-center-goshen-new-york-interior-cou.tif` |
| road | 1,456 | 752 | 653 | 51 | small_town:619, police_modern:204 | `ia__on-the-road-istanbul-sringar__on-the-road-istanbul-sringar.mp4` |
| during | 1,456 | 28 | 1413 | 15 | space_nasa:401, war_history:373 | `loc__2004676670__african-american-woman-juanita-sealy-being-carried-to-police.tif` |
| sky | 1,400 | 640 | 759 | 1 | landscapes_timelapse:381, japan:158 | `loc__2017871934__pearl-harbor-hawaii-uss-west-virginia-aflame-disregarding-th.tif` |
| old | 1,341 | 150 | 1054 | 137 | world_cities:209, economy_crisis:181 | `loc__2019691079__one-of-dozens-of-examples-of-exemplary-public-art-and-archit.tif` |
| door | 1,316 | 97 | 138 | 1081 | sfx_human_movement:1011, sfx_mechanical:62 | `freesound__407205__room-tone-small-with-door-and-window-open-to-wall-with-dista.mp3` |
| mission | 1,307 | 49 | 1258 | 0 | space_nasa:857, science_tech:386 | `loc__98502779__free-coffee-at-bowery-mission-for-unemployed.tif` |
| international | 1,300 | 80 | 1220 | 0 | space_nasa:1213, war_history:29 | `loc__2005676128__international-exhibition-phila-pa-walter-printing-press-mach.tif` |
| beach | 1,299 | 632 | 527 | 140 | ocean_nature:668, sfx_environment:135 | `coverr__9330__eroded-cliffs-on-praia-do-pinh-o-beach.mp4` |
| space station | 1,272 | 119 | 1153 | 0 | space_nasa:1205, science_tech:58 | `nasa__sl4-143-4707__view-of-skylab-space-station-cluster-in-earth-orbit-from-csm.jpg` |
| county | 1,271 | 13 | 1258 | 0 | courtroom_justice:460, factory_manufacturing:357 | `loc__2009632448__orange-county-government-center-goshen-new-york-interior-cou.tif` |
| japan | 1,182 | 366 | 791 | 25 | japan:797, space_nasa:131 | `loc__18009096__japan.jpg` |
| river | 1,169 | 316 | 682 | 171 | factory_manufacturing:247, landscapes_timelapse:240 | `loc__pa3339__u-s-steel-duquesne-works-blast-furnace-plant-along-monongahe.tif` |
| rocket | 1,154 | 90 | 1063 | 1 | space_nasa:1087, war_history:30 | `nara__17446367-17459867__acton-air-conveying-bank-and-piping-outside-cell-13-in-the-o.jpg` |
| international space | 1,152 | 65 | 1087 | 0 | space_nasa:1152 | `nasa__iss045e013851__earth-observation-from-the-international-space-station.jpg` |
| observations | 1,070 | 2 | 1068 | 0 | space_nasa:1064, science_tech:5 | `nasa__sts075-722-013__earth-observations-taken-during-sts-75.jpg` |
| earth observations | 1,060 | 1 | 1059 | 0 | space_nasa:1059, ocean_nature:1 | `nasa__sts075-722-013__earth-observations-taken-during-sts-75.jpg` |
| store | 1,059 | 84 | 972 | 3 | retail_commerce:646, selling_floor:152 | `loc__2012645659__view-of-store-fronts-along-main-street-in-benson-arizona.tif` |
| bank | 1,056 | 147 | 907 | 2 | money_banking:516, bank_and_branch:370 | `loc__2021755736__the-old-central-gas-station-building-in-donaldsonville-a-his.tif` |
| mountain | 1,049 | 275 | 749 | 25 | landscapes_timelapse:543, japan:276 | `loc__2005693170__barbourville-ky-knox-county-court-house-a-mountain-county-co.tif` |
| travel | 1,044 | 331 | 710 | 3 | world_cities:191, japan:132 | `loc__2020742585__the-1937-vintage-western-view-diner-and-steak-house-on-histo.tif` |
| office | 1,019 | 230 | 743 | 46 | business_corporate:348, courtroom_justice:99 | `loc__al0898__greene-county-courthouse-probate-judge-s-office-courthouse-s.tif` |
| sts- | 1,004 | 1 | 1003 | 0 | space_nasa:830, science_tech:169 | `nasa__sts075-722-013__earth-observations-taken-during-sts-75.jpg` |
| bird | 997 | 466 | 462 | 69 | wildlife_animals:753, sfx_environment:66 | `pixabay_extra__v_30448__hummingbird-feeder-backyard-flock-anna-s-flying-bird-wildlif.mp4` |
| observations expedition | 975 | 0 | 975 | 0 | space_nasa:975 | `nasa__iss034e039331__earth-observations-taken-by-expedition-34-crewmember.jpg` |
| sunset | 964 | 622 | 336 | 6 | landscapes_timelapse:370, ocean_nature:152 | `coverr__4178__pink-sunset-timelapse.mp4` |
| waves | 961 | 442 | 274 | 245 | ocean_nature:539, sfx_environment:245 | `coverr__3079__the-incoming-waves-of-the-ocean-gently-splash-onto-the-shore.mp4` |
| car | 950 | 333 | 336 | 281 | police_modern:412, sfx_mechanical:199 | `loc__2020635830__police-car-police-officers-and-onlookers.tif` |
| coast | 938 | 363 | 563 | 12 | ocean_nature:638, war_history:35 | `loc__2026583309__coast-guard-national-defense-and-maritime-police-functions-m.jpg` |
| trees | 932 | 369 | 475 | 88 | landscapes_timelapse:233, small_town:162 | `pixabay_extra__i_2897227__dolomites-mountains-alps-alpine-trees-conifers-coniferous-fo.jpg` |
| business | 921 | 421 | 500 | 0 | business_corporate:321, money_banking:265 | `loc__afcwip001417__view-down-east-main-street-near-the-corner-of-east-main-and.jpg` |
| close | 920 | 104 | 197 | 619 | sfx_human_movement:520, sfx_environment:81 | `freesound__657357__fire-near-open-close-wav.mp3` |
| courthouse | 915 | 18 | 897 | 0 | courtroom_justice:893, americana_1930s_1970s:13 | `loc__2010719020__interior-courtroom-william-j-nealon-federal-building-and-u-s.jpg` |
| japanese | 910 | 142 | 766 | 2 | japan:602, space_nasa:150 | `loc__2017821634__untitled-photo-possibly-related-to-corner-of-montgomery-and.tif` |
| artemis | 898 | 91 | 807 | 0 | space_nasa:851, science_tech:45 | `nasa__art002e000192__earth-from-the-perspective-of-artemis-ii.jpg` |
| house | 891 | 202 | 667 | 22 | government_buildings:146, courtroom_justice:115 | `loc__2024785551__letter-from-the-secretary-of-war-transmitting-a-system-of-fi.jpg` |
| background | 889 | 580 | 257 | 52 | textures_backgrounds:171, government_buildings:115 | `mixkit__489__black-ink-on-white-background.mp4` |
| factory | 887 | 45 | 831 | 11 | factory_manufacturing:452, economy_crisis:294 | `loc__08011463__profit-making-in-shop-and-factory-management.jpg` |
| kennedy | 874 | 35 | 839 | 0 | space_nasa:656, science_tech:168 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| space center | 859 | 9 | 850 | 0 | space_nasa:672, science_tech:167 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| aerial | 842 | 564 | 278 | 0 | landscapes_timelapse:243, ocean_nature:235 | `ia__npc-5630__aerial-views-ww2-new-ireland-island-simpson-harbor-rapapo-ta.mp4` |
| crew | 841 | 27 | 814 | 0 | space_nasa:705, science_tech:50 | `nara__6421230-13148181__crew-members-aboard-a-foreign-warship-man-the-rails-during-t.jpeg` |
| clouds | 841 | 502 | 339 | 0 | landscapes_timelapse:446, japan:80 | `ia__juusonturhavideodiary-clouds26htimelapse__juuson-turha-video-diary-clouds-26h-timelapse-3.mp4` |
| works | 839 | 7 | 832 | 0 | factory_manufacturing:750, space_nasa:36 | `loc__pa3339__u-s-steel-duquesne-works-blast-furnace-plant-along-monongahe.tif` |
| kennedy space | 833 | 9 | 824 | 0 | space_nasa:646, science_tech:167 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| national | 832 | 101 | 728 | 3 | government_buildings:303, money_banking:58 | `loc__ca10005037__rules-and-regulations-for-the-government-of-the-preventive-f.jpg` |
| telescope | 830 | 9 | 821 | 0 | science_tech:720, space_nasa:103 | `nara__6374210-14831496__a-member-of-the-9th-division-artillery-uses-a-m-65-battery-c.jpeg` |
| shuttle | 827 | 1 | 826 | 0 | space_nasa:728, science_tech:86 | `nasa__sts093-704-087__earth-observations-taken-from-space-shuttle-columbia-during.jpg` |
| mountains | 825 | 335 | 482 | 8 | landscapes_timelapse:496, japan:106 | `loc__2021756510__a-streetside-stand-selling-mouth-watering-but-fattening-food.tif` |
| air | 822 | 64 | 743 | 15 | space_nasa:254, war_history:244 | `loc__ca4313__ss-keystone-state-national-defense-reserve-fleet-alameda-nav.tif` |
| urban | 821 | 360 | 444 | 17 | world_cities:390, business_corporate:86 | `pixabay_extra__i_4472321__street-tower-krakow-poland-tourism-europe-urban-travel-krako.jpg` |
| underwater | 810 | 387 | 418 | 5 | ocean_nature:743, textures_backgrounds:29 | `nasa__KSC-03pd2367__kennedy-space-center-fla-justin-manley-of-the-national-ocean.jpg` |
| artillery | 801 | 7 | 793 | 1 | war_history:790, japan:3 | `nara__789238-502238326__australia-divider-4-artillery.jpg` |
| traffic | 799 | 537 | 127 | 135 | world_cities:247, police_modern:194 | `coverr__9024__pedestrian-traffic-light.mp4` |
| buildings | 798 | 271 | 527 | 0 | world_cities:302, government_buildings:151 | `loc__afcwip004231__three-buildings-on-the-west-side-of-main-street-north-of-gra.jpg` |
| will | 798 | 3 | 795 | 0 | space_nasa:528, science_tech:113 | `loc__2021641653__lone-pine-calif-may-1942-a-soldier-of-army-military-police-a.tif` |
| field | 785 | 118 | 625 | 42 | war_history:459, small_town:60 | `nara__6373154-14831058__sergeant-1st-class-michael-vinson-chief-of-firing-battery-fo.jpeg` |
| money | 783 | 410 | 373 | 0 | money_banking:742, bank_and_branch:21 | `ia__whatismo1947__what-is-money.mp4` |
| drone | 774 | 552 | 19 | 203 | landscapes_timelapse:199, ambience_beds:172 | `ia__20130206seattlecitycouncildrones__seattle-city-council-public-safety-civil-rights-and-technolo.mp4` |
| observation | 772 | 4 | 768 | 0 | space_nasa:731, science_tech:27 | `nasa__iss045e013851__earth-observation-from-the-international-space-station.jpg` |
| blue | 771 | 254 | 511 | 6 | ocean_nature:216, money_banking:47 | `loc__2020724560__the-now-as-of-2019-blue-star-diner-along-old-u-s-highway-60.tif` |
| man | 766 | 496 | 261 | 9 | courtroom_justice:186, newspapers_printing:73 | `coverr__4931__an-old-man-looking-out-of-the-window.mp4` |
| deer | 762 | 173 | 588 | 1 | wildlife_animals:749, americana_1930s_1970s:3 | `pixabay_extra__i_1586373__deer-fawn-young-deer-wild-bambi-fallow-deer-cub-forest-anima.jpg` |
| crewmember | 756 | 0 | 756 | 0 | space_nasa:756 | `nasa__iss034e039331__earth-observations-taken-by-expedition-34-crewmember.jpg` |
| wood | 752 | 65 | 244 | 443 | sfx_human_movement:421, courtroom_justice:89 | `freesound__155858__footsteps-in-factory-hall-on-wood-and-concrete-wav.mp3` |
| haer | 746 | 0 | 746 | 0 | factory_manufacturing:619, goods_in_motion:105 | `wikimedia__File_PHOTOCOPY_OF_CA._1934_VIEW_OF_AUTOS_COMING_OFF_ASSEMBLY__file-photocopy-of-ca-1934-view-of-autos-coming-off-assembly.tif` |
| design | 742 | 256 | 485 | 1 | textures_backgrounds:337, prison_jail:76 | `met__452365__velvet-fragment-with-bird-and-flower-design.jpg` |
| fla | 742 | 3 | 739 | 0 | space_nasa:569, science_tech:161 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| ship | 734 | 164 | 561 | 9 | goods_in_motion:446, japan:97 | `loc__2017692837__production-m-4-tanks-hull-members-of-an-m-4-tank-on-a-positi.tif` |
| center fla | 734 | 0 | 734 | 0 | space_nasa:568, science_tech:160 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| park | 733 | 142 | 549 | 42 | courtroom_justice:212, wildlife_animals:97 | `loc__ca09005868__official-souvenir-book-and-program-of-the-athletic-events-of.jpg` |
| expedition crewmember | 733 | 0 | 733 | 0 | space_nasa:733 | `nasa__iss034e039331__earth-observations-taken-by-expedition-34-crewmember.jpg` |
| interior | 730 | 42 | 635 | 53 | courtroom_justice:227, police_modern:108 | `loc__2009632448__orange-county-government-center-goshen-new-york-interior-cou.tif` |
| earth observation | 724 | 1 | 723 | 0 | space_nasa:721, landscapes_timelapse:3 | `nasa__iss045e013851__earth-observation-from-the-international-space-station.jpg` |
| battery | 721 | 4 | 716 | 1 | war_history:690, japan:17 | `nara__6471418-12947993__an-iraqi-artillery-battery-abandoned-during-operation-desert.jpeg` |
| table | 720 | 126 | 590 | 4 | police_modern:247, prison_jail:136 | `loc__2024800161__management-of-the-post-office-department-august-9-1876-laid.jpg` |
| harbor | 719 | 211 | 507 | 1 | navy_harbor:317, japan:316 | `loc__ed-1__the-islander-friday-harbor-wash-june-17-1897.jpg` |
| computer | 718 | 355 | 315 | 48 | science_tech:507, business_corporate:76 | `ia__univac-commercial-classic-old-vintage__classic-tv-commercial-for-a-univac-computer.mp4` |
| light | 716 | 269 | 364 | 83 | prison_jail:184, textures_backgrounds:61 | `loc__mt0107__anaconda-historic-district-electric-light-building-101-103-m.tif` |
| vehicle | 715 | 202 | 509 | 4 | police_modern:256, space_nasa:249 | `nara__6418527-13170342__a-pioneer-i-remotely-piloted-vehicle-rpv-is-readied-for-flig.jpeg` |
| room | 713 | 152 | 495 | 66 | police_modern:194, science_tech:113 | `loc__93515056__supreme-court-room.tif` |
| walking | 704 | 403 | 62 | 239 | courtroom_justice:302, sfx_human_movement:228 | `coverr__8360__walking-to-the-mountain-top.mp4` |
| town | 695 | 124 | 544 | 27 | small_town:286, world_cities:184 | `loc__2017789244__main-street-of-bourne-ghost-mining-town-oregon.tif` |
| green | 688 | 409 | 279 | 0 | money_banking:100, economy_crisis:73 | `ia__green-archer-ep1__green-archer-the-chapter-1-prison-bars-beckon.mp4` |
| wind | 687 | 167 | 317 | 203 | science_tech:259, sfx_environment:166 | `nara__17443346-17453348__sb-switch-in-capacitor-bank-control-in-the-10x10-foot-wind-t.jpg` |
| technology | 677 | 449 | 228 | 0 | science_tech:442, business_corporate:62 | `ia__0559-threads-of-technology__threads-of-technology.mp4` |
| open | 670 | 39 | 85 | 546 | sfx_human_movement:514, courtroom_justice:19 | `freesound__158691__distant-thunder-and-rain-from-half-open-window-2-aif.mp3` |
| coral | 670 | 212 | 457 | 1 | ocean_nature:664, navy_harbor:2 | `nasa__PIA25861__study-uses-modis-data-to-determine-belize-coral-reef-risk.jpg` |
| people | 660 | 372 | 250 | 38 | courtroom_justice:92, selling_floor:80 | `mixkit__23042__business-people-signing-contracts.mp4` |
| council | 658 | 648 | 10 | 0 | government_buildings:645, world_cities:3 | `ia__committee-04-02-2012__city-council-committee-meeting-april-2nd-2012.mp4` |
| beautiful | 655 | 541 | 114 | 0 | government_buildings:192, textures_backgrounds:114 | `coverr__8352__beautiful-rocky-shoreline.mp4` |
| reef | 653 | 225 | 427 | 1 | ocean_nature:634, money_banking:10 | `nasa__PIA25861__study-uses-modis-data-to-determine-belize-coral-reef-risk.jpg` |
| wild | 651 | 236 | 414 | 1 | wildlife_animals:553, landscapes_timelapse:15 | `pixabay_extra__i_1586373__deer-fawn-young-deer-wild-bambi-fallow-deer-cub-forest-anima.jpg` |
| window | 649 | 79 | 553 | 17 | prison_jail:305, retail_commerce:72 | `loc__2010718829__historic-courthouse-window-detail-federal-building-and-u-s-c.jpg` |
| force | 649 | 24 | 621 | 4 | space_nasa:245, japan:132 | `loc__11003805__historical-sketch-of-the-police-service-of-hartford-from-163.jpg` |
| spacex | 649 | 34 | 615 | 0 | space_nasa:648, science_tech:1 | `nasa__iss074e0723937__a-spacex-dragon-cargo-spacecraft-departs-from-the-internatio.jpg` |
| day | 644 | 72 | 526 | 46 | space_nasa:290, government_buildings:70 | `loc__2017802009__interior-of-courtroom-during-trial-of-automobile-accident-ca.tif` |
| mill | 644 | 2 | 637 | 5 | factory_manufacturing:606, stock_market_exchange:19 | `loc__2017810761__pouring-water-on-hot-ashes-from-the-blast-furnace-bethlehem.tif` |
| federal | 641 | 9 | 632 | 0 | courtroom_justice:428, government_buildings:117 | `loc__2010719020__interior-courtroom-william-j-nealon-federal-building-and-u-s.jpg` |
| flag | 639 | 532 | 107 | 0 | government_buildings:526, japan:22 | `mixkit__13312__flag-of-china-waving-in-the-wind.mp4` |
| washington | 637 | 22 | 615 | 0 | government_buildings:235, money_banking:144 | `loc__2011632073__supreme-court-building-washington-d-c.jpg` |
| woman | 627 | 364 | 262 | 1 | courtroom_justice:96, hands_and_transactions:95 | `ia__thewomaninthewindow1944__the-woman-in-the-window-1944-fritz-lang-edward-g-robinson-jo.mp4` |
| temple | 626 | 193 | 414 | 19 | japan:556, government_buildings:25 | `pixabay_extra__i_9348003__shrine-torii-japan-fushimi-nature-temple-kyoto-fushimi-inari.jpg` |
| white | 620 | 151 | 465 | 4 | wildlife_animals:78, prison_jail:49 | `loc__2012645740__supreme-court-part-i-white-plains-new-york.tif` |
| flight | 616 | 84 | 532 | 0 | space_nasa:300, science_tech:169 | `met__399885__an-allegory-of-the-rest-on-the-flight-into-egypt.jpg` |
| keyboard | 610 | 64 | 125 | 421 | sfx_mechanical:421, science_tech:78 | `freesound__437631__keyboard.mp3` |
| marine | 603 | 117 | 486 | 0 | ocean_nature:259, war_history:148 | `loc__2025876483__alaska-seal-and-fur-company-letter-from-the-secretary-of-the.jpg` |
| red | 597 | 165 | 429 | 3 | wildlife_animals:167, space_nasa:59 | `loc__ia0068__montgomery-county-courthouse-courthouse-square-red-oak-montg.tif` |
| mammal | 597 | 143 | 454 | 0 | wildlife_animals:438, government_buildings:132 | `pixabay_extra__i_9372866__fallow-deer-deer-nature-forest-wild-mammal-wildlife-animal-f.jpg` |
| wallpaper | 595 | 475 | 120 | 0 | government_buildings:185, textures_backgrounds:101 | `ia__the-lazarus-man-s-1-e-09-the-wallpaper-prison__the-lazarus-man-s1e09-the-wallpaper-prison.mp4` |
| steel | 591 | 7 | 583 | 1 | factory_manufacturing:528, prison_jail:15 | `loc__pa3339__u-s-steel-duquesne-works-blast-furnace-plant-along-monongahe.tif` |
| waterfall | 585 | 71 | 462 | 52 | landscapes_timelapse:474, sfx_environment:52 | `pixabay_extra__i_5312692__waterfall-sweden-water-nature-landscape-flow-forest-bach-fjl.jpg` |
| first | 585 | 30 | 554 | 1 | space_nasa:241, science_tech:111 | `loc__10022234__our-police-a-history-of-the-baltimore-force-from-the-first-w.jpg` |
| space shuttle | 584 | 1 | 583 | 0 | space_nasa:548, science_tech:25 | `nasa__sts093-704-087__earth-observations-taken-from-space-shuttle-columbia-during.jpg` |
| capitol | 580 | 18 | 562 | 0 | government_buildings:565, courtroom_justice:8 | `loc__2005684916__united-states-capitol.tif` |
| lights | 570 | 337 | 232 | 1 | textures_backgrounds:167, world_cities:136 | `coverr__284__blurred-christmas-lights.mp4` |
| mount | 570 | 56 | 511 | 3 | japan:517, landscapes_timelapse:11 | `nara__6480382-13053086__the-site-of-the-new-armory-being-constructed-by-naval-mobile.jpeg` |
| snow | 560 | 190 | 358 | 12 | landscapes_timelapse:199, japan:120 | `loc__2018663275__neon-rich-nightime-view-of-the-snow-cap-diner-near-seligman.tif` |
| nara | 560 | 4 | 556 | 0 | factory_manufacturing:418, depression_hardship:30 | `pixabay_extra__i_6963458__temple-night-view-yakushiji-temple-world-cultural-heritage-n.jpg` |
| aircraft | 558 | 24 | 534 | 0 | factory_manufacturing:333, space_nasa:45 | `loc__2017691815__women-aircraft-workers-women-man-america-s-machines-in-a-wes.tif` |
| nature landscape | 550 | 273 | 277 | 0 | landscapes_timelapse:285, ocean_nature:72 | `pixabay_extra__i_9247234__mountain-nature-landscape-peak-travel-forest-outdoors-summit.jpg` |
| lake | 549 | 189 | 341 | 19 | japan:107, wildlife_animals:81 | `loc__wi0580__town-of-lake-water-tower-municipal-building-4001-south-sixth.tif` |
| spacecraft | 547 | 12 | 535 | 0 | space_nasa:491, science_tech:54 | `nasa__KSC-03pd1288__kennedy-space-center-fla-orbital-sciences-l-1011-aircraft-ta.jpg` |
| mars | 544 | 8 | 536 | 0 | space_nasa:531, science_tech:6 | `nasa__KSC-03pp2101__kennedy-space-center-fla-from-a-burst-of-fire-and-smoke-the.jpg` |
| tower | 542 | 71 | 467 | 4 | space_nasa:109, small_town:100 | `loc__2021758099__an-old-tractor-sits-below-the-town-water-tower-in-funk-nebra.tif` |
| skyline | 540 | 136 | 396 | 8 | world_cities:353, business_corporate:113 | `nara__6490754-13178018__an-aerial-port-side-view-of-the-nuclear-powered-aircraft-car.jpeg` |
| shop | 537 | 105 | 431 | 1 | retail_commerce:127, factory_manufacturing:109 | `loc__2018700911__assuming-this-streetcorner-emergency-call-box-outside-a-wig.tif` |
| fish | 533 | 230 | 302 | 1 | ocean_nature:447, science_tech:24 | `nasa__KSC-03pd2367__kennedy-space-center-fla-justin-manley-of-the-national-ocean.jpg` |
| city council | 531 | 529 | 2 | 0 | government_buildings:528, world_cities:2 | `ia__committee-04-02-2012__city-council-committee-meeting-april-2nd-2012.mp4` |
| north | 525 | 51 | 466 | 8 | factory_manufacturing:119, government_buildings:64 | `loc__2010642234__historic-police-call-boxes-painted-in-stricking-colors-north.jpg` |
| glass | 521 | 67 | 426 | 28 | factory_manufacturing:154, business_corporate:107 | `loc__2025871752__report-on-the-manufactures-of-the-united-states-at-the-tenth.jpg` |
| science | 513 | 211 | 301 | 1 | science_tech:286, space_nasa:162 | `met__190159__allegory-of-science.jpg` |
| typing | 511 | 88 | 21 | 402 | sfx_mechanical:401, newspapers_printing:64 | `freesound__801120__typewriter-typing-03.mp3` |
| country | 507 | 344 | 131 | 32 | government_buildings:290, small_town:103 | `ia__germany-country-under-the-rule-of-law-role-model-or-illusion__germany-country-under-the-rule-of-law-role-model-or-illusion.mp4` |
| uss | 507 | 81 | 426 | 0 | navy_harbor:284, japan:151 | `nara__6455958-13543540__navy-musicians-play-at-a-colors-ceremony-aboard-the-guided-m.jpeg` |
| facility | 506 | 8 | 497 | 1 | space_nasa:358, science_tech:124 | `nasa__KSC-03pd2314__kennedy-space-center-fla-viewed-from-below-the-space-infrare.jpg` |
| control | 504 | 24 | 479 | 1 | science_tech:308, space_nasa:133 | `loc__14020358__the-police-control-of-the-slave-in-south-carolina.jpg` |
| paper | 500 | 59 | 315 | 126 | sfx_human_movement:125, money_banking:112 | `loc__2024851477__letter-from-the-secretary-of-the-treasury-transmitting-a-com.jpg` |
| training | 500 | 87 | 413 | 0 | war_history:207, space_nasa:151 | `loc__23010642__the-police-recruit-police-manual-of-physical-training.jpg` |
| department | 499 | 7 | 492 | 0 | retail_commerce:290, selling_floor:88 | `loc__24006610__history-of-the-seattle-police-department-1912.jpg` |
| sea ocean | 498 | 246 | 252 | 0 | ocean_nature:397, goods_in_motion:25 | `pixabay_extra__i_2562529__sea-ocean-water-waves-nature-beach-shore-coast-aerial-brown.jpg` |
| united | 496 | 38 | 458 | 0 | government_buildings:164, money_banking:62 | `loc__2005684916__united-states-capitol.tif` |
| sand | 495 | 124 | 329 | 42 | landscapes_timelapse:193, ocean_nature:132 | `nara__6509148-13020915__an-american-landing-craft-air-cushion-lcac-amphibious-vehicl.jpeg` |
| police | 493 | 61 | 429 | 3 | police_modern:264, police_period:187 | `loc__2016799032__police-station-belle-isle.tif` |
| dark | 492 | 130 | 107 | 255 | ambience_beds:138, bgm_general:117 | `freesound__614546__myst-dark-drone-synth-female-vocal-choir-atmo-ambience-cinem.mp3` |
| front | 489 | 28 | 414 | 47 | factory_manufacturing:87, newspapers_printing:68 | `loc__2010718821__historic-courthouse-front-door-federal-building-and-u-s-cour.jpg` |
| stage | 487 | 44 | 443 | 0 | space_nasa:459, goods_in_motion:5 | `nasa__sl3-114-1625__view-of-the-expended-s-ivb-second-stage-of-skylab-3-space-ve.jpg` |
| meeting | 484 | 415 | 69 | 0 | government_buildings:407, ocean_nature:15 | `ia__committee-04-02-2012__city-council-committee-meeting-april-2nd-2012.mp4` |
| air force | 484 | 8 | 476 | 0 | space_nasa:242, japan:70 | `loc__sd0059__ellsworth-air-force-base-group-administration-secure-storage.tif` |
| pad | 479 | 14 | 432 | 33 | space_nasa:394, science_tech:47 | `nasa__KSC-03pd2314__kennedy-space-center-fla-viewed-from-below-the-space-infrare.jpg` |
| winter | 476 | 200 | 259 | 17 | landscapes_timelapse:98, japan:73 | `loc__2017802628__untitled-photo-possibly-related-to-a-new-england-housewife-f.tif` |
| nasa's | 476 | 23 | 453 | 0 | space_nasa:386, science_tech:77 | `nasa__GSFC_20171208_Archive_e000273__nasa-s-hubble-captures-the-beating-heart-of-the-crab-nebula.jpg` |
| time | 471 | 185 | 262 | 24 | space_nasa:158, landscapes_timelapse:75 | `loc__2013650116__there-was-time-for-fun-and-games-last-night-near-w-123rd-pol.tif` |
| abandoned | 470 | 98 | 369 | 3 | economy_crisis:351, courtroom_justice:37 | `loc__2014631684__abandoned-buildings-and-water-tower-in-what-is-now-a-ghost-t.jpg` |
| two | 468 | 34 | 419 | 15 | space_nasa:209, science_tech:46 | `loc__2020635862__composite-photograph-of-two-images-police-officers-standing.tif` |
| state | 468 | 197 | 269 | 2 | government_buildings:337, courtroom_justice:21 | `loc__ny0910__court-of-appeals-interiors-moved-from-state-capitol-building.tif` |
| elephant | 468 | 14 | 454 | 0 | wildlife_animals:456, courtroom_justice:6 | `noaa__An_elephant_seal_from_NOAA__an-elephant-seal-from-noaa.jpg` |
| summer | 460 | 210 | 164 | 86 | ocean_nature:113, sfx_environment:63 | `pixabay_extra__v_218714__beach-ocean-sea-summer-holiday-wave-nature-beautiful-beautif.mp4` |
| floor | 452 | 68 | 191 | 193 | sfx_human_movement:185, money_banking:70 | `freesound__451862__footsteps-shoes-dirty-concrete-unfinished-basement-floor-fla.mp3` |
| june | 451 | 60 | 388 | 3 | space_nasa:276, government_buildings:61 | `loc__ed-1__the-interior-journal-stanford-ky-june-6-1879.jpg` |
| work | 451 | 162 | 283 | 6 | science_tech:123, business_corporate:81 | `loc__19013898__practical-police-work-what-to-do-and-how-to-do-it.jpg` |
| currency | 451 | 204 | 247 | 0 | money_banking:446, newspapers_printing:3 | `loc__2025848106__reimbursement-for-currency-destroyed-by-fire-may-31-1916-com.jpg` |
| africa | 449 | 113 | 316 | 20 | wildlife_animals:239, landscapes_timelapse:67 | `loc__2021645979__an-auction-sale-parade-market-square-cape-town-south-africa.tif` |
| wooden | 448 | 50 | 302 | 96 | courtroom_justice:99, sfx_human_movement:94 | `nara__6489223-13220985__a-crewman-repairs-wooden-planking-on-the-weather-deck-of-the.jpeg` |
| port | 443 | 178 | 264 | 1 | goods_in_motion:150, government_buildings:122 | `loc__2017707160__storefront-rock-port-missouri.tif` |
| transport | 443 | 168 | 275 | 0 | goods_in_motion:127, police_modern:74 | `nara__204839921-204839922__a-large-group-of-the-nine-hundred-7th-air-force-men-bound-fo.jpg` |
| metal | 442 | 46 | 220 | 176 | prison_jail:126, sfx_human_movement:107 | `loc__2020744163__a-vintage-metal-water-tower-in-grambling-louisiana-near-the.tif` |
| black | 441 | 165 | 261 | 15 | textures_backgrounds:51, prison_jail:35 | `loc__2020744163__a-vintage-metal-water-tower-in-grambling-louisiana-near-the.tif` |
| abstract | 441 | 410 | 31 | 0 | textures_backgrounds:208, money_banking:65 | `mixkit__44818__abstract-video-of-a-liquid-with-dark-ink-flowing.mp4` |
| open close | 440 | 0 | 3 | 437 | sfx_human_movement:427, sfx_mechanical:8 | `freesound__395648__open-close-door-quietly-1-mp3.mp3` |
| beautiful wallpaper | 438 | 421 | 17 | 0 | government_buildings:174, textures_backgrounds:94 | `pixabay_extra__v_218714__beach-ocean-sea-summer-holiday-wave-nature-beautiful-beautif.mp4` |
| rocks | 437 | 146 | 240 | 51 | ocean_nature:180, landscapes_timelapse:93 | `nasa__KSC-03pd1877__kennedy-space-center-fla-on-launch-complex-17-a-cape-canaver.jpg` |
| one | 436 | 23 | 406 | 7 | space_nasa:224, money_banking:40 | `loc__2019691079__one-of-dozens-of-examples-of-exemplary-public-art-and-archit.tif` |
| iss | 436 | 17 | 419 | 0 | space_nasa:402, science_tech:32 | `nasa__sts111-373-018__zenith-view-of-the-iss-silhouetted-against-earth-s-limb-take.jpg` |
| wall | 435 | 46 | 365 | 24 | stock_market_exchange:99, prison_jail:53 | `loc__93509655__the-centennial-wall-paper-printing-press-machinery-hall.tif` |
| bench | 434 | 16 | 417 | 1 | courtroom_justice:357, science_tech:39 | `nasa__as14-66-09325__u-s-flag-footprints-and-portable-work-bench-on-lunar-surface.jpg` |
| sign | 433 | 83 | 349 | 1 | economy_crisis:136, small_town:74 | `loc__2017881793__neon-sign-for-pink-cadillac-diner-wildwood-new-jersey.jpg` |
| after | 432 | 15 | 413 | 4 | space_nasa:165, navy_harbor:62 | `loc__2017802277__corner-of-main-street-center-of-town-after-blizzard-brattleb.tif` |
| outdoors | 431 | 97 | 323 | 11 | landscapes_timelapse:108, courtroom_justice:74 | `pixabay_extra__i_9247234__mountain-nature-landscape-peak-travel-forest-outdoors-summit.jpg` |
| wave | 431 | 283 | 124 | 24 | ocean_nature:339, sfx_environment:22 | `ia__ocean-wave__ocean-wave.mp4` |
| system | 431 | 52 | 377 | 2 | space_nasa:233, science_tech:76 | `loc__2024785551__letter-from-the-secretary-of-war-transmitting-a-system-of-fi.jpg` |
| field artillery | 429 | 0 | 429 | 0 | war_history:429 | `nara__6373154-14831058__sergeant-1st-class-michael-vinson-chief-of-firing-battery-fo.jpeg` |
| pennsylvania | 428 | 4 | 424 | 0 | factory_manufacturing:216, americana_1930s_1970s:114 | `loc__2010719020__interior-courtroom-william-j-nealon-federal-building-and-u-s.jpg` |
| home | 427 | 150 | 268 | 9 | factory_manufacturing:104, courtroom_justice:44 | `loc__18010549__police-reserve-and-home-defense-guard-manual.jpg` |
| army | 424 | 25 | 398 | 1 | war_history:311, government_buildings:45 | `loc__02011201__police-record-of-the-spies-smugglers-and-rebel-emissaries-in.jpg` |
| south | 422 | 42 | 367 | 13 | factory_manufacturing:95, wildlife_animals:33 | `loc__2006678359__photographs-of-the-strom-thurmond-federal-building-and-u-s-c.tif` |
| states | 422 | 32 | 390 | 0 | government_buildings:169, money_banking:62 | `loc__2005684916__united-states-capitol.tif` |
| moon | 422 | 91 | 331 | 0 | space_nasa:311, world_cities:19 | `nasa__S92-52043__galileo-view-of-moon-orbiting-the-earth-taken-from-3-9-milli.jpg` |
| left | 420 | 4 | 401 | 15 | space_nasa:187, war_history:40 | `loc__2018702648__what-s-left-of-an-old-silo-or-water-tower-now-a-graffiti-cov.tif` |
| small | 419 | 114 | 181 | 124 | small_town:125, sfx_environment:85 | `loc__2020723796__water-towers-are-a-common-and-readily-available-place-marke.tif` |
| market | 416 | 111 | 301 | 4 | world_cities:106, retail_commerce:103 | `loc__2017703204__tile-storefront-market-street-new-sharon-iowa.tif` |
| looking | 416 | 33 | 383 | 0 | factory_manufacturing:205, goods_in_motion:40 | `loc__afcwip004234__the-southwest-corner-of-grand-and-main-streets-looking-west.jpg` |
| naval | 416 | 27 | 389 | 0 | factory_manufacturing:224, navy_harbor:86 | `loc__2024798807__rifled-cannon-c-letter-from-the-secretary-of-the-navy-transm.jpg` |
| research | 416 | 37 | 379 | 0 | science_tech:301, space_nasa:63 | `nara__183510546-603086873__federal-hall-national-memorial-feha-manhattan-sites-masi-the.jpg` |
| test | 414 | 40 | 366 | 8 | space_nasa:245, science_tech:110 | `nara__6371796-14771933__preparations-are-made-to-test-fire-the-16-inch-50-cal-guns-o.jpeg` |
| finance | 412 | 256 | 156 | 0 | money_banking:389, business_corporate:13 | `pixabay_extra__v_91678__cards-coins-gambling-game-money-currency-finance-casino-happ.mp4` |
| west | 411 | 21 | 388 | 2 | factory_manufacturing:145, goods_in_motion:65 | `loc__2010718820__new-courthouse-federal-building-and-u-s-courthouse-wheeling.jpg` |
| cliff | 410 | 116 | 292 | 2 | ocean_nature:367, landscapes_timelapse:21 | `pixabay_extra__i_3749383__ocean-cliff-sea-nature-aerial-view-mountain-cliff-cliff-sea.jpg` |
| footsteps | 407 | 2 | 0 | 405 | sfx_human_movement:397, sfx_environment:8 | `freesound__155858__footsteps-in-factory-hall-on-wood-and-concrete-wav.mp3` |
| battalion | 407 | 6 | 401 | 0 | war_history:375, japan:25 | `loc__21016671__the-first-battalion-the-story-of-the-406th-telegraph-battali.jpg` |
| court | 406 | 40 | 366 | 0 | government_buildings:207, courtroom_justice:173 | `loc__2011632073__supreme-court-building-washington-d-c.jpg` |
| united states | 405 | 23 | 382 | 0 | government_buildings:157, money_banking:61 | `loc__2005684916__united-states-capitol.tif` |
| desert | 404 | 46 | 338 | 20 | landscapes_timelapse:251, war_history:52 | `loc__2018703101__the-round-cooling-towers-shown-in-the-distance-are-used-to-r.tif` |
| sun | 404 | 258 | 146 | 0 | landscapes_timelapse:135, ocean_nature:47 | `mixkit__52009__flying-over-an-arid-land-with-the-sun-shining-over-the-mesme.mp4` |
| laboratory | 398 | 67 | 331 | 0 | science_tech:260, space_nasa:99 | `loc__hi0722__u-s-naval-base-pearl-harbor-hospital-laboratory-hospital-way.tif` |
| company | 398 | 16 | 382 | 0 | factory_manufacturing:158, stock_market_exchange:47 | `loc__2020781976__to-the-public-in-embarking-in-the-enterprise-of-furnishing-p.jpg` |
| cargo | 397 | 55 | 341 | 1 | goods_in_motion:281, space_nasa:83 | `nara__204951332-204951333__troops-reporting-at-the-22nd-replacement-depot-located-in-ma.jpg` |
| symbol | 396 | 333 | 63 | 0 | government_buildings:284, money_banking:37 | `pixabay_extra__v_5433__currency-dollars-euro-money-symbol-commerce-bank-business-in.mp4` |
| county haer | 395 | 0 | 395 | 0 | factory_manufacturing:304, goods_in_motion:70 | `wikimedia__File_PHOTOCOPY_OF_CA._1934_VIEW_OF_AUTOS_COMING_OFF_ASSEMBLY__file-photocopy-of-ca-1934-view-of-autos-coming-off-assembly.tif` |
| seal | 393 | 7 | 382 | 4 | government_buildings:311, wildlife_animals:63 | `loc__2025876483__alaska-seal-and-fur-company-letter-from-the-secretary-of-the.jpg` |
| generated | 393 | 347 | 46 | 0 | science_tech:47, ocean_nature:43 | `pixabay_extra__v_365918__ai-generated-steampunk-robot-vintage-car-driver-vehicle-retr.mp4` |
| dpla | 392 | 0 | 392 | 0 | retail_commerce:94, stock_market_exchange:67 | `noaa__Assignment-_NOAA_2006_3137_48_National_Oceanic_and_Atmospher__assignment-noaa-2006-3137-48-national-oceanic-and-atmospheri.jpg` |
| fire | 391 | 115 | 213 | 63 | war_history:122, sfx_environment:61 | `loc__2022673071__trademark-registration-by-a-g-davis-for-police-special-mess.tif` |
| tunnel | 391 | 65 | 318 | 8 | science_tech:266, government_buildings:32 | `loc__99614948__main-street-entrance-to-the-tunnel.tif` |
| navy | 390 | 45 | 345 | 0 | factory_manufacturing:109, navy_harbor:94 | `loc__2024798807__rifled-cannon-c-letter-from-the-secretary-of-the-navy-transm.jpg` |
| equipment | 390 | 43 | 347 | 0 | space_nasa:86, newspapers_printing:75 | `loc__11003805__historical-sketch-of-the-police-service-of-hartford-from-163.jpg` |
| york | 389 | 54 | 333 | 2 | stock_market_exchange:75, world_cities:58 | `loc__2009632448__orange-county-government-center-goshen-new-york-interior-cou.tif` |
| hall | 386 | 28 | 350 | 8 | government_buildings:161, economy_crisis:77 | `loc__2022650295__city-hall-and-police-station-east-st-louis.tif` |
| live | 385 | 79 | 305 | 1 | space_nasa:285, war_history:47 | `nara__6510134-13130600__marines-from-india-battery-3rd-battalion-12th-marines-twenty.jpeg` |
| fence | 385 | 94 | 291 | 0 | prison_jail:352, small_town:6 | `nara__24485471-24485472__napa-ca-august-30-2014-a-steel-security-fence-marks-the-loca.jpg` |
| sls | 385 | 21 | 364 | 0 | space_nasa:385 | `nasa__B1B_Crew_Night_Launch__nasas-evolved-sls-block-1b-crew-rocket-night-launch.jpg` |
| dome | 384 | 4 | 379 | 1 | government_buildings:355, science_tech:11 | `nara__135801980-135801981__capitol-dome-at-night.jpg` |
| rural | 382 | 96 | 269 | 17 | small_town:262, japan:49 | `loc__2017763330__rural-types-on-main-street-of-ames-iowa.tif` |
| landing | 382 | 66 | 316 | 0 | war_history:179, space_nasa:162 | `nara__74241518-74241519__general-tanks-landing-craft-heavy-equipment-composite.jpg` |
| three | 381 | 8 | 371 | 2 | space_nasa:256, science_tech:53 | `loc__2019691079__one-of-dozens-of-examples-of-exemplary-public-art-and-archit.tif` |
| right | 376 | 5 | 354 | 17 | space_nasa:146, factory_manufacturing:44 | `loc__afcwip001417__view-down-east-main-street-near-the-corner-of-east-main-and.jpg` |
| cars | 375 | 290 | 55 | 30 | world_cities:100, police_modern:100 | `coverr__5837__cars-in-the-city-at-night.mp4` |
| birds | 373 | 139 | 49 | 185 | sfx_environment:155, wildlife_animals:109 | `freesound__513251__spring-distant-thunderstorm-suburban-birds-wind-rumble-ambie.mp3` |
| tree | 372 | 170 | 185 | 17 | wildlife_animals:67, landscapes_timelapse:53 | `loc__2017807299__hotel-on-main-street-of-town-lone-tree-north-dakota.tif` |
| ocean sea | 369 | 233 | 136 | 0 | ocean_nature:302, wildlife_animals:18 | `pixabay_extra__v_218714__beach-ocean-sea-summer-holiday-wave-nature-beautiful-beautif.mp4` |
| federal building | 367 | 0 | 367 | 0 | courtroom_justice:367 | `loc__2010719020__interior-courtroom-william-j-nealon-federal-building-and-u-s.jpg` |
| exploration | 367 | 5 | 362 | 0 | space_nasa:303, science_tech:25 | `nasa__MSFC-202100043__a-look-inside-the-international-space-station-payload-operat.jpg` |
| screen | 366 | 321 | 23 | 22 | money_banking:91, economy_crisis:77 | `coverr__3490__a-screen-showing-financial-analysis-of-a-cryptocurrency.mp4` |
| exercise | 365 | 48 | 317 | 0 | war_history:238, japan:37 | `nara__6350917-14698438__navy-and-marine-corps-troops-aboard-the-utility-landing-craf.jpeg` |
| construction | 362 | 145 | 214 | 3 | government_buildings:100, money_banking:44 | `loc__2025848536__to-authorize-the-secretary-of-the-navy-to-proceed-with-the-c.jpg` |
| bridge | 362 | 159 | 197 | 6 | world_cities:88, factory_manufacturing:46 | `loc__pa3386__bethlehem-steel-corporation-south-bethlehem-works-along-lehi.tif` |
| along | 361 | 12 | 346 | 3 | factory_manufacturing:251, war_history:34 | `loc__2012645659__view-of-store-fronts-along-main-street-in-benson-arizona.tif` |
| cityscape | 361 | 119 | 240 | 2 | world_cities:207, business_corporate:63 | `pixabay_extra__i_2945920__medieval-town-night-architecture-city-cityscape-europe-old-b.jpg` |
| crew- | 361 | 33 | 328 | 0 | space_nasa:360, science_tech:1 | `nasa__KSC-20240928-PH-JBS01_0031__nasa-s-spacex-crew-9-live-launch-coverage.jpg` |
| modern | 359 | 93 | 261 | 5 | business_corporate:108, government_buildings:47 | `loc__gdcmassbookdig-modernamericanra09unse__vol-9-electricity-for-locomotive-engineers-modern-american-r.jpg` |
| expedition crew | 359 | 5 | 354 | 0 | space_nasa:354, landscapes_timelapse:2 | `nasa__iss043e003041__earth-observation-taken-by-the-expedition-43-crew.jpg` |
| running | 358 | 276 | 16 | 66 | newspapers_printing:256, sfx_human_movement:40 | `mixkit__719__man-running-on-trail-in-the-park.mp4` |
| near | 357 | 14 | 307 | 36 | science_tech:52, space_nasa:51 | `loc__2010641511__historic-police-call-box-sheridan-kalorama-call-box-restorat.jpg` |
| desk | 357 | 116 | 237 | 4 | business_corporate:183, science_tech:73 | `loc__98000434__a-desk-book-of-printing-types-to-which-is-appended-a-condens.jpg` |
| crickets | 355 | 0 | 0 | 355 | sfx_environment:339, ambience_beds:13 | `freesound__637565__forest-boreal-steady-light-wind-breeze-through-trees-bird-cr.mp3` |
| engine | 354 | 12 | 225 | 117 | sfx_mechanical:112, space_nasa:90 | `loc__2017686449__a-water-tower-steam-engine-and-tender-at-tiny-osier-colorado.jpg` |
| second | 353 | 9 | 343 | 1 | space_nasa:217, science_tech:22 | `loc__2006675203__photographs-of-the-old-post-office-and-u-s-courthouse-300-we.tif` |
| hands | 353 | 180 | 173 | 0 | space_nasa:128, hands_and_transactions:68 | `ia__0555-master-hands-18-27-28-00__master-hands.mp4` |
| launch pad | 353 | 10 | 343 | 0 | space_nasa:316, science_tech:35 | `nasa__KSC-03pd2314__kennedy-space-center-fla-viewed-from-below-the-space-infrare.jpg` |
| animals | 352 | 175 | 176 | 1 | wildlife_animals:206, ocean_nature:63 | `pixabay_extra__i_1482712__roe-deer-kitz-wild-forest-red-deer-fawn-young-animals-young.jpg` |
| apollo | 351 | 3 | 348 | 0 | space_nasa:292, science_tech:51 | `nasa__GSFC_20171208_Archive_e001282__nasa-google-hangout-earthrise-a-new-visualization-45th-anniv.jpg` |
| government | 349 | 49 | 300 | 0 | government_buildings:220, factory_manufacturing:42 | `loc__2009632448__orange-county-government-center-goshen-new-york-interior-cou.tif` |
| spacex crew- | 349 | 25 | 324 | 0 | space_nasa:349 | `nasa__KSC-20240928-PH-JBS01_0031__nasa-s-spacex-crew-9-live-launch-coverage.jpg` |
| sunrise | 348 | 224 | 119 | 5 | landscapes_timelapse:121, ocean_nature:39 | `coverr__9808__sunrise-at-the-beach-dock.mp4` |
| pearl | 348 | 90 | 258 | 0 | japan:232, navy_harbor:103 | `loc__2017821634__untitled-photo-possibly-related-to-corner-of-montgomery-and.tif` |
| department store | 348 | 5 | 343 | 0 | retail_commerce:287, selling_floor:57 | `nara__7385143-16038921__civil-defense-window-display-at-sage-allen-department-store.jpg` |
| lccn | 348 | 0 | 348 | 0 | money_banking:95, factory_manufacturing:52 | `wikimedia__File_Bowery_bread_line_LCCN2014683026.jpg__file-bowery-bread-line-lccn2014683026-jpg.jpg` |
| machine | 347 | 70 | 264 | 13 | newspapers_printing:130, factory_manufacturing:77 | `loc__2024793653__purchase-of-press-and-separating-machine-for-office-of-treas.jpg` |
| island | 346 | 114 | 227 | 5 | ocean_nature:107, japan:44 | `loc__94501754__troops-of-the-185th-inf-40th-div-take-cover-behind-advancing.tif` |
| germany | 346 | 112 | 232 | 2 | government_buildings:100, courtroom_justice:64 | `loc__16002885__germany-and-england-the-real-issue.jpg` |
| plumage | 346 | 239 | 107 | 0 | wildlife_animals:305, courtroom_justice:12 | `pixabay_extra__v_191159__gull-bird-snow-plumage-sitting-winter-wildlife.mp4` |
| tourism | 345 | 116 | 229 | 0 | world_cities:93, government_buildings:69 | `pixabay_extra__i_4472321__street-tower-krakow-poland-tourism-europe-urban-travel-krako.jpg` |
| autumn | 343 | 157 | 178 | 8 | courtroom_justice:68, japan:56 | `met__435740__allegory-of-autumn.jpg` |
| treasury | 343 | 1 | 342 | 0 | money_banking:321, courtroom_justice:13 | `loc__2024862449__metropolitan-police-district-of-columbia-letter-from-the-sec.jpg` |
| county courthouse | 342 | 2 | 340 | 0 | courtroom_justice:324, americana_1930s_1970s:10 | `loc__nc0306__polk-county-courthouse-courthouse-street-columbus-polk-count.tif` |
| plant | 342 | 87 | 255 | 0 | factory_manufacturing:178, prison_jail:28 | `loc__pa3339__u-s-steel-duquesne-works-blast-furnace-plant-along-monongahe.tif` |
| highway | 341 | 255 | 74 | 12 | small_town:165, police_modern:44 | `ia__freedomh1956__freedom-highway-part-i.mp4` |
| europe | 341 | 121 | 220 | 0 | world_cities:174, government_buildings:67 | `loc__20010376__a-service-of-love-in-war-time-american-friends-relief-work-i.jpg` |
| shipping | 340 | 39 | 300 | 1 | goods_in_motion:282, factory_manufacturing:28 | `met__335971__allegory-of-shipping.jpg` |
| pearl harbor | 339 | 88 | 251 | 0 | japan:232, navy_harbor:103 | `loc__2017821634__untitled-photo-possibly-related-to-corner-of-montgomery-and.tif` |
| sls rocket | 339 | 13 | 326 | 0 | space_nasa:339 | `nasa__KSC-01172026-Artemis_II_Rollout-27__nasa-s-sls-rocket-and-orion-spacecraft-rollout-to-launch-pad.jpg` |
| ground | 338 | 218 | 113 | 7 | space_nasa:256, war_history:29 | `nasa__jsc2020m000053_Space_to_Ground_352_201223__space-to-ground-the-year-that-was-12-23-2020.mp4` |
| tokyo | 338 | 122 | 215 | 1 | japan:199, science_tech:40 | `nara__134403789-134403790__suburban-tokyo-street.jpg` |
| peak | 338 | 11 | 327 | 0 | landscapes_timelapse:291, japan:38 | `pixabay_extra__i_9247234__mountain-nature-landscape-peak-travel-forest-outdoors-summit.jpg` |
| italy | 337 | 106 | 227 | 4 | world_cities:73, government_buildings:64 | `loc__2015631001__main-street-in-italy-texas-gabriel-j-penn-postmaster-in-waxa.jpg` |
| wire | 337 | 46 | 291 | 0 | prison_jail:324, war_history:3 | `pixabay_extra__i_2387571__barbed-wire-desktop-backgrounds-daniel-detail-shooting-macro.jpg` |
| church | 336 | 59 | 267 | 10 | government_buildings:144, prison_jail:46 | `loc__2019713338__church-of-the-nativity-taken-from-the-police-station.tif` |
| space telescope | 336 | 4 | 332 | 0 | science_tech:283, space_nasa:53 | `nasa__carina-nebula__james-webb-space-telescope-nircam-image-of-the-cosmic-cliffs.png` |
| main | 335 | 7 | 323 | 5 | small_town:124, americana_1930s_1970s:63 | `loc__az0060__police-station-south-main-street-tucson-pima-county-az.tif` |
| cash | 334 | 175 | 159 | 0 | money_banking:320, retail_commerce:6 | `mixkit__47005__a-lot-of-cash-over-a-rotating-background.mp4` |
| distant | 333 | 4 | 75 | 254 | sfx_environment:179, ambience_beds:67 | `freesound__158691__distant-thunder-and-rain-from-half-open-window-2-aif.mp3` |
| empty | 333 | 152 | 174 | 7 | courtroom_justice:166, prison_jail:46 | `met__717106__standing-male-angel-holding-an-empty-bowl-and-looking-down-a.jpg` |
| laptop | 332 | 111 | 181 | 40 | science_tech:130, business_corporate:58 | `nasa__KSC-03pd2375__kennedy-space-center-fla-dr-grant-gilmore-dynamac-corp-utili.jpg` |
| war | 331 | 155 | 174 | 2 | courtroom_justice:98, factory_manufacturing:60 | `loc__afc1982010-wl-012__colquitt-county-courthouse-and-civil-war-monument-moutrie-ge.jpg` |
| morning | 330 | 126 | 90 | 114 | sfx_environment:104, courtroom_justice:33 | `ia__1913-07-27-all-in-readiness-for-franks-trial-monday-morning__sunday-27th-july-1913-all-in-readiness-for-leo-franks-trial.mp4` |
| young | 330 | 149 | 180 | 1 | wildlife_animals:75, hands_and_transactions:37 | `loc__2018676094__another-young-newsboy-in-hartford-conn-august-26-1924-locati.tif` |
| shopping | 328 | 121 | 207 | 0 | economy_crisis:129, selling_floor:92 | `pixabay_extra__i_1180397__akihabara-tokyo-night-japan-japanese-shopping-asian-technolo.jpg` |
| complex | 328 | 2 | 324 | 2 | space_nasa:174, science_tech:95 | `nasa__KSC-03pd2879__vandenberg-afb-calif-the-mobile-service-tower-on-space-launc.jpg` |
| fuji | 328 | 60 | 267 | 1 | japan:315, war_history:9 | `nara__6480382-13053086__the-site-of-the-new-armory-being-constructed-by-naval-mobile.jpeg` |
| dollar | 327 | 109 | 218 | 0 | money_banking:305, bank_and_branch:9 | `pixabay_extra__i_1974694__dollar-money-currency-trade-poverty-paper-bill-bank-note-fin.jpg` |
| workers | 326 | 51 | 274 | 1 | factory_manufacturing:97, space_nasa:82 | `loc__2018676631__group-of-workers-at-sagamore-mills-1-some-of-these-were-boys.tif` |
| usa | 324 | 72 | 238 | 14 | war_history:101, government_buildings:55 | `nara__6628231-12912625__us-army-usa-soldiers-from-the-95th-chemical-company-special.jpeg` |
| railroad | 324 | 32 | 292 | 0 | americana_1930s_1970s:128, goods_in_motion:103 | `loc__2025169042__pennsylvania-railroad-locomotive-prr-937.tif` |
| historic | 324 | 21 | 303 | 0 | government_buildings:87, courtroom_justice:55 | `loc__2010718822__historic-courthouse-federal-building-and-u-s-courthouse-whee.jpg` |
| atmosphere | 323 | 68 | 172 | 83 | space_nasa:132, landscapes_timelapse:46 | `nasa__iss035e014335__earth-atmosphere-observations-taken-by-the-expedition-35-cre.jpg` |
| ksc | 322 | 1 | 321 | 0 | space_nasa:258, science_tech:59 | `nasa__KSC-20240402-PH-KLS02_0143__earth-day-at-ksc.jpg` |
| cotton | 321 | 0 | 318 | 3 | factory_manufacturing:309, sfx_human_movement:3 | `loc__2018674972__it-seems-a-pity-that-some-of-the-spinning-frames-are-so-larg.tif` |
| rock | 321 | 101 | 214 | 6 | ocean_nature:157, landscapes_timelapse:56 | `loc__2006675203__photographs-of-the-old-post-office-and-u-s-courthouse-300-we.tif` |
| stream | 320 | 73 | 110 | 137 | sfx_environment:135, landscapes_timelapse:104 | `freesound__165286__nolde-forest-small-stream-wind-in-trees-wav.mp3` |
| coral reef | 320 | 99 | 220 | 1 | ocean_nature:319, sfx_environment:1 | `nasa__PIA25861__study-uses-modis-data-to-determine-belize-coral-reef-risk.jpg` |
| agency | 320 | 3 | 317 | 0 | space_nasa:237, science_tech:55 | `loc__ca10005037__rules-and-regulations-for-the-government-of-the-preventive-f.jpg` |
| facade | 320 | 16 | 304 | 0 | government_buildings:121, business_corporate:80 | `loc__2016645834__rear-facade-federal-building-u-s-courthouse-anniston-alabama.jpg` |
| pattern | 319 | 131 | 188 | 0 | textures_backgrounds:234, government_buildings:14 | `met__388376__embroidery-pattern-with-seven-six-pointed-stars-and-four-cor.jpg` |
| astronaut | 319 | 18 | 301 | 0 | space_nasa:223, science_tech:86 | `nasa__41G-11-027__astronaut-kathryn-sullivan-using-binoculars-for-magnifed-vie.jpg` |
| district | 318 | 26 | 289 | 3 | government_buildings:77, business_corporate:67 | `loc__2024862449__metropolitan-police-district-of-columbia-letter-from-the-sec.jpg` |
| support | 318 | 7 | 311 | 0 | war_history:153, science_tech:52 | `nara__6637256-13169765__advancing-us-marine-corps-usmc-personnel-from-charlie-compan.jpeg` |
| may | 317 | 67 | 241 | 9 | space_nasa:80, government_buildings:62 | `loc__99614110__illinois-the-anarchist-labor-troubles-in-chicago-a-police-pa.tif` |
| building courthouse | 315 | 0 | 315 | 0 | courtroom_justice:315 | `loc__2010719020__interior-courtroom-william-j-nealon-federal-building-and-u-s.jpg` |
| aircraft factory | 313 | 0 | 313 | 0 | factory_manufacturing:313 | `loc__2017691821__women-aircraft-workers-nice-work-if-you-can-get-it-a-leadman.tif` |
| hardware | 312 | 15 | 297 | 0 | retail_commerce:137, space_nasa:102 | `loc__2025871752__report-on-the-manufactures-of-the-united-states-at-the-tenth.jpg` |
| atlantis | 311 | 0 | 311 | 0 | space_nasa:296, science_tech:13 | `nasa__sts076-370-020__view-of-the-shuttle-orbiter-atlantis-from-the-mir-space-stat.jpg` |
| east | 310 | 25 | 281 | 4 | factory_manufacturing:83, government_buildings:56 | `loc__afcwip001417__view-down-east-main-street-near-the-corner-of-east-main-and.jpg` |
| aboard | 310 | 29 | 281 | 0 | space_nasa:103, navy_harbor:95 | `nara__204839927-204839928__a-large-group-of-gis-of-the-7th-air-force-bound-for-the-unit.jpg` |
| european | 309 | 46 | 261 | 2 | space_nasa:159, world_cities:77 | `nasa__jsc2015e106168__in-the-integration-facility-at-the-baikonur-cosmodrome-in-ka.jpg` |
| square | 309 | 21 | 281 | 7 | small_town:166, courtroom_justice:36 | `loc__sd0013__union-county-courthouse-courthouse-square-elk-point-union-co.tif` |
| opening | 308 | 142 | 40 | 126 | sfx_human_movement:118, money_banking:82 | `ia__200333-panama-pacific-international-exposition-opening-parad__panama-pacific-international-exposition-opening-parade.mp4` |
| surface | 307 | 32 | 271 | 4 | space_nasa:234, ocean_nature:14 | `nasa__STS053-105-002__sts-53-view-of-ov-103-s-payload-bay-plb-the-moon-and-earth-s.jpg` |
| allegory | 303 | 0 | 303 | 0 | americana_1930s_1970s:303 | `met__436278__allegory.jpg` |
| off | 302 | 80 | 196 | 26 | newspapers_printing:62, space_nasa:57 | `loc__2017688181__welty-s-general-store-founded-in-1889-in-dubois-wyoming-the.jpg` |
| side | 301 | 10 | 264 | 27 | factory_manufacturing:65, japan:36 | `loc__afcwip004231__three-buildings-on-the-west-side-of-main-street-north-of-gra.jpg` |
| ambience | 299 | 2 | 1 | 296 | ambience_beds:152, sfx_environment:112 | `freesound__750799__empty-office-ambience.mp3` |
| tropical | 299 | 135 | 157 | 7 | ocean_nature:228, landscapes_timelapse:20 | `loc__2023696450__sculpture-flotilla-of-kayaks-in-a-tropical-storm-in-the-silv.tif` |
| april | 299 | 69 | 223 | 7 | war_history:73, government_buildings:53 | `loc__ed-1__the-interior-journal-stanford-ky-april-12-1872.jpg` |
| inside | 298 | 15 | 232 | 51 | space_nasa:64, science_tech:45 | `loc__2020742211__one-rarely-sees-two-town-water-towers-close-together-such-as.tif` |
| motion | 298 | 270 | 28 | 0 | wildlife_animals:63, prison_jail:46 | `mixkit__27133__flock-of-pigeons-on-the-street-slow-motion.mp4` |
| processing | 298 | 4 | 294 | 0 | space_nasa:192, science_tech:99 | `nasa__KSC-03pd3282__vandenberg-afb-calif-in-the-nasa-spacecraft-processing-facil.jpg` |
| through | 297 | 70 | 117 | 110 | sfx_environment:86, war_history:35 | `nara__12008267-15829962__photograph-of-american-troops-marching-through-the-streets-o.jpg` |
| american | 297 | 48 | 248 | 1 | money_banking:66, government_buildings:41 | `loc__2022637908__an-american-police-station-in-peking-china.tif` |
| environment | 297 | 24 | 273 | 0 | space_nasa:182, science_tech:57 | `loc__2018673748__113-indianapolis-newsboys-waiting-for-the-base-ball-edition.tif` |
| shore | 296 | 117 | 145 | 34 | ocean_nature:169, war_history:36 | `loc__2019691079__one-of-dozens-of-examples-of-exemplary-public-art-and-archit.tif` |

## 3. Known name-vs-content traps

| source | trap |
|---|---|
| noaa | Titles are survey codes (`20260130aC0894545w340345n`). Nothing about the frame is knowable from the name — must be eyeballed. |
| nypl | 27k scans share the title `new-york-city-directory`; the subject index cannot separate them. Treat as page scans, not footage. |
| ia | Real titles, but talking-head lectures/podcasts pass the relevance gate (measured 4/24 on the courtroom_justice sheet). Check before staging. |
| factory (older shelf) | Filenames are the SEARCH QUERY, verified ~50% wrong. Use `select_factory_assets.py` + FACTORY_SUBTYPE_INVENTORY.v001.md, never the name. |
