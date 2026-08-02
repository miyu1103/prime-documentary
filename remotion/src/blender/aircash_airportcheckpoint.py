"""EP34 rolin — HERO #2 AirportCheckpoint (L3 Cycles ceiling render).

Bespoke stylized airport concourse for the civil-forfeiture episode:
  - reflective metallic floor + rows of columns + a security checkpoint arch
    (a metal-detector-style portal frame; NO readable signage / logos / text),
  - VOLUMETRIC skylight shafts: a homogeneous Principled-Volume domain lit by
    down-angled SPOT lights that punch banded god-rays through ceiling slats,
  - a CROWD of anonymous low-poly standing SILHOUETTES (faces NOT modeled),
    instanced (shared mesh data) and flowing LATERALLY across the concourse.
    The crowd's lateral travel is THE MAIN 3D MOTION (not the camera).
  - camera: slow truck (X) + dolly (Y) through the concourse, AgX tonemap.

Built to copy remotion/prototypes/motion3d/blender/bpp_cycles.py exactly for the
render plumbing (argv contract, GPU pick, AgX, caustics OFF, reflective floor,
3-point area lights + softboxes, Glare/Bloom compositor, PNG-sequence output).

ARGV CONTRACT (identical to bpp_cycles.py):
    blender -b -P aircash_airportcheckpoint.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
    FS==FE -> single test still  <OUT>_cyc.png
    FS< FE -> PNG sequence       <OUT>/f_0001.png ...

DETERMINISTIC: crowd layout is seeded (random.seed(1234)); all motion is
frame-keyframed (scene keyframe_insert). No time-based / unseeded randomness.
60fps intent: caller passes the frame range; keyframes authored on a 60fps
timeline (scene.render.fps=60). Motion blur: render.use_motion_blur + shutter 0.5.

BRIGHTNESS: AgX sinks dark. The frame is kept bright by (a) high SPOT energy for
the shafts, (b) area key/fill/rim, (c) emissive softboxes, (d) a thin emissive
accent strip on the arch lintel. If a composite reads dark after AgX, RAISE luma
at the tagged spots below: SPOT energy (KEY_SPOT_E), VOL_DENSITY (lower = brighter
shafts read), area 'key'/'fill' energy, and softbox strengths.
"""
import bpy, sys, math, random, os
from mathutils import Vector

# ---- args: OUT RX RY FS FE SAMPLES (verbatim contract) ----
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 3840)), int(A(2, 2160))
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 200))
ACC = (0.10, 0.42, 1.0)       # brand accent (linearish blue ~#4ea1ff)
ACC_HI = (0.35, 0.70, 1.0)
SKY = (0.80, 0.88, 1.00)      # cool skylight tint for the shafts
KEY_SPOT_E = 42000.0          # LUMA KNOB: per-shaft spot energy (raise if dark)
VOL_DENSITY = 0.032           # LUMA KNOB: fog density (LOWER -> brighter beams)

random.seed(1234)             # deterministic crowd layout

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
# caustics OFF on purpose (prototype note): with volume+metal they can make some
# frames explode in render time. Bloom supplies the glow. Do not re-enable.
try:
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
except Exception:
    pass

scene.render.resolution_x = RX
scene.render.resolution_y = RY
scene.render.fps = 60                     # 60fps hero (avoid judder vs 60fps comp)
scene.frame_start, scene.frame_end = FS, FE
scene.view_settings.view_transform = 'AgX'  # cinematic tonemap

# ---- motion blur (Cycles, shutter 0.5, rolling shutter off) ----
scene.render.use_motion_blur = True
try:
    scene.render.motion_blur_shutter = 0.5
except Exception:
    pass
try:
    scene.cycles.motion_blur_position = 'CENTER'
    scene.cycles.rolling_shutter_type = 'NONE'
except Exception:
    pass

# ---- world: dark blue gradient (reflections) ----
world = bpy.data.worlds.new('W'); scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
bg.inputs[0].default_value = (0.012, 0.02, 0.04, 1)
bg.inputs[1].default_value = 0.5

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

