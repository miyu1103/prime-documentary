# aircash_checkpointconverge.py
# EP34 "rolin" (airport civil forfeiture) — FIGURE #4 CheckpointConvergeMap
# SUPER-HEAVY tier · L2 Blender EEVEE (base: bpp_eevee.py).
#
# WHAT IT SHOWS (bespoke, topic-specific geometry built in code — NOT the gem showcase):
#   A schematic 3D map plane (dark, faint reflective, emissive grid) carrying FOUR nodes:
#     - 3 ORIGIN nodes as distinct COLORED markers (no readable text / no logos):
#         TSA (teal), State Police (blue), DEA (amber)
#     - 1 central CHECKPOINT hub (warm white) with a pulsing ring.
#   Each origin emits a DIRECTED stream of glowing beads that TRAVEL along an arced
#   route and CONVERGE on the central checkpoint. The travelling streams are the MAIN
#   motion (real moving 3D objects — 30 beads keyframed per-frame along bezier arcs).
#   Camera performs a slow overhead orbit. EEVEE bloom via Glare compositor.
#
# ARGV CONTRACT (identical to bpp_eevee.py / bpp_cycles.py):
#   blender -b -P aircash_checkpointconverge.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
#   FS==FE  -> single test still  -> writes <OUT>_test.png
#   FS < FE -> PNG sequence       -> writes <OUT>/f_0001.png ...   (Blender 5.x: PNG seq only)
#
# DETERMINISTIC: every bead / ring / camera transform is analytically keyframed on a
#   60fps timeline (no physics needed for this figure). random.seed(1234) fixes the only
#   randomness (tiny per-bead size jitter). No time-based randomness.

import bpy, sys, math, random
from mathutils import Vector

random.seed(1234)  # deterministic: only used for tiny bead-size jitter

# ---- args: OUT RX RY FS FE SAMPLES ----
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 3840)), int(A(2, 2160))   # super-heavy default = 4K
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 128))                      # TAA render samples (spec row: 96-192)

# ---- agency accent colors (linearish; distinct, unbranded markers) ----
TSA   = (0.05, 0.85, 0.75)   # teal
POLICE= (0.15, 0.45, 1.00)   # blue
DEA   = (1.00, 0.62, 0.12)   # amber
HUB   = (1.00, 0.92, 0.70)   # warm white checkpoint
GRIDC = (0.20, 0.42, 0.80)   # faint map grid blue

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
coll = scene.collection

# ---- engine (EEVEE Next / EEVEE) ----
engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
for cand in ['BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE']:
    if cand in engines:
        scene.render.engine = cand
        break
print('ENGINE =', scene.render.engine, '| available =', engines)

scene.render.resolution_x = RX
scene.render.resolution_y = RY
scene.render.film_transparent = False
scene.render.fps = 60                          # 60fps intent (author keyframes on 60fps timeline)
scene.frame_start, scene.frame_end = FS, FE

# motion blur (works for EEVEE Next + Cycles); travelling beads pick up the blur
try:
    scene.render.use_motion_blur = True
    scene.render.motion_blur_shutter = 0.5
except Exception as e:
    print('motion blur skip', e)

ee = scene.eevee
for a, v in [('taa_render_samples', SAMPLES), ('use_raytracing', True),
             ('use_ssr', True), ('use_gtao', True), ('use_shadows', True)]:
    if hasattr(ee, a):
        try: setattr(ee, a, v)
        except Exception as e: print('skip', a, e)
if hasattr(ee, 'ray_tracing_options'):
    try: ee.ray_tracing_options.use_denoise = True
    except Exception: pass

# ---- world: deep blue map ambient (kept lifted so composite reads bright) ----
# LUMA: if median YAVG dips below 48, raise bg strength here and key/top area energy below.
world = bpy.data.worlds.new('W'); scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
bg.inputs[0].default_value = (0.018, 0.028, 0.052, 1)
bg.inputs[1].default_value = 0.85

# ---- helpers ----
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

def emat(name, color, strength, base=None):
    m, b = new_mat(name)
    set_in(b, 'Base Color', (*(base if base else color), 1))
    emissive(b, color, strength)
    return m

# ================================================================
# BESPOKE GEOMETRY — schematic map + agency markers + checkpoint hub
# ================================================================

# ---- map plane (dark, faintly reflective; the "table" the schematic sits on) ----
bpy.ops.mesh.primitive_plane_add(size=34, location=(0, 0, 0))
mp = bpy.context.object; mp.name = 'map'
mm, mb = new_mat('mapMat')
set_in(mb, 'Base Color', (0.012, 0.02, 0.038, 1))
set_in(mb, 'Metallic', 0.55)
set_in(mb, 'Roughness', 0.42)
mp.data.materials.append(mm)

