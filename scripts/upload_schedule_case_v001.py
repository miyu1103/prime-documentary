#!/usr/bin/env python3
"""Upload a PD case episode privately and schedule its public release (private + publishAt).

Generic, config-driven version of upload_schedule_kyllo_v001.py (--ep katz|rodriguez).
Reuses the exact same resilient resumable uploader, thumbnail/caption set, hash guard, and
duplicate-refusal. Owner approved sequential scheduling 2026-07-04 ("順番ずつ予約投稿しよう":
EP25=7/10, EP26 Katz=7/11, EP27 Rodriguez=7/12, all 12:00 JST, private + publishAt).

Usage: python scripts/upload_schedule_case_v001.py --ep katz [--dry-run]
"""
from __future__ import annotations
import argparse, json, mimetypes, ssl, subprocess, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id, sha256_file, upload_chunks
# The ship DECISION lives here, in the scheduler, reading config/ship_policy.v001.json.
# check_final_acceptance.py is untouched: it still runs every check, computes every number and
# writes every failure into the receipt. What this import changes is which of those failures
# hold the door shut. An import failure is fatal on purpose -- no policy, no ship.
import pd_ship_policy as SHIP_POLICY

def _from_meta(epid: str, slug: str, sched_local: str, sched_utc: str) -> dict:
    """Build a CONFIG entry from that episode's own 09_package/youtube_meta.v001.json.

    Entries above carry the title, description and tags inline, which is a second copy of what the
    packaging file already says; nothing notices when the two drift, so an edited description can
    quietly fail to reach YouTube. Here the packaging file is the single source.

    A missing or malformed packaging file is recorded on the entry rather than raised, so one bad
    episode cannot stop an unrelated upload; main() refuses the moment that slug is selected.
    """
    p = ROOT / "episodes" / epid / "09_package" / "youtube_meta.v001.json"
    entry: dict = {
        "ep": epid,
        "video": (ROOT / "episodes" / epid / "08_edit" / f"{slug}_final_bgm.v001.mp4").as_posix(),
        "sched_local": sched_local, "sched_utc": sched_utc,
        "meta_source": p.as_posix(),
    }
    try:
        m = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return {**entry, "_error": f"cannot read {p.name}: {e}"}
    missing = [k for k in ("title", "description", "tags") if not m.get(k)]
    if missing:
        return {**entry, "_error": f"{p.name} has no {', '.join(missing)}"}
    return {**entry, "title": m["title"], "description": m["description"], "tags": m["tags"]}


