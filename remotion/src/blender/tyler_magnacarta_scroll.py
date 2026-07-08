"""EP33 tyler — HERO #5 MagnaCartaScroll — L3 Cycles ceiling (SUPER-HEAVY).

Bespoke subject: a parchment scroll that UNFURLS via cloth simulation — a
subdivided plane with a top-edge pin group, gravity + a weak wind, wrapped
around a wooden dowel. Parchment material is warm, rough, translucent (SSS).
Warm dusty god-ray shafts + drifting motes. Camera dollies along the unfurling
sheet. The 800-year source of the surplus-return principle (Magna Carta 1215,
T15 / CLM-0014A). NO readable text baked (the Latin stroke-trace + translation
is added in the Remotion layer / TerminalType); invariant 11 keeps the render an
abstract reproduction, not a facsimile record.

ARGV: blender -b -P tyler_magnacarta_scroll.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
TEST (frame-1 smoke = furled): ... out/hero_scroll 3840 2160 1 1 200
FULL (cloth needs the range): ... out/hero_scroll 3840 2160 1 300 200
"""

import bpy, sys, math, os, random
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 3840)), int(A(2, 2160))
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 200))
WARM = (1.0, 0.78, 0.45)
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
bg.inputs[0].default_value = (0.03, 0.02, 0.012, 1); bg.inputs[1].default_value = 0.5   # warm dark

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
set_in(fb, 'Base Color', (0.03, 0.022, 0.012, 1)); set_in(fb, 'Metallic', 0.3); set_in(fb, 'Roughness', 0.5)
floor.data.materials.append(fm)

# ---- wooden dowel at the top (the scroll rod) ----
bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=4.2, location=(0, 0, 2.4))
dowel = bpy.context.object; dowel.rotation_euler = (0, math.radians(90), 0)
dm, db = new_mat('dowel'); set_in(db, 'Base Color', (0.18, 0.09, 0.03, 1)); set_in(db, 'Roughness', 0.6)
dowel.data.materials.append(dm)

# ---- parchment sheet (cloth) ----
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 1.0))
sheet = bpy.context.object; sheet.name = 'parchment'
sheet.scale = (1.9, 3.0, 1)
bpy.ops.object.transform_apply(scale=True)
# subdivide for cloth resolution
bpy.context.view_layer.objects.active = sheet
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=28)
bpy.ops.object.mode_set(mode='OBJECT')
sheet.rotation_euler = (math.radians(88), 0, 0)   # near-vertical, hanging from the dowel
# parchment material: warm, rough, slight translucency
pm, pb = new_mat('parchment')
set_in(pb, 'Base Color', (0.86, 0.74, 0.52, 1)); set_in(pb, 'Roughness', 0.72)
set_in(pb, 'Subsurface Weight', 0.18) or set_in(pb, 'Subsurface', 0.18)
set_in(pb, 'Subsurface Radius', (0.4, 0.3, 0.2))
sheet.data.materials.append(pm)

# top-edge pin group (verts near the dowel line, top Y)
vg = sheet.vertex_groups.new(name='pin')
top_y = max(v.co.y for v in sheet.data.vertices)
pin_idx = [v.index for v in sheet.data.vertices if v.co.y > top_y - 0.06]
vg.add(pin_idx, 1.0, 'REPLACE')

# cloth modifier
cloth = sheet.modifiers.new('cloth', 'CLOTH')
cs = cloth.settings
cs.vertex_group_mass = 'pin'          # pinned top edge
cs.mass = 0.3; cs.tension_stiffness = 15; cs.compression_stiffness = 15
cs.bending_stiffness = 0.5
cloth.point_cache.frame_start = 1; cloth.point_cache.frame_end = max(FE, FS)

# weak wind to give the unfurl life
bpy.ops.object.effector_add(type='WIND', location=(0, -3, 1))
wind = bpy.context.object; wind.rotation_euler = (math.radians(-90), 0, 0)
wind.field.strength = 6.0; wind.field.flow = 0.6; wind.field.noise = 1.0

