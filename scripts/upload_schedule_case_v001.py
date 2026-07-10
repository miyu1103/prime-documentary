#!/usr/bin/env python3
"""Upload a PD case episode privately and schedule its public release (private + publishAt).

Generic, config-driven version of upload_schedule_kyllo_v001.py (--ep katz|rodriguez).
Reuses the exact same resilient resumable uploader, thumbnail/caption set, hash guard, and
duplicate-refusal. Owner approved sequential scheduling 2026-07-04 ("順番ずつ予約投稿しよう":
EP25=7/10, EP26 Katz=7/11, EP27 Rodriguez=7/12, all 12:00 JST, private + publishAt).

Usage: python scripts/upload_schedule_case_v001.py --ep katz [--dry-run]
"""
from __future__ import annotations
import argparse, json, mimetypes, ssl, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token
from upload_episode import CHANNEL_ALLOWLIST, get_channel_id, sha256_file, upload_chunks

CONFIG = {
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
        "video": r"H:/pd-media/episodes/PD-2026-028-forfeiture/08_edit/final.v004.mp4",
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
        "video": r"H:/pd-media/episodes/PD-2026-026-katz/08_edit/final.v001.mp4",
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
        "video": r"H:/pd-media/episodes/PD-2026-027-rodriguez/08_edit/final.v001.mp4",
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
    "cotton": {
        "ep": "PD-2026-030-cotton",
        "video": r"H:/pd-media/episodes/PD-2026-030-cotton/08_edit/renders/final.premium.v004.mp4",
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
    args = ap.parse_args(argv)
    cfg = CONFIG[args.ep]
    slug = args.ep
    EP = cfg["ep"]
    EPDIR = ROOT / "episodes" / EP
    PKG = EPDIR / "09_package"
    VIDEO = Path(cfg["video"])
    # use the LATEST selected thumbnail + final_delivery revision (v003 thumb / v004+ delivery)
    _thumbs = sorted(PKG.glob("thumbnail.selected.v*.png"))
    THUMB = _thumbs[-1] if _thumbs else PKG / "thumbnail.selected.v001.png"
    CAPS = EPDIR / "08_edit" / "captions.final.v001.srt"
    _dels = sorted(PKG.glob("final_delivery.v*.json"))
    DELIVERY = _dels[-1] if _dels else PKG / "final_delivery.v001.json"
    RESULT = PKG / "youtube_schedule_result.v001.json"

    if RESULT.exists():
        raise RuntimeError(f"Refusing duplicate: {RESULT} exists")
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
    # HARD LOCK: no upload without a green acceptance receipt bound to THIS render's bytes.
    # A video that did not pass scripts/check_final_acceptance.py --emit-receipt physically
    # cannot be scheduled. runtime_band is the channel-wide owner-accepted documented deviation.
    ALLOWED_DEVIATIONS = {"runtime_band"}
    # PLUS any deviation the owner FORMALLY documented in an APPROVED first-cut/edit acceptance
    # record for THIS episode (approvals/*.json, target_type='edit', decision approved*). This is
    # per-episode and auditable: e.g. EP35's padding is tolerated only because approvals/APR-0002
    # lists it under accepted_deviations -- a future episode with a REAL padding regression and no
    # such approval still hard-fails. A blanket allow-list would defeat the gate.
    for _aprf in sorted((EPDIR / "approvals").glob("*.json")):
        try:
            _apr = json.loads(_aprf.read_text("utf-8"))
        except Exception:
            continue
        if (_apr.get("target_type") == "edit"
                and str(_apr.get("decision", "")).startswith("approved")):
            for _d in _apr.get("accepted_deviations", []):
                if isinstance(_d, str):
                    ALLOWED_DEVIATIONS.add(_d)
    # Use the LATEST acceptance receipt (consistent with how thumbnail/delivery are globbed above).
    # Episodes that needed several render iterations have receipts v001..vNN; the final green one is
    # the latest. The sha==video and no-hard-failure checks below still fully bind it to THIS render,
    # so reading the latest cannot weaken the gate (a stale/FAIL latest receipt is rejected).
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
    bad = [c for c in rc.get("hard_failures", []) if c not in ALLOWED_DEVIATIONS]
    if bad:
        raise RuntimeError(f"acceptance gate NOT green: unresolved hard failures {bad}. "
                           f"Fix them and re-emit the receipt before scheduling.")
    print(f"OK acceptance receipt green (sha match; tolerated={sorted(set(rc.get('hard_failures', [])) & ALLOWED_DEVIATIONS)})")
    print(f"OK {EP}: title={cfg['title']!r}")
    print(f"OK video={VIDEO.name} {VIDEO.stat().st_size/1e6:.0f}MB sha_ok=True")
    print(f"OK thumb={THUMB.name} caps={CAPS.name}")
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
    set_thumbnail(token, vid, THUMB); print("OK thumbnail set")
    cap_err = None
    try:
        upload_caption(token, vid, CAPS, slug); print("OK captions uploaded")
    except Exception as e:
        cap_err = str(e); print(f"WARN captions upload failed (burned-in remain): {cap_err}")
    st = get_state(token, vid); status = ((st.get("items") or [{}])[0].get("status") or {})
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