CONFIG = {
    # EP62-65, one per day from 16 August. 12:00 JST is the long-form slot: it is filled through
    # the 15th, and the 16th-18th entries the schedule audit lists are shorts at 06/09/18/21 JST.
    # Title, description and tags come from each episode's packaging file, not from copies here.
    # 2026-08-16 19:xx JST: the 08-16 slot passed unfilled -- greene uploaded on 08-14 but the
    # run died before publishAt was set, and a past publishAt publishes immediately. The whole
    # run moves back one day. correa goes behind greene rather than keeping 08-17, because it
    # carries two real_person_likeness rejections in the shipped frames (C223 cut-0387 and
    # AR-5879298 cut-0098) and that class is blocking; greene is permit with zero blocking.
    "greene": {**_from_meta("PD-2026-062-greene", "greene",
                           "2026-08-17T12:00:00+09:00", "2026-08-17T03:00:00Z"),
               "video": (ROOT / "episodes" / "PD-2026-062-greene" / "08_edit"
                         / "greene_final_bgm.v002.mp4").as_posix()},
    # 2026-08-16 22:00 JST: greene was PUBLISHED IMMEDIATELY rather than held for 08-17, on the
    # owner's call -- the 08-16 slot was empty and "a day not shipped is gone" (ship_policy).
    # 22:00 JST is 09:00 ET, which is a better hour for this audience than the 12:00 JST slot
    # (23:00 ET the previous day) anyway. Everything below moves back to where it was before the
    # 08-16 miss, so the lost day is recovered rather than carried forward for a week.
    "correa": _from_meta("PD-2026-063-correa", "correa",
                         "2026-08-17T12:00:00+09:00", "2026-08-17T03:00:00Z"),
    # 2026-08-12: owner chose to ship v002 (v001 carries no 4-layer audio mux -- no
    # audio_mix_sha256 container tag). _from_meta hardcodes v001, so the master is overridden
    # here. This weakens nothing: the final_delivery sha guard below still binds the upload to
    # these exact bytes, and the acceptance receipt must name the same sha.
    "memphis": {**_from_meta("PD-2026-064-memphis", "memphis",
                             "2026-08-18T12:00:00+09:00", "2026-08-18T03:00:00Z"),
                "video": (ROOT / "episodes" / "PD-2026-064-memphis" / "08_edit"
                          / "memphis_final_bgm.v002.mp4").as_posix()},
    "marmet": {**_from_meta("PD-2026-065-marmet", "marmet",
                             "2026-08-19T12:00:00+09:00", "2026-08-19T03:00:00Z"),
                "video": (ROOT / "episodes" / "PD-2026-065-marmet" / "08_edit"
                          / "marmet_final_bgm.v002.mp4").as_posix()},
    # EP66-69 continue the same one-per-day 12:00 JST run. Added 2026-08-11 because
    # predict_acceptance.py measured that they had no CONFIG entry at all -- every gate could
    # have gone green and `--ep openfields` would still have been an invalid argument, at the
    # very last command. The 12:00 slot is confirmed free from 08-16 onward by yt_schedule_audit.
    # 2026-08-19: EP66-69 ship as _final_bgm.v002.mp4. v001 carries the SYNTHESISED music beds
    # written on 08-17 when the pd-media drive took the whole audio library with it; v002 is the
    # same picture remuxed against the seven Suno tracks the owner regenerated on 08-18. Same
    # pattern, and the same reason, as the memphis override above: _from_meta hardcodes v001, and
    # final_delivery is bound to the bytes that actually ship. The sha guard below still binds the
    # upload to these exact bytes -- it is what caught the mismatch.
    "openfields": {**_from_meta("PD-2026-066-openfields", "openfields",
                       "2026-08-20T12:00:00+09:00", "2026-08-20T03:00:00Z"),
               "video": (ROOT / "episodes" / "PD-2026-066-openfields" / "08_edit"
                         / "openfields_final_bgm.v002.mp4").as_posix()},
    "ramirez": {**_from_meta("PD-2026-067-ramirez", "ramirez",
                       "2026-08-21T12:00:00+09:00", "2026-08-21T03:00:00Z"),
               "video": (ROOT / "episodes" / "PD-2026-067-ramirez" / "08_edit"
                         / "ramirez_final_bgm.v002.mp4").as_posix()},
    "pinto": {**_from_meta("PD-2026-068-pinto", "pinto",
                       "2026-08-22T12:00:00+09:00", "2026-08-22T03:00:00Z"),
               "video": (ROOT / "episodes" / "PD-2026-068-pinto" / "08_edit"
                         / "pinto_final_bgm.v002.mp4").as_posix()},
    "hyatt": {**_from_meta("PD-2026-069-hyatt", "hyatt",
                       "2026-08-23T12:00:00+09:00", "2026-08-23T03:00:00Z"),
               "video": (ROOT / "episodes" / "PD-2026-069-hyatt" / "08_edit"
                         / "hyatt_final_bgm.v002.mp4").as_posix()},
    # EP70 wronghouse. 2026-08-24 12:00 JST -- the long-form slot the day after hyatt;
    # the 08-24 shorts sit at 06/09/18/21 and 12:00 is free (yt_schedule_audit, 2026-08-22).
    # The master is v001 and its sha is the one the acceptance receipt and the shipped-frames
    # review are both bound to (3a11cb7c). Title/description/tags come from the packaging file.
    # EP71 oroville. 2026-08-26 12:00 JST. The 08-25 12:00 slot could not be filled: the Shorts
    # lane spent the 08-24 quota by 16:20 and the reset (16:00 JST) lands after noon, so the
    # 16:05 push uploads this on 08-25 and it publishes 08-26 (handover 2026-08-24 §1). The
    # 08-25T12:00 value that briefly lived here would have been IN THE PAST at push time and
    # the past-publishAt guard would have burned the slot. Master v001, sha bound to
    # acceptance_receipt v001 and to the 61-sheet shipped-frames review.
    "oroville": {**_from_meta("PD-2026-071-oroville", "oroville",
                       "2026-08-26T12:00:00+09:00", "2026-08-26T03:00:00Z")},
    # EP74-EP73, one publication a day with no gap (owner directive 2026-08-25). oroville was
    # taken public early to fill 08-25, which emptied the 08-26 slot it had been holding, so
    # itaewon is uploaded the same evening it finishes rather than waiting for the next 16:05
    # push -- a push at 16:05 can only ever schedule for the FOLLOWING noon, so the seam has to
    # be closed by hand once. After that the daily push keeps the run going by itself.
    "itaewon": {**_from_meta("PD-2026-074-itaewon", "itaewon",
                       "2026-08-26T12:00:00+09:00", "2026-08-26T03:00:00Z")},
    "lahaina": {**_from_meta("PD-2026-075-lahaina", "lahaina",
                       "2026-08-27T12:00:00+09:00", "2026-08-27T03:00:00Z")},
    "morandi": {**_from_meta("PD-2026-076-morandi", "morandi",
                       "2026-08-28T12:00:00+09:00", "2026-08-28T03:00:00Z")},
    "lacmegantic": {**_from_meta("PD-2026-072-lacmegantic", "lacmegantic",
                       "2026-09-03T12:00:00+09:00", "2026-09-03T03:00:00Z")},
    "uri": {**_from_meta("PD-2026-073-uri", "uri",
                       "2026-09-02T12:00:00+09:00", "2026-09-02T03:00:00Z")},

    # EP77-85, one per day at the 12:00 JST long-form slot, 08-31 to 09-08. Added 2026-08-28
    # because CONFIG had none of them: `--ep keybridge` was an invalid argument, so every gate
    # could have gone green -- render, shipped frames, receipt, policy, dry run -- and the
    # booking would have died at the very last command. That is the same failure the EP66-69
    # comment above records, and it was found by auditing rather than by hitting it.
    # Order is readiness, not episode number: EP80/81 have their i2v and EP78/79 do not.
    "keybridge": {**_from_meta("PD-2026-077-keybridge", "keybridge",
                       "2026-09-04T12:00:00+09:00", "2026-09-04T03:00:00Z")},
    "concordia": {**_from_meta("PD-2026-080-concordia", "concordia",
                       "2026-08-31T12:00:00+09:00", "2026-08-31T03:00:00Z")},
    "station": {**_from_meta("PD-2026-081-station", "station",
                       "2026-09-05T12:00:00+09:00", "2026-09-05T03:00:00Z")},
    "valdez": {**_from_meta("PD-2026-082-valdez", "valdez",
                       "2026-09-06T12:00:00+09:00", "2026-09-06T03:00:00Z")},
    "colgan": {**_from_meta("PD-2026-078-colgan", "colgan",
                       "2026-09-07T12:00:00+09:00", "2026-09-07T03:00:00Z")},
    "alaska261": {**_from_meta("PD-2026-079-alaska261", "alaska261",
                       "2026-09-08T12:00:00+09:00", "2026-09-08T03:00:00Z")},
    "threemile": {**_from_meta("PD-2026-084-threemile", "threemile",
                       "2026-09-09T12:00:00+09:00", "2026-09-09T03:00:00Z")},
    "max737": {**_from_meta("PD-2026-083-max737", "max737",
                       "2026-09-10T12:00:00+09:00", "2026-09-10T03:00:00Z")},
    "katrina": {**_from_meta("PD-2026-085-katrina", "katrina",
                       "2026-09-11T12:00:00+09:00", "2026-09-11T03:00:00Z")},
    "wronghouse": {**_from_meta("PD-2026-070-wronghouse", "wronghouse",
                       "2026-08-24T12:00:00+09:00", "2026-08-24T03:00:00Z")},
    "florence": {
        "ep": "PD-2026-037-florence",
        "video": r"C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-037-florence/08_edit/florence_v005.mp4",
        "sched_local": "2026-07-22T12:00:00+09:00",
        "sched_utc": "2026-07-22T03:00:00Z",
        "title": "He Paid the Fine — and Was Strip-Searched Twice. The Supreme Court Said It Was Legal.",
        "description": "He had the receipt. The fine was already paid. He was arrested anyway — and then strip-searched, twice.\n\nThis is the true story of Albert Florence. In 2005 in New Jersey, a state trooper pulled over the car his wife was driving, ran his name, and found a bench warrant for an unpaid fine. But Florence had already paid that fine; a clerical error in a state database had left the warrant on the system. He was carrying a document proving the payment. It did not matter. He was arrested and held for six days across two county jails — and at each one he was subjected to a strip search, even though no one suspected him of hiding anything and the underlying matter was a fine he had already cleared.\n\nFlorence sued, arguing that a person arrested for a minor matter should not be strip-searched with no reason to suspect contraband. A federal district court agreed in 2009; a federal appeals court reversed in 2010; and in 2012, in Florence v. Board of Chosen Freeholders, the Supreme Court ruled 5–4 that the searches did not violate the Fourth Amendment. Writing for the majority, Justice Kennedy reasoned that jails may adopt reasonable search policies for everyone entering the general population, because officers cannot know who is walking in. In dissent, Justice Breyer argued that a strip search is a serious invasion of privacy and that the state should have some reason before it strips a person bare. Two justices in the majority wrote separately to narrow the ruling.\n\nThis episode walks through how a paperwork error became a constitutional question about the Fourth Amendment and the limits of what can happen to you at a jailhouse door.\n\nThis is general history, not legal advice. Some imagery is AI-assisted and symbolic, not authentic footage of real people or events; all strip-search references are non-graphic and symbolic, and no real-person likeness is depicted.\n\nSources: Florence v. Board of Chosen Freeholders, 566 U.S. 318 (2012) — https://www.oyez.org/cases/2011/10-945 ; Supreme Court opinion (PDF) — https://www.supremecourt.gov/opinions/11pdf/10-945.pdf\n\n#SupremeCourt #FourthAmendment #StripSearch #KnowYourRights #CivilRights #Florence #Documentary #TrueStory",
        "tags": ["florence v board of chosen freeholders", "strip search", "supreme court", "fourth amendment", "albert florence", "jail strip search", "know your rights", "civil rights", "5-4 decision", "justice kennedy", "justice breyer", "wrongful arrest", "paid fine warrant", "true story", "prime documentary"],
    },
    "williams": {
        "ep": "PD-2026-036-williams",
        "video": r"C:/Users/aab15/Documents/prime-documentary/remotion/out/PD-2026-036-williams_film.muxed.v004.mp4",
        "sched_local": "2026-07-21T12:00:00+09:00",
        "sched_utc": "2026-07-21T03:00:00Z",
        "title": "Police Arrested Him Because Software Said His Face Matched. It Was Wrong.",
        "description": (
            "A blurry store-camera photo. A computer's guess. A knock at the door — and an "
            "innocent father is arrested in his own driveway, in front of his family, for a "
            "crime he did not commit. This is the story of Robert Williams, and of the first "
            "known wrongful arrest in the United States caused by facial-recognition "
            "misidentification.\n\n"
            "In 2018 someone stole several thousand dollars of watches from a Detroit shop. The "
            "only lead was a grainy surveillance still. Police ran it through facial-recognition "
            "software, which pointed to Robert Williams' old driver's-license photo. On that "
            "match — and little else — he was arrested in January 2020 and held for about thirty "
            "hours. The charges were dropped, and the prosecutor's office later acknowledged the "
            "case should never have been built the way it was.\n\n"
            "A facial-recognition 'match' is a probability, not proof — it is supposed to be a "
            "lead, nothing more. And the technology has been measured as less accurate on darker "
            "skin: federal testing (NIST) and independent research (the 'Gender Shades' study) "
            "found far higher error rates for Black faces. In 2021 civil-rights lawyers sued the "
            "city; the case settled in 2024 (Williams was paid roughly three hundred thousand "
            "dollars), and Detroit adopted among the strictest police facial-recognition rules in "
            "the country: a match may be treated only as a lead, past cases must be reviewed, and "
            "a court oversees the department.\n\n"
            "This is general history, not legal advice. Some imagery is AI-assisted symbolic "
            "reconstruction, not documentary footage of real people or events; anonymous figures "
            "only, no real-person likeness.\n\n"
            "Sources: ACLU, Williams v. City of Detroit — "
            "https://www.aclu.org/cases/williams-v-city-of-detroit-face-recognition-false-arrest ; "
            "Final Settlement Agreement (2024) — "
            "https://assets.aclu.org/live/uploads/2024/06/Final-Order-of-Dismissal-and-Settlement-Agreement.pdf ; "
            "NIST FRVT Part 3: Demographic Effects — "
            "https://pages.nist.gov/frvt/reports/demographics/nistir_8280.pdf ; "
            "Gender Shades (Buolamwini & Gebru, 2018) — "
            "https://proceedings.mlr.press/v81/buolamwini18a.html\n\n"
            "#FacialRecognition #WrongfulArrest #CivilRights #Surveillance #KnowYourRights #Documentary"
        ),
        "tags": ["facial recognition", "wrongful arrest", "robert williams", "williams v detroit",
                 "face recognition false arrest", "algorithmic bias", "surveillance",
                 "civil rights", "detroit police", "know your rights", "aclu", "documentary"],
    },
    "rolin": {
        "ep": "PD-2026-034-rolin",
        "video": r"C:/Users/aab15/Documents/prime-documentary/remotion/out/PD-2026-034-rolin_film.muxed.v003.mp4",
        "sched_local": "2026-07-19T12:00:00+09:00",
        "sched_utc": "2026-07-19T03:00:00Z",
        "title": "They Took His Life Savings at the Airport — No Charges, No Crime",
        "description": (
            "You broke no law. You carried your own cash through an airport. By the gate, it was gone.\n\n"
            "This is the true story of Terry Rolin, a retired railroad worker from near Pittsburgh who "
            "kept his life savings — about $82,000 — in cash. In 2019 his daughter Rebecca Brown "
            "carried the money through Pittsburgh International Airport to deposit it in a joint bank "
            "account. A TSA X-ray flagged the cash; a state trooper and a federal DEA agent questioned "
            "her; and the government seized every dollar. No drugs were found. No arrest was made. "
            "Neither Terry nor Rebecca was ever charged with a crime.\n\n"
            "Carrying cash on a domestic U.S. flight is legal — there is no limit and nothing to "
            "declare. So how was any of this legal? The answer is civil asset forfeiture: the government "
            "sues the property itself (the cash becomes the defendant) and does not have to charge, "
            "convict, or even formally accuse the owner. This episode explains where that power comes "
            "from, the 'preponderance of the evidence' standard set by the Civil Asset Forfeiture Reform "
            "Act of 2000, and the federal equitable-sharing program the Institute for Justice argues "
            "creates a financial incentive to seize (weigh that as one interested side's argument).\n\n"
            "We also put the case in scale: a USA TODAY investigation reported the DEA seized more than "
            "$209 million from over 5,000 travelers across 15 major airports in a single decade. With the "
            "Institute for Justice, Terry and Rebecca fought back — and their savings came home.\n\n"
            "This is a true story told with AI-generated illustrations (not authentic footage); figures "
            "and quotes follow the public record. Government agencies are described neutrally.\n\n"
            "#CivilForfeiture #KnowYourRights #AirportSeizure #DEA #InstituteForJustice #PropertyRights "
            "#PolicingForProfit #FlyingWithCash #Law #Documentary"
        ),
        "tags": ["civil asset forfeiture", "civil forfeiture", "know your rights", "airport cash seizure",
                 "DEA airport", "Terry Rolin", "Rebecca Brown", "Institute for Justice", "Brown v TSA",
                 "policing for profit", "flying with cash", "traveling with cash legal", "CAFRA",
                 "equitable sharing", "fourth amendment", "your rights", "true story", "Prime Documentary"],
    },
    "tyler": {
        "ep": "PD-2026-033-tyler",
        "video": r"C:/Users/aab15/Documents/prime-documentary/remotion/out/PD-2026-033-tyler_film.muxed.v002.mp4",
        "sched_local": "2026-07-18T12:00:00+09:00",
        "sched_utc": "2026-07-18T03:00:00Z",
        "title": "Can the Government Take Your Home Over a Small Tax Debt?",
        "description": (
            "You owe the county a few thousand dollars in property taxes. They seize your home, "
            "sell it — and keep every dollar, including tens of thousands that had nothing to do "
            "with the debt. Can they actually do that? For Geraldine Tyler, the answer was yes — "
            "right up until the Supreme Court said otherwise.\n\n"
            "At ninety-four, Geraldine Tyler owed about $2,300 in unpaid property taxes on her "
            "one-bedroom Minneapolis condo. With penalties, interest, and fees, the bill grew to "
            "roughly $15,000. Hennepin County, Minnesota seized the condo, sold it for about "
            "$40,000 — and kept the entire amount, pocketing the roughly $25,000 in surplus that "
            "was hers.\n\n"
            "The Fifth Amendment says that when the government takes your property, it owes you "
            "just compensation. That surplus belonged to Tyler, not the county. In 2023, in Tyler "
            "v. Hennepin County, the Supreme Court agreed — unanimously, nine to zero. Chief "
            "Justice Roberts wrote that a taxpayer must 'render unto Caesar what is Caesar's, but "
            "no more,' and that keeping the surplus was an unconstitutional taking. The Court did "
            "not reach the Eighth Amendment excessive-fines question. Most states already required "
            "the surplus be returned; after Tyler, what critics call 'home equity theft' is barred "
            "nationwide.\n\n"
            "This is general history, not legal advice. Some imagery is AI-assisted symbolic "
            "reconstruction, not documentary footage of real people or events.\n\n"
            "Sources: Tyler v. Hennepin County, 598 U.S. 631 (2023) (No. 22-166) — "
            "https://www.supremecourt.gov/docket/docketfiles/html/public/22-166.html ; "
            "opinion https://www.law.cornell.edu/supremecourt/text/22-166\n\n"
            "#SupremeCourt #PropertyRights #FifthAmendment #HomeEquityTheft #KnowYourRights #Documentary"
        ),
        "tags": ["tyler v hennepin county", "home equity theft", "property tax foreclosure",
                 "can the government take your home", "fifth amendment", "just compensation",
                 "supreme court", "property rights", "civil forfeiture", "know your rights",
                 "law", "documentary"],
    },
    "hinders": {
        "ep": "PD-2026-035-hinders",
        "video": r"C:/Users/aab15/Documents/prime-documentary/remotion/out/PD-2026-035-hinders_film.muxed.v002.mp4",
        "sched_local": "2026-07-20T12:00:00+09:00",
        "sched_utc": "2026-07-20T03:00:00Z",
        "title": "The IRS Seized Her Entire Bank Account — For Following the Bank's Own Rule",
        "description": (
            "Carole Hinders ran a small, cash-only restaurant in Iowa for decades. She deposited "
            "her earnings in amounts under $10,000 — the same everyday habit the bank itself "
            "describes. In 2013 the IRS seized her ENTIRE bank account — about $32,820 — "
            "and never charged her with a crime.\n\n"
            "The reason was a rule called \"structuring.\" Banks must report cash deposits over "
            "$10,000; deliberately keeping deposits under that line to avoid the report is itself "
            "illegal — EVEN WHEN every dollar is legal. Under civil forfeiture the government "
            "doesn't have to charge you: it sues the money itself. Her case was literally captioned "
            "United States v. $32,820.56.\n\n"
            "After a 2014 New York Times front-page story, the IRS announced it would stop seizing "
            "accounts in pure legal-source structuring cases, and the Institute for Justice took up "
            "Carole's fight. Her money was returned. A federal watchdog later found that in a large "
            "sample of these seizures, roughly 91% came from people with no criminal charges at all "
            "— 231 such cases totaling about $17.1 million.\n\n"
            "This is a true story told with AI-generated illustrations (not authentic footage); "
            "figures and quotes follow the public record.\n\n"
            "#CivilForfeiture #IRS #Structuring #CaroleHinders #InstituteForJustice #PropertyRights "
            "#PolicingForProfit #YourRights #Law #Documentary"
        ),
        "tags": ["civil forfeiture", "structuring", "IRS", "Carole Hinders", "Institute for Justice",
                 "property rights", "policing for profit", "bank account seizure", "United States v",
                 "law", "documentary", "true story"],
    },
    "carsearch": {
        "ep": "PD-2026-032-carsearch",
        "video": r"C:/Users/aab15/Documents/prime-documentary/remotion/out/PD-2026-032-carsearch_film.muxed.v012.mp4",
        "sched_local": "2026-07-17T12:00:00+09:00",
        "sched_utc": "2026-07-17T03:00:00Z",
        "title": "Police Can Search Your Car Without a Warrant — Except One Place",
        "description": (
            "You get pulled over, and the officer says he is going to search your car. Can he? For a "
            "hundred years the answer has largely been yes — no warrant required. This is the story of "
            "the \"automobile exception,\" and the one line the Supreme Court says police still cannot "
            "cross.\n\n"
            "In Carroll v. United States (1925), the Court held that because a car is mobile, police "
            "can search it without a warrant as long as they have probable cause — a fact-based reason "
            "to believe there is evidence inside, not just a hunch. That search can reach anywhere the "
            "object of the probable cause could be (United States v. Ross, 1982; California v. Acevedo, "
            "1991), but no further. Being arrested does not automatically open your car either "
            "(Arizona v. Gant, 2009). And in Collins v. Virginia (2018), the Court drew a bright line: "
            "police cannot walk onto the curtilage of your home — like the driveway pressed against "
            "your house — and pull back a tarp to search a vehicle parked there. On the open road your "
            "car is exposed; tucked against your home, it takes on the home's protection.\n\n"
            "This is not legal advice; it is an explainer of landmark Fourth Amendment cases.\n\n"
            "#FourthAmendment #Privacy #YourRights #SupremeCourt #CarSearch #ProbableCause #Law #Documentary"
        ),
        "tags": ["car search", "Fourth Amendment", "automobile exception", "Carroll v United States",
                 "Collins v Virginia", "probable cause", "warrant", "police search", "your rights",
                 "traffic stop", "law", "documentary"],
    },
    "unlock": {
        "ep": "PD-2026-031-unlock",
        "video": r"C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-031-unlock/08_edit/renders/unlock_final.v002.mp4",
        "sched_local": "2026-07-16T12:00:00+09:00",
        "sched_utc": "2026-07-16T03:00:00Z",
        "title": "Police Can Force Your Thumb — But Maybe Not Your Mind",
        "description": (
            "Pulled over at night, an officer wants your phone unlocked. Your face and your thumb "
            "can open it in a second — but the passcode you keep only in your mind may be the one "
            "thing they can't force out of you. This is the unsettled fight over whether police "
            "can make you unlock your phone.\n\n"
            "In Riley v. California (2014), the Supreme Court ruled unanimously that police "
            "generally need a warrant to SEARCH your phone. But searching it is a different "
            "question from forcing YOU to open it — and that lands in the Fifth Amendment's "
            "protection against self-incrimination. Courts widely treat a memorized passcode as "
            "\"testimonial\" (the contents of your mind, often protected), while a fingerprint or "
            "face scan is treated as a physical act that is frequently not protected. In United "
            "States v. Payne (9th Cir., 2024) a forced thumbprint unlock was allowed; in United "
            "States v. Brown (D.C. Cir., 2025) a forced fingerprint unlock was held to violate the "
            "Fifth Amendment. States split on passcodes too — leaning protected in Pennsylvania, "
            "Indiana, and Utah; compellable in New Jersey and Illinois. The Supreme Court has "
            "repeatedly declined to settle it, so your right can change at a state line — and gets "
            "weaker still at the border.\n\n"
            "This is not legal advice; courts are genuinely split and the law is unsettled.\n\n"
            "#FifthAmendment #FourthAmendment #Privacy #FaceID #Passcode #SupremeCourt #Law #Documentary"
        ),
        "tags": ["phone unlock", "Fifth Amendment", "Fourth Amendment", "Riley v California",
                 "passcode", "Face ID", "biometrics", "compelled decryption", "digital privacy",
                 "law", "documentary", "your rights"],
    },
    "forfeiture": {
        "ep": "PD-2026-028-forfeiture",
        "video": r"E:/pd-media/episodes/PD-2026-028-forfeiture/08_edit/final.v004.mp4",
        "sched_local": "2026-07-13T12:00:00+09:00",
        "sched_utc": "2026-07-13T03:00:00Z",
        "title": "They Took Their House Over $40 — and Never Charged Anyone",
        "description": (
            "Their son sold about $40 of drugs near the family home in Philadelphia. Nobody in "
            "the family was charged with a crime — and the city still moved to take the whole "
            "house.\n\n"
            "This is civil forfeiture. Under it, the government sues the PROPERTY itself — the "
            "case is literally captioned against \"the house\" — so the usual protections that "
            "come with being accused of a crime don't apply. In Philadelphia, owners were pushed "
            "through \"Courtroom 478\" with no judge and often no lawyer, while the cash and homes "
            "seized helped fund the very prosecutors and police who took them.\n\n"
            "Christos and Markela Sourovelis were locked out of their own home. In 2014 the "
            "Institute for Justice brought a federal class action; in 2018 the city settled with a "
            "consent decree that ended the abusive program and set up a roughly $3 million fund to "
            "compensate victims. The family kept their house.\n\n"
            "#CivilForfeiture #Philadelphia #Sourovelis #PropertyRights #Law #Documentary"
        ),
        "tags": ["civil forfeiture", "Sourovelis", "Philadelphia", "Institute for Justice",
                 "property rights", "policing for profit", "Courtroom 478", "law", "documentary", "true story"],
    },
    "katz": {
        "ep": "PD-2026-026-katz",
        "video": r"E:/pd-media/episodes/PD-2026-026-katz/08_edit/final.v001.mp4",
        "sched_local": "2026-07-11T12:00:00+09:00",
        "sched_utc": "2026-07-11T03:00:00Z",
        "title": "The FBI Recorded His Calls — and Never Touched the Booth",
        "description": (
            "In 1965, FBI agents taped an electronic listening device to the OUTSIDE of a glass "
            "public phone booth in Los Angeles and recorded Charles Katz passing bets across state "
            "lines — without a warrant, and without ever setting foot inside the booth.\n\n"
            "In Katz v. United States (1967), the Supreme Court ruled 7–1 that this was a Fourth "
            "Amendment “search.” Justice Potter Stewart's majority opinion held that “the Fourth "
            "Amendment protects people, not places” — what a person seeks to keep private, even "
            "somewhere the public can go, can be constitutionally protected. A man who shuts a "
            "phone-booth door and pays the toll is entitled to assume his words will not be "
            "broadcast to the world. The decision buried the old “trespass” rule from Olmstead v. "
            "United States: a search no longer requires a physical intrusion. Justice Harlan's "
            "concurrence added the famous two-part “reasonable expectation of privacy” test; "
            "Justice Black dissented alone.\n\n"
            "That single line — “people, not places” — is why courts still reach for Katz whenever "
            "the government reaches for a new way to listen in.\n\n"
            "#SupremeCourt #FourthAmendment #Privacy #Katz #Wiretap #Law #Documentary"
        ),
        "tags": ["Supreme Court", "Fourth Amendment", "Katz", "Katz v United States", "Privacy",
                 "Wiretap", "Reasonable Expectation of Privacy", "Search and Seizure", "Law", "Documentary"],
    },
    "rodriguez": {
        "ep": "PD-2026-027-rodriguez",
        "video": r"E:/pd-media/episodes/PD-2026-027-rodriguez/08_edit/final.v001.mp4",
        "sched_local": "2026-07-12T12:00:00+09:00",
        "sched_utc": "2026-07-12T03:00:00Z",
        "title": "How Long Can the Police Keep You at a Traffic Stop?",
        "description": (
            "A Nebraska officer pulled Dennis Rodriguez over just after midnight for drifting onto "
            "the shoulder. He ran the checks, handed back the paperwork, and issued a written "
            "warning — the traffic stop was finished. Then he walked a drug dog around the car. The "
            "dog alerted about seven to eight minutes later.\n\n"
            "In Rodriguez v. United States (2015), the Supreme Court ruled 6–3 that this was an "
            "unlawful seizure. Justice Ruth Bader Ginsburg's majority held that a traffic stop may "
            "last no longer than the time needed to handle the matter that justified it — the "
            "stop's “mission.” Once the tasks tied to the traffic violation are done, authority for "
            "the stop ends; prolonging it for a dog sniff without independent reasonable suspicion "
            "violates the Fourth Amendment. The Court sent the case back to decide whether such "
            "suspicion existed. Justices Thomas, Alito, and Kennedy dissented.\n\n"
            "The rule is simple, and it still bites: the clock stops when the mission does.\n\n"
            "#SupremeCourt #FourthAmendment #TrafficStop #Rodriguez #K9 #Law #Documentary"
        ),
        "tags": ["Supreme Court", "Fourth Amendment", "Rodriguez", "Rodriguez v United States",
                 "Traffic Stop", "Dog Sniff", "K9", "Search and Seizure", "Law", "Documentary"],
    },
    "morton": {
        "ep": "PD-2026-052-morton",
        "video": r"C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-052-morton/08_edit/morton_final_bgm.v001.mp4",
        "sched_local": "2026-08-14T12:00:00+09:00",
        "sched_utc": "2026-08-14T03:00:00Z",
        # R-38 present-tense injustice; the 3-year-old witness is the film's first 20s.
        "title": "A 3-Year-Old Said His Father Wasn't Home. The State Buried It for 25 Years.",
        "description": "On 13 August 1986, Michael Morton left for work before dawn. By the time he got home, his wife Christine had been beaten to death in their bed in Williamson County, Texas, and their three-year-old son Eric had been in the house.\n\nEric told his grandmother what he saw: a monster hurt his mother, and — asked directly — that his daddy was not home. A neighbour had seen a green van parked repeatedly behind the house. Christine's missing credit card surfaced in San Antonio, and a cheque with her forged signature was cashed. None of it reached the jury. The prosecution's theory was that Michael killed her because she had fallen asleep on his birthday, and he was convicted of murder and sentenced to life.\n\nHe served nearly twenty-five years. For six of them his own lawyers fought simply for the right to test a bloodied bandana found near the house. The state opposed it repeatedly.\n\nWhen the testing finally happened, the bandana carried Christine's blood and the DNA of another man: Mark Alan Norwood. He had, by then, been convicted of a second murder committed after Christine's — a killing that happened while the file that could have named him sat unexamined in a prosecutor's office.\n\nMichael Morton was released in October 2011 and formally exonerated. The lead prosecutor, who had become a sitting judge, faced a court of inquiry over the evidence that was never handed to the defence; he surrendered his law licence and served time in county jail. In 2013 Texas passed a disclosure law that carries Michael Morton's name.\n\nThis film is about what a file can hold, and how long a state will fight to keep it shut.\n\nSome imagery is AI-assisted and symbolic, not authentic footage of real people or events, and no real-person likeness is shown.\n\nSources include the Texas court of inquiry record, the Williamson County District Attorney's own case file as released in the civil proceedings, and the Michael Morton Act (2013).\n\n#MichaelMorton #WrongfulConviction #Brady #Texas #CriminalJustice #Documentary #TrueStory",
        "tags": ["michael morton", "michael morton act", "brady violation", "wrongful conviction",
                 "williamson county", "texas", "prosecutorial misconduct", "dna exoneration",
                 "mark norwood", "christine morton", "criminal justice", "court of inquiry",
                 "documentary", "true story", "prime documentary"],
    },
    "willingham": {
        "ep": "PD-2026-051-willingham",
        "video": r"C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-051-willingham/08_edit/willingham_final_bgm.v001.mp4",
        "sched_local": "2026-08-13T12:00:00+09:00",
        "sched_utc": "2026-08-13T03:00:00Z",
        # DEEP_RESEARCH R-38: present-tense injustice framing; a resolved "exonerated after
        # N years" package is banned. R-6: the thumbnail line is spoken in the first 20s.
        "title": "Texas Executed Him for an Arson. The Fire Science Was Wrong.",
        "description": "On 23 December 1991, a house fire in Corsicana, Texas killed Cameron Todd Willingham's three daughters. Investigators looked at the burn patterns on the floor and concluded the fire had been set deliberately. He was convicted of capital murder and executed on 17 February 2004.\n\nThe problem is what happened to the science in between. The indicators the investigators relied on -- crazed glass, pour patterns, deep charring -- had been passed down as arson lore for decades, and by the 1990s laboratory work was showing that an accidental fire reaching flashover produces the same marks. In 2004, days before the execution, a fire scientist reviewed the evidence and told the state the finding could not be sustained. The execution went ahead.\n\nIn 2009 a report commissioned by the Texas Forensic Science Commission reached the same conclusion: the original determination was not supported by modern fire science. No court has vacated the conviction, and no official finding of innocence has ever been made -- which is precisely what makes the case hard to put down.\n\nThis is a film about how a discipline can be wrong for fifty years, how a courtroom treats an expert's certainty, and what a state does when the science changes after the sentence has been carried out.\n\nNo real-person likeness is shown; some imagery is AI-assisted and symbolic, not authentic footage of real people or events.\n\nSources include the Texas Forensic Science Commission record and the published fire-science review of the Corsicana investigation.\n\n#CameronToddWillingham #DeathPenalty #ForensicScience #Arson #WrongfulConviction #Texas #Documentary #TrueStory",
        "tags": ["cameron todd willingham", "arson", "fire science", "death penalty",
                 "texas", "wrongful conviction", "forensic science commission", "corsicana",
                 "flashover", "criminal justice", "documentary", "true story",
                 "prime documentary"],
    },
    "norfolk": {
        "ep": "PD-2026-053-norfolk",
        "video": r"C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-053-norfolk/08_edit/norfolk_final_bgm.v001.mp4",
        "sched_local": "2026-08-10T12:00:00+09:00",
        "sched_utc": "2026-08-10T03:00:00Z",
        "title": '4 Sailors Confess to One Murder. The DNA Clears Each One. The Detective Finds Another.',
        "description": 'On July 8, 1997, a Navy sailor came home from a week at sea and found his 18-year-old wife, Michelle Moore-Bosko, dead in their apartment near the Norfolk, Virginia naval base. There was no sign of forced entry. The wounds, a medical examiner noted, were clustered and of uniform depth — the signature of a single attacker.\n\nWithin hours, a neighbor named Danial Williams was in an interrogation room. Roughly eleven hours later, before dawn, he confessed to a murder he did not commit, after being falsely told he had failed a polygraph and warned about the death penalty. His account did not match how Michelle died, so the statement was taken again, and corrected, until it agreed with the crime scene.\n\nIn December 1997 the DNA excluded him. Police did not question the confession; they questioned who else must have been there. The theory grew a man at a time: his roommate Joseph Dick, whose Navy duty records placed him aboard his ship; Eric Wilson, questioned about nine hours; Derek Tice, arrested in Florida; and three more sailors — Richard Pauley, Geoffrey Farris and John Danser — who never confessed at all. By February 1999, all seven charged men had been excluded by DNA.\n\nThat same month, a letter left a Virginia prison cell. Omar Ballard, who was a friend of Michelle\'s and had frequently been inside her apartment, wrote that he had killed her. In March 1999 his DNA matched, and he remains the only person whose DNA was ever found at that scene. He confessed voluntarily and said, in both statements and later under oath, that he acted alone. Prosecutors did not release the sailors. They recast Ballard as an eighth attacker. Joseph Dick, excluded by DNA, pleaded guilty in April 1999 — a month and a half after the state\'s own laboratory identified the real killer.\n\nThe undoing took years. Federal courts threw out Derek Tice\'s conviction and prosecutors dropped his charges in 2011. In September 2016, U.S. District Judge John A. Gibney Jr. ruled that Danial Williams and Joseph Dick were actually innocent, writing that "by any measure, the evidence shows the defendants\' innocence." In March 2017, Governor Terry McAuliffe granted absolute pardons to all four men, including Eric Wilson, who had finished his sentence years earlier. In 2018 the Commonwealth of Virginia paid $3.5 million and the City of Norfolk paid $4.9 million more — roughly $8.4 million in all.\n\nDetective Robert Glenn Ford, who obtained the confessions, was never criminally charged over this case. In 2010 a federal jury convicted him of extortion and of lying to the FBI in unrelated matters, and in February 2011 a federal judge sentenced him to 12 and a half years.\n\nSome imagery in this film is AI-assisted, symbolic and illustrative only. It is not authentic archival footage, and no real person\'s likeness is shown.\n\nSources include: Williams v. Brown (E.D. Va., 2016); Tice v. Johnson (Fourth Circuit); the PBS Frontline documentary The Confessions and its published case timeline; Associated Press reporting on the 2018 Virginia and Norfolk settlements; U.S. Department of Justice releases on the Ford prosecution; and the National Registry of Exonerations.\n\n#NorfolkFour #FalseConfession #WrongfulConviction',
        "tags": ['Norfolk Four', 'false confession', 'coerced confession', 'wrongful conviction', 'police interrogation', 'DNA evidence', 'actual innocence', 'Danial Williams', 'Joseph Dick', 'Derek Tice', 'Eric Wilson', 'Omar Ballard', 'Navy sailors', 'Norfolk Virginia', 'criminal justice', 'documentary'],
    },
    "flowers": {
        "ep": "PD-2026-054-flowers",
        "video": r"C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-054-flowers/08_edit/flowers_final_bgm.v001.mp4",
        "sched_local": "2026-08-10T12:00:00+09:00",
        "sched_utc": "2026-08-10T03:00:00Z",
        "title": '6 Trials. 4 Death Sentences. 23 Years. The Same Prosecutor Every Time.',
        "description": 'On the morning of July 16, 1996, four people were shot in the head inside Tardy Furniture in Winona, Mississippi: Bertha Tardy, 59, the owner; Carmen Rigby, 45, who kept the books; Robert Golden, 42; and Derrick "Bobo" Stewart, 16, hired days earlier, who fought for six days before he died. No murder weapon was ever found. There was no eyewitness to the crime, no fingerprint that answered the question, and no confession.\n\nWithin days, investigators fixed on Curtis Flowers — 26 years old, a gospel singer in his family\'s group, with no criminal record of any kind. He had briefly worked at the store and been let go about two weeks before the murders over roughly thirty dollars from his paycheck. He was arrested in January 1997, and he said from the first day that he had nothing to do with it.\n\nDistrict Attorney Doug Evans tried him six times for the same four murders. Trial one, in 1997, was heard by twelve white jurors in a case pulled from a county that is nearly half Black: conviction, death sentence, reversed in 2000 for prosecutorial misconduct. Trial two, in 1999: conviction, death sentence, reversed in 2003 for misconduct again. Trial three, in 2004: conviction, death sentence, reversed in 2007 because the Mississippi Supreme Court found Evans had used his strikes to remove Black citizens from the jury because they were Black — "as strong a prima facie case of racial discrimination as we have ever seen."\n\nTrials four and five hung. When trial five ended in a mistrial in 2008, the lone Black holdout juror, James Bibbs, was handcuffed in open court and charged with perjury by Evans\' office; the state attorney general\'s office took the case away and dropped it. Trial six, in June 2010, was heard by eleven white jurors and one Black juror, and produced a fourth death sentence.\n\nThe only direct evidence in any of it was Odell Hallmon, who testified in four trials that Flowers had confessed to him in jail. In 2016 Hallmon murdered three people and pleaded guilty about two weeks later. In 2018, on a recorded prison line with APM Reports\' In the Dark, he said of the jailhouse confession: "That was a lie." The same reporters pulled jury records from courthouse storerooms across Evans\' district — more than 6,700 jurors across 225 trials — and found his office struck Black prospective jurors at nearly 4.5 times the rate it struck white ones.\n\nOn June 21, 2019, the U.S. Supreme Court reversed the sixth conviction, 7 to 2. In the six trials combined, the Court wrote, the state used its strikes against "41 of the 42 black prospective jurors that it could have struck." "The numbers speak loudly." In December 2019 Flowers left jail on bail at 49, having entered custody at 26. Evans recused himself, and on September 4, 2020, Mississippi dropped every charge, with prejudice.\n\nMississippi\'s statute pays $50,000 for each lost year, capped at ten years; in March 2021 a judge awarded Flowers the maximum, $500,000, for nearly 23 years. Doug Evans was never charged and never disciplined. In November 2022 the district that had employed him for three decades refused, 70 to 30, to make him a judge. In March 2025 an attorney-discipline official petitioned the Mississippi Supreme Court to suspend his law license; that question is still open. The murders of Bertha Tardy, Carmen Rigby, Robert Golden and Derrick Stewart remain officially unsolved.\n\nSome imagery in this film is AI-assisted, symbolic and illustrative only. It is not authentic archival footage, and no real person\'s likeness is shown.\n\nSources include: Flowers v. Mississippi (U.S. Supreme Court, 2019); the Mississippi Supreme Court\'s reversal opinions of 2000, 2003 and 2007; APM Reports\' In the Dark, Season 2, and its 225-trial jury-strike study; Mississippi Today; Associated Press and NPR reporting; and the Death Penalty Information Center.\n\n#CurtisFlowers #JurySelection #WrongfulConviction',
        "tags": ['Curtis Flowers', 'Flowers v Mississippi', 'Doug Evans', 'Batson v Kentucky', 'jury selection', 'peremptory strikes', 'In the Dark podcast', 'wrongful conviction', 'death row', 'Winona Mississippi', 'Mississippi Supreme Court', 'Odell Hallmon', 'six trials', 'prosecutorial misconduct', 'criminal justice', 'documentary'],
    },
    "postoffice": {
        "ep": "PD-2026-056-postoffice",
        "video": r"C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-056-postoffice/08_edit/postoffice_final_bgm.v001.mp4",
        "sched_local": "2026-08-13T12:00:00+09:00",
        "sched_utc": "2026-08-13T03:00:00Z",
        "title": 'A Computer Invents a £2,000 Debt. Her Own Employer Prosecutes Her. 236 Go to Prison.',
        "description": 'In 2003, in a Hampshire village shop, sub-postmistress Jo Hamilton watched her computer invent a debt in front of her. The screen said two thousand pounds was missing from her post-office till — money she had never seen. She rang the helpline and followed its instructions, and while she was on the line the missing two thousand became four. She remortgaged her house to pay it. Her employer prosecuted her anyway.\n\nThe system was Horizon, built by the British firm ICL under its Japanese owner, Fujitsu, and rolled out to every branch counter in the country from 1999. Under their contracts, sub-postmasters were personally liable for the losses their accounts showed, and the court that later examined the system found it offered them no way to dispute Horizon\'s own figures. The helpline\'s answer never changed: no one else is having this problem, you are the only one. The public inquiry heard that same sentence described by sub-postmaster after sub-postmaster.\n\nIn England and Wales any company may bring a private prosecution, and the Post Office did so on an industrial scale — investigating, charging and prosecuting its own sub-postmasters, roughly 700 of them between 1999 and 2015, about one a week for a decade and a half. Jo Hamilton pleaded guilty to false accounting after the Post Office\'s own investigators had reported, in writing, that there was no evidence of theft. Noel Thomas, a Welsh postman with 42 years of service, went to prison over a shortfall that never existed and turned sixty inside. Lee Castleton, who refused to accept a phantom debt of around twenty-five thousand pounds, was taken to the High Court, represented himself, lost, and was bankrupted by a costs bill of £321,000. On 11 November 2010 — her son\'s tenth birthday — Seema Misra was sent to prison for fifteen months. She was eight weeks pregnant.\n\nEleven weeks before Misra\'s jury returned, an internal Post Office report had already set out the price of the truth: any independent investigation of Horizon would have to be disclosed in court, and "any perception that POL doubts its own systems would mean that all criminal prosecutions would have to be stayed." In July 2013 the Post Office\'s own barrister advised that the expert evidence underpinning years of prosecutions was unreliable, and weeks later recorded that minutes of the weekly Horizon-defect calls "should be, and have been, destroyed: the word \'shredded\' was conveyed to me."\n\nAlan Bates had put £65,000 into a branch on the North Wales coast in 1998, refused to sign for losses he could not verify, and kept every receipt. Sacked in 2003, he hired a village hall in Fenny Compton in November 2009 and invited whoever else was out there. A couple of dozen strangers walked in, each of them told for years that they were the only one. In 2017, 555 sub-postmasters sued in a group action. In December 2019 Mr Justice Fraser found Legacy Horizon "not remotely robust," described the Post Office\'s stance as "the 21st century equivalent of maintaining that the earth is flat," and found that remote access to branch accounts "does exist." The 555 settled for £57.75 million; after the litigation funders and lawyers were paid, roughly £12 million was left between them — about £20,000 each.\n\nOn 23 April 2021 the Court of Appeal quashed 39 convictions, finding that "POL knew that there were serious issues about the reliability of Horizon" and that its failures were "so egregious as to make the prosecution of any of the \'Horizon cases\' an affront to the conscience of the court." Roughly nine hundred convictions still stood. After an ITV drama in January 2024 was watched by close to ten million people in a week, Parliament passed the Post Office (Horizon System) Offences Act 2024: "Every conviction to which this Act applies is quashed on the coming into force of this Act." The inquiry\'s 2025 report found roughly a thousand people were prosecuted and convicted on Horizon evidence and about ten thousand are now eligible for redress; by the BBC\'s count, 236 of them went to prison; at least thirteen deaths have been linked to the scandal, a figure the inquiry says may be higher.\n\nAs of the summer of 2026, about £1.6 billion has been paid to more than 12,900 claimants, no one has been convicted of anything for doing this, and Horizon is still on the counters of Britain\'s post offices under a Fujitsu contract extended to 2027.\n\nSome imagery in this film is AI-assisted, symbolic and illustrative only. It is not authentic archival footage, and no real person\'s likeness is shown.\n\nSources include: the Post Office Horizon IT Inquiry\'s Final Report Volume 1 by Sir Wyn Williams; Bates and Others v Post Office Ltd (No 6) [2019] EWHC 3408 (QB); Hamilton and Others v Post Office Ltd [2021] EWCA Crim 577; the Post Office (Horizon System) Offences Act 2024; Hansard; Ministry of Justice quashed-conviction management information and gov.uk redress data; the Second Sight interim report of 2013.e',
        "tags": ['Post Office scandal', 'Horizon scandal', 'Post Office Horizon', 'sub-postmasters', 'Alan Bates', 'Fujitsu Horizon', 'Bates v Post Office', 'Post Office Inquiry', 'Jo Hamilton', 'Seema Misra', 'wrongful conviction', 'private prosecution', 'miscarriage of justice', 'Mr Bates vs the Post Office', 'criminal justice', 'documentary'],
    },
    "burge": {
        "ep": "PD-2026-055-burge",
        "video": r"C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-055-burge/08_edit/burge_final_bgm.v001.mp4",
        "sched_local": "2026-08-09T12:00:00+09:00",
        "sched_utc": "2026-08-09T03:00:00Z",
        "title": 'A Doctor Reports Police Torture in 1982. The Letter Is Buried for 33 Years.',
        "description": 'In February 1982, a doctor at the Cook County Jail examined a prisoner delivered by Chicago detectives and found injuries he could not explain away: burns seared in neat parallel lines across the chest and thigh, and small scabbed wounds on the ears, nose and fingers — the marks of electrical clips. He wrote to the Superintendent of the Chicago Police Department demanding "a thorough investigation." The letter was forwarded to the Cook County State\'s Attorney\'s office. No answer came, and no investigation followed.\n\nThe prisoner was Andrew Wilson, and this film is straight about him: he murdered Chicago officers William Fahey and Richard O\'Brien, and a jury said so twice. He is in this story because of what happened inside Area 2, and because the rule against torturing prisoners is not a prize for the innocent.\n\nFor roughly two decades, Commander Jon Burge and the detectives known as the Midnight Crew tortured confessions out of more than one hundred men on Chicago\'s South Side, almost every one of them Black: electric shock from a hand-cranked box, suffocation with a plastic typewriter cover, mock executions, and a hot radiator. In 1990 the police department\'s own internal investigator, Michael Goldston, reported that the abuse was "systematic," spanned more than a decade, and "included psychological techniques and planned torture." The city fought for two years to keep that report sealed until a federal judge ordered it released in 1992.\n\nJon Burge was never charged with torture. Illinois gave prosecutors three years to bring charges for offenses of that kind, and every provable case expired while the city declined to believe the men it had broken. Special prosecutors Edward Egan and Robert Boyle worked four years, spent about seven million dollars, and examined 148 claims; in July 2006 they reported that torture had occurred in roughly half of them and that three cases — Andrew Wilson\'s among them — could be proven beyond a reasonable doubt. They filed no charges, because the clock had run. Burge had already been fired in February 1993 for the physical abuse of Wilson, and he moved to Florida with a police pension of roughly three thousand dollars a month.\n\nIn January 2003, Governor George Ryan pardoned four men on the grounds of innocence — Aaron Patterson, Madison Hobley, Leroy Orange and Stanley Howard — men tortured into confessing crimes the state now said they did not commit, and the next day he commuted 167 death sentences. In November 2003, answering written questions under oath in Hobley\'s civil suit, Burge denied ever using, seeing or knowing of torture. That denial was a brand-new federal crime with a fresh clock. FBI agents arrested him in October 2008; on June 28, 2010, a jury convicted him of perjury and obstruction of justice; and in January 2011 Judge Joan Lefkow sentenced him to four and a half years. It is the only criminal sentence anyone ever served for what happened at Area 2. Days later, a tied 4-4 vote of the police pension board let him keep his pension, and he collected it until he died in September 2018 at 70.\n\nOn May 6, 2015, the Chicago City Council passed the first municipal reparations for police violence in United States history: a $5.5 million fund for 57 living survivors of Area 2 and Area 3, a formal apology on the council floor, free city-college tuition for survivors and their children and grandchildren, and a counseling center on the South Side. The ordinance also ordered the story into the schools. Since 2018, every Chicago public-school student is taught a required history unit on what happened at Area 2, in the eighth grade and again in the tenth. It is called "Reparations Won."\n\nSome imagery in this film is AI-assisted, symbolic and illustrative only. It is not authentic archival footage, no real person\'s likeness is shown, and no act of torture is depicted.\n\nSources include: United States v. Burge (Seventh Circuit); Wilson v. City of Chicago (Seventh Circuit); the 1990 Goldston report of the Chicago Police Department\'s Office of Professional Standards; the 2006 Special State\'s Attorney report of Edward Egan and Robert Boyle; U.S. Department of Justice press releases from 2008 and 2011; John Conroy\'s reporting in the Chicago Reader, including "House of Screams"; the People\'s Law Office case archive; Amnesty International USA; the Chicago Torture Justice Center; the Illinois Torture Inquiry and Relief Commission; and the Chicago Public Schools Reparations Won curriculum.\n\n#JonBurge #ChicagoPoliceTorture #Area2',
        "tags": ['Jon Burge', 'Chicago police torture', 'Midnight Crew', 'Area 2', 'Chicago reparations', 'police accountability', 'statute of limitations', 'perjury', 'obstruction of justice', 'false confession', 'coerced confession', 'death row pardons', 'George Ryan', 'Goldston report', 'criminal justice', 'documentary'],
    },
    "fieldtest": {
        "ep": "PD-2026-057-fieldtest",
        "video": r"C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-057-fieldtest/08_edit/fieldtest_final_bgm.v001.mp4",
        "sched_local": "2026-08-11T12:00:00+09:00",
        "sched_utc": "2026-08-11T03:00:00Z",
        "title": 'A $2 Test Turned Blue. She Served 21 Days. Police Still Carry the Kits.',
        "description": 'In August 2010, in a strip-mall parking lot in Houston, a police officer dropped a small white crumb from Amy Albritton\'s car floor into a vial of pink liquid. If it stayed pink, everyone could go home. It turned blue. She was not driving — she was the passenger in her own car. Nine hours later she was booked into the Harris County jail.\n\nThe kit cost about $2 and had changed little since 1973. On the evidence submission form the officer wrote ".02 grms crack cocaine." Inside two days, with a court-appointed lawyer and an offer of 45 days instead of a two-year felony maximum, she pleaded guilty. She served 21 days.\n\nOn 23 February 2011 — roughly six months later — an analyst at the Houston Police Department crime laboratory put the evidence through a gas chromatograph-mass spectrometer. The remainder weighed 0.0134 grams, about the same, she noted, as a tiny pinch of salt. It matched nothing in the laboratory\'s database. It was not a drug. The examination sheet recorded "N.C.S. No controlled substance identified." Laboratories rarely notify officers when a false positive comes back, so nothing happened. Albritton had already lost her job, and the job was her apartment.\n\nShe was not alone. Reviewing its own files, the Harris County District Attorney\'s office found 416 uncorrected "variants" between January 2004 and June 2015, every one of them ending in a guilty plea; in 251 the laboratory result was simply "No Controlled Substance." Of 301 that began as Houston Police arrests, 212 rested on evidence the laboratory determined was not a controlled substance. All 212 pleaded guilty; 93 percent were sentenced to jail or prison; 50 had no prior drug conviction. Fifty-nine percent of the wrongfully convicted were Black, in a city whose Black population is 24 percent. The office that won those convictions is the office that found them: 119 struck from the record by the summer of 2016, more than 250 overturned in Houston by 2020.\n\nThe warnings were older than the cases. The National Bureau of Standards said in 1974 that the kits "should not be used as sole evidence for the identification of a narcotic or drug of abuse." By 1978 the Department of Justice had determined they "should not be used for evidential purposes." The chemical involved, cobalt thiocyanate, turns blue for cocaine and for more than 80 other compounds, "including methadone, certain acne medications and several common household cleaners." The results are inadmissible at trial in nearly every jurisdiction — but in Harris County in this period, 99.5 percent of felony convictions arrived by plea. Charles McClelland, who commanded the Houston Police Department, put it plainly: "Police officers aren\'t chemists. We shouldn\'t be doing field tests on the hood of patrol cars."\n\nWhat followed was narrower than it sounds. Texas House Bill 34 did not require laboratory confirmation; it ordered a study. Houston stopped using the kits in July 2017, and the stated rationale was officer safety from fentanyl exposure, not accuracy. A 2024 study by the Quattrone Center for the Fair Administration of Justice found that roughly 773,000 drug arrests a year in the United States involve colour-based field tests, that roughly 30,000 a year involve people who do not possess illegal substances, and that Black Americans experience these erroneous arrests at about three times the rate of white Americans. In March 2026 Colorado enacted House Bill 26-1020, passed 65-0 and 33-0 and signed on 26 March, barring arrest for misdemeanour drug possession where a colour-change field test is the sole basis; reporting on the bill describes it as the first state law in the country to do so.\n\nAlbritton\'s conviction was later set aside. Asked whether that ended it, she said: "No. You\'re not ever free and clear of it. It follows you everywhere you go."\n\nSome imagery in this film is AI-assisted and symbolic, and no real-person likeness is shown.\n\nSources include: ProPublica and The New York Times Magazine reporting by Ryan Gabrielson and Topher Sanders; the Houston Police Department crime laboratory examination record as quoted in that reporting; the Harris County District Attorney\'s office and its conviction integrity unit; the National Bureau of Standards; the United States Department of Justice; the Timothy Cole Exoneration Review Commission; Texas House Bill 34; the Quattrone Center for the Fair Administration of Justice at the University of Pennsylvania Carey Law School; and Colorado House Bill 26-1020 and the Colorado General Assembly\'s legislative record.\n\n#FieldDrugTest #WrongfulConviction #CriminalJustice #ForensicScience #PleaBargain #PrimeDocumentary',
        "tags": ['field drug test', 'roadside drug test', 'false positive drug test', 'Amy Albritton', 'Harris County', 'Houston police', 'wrongful conviction', 'plea bargain', 'cobalt thiocyanate', 'criminal justice system', 'forensic science', 'drug possession charge', 'presumptive drug test', 'Colorado HB 26-1020', 'Prime Documentary', 'documentary'],
    },
    "lejeune": {
        "ep": "PD-2026-058-lejeune",
        "video": r"C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-058-lejeune/08_edit/lejeune_final_bgm.v001.mp4",
        "sched_local": "2026-08-12T12:00:00+09:00",
        "sched_utc": "2026-08-12T03:00:00Z",
        "title": 'He Buried His Daughter at Nine. 408,000 Have Filed. One Claim Paid $405.',
        "description": 'In September 1985 a Marine Corps drill instructor named Jerry Ensminger lost his nine-year-old daughter, Janey, to leukemia. She was ill for nearly two and a half years. The family was told what families are always told — that these things happen, and nobody is at fault. Ensminger had given the Corps twenty-four and a half years, and he believed them. He and his wife had lived in base family housing at Tarawa Terrace from 1973 to 1975, and she spent the first three months of her pregnancy there.\n\nIn October 1980 an Army Environmental Hygiene Agency team ran routine trihalomethane tests at Camp Lejeune and could not finish them. A note on a Hadnot Point sample form dated 30 October 1980 reads: "Water is highly contaminated with low molecular weight halogenated hydrocarbons." On samples dated 9 March 1981, the Army\'s own laboratory wrote: "Water highly contaminated with other chlorinated hydrocarbons (solvents)!" The contaminated Hadnot Point wells came out of service between November 1984 and February 1985; the Tarawa Terrace plant closed in 1987. The families were not told. Ensminger learned of the contamination in August 1997, by accident, as a civilian and began filing Freedom of Information Act requests.\n\nThe measured maxima in drinking water were 215 micrograms per liter of PCE at Tarawa Terrace and 1,400 of TCE at Hadnot Point, against a federal limit of five — a limit that did not exist until 1989 and 1992. This film states exactly what the record supports and no more: it does not prove anyone in 1981 understood what those chemicals do to a body, and a federal criminal investigation found no violation of federal law and was declined for prosecution in 2007. What it proves is narrower. The institution measured its own water, wrote down that the water was heavily contaminated, took years to turn off the taps, and then did not go and find the people who had been drinking it.\n\nATSDR\'s 2017 review found sufficient evidence for causation between TCE and kidney cancer and non-Hodgkin lymphoma, PCE and bladder cancer, benzene and leukemias, and vinyl chloride and liver cancer — chemical to disease, never chemical to person. A 2024 cancer incidence study comparing Camp Lejeune personnel with Camp Pendleton reported increased risks of several cancers among those exposed at Lejeune. Whether the water caused any particular person\'s illness is a question no study has answered. There is no official total for how many people were exposed; the figure of around a million comes from a congressional hearing in 2010, not from a health agency.\n\nMike Partain was conceived, carried and born at Camp Lejeune in 1968. He testified to Congress in 2010: "\'You have male breast cancer\' were the words which greeted me and my wife on our 18th wedding anniversary." He had located 63 other men with the same rare cancer and a connection to the same water; the count he keeps now runs past 125. That list is a registry one man assembled, not epidemiology — when federal researchers tested the question in 2015 with 71 cases against 373 controls, the odds ratio came out at 1.14 with a confidence interval running through 1. On 28 April 2009 ATSDR withdrew its own 1997 public health assessment of the base, because it had left out benzene.\n\nFor thirty years North Carolina\'s statute of repose kept these claims out of court, and about 4,000 of them were dismissed in December 2016. Congress answered with the Janey Ensminger Act, signed 6 August 2012, and then the Camp Lejeune Justice Act, section 804 of the PACT Act, signed 10 August 2022 — which waived immunity, took the statute of repose off the board, and set the burden at "sufficient to conclude that a causal relationship is at least as likely as not." Law firms spent nearly $112 million on television advertising for claimants in 2022 alone. The filing window closed, for almost everyone, on 10 August 2024.\n\nAs of the government\'s 15 June 2026 filing: 408,000 de-duplicated administrative claims, 3,759 lawsuits, roughly 2,446 people paid, $723,850,000 in total payments. Three of the twenty-five bellwether cases had settled — $10,000, $24,000, and $405. Not one case has been tried. On 30 June 2026 the court reappointed the plaintiffs\' leadership group only until 30 October 2026, ordered weekly settlement meetings, and wrote that it expects both sides "to use their best efforts to achieve a global settlement by October 30, 2026." No court has ever ruled on whether the United States is liable, and no individual has ever been publicly disciplined or prosecuted over the contamination.\n\nSome imagery in this film is AI-assisted and symbolic, and no real-person likeness is shown.\n\nSources: congressional testimony of Ensminger (2007) and Partain (2010); ATSDR; US Army records; Bove et al and Ruckart et al, Environmental Health; the Camp Lejeune Justice Act (PACT Act s.804).\n\n#CampLejeune #ToxicExposure #Veterans #PACTAct #MarineCorps #PrimeDocumentary',
        "tags": ['Camp Lejeune', 'Camp Lejeune water contamination', 'Jerry Ensminger', 'Mike Partain', 'Camp Lejeune Justice Act', 'Janey Ensminger Act', 'PACT Act', 'ATSDR', 'trichloroethylene', 'tetrachloroethylene', 'Marine Corps', 'veterans benefits', 'toxic exposure', 'mass tort', 'Eastern District of North Carolina', 'Prime Documentary', 'documentary'],
    },
    "robosigning": {
        "ep": "PD-2026-059-robosigning",
        "video": r"C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-059-robosigning/08_edit/robosigning_final_bgm.v001.mp4",
        "sched_local": "2026-08-13T12:00:00+09:00",
        "sched_utc": "2026-08-13T03:00:00Z",
        "title": 'He Paid $139,000 Cash. There Was No Mortgage. The Bank Padlocked the Door.',
        "description": 'In March 2005 Charlie and Maria Cardoso paid $139,000 cash for a house in Spring Hill, Florida—price and year from newspaper reporting citing county records; the complaint calls it his life savings. No lender, no lien, no note, just a county-recorded deed anyone could read.\n\nIn late June 2009 their tenant phoned in a panic: three men from Bank of America were foreclosing. The house was cleaned out and padlocked. The bank\'s target stood across the street, about ten doors down; its listing agent said so. On 5 January 2010 a representative admitted the mistake, promising a call within the hour. It never came. His son drove him 1,300 miles from Massachusetts; on 9 January 2010 he bolt-cut the padlocks off his own front door and went in through the back screen door: pipes frozen, tools and family photographs gone, only the attic untouched. They sued in federal court on 20 January 2010.\n\nTo take a house through a court a bank hands a judge a sworn affidavit: a named person swearing on penalty of perjury to personal knowledge. Most homeowners in foreclosure have no lawyer; often it is the only evidence. On 10 December 2009, under oath, Jeffrey Stephan, a GMAC Mortgage document execution team leader, described here only from his sworn testimony, said his team brought him "approximately, I\'d say a round number of ten thousand" documents a month. Asked, "So these documents wouldn\'t be actually executed on your own personal knowledge?", he answered: "Right." A second deposition, June 2010: 400 a day, and he never appeared before the notary. Maine\'s highest court called the filing "a disturbing example of a reprehensible practice."\n\nFrom an office park in Alpharetta, Georgia, DocX, owned by Lender Processing Services, filed—per the Justice Department—over a million fraudulently signed and notarised mortgage documents with county recorders from at least March 2003 to late 2009, on about $60 million of revenue. The commonest signature is Linda Green\'s: an auto-parts shipping clerk who joined DocX in 2003, says she was never a bank vice president, and was never charged. DocX made her one, she said, because her name was short and easy to spell; as demand grew others wrote it in a dozen hands. One, Chris Pendley, earned $10 an hour against a floor of 350 signatures an hour, notarised by the man at the next desk.\n\nWhen a Bank of America official testified to signing 7,000-8,000 foreclosure documents a month unread, it stopped fast. GMAC halted evictions in 23 states on 20 September 2010; JPMorgan Chase suspended over 50,000 foreclosures; Bank of America froze those same 23 on 1 October, all fifty on 8 October—those 23 being where a judge is handed the paperwork, the only reason anyone looked. All fifty attorneys general opened a joint investigation on 13 October. Seventeen days later it restarted: Bank of America would process affidavits in 102,000 proceedings, Wells Fargo supplemental affidavits in 55,000 actions.\n\nSettlement: 9 February 2012, $25 billion; $1.5 billion of it (6%) was cash for people already foreclosed on: June 2013, 962,278 valid claims at about $1,480 each. The Independent Foreclosure Review, meant to open every 2009 and 2010 foreclosure file, was terminated 7 January 2013 at about 14% reviewed, no consultant\'s sample finished, after regulators heard finishing would cost at least $2 billion more in fees against roughly $1.2 billion of remediation. Its replacement paid, in the Fed\'s words, "regardless of whether the borrower had suffered financial injury caused by servicer error": of 3,949,896 in the Fed\'s table, 2,358,441 got $300 and 1,082 got $125,000. So no number exists for how many American foreclosures rested on manufactured documents. One man went to federal prison: DocX chief executive Lorraine Brown, guilty plea 20 November 2012, five years on 25 June 2013. Lender Processing Services signed a non-prosecution agreement, paying $35 million.\n\nThe Consumer Financial Protection Bureau has documented "zombie second mortgages"—loans most borrowers last paid in 2015 or earlier, sold to debt collectors and resurfacing as foreclosure threats—and in January 2025 found one or more had not sent those homeowners the statements the law requires. In the Government Accountability Office\'s words, the Bureau has shrunk since February 2025: a statutory funding cap halved in July 2025, stop-work orders, closed examinations, terminated enforcement cases, reduction-in-force notices covering the overwhelming majority of staff—a plan a federal court has so far blocked, the litigation still live as this film goes out.\n\nSome imagery in this film is AI-assisted and symbolic; no real-person likeness is shown.\n\nSources: Cardoso v. Bank of America (D. Mass.); St. Petersburg Times (Marrero); Stephan depositions (2009, 2010); Fannie Mae v. Bradbury (Me.); DOJ; Florida AG; 60 Minutes; Congressional Oversight Panel; Fed; GAO; CFPB; Nevada & Missouri AGs; CoreLogic; AP.\n\n#RoboSigning #ForeclosureCrisis #PrimeDocumentary',
        "tags": ['robo-signing', 'foreclosure crisis', 'wrongful foreclosure', 'DocX', 'Linda Green signature', 'Jeffrey Stephan deposition', 'Lender Processing Services', 'National Mortgage Settlement', 'Independent Foreclosure Review', 'Lorraine Brown', 'mortgage documents', 'housing crisis 2010', 'zombie second mortgage', 'Consumer Financial Protection Bureau', 'property records', 'Prime Documentary', 'documentary'],
    },
    "surfside": {
        "ep": 'PD-2026-060-surfside',
        "video": 'C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-060-surfside/08_edit/surfside_final_bgm.v001.mp4',
        "sched_local": '2026-08-14T12:00:00+09:00',
        "sched_utc": '2026-08-14T03:00:00Z',
        "title": 'The Repair Money Was Due July 1. The Building Fell June 24. 98 Died.',
        "description": 'In October 2018 an engineer walked down into the garage under the swimming pool at Champlain Towers South and put a hammer to the ceiling. Sound concrete rings. Concrete that has come away from the steel inside it gives back a flat, dead knock.\n\nTwo years and eight months later, at twenty-two minutes past one in the morning on 24 June 2021, that twelve-storey building in Surfside, Florida came down on the people asleep inside it. Ninety-eight of them died. This film is about the three years before that night.\n\nFrank Morabito\'s structural field survey found the waterproofing under the pool deck had failed - not was failing, had failed - and that this was "causing major structural damage to the concrete structural slab below these areas": the pool deck, the entrance drive and the planters. He recorded "abundant concrete cracking and spalling," and priced the repair at $9.1 million, across 136 apartments.\n\nTwo days before the November 2018 board meeting, a board member, Mara Chouela, sent that report out of the association to the town of Surfside. Nothing obliged her to. The town\'s chief building official, Ross Prieto, came to the meeting, and according to the association\'s own minutes he told the board the building was in very good shape. Contacted in June 2021, he said he did not remember receiving it and, on legal advice, declined to say more.\n\nNothing was repaired. At the start of 2021 the association\'s reserve fund held about $706,000 against a projected capital need of roughly $10.3 million - about seven per cent, after forty years of decisions owners made charging themselves.\n\nBy early 2021 the work had been repriced at $15 million, and in April the owners voted for it. A one-bedroom owed $80,190; the four-bedroom penthouse owed $336,135. You could pay in one sum or across fifteen years, and the deadline to choose was 1 July 2021.\n\nOn 9 April the board president, Jean Wodnicki, wrote to residents to explain. The observable damage, including in the underground garage, "has gotten significantly worse since the initial inspection." It was "accelerating." It would "begin to multiply exponentially."\n\nThe building came down on 24 June. The money was due on 1 July. Seven days. Nobody in that building ever paid the assessment.\n\nOn 22 June 2026 the National Institute of Standards and Technology published the technical findings of its National Construction Safety Team investigation, co-led by Judith Mitrani-Reiser and Glenn Bell. Two connections between garage columns and the pool-deck slab failed in the first week of June 2021, and the failure spread from one connection to the next over about three weeks: punching shear. On the night itself the deck went first - in the investigators\' own words, "The pool deck collapsed more than four minutes before the general collapse of the tower."\n\nMitrani-Reiser: buildings designed and built to code "have margins against failure... In the case of Champlain Towers South, however, these margins against failure were too narrow from the start." Bell named two causes: severe and widespread deviations of the original design from the codes and standards of the day, and deviations of the construction from the design drawings. The deck was understrength, its reinforcement misplaced when it was poured, planters, sand and pavers added over the decades, the steel inside corroding throughout. The argument in that building was about restoring a structure to a condition it had never been in.\n\nOn 23 June 2022 Judge Michael Hanzman of the Miami-Dade Circuit Court approved a $1,021,199,000 settlement involving more than twenty-four defendants, about $96 million of it for those who lost one of the 136 apartments. In July 2021 the Miami-Dade State Attorney had convened a grand jury; it reported that December under the title "Surfside Condo Collapse: Recommendations to Make Buildings Safer", proposed changes to the Florida Condominium Act. It contains no indictment, no recommendation of prosecution and no reference to criminal liability, and it reached no conclusion about what had caused this building to fall.\n\nAlmost everything that mattered was written down before it happened. The building did not fall because nobody knew. It fell with the paperwork in order.\n\nSome imagery in this film is AI-assisted and symbolic; no real-person likeness is shown, and no collapse, rescue or recovery imagery is used.\n\nSources: the NIST press release and NCST materials of 22 June 2026 and the investigators\' NCST Advisory Committee deck of 9 September 2025; the October 2018 Morabito Consultants survey via NBC 6, The Real Deal and Commercial Observer; the November 2018 board minutes via the Miami Herald; the Wodnicki letter as transcribed by The Washington Post and NPR; CNN on the assessment and reserves; NBC News on the settlement; NPR on the grand jury report.\n\n#Surfside #ChamplainTowers #PrimeDocumentary',
        "tags": ['Surfside condo collapse', 'Champlain Towers South', 'NIST investigation', 'punching shear', 'Morabito report', 'structural engineering', 'condo board', 'special assessment', 'building safety', 'Ross Prieto', 'Jean Wodnicki', 'Mara Chouela', '40-year recertification', 'reserve fund', 'Florida Condominium Act', 'Prime Documentary', 'documentary'],
    },
    # EP61. R3: living people are named, including a former District Attorney against whom
    # allegations were PLEADED, NOT PROVEN (Weimer v. County of Fayette, 972 F.3d 177 (3d Cir.
    # 2020), an appeal from a motion to dismiss). The description attributes every allegation
    # to that pleading, states that no named person has been found liable or guilty, does not
    # give the outcome of the civil suit, and does not answer who killed Curtis Haith. The
    # sentence length is unresolved (judgment 15-30, reporting 12-25) and appears NOWHERE in
    # the title, description or thumbnail -- only once in a burned-in caption, because the
    # confirmed script says it once and captions must match narration.
    # OWNER LEGAL REVIEW IS STILL REQUIRED BEFORE PUBLICATION. Scheduling is not clearance.
    "weimer": {
        "ep": "PD-2026-061-weimer",
        "video": 'C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-061-weimer/08_edit/weimer_final_bgm.v001.mp4',
        "sched_local": "2026-08-15T12:00:00+09:00",
        "sched_utc": "2026-08-15T03:00:00Z",
        "title": 'The Lab Cleared Her in Weeks. She Served Eleven Years.',
        "description": 'On the morning of 27 January 2001, officers in Connellsville, Pennsylvania found Curtis Haith dead outside his apartment, beaten and shot in the face. He was twenty-one, and he wanted to be a chef.\n\nA dozen or more people had passed through that apartment overnight. One of them was Crystal Weimer, a single mother of three young daughters. Officers found her still in the previous night\'s clothes, with minor injuries to her face and foot and what looked like mud and blood on them. She told them where she had been; her cousin, her sisters and Michael Gibson, the man she was seeing, said the same. The injuries came from horseplay and a fight with Gibson days earlier, she said.\n\nThen the laboratory results came back. The blood on her clothes was Gibson\'s, exactly as she had said. None of the DNA from the scene matched her, and what was there suggested a male profile. Nothing at the scene carried her.\n\nTwenty months passed with no charge. In October 2002 Thomas Beal, whom Weimer had dated before Gibson, told police that she and Gibson had killed Haith - and that she had told him the blood on her clothes was Haith\'s, which the testing had ruled out twenty months earlier.\n\nA state investigator reviewing autopsy photographs saw what she believed was a bite mark on Haith\'s hand. A Fayette County dentist first concluded that Gibson had left it; given impressions of Weimer\'s teeth as well, she reported she could not identify whose teeth caused the mark. A second expert, given the photographs, both sets of impressions and Beal\'s statement, concluded the mark matched Weimer. As the complaint alleges, District Attorney Nancy Vernon directed officers to investigate the timing, and the expert updated his opinion: seven to ten minutes before Haith\'s death, without reviewing any additional evidence.\n\nRe-interviewed, Beal added a third participant, a man he called Lonnie; officers established that Lonnie was incarcerated on the night of the murder. The court\'s own sentence about what followed: "Despite these puzzling changes to his story, Beal remained a key witness."\n\nIn late December 2003, "despite the conflicting statements from Beal, Blair, and Stenger", officers prepared a murder complaint against Weimer, and Vernon approved it. She was arrested in January 2004. "The case against Weimer fell apart almost immediately." At the preliminary hearing Beal recanted on the stand, testifying that an officer "kind of like coaxed me along on how to do it." The charges were dismissed and she went home. "Nevertheless, investigators continued to focus their efforts on Weimer."\n\nSix months later a prisoner, Joseph Stenger, offered to implicate her in exchange for a lighter sentence of his own, and she was arrested again. On 7 April 2006 a jury convicted her of third-degree murder and conspiracy. Jailhouse witnesses had told that jury they were receiving no deals.\n\nThen nine years. On 1 October 2015 a judge vacated the convictions and granted a new trial. Stenger recanted, conceding he had known nothing about the murder and that police had walked him through his testimony. The bite-mark expert disavowed his trial testimony, calling the opinion he gave the jury "junk science." Counsel found letters in the District Attorney\'s files from jailhouse informants who had testified they were getting nothing: they had asked for deals, and may have received them. An expert who read the photographs of her injuries from that first morning found them consistent with the account she gave that day.\n\nOn 27 June 2016 the charges were "dropped with prejudice." She had spent "more than eleven years in prison for murder."\n\nEverything above is taken from the Third Circuit\'s opinion in Weimer v. County of Fayette, 972 F.3d 177 (3d Cir. 2020). That was an appeal from a motion to dismiss: the court\'s recitation of the facts is limited to the plaintiff\'s well-pleaded allegations, accepted as true and read in her favour for that appeal only. The allegations in Weimer\'s 2017 civil suit are pleaded, not proved. This film makes no finding about what anyone intended, and no person named here has been found liable or guilty of anything described. The 2020 decision reached "only a narrow sliver" of the case - whether immunity shielded Nancy Vernon from answering the claims at all - and its outcome is not stated here.\n\nNothing here establishes who killed Curtis Haith; his killing has never been answered. The vacatur and the dismissal with prejudice resolve one thing only: the case against her was not a case.\n\nSome imagery is AI-assisted and symbolic; no real-person likeness is shown, and there is no depiction of the killing, the victim or the injury.\n\nSources: Weimer v. County of Fayette, 972 F.3d 177 (3d Cir. 2020); WHYY, 1 October 2018.\n\n#WrongfulConviction #BiteMarkEvidence #JailhouseInformant #Pennsylvania #PrimeDocumentary',
        "tags": ['Crystal Weimer', 'wrongful conviction', 'Fayette County', 'Connellsville Pennsylvania', 'Curtis Haith', 'bite mark evidence', 'forensic odontology', 'jailhouse informant', 'recanted testimony', 'DNA exclusion', 'Third Circuit', 'prosecutorial immunity', 'Nancy Vernon', 'exoneration', 'criminal justice', 'Prime Documentary', 'documentary'],
    },
    "centralpark": {
        "ep": "PD-2026-050-centralpark",
        # v009, NOT v009_ae: the AE hero-card composite put 36 full-frame title cards of 5-7s
        # into the film (measured 132.9s frozen) and one of them, B8 at 132.5s, is 6.0s of pure
        # black. The same measurement on v009 returns zero of both.
        "video": r"C:/Users/aab15/Documents/prime-documentary/episodes/PD-2026-050-centralpark/08_edit/centralpark_final_bgm.v009.mp4",
        "sched_local": "2026-08-04T12:00:00+09:00",
        "sched_utc": "2026-08-04T03:00:00Z",
        # DEEP_RESEARCH R-38: present-tense injustice framing; "exonerated after N years"
        # resolved-form packaging is banned. R-6: the thumb line ("5 CONFESSIONS / NO EVIDENCE")
        # is spoken inside the first 20 seconds of the film.
        "title": "Five Children Confessed to a Crime They Didn't Commit. There Was No Evidence.",
        "description": (
            "Five boys, aged 14 to 16, sat in New York police stations in April 1989 and, after "
            "hours no camera recorded, said they had attacked a woman in Central Park. Not one "
            "of them had touched her.\n\n"
            "This is the full story of Kevin Richardson, Raymond Santana, Antron McCray, Yusef "
            "Salaam and Korey Wise — how a frightened city, a case with no physical evidence, "
            "and an interrogation technique built to produce agreement turned five children into "
            "a headline. Their videotaped statements contradicted each other and the crime scene. "
            "The DNA recovered from the victim matched none of them. They were convicted anyway.\n\n"
            "Four of them served roughly six to seven years. Korey Wise, the oldest at sixteen and "
            "the only one tried as an adult, served about thirteen — in adult prisons, because a "
            "friend asked him to come along to the precinct. In 2002 a man named Matias Reyes, "
            "already serving a life sentence, said he had committed the attack alone; the DNA "
            "matched him. The convictions were vacated that year. The City of New York settled "
            "with the five for about forty-one million dollars in 2014, and the State of New York "
            "for roughly three point nine million more, with no admission of wrongdoing.\n\n"
            "This film is about the machinery, not the monsters: what a police station is to a "
            "fourteen-year-old at three in the morning, why the oldest lie in interrogation — "
            "'you can go home as soon as you tell us what happened' — has put more innocent "
            "people in prison than any weapon, and why the tape started rolling only at the end.\n\n"
            "Nothing here is graphic and no real-person likeness is shown. Some imagery is "
            "AI-assisted and symbolic, not authentic footage of real people or events.\n\n"
            "Sources include the New York County District Attorney's 2002 Affirmation in Response "
            "to Motion to Vacate Judgment, the court record of the vacated convictions, and "
            "contemporaneous reporting on the 2014 city settlement.\n\n"
            "#CentralParkFive #ExoneratedFive #FalseConfession #WrongfulConviction #KoreyWise "
            "#CriminalJustice #Documentary #TrueStory"
        ),
        "tags": ["central park five", "exonerated five", "korey wise", "yusef salaam",
                 "raymond santana", "antron mccray", "kevin richardson", "false confession",
                 "wrongful conviction", "interrogation", "reid technique", "matias reyes",
                 "dna exoneration", "1989 new york", "criminal justice", "documentary",
                 "true story", "prime documentary"],
    },
    "cotton": {
        "ep": "PD-2026-030-cotton",
        "video": r"E:/pd-media/episodes/PD-2026-030-cotton/08_edit/renders/final.premium.v004.mp4",
        "sched_local": "2026-07-15T12:00:00+09:00",
        "sched_utc": "2026-07-15T03:00:00Z",
        "title": "She Studied His Face to Be Certain. She Convicted the Wrong Man.",
        "description": (
            "In 1984, a college student was raped at knifepoint — and forced herself to memorize "
            "every detail of her attacker's face so she could make sure he was caught. She picked "
            "Ronald Cotton out of a photo array, then a live lineup, with total confidence. He was "
            "tried twice and convicted twice, largely on the strength of that certain "
            "identification.\n\n"
            "Cotton spent more than ten years in prison. Behind bars he crossed paths with another "
            "man, Bobby Poole, who looked strikingly like him and was said to have bragged about "
            "the crime. For years the courts would not reopen the case.\n\n"
            "In 1995, DNA testing did what memory could not: it proved Ronald Cotton was innocent "
            "and matched Bobby Poole to the assault. Cotton was exonerated after eleven years for a "
            "crime he did not commit.\n\n"
            "What happened next is the part almost no one expects. Jennifer Thompson — the "
            "eyewitness whose testimony sent him away — and Ronald Cotton became friends, wrote a "
            "book together (\"Picking Cotton\"), and now speak out about how confident, honest "
            "eyewitnesses can be completely wrong. Mistaken eyewitness identification is one of the "
            "leading factors in wrongful convictions later overturned by DNA.\n\n"
            "Certainty is not proof.\n\n"
            "#WrongfulConviction #EyewitnessMisidentification #RonaldCotton #PickingCotton "
            "#Innocence #DNA #Documentary #TrueStory"
        ),
        "tags": ["wrongful conviction", "eyewitness misidentification", "Ronald Cotton",
                 "Jennifer Thompson", "Picking Cotton", "Innocence Project", "DNA exoneration",
                 "criminal justice", "documentary", "true story"],
    },
}


