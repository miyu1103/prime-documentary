# EP34 "rolin" — FIGURE #21 SignSwapMorph  (L2 EEVEE hero, super-heavy tier)
#
# Bespoke topic geometry: a 3D agency sign/plate whose EMBLEM FACE MORPHS from
# one generic agency plate to another to a third (abstract extruded emblem
# blocks — NO readable text, NO "TIP", unbranded), while a small 3D odometer
# counter (rotating notched drums + a rising accumulation bar) ticks up beside
# it. The morph (blocks physically extrude / retract / reconfigure) and the
# counter (drums spin, bar rises) are the MAIN 3D motion — not a camera or a
# light sweep. Slow parallax camera. EEVEE bloom (Glare).
#
# Base: remotion/prototypes/motion3d/blender/bpp_eevee.py  (structure copied
# verbatim: engine pick, world, helpers, area lights + softboxes, DOF camera,
# setup_bloom, PNG-sequence render block). Numbers swapped for this subject.
#
# ---- argv contract (identical to bpp_eevee.py / bpp_cycles.py) --------------
#   blender -b -P aircash_signswap.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
#   FS == FE  -> single test still  -> <OUT>_test.png
#   FS <  FE  -> PNG sequence       -> <OUT>/f_0001.png ...   (60fps timeline)
# Blender 5.x has NO in-app video output: PNG sequence only; encode separately.
#
# DETERMINISTIC: every motion is frame-keyframed (scene.frame_set implied by
# keyframe_insert(frame=...)); the only randomness (tick-cube phase jitter) is
# seeded with random.seed(1234). No time-based randomness, no drivers.
#
# Test render frame 1 (4K, TAA 128):
#   blender -b -P remotion/src/blender/aircash_signswap.py -- out/hero_signswap 3840 2160 1 1 128

import bpy, sys, math, random
from mathutils import Vector

random.seed(1234)  # deterministic: fixed seed for all pseudo-random offsets

# ---- args: OUT RX RY FS FE SAMPLES -----------------------------------------
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 3840)), int(A(2, 2160))       # super-heavy: 4K default
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 128))                          # TAA 96-192 per §0-bis (#21)
ACC = (0.10, 0.42, 1.0)                           # accent blue ~#4ea1ff
ACC_HI = (0.35, 0.70, 1.0)                        # bright accent
ACC_B = (1.0, 0.62, 0.22)                         # secondary warm accent (drums)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
coll = scene.collection

# ---- engine (EEVEE Next / EEVEE) -------------------------------------------
engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
for cand in ['BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE']:
    if cand in engines:
        scene.render.engine = cand
        break
print('ENGINE =', scene.render.engine, '| available =', engines)

scene.render.resolution_x = RX
scene.render.resolution_y = RY
scene.render.film_transparent = False
scene.render.fps = 60                             # 60fps intent (§0 fps uplift)
scene.frame_start, scene.frame_end = FS, FE

# motion blur (EEVEE Next): shutter 0.5 per hard rule; harmless if unsupported
for attr, val in [('use_motion_blur', True), ('motion_blur_shutter', 0.5),
                  ('motion_blur_position', 'CENTER')]:
    try: setattr(scene.render, attr, val)
    except Exception as e: print('skip render.', attr, e)

ee = scene.eevee
for a, v in [('taa_render_samples', SAMPLES), ('use_raytracing', True),
             ('use_ssr', True), ('use_gtao', True), ('use_shadows', True)]:
    if hasattr(ee, a):
        try: setattr(ee, a, v)
        except Exception as e: print('skip eevee.', a, e)
if hasattr(ee, 'ray_tracing_options'):
    try: ee.ray_tracing_options.use_denoise = True
    except Exception: pass
# EEVEE Next also carries its own motion-blur toggle on scene.eevee in some builds
for a, v in [('use_motion_blur', True), ('motion_blur_shutter', 0.5)]:
    if hasattr(ee, a):
        try: setattr(ee, a, v)
        except Exception: pass

# ---- world: dark blue gradient (reflections). LUMA: raise strength here if
# the AgX composite reads dark (median YAVG must stay >= 48). ----------------
world = bpy.data.worlds.new('W'); scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
bg.inputs[0].default_value = (0.010, 0.016, 0.032, 1)
bg.inputs[1].default_value = 0.7                  # LUMA lever: world ambient

