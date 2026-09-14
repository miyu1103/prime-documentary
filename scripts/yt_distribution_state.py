#!/usr/bin/env python3
"""READ-ONLY distribution-state audit for the PD channel (no writes, ever).

Measures, per video, the four "own-session machine" levers identified in
`episodes/_planning/DEEP_RESEARCH_FINDINGS.v001.md` section 5:

  1. chapters      -- does the live description carry a YouTube-valid chapter block?
  2. interlinks    -- does the live description link any other video / any playlist?
  3. playlists     -- is the video a member of any playlist owned by the channel?
  4. comments      -- is there any top-level comment thread authored by the channel?
                      (NOTE: `pinned` state is NOT exposed by the Data API - see
                      `api_capability_probes` in the output JSON.)

It also probes, read-only, whether end screens are reachable through the Data API.

HTTP methods used: GET only, plus the OAuth refresh-token POST to
`oauth2.googleapis.com/token` (that is authentication, not a channel write).
There is no `--apply` / `--execute` path in this script by design.

Outputs:
  episodes/_planning/measurements/DISTRIBUTION_STATE.v001.json
  episodes/_planning/measurements/DISTRIBUTION_STATE.v001.md   (readable table)

Exit codes: 0 ok, 2 bad channel, 3 auth failure.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
OUT_DIR = ROOT / "episodes" / "_planning" / "measurements"
OUT_JSON = OUT_DIR / "DISTRIBUTION_STATE.v001.json"
OUT_MD = OUT_DIR / "DISTRIBUTION_STATE.v001.md"

CHANNEL_ALLOWLIST = ("UCuQPtAz1rca9eJ4xhvX0yKA",)
SCHEMA_VERSION = "1.0.0"

# YouTube's Shorts ceiling is 3 minutes, NOT 60 seconds. This channel publishes
# Shorts in the 61-74s band, so a 60s cut misclassifies 11 of them as long-forms
# and inflates every denominator. Long-form = strictly longer than 180s.
SHORT_MAX_SECONDS = 180

TIMESTAMP_RE = re.compile(r"^\s*(?:(\d{1,2}):)?(\d{1,2}):(\d{2})\b", re.M)
VIDEO_LINK_RE = re.compile(
    r"(?:youtube\.com/watch\?[^\s]*\bv=|youtu\.be/|youtube\.com/shorts/)([A-Za-z0-9_-]{11})"
)
PLAYLIST_LINK_RE = re.compile(r"youtube\.com/playlist\?[^\s]*\blist=([A-Za-z0-9_-]+)")


# --------------------------------------------------------------------------- env


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


# -------------------------------------------------------------------------- http


def _request(method: str, url: str, *, headers=None, form=None) -> tuple[int, dict]:
    data = urllib.parse.urlencode(form).encode() if form else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as exc:
        try:
            return exc.code, json.loads(exc.read().decode("utf-8") or "{}")
        except Exception:
            return exc.code, {}


def get(url: str, token: str) -> dict:
    """GET a Data API url. Read-only by construction."""
    status, body = _request("GET", url, headers={"Authorization": f"Bearer {token}"})
    if status != 200:
        raise RuntimeError(f"GET {url.split('?')[0]} -> HTTP {status}: {body.get('error', {}).get('message')}")
    return body


def api(path: str, token: str, **params) -> dict:
    return get(f"https://www.googleapis.com/youtube/v3/{path}?" + urllib.parse.urlencode(params), token)


def access_token(env: dict[str, str]) -> str:
    status, body = _request(
        "POST",
        "https://oauth2.googleapis.com/token",
        form={
            "client_id": env["YOUTUBE_CLIENT_ID"],
            "client_secret": env["YOUTUBE_CLIENT_SECRET"],
            "refresh_token": env["YOUTUBE_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        },
    )
    if status != 200:
        raise RuntimeError(f"token refresh failed HTTP {status}: {body.get('error')}")
    return body["access_token"]


# ------------------------------------------------------------------- measurement


def iso_duration_seconds(value: str) -> int:
    match = re.match(r"^P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", value or "")
    if not match:
        return 0
    days, hours, minutes, seconds = (int(g) if g else 0 for g in match.groups())
    return ((days * 24 + hours) * 60 + minutes) * 60 + seconds


PLACEHOLDER_RE = re.compile(r"chapters? (?:finalized|to be finalized|tbd|pending)", re.I)


def parse_chapter_block(description: str) -> dict:
    """Return the chapter analysis for one description.

    Two DIFFERENT defects are separated here, because they need different fixes:

      * `has_chapter_block` - the author wrote a chapter list at all
        (>=3 timestamps, first one 0:00). False => the writing habit was skipped.
      * `youtube_valid` - YouTube will actually RENDER the block. YouTube
        additionally requires every chapter to be >=10 seconds. A block with a
        3-second chapter exists in the description but renders as plain text,
        so it produces zero key-moment / seek-bar benefit.
    """
    stamps: list[tuple[int, str]] = []
    for line in (description or "").splitlines():
        match = TIMESTAMP_RE.match(line)
        if not match:
            continue
        hours, minutes, seconds = match.group(1), match.group(2), match.group(3)
        total = (int(hours) if hours else 0) * 3600 + int(minutes) * 60 + int(seconds)
        label = line[match.end():].strip(" -–—:\t")
        stamps.append((total, label))

    count = len(stamps)
    starts_at_zero = bool(stamps) and stamps[0][0] == 0
    monotonic = all(stamps[i][0] < stamps[i + 1][0] for i in range(count - 1))
    min_gap = min((stamps[i + 1][0] - stamps[i][0] for i in range(count - 1)), default=0)
    has_block = count >= 3 and starts_at_zero and monotonic
    valid = has_block and min_gap >= 10
    placeholder = bool(PLACEHOLDER_RE.search(description or ""))

    if placeholder and not has_block:
        state = "PLACEHOLDER"
    elif valid:
        state = "OK"
    elif has_block:
        state = "RENDER_BROKEN"      # block written, but a <10s chapter kills rendering
    elif count:
        state = "FRAGMENT"           # a stray timestamp or two, no usable block
    else:
        state = "MISSING"            # habit skipped entirely

    return {
        "state": state,
        "timestamp_count": count,
        "starts_at_zero": starts_at_zero,
        "monotonic": monotonic,
        "min_gap_seconds": min_gap,
        "has_chapter_block": has_block,
        "youtube_valid": valid,
        "has_placeholder_text": placeholder,
        "short_chapters": [
            {"at": stamps[i][0], "label": stamps[i][1], "gap": stamps[i + 1][0] - stamps[i][0]}
            for i in range(count - 1)
            if stamps[i + 1][0] - stamps[i][0] < 10
        ],
        "stamps": [{"t": t, "label": label} for t, label in stamps],
        "first_labels": [label for _, label in stamps[:4]],
    }


def collect_uploads(token: str, uploads_playlist: str) -> list[str]:
    """Every video id in the uploads playlist, de-duplicated, order preserved.

    The uploads feed can hand back the same id on two pages while the channel is
    being written to; counting it twice silently inflates every total.
    """
    ids: list[str] = []
    seen: set[str] = set()
    page = None
    while True:
        params = {"part": "contentDetails", "maxResults": 50, "playlistId": uploads_playlist}
        if page:
            params["pageToken"] = page
        data = api("playlistItems", token, **params)
        for item in data.get("items", []):
            video_id = item["contentDetails"]["videoId"]
            if video_id not in seen:
                seen.add(video_id)
                ids.append(video_id)
        page = data.get("nextPageToken")
        if not page:
            return ids


def collect_owned_videos(token: str) -> list[str]:
    """Second enumeration source: `search.list(forMine=true)`.

    The uploads playlist is NOT a reliable census - it silently omitted a public
    11-minute video on this channel (bYcqabvvxak, published 2026-06-21), and the
    channel's own `statistics.videoCount` disagrees with both. Any audit built on
    the uploads feed alone under-counts. Costs 100 quota units per page.
    """
    ids: list[str] = []
    seen: set[str] = set()
    page = None
    while True:
        params = {"part": "id", "forMine": "true", "type": "video", "maxResults": 50}
        if page:
            params["pageToken"] = page
        try:
            data = api("search", token, **params)
        except RuntimeError as exc:
            print(f"  ! search.list(forMine) unavailable: {exc}")
            return ids
        for item in data.get("items", []):
            video_id = item.get("id", {}).get("videoId")
            if video_id and video_id not in seen:
                seen.add(video_id)
                ids.append(video_id)
        page = data.get("nextPageToken")
        if not page:
            return ids


def collect_playlists(token: str) -> list[dict]:
    playlists: list[dict] = []
    page = None
    while True:
        params = {"part": "snippet,contentDetails,status", "maxResults": 50, "mine": "true"}
        if page:
            params["pageToken"] = page
        data = api("playlists", token, **params)
        playlists += data.get("items", [])
        page = data.get("nextPageToken")
        if not page:
            break

    for playlist in playlists:
        items: list[dict] = []
        page = None
        while True:
            params = {"part": "contentDetails,snippet", "maxResults": 50, "playlistId": playlist["id"]}
            if page:
                params["pageToken"] = page
            data = api("playlistItems", token, **params)
            items += data.get("items", [])
            page = data.get("nextPageToken")
            if not page:
                break
        playlist["_items"] = [
            {
                "video_id": i["contentDetails"]["videoId"],
                "position": i["snippet"].get("position"),
                "title": i["snippet"].get("title"),
            }
            for i in items
        ]
    return playlists


def collect_channel_comment_threads(token: str, channel_id: str) -> dict[str, list[dict]]:
    """All top-level comment threads on the channel, grouped by video id.

    `commentThreads.list(allThreadsRelatedToChannelId=...)` is read-only.
    The API does NOT expose whether a comment is pinned.
    """
    by_video: dict[str, list[dict]] = {}
    page = None
    while True:
        params = {
            "part": "snippet",
            "maxResults": 100,
            "allThreadsRelatedToChannelId": channel_id,
        }
        if page:
            params["pageToken"] = page
        try:
            data = api("commentThreads", token, **params)
        except RuntimeError as exc:
            print(f"  ! commentThreads unavailable: {exc}")
            return by_video
        for thread in data.get("items", []):
            snippet = thread["snippet"]
            top = snippet.get("topLevelComment", {}).get("snippet", {})
            video_id = snippet.get("videoId")
            if not video_id:
                continue
            by_video.setdefault(video_id, []).append(
                {
                    "comment_id": thread["id"],
                    "author_channel_id": (top.get("authorChannelId") or {}).get("value"),
                    "is_channel_owner": (top.get("authorChannelId") or {}).get("value") == channel_id,
                    "text": (top.get("textOriginal") or "")[:200],
                    "published_at": top.get("publishedAt"),
                    "like_count": top.get("likeCount"),
                }
            )
        page = data.get("nextPageToken")
        if not page:
            return by_video


def probe_api_capabilities(token: str, sample_video_id: str | None) -> list[dict]:
    """Read-only probes documenting what the Data API can and cannot do here."""
    probes: list[dict] = []

    if sample_video_id:
        status, body = _request(
            "GET",
            "https://www.googleapis.com/youtube/v3/videos?"
            + urllib.parse.urlencode({"part": "endScreens", "id": sample_video_id}),
            headers={"Authorization": f"Bearer {token}"},
        )
        probes.append(
            {
                "probe": "videos.list?part=endScreens",
                "http_status": status,
                "error_reason": (body.get("error", {}).get("errors") or [{}])[0].get("reason"),
                "error_message": body.get("error", {}).get("message"),
                "conclusion": "END SCREENS ARE NOT READABLE OR WRITABLE VIA THE DATA API"
                if status != 200
                else "unexpected: endScreens part accepted - re-verify",
            }
        )

        status, body = _request(
            "GET",
            "https://www.googleapis.com/youtube/v3/videos?"
            + urllib.parse.urlencode({"part": "cards", "id": sample_video_id}),
            headers={"Authorization": f"Bearer {token}"},
        )
        probes.append(
            {
                "probe": "videos.list?part=cards",
                "http_status": status,
                "error_reason": (body.get("error", {}).get("errors") or [{}])[0].get("reason"),
                "error_message": body.get("error", {}).get("message"),
                "conclusion": "CARDS ARE NOT READABLE OR WRITABLE VIA THE DATA API"
                if status != 200
                else "unexpected: cards part accepted - re-verify",
            }
        )

    probes.append(
        {
            "probe": "comments.setModerationStatus / pin",
            "http_status": None,
            "conclusion": "NO PIN ENDPOINT EXISTS. `comments.insert` can post as the channel "
            "(a write - not performed here); pinning is Studio/app-manual only, and the "
            "pinned flag is not returned by commentThreads.list.",
        }
    )
    probes.append(
        {
            "probe": "playlists.insert / playlistItems.insert",
            "http_status": None,
            "conclusion": "WRITABLE via Data API (owner GO required). Quota 50 units per insert.",
        }
    )
    probes.append(
        {
            "probe": "videos.update?part=snippet (description/chapters)",
            "http_status": None,
            "conclusion": "WRITABLE via Data API (owner GO required). Quota 50 units per update. "
            "Full snippet must be sent or fields are cleared.",
        }
    )
    return probes


# ------------------------------------------------------------------------ report


def build_markdown(state: dict) -> str:
    longs = [v for v in state["videos"] if v["is_long_form"] and v["privacy"] == "public"]
    longs_sorted = sorted(longs, key=lambda v: v["published_at"])
    lines: list[str] = []
    add = lines.append

    add("# DISTRIBUTION STATE v001 - measured, read-only")
    add("")
    add(f"- measured_at: `{state['measured_at']}`")
    add(f"- channel: `{state['channel']['id']}` ({state['channel']['title']})")
    add(f"- videos total: {state['totals']['videos']} "
        f"(long-form {state['totals']['long_forms']}, shorts {state['totals']['shorts']})")
    add(f"- long-forms **public** {state['totals']['long_forms_public']} / "
        f"private-or-scheduled {state['totals']['long_forms_private_or_scheduled']}")
    add("")
    add("> All tables below count **public long-forms only** - a private/scheduled video has")
    add("> no distribution surface yet, and its description is still editable pre-publish.")
    add("")
    add("## Headline counts (public long-forms)")
    add("")
    t = state["totals"]
    cs = t["chapter_states"]
    add("| metric | value |")
    add("|---|---|")
    add(f"| public long-forms | {t['long_forms_public']} |")
    add(f"| chapters render correctly (`OK`) | {cs['OK']} |")
    add(f"| **no chapter block written at all** (`MISSING`) | **{cs['MISSING']}** |")
    add(f"| block written but YouTube will NOT render it (`RENDER_BROKEN`, a <10s chapter) | {cs['RENDER_BROKEN']} |")
    add(f"| published with placeholder chapter text (`PLACEHOLDER`) | {cs['PLACEHOLDER']} |")
    add(f"| stray timestamps only (`FRAGMENT`) | {cs['FRAGMENT']} |")
    add(f"| **total not showing chapters to viewers** | **{t['long_forms_without_valid_chapters']}** |")
    add(f"| description links another video | {t['long_forms_linking_a_video']} |")
    add(f"| description links a playlist | {t['long_forms_linking_a_playlist']} |")
    add(f"| member of >=1 playlist | {t['long_forms_in_a_playlist']} |")
    add(f"| has a channel-authored comment thread | {t['long_forms_with_owner_comment']} |")
    add(f"| has any external comment thread | {t['long_forms_with_external_comment']} |")
    add("")
    add(f"- playlists on channel: **{len(state['playlists'])}** covering "
        f"{t['distinct_videos_in_playlists']} distinct videos "
        f"({t['long_forms_in_a_playlist']} public long-forms)")
    add("")

    add("## Chapter regression timeline (public long-forms, `has_chapter_block`)")
    add("")
    add("| publish month | long-forms | with chapter block | without | actually rendering |")
    add("|---|---|---|---|---|")
    for month, row in sorted(state["chapter_regression_by_month"].items()):
        add(f"| {month} | {row['long_forms']} | {row['with_chapters']} | "
            f"{row['without_chapters']} | {row['rendering_ok']} |")
    add("")
    cut = state["chapter_regression_cutover"]
    add(f"- last long-form WITH a chapter block: `{cut['last_with_chapters']}` "
        f"(`{cut['last_with_chapters_video_id']}`)")
    add(f"- first long-form WITHOUT one after it: `{cut['first_without_after']}`")
    add(f"- **unbroken chapterless run at the tail: {cut['tail_chapterless_run']} videos**")
    add("")

    add("## Playlists on the channel")
    add("")
    add("| id | title | privacy | items | dead items | private items |")
    add("|---|---|---|---|---|---|")
    for playlist in state["playlists"]:
        add(f"| `{playlist['id']}` | {playlist['title']} | {playlist['privacy']} | "
            f"{playlist['item_count']} | {len(playlist['dead_items'])} | {len(playlist['private_items'])} |")
    add("")
    for playlist in state["playlists"]:
        if not (playlist["dead_items"] or playlist["private_items"]):
            continue
        add(f"**{playlist['title']}** has unviewable entries:")
        for item in playlist["dead_items"]:
            add(f"- position {item['position']}: `{item['video_id']}` \"{item['title']}\" "
                f"- unresolved (deleted / not owned)")
        for item in playlist["private_items"]:
            add(f"- position {item['position']}: `{item['video_id']}` \"{item['title']}\" - not public")
        add("")

    add("## Enumeration cross-check")
    add("")
    enum = state["enumeration"]
    add(f"- uploads playlist: {enum['uploads_playlist_count']}")
    add(f"- `search.list(forMine=true)`: {enum['search_for_mine_count']}")
    add(f"- union used by this audit: **{enum['union_count']}**")
    add(f"- channel `statistics.videoCount`: {enum['channel_statistics_video_count']}")
    if enum["missing_from_uploads_playlist"]:
        add(f"- **videos the uploads playlist omits** ({len(enum['missing_from_uploads_playlist'])}): "
            + ", ".join(f"`{v}`" for v in enum["missing_from_uploads_playlist"]))
    if enum["missing_from_search"]:
        add(f"- videos search omits ({len(enum['missing_from_search'])}): "
            + ", ".join(f"`{v}`" for v in enum["missing_from_search"][:15])
            + (" ..." if len(enum["missing_from_search"]) > 15 else ""))
    add("")
    add("> Any audit that enumerates from the uploads playlist alone under-counts this channel.")
    add("")

    add("## Per long-form state (oldest first)")
    add("")
    add("| # | published | video id | title | dur | views | chapters | links vid | links pl | in playlist | owner comment |")
    add("|---|---|---|---|---|---|---|---|---|---|---|")
    for index, video in enumerate(longs_sorted, 1):
        title = video["title"].replace("|", "/")[:58]
        add(
            f"| {index} | {video['published_at'][:10]} | `{video['video_id']}` | {title} | "
            f"{video['duration_seconds'] // 60}m | {video['views']} | {video['chapters']['state']} | "
            f"{'yes' if video['links_video_ids'] else 'no'} | "
            f"{'yes' if video['links_playlist_ids'] else 'no'} | "
            f"{','.join(video['in_playlists']) or 'NONE'} | "
            f"{'yes' if video['owner_comment_count'] else 'no'} |"
        )
    add("")

    add("## Long-forms not showing chapters (restoration targets, highest views first)")
    add("")
    add("| views | published | video id | state | title | fix needed |")
    add("|---|---|---|---|---|---|")
    fix_text = {
        "MISSING": "author a full chapter block",
        "RENDER_BROKEN": "merge/extend the <10s chapters, keep the rest",
        "PLACEHOLDER": "replace placeholder line with the real block",
        "FRAGMENT": "author a full chapter block",
    }
    for video in sorted(longs_sorted, key=lambda v: -v["views"]):
        chapters = video["chapters"]
        if chapters["youtube_valid"]:
            continue
        add(
            f"| {video['views']} | {video['published_at'][:10]} | `{video['video_id']}` | "
            f"{chapters['state']} | {video['title'].replace('|', '/')[:52]} | "
            f"{fix_text.get(chapters['state'], '')} |"
        )
    add("")

    add("## API capability probes (read-only evidence)")
    add("")
    for probe in state["api_capability_probes"]:
        add(f"- **{probe['probe']}** -> HTTP `{probe['http_status']}` "
            f"{('(' + str(probe.get('error_reason')) + ')') if probe.get('error_reason') else ''}")
        add(f"  - {probe['conclusion']}")
    add("")
    add("_This file is generated by `scripts/yt_distribution_state.py`. "
        "The script performs GET requests only; it has no write path._")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-json", default=str(OUT_JSON))
    parser.add_argument("--out-md", default=str(OUT_MD))
    parser.add_argument("--skip-comments", action="store_true", help="Skip the commentThreads sweep.")
    args = parser.parse_args(argv)

    env = load_env()
    token = access_token(env)

    channel = api("channels", token, part="snippet,statistics,contentDetails", mine="true")["items"][0]
    channel_id = channel["id"]
    if channel_id not in CHANNEL_ALLOWLIST:
        print(f"REFUSING: channel {channel_id!r} is not in the allowlist {CHANNEL_ALLOWLIST}")
        return 2
    uploads_playlist = channel["contentDetails"]["relatedPlaylists"]["uploads"]
    print(f"channel {channel_id} ({channel['snippet']['title']}) uploads={uploads_playlist}")

    uploads_ids = collect_uploads(token, uploads_playlist)
    search_ids = collect_owned_videos(token)
    video_ids = list(dict.fromkeys(uploads_ids + search_ids))
    only_in_search = [v for v in search_ids if v not in set(uploads_ids)]
    only_in_uploads = [v for v in uploads_ids if v not in set(search_ids)]
    enumeration = {
        "uploads_playlist_count": len(uploads_ids),
        "search_for_mine_count": len(search_ids),
        "union_count": len(video_ids),
        "channel_statistics_video_count": channel["statistics"].get("videoCount"),
        "missing_from_uploads_playlist": only_in_search,
        "missing_from_search": only_in_uploads,
        "note": "The uploads playlist is not a complete census; the union of both "
                "sources is used. Discrepancies are listed so they can be re-checked.",
    }
    print(f"uploads={len(uploads_ids)} search={len(search_ids)} union={len(video_ids)} "
          f"(uploads-feed gap: {len(only_in_search)})")

    items: list[dict] = []
    seen_ids: set[str] = set()
    for start in range(0, len(video_ids), 50):
        chunk = video_ids[start:start + 50]
        for item in api(
            "videos", token,
            part="snippet,status,statistics,contentDetails",
            id=",".join(chunk),
            maxResults=50,
        ).get("items", []):
            if item["id"] in seen_ids:
                continue
            seen_ids.add(item["id"])
            items.append(item)
    print(f"fetched: {len(items)} unique video records")

    playlists = collect_playlists(token)
    print(f"playlists: {len(playlists)}")
    membership: dict[str, list[str]] = {}
    for playlist in playlists:
        for entry in playlist["_items"]:
            membership.setdefault(entry["video_id"], []).append(playlist["id"])

    comments_by_video: dict[str, list[dict]] = {}
    if not args.skip_comments:
        comments_by_video = collect_channel_comment_threads(token, channel_id)
        print(f"comment threads on {len(comments_by_video)} videos")

    videos: list[dict] = []
    for item in items:
        snippet, status = item["snippet"], item["status"]
        stats, details = item.get("statistics", {}), item.get("contentDetails", {})
        description = snippet.get("description", "") or ""
        seconds = iso_duration_seconds(details.get("duration", ""))
        own_id = item["id"]
        linked_videos = sorted({v for v in VIDEO_LINK_RE.findall(description) if v != own_id})
        linked_playlists = sorted(set(PLAYLIST_LINK_RE.findall(description)))
        threads = comments_by_video.get(own_id, [])
        videos.append(
            {
                "video_id": own_id,
                "title": snippet.get("title"),
                "published_at": snippet.get("publishedAt"),
                "privacy": status.get("privacyStatus"),
                "publish_at_scheduled": status.get("publishAt"),
                "duration_seconds": seconds,
                "is_long_form": seconds > SHORT_MAX_SECONDS,
                "views": int(stats.get("viewCount", 0) or 0),
                "likes": int(stats.get("likeCount", 0) or 0),
                "comment_count": int(stats.get("commentCount", 0) or 0),
                "description_length": len(description),
                # Kept verbatim so the staging scripts can diff a proposed rewrite
                # against exactly what is live, without re-hitting the API.
                "description_text": description,
                "chapters": parse_chapter_block(description),
                "links_video_ids": linked_videos,
                "links_playlist_ids": linked_playlists,
                "in_playlists": sorted(membership.get(own_id, [])),
                "owner_comment_count": sum(1 for t in threads if t["is_channel_owner"]),
                "external_comment_count": sum(1 for t in threads if not t["is_channel_owner"]),
                "watch_url": f"https://youtu.be/{own_id}",
                "studio_url": f"https://studio.youtube.com/video/{own_id}/edit",
            }
        )

    videos.sort(key=lambda v: v["published_at"])
    resolved = {v["video_id"]: v for v in videos}
    longs = [v for v in videos if v["is_long_form"]]
    public_longs = [v for v in longs if v["privacy"] == "public"]

    by_month: dict[str, dict[str, int]] = {}
    for video in public_longs:
        month = video["published_at"][:7]
        row = by_month.setdefault(
            month,
            {"long_forms": 0, "with_chapters": 0, "without_chapters": 0, "rendering_ok": 0},
        )
        row["long_forms"] += 1
        if video["chapters"]["has_chapter_block"]:
            row["with_chapters"] += 1
        else:
            row["without_chapters"] += 1
        if video["chapters"]["youtube_valid"]:
            row["rendering_ok"] += 1

    # The regression is about the WRITING habit dying, so measure on has_chapter_block.
    with_block = [v for v in public_longs if v["chapters"]["has_chapter_block"]]
    last_with = with_block[-1]["published_at"][:10] if with_block else None
    last_with_id = with_block[-1]["video_id"] if with_block else None
    first_without_after = None
    if last_with:
        after = [v for v in public_longs if v["published_at"][:10] > last_with]
        missing_after = [v for v in after if not v["chapters"]["has_chapter_block"]]
        first_without_after = missing_after[0]["published_at"][:10] if missing_after else None
    tail_run = 0
    for video in reversed(public_longs):
        if video["chapters"]["has_chapter_block"]:
            break
        tail_run += 1

    state = {
        "schema_version": SCHEMA_VERSION,
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "generator": "scripts/yt_distribution_state.py",
        "read_only": True,
        "channel": {
            "id": channel_id,
            "title": channel["snippet"].get("title"),
            "subscribers": channel["statistics"].get("subscriberCount"),
            "views": channel["statistics"].get("viewCount"),
            "video_count": channel["statistics"].get("videoCount"),
            "uploads_playlist": uploads_playlist,
        },
        "enumeration": enumeration,
        "definitions": {
            "long_form": f"contentDetails.duration > {SHORT_MAX_SECONDS}s",
            "chapters_youtube_valid": ">=3 timestamps AND first is 0:00 AND strictly increasing AND every gap >=10s",
            "links_video": "description contains a youtu.be / watch?v= / shorts/ link to a different video id",
        },
        "playlists": [
            {
                "id": p["id"],
                "title": p["snippet"].get("title"),
                "description": p["snippet"].get("description"),
                "privacy": p.get("status", {}).get("privacyStatus"),
                "item_count": len(p["_items"]),
                # A playlist item pointing at a deleted or private video is invisible
                # to viewers but still occupies its position - including position 0,
                # the slot the playlist link lands on.
                "dead_items": [i for i in p["_items"] if i["video_id"] not in resolved],
                "private_items": [
                    i for i in p["_items"]
                    if resolved.get(i["video_id"], {}).get("privacy") not in (None, "public")
                ],
                "items": p["_items"],
            }
            for p in playlists
        ],
        "totals": {
            "videos": len(videos),
            "long_forms": len(longs),
            "long_forms_public": len(public_longs),
            "long_forms_private_or_scheduled": len(longs) - len(public_longs),
            "shorts": len(videos) - len(longs),
            "chapter_states": {
                state: sum(1 for v in public_longs if v["chapters"]["state"] == state)
                for state in ("OK", "RENDER_BROKEN", "PLACEHOLDER", "FRAGMENT", "MISSING")
            },
            "long_forms_with_valid_chapters": sum(1 for v in public_longs if v["chapters"]["youtube_valid"]),
            "long_forms_without_valid_chapters": sum(1 for v in public_longs if not v["chapters"]["youtube_valid"]),
            "long_forms_without_any_chapter_block": sum(
                1 for v in public_longs if not v["chapters"]["has_chapter_block"]
            ),
            "long_forms_linking_a_video": sum(1 for v in public_longs if v["links_video_ids"]),
            "long_forms_linking_a_playlist": sum(1 for v in public_longs if v["links_playlist_ids"]),
            "long_forms_in_a_playlist": sum(1 for v in public_longs if v["in_playlists"]),
            "long_forms_with_owner_comment": sum(1 for v in public_longs if v["owner_comment_count"]),
            "long_forms_with_external_comment": sum(1 for v in public_longs if v["external_comment_count"]),
            "distinct_videos_in_playlists": len(membership),
        },
        "chapter_regression_by_month": by_month,
        "chapter_regression_cutover": {
            "basis": "public long-forms, has_chapter_block (the writing habit)",
            "last_with_chapters": last_with,
            "last_with_chapters_video_id": last_with_id,
            "first_without_after": first_without_after,
            "tail_chapterless_run": tail_run,
        },
        "api_capability_probes": probe_api_capabilities(token, longs[0]["video_id"] if longs else None),
        "videos": videos,
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    Path(args.out_md).write_text(build_markdown(state), encoding="utf-8")

    t = state["totals"]
    print(
        f"\nlong-forms={t['long_forms']} "
        f"missing_chapters={t['long_forms_without_valid_chapters']} "
        f"linking_video={t['long_forms_linking_a_video']} "
        f"in_playlist={t['long_forms_in_a_playlist']} "
        f"owner_comment={t['long_forms_with_owner_comment']}"
    )
    print(f"wrote {out_json}")
    print(f"wrote {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
