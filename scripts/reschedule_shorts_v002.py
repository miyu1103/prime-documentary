#!/usr/bin/env python3
"""Re-pack every future-scheduled Short at 2 per day so each one lands just AFTER its own long-form.

Why (owner, 2026-07-30): the Shorts queue had drifted 2-4 weeks behind the episodes it promotes.
At one Short per day, 23 booked Shorts stretched to 8/24 while the long-form ran daily and was
already at EP55. Two of them (EP50, EP51) were even publishing BEFORE their own episode, which
points a viewer at a case that is not on the channel yet.

The owner's instruction is to run Shorts at 2/day for a while to catch up, and to line them up with
the long-form dates. Long-form is assembled daily and keeps publishing daily, so this script orders
the Shorts by their episode's long-form date and packs them 2/day from 2026-07-31.

Long-form dates used for the ordering (public/scheduled = measured; 8/04 onward = the daily cadence
the owner confirmed is coming):
  EP36 7/21  EP37 7/22  EP38 7/23  EP39 7/24  EP40 7/25  EP41 7/26  EP42 7/27  EP43 7/28
  EP44 7/29  EP45 7/30  EP48 7/31  EP49 8/01  EP46 8/02  EP47 8/03
  EP50 8/04  EP51 8/05  EP52 8/06  EP53 8/07  EP54 8/08  EP55 8/09   <- assumed daily

Result: every Short publishes 1-3 days after its own episode, nothing publishes before its episode,
and the queue ends 8/11 instead of 8/24 — so from 8/12 the channel is back to 1 long-form + 1 Short
a day, with the Short belonging to that week's episode.

Only status.publishAt changes: no delete, no re-upload, same video IDs and thumbnails. Refuses to
touch anything that is not still private. Rewrites both receipts per Short.

    py -3.11 scripts/reschedule_shorts_v002.py --dry-run
    py -3.11 scripts/reschedule_shorts_v002.py
"""
from __future__ import annotations
import argparse, json, re, sys, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from pd_factory.providers import load_env
from pd_factory.providers.youtube import _access_token

CHANNEL_ALLOWLIST = {"UCuQPtAz1rca9eJ4xhvX0yKA"}
RESULTS = ROOT / "runs" / "new_shorts" / "schedule"
JST = timezone(timedelta(hours=9))

# (short, video_id, episode dir, that episode's long-form date) — ordered by long-form date.
# Two Shorts exist for EP53/54/55; both are kept, back to back, after their episode.
QUEUE = [
    (38, "EP-iiuy6L-o", "PD-2026-036-williams",    "07-21"),
    (39, "gZknzRSgRaw", "PD-2026-037-florence",    "07-22"),
    (40, "sP_lQebksIQ", "PD-2026-038-kidsforcash", "07-23"),
    (41, "v6CrJ9HtFlg", "PD-2026-039-frazier",     "07-24"),
    (42, "tFHwI4R4tJY", "PD-2026-040-lech",        "07-25"),
    (43, "g7q-9SOPDbE", "PD-2026-041-thompson",    "07-26"),
    (52, "SRUWd-5UCxE", "PD-2026-042-young",       "07-27"),
    (53, "qo9r7X_RnI8", "PD-2026-043-caniglia",    "07-28"),
    (46, "HBUYD8Uv4Ak", "PD-2026-044-tekoh",       "07-29"),
    (47, "TIWAscG6On8", "PD-2026-045-cleveland",   "07-30"),
    (50, "1FHZ5qA6pgA", "PD-2026-048-glover",      "07-31"),
    (51, "lDpfSAuFMS8", "PD-2026-049-strieff",     "08-01"),
    (48, "nFEJBlEijdw", "PD-2026-046-tlo",         "08-02"),
    (49, "wNqYS4j_VwM", "PD-2026-047-atwater",     "08-03"),
    (54, "aFPyMf3ugrA", "PD-2026-050-centralpark", "08-04*"),
    (55, "J95FzWezj2g", "PD-2026-051-willingham",  "08-05*"),
    (56, "k_5TAaWoUTk", "PD-2026-052-morton",      "08-06*"),
    (57, "An_fTeVboKY", "PD-2026-053-norfolk",     "08-07*"),
    (60, "9r2CrlG5IlU", "PD-2026-053-norfolk",     "08-07*"),
    (58, "rDCMEWgsbX4", "PD-2026-054-flowers",     "08-08*"),
    (63, "qvjB7RvpuUc", "PD-2026-054-flowers",     "08-08*"),
    (59, "LKrAG9AhCVY", "PD-2026-055-burge",       "08-09*"),
    (66, "xhoGSk8JA5c", "PD-2026-055-burge",       "08-09*"),
]