# ---- helpers (verbatim shape from bpp_eevee.py) ----------------------------
def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree.nodes.get('Principled BSDF')

def set_in(b, n, v):
    if n in b.inputs:
        b.inputs[n].default_value = v; return True
    return False

def emissive(b, color, strength):
    if not set_in(b, 'Emission Color', (*color, 1)):
        set_in(b, 'Emission', (*color, 1))
    set_in(b, 'Emission Strength', strength)

def emis_input(b):
    return b.inputs['Emission Strength'] if 'Emission Strength' in b.inputs else None

# ============================================================================
#  SUBJECT GEOMETRY (bespoke — built in code, NOT the gem showcase mesh)
# ============================================================================
# Layout (world): sign faces the camera (camera on -Y looking +Y). Tiles
# extrude toward camera in -Y. Emblem grid is 7 cols x 9 rows of extruded
# tiles on the sign face; a rising accumulation bar sits to the left and a
# 4-drum odometer counter sits to the right.

SIGN_CX, SIGN_CZ = 0.0, 1.72                       # emblem grid center
GX, GY = 7, 9                                       # cols, rows
STEP = 0.235                                         # tile pitch
FACE_Y = 0.0                                         # sign face plane (y)
OFF_Y = FACE_Y                                       # tile "off": flush
ON_Y = FACE_Y - 0.11                                 # tile "on": extruded toward cam
OFF_EMIS, ON_EMIS = 0.30, 6.0                        # emission strength off/on

# ---- three abstract agency emblems (9 rows x 7 cols). '#'=raised+glowing.
# Abstract shapes only (shield / federal chevrons / badge-star) — no glyphs,
# no readable text, no logo. They represent one agency plate morphing to the
# next (seizing authority handed off), per spec #21.
EMBLEM_A = [   # shield
    "..###..",
    ".#####.",
    "#######",
    "#######",
    "#######",
    "#.###.#",
    ".#####.",
    "..###..",
    "...#...",
]
EMBLEM_B = [   # federal chevrons / arrows
    "#.....#",
    "##...##",
    "###.###",
    "#######",
    ".#####.",
    "##...##",
    "###.###",
    "#######",
    ".#####.",
]
EMBLEM_C = [   # badge / star
    "...#...",
    "...#...",
    ".#####.",
    "#######",
    ".#####.",
    "..#.#..",
    ".##.##.",
    "##...##",
    "#.....#",
]
def on_at(pattern, c, r):
    return pattern[r][c] == '#'

# ---- sign backing plate (dark brushed metal, slightly emissive to lift luma)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(SIGN_CX, FACE_Y + 0.09, SIGN_CZ))
plate = bpy.context.object; plate.name = 'signPlate'
plate.scale = ((GX + 1.2) * STEP / 2, 0.06, (GY + 1.0) * STEP / 2)
bev = plate.modifiers.new('bev', 'BEVEL'); bev.width = 0.03; bev.segments = 3
pm, pb = new_mat('plate')
set_in(pb, 'Base Color', (0.045, 0.06, 0.10, 1))
set_in(pb, 'Metallic', 0.85)
set_in(pb, 'Roughness', 0.34)
emissive(pb, ACC, 0.35)                              # LUMA lever: plate glow
plate.data.materials.append(pm)

# ---- sign post / stand -----------------------------------------------------
bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=SIGN_CZ - (GY * STEP / 2),
                                    location=(SIGN_CX, FACE_Y + 0.09,
                                              (SIGN_CZ - (GY * STEP / 2)) / 2),
                                    vertices=24)
post = bpy.context.object; post.name = 'signPost'
pom, pob = new_mat('post')
set_in(pob, 'Base Color', (0.05, 0.06, 0.09, 1)); set_in(pob, 'Metallic', 0.9); set_in(pob, 'Roughness', 0.25)
post.data.materials.append(pom)

