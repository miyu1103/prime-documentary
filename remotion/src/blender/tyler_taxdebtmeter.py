"""EP33 tyler — HERO #1 TaxDebtMeter — L3 Cycles ceiling scene (SUPER-HEAVY tier).

Bespoke subject: a 3D extruded ring gauge (torus frame + tick ring + a swinging
needle) with an EXTRUDED 3D number at its center reading the debt total
($15,000 — the T5/CLM-0004 figure; a data glyph, not a forged record). The
needle orbits toward the total and, at the 1:50 slam, the number seats with a
lens micro-punch. Camera: 55mm slow dolly-in + 8deg orbit, DOF aperture_fstop
2.2 focused on the meter face. Thin volumetric god-ray haze (Principled Volume
density 0.02). Follows bpp_cycles.py (L3 look). Deterministic (seed 1234); all
motion frame-keyframed. No real-person likeness, no logos; the only text is the
figure's own data number (invariant 11 / R2).

ARGV CONTRACT (identical to bpp_cycles.py):
    blender -b -P tyler_taxdebtmeter.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
    FS == FE -> single test still (<OUT>_test.png)
    FS <  FE -> PNG sequence <OUT>/f_0001.png ...  (encode separately, row-6).

TEST (frame 1 smoke still):
    blender -b -P remotion/src/blender/tyler_taxdebtmeter.py -- out/hero_taxdebt 3840 2160 1 1 200
FULL (5s @ 60fps -> 300 frames, 1:20-1:50 beat):
    blender -b -P remotion/src/blender/tyler_taxdebtmeter.py -- out/hero_taxdebt 3840 2160 1 300 200
"""

import bpy, sys, math, os, random
from mathutils import Vector

# ---- args: OUT RX RY FS FE SAMPLES ----
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 3840)), int(A(2, 2160))
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 200))
ACC = (0.10, 0.42, 1.0)
ACC_HI = (0.35, 0.70, 1.0)
GOLD = (0.95, 0.72, 0.22)

random.seed(1234)

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
try:
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
except Exception:
    pass

scene.render.resolution_x = RX
scene.render.resolution_y = RY
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.frame_start, scene.frame_end = FS, FE
scene.view_settings.view_transform = 'AgX'
try:  # Blender 5.x: guarantee non-linear (bezier/auto-clamped) keyframes by default
    _ep = bpy.context.preferences.edit
    _ep.keyframe_new_interpolation_type = 'BEZIER'
    _ep.keyframe_new_handle_type = 'AUTO_CLAMPED'
except Exception: pass

# ---- motion blur (shutter 0.5) ----
scene.render.use_motion_blur = True
scene.render.motion_blur_shutter = 0.5
try:
    scene.cycles.rolling_shutter_type = 'NONE'
except Exception:
    pass

# ---- world: dark blue gradient ----
world = bpy.data.worlds.new('W'); scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
bg.inputs[0].default_value = (0.012, 0.02, 0.04, 1)
bg.inputs[1].default_value = 0.5

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

FLOOR_Z = -2.0

# ---- reflective metallic floor ----
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, FLOOR_Z))
floor = bpy.context.object; floor.name = 'floor'
fm, fb = new_mat('floor')
set_in(fb, 'Base Color', (0.01, 0.015, 0.03, 1))
set_in(fb, 'Metallic', 0.9)
set_in(fb, 'Roughness', 0.22)
floor.data.materials.append(fm)

# ---- bespoke subject: extruded ring gauge + needle + center number ----------
MC = Vector((0.0, 0.0, 0.6))            # meter center (world)

# meter ring frame (torus, facing -Y toward camera)
bpy.ops.mesh.primitive_torus_add(location=MC, major_radius=1.35, minor_radius=0.075,
                                 major_segments=96, minor_segments=16)
ring = bpy.context.object; ring.name = 'ring'
ring.rotation_euler = (math.pi / 2, 0, 0)
rm, rb_ = new_mat('ring')
set_in(rb_, 'Base Color', (0.05, 0.09, 0.16, 1))
set_in(rb_, 'Metallic', 0.85); set_in(rb_, 'Roughness', 0.28)
emissive(rb_, ACC_HI, 0.5)
ring.data.materials.append(rm)
for p in ring.data.polygons: p.use_smooth = True

