#!/usr/bin/env python3
"""Measure where a Claude Code session's tokens actually go.

Why this exists
---------------
On 2026-08-16 an audit of the five largest PD sessions found:

    conversation content ......    6,047,218 estimated tokens
    actually billed (cr+cw+out)  8,801,355,788 tokens
    amplification ............. ~1,455x

95% of the bill was ``cache_read``: every API call re-reads the whole context.
Claude's own written output (design docs, scripts, prose) was 0.2% of the bill.
So the lever is never "write less" -- it is "carry less, for fewer turns".

Context composition of those same sessions (estimated tokens):

    Bash/PowerShell in+out ..  2,631,259   43%   6,201 calls, avg 822 chars
    Read (incl. 436 images) .  1,491,929   25%
    Write tool input ........    767,067   13%
    user text + reminders ...    710,841   12%
    assistant text ..........    429,522    7%   <- NOT the problem

A shell call costs its own size ONCE, then gets re-billed on every later turn in
the session. Real cost = size x remaining turns. That is why an 800-char command
at turn 100 of a 5,000-turn session is not cheap.

Usage
-----
    py -3.11 scripts/token_audit.py                 # all sessions, ranked
    py -3.11 scripts/token_audit.py --live          # the session running now
    py -3.11 scripts/token_audit.py --session <id>  # one session in detail
    py -3.11 scripts/token_audit.py --top 40        # more rows in detail mode

Exit codes: 0 always (this is a measuring instrument, not a gate).

What it cannot do
-----------------
It reads the local JSONL transcripts, so it reports what the client logged, not
what the provider billed. Text tokens are estimated at chars/3.5 and images at a
flat 1500; both are approximations. The ``usage`` block IS provider-reported and
exact -- that is the number to trust for cost. Subagent transcripts under
``subagents/`` are counted separately, not folded into the parent.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

# A resized image (long side <= 1568px) costs roughly this much. Flat estimate.
IMAGE_TOKENS = 1500
# Rough chars-per-token for the mixed EN/JA + JSON that fills these transcripts.
CHARS_PER_TOKEN = 3.5

# Context sizes above this mean every subsequent turn is expensive.
CTX_WARN = 300_000
CTX_CRIT = 500_000


def projects_root() -> Path:
    return Path(os.path.expanduser("~")) / ".claude" / "projects"


def session_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.glob("*.jsonl"), key=lambda p: p.stat().st_size, reverse=True)


def default_project_dir() -> Path:
    """The transcript dir for whichever project has the most logged bytes."""
    root = projects_root()
    best, best_size = None, -1
    for d in root.iterdir() if root.exists() else []:
        if not d.is_dir():
            continue
        size = sum(f.stat().st_size for f in d.glob("*.jsonl"))
        if size > best_size:
            best, best_size = d, size
    return best or root


class Stats:
    def __init__(self) -> None:
        self.category: Counter[str] = Counter()
        self.tool_in: Counter[str] = Counter()
        self.tool_out: Counter[str] = Counter()
        self.calls: Counter[str] = Counter()
        self.cmd_prefix: Counter[str] = Counter()
        self.big_outputs: list[tuple[int, str]] = []
        self.images = 0
        self.ctx: list[int] = []
        self.usage = Counter()  # in / cache_read / cache_write / out


def _text_chars(node, st: Stats) -> int:
    """Sum text chars under ``node``; count image blocks separately."""
    if isinstance(node, str):
        return len(node)
    if isinstance(node, list):
        return sum(_text_chars(x, st) for x in node)
    if isinstance(node, dict):
        if node.get("type") == "image":
            st.images += 1
            return 0
        total = 0
        for key, value in node.items():
            if key in ("source", "data", "base64"):
                continue  # base64 payload is not what gets billed
            total += _text_chars(value, st)
        return total
    return 0


def _est_tokens(node, st: Stats) -> float:
    before = st.images
    chars = _text_chars(node, st)
    return chars / CHARS_PER_TOKEN + (st.images - before) * IMAGE_TOKENS


def scan(paths: list[Path]) -> Stats:
    st = Stats()
    tool_name_by_id: dict[str, str] = {}
    cmd_by_id: dict[str, str] = {}

    for path in paths:
        with path.open(encoding="utf-8", errors="replace") as handle:
            for line in handle:
                try:
                    record = json.loads(line)
                except (ValueError, TypeError):
                    continue
                message = record.get("message") or {}

                usage = message.get("usage") or {}
                if usage:
                    st.usage["in"] += usage.get("input_tokens", 0)
                    st.usage["cache_read"] += usage.get("cache_read_input_tokens", 0)
                    st.usage["cache_write"] += usage.get("cache_creation_input_tokens", 0)
                    st.usage["out"] += usage.get("output_tokens", 0)
                    ctx = (
                        usage.get("input_tokens", 0)
                        + usage.get("cache_read_input_tokens", 0)
                        + usage.get("cache_creation_input_tokens", 0)
                    )
                    if ctx:
                        st.ctx.append(ctx)

                content = message.get("content")
                role = "assistant" if record.get("type") == "assistant" else "user"
                if isinstance(content, str):
                    st.category[f"{role}_text"] += len(content) / CHARS_PER_TOKEN
                    continue
                if not isinstance(content, list):
                    continue

                for block in content:
                    if not isinstance(block, dict):
                        continue
                    kind = block.get("type")

                    if kind == "text":
                        st.category[f"{role}_text"] += len(block.get("text", "")) / CHARS_PER_TOKEN

                    elif kind == "thinking":
                        st.category["thinking"] += len(block.get("thinking", "")) / CHARS_PER_TOKEN

                    elif kind == "tool_use":
                        name = block.get("name", "?")
                        tool_name_by_id[block.get("id")] = name
                        st.calls[name] += 1
                        tokens = _est_tokens(block.get("input"), st)
                        st.tool_in[name] += tokens
                        st.category["tool_input"] += tokens
                        if name in ("Bash", "PowerShell"):
                            command = (block.get("input") or {}).get("command", "")
                            cmd_by_id[block.get("id")] = command
                            stripped = re.sub(r"^\s*(cd\s+\S+\s*(&&|;)\s*)?", "", command)
                            st.cmd_prefix[" ".join(stripped.split()[:3])[:58]] += 1

                    elif kind == "tool_result":
                        use_id = block.get("tool_use_id")
                        name = tool_name_by_id.get(use_id, "?")
                        tokens = _est_tokens(block.get("content"), st)
                        st.tool_out[name] += tokens
                        st.category["tool_result"] += tokens
                        if use_id in cmd_by_id and tokens > 0:
                            st.big_outputs.append((int(tokens), cmd_by_id[use_id][:88]))
    return st


def verdict(avg_ctx: int, calls: int) -> str:
    if avg_ctx >= CTX_CRIT:
        return "CRIT  文脈が肥大。工程の切れ目でセッションを分ける（docs/HANDOVER.md に書いて新規セッション）"
    if avg_ctx >= CTX_WARN:
        return "WARN  そろそろ分割どき。次の工程の頭で切る"
    return "OK    この範囲なら継続してよい"


def report_all(project_dir: Path) -> None:
    paths = session_files(project_dir)
    if not paths:
        print(f"no transcripts under {project_dir}")
        return
    print(f"project: {project_dir}")
    print(f"{'session':10s} {'MB':>7s} {'API calls':>10s} {'avg ctx':>10s} {'max ctx':>10s} {'billed(cr+cw+out)':>19s}")
    grand = 0
    for path in paths[:20]:
        st = scan([path])
        if not st.ctx:
            continue
        billed = st.usage["cache_read"] + st.usage["cache_write"] + st.usage["out"]
        grand += billed
        avg = sum(st.ctx) // len(st.ctx)
        print(
            f"{path.stem[:8]:10s} {path.stat().st_size/1048576:7.1f} {len(st.ctx):>10,} "
            f"{avg:>10,} {max(st.ctx):>10,} {billed:>19,}"
        )
    print(f"\nbilled across the sessions above: {grand:,} tokens")
    print("detail for one session:  py -3.11 scripts/token_audit.py --session <id>")


def report_one(paths: list[Path], top: int) -> None:
    st = scan(paths)
    content = sum(st.category.values())
    billed = st.usage["cache_read"] + st.usage["cache_write"] + st.usage["out"]
    calls = len(st.ctx)
    avg_ctx = sum(st.ctx) // calls if calls else 0

    print("=" * 74)
    for path in paths:
        print(f"session {path.stem}  ({path.stat().st_size/1048576:.1f} MB)")
    print("=" * 74)
    print(f"API calls .................. {calls:,}")
    print(f"average context ............ {avg_ctx:,} tokens")
    print(f"peak context ............... {max(st.ctx) if st.ctx else 0:,} tokens")
    print(f"conversation content ....... {content:,.0f} tokens (estimated)")
    print(f"billed cache_read .......... {st.usage['cache_read']:,}")
    print(f"billed cache_write ......... {st.usage['cache_write']:,}")
    print(f"billed output .............. {st.usage['out']:,}")
    print(f"billed total ............... {billed:,}")
    if content:
        print(f"AMPLIFICATION .............. {billed/content:,.0f}x  (content carried, re-read every turn)")
    print(f"\n{verdict(avg_ctx, calls)}")

    if content:
        print("\n--- what fills the context ---")
        for key, value in st.category.most_common():
            print(f"  {key:16s} {value:>12,.0f}  {100*value/content:5.1f}%")

        print("\n--- tool result tokens ---")
        for key, value in st.tool_out.most_common(12):
            n = st.calls.get(key, 0)
            avg = int(value / n) if n else 0
            print(f"  {key:16s} {value:>12,.0f}  {100*value/content:5.1f}%  calls={n:<6,} avg={avg:,}")

        print("\n--- tool input tokens ---")
        for key, value in st.tool_in.most_common(8):
            n = st.calls.get(key, 0)
            print(f"  {key:16s} {value:>12,.0f}  {100*value/content:5.1f}%  calls={n:,}")

    if st.cmd_prefix:
        print(f"\n--- most repeated shell commands (top {top}) ---")
        for key, value in st.cmd_prefix.most_common(top):
            print(f"  {value:>5}x  {key}")

    if st.big_outputs:
        print(f"\n--- biggest single shell outputs (top {min(top, 15)}) ---")
        for tokens, command in sorted(st.big_outputs, reverse=True)[: min(top, 15)]:
            print(f"  {tokens:>7,} tok  {command}")
        total = sum(t for t, _ in st.big_outputs)
        ranked = sorted((t for t, _ in st.big_outputs), reverse=True)
        if total:
            tenth = sum(ranked[: max(len(ranked) // 10, 1)])
            print(f"\n  top 10% of shell calls = {100*tenth/total:.0f}% of all shell output tokens")
            print("  -> それらを head/tail/集計に絞るのが一番効く")

    print(f"\nimages read: {st.images} (~{st.images*IMAGE_TOKENS:,} tokens)")
    print("画像の目視QCは品質の生命線。減らすのではなく、サブエージェントに出して親に残さない。")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--session", help="session id (or path) to inspect in detail")
    parser.add_argument("--live", action="store_true", help="inspect the most recently written session")
    parser.add_argument("--top", type=int, default=25, help="rows in the repeated-command tables")
    parser.add_argument("--project-dir", help="override the transcript directory")
    args = parser.parse_args(argv)

    project_dir = Path(args.project_dir) if args.project_dir else default_project_dir()

    if args.session:
        candidate = Path(args.session)
        if not candidate.exists():
            candidate = project_dir / f"{args.session}.jsonl"
        if not candidate.exists():
            print(f"no such session: {args.session}", file=sys.stderr)
            return 0
        report_one([candidate], args.top)
        return 0

    if args.live:
        paths = session_files(project_dir)
        if not paths:
            print(f"no transcripts under {project_dir}")
            return 0
        newest = max(paths, key=lambda p: p.stat().st_mtime)
        report_one([newest], args.top)
        return 0

    report_all(project_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