# bake cloth
scene.frame_set(FS)
try:
    bpy.ops.ptcache.bake_all(bake=True); print('BAKED cloth', cloth.point_cache.frame_start, '..', cloth.point_cache.frame_end)
except Exception as e:
    print('bake err', e)

# ---- drifting dust motes (warm) ----
dust_mat, dbb = new_mat('dust'); emissive(dbb, WARM, 5.0); set_in(dbb, 'Base Color', (1, 1, 1, 1))
for i in range(24):
    dx = (random.random() - 0.5) * 5; dy = (random.random() - 0.5) * 2 - 1.5; dz = FLOOR_Z + 0.4 + random.random() * 4
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.012 + random.random() * 0.01, location=(dx, dy, dz))
    d = bpy.context.object
    for p in d.data.polygons: p.use_smooth = True
    d.data.materials.append(dust_mat)

# ---- warm god-ray + fill ----
sp = bpy.data.lights.new('godray', 'SPOT'); sp.energy = 4000; sp.spot_size = math.radians(50); sp.color = WARM
spo = bpy.data.objects.new('godray', sp); spo.location = (-4, -5, 7); coll.objects.link(spo)
spo.rotation_euler = (Vector((0, 0, 1.0)) - Vector(spo.location)).to_track_quat('-Z', 'Y').to_euler()
def area(name, loc, energy, color, size=6, target=Vector((0, 0, 1.0))):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    ob.rotation_euler = (target - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
area('fill', (5, -5, 3), 900, (1.0, 0.9, 0.7), 7)
area('rim', (-3, 5, 5), 1300, (1.0, 0.85, 0.6), 5)

# ---- atmospheric haze for the shafts ----
bpy.ops.mesh.primitive_cube_add(size=16, location=(0, 0, 1.5))
vol = bpy.context.object; vm = bpy.data.materials.new('haze'); vm.use_nodes = True
vnt = vm.node_tree
for n in list(vnt.nodes):
    if n.type == 'BSDF_PRINCIPLED': vnt.nodes.remove(n)
pv = vnt.nodes.new('ShaderNodeVolumePrincipled'); pv.inputs['Density'].default_value = 0.014
pv.inputs['Color'].default_value = (1.0, 0.85, 0.6, 1)
vnt.links.new(pv.outputs['Volume'], vnt.nodes.get('Material Output').inputs['Volume'])
vol.data.materials.append(vm)

# ---- camera dolly along the sheet ----
LOOK = Vector((0, 0, 1.0))
CAM_START = Vector((3.5, -6.5, 2.4)); CAM_END = Vector((-1.5, -5.5, 0.6))
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd); coll.objects.link(cam); scene.camera = cam
cd.lens = 50; cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.4
cam.location = CAM_START; cam.rotation_euler = (LOOK - CAM_START).to_track_quat('-Z', 'Y').to_euler()
cd.dof.focus_distance = (CAM_START - LOOK).length
if FE > FS:
    cam.location = CAM_START; cam.keyframe_insert('location', frame=FS)
    cam.location = CAM_END; cam.keyframe_insert('location', frame=FE)
    cam.rotation_euler = (LOOK - CAM_START).to_track_quat('-Z', 'Y').to_euler(); cam.keyframe_insert('rotation_euler', frame=FS)
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
    sock('Quality', 'High'); sock('Highlights Threshold', 0.8); sock('Strength', 0.9); sock('Size', 0.8)
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

scene.frame_set(FE)
scene.render.image_settings.file_format = 'PNG'
if FE == FS:
    os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
    scene.render.filepath = OUT + '_test.png'; bpy.ops.render.render(write_still=True); print('WROTE', scene.render.filepath)
else:
    os.makedirs(OUT, exist_ok=True); scene.render.filepath = OUT + '/f_'; bpy.ops.render.render(animation=True); print('WROTE SEQ', OUT)
