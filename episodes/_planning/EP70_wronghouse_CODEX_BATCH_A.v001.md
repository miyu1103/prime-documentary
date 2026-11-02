# EP70 · THE WRONG HOUSE — IMAGE ORDER (Codex) v001

**Episode `PD-2026-070-wronghouse` · slug `wronghouse` · 2026-08-12**
**GENERATED FILE. Do not hand-edit — edit `04_scenes/build_codex_order.v001.py` and re-run.**
**Contract:** `episodes/PD-2026-070-wronghouse/episode_spec.v001.json` — `mandatory_stills` **W001.png … W160.png (160 ids)**, `people_plates` **26 ids, named individually**, 209 `forbidden_subjects`, 23 `forbidden_claims`, `era_setting` **USA, 1973–2026**.
**Design:** `EP70_wronghouse_FILM_BIBLE.v001.md` · **Facts:** `EP70_wronghouse_FACTS_LEDGER.v001.md` · **Script:** `EP70_wronghouse_script.en.v001.md`.

---

## 0. Who generates these, and with what

- **Every plate here is a Codex commission.** Do not start a local model to fill this order.
- Local generation is an exception, not a lane: commercially-clear tuned paths (**SD3.5 Large** via `sd35_gen.py`, or **SDXL** via `gen_max.ps1`) **only** to repair a Codex plate or fill an emergency gap. **Bare SDXL is not allowed. FLUX.1-dev is not allowed in any deliverable.**
- **Long edge ≥ 3840** on every plate (spec v2 row 5).
- Every plate is an **illustration**, never evidence (CLAUDE invariant 11).

## 1. The measured trap, and the rule that follows from it

**Codex is one-shot.** One motif, one beat, **two images per prompt**. A prompt that asks for two subjects returns one muddled frame, and the builder now refuses a subject containing two `and`s. Every prompt below therefore names exactly one thing, and asks for it twice from two camera positions — `W0nn.png` and `W0nnb.png`.

## 2. What is barred, absolutely

| Never depict | Why |
|---|---|
| **any child, or any person who reads as under 20** | a real seven-year-old is the centre of this story, he is about sixteen now, and he is never on screen (`forbidden_claims` 11) |
| **Curtrina Martin, Toi Cliatt, Lawrence Guerra, Joseph Riley, any agent, judge, justice or attorney** | CLAUDE invariant 11. Where a person is needed the plate is a hand, a shoulder, a back or a pair of shoes — **26 people plates, not one face** |
| **a photograph of either real house** | the plates show the *type*, never the address |
| **any readable document, warrant, docket, order or newspaper** | a generated document presented as a record is a fabricated record (`forbidden_claims` 19). Type is texture, never text |
| **the moment of violence, a weapon pointed at a person, a wound, fire** | the substitution table in `EP70_wronghouse_FILM_BIBLE.v001.md` §7 is binding |

## 3. Shared blocks — appended by the builder to every prompt

```
STYLE     Photoreal documentary still, 3:2 landscape, full-frame camera at f/2.0, natural available light only, muted desaturated palette of slate blue, sodium amber and neutral grey, deep shadows that retain detail, fine 35mm grain, shallow depth of field, nothing centred, no on-screen text of any kind, long edge 3840 px.

NEGATIVE  no text, no lettering, no numbers rendered as readable type, no watermark, no logo, no badge insignia, no cartoon, no illustration, no 3D render, no anime, no child, no person under 20, no blood, no wound, no fire, no flame, no explosion, no smoke, no military, no soldier, no war, no gore, no gavel, no scales of justice, no flag, no political imagery, no crypto, no stock-photo smiling, no eye contact with camera, no recognisable real person, no identifiable face

ACT_4 ONLY (period lock) Strict period lock, April 1973 to 1974, United States. In frame: crackle-finish enamel, chrome, brown and avocado tones, wood veneer, rotary telephone, typewriter, carbon paper, incandescent light, single-glazed windows, wide American sedans with no badge visible. NOT in frame: any mobile phone, any flat screen, any LED, any computer, any modern vehicle, any modern signage, any plastic that did not exist in 1973.
```

## 4. The order

Each row is one prompt. **`script anchor` is the sentence in the narration this plate exists for** — the image matches the meaning of the line it sits under, which is the whole point (`feedback_visual_narration_meaning_match`). Every anchor is checked by the builder to be a real substring of a spoken line before this file is written.

