#!/usr/bin/env python3
"""Stage EP39 factory clips that passed frame-by-frame visual review.

The ordinary EP39 factory directory currently also contains another thread's
placeholder clips.  This script never removes or overwrites those files.  The
reviewed production set is isolated under factory/selected and the episode QC
record names exactly what was seen in the extracted representative frame.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from factory_themes import theme_of  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SHELF = Path("H:/pd-media/assets")
GLOBAL_MANIFEST = ROOT / "assets" / "asset_manifest.v001.json"
DEST = ROOT / "remotion/public/frazier/factory/selected"
QC_OUT = ROOT / "episodes/PD-2026-039-frazier/05_visuals/factory_clip_qc.v001.json"
OVERLAY_DEST = ROOT / "remotion/public/frazier/overlay/selected"

REVIEWED_OVERLAYS = [
    "AF-LIGHT-1282__anamorphic_lens_flare_blue.mp4",
    "AF-LIGHT-0713__light_leak_overlay.mp4",
    "AF-LIGHT-2932__stage_spotlight_beams_haze.mp4",
    "AF-LIGHT-0977__sun_flare_warm.mp4",
    "AF-LIGHT-0421__light_streaks_motion.mp4",
    "AF-LIGHT-5743__match_strike_flame.mp4",
    "AF-LIGHT-5746__match_strike_flame.mp4",
    "AF-LIGHT-6932__fireworks_in_dark_sky.mp4",
    "AF-PART-0671__snow_falling_dark.mp4",
    "AF-PART-1532__bubbles_underwater_dark.mp4",
    "AF-PART-3581__ash_falling.mp4",
    "AF-PART-0368__sparks_slow_motion.mp4",
    "AF-PART-0548__bokeh_particles_dark.mp4",
    "AF-PART-1609__static_noise_particles.mp4",
    "AF-PART-0172__embers_floating.mp4",
    "AF-PART-2757__sand_blowing_desert.mp4",
    "AF-VFX-4048__dust_explosion_black.mp4",
    "AF-VFX-3790__fire_flames_black_background.mp4",
    "AF-VFX-0983__fire_flames_black_background.mp4",
    "AF-VFX-4881__colored_powder_burst.mp4",
    "AF-VFX-4110__electric_spark.mp4",
    "AF-VFX-2666__tear_gas_smoke_cloud.mp4",
    "AF-LOOP-0186__looping_light_rays.mp4",
    "AF-LOOP-0390__looping_gradient_navy.mp4",
    "AF-LOOP-0414__data_stream_loop.mp4",
    "AF-LOOP-0254__abstract_network_nodes_loop.mp4",
    "AF-LOOP-0152__looping_gradient_navy.mp4",
    "AF-LOOP-0054__particle_loop_dark.mp4",
    "AF-LOOP-0398__looping_light_rays.mp4",
    "AF-LOOP-0129__looping_particles_blue.mp4",
    "AF-LOOP-0015__abstract_loop_dark.mp4",
    "AF-LOOP-0012__abstract_loop_dark.mp4",
]

# basename, observed representative-frame content, scene code
REVIEWED = [
    ("AF-BG-10145__old_library_archive.mp4", "hands browsing rows of wooden archive card drawers", "S33"),
    ("AF-BG-11129__city_rooftop_dusk.mp4", "top-down daylight aerial of a dense civic building complex", "S40"),
    ("AF-BG-1291__documents_on_desk.mp4", "blue-lit monitoring room with multiple computer screens and empty chairs", "S50"),
    ("AF-BG-14768__police_station_at_night.mp4", "two uniformed officers standing beside a marked patrol car at night", "S11"),
    ("AF-BG-14911__evidence_locker_shelves.mp4", "green matrix-like vertical data lights on a dark background", "S50"),
    ("AF-BG-15010__crime_scene_tape_night.mp4", "uniformed officers inspecting a person beside a patrol car at night", "S10"),
    ("AF-BG-16356__capitol_dome_dusk.mp4", "aerial view of a domed state capitol building under clouds", "S40"),
    ("AF-BG-16375__capitol_dome_dusk.mp4", "straight-down aerial of a domed civic building", "S40"),
    ("AF-BG-20265__wax_seal_on_document.mp4", "hands presenting a signed contract across an office desk", "S42"),
    ("AF-BG-21351__train_platform_night.mp4", "light-rail train stopped at a city platform", "S07"),
    ("AF-BG-28651__rain_on_city_street_neon.mp4", "rainy city street at night with wet neon reflections and pedestrians", "S07"),
    ("AF-BG-30347__newspaper_macro.mp4", "macro view of turning printed book or newspaper pages", "S35"),
    ("AF-BG-30500__highway_night_long_exposure.mp4", "night highway traffic through dark hills", "S43"),
    ("AF-BG-30585__suburban_house_exterior_night.mp4", "suburban house exterior glowing at blue hour", "S04"),
    ("AF-BG-31115__bank_building_columns.mp4", "close view of monumental stone columns", "S31"),
    ("AF-BG-32239__jail_cell_bars.mp4", "soft-focus couple seated in a daylight diner or cafe", "S06"),
    ("AF-BG-3288__courthouse_steps.mp4", "civic building facade framed by an American flag", "S31"),
    ("AF-BG-32984__cell_tower_silhouette.mp4", "communications tower silhouetted against sunset", "S50"),
    ("AF-BG-33137__rural_road_america.mp4", "steep city street lined with buildings", "S43"),
    ("AF-BG-33699__old_library_archive.mp4", "rows of books on a library shelf", "S33"),
    ("AF-BG-33921__vintage_typewriter.mp4", "close-up of a mechanical typewriter", "S34"),
    ("AF-BG-37075__burning_paper_documents.mp4", "isolated flames against a black background", "S37"),
    ("AF-BG-37538__train_platform_night.mp4", "empty train carriage glowing at sunset", "S07"),
    ("AF-BG-37893__white_picket_fence.mp4", "snow-covered residential fence and yard", "S04"),
    ("AF-BG-38181__white_house_exterior.mp4", "weathered house entrance partly hidden by a tree", "S46"),
    ("AF-BG-3913__law_library_books.mp4", "person reading among tall library shelves", "S33"),
    ("AF-BG-41065__city_bridge_night_long_exposure.mp4", "illuminated bridge and city skyline at night", "S43"),
    ("AF-BG-4522__documents_on_desk.mp4", "hands writing notes on open paperwork", "S42"),
    ("AF-BG-4968__police_car_lights_night.mp4", "vintage patrol car driving through smoke at night", "S10"),
    ("AF-BG-6607__supreme_court_building.mp4", "large neoclassical courthouse exterior in daylight", "S48"),
    ("AF-BG-39983__ambulance_lights_at_night.mp4", "emergency vehicle and responders on a city street at night", "S10"),
    ("AF-BG-30798__police_car_lights_night.mp4", "marked patrol car moving through a dark street with warning lights", "S10"),
    ("AF-BG-14917__evidence_locker_shelves.mp4", "rows of green digital symbols receding into darkness", "S50"),
    ("AF-BG-15019__crime_scene_tape_night.mp4", "close-up of a spinning reel-to-reel recorder", "S35"),
    ("AF-BG-39980__ambulance_lights_at_night.mp4", "ambulance and responders on a wet city street at night", "S10"),
    ("AF-BG-1903__police_car_lights_night.mp4", "close-up of a patrol-car red and blue lightbar", "S10"),
    ("AF-BG-15024__crime_scene_tape_night.mp4", "front view of a vintage reel-to-reel tape machine", "S35"),
    ("AF-BG-23694__case_files_stack_desk.mp4", "minimal white desk with a wire tray and blank papers", "S34"),
    ("AF-BG-4898__prison_corridor.mp4", "empty symmetrical corridor lined with purple and blue lights", "S12"),
    ("AF-BG-36373__evidence_locker_shelves.mp4", "hands sorting a thick stack of paper files", "S33"),
    ("AF-BG-14772__police_station_at_night.mp4", "police vehicles with warning lights outside at night", "S11"),
    ("AF-BG-26325__ambulance_lights_at_night.mp4", "emergency vehicle driving on an empty city boulevard at night", "S43"),
    ("AF-BG-39985__ambulance_lights_at_night.mp4", "top-down night aerial of emergency vehicles at an incident", "S10"),
    ("AF-BG-14900__evidence_locker_shelves.mp4", "misty empty institutional locker room", "S12"),
    ("AF-BG-4962__police_car_lights_night.mp4", "police vehicles blocking a rainy street at night", "S10"),
    ("AF-BG-20415__evidence_locker_shelves.mp4", "archivist pulling folders from compact storage shelves", "S33"),
    ("AF-BG-14908__evidence_locker_shelves.mp4", "red-and-gray institutional locker doors with a distant person", "S12"),
    ("AF-BG-38402__case_files_stack_desk.mp4", "investigator seen from behind studying a wall of case material", "S36"),
    ("AF-BG-15020__crime_scene_tape_night.mp4", "vintage reel-to-reel tape recorder in warm low light", "S35"),
    ("AF-BG-4961__police_car_lights_night.mp4", "two police cruisers with warning lights on a dark road", "S10"),
    ("AF-BG-29936__government_building_exterior.mp4", "tall stone civic building seen through bare tree branches", "S31"),
    ("AF-BG-16365__capitol_dome_dusk.mp4", "daylight city skyline with a government tower near the river", "S40"),
    ("AF-BG-29944__government_building_exterior.mp4", "high aerial of a broad government district and avenue", "S40"),
    ("AF-BG-10029__balance_scale_brass.mp4", "hand writing at a legal desk beside a wooden gavel", "S32"),
    ("AF-BG-10030__balance_scale_brass.mp4", "graphic scale balancing a human brain and a computer chip", "S41"),
    ("AF-BG-37214__capitol_dome_dusk.mp4", "domed capitol building beyond a wide green lawn", "S40"),
    ("AF-BG-6606__supreme_court_building.mp4", "white neoclassical government building with tall columns", "S48"),
    ("AF-BG-0597__law_library_books.mp4", "person reading a book in front of full library shelves", "S33"),
    ("AF-BG-37219__capitol_dome_dusk.mp4", "domed state capitol at the end of an empty avenue", "S40"),
    ("AF-BG-16357__capitol_dome_dusk.mp4", "aerial view circling a domed state capitol", "S40"),
    ("AF-BG-0599__law_library_books.mp4", "seated reader in a narrow book-lined library aisle", "S33"),
    ("AF-BG-3914__law_library_books.mp4", "person reading at a table surrounded by library shelves", "S33"),
    ("AF-BG-6287__judge_gavel_wooden.mp4", "small Lady Justice statue on a legal desk", "S41"),
    ("AF-BG-10024__balance_scale_brass.mp4", "digital golden scales against a star-filled background", "S41"),
    ("AF-BG-37218__capitol_dome_dusk.mp4", "aerial of a civic government building at dusk", "S40"),
    ("AF-BG-3357__judge_gavel_wooden.mp4", "white classical columns in shallow focus", "S31"),
    ("AF-BG-3356__judge_gavel_wooden.mp4", "attorneys reviewing papers beside a gavel with faces cropped", "S36"),
    ("AF-BG-0592__law_library_books.mp4", "close view of worn leather-bound legal books", "S33"),
    ("AF-BG-3289__courthouse_steps.mp4", "person seen from behind walking up courthouse steps", "S31"),
    ("AF-BG-37228__capitol_dome_dusk.mp4", "ornate white domed ceiling inside a civic building", "S40"),
    ("AF-BG-33911__vintage_typewriter.mp4", "mechanical typewriter resting on an outdoor table", "S34"),
    ("AF-BG-49835__person_signing_document_hand.mp4", "hand signing a dense printed form", "S42"),
    ("AF-BG-4523__documents_on_desk.mp4", "person viewed from above reading paperwork with face hidden", "S42"),
    ("AF-BG-49829__person_signing_document_hand.mp4", "close-up of a hand writing on white paper", "S42"),
    ("AF-BG-10479__vintage_typewriter.mp4", "close-up of typewriter keys and paper platen", "S34"),
    ("AF-BG-16106__burning_paper_documents.mp4", "flame licking upward against a black background", "S37"),
    ("AF-BG-10485__vintage_typewriter.mp4", "green vintage computer terminal in a dark room", "S50"),
    ("AF-BG-10229__stacked_legal_documents.mp4", "wooden gavel resting on a courtroom table", "S36"),
    ("AF-BG-10329__newspaper_printing_press.mp4", "industrial press moving a wide roll of paper", "S35"),
    ("AF-BG-15146__magnifying_glass_on_document.mp4", "close-up of a vintage reel-to-reel audio deck", "S35"),
    ("AF-BG-10320__newspaper_printing_press.mp4", "sheet-fed printing press moving stacks of paper", "S35"),
    ("AF-BG-10331__newspaper_printing_press.mp4", "industrial press moving blank paper through rollers", "S35"),
    ("AF-BG-33700__old_library_archive.mp4", "blue-lit archive binders beneath a translucent globe graphic", "S33"),
    ("AF-BG-1364__newspaper_macro.mp4", "hands holding an open newspaper with the reader's face excluded", "S35"),
    ("AF-BG-8249__contract_paperwork_signing.mp4", "contract and fountain pen beside a wooden gavel", "S42"),
    ("AF-BG-57506__airport_runway_at_night.mp4", "airport control tower and terminal at blue hour", "S43"),
    ("AF-BG-3773__office_interior_dark.mp4", "modern empty office table surrounded by plants", "S11"),
    ("AF-BG-7605__city_traffic_night_long_exposure.mp4", "urban highway seen from above at night", "S43"),
    ("AF-BG-30503__highway_night_long_exposure.mp4", "highway light trails cutting through darkness", "S43"),
    ("AF-BG-57253__subway_train_motion_blur.mp4", "commuter train moving through a daylight rail corridor", "S07"),
    ("AF-BG-11128__city_rooftop_dusk.mp4", "elevated highway winding through a city skyline at sunset", "S43"),
    ("AF-BG-62431__drone_flying_at_dusk.mp4", "city river and long bridge under a fading sunset", "S43"),
    ("AF-BG-7598__city_traffic_night_long_exposure.mp4", "busy city boulevard filled with traffic at night", "S43"),
    ("AF-BG-57241__subway_train_motion_blur.mp4", "empty underground rail tunnel and platform in monochrome", "S07"),
    ("AF-BG-21324__train_platform_night.mp4", "train moving past a dim station platform at night", "S07"),
    ("AF-BG-12009__binary_code_screen_green.mp4", "blue binary-code pattern moving across a dark screen", "S50"),
    ("AF-BG-4309__data_center.mp4", "business analyst seen from behind reviewing a large data dashboard", "S50"),
    ("AF-BG-27679__vintage_tv_static.mp4", "vintage CRT television showing analog static", "S50"),
    ("AF-BG-3428__surveillance_camera_city.mp4", "fisheye surveillance-camera view of a building interior", "S50"),
    ("AF-BG-34641__binary_code_screen_green.mp4", "black-and-white streams of code and circuit graphics", "S50"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def act_for(scene_code: str) -> int:
    n = int(scene_code[1:])
    if n <= 3:
        return 0
    if n <= 15:
        return 1
    if n <= 30:
        return 2
    if n <= 42:
        return 3
    return 4


def main() -> int:
    if len(REVIEWED) != 100 or len({x[0] for x in REVIEWED}) != 100:
        raise AssertionError("reviewed factory selection must contain 100 unique files")
    manifest = json.loads(GLOBAL_MANIFEST.read_text(encoding="utf-8"))["assets"]
    by_name = {Path(str(x["path"])).name: x for x in manifest}
    DEST.mkdir(parents=True, exist_ok=True)
    copied = 0
    clips = []
    for basename, saw, scene_code in REVIEWED:
        item = by_name.get(basename)
        if item is None:
            raise FileNotFoundError(f"not in global asset manifest: {basename}")
        src = SHELF / item["path"]
        dst = DEST / basename
        if not src.is_file():
            raise FileNotFoundError(src)
        if dst.exists():
            if sha256(src) != sha256(dst):
                raise RuntimeError(f"refusing to overwrite different existing file: {dst}")
        else:
            shutil.copy2(src, dst)
            copied += 1
        clips.append({
            "file": basename,
            "filename": basename,
            "public_path": f"frazier/factory/selected/{basename}",
            "saw": saw,
            "scene_code": scene_code,
            "act": act_for(scene_code),
            "theme": theme_of(item.get("subtype", ""), item.get("type")),
            "reviewed": True,
            "on_theme": True,
        })

    QC_OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "episode_id": "PD-2026-039-frazier",
        "reviewed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "reviewer": "codex-thread-A",
        "scope": "reviewed production clips under remotion/public/frazier/factory/selected",
        "clips": clips,
    }
    QC_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if len(REVIEWED_OVERLAYS) != 32 or len(set(REVIEWED_OVERLAYS)) != 32:
        raise AssertionError("reviewed overlay selection must contain 32 unique files")
    OVERLAY_DEST.mkdir(parents=True, exist_ok=True)
    overlay_copied = 0
    for basename in REVIEWED_OVERLAYS:
        item = by_name.get(basename)
        if item is None:
            raise FileNotFoundError(f"overlay not in global asset manifest: {basename}")
        src = SHELF / item["path"]
        dst = OVERLAY_DEST / basename
        if not src.is_file():
            raise FileNotFoundError(src)
        if dst.exists():
            if sha256(src) != sha256(dst):
                raise RuntimeError(f"refusing to overwrite different existing file: {dst}")
        else:
            shutil.copy2(src, dst)
            overlay_copied += 1
    print(f"reviewed={len(clips)} copied={copied} dest={DEST}")
    print(f"overlays={len(REVIEWED_OVERLAYS)} copied={overlay_copied} dest={OVERLAY_DEST}")
    print(f"wrote {QC_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
