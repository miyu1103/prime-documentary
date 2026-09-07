"""EP34 rolin — HERO #1 CashStack — L3 Cycles ceiling scene (SUPER-HEAVY tier).

Bespoke subject: banded currency bundles (rounded rectangular bill blocks each
wrapped by a paper-band strap) that STACK UP from the floor into a pile via
rigidbody physics (substeps 20 / solver 20 / restitution 0.05 — light contact
settle), then hold. Camera: 55mm dolly-in, DOF aperture_fstop 2.2, focus pull
onto the settled stack. Lighting: 3-point area + 3 off-camera softboxes
(1.4/1.1/0.8) + Glare Bloom (Strength 1.0 / Size 0.8). Seeded 30 additive dust
motes drift through the volume.

Follows remotion/prototypes/motion3d/blender/bpp_cycles.py (L3 look) and
bpp_physics.py (rigidbody + point_cache bake). Deterministic: seeded
random.seed(1234); all motion is frame-keyframed or physics-baked. No
real-person likeness, no readable text/logos, unbranded (invariant 11).

ARGV CONTRACT (identical to bpp_cycles.py):
    blender -b -P aircash_cashstack.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
    FS == FE -> single test still (<OUT>_test.png)
    FS <  FE -> PNG sequence <OUT>/f_0001.png ...  (Blender 5.x has no in-app
                video output; encode the PNG sequence separately with ffmpeg).

TEST (frame 1 smoke still):
    blender -b -P remotion/src/blender/aircash_cashstack.py -- out/hero_cashstack 3840 2160 1 1 200
FULL (12s @ 60fps -> 720 frames):
    blender -b -P remotion/src/blender/aircash_cashstack.py -- out/hero_cashstack 3840 2160 1 720 200
"""

import bpy, sys, math, os, random

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

# ---- args: OUT RX RY FS FE SAMPLES ----
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 3840)), int(A(2, 2160))     # super-heavy: 4K default
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 200))                       # L3 ceiling default
ACC = (0.10, 0.42, 1.0)                        # blue accent (rim/softbox)
ACC_HI = (0.35, 0.70, 1.0)

random.seed(1234)                              # deterministic — no time-based randomness

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
# caustics OFF on purpose (prototype note): avoids per-frame render explosions.
try:
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
except Exception:
    pass

scene.render.resolution_x = RX
scene.render.resolution_y = RY
scene.render.resolution_percentage = 100
scene.render.fps = 60                          # 60fps authoring (spec §0 uplift)
scene.frame_start, scene.frame_end = FS, FE
scene.view_settings.view_transform = 'AgX'     # cinematic tonemap

# ---- motion blur (Cycles, shutter 0.5, rolling shutter off) ----
scene.render.use_motion_blur = True
scene.render.motion_blur_shutter = 0.5
try:
    scene.cycles.rolling_shutter_type = 'NONE'
except Exception:
    pass

# ---- world: dark blue gradient (for reflections) ----
world = bpy.data.worlds.new('W'); scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
bg.inputs[0].default_value = (0.012, 0.02, 0.04, 1)
bg.inputs[1].default_value = 0.5               # LUMA: raise this if composite reads dark

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

# ---- rigidbody helper (bpp_physics.py pattern) ----
def rb(obj, kind, shape, mass=1.0, friction=0.5, restitution=0.05):
    bpy.context.view_layer.objects.active = obj
    for o in bpy.context.selected_objects:
        o.select_set(False)
    obj.select_set(True)
    bpy.ops.rigidbody.object_add()
    obj.rigid_body.type = kind
    obj.rigid_body.collision_shape = shape
    obj.rigid_body.mass = mass
    obj.rigid_body.friction = friction
    obj.rigid_body.restitution = restitution   # 0.05 = light contact settle (spec)
    if kind == 'ACTIVE':
        # damping so the pile settles and HOLDS rather than jittering
        obj.rigid_body.linear_damping = 0.25
        obj.rigid_body.angular_damping = 0.35
        obj.rigid_body.use_margin = True
        obj.rigid_body.collision_margin = 0.006