### HOOK — 8 plates

| id | people | script anchor | subject (one motif) |
|---|---|---|---|
| `W001` |  | Five o'clock in the morning | A dark bedroom ceiling seen from floor height, one thin bar of streetlight across it through a gap in the blinds |
| `W002` |  | another house | A suburban street-name sign on a metal pole at night, the lettering deliberately out of focus and unreadable |
| `W003` |  | another house | A domestic mailbox on a post at the end of a driveway, half in shadow, the numerals turned away from camera |
| `W004` |  | Same corner. Same shape. | A beige split-level American suburban house on a corner lot with one large tree, photographed as architecture from across the road before sunrise |
| `W005` |  | Same corner. Same shape. | A second beige split-level American suburban house on a corner lot with one large tree, the same framing as the first, near-identical |
| `W006` | P | a woman is asleep | A woman's hand asleep on a bedside table beside a glass of water, cropped at the wrist, no face |
| `W007` |  | shotgun in the bedroom closet | The inside of a domestic wardrobe: a rail of hanging clothes, shoes below, a sliver of light under the door |
| `W008` |  | He does not know he went to the wrong one | A residential front door photographed from inside the house, closed, chain hanging loose, hallway dark |

### OP — 2 plates

| id | people | script anchor | subject (one motif) |
|---|---|---|---|
| `W009` |  | True stories about the systems | An empty American residential street from above at first light, rows of driveways, no people, no cars moving |
| `W010` |  | True stories about the systems | A stack of unopened post on a hall floor beneath a letterbox, shot from above |

### ACT_1 — 25 plates

| id | people | script anchor | subject (one motif) |
|---|---|---|---|
| `W011` |  | a line of vehicles leaves a car park | An empty tarmac car park before dawn, sodium lights, painted bays, tyre marks, no vehicles |
| `W012` |  | It is still dark | Vehicle headlights approaching along a suburban road at night, seen low from the kerb, the cars themselves lost in glare |
| `W013` | P | six-member SWAT team | The shoulder and upper arm of a person in matt black tactical body armour, gloved hand at their side, framed tight, head out of frame |
| `W014` | P | seven search warrants and seventeen arrest warrants | A gloved hand resting on a stack of stapled legal papers on a car seat, torch beam across the top sheet, no readable type |
| `W015` | P | The team forms up on the front step | Boots and shins of several people standing close together on a concrete front step at night, from ankle height |
| `W016` | P | Somebody knocks | A gloved knuckle a few centimetres from a painted wooden front door, caught mid-approach |
| `W017` |  | Then they wait ten to twenty seconds | A closed front door photographed straight on from outside in the dark, nothing happening, the porch light off |
| `W018` |  | two adults are asleep | An empty hallway inside a house at night, doors ajar on both sides, seen from floor level |
| `W019` |  | A seven-year-old is asleep across the hall | The corner of a bed with a rumpled blanket pulled up, no person, no toys, a strip of hallway light on the wall |
| `W020` |  | The door comes in | A splintered domestic doorframe at the strike plate, timber torn outward, brass latch bent, morning light on the damage |
| `W021` |  | a flash-bang grenade goes off in the hallway | A ceiling and cornice blown to pure white by a single instant of light, the room's edges just visible |
| `W022` |  | hid in a bedroom closet | The interior of a walk-in wardrobe from inside, looking out through a gap in the doors into a lit bedroom |
| `W023` | P | dragged Mr. Cliatt from the closet | A man's back and shoulders face down on a carpeted bedroom floor, wrists together behind him, head out of frame |
| `W024` |  | trained his weapon on Ms. Martin | The angular shadow of a rifle and a torch thrown across a plain interior wall, the objects themselves out of frame |
| `W025` | P | some mail with the home's address on it | A gloved hand lifting two envelopes from a carpeted floor beside a skirting board, address block turned away |
| `W026` |  | The address was also on the mailbox | A mailbox at the end of a driveway in flat morning light, the flag down, numerals present but softly out of focus |
| `W027` |  | the street sign at the corner | A suburban street-name sign against a pale dawn sky, shot from below, lettering deliberately illegible |
| `W028` |  | filed in a federal courthouse in Atlanta | A civil complaint's cover page seen at a steep raking angle, headings visible as shapes only, no readable words |
| `W029` |  | her first instinct was to run to her son's room | An open bedroom doorway seen from the far end of a dark hallway, a rectangle of grey light on the floor |
| `W030` |  | that is where he kept his shotgun | The high shelf of a domestic wardrobe, folded blankets and a shoebox, one empty space where something rectangular has been |
| `W031` | P | before Mr. Cliatt reached his firearm | A man's outstretched hand in the dark, fingers open, reaching towards the top of a wardrobe, arm only |
| `W032` | P | held her at gunpoint in the corner of that closet | A woman's bare forearm and flat palm pressed against a carpeted floor in the corner of a wardrobe, cropped at the elbow |
| `W033` |  | pulled the covers over his head | The edge of a duvet raised into a low tent shape on a small bed, empty room, dawn light |
| `W034` | P | He apologised | A business card held between two fingers over a kitchen counter, the printing on it a blur |
| `W035` |  | A splintered front door frame | A rectangle of chipboard screwed over a broken front door from outside, the house otherwise ordinary in daylight |