def volume_mat(name, color, density, aniso, emission=0.0):
    """Volume-only material (Principled Volume -> Material Output.Volume)."""
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    def vset(k, v):
        if k in vol.inputs:
            try: vol.inputs[k].default_value = v
            except Exception: pass
    vset('Color', (*color, 1))
    vset('Density', density)
    vset('Anisotropy', aniso)          # forward scatter -> crisper shafts
    if emission > 0:
        vset('Emission Strength', emission)
        vset('Emission Color', (*color, 1))
    nt.links.new(vol.outputs[0], out.inputs['Volume'])
    return m

# ================= BESPOKE CONCOURSE GEOMETRY =================
# Concourse runs along +Y (depth). Camera starts at -Y and dollies toward +Y.
# Crowd flows along X (screen left<->right) crossing in front of the arch.

# --- reflective metallic floor ---
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 6, 0.0))
fl = bpy.context.object; fl.name = 'floor'
fm, fb = new_mat('floor')
set_in(fb, 'Base Color', (0.015, 0.02, 0.035, 1))
set_in(fb, 'Metallic', 0.9)
set_in(fb, 'Roughness', 0.22)
fl.data.materials.append(fm)

# --- dark ceiling with slat GAPS (so spots read as banded skylight shafts) ---
ceil_mat, ceil_b = new_mat('ceil')
set_in(ceil_b, 'Base Color', (0.02, 0.03, 0.05, 1))
set_in(ceil_b, 'Metallic', 0.4); set_in(ceil_b, 'Roughness', 0.6)
CEIL_Z = 8.6
for yi in range(-3, 20):                 # slats span X, spaced along Y -> gaps
    y = yi * 1.6
    bpy.ops.mesh.primitive_cube_add(location=(0, y, CEIL_Z))
    sl = bpy.context.object
    sl.scale = (14.0, 0.55, 0.18)        # wide (X) thin (Y) -> light passes gaps
    sl.data.materials.append(ceil_mat)

# --- column material (dark brushed metal) ---
col_mat, col_b = new_mat('col')
set_in(col_b, 'Base Color', (0.03, 0.045, 0.07, 1))
set_in(col_b, 'Metallic', 0.85); set_in(col_b, 'Roughness', 0.35)

def column(x, y):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.42, depth=8.4,
                                        location=(x, y, 4.2))
    c = bpy.context.object
    c.data.materials.append(col_mat)
    # capital block
    bpy.ops.mesh.primitive_cube_add(location=(x, y, 8.3))
    cap = bpy.context.object; cap.scale = (0.62, 0.62, 0.22)
    cap.data.materials.append(col_mat)

for yi in range(0, 8):                   # two colonnades line the concourse
    y = -2 + yi * 3.2
    column(-6.2, y); column(6.2, y)

# --- security checkpoint ARCH(es): portal frame, NO signage/text ---
arch_mat, arch_b = new_mat('arch')
set_in(arch_b, 'Base Color', (0.05, 0.06, 0.085, 1))
set_in(arch_b, 'Metallic', 0.9); set_in(arch_b, 'Roughness', 0.28)
accent_mat, accent_b = new_mat('archAccent')
emissive(accent_b, ACC, 3.2)             # thin light strip (unbranded), adds luma
set_in(accent_b, 'Base Color', (*ACC, 1))

def checkpoint_arch(y, half_w=2.3, height=3.2):
    for sx in (-1, 1):                    # two posts
        bpy.ops.mesh.primitive_cube_add(location=(sx * half_w, y, height / 2))
        p = bpy.context.object; p.scale = (0.22, 0.30, height / 2)
        p.data.materials.append(arch_mat)
    # lintel beam across the top
    bpy.ops.mesh.primitive_cube_add(location=(0, y, height))
    ln = bpy.context.object; ln.scale = (half_w + 0.22, 0.30, 0.20)
    ln.data.materials.append(arch_mat)
    # thin emissive accent line under the lintel (light only, no text)
    bpy.ops.mesh.primitive_cube_add(location=(0, y - 0.30, height - 0.24))
    ac = bpy.context.object; ac.scale = (half_w, 0.03, 0.05)
    ac.data.materials.append(accent_mat)

checkpoint_arch(6.0)                      # near portal (hero focus)
checkpoint_arch(12.5)                     # far portal (depth)

# --- low divider rails flanking the checkpoint lane (guides the eye) ---
rail_mat, rail_b = new_mat('rail')
set_in(rail_b, 'Base Color', (0.04, 0.05, 0.075, 1))
set_in(rail_b, 'Metallic', 0.8); set_in(rail_b, 'Roughness', 0.4)
for sx in (-1, 1):
    bpy.ops.mesh.primitive_cube_add(location=(sx * 2.9, 8.5, 0.55))
    rr = bpy.context.object; rr.scale = (0.08, 2.4, 0.55)
    rr.data.materials.append(rail_mat)

