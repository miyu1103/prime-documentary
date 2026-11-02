import bpy, sys, math, random, os

def _act_fcurves(action):
    """Blender 5.x removed Action.fcurves (slotted actions). Return an action's F-curves across
    versions so keyframe easing still works on 5.1 (was an AttributeError crash on sequence renders)."""
    if action is None:
        return []
    try:
        return list(action.fcurves)          # Blender <= 4.3
    except AttributeError:
        pass
    out = []
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for cbag in getattr(strip, "channelbags", []):
                out.extend(getattr(cbag, "fcurves", []))
    return out

from mathutils import Vector

# ============================================================================
# EP34 "rolin" (PD-2026-034) — HEROES #12-14  USForfeitureNumber
# L3 Cycles ceiling hero. Bespoke, topic-specific geometry:
#   a large 3D EXTRUDED currency figure ($209M / $3.2B / $68.8B) that DROPS
#   into place digit-by-digit, then a BURST of cash-bill particles scatters
#   outward on landing. Slow camera push tracks the digits. Glare Bloom +
#   off-camera softboxes.  (Built from bpp_cycles.py — do NOT reuse gem mesh.)
#
# ARGV CONTRACT (identical to bpp_cycles.py, plus one EXTRA figure arg):
#   blender -b -P aircash_usforfeiture.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES> [FIGURE]
#     OUT      output dir (PNG seq) or filename stem (single still)
#     RX RY    resolution (super-heavy hero = 3840 2160)
#     FS FE    frame range. FS==FE -> single test still. FS<FE -> PNG seq f_%04d.png
#     SAMPLES  cycles samples (super-heavy ceiling = 200)
#     FIGURE   (argv idx 6) the EXACT string to render, e.g. "$209M" "$3.2B" "$68.8B"
#              Digit meshes are built from this string verbatim. Numbers are NOT
#              invented — whatever is passed is rendered exactly.
#
# DETERMINISTIC: every motion is frame-keyframed on a 60fps timeline; the cash
# burst uses random.seed(1234) with fixed per-bill targets (no physics bake
# needed for this asset — manifest row #12-14 lists 物理シム = none).
# ============================================================================

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 3840)), int(A(2, 2160))
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 200))
FIGURE = A(6, '$209M')            # rendered EXACTLY as passed — do not invent numbers

random.seed(1234)                 # fixed seed: deterministic cash burst

# --- palette ---
ACC = (0.10, 0.42, 1.0)           # brand accent blue (floor/rim/softbox reflections)
ACC_HI = (0.35, 0.70, 1.0)
GOLD = (1.0, 0.80, 0.34)          # the money figure emits warm gold (reads bright under AgX)
GOLD_HI = (1.0, 0.90, 0.62)
BILL_A = (0.13, 0.42, 0.20)       # currency green (two unbranded variants, no text/logo)
BILL_B = (0.18, 0.52, 0.28)

FPS = 60                          # 60fps intent (frames derived from seconds below)
FLOOR_Z = -1.35                   # reflective floor height
sec = lambda s: int(round(s * FPS))

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
coll = scene.collection

# ---- CYCLES + GPU (OptiX -> CUDA -> HIP -> ONEAPI -> CPU) ----
scene.render.engine = 'CYCLES'
prefs = bpy.context.preferences.addons['cycles'].preferences
picked = 'CPU'
for dt in ['OPTIX', 'CUDA', 'HIP', 'ONEAPI']:
    try:
        prefs.compute_device_type = dt
        prefs.get_devices()
        if any(d.type != 'CPU' for d in prefs.devices):
            for d in prefs.devices:
                d.use = True
            scene.cycles.device = 'GPU'
            picked = dt
            break
    except Exception as e:
        print('gpu try', dt, e)
print('CYCLES device =', picked)
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
# caustics OFF on purpose (prototype note): glass/emission caustics stall some
# frames for minutes. The Glare bloom supplies the glow. Do not re-enable.
try:
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
except Exception:
    pass

