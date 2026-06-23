#!/usr/bin/env python
"""Validate one PD episode's script-stage artifacts.

Usage:
    .venv/Scripts/python.exe scripts/validate_episode.py 6
    .venv/Scripts/python.exe scripts/validate_episode.py PD-2026-006-terry

Checks (script stage): schema validity (topic, claims, annotated, manifest, approval, sources),
claim/span consistency (no dangling claim ids, no unused claims, chapter span_ids == spans),
manifest artifact checksum == actual annotated hash, and script_qc metrics
(readability, length/timing, AI-filler). Exit code 0 = OK, 1 = problems.
"""
import sys, os, json, re, glob, hashlib
from jsonschema import Draft202012Validator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPDIR = os.path.join(ROOT, "episodes")
BANNED = ["but here's the thing", "what happened next changed everything", "the answer may surprise you",
          "in a world where", "little did they know", "the truth is more complicated",
          "at the end of the day", "needless to say"]

def syll(w):
    w = re.sub(r'[^a-z]', '', w.lower())
    if not w:
        return 0
    n = len(re.findall(r'[aeiouy]+', w))
    if w.endswith('e') and n > 1:
        n -= 1
    return max(1, n)

def resolve(arg):
    if os.path.isdir(os.path.join(EPDIR, arg)):
        return arg
    hits = [os.path.basename(p) for p in glob.glob(os.path.join(EPDIR, f"PD-*-{int(arg):03d}-*"))] \
        if arg.isdigit() else []
    if not hits:
        hits = [os.path.basename(p) for p in glob.glob(os.path.join(EPDIR, f"*{arg}*")) if os.path.isdir(p)]
    if len(hits) == 1:
        return hits[0]
    raise SystemExit(f"Could not resolve episode '{arg}'. Matches: {hits}")

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: validate_episode.py <episode-number-or-id>")
    ep = resolve(sys.argv[1])
    b = os.path.join(EPDIR, ep)
    sd = os.path.join(ROOT, "schemas")
    sch = {k: load(os.path.join(sd, v)) for k, v in {
        "topic": "topic.schema.json", "claims": "claim-ledger.schema.json",
        "ann": "script-annotated.schema.json", "manifest": "episode-manifest.schema.json",
        "approval": "approval.schema.json", "source": "source.schema.json"}.items()}
    problems = []

    def val(schema, doc, label):
        errs = [f"{label}: {list(e.path)} {e.message}" for e in Draft202012Validator(schema).iter_errors(doc)]
        problems.extend(errs)

    topic = load(f"{b}/00_topic/topic.v001.json")
    claims = load(f"{b}/01_research/claims.v001.json")
    ann = load(f"{b}/03_script/script.annotated.v001.json")
    man = load(f"{b}/manifest.json")
    val(sch["topic"], topic, "topic"); val(sch["claims"], claims, "claims")
    val(sch["ann"], ann, "annotated"); val(sch["manifest"], man, "manifest")
    # This is a SCRIPT-STAGE validator: only generic request->decision approvals match
    # approval.schema.json. Publish-gate approvals (title/thumbnail/publish/schedule) use a
    # different shape (approved_at/gate/scheduled_at_utc, no requested_at) and are validated
    # at publish time (pd-publish-preflight), not here -- skip them instead of mis-applying.
    skipped_publish = []
    for fp in glob.glob(f"{b}/approvals/APR-*.json"):
        ap = load(fp)
        if "requested_at" not in ap and ("gate" in ap or "scheduled_at_utc" in ap):
            skipped_publish.append(os.path.basename(fp))
            continue
        val(sch["approval"], ap, os.path.basename(fp))
    for i, s in enumerate(load(f"{b}/01_research/sources.v001.json")):
        val(sch["source"], s, f"source[{i}]")
    # events + qc parse
    for ln in open(f"{b}/events/events.jsonl", encoding="utf-8"):
        if ln.strip():
            json.loads(ln)
    load(f"{b}/03_script/script_qc.v001.json")

    # consistency
    cids = {c["claim_id"] for c in claims["claims"]}
    annids = {c for sp in ann["spans"] for c in sp["claim_ids"]}
    md = open(f"{b}/03_script/script.en.v001.md", encoding="utf-8").read()
    sids = set(re.findall(r"CLM-\d{4}", md))
    for d in sorted((annids | sids) - cids):
        problems.append(f"dangling claim ref: {d}")
    listed = [s for c in ann["chapters"] for s in c["span_ids"]]
    spanids = [s["span_id"] for s in ann["spans"]]
    if set(listed) ^ set(spanids):
        problems.append(f"chapter/span mismatch: {sorted(set(listed) ^ set(spanids))}")
    # manifest checksum vs annotated
    actual = "sha256:" + hashlib.sha256(open(f"{b}/03_script/script.annotated.v001.json", "rb").read()).hexdigest()
    annart = [a for a in man["artifacts"] if a["artifact_type"] == "annotated_script"]
    if annart and annart[0]["checksum"] != actual:
        problems.append(f"manifest checksum != annotated hash ({annart[0]['checksum'][:18]}.. vs {actual[:18]}..)")

    # QC metrics
    vo = re.sub(r'\[CLM-\d{4}\]', '', " ".join(re.findall(r'^\[VO:\]\s*(.+)$', md, flags=re.M)))
    vo = re.sub(r'\s+', ' ', vo).strip()
    sents = [s for s in re.split(r'(?<=[.!?])\s+', vo) if s.strip()]
    words = re.findall(r"[A-Za-z']+", vo)
    nw, ns = len(words), max(1, len(sents))
    fk = 0.39 * (nw / ns) + 11.8 * (sum(syll(w) for w in words) / max(1, nw)) - 15.59
    dur = nw / 150.0
    filler = {x: vo.lower().count(x) for x in BANNED if vo.lower().count(x) > 0}
    warns = []
    # Duration band. Standard episodes: 10.0-12.8 narration-minutes. FEATURE episodes
    # (manifest.target_duration_minutes >= 20) use a wider narration band that scales
    # with the planned runtime: feature cuts use deliberate silence + visual/music
    # sequences, so narration-minutes run well below total runtime. See
    # decisions/0003-feature-duration-profile.md (ADR-0003). This is an explicit,
    # documented profile keyed off an existing manifest field, applied ONLY when the
    # manifest declares a feature-length target -- NOT a silent weakening of the
    # standard gate (invariant 15); the standard 10.0-12.8 band is unchanged.
    tdm = man.get("target_duration_minutes")
    if isinstance(tdm, (int, float)) and tdm >= 20:
        lo, hi = 0.50 * tdm, 1.05 * tdm
        band = f"{lo:.1f}-{hi:.1f}min (feature; target {tdm:.0f}min runtime)"
    else:
        lo, hi = 10.0, 12.8
        band = "10.0-12.8min"
    if not (lo <= dur <= hi):
        warns.append(f"narration {dur:.1f}min outside {band}")
    if fk > 9.5:
        warns.append(f"readability FK {fk:.1f} > 9.5")
    if filler:
        warns.append(f"AI-filler {filler}")

    print(f"Episode: {ep}   state={man.get('state')}   annotated qc_status={ann.get('qc_status')}")
    print(f"QC: words={nw} FK={fk:.1f} duration={dur:.1f}min sentences={ns}")
    print(f"Schema errors: {len(problems)} | claims={len(cids)} spans={len(spanids)}")
    if skipped_publish:
        print(f"  note: skipped {len(skipped_publish)} publish-gate approval(s) (validated at publish preflight): {skipped_publish}")
    for p in problems:
        print("  ERROR:", p)
    for w in warns:
        print("  QC-WARN:", w)
    ok = not problems
    print("\nRESULT:", "PASS" if ok and not warns else ("PASS (with QC warnings)" if ok else "FAIL"))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
