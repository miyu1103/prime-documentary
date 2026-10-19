import bpy, sys, math, random
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out'); RX, RY = int(A(1, 1920)), int(A(2, 1080))
FS, FE = int(A(3, 1)), int(A(4, 90)); SAMPLES = int(A(5, 96))
ACC = (0.10, 0.42, 1.0); ACC_HI = (0.35, 0.70, 1.0)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene; coll = scene.collection

engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in engines else 'BLENDER_EEVEE'
scene.render.resolution_x = RX; scene.render.resolution_y = RY
scene.render.fps = 30; scene.frame_start, scene.frame_end = FS, FE
ee = scene.eevee
for a, v in [('taa_render_samples', SAMPLES), ('use_raytracing', True), ('use_ssr', True), ('use_gtao', True)]:
    if hasattr(ee, a):
        try: setattr(ee, a, v)
        except Exception: pass

world = bpy.data.worlds.new('W'); scene.world = world; world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
bg.inputs[0].default_value = (0.008, 0.012, 0.025, 1); bg.inputs[1].default_value = 0.6

def new_mat(n):
    m = bpy.data.materials.new(n); m.use_nodes = True
    return m, m.node_tree.nodes.get('Principled BSDF')
def set_in(b, n, v):
    if n in b.inputs: b.inputs[n].default_value = v; return True
    return False
def emissive(b, c, s):
    if not set_in(b, 'Emission Color', (*c, 1)): set_in(b, 'Emission', (*c, 1))
    set_in(b, 'Emission Strength', s)

def rb(obj, kind, shape, mass=1.0, kinematic=False):
    bpy.context.view_layer.objects.active = obj
    for o in bpy.context.selected_objects: o.select_set(False)
    obj.select_set(True)
    bpy.ops.rigidbody.object_add()
    obj.rigid_body.type = kind
    obj.rigid_body.collision_shape = shape
    obj.rigid_body.mass = mass
    obj.rigid_body.kinematic = kinematic
    obj.rigid_body.friction = 0.35
    obj.rigid_body.restitution = 0.05

# --- ground (passive) ---
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -3.0))
ground = bpy.context.object
gm, gb = new_mat('ground'); set_in(gb, 'Base Color', (0.01, 0.015, 0.03, 1)); set_in(gb, 'Metallic', 0.9); set_in(gb, 'Roughness', 0.25)
ground.data.materials.append(gm)
rb(ground, 'PASSIVE', 'BOX')

# --- block materials ---
mDark, bD = new_mat('blkDark'); set_in(bD, 'Base Color', (0.02, 0.04, 0.09, 1)); set_in(bD, 'Metallic', 0.85); set_in(bD, 'Roughness', 0.3)
mGlow, bG = new_mat('blkGlow'); set_in(bG, 'Base Color', (0.02, 0.04, 0.09, 1)); set_in(bG, 'Metallic', 0.6); emissive(bG, ACC, 1.2)

# --- 崩落するブロック群（上空から降らせる＝重力で確実に動く） ---
# 塔状に積むが各ブロックをランダム回転＋微オフセット＝不安定→重力で座屈・崩落・堆積。
random.seed(5)
BW, BH, BD = 0.55, 0.42, 0.55
COLS, ROWS, DEP = 6, 16, 2
x0 = -(COLS * BW) / 2 + BW / 2
z0 = -3.0 + BH / 2 + 0.02
blocks = []
for r in range(ROWS):
    for cx in range(COLS):
        for dz in range(DEP):
            # 微オフセット＋回転で不安定に（上ほど大きく揺らす＝上から崩れる）
            jit = 0.02 + r * 0.006
            x = x0 + cx * (BW + 0.01) + (random.random() - 0.5) * jit
            z = z0 + r * (BH + 0.02)
            y = -(DEP * BD) / 2 + BD / 2 + dz * (BD + 0.01) + (random.random() - 0.5) * jit
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            blk = bpy.context.object
            blk.scale = (BW / 2, BD / 2, BH / 2)
            blk.rotation_euler = (
                (random.random() - 0.5) * 0.06 * (1 + r * 0.15),
                (random.random() - 0.5) * 0.06 * (1 + r * 0.15),
                (random.random() - 0.5) * 0.06,
            )
            blk.data.materials.append(mGlow if random.random() < 0.18 else mDark)
            rb(blk, 'ACTIVE', 'BOX', mass=1.0)
            blocks.append(blk)

