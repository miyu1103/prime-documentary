#!/usr/bin/env python3
"""Execute the approved PD series-playlist plan against the live channel.

This module owns ONE responsibility: performing the playlist writes that
`scripts/plan_series_playlists.py` has already planned, verified and gated.
It is never invoked directly from the command line - the guard chain in
`plan_series_playlists.py` (`--execute` + `--owner-approval` + `--confirm` +
`config.status == "approved"` + zero validation errors) is the only entry point.

Design constraints, all of them load-bearing:

* **Scope fence.** Only `playlists` and `playlistItems` endpoints may be
  contacted. Every planned call is checked against that fence *before* the
  first write, and every outgoing request is re-checked at send time. A call
  that would touch a video's title, description, thumbnail, visibility,
  schedule, chapters, comments or end screens aborts the run (APR-0006 scope).
* **Verify-then-proceed.** After every write the affected resource is re-read
  with a GET and compared against the intended state. The first mismatch
  aborts the whole run, leaving a resumable state file.
* **Resumable + idempotent.** Every completed step is recorded to
  `episodes/_planning/measurements/PLAYLIST_EXECUTION.v001.json` with the ids
  the API returned. Re-running skips completed steps, and a playlist that a
  previous run created is adopted rather than created again (an existing
  same-title playlist owned by the channel is also adopted, so a crash between
  "insert succeeded" and "state written" cannot produce a duplicate).
* **Budget fence.** The run may not exceed the approved call count / quota
  units recorded in the plan. It aborts rather than overrun.

Positions are resolved live, never trusted from the plan. The plan's own call
list annotates playlist-item ids as "re-read at execution time" because a
`playlistItems.insert` at position N shifts every later item down by one: the
plan's literal position arguments were computed against the pre-write state and
do not survive their own inserts. The executor therefore converges each
playlist onto the approved order in `config/distribution/series_clusters.v001.json`
one index at a time, which is the outcome the owner approved.

Side effects: HTTP writes to the YouTube Data API v3 (playlists, playlistItems)
for the allowlisted channel only. Quota: 50 units per write, 1 per read.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
from yt_distribution_state import (  # noqa: E402  - shared read-only helpers, do not duplicate
    CHANNEL_ALLOWLIST,
    access_token,
    api,
    load_env,
)

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "episodes" / "_planning" / "measurements" / "PLAYLIST_EXECUTION.v001.json"
API_BASE = "https://www.googleapis.com/youtube/v3"

#: The only endpoints APR-0006 authorises. Anything else aborts before a write.
ALLOWED_ENDPOINTS = frozenset({"playlists", "playlistItems"})
ALLOWED_OPS = frozenset({
    "playlists.insert", "playlists.update",
    "playlistItems.insert", "playlistItems.update", "playlistItems.delete",
})
WRITE_QUOTA = 50
READ_QUOTA = 1

#: Transient conditions worth retrying. A hard `quotaExceeded` is NOT retried -
#: the daily allowance does not come back within a backoff window.
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
RETRY_REASONS = frozenset({"rateLimitExceeded", "userRateLimitExceeded", "backendError", "internalError"})
BACKOFF_SECONDS = (2, 5, 15, 45)
POLITE_SLEEP_SECONDS = 0.6


class Aborted(RuntimeError):
    """Raised on any mismatch, scope breach or budget breach. Ends the run."""


# --------------------------------------------------------------------------- io


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def _endpoint_of(url: str) -> str:
    """The Data API resource name a url addresses, e.g. 'playlistItems'."""
    path = urllib.parse.urlsplit(url).path
    return path.rsplit("/", 1)[-1]


def _assert_in_scope(url: str, op: str) -> None:
    endpoint = _endpoint_of(url)
    if endpoint not in ALLOWED_ENDPOINTS:
        raise Aborted(
            f"SCOPE BREACH: {op} targets endpoint {endpoint!r}; APR-0006 authorises "
            f"only {sorted(ALLOWED_ENDPOINTS)}. Refusing to send."
        )
    if op not in ALLOWED_OPS:
        raise Aborted(f"SCOPE BREACH: operation {op!r} is not one of {sorted(ALLOWED_OPS)}.")


# ------------------------------------------------------------------------- http


def _send(method: str, url: str, token: str, body: dict | None) -> tuple[int, dict]:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
            return response.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as exc:
        try:
            raw = exc.read().decode("utf-8")
            return exc.code, (json.loads(raw) if raw.strip() else {})
        except Exception:
            return exc.code, {}


class Executor:
    """Performs the approved writes, verifying each one before the next."""

    def __init__(self, config: dict, plan: dict, approval_id: str,
                 state_path: Path = STATE_PATH, log: Callable[[str], None] = print) -> None:
        self.config = config
        self.plan = plan
        self.approval_id = approval_id
        self.state_path = state_path
        self.log = log
        self.env = load_env()
        self.token = access_token(self.env)
        self.request_no = 0
        self.max_calls = int(plan["total_calls"])
        self.max_quota = int(plan["total_quota_units"])
        self.state = self._load_state()

    # ------------------------------------------------------------- state file

    def _load_state(self) -> dict:
        if self.state_path.exists():
            state = json.loads(self.state_path.read_text(encoding="utf-8"))
            self.log(f"resuming from {self.state_path.name}: "
                     f"{len(state.get('completed_steps', {}))} step(s) already done, "
                     f"{state.get('quota_used', 0)} quota units already spent")
            state.setdefault("runs", []).append({"started_at": _utcnow(), "approval": self.approval_id})
            state["status"] = "in_progress"
            return state
        return {
            "schema_version": "1.0.0",
            "generator": "scripts/yt_playlist_executor.py",
            "approval_record": self.approval_id,
            "design_revision": self.config["revision"],
            "plan_total_calls": self.max_calls,
            "plan_total_quota_units": self.max_quota,
            "runs": [{"started_at": _utcnow(), "approval": self.approval_id}],
            "status": "in_progress",
            "abort_reason": None,
            "channel_id": None,
            "playlist_ids": {},
            "completed_steps": {},
            "call_log": [],
            "write_calls": 0,
            "read_calls": 0,
            "quota_used": 0,
        }

    def _save(self) -> None:
        _write_atomic(self.state_path,
                      json.dumps(self.state, ensure_ascii=False, indent=2) + "\n")

    def _done(self, key: str) -> dict | None:
        return self.state["completed_steps"].get(key)

    def _record(self, key: str, payload: dict) -> None:
        self.state["completed_steps"][key] = {"at": _utcnow(), **payload}
        self._save()

    # ----------------------------------------------------------------- budget

    def _charge(self, quota: int, is_write: bool) -> None:
        projected = self.state["quota_used"] + quota
        if is_write:
            if self.state["write_calls"] + 1 > self.max_calls:
                raise Aborted(
                    f"BUDGET BREACH: this would be write call "
                    f"{self.state['write_calls'] + 1} of an approved maximum {self.max_calls}."
                )
            if projected > self.max_quota + READ_QUOTA * 400:
                raise Aborted(f"BUDGET BREACH: projected quota {projected} exceeds approval.")
            self.state["write_calls"] += 1
        else:
            self.state["read_calls"] += 1
        self.state["quota_used"] = projected

    # ------------------------------------------------------------- transport

    def _call(self, method: str, url: str, *, op: str, body: dict | None = None,
              is_write: bool) -> dict:
        """Send one API call with scope fence, budget charge, retry and logging."""
        if is_write:
            _assert_in_scope(url, op)
        self._charge(WRITE_QUOTA if is_write else READ_QUOTA, is_write)
        self.request_no += 1
        request_no = self.request_no

        attempt = 0
        while True:
            status, payload = _send(method, url, self.token, body)
            reason = ((payload.get("error", {}).get("errors") or [{}])[0]).get("reason")
            if status in (200, 204):
                break
            retryable = status in RETRY_STATUSES or (status == 403 and reason in RETRY_REASONS)
            if retryable and attempt < len(BACKOFF_SECONDS):
                wait = BACKOFF_SECONDS[attempt]
                self.log(f"  req#{request_no} {op} -> HTTP {status} ({reason}); "
                         f"retry {attempt + 1}/{len(BACKOFF_SECONDS)} in {wait}s")
                time.sleep(wait)
                attempt += 1
                continue
            entry = {
                "request_no": request_no, "at": _utcnow(), "op": op, "method": method,
                "endpoint": _endpoint_of(url), "http_status": status,
                "error_reason": reason,
                "error_message": payload.get("error", {}).get("message"),
                "is_write": is_write,
            }
            self.state["call_log"].append(entry)
            self._save()
            raise Aborted(f"{op} failed: HTTP {status} ({reason}) "
                          f"{payload.get('error', {}).get('message')}")

        entry = {
            "request_no": request_no, "at": _utcnow(), "op": op, "method": method,
            "endpoint": _endpoint_of(url), "http_status": status,
            "response_id": payload.get("id"), "response_etag": payload.get("etag"),
            "is_write": is_write, "retries": attempt,
        }
        if is_write:
            self.state["call_log"].append(entry)
            self._save()
            self.log(f"  req#{request_no} {op} -> HTTP {status} id={payload.get('id')}")
            time.sleep(POLITE_SLEEP_SECONDS)
        return payload

    # ------------------------------------------------------------------ reads

    def _get(self, path: str, **params: Any) -> dict:
        url = f"{API_BASE}/{path}?" + urllib.parse.urlencode(params)
        return self._call("GET", url, op=f"{path}.list", is_write=False)

    def playlist_items(self, playlist_id: str) -> list[dict]:
        """Live items of a playlist, ordered by position (verification source)."""
        items: list[dict] = []
        page = None
        while True:
            params = {"part": "snippet,contentDetails,status", "maxResults": 50,
                      "playlistId": playlist_id}
            if page:
                params["pageToken"] = page
            data = self._get("playlistItems", **params)
            for item in data.get("items", []):
                items.append({
                    "item_id": item["id"],
                    "video_id": item["contentDetails"]["videoId"],
                    "position": item["snippet"].get("position"),
                    "title": item["snippet"].get("title"),
                    "privacy": (item.get("status") or {}).get("privacyStatus"),
                })
            page = data.get("nextPageToken")
            if not page:
                break
        return sorted(items, key=lambda i: i["position"])

    def playlist(self, playlist_id: str) -> dict | None:
        data = self._get("playlists", part="snippet,status,contentDetails", id=playlist_id)
        items = data.get("items") or []
        return items[0] if items else None

    def my_playlists(self) -> list[dict]:
        playlists: list[dict] = []
        page = None
        while True:
            params = {"part": "snippet,status", "maxResults": 50, "mine": "true"}
            if page:
                params["pageToken"] = page
            data = self._get("playlists", **params)
            playlists += data.get("items", [])
            page = data.get("nextPageToken")
            if not page:
                return playlists

    def video_exists(self, video_id: str) -> bool:
        return bool((self._get("videos", part="id", id=video_id).get("items") or []))

    # ------------------------------------------------------------ preflight

    def preflight(self) -> None:
        """Everything that must hold before the first write."""
        channel = self._get("channels", part="id", mine="true")["items"][0]
        if channel["id"] not in CHANNEL_ALLOWLIST:
            raise Aborted(f"channel {channel['id']!r} is not allowlisted {CHANNEL_ALLOWLIST}")
        if self.state["channel_id"] and self.state["channel_id"] != channel["id"]:
            raise Aborted("state file belongs to a different channel")
        self.state["channel_id"] = channel["id"]
        self.log(f"channel confirmed: {channel['id']}")

        # Scope fence over the entire approved plan, before anything is sent.
        for call in self.plan["calls"]:
            _assert_in_scope(call["url"], call["op"])
        self.log(f"scope fence: all {len(self.plan['calls'])} planned calls target "
                 f"{sorted(ALLOWED_ENDPOINTS)} only")

        if self.plan["design_status"] != "approved" or not self.plan["validation"]["passed"]:
            raise Aborted("plan is not an approved, validated plan")

        # Exactly one delete is approved, and only for a dead item.
        deletes = [c for c in self.plan["calls"] if c["op"] == "playlistItems.delete"]
        if len(deletes) != 1:
            raise Aborted(f"expected exactly 1 approved delete, plan has {len(deletes)}")
        self._save()

    # ------------------------------------------------------------- playlists

    def ensure_playlist(self, spec: dict) -> str:
        """Return the playlist id for `spec`, creating it only if it truly does not exist."""
        key = spec["key"]
        step = f"{key}:playlist"

        recorded = self.state["playlist_ids"].get(key)
        if recorded:
            live = self.playlist(recorded)
            if live is None:
                raise Aborted(f"{key}: recorded playlist {recorded} no longer exists")
            self.log(f"{key}: adopting playlist {recorded} from state file")
            return recorded

        if spec["action"] != "create_new" and spec.get("existing_playlist_id"):
            playlist_id = spec["existing_playlist_id"]
            live = self.playlist(playlist_id)
            if live is None:
                raise Aborted(f"{key}: existing playlist {playlist_id} not found on the channel")
            self.state["playlist_ids"][key] = playlist_id
            self._save()
            self.log(f"{key}: reusing existing playlist {playlist_id} "
                     f"({live['snippet'].get('title')!r})")
            return playlist_id

        # create_new. Duplicate guard: adopt a same-title playlist the channel
        # already owns (a previous run may have created it and died before the
        # state file was written).
        for existing in self.my_playlists():
            if (existing["snippet"].get("title") or "").strip() == spec["title"].strip():
                self.state["playlist_ids"][key] = existing["id"]
                self._save()
                self.log(f"{key}: adopting pre-existing playlist {existing['id']} "
                         f"with the target title (no duplicate created)")
                return existing["id"]

        body = {
            "snippet": {"title": spec["title"], "description": spec["description"],
                        "defaultLanguage": "en"},
            "status": {"privacyStatus": spec["privacy"]},
        }
        created = self._call("POST", f"{API_BASE}/playlists?part=snippet,status",
                             op="playlists.insert", body=body, is_write=True)
        playlist_id = created["id"]

        live = self.playlist(playlist_id)  # verify-then-proceed
        if live is None:
            raise Aborted(f"{key}: playlists.insert returned {playlist_id} but a read-back found nothing")
        if (live["snippet"].get("title") or "") != spec["title"]:
            raise Aborted(f"{key}: created playlist title {live['snippet'].get('title')!r} "
                          f"!= intended {spec['title']!r}")
        if (live.get("status") or {}).get("privacyStatus") != spec["privacy"]:
            raise Aborted(f"{key}: created playlist privacy mismatch")

        self.state["playlist_ids"][key] = playlist_id
        self._record(step, {"op": "playlists.insert", "playlist_id": playlist_id,
                            "title": spec["title"]})
        self.log(f"{key}: created and verified playlist {playlist_id}")
        return playlist_id

    def ensure_metadata(self, spec: dict, playlist_id: str) -> None:
        """Title/description/privacy of an existing playlist -> the approved values."""
        key = spec["key"]
        step = f"{key}:playlists.update"
        if self._done(step):
            self.log(f"{key}: metadata update already completed, skipping")
            return

        live = self.playlist(playlist_id)
        if live is None:
            raise Aborted(f"{key}: playlist {playlist_id} vanished")
        snippet = live["snippet"]
        was_title = snippet.get("title")
        was_description = snippet.get("description")
        if was_title == spec["title"] and was_description == spec["description"]:
            self.log(f"{key}: metadata already matches the design, no write needed")
            self._record(step, {"op": "playlists.update", "skipped": "already matching",
                                "playlist_id": playlist_id})
            return

        body = {
            "id": playlist_id,
            "snippet": {"title": spec["title"], "description": spec["description"],
                        "defaultLanguage": "en"},
            "status": {"privacyStatus": spec["privacy"]},
        }
        self._call("PUT", f"{API_BASE}/playlists?part=snippet,status",
                   op="playlists.update", body=body, is_write=True)

        after = self.playlist(playlist_id)  # verify-then-proceed
        if after is None or after["snippet"].get("title") != spec["title"]:
            raise Aborted(f"{key}: playlists.update did not take effect "
                          f"(title is {after and after['snippet'].get('title')!r})")
        if after["snippet"].get("description") != spec["description"]:
            raise Aborted(f"{key}: playlists.update description mismatch after read-back")

        self._record(step, {"op": "playlists.update", "playlist_id": playlist_id,
                            "was_title": was_title, "was_description": was_description,
                            "now_title": spec["title"]})
        changed = ("title" if was_title != spec["title"] else "") + \
                  ("+description" if was_description != spec["description"] else "")
        self.log(f"{key}: metadata updated ({changed.strip('+')}): "
                 f"{was_title!r} -> {spec['title']!r} (verified)")

    # ----------------------------------------------------------- dead items

    def remove_dead_items(self, spec: dict, playlist_id: str) -> None:
        """Delete ONLY the approved dead-video placeholder(s), after proving what they are."""
        key = spec["key"]
        approved = [c for c in self.plan["calls"]
                    if c["op"] == "playlistItems.delete" and c["playlist_key"] == key]
        for call in approved:
            # The plan's url is a placeholder ("re-read at execution time"); the
            # video id is the only durable identifier in it.
            video_id = call["url"].split("for ")[1].split(" ")[0]
            step = f"{key}:playlistItems.delete:{video_id}"
            if self._done(step):
                self.log(f"{key}: delete of {video_id} already completed, skipping")
                continue

            items = self.playlist_items(playlist_id)
            matches = [i for i in items if i["video_id"] == video_id]
            if not matches:
                self.log(f"{key}: {video_id} is no longer in the playlist; nothing to delete")
                self._record(step, {"op": "playlistItems.delete", "skipped": "already absent",
                                    "video_id": video_id})
                continue
            if len(matches) != 1:
                raise Aborted(f"{key}: {video_id} appears {len(matches)} times; refusing to delete")
            item = matches[0]

            # Three independent proofs that this is the approved dead placeholder.
            if item["position"] != 0:
                raise Aborted(f"{key}: {video_id} is at position {item['position']}, not 0. "
                              "The approval covers only the position-0 placeholder. Aborting.")
            if self.video_exists(video_id):
                raise Aborted(f"{key}: video {video_id} EXISTS. The approval covers only a "
                              "deleted-video placeholder. Refusing to delete a live video's item.")
            if (item["title"] or "").strip().lower() not in ("deleted video", "private video"):
                raise Aborted(f"{key}: item title {item['title']!r} is not a deleted-video "
                              "placeholder. Aborting rather than guessing.")

            self.log(f"{key}: verified {video_id} is a deleted-video placeholder at position 0 "
                     f"(title {item['title']!r}, videos.list returns nothing) - deleting")
            url = f"{API_BASE}/playlistItems?" + urllib.parse.urlencode({"id": item["item_id"]})
            self._call("DELETE", url, op="playlistItems.delete", is_write=True)

            after = self.playlist_items(playlist_id)  # verify-then-proceed
            if any(i["item_id"] == item["item_id"] for i in after):
                raise Aborted(f"{key}: playlistItems.delete did not remove {item['item_id']}")
            if any(i["video_id"] == video_id for i in after):
                raise Aborted(f"{key}: {video_id} is still present after the delete")

            self._record(step, {"op": "playlistItems.delete", "playlist_id": playlist_id,
                                "playlist_item_id": item["item_id"], "video_id": video_id,
                                "was_title": item["title"], "was_position": 0})
            self.log(f"{key}: deleted placeholder item {item['item_id']} (verified gone)")

    # ---------------------------------------------------------------- order

    def converge_order(self, spec: dict, playlist_id: str) -> None:
        """Drive the playlist to the approved order, one index at a time.

        Positions come from a live read before every decision. Indices below the
        cursor are already final, so each operation is the only one that can put
        the right video at the cursor.
        """
        key = spec["key"]
        target = [entry["video_id"] for entry in spec["order"]]
        items = self.playlist_items(playlist_id)

        for index, video_id in enumerate(target):
            current = [i["video_id"] for i in items]
            if index < len(current) and current[index] == video_id:
                continue

            present = [i for i in items if i["video_id"] == video_id]
            if len(present) > 1:
                raise Aborted(f"{key}: {video_id} appears {len(present)} times in the playlist")

            if present:
                item = present[0]
                step = f"{key}:playlistItems.update:{video_id}:{index}"
                body = {
                    "id": item["item_id"],
                    "snippet": {"playlistId": playlist_id, "position": index,
                                "resourceId": {"kind": "youtube#video", "videoId": video_id}},
                }
                self._call("PUT", f"{API_BASE}/playlistItems?part=snippet",
                           op="playlistItems.update", body=body, is_write=True)
                op_name, extra = "playlistItems.update", {"was_position": item["position"]}
            else:
                step = f"{key}:playlistItems.insert:{video_id}"
                position = min(index, len(items))
                body = {
                    "snippet": {"playlistId": playlist_id, "position": position,
                                "resourceId": {"kind": "youtube#video", "videoId": video_id}},
                }
                self._call("POST", f"{API_BASE}/playlistItems?part=snippet",
                           op="playlistItems.insert", body=body, is_write=True)
                op_name, extra = "playlistItems.insert", {"requested_position": position}

            # verify-then-proceed: re-read and confirm this index is now correct.
            items = self.playlist_items(playlist_id)
            if index >= len(items) or items[index]["video_id"] != video_id:
                got = items[index]["video_id"] if index < len(items) else "<past end>"
                raise Aborted(
                    f"{key}: after {op_name} of {video_id} the read-back shows {got} at "
                    f"index {index}. Aborting with {len(items)} items in place; "
                    f"state file is resumable."
                )
            if [i["video_id"] for i in items[:index]] != target[:index]:
                raise Aborted(f"{key}: {op_name} disturbed an already-final prefix. Aborting.")

            self._record(step, {"op": op_name, "playlist_id": playlist_id,
                                "video_id": video_id, "index": index,
                                "playlist_item_id": items[index]["item_id"], **extra})
            self.log(f"  {key}[{index}] = {video_id} ({op_name}, verified)")

        self.verify_playlist(spec, playlist_id, items)

    # --------------------------------------------------------- verification

    def verify_playlist(self, spec: dict, playlist_id: str, items: list[dict] | None = None) -> dict:
        """Independent read-back check of one finished playlist."""
        key = spec["key"]
        target = [entry["video_id"] for entry in spec["order"]]
        items = self.playlist_items(playlist_id) if items is None else items
        actual = [i["video_id"] for i in items]
        live = self.playlist(playlist_id)

        problems: list[str] = []
        if actual != target:
            problems.append(f"order mismatch: {actual} != {target}")
        if len(set(actual)) != len(actual):
            problems.append("duplicate video ids present")
        if live is None:
            problems.append("playlist not readable")
        else:
            if live["snippet"].get("title") != spec["title"]:
                problems.append(f"title is {live['snippet'].get('title')!r}")
            if live["snippet"].get("description") != spec["description"]:
                problems.append("description does not match the design")
            if (live.get("status") or {}).get("privacyStatus") != spec["privacy"]:
                problems.append("privacy does not match the design")
        if actual and actual[0] != spec["entry_point_video_id"]:
            problems.append(f"entry point at position 0 is {actual[0]}, "
                            f"expected {spec['entry_point_video_id']}")
        if problems:
            raise Aborted(f"{key}: verification failed - " + "; ".join(problems))

        result = {
            "playlist_key": key, "playlist_id": playlist_id,
            "title": live["snippet"].get("title"), "item_count": len(actual),
            "entry_point": actual[0] if actual else None, "order": actual,
            "url": f"https://www.youtube.com/playlist?list={playlist_id}",
        }
        self.log(f"{key}: VERIFIED {len(actual)} items, entry point {result['entry_point']}")
        return result

    # ------------------------------------------------------------------ run

    def run(self) -> dict:
        self.preflight()
        results = []
        for spec in self.config["playlists"]:
            self.log(f"\n--- {spec['key']} ---")
            playlist_id = self.ensure_playlist(spec)
            # Runs for every playlist, not just reused ones: a playlist adopted by
            # the duplicate guard carries whatever title/description it was created
            # with, and must be brought onto the approved design too. It is a no-op
            # (no write) when the metadata already matches.
            self.ensure_metadata(spec, playlist_id)
            self.remove_dead_items(spec, playlist_id)
            self.converge_order(spec, playlist_id)
            results.append(self.verify_playlist(spec, playlist_id))

        self.state["status"] = "completed"
        self.state["completed_at"] = _utcnow()
        self.state["result"] = results
        self._save()
        return {"results": results, "write_calls": self.state["write_calls"],
                "read_calls": self.state["read_calls"], "quota_used": self.state["quota_used"]}


def execute(config: dict, plan: dict, approval_id: str,
            state_path: Path = STATE_PATH) -> int:
    """Entry point used by the guarded `--execute` path. Returns an exit code."""
    executor = Executor(config, plan, approval_id, state_path=state_path)
    try:
        summary = executor.run()
    except Aborted as exc:
        executor.state["status"] = "aborted"
        executor.state["abort_reason"] = str(exc)
        executor._save()
        print(f"\nABORTED: {exc}")
        print(f"state written to {state_path} - re-run the same command to resume.")
        return 5
    except Exception as exc:  # unexpected: still leave a resumable state file
        executor.state["status"] = "aborted"
        executor.state["abort_reason"] = f"{type(exc).__name__}: {exc}"
        executor._save()
        print(f"\nABORTED (unexpected): {type(exc).__name__}: {exc}")
        print(f"state written to {state_path} - re-run the same command to resume.")
        return 5

    print("\n=== EXECUTION COMPLETE - all playlists verified by read-back ===")
    for result in summary["results"]:
        print(f"  {result['playlist_id']}  {result['item_count']:>2} items  "
              f"entry={result['entry_point']}  {result['title']}")
    print(f"writes: {summary['write_calls']} (approved max {plan['total_calls']}), "
          f"reads: {summary['read_calls']}, quota: {summary['quota_used']} units")
    print(f"state: {state_path}")
    return 0
