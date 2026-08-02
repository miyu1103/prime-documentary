#!/usr/bin/env python3
"""Read-only: harvest episode candidates from real US case law (CourtListener v4).

Owner proposal 2026-08-02: instead of thinking of a topic and then hunting for a case,
start from the actual decided cases and pick from those. This is the candidate generator
for that. It does NOT pick a topic, and it cannot: an opinion tells you the legal holding,
never whether the story carries 40 minutes. It hands you a ranked shortlist whose facts are
already anchored to a citable published decision; a human then reads them and
`topic_demand_probe.py` measures whether the premise has an audience.

Why these lanes: the channel's measured winning pattern is 判例 x 権利 x an ordinary person
against the state (pd-analytics-findings). Each lane below is a doctrine that produces that
shape. Commercial disputes are filtered out because two companies arguing is not the show.

Scoring is explicitly proxy-based, and each proxy is named in the output so a human can
disagree with it:
  person_vs_state  caption shape - an individual or a seized res against a government body
  obscurity        citeCount. A landmark (100+ cites) is already on YouTube ten times over;
                   0 cites often means unpublished noise. The band in between is the lane.
  recency          filed recently enough that participants, records and press still exist
  concreteness     suitNature / snippet mentions a seizure, a death, a conviction, a home

Quota: CourtListener has no published hard cap for token users but does throttle. One query
per lane per page, 0.8s apart, so a full run is ~40 requests.

    py -3.11 scripts/harvest_caselaw_topics.py --dry-run
    py -3.11 scripts/harvest_caselaw_topics.py --lanes forfeiture,exoneration --pages 2
    py -3.11 scripts/harvest_caselaw_topics.py --output episodes/_planning/measurements/CASELAW_HARVEST.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict, field
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://www.courtlistener.com/api/rest/v4/search/"
DEFAULT_OUT = ROOT / "episodes" / "_planning" / "measurements" / "CASELAW_HARVEST.json"
SCHEMA_VERSION = "caselaw-harvest/v001"

# doctrine -> (label, CourtListener query). Quoted phrases are exact-phrase in their engine.
LANES: dict[str, tuple[str, str]] = {
    "forfeiture": (
        "民事没収 — 有罪判決なしに財産を取られる",
        '"civil forfeiture" AND ("innocent owner" OR "excessive fine")'),
    "structuring": (
        "現金の構造化 — 合法な金を口座ごと押さえられる",
        '("structuring" OR "31 U.S.C. 5324") AND (seizure OR forfeiture)'),
    "exoneration": (
        "冤罪 — 後から無実が確定した人",
        '("actual innocence" OR exoneration) AND ("wrongful conviction" OR "new trial")'),
    "false_confession": (
        "虚偽自白 — 取調べで自分が犯人だと言わされた",
        '"false confession" AND (interrogation OR "Miranda")'),
    "forensic_fraud": (
        "科学の誤り — 鑑定が間違っていた",
        '("forensic" OR "hair comparison" OR "bite mark" OR "arson") AND ("junk science" OR unreliable OR misconduct)'),
    "brady": (
        "証拠隠し — 検察が有利な証拠を隠した",
        '"Brady v. Maryland" AND (suppressed OR "exculpatory evidence")'),
    "qualified_immunity": (
        "免責特権 — 訴えても公務員が守られる",
        '"qualified immunity" AND ("excessive force" OR "clearly established")'),
    "fourth_amendment": (
        "捜索の限界 — どこまで踏み込めるか",
        '"Fourth Amendment" AND (curtilage OR "warrantless search" OR "thermal imaging" OR "cell site")'),
    "eminent_domain": (
        "収用 — 家を取り上げられる",
        '("eminent domain" OR "public use") AND ("just compensation" OR condemnation)'),
    "guardianship": (
        "成年後見 — 判断能力を理由に自由を失う",
        '(guardianship OR conservatorship) AND (ward OR "incapacitated person") AND (abuse OR removal)'),
    "child_removal": (
        "児童の取り上げ — 行政が子を連れて行く",
        '("termination of parental rights" OR "child protective") AND (removal OR "due process")'),
    "debtors_prison": (
        "罰金で収監 — 払えないから刑務所へ",
        '("failure to pay" OR fines OR fees) AND (indigent OR "ability to pay") AND (incarcerat* OR jail)'),
    "medical_neglect": (
        "収容中の医療放置",
        '("deliberate indifference" OR "Eighth Amendment") AND (medical OR "serious medical need") AND (jail OR prison)'),
    "wage_theft": (
        "働いた分が払われない",
        '("Fair Labor Standards Act" OR "unpaid wages") AND (retaliation OR misclassification)'),
    "whistleblower": (
        "内部告発してつぶされた人",
        '(whistleblower OR "False Claims Act") AND (retaliation OR "qui tam")'),
    "building_safety": (
        "建物・製品の安全 — 誰も止めなかった",
        '(negligence OR "wrongful death") AND (collapse OR "structural" OR "code violation" OR inspection)'),
}

GOV_PAT = re.compile(
    r"\b(united states|u\.?s\.?a?\.?|state|commonwealth|people|city|county|town|"
    r"village|borough|department|district|board|commission|sheriff|police|warden|"
    r"director|secretary|attorney general|dep't|comm'r|commissioner)\b", re.I)
CORP_PAT = re.compile(
    r"\b(inc\.?|l\.?l\.?c\.?|corp\.?|corporation|co\.|company|ltd\.?|l\.?p\.?|"
    r"insurance|bank|holdings|group|partners|associates|n\.?a\.?|plc)\b", re.I)
RES_PAT = re.compile(r"(\$[\d,]+|\bin rem\b|\bone \d{4}\b|\breal property\b|\bcurrency\b)", re.I)
CONCRETE_PAT = re.compile(
    r"\b(seiz\w+|forfeit\w+|kill\w+|death|died|shot|home|house|child|children|"
    r"convict\w+|sentenc\w+|imprison\w+|evict\w+|collaps\w+|injur\w+)\b", re.I)


def load_token() -> str:
    """Read COURTLISTENER_TOKEN from the environment or .env. Never logged."""
    tok = os.environ.get("COURTLISTENER_TOKEN", "").strip()
    if tok:
        return tok
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("COURTLISTENER_TOKEN=") and "=" in line:
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("COURTLISTENER_TOKEN not found in environment or .env")


@dataclass
class Candidate:
    """One decided case, scored as a possible episode. Scores are proxies, not verdicts."""
    lane: str
    lane_label: str
    cluster_id: int
    case_name: str
    court: str
    court_id: str
    date_filed: str
    docket: str
    cite_count: int
    citation: list[str]
    url: str
    suit_nature: str
    snippet: str
    person_vs_state: bool
    corporate_only: bool
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)


def score(c: Candidate, today: date) -> Candidate:
    """Rank by how closely the case matches the channel's measured winning shape."""
    pts, why = 0.0, []

    if c.person_vs_state:
        pts += 3.0
        why.append("普通の人 or 押収財産 vs 国家 (+3)")
    if c.corporate_only:
        pts -= 4.0
        why.append("両当事者が法人 — 商事紛争 (-4)")

    # obscurity band: landmarks are saturated, zero-cite cases are usually noise
    n = c.cite_count
    if 1 <= n <= 15:
        pts += 2.0
        why.append(f"無名だが実体はある (citeCount={n}, +2)")
    elif 16 <= n <= 60:
        pts += 1.0
        why.append(f"やや知られている (citeCount={n}, +1)")
    elif n > 100:
        pts -= 2.0
        why.append(f"著名判例 — 既出だらけ (citeCount={n}, -2)")

    try:
        yrs = (today - date.fromisoformat(c.date_filed)).days / 365.25
    except ValueError:
        yrs = 99.0
    if yrs <= 12:
        pts += 1.5
        why.append(f"{yrs:.0f}年前 — 当事者と資料が生きている (+1.5)")
    elif yrs > 30:
        pts -= 1.0
        why.append(f"{yrs:.0f}年前 — 一次資料が薄い (-1)")

    blob = f"{c.case_name} {c.suit_nature} {c.snippet}"
    hits = sorted({m.group(0).lower() for m in CONCRETE_PAT.finditer(blob)})
    if hits:
        pts += min(2.0, 0.5 * len(hits))
        why.append(f"具体的な被害語: {', '.join(hits[:6])} (+{min(2.0, 0.5*len(hits)):.1f})")
    else:
        why.append("抽象的 — 何が起きたか読み取れない (0)")

    c.score, c.reasons = round(pts, 2), why
    return c


