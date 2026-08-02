#!/usr/bin/env python
"""Apply a change and PROVE it took effect -- or put the file back.

Every avoidable failure this week had the same shape: a replacement was applied, the command
exited 0, and the run continued for hours on a file that had not actually changed.

  * the caption lead was written into _finish_episode.sh twice and reached the render zero times
  * an inline heredoc had an f-string backslash error, so an episode rebuild never started and
    was only noticed three hours later
  * a filmconfig was written as EP057_... while the builder looks for EP57_...

Exit 0 means the command ran. It never meant the intent landed. This tool checks the intent:
the new text must be present afterwards, the file must still parse, and -- when --smoke is
given -- the smallest real invocation of that file must succeed. Any failure restores the
original bytes, so a half-applied edit cannot survive.

    python scripts/pd_edit.py --file scripts/_finish_episode.sh \
        --old '--srt "$SRT"' --new '--srt "$SRT" --lead 0.25' \
        --smoke 'bash -n scripts/_finish_episode.sh'

    python scripts/pd_edit.py --file scripts/build_case_film_generic.py --show 'still_lift'
"""
from __future__ import annotations

import argparse
import ast
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def syntax_ok(path: Path) -> tuple[bool, str]:
    if path.suffix == ".py":
        try:
            ast.parse(path.read_text(encoding="utf-8"))
            return True, "python parses"
        except SyntaxError as exc:
            return False, f"python syntax error line {exc.lineno}: {exc.msg}"
    if path.suffix in (".sh", ".bash"):
        r = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
        return r.returncode == 0, (r.stderr.strip() or "bash -n ok")
    if path.suffix == ".json":
        import json
        try:
            json.loads(path.read_text(encoding="utf-8"))
            return True, "json parses"
        except Exception as exc:  # noqa: BLE001
            return False, f"json error: {exc}"
    return True, "no syntax checker for this type"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--old", help="exact text to replace (must appear exactly once)")
    ap.add_argument("--new", help="replacement text")
    ap.add_argument("--show", help="just report whether this text is present, change nothing")
    ap.add_argument("--count", type=int, default=1, help="how many occurrences --old must have")
    ap.add_argument("--smoke", help="command that must succeed after the edit")
    a = ap.parse_args()

    path = Path(a.file)
    if not path.is_absolute():
        path = ROOT / path
    if not path.is_file():
        print(f"[edit] no such file: {path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")

    if a.show:
        n = text.count(a.show)
        print(f"[edit] {path.name}: {n} occurrence(s) of {a.show!r}")
        return 0 if n else 1

    if a.old is None or a.new is None:
        print("[edit] --old and --new are required (or use --show)", file=sys.stderr)
        return 1

    found = text.count(a.old)
    if found != a.count:
        print(f"[edit] REFUSED: {path.name} contains {found} occurrence(s) of the anchor, "
              f"expected {a.count}. Nothing was changed -- fix the anchor, do not guess.",
              file=sys.stderr)
        return 1

    backup = path.with_suffix(path.suffix + ".pd_edit_bak")
    shutil.copy2(path, backup)
    path.write_text(text.replace(a.old, a.new), encoding="utf-8")

    def fail(reason: str) -> int:
        shutil.copy2(backup, path)
        backup.unlink(missing_ok=True)
        print(f"[edit] REVERTED {path.name}: {reason}", file=sys.stderr)
        return 1

    after = path.read_text(encoding="utf-8")
    if a.new not in after:
        return fail("the new text is not in the file after writing")
    ok, msg = syntax_ok(path)
    if not ok:
        return fail(msg)

    if a.smoke:
        r = subprocess.run(a.smoke, shell=True, cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            return fail(f"smoke command failed ({r.returncode}): "
                        f"{(r.stderr or r.stdout).strip()[:300]}")
        print(f"[edit] smoke ok: {a.smoke}")

    backup.unlink(missing_ok=True)
    line = next((i + 1 for i, l in enumerate(after.splitlines()) if a.new.splitlines()[0] in l), 0)
    print(f"[edit] {path.name}: applied and verified ({msg}); new text at line {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
