"""Minimal one-screen web UI: theme in -> script / scenes / QC out.

Adapter layer only. It owns HTTP and HTML; all real work is delegated to
pd_factory.studio. Built on the standard library (http.server) so it adds no
dependency and starts no external connection.

The render_* functions are pure (data in, HTML string out) and HTML-escape every
piece of user/artifact content, so they are unit-testable without a socket.
"""
from __future__ import annotations

from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from .studio import EpisodeView, StudioError, create_and_run

_STYLE = """
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;max-width:820px;
margin:2rem auto;padding:0 1rem;line-height:1.55;color:#1b1b1f}
h1{font-size:1.5rem} h2{font-size:1.1rem;margin-top:1.6rem;border-bottom:1px solid #ddd;padding-bottom:.2rem}
form{display:flex;gap:.5rem;margin:1rem 0} input[type=text]{flex:1;padding:.6rem;font-size:1rem;
border:1px solid #bbb;border-radius:6px} button{padding:.6rem 1.1rem;font-size:1rem;border:0;
border-radius:6px;background:#1b6ef3;color:#fff;cursor:pointer}
.note{background:#fff8e1;border:1px solid #f0d000;padding:.6rem .8rem;border-radius:6px;font-size:.9rem}
.err{background:#fdecea;border:1px solid #f5c6cb;padding:.6rem .8rem;border-radius:6px;color:#9b1c1c}
.badge{display:inline-block;padding:.1rem .5rem;border-radius:10px;font-size:.85rem;font-weight:600}
.pass{background:#e6f4ea;color:#137333} .warn{background:#fef7e0;color:#a06000}
.fail{background:#fdecea;color:#9b1c1c}
.span{border-left:3px solid #1b6ef3;padding:.3rem .7rem;margin:.5rem 0;background:#f7f9ff}
.fn{color:#666;font-size:.8rem;text-transform:uppercase;letter-spacing:.04em}
table{border-collapse:collapse;width:100%} td,th{border:1px solid #ddd;padding:.35rem .5rem;text-align:left;font-size:.92rem}
.meta{color:#666;font-size:.9rem}
"""

_DISCLAIMER = (
    "ローカル実行のみ・外部送信/LLM/課金/アップロードなし。生成物は決定論的な"
    "プレースホルダで、実調査前は公開不可です（QC が判定）。"
)


def _page(body: str, *, title: str = "Prime Documentary") -> str:
    return (
        "<!doctype html><html lang=ja><head><meta charset=utf-8>"
        "<meta name=viewport content='width=device-width,initial-scale=1'>"
        f"<title>{escape(title)}</title><style>{_STYLE}</style></head>"
        f"<body>{body}</body></html>"
    )


def render_index(error: str | None = None) -> str:
    err = f"<p class=err>{escape(error)}</p>" if error else ""
    body = (
        "<h1>Prime Documentary — 最小スタジオ</h1>"
        f"<p class=note>{escape(_DISCLAIMER)}</p>"
        f"{err}"
        "<form method=post action='/run'>"
        "<input type=text name=theme placeholder='テーマを入力（例: なぜ鉛筆は黄色いのか）' "
        "autofocus required minlength=3>"
        "<button type=submit>パイプライン実行</button>"
        "</form>"
        "<p class=meta>入力したテーマから topic → research → claims → thesis → script → "
        "scene_plan → … → qc_report を生成し、台本・場面・QC を表示します。</p>"
    )
    return _page(body)


def _qc_badge(result: str) -> str:
    cls = {"pass": "pass", "pass_with_warnings": "warn"}.get(result, "fail")
    return f"<span class='badge {cls}'>{escape(result)}</span>"