# ---- schematic grid lines (emissive thin bars) — reads as a map, low strength ----
gridM = emat('gridMat', GRIDC, 1.6, base=(0.02, 0.04, 0.09))
def grid_bar(loc, scale, rotz=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.object
    o.scale = scale
    o.rotation_euler = (0, 0, rotz)
    o.data.materials.append(gridM)
    return o
GRID_HALF = 15.0
GRID_N = 11
for i in range(GRID_N):
    x = -GRID_HALF + (2 * GRID_HALF) * i / (GRID_N - 1)
    grid_bar((x, 0.0, 0.015), (0.03, GRID_HALF, 0.02))   # vertical line
    grid_bar((0.0, x, 0.015), (GRID_HALF, 0.03, 0.02))   # horizontal line

# ---- node positions on the map (XY plane, Z up) ----
CENTER = Vector((0.0, 0.0, 0.6))     # checkpoint hub top (bead arrival point)
ORIGINS = [
    ('TSA',    Vector((-6.8,  4.2, 0.15)), TSA),
    ('POLICE', Vector(( 7.0,  3.0, 0.15)), POLICE),
    ('DEA',    Vector((-0.8, -7.2, 0.15)), DEA),
]

# ---- origin markers: dark post + bright colored dome (distinct colored markers) ----
def origin_marker(pos, color):
    # post
    bpy.ops.mesh.primitive_cylinder_add(radius=0.28, depth=1.1,
                                        location=(pos.x, pos.y, 0.55))
    post = bpy.context.object
    pm, pb = new_mat('postMat')
    set_in(pb, 'Base Color', (0.03, 0.05, 0.08, 1))
    set_in(pb, 'Metallic', 0.8); set_in(pb, 'Roughness', 0.3)
    post.data.materials.append(pm)
    # glowing colored dome on top = the agency marker
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(pos.x, pos.y, 1.15))
    dome = bpy.context.object
    for p in dome.data.polygons: p.use_smooth = True
    dome.data.materials.append(emat('markMat', color, 7.0))
    # thin base ring accent
    bpy.ops.mesh.primitive_torus_add(location=(pos.x, pos.y, 0.05),
                                     major_radius=0.7, minor_radius=0.05)
    ring = bpy.context.object
    for p in ring.data.polygons: p.use_smooth = True
    ring.data.materials.append(emat('markRing', color, 4.0))
    return dome

for _name, pos, color in ORIGINS:
    origin_marker(pos, color)

# ---- central checkpoint hub (warm white) + pulsing ring ----
bpy.ops.mesh.primitive_cylinder_add(radius=1.15, depth=0.9, location=(0, 0, 0.45))
hub = bpy.context.object; hub.name = 'hub'
hm, hb = new_mat('hubMat')
set_in(hb, 'Base Color', (0.06, 0.07, 0.09, 1))
set_in(hb, 'Metallic', 0.85); set_in(hb, 'Roughness', 0.22)
hub.data.materials.append(hm)
# bright emissive dome cap (the convergence point)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 0, 0.9))
cap = bpy.context.object; cap.name = 'hubCap'
for p in cap.data.polygons: p.use_smooth = True
cap.data.materials.append(emat('hubCap', HUB, 9.0))
# pulsing ring around the hub (scales with arrivals — keyframed below)
bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0.12), major_radius=1.5, minor_radius=0.07)
pulse = bpy.context.object; pulse.name = 'hubPulse'
for p in pulse.data.polygons: p.use_smooth = True
pulse.data.materials.append(emat('hubPulseMat', HUB, 6.0))

# ---- ground route tracks (faint arced-looking straight tubes O->C, stream-colored) ----
def route_track(pos, color):
    a = Vector((pos.x, pos.y, 0.05)); b = Vector((0, 0, 0.05))
    mid = (a + b) * 0.5
    length = (b - a).length
    bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=length, location=mid)
    t = bpy.context.object
    t.rotation_euler = (b - a).to_track_quat('Z', 'Y').to_euler()
    t.data.materials.append(emat('routeMat', color, 2.2, base=(0.02, 0.03, 0.05)))

for _name, pos, color in ORIGINS:
    route_track(pos, color)

# ================================================================
# MAIN MOTION — directed bead streams travelling origin -> checkpoint
# ================================================================
# Each stream = BEADS_PER beads on a quadratic bezier arc (rises off the map, descends
# into the hub). Beads are phase-staggered and LOOP with period PERIOD frames so the
# stream flows continuously and converges on the checkpoint. Fully deterministic:
# position is an analytic function of the absolute frame; per-frame keyframes trace the arc.
BEADS_PER = 10
PERIOD = 120            # frames for one origin->checkpoint traversal (2.0s @ 60fps)
ARC_H = 3.0             # peak lift of the bezier control point above the map

def bezier(a, m, c, t):
    u = 1.0 - t
    return (a * (u * u)) + (m * (2 * u * t)) + (c * (t * t))