# ================= VOLUMETRIC LIGHT-SHAFT DOMAIN =================
# Homogeneous Principled-Volume box enclosing the concourse; the SPOT lights
# below scatter through it -> visible skylight beams / god-rays.
bpy.ops.mesh.primitive_cube_add(location=(0, 7, 4.0))
dome = bpy.context.object; dome.name = 'volDomain'
dome.scale = (11.0, 15.0, 4.4)           # spans X:-11..11 Y:-8..22 Z:-0.4..8.4
dome.data.materials.append(volume_mat('shaftVol', SKY, VOL_DENSITY, 0.45))

# ================= CROWD: anonymous instanced silhouettes =================
# One low-poly figure template (faces NOT modeled); copies share the mesh data
# (true instancing). Two lanes flow LATERALLY in opposite directions = MAIN motion.
def build_figure():
    parts = []
    bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.21, radius2=0.12,
                                    depth=1.02, location=(0, 0, 0.75))  # torso
    parts.append(bpy.context.object)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=7, radius=0.22,
                                         location=(0, 0, 1.16))          # shoulders
    o = bpy.context.object; o.scale = (1.0, 0.62, 0.5); parts.append(o)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.155,
                                         location=(0, 0, 1.52))          # head (blank)
    parts.append(bpy.context.object)
    for lx in (-0.10, 0.10):                                             # legs
        bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=0.075, depth=0.62,
                                            location=(lx, 0, 0.24))
        parts.append(bpy.context.object)
    for p in parts:
        for f in p.data.polygons:
            f.use_smooth = True
    for ob in bpy.context.selected_objects:
        ob.select_set(False)
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    return bpy.context.active_object

# figure material: dark silhouette with a faint fill emission so it never fully
# crushes to black under AgX (raise emission strength if figures disappear).
fig_mat, fig_b = new_mat('figure')
set_in(fig_b, 'Base Color', (0.015, 0.02, 0.03, 1))
set_in(fig_b, 'Metallic', 0.0); set_in(fig_b, 'Roughness', 0.7)
emissive(fig_b, (0.05, 0.09, 0.16), 0.12)   # LUMA KNOB: faint fill so silhouettes read

fig_tpl = build_figure()
fig_tpl.name = 'figure_tpl'
fig_tpl.data.materials.clear()
fig_tpl.data.materials.append(fig_mat)
fig_tpl.hide_render = True                    # template itself not rendered
fig_tpl.location = (0, -50, 0)

def key_walk(obj, start_x, travel_x, band_y, phase, base_scale):
    """Deterministic lateral walk (+ subtle vertical bob), keyframed on 60fps."""
    obj.scale = (base_scale, base_scale, base_scale)
    if FE > FS:
        steps = list(range(FS, FE + 1, 8))
        if steps[-1] != FE:
            steps.append(FE)
        for f in steps:
            t = (f - FS) / (FE - FS)
            x = start_x + travel_x * t
            z = 0.06 * abs(math.sin(phase + t * math.tau * 5.0))   # step bob (feet stay >=0)
            obj.location = (x, band_y, z)
            obj.keyframe_insert('location', frame=f)
    else:
        obj.location = (start_x, band_y, 0.0)

CROWD_N = 32
for i in range(CROWD_N):
    lane = i % 2
    band_y = 2.0 + (i % 6) * 0.95 + random.uniform(-0.25, 0.25)   # depth spread 2.0..~7
    scale = random.uniform(0.9, 1.14)
    phase = random.uniform(0.0, math.tau)
    if lane == 0:                                                 # left -> right (+X)
        start_x = random.uniform(-12.0, 5.0)
        travel_x = random.uniform(11.0, 15.0)
    else:                                                         # right -> left (-X)
        start_x = random.uniform(-5.0, 12.0)
        travel_x = -random.uniform(11.0, 15.0)
    fig = fig_tpl.copy()                                          # shares mesh (instanced)
    coll.objects.link(fig)
    fig.hide_render = False
    fig.name = 'crowd_%02d' % i
    key_walk(fig, start_x, travel_x, band_y, phase, scale)

