"""EP33 tyler — HERO #2 EquityBar — L3 Cycles ceiling scene (SUPER-HEAVY tier).

Bespoke subject: three 3D extruded bars — DEBT $15,000 (grey) / SALE $40,000
(green) / SURPLUS $25,000 (red) — heights proportional to value, each capped by
a 3D extruded data number. Camera rack-focuses bar to bar (55mm dolly, DOF
fstop 2.2); the red SURPLUS bar seats last with a lens micro-punch (the 4:50
$25,000 payoff). Cool volumetric god-ray haze. Figures are the case's own data
(T7 / CLM-0004/0005); no likeness, no logos (invariant 11).

ARGV: blender -b -P tyler_equitybar.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
TEST: blender -b -P remotion/src/blender/tyler_equitybar.py -- out/hero_equitybar 3840 2160 1 1 200
FULL: blender -b -P remotion/src/blender/tyler_equitybar.py -- out/hero_equitybar 3840 2160 1 300 200
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
scene.render.fps = 30; scene.frame_start, scene.frame_end = FS, FE
scene.view_settings.view_transform = 'AgX'
try:  # Blender 5.x: guarantee non-linear (bezier/auto-clamped) keyframes by default
    _ep = bpy.context.preferences.edit
    _ep.keyframe_new_interpolation_type = 'BEZIER'
    _ep.keyframe_new_handle_type = 'AUTO_CLAMPED'
except Exception: pass
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
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, FLOOR_Z))
floor = bpy.context.object; fm, fb = new_mat('floor')
set_in(fb, 'Base Color', (0.01, 0.015, 0.03, 1)); set_in(fb, 'Metallic', 0.9); set_in(fb, 'Roughness', 0.22)
floor.data.materials.append(fm)

# ---- bespoke subject: three extruded bars + capped numbers ------------------
BARS = [
    ('DEBT',    '$15,000', 15000, (0.55, 0.58, 0.63), -3.0),
    ('SALE',    '$40,000', 40000, (0.20, 0.70, 0.35),  0.0),
    ('SURPLUS', '$25,000', 25000, (0.90, 0.24, 0.24),  3.0),
]
HMAX = 4.2          # world height for the tallest ($40,000)
BW = 1.5
bar_objs = []
for name, glyph, val, col, x in BARS:
    h = HMAX * (val / 40000.0)
    bpy.ops.mesh.primitive_cube_add(location=(x, 0, FLOOR_Z + h / 2))
    b = bpy.context.object; b.name = 'bar_%s' % name
    b.scale = (BW / 2, BW / 2, h / 2)
    bev = b.modifiers.new('bev', 'BEVEL'); bev.width = 0.03; bev.segments = 2
    m, bb = new_mat('bar_%s' % name)
    set_in(bb, 'Base Color', col + (1,)); set_in(bb, 'Metallic', 0.3); set_in(bb, 'Roughness', 0.4)
    emissive(bb, col, 0.6)
    b.data.materials.append(m)
    bar_objs.append((b, FLOOR_Z + h))
    # capped 3D number
    bpy.ops.object.text_add(location=(x, 0, FLOOR_Z + h + 0.5))
    t = bpy.context.object; t.data.body = glyph
    t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.size = 0.55
    t.data.extrude = 0.05; t.data.bevel_depth = 0.006
    t.rotation_euler = (math.pi / 2, 0, 0)
    tm, tb = new_mat('num_%s' % name); set_in(tb, 'Base Color', (0.96, 0.97, 1.0, 1)); emissive(tb, (0.9, 0.95, 1.0), 1.0)
    t.data.materials.append(tm)
    # base label
    bpy.ops.object.text_add(location=(x, 0, FLOOR_Z + 0.18))
    lb = bpy.context.object; lb.data.body = name
    lb.data.align_x = 'CENTER'; lb.data.align_y = 'CENTER'; lb.data.size = 0.32
    lb.data.extrude = 0.03; lb.rotation_euler = (math.pi / 2, 0, 0)
    lm, lbb = new_mat('lab_%s' % name); set_in(lbb, 'Base Color', (0.8, 0.84, 0.9, 1)); emissive(lbb, (0.7, 0.8, 0.95), 0.5)
    lb.data.materials.append(lm)

# ---- thin volumetric haze ----
bpy.ops.mesh.primitive_cube_add(size=18, location=(0, 0, 1.2))
vol = bpy.context.object; vm = bpy.data.materials.new('haze'); vm.use_nodes = True
vnt = vm.node_tree
for n in list(vnt.nodes):
    if n.type == 'BSDF_PRINCIPLED': vnt.nodes.remove(n)
pv = vnt.nodes.new('ShaderNodeVolumePrincipled'); pv.inputs['Density'].default_value = 0.010
vnt.links.new(pv.outputs['Volume'], vnt.nodes.get('Material Output').inputs['Volume'])
vol.data.materials.append(vm)

# ---- 3-point lights + softboxes ----
def area(name, loc, energy, color, size=6, target=Vector((0, 0, 0.6))):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    ob.rotation_euler = (target - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
area('key', (6, -6, 6), 2400, (1.0, 0.98, 0.92), 7)
area('fill', (-7, -3, 2), 1000, ACC_HI, 8)
area('rim', (-2, 5, 6), 1700, (0.6, 0.8, 1.0), 6)
def softbox(loc, size, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object; m, b = new_mat('sb'); emissive(b, color, strength); o.data.materials.append(m)
    o.rotation_euler = (Vector((0, 0, 0.6)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
softbox((-9, -6, 3), 5, ACC_HI, 1.3); softbox((9, -6, 2.5), 5, (0.9, 0.94, 1.0), 1.0); softbox((0, -10, 6), 6, (0.7, 0.82, 1.0), 0.8)

# ---- camera + DOF rack focus (bar to bar) ----
FOCI = [Vector((x, 0, FLOOR_Z + 1.0)) for *_, x in [(b) for b in BARS]]
SURPLUS_C = Vector((3.0, 0, FLOOR_Z + HMAX * 25000 / 40000 / 2))
CAM_START = Vector((-1.6, -15.5, 3.2)); CAM_END = Vector((1.2, -13.0, 2.6))
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); coll.objects.link(cam); scene.camera = cam
cd.lens = 42; cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.6   # wider + back so all 3 bars + numbers fit
LOOK = Vector((0, 0, FLOOR_Z + 1.9))
cam.location = CAM_START; cam.rotation_euler = (LOOK - CAM_START).to_track_quat('-Z', 'Y').to_euler()
cd.dof.focus_distance = (CAM_START - Vector((-3.0, 0, 0))).length

if FE > FS:
    slam = FS + int((FE - FS) * 0.80)
    cam.location = CAM_START; cam.keyframe_insert('location', frame=FS)
    cam.rotation_euler = (LOOK - CAM_START).to_track_quat('-Z', 'Y').to_euler(); cam.keyframe_insert('rotation_euler', frame=FS)
    cam.location = CAM_END; cam.keyframe_insert('location', frame=FE)
    cam.rotation_euler = (LOOK - CAM_END).to_track_quat('-Z', 'Y').to_euler(); cam.keyframe_insert('rotation_euler', frame=FE)
    # rack focus: DEBT -> SALE -> SURPLUS
    cd.dof.focus_distance = (CAM_START - FOCI[0]).length; cd.dof.keyframe_insert('focus_distance', frame=FS)
    cd.dof.focus_distance = (CAM_START.lerp(CAM_END, 0.5) - FOCI[1]).length; cd.dof.keyframe_insert('focus_distance', frame=FS + int((FE - FS) * 0.5))
    cd.dof.focus_distance = (CAM_END - SURPLUS_C).length; cd.dof.keyframe_insert('focus_distance', frame=FE)
    # SURPLUS bar seat pop (scale z) + lens punch
    surb = bar_objs[2][0]
    surb.scale = (BW / 2, BW / 2, 0.02); surb.keyframe_insert('scale', frame=slam - 10)
    surb.scale = (BW / 2, BW / 2, HMAX * 25000 / 40000 / 2 * 1.04); surb.keyframe_insert('scale', frame=slam)
    surb.scale = (BW / 2, BW / 2, HMAX * 25000 / 40000 / 2); surb.keyframe_insert('scale', frame=slam + 8)
    cd.lens = 55; cd.keyframe_insert('lens', frame=slam - 4)
    cd.lens = 51; cd.keyframe_insert('lens', frame=slam)
    cd.lens = 55; cd.keyframe_insert('lens', frame=slam + 6)
    for ob in (cam, cd, bar_objs[2][0]):
        ad = ob.animation_data
        if ad and ad.action:
            for fc in getattr(ad.action, 'fcurves', []):
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
    sock('Quality', 'High'); sock('Highlights Threshold', 0.8); sock('Strength', 1.0); sock('Size', 0.8)
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
