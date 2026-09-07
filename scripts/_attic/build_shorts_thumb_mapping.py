#!/usr/bin/env python3
"""Build runs/shorts_thumbs/mapping.v001.json + per-short props JSON for ShortThumbYT.

Maps each published Short (channel_uploads.v001.json) to its SHORTxx source data by title/topic,
and derives a CTR headline/subhead/badge + a concrete hero still. No uploads. Read-only side of the repo.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UP = ROOT / "runs" / "shorts_thumbs" / "channel_uploads.v001.json"
PUBLIC = ROOT / "remotion" / "public"
OUT_DIR = ROOT / "runs" / "shorts_thumbs"
PROPS_DIR = OUT_DIR / "props"

GOLD = "#E5B53A"

# video_id -> shortId (from title/topic correlation). Verified 1:1 against source data files.
VID_TO_SHORT = {
    "dedDocuyCUM": "short06",  # Police Can Stop & Frisk You (Terry v. Ohio)
    "L8iKnBSVXKg": "short07",  # Police Need a Warrant to Search Your Phone (Riley)
    "m33s6uFmXao": "short08",  # Tracked His Phone for 127 Days (Carpenter)
    "mrPV1Tv_6gE": "short09",  # Take Your Property Without a Conviction (Timbs)
    "6rUWUk3x9Xs": "short10",  # Take Your Home for a Private Company (Kelo)
    "sxk0gbFBnMU": "short11",  # School Punish You for a Post at Home (Mahanoy)
    "bFGZ_6BTI9I": "short12",  # Sign Away Your Right to Sue (Arbitration)
    "Lux3a25vBSw": "short13",  # Arrested? Police Take Your DNA (Maryland v. King)
    "2XWqZWx916c": "short14",  # Chase You Into Your Own Home (Lange)
    "Ri1hlCBOjhc": "short27",  # Traffic Stop Was Already Over (Rodriguez)
    "2Smc35dUF5c": "short15",  # Bold Promise Become a Crime (Theranos)
    "iDtER8rxPR0": "short23",  # Website He Took From Didn't Want Him Charged (Swartz)
    "8YxBH6zKals": "short28",  # Son Sold $40 of Drugs -> take parents' house (Civil forfeiture)
    "KEDs-D_hhn0": "short29",  # 30 Years on Death Row / bullet matched nothing (Hinton)
    "XrOiibG62wc": "short30",  # Certain He Attacked Her, DNA proved wrong man (Cotton)
    "k26eTD3alnA": "short31",  # Force Your Thumb to Unlock a Phone (Unlock)
    "NMqzv7KcHdM": "short32",  # Search Your Car Without a Warrant (Auto exception)
    "_TcVNCh2PlA": "short16",  # Counted Down 4 Days. Already Gone. (Titan sub)
    "TxGQKxxzjfs": "short17",  # Crypto That Never Existed (OneCoin)
    "gR6IpnynBzM": "short33",  # County Took Her Home over $15,000 debt (Tyler v. Hennepin)
    "smfqeisWRUo": "short34",  # Fly With Cash, airport takes it (Rolin)
    "3rW-jeKH8Z0": "short35",  # Cash Restaurant, IRS emptied account (Hinders structuring)
    "NLvlce3XCaw": "short18",  # $1 Trillion Vanished in 36 Minutes (Flash Crash)
    "ypDjfK9o5Bg": "short01",  # Why Do Police Read You Your Rights (Miranda)
    "uL9q1GM_1Vw": "short02",  # A Pencil Letter Changed Everything (Gideon)
    "PF4ZJjy_KCs": "short03",  # Police Searched Illegally (Mapp)
    "AMZXUw3Arn0": "short04",  # $8 Billion Vanished From a Crypto Exchange (FTX)
    "54Vo5kJj6tk": "short36",  # Search Your Entire Phone - Legally? (Riley remake)
    "ACS2lVlX_mQ": "short37",  # Broke In With a Warrant That Didn't Exist (Mapp remake)
    "O0mK6cK1iTs": "short05",  # Steady Returns / almost zero real trades (Madoff)
    "jD5nQ2ARL-M": "short19",  # Wealthy Parents Sneak Kids Into Colleges (Varsity Blues)
    "vLs3VaidXkI": "short20",  # Biggest Art Heist Still Unsolved (Gardner)
    "rV-56tT8cMg": "short21",  # Jumped From a Plane With $200,000 (D.B. Cooper)
    "PpiUNN5QWQQ": "short22",  # 98 Counts, Pleaded Guilty to 6 (Milken)
    "9iHmgihSWYk": "short24",  # FBI Caught a Billionaire Trader / wiretaps (Rajaratnam)
    "Huujtv3_iEA": "short25",  # Never Set Foot on the Property / "search" (Kyllo)
    "fN49trupNgc": "short26",  # Record Him Without Touching the Phone Booth (Katz)
}

# shortId -> {topic, headline, subhead(case label), badge, accent, focusY}
DESIGN = {
    "short01": ("Miranda rights (Miranda v. Arizona)", "READ YOUR\nRIGHTS", "MIRANDA v. ARIZONA - 1966", "5-4", GOLD, 24),
    "short02": ("Right to a lawyer (Gideon v. Wainwright)", "A PENCIL\nLETTER", "GIDEON v. WAINWRIGHT - 1963", "9-0", GOLD, 24),
    "short03": ("Exclusionary rule (Mapp v. Ohio)", "ILLEGAL\nSEARCH", "MAPP v. OHIO - 1961", "6-3", GOLD, 26),
    "short04": ("FTX crypto collapse", "$8 BILLION\nGONE", "THE FTX COLLAPSE", "GUILTY", GOLD, 30),
    "short05": ("Madoff Ponzi scheme", "ZERO REAL\nTRADES", "THE MADOFF PONZI", "150 YEARS", GOLD, 28),
    "short06": ("Stop & frisk (Terry v. Ohio)", "STOPPED &\nFRISKED", "TERRY v. OHIO - 1968", "8-1", GOLD, 26),
    "short07": ("Phone search warrant (Riley v. California)", "SEARCH YOUR\nPHONE?", "RILEY v. CALIFORNIA - 2014", "9-0", GOLD, 26),
    "short08": ("Cell-site tracking (Carpenter v. U.S.)", "127 DAYS\nTRACKED", "CARPENTER v. U.S. - 2018", "5-4", GOLD, 26),
    "short09": ("Excessive fines / forfeiture (Timbs v. Indiana)", "TAKEN - NO\nCONVICTION", "TIMBS v. INDIANA - 2019", "9-0", GOLD, 26),
    "short10": ("Eminent domain (Kelo v. New London)", "THEY TOOK\nHER HOME", "KELO v. NEW LONDON - 2005", "5-4", GOLD, 26),
    "short11": ("Student off-campus speech (Mahanoy v. B.L.)", "PUNISHED\nFOR A POST", "MAHANOY v. B.L. - 2021", "8-1", GOLD, 26),
    "short12": ("Forced arbitration clauses", "YOU CAN'T\nSUE", "FORCED ARBITRATION", "5-4", GOLD, 26),
    "short13": ("DNA at booking (Maryland v. King)", "DNA TAKEN\nAT BOOKING", "MARYLAND v. KING - 2013", "5-4", GOLD, 26),
    "short14": ("Hot pursuit into home (Lange v. California)", "CHASED\nINTO HOME", "LANGE v. CALIFORNIA - 2021", "9-0", GOLD, 26),
    "short15": ("Theranos blood-test fraud", "PROMISE\nOR CRIME?", "THE THERANOS FRAUD", "GUILTY", GOLD, 26),
    "short16": ("Titan submersible implosion", "4 DAYS.\nNO SOUND.", "THE TITAN SUB - 2023", "IMPLOSION", GOLD, 30),
    "short17": ("OneCoin crypto scam", "A COIN THAT\nNEVER EXISTED", "THE ONECOIN SCAM", "4B EUROS", GOLD, 28),
    "short18": ("2010 Flash Crash", "$1 TRILLION\nGONE", "THE 2010 FLASH CRASH", "36 MIN", GOLD, 30),
    "short19": ("Operation Varsity Blues", "BUYING\nADMISSION", "OPERATION VARSITY BLUES", "50 CHARGED", GOLD, 28),
    "short20": ("Gardner Museum art heist", "STILL\nUNSOLVED", "THE GARDNER HEIST - 1990", "$500M", GOLD, 24),
    "short21": ("D.B. Cooper hijacking", "HE\nVANISHED", "THE D.B. COOPER CASE - 1971", "UNSOLVED", GOLD, 26),
    "short22": ("Michael Milken junk bonds", "98 COUNTS,\nPLEADED TO 6", "THE MILKEN CASE", "JUNK BONDS", GOLD, 28),
    "short23": ("Aaron Swartz / JSTOR case", "CHARGED\nANYWAY", "THE AARON SWARTZ CASE", "35 YEARS?", GOLD, 28),
    "short24": ("Raj Rajaratnam insider trading", "WIRETAPS ON\nWALL STREET", "THE RAJARATNAM CASE", "GUILTY x14", GOLD, 28),
    "short25": ("Thermal imaging (Kyllo v. U.S.)", "NEVER\nENTERED", "KYLLO v. U.S. - 2001", "5-4", GOLD, 26),
    "short26": ("Wiretap privacy (Katz v. U.S.)", "RECORDED\nIN A BOOTH", "KATZ v. U.S. - 1967", "7-1", GOLD, 26),
    "short27": ("Prolonged traffic stop (Rodriguez v. U.S.)", "THE STOP\nWAS OVER", "RODRIGUEZ v. U.S. - 2015", "6-3", GOLD, 26),
    "short28": ("Civil asset forfeiture ($40 sale)", "A $40\nSALE", "CIVIL FORFEITURE", "SEIZED", GOLD, 28),
    "short29": ("Anthony Ray Hinton wrongful conviction", "30 YEARS\nINNOCENT", "THE ANTHONY HINTON CASE", "9-0", GOLD, 26),
    "short30": ("Ronald Cotton misidentification", "SO SURE.\nSO WRONG.", "THE RONALD COTTON CASE", "DNA CLEARED", GOLD, 26),
    "short31": ("Compelled phone unlock (thumb vs passcode)", "UNLOCK\nIT", "THUMB vs PASSCODE", "2024", GOLD, 26),
    "short32": ("Automobile exception (car searches)", "SEARCH\nYOUR CAR", "THE AUTOMOBILE EXCEPTION", "SINCE 1925", GOLD, 26),
    "short33": ("Home-equity theft (Tyler v. Hennepin)", "THEY KEPT\nIT ALL", "TYLER v. HENNEPIN - 2023", "9-0", GOLD, 26),
    "short34": ("Airport cash seizure (Rolin)", "TAKEN AT\nTHE GATE", "AIRPORT CASH SEIZURE", "NO CRIME", GOLD, 28),
    "short35": ("IRS structuring (Hinders)", "ACCOUNT\nEMPTIED", "THE IRS STRUCTURING CASE", "NO CRIME", GOLD, 28),
    "short36": ("Phone search warrant, remake (Riley)", "THEY SEARCHED\nYOUR PHONE", "RILEY v. CALIFORNIA - 2014", "9-0", GOLD, 26),
    "short37": ("Exclusionary rule, remake (Mapp)", "NO WARRANT.\nTHEY BROKE IN.", "MAPP v. OHIO - 1961", "6-3", GOLD, 26),
}


def hero_for(short_id: str) -> str:
    """Prefer the hook still (_01); fall back to the prepped _thumb.png."""
    cand = f"shorts/{short_id}/{short_id}_01.png"
    if (PUBLIC / cand).exists():
        return cand
    return f"shorts/{short_id}/{short_id}_thumb.png"


def main():
    uploads = json.loads(UP.read_text(encoding="utf-8"))
    shorts = [u for u in uploads if u["is_short"]]
    # dedupe by video_id (uploads playlist returned some twice)
    seen = {}
    dups = []
    for s in shorts:
        vid = s["video_id"]
        if vid in seen:
            dups.append(vid)
            continue
        seen[vid] = s
    mapping = []
    PROPS_DIR.mkdir(parents=True, exist_ok=True)
    mapped = 0
    unmapped = []
    for vid, s in seen.items():
        sid = VID_TO_SHORT.get(vid)
        if sid is None:
            unmapped.append(s)
            mapping.append({
                "video_id": vid, "title": s["title"], "seconds": s["seconds"],
                "privacy": s["privacy"], "matched_short_data": None,
                "note": "Could not confidently correlate title to a SHORTxx source.",
            })
            continue
        mapped += 1
        topic, headline, subhead, badge, accent, focusy = DESIGN[sid]
        hero = hero_for(sid)
        entry = {
            "video_id": vid,
            "title": s["title"],
            "seconds": s["seconds"],
            "privacy": s["privacy"],
            "matched_short_data": sid,
            "hook_headline": headline.replace("\n", " / "),
            "subhead": subhead,
            "badge": badge,
            "best_image_source": f"remotion/public/{hero}",
            "topic": topic,
        }
        mapping.append(entry)
        # per-short props for ShortThumbYT
        props = {
            "headline": headline, "subhead": subhead, "heroImage": hero,
            "accent": accent, "badge": badge, "focusY": focusy,
        }
        (PROPS_DIR / f"{sid}.json").write_text(
            json.dumps(props, indent=2, ensure_ascii=False), encoding="utf-8")

    mapping.sort(key=lambda m: (m["matched_short_data"] or "zzz"))
    (OUT_DIR / "mapping.v001.json").write_text(
        json.dumps(mapping, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"unique shorts: {len(seen)}  (rows={len(shorts)}, duplicate playlist rows={len(dups)}: {dups})")
    print(f"mapped confidently: {mapped}/{len(seen)}")
    print(f"unmapped: {len(unmapped)}")
    print(f"props written: {len(list(PROPS_DIR.glob('*.json')))}")
    print(f"mapping -> {OUT_DIR / 'mapping.v001.json'}")


if __name__ == "__main__":
    main()
