import json, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
pool = json.load(open("pool.json", encoding="utf-8"))
ARCH = {"ia", "nara", "loc", "nypl", "smithsonian", "met", "wikimedia"}
items = [(v["t"] or "", (v["src"] or "").lower()) for v in pool.values()]

def hits(rx):
    p = re.compile(rx, re.I)
    s = set(); a = 0
    for i, (t, src) in enumerate(items):
        if p.search(t):
            s.add(i)
            if src in ARCH:
                a += 1
    return s, a

# The subset of each film whose frame MUST read as a specific thing.
# 400 cuts total; ~40% (160 cuts, ~131 distinct at 0.818) live on these registers.
NARROW = {
 "A_martin_wronghouse": {
   "residential front door / doorway": r"\b(front door|doorway|door|porch|driveway|mailbox)\b",
   "tactical police / raid / fbi": r"\b(swat|tactical|raid|police|officer|officers|law enforcement|fbi|federal agent|handcuff\w*)\b",
   "courtroom / supreme court interior": r"\b(courtroom|courthouse|supreme court|judge|jury|gavel|bench)\b",
 },
 "B_midas_algorithm": {
   "state agency office / clerk counter": r"\b(agency|bureau|government office|clerk|counter|cubicle|call center|call centre|department)\b",
   "mainframe / server / database screen": r"\b(server|servers|mainframe|database|data center|data centre|algorithm|software|code|monitor|screen)\b",
   "notice letter / envelope / mailbox": r"\b(letter|letters|envelope|envelopes|mailbox|mail|notice|postal)\b",
 },
 "C_torres_burnpits": {
   "iraq deployment / desert base": r"\b(iraq|afghanistan|desert|deployment|deployed|convoy|base|soldier|soldiers|troop|troops|army|military)\b",
   "open burning pit / smoke plume": r"\b(burn pit|burning|bonfire|incinerat\w*|landfill|dump|trash|garbage|waste|smoke|smoke plume)\b",
   "oxygen / lungs / respiratory care": r"\b(oxygen|lung|lungs|breath\w*|inhaler|respirator|ventilator|x-ray|hospital|clinic|patient)\b",
 },
 "D_serrano_forfeiture": {
   "border port of entry / customs booth": r"\b(border|checkpoint|customs|port of entry|crossing|immigration|mexico|passport)\b",
   "pickup truck / impound lot": r"\b(pickup|pick-up|truck|impound|tow|towed|chain link|padlock|storage lot)\b",
   "bullets / magazine / handgun": r"\b(bullet|bullets|ammunition|ammo|magazine|cartridge|handgun|pistol|firearm)\b",
 },
 "E_strickland_exoneration": {
   "PERIOD 1970s american street/interior": r"\b(1970s|1971|1972|1973|1974|1975|1976|1977|1978|1979|seventies|super 8|8mm|16mm)\b",
   "prison cell / bars / razor wire": r"\b(prison|jail|cell|cells|bars|inmate|penitentiary|razor wire|barbed|corrections)\b",
   "police lineup / mugshot / interrogation": r"\b(lineup|line-up|mugshot|interrogation|precinct|detective|booking)\b",
 },
 "F_detroit_facerecognition": {
   "cctv / security camera view": r"\b(cctv|surveillance|security camera|camera|footage|monitor|recording)\b",
   "face grid / biometric scan": r"\b(facial|biometric|face|faces|scan|scanning|recognition|identity)\b",
   "police station / booking / cell": r"\b(police|precinct|station|booking|jail|cell|handcuff\w*|arrest\w*|officer|officers)\b",
 },
 "G_ssa_overpayment": {
   "official letter / envelope / mailbox": r"\b(letter|letters|envelope|envelopes|mailbox|mail|notice|postal|post office)\b",
   "older person at home / caregiver": r"\b(elderly|senior|seniors|old man|old woman|grandmother|grandfather|retire\w*|caregiver|wheelchair|walker|cane|nursing)\b",
   "government counter / federal office": r"\b(government|federal building|agency|bureau|office|counter|waiting room|clerk|queue|department)\b",
 },
 "H_pge_campfire": {
   "wildfire flame front / ember storm": r"\b(wildfire|forest fire|flame|flames|blaze|ember|embers|burning|fire)\b",
   "burned-out town / foundations / ash": r"\b(burned|burnt|charred|ruin|ruins|rubble|debris|destroyed|ash|ashes|wreckage)\b",
   "power line / transmission tower": r"\b(power line|power lines|powerline|transmission|pylon|transformer|utility pole|substation|electric|grid)\b",
 },
}

NEED_NARROW_CUTS = 160
NEED_NARROW_DIST = 131
col = lambda u: "GREEN" if u <= 0.15 else ("AMBER" if u <= 0.40 else "RED")
out = {}
for cand, bk in NARROW.items():
    print("=" * 96)
    print(cand, "  -- NARROW CORE (the registers whose frame must read specifically)")
    union = set(); rows = {}
    for n, rx in bk.items():
        s, a = hits(rx)
        union |= s
        rows[n] = (len(s), a)
        print("  %-44s %6d  archival %5d" % (n, len(s), a))
    u = NEED_NARROW_CUTS / len(union) if union else 99
    ud = NEED_NARROW_DIST / len(union) if union else 99
    print("  %-44s %6d" % ("NARROW UNION", len(union)))
    print("  narrow utilisation 160 cuts = %.4f  %s   (131 distinct = %.4f %s)"
          % (u, col(u), ud, col(ud)))
    out[cand] = {"buckets": rows, "union": len(union),
                 "narrow_util_160": round(u, 4), "narrow_util_131": round(ud, 4)}
json.dump(out, open("narrow.json", "w", encoding="utf-8"), indent=2)
