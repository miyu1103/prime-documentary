#!/usr/bin/env python3
r"""Build the EP35 (hinders) scene/shot plan — the $0 assembly foundation.

State transition: script_verified -> scene_planned. Maps every verified-script
[VO:] beat to a scene, wiring it to the REAL assets that already exist:
  - FigureBeats F1-F21 (remotion/src/components/hinders FIGURE_REGISTRY)
  - hero mp4s (hero_bsa_flow / hero_frozen_account / hero_carole_after)
  - generated stills S001-S068 (+ _depth) in remotion/public/hinders/img
Figure placement is aligned to EP35_hinders_ANIMATION_ASSETS.v001.md (act/reveal).

Timing note: cut/caption seconds are NARRATION-derived and are the audio thread's
lane (voice_plan.v001 -> narration_index). This plan is ORDINAL (beat order +
act minute-anchors from the script), so build_case_film_audio.py / the film
builder fills exact seconds once narration_index lands. Captions carry the
verbatim [VO:] text; the mix step re-times them to the master.

No paid calls, no external side effects, no overwrite of another thread's audio
artifacts. Writes episodes/PD-2026-035-hinders/04_scenes/scene_plan.v001.json.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EP = "PD-2026-035-hinders"
OUT = ROOT / "episodes" / EP / "04_scenes" / "scene_plan.v001.json"

# Each beat: scene, act, section, anchor (script minute), purpose, claims,
# figure (FIGURE_REGISTRY id or None), hero mp4 key (or None), visual_mode,
# treatment (depth/card/bleed/scan/...), on_screen_text, motion, sfx,
# caption (verbatim [VO:] — trimmed of [CLM] tags), image_hint.
BEATS = [
    dict(scene="S001", act="HOOK", section="COLD_OPEN_THREAT", anchor="0:00", purpose="8s threat hook — pays off in Act V",
         claims=["CLM-0002", "CLM-0004"], figure=None, hero=None, visual_mode="object", treatment="depth",
         on_screen_text=["UNDER $10,000", "NO CRIME. NO CHARGE."], motion="pen writes a figure just under the $10k line, stops short",
         sfx="pen_scratch -> single low_impact_stamp",
         caption="No crime. No charge. You kept every deposit under ten thousand dollars — and the government took your account anyway.",
         image_hint="deposit-slip close-up, pen under the ten-thousand line"),
    dict(scene="S002", act="OP", section="TITLE", anchor="0:07", purpose="branded bookend title card", claims=[],
         figure=None, hero=None, visual_mode="typography", treatment="card",
         on_screen_text=["FOLLOWING THE RULE."], motion="PD bookend over bank-ledger motif; title mask-reveal (no static logo)",
         sfx="tight riser resolving into a held tone", caption="", image_hint="bank-ledger motif backdrop"),

    # ---- ACT I ----
    dict(scene="S003", act="I", section="ACT1_THE_RULE", anchor="0:19", purpose="introduce Carole / Mrs. Lady's, second-person stakes",
         claims=["CLM-0001"], figure="F1", hero=None, visual_mode="location", treatment="depth",
         on_screen_text=["38 YEARS", "MRS. LADY'S"], motion="diner exterior; anonymous hands at register; cash bag to bank (no face)",
         sfx="warm room-tone, register drawer, bank door chime",
         caption="For thirty-eight years, a small cash restaurant sat off the lakes country of northwest Iowa. Mrs. Lady's. A woman in her late sixties ran it six days a week. She was not hiding anything. What the government did to her should worry anyone who has ever run a small business on cash.",
         image_hint="modest diner exterior off a lakes road; register; cash bag"),
    dict(scene="S004", act="I", section="ACT1_THE_RULE", anchor="1:20", purpose="the $10k reporting rule + 1970 BSA origin",
         claims=["CLM-0003", "CLM-0015"], figure="F2", hero="hero_bsa_flow", visual_mode="diagram", treatment="depth",
         on_screen_text=["THE BANK FILES THIS — NOT YOU", "1970"], motion="CTR form fills a teller screen; 1970 dirty-money flow drips to a small till (hero fluid)",
         sfx="keyboard tap, soft archival stamp",
         caption="There is a banking rule almost nobody bothers to explain. If you deposit more than ten thousand dollars in cash, your bank files a single report. That obligation falls on the bank, not on you. The rule came out of a nineteen-seventy law written to track organized crime — never aimed at a cash register in a diner.",
         image_hint="teller screen with a currency transaction report; 1970 ledger stamp"),
    dict(scene="S005", act="I", section="ACT1_THE_RULE", anchor="2:10", purpose="structuring added 1986 — staying small is the crime",
         claims=["CLM-0015", "CLM-0004"], figure="F2b", hero=None, visual_mode="diagram", treatment="card",
         on_screen_text=["1970 -> 1986", "KEEPING IT SMALL = THE CRIME (§5324)"], motion="timeline 1970->1986; one statute splits into two branches, the second glows",
         sfx="two-note stinger on the split",
         caption="The offense that trapped her was not even part of that original law. It was added sixteen years later, in nineteen eighty-six, when Congress made it a separate crime to deliberately split your cash into smaller deposits to keep them under the ten-thousand-dollar line.",
         image_hint="statute splitting into two branches"),
    dict(scene="S006", act="I", section="ACT1_THE_RULE", anchor="2:55", purpose="name the crime — STRUCTURING inverts what a crime is",
         claims=["CLM-0004"], figure="F2b", hero=None, visual_mode="typography", treatment="card",
         on_screen_text=["STRUCTURING"], motion="the word STRUCTURING mask-reveals; a row of small deposits below the $10k line lights up as 'suspicious'",
         sfx="low inversion sweep",
         caption="That new crime has a name. Structuring. And the name inverts what you think a crime is. The law watches you for staying small, and it decides, on its own, what a pattern of small deposits means — long before it asks you a single question.",
         image_hint="row of small deposits below a threshold line"),
    dict(scene="S007", act="I", section="ACT1_THE_RULE", anchor="3:05", purpose="the $10k threshold + ordinary rhythm read as a plan",
         claims=["CLM-0004"], figure="F3", hero=None, visual_mode="data", treatment="depth",
         on_screen_text=["$10,000 REPORTING THRESHOLD", "a plan?"], motion="deposit-by-day bar chart; 3D threshold gauge; a hand circles the pattern in red",
         sfx="marker squeak, low unease bed",
         caption="To stay on the right side of it, you would first have to know the reporting threshold exists, and then know that trying to stay beneath it is itself the offense. To an investigator reading a bank printout months later, that ordinary rhythm can be made to look like a plan. And once it looks like a plan, the burden of proving it was not lands on the person who made the deposits.",
         image_hint="deposit-by-day bar chart circled in red"),
    dict(scene="S008", act="I", section="ACT1_THE_RULE", anchor="4:00", purpose="the habit from her mother; the law was watching all along",
         claims=["CLM-0006", "CLM-0001"], figure="F4", hero=None, visual_mode="object", treatment="depth",
         on_screen_text=["THE LAW WAS WATCHING THE ENTIRE TIME"], motion="mother's old ledger dissolves to the routine years on; faint statute text scrolls unnoticed; threshold line cracks",
         sfx="paper, a distant clock, a held minor chord",
         caption="She had kept her deposits under ten thousand for years. By her own account, the habit came from her mother, who told her to stay under the line and skip the extra bank paperwork. She never knew banks reported large deposits at all. The law was watching the entire time. She simply had no idea it had started watching her.",
         image_hint="old ledger in a mother's hand; faint statute scroll"),

    # ---- ACT II ----
    dict(scene="S009", act="II", section="ACT2_GUILTY_UNTIL", anchor="4:20", purpose="the seizure — $32,820.56 to zero",
         claims=["CLM-0002"], figure="F5", hero="hero_frozen_account", visual_mode="data", treatment="depth",
         on_screen_text=["$32,820.56", "SEIZED"], motion="balance ticks to $32,820.56, hard-cut to $0.00 with SEIZED; frozen-account ice fractures (hero)",
         sfx="data-drain, hard zero thud",
         caption="In two thousand thirteen, without a warning she could see coming, the government emptied the restaurant's checking account. Thirty-two thousand, eight hundred twenty dollars and fifty-six cents, gone in a single legal stroke. It is not overdrawn. It is seized.",
         image_hint="account balance draining to zero with SEIZED overlay"),
    dict(scene="S010", act="II", section="ACT2_GUILTY_UNTIL", anchor="5:00", purpose="never charged; bills still came",
         claims=["CLM-0002"], figure=None, hero=None, visual_mode="object", treatment="card",
         on_screen_text=["CHARGES: NONE"], motion="a CHARGES: NONE card; unpaid invoices stack against a padlocked account icon",
         sfx="padlock click, paper piling",
         caption="She was never charged with a crime. Not money laundering, not tax evasion. And the bills still came. The food still had to be bought. Her savings were locked inside a legal case with a name that tells you almost everything you need to know.",
         image_hint="CHARGES: NONE card; padlocked account; unpaid invoices"),
    dict(scene="S011", act="II", section="ACT2_GUILTY_UNTIL", anchor="6:00", purpose="the in-rem caption — prosecuting the money",
         claims=["CLM-0002"], figure="F6", hero=None, visual_mode="typography", treatment="card",
         on_screen_text=["UNITED STATES v. $32,820.56 IN U.S. CURRENCY"], motion="court caption types on; the defendant line is a dollar figure, not a name; empty dock dolly",
         sfx="typewriter strike on the number",
         caption="The case was not called The United States versus Carole Hinders. It was called The United States versus thirty-two thousand, eight hundred twenty dollars and fifty-six cents. The government was not prosecuting her. It was prosecuting her money.",
         image_hint="court caption with a dollar figure as defendant"),
    dict(scene="S012", act="II", section="ACT2_GUILTY_UNTIL", anchor="6:40", purpose="civil forfeiture runs backwards — burden inverted",
         claims=["CLM-0005"], figure="F5b", hero=None, visual_mode="diagram", treatment="card",
         on_screen_text=["PROVE IT INNOCENT"], motion="scales-of-justice flip: presumed-innocent plate slides under the money; owner pushes uphill against a federal seal",
         sfx="slow mechanical flip, strained low tone",
         caption="This is civil forfeiture, and it runs backwards from everything you assume. In a criminal court, you are presumed innocent. Here, the money itself was treated as guilty, and it was on her to prove it innocent. The government does not have to convict you. It only has to hold your money — and wait.",
         image_hint="scales of justice flipping; owner vs federal seal"),
    dict(scene="S013", act="II", section="ACT2_GUILTY_UNTIL", anchor="7:10", purpose="the trap: fight costs more than the cash — walk away",
         claims=["CLM-0005"], figure="F7", hero=None, visual_mode="diagram", treatment="card",
         on_screen_text=["SEIZED -> LAWYER -> COSTS -> WALK AWAY -> PERMANENT"], motion="loop diagram of the trap; an anonymous owner turns and leaves; a row greys out",
         sfx="closing-loop click, footsteps fading",
         caption="To fight, you need a lawyer. A lawyer costs money. Your money is the thing the government is holding. Plenty of people do the arithmetic and walk away. Every time that happens, the seizure becomes permanent without a judge ever ruling on whether a crime occurred. It only needs you to give up.",
         image_hint="loop diagram; anonymous owner leaving"),
    dict(scene="S014", act="II", section="ACT2_GUILTY_UNTIL", anchor="7:20", purpose="the inversion structure + the coming Treasury number",
         claims=["CLM-0014"], figure="F8", hero=None, visual_mode="diagram", treatment="scan",
         on_screen_text=["STRUCTURING SEIZURES", "coming"], motion="civil-forfeiture inversion bars rotate; Treasury watchdog seal; file boxes wheeled out; a redacted number holds 'coming'",
         sfx="file-box rumble, suspended sting",
         caption="And she was not the only one it was built for. A government watchdog inside the Treasury would go back and pull the files on these structuring seizures, hundreds of them, and what it found would turn one grandmother's misfortune into a number that indicted the entire practice. That number is coming.",
         image_hint="Treasury seal; STRUCTURING SEIZURES file boxes"),
    dict(scene="S015", act="II", section="ACT2_GUILTY_UNTIL", anchor="8:05", purpose="the pattern was the case; she becomes the one whose story got out",
         claims=["CLM-0019"], figure="F9", hero=None, visual_mode="data", treatment="depth",
         on_screen_text=["NO THEFT / NO DRUGS / NO VICTIM"], motion="bank statement deposits ringed; three cards flip; the person thins to a silhouette beside the case number",
         sfx="soft flip per card, hollow room-tone",
         caption="Investigators decided the pattern itself was the offense. No theft. No drugs. No victim. A small-town cook who, they said, made her deposits too small, too often. In a case against money, the person barely appears at all. She would turn out to be the one whose story got out.",
         image_hint="bank statement with deposits ringed; silhouette beside a case number"),

    # ---- ACT III ----
    dict(scene="S016", act="III", section="ACT3_FRONT_PAGE", anchor="8:34", purpose="NYT front page 2014-10-25",
         claims=["CLM-0007"], figure="F10", hero=None, visual_mode="typography", treatment="card",
         on_screen_text=["LAW LETS I.R.S. SEIZE ACCOUNTS ON SUSPICION, NO CRIME REQUIRED", "OCT 25, 2014"], motion="front page assembles; headline mask-reveals verbatim; paper multiplies across newsstands and phone screens",
         sfx="printing-press roll, rising murmur",
         caption="Someone noticed. On the twenty-fifth of October, two thousand fourteen, The New York Times put her on its front page. Overnight, the country was reading about a statute built to catch money launderers, turned on a woman who sold Mexican food out of a small building in Iowa.",
         image_hint="newspaper front page; newsstands; phone screens"),
    dict(scene="S017", act="III", section="ACT3_FRONT_PAGE", anchor="9:30", purpose="IJ + IRS policy signal; dismissal (on paper she won)",
         claims=["CLM-0010", "CLM-0008", "CLM-0009"], figure="F11", hero=None, visual_mode="diagram", treatment="depth",
         on_screen_text=["POLICY CHANGE — LEGAL-SOURCE CASES", "DISMISSED / FUNDS RETURNED", "On paper"], motion="IJ case-file opens; agency policy-change memo; DISMISSED/FUNDS RETURNED stamp; playhead timeline (hero motion) with a persistent node",
         sfx="confident stamp that leaves a faint doubt-tone",
         caption="The Institute for Justice took her on and demanded the money back. The tax agency signaled a change: going forward it would generally stop seizing money where the cash came from a plainly legal source. About three months after her lawyers stepped in, the government moved to dismiss and return every dollar. On paper, she won.",
         image_hint="IJ case file; policy-change memo; DISMISSED stamp"),
    dict(scene="S018", act="III", section="ACT3_FRONT_PAGE", anchor="10:20", purpose="the fine print — dismissed WITHOUT PREJUDICE",
         claims=["CLM-0009"], figure="F12", hero=None, visual_mode="typography", treatment="card",
         on_screen_text=["WITHOUT PREJUDICE"], motion="dismissal order zooms to two words WITHOUT PREJUDICE, which lock into a persistent corner node; seizure vs return collide",
         sfx="legal-stamp, quiet ominous pad",
         caption="But the fine print is where this turns. It dismissed the case 'without prejudice.' It walked away without conceding a thing, and kept the right to come back. It did not apologize. It did not say she was innocent. Those two words come back later, and they cost her.",
         image_hint="dismissal order zooming to WITHOUT PREJUDICE"),
    dict(scene="S019", act="III", section="ACT3_FRONT_PAGE", anchor="11:00", purpose="a memo is not a law; luck, not correction",
         claims=["CLM-0008"], figure="F13", hero=None, visual_mode="diagram", treatment="scan",
         on_screen_text=["AGENCY POLICY — NOT LAW"], motion="one lit front page beside dozens of dark unreported account icons; a memo flexes narrow and wide; a dismissed stamp",
         sfx="single bright note against a field of muted ones",
         caption="For a moment it looked like the system had corrected itself. But what it took was a reporter, a front page, and a national audience — a run of luck almost nobody in her position gets. And a policy memo is not a law. It is an instruction the agency writes to itself. Nobody outside the agency voted on it. Seizures like hers kept happening anyway.",
         image_hint="one lit front page among dark account icons; memo card"),

    # ---- ACT IV ----
    dict(scene="S020", act="IV", section="ACT4_KEPT_HAPPENING", anchor="11:37", purpose="a false ending; the memo did not reach an open case",
         claims=["CLM-0008"], figure=None, hero=None, visual_mode="typography", treatment="card",
         on_screen_text=["THE END?"], motion="a false 'THE END' card cracks; a memo page blows across a map from Iowa toward the Southeast, not arriving",
         sfx="fake resolve chord that snaps",
         caption="You would think that is where it ends. New policy, money returned. But a memo is only words on a page, and words on a page do not always reach a case already sitting open in a field office in another part of the country.",
         image_hint="cracked THE END card; memo blowing across a map"),
    dict(scene="S021", act="IV", section="ACT4_KEPT_HAPPENING", anchor="12:20", purpose="McLellan NC — $107,702.66 / 301 deposits / ~$2M",
         claims=["CLM-0012", "CLM-0013", "CLM-0004"], figure="F14", hero=None, visual_mode="data", treatment="depth",
         on_screen_text=["$107,702.66 SEIZED", "301 DEPOSITS", "~$2M / 3 YRS"], motion="Iowa|NC split (hero 3D parallel); rural store; balance drains to $107,702.66; ticker 0->301",
         sfx="register bell per small sale, a drain on the seizure",
         caption="In Fairmont, North Carolina, a man named Lyndon McLellan ran a country convenience store. The government seized one hundred seven thousand, seven hundred two dollars and sixty-six cents — his entire business account, over the same theory used on Carole. Three hundred one deposits. Around two million dollars in legitimate sales over three years, every one under ten thousand dollars.",
         image_hint="rural NC convenience store; counter of small sales"),
    dict(scene="S022", act="IV", section="ACT4_KEPT_HAPPENING", anchor="12:55", purpose="the ledger of 301 deposits; same law, outcome withheld",
         claims=["CLM-0011", "CLM-0013"], figure="F14b", hero=None, visual_mode="data", treatment="depth",
         on_screen_text=["301 DEPOSITS", "SAME LAW / SAME CLAIM / ?"], motion="301-instanced ledger lights up (hero); two case cards side by side, identical law, outcome fields blur to '?'",
         sfx="paired tone that leaves one string unresolved",
         caption="A difference here would come to sting. Two people, McLellan and Carole, caught by the same law, making the same argument — that the money was clean and the seizure was wrong. You would expect the law to treat them the same way in the end. It does not, and the reason will land in a few minutes.",
         image_hint="two case cards side by side; ledger grid"),
    dict(scene="S023", act="IV", section="ACT4_KEPT_HAPPENING", anchor="13:45", purpose="Carole sold Mrs. Lady's while the case dragged",
         claims=["CLM-0018"], figure="F14c", hero=None, visual_mode="location", treatment="depth",
         on_screen_text=["FOR SALE"], motion="rural store dolly; a FOR SALE sign on the diner; returned balance lands beside a shuttered storefront",
         sfx="sign creak, quiet piano fall",
         caption="For Carole, the fight had already taken its price. According to her lawyers and the reporting, while her money was tied up she sold Mrs. Lady's, the restaurant she had built over thirty-eight years. You can return a bank balance. You cannot return the years, or the thing a person spent them building.",
         image_hint="FOR SALE sign on the diner; shuttered storefront"),
    dict(scene="S024", act="IV", section="ACT4_KEPT_HAPPENING", anchor="14:30", purpose="the TIGTA number — 278 / 91% / $17.1M",
         claims=["CLM-0014"], figure="F15", hero=None, visual_mode="data", treatment="depth",
         on_screen_text=["278 TRACEABLE CASES", "91% LEGAL SOURCE", "231 CASES / $17.1M"], motion="278-point cloud composes; 91% flips green (hero); a bar fills to nine-in-ten; 231 / $17.1M",
         sfx="data-fills, decisive low hit on 91%",
         caption="And then came the number this whole case had been circling. In a sample of two hundred seventy-eight cases where investigators could trace where the money came from, ninety-one percent involved money from legal sources. Nine in ten. Across more than two hundred of those cases, the government had taken in around seventeen million dollars from people whose money it could not tie to any crime. Carole was not an unlucky exception. She was a representative case.",
         image_hint="data panel: 278 -> 91% legal source", secondary=["F15b"]),

    # ---- ACT V ----
    dict(scene="S025", act="V", section="ACT5_WHAT_THEY_BUILT", anchor="15:06", purpose="what 'without prejudice' cost — 2016 no fees",
         claims=["CLM-0011", "CLM-0009"], figure="F16", hero=None, visual_mode="typography", treatment="card",
         on_screen_text=["NOT SUBSTANTIALLY PREVAILED -> NO FEES", "2016"], motion="the WITHOUT PREJUDICE node reactivates; 2016 appeals ruling; a legal-bill total stays red",
         sfx="gavel, heavy ledger thud",
         caption="Remember without prejudice? Because the government dismissed her case that way, a federal appeals court ruled, in two thousand sixteen, that Carole had not substantially prevailed. She got her money back, but she was not entitled to her legal fees. She won, and still paid to win.",
         image_hint="2016 appeals ruling; red legal-bill total"),
    dict(scene="S026", act="V", section="ACT5_WHAT_THEY_BUILT", anchor="15:55", purpose="McLellan got fees+costs+interest — opposite ending",
         claims=["CLM-0013"], figure="F17b", hero=None, visual_mode="diagram", treatment="card",
         on_screen_text=["McLELLAN: FEES + COSTS + INTEREST", "CAROLE: NOTHING"], motion="the two blurred outcome fields resolve; split hard down the middle",
         sfx="one side lifts, the other lands flat",
         caption="McLellan's case ended the other way. His money was returned, and a judge ordered the government to pay his legal fees, his costs, and interest. The justice Carole never got, he did — the same law, the same innocence, opposite endings, decided almost entirely by the procedural wording of how each case was closed.",
         image_hint="split comparison card, two outcomes"),
    dict(scene="S027", act="V", section="ACT5_WHAT_THEY_BUILT", anchor="16:40", purpose="still on the books; Congress hearings 2015",
         claims=["CLM-0017"], figure="F18", hero=None, visual_mode="reenactment", treatment="depth",
         on_screen_text=["STILL ON THE BOOKS", "HEARINGS — 2015"], motion="threat re-hook panel; congressional hearing room; anonymous business-owner witnesses (no likeness); a clock over the government's side",
         sfx="gavel, low room murmur, a ticking start",
         caption="This power is still on the books, and the real question is who it reaches for next. By two thousand fifteen, the pressure had moved to Congress. Lawmakers held hearings, and business owners who had lived through these seizures came and testified. The reform put a clock on the government for the first time.",
         image_hint="congressional hearing room; anonymous witnesses; clock icon", secondary=["F17"]),
    dict(scene="S028", act="V", section="ACT5_WHAT_THEY_BUILT", anchor="18:15", purpose="2019 reform act — 30-day hearing; Carole's business long gone",
         claims=["CLM-0016", "CLM-0018", "CLM-0020"], figure="F19", hero=None, visual_mode="typography", treatment="card",
         on_screen_text=["2019 REFORM — SIGNED JULY", "30-DAY HEARING", "LEGAL-SOURCE ACCOUNTS PROTECTED"], motion="2019 reform card; 30-DAY HEARING and protected-accounts chips; a door closes on the specific trap (RESPECT Act node lights gold)",
         sfx="firm bill-signing stamp, a door easing shut",
         caption="In two thousand nineteen, it became law. A reform act, signed that July. From then on, the government could no longer take a legal-source account just because the deposits stayed under ten thousand dollars, and the owner now gets a hearing within thirty days. By the time the law changed, the business was long gone — she had sold it while the case dragged on.",
         image_hint="2019 reform act card; 30-day hearing chip; closing door"),
    dict(scene="S029", act="V", section="ACT5_WHAT_THEY_BUILT", anchor="18:50", purpose="L4 payoff — the store after; the hallway of open doors",
         claims=["CLM-0016", "CLM-0005"], figure="F20", hero="hero_carole_after", visual_mode="location", treatment="depth",
         on_screen_text=["SOLD", "THE HALLWAY IS STILL OPEN"], motion="empty Mrs. Lady's interior, back->counter dolly, SOLD placard lands (hero); a closed door reveals a hallway of doors still open (drug cases / highway stops / tax files)",
         sfx="sustained unresolved pad",
         caption="That reform closed one door; it did not close the hallway. The specific trick that trapped Carole is off the table now. But civil forfeiture itself — the power to put your property on trial instead of you — is still very much alive, in drug cases and highway stops and tax files. The law that took Carole's account was reformed. The idea behind it was not.",
         image_hint="empty store interior; SOLD sign; hallway of open doors"),

    # ---- ENDING / CTA ----
    dict(scene="S030", act="ED", section="EARNED_CTA_AND_NEXT_ARC", anchor="19:45", purpose="earn the like + next-arc open loop; hook payoff",
         claims=["CLM-0001", "CLM-0018"], figure="F21", hero=None, visual_mode="typography", treatment="card",
         on_screen_text=["WHOSE RULES?", "THAT IS NEXT."], motion="PD end bookend; the deposit-slip motif from the hook returns, the pen finally lifting off the page; teaser frame of the next case's courtroom",
         sfx="resolving cadence anchored to the final word 'next', easing into ending ambience",
         caption="So the next time someone tells you the rules exist to protect you, the sharper question is whose rules, and who decides what your pattern means. Carole followed the rule. The government still emptied her account and locked away a year of her life. There is one more account this same power emptied, and that case is the one that finally moved a courtroom. That is next.",
         image_hint="deposit-slip motif returns; pen lifts; next-case courtroom teaser"),
]

HERO_MP4 = {
    "hero_bsa_flow": "hinders/hero_bsa_flow.mp4",
    "hero_frozen_account": "hinders/hero_frozen_account.mp4",
    "hero_carole_after": "hinders/hero_carole_after.mp4",
}


def main() -> int:
    acts = {}
    for b in BEATS:
        acts.setdefault(b["act"], 0)
        acts[b["act"]] += 1
    scenes = []
    for i, b in enumerate(BEATS, 1):
        scenes.append({
            "scene_id": b["scene"],
            "order": i,
            "act": b["act"],
            "section": b["section"],
            "script_anchor": b["anchor"],
            "purpose": b["purpose"],
            "primary_claims": b["claims"],
            "visual_mode": b["visual_mode"],
            "treatment": b["treatment"],
            "figure": b["figure"],                 # FIGURE_REGISTRY id (F1-F21) or null
            "secondary_figures": b.get("secondary", []),  # extra figure beats within the scene
            "figure_component": (b["figure"] and f"FIGURE_REGISTRY['{b['figure']}']") or None,
            "hero_video": HERO_MP4.get(b["hero"]) if b["hero"] else None,
            "on_screen_text": b["on_screen_text"],
            "motion": b["motion"],
            "sfx": b["sfx"],
            "caption_verbatim": b["caption"],
            "image_hint": b["image_hint"],
            "image_pool": [],                       # filled by asset selection (S0NN candidates)
            "depth_required": b["treatment"] == "depth",
            "needs_human_review": b["figure"] is None and b["hero"] is None and b["visual_mode"] == "reenactment",
        })
    doc = {
        "schema": "pd.scene_plan.v001",
        "episode_id": EP,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_script": "03_script/script.en.v001.md",
        "binding": ["EP35_hinders_ANIMATION_ASSETS.v001.md", "claims.v001.json"],
        "timing_note": "ORDINAL plan. cut/caption seconds are narration-derived (voice_plan.v001 -> narration_index, audio thread's lane). The film builder fills exact seconds once narration_index lands; captions carry verbatim VO and are re-timed to the master.",
        "assets": {
            "figures": "remotion/src/components/hinders (FIGURE_REGISTRY F1-F21)",
            "heroes": HERO_MP4,
            "image_pool_dir": "remotion/public/hinders/img (S001-S068 exist; design pool target >=136 — Codex)",
        },
        "coverage": {
            "script_beats": len(BEATS),
            "scenes": len(scenes),
            "acts": acts,
            "figures_placed": sorted({b["figure"] for b in BEATS if b["figure"]}),
            "heroes_placed": sorted({b["hero"] for b in BEATS if b["hero"]}),
        },
        "scenes": scenes,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    placed = sorted({b["figure"] for b in BEATS if b["figure"]}, key=lambda x: (len(x), x))
    print(f"wrote {OUT}")
    print(f"scenes={len(scenes)} acts={acts}")
    print(f"figures placed ({len(placed)}): {placed}")
    print(f"heroes placed: {sorted({b['hero'] for b in BEATS if b['hero']})}")
    missing = sorted({f'F{n}' for n in range(1, 22)} | {'F2b', 'F5b', 'F14b', 'F14c', 'F15b', 'F17b'})
    used = {b["figure"] for b in BEATS if b["figure"]} | {f for b in BEATS for f in b.get("secondary", [])}
    print(f"figure ids NOT yet placed: {sorted(set(missing) - used, key=lambda x:(len(x),x))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