START = "2026-07-31"   # first slot (tomorrow)
PER_DAY = 2
HOUR_UTC = "T03:00:00Z"  # 12:00 JST


def plan():
    d0 = datetime.strptime(START, "%Y-%m-%d").date()
    out = []
    for i, (n, vid, ep, lf) in enumerate(QUEUE):
        day = d0 + timedelta(days=i // PER_DAY)
        out.append((n, vid, ep, lf, f"{day.isoformat()}{HOUR_UTC}"))
    return out


def api(tok, url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"}),
                                timeout=60) as r:
        return json.loads(r.read().decode())


def set_publish_at(tok, vid, when):
    body = json.dumps({"id": vid, "status": {"privacyStatus": "private", "publishAt": when,
                                             "selfDeclaredMadeForKids": False}}).encode()
    r = urllib.request.Request("https://www.googleapis.com/youtube/v3/videos?part=status", data=body,
                               headers={"Authorization": f"Bearer {tok}",
                                        "Content-Type": "application/json"}, method="PUT")
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode())


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    moves = plan()
    for _, _, _, _, when in moves:
        if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", when):
            raise RuntimeError(f"bad publishAt {when}")
    seen = {}
    for n, vid, _, _, when in moves:
        seen.setdefault(when, []).append(n)
    over = {w: v for w, v in seen.items() if len(v) > PER_DAY}
    if over:
        raise RuntimeError(f"more than {PER_DAY} Shorts on a day: {over}")

    tok = _access_token(load_env())
    ch = api(tok, "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true")["items"][0]["id"]
    if ch not in CHANNEL_ALLOWLIST:
        print(f"BLOCKED: channel {ch} not allowlisted"); return 1
    print(f"OK channel {ch}\n")

    ids = [m[1] for m in moves]
    cur = {}
    for k in range(0, len(ids), 50):
        for v in api(tok, "https://www.googleapis.com/youtube/v3/videos?part=snippet,status&id="
                     + ",".join(ids[k:k + 50]))["items"]:
            cur[v["id"]] = v
    missing = [i for i in ids if i not in cur]
    if missing:
        print(f"BLOCKED: video(s) not found: {missing}"); return 1
    live = [i for i in ids if cur[i]["status"]["privacyStatus"] != "private"]
    if live:
        print(f"BLOCKED: not private (already public?): {live}"); return 1

    print(f"{'short':>6}  {'episode':<24}{'long-form':<11}{'now':<12}{'->':<3}{'new':<12}delta")
    changed = 0
    for n, vid, ep, lf, when in moves:
        was = cur[vid]["status"].get("publishAt", "")
        wj = datetime.fromisoformat(was.replace("Z", "+00:00")).astimezone(JST).strftime("%m-%d") if was else "-"
        nj = datetime.fromisoformat(when.replace("Z", "+00:00")).astimezone(JST).strftime("%m-%d")
        mark = "" if wj == nj else "  MOVE"
        print(f"{n:>6}  {ep:<24}{lf:<11}{wj:<12}->  {nj:<12}{mark}")
        if wj == nj or args.dry_run:
            continue
        set_publish_at(tok, vid, when)
        changed += 1
        for p in (RESULTS / f"short{n}.result.json",
                  ROOT / "episodes" / ep / "09_package" / f"short{n}_youtube_schedule_result.v001.json"):
            if p.exists():
                d = json.loads(p.read_text(encoding="utf-8"))
                d["publishAt"] = when
                p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n{'[dry-run] would move' if args.dry_run else 'moved'}: "
          f"{sum(1 for n, vid, _, _, w in moves if cur[vid]['status'].get('publishAt') != w)} of {len(moves)}"
          if args.dry_run else f"\nmoved {changed} of {len(moves)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
