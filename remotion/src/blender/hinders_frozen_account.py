# hinders_frozen_account.py — EP35 F5 FrozenAccount ★ (SUPER-HEAVY / L3 ceiling)
#
# 3D手法: Blender rigid-body / cell-fracture。通帳/口座パネルを氷結晶化→亀裂連鎖で破断。
#         破片~120。氷=glass(Transmission1.0/Roughness0.02/IOR1.85+Bevel0.025×3seg)。
# 基準ソース: bpp_physics.py（rigid-body world substeps20/solver20・friction0.35/restitution0.05・
#           WIND field strength95→0 frame1-18・bake_all→render animation）
#           ＋ bpp_cycles.py（Cycles/OptiX・AgX・caustics OFF・glass・softbox・DOF・bloom）。
# 引数規約: blender -b -P hinders_frozen_account.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
#   FS==FE → テスト静止画 <OUT>_cyc.png（シム未進行＝frame1の無傷の氷パネルで1枚出す）
#   else   → PNG連番 <OUT>/f_0001.png…（bake_all→render animation）
# invariant11: 実在肖像/判読テキスト/実ロゴ/実通貨なし＝抽象の氷パネル（$32,820.56 等の数字は描かない）。
# 決定論: random.seed 固定。
import bpy, sys, math, random
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 1920)), int(A(2, 1080))
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 200))   # §SH.1 Cycles ceiling 200 samples
random.seed(5205)          # EP35 F5 決定論

ACC = (0.10, 0.42, 1.0)
ACC_HI = (0.35, 0.70, 1.0)
COLD = (0.55, 0.78, 1.0)   # 冷色rim

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
coll = scene.collection

# ---- CYCLES + GPU（bpp_cycles.py 試行→CPUフォールバック）----
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
# NOTE: caustics OFF on purpose — 氷ガラス＋caustics は一部フレームでレンダ時間爆発。
# Glare bloom がグローを供給する（bpp_cycles.py と同方針）。アニメで再有効化しない。
try:
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
except Exception:
    pass

scene.render.resolution_x = RX
scene.render.resolution_y = RY
scene.render.fps = 30
scene.frame_start, scene.frame_end = FS, FE
try:
    scene.view_settings.view_transform = 'AgX'   # 映画的トーンマップ
except Exception:
    pass

# ---- motion blur（§SH.1 steps=16 / shutter0.5）----
scene.render.use_motion_blur = True
for holder, attr, val in [
    (scene.render, 'motion_blur_shutter', 0.5),
    (scene.render, 'motion_blur_position', 'CENTER'),
]:
    try: setattr(holder, attr, val)
    except Exception: pass
def set_mblur_steps(obj, n=4):   # 値N→2^N。N=4→16 サブステップ＝steps=16。
    try: obj.cycles.motion_steps = n
    except Exception: pass

# ---- world: 冷たい暗青 ----
world = bpy.data.worlds.new('W'); scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
bg.inputs[0].default_value = (0.010, 0.018, 0.038, 1)
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

# 氷＝glass（bpp_cycles.py の gem と同一パラメータ）
def ice_mat(name):
    m, b = new_mat(name)
    set_in(b, 'Base Color', (0.75, 0.86, 1.0, 1))
    set_in(b, 'Transmission Weight', 1.0)   # Transmission 1.0
    set_in(b, 'Roughness', 0.02)            # Roughness 0.02
    set_in(b, 'IOR', 1.85)                  # IOR 1.85
    return m
mIce = ice_mat('ice_glass')
# 内部の冷たい発光核（氷の内部散乱を見せる）
mCore, cb = new_mat('ice_core'); emissive(cb, COLD, 1.4); set_in(cb, 'Base Color', (*COLD, 1))

# ---- rigid-body world tuning（bpp_physics.py と同値）----
def rb(obj, kind, shape, mass=1.0, kinematic=False):
    bpy.context.view_layer.objects.active = obj
    for o in bpy.context.selected_objects: o.select_set(False)
    obj.select_set(True)
    bpy.ops.rigidbody.object_add()
    obj.rigid_body.type = kind
    obj.rigid_body.collision_shape = shape
    obj.rigid_body.mass = mass
    obj.rigid_body.kinematic = kinematic
    obj.rigid_body.friction = 0.35       # bpp_physics.py: 0.35
    obj.rigid_body.restitution = 0.05    # bpp_physics.py: 0.05

