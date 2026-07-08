"""EP33 tyler — HERO #6 VoteTally 9-0 bench — L3 Cycles ceiling (SUPER-HEAVY).

Bespoke subject: an abstract nine-seat court bench (a long curved desk with nine
raised seat blocks). A dolly reveal travels the bench; the nine seats fill
directionally, then at ~18:15 all nine IGNITE simultaneously with a single hard
impact (unanimous 9-0, T18 / CLM-0010). Cool volumetric shafts. The 9-0 / "598
U.S. 631" glyphs are added in the Remotion VoteTally layer; this render stays an
abstract court tableau — no likeness, no readable text, no logos (invariant 11).

ARGV: blender -b -P tyler_votetally_bench.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
TEST: blender -b -P remotion/src/blender/tyler_votetally_bench.py -- out/hero_vote 3840 2160 1 1 200
FULL: blender -b -P remotion/src/blender/tyler_votetally_bench.py -- out/hero_vote 3840 2160 1 300 200
"""

import bpy, sys, math, os, random
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 3840)), int(A(2, 2160))
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 200))
ACC_HI = (0.35, 0.70, 1.0)
GOLD = (0.95, 0.72, 0.22)
random.seed(1234)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene; coll = scene.collection

scene.render.engine = 'CYCLES'
prefs = bpy.context.preferences.addons['cycles'].preferences
picked = 'CPU'
for dt in ['OPTIX', 'CUDA', 'HIP', 'ONEAPI']:
    try:
        prefs.compute_device_type = dt; prefs.get_devices()
        if any(d.type != 'CPU' for d in prefs.devices):
            for d in prefs.devices: d.use = True
            scene.cycles.device = 'GPU'; picked = dt; break
    except Exception as e:
        print('gpu try', dt, e)
print('CYCLES device =', picked)
scene.cycles.samples = SAMPLES; scene.cycles.use_denoising = True
try: scene.cycles.caustics_reflective = False; scene.cycles.caustics_refractive = False
except Exception: pass
scene.render.resolution_x = RX; scene.render.resolution_y = RY; scene.render.resolution_percentage = 100
scene.render.fps = 60; scene.frame_start, scene.frame_end = FS, FE
scene.view_settings.view_transform = 'AgX'
scene.render.use_motion_blur = True; scene.render.motion_blur_shutter = 0.5
try: scene.cycles.rolling_shutter_type = 'NONE'
except Exception: pass

world = bpy.data.worlds.new('W'); scene.world = world; world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
bg.inputs[0].default_value = (0.012, 0.02, 0.04, 1); bg.inputs[1].default_value = 0.5

def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree.nodes.get('Principled BSDF')
def set_in(b, n, v):
    if n in b.inputs: b.inputs[n].default_value = v; return True
    return False
def emissive(b, color, strength):
    if not set_in(b, 'Emission Color', (*color, 1)): set_in(b, 'Emission', (*color, 1))
    set_in(b, 'Emission Strength', strength)

FLOOR_Z = -2.0
bpy.ops.mesh.primitive_plane_add(size=50, location=(0, 0, FLOOR_Z))
floor = bpy.context.object; fm, fb = new_mat('floor')
set_in(fb, 'Base Color', (0.01, 0.015, 0.03, 1)); set_in(fb, 'Metallic', 0.85); set_in(fb, 'Roughness', 0.26)
floor.data.materials.append(fm)