scene.render.resolution_x = RX
scene.render.resolution_y = RY
scene.render.fps = FPS
scene.frame_start, scene.frame_end = FS, FE
scene.view_settings.view_transform = 'AgX'          # cinematic tonemap (sinks dark -> keep well-lit)

# ---- motion blur (Cycles): fast cash burst reads as streaks ----
scene.render.use_motion_blur = True
scene.render.motion_blur_shutter = 0.5
try:
    scene.cycles.rolling_shutter_type = 'NONE'
except Exception:
    pass

# ---- world: dark blue gradient (for metallic reflections) ----
world = bpy.data.worlds.new('W'); scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
bg.inputs[0].default_value = (0.012, 0.02, 0.04, 1)
bg.inputs[1].default_value = 0.55                    # LUMA: raise this if composite median < 48

# ---- material helpers ----
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

def kf(obj, path, frame):
    obj.keyframe_insert(path, frame=frame)

def set_interp(obj, path, index, interp='BEZIER', easing='EASE_OUT'):
    """Force an F-curve segment's interpolation/easing (deterministic easing)."""
    ad = obj.animation_data
    if not ad or not ad.action:
        return
    for fc in _act_fcurves(ad.action):
        if fc.data_path == path and fc.array_index == index:
            for kp in fc.keyframe_points:
                kp.interpolation = interp
                kp.easing = easing

# ============================================================================
# SUBJECT: extruded, beveled digit meshes built from FIGURE (bespoke geometry)
# ============================================================================
# Money figure material — dark metallic body with a warm gold emission so the
# number stays bright under AgX (LUMA: raise Emission Strength if median < 48).
mNum, bNum = new_mat('num')
set_in(bNum, 'Base Color', (0.16, 0.11, 0.03, 1))
set_in(bNum, 'Metallic', 0.9)
set_in(bNum, 'Roughness', 0.16)
if not set_in(bNum, 'Specular IOR Level', 0.6):
    set_in(bNum, 'Specular', 0.6)
set_in(bNum, 'Coat Weight', 0.3)
set_in(bNum, 'Coat Roughness', 0.08)
emissive(bNum, GOLD, 3.6)                            # LUMA lever #1

GAP = 0.12                                           # inter-glyph spacing
chars = []
cursor_x = 0.0
for idx, ch in enumerate(FIGURE):
    if ch == ' ':
        cursor_x += 0.45
        continue
    bpy.ops.object.text_add(location=(0, 0, 0))
    t = bpy.context.object
    t.name = 'glyph_%02d' % idx
    td = t.data
    td.body = ch
    td.align_x = 'LEFT'          # advance along +X
    td.align_y = 'CENTER'        # vertically centred on origin
    td.size = 1.0
    td.extrude = 0.18            # front-to-back thickness (becomes world -Y after rotate)
    td.bevel_depth = 0.02
    td.bevel_resolution = 2
    bpy.context.view_layer.update()
    w = t.dimensions.x           # glyph advance width (invariant under the X-rotation below)
    t.location = (cursor_x, 0.0, 0.0)
    t.rotation_euler = (math.pi / 2, 0.0, 0.0)   # stand upright, face -Y (toward camera)
    td.materials.append(mNum)
    chars.append(t)
    cursor_x += w + GAP

total_w = max(cursor_x - GAP, 0.001)
for t in chars:                  # recentre the whole figure on X (centre = origin)
    t.location.x -= total_w / 2.0

# focus / aim target at the figure centre
tgt = bpy.data.objects.new('numCenter', None)
tgt.location = (0, 0, 0)
coll.objects.link(tgt)

# ============================================================================
# CASH-BILL BURST — deterministic particle scatter (seeded, fully keyframed)
# ============================================================================
mBillA, bA = new_mat('billA'); set_in(bA, 'Base Color', (*BILL_A, 1)); set_in(bA, 'Roughness', 0.55); set_in(bA, 'Metallic', 0.0); emissive(bA, BILL_A, 0.6)
mBillB, bB = new_mat('billB'); set_in(bB, 'Base Color', (*BILL_B, 1)); set_in(bB, 'Roughness', 0.5); set_in(bB, 'Metallic', 0.0); emissive(bB, BILL_B, 0.7)

