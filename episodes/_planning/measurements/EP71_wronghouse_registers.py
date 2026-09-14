# EP71 / PD-2026-071-wronghouse -- Martin v. United States -- register inventory.
#
# Method is EP68_pinto_register_inventory.v001.md, as reproduced in
# EP70_45min_candidates.v001.md section 10.  Nothing here is new method:
#   * the pool is built by EP70_45min_pool.py -- REUSED, NOT FORKED.  If pool.json
#     is not already in the current working directory this script runs that file
#     with runpy so the pool is byte-for-byte the EP70 pool (26,101 distinct
#     playable video).
#   * a register is a word-boundary re.I search over the PROVIDER TITLE, exactly
#     as EP70_45min_registers.py / EP70_45min_registers_narrow.py do.  No semantic
#     matcher, no embedding, no filename fallback beyond the pool builder's own.
#
# The split is config/pd_planning_os.v002.json -> producibility_gate.period_rule:
#   ERA-NEUTRAL registers are scored against the whole playable pool.
#   ERA-BOUND registers are scored against ARCHIVAL SOURCES ONLY.
# This episode is contemporary (2017-2026 USA) except one act set in April 1973
# (Collinsville, Illinois), so the era-bound half is measured twice for the
# contemporary registers -- whole pool AND archival-only -- and once, archival
# only, for the 1973 registers.
#
# Run:  cd <any working dir> && py -3.11 <this file>
# Writes: EP71_WRONGHOUSE_REGISTER_INVENTORY.v001.json beside this script.
# Read-only against the shelf.  No render, build, GPU, upload or API call.

import json, os, re, runpy, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
POOL_BUILDER = os.path.join(HERE, "EP70_45min_pool.py")
OUT = os.path.join(HERE, "EP71_WRONGHOUSE_REGISTER_INVENTORY.v001.json")

# ---------------------------------------------------------------- pool (reused)
if not os.path.exists("pool.json"):
    print("pool.json not in cwd -- running EP70_45min_pool.py (reuse, not fork)")
    runpy.run_path(POOL_BUILDER, run_name="__main__")
pool = json.load(open("pool.json", encoding="utf-8"))

ARCH = {"ia", "nara", "loc", "nypl", "smithsonian", "met", "wikimedia"}
items = [(v["t"] or "", (v["src"] or "").lower()) for v in pool.values()]
arch_idx = {i for i, (t, s) in enumerate(items) if s in ARCH}

YEAR = re.compile(r"\b(19[0-9]{2}|20[0-9]{2})\b")
DECADE = re.compile(r"\b(1950s|1960s|1970s|1980s|fifties|sixties|seventies|eighties)\b", re.I)


def era_marked(t):
    """title names a year 1955-1985, or a 1950s-1980s decade word."""
    for m in YEAR.findall(t):
        if 1955 <= int(m) <= 1985:
            return True
    return bool(DECADE.search(t))


ERA_IDX = {i for i, (t, s) in enumerate(items) if era_marked(t)}


def hits(rx):
    p = re.compile(rx, re.I)
    s = set()
    for i, (t, _s) in enumerate(items):
        if p.search(t):
            s.add(i)
    return s


