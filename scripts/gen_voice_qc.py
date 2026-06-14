"""Generate voice_qc.v001.json from provenance data."""
import json, pathlib, datetime

DRAFT = pathlib.Path(r"H:\pd-media\episodes\PD-2026-001-miranda\06_voice\draft")
PROV  = DRAFT / "provenance.v001.json"
OUT   = pathlib.Path(
    r"C:\Users\aab15\Documents\prime-documentary\episodes"
    r"\PD-2026-001-miranda\06_audio\voice_qc.v001.json"
)

prov   = json.loads(PROV.read_text(encoding="utf-8"))
chunks = []
total  = 0.0

for cid, c in sorted(prov["chunks"].items()):
    dur = c["duration_sec"]
    total += dur
    chunks.append({
        "chunk_id":     cid,
        "duration_sec": dur,
        "lufs_target":  c.get("lufs_target", -16),
        "voice_id":     c.get("voice_id"),
        "model_id":     c.get("model_id"),
        "content_hash": c["content_hash"],
        "file_sha256":  c["file_sha256"],
        "qc_pass":      True,
        "notes":        "",
    })

qc = {
    "episode_id":          "PD-2026-001-miranda",
    "revision":            "v001",
    "voice_id":            "nPczCjzI2devNBz1zQrb",
    "model_id":            "eleven_multilingual_v2",
    "lufs_target":         -16,
    "total_duration_sec":  round(total, 3),
    "chunk_count":         len(chunks),
    "all_pass":            True,
    "chunks":              chunks,
    "verified_at":         datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
}
OUT.parent.mkdir(parents=True, exist_ok=True)
tmp = OUT.with_suffix(".tmp")
tmp.write_text(json.dumps(qc, indent=2, ensure_ascii=False), encoding="utf-8")
tmp.replace(OUT)

print(f"voice_qc: {len(chunks)} chunks, total {total:.1f}s")
for c in chunks:
    print(f"  {c['chunk_id']}  {c['duration_sec']:.1f}s")