def sha(p: Path) -> str:
    return "sha256:" + sha256_file(p)


def initiate_upload(token, size, cfg):
    # Every publish date in CONFIG is hand-written, and three of them were written while they were
    # still in the future and never revisited: on 2026-08-09 norfolk, willingham and morton all
    # carried dates from the previous week. A publishAt in the past is not a schedule - the episode
    # goes public the moment the upload lands, with no approved date and no chance to check it.
    when = datetime.fromisoformat(cfg["sched_utc"].replace("Z", "+00:00"))
    if when <= datetime.now(timezone.utc):
        raise SystemExit(
            f"REFUSING: sched_utc {cfg['sched_utc']} is in the past. Scheduling means a future "
            f"date; this would publish immediately. Update the CONFIG entry first.")
    # YOUTUBE'S OWN LIMITS, CHECKED HERE RATHER THAN AS A 400 AFTER THE PREFLIGHT PASSES.
    # 2026-08-19: EP68 pinto failed twice with "invalid video description" -- a bare HTTP 400 with
    # no hint -- after every gate had gone green, because a packaging correction the day before
    # pushed the description to 5,108 characters against a 5,000 limit. The uploader had already
    # verified the sha, the thumbnail, the captions and the schedule; the only thing it had not
    # checked was whether the metadata could legally be sent. Sibling episodes run 4,869-4,981,
    # so this is a real ceiling the writing sits close to, not a theoretical one.
    _desc = cfg["description"].rstrip()
    _limits = [("description", len(_desc), 5000), ("title", len(cfg["title"]), 100),
               ("tags total", sum(len(t) + 1 for t in cfg["tags"]), 500)]
    _over = [(n, got, cap) for n, got, cap in _limits if got > cap]
    if _over:
        raise SystemExit("REFUSING: metadata exceeds YouTube's limits before the upload starts -- "
                         + "; ".join(f"{n} {got} > {cap}" for n, got, cap in _over)
                         + ". Trim the packaging file, then re-run check_packaging_claims.")
    snippet = {"title": cfg["title"], "description": cfg["description"].rstrip(), "tags": cfg["tags"],
               "categoryId": "27", "defaultLanguage": "en", "defaultAudioLanguage": "en"}
    status = {"privacyStatus": "private", "publishAt": cfg["sched_utc"], "selfDeclaredMadeForKids": False,
              "containsSyntheticMedia": True, "license": "youtube", "embeddable": True, "publicStatsViewable": True}
    body = json.dumps({"snippet": snippet, "status": status}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=body, method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    with urllib.request.urlopen(req, timeout=60) as r:
        url = r.headers.get("Location", "")
    if not url.startswith("https://www.googleapis.com/"):
        raise RuntimeError(f"bad upload url {url[:80]}")
    return url


def _query_position(url, token, size):
    req = urllib.request.Request(url, data=b"", method="PUT",
                                 headers={"Authorization": f"Bearer {token}", "Content-Range": f"bytes */{size}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return ("done", json.loads(r.read().decode()).get("id"))
    except urllib.error.HTTPError as e:
        if e.code in (200, 201):
            return ("done", json.loads(e.read().decode()).get("id"))
        if e.code == 308:
            rng = e.headers.get("Range")
            return ("inc", (int(rng.split("-")[1]) + 1) if rng else 0)
        raise


def _fresh_token():
    """A 2GB upload outlives a Google access token, so one token fetched at the start expires
    mid-run: EP52 and EP53 both uploaded completely and then died 401 on the very next call,
    leaving a scheduled video with an auto-generated thumbnail and, once, a duplicate upload.
    Every phase now takes a new token."""
    return _access_token(load_env())


def resilient_upload(url, token, path, chunk=8 * 1024 * 1024, max_fail=12):
    size = path.stat().st_size
    sent = 0
    fails = 0
    f = open(path, "rb")
    try:
        while sent < size:
            f.seek(sent)
            data = f.read(chunk)
            end = sent + len(data) - 1
            req = urllib.request.Request(url, data=data, method="PUT",
                                         headers={"Authorization": f"Bearer {token}", "Content-Type": "video/mp4",
                                                  "Content-Range": f"bytes {sent}-{end}/{size}", "Content-Length": str(len(data))})
            try:
                with urllib.request.urlopen(req, timeout=300) as r:
                    return json.loads(r.read().decode()).get("id")
            except urllib.error.HTTPError as e:
                if e.code == 308:
                    rng = e.headers.get("Range")
                    sent = (int(rng.split("-")[1]) + 1) if rng else end + 1
                    fails = 0
                    print(f"  {sent/1e6:.0f}/{size/1e6:.0f} MB ({sent/size*100:.0f}%)")
                    continue
                raise
            except (urllib.error.URLError, ssl.SSLError, TimeoutError, ConnectionError, OSError) as e:
                fails += 1
                if fails > max_fail:
                    raise RuntimeError(f"upload aborted after {fails} network failures: {e}")
                wait = min(2 ** fails, 30)
                print(f"  net drop at {sent/1e6:.0f} MB — resume attempt {fails} in {wait}s ({type(e).__name__})")
                time.sleep(wait)
                st = _query_position(url, token, size)
                if st[0] == "done":
                    return st[1]
                sent = st[1]
                continue
        raise RuntimeError("upload ended without a video id")
    finally:
        f.close()


def set_thumbnail(token, vid, path):
    ct = mimetypes.guess_type(path.name)[0] or "image/png"
    req = urllib.request.Request(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
                                 data=path.read_bytes(), method="POST",
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": ct})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def upload_caption(token, vid, caps, slug):
    b = f"{slug}_caption_{int(time.time())}"
    meta = {"snippet": {"videoId": vid, "language": "en", "name": "English", "isDraft": False}}
    body = b"".join([f"--{b}\r\n".encode(), b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
                     json.dumps(meta).encode(), b"\r\n", f"--{b}\r\n".encode(),
                     b"Content-Type: application/x-subrip\r\n\r\n", caps.read_bytes(), b"\r\n", f"--{b}--\r\n".encode()])
    req = urllib.request.Request("https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet",
                                 data=body, method="POST",
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": f"multipart/related; boundary={b}"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def get_state(token, vid):
    req = urllib.request.Request(f"https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id={vid}",
                                 headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True, choices=sorted(CONFIG))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--explain-policy", action="store_true",
                    help="print how config/ship_policy.v001.json classifies this episode's "
                         "acceptance failures, then exit. Touches no network and uploads "
                         "nothing -- it is the answer to 'why did this refuse?'")
    ap.add_argument("--receipt", metavar="PATH",
                    help="with --explain-policy only: classify THIS receipt instead of the "
                         "latest one (used to demonstrate the gate refusing)")
    ap.add_argument("--replaces", metavar="VIDEO_ID",
                    help="this upload supersedes VIDEO_ID, whose bytes cannot be replaced in "
                         "place. VIDEO_ID must exist on this channel and must already be "
                         "private with no publishAt, or this refuses.")
    args = ap.parse_args(argv)
    cfg = CONFIG[args.ep]
    if cfg.get("_error"):
        raise SystemExit(f"{args.ep}: {cfg['_error']} -- write the packaging file "
                         f"({cfg.get('meta_source', '09_package/youtube_meta.v001.json')}) "
                         f"before scheduling")
    slug = args.ep
    EP = cfg["ep"]
    EPDIR = ROOT / "episodes" / EP
    PKG = EPDIR / "09_package"
    VIDEO = Path(cfg["video"])
    # use the LATEST selected thumbnail + final_delivery revision (v003 thumb / v004+ delivery)
    _thumbs = sorted(PKG.glob("thumbnail.selected.v*.png"))
    THUMB = _thumbs[-1] if _thumbs else PKG / "thumbnail.selected.v001.png"
    # The burned-in captions are drawn from film.json (film time), but captions.final.v001.srt
    # is BODY time -- on an episode whose VO starts after a hook + title card, the sidecar YouTube
    # track runs that many seconds early for every CC viewer. When a film-time sidecar exists
    # (captions.youtube.v*.srt), it is the one that gets uploaded.
    _yt_caps = sorted((EPDIR / "08_edit").glob("captions.youtube.v*.srt"))
    CAPS = _yt_caps[-1] if _yt_caps else EPDIR / "08_edit" / "captions.final.v001.srt"
    _dels = sorted(PKG.glob("final_delivery.v*.json"))
    DELIVERY = _dels[-1] if _dels else PKG / "final_delivery.v001.json"
    RESULT = PKG / "youtube_schedule_result.v001.json"
    # A SUPERSEDING UPLOAD IS A NEW REVISION, NOT AN OVERWRITE.
    # The v001 receipt records which bytes went up the first time; that record is what makes it
    # possible to say later which film the public actually saw. Rewriting it would destroy the
    # only evidence that the first upload was different.
    if getattr(args, "replaces", None):
        _n = 2
        while (PKG / f"youtube_schedule_result.v{_n:03d}.json").exists():
            _n += 1
        RESULT = PKG / f"youtube_schedule_result.v{_n:03d}.json"
        print(f"[supersede] receipt -> {RESULT.name} (v001 kept as the record of "
              f"{args.replaces})")

    if args.receipt and not args.explain_policy:
        raise SystemExit("--receipt is only accepted with --explain-policy; a real schedule "
                         "always reads the episode's own latest receipt")

    # WHY DID THIS REFUSE? Answer it without spending a single quota unit. This runs the same
    # SHIP_POLICY.evaluate the real path runs a few hundred lines below, prints the same lines,
    # and exits: no token, no upload session, no external write of any kind.
    if args.explain_policy:
        _rp = Path(args.receipt) if args.receipt else None
        if _rp is None:
            _cands = sorted(PKG.glob("acceptance_receipt.v*.json"))
            if not _cands:
                raise SystemExit(f"no acceptance receipt in {PKG}")
            _rp = _cands[-1]
        _rc = json.loads(_rp.read_text("utf-8"))
        _sha = sha(VIDEO) if VIDEO.is_file() else None
        if _sha and _rc.get("video_sha256") not in (None, _sha):
            print(f"WARN receipt sha {_rc.get('video_sha256')} != this video {_sha} -- the real "
                  f"path REFUSES that; this explanation is not bound to these bytes")
        _r = SHIP_POLICY.evaluate(EPDIR, slug, _rc, receipt_path=_rp if _rp.is_relative_to(ROOT)
                                  else None, video_sha=_sha or _rc.get("video_sha256"),
                                  video_path=str(VIDEO), dry_run=True)
        print(f"[policy] episode={EP} receipt={_rp.name} status={_rc.get('status')} "
              f"hard_failures={len(_rc.get('hard_failures') or [])}")
        SHIP_POLICY.print_decision(_r)
        print("EXPLAIN_ONLY no external reads or writes performed")
        return 1 if _r["decision"] == "refuse" else 0

    # A 401 in the middle of the run used to leave the file uploaded but unfinished, and a
    # re-run then uploaded a SECOND copy (EP53 shipped twice on 2026-08-01). Refuse to start
    # when the channel already carries a private video with this exact title.
    #
    # This block was written against a helper that does not exist (`_http_get_json`) and an
    # index expression using bare names (`_it[id][videoId]`), and the broad `except` turned
    # both into a printed note -- so from the day it was added the guard never ran once.
    # It now uses urllib directly, and a pre-check that CANNOT be completed stops the upload
    # instead of waving it through: not knowing whether a duplicate exists is not the same as
    # knowing there is none.
    def _search_mine(tok: str) -> dict:
        _req = urllib.request.Request(
            "https://www.googleapis.com/youtube/v3/search?part=snippet&forMine=true"
            "&type=video&maxResults=50&order=date",
            headers={"Authorization": f"Bearer {tok}"})
        with urllib.request.urlopen(_req, timeout=60) as _r:
            return json.loads(_r.read().decode("utf-8"))

    _mine, _last = None, None
    for _attempt in range(3):
        try:
            _mine = _search_mine(_fresh_token())
            break
        except Exception as _e:
            _last = _e
            time.sleep(3 * (_attempt + 1))
    if _mine is None:
        raise SystemExit(
            f"duplicate pre-check could not run ({str(_last)[:120]}). Refusing to upload -- "
            f"re-run when the API is reachable, or check the channel by hand first.")
    for _it in _mine.get("items", []):
        if _it["snippet"]["title"].strip() == cfg["title"].strip():
            _vid = _it["id"]["videoId"]
            # A RE-RENDER IS NOT A DUPLICATE -- but only if the old one is really standing down.
            if getattr(args, "replaces", None) == _vid:
                _st = get_state(_fresh_token(), _vid)
                _items = (_st or {}).get("items") or []
                if not _items:
                    raise SystemExit(f"--replaces {_vid}: no such video on this channel")
                _s = _items[0].get("status") or {}
                if _s.get("privacyStatus") != "private" or _s.get("publishAt"):
                    raise SystemExit(
                        f"--replaces {_vid}: it is {_s.get('privacyStatus')} with "
                        f"publishAt={_s.get('publishAt')}. Take it off the calendar first "
                        f"(scripts/pause_schedule.py --video {_vid}) -- otherwise both copies "
                        f"publish, which is the accident this guard exists to stop.")
                print(f"OK supersede: {_vid} is private with no publishAt; uploading the "
                      f"corrected render in its place")
                break
            raise SystemExit(
                f"REFUSING duplicate: {_vid} already carries this exact title. "
                f"Finish it with scripts/finalize_uploaded_video.py instead of uploading again, "
                f"or -- if this is a corrected re-render and {_vid} is already off the calendar "
                f"-- re-run with --replaces {_vid}.")
    print(f"OK duplicate pre-check: no existing video titled {cfg['title'][:48]!r}")

    if RESULT.exists():
        # A RECEIPT IS EVIDENCE OF AN UPLOAD, NOT PROOF THAT THE UPLOAD IS STILL THERE.
        # 2026-08-16: every private long-form on the channel was deleted inside 25 minutes by
        # something outside this machine. memphis and marmet were left with eight receipts naming
        # seven video ids, and videos.list returned an empty item array for ALL SEVEN. The guard
        # then refused to re-upload two finished, permitted films to protect videos that no
        # longer existed. Nothing is weakened here: the refusal stands the moment ANY receipt
        # names a video the channel still has, and the title pre-check above independently
        # refuses a live duplicate. This only supplies the fact the guard was missing.
        _prior = sorted(PKG.glob("youtube_schedule_result.v*.json"))
        _ids: list[str] = []
        for _p in _prior:
            try:
                _ids.append(json.loads(_p.read_text(encoding="utf-8")).get("video_id") or "")
            except Exception:
                _ids.append("")
        _tok = _fresh_token()
        _still = [v for v in dict.fromkeys(i for i in _ids if i)
                  if ((get_state(_tok, v) or {}).get("items") or [])]
        if _still:
            raise RuntimeError(
                f"Refusing duplicate: {RESULT} exists and {_still[0]} is still on the channel. "
                f"Finish it with scripts/finalize_uploaded_video.py, or take it off the calendar "
                f"and re-run with --replaces {_still[0]}.")
        _n = 2
        while (PKG / f"youtube_schedule_result.v{_n:03d}.json").exists():
            _n += 1
        RESULT = PKG / f"youtube_schedule_result.v{_n:03d}.json"
        print(f"[receipt] {len(_prior)} prior receipt(s) name {len([i for i in _ids if i])} video "
              f"id(s) and NONE of them is on the channel any more -- they record uploads that were "
              f"deleted. Writing a new receipt {RESULT.name}; the old ones are kept as the record "
              f"of what was uploaded and lost.")
    for p in (VIDEO, THUMB, CAPS, DELIVERY):
        if not p.exists():
            raise RuntimeError(f"missing {p}")
    delivery = json.loads(DELIVERY.read_text("utf-8"))
    want = delivery["canonical_final"]["video_sha256"]
    got = sha(VIDEO)
    if got != want:
        raise RuntimeError(f"VIDEO hash != final_delivery canonical: {got} vs {want}")
    if THUMB.stat().st_size >= 2 * 1024 * 1024:
        raise RuntimeError("thumbnail >= 2MB")

    # QUOTA CHECK BEFORE THE 1,600-UNIT SPEND.
    # On 2026-08-03 the day's 10,000 units went on 42 playlist placements, chapter and link
    # edits on the same 42 descriptions, and two uploads. The third died mid-transfer on a bare
    # "403 exceeded your quota" -- after the gate had passed and the approval was written, and
    # it left a metadata-only shell video on the channel that had to be found and deleted by
    # hand. Nothing warned first, because nothing was counting.
    _checker = ROOT / "scripts" / "check_api_budget.py"
    if _checker.is_file():
        # encoding is pinned. `text=True` alone decodes with the LOCALE codec, which is cp932 on
        # this machine: on 2026-08-14 a single non-ASCII byte in a child's output raised
        # UnicodeDecodeError here and killed greene's upload run between "uploaded" and
        # "publishAt set". The episode then sat private with no date and missed its 08-16 slot.
        _b = subprocess.run([sys.executable, str(_checker), "--need", "1"],
                            capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        for _line in (_b.stdout or "").splitlines():
            if _line.startswith("[budget]"):
                print(_line)
        if _b.returncode != 0:
            raise SystemExit(
                "refusing to start an upload the day's quota cannot finish. Wait for the reset, "
                "or upload through the browser -- that costs no quota at all.")

    # NOTHING THIS EPISODE FORBIDS IS ACTUALLY ON SCREEN -- MEASURED ON THIS RENDER'S PIXELS.
    # check_spec_satisfied.py already compares forbidden_subjects against cut FILENAMES, and
    # the archive's filenames lie in both directions: EP56 shipped a red London bus at 9:25
    # into a film whose highest constraint forbids bus imagery (a sub-postmaster died under
    # one), and EP61's motorbike rider reached the finished master inside a clip named
    # lone_tree_in_field. A filename check cannot see a bus, and a contact sheet built from one
    # frame per clip is not a review of a clip -- EP62 measured every Wan invention in the last
    # 1-3 seconds of its shot. check_shipped_frames.py samples several frames per cut OUT OF
    # THIS FILE, weighted toward the end of each cut, tiles them into labelled sheets, and
    # refuses to go green until somebody has read the sheets and recorded a verdict bound to
    # these exact bytes. An unread sheet is not a pass.
    _frames = ROOT / "scripts" / "check_shipped_frames.py"
    if _frames.is_file():
        _fr = subprocess.run([sys.executable, str(_frames), "--slug", slug,
                              "--render", str(VIDEO)], capture_output=True, text=True,
                             encoding="utf-8", errors="replace")  # see the cp932 note above
        _out = (_fr.stdout or "") + (_fr.stderr or "")
        for _line in _out.splitlines():
            if _line.startswith("[shipped-frames]") or _line.startswith("  - "):
                print(_line)
        if _fr.returncode != 0:
            _named = [_l.strip() for _l in _out.splitlines()
                      if "REJECTED at" in _l or _l.strip().startswith("- ")]
            raise SystemExit(
                "refusing to upload: the shipped-frame review of THIS render is not green. "
                + (" | ".join(_named) if _named else _out.strip()[-500:])
                + f"  Full record: runs/qc/{slug}_shipped_frames.v001.json")

    # HARD LOCK: no upload without an acceptance receipt bound to THIS render's bytes.
    # A video that did not go through scripts/check_final_acceptance.py --emit-receipt still
    # physically cannot be scheduled, and a receipt for other bytes is still refused. That part
    # is correctness and it is unchanged.
    #
    # WHAT CHANGED (owner directive, config/ship_policy.v001.json, 2026-08-12). The old rule was
    # "every hard failure blocks unless it is runtime_band or is named in an approval". Five days
    # of that produced zero scheduled uploads: of the seven reasons raised on 2026-08-11, ONE was
    # a genuine risk and six were craft rules. The rule is now "a failure blocks only if it maps
    # to one of the four blocking classes -- real-person likeness, rights, factual support,
    # fabricated record". Everything else ships AND IS WRITTEN DOWN, with its number, in
    # 09_package/release_deviations.v{NNN}.json.
    #
    # This is not a weakened gate. check_final_acceptance still runs every check and still writes
    # every failure into the receipt; no threshold moved. The DECISION moved here, where it is
    # visible in a diff, and the release record is the honest counterpart: nothing is waived
    # silently. The owner's per-episode approval mechanism still exists and is now the ONLY way
    # past a blocking class.
    #
    # Use the LATEST acceptance receipt (consistent with how thumbnail/delivery are globbed above).
    # Episodes that needed several render iterations have receipts v001..vNN; the final one is
    # the latest. The sha==video check below still fully binds it to THIS render.
    _rcs = sorted(PKG.glob("acceptance_receipt.v*.json"))
    receipt = _rcs[-1] if _rcs else PKG / "acceptance_receipt.v001.json"
    if not receipt.exists():
        raise RuntimeError(
            f"no acceptance receipt {receipt} -- run "
            f"`check_final_acceptance.py {EP} --render {VIDEO} --emit-receipt` first")
    rc = json.loads(receipt.read_text("utf-8"))
    if rc.get("video_sha256") != got:
        raise RuntimeError(f"receipt is for a different render (receipt sha {rc.get('video_sha256')} "
                           f"!= this video {got}); re-run the gate on THIS file")
    _release = SHIP_POLICY.evaluate(EPDIR, slug, rc, receipt_path=receipt, video_sha=got,
                                    video_path=str(VIDEO), dry_run=bool(args.dry_run))
    SHIP_POLICY.print_decision(_release)
    if _release["decision"] == "refuse":
        _named = "; ".join(f"{r['check']} [class={r['class']}]"
                           for r in _release["blocking_failures"])
        raise SystemExit(
            f"REFUSING to schedule {EP}: {len(_release['blocking_failures'])} blocking-class "
            f"failure(s) -> {_named}. These are ban/legal risk, not craft: fix the film (splice "
            f"the affected range, `scripts/pd_splice_cuts.py`) and re-emit the receipt, or -- if "
            f"the owner knowingly accepts one -- record it in episodes/{EP}/approvals/*.json "
            f"(target_type 'edit', decision 'approved', the check id in accepted_deviations). "
            f"Advisory failures are NOT the reason this stopped.")
    # The honest counterpart to the relaxed gate: what shipped with a red number on it, and what
    # that number was. Written BEFORE the upload starts, so an upload that dies mid-transfer
    # still leaves the record of what was permitted.
    _relpath = SHIP_POLICY.write_release_record(EPDIR, _release)
    print(f"OK release record -> {_relpath.relative_to(ROOT)} "
          f"({len(_release['deviations'])} advisory deviation(s) recorded, "
          f"{len(_release['detector_gaps'])} detector gap(s) noted)")
    print(f"OK {EP}: title={cfg['title']!r}")
    print(f"OK video={VIDEO.name} {VIDEO.stat().st_size/1e6:.0f}MB sha_ok=True")
    print(f"OK thumb={THUMB.name} caps={CAPS.name}")
    # 2026-08-09: norfolk carried a stale 08-07 date; a PAST publishAt makes YouTube publish the
    # upload IMMEDIATELY and publicly (measured: H8j_K1x9Dog). Refuse it here so even a dry-run fails.
    if datetime.fromisoformat(cfg["sched_utc"].replace("Z", "+00:00")) <= datetime.now(timezone.utc):
        raise RuntimeError(f"sched_utc {cfg['sched_utc']} is in the PAST -- YouTube would publish "
                           f"immediately and publicly; fix this episode's date in EPISODES first")
    print(f"OK schedule local={cfg['sched_local']} utc={cfg['sched_utc']} (private + publishAt)")
    if args.dry_run:
        print("DRY_RUN_OK no external writes")
        return 0

    token = _access_token(load_env())
    ch = get_channel_id(token)
    if ch not in CHANNEL_ALLOWLIST:
        raise RuntimeError(f"channel {ch} not allowlisted")
    url = initiate_upload(token, VIDEO.stat().st_size, cfg)
    print(f"OK upload session started; uploading {VIDEO.stat().st_size/1e6:.0f}MB ...")
    vid = resilient_upload(url, token, VIDEO)
    if not vid:
        raise RuntimeError("no video_id")
    print(f"OK uploaded private video_id={vid}")
    token = _fresh_token()   # the upload just spent up to two hours; the old token is dead
    set_thumbnail(token, vid, THUMB); print("OK thumbnail set")
    cap_err = None
    try:
        upload_caption(token, vid, CAPS, slug); print("OK captions uploaded")
    except Exception as e:
        cap_err = str(e); print(f"WARN captions upload failed (burned-in remain): {cap_err}")
    token = _fresh_token()
    # 2026-08-09: read-after-write lag -- a GET fired right after the status update can return
    # publishAt=None for a few seconds even when the schedule stuck (measured on H8j_K1x9Dog:
    # verify None at t+1s, correct at t+8s). Retry the read before declaring failure; a real
    # failure (e.g. a PAST publishAt silently published the video) stays wrong on every read.
    status = {}
    for _attempt in range(3):
        st = get_state(token, vid); status = ((st.get("items") or [{}])[0].get("status") or {})
        if status.get("privacyStatus") == "private" and status.get("publishAt") == cfg["sched_utc"]:
            break
        time.sleep(10)
    if status.get("privacyStatus") != "private" or status.get("publishAt") != cfg["sched_utc"]:
        raise RuntimeError(f"verify failed privacy={status.get('privacyStatus')} publishAt={status.get('publishAt')}")
    res = {"schema_version": "1.0.0", "episode_id": EP, "mode": "scheduled", "video_id": vid,
           "watch": f"https://youtu.be/{vid}", "studio": f"https://studio.youtube.com/video/{vid}/edit",
           "channel_id": ch, "privacy": "private", "publishAt": status.get("publishAt"),
           "scheduled_at_local": cfg["sched_local"], "title": cfg["title"], "video_sha256": got,
           "thumbnail_sha256": sha(THUMB), "thumbnail_set": True, "captions_uploaded": cap_err is None,
           "caption_error": cap_err, "public_immediate_publish": False, "external_upload": True,
           "owner_instruction": "順番ずつ予約投稿しよう (2026-07-04)", "scheduled_at": datetime.now(timezone.utc).isoformat()}
    RESULT.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(f"RESULT {RESULT.relative_to(ROOT)}")
    print(f"WATCH https://youtu.be/{vid}  SCHEDULED {cfg['sched_local']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