# ------------------------------------------------------------------- registers
# ERA-NEUTRAL: scored against the whole playable pool (period_rule).
NEUTRAL = {
 "N01_hands_writing_signing": r"\b(hand|hands|finger|fingers|fingertip\w*|palm|palms|wrist|writing|handwriting|handwritten|pen|pens|pencil|pencils|notebook|signature|signatures|signing|paperwork|typing|scribbl\w*)\b",
 "N02_documents_paper_files": r"\b(document\w*|paper|papers|page|pages|file|files|filing|folder|folders|form|forms|report|reports|record|records|letter|letters|envelope|envelopes|stamp\w*|contract|contracts|dossier|print|printing|printer|clipboard)\b",
 "N03_door_lock_key_handle": r"\b(door|doors|doorway|doorstep|doorknob|door handle|threshold|lock|locks|locked|padlock|key|keys|keyhole|handle|handles|hinge|hinges|latch|deadbolt|knob|bolt)\b",
 "N04_mail_envelope_letter": r"\b(mail|mailbox|mail box|letterbox|letter box|mailman|postman|postal|post office|envelope|envelopes|letter|letters|postcard|parcel|package|packages|delivery|courier|postmark)\b",
 "N05_clock_watch_countdown": r"\b(clock|clocks|clockwork|wristwatch|watches|stopwatch|timer|timers|countdown|hourglass|sundial|alarm clock|minute hand|second hand|pendulum|time lapse|timelapse)\b",
 "N06_dawn_sunrise_first_light": r"\b(dawn|daybreak|sunrise|sunup|first light|early morning|morning light|predawn|pre-dawn|twilight|dusk|sunset|golden hour|horizon|skyline at dawn)\b",
 "N07_empty_room_hallway_stairs": r"\b(empty room|hallway|hallways|corridor|corridors|staircase|stairs|stairway|stairwell|bedroom|bedrooms|closet|wardrobe|interior|interiors|room|rooms|apartment|living room|attic|basement|hall)\b",
 "N08_rain_storm_cloud_sky_fog": r"\b(rain|raining|rainy|raindrop\w*|storm|storms|stormy|thunder|thunderstorm|lightning|cloud|clouds|cloudy|overcast|sky|skies|fog|foggy|mist|misty|drizzle|downpour|puddle|puddles)\b",
 "N09_cabinet_archive_boxes_shelves": r"\b(filing cabinet|file cabinet|archive|archives|archival|box|boxes|carton|cartons|crate|crates|shelf|shelves|shelving|bookshelf|bookcase|library|stacks|storage|warehouse|ledger|binder|binders|catalogue|catalog)\b",
 "N10_texture_dust_blinds_glass_shadow": r"\b(dust|dusty|particle|particles|light beam|sunbeam|sunlight|blind|blinds|venetian|window|windows|windowpane|glass|reflection|reflections|reflecting|shadow|shadows|silhouette|silhouettes|texture|textures|abstract|bokeh|smoke|haze)\b",
 "N11_map_gps_route_dashboard": r"\b(map|maps|mapping|navigation|navigating|navigator|gps|satellite|satellites|route|routes|compass|coordinates|dashboard|windshield|windscreen|street sign|address|addresses|aerial|drone)\b",
 "N12_keyboard_screen_data_server": r"\b(keyboard|keyboards|screen|screens|monitor|monitors|computer|computers|laptop|laptops|data|database|databases|server|servers|data center|data centre|code|coding|software|network|networks|digital|terminal)\b",
}