### ACT_2 — 23 plates

| id | people | script anchor | subject (one motif) |
|---|---|---|---|
| `W036` |  | the FBI opened an investigation into violent gang activity | A wall-sized city map in a plain office, coloured pins clustered in one district, no legible place names |
| `W037` |  | criminal indictments against thirty people | Thirty identical buff file folders stood upright in a drawer, tabs blank |
| `W038` |  | There was an Operation Order | A thick ring binder open on a desk under a lamp, columns and boxes visible as structure only, no readable text |
| `W039` |  | a description of the house and a photograph of it | An overhead satellite-style view of an American suburban block, driveways and roofs, no labels |
| `W040` |  | Step-by-step directions with a map | A printed street map on a passenger seat with a route traced in ballpoint, place names out of focus |
| `W041` | P | watched the house through binoculars for more than two hours | A pair of hands resting on a steering wheel at night in a parked car, dashboard dark, street beyond the windscreen |
| `W042` | P | drove out earlier that month to look at it | A driver's forearm resting on an open car window sill, a suburban corner lot beyond in flat daylight |
| `W043` |  | A tight stairway and a stoop | A narrow concrete stoop and three steps leading to a front door, iron handrail, framed square |
| `W044` |  | Windows on either side | Two windows flanking a front door, blinds down, seen from the driveway at eye level |
| `W045` |  | picked the car park the team would gather in | An email inbox on a monitor at an angle steep enough that nothing is readable, cursor visible |
| `W046` |  | who breaches, who carries the shield | A hand-drawn diagram of numbered figures in a line on lined paper, ballpoint, no words |
| `W047` |  | He dimmed his headlights so nobody would notice the car | A car's dipped headlights on a dark residential road, the beam falling short of the kerb |
| `W048` |  | a personal GPS device. His own. | A small consumer satellite-navigation unit on a windscreen mount at night, screen glow only, no readable map |
| `W049` |  | everything he saw confirmed he was at the right one | A large mature tree overhanging a suburban corner lot at night, silhouetted against a sodium sky |
| `W050` |  | There was one thing in the driveway | The rear quarter of a dark two-door American coupe parked on a residential driveway at night, no badge visible |
| `W051` |  | Something to steer by in the dark | A dark car's paintwork reflecting a single streetlight, abstract, shot close |
| `W052` |  | the mailbox, at the end of the driveway | A mailbox at the end of a driveway photographed from a passing car at night, motion-blurred |
| `W053` | P | they asked for the GPS | A hand pulling open an empty desk drawer under a lamp, one clean rectangle in the dust where an object sat |
| `W054` |  | threw away his GPS device | A domestic wheelie bin at a kerbside on a suburban street in daylight, lid closed |
| `W055` |  | no longer exists | A wall of grey server racks in a cold corridor, one bay empty |
| `W056` |  | seven of the sixteen personnel | Sixteen mobile phones face down in a grid on a plain table, seven of the places empty |
| `W057` |  | no metadata on them at all | A photographic contact sheet on a light box with every frame blank white |
| `W058` |  | there was no rule to break | An open policy manual on a desk, the facing page entirely blank, lamp light across it |

### ACT_3 — 28 plates