BURST_ORIGIN = Vector((0.0, 0.0, FLOOR_Z + 0.55))    # bills spawn at the figure base
NBILLS = 60
bills = []                                           # (obj, origin, peak, rest, spin)
for i in range(NBILLS):
    bpy.ops.mesh.primitive_cube_add(location=BURST_ORIGIN)
    b = bpy.context.object
    b.name = 'bill_%03d' % i
    b.scale = (0.26, 0.115, 0.006)                   # thin currency-note proportions (unbranded solid)
    b.data.materials.append(mBillA if (i % 2 == 0) else mBillB)
    # deterministic scatter targets
    ang = random.random() * math.tau
    r_peak = 1.4 + random.random() * 2.2
    z_peak = FLOOR_Z + 1.1 + random.random() * 2.1
    peak = Vector((math.cos(ang) * r_peak, (random.random() - 0.5) * 1.2, z_peak))
    r_rest = 1.2 + random.random() * 3.0
    a_rest = ang + (random.random() - 0.5) * 0.9
    rest = Vector((math.cos(a_rest) * r_rest,
                   (random.random() - 0.5) * 2.4 - 1.0,   # bias toward -Y (nearer camera floor)
                   FLOOR_Z + 0.012 + random.random() * 0.04))
    spin = (random.random() * math.tau, random.random() * math.tau, random.random() * math.tau)
    b.rotation_euler = (math.pi / 2 * random.random(), 0, random.random() * math.tau)  # settled-ish default
    bills.append((b, BURST_ORIGIN.copy(), peak, rest, spin))
    # default (still / no-anim) pose = settled scatter on the floor
    b.location = rest

# ============================================================================
# reflective metallic floor (manifest: Metallic 0.9 / Roughness 0.22)
# ============================================================================
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, FLOOR_Z))
fl = bpy.context.object
fm, fb = new_mat('floor')
set_in(fb, 'Base Color', (0.01, 0.015, 0.03, 1))
set_in(fb, 'Metallic', 0.9)
set_in(fb, 'Roughness', 0.22)
fl.data.materials.append(fm)

# ============================================================================
# lights: 3-point area (manifest key1600/fill800/rim1300) + off-cam softboxes
# ============================================================================
def area(name, loc, energy, color, size=6):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    d = Vector((0, 0, 0)) - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob
area('key',  (5, -4, 6), 1600, (1, 1, 1), 6)         # LUMA lever #2: raise key energy if dark
area('fill', (-6, -2, 2), 800, ACC_HI, 7)
area('rim',  (-2, 5, 4), 1300, (0.6, 0.8, 1.0), 5)

def softbox(loc, size, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object
    m, b = new_mat('sb'); emissive(b, color, strength); o.data.materials.append(m)
    d = Vector((0, 0, 0)) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
softbox((-8, -5, 3), 5, ACC_HI, 1.4)                 # manifest softbox strengths 1.4/1.1/0.8
softbox((8, -5, 2.5), 5, (0.75, 0.88, 1.0), 1.1)
softbox((0, -9, 5), 6, (0.55, 0.72, 1.0), 0.8)

# ============================================================================
# camera: slow push tracking the digits (55mm + DOF on the figure centre)
# ============================================================================
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam); scene.camera = cam
cam_start = Vector((0.5, -9.6, 0.9))
cam_end = Vector((0.3, -7.7, 0.6))
cam.location = cam_start
cd.lens = 55
cd.dof.use_dof = True
cd.dof.focus_object = tgt
cd.dof.aperture_fstop = 2.2
d = Vector((0, 0, 0)) - cam_start
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