# ---- emblem tiles (each its own emissive material so we can morph per tile) -
tiles = []   # list of (obj, bsdf, aOn, bOn, cOn)
DIAG_MAX = (GX - 1) + (GY - 1)
for r in range(GY):
    for c in range(GX):
        x = SIGN_CX + (c - (GX - 1) / 2) * STEP
        z = SIGN_CZ + ((GY - 1) / 2 - r) * STEP
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, OFF_Y, z))
        t = bpy.context.object; t.name = f'tile_{r}_{c}'
        t.scale = (STEP * 0.42, 0.05, STEP * 0.42)
        tb = t.modifiers.new('b', 'BEVEL'); tb.width = 0.012; tb.segments = 2
        tm, tbsdf = new_mat(f'tileMat_{r}_{c}')
        set_in(tbsdf, 'Base Color', (0.02, 0.035, 0.07, 1))
        set_in(tbsdf, 'Metallic', 0.6); set_in(tbsdf, 'Roughness', 0.32)
        emissive(tbsdf, ACC_HI, OFF_EMIS)
        t.data.materials.append(tm)
        tiles.append((t, tbsdf,
                      on_at(EMBLEM_A, c, r), on_at(EMBLEM_B, c, r), on_at(EMBLEM_C, c, r)))

def set_tile_state(entry, on, frame=None):
    """Set a tile to on/off (extrude + emission). Keyframe if frame given."""
    t, bsdf = entry[0], entry[1]
    t.location.y = ON_Y if on else OFF_Y
    es = emis_input(bsdf)
    if es is not None:
        es.default_value = ON_EMIS if on else OFF_EMIS
    if frame is not None:
        t.keyframe_insert('location', frame=frame)
        if es is not None:
            es.keyframe_insert('default_value', frame=frame)

# ============================================================================
#  ODOMETER COUNTER (rotating notched drums + rising accumulation bar)
# ============================================================================
DRUMS = 4
DRUM_R = 0.17
drum_x0 = 1.55
drum_step = 0.40
drum_empties = []          # (empty, turns) — turns keyframed over the range
drum_turns = [7.5, 2.6, 0.95, 0.42]   # rightmost fastest -> odometer feel

dm, db = new_mat('drum')
set_in(db, 'Base Color', (0.06, 0.07, 0.10, 1)); set_in(db, 'Metallic', 0.88); set_in(db, 'Roughness', 0.28)
tm2, tb2 = new_mat('tick'); emissive(tb2, ACC_B, 7.0); set_in(tb2, 'Base Color', (1, 1, 1, 1))

for k in range(DRUMS):
    x = drum_x0 + k * drum_step
    piv = bpy.data.objects.new(f'drumPiv_{k}', None)
    piv.location = (x, 0.0, SIGN_CZ)
    coll.objects.link(piv)
    # drum body: cylinder, axis laid along world X (faceted -> catches light)
    bpy.ops.mesh.primitive_cylinder_add(radius=DRUM_R, depth=0.30,
                                        location=(x, 0.0, SIGN_CZ), vertices=22)
    d = bpy.context.object; d.name = f'drum_{k}'
    d.rotation_euler = (0.0, math.radians(90), 0.0)   # axis -> world X
    d.data.materials.append(dm)
    d.parent = piv
    # emissive tick marks around circumference (in Y-Z plane; axis = X)
    nticks = 12
    jitter = (random.random() - 0.5) * 0.05           # seeded, deterministic
    for i in range(nticks):
        ang = i / nticks * math.tau + jitter
        ty = DRUM_R * math.cos(ang)
        tz = SIGN_CZ + DRUM_R * math.sin(ang)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, ty, tz))
        tk = bpy.context.object; tk.name = f'tick_{k}_{i}'
        tk.scale = (0.10, 0.018, 0.045)
        tk.rotation_euler = (ang, 0.0, 0.0)
        tk.data.materials.append(tm2)
        tk.parent = piv
    drum_empties.append((piv, drum_turns[k]))