FLOOR_Z = -2.0

# ---- reflective metallic floor (passive rigidbody) ----
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, FLOOR_Z))
floor = bpy.context.object; floor.name = 'floor'
fm, fb = new_mat('floor')
set_in(fb, 'Base Color', (0.01, 0.015, 0.03, 1))
set_in(fb, 'Metallic', 0.9)
set_in(fb, 'Roughness', 0.22)
floor.data.materials.append(fm)
rb(floor, 'PASSIVE', 'BOX', friction=0.6)

# ---- bill-block + paper-band materials ----
# Bills: desaturated green paper, matte with a faint sheen. Kept light so it
# reads bright under AgX (LUMA: nudge Base Color / Roughness up if it sinks).
def bill_mat(i):
    m, b = new_mat('bills_%02d' % i)
    g = 0.20 + random.random() * 0.06          # seeded per-bundle variation
    set_in(b, 'Base Color', (0.14 + g * 0.5, 0.30 + g, 0.20 + g * 0.5, 1))
    set_in(b, 'Metallic', 0.0)
    set_in(b, 'Roughness', 0.55)
    if not set_in(b, 'Specular IOR Level', 0.4):
        set_in(b, 'Specular', 0.4)
    return m

# Paper strap: warm off-white, faint emission so bloom catches the bands.
band_mat, band_b = new_mat('band')
set_in(band_b, 'Base Color', (0.86, 0.80, 0.62, 1))
set_in(band_b, 'Roughness', 0.4)
emissive(band_b, (0.9, 0.82, 0.6), 0.35)       # subtle accent for Glare Bloom

# ---- bespoke banded currency bundle ----------------------------------------
# A bundle = a flattened rounded box (the stacked bills) wrapped by a thin
# proud strap across its girth (the paper band). The strap is parented to the
# block, so it rides the rigidbody-baked motion. Unbranded, no text (invariant 11).
BX, BY, BZ = 0.90, 0.42, 0.22                   # full dims of one bundle
bundles = []
N_BUNDLES = 16

def make_bundle(i, loc, rot):
    # bill block
    bpy.ops.mesh.primitive_cube_add(location=loc)
    blk = bpy.context.object
    blk.name = 'bundle_%02d' % i
    blk.scale = (BX / 2, BY / 2, BZ / 2)
    blk.rotation_euler = rot
    bev = blk.modifiers.new('bev', 'BEVEL')     # rounded bill-stack edges
    bev.width = 0.012; bev.segments = 2
    blk.data.materials.append(bill_mat(i))

    # paper band strap: thin in X, slightly proud in Y/Z, at block center
    bpy.ops.mesh.primitive_cube_add(location=loc)
    band = bpy.context.object
    band.name = 'band_%02d' % i
    band.scale = (0.055, BY / 2 * 1.03, BZ / 2 * 1.06)
    band.rotation_euler = rot
    band.data.materials.append(band_mat)

    # parent band to block, keeping current world transform (rides physics)
    bpy.context.view_layer.update()
    band.parent = blk
    band.matrix_parent_inverse = blk.matrix_world.inverted()

    rb(blk, 'ACTIVE', 'BOX', mass=1.0)
    bundles.append(blk)

# Spawn bundles fully staggered in Z (0.42 gap > 0.22 thickness => never
# overlapping at spawn, so no physics explosion) inside a tight XY disc so they
# fall and STACK UP into a heap. Lower bundles start nearer the floor and land
# first; higher ones land later => the pile builds from the bottom up.
for i in range(N_BUNDLES):
    ang = random.random() * math.tau
    rad = random.random() * 0.55
    x = math.cos(ang) * rad
    y = math.sin(ang) * rad * 0.6               # squashed toward camera axis
    z = FLOOR_Z + 1.15 + i * 0.42               # staggered drop heights
    rot = ((random.random() - 0.5) * 0.14,      # near-flat, slight tumble
           (random.random() - 0.5) * 0.14,
           (random.random() - 0.5) * math.tau)  # free yaw for an organic heap
    make_bundle(i, (x, y, z), rot)