| id | people | script anchor | subject (one motif) |
|---|---|---|---|
| `W059` |  | she does not go to work | An office desk with a chair pushed in and a coat still on the hook behind it, blinds half closed |
| `W060` |  | The boy changes schools | An empty school corridor at dusk, lockers on both sides, no people |
| `W061` |  | Then he changes schools again | A second empty school corridor, different floor colour, same emptiness, seen from the far end |
| `W062` |  | they have been in counselling | Two empty upholstered chairs facing each other in a small consulting room, a box of tissues on a side table |
| `W063` | P | An insurer covers the damage to the house | A hand signing a form on a clipboard on a kitchen counter, pen visible, writing illegible |
| `W064` |  | you have to ask it first | A government-issue paper form on a wooden table, boxes and rules visible, no readable words |
| `W065` | P | they file a detailed tort claim with the FBI | A hand posting a brown envelope into a public post box on an American street in daylight |
| `W066` |  | a stack that is still growing today | A column of ring binders stacked chest high against an office wall, spines unlabelled |
| `W067` |  | In September twenty-nineteen they sue | A courthouse filing counter with a bell and a wire tray of documents, no staff in frame |
| `W068` |  | It takes three years | A wall clock in a beige institutional corridor, hands at an ordinary hour, paint slightly scuffed |
| `W069` | P | Depositions | A hand resting flat on a conference table beside a microphone, empty chairs beyond, window light from the left |
| `W070` |  | Geolocation data pulled from sixteen phones | A dense scatter of anonymous location dots over a plain grey grid on a monitor, no map, no labels |
| `W071` |  | both sides argue it out in front of a federal judge | An empty courtroom well seen from the public gallery: two counsel tables, a lectern, the bench beyond, nobody present |
| `W072` |  | the order comes down | A judge's bench from the well of an empty courtroom, one closed folder on it |
| `W073` |  | It runs to thirty-eight pages | A thick stapled order face down on a desk, page edges fanned, no readable text |
| `W074` |  | The court threw four of them out | Four buff folders dropped loose into a large recycling bin, seen from above |
| `W075` |  | the same appeals court that covers Georgia | A monumental American federal courthouse façade in flat overcast light, columns and steps, no signage legible |
| `W076` |  | how dangerous the target is | A police radio handset resting on a car seat, coiled cable, matt black, single window light |
| `W077` |  | But two claims survived | Two buff folders left alone on an otherwise empty desk under a lamp |
| `W078` |  | they had a live case | A courtroom door standing open onto a lit corridor, seen from inside the dark courtroom |
| `W079` |  | go and settle it | A small mediation room with a round table and four chairs, jug of water, blinds closed |
| `W080` |  | in a courthouse in Rome, Georgia | A modest county courthouse in a small American town, seen across an empty square in autumn light |
| `W081` |  | Case did not settle | A single sheet of paper alone in the centre of a large empty conference table |
| `W082` | P | asked the judge to change his mind | A hand sliding a stapled cover page across a counter towards camera, type visible only as texture |
| `W083` |  | a different court, in a different case | A shelf of bound case reporters in a law library, spines uniform, no legible titles |
| `W084` |  | eight days after Christmas | A domestic living room in early January, curtains open on a grey afternoon, one bare side table |
| `W085` |  | the Clerk is directed to close the case | A cardboard archive box being closed with its lid, seen from above, unlabelled |
| `W086` |  | marked at the top: do not publish | A stapled appellate opinion face down on a metal shelf among identical others |

### ACT_4 — 23 plates