# ---- rising accumulation bar (bottom-anchored via scaled empty) ------------
BAR_X, BAR_Z0, BAR_H = -1.72, 0.30, 1.85
bar_piv = bpy.data.objects.new('barPiv', None)
bar_piv.location = (BAR_X, 0.0, BAR_Z0)
coll.objects.link(bar_piv)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(BAR_X, 0.0, BAR_Z0 + BAR_H / 2))
bar = bpy.context.object; bar.name = 'countBar'
bar.scale = (0.16, 0.10, BAR_H / 2)
bm, bb = new_mat('barMat')
set_in(bb, 'Base Color', (*ACC_HI, 1)); emissive(bb, ACC_HI, 5.5)   # LUMA lever
bar.data.materials.append(bm)
bar.parent = bar_piv
# thin notch rings on the bar for readable "filling up" motion (static geo)
for i in range(6):
    zz = BAR_Z0 + 0.12 + i * (BAR_H - 0.2) / 6
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(BAR_X, -0.11, zz))
    nk = bpy.context.object; nk.name = f'barNotch_{i}'
    nk.scale = (0.20, 0.02, 0.012)
    nm, nb = new_mat(f'barNotch_{i}'); emissive(nb, ACC_B, 4.0); set_in(nb, 'Base Color', (1, 1, 1, 1))
    nk.data.materials.append(nm)

# ---- reflective floor ------------------------------------------------------
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0))
fl = bpy.context.object; fl.name = 'floor'
fm, fb = new_mat('floor')
set_in(fb, 'Base Color', (0.012, 0.018, 0.032, 1)); set_in(fb, 'Metallic', 0.9); set_in(fb, 'Roughness', 0.30)
fl.data.materials.append(fm)

# ---- lights (3-point area + off-camera softboxes). Energies are LUMA levers:
# raise key/fill/rim if the AgX composite reads dark. --------------------------
def area(name, loc, energy, color, size=6):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    d = Vector((SIGN_CX, 0, SIGN_CZ)) - Vector(loc)
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob
area('key',  (5, -5, 6), 2400, (1, 1, 1), 7)         # LUMA lever
area('fill', (-6, -3, 3), 1200, ACC_HI, 8)           # LUMA lever
area('rim',  (-2, 5, 5), 1700, (0.6, 0.8, 1.0), 6)   # LUMA lever

def softbox(loc, size, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object; m, b = new_mat('sb'); emissive(b, color, strength); o.data.materials.append(m)
    d = Vector((SIGN_CX, 0, SIGN_CZ)) - Vector(loc)
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
softbox((-8, -6, 4), 6, ACC_HI, 3.4)                 # LUMA lever
softbox((8, -6, 3), 6, (0.75, 0.88, 1.0), 2.6)       # LUMA lever
softbox((0, -10, 6), 7, (0.55, 0.72, 1.0), 2.0)      # LUMA lever

# ---- camera + DOF ----------------------------------------------------------
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam); scene.camera = cam
cd.lens = 52
cd.dof.use_dof = True
cd.dof.focus_object = plate
cd.dof.aperture_fstop = 2.6
TARGET = Vector((0.45, 0.0, SIGN_CZ - 0.05))
CAM_A = Vector((-0.45, -7.3, 1.70))                  # parallax start
CAM_B = Vector(( 1.05, -6.8, 1.98))                  # parallax end
def aim(cam_ob, loc):
    cam_ob.location = loc
    d = TARGET - Vector(loc)
    cam_ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
aim(cam, CAM_A)

