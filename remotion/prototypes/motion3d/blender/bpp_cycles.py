import bpy, sys, math, random
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 1920)), int(A(2, 1080))
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 160))
ACC = (0.10, 0.42, 1.0)
ACC_HI = (0.35, 0.70, 1.0)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
coll = scene.collection

# ---- CYCLES + GPU ----
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
# NOTE: caustics OFF on purpose — with glass they make some frames explode in
# render time (a single frame stalled for minutes mid-animation). The Glare
# bloom already supplies the glow. Do not re-enable for animation renders.
try: scene.cycles.caustics_reflective = False; scene.cycles.caustics_refractive = False
except Exception: pass

scene.render.resolution_x = RX
scene.render.resolution_y = RY
scene.render.fps = 30
scene.frame_start, scene.frame_end = FS, FE
scene.view_settings.view_transform = 'AgX'   # 映画的トーンマップ

# ---- world: dark blue gradient (reflections) ----
world = bpy.data.worlds.new('W'); scene.world = world
world.use_nodes = True
wn = world.node_tree
bg = wn.nodes.get('Background')
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

# ---- crystal gem (glass + bevel) ----
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.2, location=(0, 0, 0))
gem = bpy.context.object; gem.name = 'gem'
for p in gem.data.polygons: p.use_smooth = False
bev = gem.modifiers.new('bev', 'BEVEL'); bev.width = 0.025; bev.segments = 3
gm, gb = new_mat('glass')
set_in(gb, 'Base Color', (0.75, 0.86, 1.0, 1))
set_in(gb, 'Transmission Weight', 1.0)
set_in(gb, 'Roughness', 0.02)
set_in(gb, 'IOR', 1.85)
gem.data.materials.append(gm)

# emissive core (refracts through the glass) — 控えめにしてガラスを見せる
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.5, location=(0, 0, 0))
core = bpy.context.object; core.name = 'core'
for p in core.data.polygons: p.use_smooth = True
cm, cb = new_mat('core'); emissive(cb, ACC, 2.2)
set_in(cb, 'Base Color', (*ACC, 1))
core.data.materials.append(cm)
wire = None

# orbiting emissive satellites
piv = bpy.data.objects.new('pivot', None); coll.objects.link(piv)
sm, sb = new_mat('sat'); emissive(sb, (0.7, 0.85, 1.0), 6.0); set_in(sb, 'Base Color', (1, 1, 1, 1))
random.seed(7)
for i in range(9):
    ang = i / 9 * math.tau; r = 2.7 + random.random() * 0.5; z = (random.random() - 0.5) * 1.4
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06 + random.random() * 0.05,
                                         location=(math.cos(ang) * r, math.sin(ang) * r, z))
    s = bpy.context.object
    for p in s.data.polygons: p.use_smooth = True
    s.data.materials.append(sm); s.parent = piv

# reflective floor
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -1.7))
fl = bpy.context.object
fm, fb = new_mat('floor')
set_in(fb, 'Base Color', (0.01, 0.015, 0.03, 1)); set_in(fb, 'Metallic', 0.9); set_in(fb, 'Roughness', 0.22)
fl.data.materials.append(fm)

# lights
def area(name, loc, energy, color, size=5):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    d = Vector((0, 0, 0)) - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
area('key', (5, -4, 6), 1600, (1, 1, 1), 6)
area('fill', (-6, -2, 2), 800, ACC_HI, 7)
area('rim', (-2, 5, 4), 1300, (0.6, 0.8, 1.0), 5)

# reflection softboxes (off camera)
def softbox(loc, size, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object; m, b = new_mat('sb'); emissive(b, color, strength); o.data.materials.append(m)
    d = Vector((0, 0, 0)) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
softbox((-8, -5, 3), 5, ACC_HI, 1.4)
softbox((8, -5, 2.5), 5, (0.75, 0.88, 1.0), 1.1)
softbox((0, -9, 5), 6, (0.55, 0.72, 1.0), 0.8)

# camera + DOF
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam); scene.camera = cam
cam.location = (2.2, -5.6, 1.5); cd.lens = 55
cd.dof.use_dof = True; cd.dof.focus_object = gem; cd.dof.aperture_fstop = 2.2
d = Vector((0, 0, 0.1)) - Vector(cam.location); cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

if FE > FS:
    spins = [(gem, 0.25), (piv, 0.5), (core, -0.15)]
    if wire is not None: spins.append((wire, 0.25))
    for ob, turns in spins:
        ob.rotation_euler = (0, 0, 0); ob.keyframe_insert('rotation_euler', frame=FS)
        ob.rotation_euler = (0, 0, math.tau * turns); ob.keyframe_insert('rotation_euler', frame=FE)
    cam.location = (2.2, -5.6, 1.5); cam.keyframe_insert('location', frame=FS)
    cam.location = (1.4, -4.9, 1.3); cam.keyframe_insert('location', frame=FE)

# compositor bloom (Blender 5.x node group + socket API)
def setup_bloom(scene):
    nt = None
    try:
        scene.use_nodes = True; nt = scene.node_tree
    except Exception:
        nt = None
    if nt is None and hasattr(scene, 'compositing_node_group'):
        ng = bpy.data.node_groups.new('comp', 'CompositorNodeTree'); scene.compositing_node_group = ng; nt = ng
    if nt is None: return
    for n in list(nt.nodes): nt.nodes.remove(n)
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

scene.render.image_settings.file_format = 'PNG'
if FE == FS:
    scene.render.filepath = OUT + '_cyc.png'
    bpy.ops.render.render(write_still=True)
    print('WROTE', scene.render.filepath)
else:
    scene.render.filepath = OUT + '/f_'
    bpy.ops.render.render(animation=True)
    print('WROTE SEQ', OUT)
