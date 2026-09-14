"""Rewrite runs/qc/itaewon_clip_verdicts.v001.json into the shape the gates actually read.

The reviewer's own draft used a list of {name, why} objects for `rejected`. Measured:
check_episode_inputs hashes that key and died with "unhashable type: dict", and
check_pool_frames looks for a `pool_frame_review` block that was not there at all. The
contract is `rejected` as {clip: why} and `pool_frame_review.accepted` as a list, bound to
the pool by `pool_id_sha256`.
"""
import hashlib
import json
import os

V = "runs/qc/itaewon_clip_verdicts.v001.json"
POOL = "remotion/public/itaewon/factory"

METHOD = (
    "Two rounds. Round 1 was the pool staged from one-word and long-phrase title queries; round 2 "
    "was 501 clips added on 2026-08-22 from 139 TWO-WORD queries, after measurement showed five-word "
    "queries returned nothing and one-word queries returned the wrong thing: 'alley' brought back a "
    "bowling alley and a tree avenue, and 'camera' brought back a man's face, from the phrase "
    "'towards the camera'. Every clip was rendered as 6 frames spread across its own length, packed "
    "8 clips to a sheet, and every sheet was opened and read tile by tile. Round 2 kept 169 of 501 "
    "(34 per cent); round 1 kept 88 of 325 (27 per cent). "
    "Rejection kinds, most frequent first: a readable face (stock actors at desks and on phones, and "
    "whole festival and beach shoots where every foreground face is legible); the wrong country (New "
    "York, London, Paris, Warsaw, Belgrade, Dhaka, Bangkok, Istanbul, Los Angeles, Miami, Las Vegas, "
    "and named landmarks); synthetic (3D police cars, CG moons, anime interiors, synthwave loops, "
    "data globes); nothing for the narration to mean (bokeh, smoke, lens flares, gradients, "
    "defocused traffic); unusable exposure (near-black frames, blown highlights, mid-clip exposure "
    "jumps); and a mid-clip break, where a compilation reel changes shot inside one file. "
    "TWO NORTH KOREAN FLAGS reached the pool and were rejected by eye. Nothing mechanical could "
    "catch them: the shelf labels both 'korea flag' and this episode had no forbidden term for the "
    "wrong Korea. "
    "THREE CLIPS ARE ACCEPTED WITH A CONDITION and must not be cut whole. AR-27856: frames 1 and 3 "
    "are near-black, use the lit middle. AR-pexels_15201563: the tail cuts to a curtain, trim it. "
    "AR-v_24603: the densest crowd image in the pool, but one mid-clip frame carries a readable "
    "face, so use only the blurred passages."
)

MECHANICAL = (
    "33 clips left the pool by rule rather than by eye, before review: 20 vertical or squarer than "
    "1.30:1 (stage_footage_by_title had no shape filter when round 1 was staged, and a 16:9 film can "
    "only pillarbox them), and 13 whose titles carry the pixabay ambience-loop vocabulary -- "
    "wallpaper, seamless loop, rain sounds, fireplace. block_ai_generated_shelf_clips flags 793 "
    "shelf clips whose TITLE says 'ai generated', and zero of those reached this pool, so that "
    "defence works. The loop category is the hole beside it: those files are CG and their titles "
    "never say so."
)


def main() -> int:
    d = json.load(open(V, encoding="utf-8"))
    pool = sorted(os.listdir(POOL))
    acc = sorted(set(d["accepted"]))
    raw = d["rejected"]
    rej = {r["name"]: r["why"] for r in raw} if isinstance(raw, list) else dict(raw)
    reviewed = sorted(set(acc) | set(rej))
    out = {
        "schema_version": "itaewon_clip_verdicts.v1",
        "slug": "itaewon",
        "reviewed_at": "2026-08-23",
        "reviewer": ("EP74 thread (Claude Opus 5, Claude Code) -- 104 dense contact sheets, "
                     "6 frames per clip, read by the reviewer"),
        "review_method": METHOD,
        "pool_size": len(pool),
        "accepted_count": len(acc),
        "rejected_count": len(rej),
        "reviewed_sheets": ["runs/qc/pool_frames/itaewon/dense/ -- 63 sheets round 2, 41 sheets round 1"],
        "rejected": rej,
        "accepted_notes": d.get("accepted_notes", {}),
        "pool_frame_review": {
            "reviewer": "EP74 thread (Claude Opus 5, Claude Code)",
            "reviewed_at": "2026-08-23",
            "pool_id_sha256": hashlib.sha256("\n".join(pool).encode()).hexdigest(),
            "reviewed_clips": reviewed,
            "accepted": acc,
        },
        "_mechanical_removals": MECHANICAL,
        "_near_duplicate_note": d.get("_near_duplicate_note", ""),
    }
    json.dump(out, open(V, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"accepted {len(acc)} / rejected {len(rej)} / reviewed {len(reviewed)} / pool {len(pool)}")
    missing = [c for c in pool if c not in reviewed]
    print("pool clips with no verdict:", len(missing), missing[:3])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