# ---- the bench (a long slightly-curved desk) ----
bench_mat, bmb = new_mat('bench')
set_in(bmb, 'Base Color', (0.10, 0.06, 0.03, 1)); set_in(bmb, 'Metallic', 0.2); set_in(bmb, 'Roughness', 0.35)
N = 9
seats = []
seat_bs = []
CURVE = 0.9   # subtle arc toward camera at the ends
for i in range(N):
    x = (i - (N - 1) / 2) * 1.35
    y = CURVE * (abs(i - (N - 1) / 2) / ((N - 1) / 2)) ** 2   # ends closer to camera (-Y)
    y = -y
    # desk segment
    bpy.ops.mesh.primitive_cube_add(location=(x, y, FLOOR_Z + 0.55))
    seg = bpy.context.object; seg.scale = (0.66, 0.5, 0.55)
    bev = seg.modifiers.new('bev', 'BEVEL'); bev.width = 0.03; bev.segments = 2
    seg.data.materials.append(bench_mat)
    # seat marker (raised emissive block behind the desk)
    bpy.ops.mesh.primitive_cube_add(location=(x, y + 0.1, FLOOR_Z + 1.5))
    st = bpy.context.object; st.name = 'seat_%02d' % i; st.scale = (0.34, 0.2, 0.5)
    sm, sb = new_mat('seat_%02d' % i)
    set_in(sb, 'Base Color', (0.06, 0.10, 0.18, 1)); set_in(sb, 'Metallic', 0.3); set_in(sb, 'Roughness', 0.3)
    emissive(sb, ACC_HI, 0.2)   # dim until it fills / ignites
    st.data.materials.append(sm)
    seats.append(st); seat_bs.append(sb)

# ---- volumetric court shafts (cool) ----
bpy.ops.mesh.primitive_cube_add(size=24, location=(0, 0, 1.5))
vol = bpy.context.object; vm = bpy.data.materials.new('haze'); vm.use_nodes = True
vnt = vm.node_tree
for n in list(vnt.nodes):
    if n.type == 'BSDF_PRINCIPLED': vnt.nodes.remove(n)
pv = vnt.nodes.new('ShaderNodeVolumePrincipled'); pv.inputs['Density'].default_value = 0.010
vnt.links.new(pv.outputs['Volume'], vnt.nodes.get('Material Output').inputs['Volume'])
vol.data.materials.append(vm)

# ---- lights: high raking shafts ----
sp = bpy.data.lights.new('shaft', 'SPOT'); sp.energy = 4200; sp.spot_size = math.radians(60); sp.color = (0.7, 0.82, 1.0)
spo = bpy.data.objects.new('shaft', sp); spo.location = (-3, -7, 9); coll.objects.link(spo)
spo.rotation_euler = (Vector((0, 0, FLOOR_Z + 1.0)) - Vector(spo.location)).to_track_quat('-Z', 'Y').to_euler()
def area(name, loc, energy, color, size=6, target=Vector((0, 0, FLOOR_Z + 1.0))):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    ob.rotation_euler = (target - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
area('key', (6, -6, 6), 2000, (1.0, 0.98, 0.92), 7)
area('fill', (-7, -3, 2), 900, ACC_HI, 8)

# ---- directional seat fill + simultaneous ignition ----
if FE > FS:
    ignite = FS + int((FE - FS) * 0.82)   # ~18:15 all-nine ignition
    for i, sb in enumerate(seat_bs):
        # each seat fills (rises in emission) in sequence L->R before ignition
        fill_f = FS + int((ignite - FS) * (0.15 + 0.6 * i / (N - 1)))
        def key_em(strength, frame):
            inp = sb.inputs.get('Emission Strength')
            if inp is not None:
                inp.default_value = strength; inp.keyframe_insert('default_value', frame=frame)
        key_em(0.2, FS)
        key_em(0.9, fill_f)            # directional fill (blue)
        key_em(0.9, ignite - 2)
        # ignition: swap to gold + hard bright
        col = sb.inputs.get('Emission Color') or sb.inputs.get('Emission')
        if col is not None:
            col.default_value = (*ACC_HI, 1); col.keyframe_insert('default_value', frame=ignite - 2)
            col.default_value = (*GOLD, 1); col.keyframe_insert('default_value', frame=ignite)
        key_em(6.0, ignite)            # hard impact flash
        key_em(2.6, ignite + 10)       # settle to a firm hold (not dark)
    # seat pop-up scale at ignition (single hard impact)
    for st in seats:
        base = st.scale.copy()
        st.scale = base; st.keyframe_insert('scale', frame=ignite - 3)
        st.scale = (base.x * 1.06, base.y * 1.06, base.z * 1.1); st.keyframe_insert('scale', frame=ignite)
        st.scale = base; st.keyframe_insert('scale', frame=ignite + 8)

# ---- camera dolly reveal across the bench ----
LOOK = Vector((0, 0, FLOOR_Z + 1.2))
CAM_START = Vector((-6.5, -8.5, 1.8)); CAM_END = Vector((0.5, -7.5, 1.5))
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); coll.objects.link(cam); scene.camera = cam
cd.lens = 40; cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.8
cam.location = CAM_START; cam.rotation_euler = (LOOK - CAM_START).to_track_quat('-Z', 'Y').to_euler()
cd.dof.focus_distance = (CAM_START - LOOK).length
if FE > FS:
    ignite = FS + int((FE - FS) * 0.82)
    cam.location = CAM_START; cam.keyframe_insert('location', frame=FS)
    cam.location = CAM_END; cam.keyframe_insert('location', frame=FE)
    cam.rotation_euler = (LOOK - CAM_START).to_track_quat('-Z', 'Y').to_euler(); cam.keyframe_insert('rotation_euler', frame=FS)
    cam.rotation_euler = (LOOK - CAM_END).to_track_quat('-Z', 'Y').to_euler(); cam.keyframe_insert('rotation_euler', frame=FE)
    cd.dof.focus_distance = (CAM_START - LOOK).length; cd.dof.keyframe_insert('focus_distance', frame=FS)
    cd.dof.focus_distance = (CAM_END - LOOK).length; cd.dof.keyframe_insert('focus_distance', frame=FE)
    cd.lens = 40; cd.keyframe_insert('lens', frame=ignite - 3)
    cd.lens = 37; cd.keyframe_insert('lens', frame=ignite)     # snap-in at ignition
    cd.lens = 40; cd.keyframe_insert('lens', frame=ignite + 8)
    for ob in [cam, cd] + seats:
        ad = ob.animation_data
        if ad and ad.action:
            for fc in ad.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = 'BEZIER'; kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'