# ERA-BOUND, CONTEMPORARY USA 2017-2026.  Measured BOTH ways (see report).
CONTEMP = {
 "C01_front_door_suburban_house": r"\b(front door|porch|driveway|doorstep|suburb|suburbs|suburban|suburbia|subdivision|neighborhood|neighbourhood|residential|house|houses|home|homes|bungalow|yard|front lawn|lawn|garage|garden fence|picket fence|mailbox)\b",
 "C02_swat_tactical_raid_breach": r"\b(swat|tactical|body armor|body armour|bulletproof|kevlar|helmet|helmets|raid|raids|raided|breach|breaching|battering ram|riot|riot police|special forces|assault rifle|rifle|rifles|shield|shields|commando|task force|fbi|federal agent|federal agents)\b",
 "C03_police_car_patrol_lights": r"\b(police car|police cars|patrol car|squad car|cruiser|police vehicle|patrol|siren|sirens|emergency light|emergency lights|blue light|blue lights|flashing light|flashing lights|law enforcement|sheriff|police|policeman|officer|officers|cop|cops|badge|precinct)\b",
 "C04_courthouse_courtroom_judge": r"\b(court|courts|courtroom|courthouse|judge|judges|jury|juror|jurors|trial|trials|hearing|hearings|verdict|testimony|witness stand|bench|attorney|attorneys|lawyer|lawyers|counsel|litigation|appeal|appeals|deposition)\b",
 "C05_supreme_court_dc_capitol": r"\b(supreme court|washington|capitol|congress|congressional|senate|house of representatives|federal building|government building|white house|monument|monuments|memorial|marble|colonnade|column|columns|dome|rotunda|flag|flags)\b",
 "C06_atlanta_suburb_aerial_street": r"\b(atlanta|georgia|american suburb|suburb|suburbs|suburban|suburbia|subdivision|neighborhood|neighbourhood|residential street|neighborhood street|street scene|cul-de-sac|aerial|drone|rooftop|rooftops|housing development|housing estate)\b",
 "C07_school_classroom_corridor": r"\b(school|schools|schoolyard|schoolroom|classroom|classrooms|kindergarten|elementary|high school|pupil|pupils|student|students|teacher|teachers|locker|lockers|playground|campus|gymnasium|blackboard|whiteboard|schoolbus|school bus)\b",
 "C08_counselling_clinic_waiting_room": r"\b(counseling|counselling|counselor|counsellor|therapy|therapist|psychiatr\w*|psycholog\w*|waiting room|clinic|clinics|clinical|consultation|patient|patients|doctor|doctors|physician|nurse|nurses|mental health|hospital|appointment)\b",
 "C09_lawyer_office_briefcase_books": r"\b(lawyer|lawyers|attorney|attorneys|legal|law firm|law office|law book|law books|briefcase|briefcases|paralegal|notary|conference room|boardroom|board room|office|offices|desk|desks|handshake|meeting|meetings)\b",
 "C10_flashlight_night_silhouette": r"\b(flashlight|flash light|torch|torchlight|night vision|infrared|thermal|searchlight|spotlight|light beam|beam of light|dark|darkness|night|nighttime|night-time|silhouette|silhouettes|headlight|headlights|lantern|shadowy)\b",
}

# ERA-BOUND, PAST -- April 1973, Collinsville Illinois.  ARCHIVAL SOURCES ONLY.
PAST = {
 "P01_1970s_street_interior_car_town": r"\b(1970s|1970|1971|1972|1973|1974|1975|1976|1977|1978|1979|seventies|super 8|super-8|8mm|16mm|newsreel|home movie|home movies|vintage|retro|period film)\b",
 "P02_1970s_senate_hearing_govt_office": r"\b(senate|senator|senators|congress|congressional|subcommittee|committee|hearing|hearings|testimony|capitol hill|government office|federal office|legislature|legislative|statehouse|state house)\b",
}

# The NARROW CORE: 40% of the film (160 cuts / 131 distinct) whose frame must read
# as a SPECIFIC THING, not as an abstraction.
# In: C01 C02 C03 C04 C05 C06 C10 -- a wrong front door, a stack, a patrol light,
#     a courtroom, the Supreme Court, an Atlanta street, a torch in a dark hallway.
#     None of these can be substituted by an era-neutral abstraction.
# Out: N01-N12 (abstractions by definition); C07 C08 C09 (a school, a clinic
#     waiting room and a law office read correctly from ANY contemporary stock --
#     the frame does not have to be the specific building);
#     P01 P02 (different denominator -- archival only -- so they cannot be unioned
#     into a whole-pool narrow figure; reported separately).
NARROW_KEYS = ["C01_front_door_suburban_house", "C02_swat_tactical_raid_breach",
               "C03_police_car_patrol_lights", "C04_courthouse_courtroom_judge",
               "C05_supreme_court_dc_capitol", "C06_atlanta_suburb_aerial_street",
               "C10_flashlight_night_silhouette"]

