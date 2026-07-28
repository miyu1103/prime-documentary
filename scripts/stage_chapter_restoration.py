#!/usr/bin/env python3
"""Recover a valid chapter block for every long-form that is not showing chapters.

STAGING ONLY. This script reads the repo and the stored channel measurement and
writes local files. It makes no network call and cannot publish anything.

Two defects need two different repairs (see `parse_chapter_block` in
`yt_distribution_state.py`):

  RENDER_BROKEN  A chapter block exists in the live description but YouTube
                 refuses to render it because one chapter is under 10 seconds.
                 On this channel the culprit is always the brand-sting chapter
                 ("Opening: <case>" / "Brand opening" / "Hook") sitting 3-9s from
                 its neighbour. Repair = drop that one line. Highest confidence:
                 every other timestamp and label is the author's own, unchanged.

  MISSING / PLACEHOLDER
                 No usable block was ever published. Repair = rebuild from
                 `03_script/script.annotated.*.json` (`chapters[].title` +
                 `spans[].text`, the canonical authored structure) and recover the
                 timestamps by aligning each chapter's opening span against the
                 episode's caption track. Lower confidence: the LABELS are the
                 author's, the TIMES are derived, so every row is marked for
                 owner review.

Outputs:
  episodes/_planning/measurements/CHAPTER_RESTORATION.v001.json
  episodes/_planning/CHAPTER_RESTORATION.v001.md   (line-by-line review sheet)

Exit codes: 0 all targets resolved, 1 one or more targets need manual authoring.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "episodes" / "_planning" / "measurements" / "DISTRIBUTION_STATE.v001.json"
OUT_JSON = ROOT / "episodes" / "_planning" / "measurements" / "CHAPTER_RESTORATION.v001.json"
OUT_MD = ROOT / "episodes" / "_planning" / "CHAPTER_RESTORATION.v001.md"

MIN_CHAPTER_SECONDS = 10          # YouTube's floor; the whole block dies below it
MIN_CHAPTERS = 3                  # YouTube's floor
ALIGN_WORDS = 12                  # words of a span used to locate it in the captions
ALIGN_MIN_RATIO = 0.55            # below this the alignment is not trusted

SRT_TIME_RE = re.compile(r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->")
WORD_RE = re.compile(r"[a-z0-9']+")

# Production-internal structure names. They are correct in the script and useless
# as YouTube chapters - a viewer scanning the seek bar for "the trial" will not
# search for "ACT II", and key-moment search indexes the label text.
ACT_PREFIX_RE = re.compile(
    r"^\s*(?:ACT|Act)\s+(?:[IVX]+|\d+)\s*(?:[-–—:.]\s*)?", re.U
)
BRAND_OPENING_RE = re.compile(
    r"^\s*(?:brand\s+opening|prime\s+documentary(?:\s+opening)?|opening(?:\s*[:–—-].*)?)\s*$",
    re.I,
)
NEEDS_LABEL_RE = re.compile(
    r"^\s*(?:hook|cold\s*open|opening|ending|outro|endcard|end\s*card|cta|"
    r"subscribe(?:\s*/\s*endcard)?|ending\s*/\s*cta|act\s+[ivx\d]+)\s*$",
    re.I,
)
# Headings in the markdown scripts, e.g. "## ACT 2 — What it costs to be the address"
MD_HEADING_RE = re.compile(
    r"^#{1,3}\s+(HOOK|OPENING|ACT\s+(?:[IVX]+|\d+)|ENDING)\b\s*(?:[-–—:]\s*)?(.*)$"
)
VO_LINE_RE = re.compile(r"^\s*(?:\[VO:?\]|\[VO\]:)\s*(.+)$", re.I)
# Non-narration lines inside a script body: stage directions, visual notes, markers.
NON_PROSE_RE = re.compile(r"^\s*(?:[>*_\-#|]+\s*)*(?:\[|【|\(VIS|\(SFX|!\[)")


def clean_heading_title(raw: str) -> str:
    """Turn a script act heading tail into a viewer-facing chapter label."""
    title = raw
    title = re.sub(r"(?:\s*[-–—]\s*)?\brole\s*:.*$", "", title, flags=re.I)  # "— role: body"
    title = re.sub(r"\s*\*\(.*?\)\*", "", title)                     # "*(kept short)*"
    title = re.sub(r"\s*[\(（][^)）]*[\)）]", "", title)               # "(=0:24-3:40)"
    title = re.sub(r"\s*\[[^\]]*\]", "", title)                      # "[S01 S02]"
    title = title.strip(" *_·—–-:\"'“”「」")

    # A tail that is only a timecode range ("0:00–0:30") is a production note,
    # not a label. So is anything still carrying Japanese production shorthand.
    if re.fullmatch(r"[\d:：]+\s*[-–—~]\s*[\d:：]+", title):
        return ""
    if re.search(r"[぀-ヿ一-鿿]", title):
        return ""

    if title and title.upper() == title and len(title) > 3:
        title = title.title()
    return title.strip()


def first_prose_line(lines: list[str]) -> str:
    """The first line under a heading that is actual narration, not a direction."""
    for line in lines:
        voice = VO_LINE_RE.match(line)
        if voice:
            return voice.group(1).strip()
        stripped = re.sub(r"^\s*[>*_]+\s*", "", line).strip()
        if not stripped or NON_PROSE_RE.match(line) or stripped.startswith("**["):
            continue
        stripped = re.sub(r"\*\*|\[CLM-\d+\]|【[^】]*】", "", stripped).strip()
        if len(stripped.split()) >= 8:
            return stripped
    return ""


# ------------------------------------------------------------------ repo lookup


def find_episode_dirs() -> list[Path]:
    return sorted(p for p in (ROOT / "episodes").glob("PD-*") if p.is_dir())


def map_videos_to_episodes(video_ids: set[str]) -> dict[str, str]:
    """Match each video id to the episode whose JSON artifacts mention it."""
    mapping: dict[str, str] = {}
    for episode in find_episode_dirs():
        for path in episode.rglob("*.json"):
            if "generated_images" in path.parts or "04_scenes" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for video_id in video_ids:
                if video_id in text and video_id not in mapping:
                    mapping[video_id] = episode.name
    return mapping


def load_annotated_chapters(episode: Path) -> tuple[list[dict], str] | tuple[None, None]:
    """The authored chapter structure: [{title, first_span_text}], plus its source path."""
    candidates = sorted(episode.glob("03_script/script.annotated*.json"), reverse=True)
    for path in candidates:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        chapters = data.get("chapters")
        spans = {s.get("span_id"): s.get("text", "") for s in data.get("spans", [])}
        if not chapters:
            continue
        out: list[dict] = []
        for chapter in chapters:
            span_ids = chapter.get("span_ids") or []
            first_text = ""
            for span_id in span_ids:
                if spans.get(span_id):
                    first_text = spans[span_id]
                    break
            out.append({"title": chapter.get("title", "").strip(), "first_span_text": first_text})
        if out:
            return out, str(path.relative_to(ROOT).as_posix())
    return None, None


def load_markdown_chapters(episode: Path, episode_number: int) -> tuple[list[dict], str] | tuple[None, None]:
    """Fallback source: act headings in the prose script.

    Some episodes never got a `script.annotated.json` (the annotated layer was
    skipped) but do have `## ACT 2 - <title>` headings plus `[VO:]` narration
    lines underneath, which is enough to recover both the label and an anchor
    sentence to align against the captions.
    """
    candidates = list(episode.glob("03_script/script.en.v*.md"))
    candidates += list((ROOT / "episodes" / "_planning").glob(f"EP{episode_number}_*script.en.v*.md"))
    for path in sorted(candidates, reverse=True):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        sections: list[tuple[str, list[str]]] = []
        current: tuple[str, list[str]] | None = None
        for line in lines:
            heading = MD_HEADING_RE.match(line)
            if heading:
                if current:
                    sections.append(current)
                kind, tail = heading.group(1), heading.group(2)
                current = (clean_heading_title(tail) or kind.title(), [])
                continue
            if current:
                current[1].append(line)
        if current:
            sections.append(current)
        chapters = [
            {"title": title, "first_span_text": first_prose_line(body)}
            for title, body in sections
        ]
        if len([c for c in chapters if c["first_span_text"]]) >= MIN_CHAPTERS:
            return chapters, str(path.relative_to(ROOT).as_posix())
    return None, None


def clean_labels(chapters: list[dict]) -> tuple[list[dict], list[str], list[str]]:
    """Strip production-internal naming. Returns (chapters, notes, needs_authoring)."""
    notes: list[str] = []
    needs: list[str] = []
    out: list[dict] = []
    for chapter in chapters:
        title = (chapter.get("title") or "").strip()

        if BRAND_OPENING_RE.match(title) and (chapter.get("seconds") or 0) < 90:
            notes.append(f"dropped the brand-sting chapter {title!r} - it is the line that "
                         "broke rendering on 13 videos and means nothing to a viewer")
            continue

        stripped = ACT_PREFIX_RE.sub("", title).strip(" -–—:")
        if stripped and stripped != title:
            notes.append(f"relabelled {title!r} -> {stripped!r}")
            title = stripped

        entry = dict(chapter)
        entry["title"] = title
        if NEEDS_LABEL_RE.match(title) or len(title) < 3:
            entry["needs_authoring"] = True
            needs.append(title)
        out.append(entry)
    return out, notes, needs


def load_captions(episode: Path) -> tuple[list[tuple[float, str]], str] | tuple[None, None]:
    """Caption cues as (start_seconds, text), from the most authoritative SRT present."""
    preferred = ["captions.final.v001.srt", "captions.final.v002.srt", "captions.final.v003.srt"]
    paths = [episode / "08_edit" / name for name in preferred]
    paths = [p for p in paths if p.exists()]
    if not paths:
        paths = sorted(episode.glob("08_edit/*.srt"), reverse=True)
    if not paths:
        return None, None
    path = paths[-1] if len(paths) > 1 else paths[0]
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, None

    cues: list[tuple[float, str]] = []
    start: float | None = None
    buffer: list[str] = []
    for line in raw.splitlines():
        match = SRT_TIME_RE.search(line)
        if match:
            if start is not None and buffer:
                cues.append((start, " ".join(buffer)))
            hours, minutes, seconds, millis = (int(g) for g in match.groups())
            start = hours * 3600 + minutes * 60 + seconds + millis / 1000
            buffer = []
        elif line.strip() and not line.strip().isdigit() and start is not None:
            buffer.append(line.strip())
    if start is not None and buffer:
        cues.append((start, " ".join(buffer)))
    return cues, str(path.relative_to(ROOT).as_posix())


# -------------------------------------------------------------------- alignment


def normalize(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def align_span(span_text: str, cues: list[tuple[float, str]]) -> tuple[float | None, float]:
    """Locate a span's opening words in the caption stream. Returns (seconds, ratio)."""
    needle = normalize(span_text)[:ALIGN_WORDS]
    if len(needle) < 4 or not cues:
        return None, 0.0

    words: list[tuple[str, float]] = []
    for start, text in cues:
        for word in normalize(text):
            words.append((word, start))
    if len(words) < len(needle):
        return None, 0.0

    target = " ".join(needle)
    best_ratio = 0.0
    best_time: float | None = None
    window = len(needle)
    for index in range(0, len(words) - window + 1):
        candidate = " ".join(w for w, _ in words[index:index + window])
        # cheap pre-filter: the first word must match, else skip the expensive compare
        if words[index][0] != needle[0]:
            continue
        ratio = SequenceMatcher(None, target, candidate).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_time = words[index][1]
    return best_time, best_ratio