# ---- ground (passive) ----
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -2.2))
ground = bpy.context.object
gm, gb = new_mat('ground'); set_in(gb, 'Base Color', (0.01, 0.015, 0.03, 1)); set_in(gb, 'Metallic', 0.9); set_in(gb, 'Roughness', 0.24)
ground.data.materials.append(gm)
rb(ground, 'PASSIVE', 'BOX')

# ---- 口座パネルを氷結晶の破片グリッドへ（cell-fracture 相当・破片~120）----
# 注記: cell_fracture addon はheadlessで不安定なため、決定論的な voronoi風グリッド破片
#       （12×10=120片）を直接生成する＝rigid-body fracture（bpp_physics.py 規律で破断）。
#       各片は最初 kinematic で無傷パネルを保持→列ごとに時間差で解放＝亀裂連鎖伝播。
PW, PH = 3.4, 2.2          # パネル寸法（抽象の通帳/口座パネル）
COLS, ROWS = 12, 10        # 12*10 = 120 破片
PZ = 0.0
tx = PW / COLS
ty = PH / ROWS
x0 = -PW / 2 + tx / 2
y0 = -PH / 2 + ty / 2
shards = []
for r in range(ROWS):
    for c in range(COLS):
        jx = (random.random() - 0.5) * tx * 0.28   # voronoi風の不規則性
        jy = (random.random() - 0.5) * ty * 0.28
        x = x0 + c * tx + jx
        y = y0 + r * ty + jy
        bpy.ops.mesh.primitive_cube_add(location=(x, PZ, 0))  # Z-up: パネルはXY面…だが縦置き
        s = bpy.context.object
        # パネルを縦（カメラ正対）に：厚み薄・幅tx・高さty。Y=奥行きに薄く。
        s.scale = (tx / 2 * 0.94, 0.06, ty / 2 * 0.94)
        s.location = (x, 0.0, y)     # X=横 / Z=縦 / Y薄
        s.rotation_euler = (
            (random.random() - 0.5) * 0.02,
            (random.random() - 0.5) * 0.02,
            (random.random() - 0.5) * 0.02,
        )
        s.data.materials.append(mIce)
        bev = s.modifiers.new('bev', 'BEVEL'); bev.width = 0.025; bev.segments = 3  # Bevel0.025×3seg
        set_mblur_steps(s)
        # 最初は kinematic（無傷パネルとして静止）→解放キーで破断
        rb(s, 'ACTIVE', 'CONVEX_HULL', mass=0.6, kinematic=True)
        shards.append((s, c, r))

# 破片の時間差解放（左→右へ亀裂連鎖・0–40f 目安・λ0.75 の伝播感）
if FE > FS:
    for s, c, r in shards:
        rel = FS + 6 + int(c * 1.6) + (r % 2)   # 列で伝播＋行で微ゆらぎ
        rel = min(rel, FE - 1)
        s.rigid_body.kinematic = True
        s.keyframe_insert('rigid_body.kinematic', frame=FS)
        s.keyframe_insert('rigid_body.kinematic', frame=max(FS, rel - 1))
        s.rigid_body.kinematic = False
        s.keyframe_insert('rigid_body.kinematic', frame=rel)

# 発光する「破断核」＝上から落として亀裂を起こす（bpp_physics.py の落下核と同趣旨）
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.5, location=(0, -0.9, 2.6))
core = bpy.context.object; core.name = 'fracture_core'
for p in core.data.polygons: p.use_smooth = True
core.data.materials.append(mCore)
set_mblur_steps(core)
rb(core, 'ACTIVE', 'SPHERE', mass=14.0)

# WIND フォースフィールド（bpp_physics.py：strength95→0 frame1-18 で破断を確実化）
bpy.ops.object.effector_add(type='WIND', location=(0, -6, 0.4))
wind = bpy.context.object
wind.rotation_euler = (math.radians(-90), 0, 0)   # +Y（奥）へ吹いてパネルを砕き飛ばす
fs = wind.field
fs.flow = 0.0
fs.strength = 95.0; wind.keyframe_insert('field.strength', frame=FS)
wind.keyframe_insert('field.strength', frame=FS + 13)
fs.strength = 0.0; wind.keyframe_insert('field.strength', frame=FS + 17)

