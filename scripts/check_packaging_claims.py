#!/usr/bin/env python3
"""Read a TITLE, THUMBNAIL TEXT and DESCRIPTION against the episode's own record.

WHY THIS EXISTS
---------------
`config/ship_policy.v001.json` puts the title, the thumbnail text and the description inside
the BLOCKING `factual_support` class -- "they are the first claim a viewer meets and the most
widely read sentence the channel publishes". `.claude/rules/19-ship-gate.md` then recorded, in
the same breath, that nothing enforced it: *"タイトル/サムネ/説明文の主張を台本と突き合わせる
機械チェックは存在しない"*.

On 2026-08-12 a repackaging pass proposed two titles that were FALSE and that passed every
mechanical rule the repo had (length band, question form, second person, case citation, pipe
character):

    "Five Boys Confessed on Camera"      -- the Central Park film's own narration says
                                            "Yusef Salaam gave no videotaped confession at
                                            all". FOUR were videotaped, not five.
    "Seven Sailors Signed Confessions"   -- the Norfolk film enumerates FOUR false confessions
                                            and says of the other three "None of the three ever
                                            confessed". Seven were CHARGED.

Only a human reading the script caught them. This module is the machine that would have.

WHAT IT DOES
------------
1. EXTRACT every checkable claim from the packaging text -- cardinal numbers and quantities,
   money, durations, dates and years, proper names of people and institutions, and outcome
   verbs that assert a fact. It deliberately OVER-extracts: a claim that is extracted and then
   verified costs a line of output; a claim that is never extracted is the one that ships.
2. VERIFY each against that episode's own record -- the narration script, the captions, the
   claims.v*.json ledger, the `*_facts.v*.json` file and the planning FACTS_LEDGER -- at
   SENTENCE granularity, because a 300-word paragraph contains both "five boys ... confessed"
   and "gave no videotaped confession" and a line-level matcher cannot tell them apart.
3. REFUSE anything that is not SUPPORTED. **UNVERIFIED IS A FAILURE, NOT A PASS.** That
   asymmetry is the entire point: "five" is caught against a script that says four not because
   the machine understands counting, but because it demands the record say five and it does not.
4. PRINT the claim, the verdict, and the exact record line -- file and line number -- that
   decided it, so a reviewer can check the check in one glance.

VERDICTS (only the first one passes)
------------------------------------
    SUPPORTED             a sentence of the record states it: the terms, the number and the
                          polarity all match.
    CONTRADICTED          a sentence of the record denies it -- a negation attached to one of
                          the claim's own terms, with the subject corroborated in the same
                          paragraph.
    NUMBER_MISMATCH       the record states a DIFFERENT number for the same subject.
    QUALIFIED_ONLY        the record carries the figure only inside a strong hedge
                          ("theoretical", "the maximum", "up to", "would have"), and the
                          packaging states it flat. This is `swartz`'s "35 YEARS FOR PAPERS."
    FORBIDDEN_AS_FACT     the episode's own DO_NOT_STATE_AS_FACT block or a claim's
                          `prohibited_wording` names this figure as one that may not be
                          asserted bare.
    SUPPORTED_LEDGER_ONLY the research ledger has it but the NARRATION never says it. A viewer
                          who watches the whole film never hears the thing the title promised.
                          This is `madoff`'s "in 2000".
    UNVERIFIED            nothing in the record addresses it.

The ladder, in order, because the order is the design:

    sentence support > STRONG denial (a sentence of the FILM negating two of the claim's own
    terms) > number mismatch > qualified-only > forbidden-as-fact > paragraph support > WEAK
    denial (one term negated, subject established in the paragraph -- it only speaks when
    nothing in the record supports the claim) > ledger-only > unverified.

A single sentence that states the whole claim beats a denial elsewhere: a 10,000-word film
argues with itself constantly, and the denial is still printed underneath as counter-evidence.
A denial beats paragraph-level co-occurrence, which is what rejects "Five Boys Confessed on
Camera" against a paragraph that contains "five", "boys", "confessed" and "videotaped" but no
sentence that puts them together.

HARD vs SOFT (why the exit code is not simply "every claim")
------------------------------------------------------------
Every claim is extracted, verified and printed. Only HARD ones hold the door shut: anything
carrying a number, money, a duration, a date or a proper name, and outcome verbs from the
curated lexicon ("confessed", "acquitted", "seized", "died", "landed") -- the assertions this
channel would be sued over. A generic past-tense verb ("became", "closed", "chose") is
extracted and reported as a `note`, because the verifier matches words and the films paraphrase
constantly; blocking a booking on "He Had Closed the Door" is how a check gets switched off in
a day. `--strict` blocks on both. Measured 2026-08-12 over a known-good set of 13 titles:
45 claims, 0 hard failures, 8 soft notes. In a DESCRIPTION, UNVERIFIED is a note too -- see
check_packaging().

WHAT THIS WILL NEVER DO -- READ THIS BEFORE TRUSTING A GREEN
------------------------------------------------------------
It cannot judge TONE. It cannot judge IMPLICATION -- a title whose every word is in the script
can still promise something the film does not deliver, and this check will pass it. It cannot
judge a claim the SCRIPT ITSELF makes badly: the record is the standard here, so a false
narration produces a false title with a green tick. It matches words, stems and numbers, so a
paraphrase the record states in different vocabulary reads as UNVERIFIED (a false alarm), and a
sentence that happens to contain the right words in the wrong relation reads as SUPPORTED (a
miss) -- it has no grammar and no notion of who did what to whom. Its synonym list is small,
hand-written and domain-specific, and everything outside it is invisible.

**It reduces the gap. It does not close it. Anyone reading a green from this must still read
the title against the film.**

USAGE
-----
    py -3.11 scripts/check_packaging_claims.py --slug norfolk \
        --title "Seven Sailors Signed Confessions. The DNA Matched None of Them."
    py -3.11 scripts/check_packaging_claims.py --slug centralpark --package   # 09_package meta
    py -3.11 scripts/check_packaging_claims.py --live                         # every live title
    py -3.11 scripts/check_packaging_claims.py --live --slug swartz --json

Exit 0 = every claim SUPPORTED. Exit 1 = at least one is not, and it is named. Read-only:
no writes, no network, no paid calls.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENOME = ROOT / "data" / "content_genome.v001.jsonl"

PASS_VERDICTS = {"SUPPORTED"}

# Which failing verdicts hold the door shut. The sharp ones -- the record denies it, states a
# different number, hedges it, or forbids it outright. UNVERIFIED and SUPPORTED_LEDGER_ONLY are
# reported on every claim and blocked only under `--strict`; see check_packaging().
BLOCKING_VERDICTS = {"CONTRADICTED", "NUMBER_MISMATCH", "QUALIFIED_ONLY", "FORBIDDEN_AS_FACT"}

# --------------------------------------------------------------------------------- lexicons

NUM_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
    "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
    "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fourty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}
MULTIPLIER_WORDS = {"hundred": 100, "thousand": 1_000, "million": 1_000_000,
                    "billion": 1_000_000_000, "trillion": 1_000_000_000_000}
SUFFIX_MULT = {"k": 1_000, "m": 1_000_000, "bn": 1_000_000_000, "b": 1_000_000_000}

# Words that carry no discriminating power. A claim term list is filtered through this before
# anything is required of the record.
STOPWORDS = set("""
a an the and or but nor for yet so of to in on at by with from into onto over under about as
is are was were be been being am do does did done doing have has had having will would shall
should can could may might must this that these those it its it's they them their there here
he him his she her hers we us our you your i me my mine who whom whose which what when where
why how all any both each few more most other some such only own same than too very just now
then than out up down off again once during before after above below between through against
while because if unless until since not no nor never none nothing nobody neither also still
one's s t don doesn didn isn aren wasn weren wouldn couldn shouldn mustn ll re ve d m
said says say every another anything something someone anyone everyone many much lot lots
thing things way ways made make makes making got get gets anyway anyhow
first second third last next new old own real true whole full half part parts kind sort
among amid amongst beyond toward towards upon per via plus versus near behind along across
throughout inside outside beside besides despite according regarding concerning
ever still already again yet almost nearly just only even really quite rather simply today
back away ahead anyway anyhow instead perhaps maybe indeed actually finally soon later
cannot cant couldnt didnt doesnt dont isnt wasnt werent wont wouldnt havent hasnt hadnt
didn't don't doesn't isn't wasn't weren't won't wouldn't can't couldn't hasn't haven't hadn't
shouldn't aren't ain't
vs v versus etc ie eg per cent
""".split())

# Extra common vocabulary used ONLY to decide whether a capitalised token is a proper name.
# A title is Title Case, so capitalisation alone proves nothing; a token is treated as a name
# when it is capitalised AND is not ordinary English.
COMMON_WORDS = STOPWORDS | set("""
man men woman women boy boys girl girls child children kid kids people person police officer
officers court courts judge judges jury juries lawyer lawyers attorney prosecutor prosecutors
state states federal government city county case cases crime crimes murder rape theft money
cash dollars prison jail cell years months days hours minutes night day morning evening
confession confessions confessed confess statement statements evidence dna test tests
witness witnesses trial trials appeal appeals verdict sentence sentenced convicted conviction
convictions acquitted acquittal exonerated innocent guilty charged charge charges arrest
arrested searched search warrant warrants seized seizure took take taken gave give given
found find kept keep ran run running handed hand held hold home house door window car cars
plane planes museum museums bank banks paper papers file files record records report reports
site sites law laws rule rules right rights never nothing none nobody still again anyway
because until after before while during since without within against between among across
mother father son daughter wife husband family families friend friends neighbour neighbor
army navy sailor sailors soldier soldiers detective detectives agent agents
what who why how when where which whose
""".split())

# Verbs (and their common inflections) that ASSERT A FACT about what happened. This is the
# outcome lexicon; anything here becomes a checkable claim.
OUTCOME_VERBS = set("""
confess confessed confesses confessing acquit acquitted convict convicted convicting
exonerate exonerated exoneration charge charged charging indict indicted sentence sentenced
arrest arrested jail jailed imprison imprisoned execute executed die died dies dead killed
kill kills murdered murder survived survive vanished vanish disappeared disappear escaped
escape fled flee jumped jump landed land crashed crash burned burn drowned drown
sued sue sued suing settled settle settlement paid pay paid repaid refunded refused refuse
denied deny dismissed dismiss dropped drop vacated vacate overturned overturn reversed reverse
upheld uphold affirmed affirm ruled rule ordered order granted grant awarded award
seized seize seizing took take taken taking kept keep stole steal stolen robbed rob
searched search raided raid entered enter emptied empty emptying stripped strip
signed sign signing recanted recant admitted admit denied confessed lied lie lying
warned warn warning ignored ignore ignoring buried bury covered cover hid hide hidden
freed free released release exposed expose revealed reveal proved prove proven matched match
excluded exclude cleared clear identified identify named name naming found find
won win lost lose beat beaten defeated defeat
recovered recover returned return survived resigned resign fired fire fined fined
""".split())

# Past-tense verbs whose surface form no rule can recognise. A title's assertion usually lives
# in one of these or in an -ed form, and a claim that is never extracted is the one that ships.
IRREGULAR_PAST = set("""
took taken kept wrote written won lost sold told gave given made went gone came saw seen knew
known thought brought bought caught taught sent spent built held left felt meant met paid ran
sat stood understood drove driven fell fallen flew grew hid hidden struck stole stolen swore
sworn threw thrown wore woke rose risen spoke spoken chose chosen froze drew blew shot found
got gotten heard led sought began begun broke broken shook sank sunk swam rode arose bore
borne dealt fought lent lit slept stuck swept wept wound put cut hit hurt cost set beat read
""".split())

NEGATION_CUES = {"no", "not", "never", "none", "nothing", "nobody", "neither", "nor",
                 "without", "n't", "cannot", "cant", "denied", "denies", "deny", "refused",
                 "refuses", "refuse", "failed", "fails", "fail", "unable", "rejected",
                 "didn't", "don't", "doesn't", "isn't", "wasn't", "weren't", "won't",
                 "wouldn't", "can't", "couldn't", "hasn't", "haven't", "hadn't",
                 "shouldn't", "aren't", "ain't", "nowhere", "nor"}

# "without a warrant" is a preposition doing ordinary work, not the record denying anything.
# Leaving it in the denial set made the check call riley's live title contradicted by the
# very sentence that states its holding.
DENIAL_EXCLUDED = {"without", "nowhere"}

# A figure the record states only inside one of these is NOT a figure the packaging may state
# flat. "the theoretical stacked maximum was thirty-five years" does not license
# "35 YEARS FOR PAPERS."
STRONG_HEDGE = {"theoretical", "theoretically", "hypothetical", "maximum", "maximums",
                "maxima", "ceiling", "potential", "potentially", "could", "would", "might",
                "may", "if", "faced", "facing", "alleged", "allegedly", "reportedly",
                "reported", "claimed", "supposed", "supposedly", "purported", "purportedly",
                "rumoured", "rumored", "speculation", "speculated", "unverified", "disputed",
                "stacked", "paper", "sought", "possible", "possibly"}
# "up" alone is not a hedge ("rides all the way up to the Supreme Court"); "up to" is.
HEDGE_BIGRAMS = {("up", "to"), ("as", "much"), ("at", "most"), ("no", "more")}
# Ordinary house-style softeners. The channel writes "about forty-one million dollars" as a
# matter of style; treating that as a hedge would fail the whole catalogue.
WEAK_HEDGE = {"about", "around", "roughly", "approximately", "nearly", "almost", "some",
              "estimate", "estimated", "common", "or", "so", "over", "under", "more", "less"}

# Small, hand-written, domain-specific. Everything outside it is invisible to this check --
# that is a known limitation and it is in the docstring.
SYNONYMS = {
    "boy": "child", "girl": "child", "kid": "child", "teen": "child", "teenager": "child",
    "youth": "child", "juvenile": "child", "minor": "child", "children": "child",
    "sailor": "sailor", "seaman": "sailor", "serviceman": "sailor",
    "confession": "confess", "confessed": "confess",
    "videotape": "videotape", "videotaped": "videotape", "video": "videotape",
    "camera": "videotape", "tape": "videotape", "taped": "videotape", "film": "videotape",
    "filmed": "videotape", "record": "videotape", "recorded": "videotape",
    "indictment": "charge", "indicted": "charge", "indict": "charge",
    "felony": "felony", "felonies": "felony", "count": "charge", "counts": "charge",
    "acquittal": "acquit", "exoneration": "exonerate",
    "cash": "money", "dollar": "money", "dollars": "money",
    "attorney": "lawyer", "counsel": "lawyer",
    "cop": "police", "officer": "police", "detective": "police",
    "gaol": "jail", "prison": "prison", "penitentiary": "prison",
    "vacated": "vacate", "overturned": "overturn", "reversed": "reverse",
    # Irregular past tenses. Without these a title that says "took" never finds a script that
    # says "takes", and the check reports UNVERIFIED on a claim the film states plainly.
    "took": "take", "taken": "take", "takes": "take", "kept": "keep", "wrote": "write",
    "written": "write", "won": "win", "lost": "lose", "sold": "sell", "told": "tell",
    "gave": "give", "given": "give", "made": "make", "went": "go", "gone": "go",
    "came": "come", "saw": "see", "seen": "see", "knew": "know", "known": "know",
    "thought": "think", "brought": "bring", "bought": "buy", "caught": "catch",
    "taught": "teach", "sent": "send", "spent": "spend", "built": "build", "held": "hold",
    "left": "leave", "felt": "feel", "meant": "mean", "met": "meet", "paid": "pay",
    "ran": "run", "sat": "sit", "stood": "stand", "understood": "understand",
    "drove": "drive", "driven": "drive", "fell": "fall", "fallen": "fall", "flew": "fly",
    "grew": "grow", "hid": "hide", "hidden": "hide", "struck": "strike", "stole": "steal",
    "stolen": "steal", "swore": "swear", "sworn": "swear", "threw": "throw",
    "thrown": "throw", "wore": "wear", "woke": "wake", "rose": "rise", "risen": "rise",
    "spoke": "speak", "spoken": "speak", "chose": "choose", "chosen": "choose",
    "froze": "freeze", "drew": "draw", "blew": "blow", "shot": "shoot", "found": "find",
    "got": "get", "gotten": "get", "heard": "hear", "led": "lead", "sought": "seek",
    "began": "begin", "begun": "begin", "broke": "break", "broken": "break",
    "shook": "shake", "sank": "sink", "sunk": "sink", "swam": "swim", "rode": "ride",
    "arose": "arise", "bore": "bear", "borne": "bear", "dealt": "deal", "fought": "fight",
    "lent": "lend", "lit": "light", "slept": "sleep",
    "spread": "spread", "stuck": "stick", "swept": "sweep", "wept": "weep", "wound": "wind",
    "seized": "seize", "seizure": "seize", "confiscated": "seize", "forfeited": "forfeit",
    # "died" is short enough that no suffix rule reaches the base form ("di"), and the record
    # says "deaths" where a title says "Died".
    "died": "die", "dying": "die", "death": "die", "deaths": "die",
}

TIME_UNITS = {"year", "month", "day", "hour", "minute", "week", "decade"}
UNIT_NOUNS = TIME_UNITS | {"mile", "foot", "feet", "dollar", "cent", "percent", "count",
                           "felony", "charge", "page"}

# A verb or a number word is never a proper name, whatever the Title Case says.
COMMON_WORDS |= OUTCOME_VERBS | set(NUM_WORDS) | set(MULTIPLIER_WORDS)

# Channel furniture. "PRIME DOCUMENTARY" on a thumbnail is a logo, not a claim about the case.
BRAND_WORDS = {"prime", "documentary", "documentaries", "subscribe", "watch", "episode",
               "full", "series", "channel", "true", "story", "part", "shorts", "short"}

# A synonym map is only consistent if every VALUE also stems to itself.
for _v in list(dict.fromkeys(SYNONYMS.values())):
    SYNONYMS.setdefault(_v, _v)
    if _v.endswith("e"):
        SYNONYMS.setdefault(_v[:-1], _v)

# ------------------------------------------------------------------------------ normalising


def _is_vowel(w: str, i: int) -> bool:
    c = w[i]
    return c in "aeiou" or (c == "y" and i > 0 and w[i - 1] not in "aeiou")


def _measure(w: str) -> int:
    """Porter's m: how many vowel-then-consonant runs the stem contains."""
    return "".join("v" if _is_vowel(w, i) else "c" for i in range(len(w))).count("vc")