# The narrow core as written above still carries broad tokens ('dark', 'night',
# 'aerial', 'drone', 'house', 'home'), which INFLATE availability. The tight
# variant keeps only nouns that can name the thing itself. Both are reported;
# the tight one is the honest one.
NARROW_TIGHT = {
 "C01_tight_front_door_suburban": r"\b(front door|doorstep|porch|driveway|suburban|suburbia|subdivision|residential|front lawn|picket fence|mailbox)\b",
 "C02_tight_swat_raid_breach": r"\b(swat|tactical|body armor|body armour|kevlar|bulletproof|battering ram|breaching|riot police|special forces|raid|raided)\b",
 "C03_tight_police_vehicle_lights": r"\b(police car|police cars|patrol car|squad car|cruiser|police vehicle|siren|sirens|emergency lights|blue lights|flashing lights|law enforcement|sheriff|police)\b",
 "C04_tight_courtroom_courthouse": r"\b(courtroom|courthouse|supreme court|judge|judges|jury|jurors|gavel|witness stand)\b",
 "C05_tight_capitol_supreme_court": r"\b(supreme court|capitol|congress|senate|white house|washington|federal building|government building|rotunda)\b",
 "C06_tight_atlanta_suburb_street": r"\b(atlanta|georgia|suburban|suburbia|subdivision|residential street|neighborhood street|cul-de-sac|housing development)\b",
 "C10_tight_flashlight_nightvision": r"\b(flashlight|torchlight|night vision|infrared|searchlight|spotlight|silhouette|silhouettes|headlights)\b",
}

# EP70_45min_candidates.v001.md section 10 published narrow union 366 / util 0.437
# for this same premise (candidate 1, "wrong house"). Reproduced verbatim here so
# the delta between the two narrow definitions is visible rather than smoothed.
EP70_NARROW_VERBATIM = {
 "residential front door / doorway": r"\b(front door|doorway|door|porch|driveway|mailbox)\b",
 "tactical police / raid / fbi": r"\b(swat|tactical|raid|police|officer|officers|law enforcement|fbi|federal agent|handcuff\w*)\b",
 "courtroom / supreme court interior": r"\b(courtroom|courthouse|supreme court|judge|jury|gavel|bench)\b",
}

# --------------------------------------------------------------------- sizing
RUNTIME_MIN = 45
NEED_CUTS = 400
DISTINCT_FRACTION = 0.818          # EP68 measured
NEED_DISTINCT = 327                # 400 * 0.818 = 327.2 -> 327, as EP70
NARROW_SHARE = 0.40
NEED_NARROW_CUTS = 160
NEED_NARROW_DIST = 131
ACT_1973_MIN = 5.0                 # the Collinsville act, of a 45-minute film
ACT_1973_CUTS = round(NEED_CUTS * ACT_1973_MIN / RUNTIME_MIN)      # 44
ACT_1973_DIST = round(ACT_1973_CUTS * DISTINCT_FRACTION)           # 36

GREEN, AMBER = 0.15, 0.40          # producibility_gate.thresholds


def col(u):
    return "GREEN" if u <= GREEN else ("AMBER" if u <= AMBER else "RED")


def util(need, avail):
    return round(need / avail, 4) if avail else None


def block(name, regs, label):
    print("=" * 100)
    print(label)
    rows, uni, uni_arch, uni_era = {}, set(), set(), set()
    for k, rx in regs.items():
        s = hits(rx)
        a = s & arch_idx
        e = s & ERA_IDX
        rows[k] = {"regex": rx, "total": len(s), "archival": len(a),
                   "modern": len(s) - len(a), "title_year_1955_1985": len(e)}
        uni |= s
        uni_arch |= a
        uni_era |= e
        print("  %-42s %7d  arch %5d  era-titled %4d" % (k, len(s), len(a), len(e)))
    print("  %-42s %7d  arch %5d  era-titled %4d" % ("UNION (distinct)", len(uni),
                                                     len(uni_arch), len(uni_era)))
    return rows, uni, uni_arch, uni_era