# tick marks around the lower 300deg arc
tick_mat, tb = new_mat('tick'); emissive(tb, ACC_HI, 1.4)
set_in(tb, 'Base Color', ACC_HI + (1,))
for i in range(31):
    a = math.radians(-150 + i * 300 / 30)
    tx = MC.x + math.sin(a) * 1.2
    tz = MC.z + math.cos(a) * 1.2
    bpy.ops.mesh.primitive_cube_add(location=(tx, 0.0, tz))
    t = bpy.context.object; t.name = 'tick_%02d' % i
    big = (i % 5 == 0)
    t.scale = (0.012, 0.02, 0.09 if big else 0.05)
    t.rotation_euler = (0, -a, 0)
    t.data.materials.append(tick_mat)

# needle (thin wedge) pivoting at center
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.05, radius2=0.0, depth=1.15,
                                location=MC)
needle = bpy.context.object; needle.name = 'needle'
needle.rotation_euler = (0, 0, 0)
nm, nb = new_mat('needle'); set_in(nb, 'Base Color', GOLD + (1,))
set_in(nb, 'Metallic', 0.6); set_in(nb, 'Roughness', 0.3); emissive(nb, GOLD, 1.2)
needle.data.materials.append(nm)
# pivot object at center so needle rotates about the hub
bpy.ops.object.empty_add(location=MC); pivot = bpy.context.object; pivot.name = 'pivot'
needle.parent = pivot
needle.location = (0, 0, 0.5)   # tip offset along local +Z from hub

# hub cap
bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.06, location=MC)
hub = bpy.context.object; hub.rotation_euler = (math.pi / 2, 0, 0)
hub.data.materials.append(nm)

# center 3D extruded number (the figure's own data glyph — $15,000)
bpy.ops.object.text_add(location=(MC.x, 0.02, MC.z - 0.02))
num = bpy.context.object; num.name = 'debt_num'
num.data.body = '$15,000'
num.data.align_x = 'CENTER'; num.data.align_y = 'CENTER'
num.data.size = 0.42
num.data.extrude = 0.05
num.data.bevel_depth = 0.006
num.rotation_euler = (math.pi / 2, 0, 0)
tm, tbb = new_mat('num'); set_in(tbb, 'Base Color', (0.96, 0.97, 1.0, 1))
emissive(tbb, (0.85, 0.92, 1.0), 1.0)
num.data.materials.append(tm)

# ---- thin volumetric god-ray haze (Principled Volume domain) ----
bpy.ops.mesh.primitive_cube_add(size=14, location=(0, 0, 1.0))
vol = bpy.context.object; vol.name = 'haze'
vm = bpy.data.materials.new('haze'); vm.use_nodes = True
vnt = vm.node_tree
for n in list(vnt.nodes):
    if n.type == 'BSDF_PRINCIPLED': vnt.nodes.remove(n)
pv = vnt.nodes.new('ShaderNodeVolumePrincipled')
pv.inputs['Density'].default_value = 0.012   # thin haze — keep god-rays without washing bg
out = vnt.nodes.get('Material Output')
vnt.links.new(pv.outputs['Volume'], out.inputs['Volume'])
vol.data.materials.append(vm)

# ---- 3-point area lights ----
def area(name, loc, energy, color, size=6, target=Vector((0, 0, 0.6))):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    d = target - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
area('key', (5, -5, 5), 2200, (1.0, 0.98, 0.92), 6)
area('fill', (-6, -3, 2), 950, ACC_HI, 7)
area('rim', (-2, 4, 5), 1600, (0.6, 0.8, 1.0), 5)
# a hard spot behind for the god-ray shafts through the haze
sp = bpy.data.lights.new('godray', 'SPOT'); sp.energy = 2600; sp.spot_size = math.radians(55)
sp.color = (0.7, 0.82, 1.0)
spo = bpy.data.objects.new('godray', sp); spo.location = (-3, 6, 6); coll.objects.link(spo)
spo.rotation_euler = (Vector((0, 0, 0.6)) - Vector(spo.location)).to_track_quat('-Z', 'Y').to_euler()