def _cvc(w: str) -> bool:
    """Porter's *o: ends consonant-vowel-consonant, last not w/x/y -- "car", "nam", "hop"."""
    return (len(w) >= 3 and not _is_vowel(w, len(w) - 1) and _is_vowel(w, len(w) - 2)
            and not _is_vowel(w, len(w) - 3) and w[-1] not in "wxy")


def stem(word: str) -> str:
    """Crude, deliberate stemmer. Small enough to reason about; wrong sometimes, and said so.

    The silent "e" is handled by Porter's two rules rather than by chopping every trailing e.
    An unconditional chop collided "care" with "car" -- and on 2026-08-12 that collision made
    the checker read a ledger line about the patients' CARE as a denial of a title about a CAR
    that no one had mentioned. `care`/`cared`/`caring` still land on one key; `car` keeps its own.
    """
    w = word.lower().strip("'’")
    if w.endswith("'s") or w.endswith("’s"):
        w = w[:-2]
    if w in SYNONYMS:
        return SYNONYMS[w]
    if len(w) > 4 and w.endswith("ies"):
        w = w[:-3] + "y"
    elif len(w) > 4 and w.endswith("sses"):
        w = w[:-2]
    elif len(w) > 3 and w.endswith("s") and not w.endswith(("ss", "us", "is")):
        w = w[:-1]
    if len(w) > 4 and w.endswith("ied"):
        w = w[:-3] + "y"          # emptied -> empty, buried -> bury, carried -> carry
    stripped = doubled = False
    if len(w) > 4 and w.endswith("ing"):
        w = w[:-3]
        stripped = True
    elif len(w) > 3 and w.endswith("ed"):
        w = w[:-2] if not w.endswith("eed") else w[:-1]
        stripped = True
    # Porter's *d rule keeps a doubled l/s/z: "called" -> call (not cal), "pulled" -> pull.
    if stripped and len(w) > 2 and w[-1] == w[-2] and w[-1] not in "aeioulsz":
        w, doubled = w[:-1], True
    # Porter step 1b: a short stem left by -ed/-ing lost a silent e ("nam" -> name,
    # "car"(ing) -> care, "liv"(ed) -> live). Exactly the inverse of the rule below, so a
    # restored e is never chopped straight off again. It is an ALTERNATIVE to the doubled-
    # consonant rule above, never applied after it: "called" -> "call" -> "cal" -> "cale"
    # would part company with "call", which is the same collision in the other direction.
    if stripped and not doubled and _measure(w) == 1 and _cvc(w):
        w += "e"
    # Porter step 5a: drop the silent e only when what is left is NOT a short cvc stem.
    # "charge" -> charg, "use" -> us, but "care" stays care and never becomes "car".
    if w.endswith("e"):
        base = w[:-1]
        if _measure(base) > 1 or (_measure(base) == 1 and not _cvc(base)):
            w = base
    return SYNONYMS.get(w, w)


TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z'’-]*|\$?\d[\d,\.]*")


def tokens_of(text: str) -> list[str]:
    return TOKEN_RE.findall(text)


def content_stems(text: str) -> list[str]:
    """The words a claim actually stands on.

    Number words are excluded: the number itself is already extracted and compared as a
    number, and leaving "seven" in as a term made the checker cite a sentence that merely
    contained the word seven. Stopwords are tested on the raw token AND on the stem, because
    the trailing-e rule turns "none" into "non".
    """
    out = []
    for tok in tokens_of(text):
        # "strip-searched" in a title against "strip searched" in a script is the same claim.
        # Number words keep their hyphens: "thirty-two" is parsed as a number, not as terms.
        parts = [tok] if tok.lower() in NUM_WORDS else tok.split("-")
        for t in parts:
            low = t.lower()
            if not t or t[0].isdigit() or t.startswith("$"):
                continue
            if low in NUM_WORDS or low in MULTIPLIER_WORDS or low in STOPWORDS:
                continue
            st = stem(t)
            if st and st not in STOPWORDS and len(st) > 1:
                out.append(st)
    return out


# --------------------------------------------------------------------------------- numbers

@dataclass
class NumMention:
    value: float
    kind: str          # "money" | "year" | "count"
    head: str | None   # stem of the noun the number is attached to ("sailor", "year", ...)
    tok_i: int         # token index, for negation/hedge proximity
    surface: str


def _word_number(toks: list[str], i: int) -> tuple[float, int] | None:
    """Parse a spelled-out number starting at toks[i]. Returns (value, next_index)."""
    total, cur, n, j = 0.0, 0.0, 0, i
    while j < len(toks):
        w = toks[j].lower().strip("-")
        parts = [p for p in re.split(r"-", w) if p]
        if all(p in NUM_WORDS or p in MULTIPLIER_WORDS for p in parts) and parts:
            for p in parts:
                if p in MULTIPLIER_WORDS:
                    m = MULTIPLIER_WORDS[p]
                    cur = (cur or 1) * m if m < 1000 else (cur or 1) * m
                    if m >= 1000:
                        total += cur
                        cur = 0.0
                else:
                    cur += NUM_WORDS[p]
            n += 1
            j += 1
            if j < len(toks) and toks[j].lower() == "and" and j + 1 < len(toks):
                nxt = toks[j + 1].lower()
                if nxt in NUM_WORDS or nxt in MULTIPLIER_WORDS:
                    j += 1
                    continue
            continue
        break
    if n == 0:
        return None
    return total + cur, j


def _digit_value(tok: str) -> float | None:
    t = tok.replace(",", "").lstrip("$")
    if not t or not t[0].isdigit():
        return None
    try:
        return float(t)
    except ValueError:
        return None


def find_numbers(text: str) -> list[NumMention]:
    """Every number in a span, normalised, with the noun it is attached to."""
    toks = tokens_of(text)
    out: list[NumMention] = []
    i = 0
    while i < len(toks):
        tok = toks[i]
        val: float | None = None
        end = i + 1
        is_money = tok.startswith("$")
        if tok[0].isdigit() or is_money:
            val = _digit_value(tok)
        elif not (tok.lower() == "one" and i and toks[i - 1].lower()
                  in ("no", "any", "some", "every", "each", "not")):
            # "NO ONE ASKED" is not a claim that one person asked.
            wn = _word_number(toks, i)
            if wn:
                val, end = wn
        if val is None:
            i += 1
            continue
        # trailing multiplier: "41 million", "$200,000", "13 billion", "20k"
        if end < len(toks) and toks[end].lower() in MULTIPLIER_WORDS:
            val *= MULTIPLIER_WORDS[toks[end].lower()]
            end += 1
        elif re.fullmatch(r"\$?\d[\d,\.]*[kmb]n?", tok, re.I):
            m = re.search(r"([kmb]n?)$", tok, re.I)
            if m and _digit_value(tok[: m.start()]) is not None:
                val = _digit_value(tok[: m.start()]) * SUFFIX_MULT[m.group(1).lower()]
        # the noun it is attached to
        head = None
        j = end
        while j < len(toks) and j < end + 3:
            s = stem(toks[j])
            if s in ("of", "a", "an", "the", "additional", "more", "other", "us", "united"):
                j += 1
                continue
            if s not in STOPWORDS and not toks[j][0].isdigit():
                head = s
                break
            j += 1
        kind = "count"
        if is_money or "$" in tok or (head in ("dollar", "money")):
            kind = "money"
        elif (val == int(val) and 1500 <= val <= 2100 and head not in UNIT_NOUNS
              and not re.fullmatch(r"\d{1,3}", tok.replace(",", ""))):
            kind = "year"
            head = None
        out.append(NumMention(float(val), kind, head, i, " ".join(toks[i:end])))
        i = max(end, i + 1)
    return out


def num_close(a: float, b: float) -> bool:
    """Exact for small counts; 2% for anything the record may round (money, big figures)."""
    if a == b:
        return True
    if max(abs(a), abs(b)) >= 1000:
        return abs(a - b) / max(abs(a), abs(b)) <= 0.02
    return False


# ---------------------------------------------------------------------------------- record

@dataclass
class Sentence:
    path: str
    line: int
    text: str
    stems: set[str] = field(default_factory=set)
    toks: list[str] = field(default_factory=list)
    nums: list[NumMention] = field(default_factory=list)
    source: str = "narration"   # "narration" | "ledger"
    line_key: tuple = ()
    record_meta: bool = False   # describes what a document contains, not what happened


@dataclass
class Record:
    sentences: list[Sentence]
    guardrails: list[tuple[str, str]]      # (text, where)
    line_stems: dict[tuple, set[str]]      # paragraph-level term index
    df: dict[str, int]
    sources: list[str]
    lower_vocab: set[str] = field(default_factory=set)   # words the record uses lower-case
    line_sents: dict[tuple, list] = field(default_factory=dict)   # paragraph -> its sentences
    stem_source: dict[str, set[str]] = field(default_factory=dict)

    def has_narration(self) -> bool:
        return any(s.source == "narration" for s in self.sentences)

    def where(self, stem_key: str) -> set[str]:
        """Which classes of source use this term at all: {} / {'ledger'} / {'narration', ...}"""
        return self.stem_source.get(stem_key, set())


SENT_SPLIT = re.compile(r"(?<=[.!?:;])\s+|\s+—\s+")
VO_RE = re.compile(r"^\s*\[[^\]]*\]\s*")
MD_STRIP = re.compile(r"[*_`>#\[\]]")
# `[CLM-0008]` is a claim tag, not a number in the narration. Left in, the tokenizer read the
# 0008 as the number eight and certified "8-1 SUPREME COURT" against a sentence that contains
# neither an eight nor a vote.
TAG_RE = re.compile(r"\[(?:CLM|SRC|SPN|NF|VC)-?[0-9A-Za-z/,\- ]{0,24}\]")


def _mk_sentences(path: Path, line_no: int, text: str, source: str) -> list[Sentence]:
    txt = MD_STRIP.sub("", TAG_RE.sub(" ", VO_RE.sub("", text))).strip()
    if not txt:
        return []
    rel = path.resolve().relative_to(ROOT).as_posix() if str(path).startswith(str(ROOT)) else str(path)
    out = []
    for part in SENT_SPLIT.split(txt):
        part = part.strip()
        if len(part) < 3:
            continue
        if is_meta(part):
            continue
        toks = tokens_of(part)
        s = Sentence(rel, line_no, part, set(content_stems(part)), toks,
                     find_numbers(part), source, (rel, line_no), is_record_meta(part))
        out.append(s)
    return out


