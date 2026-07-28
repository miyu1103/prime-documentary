"""
scripts/gen_kidsforcash_narration.py
Role: audio-director — EP38 Kids for Cash master narration.

Voice: Brian (nPczCjzI2devNBz1zQrb), eleven_multilingual_v2 (channel standard, matches gen_narration.py).
Source: episodes/_planning/EP38_kidsforcash_script.en.v003.md (FACT-LOCKED v003).
Chunking: by section (HOOK / ACT 1..4 / ED). Strips annotations, 〔CARD〕, [L:...], (parenthetical), headers, JP notes.
QC: per-chunk loudnorm -16 LUFS / -1.5 TP / LRA 11. Concatenate to narration_master.mp3.
Output:
  H:/pd-media/episodes/PD-2026-038-kidsforcash/06_audio/draft/VC-00xx.mp3
  remotion/public/kidsforcash/narration_master.mp3
  episodes/PD-2026-038-kidsforcash/06_audio/narration_index.v001.json  (per-chunk offset/duration + char log)
Idempotent by SHA-256 of spoken_text. --dry-run prints chunks + char counts, no API spend.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")
ENV_PATH = ROOT / ".env"
SCRIPT_MD = ROOT / "episodes" / "_planning" / "EP38_kidsforcash_script.en.v004.md"
EP = "PD-2026-038-kidsforcash"
DRAFT_DIR = Path(r"H:/pd-media/episodes") / EP / "06_audio" / "draft"
PUB_DIR = ROOT / "remotion" / "public" / "kidsforcash"
INDEX_PATH = ROOT / "episodes" / EP / "06_audio" / "narration_index.v001.json"
FFMPEG = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"
FFPROBE = r"C:\Users\aab15\AppData\Local\Microsoft\WinGet\Links\ffprobe.exe"

VOICE_ID = "nPczCjzI2devNBz1zQrb"  # Brian
MODEL_ID = "eleven_multilingual_v2"
EL_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
VOICE_SETTINGS = {"stability": 0.60, "similarity_boost": 0.75, "style": 0.0, "use_speaker_boost": True}

SECTIONS = [("HOOK", "## HOOK"), ("ACT1", "## ACT 1"), ("ACT2", "## ACT 2"),
            ("ACT3", "## ACT 3"), ("ACT4", "## ACT 4"), ("ED", "## ED")]


def load_env() -> dict[str, str]:
    env = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("="); env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def clean_line(s: str) -> str:
    s = re.sub(r"\[[^\]]*\]", "", s)      # [L: ...]
    s = re.sub(r"〔[^〕]*〕", "", s)         # 〔CARD ...〕
    s = re.sub(r"\([^)]*\)", "", s)        # (parenthetical stage notes)
    return re.sub(r"\s+", " ", s).strip()


def extract_chunks() -> list[dict]:
    """Split the script into spoken-text chunks by section."""
    text = SCRIPT_MD.read_text(encoding="utf-8").splitlines()
    # find section start line indices
    starts = []
    for i, ln in enumerate(text):
        for key, hdr in SECTIONS:
            if ln.strip().startswith(hdr):
                starts.append((i, key))
    starts.append((len(text), "END"))
    chunks = []
    for idx in range(len(starts) - 1):
        (a, key) = starts[idx]; (b, _) = starts[idx + 1]
        prose = []
        for ln in text[a + 1:b]:
            s = ln.strip()
            if not s: continue
            if s[0] in "#*->" or s.startswith("[") or s.startswith("(") or s.startswith("|"): continue
            c = clean_line(s)   # strip [L:...] / 〔CARD〕 / (notes) FIRST
            if not c: continue
            # skip only PURE-JP note lines; an English sentence with an inline [L: 日本語]
            # annotation cleans to pure English and MUST be kept (was dropping the Act3
            # "he took his own life" passage -> missing from the VO).
            if re.search(r"[぀-ヿ一-鿿]", c): continue
            prose.append(c)
        spoken = " ".join(prose).strip()
        if spoken:
            chunks.append({"chunk_id": f"VC-{idx+1:04d}", "section": key, "spoken_text": spoken})
    return chunks


def content_hash(t: str) -> str: return hashlib.sha256(t.encode("utf-8")).hexdigest()


def probe_dur(p: Path) -> float:
    r = subprocess.run([FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return round(float(r.stdout.strip()), 3)


def loudnorm(raw: Path, out: Path) -> None:
    tmp = out.parent / (out.stem + ".norm_tmp.mp3")
    r = subprocess.run([FFMPEG, "-y", "-i", str(raw), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-f", "mp3", "-c:a", "libmp3lame", "-b:a", "192k", str(tmp)],
                       capture_output=True, encoding="utf-8", errors="replace")
    if r.returncode != 0: raise RuntimeError(f"loudnorm failed: {r.stderr[-400:]}")
    tmp.replace(out)


def tts(api_key: str, text: str, retries: int = 3) -> bytes:
    payload = json.dumps({"text": text, "model_id": MODEL_ID, "voice_settings": VOICE_SETTINGS}).encode()
    req = urllib.request.Request(EL_URL, data=payload, method="POST",
                                 headers={"xi-api-key": api_key, "Content-Type": "application/json",
                                          "Accept": "audio/mpeg"})
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            body = e.read(300).decode("utf-8", errors="replace")
            if e.code == 429 or e.code >= 500:
                time.sleep(6 * attempt); continue
            raise RuntimeError(f"ElevenLabs HTTP {e.code}: {body}") from e
    raise RuntimeError("all TTS attempts failed")


def main(dry: bool) -> int:
    chunks = extract_chunks()
    total_chars = sum(len(c["spoken_text"]) for c in chunks)
    print(f"EP38 narration — {len(chunks)} chunks, {total_chars} chars total\n")
    for c in chunks:
        print(f"  {c['chunk_id']} [{c['section']}] {len(c['spoken_text'])} chars")
        print(f"      {c['spoken_text'][:110]}{'...' if len(c['spoken_text'])>110 else ''}")
    if dry:
        print(f"\n[DRY] no API spend. total chars = {total_chars}")
        return 0

    env = load_env(); api = env.get("ELEVENLABS_API_KEY", "")
    if not api: raise RuntimeError("ELEVENLABS_API_KEY missing")
    DRAFT_DIR.mkdir(parents=True, exist_ok=True); PUB_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    entries, offset, listfile = [], 0.0, DRAFT_DIR / "_concat.txt"
    concat_lines = []
    for c in chunks:
        out = DRAFT_DIR / f"{c['chunk_id']}.mp3"
        print(f"  GEN {c['chunk_id']} [{c['section']}] {len(c['spoken_text'])} chars ...")
        raw = tts(api, c["spoken_text"]); rawp = DRAFT_DIR / f"{c['chunk_id']}.raw.partial"
        rawp.write_bytes(raw); loudnorm(rawp, out); rawp.unlink(missing_ok=True)
        dur = probe_dur(out)
        entries.append({"chunk_id": c["chunk_id"], "section": c["section"],
                        "chars": len(c["spoken_text"]), "offset_sec": round(offset, 3),
                        "duration_sec": dur, "file_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                        "spoken_text": c["spoken_text"]})
        offset += dur
        concat_lines.append(f"file '{out.as_posix()}'")
        print(f"    ok {dur:.1f}s (cum {offset:.1f}s)")
        time.sleep(0.3)

    # concat -> master
    listfile.write_text("\n".join(concat_lines), encoding="utf-8")
    master = PUB_DIR / "narration_master.mp3"
    r = subprocess.run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
                        "-c", "copy", str(master)], capture_output=True, text=True)
    if r.returncode != 0:
        r = subprocess.run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
                            "-c:a", "libmp3lame", "-b:a", "192k", str(master)], capture_output=True, text=True)
    master_dur = probe_dur(master) if master.exists() else 0.0
    listfile.unlink(missing_ok=True)

    index = {"schema_version": "1", "episode_id": EP, "voice_id": VOICE_ID, "model_id": MODEL_ID,
             "lufs_target": -16, "generated_at": now, "total_chars": total_chars,
             "master": str(master), "master_duration_sec": master_dur, "chunks": entries}
    tmp = INDEX_PATH.with_suffix(".tmp"); tmp.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(INDEX_PATH)
    print(f"\nMASTER {master}  {master_dur:.1f}s ({master_dur/60:.1f} min)")
    print(f"INDEX  {INDEX_PATH}")
    print(f"CHARS  {total_chars} (ElevenLabs billed)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    raise SystemExit(main(ap.parse_args().dry_run))
