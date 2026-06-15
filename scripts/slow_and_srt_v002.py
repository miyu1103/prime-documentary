"""
scripts/slow_and_srt_v002.py
VC-0001..VC-0023 を atempo で減速 → vc_master_v002.mp3 → subs_vc_v002.srt

SLOW_FACTOR = 0.856 → 約 674s（12分アセンブリの本編尺に対応）
idempotent: 個別スロー済みファイルが存在する場合はスキップ
"""
from __future__ import annotations
import json, pathlib, re, subprocess, tempfile, textwrap

FFMPEG  = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"

REPO       = pathlib.Path(__file__).resolve().parents[1]
DRAFT_DIR  = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_voice\draft")
SLOW_DIR   = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_voice\slow_v001")
MASTER_OUT = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_voice\master\vc_master_v002.mp3")
PLAN_JSON  = REPO / "episodes/PD-2026-001-miranda/06_audio/voice_plan.v001.json"
SRT_OUT    = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\07_edit\sample\subs_vc_v002.srt")

SLOW_FACTOR = 0.856   # output speed; <1 = slower; output_dur = input_dur / SLOW_FACTOR
MAX_WORDS   = 10      # max words per subtitle entry (American documentary standard)
N_CHUNKS    = 23


def run(cmd: list[str], desc: str = "") -> None:
    print(f"  >> {desc}")
    r = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"FAILED [{r.returncode}] {desc}\n{r.stderr[-1000:]}")


def probe_duration(path: pathlib.Path) -> float:
    r = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def fmt_ts(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec % 1) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def split_to_subtitles(text: str) -> list[str]:
    """Split at natural English boundaries: sentence > clause > word count.

    Priority order:
      1. Sentence endings (.  !  ?)
      2. Clause boundaries (,  ;  em-dash)
      3. Hard cap at MAX_WORDS words
    Timing is allocated proportionally to character count so longer
    phrases get more screen time.
    """
    text = re.sub(r'\s+', ' ', text.strip())
    # Split on sentence endings, keeping punctuation with the left side
    sentences = re.split(r'(?<=[.!?])\s+', text)
    result: list[str] = []
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        if len(sent.split()) <= MAX_WORDS:
            result.append(sent)
        else:
            # Split on clause boundaries: comma, semicolon, em-dash
            clauses = re.split(r'(?<=[,;])\s+|\s*—\s*', sent)
            buf: list[str] = []
            for clause in clauses:
                clause = clause.strip()
                if not clause:
                    continue
                cw = clause.split()
                if len(buf) + len(cw) <= MAX_WORDS:
                    buf.extend(cw)
                else:
                    if buf:
                        result.append(' '.join(buf))
                    if len(cw) > MAX_WORDS:
                        for i in range(0, len(cw), MAX_WORDS):
                            result.append(' '.join(cw[i:i + MAX_WORDS]))
                        buf = []
                    else:
                        buf = cw[:]
            if buf:
                result.append(' '.join(buf))
    return [s for s in result if s]


# ── 1. slow each chunk ─────────────────────────────────────────────────────────
SLOW_DIR.mkdir(parents=True, exist_ok=True)
MASTER_OUT.parent.mkdir(parents=True, exist_ok=True)
SRT_OUT.parent.mkdir(parents=True, exist_ok=True)

chunk_ids = [f"VC-{i:04d}" for i in range(1, N_CHUNKS + 1)]
slow_paths: list[pathlib.Path] = []

print(f"\n[1/3] Slowing {N_CHUNKS} chunks  factor={SLOW_FACTOR}")
for cid in chunk_ids:
    src = DRAFT_DIR / f"{cid}.mp3"
    dst = SLOW_DIR  / f"{cid}.mp3"
    slow_paths.append(dst)
    if not src.exists():
        raise FileNotFoundError(src)
    if dst.exists():
        print(f"  skip: {cid}")
        continue
    tmp = dst.with_suffix(".tmp.mp3")
    run([FFMPEG, "-y", "-i", str(src),
         "-af", f"atempo={SLOW_FACTOR}",
         "-f", "mp3", str(tmp)],
        f"slow {cid}")
    tmp.replace(dst)

# ── 2. concat → vc_master_v002.mp3 ────────────────────────────────────────────
print(f"\n[2/3] Concat → {MASTER_OUT.name}")
if MASTER_OUT.exists():
    print("  skip (exists)")
else:
    with tempfile.NamedTemporaryFile("w", suffix=".txt",
                                     delete=False, encoding="utf-8") as f:
        for p in slow_paths:
            f.write(f"file '{p.as_posix()}'\n")
        concat_list = pathlib.Path(f.name)
    tmp_master = MASTER_OUT.with_suffix(".tmp.mp3")
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0",
         "-i", str(concat_list),
         "-c:a", "copy", str(tmp_master)],
        "concat master")
    tmp_master.replace(MASTER_OUT)
    concat_list.unlink(missing_ok=True)

total_dur = probe_duration(MASTER_OUT)
print(f"  master duration: {total_dur:.1f}s ({total_dur/60:.1f} min)")

# ── 3. build SRT v2 ────────────────────────────────────────────────────────────
print(f"\n[3/3] Building SRT → {SRT_OUT.name}")

plan   = json.loads(PLAN_JSON.read_text(encoding="utf-8"))
chunks = {c["chunk_id"]: c["spoken_text"] for c in plan["chunks"]}

srt_entries: list[str] = []
idx   = 1
t_cur = 0.0

for cid, p in zip(chunk_ids, slow_paths):
    dur     = probe_duration(p)
    text    = chunks.get(cid, "")
    phrases = split_to_subtitles(text)
    total_chars = sum(len(ph) for ph in phrases) or 1
    t_offset = 0.0

    for phrase in phrases:
        # Character-proportional timing: longer phrases stay on screen longer
        frac        = len(phrase) / total_chars
        phrase_dur  = dur * frac
        t_start     = t_cur + t_offset
        t_end       = t_start + phrase_dur - 0.04   # 40 ms gap between entries
        srt_entries.append(
            f"{idx}\n{fmt_ts(t_start)} --> {fmt_ts(max(t_start + 0.3, t_end))}\n{phrase}\n"
        )
        idx      += 1
        t_offset += phrase_dur
    t_cur += dur

tmp_srt = SRT_OUT.with_suffix(".tmp.srt")
tmp_srt.write_text("\n".join(srt_entries), encoding="utf-8")
tmp_srt.replace(SRT_OUT)

print(f"  {len(srt_entries)} entries  total {t_cur:.1f}s ({t_cur/60:.1f} min)")
print("\nDone.")
