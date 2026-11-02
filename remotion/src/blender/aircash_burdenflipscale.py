"""EP34 rolin — HERO #8 BurdenFlipScale — L3 Cycles ceiling scene (SUPER-HEAVY tier).

Bespoke subject: a two-pan BALANCE SCALE (central fulcrum post + a horizontal
beam that pivots on it + a hanging pan at each end via a thin rod). A small
"citizen" weight rests in the LEFT (citizen) pan from frame 1, so the beam
starts leaning citizen-down. A heavy banded CASH-BUNDLE proxy (block wrapped by
crossed paper straps) then DROPS from above onto the RIGHT (government) pan; via
rigidbody + a GENERIC_SPRING angular constraint on the fulcrum, the beam FLIPS
from the citizen side to the government side and SETTLES with a damped
oscillation. This visualizes the burden of proof flipping to ">50% — more
likely than not" (CAFRA). Camera: 55mm push-in that FOLLOWS the descending
government pan, DOF aperture_fstop 2.4.

Physics (spec §0-bis row #8): substeps_per_frame 20, solver_iterations 20,
point_cache bake_all, restitution 0.05. The tilt is a REAL moving 3D object
(the beam + both pans + the loaded mass), not a camera/light move.

Lighting: 3-point area + 3 off-camera softboxes (1.4/1.1/0.8) + Glare Bloom
(Strength 1.0 / Size 0.8). Seeded 30 additive dust motes drift through the
volume. Follows remotion/prototypes/motion3d/blender/bpp_cycles.py (L3 look) and
bpp_physics.py (rigidbody + point_cache bake), and the sibling
aircash_cashstack.py house style. Deterministic: seeded random.seed(1234); all
motion is frame-keyframed or physics-baked. No real-person likeness, no readable
text/logos, unbranded (invariant 11).

ARGV CONTRACT (identical to bpp_cycles.py):
    blender -b -P aircash_burdenflipscale.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
    FS == FE -> single test still (<OUT>_test.png)
    FS <  FE -> PNG sequence <OUT>/f_0001.png ...  (Blender 5.x has no in-app
                video output; encode the PNG sequence separately with ffmpeg).

TEST (frame 1 smoke still):
    blender -b -P remotion/src/blender/aircash_burdenflipscale.py -- out/hero_burdenflipscale 3840 2160 1 1 200
FULL (12s @ 60fps -> 720 frames):
    blender -b -P remotion/src/blender/aircash_burdenflipscale.py -- out/hero_burdenflipscale 3840 2160 1 720 200
    npx remotion ffmpeg -framerate 60 -i out/hero_burdenflipscale/f_%04d.png -c:v libx264 -crf 16 -pix_fmt yuv420p -y public/EP34/hero_burdenflipscale.mp4
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
ACC = (0.10, 0.42, 1.0)                        # blue accent (rim/softbox/gov glow)
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

def steel_mat(name, base=(0.05, 0.06, 0.08), rough=0.28, metallic=0.85):
    m, b = new_mat(name)
    set_in(b, 'Base Color', (*base, 1))
    set_in(b, 'Metallic', metallic)
    set_in(b, 'Roughness', rough)
    return m

# ---- rigidbody helper (bpp_physics.py pattern) ----
def rb(obj, kind, shape, mass=1.0, friction=0.5, restitution=0.05,
       lin_damp=0.04, ang_damp=0.06, margin=0.006):
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
        # LOW body damping: the SETTLE comes from the spring's angular damping,
        # not from body damping (which would kill the oscillation the spec wants).
        obj.rigid_body.linear_damping = lin_damp
        obj.rigid_body.angular_damping = ang_damp
        obj.rigid_body.use_margin = True
        obj.rigid_body.collision_margin = margin

# ---- mesh build helpers (apply scale so joined collision meshes are clean) ----
def make_box(name, loc, dims, mat=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.name = name
    o.scale = dims; o.rotation_euler = rot
    for s in bpy.context.selected_objects: s.select_set(False)
    o.select_set(True); bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat: o.data.materials.append(mat)
    return o

def make_cyl(name, loc, radius, depth, mat=None, verts=56):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=loc, vertices=verts)
    o = bpy.context.object; o.name = name
    if mat: o.data.materials.append(mat)
    return o

def join_into(target, others):
    for s in bpy.context.selected_objects: s.select_set(False)
    target.select_set(True)
    for o in others: o.select_set(True)
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.join()
    return target

# ============================================================================
# GEOMETRY  (all Z measured up from the metallic floor)
# ============================================================================
FLOOR_Z = -2.0
PIVOT_Z = FLOOR_Z + 4.0        # = 2.0  (top of fulcrum post = beam pivot)
ARM = 2.0                      # pan lever arm (half beam span, m)
PAN_DROP = 0.92                # how far each pan hangs below the beam
PAN_TOP_Z = PIVOT_Z - PAN_DROP + 0.05

steel = steel_mat('steel', base=(0.06, 0.07, 0.10), rough=0.26, metallic=0.9)
brass = steel_mat('brass', base=(0.14, 0.11, 0.05), rough=0.34, metallic=0.9)  # warm beam

# ---- reflective metallic floor (passive rigidbody) ----
bpy.ops.mesh.primitive_plane_add(size=44, location=(0, 0, FLOOR_Z))
floor = bpy.context.object; floor.name = 'floor'
fm, fb = new_mat('floor')
set_in(fb, 'Base Color', (0.01, 0.015, 0.03, 1))
set_in(fb, 'Metallic', 0.9)
set_in(fb, 'Roughness', 0.22)
floor.data.materials.append(fm)
rb(floor, 'PASSIVE', 'BOX', friction=0.7)

# ---- fulcrum post (passive rigidbody; also the spring constraint's anchor) ----
post = make_cyl('post', (0, 0, FLOOR_Z + (PIVOT_Z - FLOOR_Z) / 2.0), 0.16,
                PIVOT_Z - FLOOR_Z, steel)
# a small knuckle at the pivot for a mechanical read
knob = make_cyl('post_knob', (0, 0, PIVOT_Z), 0.24, 0.14, steel)
knob.rotation_euler = (math.radians(90), 0, 0)
post = join_into(post, [knob])
rb(post, 'PASSIVE', 'MESH', friction=0.7)

# ---- balance-scale assembly: beam + 2 hanger rods + 2 pans (ONE rigidbody) ---
# Built as a single joined mesh whose ORIGIN sits at the pivot (0,0,PIVOT_Z) so
# the angular spring rotates it cleanly about the pivot.
beam = make_box('beam', (0, 0, PIVOT_Z), (2 * ARM + 0.4, 0.16, 0.17), brass)
# end caps / hanger knuckles at each beam end
capL = make_box('capL', (-ARM, 0, PIVOT_Z), (0.16, 0.22, 0.30), steel)
capR = make_box('capR', (ARM, 0, PIVOT_Z), (0.16, 0.22, 0.30), steel)
# thin vertical hanger rods down to the pans
rodL = make_box('rodL', (-ARM, 0, PIVOT_Z - PAN_DROP / 2.0), (0.05, 0.05, PAN_DROP), steel)
rodR = make_box('rodR', (ARM, 0, PIVOT_Z - PAN_DROP / 2.0), (0.05, 0.05, PAN_DROP), steel)
# shallow round pans (flat discs; high friction holds the mass on the tilt —
# atan(0.9) ~= 42deg static limit >> the ~15deg settled tilt, so nothing slides)
panL = make_cyl('panL', (-ARM, 0, PAN_TOP_Z - 0.05), 0.58, 0.10, steel)
panR = make_cyl('panR', (ARM, 0, PAN_TOP_Z - 0.05), 0.58, 0.10, steel)
beam = join_into(beam, [capL, capR, rodL, rodR, panL, panR])
# ACTIVE + MESH collision so the dropped mass lands IN the pan (on the disc
# face), not on a convex-hull lid. MESH active is stable here because it only
# ROTATES (all translation is locked by the constraint) and substeps=20.
rb(beam, 'ACTIVE', 'MESH', mass=2.0, friction=0.9, restitution=0.05,
   lin_damp=0.02, ang_damp=0.03)

# ---- government-side accent underglow disc (rides the beam via parenting) ----
# Faint blue emissive disc under the RIGHT (government) pan -> Glare Bloom catches
# it, reading "burden now on the government". Decorative only; no text.
glow = make_cyl('gov_glow', (ARM, 0, PAN_TOP_Z - 0.14), 0.5, 0.02)
gm, gb = new_mat('gov_glow_mat'); emissive(gb, ACC, 3.0); glow.data.materials.append(gm)
bpy.context.view_layer.update()
glow.parent = beam
glow.matrix_parent_inverse = beam.matrix_world.inverted()

# ---- GENERIC_SPRING angular constraint at the fulcrum ------------------------
# Locks ALL translation and rotation about X/Z; leaves rotation about Y free with
# an angular spring (rest = level, captured at bake start). The dropped mass adds
# torque; the spring resists -> the beam settles at a tilt with a DAMPED
# oscillation (exactly the spec's "settling oscillation"). object2 = static post,
# so the pivot is world-anchored.
STIFF_ANG_Y = 400.0   # LUMA-of-motion dial: RAISE to reduce tilt magnitude / a
                      # gentler flip; LOWER for a bigger, more dramatic flip.
DAMP_ANG_Y = 22.0     # RAISE to settle faster (fewer swings); LOWER for more ring.
ANG_LIMIT = 0.9       # hard +/- rad stop so a mistuned spring can't flip over.

bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, PIVOT_Z))
pivot = bpy.context.object; pivot.name = 'pivot_spring'
bpy.context.view_layer.objects.active = pivot
bpy.ops.rigidbody.constraint_add(type='GENERIC_SPRING')
rbc = pivot.rigid_body_constraint
def _cset(attr, val):
    try: setattr(rbc, attr, val)
    except Exception as e: print('constraint set fail', attr, e)
_cset('object1', beam)
_cset('object2', post)
_cset('disable_collisions', True)
# CRITICAL: only the SPRING2 solver (btGeneric6DofSpring2Constraint) actually
# drives the ANGULAR springs (use_spring_ang_*). SPRING1 exposes the same
# attributes but silently ignores them -> the beam would become a spring-LESS
# free hinge that just swings to its +/-ANG_LIMIT and clacks (a totally different
# motion). The GENERIC_SPRING operator defaults to SPRING2, but we pin it
# explicitly and verify it below so a version/default change can never regress it.
_cset('spring_type', 'SPRING2')
# lock all three translations to 0 (pin the pivot point)
for ax in ('x', 'y', 'z'):
    _cset('use_limit_lin_' + ax, True)
    _cset('limit_lin_' + ax + '_lower', 0.0)
    _cset('limit_lin_' + ax + '_upper', 0.0)
# lock rotation about X and Z (beam may only see-saw about Y)
for ax in ('x', 'z'):
    _cset('use_limit_ang_' + ax, True)
    _cset('limit_ang_' + ax + '_lower', 0.0)
    _cset('limit_ang_' + ax + '_upper', 0.0)
# free-with-spring rotation about Y, bounded by a hard stop
_cset('use_limit_ang_y', True)
_cset('limit_ang_y_lower', -ANG_LIMIT)
_cset('limit_ang_y_upper', ANG_LIMIT)
_cset('use_spring_ang_y', True)
_cset('spring_stiffness_ang_y', STIFF_ANG_Y)
_cset('spring_damping_ang_y', DAMP_ANG_Y)

# ---- M3 FIX: FAIL-FAST verification of the angular spring -------------------
# _cset() swallows AttributeErrors and only prints. If a Blender-version attr
# rename (or a wrong spring_type) made the spring silently a no-op, the flip
# would look completely wrong and we'd only find out after a full 720-frame
# render. Read the critical attributes back and hard-fail if the spring did not
# actually take effect. (Verified on Blender 5.1: these are the live names.)
def _expect(attr, want, tol=1e-4):
    try:
        got = getattr(rbc, attr)
    except AttributeError as e:
        raise RuntimeError(
            'BurdenFlipScale spring BROKEN: attribute %r missing on this Blender '
            '(rigid_body_constraint) -> the angular spring would be a no-op. %s' % (attr, e))
    ok = (abs(got - want) <= tol) if isinstance(want, float) else (got == want)
    if not ok:
        raise RuntimeError(
            'BurdenFlipScale spring BROKEN: %s = %r but expected %r. The GENERIC_SPRING '
            'did not take effect (beam would be a spring-less free hinge). Aborting before '
            'a wasted render.' % (attr, got, want))
    return got
_expect('spring_type', 'SPRING2')          # angular springs are live ONLY on SPRING2
_expect('use_spring_ang_y', True)
_expect('spring_stiffness_ang_y', float(STIFF_ANG_Y))
_expect('spring_damping_ang_y', float(DAMP_ANG_Y))
_expect('use_limit_ang_y', True)
_expect('use_limit_ang_x', True)
_expect('use_limit_ang_z', True)
if rbc.object1 is not beam or rbc.object2 is not post:
    raise RuntimeError('BurdenFlipScale spring BROKEN: constraint endpoints not (beam, post): %r %r'
                       % (rbc.object1, rbc.object2))
print('SPRING OK: type=%s stiffness_ang_y=%.1f damping_ang_y=%.1f' % (
    rbc.spring_type, rbc.spring_stiffness_ang_y, rbc.spring_damping_ang_y))

# ---- currency / weight materials (bill green + warm paper strap) ----
def bill_mat(name):
    m, b = new_mat(name)
    set_in(b, 'Base Color', (0.24, 0.42, 0.28, 1))   # desaturated bill green
    set_in(b, 'Metallic', 0.0)
    set_in(b, 'Roughness', 0.55)
    if not set_in(b, 'Specular IOR Level', 0.4):
        set_in(b, 'Specular', 0.4)
    return m
band_mat, band_b = new_mat('band')
set_in(band_b, 'Base Color', (0.86, 0.80, 0.62, 1))
set_in(band_b, 'Roughness', 0.4)
emissive(band_b, (0.9, 0.82, 0.6), 0.35)             # subtle accent for Glare Bloom

# ---- bespoke banded CASH-BUNDLE proxy (the falling symbolic mass) ----
# A flattened rounded bill block wrapped by TWO crossed paper straps. Straps are
# parented to the block so they ride the rigidbody-baked fall. Unbranded, no text.
GX, GY, GZ = 0.86, 0.60, 0.40
DROP_START = Vector((ARM, 0.0, PIVOT_Z + 2.3))        # above the government pan
# ---- M2 FIX: release timing (frames derived from fps, NOT hard-coded) --------
# The bundle is HELD in the air (rigidbody kinematic=True) for the first
# HOLD_SECS, then RELEASED (kinematic=False) so physics takes over. This spreads
# the drop + the long spring-damped settling oscillation across most of the 12s
# instead of finishing the whole flip in the first ~1s (which left ~11s static).
# All frames are ABSOLUTE (anchored to physics frame 1 == point_cache start), so
# a resumed sub-range render still bakes the identical motion.
FPS = scene.render.fps                                # 60 (authoring fps)
HOLD_SECS = 2.5                                        # bundle hovers before drop
RELEASE_FRAME = 1 + int(round(HOLD_SECS * FPS))       # -> frame 151 @60fps
# Pre-release motion is carried by the citizen weight settling into the left pan
# (it starts 0.27 above the pan and drops from frame 1, ringing the beam through
# the spring), so there is no dead-still stretch before the release.
govblk = make_box('cashbundle', DROP_START, (GX, GY, GZ), bill_mat('cash_bills'),
                  rot=(0.06, -0.05, 0.10))
bevm = govblk.modifiers.new('bev', 'BEVEL'); bevm.width = 0.02; bevm.segments = 2
strapA = make_box('strapA', DROP_START, (0.09, GY * 1.04, GZ * 1.06), band_mat,
                  rot=(0.06, -0.05, 0.10))
strapB = make_box('strapB', DROP_START, (GX * 1.04, 0.09, GZ * 1.06), band_mat,
                  rot=(0.06, -0.05, 0.10))
for s in (strapA, strapB):
    bpy.context.view_layer.update()
    s.parent = govblk
    s.matrix_parent_inverse = govblk.matrix_world.inverted()
# HEAVY, so it clearly overpowers the citizen weight and flips the beam past level.
rb(govblk, 'ACTIVE', 'BOX', mass=6.0, friction=0.9, restitution=0.05,
   lin_damp=0.05, ang_damp=0.15)
# HOLD in the air, then RELEASE at RELEASE_FRAME (bpp_physics/hinders pattern):
# kinematic=True keyframed True through RELEASE_FRAME-1, then False at
# RELEASE_FRAME so the point-cache bake makes the bundle free-fall from there.
govblk.rigid_body.kinematic = True
govblk.keyframe_insert('rigid_body.kinematic', frame=1)
govblk.keyframe_insert('rigid_body.kinematic', frame=max(1, RELEASE_FRAME - 1))
govblk.rigid_body.kinematic = False
govblk.keyframe_insert('rigid_body.kinematic', frame=RELEASE_FRAME)
# a boolean must switch, never interpolate: force CONSTANT interpolation so the
# release is a clean step (and stays deterministic).
if govblk.animation_data:
    for _fc in _act_fcurves(govblk.animation_data.action):
        if _fc.data_path.endswith('kinematic'):
            for _kp in _fc.keyframe_points:
                _kp.interpolation = 'CONSTANT'

# ---- citizen-side weight: rests in the LEFT pan from frame 1 (initial lean) ---
# A small dark calibration-weight block. Light -> gives a gentle citizen-down
# lean at rest, which the dropped cash then FLIPS to government-down.
CIT_START = Vector((-ARM, 0.0, PAN_TOP_Z + 0.27))
citw = make_box('citizen_weight', CIT_START, (0.42, 0.42, 0.5),
                steel_mat('cit_metal', base=(0.04, 0.05, 0.07), rough=0.35, metallic=0.9))
cbev = citw.modifiers.new('bev', 'BEVEL'); cbev.width = 0.02; cbev.segments = 2
rb(citw, 'ACTIVE', 'BOX', mass=1.5, friction=0.9, restitution=0.05,
   lin_damp=0.1, ang_damp=0.2)

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
    d = Vector((0, 0, PIVOT_Z - 0.4)) - Vector(loc)
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
# LUMA: key/fill/rim energies are the primary brightness dial — raise together if
# the composite median luma reads low (spec §4 floor: median YAVG >= 48).
area('key', (5, -5, 7), 2400, (1.0, 0.98, 0.92), 7)
area('fill', (-6, -2, 3), 1100, ACC_HI, 8)
area('rim', (-2, 6, 5), 1700, (0.6, 0.8, 1.0), 5)

# ---- off-camera softboxes (emission strengths 1.4 / 1.1 / 0.8 per spec) ----
def softbox(loc, size, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object
    m, b = new_mat('sb'); emissive(b, color, strength); o.data.materials.append(m)
    d = Vector((0, 0, PIVOT_Z - 0.4)) - Vector(loc)
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
softbox((-8, -5, 4), 5, ACC_HI, 1.4)            # LUMA: softbox strengths are the
softbox((8, -5, 3.5), 5, (0.9, 0.94, 1.0), 1.1) #        secondary brightness dial
softbox((0, -9, 6), 6, (0.7, 0.82, 1.0), 0.8)

# ---- seeded additive dust motes (30) drifting through the volume ----
dust_mat, dust_b = new_mat('dust')
set_in(dust_b, 'Base Color', (1, 1, 1, 1))
emissive(dust_b, (0.8, 0.9, 1.0), 6.0)          # emissive -> additive glow via Bloom
dust = []
for i in range(30):
    dx = (random.random() - 0.5) * 5.2
    dy = (random.random() - 0.5) * 2.6 - 1.0
    dz = FLOOR_Z + 0.4 + random.random() * 4.0
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.012 + random.random() * 0.012,
                                           location=(dx, dy, dz))
    d = bpy.context.object; d.name = 'dust_%02d' % i
    for p in d.data.polygons: p.use_smooth = True
    d.data.materials.append(dust_mat)
    d['drift'] = (
        (random.random() - 0.5) * 0.25,
        (random.random() - 0.5) * 0.25,
        0.35 + random.random() * 0.55,
    )
    dust.append(d)

# ---- camera + DOF (55mm, aperture_fstop 2.4) — push-in FOLLOWING the pans -----
# The look target travels from the beam center toward the RIGHT (government) pan
# as it descends, so the camera literally follows the loaded pan through the flip.
LOOK_START = Vector((0.0, 0.0, PIVOT_Z - 0.2))
LOOK_END = Vector((ARM * 0.8, 0.0, PAN_TOP_Z - 0.15))
CAM_START = Vector((2.4, -9.4, 2.6))
CAM_END = Vector((1.7, -6.5, 1.6))              # dolly-in, slightly lower
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam); scene.camera = cam
cd.lens = 55
cd.dof.use_dof = True
cd.dof.aperture_fstop = 2.4
cam.location = CAM_START
cam.rotation_euler = (LOOK_START - CAM_START).to_track_quat('-Z', 'Y').to_euler()
cd.dof.focus_distance = (CAM_START - LOOK_START).length

# ---- keyframed camera motion (only for a real range) ----
if FE > FS:
    cam.location = CAM_START; cam.keyframe_insert('location', frame=FS)
    cam.rotation_euler = (LOOK_START - CAM_START).to_track_quat('-Z', 'Y').to_euler()
    cam.keyframe_insert('rotation_euler', frame=FS)
    cam.location = CAM_END; cam.keyframe_insert('location', frame=FE)
    cam.rotation_euler = (LOOK_END - CAM_END).to_track_quat('-Z', 'Y').to_euler()
    cam.keyframe_insert('rotation_euler', frame=FE)
    cd.dof.focus_distance = (CAM_START - LOOK_START).length
    cd.dof.keyframe_insert('focus_distance', frame=FS)
    cd.dof.focus_distance = (CAM_END - LOOK_END).length
    cd.dof.keyframe_insert('focus_distance', frame=FE)
    # ease the dolly (smooth, not linear)
    for fc in _act_fcurves(cam.animation_data.action if cam.animation_data else None):
        for kp in fc.keyframe_points:
            kp.interpolation = 'BEZIER'; kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
    if cd.animation_data:
        for fc in _act_fcurves(cd.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = 'BEZIER'; kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
    # deterministic seeded dust drift
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
