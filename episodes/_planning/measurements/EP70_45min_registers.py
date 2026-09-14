import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pool = json.load(open("pool.json", encoding="utf-8"))
ARCH = {"ia", "nara", "loc", "nypl", "smithsonian", "met", "wikimedia"}
items = [(v["t"] or "", (v["src"] or "").lower()) for v in pool.values()]

def count(rx):
    p = re.compile(rx, re.I)
    tot = set(); arch = 0
    for i, (t, s) in enumerate(items):
        if p.search(t):
            tot.add(i)
            if s in ARCH:
                arch += 1
    return tot, arch

CAND = {
 "A_martin_wronghouse": {
  "front door / suburban house": r"\b(front door|doorway|door|porch|house|houses|home|homes|residential|suburb\w*|neighborhood|neighbourhood|driveway|mailbox|yard|lawn)\b",
  "police / swat / tactical": r"\b(police|policeman|officer|officers|swat|tactical|raid|law enforcement|patrol|squad car|cop|cops|handcuff\w*|arrest\w*|federal agent|fbi)\b",
  "night street / dark residential": r"\b(night|nighttime|dark|darkness|streetlight|street light|headlight|flashlight|dusk|predawn|dawn)\b",
  "courtroom / judge / trial": r"\b(court|courtroom|courthouse|judge|jury|trial|attorney|lawyer|hearing|verdict|supreme court|appeal|gavel)\b",
  "documents / filings": r"\b(document\w*|paperwork|file|files|filing|form|forms|report|records|paper|letter|envelope|stamp\w*|signature)\b",
  "family interior / children": r"\b(family|child|children|kid|kids|boy|girl|mother|father|parent|bedroom|living room|kitchen|closet|toy|toys)\b",
  "gps / phone / map screen": r"\b(gps|navigation|map|maps|smartphone|phone|screen|satellite|route|street sign|address)\b",
  "washington / federal buildings": r"\b(washington|capitol|supreme court|federal building|government building|monument|marble|column\w*|flag)\b",
 },
 "B_midas_algorithm": {
  "office / cubicle / clerk": r"\b(office|offices|desk|cubicle|clerk|worker|workers|employee|staff|call center|call centre|typing|keyboard|paperwork)\b",
  "computer / server / data": r"\b(computer|server|servers|data|database|screen|monitor|code|coding|software|algorithm|network|machine learning|artificial intelligence|digital)\b",
  "mail / letters / notices": r"\b(mail|mailbox|letter|letters|envelope|envelopes|postal|notice|stamp\w*|post office)\b",
  "money / paycheck / bank": r"\b(money|cash|dollar|dollars|bank|banking|paycheck|payroll|wage|wages|check|cheque|atm|coin|coins|tax|taxes|refund|invoice|bill|bills)\b",
  "courtroom / judge": r"\b(court|courtroom|courthouse|judge|jury|trial|attorney|lawyer|hearing|verdict|supreme court|appeal|gavel)\b",
  "unemployment / factory worker": r"\b(unemploy\w*|jobless|layoff|laid off|factory|plant|assembly|industrial|warehouse|worker|labor|labour|union|job|employment)\b",
  "home / kitchen table": r"\b(home|house|kitchen|living room|table|apartment|family|sitting)\b",
  "state capitol / michigan / civic": r"\b(capitol|state house|government|civic|city hall|michigan|detroit|agency|bureau|department)\b",
 },
 "C_torres_burnpits": {
  "military / deployment / iraq": r"\b(military|army|soldier|soldiers|troop|troops|marine|reserve|deployment|deployed|iraq|afghanistan|desert|base|convoy|helmet|uniform|veteran|combat|war)\b",
  "fire / smoke / burning pit": r"\b(fire|fires|burning|burn|smoke|smoky|flame|flames|ash|ashes|blaze|incinerat\w*|trash|garbage|waste|dump|landfill)\b",
  "hospital / breathing / oxygen": r"\b(hospital|clinic|medical|doctor|nurse|patient|lung|lungs|breath\w*|oxygen|inhaler|x-ray|scan|ward|treatment|illness|sick)\b",
  "police cruiser / trooper / texas": r"\b(patrol|trooper|highway patrol|police car|squad car|cruiser|sheriff|texas|badge|siren)\b",
  "courtroom / supreme court": r"\b(court|courtroom|courthouse|judge|jury|trial|attorney|lawyer|hearing|verdict|supreme court|appeal|gavel)\b",
  "documents / claim forms": r"\b(document\w*|paperwork|file|files|form|forms|claim|report|records|paper|letter|envelope|denial)\b",
  "home / family / porch": r"\b(home|house|family|porch|kitchen|living room|wife|husband|child|children|yard)\b",
  "flag / capitol / congress": r"\b(flag|capitol|congress|senate|washington|memorial|veterans|ceremony|salute)\b",
 },
 "D_serrano_forfeiture": {
  "border crossing / port of entry": r"\b(border|frontier|checkpoint|customs|immigration|crossing|port of entry|fence|wall|mexico|passport|inspection)\b",
  "pickup truck / vehicle": r"\b(truck|pickup|pick-up|vehicle|vehicles|car|cars|van|suv|driving|driver|steering|dashboard|engine|tire|tires|wheel)\b",
  "impound lot / fence / storage": r"\b(impound|lot|yard|storage|fence|fenced|chain link|padlock|gate|parking|abandoned|junkyard|salvage)\b",
  "cash / money / bank": r"\b(money|cash|dollar|dollars|bank|banking|wallet|bill|bills|coin|coins|payment|loan|debt)\b",
  "courtroom / judge": r"\b(court|courtroom|courthouse|judge|jury|trial|attorney|lawyer|hearing|verdict|supreme court|appeal|gavel)\b",
  "highway / rural kentucky": r"\b(highway|freeway|interstate|road|roads|route|rural|country road|farm|farmland|barn|field|fields|hills|kentucky|driving)\b",
  "documents / seizure notice": r"\b(document\w*|paperwork|form|forms|notice|letter|envelope|file|files|stamp\w*|signature|report|records)\b",
  "guns / ammunition / permit": r"\b(gun|guns|firearm|firearms|pistol|handgun|ammunition|ammo|bullet|bullets|magazine|holster|permit|licence|license)\b",
 },
 "E_strickland_exoneration": {
  "prison / cell / bars": r"\b(prison|jail|cell|cells|bars|inmate|inmates|incarcerat\w*|penitentiary|corrections|barbed|razor wire|guard)\b",
  "courtroom / judge / trial": r"\b(court|courtroom|courthouse|judge|jury|trial|attorney|lawyer|hearing|verdict|testimony|witness|appeal|gavel)\b",
  "PERIOD 1970s kansas city": r"\b(1970s|1978|1979|seventies|super 8|8mm|16mm|kansas city|missouri)\b",
  "police / detective / lineup": r"\b(police|detective|officer|officers|interrogation|lineup|line-up|mugshot|arrest\w*|handcuff\w*|precinct|station|badge)\b",
  "documents / case file": r"\b(document\w*|file|files|paperwork|transcript|record|records|report|affidavit|statement|paper|folder|archive)\b",
  "release / freedom / gate": r"\b(release|freed|freedom|gate|reunion|embrace|hug|sunlight|sky)\b",
  "family / home / aging": r"\b(family|mother|brother|sister|home|house|kitchen|elderly|aging|grave|cemetery|funeral)\b",
  "money / compensation / capitol": r"\b(money|cash|dollar|dollars|check|cheque|compensation|capitol|legislature|senate|bill|law)\b",
 },
 "F_detroit_facerecognition": {
  "city street / detroit / retail": r"\b(city|street|streets|urban|downtown|storefront|shop|store|retail|mall|sidewalk|traffic|detroit|michigan)\b",
  "cctv / surveillance camera": r"\b(cctv|surveillance|security camera|camera|cameras|monitor|monitors|footage|recording|lens)\b",
  "face / biometric / scanning": r"\b(face|faces|facial|portrait|biometric|scan|scanning|recognition|identity|match|profile|crowd)\b",
  "police / arrest / precinct": r"\b(police|officer|officers|arrest\w*|handcuff\w*|precinct|station|patrol|squad car|detective|badge|jail|cell|booking)\b",
  "computer / algorithm / database": r"\b(computer|software|algorithm|database|data|screen|monitor|server|code|network|artificial intelligence|machine learning|digital)\b",
  "courtroom / lawsuit": r"\b(court|courtroom|courthouse|judge|jury|trial|attorney|lawyer|hearing|verdict|settlement|appeal|gavel)\b",
  "family / driveway / daughters": r"\b(family|child|children|daughter|daughters|wife|husband|home|house|driveway|yard|neighborhood|porch)\b",
  "documents / warrant / photo": r"\b(document\w*|warrant|paperwork|form|forms|file|files|report|records|paper|photograph|photo|print)\b",
 },
 "G_ssa_overpayment": {
  "mailbox / letter / notice": r"\b(mail|mailbox|letter|letters|envelope|envelopes|postal|notice|stamp\w*|post office|delivery|package)\b",
  "elderly person at home": r"\b(elderly|old man|old woman|senior|seniors|retire\w*|grandmother|grandfather|aging|wheelchair|cane|walker|nursing|caregiver)\b",
  "government office / counter": r"\b(government|agency|office|offices|counter|queue|waiting room|clerk|bureau|department|federal building|civic|city hall)\b",
  "money / bank / check": r"\b(money|cash|dollar|dollars|bank|banking|check|cheque|deposit|atm|coin|coins|payment|benefit|pension|wallet|purse|budget|bill|bills)\b",
  "kitchen table / paperwork": r"\b(kitchen|table|home|house|apartment|living room|paperwork|document\w*|form|forms|calculator|pen|writing|sitting)\b",
  "computer / database / records": r"\b(computer|database|data|screen|monitor|server|software|system|records|file|files|digital|network)\b",
  "capitol / congress / hearing": r"\b(capitol|congress|senate|hearing|washington|testimony|committee|podium|microphone|flag)\b",
  "grocery / pharmacy / daily life": r"\b(grocery|supermarket|pharmacy|medicine|prescription|shopping|cart|store|food|meal|bus|transit)\b",
 },
 "H_pge_campfire": {
  "wildfire / flames / smoke": r"\b(wildfire|fire|fires|flame|flames|burning|blaze|smoke|smoky|ember|embers|ash|ashes|forest fire|bushfire)\b",
  "burned town / ruins / debris": r"\b(ruin|ruins|rubble|debris|destroyed|destruction|burned|burnt|charred|wreckage|collapse|abandoned|shell)\b",
  "power lines / utility / grid": r"\b(power line|power lines|powerline|electric|electricity|utility|grid|transmission|pylon|transformer|pole|poles|cable|wire|wires|substation)\b",
  "evacuation / emergency": r"\b(evacuat\w*|traffic|convoy|highway|road|driving|escape|fleeing|siren|emergency|firefighter|fire truck|helicopter)\b",
  "trailer / rebuild / construction": r"\b(trailer|caravan|rv|temporary|shelter|tent|construction|rebuild\w*|building site|foundation|framing|housing)\b",
  "courtroom / bankruptcy / corporate": r"\b(court|courtroom|courthouse|judge|trial|attorney|lawyer|hearing|bankrupt\w*|corporate|boardroom|shareholder|stock|wall street|trading)\b",
  "forest / california landscape": r"\b(forest|forests|pine|pines|woods|woodland|tree|trees|mountain|ridge|valley|california|sierra|canyon)\b",
  "documents / claim forms": r"\b(document\w*|paperwork|form|forms|claim|file|files|letter|envelope|report|records|paper|check|cheque)\b",
 },
}

NEED_CUTS = 400
NEED_DISTINCT = 327
col = lambda u: "GREEN" if u <= 0.15 else ("AMBER" if u <= 0.40 else "RED")
out = {}
for cand, buckets in CAND.items():
    print("=" * 96)
    print(cand)
    union = set(); rows = {}
    for name, rx in buckets.items():
        s, a = count(rx)
        union |= s
        rows[name] = (len(s), a)
        print("  %-42s %7d  archival %5d" % (name, len(s), a))
    u_cuts = NEED_CUTS / len(union) if union else 99
    u_dist = NEED_DISTINCT / len(union) if union else 99
    print("  %-42s %7d" % ("DISTINCT UNION", len(union)))
    print("  utilisation 400 cuts  = %.4f  %s" % (u_cuts, col(u_cuts)))
    print("  utilisation 327 dist. = %.4f  %s" % (u_dist, col(u_dist)))
    out[cand] = {"buckets": rows, "union": len(union),
                 "util_400": round(u_cuts, 4), "util_327": round(u_dist, 4)}
json.dump(out, open("registers.json", "w", encoding="utf-8"), indent=2)
print("\nwrote registers.json  (pool =", len(items), "distinct playable video)")