# -------------------------------------------------------------------- repairing


def enforce_youtube_rules(chapters: list[dict], duration: int) -> tuple[list[dict], list[str]]:
    """Drop chapters that violate YouTube's floors. Returns (kept, notes).

    A chapter shorter than 10s does not merely fail on its own - it stops YouTube
    rendering the ENTIRE block. Dropping the short one keeps the rest working.
    """
    notes: list[str] = []
    kept: list[dict] = []
    for chapter in sorted(chapters, key=lambda c: c["seconds"]):
        if chapter["seconds"] >= duration:
            notes.append(f"dropped {chapter['title']!r} at {chapter['seconds']}s "
                         f"(past the {duration}s runtime)")
            continue
        if not kept:
            kept.append(dict(chapter))
            continue
        gap = chapter["seconds"] - kept[-1]["seconds"]
        if gap < MIN_CHAPTER_SECONDS:
            notes.append(f"dropped {chapter['title']!r} at {chapter['seconds']}s "
                         f"({gap}s after {kept[-1]['title']!r} - under YouTube's "
                         f"{MIN_CHAPTER_SECONDS}s floor, which is what was silently "
                         f"killing the whole block)")
            continue
        kept.append(dict(chapter))

    if kept and kept[0]["seconds"] != 0:
        notes.append(f"first chapter moved from {kept[0]['seconds']}s to 0s "
                     "(YouTube requires the block to start at 0:00)")
        kept[0]["seconds"] = 0
    return kept, notes