def render_result(view: EpisodeView) -> str:
    spans = view.script.get("spans", [])
    script_html = "".join(
        f"<div class=span><div class=fn>{escape(str(s.get('narrative_function','')))}</div>"
        f"{escape(str(s.get('text','')))}</div>"
        for s in spans
    ) or "<p class=meta>(no spans)</p>"

    scenes = view.scene_plan.get("scenes", [])
    scene_rows = "".join(
        f"<tr><td>{escape(str(sc.get('scene_id','')))}</td>"
        f"<td>{escape(str(sc.get('purpose','')))}</td>"
        f"<td>{escape(str(sc.get('visual_mode','')))}</td>"
        f"<td>{escape(str(sc.get('duration_seconds','')))}s</td></tr>"
        for sc in scenes
    ) or "<tr><td colspan=4 class=meta>(no scenes)</td></tr>"

    findings = view.qc.get("findings", [])
    finding_rows = "".join(
        f"<tr><td>{escape(str(f.get('severity','')))}</td>"
        f"<td>{escape(str(f.get('code','')))}</td>"
        f"<td>{escape(str(f.get('message','')))}</td></tr>"
        for f in findings
    ) or "<tr><td colspan=3 class=meta>(no findings)</td></tr>"

    body = (
        "<h1>結果</h1>"
        f"<p class=note>{escape(_DISCLAIMER)}</p>"
        f"<p class=meta>episode: <b>{escape(view.episode_id)}</b> ・ "
        f"final_state: <b>{escape(view.final_state)}</b> ・ "
        f"produced {len(view.produced)} / skipped {len(view.skipped)}</p>"
        f"<p>テーマ: <b>{escape(view.theme)}</b></p>"
        "<h2>Thesis</h2>"
        f"<p>{escape(str(view.thesis.get('final_thesis','(none)')))}</p>"
        "<h2>Script（台本）</h2>"
        f"{script_html}"
        "<h2>Scene Plan（場面）</h2>"
        "<table><tr><th>scene</th><th>purpose</th><th>visual</th><th>dur</th></tr>"
        f"{scene_rows}</table>"
        f"<h2>QC 判定 {_qc_badge(str(view.qc.get('result','')))}</h2>"
        "<table><tr><th>severity</th><th>code</th><th>message</th></tr>"
        f"{finding_rows}</table>"
        "<p><a href='/'>← 別のテーマで実行</a></p>"
    )
    return _page(body, title=f"PD — {view.theme}")


def handle_run(form: dict[str, list[str]], runs_dir: Path) -> tuple[int, str]:
    """Dispatch a /run submission. Returns (http_status, html). Pure except for
    the pipeline's writes under runs_dir."""
    theme = (form.get("theme", [""])[0] or "").strip()
    try:
        view = create_and_run(runs_dir, theme)
    except StudioError as exc:
        return 400, render_index(error=str(exc))
    return 200, render_result(view)


def make_handler(runs_dir: Path) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def _send(self, status: int, html: str) -> None:
            payload = html.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:  # noqa: N802 (stdlib naming)
            if self.path.split("?", 1)[0] != "/":
                self._send(404, _page("<h1>404</h1><p><a href='/'>home</a></p>"))
                return
            self._send(200, render_index())

        def do_POST(self) -> None:  # noqa: N802
            if self.path.split("?", 1)[0] != "/run":
                self._send(404, _page("<h1>404</h1>"))
                return
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length).decode("utf-8") if length else ""
            status, html = handle_run(parse_qs(body), runs_dir)
            self._send(status, html)

        def log_message(self, *args) -> None:  # keep stdout clean
            return

    return Handler


def serve(host: str = "127.0.0.1", port: int = 8765, runs_dir: Path | None = None) -> None:
    runs_dir = Path(runs_dir or (Path.cwd() / "runs" / "ui"))
    runs_dir.mkdir(parents=True, exist_ok=True)
    httpd = ThreadingHTTPServer((host, port), make_handler(runs_dir))
    print(f"Prime Documentary minimal UI: http://{host}:{port}  (Ctrl-C to stop)")
    print(f"episodes written under: {runs_dir}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
    finally:
        httpd.server_close()