GUARD_HEAD = re.compile(r"do\s*[-_ ]?not\s*state|never\s+state|do\s+not\s+assert|"
                        r"prohibited|forbidden|do_not_state", re.I)

# A sentence that TELLS THE WRITER WHAT NOT TO SAY is not the film saying it. These lines live
# all through the facts ledgers and the claim files ("do NOT say 'jailed on his birthday'",
# "Say police can never search a car in a driveway"), and reading them as narration produced
# some of this check's most confusing citations.
# Substring test, not a regex: this file is edited through tooling that eats backslashes,
# and a silently broken word boundary here would put instruction text back into the record.
META_PHRASES = (
    "do not ", "don't ", "never say", "never state", "never use", "avoid ",
    "prohibited", "forbidden", "must not", "should not", "grepped", "safe phrasing",
    "soft-cite", "hedge", "use:", "src:", "usage", "rules/09", "claude",
    "framing/transition", "do NOT", "not new facts",
    # The fact-map / beat-sheet tables appended to a script are shorthand ("Pauley/Farris/
    # Danser charged with capital murder, never confessed -> NF-16"), not narration.
    "→", "->", "fact map", "beat sheet", "not asserted", "counterevidence",
)


# A statement about what a DOCUMENT contains is not a statement about what happened.
# "Nothing about their care, injuries or deaths is in this document" says the opinion is silent;
# it does not deny that three patients died. Read as a denial, it made marmet's true title
# CONTRADICTED by its own facts ledger. These sentences stay in the record (they can still
# support and they are still printed) -- they may not serve as the negation of a fact.
RECORD_META_RE = re.compile(
    r"nothing\b[^.]{0,90}\b(?:in|about)\b[^.]{0,40}"
    r"\b(?:this document|the document|the record|the opinion|the transcript|the file|"
    r"the docket|the ruling|the filing)s?\b"
    r"|\b(?:not|never|nowhere)\b[^.]{0,40}\bin (?:this document|the document|the record|"
    r"the opinion|the transcript|the docket)\b"
    r"|\b(?:this document|the document|the record|the opinion|the transcript|the docket|"
    r"the ruling|the filing|the complaint|the caption)s?\b[^.]{0,40}"
    r"\b(?:does not|do not|did not|doesn't|don't|never|no longer)\s+"
    r"(?:\w+\s+){0,2}(?:discuss|record|mention|say|state|name|address|contain|include|"
    r"identify|describe|explain|list|specify|note|report|reach|reveal|show|tell|appear)"
    r"|\bdoes not appear (?:in|anywhere)\b|\bno mention of\b"
    r"|\bis not (?:in|part of) the record\b|\bnot in this document\b",
    re.I)


def is_record_meta(text: str) -> bool:
    """True for a sentence that describes the SILENCE OF A DOCUMENT, not the absence of a fact."""
    return RECORD_META_RE.search(text) is not None


def is_meta(text: str) -> bool:
    """True for a line that instructs the WRITER rather than stating a fact."""
    low = text.lower()
    return any(ph.lower() in low for ph in META_PHRASES)


