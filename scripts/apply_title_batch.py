#!/usr/bin/env python3
"""Apply a batch of back-catalogue TITLE rewrites from a JSON file, safely and measurably.

WHY THIS EXISTS (and why it is not `retitle_packaging_v001.py`)
---------------------------------------------------------------
`retitle_packaging_v001.py` hardcodes six specific 2026-07-19 changes. This one is
file-driven, re-verifies every row against the CURRENT rule set, and refuses to touch
the locked publishing window. Same proven write pattern, generalised.

THE THREE WAYS A TITLE UPDATE DESTROYS SOMETHING, AND THE GUARD FOR EACH
------------------------------------------------------------------------
1. `videos.update` REPLACES the whole `snippet`. A body carrying only `title` silently
   WIPES description/tags/categoryId/defaultLanguage. 56 descriptions were rewritten on
   2026-08-10; losing them is unrecoverable without a re-write pass.
   GUARD: fetch the live snippet, echo every SNIPPET_KEY back byte-identical, change only
   `title`, then RE-FETCH and assert the description is byte-identical. Any mismatch is a
   hard stop for the whole batch, not a warning.

2. Sending a `status` object can move `privacyStatus` / `publishAt` — i.e. it can publish a
   scheduled video early, or unpublish a live one.
   GUARD: `part=snippet` only. This module never constructs a status object; there is no
   code path that can. The post-write re-fetch asserts both fields are unmoved anyway,
   because "structurally impossible" is a claim that should still be measured.

3. Editing something inside the locked publishing window.
   GUARD: the locked set is computed from the LIVE channel (publishAt >= cutoff, or
   publishedAt >= cutoff), never from a local manifest, and every target is asserted
   outside it before the first write.

Read-only by default. `--apply` writes. Every write is preceded by a rollback file
containing the complete pre-change snippet of every target.

Usage:
    py -3.11 scripts/apply_title_batch.py <batch.json>                  # dry run
    py -3.11 scripts/apply_title_batch.py <batch.json> --apply
    py -3.11 scripts/apply_title_batch.py --rollback <backup.json>

Batch file format: a JSON list of {"video_id": ..., "slug": ..., "new_title": ...}.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_packaging_qc import TITLE_MIN_CHARS, TITLE_MAX_CHARS  # noqa: E402  single source of truth
from yt_channel_index import API, authorize, http, list_video_ids, fetch_videos  # noqa: E402
import yt_quota  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Everything published or scheduled on/after this date is untouchable.
LOCK_CUTOFF = "2026-08-10"

# Fields videos.update accepts on snippet. Present-on-current + listed here = echoed back.
SNIPPET_KEYS = ("title", "description", "tags", "categoryId",
                "defaultLanguage", "defaultAudioLanguage")


def rule_failures(title: str) -> list[str]:
    """Every reason this title may not be shipped. Empty list = compliant.

    Band and both bounds come from check_packaging_qc so there is exactly one definition.
    """
    f: list[str] = []
    n = len(title)
    if not TITLE_MIN_CHARS <= n <= TITLE_MAX_CHARS:
        f.append(f"length {n} outside {TITLE_MIN_CHARS}-{TITLE_MAX_CHARS}")
    if "?" in title:
        f.append("question form")
    if re.search(r"\b(you|your|yours|yourself|you're)\b", title, re.I):
        f.append("second person")
    if re.search(r"\bv\.\s", title) or re.search(r"\bvs\.?\s", title, re.I):
        f.append("case citation")
    if "|" in title:
        f.append("pipe character")
    return f


def fact_failures(slug: str | None, title: str) -> list[str]:
    """Every claim in this title the episode's own record does not support.

    THE REASON THIS IS HERE. On 2026-08-12 a repackaging pass proposed "Five Boys Confessed on
    Camera" and "Seven Sailors Signed Confessions". Both are false -- four boys were videotaped
    and four sailors confessed -- and both passed `rule_failures` above, because every rule up
    there measures length, form and punctuation and none of them measures truth. A title is the
    most widely read sentence this channel publishes and `config/ship_policy.v001.json` puts it
    in the BLOCKING factual_support class; a writer that can change it live has to check it.

    Refuses on a missing detector rather than passing: an unverifiable title is not a verified
    one. Override with --allow-unverified-claims, which is recorded in the run output.
    """
    if not slug:
        return ["no slug on this row -- the title cannot be read against any episode record"]
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        import check_packaging_claims as cpc
        return cpc.fact_failures(slug, title)
    except Exception as exc:  # noqa: BLE001
        return [f"claim check unavailable ({type(exc).__name__}: {exc})"]


def locked_ids(auth: dict) -> tuple[set[str], dict]:
    """Video ids inside the frozen publishing window, measured from the live channel."""
    ids = list_video_ids(auth)
    vids = fetch_videos(auth, ids, part="snippet,status")
    for _ in range((len(ids) + 49) // 50):
        yt_quota.record("videos.list")
    locked = set()
    for vid, v in vids.items():
        st, sn = v["status"], v["snippet"]
        pub_at = (st.get("publishAt") or "")[:10]
        published = (sn.get("publishedAt") or "")[:10]
        if pub_at >= LOCK_CUTOFF and pub_at:
            locked.add(vid)
        elif not st.get("publishAt") and published >= LOCK_CUTOFF:
            locked.add(vid)
    return locked, vids


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("batch", nargs="?", type=Path, help="JSON list of {video_id, slug, new_title}")
    ap.add_argument("--apply", action="store_true", help="actually write (default: dry run)")
    ap.add_argument("--rollback", type=Path, help="restore titles from a backup json")
    ap.add_argument("--out", type=Path, help="where to write the backup/dry-run record")
    ap.add_argument("--allow-unverified-claims", action="store_true",
                    help="skip check_packaging_claims (title vs the episode's own script). "
                         "Only with an owner decision on the specific rows -- this is the gate "
                         "the two false titles of 2026-08-12 would have hit.")
    a = ap.parse_args()

    auth = authorize(ROOT)

    if a.rollback:
        data = json.loads(a.rollback.read_text(encoding="utf-8"))
        for row in data["videos"]:
            snip = row["snippet_before"]
            body = {k: snip[k] for k in SNIPPET_KEYS if k in snip}
            st, b = http("PUT", f"{API}/videos?part=snippet", headers=auth,
                         body={"id": row["video_id"], "snippet": body})
            yt_quota.record("videos.update")
            print(f"{'OK ' if st == 200 else 'ERR'} {row['video_id']} -> {row['title_before']!r}")
        return 0

    if not a.batch:
        ap.error("batch file required unless --rollback")

    proposals = json.loads(a.batch.read_text(encoding="utf-8"))
    locked, live = locked_ids(auth)
    print(f"locked window (>= {LOCK_CUTOFF}): {len(locked)} videos -- none of these may be written\n")

    todo, skipped = [], []
    for r in proposals:
        vid, new = r["video_id"], r["new_title"]
        cur = live.get(vid)
        if cur is None:
            skipped.append((vid, r.get("slug"), new, ["not on channel"]))
            continue
        reasons = rule_failures(new)
        if not a.allow_unverified_claims:
            reasons += [f"UNSUPPORTED CLAIM: {x}"
                        for x in fact_failures(r.get("slug"), new)]
        if vid in locked:
            reasons.insert(0, "INSIDE LOCKED PUBLISH WINDOW")
        if cur["snippet"].get("title", "") == new:
            reasons.append("already live (no change needed)")
        if reasons:
            skipped.append((vid, r.get("slug"), new, reasons))
        else:
            todo.append((vid, r.get("slug"), new, cur))

    for vid, slug, new, reasons in skipped:
        print(f"SKIP {vid} {slug or '':<18} {'; '.join(reasons)}")
    print()
    for vid, slug, new, _ in todo:
        print(f"PASS {vid} {slug or '':<18} [{len(new)}] {new}")
    print(f"\n{len(todo)} to write, {len(skipped)} skipped, of {len(proposals)} proposed")

    # Assert the invariant before any write, loudly, rather than trusting the loop above.
    assert not (set(v for v, _, _, _ in todo) & locked), "REFUSING: a target is inside the lock"

    record = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "batch_file": str(a.batch),
        "band": [TITLE_MIN_CHARS, TITLE_MAX_CHARS],
        "lock_cutoff": LOCK_CUTOFF,
        "locked_count": len(locked),
        "applied": bool(a.apply),
        "videos": [],
        "skipped": [{"video_id": v, "slug": s, "new_title": n, "reasons": r}
                    for v, s, n, r in skipped],
    }

    for vid, slug, new, cur in todo:
        snip = cur["snippet"]
        record["videos"].append({
            "video_id": vid, "slug": slug,
            "title_before": snip.get("title", ""), "title_after": new,
            "privacy_before": cur["status"].get("privacyStatus"),
            "publish_at_before": cur["status"].get("publishAt"),
            "description_sha_before": None, "snippet_before": snip,
        })

    out = a.out or (ROOT / "episodes" / "_planning" / "measurements" /
                    (f"TITLE_APPLY.{'applied' if a.apply else 'dryrun'}.json"))

    if not a.apply:
        out.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\nDRY RUN -- nothing written to YouTube. record: {out}")
        return 0

    out.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nrollback file written BEFORE any write: {out}")

    failures = 0
    for row in record["videos"]:
        vid, snip, new = row["video_id"], row["snippet_before"], row["title_after"]
        body = {k: snip[k] for k in SNIPPET_KEYS if k in snip}
        body["title"] = new
        st, b = http("PUT", f"{API}/videos?part=snippet", headers=auth,
                     body={"id": vid, "snippet": body})
        yt_quota.record("videos.update")
        if st == 403 and "quota" in json.dumps(b).lower():
            yt_quota.record("exhausted_observed_403")
            row["result"] = "quota 403 -- not attempted"
            # Save progress BEFORE returning: the rows already written need their verify
            # results on disk, and every row needs its snippet_before for rollback.
            out.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  QUOTA EXCEEDED (real 403) on {vid} -- stopping the batch here.")
            print(f"  progress saved to {out}; re-run after the 16:00 JST reset to finish.")
            return 2
        if st != 200:
            print(f"  ERROR {st} on {vid}: {json.dumps(b)[:200]}")
            row["result"] = f"http {st}"
            failures += 1
            continue

        # Independent re-read. Trust the GET, not the PUT's echo.
        got = fetch_videos(auth, [vid], part="snippet,status")[vid]
        yt_quota.record("videos.list")
        g_sn, g_st = got["snippet"], got["status"]
        checks = {
            "title_changed": g_sn.get("title") == new,
            "description_identical": g_sn.get("description", "") == snip.get("description", ""),
            "privacy_unmoved": g_st.get("privacyStatus") == row["privacy_before"],
            "publish_at_unmoved": g_st.get("publishAt") == row["publish_at_before"],
        }
        row["verify"] = checks
        row["result"] = "ok" if all(checks.values()) else "VERIFY FAILED"
        if not all(checks.values()):
            failures += 1
        print(f"  {row['result']:<14} {vid} {checks}")

    out.write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(record['videos']) - failures} verified OK, {failures} failed. record: {out}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