# build one template bead mesh once, then give every bead its OWN copy so each
# stream keeps its own color (material lives on mesh data).
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0))
tmpl = bpy.context.object
for p in tmpl.data.polygons: p.use_smooth = True
base_mesh = tmpl.data
bpy.data.objects.remove(tmpl, do_unlink=True)   # keep only the mesh datablock as a template

beads = []  # (obj, a, mid, c, phase)
for si, (_name, pos, color) in enumerate(ORIGINS):
    a = Vector((pos.x, pos.y, 0.15))
    c = CENTER.copy()
    mid = (a + c) * 0.5 + Vector((0, 0, ARC_H))
    smat = emat('beadMat_%d' % si, color, 8.0, base=(1, 1, 1))
    for bi in range(BEADS_PER):
        r = 0.14 + random.random() * 0.05           # deterministic jitter (seed 1234)
        bead = bpy.data.objects.new('bead_%d_%d' % (si, bi), base_mesh.copy())
        coll.objects.link(bead)
        bead.scale = (r, r, r)
        bead.data.materials.clear()
        bead.data.materials.append(smat)
        phase = bi / BEADS_PER
        beads.append((bead, a, mid, c, phase))

def bead_pos(a, m, c, phase, frame):
    # looping parameter in [0,1)
    t = ((frame - FS) / PERIOD + phase) % 1.0
    return bezier(a, m, c, t)

# ---- lights: 3-point + overhead top fill (keeps the map bright under bloom) ----
def area(name, loc, energy, color, size=6):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    d = Vector((0, 0, 0)) - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob
# LUMA: raise these energies if composite median YAVG < 48.
area('key',  (7, -6, 10), 1500, (1, 1, 1), 7)
area('fill', (-8, -3, 5),  750, (0.6, 0.8, 1.0), 8)
area('rim',  (-3, 8, 7),  1200, (0.7, 0.85, 1.0), 6)
area('top',  (0, 0, 15),  1600, (0.9, 0.95, 1.0), 12)   # overhead fill for the map

# reflection softboxes (off camera; glint on hub/markers)
def softbox(loc, size, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object; o.data.materials.append(emat('sb', color, strength))
    d = Vector((0, 0, 0)) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
softbox((-10, -7, 6), 6, (0.55, 0.72, 1.0), 3.0)
softbox(( 10, -7, 5), 6, (0.75, 0.88, 1.0), 2.2)
softbox((0, -11, 8),  7, (0.6, 0.75, 1.0),  1.6)

# ---- camera: slow OVERHEAD orbit (parented to a pivot empty for deterministic orbit) ----
piv = bpy.data.objects.new('camPivot', None); coll.objects.link(piv)
piv.location = (0, 0, 0)
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam); scene.camera = cam
cam.location = (0.0, -10.5, 13.5)     # high angle ~ overhead, still sees the 3D markers
cd.lens = 42
cd.dof.use_dof = True
cd.dof.focus_object = hub
cd.dof.aperture_fstop = 4.0           # map stays mostly sharp (schematic clarity)
d = Vector((0, 0, 0.5)) - Vector(cam.location)
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
cam.parent = piv

# ================================================================
# KEYFRAMES (deterministic) — only when a real range is requested
# ================================================================
if FE > FS:
    # main motion: per-frame bead positions along the arcs (exact path, no interp error)
    for f in range(FS, FE + 1):
        for (bead, a, m, c, phase) in beads:
            bead.location = bead_pos(a, m, c, phase, f)
            bead.keyframe_insert('location', frame=f)
    # slow overhead orbit: rotate the camera pivot around Z
    ORBIT_TURNS = 0.14
    piv.rotation_euler = (0, 0, 0.0)
    piv.keyframe_insert('rotation_euler', frame=FS)
    piv.rotation_euler = (0, 0, math.tau * ORBIT_TURNS)
    piv.keyframe_insert('rotation_euler', frame=FE)
    # checkpoint pulse ring: gentle sine breathing synced to bead arrival cadence
    for f in range(FS, FE + 1, 3):
        s = 1.0 + 0.10 * math.sin((f - FS) / PERIOD * math.tau * BEADS_PER)
        pulse.scale = (s, s, 1.0)
        pulse.keyframe_insert('scale', frame=f)
else:
    # single test still: freeze beads spread along their arcs at FS (reads as a full stream)
    for (bead, a, m, c, phase) in beads:
        bead.location = bead_pos(a, m, c, phase, FS)

# ---- compositor bloom (Glare) — robust across Blender 4.x/5.x (from bpp_eevee.py) ----
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
    sock('Highlights Smoothness', 0.3); sock('Strength', 1.0); sock('Size', 0.85)
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

# ---- render (PNG only; Blender 5.x has no in-app video output) ----
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