def load_record(epdir: Path, *, quiet: bool = True) -> Record:
    """Everything this episode says about itself, at sentence granularity.

    narration = the script body and the captions (what a viewer actually hears).
    ledger    = claims.v*.json, *_facts.v*.json and the planning FACTS_LEDGER (what was
                researched). The distinction matters: a title may cite the ledger, but if the
                narration never says it the viewer never hears it, and that is reported.
    """
    sents: list[Sentence] = []
    guards: list[tuple[str, str]] = []
    sources: list[str] = []

    # 1. the narration script -------------------------------------------------
    for sp in sorted((epdir / "03_script").glob("script.en.v*.md")):
        sources.append(sp.relative_to(ROOT).as_posix())
        in_guard = False
        for n, raw in enumerate(sp.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            line = raw.rstrip()
            if not line.strip():
                continue
            head = line.lstrip("#> ").strip()
            if line.lstrip().startswith("#") or line.lstrip().startswith(">"):
                if GUARD_HEAD.search(head):
                    in_guard = True
                    guards.append((head, f"{sp.relative_to(ROOT).as_posix()}:{n}"))
                    continue
                if line.lstrip().startswith("#"):
                    in_guard = False
                if GUARD_HEAD.search(head):
                    guards.append((head, f"{sp.relative_to(ROOT).as_posix()}:{n}"))
                continue          # headings/metadata are not narration
            if in_guard and line.lstrip().startswith("-"):
                guards.append((head, f"{sp.relative_to(ROOT).as_posix()}:{n}"))
                continue
            in_guard = False
            sents += _mk_sentences(sp, n, line, "narration")

    # 2. captions (what was actually said on the render) ----------------------
    edit = epdir / "08_edit"
    cap = None
    for pat in ("captions.final.v*.srt", "captions.youtube.v*.srt", "captions.v*.srt"):
        hits = sorted(edit.glob(pat))
        if hits:
            cap = hits[-1]
            break
    if cap:
        sources.append(cap.relative_to(ROOT).as_posix())
        buf, start = [], 1
        for n, raw in enumerate(cap.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            t = raw.strip()
            if not t or t.isdigit() or "-->" in t:
                if buf:
                    sents += _mk_sentences(cap, start, " ".join(buf), "narration")
                    buf = []
                continue
            if not buf:
                start = n
            buf.append(t)
        if buf:
            sents += _mk_sentences(cap, start, " ".join(buf), "narration")

    # 3. the research claim ledger -------------------------------------------
    for cp in sorted((epdir / "01_research").glob("claims.v*.json")):
        if cp.name.endswith(".meta.json"):
            continue
        sources.append(cp.relative_to(ROOT).as_posix())
        try:
            data = json.loads(cp.read_text(encoding="utf-8"))
        except Exception:                                             # noqa: BLE001
            continue
        claims = data.get("claims", data) if isinstance(data, dict) else data
        if not isinstance(claims, list):
            continue
        for k, c in enumerate(claims, 1):
            if not isinstance(c, dict):
                continue
            for key in ("normalized_claim", "temporal_scope", "units"):
                if c.get(key):
                    sents += _mk_sentences(cp, k, str(c[key]), "ledger")
            for key in ("allowed_wording", "evidence_locations"):
                for v in c.get(key) or []:
                    sents += _mk_sentences(cp, k, str(v), "ledger")
            for v in c.get("prohibited_wording") or []:
                guards.append((str(v), f"{cp.relative_to(ROOT).as_posix()}:claim {k}"))

    # 4. the episode facts file ----------------------------------------------
    for fp in sorted((epdir / "03_script").glob("*_facts.v*.json")):
        sources.append(fp.relative_to(ROOT).as_posix())
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:                                             # noqa: BLE001
            continue
        for g in (data.get("DO_NOT_STATE_AS_FACT") or []):
            guards.append((str(g), f"{fp.relative_to(ROOT).as_posix()}:DO_NOT_STATE_AS_FACT"))
        for k, row in enumerate(data.get("ledger") or [], 1):
            if isinstance(row, dict):
                for key in ("claim", "detail", "wording", "note"):
                    if row.get(key):
                        sents += _mk_sentences(fp, k, str(row[key]), "ledger")

    # 5. the planning FACTS_LEDGER -------------------------------------------
    slug = epdir.name.split("-", 3)[-1]
    for lp in sorted((ROOT / "episodes" / "_planning").glob(f"EP*_{slug}_FACTS_LEDGER.v*.md")):
        sources.append(lp.relative_to(ROOT).as_posix())
        for n, raw in enumerate(lp.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if raw.strip():
                sents += _mk_sentences(lp, n, raw, "ledger")

    line_stems: dict[tuple, set[str]] = {}
    df: dict[str, int] = {}
    lower_vocab: set[str] = set()
    stem_source: dict[str, set[str]] = {}
    for s in sents:
        line_stems.setdefault(s.line_key, set()).update(s.stems)
        for t in s.stems:
            df[t] = df.get(t, 0) + 1
            stem_source.setdefault(t, set()).add(s.source)
        # A token the record itself writes in lower case is ordinary English in this domain,
        # whatever a Title-Cased headline does with it. This is how "Camera" is kept out of
        # the proper-name channel without a hand-written dictionary of every English noun.
        for tok in s.toks:
            if tok[:1].islower():
                lower_vocab.add(stem(tok))
    line_sents: dict[tuple, list[Sentence]] = {}
    for s_ in sents:
        line_sents.setdefault(s_.line_key, []).append(s_)
    return Record(sents, guards, line_stems, df, sources, lower_vocab, line_sents, stem_source)


# ----------------------------------------------------------------------------------- claims

@dataclass
class Claim:
    kind: str                     # quantity | duration | money | date | name | outcome
    text: str
    field: str                    # title | thumbnail_text | description
    terms: list[str]              # ALL content stems in the claim span
    core: list[str]               # the rarest ones, which the record must actually contain
    number: float | None = None
    num_kind: str | None = None
    head: str | None = None
    negated: bool = False
    hedged: bool = False
    hard: bool = True

    def key(self) -> tuple:
        return (self.kind, self.number, self.head, tuple(sorted(self.core)), self.negated)


def _negated_at(toks: list[str], i: int, window: int = 5) -> bool:
    lo = max(0, i - window)
    for t in toks[lo:i]:
        if t.lower() in NEGATION_CUES:
            return True
    for t in toks[i + 1:i + 3]:
        if t.lower() in NEGATION_CUES:
            return True
    return False


def _pick_core(terms: list[str], df: dict[str, int], keep: str | None, n: int = 3) -> list[str]:
    """The rarest terms in the record. Requiring ALL of many terms guarantees UNVERIFIED;
    requiring the rarest few is what discriminates."""
    uniq = list(dict.fromkeys(t for t in terms if t not in STOPWORDS))
    uniq.sort(key=lambda t: (df.get(t, 0), -len(t)))
    core = uniq[:n]
    if keep and keep not in core:
        core = ([keep] + core)[:max(n, 1)]
    return core


# Channel furniture in a description makes claims about the CHANNEL -- "one of 56 full-length
# cases on this channel, 28 of them posted in the last 28 days". No episode record can support
# those numbers and they say nothing about the case.
BOILERPLATE = ("this channel", "the channel", "subscribe", "full-length case", "posted in the",
               "more like this", "new episode", "playlist", "sources and citations",
               "ai-generated", "ai generated", "generated with", "chapters", "timestamps",
               "follow us", "0:00", "http", "youtube.com", "youtu.be", "sub_confirmation",
               "@prime", "watch next", "read the sources",
               # Channel CTA. "More are finished and already scheduled" and "Subscribing is
               # what puts the next one in front of you" are promises about the CHANNEL; no
               # episode script can ever state them, so verifying them only produces noise.
               "subscrib", "already scheduled", "are finished and", "in front of you",
               "the next one", "notification", "comment below", "let me know")


VOTE_RE = re.compile(r"\b([0-9])\s*[-–]\s*([0-9])\b")


def is_boilerplate(chunk: str) -> bool:
    low = chunk.lower()
    return any(b in low for b in BOILERPLATE)


def extract_claims(text: str, field_name: str, rec: Record) -> list[Claim]:
    """Over-extract on purpose: the verifier decides, not the extractor."""
    claims: list[Claim] = []
    if not text or not text.strip():
        return claims
    for chunk in re.split(r"(?<=[.!?])\s+|\s*[—|/]\s*|\n+", text):
        chunk = chunk.strip()
        if len(chunk) < 2 or is_boilerplate(chunk):
            continue
        # A vote split is ONE claim about ONE decision. Read as two numbers, "8-1" became a
        # claim that eight of something and one of something else appear in the film.
        votes = VOTE_RE.findall(chunk)
        if votes:
            chunk = VOTE_RE.sub(" ", chunk)
        for a_, b_ in votes:
            claims.append(Claim("vote", f"{a_}-{b_}", field_name, [f"{a_}-{b_}"],
                                [f"{a_}-{b_}"], None, None, None, False, False, True))

        toks = tokens_of(chunk)
        low = [t.lower() for t in toks]
        stems = content_stems(chunk)
        hedged = any(t in STRONG_HEDGE or t in WEAK_HEDGE for t in low)
        # Polarity is a property of the CLAUSE. "Five Children Confessed to a Crime They
        # Didn't Commit" is a negative claim about committing, and reading only a 5-token
        # window around "Five" made the checker treat the film's own "DNA proved they did
        # not commit" as a contradiction of the title it actually supports.
        clause_neg = any(t in NEGATION_CUES for t in low)

        # --- numbers: quantity / duration / money / date
        for m in find_numbers(chunk):
            neg = _negated_at(toks, m.tok_i)
            kind = {"money": "money", "year": "date"}.get(m.kind, "quantity")
            if m.head in TIME_UNITS:
                kind = "duration"
            terms = [t for t in stems]
            core = _pick_core(terms, rec.df, m.head)
            # "$0" / "0 GUILTY" asserts an absence. Treating it as a positive claim made the
            # record's own "the city refused to pay" read as a contradiction of "THEY PAID
            # HIM $0", which is the same fact.
            claims.append(Claim(kind, chunk, field_name, terms, core, m.value, m.kind,
                                m.head, neg or clause_neg or m.value == 0, hedged))

        # --- outcome verbs
        for i, t in enumerate(low):
            # A curated lexicon under-extracts: "Agents Never Stepped on His Property" carries
            # a factual assertion and yielded no claim at all. Any past-tense form is a claim.
            in_lexicon = t in OUTCOME_VERBS
            if not (in_lexicon or t in IRREGULAR_PAST
                    or (len(t) > 4 and t.endswith("ed") and t not in STOPWORDS)):
                continue
            st = stem(t)
            lo, hi = max(0, i - 7), min(len(toks), i + 8)
            span = " ".join(toks[lo:hi])
            terms = [x for x in content_stems(span)]
            if st not in terms:
                terms.append(st)
            core = _pick_core(terms, rec.df, st)
            # HARD vs SOFT. Every past-tense verb is extracted, verified and printed -- an
            # unextracted claim is the one that ships. But only the outcome LEXICON blocks:
            # "confessed", "acquitted", "seized", "died" are the assertions this channel gets
            # sued over, while "became", "closed", "chose" are ordinary prose that the film
            # states in different words as often as not. Blocking a booking on "He Had Closed
            # the Door" is how a check gets switched off in a day. --strict blocks on both.
            claims.append(Claim("outcome", chunk, field_name, terms, core, None, None, st,
                                _negated_at(toks, i) or clause_neg, hedged, in_lexicon))

        # --- proper names of people and institutions
        #
        # A title is Title Case, so capitalisation alone proves nothing. A token counts as a
        # name when it is capitalised, is not a number word, is not ordinary English, and is
        # not a word the record itself writes in lower case.
        for t in toks:
            if not t[:1].isalpha() or len(t) < 3 or not t[0].isupper():
                continue
            base = t.lower().strip("'’")
            if base in NUM_WORDS or base in MULTIPLIER_WORDS:
                continue
            if re.search(r"(ed|ing|ly|ise|ised|ize|ized|ness|ment)$", base) and len(base) > 5:
                continue
            st = stem(t)
            if base in COMMON_WORDS or st in COMMON_WORDS or st in STOPWORDS:
                continue
            if base in BRAND_WORDS or st in BRAND_WORDS:
                continue
            if st in rec.lower_vocab or st in channel_vocab():
                continue
            claims.append(Claim("name", t, field_name, [st], [st], None, None, st, False,
                                hedged))

    out, seen = [], set()
    for c in claims:
        if c.key() in seen:
            continue
        seen.add(c.key())
        out.append(c)
    return out


# ------------------------------------------------------------------------------ verification

@dataclass
class Evidence:
    kind: str        # support | contradiction | mismatch | qualified | guardrail
    where: str
    text: str
    source: str
    note: str = ""

    def as_dict(self) -> dict:
        return {"kind": self.kind, "where": self.where, "source": self.source,
                "note": self.note, "line": self.text}


def _num_ok(claim: Claim, s: Sentence) -> NumMention | None:
    """A number in this sentence that is THIS claim's number, attached to THIS claim's noun.

    The proximity rule matters more than it looks: "a sailor named Eric Wilson was questioned
    for about NINE HOURS" contains the number nine and the word sailor, and without it the
    checker certified "Nine Sailors Were Charged" against a film that says seven. It was found
    by tests/test_packaging_claims.py, not by reading the code.
    """
    for m in s.nums:
        if not num_close(m.value, claim.number) or m.kind != claim.num_kind:
            continue
        if claim.head is None:
            return m
        if m.head == claim.head:
            return m
        if m.head is not None and m.head in UNIT_NOUNS and claim.head not in UNIT_NOUNS:
            continue                      # "nine hours" is not "nine sailors"
        # the noun may sit further from the digits in the record than in a title, but it has
        # to be NEAR them
        for j, tok in enumerate(s.toks):
            if stem(tok) == claim.head and abs(j - m.tok_i) <= 4:
                return m
    return None


def _num_conflict(claim: Claim, s: Sentence) -> NumMention | None:
    """A different number for the same subject AND the same kind of quantity.

    Without the kind test, "$550 million in a year" was reported as contradicted by "in one
    year, he was paid more than entire corporations earned" -- 1 year against 550,000,000
    dollars, compared because both were filed under the noun "year".
    """
    for m in s.nums:
        if num_close(m.value, claim.number):
            return None
    for m in s.nums:
        if (m.head and claim.head and m.head == claim.head
                and m.kind == claim.num_kind
                and not num_close(m.value, claim.number)):
            return m
    return None


def _hedge_at(s: Sentence, i: int, window: int = 12) -> str | None:
    """Every strong hedge sitting around this number, joined -- one word rarely tells the story
    ("on paper ... as much as ... the theoretical maximum" is three)."""
    lo, hi = max(0, i - window), min(len(s.toks), i + 4)
    win = [t.lower() for t in s.toks[lo:hi]]
    hits = [t for t in win if t in STRONG_HEDGE]
    hits += [" ".join(b) for b in HEDGE_BIGRAMS if any(
        win[k] == b[0] and win[k + 1] == b[1] for k in range(len(win) - 1))]
    return " / ".join(dict.fromkeys(hits)) if hits else None


def _neg_attached(claim: Claim, s: Sentence, *, strict: bool = False
                  ) -> tuple[set[str], int, str] | None:
    """A negation cue sitting on one of the claim's own terms, in this sentence.

    Returns (which core terms are negated, how close the nearest cue is, the snippet). The
    distance is what separates "gave NO videotaped confession" from a paragraph that merely
    contains a "not" somewhere near the word "confession".
    """
    negated: set[str] = set()
    best, snippet = 99, ""
    for i, t in enumerate(s.toks):
        st = stem(t)
        if st not in claim.core:
            continue
        d = (_neg_distance(s.toks, i, 5, governs=set(claim.core), allow_modal=False)
             if strict else _neg_distance(s.toks, i, 5))
        if d is None:
            continue
        negated.add(st)
        if d < best:
            best, snippet = d, " ".join(s.toks[max(0, i - 5):i + 2])
    return (negated, best, snippet) if negated else None


MODALS = {"could", "can", "cannot", "cant", "would", "will", "shall", "should", "may",
          "might", "must"}


def _neg_distance(toks: list[str], i: int, window: int = 5, *, governs: set[str] | None = None,
                  allow_modal: bool = True) -> int | None:
    """How close a negation cue is to toks[i], or None if none governs it.

    `governs` switches on the strict reading used for CONTRADICTION: the cue may only be
    separated from the word by stopwords, number words and the claim's OWN terms. That one
    rule is the difference between

        "gave NO videotaped confession"          -> the film denies the claim
        "was NOT built and the land sat vacant"  -> the film says something else entirely

    and it removed most of this check's false alarms. `allow_modal=False` additionally drops
    "could not be searched" and "cannot be used" -- a rule about what MAY happen is not a
    denial of what DID happen.
    """
    if governs is not None:
        # "The building did not fall BECAUSE nobody knew" denies the cause, not the event.
        for t in toks[i + 1:i + 4]:
            if t.lower() in ("because", "merely", "simply", "just", "only"):
                return None
    lo = max(0, i - window)
    for j in range(i - 1, lo - 1, -1):
        w = toks[j].lower()
        if w in NEGATION_CUES and not (governs is not None and w in DENIAL_EXCLUDED):
            if not allow_modal and (w in MODALS or (j and toks[j - 1].lower() in MODALS)):
                return None
            return i - j
        if governs is not None:
            st = stem(toks[j])
            if not (w in STOPWORDS or w in NUM_WORDS or w in MULTIPLIER_WORDS
                    or st in governs or st in STOPWORDS or toks[j][0].isdigit()):
                return None
    for j in range(i + 1, min(len(toks), i + 3)):
        w = toks[j].lower()
        if w in NEGATION_CUES and not (governs is not None and w in DENIAL_EXCLUDED):
            if not allow_modal and (w in MODALS or toks[j - 1].lower() in MODALS):
                return None
            return j - i
        if governs is not None and not (w in STOPWORDS or stem(toks[j]) in STOPWORDS):
            return None
    return None


def _dedupe(evs: list[Evidence]) -> list[Evidence]:
    """The captions repeat the script almost verbatim; the same line twice is not two proofs."""
    out, seen = [], set()
    for e in evs:
        k = re.sub(r"[^a-z0-9 ]", "", e.text.lower())[:120]
        if k in seen:
            continue
        seen.add(k)
        out.append(e)
    return out


def _verify_name(claim: Claim, rec: Record) -> dict:
    """A name is checked for PRESENCE only -- negation logic makes no sense on a noun.

    The question a name claim answers is the one that matters: does this episode's own record
    mention this person, institution or place at all, or did the packaging invent it?
    """
    key = claim.core[0]
    where = rec.where(key)
    ev: list[Evidence] = []
    prefer = "narration" if "narration" in where else ("ledger" if where else None)
    for s in rec.sentences:
        if s.source == prefer and key in s.stems:
            ev.append(Evidence("support", f"{s.path}:{s.line}", s.text, s.source,
                               f"the record names {claim.text!r}"))
            if len(ev) >= 2:
                break
    if "narration" in where:
        verdict = "SUPPORTED"
    elif where:
        verdict = "SUPPORTED_LEDGER_ONLY" if rec.has_narration() else "SUPPORTED"
    else:
        verdict = "UNVERIFIED"
    return {
        "claim": claim.text.strip(), "kind": "name", "field": claim.field, "number": None,
        "head": claim.head, "negated": False, "required_terms": claim.core,
        "verdict": verdict, "ok": verdict in PASS_VERDICTS, "hard": True,
        "evidence": [e.as_dict() for e in ev], "counter_evidence": [],
    }


def _verify_vote(claim: Claim, rec: Record) -> dict:
    """A vote split is verified as the pair it is: "9-0" or "nine to nothing", not two counts."""
    a, b = claim.text.split("-")
    words = {"0": "(?:zero|nothing|none)", "1": "one", "2": "two", "3": "three", "4": "four",
             "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
    pat = re.compile(rf"\b{a}\s*[-–to ]{{1,4}}\s*{b}\b|\b{words.get(a, a)}"
                     rf"[ -]to[ -]{words.get(b, b)}\b", re.I)
    ev: list[Evidence] = []
    for s in rec.sentences:
        if pat.search(s.text):
            ev.append(Evidence("support", f"{s.path}:{s.line}", s.text, s.source,
                               f"the record states the split {claim.text}"))
            if len(ev) >= 2:
                break
    return {"claim": claim.text, "kind": "vote", "field": claim.field, "number": None,
            "head": None, "negated": False, "required_terms": claim.core,
            "verdict": "SUPPORTED" if ev else "UNVERIFIED", "ok": bool(ev), "hard": True,
            "evidence": [e.as_dict() for e in ev], "counter_evidence": []}


def verify_claim(claim: Claim, rec: Record) -> dict:
    """One claim against the whole record. Returns verdict + the lines that decided it."""
    if claim.kind == "name":
        return _verify_name(claim, rec)
    if claim.kind == "vote":
        return _verify_vote(claim, rec)
    support: list[Evidence] = []
    line_support: list[Evidence] = []
    ledger_support: list[Evidence] = []
    qualified: list[Evidence] = []
    contra: list[Evidence] = []  # filled from contra_rank below
    mismatch: list[Evidence] = []

    contra_rank: list[tuple] = []
    core = set(claim.core)

    # Does the record pair THIS number with THIS subject anywhere at all? If it does, a
    # different number somewhere else in a 10,000-word script is a different moment, not a
    # contradiction -- swartz's narration says "four felonies" in July 2011 and "thirteen
    # felony counts" after the superseding indictment, and both are true. NUMBER_MISMATCH is
    # reserved for the case the policy actually names: the record states a different number
    # for the same subject and never states this one.
    num_confirmed = False
    if claim.number is not None:
        for s in rec.sentences:
            if _num_ok(claim, s) is not None and (claim.head is None or claim.head in s.stems):
                num_confirmed = True
                break

    for s in rec.sentences:
        matched = core & s.stems
        # --------------------------------------------------- support
        if matched == core:
            num_m = None
            if claim.number is not None:
                num_m = _num_ok(claim, s)
            neg_here = _neg_attached(claim, s) is not None
            polarity_ok = (neg_here == claim.negated)
            if (claim.number is None or num_m is not None) and polarity_ok:
                hedge = None
                if claim.number is not None and num_m is not None and not claim.hedged:
                    hedge = _hedge_at(s, num_m.tok_i)
                ev = Evidence("support", f"{s.path}:{s.line}", s.text, s.source,
                              f"matched {sorted(core)}"
                              + (f" number={claim.number:g}" if claim.number is not None else ""))
                if hedge:
                    qualified.append(Evidence("qualified", ev.where, s.text, s.source,
                                              f"the record states this only inside a hedge "
                                              f"(\"{hedge}\"); the packaging states it flat"))
                elif s.source == "narration":
                    support.append(ev)
                else:
                    ledger_support.append(ev)
                continue
        # --------------------------------------------------- contradiction
        if matched and not s.record_meta:
            neg = _neg_attached(claim, s, strict=True)
            if neg and not claim.negated:
                negated_terms, dist, snippet = neg
                # The subject has to be in play: either this sentence carries two of the
                # claim's terms, or the surrounding paragraph does.
                # STRONG: this one sentence carries two or more of the claim's own terms and
                # denies them -- "gave no videotaped confession" against "five boys confessed
                # on camera". That outranks everything except a whole-sentence statement of
                # the claim.
                # WEAK: one term denied here, the subject established in the surrounding
                # paragraph -- "None of the three ever confessed", in the paragraph about the
                # seven sailors. It is real evidence and it is what catches the Norfolk title,
                # but on its own it fires on any film that argues with itself, so it only
                # speaks when NOTHING in the record supports the claim.
                # STRONG needs the denial itself to cover two of the claim's terms, in the
                # FILM's own words. "The Court did not say the police can never see what is
                # on your phone" mentions three of riley's title terms but negates one of
                # them, and it is not a denial of that title.
                strong = len(negated_terms) >= 2 and s.source == "narration"
                corroborated = (strong
                                or len(core & rec.line_stems.get(s.line_key, set())) >= 2)
                if corroborated or len(core) == 1:
                    ev = Evidence("contradiction", f"{s.path}:{s.line}", s.text, s.source,
                                  f"negation attached to {sorted(negated_terms)} "
                                  f"(cue {dist} token(s) away): …{snippet}…")
                    # Rank the denials. What the FILM says outranks what the research ledger
                    # says; a sentence whose paragraph carries more of the claim outranks a
                    # stray stem collision ("no sign of forced entry" vs "signed"); then the
                    # most of the claim denied, the closest cue, the most focused sentence.
                    # The sharpest denial has to print first or the reviewer reads three
                    # vague lines and stops reading.
                    para = len(core & rec.line_stems.get(s.line_key, set()))
                    contra_rank.append((0 if strong else 1,
                                        0 if s.source == "narration" else 1,
                                        0 if len(s.toks) >= 8 else 1, -para,
                                        -len(negated_terms), -len(matched), dist,
                                        len(s.text), len(contra_rank), ev))
                    continue

        # --------------------------------------------------- number mismatch
        # A claim of ZERO ("0 GUILTY") asserts an absence; the record naturally counts other
        # things ("the one guilty man"), and calling that a mismatch is arithmetic, not truth.
        if (claim.number and claim.head and claim.head in s.stems and not num_confirmed):
            if len(matched) >= min(2, len(core)):
                bad = _num_conflict(claim, s)
                if bad is not None:
                    mismatch.append(Evidence("mismatch", f"{s.path}:{s.line}", s.text, s.source,
                                             f"the record states {bad.value:g} "
                                             f"{bad.head or ''} where the packaging states "
                                             f"{claim.number:g}"))
                    continue
        # --------------------------------------------------- paragraph-level support
    # ------------------------------------------------------------ paragraph-level support
    #
    # A title clause is routinely spread over a paragraph of narration: riley's film asks
    # "can the police simply open it" two sentences before "an officer takes the smartphone
    # out of his pocket". Requiring one sentence to carry the whole clause was the single
    # largest source of false UNVERIFIED. This is weaker evidence and says so on the line --
    # and a sentence-level DENIAL still outranks it.
    for lk, group in rec.line_sents.items():
        if not core <= rec.line_stems.get(lk, set()):
            continue
        best_s, best_n = None, -1
        for s in group:
            if claim.number is not None and _num_ok(claim, s) is None:
                continue
            n = len(core & s.stems)
            if n > best_n:
                best_s, best_n = s, n
        if best_s is None or best_n < 1:
            continue
        if claim.negated and not any(_neg_attached(claim, x) for x in group):
            continue
        line_support.append(
            Evidence("support", f"{best_s.path}:{best_s.line}", best_s.text, best_s.source,
                     f"terms {sorted(core)} co-occur in this paragraph"
                     + (" and the number is in this sentence" if claim.number is not None
                        else "") + " (weaker than a single-sentence match)"))

    ranked = sorted(contra_rank, key=lambda r: r[:-1])
    contra = [row[-1] for row in ranked if row[0] == 0]
    weak_contra = [row[-1] for row in ranked if row[0] == 1]

    # guardrails: the episode's own "do not state this as fact" block
    guard_hits: list[Evidence] = []
    if claim.number is not None or claim.kind == "outcome":
        for text, where in rec.guardrails:
            gs = set(content_stems(text))
            shared = gs & core
            same_number = (claim.number is not None
                           and any(num_close(m.value, claim.number)
                                   for m in find_numbers(text)))
            # Polarity. A DO_NOT_STATE line forbids ASSERTING something ("The Court ordered
            # Kentucky to use the mail."); packaging that says the OPPOSITE ("It did not order
            # Kentucky to use the mail") is the episode obeying the guardrail, not breaking it.
            if claim.negated and not any(t.lower() in NEGATION_CUES for t in tokens_of(text)):
                continue
            if len(shared) >= 3 or (same_number and len(shared) >= 2):
                guard_hits.append(Evidence("guardrail", where, text, "guardrail",
                                           f"the episode forbids stating this bare "
                                           f"(shared terms {sorted(shared)})"))

    # ---------------------------------------------------------------- precedence
    if support:
        # The record states the whole claim, in one sentence, with the right number and the
        # right polarity. A negation somewhere else in a 10,000-word script is a different
        # sentence about a different thing -- it is printed as counter-evidence, not as a
        # verdict. (Neither false title reaches here: no sentence of either film states them.)
        verdict = "SUPPORTED"
        decided = support
    elif contra:
        verdict = "CONTRADICTED"
        decided = contra
    elif mismatch:
        verdict = "NUMBER_MISMATCH"
        decided = mismatch
    elif qualified:
        verdict = "QUALIFIED_ONLY"
        decided = qualified
    elif guard_hits:
        verdict = "FORBIDDEN_AS_FACT"
        decided = guard_hits
    elif line_support:
        verdict = "SUPPORTED"
        decided = line_support
    elif ledger_support:
        # A whole sentence that states the claim -- terms, number and polarity -- outranks a
        # WEAK denial, which is one term with a negation near it and the subject only
        # established in the surrounding paragraph. Sharper evidence wins: the weak denial is
        # printed underneath as counter-evidence. (STRONG denials are decided far above.)
        verdict = "SUPPORTED_LEDGER_ONLY" if rec.has_narration() else "SUPPORTED"
        decided = ledger_support
    elif weak_contra:
        verdict = "CONTRADICTED"
        decided = weak_contra
    else:
        verdict = "UNVERIFIED"
        decided = []

    decided = _dedupe(decided)
    # Whatever did NOT decide the verdict is still shown, briefly. On a pass it is the
    # counter-evidence a reviewer must see; on a failure it is the second reason (the record
    # may both deny the claim AND state a different number, and both are worth one line).
    others = {"CONTRADICTED": mismatch + qualified + support + weak_contra,
              "NUMBER_MISMATCH": contra + qualified + support,
              "SUPPORTED": contra + mismatch + qualified,
              "QUALIFIED_ONLY": contra + mismatch,
              "SUPPORTED_LEDGER_ONLY": weak_contra + contra + mismatch + qualified,
              "UNVERIFIED": contra + weak_contra + mismatch + qualified + ledger_support,
              }.get(verdict, [])
    counter = [e.as_dict() for e in _dedupe(others)[:2]]
    if verdict != "FORBIDDEN_AS_FACT" and guard_hits and verdict == "SUPPORTED":
        verdict = "FORBIDDEN_AS_FACT"
        decided = guard_hits

    return {
        "claim": claim.text.strip(),
        "kind": claim.kind,
        "field": claim.field,
        "number": claim.number,
        "head": claim.head,
        "negated": claim.negated,
        "required_terms": claim.core,
        "verdict": verdict,
        "ok": verdict in PASS_VERDICTS,
        "hard": claim.hard,
        "evidence": [e.as_dict() for e in decided[:3]],
        "counter_evidence": counter,
    }


# --------------------------------------------------------------------------------- the gate

def check_packaging(epdir: Path, fields: dict[str, str], *, strict: bool = False) -> dict:
    """Verify one episode's packaging text. `fields` = {title, thumbnail_text, description}.

    `strict` also blocks on SOFT claims (ordinary past-tense verbs outside the outcome
    lexicon). They are always extracted, verified and printed; by default they do not hold
    the door shut, because the verifier matches words and the films paraphrase.
    """
    rec = load_record(epdir)
    claims: list[Claim] = []
    for name, text in fields.items():
        if text:
            claims += extract_claims(str(text), name, rec)
    results = [verify_claim(c, rec) for c in claims]
    # A DESCRIPTION is 4,000 characters of prose; UNVERIFIED there is dominated by paraphrase,
    # and 55 of them at once would bury the one that matters. In a description only the sharp
    # verdicts hold the door: the record DENYING it, a different number for the same subject,
    # a figure the record only hedges. In a TITLE and on a THUMBNAIL -- short, deliberate, the
    # most widely read sentence the channel publishes, and cheap to write out of the film's own
    # words -- UNVERIFIED still blocks.
    #
    # UNVERIFIED IS NOW A NOTE EVERYWHERE, NOT ONLY IN A DESCRIPTION (2026-08-12). Measured over
    # the live catalogue: 84 blocking rows, 71 of them UNVERIFIED, and the hand-checked sample
    # was overwhelmingly paraphrase -- the film states the same fact in other words and a
    # stem matcher cannot see it. A gate that is wrong five times out of six is switched off
    # within a week, and it was holding four finished episodes at once. The SHARP verdicts keep
    # the door: the record DENYING the claim, a different number for the same subject, a figure
    # the record only hedges, and a figure the episode's own DO_NOT_STATE block forbids. Those
    # are the ones that caught both false titles, and their measured precision is far higher.
    # `--strict` restores the old behaviour and blocks on everything.
    for r in results:
        if r["verdict"] not in BLOCKING_VERDICTS:
            r["hard"] = False          # demote only; a soft claim never becomes hard here
    bad = [r for r in results if not r["ok"] and (r.get("hard", True) or strict)]
    soft = [r for r in results if not r["ok"] and not (r.get("hard", True) or strict)]
    return {
        "check": "packaging_claims",
        "episode": epdir.name,
        "ok": not bad,
        "hard": bool(bad),
        "record_sources": rec.sources,
        "record_sentences": len(rec.sentences),
        "record_has_narration": rec.has_narration(),
        "guardrails": len(rec.guardrails),
        "fields": {k: v for k, v in fields.items() if v},
        "claims_checked": len(results),
        "unsupported": len(bad),
        "soft_unsupported": len(soft),
        "strict": bool(strict),
        "reason": ("; ".join(f"{r['verdict']}: {r['claim'][:60]}" for r in bad[:4])
                   if bad else "every extracted claim is stated by the episode's own record"),
        "results": results,
    }


def _thumb_text(epdir: Path) -> str:
    """Whatever thumbnail wording this episode declares, from wherever it declares it."""
    parts: list[str] = []
    pkg = epdir / "09_package"
    for pat in ("title_thumbnail_candidates.v*.json", "youtube_meta.v*.json",
                "thumbnail_text.v*.json"):
        for p in sorted(pkg.glob(pat)):
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
            except Exception:                                          # noqa: BLE001
                continue
            stack = [d]
            while stack:
                cur = stack.pop()
                if isinstance(cur, dict):
                    for k, v in cur.items():
                        if isinstance(v, str) and "thumb" in k.lower() and "text" in k.lower():
                            parts.append(v)
                        elif isinstance(v, (dict, list)):
                            stack.append(v)
                elif isinstance(cur, list):
                    stack.extend(cur)
    # the live record, when the repo has one
    gen = genome_row(epdir.name)
    if gen and gen.get("thumbnail_text"):
        parts.append(gen["thumbnail_text"])
    return " . ".join(dict.fromkeys(p for p in parts if p))


def evaluate(epdir: Path, *, strict: bool = False) -> dict:
    """Gate entry point, same shape as every other `check_*.evaluate(epdir)` in scripts/.

    Reads the packaging the SCHEDULER would upload: 09_package/youtube_meta.v001.json (title +
    description) plus whatever thumbnail wording the episode declares.
    """
    epdir = Path(epdir)
    metas = sorted((epdir / "09_package").glob("youtube_meta.v*.json"))
    title = desc = ""
    if metas:
        try:
            m = json.loads((epdir / "09_package" / "youtube_meta.v001.json").read_text(
                encoding="utf-8")) if (epdir / "09_package" / "youtube_meta.v001.json").is_file() \
                else json.loads(metas[-1].read_text(encoding="utf-8"))
            title, desc = m.get("title", ""), m.get("description", "")
        except Exception as exc:                                       # noqa: BLE001
            return {"check": "packaging_claims", "ok": False, "hard": True, "skipped": False,
                    "reason": f"cannot read youtube_meta: {exc}"}
    thumb = _thumb_text(epdir)
    if not (title or thumb or desc):
        return {"check": "packaging_claims", "ok": True, "hard": False, "skipped": True,
                "reason": "no packaging authored yet (no youtube_meta, no thumbnail text): "
                          "packaging is a late step and absence is not a failure"}
    return check_packaging(epdir, {"title": title, "thumbnail_text": thumb,
                                   "description": desc}, strict=strict)


def fact_failures(slug_or_epid: str, title: str, thumbnail_text: str = "",
                  description: str = "") -> list[str]:
    """Reasons this packaging may not be published. Empty list = every claim is supported.

    Callable from the live-title writers (`apply_title_batch.py`) which have a title and a slug
    and nothing else.
    """
    epdir = resolve_epdir(slug_or_epid)
    if epdir is None:
        return [f"no episode directory for {slug_or_epid!r} -- claims cannot be verified"]
    r = check_packaging(epdir, {"title": title, "thumbnail_text": thumbnail_text,
                                "description": description})
    return [f"{x['verdict']} {x['claim'][:70]!r}"
            + (f" <- {x['evidence'][0]['where']}" if x["evidence"] else "")
            for x in r["results"] if not x["ok"]]


# ------------------------------------------------------------------------------------ CLI

def resolve_epdir(key: str) -> Path | None:
    key = key.strip()
    p = ROOT / "episodes" / key
    if p.is_dir():
        return p
    hits = sorted((ROOT / "episodes").glob(f"PD-*-{key}"))
    if hits:
        return hits[-1]
    hits = sorted((ROOT / "episodes").glob(f"*{key}*"))
    return hits[-1] if hits else None


_CHANNEL_VOCAB: set[str] | None = None


def channel_vocab() -> set[str]:
    """Every word the CHANNEL writes in lower case, across all episode scripts.

    This is the English lexicon the proper-name test needs, taken from the repo instead of
    hard-coded: if any of the 70 scripts writes "camera", "showed" or "swore" in lower case,
    then a Title-Cased "Camera" in a headline is an ordinary word, not the name of a person or
    an institution. Built once per process; 70 files, well under a second.
    """
    global _CHANNEL_VOCAB
    if _CHANNEL_VOCAB is None:
        v: set[str] = set()
        for sp in (ROOT / "episodes").glob("PD-*/03_script/script.en.v*.md"):
            try:
                txt = sp.read_text(encoding="utf-8", errors="replace")
            except Exception:                                          # noqa: BLE001
                continue
            for tok in TOKEN_RE.findall(txt):
                if tok[:1].islower():
                    v.add(stem(tok))
        _CHANNEL_VOCAB = v
    return _CHANNEL_VOCAB


_GENOME_CACHE: dict[str, dict] | None = None


def genome_rows() -> dict[str, dict]:
    global _GENOME_CACHE
    if _GENOME_CACHE is None:
        rows: dict[str, dict] = {}
        if GENOME.is_file():
            for ln in GENOME.read_text(encoding="utf-8").splitlines():
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    d = json.loads(ln)
                except Exception:                                      # noqa: BLE001
                    continue
                rows[d.get("episode_id", "")] = {
                    "video_id": d.get("video_id"),
                    "title": d.get("title", ""),
                    "thumbnail_text": (d.get("genome") or {}).get("thumbnail_text", ""),
                }
        _GENOME_CACHE = rows
    return _GENOME_CACHE


def genome_row(epid: str) -> dict | None:
    return genome_rows().get(epid)


def _print_report(res: dict, *, verbose: bool = False) -> None:
    head = "PASS" if res["ok"] else "FAIL"
    print(f"[{head}] {res['episode']}  claims={res['claims_checked']} "
          f"unsupported={res['unsupported']}"
          + (f" (+{res['soft_unsupported']} soft, not blocking)"
             if res.get("soft_unsupported") else "")
          + f"  record={res['record_sentences']} sentences "
            f"from {len(res['record_sources'])} files")
    for k, v in res["fields"].items():
        print(f"    {k:<15} {v[:150]}")
    for r in res["results"]:
        if r["ok"] and not verbose:
            continue
        blocking = (not r["ok"]) and (r.get("hard", True) or res.get("strict"))
        mark = "ok  " if r["ok"] else ("FAIL" if blocking else "note")
        print(f"  {mark} {r['verdict']:<22} [{r['field']}/{r['kind']}] {r['claim'][:78]!r}")
        print(f"       needs: {r['required_terms']}"
              + (f"  number={r['number']:g}" if r["number"] is not None else "")
              + (f"  head={r['head']}" if r["head"] else "")
              + ("  (negated)" if r["negated"] else ""))
        for e in r["evidence"]:
            print(f"       {e['where']}  [{e['source']}] {e['note']}")
            print(f"         > {e['line'][:230]}")
        if not r["evidence"]:
            print("       (no line in the record addresses this)")
        for e in r["counter_evidence"]:
            print(f"       counter-evidence {e['where']}: {e['line'][:150]}")
    if res["ok"]:
        print("  every extracted claim is stated by the episode's own record.")
        print("  NOTE: this cannot judge tone, implication, or a claim the script makes badly. "
              "Read the title against the film.")


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:                                                  # noqa: BLE001
        pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--slug", help="episode slug, id, or directory name")
    ap.add_argument("--title")
    ap.add_argument("--thumb-text", default="")
    ap.add_argument("--description", default="")
    ap.add_argument("--description-file", type=Path)
    ap.add_argument("--package", action="store_true",
                    help="check the packaging on disk (09_package/youtube_meta.v001.json)")
    ap.add_argument("--live", action="store_true",
                    help="check the titles/thumbnail text recorded live in "
                         "data/content_genome.v001.jsonl")
    ap.add_argument("--proposal", type=Path,
                    help="check every {slug|episode_id, title|new_title|recommended_title} row "
                         "in a proposal json")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--verbose", action="store_true", help="print supported claims too")
    ap.add_argument("--strict", action="store_true",
                    help="also block on SOFT claims (ordinary past-tense verbs outside the "
                         "outcome lexicon). They are printed either way.")
    a = ap.parse_args(argv)

    jobs: list[tuple[Path, dict]] = []

    if a.live:
        for epid, row in sorted(genome_rows().items()):
            if a.slug and a.slug not in epid:
                continue
            ep = resolve_epdir(epid)
            if ep is None:
                print(f"[skip] {epid}: no episode directory")
                continue
            jobs.append((ep, {"title": row["title"], "thumbnail_text": row["thumbnail_text"]}))
    elif a.proposal:
        data = json.loads(a.proposal.read_text(encoding="utf-8"))
        found: list[dict] = []
        title_keys = ("recommended_title", "new_title", "core", "broad", "title",
                      "proposed_title", "REJECTED_ALTERNATIVE")

        def walk(node, key: str | None, thumb: str) -> None:
            """Carry the nearest enclosing episode id down: a proposal keeps the id on the row
            and the titles in a nested `proposal` object, so a flat scan finds neither."""
            if isinstance(node, dict):
                key = node.get("episode_id") or node.get("slug") or key
                thumb = (node.get("thumbnail_text") or node.get("thumb_text") or thumb)
                titles = [node[k] for k in title_keys if isinstance(node.get(k), str)]
                if key and titles:
                    found.append({"key": key, "titles": titles, "thumb": thumb})
                for v in node.values():
                    if isinstance(v, (dict, list)):
                        walk(v, key, thumb)
            elif isinstance(node, list):
                for v in node:
                    walk(v, key, thumb)

        walk(data, None, "")
        for f in found:
            if a.slug and a.slug not in str(f["key"]):
                continue
            ep = resolve_epdir(str(f["key"]))
            if ep is None:
                continue
            for t in dict.fromkeys(f["titles"]):
                jobs.append((ep, {"title": t, "thumbnail_text": f["thumb"]}))
    elif a.package:
        if not a.slug:
            ap.error("--package needs --slug")
        ep = resolve_epdir(a.slug)
        if ep is None:
            raise SystemExit(f"no episode for {a.slug!r}")
        r = evaluate(ep, strict=a.strict)
        if a.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        elif r.get("skipped"):
            print(f"[skip] {ep.name}: {r['reason']}")
        else:
            _print_report(r, verbose=a.verbose)
        return 0 if r["ok"] else 1
    else:
        if not (a.slug and (a.title or a.thumb_text or a.description or a.description_file)):
            ap.error("give --slug plus --title/--thumb-text/--description, "
                     "or use --package / --live / --proposal")
        ep = resolve_epdir(a.slug)
        if ep is None:
            raise SystemExit(f"no episode for {a.slug!r}")
        desc = a.description
        if a.description_file:
            desc = a.description_file.read_text(encoding="utf-8")
        jobs.append((ep, {"title": a.title or "", "thumbnail_text": a.thumb_text,
                          "description": desc}))

    out, failed = [], 0
    for ep, fields in jobs:
        r = check_packaging(ep, fields, strict=a.strict)
        out.append(r)
        if not r["ok"]:
            failed += 1
        if not a.json:
            _print_report(r, verbose=a.verbose)
            print()
    if a.json:
        print(json.dumps(out if len(out) != 1 else out[0], ensure_ascii=False, indent=2))
    elif len(jobs) > 1:
        print(f"== {len(jobs) - failed}/{len(jobs)} packaging sets fully supported; "
              f"{failed} carry at least one unsupported claim ==")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
