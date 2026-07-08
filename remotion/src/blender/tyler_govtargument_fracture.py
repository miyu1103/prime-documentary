"""EP33 tyler — HERO #4 GovtArgumentCard collapse — L3 Cycles ceiling (SUPER-HEAVY).

Bespoke subject: a stack of glass-edged argument SLABS (the county's surplus-
retention justification, OL4 / CLM-0006 related — abstract slabs, no readable
text so nothing reads as a record; invariant 11). A WIND force field ramps
95->0 over frames 1-18 and topples the stack via rigidbody physics
(substeps 20 / solver 20 / friction 0.35 / restitution 0.05, point-cache baked).
Camera pushes in on the collapse; dust volume drifts after. The 13:20 payoff.

ARGV: blender -b -P tyler_govtargument_fracture.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
TEST (frame-1 smoke = intact stack): ... out/hero_govt 3840 2160 1 1 200
FULL (physics needs the full range): ... out/hero_govt 3840 2160 1 240 160
"""

import bpy, sys, math, os, random
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 3840)), int(A(2, 2160))
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 160))
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
def rb(obj, kind, shape, mass=1.0, friction=0.35, restitution=0.05):
    bpy.context.view_layer.objects.active = obj
    for o in bpy.context.selected_objects: o.select_set(False)
    obj.select_set(True); bpy.ops.rigidbody.object_add()
    obj.rigid_body.type = kind; obj.rigid_body.collision_shape = shape
    obj.rigid_body.mass = mass; obj.rigid_body.friction = friction; obj.rigid_body.restitution = restitution
    if kind == 'ACTIVE':
        obj.rigid_body.linear_damping = 0.12; obj.rigid_body.angular_damping = 0.2
        obj.rigid_body.use_margin = True; obj.rigid_body.collision_margin = 0.006

FLOOR_Z = -2.0
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, FLOOR_Z))
floor = bpy.context.object; fm, fb = new_mat('floor')
set_in(fb, 'Base Color', (0.01, 0.015, 0.03, 1)); set_in(fb, 'Metallic', 0.9); set_in(fb, 'Roughness', 0.22)
floor.data.materials.append(fm)
rb(floor, 'PASSIVE', 'BOX', friction=0.6)

# ---- stacked argument slabs (glass-edged, emissive rims) -------------------
SLABS = 4
SX, SY, SZ = 3.0, 0.9, 0.34
slab_objs = []
for i in range(SLABS):
    z = FLOOR_Z + SZ / 2 + i * (SZ + 0.02)
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, z))
    s = bpy.context.object; s.name = 'slab_%02d' % i
    s.scale = (SX / 2, SY / 2, SZ / 2)
    bev = s.modifiers.new('bev', 'BEVEL'); bev.width = 0.02; bev.segments = 2
    m, b = new_mat('slab_%02d' % i)
    set_in(b, 'Base Color', (0.06, 0.12, 0.22, 1)); set_in(b, 'Metallic', 0.2); set_in(b, 'Roughness', 0.32)
    emissive(b, ACC_HI, 0.9)
    s.data.materials.append(m)
    rb(s, 'ACTIVE', 'BOX', mass=1.2)
    slab_objs.append(s)

# ---- WIND force field that topples the stack (strength 95 -> 0) ------------
bpy.ops.object.effector_add(type='WIND', location=(-6, 0, FLOOR_Z + 1.5))
wind = bpy.context.object; wind.name = 'wind'
wind.rotation_euler = (0, math.radians(90), 0)   # blow along +X toward the stack
wind.field.strength = 95.0
wind.field.flow = 0.4

# ---- rigidbody world + BAKE ----
rw = scene.rigidbody_world
rw.substeps_per_frame = 20; rw.solver_iterations = 20
rw.point_cache.frame_start = 1; rw.point_cache.frame_end = max(FE, FS)
if FE > FS:
    # keyframe wind strength 95 -> 0 across frames 1..18 (topple, then stop pushing)
    wind.field.strength = 95.0
    wind.field.keyframe_insert('strength', frame=1)
    wind.field.strength = 0.0
    wind.field.keyframe_insert('strength', frame=18)
scene.frame_set(FS)
try:
    bpy.ops.ptcache.bake_all(bake=True); print('BAKED', rw.point_cache.frame_start, '..', rw.point_cache.frame_end)
except Exception as e:
    print('bake err', e)

# ---- lights + softboxes ----
def area(name, loc, energy, color, size=6, target=Vector((0, 0, FLOOR_Z + 0.8))):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    ob.rotation_euler = (target - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
area('key', (5, -5, 6), 2200, (1.0, 0.98, 0.92), 6)
area('fill', (-6, -3, 2), 950, ACC_HI, 7)
area('rim', (-2, 5, 5), 1600, (0.6, 0.8, 1.0), 5)
def softbox(loc, size, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object; m, b = new_mat('sb'); emissive(b, color, strength); o.data.materials.append(m)
    o.rotation_euler = (Vector((0, 0, FLOOR_Z + 0.8)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
softbox((-8, -5, 3), 5, ACC_HI, 1.4); softbox((8, -5, 2.5), 5, (0.9, 0.94, 1.0), 1.1); softbox((0, -9, 5), 6, (0.7, 0.82, 1.0), 0.8)

# ---- drifting dust volume domain (post-collapse haze) ----
bpy.ops.mesh.primitive_cube_add(size=16, location=(1.5, 0, FLOOR_Z + 1.5))
vol = bpy.context.object; vm = bpy.data.materials.new('dustvol'); vm.use_nodes = True
vnt = vm.node_tree
for n in list(vnt.nodes):
    if n.type == 'BSDF_PRINCIPLED': vnt.nodes.remove(n)
pv = vnt.nodes.new('ShaderNodeVolumePrincipled'); pv.inputs['Density'].default_value = 0.012
vnt.links.new(pv.outputs['Volume'], vnt.nodes.get('Material Output').inputs['Volume'])
vol.data.materials.append(vm)

# ---- camera push-in on the collapse ----
LOOK = Vector((0.5, 0, FLOOR_Z + 0.9))
CAM_START = Vector((3.0, -9.0, 1.6)); CAM_END = Vector((2.2, -6.6, 1.2))
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); coll.objects.link(cam); scene.camera = cam
cd.lens = 50; cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.6
cam.location = CAM_START; cam.rotation_euler = (LOOK - CAM_START).to_track_quat('-Z', 'Y').to_euler()
cd.dof.focus_distance = (CAM_START - LOOK).length
if FE > FS:
    zoomf = FS + 20
    cam.location = CAM_START; cam.keyframe_insert('location', frame=FS)
    cam.location = CAM_END; cam.keyframe_insert('location', frame=FE)
    cam.rotation_euler = (LOOK - CAM_START).to_track_quat('-Z', 'Y').to_euler(); cam.keyframe_insert('rotation_euler', frame=FS)
    cam.rotation_euler = (LOOK - CAM_END).to_track_quat('-Z', 'Y').to_euler(); cam.keyframe_insert('rotation_euler', frame=FE)
    cd.dof.focus_distance = (CAM_START - LOOK).length; cd.dof.keyframe_insert('focus_distance', frame=FS)
    cd.dof.focus_distance = (CAM_END - LOOK).length; cd.dof.keyframe_insert('focus_distance', frame=FE)
    # zoompunch at collapse ignition
    cd.lens = 50; cd.keyframe_insert('lens', frame=zoomf - 4)
    cd.lens = 44; cd.keyframe_insert('lens', frame=zoomf)
    cd.lens = 50; cd.keyframe_insert('lens', frame=zoomf + 8)
    for ob in (cam, cd):
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