# ---- rigidbody world tuning + BAKE (deterministic) ----
rw = scene.rigidbody_world
rw.substeps_per_frame = 20
rw.solver_iterations = 20
rw.point_cache.frame_start = 1
rw.point_cache.frame_end = max(FE, FS)
scene.frame_set(FS)
try:
    bpy.ops.ptcache.bake_all(bake=True)
    print('BAKED', rw.point_cache.frame_start, '..', rw.point_cache.frame_end)
except Exception as e:
    print('bake err', e)

# ---- 3-point area lights (bpp_cycles.py values; key raised for 4K/AgX) ----
def area(name, loc, energy, color, size=6):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    d = Vector((0, 0, FLOOR_Z + 0.4)) - Vector(loc)
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
# LUMA: key/fill/rim energies are the main brightness dial — raise together if
# the composite median luma reads low (spec §4 floor: median YAVG >= 48).
area('key', (5, -4, 6), 2000, (1.0, 0.98, 0.92), 6)
area('fill', (-6, -2, 2), 900, ACC_HI, 7)
area('rim', (-2, 5, 4), 1500, (0.6, 0.8, 1.0), 5)

# ---- off-camera softboxes (emission strengths 1.4 / 1.1 / 0.8 per spec) ----
def softbox(loc, size, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object
    m, b = new_mat('sb'); emissive(b, color, strength); o.data.materials.append(m)
    d = Vector((0, 0, FLOOR_Z + 0.4)) - Vector(loc)
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
softbox((-8, -5, 3), 5, ACC_HI, 1.4)           # LUMA: softbox strengths are the
softbox((8, -5, 2.5), 5, (0.9, 0.94, 1.0), 1.1) #        secondary brightness dial
softbox((0, -9, 5), 6, (0.7, 0.82, 1.0), 0.8)

# ---- seeded additive dust motes (30) drifting through the volume ----
dust_mat, dust_b = new_mat('dust')
set_in(dust_b, 'Base Color', (1, 1, 1, 1))
emissive(dust_b, (0.8, 0.9, 1.0), 6.0)         # emissive -> additive glow via Bloom
dust = []
for i in range(30):
    dx = (random.random() - 0.5) * 3.6
    dy = (random.random() - 0.5) * 2.4 - 1.0
    dz = FLOOR_Z + 0.3 + random.random() * 3.2
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.012 + random.random() * 0.012,
                                           location=(dx, dy, dz))
    d = bpy.context.object; d.name = 'dust_%02d' % i
    for p in d.data.polygons: p.use_smooth = True
    d.data.materials.append(dust_mat)
    # deterministic slow drift target (seeded), keyframed below when animating
    d['drift'] = (
        (random.random() - 0.5) * 0.25,
        (random.random() - 0.5) * 0.25,
        0.35 + random.random() * 0.55,
    )
    dust.append(d)

# ---- camera + DOF (55mm, aperture_fstop 2.2, focus pull) ----
STACK_CENTER = Vector((0.0, 0.0, FLOOR_Z + 0.6))   # ~settled pile center
CAM_START = Vector((0.6, -7.8, 1.4))
CAM_END = Vector((0.35, -5.4, 0.55))               # dolly-in, slightly lower
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam); scene.camera = cam
cd.lens = 55
cd.dof.use_dof = True
cd.dof.aperture_fstop = 2.2
cam.location = CAM_START
d = STACK_CENTER - CAM_START
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
# focus pull: start focused behind the pile (bundles land soft), rack onto the
# settled stack at the end.
FOC_START = (CAM_START - STACK_CENTER).length + 2.2
FOC_END = (CAM_END - STACK_CENTER).length
cd.dof.focus_distance = FOC_START if FE > FS else (CAM_START - STACK_CENTER).length