# --- 横風フォースフィールドで塔を突き倒す（確実にコリジョン連鎖を起こす） ---
bpy.ops.object.effector_add(type='WIND', location=(-6, 0, z0 + ROWS * BH * 0.55))
wind = bpy.context.object
wind.rotation_euler = (0, math.radians(90), 0)  # +X方向へ吹く
fs = wind.field
fs.flow = 0.0
# 強い横風を初撃で（塔を確実に倒す）→その後は重力任せ
fs.strength = 95.0; wind.keyframe_insert('field.strength', frame=1)
wind.keyframe_insert('field.strength', frame=14)
fs.strength = 0.0; wind.keyframe_insert('field.strength', frame=18)

# 発光する「破壊の核」も飛ばして絵的アクセント（動的・初速つき代わりに高所から落下）
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.9, location=(0, 0, z0 + ROWS * BH + 2.0))
ball = bpy.context.object
for p in ball.data.polygons: p.use_smooth = True
sm, sb = new_mat('ball'); set_in(sb, 'Base Color', (1, 1, 1, 1)); emissive(sb, ACC_HI, 8.0)
ball.data.materials.append(sm)
rb(ball, 'ACTIVE', 'SPHERE', mass=25.0)

# --- rigid body world tuning + bake ---
rw = scene.rigidbody_world
rw.substeps_per_frame = 20
rw.solver_iterations = 20
rw.point_cache.frame_start = 1
rw.point_cache.frame_end = FE
scene.frame_set(1)
try:
    bpy.ops.ptcache.bake_all(bake=True)
    print('BAKED')
except Exception as e:
    print('bake err', e)

# --- lights / softboxes ---
def area(nm, loc, en, col, sz=6):
    ld = bpy.data.lights.new(nm, 'AREA'); ld.energy = en; ld.color = col; ld.size = sz
    ob = bpy.data.objects.new(nm, ld); ob.location = loc; coll.objects.link(ob)
    d = Vector((0, 0, 0)) - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
area('key', (6, -6, 8), 2200, (1, 1, 1), 8)
area('fill', (-7, -3, 3), 1000, ACC_HI, 8)
area('rim', (-3, 6, 5), 1400, (0.6, 0.8, 1.0), 6)

# --- camera + DOF ---
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam); scene.camera = cam
cam.location = (11.0, -13.0, 3.4); cd.lens = 46
cd.dof.use_dof = True; cd.dof.aperture_fstop = 4.5
tgt = bpy.data.objects.new('tgt', None); tgt.location = (0, 0, 0.8); coll.objects.link(tgt)
cd.dof.focus_object = tgt
d = Vector((0, 0, 1.4)) - Vector(cam.location); cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

# --- bloom (Blender 5.x compositor node group + socket API) ---
def setup_bloom(scene):
    nt = None
    try: scene.use_nodes = True; nt = scene.node_tree
    except Exception: nt = None
    if nt is None and hasattr(scene, 'compositing_node_group'):
        ng = bpy.data.node_groups.new('comp', 'CompositorNodeTree'); scene.compositing_node_group = ng; nt = ng
    if nt is None: return
    for n in list(nt.nodes): nt.nodes.remove(n)
    rl = nt.nodes.new('CompositorNodeRLayers'); gl = nt.nodes.new('CompositorNodeGlare')
    def sock(nm, v):
        if nm in gl.inputs:
            try: gl.inputs[nm].default_value = v
            except Exception: pass
    sock('Type', 'Bloom'); sock('Quality', 'High'); sock('Highlights Threshold', 0.8); sock('Strength', 1.0); sock('Size', 0.8)
    out = None
    try: out = nt.nodes.new('CompositorNodeComposite')
    except Exception: pass
    nt.links.new(rl.outputs['Image'], gl.inputs['Image'])
    if out is not None: nt.links.new(gl.outputs['Image'], out.inputs['Image'])
    else:
        go = nt.nodes.new('NodeGroupOutput')
        nt.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
        nt.links.new(gl.outputs['Image'], go.inputs[0])
setup_bloom(scene)

scene.render.image_settings.file_format = 'PNG'
if FE == FS:
    scene.render.filepath = OUT + '_test.png'; bpy.ops.render.render(write_still=True); print('WROTE', scene.render.filepath)
else:
    scene.render.filepath = OUT + '/f_'; bpy.ops.render.render(animation=True); print('WROTE SEQ', OUT)
