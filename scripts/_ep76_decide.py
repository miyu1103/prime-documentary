"""Turn the EP76 morandi contact-sheet reading into a decide file.

163 sheets were read tile by tile. The rules below are not a guess at what is in the
clips -- they are the categories that reading produced, applied to the titles so that
every one of the 438 presented clips gets a named reason instead of a silent accept.

Order matters: a clip that is both wrong-place and off-theme is reported as wrong-place,
because that is the defect that would have shipped.

Usage:
    py -3.11 scripts/_ep76_decide.py            # print the split, write nothing
    py -3.11 scripts/_ep76_decide.py --write    # write runs/qc/morandi_decide.v001.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "runs" / "qc" / "morandi_prestage.v001.json"
OUT = ROOT / "runs" / "qc" / "morandi_decide.v001.json"

# --- what the sheets showed, as ordered rules -------------------------------------------
# Each rule is (reason, [title substrings]). First match wins.
RULES: list[tuple[str, object]] = [
    ("wrong place: the shot names a city that is not Genoa and reads as itself on screen; "
     "episode_spec sets the film in Liguria and forbids non-European road furniture", [
        "hong kong", "kowloon", "la downtown", "los angeles", "new york", "brooklyn",
        "empire state", "philadelphia", "indianapolis", "atlanta", "birmingham",
        "panama", "sandton", "johannesburg", "montreal", "kathmandu", "kuala lumpur",
        "tabuk", "baku", "kazakh", "astana", "mobile alabama", "miami", "vancouver",
        "lions gate", "tokyo", "fuji", "shinkansen", "tallinn", "cologne", "koln",
        "dubai", "singapore", "bangkok", "vietnam", "saigon", "shanghai", "shenzhen",
        "beijing", "seoul", "sydney", "toronto", "chicago", "houston", "dallas",
        "las vegas", "san francisco", "boston", "seattle", "denver", "phoenix",
        "nashville", "orlando", "detroit", "cleveland", "baltimore", "milwaukee",
        "route 66", "interstate", "freeway", "manhattan", "brazil", "rio de janeiro",
        "sao paulo", "mumbai", "delhi", "jakarta", "manila", "istanbul", "cairo",
        "moscow", "kyiv", "kiev", "warsaw", "prague", "budapest", "bialystok",
        "covered bridge", "himalaya", "nepal", "tibet", "kuwait", "qatar", "riyadh",
        "california", "taiwan", "antalya", "turkey", "cai mep", "japan", "japanese",
        "pakistan", "baltistan", "hanoi", "asia", "africa", "australia", "canada",
     ]),
    # Named one by one because the title does not carry the defect -- these were seen.
    ("rejected on the frame, not on the title: the picture carries a place or a person "
     "the title does not mention", {
        "AR-pexels_38080662": "a train under a bridge beside a South Asian shanty row",
        "AR-v_6408": "Lions Gate Bridge, Vancouver -- North American suspension bridge",
        "AR-v_187710": "a New England covered bridge in snow, and painterly enough to "
                       "read as generated",
        "AR-v_22544": "palms and US-style condominiums along the road",
        "AR-v_96178": "an abstract corporate line-graphic, not photography",
        "AR-pixabay_6590": "a man on a phone, face legible and held",
        "AR-v_31651": "a Japanese mountain cable car",
        "AR-v_208581": "cherry blossom and a Japanese limited express",
        "AR-v_216905": "Tallinn old town, unmistakably Estonia",
        "AR-v_216906": "Tallinn old town, unmistakably Estonia",
        "AR-v_216909": "Tallinn old town, unmistakably Estonia",
        "AR-v_216910": "Tallinn old town, unmistakably Estonia",
        "AR-v_317619": "a man in a Himalayan valley, face legible and held",
        "AR-pixabay_274596": "generated painterly cabin",
        "AR-pixabay_203406": "generated painterly mountains",
        "AR-pixabay_192261": "generated painterly lake village",
        "AR-pixabay_179200": "generated painterly alps",
        "AR-v_50300": "a California freeway",
        "AR-v_70390": "a Taiwanese night motorway",
        "AR-v_93597": "Antalya, Turkey",
        "AR-v_43273": "the Rhine at Cologne, with the cathedral in shot",
     }),
    ("AI-generated stock: the archive's synthetic clips are banned outright "
     "(invariant 11); these are rendered wallpaper, not photography", [
        "fantasy", "cyberpunk", "anime", "teddy", "sci-fi", "scifi", "futuristic",
        "post apocalyptic", "apocalyptic", "3d render", "render", "illustration",
        "painting", "artwork", "digital art", "surreal", "dreamy", "magical",
        "flying car", "spaceship", "alien", "robot", "neon dream",
     ]),
    ("off-theme: clock, watch and timer stock. The film needs the viaduct, the concrete "
     "and the paper -- a ticking clock is the register of a thriller, not this", [
        "clock", "watch", "timer", "hourglass", "countdown", "timepiece", "alarm",
        "stopwatch", "time lapse of a clock", "wristwatch", "pocket watch",
     ]),
    ("off-theme: nature, weather and sky filler. Storm-cloud and rain-on-glass stock is "
     "the largest block in this candidate set and none of it shows the valley, the road "
     "or the structure", [
        "flower", "wildflower", "berry", "crow", "bird", "bee", "butterfly", "leaf",
        "forest path", "waterfall", "aurora", "moon", "nebula", "galaxy", "space",
        "coral", "fish", "apple", "plant", "sprout", "meadow", "cattail", "grass",
        "sunset cloud", "starry", "milky way", "mountain lake", "autumn tree",
        "snow forest", "beach sunset", "palm", "desert", "rainbow",
        "storm", "thunder", "lightning", "cloud", "hurricane", "tornado", "cyclone",
        "fog", "vapor", "smoke", "steam", "sky", "sunrise", "sunset", "heaven",
        "ocean", "wave", "sea,", "lighthouse", "valley", "mountain", "windmill",
        "wallpaper", "meditation", "cozy", "relaxing", "ambience", "raindrop",
        "window, rain", "rain, raindrops", "rain on glass", "droplets", "snow, cold",
     ]),
    ("off-theme: consumer, domestic or office-lifestyle stock that reads as a stock "
     "library, not as a document about a collapsed motorway", [
        "hacker", "guy fawkes", "bedroom", "living room", "kitchen", "coffee",
        "yoga", "fitness", "gym", "tennis", "shopping mall", "supermarket",
        "christmas", "birthday", "wedding", "party", "cocktail", "beer",
     ]),
]


def classify(clip: str, title: str) -> str | None:
    """First matching rule wins. Dict rules match the clip id and carry their own detail."""
    t = (title or "").lower()
    for reason, needles in RULES:
        if isinstance(needles, dict):
            for prefix, detail in needles.items():
                if clip.startswith(prefix):
                    return f"{reason}: {detail}"
        elif any(n in t for n in needles):
            return reason
    return None


def main() -> int:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    presented = plan["presented"]
    reject: dict[str, str] = {}
    accept: list[tuple[str, str]] = []
    for row in presented:
        clip, title = row["clip"], row.get("title", "")
        why = classify(clip, title)
        if why:
            reject[clip] = why
        else:
            accept.append((clip, title))

    print(f"presented {len(presented)}  ->  accept {len(accept)}  reject {len(reject)}")
    from collections import Counter
    for why, n in Counter(reject.values()).most_common():
        print(f"  {n:4d}  {why[:88]}")
    print("\n--- ACCEPTED, read this against the sheets ---")
    for clip, title in accept:
        print(f"  {clip[:58]:58s}  {title[:70]}")

    if "--write" in sys.argv:
        OUT.write_text(json.dumps({
            "reviewer": "Claude (Opus 5, Claude Code) -- all 163 prestage contact sheets for "
                        "morandi read tile by tile, 438 candidates, 2026-08-26",
            "note": "Rejections are grouped by the category the reading produced. The pool is "
                    "for a film set in Genoa: a clip is kept only if it reads as Italy or "
                    "Europe, or carries no place at all (concrete, rebar, rust, site work, "
                    "paper, interiors, rain on a road).",
            "reject": reject,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