# ---- keyframed motion (only for a real range) ----
if FE > FS:
    # camera dolly-in + re-aim onto settled stack
    cam.location = CAM_START; cam.keyframe_insert('location', frame=FS)
    cam.rotation_euler = (STACK_CENTER - CAM_START).to_track_quat('-Z', 'Y').to_euler()
    cam.keyframe_insert('rotation_euler', frame=FS)
    cam.location = CAM_END; cam.keyframe_insert('location', frame=FE)
    cam.rotation_euler = (STACK_CENTER - CAM_END).to_track_quat('-Z', 'Y').to_euler()
    cam.keyframe_insert('rotation_euler', frame=FE)
    # focus pull onto the settled stack
    cd.dof.focus_distance = FOC_START; cd.dof.keyframe_insert('focus_distance', frame=FS)
    cd.dof.focus_distance = FOC_END; cd.dof.keyframe_insert('focus_distance', frame=FE)
    # ease the camera (smooth dolly, not linear)
    for fc in _act_fcurves(cam.animation_data.action if cam.animation_data else None):
        for kp in fc.keyframe_points:
            kp.interpolation = 'BEZIER'; kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
    # dust drift (deterministic, seeded targets)
    for d in dust:
        base = d.location.copy(); dr = d['drift']
        d.location = base; d.keyframe_insert('location', frame=FS)
        d.location = (base.x + dr[0], base.y + dr[1], base.z + dr[2])
        d.keyframe_insert('location', frame=FE)

# ---- compositor Glare Bloom (Blender 5.x node-group + socket API) ----
def setup_bloom(scene):
    nt = None
    try:
        scene.use_nodes = True; nt = scene.node_tree
    except Exception:
        nt = None
    if nt is None and hasattr(scene, 'compositing_node_group'):
        ng = bpy.data.node_groups.new('comp', 'CompositorNodeTree')
        scene.compositing_node_group = ng; nt = ng
    if nt is None:
        print('BLOOM: no compositor API, skipping'); return
    for n in list(nt.nodes): nt.nodes.remove(n)
    rl = nt.nodes.new('CompositorNodeRLayers')
    gl = nt.nodes.new('CompositorNodeGlare')
    def sock(name, val):
        if name in gl.inputs:
            try: gl.inputs[name].default_value = val
            except Exception as e: print('sock fail', name, e)
    if 'Type' in gl.inputs:
        try: gl.inputs['Type'].default_value = 'Bloom'
        except Exception: sock('Type', 'Fog Glow')
    sock('Quality', 'High')
    sock('Highlights Threshold', 0.8)
    sock('Highlights Smoothness', 0.3)
    sock('Strength', 1.0)
    sock('Size', 0.8)
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
    print('BLOOM: ok')
setup_bloom(scene)

# ---- render (PNG still or PNG sequence f_%04d.png) ----
scene.render.image_settings.file_format = 'PNG'
if FE == FS:
    os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
    scene.render.filepath = OUT + '_test.png'
    bpy.ops.render.render(write_still=True)
    print('WROTE', scene.render.filepath)
else:
    os.makedirs(OUT, exist_ok=True)
    scene.render.filepath = OUT + '/f_'          # -> f_0001.png, f_0002.png ...
    import os as _os
    for _f in range(FS, FE + 1):
        _fp = '%s/f_%04d' % (OUT, _f)
        if _os.path.exists(_fp + '.png'):
            continue                      # RESUME: skip frames already on disk (crash-tolerant)
        scene.frame_set(_f)
        scene.render.filepath = _fp
        bpy.ops.render.render(write_still=True)
    print('WROTE SEQ', OUT)