def format_timestamp(seconds: int) -> str:
    if seconds >= 3600:
        return f"{seconds // 3600}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"
    return f"{seconds // 60}:{seconds % 60:02d}"


def repair_render_broken(video: dict) -> dict:
    """Rebuild the block from the live description, dropping only the sub-10s rows."""
    chapters = [
        {"title": stamp["label"], "seconds": int(stamp["t"])}
        for stamp in video["chapters"]["stamps"]
    ]
    kept, notes = enforce_youtube_rules(chapters, video["duration_seconds"])
    kept, label_notes, needs = clean_labels(kept)
    kept, rule_notes = enforce_youtube_rules(kept, video["duration_seconds"])
    return {
        "method": "drop_sub_10s_chapters_from_live_description",
        "confidence": "high",
        "source": "the live YouTube description (surviving labels and times unchanged)",
        "chapters": kept,
        "notes": notes + label_notes + rule_notes,
        "labels_needing_authoring": needs,
        "needs_owner_review": "light - confirm the dropped lines"
                              + (f"; {len(needs)} labels still need a real title" if needs else ""),
    }


def repair_from_script(video: dict, episode: Path, episode_number: int) -> dict:
    authored, script_path = load_annotated_chapters(episode)
    if not authored:
        authored, script_path = load_markdown_chapters(episode, episode_number)
    if not authored:
        return {
            "method": "unresolved",
            "confidence": "none",
            "source": None,
            "chapters": [],
            "notes": [f"no script.annotated*.json with chapters[] and no script.en.v*.md with "
                      f"ACT headings under {episode.name}/03_script/ or episodes/_planning/"],
            "labels_needing_authoring": [],
            "needs_owner_review": "BLOCKED - chapter titles must be authored by hand",
        }
    cues, caption_path = load_captions(episode)
    if not cues:
        return {
            "method": "unresolved",
            "confidence": "none",
            "source": script_path,
            "chapters": [{"title": c["title"], "seconds": None} for c in authored],
            "notes": [f"chapter TITLES recovered from {script_path} but no caption track "
                      f"was found under {episode.name}/08_edit/, so no timestamps could "
                      f"be derived - the owner must time these against the render"],
            "labels_needing_authoring": [],
            "needs_owner_review": "BLOCKED - titles ready, timestamps missing",
        }

    chapters: list[dict] = []
    notes: list[str] = []
    weak = 0
    for index, chapter in enumerate(authored):
        seconds, ratio = align_span(chapter["first_span_text"], cues)
        if index == 0:
            seconds, ratio = 0.0, 1.0
        if seconds is None or ratio < ALIGN_MIN_RATIO:
            weak += 1
            notes.append(f"{chapter['title']!r}: caption alignment weak "
                         f"(best match {ratio:.2f}) - timestamp not trusted")
            continue
        chapters.append({"title": chapter["title"], "seconds": int(seconds), "align_ratio": round(ratio, 3)})

    kept, rule_notes = enforce_youtube_rules(chapters, video["duration_seconds"])
    kept, label_notes, needs = clean_labels(kept)
    kept, rule_notes2 = enforce_youtube_rules(kept, video["duration_seconds"])
    notes += rule_notes + label_notes + rule_notes2
    confidence = "medium" if weak == 0 else "low"
    review = "FULL - labels are the author's, every timestamp is derived"
    if needs:
        review = (f"FULL + {len(needs)} labels are production-internal "
                  f"({', '.join(needs[:4])}) and must be rewritten before publishing")
    return {
        "method": "rebuilt_from_annotated_script_aligned_to_captions",
        "confidence": confidence,
        "source": f"{script_path} + {caption_path}",
        "chapters": kept,
        "notes": notes,
        "labels_needing_authoring": needs,
        "needs_owner_review": review,
    }