def main():
    print("pool =", len(items), "distinct playable video  | archival-source rows =",
          len(arch_idx), "| title-year 1955-1985 =", len(ERA_IDX))

    n_rows, n_uni, n_arch, n_era = block("neutral", NEUTRAL,
        "ERA-NEUTRAL (N01-N12) -- scored against the WHOLE playable pool")
    c_rows, c_uni, c_arch, c_era = block("contemp", CONTEMP,
        "ERA-BOUND CONTEMPORARY (C01-C10) -- scored BOTH ways")
    p_rows, p_uni, p_arch, p_era = block("past", PAST,
        "ERA-BOUND PAST 1973 (P01-P02) -- ARCHIVAL SOURCES ONLY governs")

    # narrow core
    narrow = set()
    for k in NARROW_KEYS:
        narrow |= hits(CONTEMP[k])
    narrow_arch = narrow & arch_idx

    tight_rows, tight = {}, set()
    for k, rx in NARROW_TIGHT.items():
        s = hits(rx)
        tight_rows[k] = {"regex": rx, "total": len(s), "archival": len(s & arch_idx)}
        tight |= s
    print("  -- narrow core, TIGHT variant --")
    for k, v in tight_rows.items():
        print("  %-42s %7d  arch %5d" % (k, v["total"], v["archival"]))
    print("  %-42s %7d" % ("TIGHT UNION", len(tight)))

    ep70_rows, ep70 = {}, set()
    for k, rx in EP70_NARROW_VERBATIM.items():
        s = hits(rx)
        ep70_rows[k] = {"regex": rx, "total": len(s), "archival": len(s & arch_idx)}
        ep70 |= s
    print("  EP70 narrow verbatim union %d  util160 %.4f %s  (published: 366 / 0.437 RED)"
          % (len(ep70), 160 / len(ep70), col(160 / len(ep70))))

    # the one register combination that could actually dress Collinsville 1973:
    # archival AND period-marked AND on a 1970s-subject register.
    p1 = hits(PAST["P01_1970s_street_interior_car_town"])
    p2 = hits(PAST["P02_1970s_senate_hearing_govt_office"])
    p1_arch_era = p1 & arch_idx & ERA_IDX
    p2_arch_era = p2 & arch_idx & ERA_IDX
    p_arch_era = (p1 | p2) & arch_idx & ERA_IDX
    period_titles = sorted(items[i][0] for i in (arch_idx & ERA_IDX))
    p_arch_titles = sorted(items[i][0] for i in ((p1 | p2) & arch_idx))
    p_arch_era_titles = sorted(items[i][0] for i in p_arch_era)
    p2_arch_titles = sorted(items[i][0] for i in (p2 & arch_idx))

    # EP68 section 5 contract: F + 2M >= cuts, at 206 s per i2v conversion.
    # F = footage actually usable for the act; by hand review of p_arch_era_titles
    # only texture-grade 1970s American material exists (see JSON), so F is taken
    # at the optimistic 3 and the pessimistic 0.
    def budget(F, cuts=ACT_1973_CUTS):
        M = max(0, -(-(cuts - F) // 2))
        return {"footage_cuts": F, "i2v_conversions": M,
                "gpu_hours": round(M * 206 / 3600, 2),
                "ai_motion_share_of_45min_film": round((2 * M) / NEED_CUTS, 3)}

    out = {
      "episode": "PD-2026-071-wronghouse",
      "title": "Martin v. United States -- the FBI raided the wrong house",
      "measured": "2026-08-12",
      "read_only": True,
      "method": ("EP68_pinto_register_inventory.v001.md method as reproduced in "
                 "EP70_45min_candidates.v001.md section 10. Pool built by "
                 "EP70_45min_pool.py (reused, not forked). Register = word-boundary "
                 "re.I search over the provider title."),
      "period_rule": ("config/pd_planning_os.v002.json -> producibility_gate.period_rule: "
                      "era-neutral registers scored against the whole pool, era-bound "
                      "registers scored against ARCHIVAL SOURCES ONLY."),
      "thresholds": {"green": GREEN, "amber": AMBER, "red_above": AMBER},
      "pool": {
        "distinct_playable_video": len(items),
        "reproduced_EP70_26101": len(items) == 26101,
        "archival_source_rows": len(arch_idx),
        "modern_rows": len(items) - len(arch_idx),
        "title_year_1955_1985_or_decade_word": len(ERA_IDX),
        "archival_and_period_titled": len(arch_idx & ERA_IDX),
      },
      "sizing": {
        "runtime_min": RUNTIME_MIN, "cuts": NEED_CUTS,
        "distinct_fraction": DISTINCT_FRACTION, "distinct_assets": NEED_DISTINCT,
        "narrow_share": NARROW_SHARE, "narrow_cuts": NEED_NARROW_CUTS,
        "narrow_distinct": NEED_NARROW_DIST,
        "act_1973_min": ACT_1973_MIN, "act_1973_cuts": ACT_1973_CUTS,
        "act_1973_distinct": ACT_1973_DIST,
      },
      "groups": {
        "era_neutral": {
          "governs": "whole pool",
          "registers": n_rows,
          "union": len(n_uni), "union_archival": len(n_arch),
          "util_400": util(NEED_CUTS, len(n_uni)), "util_327": util(NEED_DISTINCT, len(n_uni)),
          "colour_400": col(util(NEED_CUTS, len(n_uni))),
          "colour_327": col(util(NEED_DISTINCT, len(n_uni))),
        },
        "era_bound_contemporary": {
          "governs": ("whole pool -- the shelf is 93.5% contemporary stock, so for a "
                      "2017-2026 premise the contemporary stock IS the era-correct "
                      "supply; the archival-only reading is reported for completeness "
                      "and is NOT the binding one."),
          "registers": c_rows,
          "union": len(c_uni), "union_archival": len(c_arch),
          "util_400_wholepool": util(NEED_CUTS, len(c_uni)),
          "util_327_wholepool": util(NEED_DISTINCT, len(c_uni)),
          "colour_400_wholepool": col(util(NEED_CUTS, len(c_uni))),
          "colour_327_wholepool": col(util(NEED_DISTINCT, len(c_uni))),
          "util_400_archivalonly": util(NEED_CUTS, len(c_arch)),
          "util_327_archivalonly": util(NEED_DISTINCT, len(c_arch)),
          "colour_400_archivalonly": col(util(NEED_CUTS, len(c_arch))),
          "colour_327_archivalonly": col(util(NEED_DISTINCT, len(c_arch))),
        },
        "era_bound_past_1973": {
          "governs": "archival sources only (period_rule)",
          "registers": p_rows,
          "union": len(p_uni), "union_archival": len(p_arch),
          "union_archival_and_period_titled": len(p_arch_era),
          "P01_archival_and_period_titled": len(p1_arch_era),
          "P02_archival_and_period_titled": len(p2_arch_era),
          "util_act_44cuts_archivalonly": util(ACT_1973_CUTS, len(p_arch)),
          "util_act_36distinct_archivalonly": util(ACT_1973_DIST, len(p_arch)),
          "colour_act_44_archivalonly": col(util(ACT_1973_CUTS, len(p_arch))) if p_arch else "RED",
          "util_act_44_archival_period_titled": util(ACT_1973_CUTS, len(p_arch_era)),
          "util_act_36_archival_period_titled": util(ACT_1973_DIST, len(p_arch_era)),
          "colour_act_44_archival_period_titled": col(util(ACT_1973_CUTS, len(p_arch_era))) if p_arch_era else "RED",
          "util_400_archivalonly": util(NEED_CUTS, len(p_arch)),
          "P01_archival_titles": p_arch_titles,
          "P01_P02_archival_AND_period_titled_titles": p_arch_era_titles,
          "P02_archival_titles": p2_arch_titles,
          "whole_shelf_archival_period_titled_titles": period_titles,
          "act_budget_EP68_contract_F_plus_2M_ge_cuts": {
            "optimistic_F3": budget(3), "pessimistic_F0": budget(0),
            "seconds_per_i2v": 206,
          },
        },
      },
      "narrow_core": {
        "definition": ("40% of the film -- the registers whose frame must read as a "
                       "specific thing rather than an abstraction."),
        "in": NARROW_KEYS,
        "out_and_why": {
          "N01-N12": "abstractions by definition; they are the wide half",
          "C07_school_classroom_corridor": "any contemporary school reads as the school",
          "C08_counselling_clinic_waiting_room": "any waiting room reads as the waiting room",
          "C09_lawyer_office_briefcase_books": "any law office reads as the law office",
          "P01/P02": "archival-only denominator; cannot be unioned with a whole-pool figure",
        },
        "union": len(narrow), "union_archival": len(narrow_arch),
        "util_160": util(NEED_NARROW_CUTS, len(narrow)),
        "util_131": util(NEED_NARROW_DIST, len(narrow)),
        "colour_160": col(util(NEED_NARROW_CUTS, len(narrow))),
        "colour_131": col(util(NEED_NARROW_DIST, len(narrow))),
        "util_160_archivalonly": util(NEED_NARROW_CUTS, len(narrow_arch)),
        "colour_160_archivalonly": col(util(NEED_NARROW_CUTS, len(narrow_arch))),
        "tight": {
          "why": ("the broad-token narrow core above is inflated by 'dark', 'night', "
                  "'aerial', 'drone', 'house', 'home'; this variant keeps only nouns "
                  "that name the thing itself. This is the honest narrow figure."),
          "registers": tight_rows,
          "union": len(tight),
          "util_160": util(NEED_NARROW_CUTS, len(tight)),
          "util_131": util(NEED_NARROW_DIST, len(tight)),
          "colour_160": col(util(NEED_NARROW_CUTS, len(tight))),
          "colour_131": col(util(NEED_NARROW_DIST, len(tight))),
        },
        "ep70_verbatim_reproduction": {
          "why": ("EP70_45min_candidates.v001.md section 10 published narrow union 366 "
                  "and util 0.437 RED for this same premise. Reproduced here to prove "
                  "the pool and matcher are identical."),
          "registers": ep70_rows, "union": len(ep70),
          "util_160": util(NEED_NARROW_CUTS, len(ep70)),
          "util_131": util(NEED_NARROW_DIST, len(ep70)),
          "colour_160": col(util(NEED_NARROW_CUTS, len(ep70))),
          "published_union": 366, "published_util_160": 0.437,
          "reproduced": len(ep70) == 366,
        },
      },
      "what_the_number_cannot_see": [
        "THE SHELF HAS NO ERA FIELD. No year, no created-date, no archival flag on any "
        "ledger row (period_rule.finding). Era is proxied only by source class and by a "
        "year appearing inside a provider title.",
        "A TITLE MATCH IS NOT A SUPPLY COUNT. It says the word is in the title; it does "
        "not say the clip is usable, in date, in the right country, above 720p, or that "
        "a human would accept the frame. EP68 measured a 1.3% hand-accept rate against a "
        "green noun number.",
        "64% of the 1,058-clip archival pool is below 720p (EP68 section 2).",
        "Registers overlap; the union is distinct, but a clip counted in two registers "
        "can only be spent once. Union availability therefore overstates supply.",
        "Broad tokens carry noise: 'key' also matches 'key west', 'watch' is a verb, "
        "'hall' matches concert halls, 'dark' matches dark chocolate. Noise inflates the "
        "denominator, i.e. it makes utilisation look BETTER than it is.",
        "C06 deliberately excludes the bare token 'street' (it would add thousands of "
        "non-American streets); C03 keeps the broad token 'police'.",
        "No disk re-verification is done here beyond the pool builder's absent_index.json.",
      ],
    }

    print("=" * 100)
    print("NARROW CORE union %d  -> 160 cuts %.4f %s | 131 distinct %.4f %s"
          % (len(narrow), out["narrow_core"]["util_160"], out["narrow_core"]["colour_160"],
             out["narrow_core"]["util_131"], out["narrow_core"]["colour_131"]))
    g = out["groups"]
    print("ERA-NEUTRAL union %d -> 400 %.4f %s | 327 %.4f %s"
          % (len(n_uni), g["era_neutral"]["util_400"], g["era_neutral"]["colour_400"],
             g["era_neutral"]["util_327"], g["era_neutral"]["colour_327"]))
    print("CONTEMPORARY union %d -> 400 %.4f %s (whole pool) | archival-only %d -> %.4f %s"
          % (len(c_uni), g["era_bound_contemporary"]["util_400_wholepool"],
             g["era_bound_contemporary"]["colour_400_wholepool"], len(c_arch),
             g["era_bound_contemporary"]["util_400_archivalonly"],
             g["era_bound_contemporary"]["colour_400_archivalonly"]))
    print("PAST 1973 archival-only %d (period-titled %d) -> act %d cuts %s"
          % (len(p_arch), len(p_arch_era), ACT_1973_CUTS,
             out["groups"]["era_bound_past_1973"]["colour_act_44_archivalonly"]))

    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