def fetch(token: str, query: str, page: int, filed_after: str, timeout: int,
          order_by: str = "score desc") -> dict:
    """One CourtListener search page, with backoff.

    Their search endpoint throttles in bursts: a 16-lane run measured 5 lanes through and
    then 429 on every remaining one, while a single request 90 seconds later succeeded. So
    429 is a wait, not a failure, and is retried rather than dropping the lane.
    """
    params = {"q": query, "type": "o", "order_by": order_by,
              "filed_after": filed_after, "stat_Published": "on", "page": str(page)}
    url = API + "?" + urllib.parse.urlencode(params)
    headers = {"Authorization": f"Token {token}", "User-Agent": "PD-research/1.0"}
    delays = [10, 30, 60, 120]
    for i, wait in enumerate(delays + [0]):
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(url, headers=headers), timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code not in (429, 502, 503, 504) or i == len(delays):
                raise
            retry_after = e.headers.get("Retry-After")
            pause = int(retry_after) if (retry_after or "").isdigit() else wait
            print(f"    HTTP {e.code} — waiting {pause}s (retry {i + 1}/{len(delays)})",
                  flush=True)
            time.sleep(pause)
    raise RuntimeError("unreachable")


def to_candidate(lane: str, label: str, r: dict) -> Candidate:
    name = r.get("caseName") or ""
    ops = r.get("opinions") or []
    snip = re.sub(r"<[^>]+>", "", (ops[0].get("snippet") or "") if ops else "")
    parts = re.split(r"\bv\.?\s", name, maxsplit=1)
    left, right = (parts + [""])[:2]
    gov = bool(GOV_PAT.search(left) or GOV_PAT.search(right))
    corp_l, corp_r = bool(CORP_PAT.search(left)), bool(CORP_PAT.search(right))
    return Candidate(
        lane=lane, lane_label=label, cluster_id=int(r.get("cluster_id") or 0), case_name=name,
        court=r.get("court") or "", court_id=r.get("court_id") or "",
        date_filed=r.get("dateFiled") or "", docket=r.get("docketNumber") or "",
        cite_count=int(r.get("citeCount") or 0), citation=list(r.get("citation") or []),
        url="https://www.courtlistener.com" + (r.get("absolute_url") or ""),
        suit_nature=r.get("suitNature") or "", snippet=snip[:400].strip(),
        person_vs_state=gov and not (corp_l and corp_r) or bool(RES_PAT.search(name)),
        corporate_only=corp_l and corp_r)


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lanes", default="", help=f"comma-separated subset of: {','.join(LANES)}")
    ap.add_argument("--pages", type=int, default=1, help="result pages per lane (20 each)")
    ap.add_argument("--filed-after", default="2008-01-01")
    ap.add_argument("--top", type=int, default=12, help="candidates to print per lane")
    ap.add_argument("--order-by", default="score desc",
                    choices=["score desc", "dateFiled desc", "citeCount desc"],
                    help="relevance by default; dateFiled desc returns mostly fresh 0-cite appeals")
    ap.add_argument("--sleep", type=float, default=3.0,
                    help="pause between requests; their search endpoint throttles in bursts")
    ap.add_argument("--timeout", type=int, default=90)
    ap.add_argument("--output", default=str(DEFAULT_OUT))
    ap.add_argument("--force", action="store_true", help="overwrite an existing output file")
    ap.add_argument("--dry-run", action="store_true", help="print the plan; no requests, no writes")
    a = ap.parse_args(argv)

    lanes = [k.strip() for k in a.lanes.split(",") if k.strip()] or list(LANES)
    bad = [k for k in lanes if k not in LANES]
    if bad:
        print(f"unknown lane(s): {', '.join(bad)}", file=sys.stderr)
        return 2

    if a.dry_run:
        print(f"DRY RUN — {len(lanes)} lanes x {a.pages} page(s) "
              f"= {len(lanes) * a.pages} requests, filed_after={a.filed_after}\n")
        for k in lanes:
            print(f"  {k:<18} {LANES[k][0]}\n{' ' * 21}{LANES[k][1]}")
        print(f"\nwould write {a.output}")
        return 0

    out_path = Path(a.output)
    if out_path.exists() and not a.force:
        print(f"{out_path} exists; pass --force to overwrite", file=sys.stderr)
        return 2

    token = load_token()
    today = datetime.now(timezone.utc).date()
    all_c: list[Candidate] = []
    errors: list[dict] = []

    for k in lanes:
        label, query = LANES[k]
        got: list[Candidate] = []
        for page in range(1, a.pages + 1):
            try:
                d = fetch(token, query, page, a.filed_after, a.timeout, a.order_by)
            except urllib.error.HTTPError as e:
                # one bad lane must not stop the harvest
                errors.append({"lane": k, "page": page, "http": e.code})
                break
            except Exception as e:
                errors.append({"lane": k, "page": page, "error": str(e)[:120]})
                break
            for r in d.get("results") or []:
                got.append(score(to_candidate(k, label, r), today))
            if not d.get("next"):
                break
            time.sleep(a.sleep)
        seen: set[tuple] = set()
        uniq: list[Candidate] = []
        for c in got:  # the same cluster comes back under sibling opinions
            key = (c.cluster_id, c.case_name.lower(), c.date_filed)
            if key in seen:
                continue
            seen.add(key)
            uniq.append(c)
        got = uniq
        got.sort(key=lambda c: (-c.score, -c.cite_count))
        all_c.extend(got)
        print(f"\n=== {k} — {label}   ({len(got)} hits)")
        for c in got[:a.top]:
            flag = "★" if c.score >= 6 else " "
            print(f" {flag} {c.score:>5.1f}  {c.case_name[:58]:<58} {c.date_filed}  "
                  f"{c.court_id:<9} cites={c.cite_count}")
        time.sleep(a.sleep)

    all_c.sort(key=lambda c: -c.score)
    payload = {"schema_version": SCHEMA_VERSION,
               "measured_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "source": "CourtListener REST v4 /search/ type=o stat_Published=on",
               "filed_after": a.filed_after, "lanes": lanes, "pages_per_lane": a.pages,
               "caveat": "Scores are proxies for the channel's winning shape, not editorial "
                         "judgement. An opinion states a holding, never whether the story "
                         "carries 40 minutes. Run topic_demand_probe.py on the shortlist next.",
               "errors": errors, "count": len(all_c),
               "candidates": [asdict(c) for c in all_c]}
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(out_path)

    print(f"\n{'=' * 78}\nTOP 25 OVERALL")
    for c in all_c[:25]:
        print(f" {c.score:>5.1f}  {c.lane:<16} {c.case_name[:52]:<52} {c.date_filed} "
              f"cites={c.cite_count}")
    if errors:
        print(f"\n{len(errors)} lane(s) failed: "
              f"{', '.join(sorted({e['lane'] for e in errors}))}")
    try:
        shown = out_path.relative_to(ROOT)
    except ValueError:
        shown = out_path  # --output may point outside the repo
    print(f"\nwrote {shown}  ({len(all_c)} candidates)")
    print("NEXT: read the top rows, then measure demand:\n"
          '  py -3.11 scripts/topic_demand_probe.py "<premise in plain English> documentary"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
