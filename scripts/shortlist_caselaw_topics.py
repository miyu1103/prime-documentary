#!/usr/bin/env python3
"""Read the harvest and surface the rows that actually look like a story.

`harvest_caselaw_topics.py` scores caption shape, obscurity and recency. Those proxies
cannot tell `State v. Brown` from a film. This pass adds the one signal that separates
them: **is there a named human or a named seized thing in the caption**, and does the
opinion snippet describe events rather than procedure.

    State v. Brown                                 -> nothing to hold on to
    Kenneth John Jouppi v. State of Alaska         -> a named person the state took from
    United States v. $134,972.34 Seized from ...   -> the money is the defendant

Still not a topic decision. It is a reading list, ordered so the top of it is worth a human
half hour. Output is markdown so it can be pasted into a TOPIC_PIPELINE doc.

    py -3.11 scripts/shortlist_caselaw_topics.py
    py -3.11 scripts/shortlist_caselaw_topics.py --inputs a.json b.json --top 40
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEAS = ROOT / "episodes" / "_planning" / "measurements"
DEFAULT_INPUTS = [MEAS / "CASELAW_HARVEST.json", MEAS / "CASELAW_HARVEST_B.json"]
DEFAULT_OUT = MEAS / "CASELAW_SHORTLIST.md"

# a caption with a given name and a surname, e.g. "Kenneth John Jouppi v. State of Alaska"
FULL_NAME = re.compile(r"\b[A-Z][a-z]{2,}\s+(?:[A-Z]\.\s+|[A-Z][a-z]{2,}\s+)?[A-Z][a-z]{2,}\b")
# the seized thing is the defendant: money, a vehicle, a house
NAMED_RES = re.compile(
    r"(\$[\d,][\d,.]*|\b(19|20)\d{2}\s+[A-Z][a-z]+|\bReal Property\b|\bCurrency\b|"
    r"\bChevrolet\b|\bJeep\b|\bFord\b|\bHarley\b|\bAircraft\b|\bAirplane\b)", re.I)
# procedural boilerplate: the opinion is about a motion, not about what happened
PROCEDURAL = re.compile(
    r"\b(remand\w*|affirm\w*|revers\w*|per curiam|memorandum decision|"
    r"petition for (a )?writ|summary (order|judgment)|motion to (dismiss|compel)|"
    r"standard of review|abuse of discretion)\b", re.I)
# events: something happened to somebody
EVENTFUL = re.compile(
    r"\b(seiz\w+|stopp?ed|search\w*|arrest\w+|shot|shoot\w*|killed|died|death|"
    r"confess\w+|interrogat\w+|testif\w+|witness\w+|hair|bite|arson|fire|"
    r"foreclos\w+|evict\w+|took|taken|refused|denied|home|house|apartment|"
    r"daughter|son|wife|husband|mother|father|child)\b", re.I)

GENERIC_CAPTION = re.compile(
    r"^(state|people|commonwealth|united states|u\.s\.)\s+v\.?\s+[A-Z][a-z]+\.?$", re.I)


# words that are capitalised in every legal thesis and mean nothing about the topic
NOVELTY_STOP = {
    "United", "States", "State", "Supreme", "Court", "Circuit", "County", "City",
    "District", "Department", "Police", "Sheriff", "Justice", "Amendment", "America",
    "American", "Constitution", "Congress", "Federal", "National", "Institute",
    "Attorney", "General", "Office", "Commission", "Board", "January", "February",
    "March", "April", "August", "September", "October", "November", "December",
    "Civil", "Criminal", "Appeals", "Common", "Pleas", "Commonwealth", "People",
}
PROPER = re.compile(r"\b[A-Z][A-Za-z'\-]{4,}\b")


def existing_topics() -> dict[str, str]:
    """Distinctive proper noun -> episode id, read from each episode's own thesis.

    Slug matching was tried first and got it wrong: `PD-2026-042-young` is Anjanette Young
    (a wrong-address raid in Chicago), not the Elizabeth Young forfeiture case, so a slug
    match would have hidden a genuinely new topic while missing the real overlap, which is
    `PD-2026-028-forfeiture` (the same Philadelphia forfeiture machine). The thesis names
    the actual people and places, so that is what we match on.
    """
    out: dict[str, str] = {}
    ep_dir = ROOT / "episodes"
    if not ep_dir.is_dir():
        return out
    plan = ep_dir / "_planning"
    for d in sorted(ep_dir.iterdir()):
        if not d.is_dir() or not d.name.startswith("PD-"):
            continue
        text = ""
        # JSON thesis first — it is the most concentrated statement of the topic
        for f in sorted((d / "03_script").glob("*.json")) + [d / "manifest.json"]:
            if not f.exists():
                continue
            try:
                obj = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue  # a malformed episode file must not stop the sweep
            for key in ("thesis", "viewer_promise", "title", "controlling_idea"):
                v = obj.get(key)
                if isinstance(v, str):
                    text += " " + v
            if text:
                break
        # Markdown fallback. JSON-only reached 35 of 60 episodes and missed exactly the
        # recent slate — willingham, morton, norfolk, flowers, burge — whose scripts are
        # markdown with no JSON beside them. Those are the wrongful-conviction episodes,
        # i.e. the ones most likely to collide with a new candidate, so missing them made
        # the whole check worse than useless.
        if not text:
            mds = sorted((d / "03_script").glob("*.md"))
            num = d.name.split("-")[2] if len(d.name.split("-")) > 2 else ""
            if num:
                mds += sorted(plan.glob(f"EP{int(num)}_*.md")) if num.isdigit() else []
            for f in mds[:3]:
                try:
                    text += " " + f.read_text(encoding="utf-8")[:4000]
                except Exception:
                    continue
        for w in PROPER.findall(text):
            if w not in NOVELTY_STOP:
                out.setdefault(w, d.name)
    return out


def story_score(c: dict, made: dict[str, str]) -> tuple[float, list[str], str]:
    """Add narrative signal on top of the harvest score. Returns (score, why, already_made)."""
    pts, why = float(c.get("score") or 0.0), []
    name = c.get("case_name") or ""
    snip = c.get("snippet") or ""
    blob = name + " " + snip
    hit = next((ep for w, ep in made.items()
                if re.search(rf"\b{re.escape(w)}\b", blob)), "")
    if hit:
        pts -= 8.0
        why.append(f"既に制作済みの可能性: {hit} (-8)")

    if GENERIC_CAPTION.match(name.strip()):
        pts -= 3.0
        why.append("caption が `State v. 姓` だけ — 手がかりゼロ (-3)")
    else:
        if FULL_NAME.search(re.sub(r"\b(State|United States|Commonwealth|County|City|"
                                   r"Department|Court|Office|Sheriff)\b", "", name)):
            pts += 2.5
            why.append("実名の個人が当事者 (+2.5)")
        m = NAMED_RES.search(name)
        if m:
            pts += 2.5
            why.append(f"押収物そのものが被告: {m.group(0)} (+2.5)")

    ev = sorted({m.group(0).lower() for m in EVENTFUL.finditer(snip)})
    if ev:
        pts += min(2.5, 0.4 * len(ev))
        why.append(f"出来事が書かれている: {', '.join(ev[:8])} (+{min(2.5, 0.4*len(ev)):.1f})")
    elif snip:
        why.append("snippet が手続きの話だけ (0)")
    else:
        pts -= 1.0
        why.append("snippet なし — 中身が読めない (-1)")

    if PROCEDURAL.search(snip) and not ev:
        pts -= 1.5
        why.append("純粋な手続き判断 (-1.5)")

    return round(pts, 2), why, hit


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inputs", nargs="*", default=[str(p) for p in DEFAULT_INPUTS])
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--per-lane", type=int, default=3, help="cap per doctrine, for variety")
    ap.add_argument("--output", default=str(DEFAULT_OUT))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-novelty-check", action="store_true",
                    help="do not penalise cases naming a person or place an episode already covered")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    rows: list[dict] = []
    for p in a.inputs:
        path = Path(p)
        if not path.exists():
            print(f"missing input: {path}", file=sys.stderr)
            continue
        rows.extend(json.loads(path.read_text(encoding="utf-8")).get("candidates") or [])
    if not rows:
        print("no candidates loaded", file=sys.stderr)
        return 2

    made = {} if a.no_novelty_check else existing_topics()
    if made:
        print(f"novelty check against {len(made)} existing episodes\n")
    seen: set[tuple] = set()
    scored: list[dict] = []
    for c in rows:
        key = (c.get("cluster_id"), (c.get("case_name") or "").lower())
        if key in seen:
            continue
        seen.add(key)
        s, why, hit = story_score(c, made)
        c = dict(c, story_score=s, story_reasons=why, already_made=hit)
        scored.append(c)
    scored.sort(key=lambda c: -c["story_score"])

    per: dict[str, int] = {}
    picked: list[dict] = []
    for c in scored:
        lane = c["lane"]
        if per.get(lane, 0) >= a.per_lane:
            continue
        per[lane] = per.get(lane, 0) + 1
        picked.append(c)
        if len(picked) >= a.top:
            break

    for c in picked:
        mark = "  [既出? " + c["already_made"] + "]" if c["already_made"] else ""
        print(f"{c['story_score']:>6.1f}  {c['lane']:<18} {c['case_name'][:58]}{mark}")

    if a.dry_run:
        print("\n(dry run — nothing written)")
        return 0

    out = Path(a.output)
    if out.exists() and not a.force:
        print(f"{out} exists; pass --force", file=sys.stderr)
        return 2

    lines = [
        "# CASE-LAW SHORTLIST — 実在判例から選ぶ題材候補",
        "",
        f"Generated by `scripts/shortlist_caselaw_topics.py` from {len(rows)} harvested cases "
        f"({len(scored)} after dedupe). **This is a reading list, not a decision.** An opinion "
        "states a holding; it never says whether the story carries 40 minutes. Read the top rows, "
        "then run `topic_demand_probe.py` on whichever premises survive.",
        "",
        f"Capped at {a.per_lane} per doctrine so one lane cannot fill the list.",
        "",
    ]
    for i, c in enumerate(picked, 1):
        lines += [
            f"## {i}. {c['case_name']}",
            "",
            f"- **{c['lane_label']}**",
            f"- {c['court']} · {c['date_filed']} · docket {c['docket'] or '—'} · "
            f"cites {c['cite_count']}",
            f"- {c['url']}",
            f"- story score **{c['story_score']}** (harvest {c['score']})"
            + (f" · ⚠ 既出の疑い: {c['already_made']}" if c["already_made"] else ""),
            "",
        ]
        if c.get("snippet"):
            lines += ["> " + c["snippet"].replace("\n", " "), ""]
        lines += ["  - " + r for r in c["story_reasons"]] + [""]

    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    tmp.replace(out)
    try:
        shown = out.relative_to(ROOT)
    except ValueError:
        shown = out
    print(f"\nwrote {shown}  ({len(picked)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