# ---- frost 結晶パーティクル ~5k（hair＝静止画でも可視・決定論seed）----
bpy.ops.mesh.primitive_plane_add(size=4.4, location=(0, 0.9, 0), rotation=(math.radians(90), 0, 0))
frost_emit = bpy.context.object; frost_emit.name = 'frost_emitter'
mFrost, fb = new_mat('frost'); emissive(fb, (0.8, 0.92, 1.0), 3.0); set_in(fb, 'Base Color', (1, 1, 1, 1))
frost_emit.data.materials.append(mFrost)
try:
    psys_mod = frost_emit.modifiers.new('frost', 'PARTICLE_SYSTEM')
    ps = frost_emit.particle_systems[0].settings
    ps.type = 'HAIR'
    ps.count = 5000                    # §SH.1 frost ~5k
    ps.hair_length = 0.06
    ps.use_advanced_hair = True
    ps.render_type = 'PATH'
    try: frost_emit.particle_systems[0].seed = 5205
    except Exception: pass
    try: ps.child_type = 'NONE'
    except Exception: pass
except Exception as e:
    print('frost particle skip', e)

# ---- lights / softboxes（冷色rim＋softbox反射で氷の内部散乱）----
def area(name, loc, energy, color, size=6):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    d = Vector((0, 0, 0)) - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
area('key', (5, -5, 6), 1800, (1, 1, 1), 6)
area('fill', (-6, -3, 2), 800, ACC_HI, 7)
area('rim', (-2, 5, 5), 1500, COLD, 5)    # 冷色rim
def softbox(loc, size, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object; m, b = new_mat('sb'); emissive(b, color, strength); o.data.materials.append(m)
    d = Vector((0, 0, 0)) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
softbox((-8, -5, 3), 5, ACC_HI, 1.4)
softbox((8, -5, 2.5), 5, COLD, 1.1)
softbox((0, -9, 5), 6, (0.55, 0.72, 1.0), 0.8)

# ---- camera：通帳へ push-in 0–40f（+終端push相当の寄り）----
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam); scene.camera = cam
cd.lens = 50
cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.2   # DOF f2.2
tgt = bpy.data.objects.new('tgt', None); tgt.location = (0, 0, 0.1); coll.objects.link(tgt)
cd.dof.focus_object = tgt
set_mblur_steps(cam)
CAM_A = (0.6, -7.4, 0.9)
CAM_B = (0.3, -5.2, 0.5)   # push-in
def look_from(loc, look=(0, 0, 0.1)):
    d = Vector(look) - Vector(loc)
    return d.to_track_quat('-Z', 'Y').to_euler()
cam.location = CAM_A; cam.rotation_euler = look_from(CAM_A)
if FE > FS:
    kb = min(FS + 40, FE)   # 0–40f push-in
    cam.location = CAM_A; cam.keyframe_insert('location', frame=FS)
    cam.location = CAM_B; cam.keyframe_insert('location', frame=kb)

# ---- compositor bloom（Blender 5.x node group + socket API）----
def setup_bloom(scene):
    nt = None
    try: scene.use_nodes = True; nt = scene.node_tree
    except Exception: nt = None
    if nt is None and hasattr(scene, 'compositing_node_group'):
        ng = bpy.data.node_groups.new('comp', 'CompositorNodeTree'); scene.compositing_node_group = ng; nt = ng
    if nt is None: return
    for n in list(nt.nodes): nt.nodes.remove(n)
    rl = nt.nodes.new('CompositorNodeRLayers'); gl = nt.nodes.new('CompositorNodeGlare')
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

# ---- rigid-body world tune + bake（bpp_physics.py 規律）----
rw = scene.rigidbody_world
if rw is not None:
    rw.substeps_per_frame = 20     # bpp_physics.py: 20
    rw.solver_iterations = 20      # bpp_physics.py: 20
    rw.point_cache.frame_start = FS
    rw.point_cache.frame_end = FE

scene.render.image_settings.file_format = 'PNG'
if FE == FS:
    # 静止画テスト：シム未進行＝frame1の無傷の氷パネルで1枚出す。
    scene.render.filepath = OUT + '_cyc.png'
    bpy.ops.render.render(write_still=True)
    print('WROTE', scene.render.filepath)
else:
    scene.frame_set(FS)
    try:
        bpy.ops.ptcache.bake_all(bake=True)
        print('RB BAKED')
    except Exception as e:
        print('bake err', e)
    scene.render.filepath = OUT + '/f_'
    bpy.ops.render.render(animation=True)
    print('WROTE SEQ', OUT)
