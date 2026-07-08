"""EP33 tyler — HERO #3 EquityTheftTally national map — L3 Cycles ceiling (SUPER-HEAVY).

Bespoke subject: an abstract continental-US silhouette slab on a dark reflective
ground, seeded with ~8,000 emissive point instances (one glowing mote = one lost
home; the count is a VISUAL expression of the PLF "Est." scale, not a factual
assertion — invariant 11). Aerial camera sweeps down over the field. The dense
national glow conveys the $780M+ scale; the running counter / accumulation lives
in the Remotion 2D companion (components/tyler/EquityTheftTally.tsx). No text,
no likeness, no logos.

ARGV: blender -b -P tyler_equitytheft_map.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
TEST: blender -b -P remotion/src/blender/tyler_equitytheft_map.py -- out/hero_map 3840 2160 1 1 200
FULL: blender -b -P remotion/src/blender/tyler_equitytheft_map.py -- out/hero_map 3840 2160 1 420 200
"""

import bpy, sys, math, os, random, bmesh
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
bg.inputs[0].default_value = (0.010, 0.016, 0.03, 1); bg.inputs[1].default_value = 0.4

def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree.nodes.get('Principled BSDF')
def set_in(b, n, v):
    if n in b.inputs: b.inputs[n].default_value = v; return True
    return False
def emissive(b, color, strength):
    if not set_in(b, 'Emission Color', (*color, 1)): set_in(b, 'Emission', (*color, 1))
    set_in(b, 'Emission Strength', strength)

FLOOR_Z = -0.2
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, FLOOR_Z - 0.05))
floor = bpy.context.object; fm, fb = new_mat('floor')
set_in(fb, 'Base Color', (0.008, 0.012, 0.025, 1)); set_in(fb, 'Metallic', 0.85); set_in(fb, 'Roughness', 0.3)
floor.data.materials.append(fm)

# ---- abstract US silhouette slab (filled ngon from an outline) --------------
# Outline in XY (world units), abstract low-poly — NOT a precise geographic map.
OUTLINE = [
    (-8.0, 0.4), (-7.2, 1.6), (-5.0, 2.3), (-2.0, 2.6), (1.5, 2.9), (5.0, 2.5),
    (7.0, 2.0), (7.9, 1.2), (7.6, 0.4), (6.9, 0.1), (6.4, 0.6), (6.0, 1.2),
    (5.2, 1.0), (4.0, 0.5), (2.5, 0.1), (0.5, -0.3), (-1.5, -0.2), (-3.5, -0.6),
    (-5.2, -0.9), (-6.6, -0.7), (-7.6, -0.2),
]
mesh = bpy.data.meshes.new('us'); usobj = bpy.data.objects.new('us', mesh); coll.objects.link(usobj)
bm = bmesh.new()
verts = [bm.verts.new((x, y, FLOOR_Z)) for (x, y) in OUTLINE]
try:
    bm.faces.new(verts)
except Exception as e:
    print('face err', e)
bmesh.ops.triangulate(bm, faces=bm.faces[:])
bm.to_mesh(mesh); bm.free()
sm, sb = new_mat('us'); set_in(sb, 'Base Color', (0.04, 0.08, 0.14, 1)); set_in(sb, 'Metallic', 0.4); set_in(sb, 'Roughness', 0.45)
emissive(sb, ACC_HI, 0.25)
usobj.data.materials.append(sm)
# faint raised border (solidify) for relief
sol = usobj.modifiers.new('sol', 'SOLIDIFY'); sol.thickness = 0.08; sol.offset = 1.0

# ---- ~8,000 emissive motes as a particle system on the US slab -------------
# one instance object (tiny emissive ico), instanced over the slab faces.
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.045, location=(0, 0, -50))
mote = bpy.context.object; mote.name = 'mote'
for p in mote.data.polygons: p.use_smooth = True
mm, mb = new_mat('mote'); set_in(mb, 'Base Color', GOLD + (1,)); emissive(mb, GOLD, 3.2)
mote.data.materials.append(mm)

