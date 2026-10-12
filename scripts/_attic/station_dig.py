# -*- coding: utf-8 -*-
"""Mine NIST NCSTAR 2 for the EP81 facts ledger, page-cited.

TRAP: this PDF extracts with NO SPACES between words --
"Pyrotechnicdevicesshouldbebanned...". A normal keyword search returns almost
nothing and looks like the facts are absent. So every pattern here is matched
against a space-stripped copy of each page, and the printed context is
space-stripped too. It is ugly to read but it is the actual text.
"""
import re, sys, io, pathlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

raw = pathlib.Path("station_ncstar2.txt").read_text(encoding="utf-8")
parts = re.split(r"<<<PAGE (\d+)>>>", raw)
pages = [(int(parts[i]), re.sub(r"\s+", "", parts[i + 1])) for i in range(1, len(parts), 2)]
body = [(p, t) for p, t in pages if p >= 20]


def show(title, pat, n=2, before=260, after=700):
    print("\n===== %s =====" % title)
    pat = pat.replace(" ", "")
    c = 0
    seen = set()
    for p, t in body:
        for m in re.finditer(pat, t, re.I):
            s = max(0, m.start() - before); e = min(len(t), m.end() + after)
            frag = t[s:e]
            if frag[:60] in seen:
                continue
            seen.add(frag[:60])
            print(" [p%d]" % p, frag[:620]); c += 1
            if c >= n: break
        if c >= n: break
    if not c: print("  (no hit)")


show("how many people inside", r"(occupantsinthenightclub|peopleinthebuilding|approximately\d{3}people|\d{3}occupants)", 3)
show("100 died", r"(100|onehundred)(people|persons|individuals)?(died|losttheirlives|fatalities)", 3)
show("95 of the fatalities", r"95ofthe(fatalities|100)", 2)
show("pyrotechnics ignited the foam", r"pyrotechnics?(that)?ignited", 3)
show("polyurethane foam", r"polyurethanefoam", 3)
show("no sprinklers", r"notequippedwithsprinklers|nosprinklersystem|unsprinklered", 3)
show("crowd crush", r"crowdcrush", 3)
show("exits", r"fourexits|exitswereavailable|therewerefourdoors", 3)
show("main entrance width", r"mainentrance.{0,90}(inches|width|door)", 3)
show("90 seconds", r"90safterignition|within90seconds|priorto90", 3)
show("smoke visible one minute", r"smokewasvisible|littlemorethanoneminute", 2)
show("flames through roof", r"flames.{0,60}roof", 2)
show("occupant load posted", r"postedoccupan|occupancylimitof", 3)
show("egress time simulation", r"egresssimulation|evacuationsimulation", 2)
