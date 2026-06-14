#!/usr/bin/env python3
"""Local animatic review server (stdlib only). One command, localhost-only, $0.

    py -3.11 review/serve.py            # serve + open browser at http://127.0.0.1:7332
    py -3.11 review/serve.py --port 8080 --no-open

Serves the review UI + the already-rendered animatic MP4 (HTTP range for seeking) and a
JSON review API. JSON under episodes/.../08_qc/reviews/ is the source of truth. No paid
calls, no uploads, no secrets, no destructive ops (P0 spec; CLAUDE.md §13).
"""
from __future__ import annotations

import argparse
import json
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# Robust on Windows' cp932 console (the UI/JSON itself is always UTF-8).
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_meta  # noqa: E402
import store  # noqa: E402

STATIC_DIR = Path(__file__).resolve().parent / "static"
CONTENT_TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
                 ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
                 ".mp4": "video/mp4"}
MAX_PUT_BYTES = 8_000_000


class Handler(BaseHTTPRequestHandler):
    server_version = "PDReview/0.1"

    def log_message(self, *args):  # quieter console
        pass

    # -- helpers --
    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path):
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", CONTENT_TYPES.get(path.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_media(self, path: Path):
        """Serve the MP4 with HTTP range support so the <video> can seek."""
        size = path.stat().st_size
        rng = self.headers.get("Range")
        start, end = 0, size - 1
        status = 200
        if rng and rng.startswith("bytes="):
            try:
                s, _, e = rng[6:].partition("-")
                start = int(s) if s else 0
                end = int(e) if e else size - 1
                end = min(end, size - 1)
                status = 206
            except ValueError:
                start, end, status = 0, size - 1, 200
        length = end - start + 1
        self.send_response(status)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(length))
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        with path.open("rb") as f:
            f.seek(start)
            remaining = length
            while remaining > 0:
                chunk = f.read(min(262144, remaining))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return  # client seeked / closed; normal for video
                remaining -= len(chunk)

    def _safe_static(self, rel: str) -> Path | None:
        target = (STATIC_DIR / rel).resolve()
        if STATIC_DIR.resolve() in target.parents and target.is_file():
            return target
        return None

    # -- routes --
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/" or path == "/index.html":
            f = STATIC_DIR / "index.html"
            return self._send_file(f) if f.exists() else self._send_json({"error": "ui missing"}, 500)
        if path == "/api/meta":
            return self._send_json(gen_meta.build_meta())
        if path == "/api/review":
            doc = store.load_or_init(gen_meta.build_meta())
            return self._send_json(doc)
        if path == "/api/review/draft":
            return self._send_json(json.loads(store.DRAFT_PATH.read_text(encoding="utf-8")) if store.DRAFT_PATH.exists() else None)
        if path.startswith("/media/"):
            mp4 = gen_meta.media_file()
            return self._send_media(mp4) if mp4 else self._send_json({"error": "render the animatic first"}, 404)
        if path.startswith("/static/"):
            f = self._safe_static(path[len("/static/"):])
            return self._send_file(f) if f else self._send_json({"error": "not found"}, 404)
        return self._send_json({"error": "not found"}, 404)

    def do_PUT(self):
        length = int(self.headers.get("Content-Length", 0))
        if length > MAX_PUT_BYTES:
            return self._send_json({"error": "payload too large"}, 413)
        body = self.rfile.read(length)
        try:
            doc = json.loads(body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return self._send_json({"error": "invalid json"}, 400)
        path = self.path.split("?", 1)[0]
        if path == "/api/review/draft":
            store.save_draft(doc)
            return self._send_json({"ok": True})
        if path == "/api/review":
            try:
                store.save_atomic(doc)  # validates + backups + atomic
            except Exception as exc:  # surface validation/write errors to the UI
                return self._send_json({"ok": False, "error": str(exc)}, 422)
            return self._send_json({"ok": True, "saved_to": str(store.REVIEW_PATH.relative_to(store.REPO_ROOT)),
                                    "last_saved_at": doc.get("session", {}).get("last_saved_at")})
        return self._send_json({"error": "not found"}, 404)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Prime Documentary local animatic review server")
    ap.add_argument("--port", type=int, default=7332)
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args(argv)

    meta = gen_meta.build_meta()
    url = f"http://127.0.0.1:{args.port}/"
    print("Prime Documentary — Animatic Review (local, $0)")
    print(f"  composition : {meta['composition_id']}  fps={meta['fps']}  ~{meta['duration_seconds']}s")
    print(f"  media       : {'OK ' + str(meta['media_name']) if meta['media_available'] else 'MISSING — render the animatic first'}")
    print(f"  review JSON : {store.REVIEW_PATH.relative_to(store.REPO_ROOT)}")
    print(f"  open        : {url}")
    if not meta["media_available"]:
        print("  NOTE: run the full render first (remotion: render Animatic out/miranda-animatic.mp4).")
    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    if not args.no_open:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
