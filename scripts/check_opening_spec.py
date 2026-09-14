"""Check the EP66 opening spec against the owner's manual, line by line, instead of asserting.

Asked four times whether the document follows the rules. I have answered yes twice and been wrong
once already (section 0 was missing and I had decided it did not apply). So this reads the manual's
requirements as a list and searches the document for evidence of each, printing what it found. A
requirement with no evidence is reported as missing, not explained away.

The manual is C:/Users/aab15/CLAUDE.md. Its literal numbers (fps 60, durationInFrames 180, the
props title/subtitle/accent/hasLogo) belong to the pino-channel opening it was written for; the
manual itself says a new design replaces the numbers. So this checks that each REQUIREMENT is
answered, not that the values match pino's.
"""
import re
import sys
from pathlib import Path

import argparse

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(r"C:\Users\aab15\Documents\prime-documentary")


# Split out of module scope 2026-08-10 so check_design_doc.py can IMPORT the CHECKS list
# instead of retyping it. Retyping this list is exactly how it came to be ten items short.
# The CLI below behaves as before; only the packaging moved.
def find_doc(slug: str):
    """Newest episodes/_planning/EP*_<slug>_PACKAGING.v*.md, or None when there is none."""
    docs = sorted((ROOT / "episodes" / "_planning").glob(f"EP*_{slug}_PACKAGING.v*.md"))
    return docs[-1] if docs else None


def opening_section(text: str) -> str:
    """The opening design spec is section 7 of the packaging document and nothing else.

    Returns "" when there is no section 7, which makes every must-exist check below fail.
    An absent section is a MISSING answer, never an exemption.
    """
    start = text.find("## 7. OPENING OVERLAY")
    if start < 0:
        return ""
    end = text.find("\n## 8.", start)
    return text[start:end if end > 0 else len(text)]


def run_checks(sec: str) -> list[tuple[str, bool, str, bool]]:
    """(label, ok, matched_snippet, must_exist) for every entry in CHECKS, against `sec`."""
    results = []
    for label, pat, must in CHECKS:
        hit = re.search(pat, sec, re.M | re.I)
        ok = bool(hit) if must else not bool(hit)
        results.append((label, ok, hit.group(0)[:44].replace("\n", " ") if hit else "", must))
    return results

CHECKS = [
    # (label, regex, must_exist)
    ("§0 解像度",                r"1920\s*[×x]\s*1080", True),
    ("§0 fps",                   r"\bfps\b.*\b30\b|\b30\b.*fps", True),
    ("§0 composition id",        r"composition id|Ep66Openfields", True),
    ("§0 durationInFrames",      r"durationInFrames", True),
    ("§0 コーデック/CRF",         r"h264|libx264", True),
    ("§0 CRF16",                 r"CRF\s*\*?\*?16|crf.*16", True),
    ("§0 pixelFormat",           r"yuv420p", True),
    ("§0 音声コーデック",         r"\baac\b", True),
    ("§0 npm i motion-blur",     r"npm i .*motion-blur", True),
    ("§1 秒数ベースのタイムライン", r"秒数ベースのタイムライン", True),
    ("§2 イージング種別を明記",    r"Easing\.(out|in)\(Easing\.cubic\)", True),
    ("§2 spring と damping",      r"spring\(.*damping", True),
    ("§2 移動量（px）",           r"[-+]?\d+\s*(?:→|->)\s*0\s*px|→\s*0\s*px", True),
    ("§2 ディレイ（スタッガー）",  r"スタッガー|\+\d+F ずつ", True),
    ("§3 レイヤー構成",           r"レイヤー構成", True),
    ("§3 3層以上",               r"^\s*4\.\s", True),
    ("§4 props と型",            r"type BrandOpeningProps|props と型", True),
    ("§5 確認方法 studio",        r"npm run studio", True),
    ("§5 量産レンダーコマンド",    r"npx remotion render", True),
    ("品質 モーションブラー Trail", r"Trail", True),
    ("品質 マスク切り上がり",      r"overflow\s*:\s*hidden", True),
    ("品質 opacity単独でない",     r"併用", True),
    ("品質 fpsから算出",          r"useVideoConfig|Math\.round\(.*fps\)", True),
    ("品質 定数化",               r"定数として1箇所|OVERLAY\s*=\s*\{", True),
    ("禁止 等速線形が無い",        r"Easing\.linear|linear", False),
    # --- added 2026-08-10 after reading the manual line by line against this list. The five
    # settings below are named inside the manual's "remotion.config.ts の内容" bullet and the
    # first version of this audit collapsed them into four; the rest were simply absent.
    ("§0 画像フォーマット png",    r"\bpng\b", True),
    ("§0 concurrency",           r"concurrency|並列", True),
    ("§0 colorSpace",            r"colorSpace|bt709|色空間", True),
    ("§0 音声ビットレート",        r"\b\d{2,3}k\b|kbps|ビットレート", True),
    ("§0 GPU設定",               r"GPU|angle|gl\b", True),
    ("§1 全区間を記述",           r"タイムライン[\s\S]{0,400}?\|\s*out\s*\|", True),
    ("§3 レイヤーの種類を明記",     r"スクリム|グラデ|グロー|背景|本編カット", True),
    ("§4 props名を列挙",          r"seriesLabel|title\s*:|subtitle", True),
    ("正典実装を基準にしている",     r"Bookends|BrandOpening", True),
    # The manual's headline rule. These are the words it names as forbidden, plus the family of
    # vague sizing that replaces a number.
    ("禁止 抽象表現",             r"かっこよく|いい感じ|適度に|うまく|きれいに|それっぽく", False),
]

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slug", required=True)
    a = ap.parse_args()

    doc = find_doc(a.slug)
    if doc is None:
        print(f"[opening-spec] no EP*_{a.slug}_PACKAGING.v*.md -- nothing to audit")
        return 0
    sec = opening_section(doc.read_text(encoding="utf-8"))
    print(f"section 7 is {len(sec)} chars, {sec.count(chr(10))} lines\n")

    missing, extra = [], []
    for label, ok, snippet, must in run_checks(sec):
        mark = "ok " if ok else "MISSING" if must else "VIOLATION"
        print(f"[{mark:9s}] {label:26s} {snippet}")
        if not ok:
            (missing if must else extra).append(label)

    print()
    if not missing and not extra:
        print("すべての要件に該当箇所あり")
    else:
        if missing:
            print(f"欠落 {len(missing)}件: {missing}")
        if extra:
            print(f"禁止事項の混入 {len(extra)}件: {extra}")
    return 1 if (missing or extra) else 0


if __name__ == "__main__":
    sys.exit(main())
