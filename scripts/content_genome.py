#!/usr/bin/env python3
"""Build and read the Content Genome -- one DNA record per published long-form.

WHY THIS EXISTS
    config/pd_planning_os.v002.json -> content_genome: "Classifying episodes by theme hides the
    thing that actually predicts performance. Recording each film's DNA lets the winning STRUCTURE
    be transplanted onto a different subject." The hypothesis it wants tested against our own data
    is blunt: *"police" may never have been the reason anything performed; "specific number +
    ordinary person + institutional contradiction" may be.*

    So this tool never groups by theme. It groups by structural feature, and it prints the sample
    size beside every number, because with ~57 public long-forms most cuts cannot support a
    conclusion and saying so is the correct output.

WHAT IS MEASURED AND WHAT IS NOT
    ctr             Studio internal scrape only, fixed 28-day window. The Analytics API has no
                    `impressions` / `impressionClickThroughRate` metric -- probed 2026-08-12, it
                    returns 400 "Unknown identifier". Videos absent from the scrape are
                    "unavailable", never 0.
    rpm             "unavailable" on every row. estimatedRevenue/cpm return 401 "Insufficient
                    permission to access this report" for the token in .env (probed 2026-08-12).
    avd, retention_30s, browse_ratio, suggested_ratio, subs_per_1000
                    YouTube Analytics API, lifetime window. Free of the Data API's 10,000/day
                    quota -- it is a different service with a different allowance.

    The two sentinels are load-bearing and are never interchangeable:
        "unknown"     -- a judgement field we could not determine from the material we hold
        "unavailable" -- a metric no source we have can supply
    Neither is ever replaced with 0 or null. A dataset with honest gaps is usable; one with
    invented values is poison.

QUOTA
    Enumeration goes through scripts/yt_channel_index.py (union of uploads playlist + search;
    the playlist alone silently omits videos). That is ~301 Data API units per cold sweep, cached
    15 minutes, plus 1 unit per 50 ids for videos.list. Every call this tool makes is recorded in
    the ledger via scripts/yt_quota.py. Read-only throughout: no writes to YouTube, ever.

USAGE
    py -3.11 scripts/content_genome.py --build                 # rebuild the jsonl from caches
    py -3.11 scripts/content_genome.py --build --refresh       # re-query YouTube first
    py -3.11 scripts/content_genome.py --report                # the grouped report
    py -3.11 scripts/content_genome.py --report --min-n 8      # only cuts big enough to read

FILES
    data/content_genome.v001.jsonl                  the dataset, one JSON object per video
    data/content_genome_annotations.v001.json       the judgement fields, keyed by episode_id
    schemas/content_genome.v001.json                the record contract
    runs/_cache/content_genome_perf.v001.json       raw analytics responses (refresh with --refresh)
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

OUT_JSONL = ROOT / "data" / "content_genome.v001.jsonl"
ANNOTATIONS = ROOT / "data" / "content_genome_annotations.v001.json"
PERF_CACHE = ROOT / "runs" / "_cache" / "content_genome_perf.v001.json"
CLUSTERS = ROOT / "config" / "distribution" / "series_clusters.v001.json"
STUDIO_CTR = ROOT / "scripts" / "_yt_studio_video_ctr.json"

LONGFORM_MIN_SEC = 186          # same threshold yt_channel_index.py uses: a Short is <= 3 minutes
ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"
LIFETIME_START = "2026-01-01"   # earlier than the channel's first upload (2026-06-16)

# The one link the repo cannot prove from a package file. The Central Park Five film is EP50; its
# video id is recorded only in episodes/_planning/measurements/*.json, never inside the episode
# directory, so it is asserted here with its evidence rather than silently dropped or guessed at
# by title similarity.
MANUAL_EPISODE_LINKS = {
    "_8DaMu8_yFw": (
        "PD-2026-050-centralpark",
        "manual: episodes/_planning/measurements/PINNED_COMMENTS.v001.json ties this id to "
        "'Five Children Confessed to a Crime They Didn't Commit.'; PD-2026-050-centralpark is the "
        "only Central Park Five long-form in episodes/",
    ),
}

UNKNOWN = "unknown"
UNAVAILABLE = "unavailable"


# --------------------------------------------------------------------------- enumeration

def _auth():
    from yt_channel_index import authorize
    return authorize(ROOT)


ENUM_TTL_SEC = 6 * 3600     # see comment in enumerate_channel


def enumerate_channel(*, ttl: int = ENUM_TTL_SEC) -> tuple[list[dict], str]:
    """Every public long-form on the channel, from the audited union index.

    The cache TTL is six hours rather than yt_channel_index's default fifteen minutes, and the
    reason is measured: building this dataset is an iterative activity -- annotate, rebuild, look,
    fix, rebuild -- and each cold sweep costs ~405 Data API units (4 search pages at 100 each,
    plus the playlist pages and channels.list). Four rebuilds inside an hour at the default TTL
    burned roughly 810 units on re-reading a video list that had not changed. --refresh is there
    for when freshness actually matters.

    yt_channel_index does NOT record its own search.list/playlistItems.list spend, so this
    function records it. A sweep that is served from cache spends nothing and records nothing.
    """
    from yt_channel_index import list_video_ids, fetch_videos, iso_seconds, CACHE
    import yt_quota
    import time as _time

    before = CACHE.stat().st_mtime if CACHE.exists() else 0
    auth = _auth()
    ids = list_video_ids(auth, ttl=ttl)
    was_cold = not CACHE.exists() or CACHE.stat().st_mtime > before
    vids = fetch_videos(auth, ids)
    yt_quota.record("videos.list", (len(ids) + 49) // 50)
    if was_cold:
        pages = (len(ids) + 49) // 50
        yt_quota.record("search.list", pages)
        yt_quota.record("playlistItems.list", pages)
        yt_quota.record("channels.list")
    rows = []
    for v in vids.values():
        dur = iso_seconds(v["contentDetails"]["duration"])
        if dur < LONGFORM_MIN_SEC or v["status"]["privacyStatus"] != "public":
            continue
        rows.append({
            "video_id": v["id"],
            "title": v["snippet"]["title"],
            "published_at": v["snippet"]["publishedAt"],
            "duration_sec": dur,
        })
    rows.sort(key=lambda r: r["published_at"])
    note = (f"scripts/yt_channel_index.py union (uploads playlist + search.list); "
            f"{len(ids)} ids on channel, {len(rows)} public long-forms >= {LONGFORM_MIN_SEC}s")
    return rows, note


def episode_links() -> dict[str, tuple[str, str]]:
    """video_id -> (episode_id, the file that proves it)."""
    out: dict[str, tuple[str, str]] = {}
    if CLUSTERS.exists():
        d = json.loads(CLUSTERS.read_text(encoding="utf-8"))
        for pl in d.get("playlists", []):
            for o in pl.get("order", []):
                if o.get("video_id") and o.get("episode"):
                    out[o["video_id"]] = (o["episode"], str(CLUSTERS.relative_to(ROOT)).replace("\\", "/"))
    for p in sorted(ROOT.glob("episodes/PD-*/09_package/*.json")) + \
            sorted(ROOT.glob("episodes/PD-*/events/*.json")):
        if "short" in p.name.lower():
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        vid = d.get("video_id") or d.get("videoId")
        if isinstance(vid, str) and vid and vid not in out:
            out[vid] = (p.parts[len(ROOT.parts) + 1], str(p.relative_to(ROOT)).replace("\\", "/"))
    for vid, (ep, why) in MANUAL_EPISODE_LINKS.items():
        out.setdefault(vid, (ep, why))
    return out


def series_clusters() -> dict[str, str]:
    if not CLUSTERS.exists():
        return {}
    d = json.loads(CLUSTERS.read_text(encoding="utf-8"))
    return {o["video_id"]: pl["key"] for pl in d.get("playlists", []) for o in pl.get("order", [])}


# --------------------------------------------------------------------------- performance

def _analytics_token() -> str:
    from pd_factory.providers import load_env
    from pd_factory.providers.youtube import _access_token
    return _access_token(load_env())


def _aq(tok: str, **params) -> tuple[int, dict]:
    params.setdefault("ids", "channel==MINE")
    req = urllib.request.Request(ANALYTICS + "?" + urllib.parse.urlencode(params),
                                 headers={"Authorization": f"Bearer {tok}"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return 200, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}


def fetch_performance(video_ids: list[str], *, end: str | None = None) -> dict:
    """Query the Analytics API for everything the genome needs. Costs no Data API quota."""
    tok = _analytics_token()
    end = end or date.today().isoformat()
    out = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "window": f"{LIFETIME_START}..{end} (lifetime: channel's first upload is 2026-06-16)",
        "per_video": {}, "retention": {}, "traffic": {}, "probes": {},
    }

    st, r = _aq(tok, startDate=LIFETIME_START, endDate=end, dimensions="video", maxResults=200,
                sort="-views",
                metrics="views,estimatedMinutesWatched,averageViewDuration,"
                        "averageViewPercentage,subscribersGained,subscribersLost")
    if st != 200:
        raise SystemExit(f"per-video analytics failed: HTTP {st} {r}")
    cols = [h["name"] for h in r["columnHeaders"]]
    for row in r.get("rows", []):
        rec = dict(zip(cols, row))
        out["per_video"][rec["video"]] = rec
    print(f"[perf] per-video lifetime: {len(out['per_video'])} videos", file=sys.stderr)

    # Revenue and impressions are probed once each so the "unavailable" in the dataset is a
    # recorded measurement rather than a belief carried over from memory.
    st_rev, r_rev = _aq(tok, startDate=LIFETIME_START, endDate=end, dimensions="video",
                        maxResults=5, metrics="estimatedRevenue,cpm")
    out["probes"]["revenue"] = {"http": st_rev, "body": str(r_rev)[:300]}
    st_imp, r_imp = _aq(tok, startDate=LIFETIME_START, endDate=end, dimensions="video",
                        maxResults=5, metrics="impressions,impressionClickThroughRate")
    out["probes"]["impressions"] = {"http": st_imp, "body": str(r_imp)[:300]}
    print(f"[perf] probes: revenue HTTP {st_rev}, impressions HTTP {st_imp}", file=sys.stderr)

    for i, vid in enumerate(video_ids, 1):
        st, r = _aq(tok, startDate=LIFETIME_START, endDate=end,
                    dimensions="elapsedVideoTimeRatio",
                    metrics="audienceWatchRatio,relativeRetentionPerformance",
                    filters=f"video=={vid}")
        out["retention"][vid] = r.get("rows", []) if st == 200 else {"http": st}
        st, r = _aq(tok, startDate=LIFETIME_START, endDate=end,
                    dimensions="insightTrafficSourceType", metrics="views",
                    filters=f"video=={vid}")
        out["traffic"][vid] = r.get("rows", []) if st == 200 else {"http": st}
        if i % 10 == 0:
            print(f"[perf] retention+traffic {i}/{len(video_ids)}", file=sys.stderr)

    PERF_CACHE.parent.mkdir(parents=True, exist_ok=True)
    PERF_CACHE.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[perf] written {PERF_CACHE.relative_to(ROOT)}", file=sys.stderr)
    return out


def retention_at(curve, duration_sec: int, seconds: float = 30.0):
    """audienceWatchRatio interpolated at `seconds` into the video.

    The API reports on a 0.01 grid of elapsedVideoTimeRatio, so 30s in a 1,700s film falls between
    two published points; taking the nearest one would quantise a 17-second error into the number.
    """
    if not isinstance(curve, list) or not curve or duration_sec <= 0:
        return UNAVAILABLE
    target = seconds / duration_sec
    pts = sorted((float(p[0]), float(p[1])) for p in curve if len(p) >= 2)
    if target <= pts[0][0]:
        return pts[0][1]
    if target >= pts[-1][0]:
        return pts[-1][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= target <= x1:
            if x1 == x0:
                return y0
            return y0 + (y1 - y0) * (target - x0) / (x1 - x0)
    return UNAVAILABLE


def traffic_ratios(rows):
    if not isinstance(rows, list) or not rows:
        return UNAVAILABLE, UNAVAILABLE
    total = sum(float(r[1]) for r in rows)
    if total <= 0:
        return UNAVAILABLE, UNAVAILABLE
    by = {r[0]: float(r[1]) for r in rows}
    return (round(by.get("BROWSE_FEATURES", 0.0) / total, 4),
            round(by.get("RELATED_VIDEO", 0.0) / total, 4))


def studio_ctr() -> dict[str, dict]:
    if not STUDIO_CTR.exists():
        return {}
    d = json.loads(STUDIO_CTR.read_text(encoding="utf-8"))
    return {r["video_id"]: r for r in d.get("rows", [])}


# --------------------------------------------------------------------------- mechanical fields

IRREGULAR = {
    "took", "gave", "held", "kept", "found", "told", "sold", "paid", "hid", "drove", "wrote",
    "ran", "sat", "left", "came", "went", "made", "said", "drew", "swore", "spent", "sent",
    "built", "broke", "brought", "bought", "caught", "chose", "dove", "fell", "felt", "got",
    "had", "heard", "knew", "lost", "met", "saw", "shot", "stood", "struck", "taught", "thought",
    "threw", "understood", "won", "wore", "blew", "began", "dug", "forgot", "froze", "grew",
    "laid", "lay", "rose", "shook", "sang", "sank", "spoke", "stole", "swam", "tore", "woke",
    "read", "cut", "put", "let", "set", "hit", "beat", "cost", "ran",
    # past participles that carry the sentence in a passive title
    "written", "taken", "given", "seen", "done", "known", "driven", "stolen", "broken",
    "forgotten", "hidden", "shown", "thrown", "gone", "worn", "paid",
}
PRESENT = {
    "invents", "reports", "carry", "carries", "takes", "keeps", "holds", "says", "finds",
    "fights", "runs", "sells", "hangs", "dive", "dives", "goes", "confess", "confesses",
    "clear", "clears", "calls", "wins", "pays", "opens", "files", "sues", "dies", "die",
}
NOT_A_VERB = {
    # -ed words that are adjectives or nouns in these titles
    "blurred", "wanted", "armed", "aged", "red", "sacred", "hundred", "bed", "need",
    "indeed", "instead", "ted", "wed", "united", "advanced", "limited", "deed", "seed", "weed",
    "reed", "shed", "greed", "speed", "creed", "breed", "freed",
}


def title_verb(title: str) -> str:
    """Head verb of the title, or 'unknown'. Mechanical, lexicon-driven and auditable.

    The first sentence is tried first because PD titles are Subject + Verb + Object; only if it
    contains no verb at all (a title like '6 Trials. 4 Death Sentences. 23 Years.' genuinely has
    none) does it fall through to the rest of the title, and then to 'unknown'. A lexicon miss is
    reported by --build rather than papered over -- a wrong verb is worse than a missing one.
    """
    def scan(text: str) -> str | None:
        for t in text.split():
            low = t.strip(".,:;!?—–-'’\"").lower()
            if not low or low in NOT_A_VERB:
                continue
            if low in IRREGULAR or low in PRESENT:
                return low
            if len(low) >= 4 and low.endswith("ed") and low.isalpha():
                return low
        return None

    parts = re.split(r"(?<=[.!?])\s+", title.strip())
    return scan(parts[0]) or scan(title) or UNKNOWN


MONEY = re.compile(r"[$£€]\s?[\d,]+|\b\d[\d,]*\s?(?:million|billion|dollars?)\b", re.I)
DIGIT = re.compile(r"\d")


def title_flags(title: str) -> tuple[bool, bool]:
    return bool(DIGIT.search(title)), bool(MONEY.search(title))


# --------------------------------------------------------------------------- build

GENOME_JUDGEMENT_FIELDS = [
    "protagonist_type", "system", "contradiction", "stakes", "emotion_arc", "ending_emotion",
    "hook_type", "evidence_type", "structure", "title_archetype", "thumbnail_kind", "instincts",
]


def build(refresh: bool) -> int:
    rows, enum_note = enumerate_channel(ttl=0 if refresh else 900)
    links = episode_links()
    clusters = series_clusters()
    ann_doc = json.loads(ANNOTATIONS.read_text(encoding="utf-8")) if ANNOTATIONS.exists() else {}
    ann = {a["episode_id"]: a for a in ann_doc.get("annotations", [])}

    if refresh or not PERF_CACHE.exists():
        perf = fetch_performance([r["video_id"] for r in rows])
    else:
        perf = json.loads(PERF_CACHE.read_text(encoding="utf-8"))
        print(f"[build] performance from cache {PERF_CACHE.relative_to(ROOT)} "
              f"({perf.get('captured_at')})", file=sys.stderr)

    ctr_rows = studio_ctr()
    rev_unavailable = perf.get("probes", {}).get("revenue", {}).get("http") != 200
    records, missing_ann, unknown_verbs = [], [], []

    for r in rows:
        vid = r["video_id"]
        ep, ep_src = links.get(vid, (UNKNOWN, "unlinked: no package file names this video id"))
        a = ann.get(ep, {})
        if not a:
            missing_ann.append(f"{ep}/{vid}")
        pv = perf.get("per_video", {}).get(vid, {})
        views = pv.get("views")
        subs = pv.get("subscribersGained")
        c = ctr_rows.get(vid)
        tv = title_verb(r["title"])
        if tv == UNKNOWN:
            unknown_verbs.append(r["title"])
        has_num, has_money = title_flags(r["title"])
        browse, sugg = traffic_ratios(perf.get("traffic", {}).get(vid))

        genome = {
            "protagonist_type": a.get("protagonist_type", UNKNOWN),
            "system": a.get("system", UNKNOWN),
            "system_secondary": a.get("system_secondary"),
            "contradiction_present": a.get("contradiction_present", UNKNOWN),
            "contradiction": a.get("contradiction", "") or ("" if a else UNKNOWN),
            "contradiction_quote": a.get("contradiction_quote", ""),
            "stakes": a.get("stakes", [UNKNOWN]),
            "emotion_arc": a.get("emotion_arc", UNKNOWN),
            "ending_emotion": a.get("ending_emotion", UNKNOWN),
            "hook_type": a.get("hook_type", UNKNOWN),
            "hook_quote": a.get("hook_quote", ""),
            "evidence_type": a.get("evidence_type", [UNKNOWN]),
            "structure": a.get("structure", UNKNOWN),
            "title_verb": tv,
            "title_archetype": a.get("title_archetype", UNKNOWN),
            "title_has_number": has_num,
            "title_has_money": has_money,
            "thumbnail_kind": a.get("thumbnail_kind", UNKNOWN),
            "thumbnail_text": a.get("thumbnail_text", ""),
            "thumbnail_face": a.get("thumbnail_face", UNKNOWN),
            # v002 assigns a role at the premise stage; nothing published predates that rule with
            # a role on file, so claiming one here would be invention.
            "video_role": UNKNOWN,
            "instincts": a.get("instincts", [UNKNOWN]),
            "series_id": clusters.get(vid, UNKNOWN),
            "annotation_confidence": a.get("confidence", UNKNOWN),
            "annotation_notes": a.get("notes", ""),
        }

        performance = {
            "ctr": c["VIDEO_THUMBNAIL_IMPRESSIONS_VTR"] if c and c.get("VIDEO_THUMBNAIL_IMPRESSIONS_VTR") is not None else UNAVAILABLE,
            "ctr_impressions": c["VIDEO_THUMBNAIL_IMPRESSIONS"] if c else UNAVAILABLE,
            "ctr_window": "studio_internal_28d" if c else UNAVAILABLE,
            "avd": pv.get("averageViewPercentage", UNAVAILABLE),
            "average_view_duration_sec": pv.get("averageViewDuration", UNAVAILABLE),
            "retention_30s": retention_at(perf.get("retention", {}).get(vid), r["duration_sec"]),
            "browse_ratio": browse,
            "suggested_ratio": sugg,
            "subs_per_1000": round(subs / views * 1000, 3) if views else UNAVAILABLE,
            # Kept as a probed fact rather than an assumption: if a monetary-scope token ever
            # exists, this stops being a constant without anyone having to remember to change it.
            "rpm": UNAVAILABLE if rev_unavailable else pv.get("rpm", UNAVAILABLE),
            "views": views if views is not None else UNAVAILABLE,
            "subscribers_gained": subs if subs is not None else UNAVAILABLE,
            "estimated_minutes_watched": pv.get("estimatedMinutesWatched", UNAVAILABLE),
            "window": perf.get("window", UNKNOWN),
            "captured_at": perf.get("captured_at", UNKNOWN),
        }

        unknown_fields = [k for k in GENOME_JUDGEMENT_FIELDS
                          if genome.get(k) == UNKNOWN or genome.get(k) == [UNKNOWN]
                          or (k == "contradiction" and genome["contradiction_present"] is not True)]
        if genome["title_verb"] == UNKNOWN:
            unknown_fields.append("title_verb")
        if genome["series_id"] == UNKNOWN:
            unknown_fields.append("series_id")
        unknown_fields.append("video_role")
        unavailable = [k for k, v in performance.items() if v == UNAVAILABLE]

        records.append({
            "schema_version": "1.0.0",
            "video_id": vid,
            "episode_id": ep,
            "title": r["title"],
            "published_at": r["published_at"],
            "duration_sec": r["duration_sec"],
            "genome": genome,
            "performance": performance,
            "provenance": {
                "episode_link": ep_src,
                "annotation_source": a.get("_source", "none: episode not annotated"),
                "narration_source": a.get("_narration_source"),
                "enumeration": enum_note,
                "unknown_fields": sorted(set(unknown_fields)),
                "unavailable_metrics": sorted(unavailable),
            },
        })

    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSONL.open("w", encoding="utf-8", newline="\n") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"wrote {len(records)} records -> {OUT_JSONL.relative_to(ROOT)}")
    if missing_ann:
        print(f"  {len(missing_ann)} videos with no annotation row (all judgement fields "
              f"'unknown'): {', '.join(missing_ann[:8])}")
    if unknown_verbs:
        print(f"  title_verb 'unknown' on {len(unknown_verbs)} titles (lexicon miss, not a guess):")
        for t in unknown_verbs:
            print(f"      {t[:88]}")
    return 0


# --------------------------------------------------------------------------- annotations

def merge_annotations(src_dir: Path, bundle_index: Path | None, spec: str) -> int:
    """Fold per-batch annotation files into data/content_genome_annotations.v001.json.

    The judgement fields live in their own file rather than inside --build for one reason: --build
    re-queries YouTube and must be re-runnable at any time, and a rebuild that silently discarded
    hand-read judgements would be the fastest possible way to end up with a dataset nobody trusts.
    """
    narr = {}
    if bundle_index and bundle_index.exists():
        for b in json.loads(bundle_index.read_text(encoding="utf-8")):
            narr[b["episode_id"]] = b.get("narration_source")
    rows, seen = [], {}
    for p in sorted(src_dir.glob("*.json")):
        for a in json.loads(p.read_text(encoding="utf-8")):
            ep = a["episode_id"]
            if ep in seen:
                raise SystemExit(f"{ep} annotated twice: {seen[ep]} and {p.name}")
            seen[ep] = p.name
            a["_source"] = f"annotated by read of narration + live thumbnail ({p.name})"
            a["_narration_source"] = narr.get(ep)
            rows.append(a)
    doc = {
        "schema_version": "1.0.0",
        "artifact_type": "content_genome_annotations",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "method": spec,
        "rule": "Every field may be 'unknown'. Quotes are verbatim from the narration so a later "
                "reader can check an annotation instead of trusting it. No field was filled to "
                "make a row look complete.",
        "annotations": sorted(rows, key=lambda a: a["episode_id"]),
    }
    ANNOTATIONS.parent.mkdir(parents=True, exist_ok=True)
    ANNOTATIONS.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"merged {len(rows)} annotations -> {ANNOTATIONS.relative_to(ROOT)}")
    return 0


# --------------------------------------------------------------------------- statistics

def _num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def mann_whitney_p(a: list[float], b: list[float]) -> float | None:
    """Two-sided Mann-Whitney U with a normal approximation and tie correction.

    Deliberately hand-rolled: this repo has no scipy pin, and a missing dependency that silently
    turns into "no p-value" would read as "no difference".
    """
    na, nb = len(a), len(b)
    if na < 3 or nb < 3:
        return None
    allv = sorted([(v, 0) for v in a] + [(v, 1) for v in b])
    ranks, i = [0.0] * len(allv), 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1][0] == allv[i][0]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[k] = r
        i = j + 1
    ra = sum(rk for rk, (_, g) in zip(ranks, allv) if g == 0)
    u_a = ra - na * (na + 1) / 2
    mu = na * nb / 2
    ties = {}
    for v, _ in allv:
        ties[v] = ties.get(v, 0) + 1
    n = na + nb
    tie_term = sum(t ** 3 - t for t in ties.values())
    sd = math.sqrt(na * nb / 12 * ((n + 1) - tie_term / (n * (n - 1)))) if n > 1 else 0
    if sd == 0:
        return None
    z = (abs(u_a - mu) - 0.5) / sd
    return 2 * 0.5 * math.erfc(z / math.sqrt(2))


def cliffs_delta(a: list[float], b: list[float]) -> float:
    gt = sum(1 for x in a for y in b if x > y)
    lt = sum(1 for x in a for y in b if x < y)
    return (gt - lt) / (len(a) * len(b)) if a and b else 0.0


def n_needed(a: list[float], b: list[float]) -> int | None:
    """Per-group n for 80% power at alpha .05 given the observed standardised difference."""
    if len(a) < 2 or len(b) < 2:
        return None
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    va = sum((x - ma) ** 2 for x in a) / (len(a) - 1)
    vb = sum((x - mb) ** 2 for x in b) / (len(b) - 1)
    sp = math.sqrt((va + vb) / 2)
    if sp == 0:
        return None
    d = abs(ma - mb) / sp
    if d < 0.01:
        return None
    return int(math.ceil(16 / d ** 2))


METRICS = [
    ("ctr", "CTR % (28d)", 2),
    ("avd", "APV %", 1),
    ("retention_30s", "ret@30s", 3),
    ("subs_per_1000", "subs/1k", 2),
    ("views", "views", 0),
]

# Two floors, both measured rather than chosen for taste.
#
# CTR_IMPRESSION_FLOOR: a 4.55% CTR on 66 impressions (EP57 fieldtest, 2026-08-11) is three clicks.
# Below a few hundred impressions the figure moves by whole percentage points on one click.
#
# VIEWS_FLOOR: averageViewPercentage and audienceWatchRatio are averages over the video's views.
# The median public long-form on this channel has ELEVEN lifetime views. An APV computed over 11
# views is one person's viewing session, and a curve drawn through it is decoration. Rows below the
# floor are excluded from these three metrics -- not zeroed, excluded, and counted out loud.
CTR_IMPRESSION_FLOOR = 300
VIEWS_FLOOR = 30
VIEW_GATED = {"avd", "retention_30s", "subs_per_1000"}


def metric_values(recs: list[dict], key: str) -> list[float]:
    out = []
    for r in recs:
        v = _num(r["performance"].get(key))
        if v is None:
            continue
        if key == "ctr":
            imp = _num(r["performance"].get("ctr_impressions"))
            if imp is None or imp < CTR_IMPRESSION_FLOOR:
                continue
        if key in VIEW_GATED:
            views = _num(r["performance"].get("views"))
            if views is None or views < VIEWS_FLOOR:
                continue
        out.append(v)
    return out


def _fmt(v, nd):
    return "n/a" if v is None else (f"{v:,.0f}" if nd == 0 else f"{v:.{nd}f}")


def group_table(recs: list[dict], label: str, keyfn, min_n: int) -> None:
    groups: dict[str, list[dict]] = {}
    for r in recs:
        k = keyfn(r)
        if k is None:
            continue
        for kk in (k if isinstance(k, list) else [k]):
            groups.setdefault(str(kk), []).append(r)
    print(f"\n### {label}")
    shown = {k: v for k, v in groups.items() if len(v) >= min_n}
    hidden = {k: v for k, v in groups.items() if len(v) < min_n}
    if not shown:
        print(f"    every level has n < {min_n} -- nothing here can be read. "
              f"levels: {', '.join(f'{k}({len(v)})' for k, v in sorted(groups.items()))}")
        return
    head = f"    {'level':<30}{'n':>4}"
    for _, name, _ in METRICS:
        head += f"{name:>14}"
    head += f"{'med dur':>9}{'med age d':>11}"
    print(head)
    today = datetime.now(timezone.utc)
    for k, v in sorted(shown.items(), key=lambda kv: -len(kv[1])):
        line = f"    {k:<30}{len(v):>4}"
        for key, _, nd in METRICS:
            vals = metric_values(v, key)
            cell = (_fmt(median(vals), nd) if vals else "-") + f"({len(vals)})"
            line += f"{cell:>14}"
        durs = [r["duration_sec"] / 60 for r in v]
        ages = [(today - datetime.fromisoformat(r["published_at"].replace("Z", "+00:00"))).days
                for r in v]
        line += f"{median(durs):>8.0f}m{median(ages):>11.0f}"
        print(line)
    if hidden:
        print(f"    below n={min_n}, not shown: "
              f"{', '.join(f'{k}({len(v)})' for k, v in sorted(hidden.items()))}")


# Below this many subscribers across both sides, subs/1k is not a rate, it is a handful of
# individual people spread over a denominator. Ranks will still produce a p-value; it would be a
# lie. The verdict is withheld and the numerator printed instead.
SUBS_NUMERATOR_FLOOR = 30


def contrast(recs: list[dict], label: str, predicate, min_n: int) -> dict[str, int]:
    """A vs not-A on every metric, with p, effect size and the n that would be needed."""
    needs: dict[str, int] = {}
    a = [r for r in recs if predicate(r) is True]
    b = [r for r in recs if predicate(r) is False]
    print(f"\n### {label}")
    print(f"    yes n={len(a)}   no n={len(b)}")
    if min(len(a), len(b)) < 3:
        print("    one side has n < 3 -- no comparison is possible.")
        return needs
    # Raw counts, printed before the rates, because a rate with a big-looking gap on this channel
    # is usually two or three subscribers moving. p-values do not protect against that; seeing the
    # numerator does.
    def totals(g):
        return (sum(_num(r["performance"]["views"]) or 0 for r in g),
                sum(_num(r["performance"]["subscribers_gained"]) or 0 for r in g))
    (va_, sa_), (vb_, sb_) = totals(a), totals(b)
    print(f"    raw totals     yes {va_:,} views / {sa_} subscribers      "
          f"no {vb_:,} views / {sb_} subscribers")
    for key, name, nd in METRICS:
        va, vb = metric_values(a, key), metric_values(b, key)
        if min(len(va), len(vb)) < 3:
            print(f"    {name:<14} n/a (yes={len(va)}, no={len(vb)} usable)")
            continue
        p = mann_whitney_p(va, vb)
        d = cliffs_delta(va, vb)
        need = n_needed(va, vb)
        if need:
            needs[key] = need
        verdict = ("SEPARATES" if p is not None and p < 0.05 else
                   f"cannot separate (need ~{need}/group)" if need else "cannot separate")
        if key == "subs_per_1000" and (sa_ + sb_) < SUBS_NUMERATOR_FLOOR:
            verdict = (f"NO VERDICT -- only {sa_ + sb_} subscribers across both sides; "
                       f"a rate built on that is not a measurement")
        print(f"    {name:<14} yes {_fmt(median(va), nd):>10} (n={len(va):>2})   "
              f"no {_fmt(median(vb), nd):>10} (n={len(vb):>2})   "
              f"p={'n/a' if p is None else f'{p:.3f}'}  delta={d:+.2f}  {verdict}")
    return needs


def spearman(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 4 or len(xs) != len(ys):
        return None

    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        rk = [0] * len(v)
        for pos, i in enumerate(order):
            rk[i] = pos + 1
        return rk
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    d2 = sum((rx[i] - ry[i]) ** 2 for i in range(n))
    return 1 - 6 * d2 / (n * (n * n - 1))


def ctr_scan(recs: list[dict], min_side: int = 8) -> None:
    """Every structural feature against CTR, ranked by p, with the chance-expectation stated.

    CTR is the only metric on this channel with enough sample to test anything, so it gets a
    systematic sweep rather than a hand-picked comparison. Running ~30 tests at alpha .05 produces
    about 1.5 false positives by construction; that arithmetic is printed next to the results so a
    top row is never mistaken for a finding on its own.
    """
    single = ["protagonist_type", "system", "structure", "hook_type", "ending_emotion",
              "thumbnail_kind", "title_archetype", "title_has_number", "title_has_money",
              "thumbnail_face", "series_id"]
    listy = ["stakes", "instincts", "evidence_type"]
    tests = []
    for f in single:
        for lv in sorted({str(r["genome"][f]) for r in recs}):
            a = [r for r in recs if str(r["genome"][f]) == lv]
            b = [r for r in recs if str(r["genome"][f]) != lv]
            tests.append((f"{f}={lv}", a, b))
    for f in listy:
        for lv in sorted({x for r in recs for x in r["genome"][f]}):
            tests.append((f"{f} has {lv}",
                          [r for r in recs if lv in r["genome"][f]],
                          [r for r in recs if lv not in r["genome"][f]]))
    for lo, hi, name in [(0, 780, "runtime <13m"), (780, 1380, "runtime 13-22m"),
                         (1380, 10 ** 9, "runtime >=23m")]:
        tests.append((name, [r for r in recs if lo <= r["duration_sec"] < hi],
                      [r for r in recs if not lo <= r["duration_sec"] < hi]))

    out = []
    for name, a, b in tests:
        va, vb = metric_values(a, "ctr"), metric_values(b, "ctr")
        if min(len(va), len(vb)) < min_side:
            continue
        p = mann_whitney_p(va, vb)
        if p is None:
            continue
        out.append((p, name, median(va), len(va), median(vb), len(vb), cliffs_delta(va, vb)))
    out.sort(key=lambda t: t[0])
    print(f"\n{len(out)} feature-vs-CTR tests with >= {min_side} usable films on each side, "
          f"ranked by p:")
    print(f"    {'feature':<38}{'with':>18}{'without':>18}{'p':>9}{'delta':>8}")
    for p, name, ma, na, mb, nb, d in out:
        print(f"    {name:<38}{f'{ma:.2f} (n={na})':>18}{f'{mb:.2f} (n={nb})':>18}"
              f"{p:>9.4f}{d:>+8.2f}")
    sig = [t for t in out if t[0] < 0.05]
    bonf = 0.05 / max(1, len(out))
    print(f"    {len(sig)} of {len(out)} reach p<0.05; {0.05 * len(out):.1f} are expected by "
          f"chance alone. Only p < {bonf:.4f} (Bonferroni) is safe to quote unaided.")
    for p, name, ma, na, mb, nb, d in out:
        if p < bonf:
            print(f"    -> {name} survives correction (p={p:.5f}), and is the only cut in this "
                  f"dataset that does.")


def report(min_n: int) -> int:
    if not OUT_JSONL.exists():
        raise SystemExit(f"{OUT_JSONL} does not exist -- run --build first")
    recs = [json.loads(l) for l in OUT_JSONL.read_text(encoding="utf-8").splitlines() if l.strip()]
    today = datetime.now(timezone.utc)

    print("=" * 100)
    print("CONTENT GENOME REPORT -- grouped by STRUCTURE, never by theme")
    print("=" * 100)
    print(f"{len(recs)} public long-forms. Performance window: "
          f"{recs[0]['performance']['window'] if recs else 'n/a'}")
    print(f"Captured {recs[0]['performance']['captured_at'] if recs else 'n/a'}")
    print(f"Cells read 'median(n usable)'. CTR is Studio's 28-day window and is only counted "
          f"above {CTR_IMPRESSION_FLOOR} impressions; every other metric is lifetime.")

    views = sorted(v for v in (_num(r["performance"]["views"]) for r in recs) if v is not None)
    print("\n" + "!" * 100)
    print("READ THIS BEFORE ANY NUMBER BELOW: the outcome side of this dataset is nearly empty.")
    print("!" * 100)
    if views:
        print(f"  Lifetime views per public long-form: min {views[0]}, median {median(views):.0f}, "
              f"max {views[-1]}, total {sum(views):,}.")
        print(f"  {sum(1 for v in views if v >= VIEWS_FLOOR)} of {len(recs)} films have reached "
              f"even {VIEWS_FLOOR} views.")
    print(f"  APV, retention@30s and subs/1k are averages over those views, so they are only "
          f"counted above {VIEWS_FLOOR} views:")
    for key, name, _ in METRICS:
        if key == "views":
            continue
        print(f"      {name:<12} usable rows: {len(metric_values(recs, key))} of {len(recs)}")
    print(f"  CTR is the ONLY metric with real sample behind it: impressions run to the thousands "
          f"because YouTube keeps showing these films. It is views, not exposure, that is missing.")
    print(f"  Consequence: no cut of this dataset can currently separate one structure from "
          f"another on watch behaviour. That is a fact about the channel, not about the schema.")

    ages = [(today - datetime.fromisoformat(r["published_at"].replace("Z", "+00:00"))).days
            for r in recs]
    durs = [r["duration_sec"] / 60 for r in recs]
    print(f"\nCONFOUNDS YOU MUST CARRY INTO EVERY LINE BELOW")
    print(f"  age      {min(ages)}-{max(ages)} days since publish (median {median(ages):.0f}). "
          f"Views are not age-adjusted; APV and retention are far less age-sensitive.")
    print(f"  runtime  {min(durs):.0f}-{max(durs):.0f} min (median {median(durs):.0f}). "
          f"Runtime moved with the calendar -- the 11-min films are the early ones and the "
          f"27-30 min films are recent, so 'structure' and 'era' are partly the same variable.")
    n_unav = {}
    for r in recs:
        for k in r["provenance"]["unavailable_metrics"]:
            n_unav[k] = n_unav.get(k, 0) + 1
    print(f"  gaps     " + ", ".join(f"{k}={v}" for k, v in sorted(n_unav.items())) +
          "  (out of %d rows)" % len(recs))

    print("\n" + "=" * 100)
    print("PART 1 -- THE OWNER'S HYPOTHESIS: was it ever 'police'?")
    print("=" * 100)

    def is_police(r):
        g = r["genome"]
        if g["system"] == UNKNOWN:
            return None
        return g["system"] in ("police", "prosecution", "prison_jail")

    needs_police = contrast(recs, "police/prosecution/jail  vs  every other system",
                            is_police, min_n)

    def genotype(r):
        """The v002 candidate: specific number + ordinary person + institutional contradiction."""
        g = r["genome"]
        if g["protagonist_type"] == UNKNOWN:
            return None
        ordinary = g["protagonist_type"] in ("ordinary_individual", "group_of_ordinary_people",
                                             "small_business_owner", "employee")
        return bool(g["title_has_number"]) and ordinary and bool(g["contradiction_present"])

    needs_geno = contrast(recs, "GENOTYPE: number in title + ordinary protagonist + "
                                "stated contradiction", genotype, min_n)

    print("\n### the 2x2 that actually answers it (police x genotype)")
    cells = {}
    for r in recs:
        p, gt = is_police(r), genotype(r)
        if p is None or gt is None:
            continue
        cells.setdefault(f"police={p}, genotype={gt}", []).append(r)
    print(f"    {'cell':<30}{'n':>4}{'med APV':>12}{'med ret@30s':>14}{'med subs/1k':>14}")
    for k, v in sorted(cells.items()):
        avd = metric_values(v, "avd")
        ret = metric_values(v, "retention_30s")
        spk = metric_values(v, "subs_per_1000")
        print(f"    {k:<30}{len(v):>4}"
              f"{(_fmt(median(avd) if avd else None, 1)):>12}"
              f"{(_fmt(median(ret) if ret else None, 3)):>14}"
              f"{(_fmt(median(spk) if spk else None, 2)):>14}")
    small = [k for k, v in cells.items() if len(v) < min_n]
    if small:
        print(f"    cells under n={min_n}: {', '.join(small)} -- read these as anecdotes, not data.")

    print("\n" + "=" * 100)
    print("PART 2 -- PERFORMANCE BY STRUCTURAL FEATURE")
    print("=" * 100)
    group_table(recs, "protagonist_type", lambda r: r["genome"]["protagonist_type"], min_n)
    group_table(recs, "system", lambda r: r["genome"]["system"], min_n)
    group_table(recs, "structure", lambda r: r["genome"]["structure"], min_n)
    group_table(recs, "hook_type (what the narration opens on)",
                lambda r: r["genome"]["hook_type"], min_n)
    group_table(recs, "ending_emotion", lambda r: r["genome"]["ending_emotion"], min_n)
    group_table(recs, "thumbnail_kind (live thumbnail)",
                lambda r: r["genome"]["thumbnail_kind"], min_n)
    group_table(recs, "title_archetype", lambda r: r["genome"]["title_archetype"], min_n)
    group_table(recs, "title_verb (mechanical)", lambda r: r["genome"]["title_verb"], min_n)
    group_table(recs, "stakes (a film can appear in several rows)",
                lambda r: r["genome"]["stakes"], min_n)
    group_table(recs, "instincts (a film can appear in several rows)",
                lambda r: r["genome"]["instincts"], min_n)
    group_table(recs, "runtime tier", lambda r: (
        "daily 8-12m" if r["duration_sec"] < 780 else
        "investigates 13-22m" if r["duration_sec"] < 1380 else "prime 23m+"), min_n)
    group_table(recs, "series_id (measured playlist cluster)",
                lambda r: r["genome"]["series_id"], min_n)

    print("\n" + "=" * 100)
    print("PART 2B -- THE ONLY METRIC WITH SAMPLE: EVERY FEATURE vs CTR")
    print("=" * 100)
    usable_ctr = [r for r in recs
                  if _num(r["performance"]["ctr"]) is not None
                  and (_num(r["performance"]["ctr_impressions"]) or 0) >= CTR_IMPRESSION_FLOOR]
    ctr_ages = [(today - datetime.fromisoformat(r["published_at"].replace("Z", "+00:00"))).days
                for r in usable_ctr]
    rho = spearman(ctr_ages, [r["performance"]["ctr"] for r in usable_ctr])
    print(f"  BEFORE READING THE TABLE: CTR here is Studio's ROLLING 28-day window, so an older "
          f"film is measured over a mature month and a new one over its launch month. Those are "
          f"different lifecycle stages, not comparable exposure.")
    if rho is not None:
        print(f"  Spearman(age, CTR) = {rho:+.2f} on n={len(usable_ctr)} -- age is doing real work "
              f"in this table, and anything that correlates with publish era will inherit it.")
    ctr_scan(recs)

    print("\n" + "=" * 100)
    print("PART 3 -- SINGLE-FEATURE CONTRASTS")
    print("=" * 100)
    contrast(recs, "title contains a digit", lambda r: bool(r["genome"]["title_has_number"]), min_n)
    contrast(recs, "title contains a money amount",
             lambda r: bool(r["genome"]["title_has_money"]), min_n)
    contrast(recs, "narration opens on a specific number (hook_type)",
             lambda r: (None if r["genome"]["hook_type"] == UNKNOWN else
                        r["genome"]["hook_type"] in ("specific_dollar_amount",
                                                     "specific_number_nonmoney")), min_n)
    contrast(recs, "contradiction stated in the film",
             lambda r: (None if r["genome"]["protagonist_type"] == UNKNOWN else
                        bool(r["genome"]["contradiction_present"])), min_n)
    contrast(recs, "ordinary protagonist",
             lambda r: (None if r["genome"]["protagonist_type"] == UNKNOWN else
                        r["genome"]["protagonist_type"] in
                        ("ordinary_individual", "group_of_ordinary_people",
                         "small_business_owner", "employee")), min_n)
    contrast(recs, "a human face on the thumbnail",
             lambda r: (None if r["genome"]["thumbnail_face"] in (UNKNOWN, None)
                        else bool(r["genome"]["thumbnail_face"])), min_n)

    print("\n" + "=" * 100)
    print("PART 4 -- HOW MUCH MORE WOULD IT TAKE")
    print("=" * 100)
    usable = sum(1 for r in recs if (_num(r["performance"]["views"]) or 0) >= VIEWS_FLOOR)
    both = {f"police/{k}": v for k, v in needs_police.items()}
    both.update({f"genotype/{k}": v for k, v in needs_geno.items()})
    total_subs = sum(_num(r["performance"]["subscribers_gained"]) or 0 for r in recs)
    if total_subs < SUBS_NUMERATOR_FLOOR:
        both.pop("police/subs_per_1000", None)
        both.pop("genotype/subs_per_1000", None)
        # its "need" is computed from a rate that is mostly zeros; quoting it would make the
        # cheapest-looking question the least trustworthy one.
    cheapest = min(both.values()) if both else None
    print(f"  The blocker is NOT the number of episodes -- 57 films is a reasonable sample. "
          f"The blocker is that only {usable} of them have {VIEWS_FLOOR}+ views, so the "
          f"watch-behaviour metrics have almost nothing to average over.")
    if cheapest:
        cheap_key = min(both, key=both.get)
        print(f"  On the observed effect sizes, the cheapest of the headline questions "
              f"({cheap_key}) would need about {cheapest} films PER SIDE at 80% power / alpha .05 "
              f"-- roughly {cheapest * 2} films with real viewership, against {usable} today.")
        print(f"  Every other headline metric needs far more: "
              f"{', '.join(f'{k} ~{v}/side' for k, v in sorted(both.items(), key=lambda kv: kv[1]))}.")
    print(f"  Two ways to close that gap, and only one of them is 'make more episodes':")
    print(f"    1. Give the {len(recs) - usable} existing films distribution. Their thumbnails "
          f"are already being served thousands of impressions; the missing quantity is clicks, "
          f"not inventory. Every one of them that reaches ~200 views converts a dead row in this "
          f"dataset into a live one, at zero production cost.")
    print(f"    2. Keep annotating new episodes at publish time so the genome is never "
          f"reconstructed after the fact again.")
    print(f"  Until then: 'cannot separate' means not enough data, NOT 'no difference'. Nothing "
          f"in this report licenses dropping police, and nothing in it licenses keeping police.")
    return 0


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build", action="store_true", help="rebuild data/content_genome.v001.jsonl")
    ap.add_argument("--refresh", action="store_true",
                    help="with --build: re-query YouTube (Data API ~301 units, Analytics free)")
    ap.add_argument("--report", action="store_true", help="print the grouped report")
    ap.add_argument("--min-n", type=int, default=5,
                    help="hide any group smaller than this in the report (default 5)")
    ap.add_argument("--merge-annotations", metavar="DIR",
                    help="fold per-batch annotation json files into "
                         "data/content_genome_annotations.v001.json")
    ap.add_argument("--bundle-index", metavar="PATH",
                    help="with --merge-annotations: json listing each episode's narration source")
    ap.add_argument("--annotation-method", default="unrecorded",
                    help="with --merge-annotations: one sentence saying how the judgement fields "
                         "were arrived at, stored in the output so a later reader can judge them")
    args = ap.parse_args()
    if not (args.build or args.report or args.merge_annotations):
        ap.print_help()
        return 2
    rc = 0
    if args.merge_annotations:
        rc = merge_annotations(Path(args.merge_annotations),
                               Path(args.bundle_index) if args.bundle_index else None,
                               args.annotation_method)
    if args.build:
        rc = build(args.refresh)
    if args.report:
        rc = report(args.min_n) or rc
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