# ----------------------------------------------------------------------- output


def build_markdown(report: dict) -> str:
    lines: list[str] = []
    add = lines.append
    add("# CHAPTER RESTORATION v001 - staged, nothing published")
    add("")
    add(f"- generated: `{report['generated_at']}`")
    add(f"- targets: **{report['summary']['targets']}** long-forms not showing chapters")
    add(f"- resolved: {report['summary']['resolved']} "
        f"(high confidence {report['summary']['high_confidence']}, "
        f"medium {report['summary']['medium_confidence']}, "
        f"low {report['summary']['low_confidence']})")
    add(f"- **blocked, need hand authoring: {report['summary']['blocked']}**")
    add(f"- chapter LABELS still reading as production-internal "
        f"(\"Hook\", \"Ending\", bare \"Act III\"): "
        f"**{report['summary']['total_labels_needing_authoring']} across "
        f"{report['summary']['videos_with_labels_needing_authoring']} videos** - "
        f"these must be rewritten before publishing, because YouTube indexes the "
        f"chapter text for key-moment search and \"Hook\" matches nothing a viewer types")
    add("")
    add("Review each block below line by line. Nothing here has been sent to YouTube; "
        "`scripts/stage_description_batch.py` folds the approved blocks into staged "
        "description text, which is also never published by these scripts.")
    add("")

    add("## Summary")
    add("")
    add("| video id | episode | was | method | confidence | chapters | review |")
    add("|---|---|---|---|---|---|---|")
    for item in report["items"]:
        add(f"| `{item['video_id']}` | {item['episode_id'] or '?'} | {item['state_before']} | "
            f"{item['repair']['method'][:34]} | {item['repair']['confidence']} | "
            f"{len(item['repair']['chapters'])} | {item['repair']['needs_owner_review'][:26]} |")
    add("")

    for item in report["items"]:
        repair = item["repair"]
        add(f"### {item['title']}")
        add("")
        add(f"- video: `{item['video_id']}` / {item['watch_url']}")
        add(f"- episode: `{item['episode_id']}` | runtime {item['duration_seconds']}s "
            f"| views {item['views']}")
        add(f"- previous state: **{item['state_before']}** | repair: `{repair['method']}` "
            f"| confidence **{repair['confidence']}**")
        add(f"- source: {repair['source'] or 'NONE'}")
        add(f"- review needed: **{repair['needs_owner_review']}**")
        add("")
        if repair["chapters"]:
            add("```")
            for chapter in repair["chapters"]:
                seconds = chapter["seconds"]
                stamp = format_timestamp(seconds) if seconds is not None else "?:??"
                flag = "    <-- REWRITE THIS LABEL" if chapter.get("needs_authoring") else ""
                add(f"{stamp} {chapter['title']}{flag}")
            add("```")
        else:
            add("_no chapter block could be staged_")
        add("")
        if repair["notes"]:
            add("Notes:")
            for note in repair["notes"]:
                add(f"- {note}")
            add("")
        valid = item["validation"]
        add(f"Validation: **{'PASS' if valid['youtube_valid'] else 'FAIL'}** "
            f"- {valid['chapter_count']} chapters, first at {valid['first_seconds']}s, "
            f"shortest chapter {valid['min_gap']}s")
        add("")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", nargs="*", default=None, help="Limit to these video ids.")
    args = parser.parse_args(argv)

    if not STATE.exists():
        print(f"missing {STATE} - run scripts/yt_distribution_state.py first")
        return 1
    state = json.loads(STATE.read_text(encoding="utf-8"))

    targets = [
        v for v in state["videos"]
        if v["is_long_form"] and v["privacy"] == "public" and not v["chapters"]["youtube_valid"]
    ]
    if args.only:
        targets = [v for v in targets if v["video_id"] in set(args.only)]
    print(f"{len(targets)} long-forms are not showing chapters")

    mapping = map_videos_to_episodes({v["video_id"] for v in targets})
    print(f"mapped {len(mapping)}/{len(targets)} to episode folders")

    items: list[dict] = []
    for video in sorted(targets, key=lambda v: -v["views"]):
        episode_id = mapping.get(video["video_id"])
        episode_dir = (ROOT / "episodes" / episode_id) if episode_id else None

        episode_number = int(episode_id.split("-")[2]) if episode_id else 0
        if video["chapters"]["state"] == "RENDER_BROKEN":
            repair = repair_render_broken(video)
        elif episode_dir and episode_dir.exists():
            repair = repair_from_script(video, episode_dir, episode_number)
        else:
            repair = {
                "method": "unresolved", "confidence": "none", "source": None,
                "chapters": [], "notes": ["no episode folder matched this video id"],
                "labels_needing_authoring": [],
                "needs_owner_review": "BLOCKED - no repo source",
            }

        chapters = repair["chapters"]
        seconds = [c["seconds"] for c in chapters if c["seconds"] is not None]
        gaps = [seconds[i + 1] - seconds[i] for i in range(len(seconds) - 1)]
        validation = {
            "chapter_count": len(chapters),
            "first_seconds": seconds[0] if seconds else None,
            "min_gap": min(gaps) if gaps else None,
            "youtube_valid": (
                len(chapters) >= MIN_CHAPTERS
                and len(seconds) == len(chapters)
                and seconds[0] == 0
                and all(gap >= MIN_CHAPTER_SECONDS for gap in gaps)
            ),
        }
        items.append({
            "video_id": video["video_id"],
            "title": video["title"],
            "episode_id": episode_id,
            "watch_url": video["watch_url"],
            "studio_url": video["studio_url"],
            "duration_seconds": video["duration_seconds"],
            "views": video["views"],
            "state_before": video["chapters"]["state"],
            "repair": repair,
            "validation": validation,
            "chapter_lines": [
                f"{format_timestamp(c['seconds'])} {c['title']}"
                for c in chapters if c["seconds"] is not None
            ],
        })

    resolved = [i for i in items if i["validation"]["youtube_valid"]]
    report = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "scripts/stage_chapter_restoration.py",
        "published": False,
        "measured_state": STATE.relative_to(ROOT).as_posix(),
        "summary": {
            "targets": len(items),
            "resolved": len(resolved),
            "blocked": len(items) - len(resolved),
            "high_confidence": sum(1 for i in resolved if i["repair"]["confidence"] == "high"),
            "medium_confidence": sum(1 for i in resolved if i["repair"]["confidence"] == "medium"),
            "low_confidence": sum(1 for i in resolved if i["repair"]["confidence"] == "low"),
            "videos_with_labels_needing_authoring": sum(
                1 for i in items if i["repair"].get("labels_needing_authoring")
            ),
            "total_labels_needing_authoring": sum(
                len(i["repair"].get("labels_needing_authoring") or []) for i in items
            ),
        },
        "items": items,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(build_markdown(report), encoding="utf-8")

    summary = report["summary"]
    print(f"resolved {summary['resolved']}/{summary['targets']} "
          f"(high {summary['high_confidence']}, medium {summary['medium_confidence']}, "
          f"low {summary['low_confidence']}), blocked {summary['blocked']}")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    return 1 if summary["blocked"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