# ============================================================================
# ANIMATION (only for a real range; a single still shows the composed rest pose)
# Main motion = digits DROP-land (staggered) + cash-bill BURST = real moving 3D.
# ============================================================================
if FE > FS:
    LAND0 = sec(0.23)            # first glyph lands at FS + 0.23s
    STAG = sec(0.11)             # per-glyph stagger
    DROP = sec(0.43)             # fall duration
    DROP_H = 6.5                 # start height above final rest

    # ---- glyphs drop in, staggered, with a bounce landing + squash ----
    last_land = FS
    for i, t in enumerate(chars):
        land = FS + LAND0 + i * STAG
        start = land - DROP
        last_land = max(last_land, land)
        fz = 0.0                                     # glyph final Z (centred)
        # location Z: high -> land
        t.location.z = fz + DROP_H; kf(t, 'location', start)
        t.location.z = fz;          kf(t, 'location', land)
        set_interp(t, 'location', 2, interp='BOUNCE', easing='EASE_OUT')
        # scale squash on impact then settle (punch)
        t.scale = (1, 1, 1);            kf(t, 'scale', start)
        t.scale = (1.14, 1.14, 0.82);   kf(t, 'scale', land)
        t.scale = (1, 1, 1);            kf(t, 'scale', land + sec(0.12))

    BURST = last_land + sec(0.06)                    # burst on the last digit's landing
    PEAK = BURST + sec(0.28)
    REST = BURST + sec(1.35)

    # ---- cash-bill burst: hidden -> pop at origin -> explode to peak -> settle ----
    for (b, origin, peak, rest, spin) in bills:
        b.scale = (0.0, 0.0, 0.0);  kf(b, 'scale', FS)
        b.scale = (0.0, 0.0, 0.0);  kf(b, 'scale', BURST - 1)
        b.scale = (0.26, 0.115, 0.006); kf(b, 'scale', BURST)
        b.location = origin;        kf(b, 'location', BURST)
        b.rotation_euler = (0, 0, 0); kf(b, 'rotation_euler', BURST)
        b.location = peak;          kf(b, 'location', PEAK)
        b.rotation_euler = spin;    kf(b, 'rotation_euler', PEAK)
        set_interp(b, 'location', 0); set_interp(b, 'location', 1); set_interp(b, 'location', 2)
        b.location = rest;          kf(b, 'location', REST)
        b.rotation_euler = (spin[0] + math.pi, spin[1], spin[2] + 0.6); kf(b, 'rotation_euler', REST)

    # ---- slow camera push across the whole clip (sustains motion under the beats) ----
    cam.location = cam_start; kf(cam, 'location', FS)
    cam.location = cam_end;   kf(cam, 'location', FE)
    set_interp(cam, 'location', 0); set_interp(cam, 'location', 1); set_interp(cam, 'location', 2)

# ============================================================================
# compositor Glare Bloom (Blender 5.x node-group + socket API — from bpp_cycles)
# ============================================================================
def setup_bloom(scene):
    nt = None
    try:
        scene.use_nodes = True; nt = scene.node_tree
    except Exception:
        nt = None
    if nt is None and hasattr(scene, 'compositing_node_group'):
        ng = bpy.data.node_groups.new('comp', 'CompositorNodeTree'); scene.compositing_node_group = ng; nt = ng
    if nt is None:
        return
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    rl = nt.nodes.new('CompositorNodeRLayers')
    gl = nt.nodes.new('CompositorNodeGlare')
    def sock(name, val):
        if name in gl.inputs:
            try: gl.inputs[name].default_value = val
            except Exception: pass
    sock('Type', 'Bloom'); sock('Quality', 'High'); sock('Highlights Threshold', 0.8)
    sock('Highlights Smoothness', 0.3); sock('Strength', 1.0); sock('Size', 0.8)
    for attr, val in [('glare_type', 'BLOOM')]:
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
setup_bloom(scene)

# ============================================================================
# render — PNG only (Blender 5.x has no in-app video output)
# ============================================================================
scene.render.image_settings.file_format = 'PNG'
if FE == FS:
    scene.render.filepath = OUT + '_cyc.png'
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