bpy.context.view_layer.objects.active = usobj
ps = usobj.modifiers.new('motes', 'PARTICLE_SYSTEM')
pset = usobj.particle_systems[0].settings
pset.count = 8000
pset.frame_start = 1; pset.frame_end = max(1, FE)   # accumulate over the shot
pset.lifetime = 100000
pset.emit_from = 'FACE'; pset.use_emit_random = True
pset.distribution = 'RAND'
pset.physics_type = 'NO'
pset.render_type = 'OBJECT'; pset.instance_object = mote
pset.particle_size = 1.0; pset.size_random = 0.5
try: pset.seed = 1234
except Exception: pass
usobj.particle_systems[0].seed = 1234
# raise motes slightly above the slab so they read as points of light
pset.normal_factor = 0.06

# ---- lights (top-down + rim) ----
def area(name, loc, energy, color, size=8, target=Vector((0, 0, 0))):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    ob.rotation_euler = (target - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
area('key', (2, -6, 12), 1600, (0.8, 0.88, 1.0), 12)
area('rim', (-8, 6, 6), 1200, ACC_HI, 8)

# ---- thin atmospheric haze over the terrain ----
bpy.ops.mesh.primitive_cube_add(size=30, location=(0, 0, 2.0))
vol = bpy.context.object; vm = bpy.data.materials.new('haze'); vm.use_nodes = True
vnt = vm.node_tree
for n in list(vnt.nodes):
    if n.type == 'BSDF_PRINCIPLED': vnt.nodes.remove(n)
pv = vnt.nodes.new('ShaderNodeVolumePrincipled'); pv.inputs['Density'].default_value = 0.008
vnt.links.new(pv.outputs['Volume'], vnt.nodes.get('Material Output').inputs['Volume'])
vol.data.materials.append(vm)

# ---- aerial camera sweep-down ----
LOOK = Vector((0, 0.8, FLOOR_Z))
CAM_START = Vector((0, -13, 14)); CAM_END = Vector((0, -8.5, 8))
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); coll.objects.link(cam); scene.camera = cam
cd.lens = 42; cd.dof.use_dof = True; cd.dof.aperture_fstop = 3.2
cam.location = CAM_START; cam.rotation_euler = (LOOK - CAM_START).to_track_quat('-Z', 'Y').to_euler()
cd.dof.focus_distance = (CAM_START - LOOK).length
if FE > FS:
    cam.location = CAM_START; cam.keyframe_insert('location', frame=FS)
    cam.rotation_euler = (LOOK - CAM_START).to_track_quat('-Z', 'Y').to_euler(); cam.keyframe_insert('rotation_euler', frame=FS)
    cam.location = CAM_END; cam.keyframe_insert('location', frame=FE)
    cam.rotation_euler = (LOOK - CAM_END).to_track_quat('-Z', 'Y').to_euler(); cam.keyframe_insert('rotation_euler', frame=FE)
    cd.dof.focus_distance = (CAM_START - LOOK).length; cd.dof.keyframe_insert('focus_distance', frame=FS)
    cd.dof.focus_distance = (CAM_END - LOOK).length; cd.dof.keyframe_insert('focus_distance', frame=FE)
    for ob in (cam, cd):
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
    sock('Quality', 'High'); sock('Highlights Threshold', 0.75); sock('Strength', 1.0); sock('Size', 0.85)
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

# ensure particle system is evaluated at the render frame
scene.frame_set(FE)

scene.render.image_settings.file_format = 'PNG'
if FE == FS:
    os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
    scene.render.filepath = OUT + '_test.png'; bpy.ops.render.render(write_still=True); print('WROTE', scene.render.filepath)
else:
    os.makedirs(OUT, exist_ok=True); scene.render.filepath = OUT + '/f_'; bpy.ops.render.render(animation=True); print('WROTE SEQ', OUT)