# ---- off-camera softboxes ----
def softbox(loc, size, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object
    m, b = new_mat('sb'); emissive(b, color, strength); o.data.materials.append(m)
    d = Vector((0, 0, 0.6)) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
softbox((-8, -5, 3), 5, ACC_HI, 1.4)
softbox((8, -5, 2.5), 5, (0.9, 0.94, 1.0), 1.1)
softbox((0, -9, 5), 6, (0.7, 0.82, 1.0), 0.8)

# ---- camera + DOF (55mm, fstop 2.2, dolly-in + 8deg orbit) ----
def cam_at(theta, dist, height):
    return Vector((math.sin(theta) * dist, -math.cos(theta) * dist, height))
CAM_START = cam_at(math.radians(-4), 7.4, 1.2)
CAM_END = cam_at(math.radians(4), 5.6, 0.85)
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam); scene.camera = cam
cd.lens = 55; cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.2
cam.location = CAM_START
cam.rotation_euler = (MC - CAM_START).to_track_quat('-Z', 'Y').to_euler()
cd.dof.focus_distance = (CAM_START - MC).length

# ---- keyframed motion (needle orbit + camera + slam punch) ----
if FE > FS:
    slam = FS + int((FE - FS) * 0.85)   # 1:50 slam near the end
    # needle sweeps from -150deg toward the debt reading (~+95deg), overshoot then settle
    pivot.rotation_euler = (0, math.radians(-150), 0); pivot.keyframe_insert('rotation_euler', frame=FS)
    pivot.rotation_euler = (0, math.radians(105), 0); pivot.keyframe_insert('rotation_euler', frame=slam)
    pivot.rotation_euler = (0, math.radians(95), 0); pivot.keyframe_insert('rotation_euler', frame=FE)
    # camera dolly-in + orbit
    cam.location = CAM_START; cam.keyframe_insert('location', frame=FS)
    cam.rotation_euler = (MC - CAM_START).to_track_quat('-Z', 'Y').to_euler(); cam.keyframe_insert('rotation_euler', frame=FS)
    cam.location = CAM_END; cam.keyframe_insert('location', frame=FE)
    cam.rotation_euler = (MC - CAM_END).to_track_quat('-Z', 'Y').to_euler(); cam.keyframe_insert('rotation_euler', frame=FE)
    cd.dof.focus_distance = (CAM_START - MC).length; cd.dof.keyframe_insert('focus_distance', frame=FS)
    cd.dof.focus_distance = (CAM_END - MC).length; cd.dof.keyframe_insert('focus_distance', frame=FE)
    # lens micro-punch at slam (focal length dip)
    cd.lens = 55; cd.keyframe_insert('lens', frame=slam - 4)
    cd.lens = 51; cd.keyframe_insert('lens', frame=slam)
    cd.lens = 55; cd.keyframe_insert('lens', frame=slam + 6)
    # bezier ease everywhere (no linear)
    for ob in (pivot, cam, cd):
        ad = ob.animation_data
        if ad and ad.action:
            for fc in getattr(ad.action, 'fcurves', []):
                for kp in fc.keyframe_points:
                    kp.interpolation = 'BEZIER'; kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
else:
    pivot.rotation_euler = (0, math.radians(-150), 0)   # rest at gauge zero (clears the number)

# ---- compositor Glare Bloom ----
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
    sock('Quality', 'High'); sock('Highlights Threshold', 0.8)
    sock('Highlights Smoothness', 0.3); sock('Strength', 1.0); sock('Size', 0.8)
    try: gl.glare_type = 'BLOOM'
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

# ---- render ----
scene.render.image_settings.file_format = 'PNG'
if FE == FS:
    os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
    scene.render.filepath = OUT + '_test.png'
    bpy.ops.render.render(write_still=True)
    print('WROTE', scene.render.filepath)
else:
    os.makedirs(OUT, exist_ok=True)
    scene.render.filepath = OUT + '/f_'
    bpy.ops.render.render(animation=True)
    print('WROTE SEQ', OUT)