# ================= LIGHTS =================
# 3-point area (solid geometry read) — bpp_cycles.py pattern, energies uplifted.
def area(name, loc, energy, color, size=6, target=(0, 6, 1.2)):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    d = Vector(target) - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
area('key',  (7, -3, 6.5), 2400, (1.0, 0.98, 0.95), 7)   # LUMA KNOB
area('fill', (-7, 0, 3.0), 1200, ACC_HI, 8)              # LUMA KNOB
area('rim',  (-2, 14, 6.0), 1700, (0.6, 0.8, 1.0), 6)

# skylight SPOTS -> volumetric shafts through the ceiling-slat gaps.
def spot(name, loc, energy, color, size_deg=48, blend=0.35, target=(0, 0, 0)):
    ld = bpy.data.lights.new(name, 'SPOT'); ld.energy = energy; ld.color = color
    ld.spot_size = math.radians(size_deg); ld.spot_blend = blend
    try: ld.shadow_soft_size = 0.6
    except Exception: pass
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    d = Vector(target) - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob

# rows of shafts marching down the concourse; alternate side x-offset -> crossing beams.
for k, y in enumerate([0.0, 3.5, 7.0, 10.5, 14.0]):
    sx = -2.6 if k % 2 == 0 else 2.6
    tint = SKY if k % 2 == 0 else (0.95, 0.92, 0.82)   # cool / warm alternation
    spot('shaft_%d' % k, (sx, y - 1.5, 11.0), KEY_SPOT_E, tint,
         size_deg=46, blend=0.32, target=(sx * 0.25, y + 1.0, 0.0))

# ---- reflection softboxes (off camera) — bpp_cycles.py pattern ----
def softbox(loc, size, color, strength, target=(0, 6, 1.0)):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object
    m, b = new_mat('sb'); emissive(b, color, strength); o.data.materials.append(m)
    d = Vector(target) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
softbox((-9, -2, 3.2), 6, ACC_HI, 1.4)          # LUMA KNOB
softbox((9, 2, 3.0), 6, SKY, 1.1)               # LUMA KNOB
softbox((0, -8, 5.5), 7, (0.55, 0.72, 1.0), 0.85)

# ================= CAMERA: slow truck + dolly through the concourse =================
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam); scene.camera = cam
cd.lens = 40                                     # slightly wide -> concourse depth
cd.dof.use_dof = True
cd.dof.aperture_fstop = 3.5
tgt = bpy.data.objects.new('camTgt', None); tgt.location = (0, 6.2, 1.5); coll.objects.link(tgt)
cd.dof.focus_object = tgt
# TRACK_TO keeps framing on the near arch while the rig trucks/dollies (deterministic).
trk = cam.constraints.new('TRACK_TO'); trk.target = tgt
trk.track_axis = 'TRACK_NEGATIVE_Z'; trk.up_axis = 'UP_Y'

# Camera stays OUTSIDE the volume domain (near face Y=-8; see volDomain: center
# Y=7, Y-scale=15 -> Y spans -8..22) for the WHOLE move, so it looks INTO the
# volumetric god-rays rather than pushing the lens through dense fog. Keeping
# Y<=-9 (>=1 unit in front of the near face) both preserves contrast/shafts and
# avoids path-tracing thick near-camera volume (much faster). The X-truck
# (1.8 -> -1.4) + columns/crowd give the sense of moving through the concourse.
CAM_A = (1.8, -9.5, 1.7)     # start: off-axis, back of concourse (Y=-9.5, outside)
CAM_B = (-1.4, -9.0, 1.6)    # end: trucked left (X) + slight dolly (Y=-9.0, still outside fog)
if FE > FS:
    cam.location = CAM_A; cam.keyframe_insert('location', frame=FS)
    cam.location = CAM_B; cam.keyframe_insert('location', frame=FE)
else:
    cam.location = CAM_A

# ================= compositor bloom (Blender 5.x node group + socket API) =================
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

# ================= OUTPUT (PNG still or PNG sequence f_%04d.png) =================
scene.render.image_settings.file_format = 'PNG'
scene.frame_set(FS)
if FE == FS:
    scene.render.filepath = OUT + '_cyc.png'
    os.makedirs(os.path.dirname(os.path.abspath(OUT)) or '.', exist_ok=True)
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