| id | people | script anchor | subject (one motif) |
|---|---|---|---|
| `W087` |  | Sovereign immunity | The stone entablature of a 1930s American federal building photographed from below in hard sun, no lettering in frame |
| `W088` |  | a private bill, with your name on it | A 1970s congressional bill printed on folded paper, typewritten, seen at a raking angle, no readable words |
| `W089` |  | That was the remedy | A wooden pigeonhole rack in a government mailroom, 1970s, stuffed with paper |
| `W090` |  | Congress abolished it | A 1970s office desk with a manual typewriter, a stack of carbon paper and a rotary telephone, morning light |
| `W091` |  | April, nineteen seventy-three | A 1973 American residential street at night, wide sedans at the kerb, warm porch lights, telephone wires overhead |
| `W092` |  | Collinsville, Illinois | A small midwestern American town's main street in 1973, low brick storefronts, no legible signage, overcast |
| `W093` |  | a married couple | A 1973 domestic bedroom interior: chenille bedspread, wood-veneer headboard, bedside lamp with a fabric shade |
| `W094` |  | the sound of someone smashing down their door | A 1970s panelled front door burst inward off its hinges, seen from inside a dark hallway |
| `W095` |  | Fifteen state and federal officers ransacked the house | A 1973 living room after a search: drawers pulled out, cushions overturned, a lamp on its side |
| `W096` | P | tied the Giglottos up at gunpoint | Two pairs of wrists bound with cord on a 1970s patterned carpet, arms only, no faces |
| `W097` |  | had the wrong people | A 1973 kitchen table with two cold cups of coffee and an ashtray, chairs pushed back |
| `W098` |  | another house, belonging to a man named Donald Askew | A second 1973 American house exterior at night, screen door hanging open, porch light on |
| `W099` |  | they had acted on a bad tip | A 1970s handwritten note on a torn-off pad sheet, ballpoint, held under a desk lamp, words illegible |
| `W100` |  | became a national story | A 1973 newsstand rack of folded newspapers photographed from above at a steep angle, headlines unreadable |
| `W101` |  | the United States Senate looked into them | A 1970s Senate committee room: long raised bench, leather chairs, table microphones, empty |
| `W102` |  | no effective legal remedy | A 1970s typewritten committee report page seen edge-on under a lamp, text as texture only |
| `W103` |  | Congress amended the Federal Tort Claims Act | A 1974 statute book open on a wooden lectern in a law library, pages fanned, no readable print |
| `W104` |  | Assault. Battery. False imprisonment. | Six identical index-card slots in a wooden card catalogue drawer, 1970s, tabs blank |
| `W105` |  | innocent individuals who are subjected to raids | A 1973 American front door photographed from the street in daylight, ordinary, undamaged, mailbox at the kerb |
| `W106` |  | much less the pain, suffering and humiliation | A 1970s kitchen chair in an empty room, low afternoon sun across the floor |
| `W107` |  | built a door for it | A heavy 1930s bronze government door, closed, photographed straight on in flat light |
| `W108` |  | a second door behind it | A second identical bronze government door directly behind the first, seen through the opening of the first |
| `W109` |  | legislative history is not the law | A single printed statutory subsection on a page, photographed so close that only the shape of a line of type is legible |

### ACT_5 — 42 plates