def setup_bloom(scene):
    nt = None
    try: scene.use_nodes = True; nt = scene.node_tree
    except Exception: nt = None
    if nt is None and hasattr(scene, 'compositing_node_group'):
        ng = bpy.data.node_groups.new('comp', 'CompositorNodeTree')
        scene.compositing_node_group = ng; nt = ng
    if nt is None: print('BLOOM: skip'); return
    for n in list(nt.nodes): nt.nodes.remove(n)
    rl = nt.nodes.new('CompositorNodeRLayers'); gl = nt.nodes.new('CompositorNodeGlare')
    def sock(name, val):
        if name in gl.inputs:
            try: gl.inputs[name].default_value = val
            except Exception as e: print('sock', name, e)
    if 'Type' in gl.inputs:
        try: gl.inputs['Type'].default_value = 'Bloom'
        except Exception: sock('Type', 'Fog Glow')
    sock('Quality', 'High'); sock('Highlights Threshold', 0.78); sock('Strength', 1.0); sock('Size', 0.85)
    try: gl.glare_type = 'BLOOM'
    except Exception: pass
    nt.links.new(rl.outputs['Image'], gl.inputs['Image'])
    out = None
    try: out = nt.nodes.new('CompositorNodeComposite')
    except Exception: pass
    if out is not None:
        nt.links.new(gl.outputs['Image'], out.inputs['Image'])
    else:
        go = nt.nodes.new('NodeGroupOutput')
        nt.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
        nt.links.new(gl.outputs['Image'], go.inputs[0])
    print('BLOOM: ok')
setup_bloom(scene)

scene.render.image_settings.file_format = 'PNG'
if FE == FS:
    os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
    scene.render.filepath = OUT + '_test.png'; bpy.ops.render.render(write_still=True); print('WROTE', scene.render.filepath)
else:
    os.makedirs(OUT, exist_ok=True); scene.render.filepath = OUT + '/f_'; bpy.ops.render.render(animation=True); print('WROTE SEQ', OUT)