# ============================================================================
#  ANIMATION (only if a real range). MAIN motion = emblem morph A->B->C +
#  odometer drums spinning + accumulation bar rising. Camera is slow parallax.
# ============================================================================
if FE > FS:
    D = float(FE - FS)
    def f_at(frac): return int(round(FS + frac * D))
    # phase frames
    p1 = f_at(0.20)   # morph1 start (hold A: FS..p1)
    p2 = f_at(0.42)   # morph1 end / hold B start
    p3 = f_at(0.60)   # morph2 start
    p4 = f_at(0.82)   # morph2 end / hold C start
    TL = max(4, int(round(0.05 * D)))   # per-tile transition length (frames)

    for entry in tiles:
        aOn, bOn, cOn = entry[2], entry[3], entry[4]
        # find this tile's staggered transition frames (diagonal wave)
        # (recompute grid coords from name)
        nm = entry[0].name.split('_'); r = int(nm[1]); c = int(nm[2])
        diag = c + r
        frac = diag / DIAG_MAX
        ft1 = int(round(p1 + frac * max(0, (p2 - p1 - TL))))
        ft2 = int(round(p3 + frac * max(0, (p4 - p3 - TL))))
        # A hold
        set_tile_state(entry, aOn, frame=FS)
        set_tile_state(entry, aOn, frame=ft1)
        # morph1 A->B
        set_tile_state(entry, bOn, frame=ft1 + TL)
        set_tile_state(entry, bOn, frame=p2)
        set_tile_state(entry, bOn, frame=p3)
        set_tile_state(entry, bOn, frame=ft2)
        # morph2 B->C
        set_tile_state(entry, cOn, frame=ft2 + TL)
        set_tile_state(entry, cOn, frame=p4)
        set_tile_state(entry, cOn, frame=FE)

    # odometer drums: continuous staggered rotation about X (their axis)
    for piv, turns in drum_empties:
        piv.rotation_euler = (0.0, 0.0, 0.0); piv.keyframe_insert('rotation_euler', frame=FS)
        piv.rotation_euler = (math.tau * turns, 0.0, 0.0); piv.keyframe_insert('rotation_euler', frame=FE)

    # accumulation bar rises (bottom-anchored scale on empty)
    bar_piv.scale = (1.0, 1.0, 0.06); bar_piv.keyframe_insert('scale', frame=FS)
    bar_piv.scale = (1.0, 1.0, 1.0);  bar_piv.keyframe_insert('scale', frame=FE)

    # slow parallax camera (re-aimed both ends so subject stays framed)
    aim(cam, CAM_A); cam.keyframe_insert('location', frame=FS); cam.keyframe_insert('rotation_euler', frame=FS)
    aim(cam, CAM_B); cam.keyframe_insert('location', frame=FE); cam.keyframe_insert('rotation_euler', frame=FE)
    aim(cam, CAM_A)  # leave scene at start pose
else:
    # single test still: show emblem A statically
    for entry in tiles:
        set_tile_state(entry, entry[2])

# ---- compositor bloom (Glare) — robust across Blender 4.x/5.x --------------
def setup_bloom(scene):
    nt = None
    try:
        scene.use_nodes = True; nt = scene.node_tree
    except Exception:
        nt = None
    if nt is None and hasattr(scene, 'compositing_node_group'):
        ng = bpy.data.node_groups.new('comp', 'CompositorNodeTree'); scene.compositing_node_group = ng; nt = ng
    if nt is None:
        print('BLOOM: no compositor API, skipping'); return
    for n in list(nt.nodes): nt.nodes.remove(n)
    rl = nt.nodes.new('CompositorNodeRLayers')
    gl = nt.nodes.new('CompositorNodeGlare')
    def sock(name, val):
        if name in gl.inputs:
            try: gl.inputs[name].default_value = val
            except Exception as e: print('sock fail', name, e)
    if not sock('Type', 'Bloom'):
        sock('Type', 'Fog Glow')
    sock('Quality', 'High'); sock('Highlights Threshold', 0.8)
    sock('Highlights Smoothness', 0.3); sock('Strength', 1.0); sock('Size', 0.8)
    for attr, val in [('glare_type', 'FOG_GLOW')]:
        try: setattr(gl, attr, val)
        except Exception: pass
    out = None
    try: out = nt.nodes.new('CompositorNodeComposite')
    except Exception: pass
    nt.links.new(rl.outputs['Image'], gl.inputs['Image'])
    if out is not None:
        nt.links.new(gl.outputs['Image'], out.inputs['Image'])
    else:
        go = nt.nodes.new('NodeGroupOutput')
        nt.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
        nt.links.new(gl.outputs['Image'], go.inputs[0])
    print('BLOOM: ok')

setup_bloom(scene)

# ---- render (PNG sequence only — Blender 5.x has no in-app video output) ----
import os
scene.render.image_settings.file_format = 'PNG'
if FE == FS:
    scene.render.filepath = OUT + '_test.png'
    bpy.ops.render.render(write_still=True)
    print('WROTE', scene.render.filepath)
else:
    os.makedirs(OUT, exist_ok=True)
    scene.render.filepath = OUT + '/f_'
    import os as _os
    for _f in range(FS, FE + 1):
        _fp = '%s/f_%04d' % (OUT, _f)
        if _os.path.exists(_fp + '.png'):
            continue                      # RESUME: skip frames already on disk (crash-tolerant)
        scene.frame_set(_f)
        scene.render.filepath = _fp
        bpy.ops.render.render(write_still=True)
    print('WROTE SEQ', OUT)