| id | people | script anchor | subject (one motif) |
|---|---|---|---|
| `W110` |  | asked the Supreme Court of the United States to take their case | A bound petition on a marble counter, seen at a low angle, no readable text |
| `W111` |  | Almost nobody gets in | The west façade of the Supreme Court of the United States in flat morning light, steps empty |
| `W112` |  | distributed to the justices' conference three times | A polished conference table with nine empty chairs around it, one closed folder at each place |
| `W113` | P | the Court granted it | A hand placing a single sheet of paper on a marble step, weighted by a small stone, type illegible |
| `W114` |  | It granted the case on two questions only | Two identical closed folders side by side on a bench, nothing else in frame |
| `W115` | P | the Court went out and appointed a lawyer | A hand resting on the edge of an empty lectern in a wood-panelled courtroom, seen from the side |
| `W116` |  | Briefs came in from members of Congress | A trolley stacked with identical bound briefs in a marble corridor |
| `W117` |  | the case was called | A pair of tall courtroom doors from inside, closed, brass handles, red drapery to either side |
| `W118` | P | For the family, Patrick Jaicomo | A hand lifting a briefcase from a wooden bench in a courthouse corridor, coat folded beside it |
| `W119` | P | an Assistant to the Solicitor General | A dark suit sleeve and cuff resting on a lectern edge, hand relaxed, no face |
| `W120` |  | The recording is public | A vintage-style ribbon microphone on a stand against a dark background, single top light |
| `W121` |  | the argument arrives at a mailbox | A plain American mailbox on a post against a white studio background, hard single light, isolated like an exhibit |
| `W122` |  | you might look at the address of the house | A close macro of embossed house numerals on a metal mailbox, one digit sharp, the rest falling out of focus |
| `W123` |  | exposing the agents to potential lines of fire | A driveway seen from a mailbox's position looking back at a house, two dark windows facing the viewer |
| `W124` | P | Six people were about to walk up to a house | Backs of several people in dark clothing walking up a driveway before dawn, seen from behind and below, no faces |
| `W125` |  | making sure you're on the right street | A street-name sign at an intersection photographed straight on in daylight, lettering deliberately blurred |
| `W126` |  | a federal banking regulator | Two ordinary saloon cars stopped at an angle in an intersection in daylight, seen from a distance, no damage visible |
| `W127` | P | driving requires the constant exercise of discretion | A driver's hands on a steering wheel in daylight, windscreen showing an ordinary road |
| `W128` |  | He got the right target. He just had the wrong house. | Two identical suburban houses side by side in one frame, shot flat and symmetrical, nothing to tell them apart |
| `W129` |  | the Court answered | A marble courtroom interior with empty seating, seen from the rear, cold north light |
| `W130` |  | It was unanimous. Nine to nothing. | Nine identical high-backed chairs behind a long bench, empty, photographed straight on |
| `W131` | P | vacated, and the case is remanded | Gloved hands lifting a file box off a shelf in a records room |
| `W132` |  | did not give them a trial | An empty jury box, fourteen seats, dust in a shaft of window light |
| `W133` |  | still shut | A closed courtroom door at the end of a long marble corridor, seen from far away |
| `W134` |  | sent the record back to Georgia | A courier trolley of file boxes in a service corridor, strip lighting overhead |
| `W135` |  | One box. Four envelopes of sealed exhibits. | One cardboard archive box on a metal shelf with four large sealed manila envelopes standing in it |
| `W136` |  | the last thing that has ever happened | A docket screen on a monitor photographed at a steep angle, rows visible as bands, nothing readable |
| `W137` |  | asked both sides to write it new briefs | Two identical stacks of paper on opposite ends of a long table |
| `W138` |  | the court set a date | A wall-mounted paper calendar with one date circled in ink, the month name out of frame |
| `W139` |  | Courtroom: Atlanta three-three-nine | A closed courtroom door with a brass room number, the numerals softly out of focus |
| `W140` |  | three federal judges sat down to hear this case | A raised appellate bench with three empty chairs, seen from the well, warm wood |
| `W141` |  | sixty published cases since nineteen ninety | A long run of identical bound law reporters on a shelf, receding into shallow focus |
| `W142` |  | they are all over the place | Sixty loose index cards scattered face down across a dark table top, no order |
| `W143` |  | at the place described in the warrant | A single house on a suburban street isolated by a hard shaft of afternoon sun, its neighbours in shadow |
| `W144` | P | regardless whether you're an FBI agent or a private person | Two pairs of shoes side by side on a courthouse floor, one polished formal, one ordinary trainers |
| `W145` |  | the elephant in the room | A statute book left open and face down on a courtroom counsel table |
| `W146` |  | did not say when they would rule | An empty appellate bench photographed after a hearing, papers cleared, one water glass left |
| `W147` |  | In nineteen forty-six, Congress said | A mid-century American federal building's revolving door photographed from inside at dawn |
| `W148` |  | Thirteen ways the sentence | Thirteen identical closed doors along one institutional corridor, receding, all shut |
| `W149` |  | That is the gate that is still shut | A single closed steel gate in a plain concrete wall, no handle on this side |
| `W150` |  | two hundred and twenty-three entries | A wall of identical box files filling the frame edge to edge, unlabelled |
| `W151` |  | Not one of those entries is a trial | An empty courtroom photographed wide from the judge's position, every seat vacant |

### ENDING — 9 plates

| id | people | script anchor | subject (one motif) |
|---|---|---|---|
| `W152` |  | Six people made a mistake in the dark | A residential driveway at first light, an ordinary morning, one recycling bin at the kerb |
| `W153` |  | a system working exactly as designed | A mechanical interlock of brass gears in a display case, still, clean, perfectly meshed |
| `W154` |  | which is a good rule | A plain closed door with a well-made brass lock, photographed straight on in even light |
| `W155` |  | Stack them | Five closed doors photographed in sequence one behind another through their openings, receding to darkness |
| `W156` |  | waits nine years | A domestic hallway photographed at the same angle as the film's opening image, now in ordinary daylight, empty |
| `W157` |  | It is whether the mistake it made was the kind of mistake somebody was allowed to make | A single mailbox at the end of a driveway in warm late light, shot as a portrait, the whole frame given to it |
| `W158` |  | a wrong address, a wrong name, a wrong file | A dense grid of identical filing-cabinet drawer fronts filling the frame, one drawer very slightly open |
| `W159` |  | a panel of three judges holding a decision | Three empty chairs behind a bench in a dim courtroom, one shaft of late light across them |
| `W160` |  | When it lands, we will come back to it | An American suburban street at dusk, lights coming on in windows one by one, seen from the end of the road |

