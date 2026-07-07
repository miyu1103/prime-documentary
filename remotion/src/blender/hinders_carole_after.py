# hinders_carole_after.py — EP35 F20 CaroleAfterCard ★ (SUPER-HEAVY / L3 ceiling)
#
# 3D手法: Blender Cycles ceiling。空店内(Mrs.Lady's抽象化)を3D化・奥→手前 dolly 0–72f＋
#         "SOLD"札の落下。窓からの体積ゴッドレイ＋softbox反射・AgX・埃/光条パーティクル。
# 基準ソース: bpp_cycles.py（Cycles/OptiX→CPU・AgX・caustics OFF・glass・softbox・DOF f2.2・bloom）。
# 引数規約: blender -b -P hinders_carole_after.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
#   FS==FE → テスト静止画 <OUT>_cyc.png / else → PNG連番 <OUT>/f_0001.png…
# invariant11: 実在肖像/判読テキスト/実ロゴ/実通貨なし。"SOLD"札は文字ではなく抽象の札
#             （タグ形状＋発光バー・フォント非依存）として描く。
# 決定論: random.seed 固定。物理シム無し＝純Cycles（重いbake不要）。
import bpy, sys, math, random
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 1920)), int(A(2, 1080))
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 200))   # §SH.1 Cycles ceiling 200 samples
random.seed(2035)          # EP35 F20 決定論

ACC = (0.10, 0.42, 1.0)
ACC_HI = (0.35, 0.70, 1.0)
WARM = (1.0, 0.72, 0.38)   # 窓からの暖い外光（Iowa=暖アンバー系）

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
# NOTE: caustics OFF on purpose — 窓ガラス＋caustics は一部フレームでレンダ時間爆発。
# Glare bloom がグローを供給する（bpp_cycles.py と同方針）。アニメで再有効化しない。
try:
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
except Exception:
    pass
# 体積ゴッドレイを見せるためボリューム散乱のバウンスを確保
try: scene.cycles.volume_bounces = 2
except Exception: pass

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
def set_mblur_steps(obj, n=4):   # N=4 → 2^4 = 16 サブステップ＝steps=16。
    try: obj.cycles.motion_steps = n
    except Exception: pass

# ---- world: 暗い店内＋薄い体積霧（窓光が射し込むと光条＝ゴッドレイになる）----
world = bpy.data.worlds.new('W'); scene.world = world
world.use_nodes = True
wn = world.node_tree
bg = wn.nodes.get('Background')
bg.inputs[0].default_value = (0.020, 0.020, 0.026, 1)
bg.inputs[1].default_value = 0.25
try:
    vs = wn.nodes.new('ShaderNodeVolumeScatter')
    vs.inputs['Density'].default_value = 0.018     # 埃っぽい空気＝窓光でゴッドレイ
    if 'Anisotropy' in vs.inputs:
        vs.inputs['Anisotropy'].default_value = 0.4
    wout = wn.nodes.get('World Output')
    wn.links.new(vs.outputs['Volume'], wout.inputs['Volume'])
except Exception as e:
    print('world volume skip', e)

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
def diffuse(name, col, rough=0.6, metal=0.0):
    m, b = new_mat(name); set_in(b, 'Base Color', (*col, 1)); set_in(b, 'Roughness', rough); set_in(b, 'Metallic', metal)
    return m
def glass_mat(name, tint=(0.8, 0.88, 0.95)):   # bpp_cycles.py glass 規律を窓に適用
    m, b = new_mat(name)
    set_in(b, 'Base Color', (*tint, 1))
    set_in(b, 'Transmission Weight', 1.0)
    set_in(b, 'Roughness', 0.02)
    set_in(b, 'IOR', 1.85)
    return m

mFloor = diffuse('floor', (0.06, 0.05, 0.045), rough=0.35, metal=0.1)
mWall = diffuse('wall', (0.10, 0.095, 0.085), rough=0.8)
mCounter = diffuse('counter', (0.05, 0.055, 0.07), rough=0.3, metal=0.4)
mShelf = diffuse('shelf', (0.08, 0.07, 0.06), rough=0.7)
mGlass = glass_mat('window_glass')

# ---- 店内シェル（床/奥壁/左右壁）----
def box(name, loc, scale, mat, bevel=False):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    o.data.materials.append(mat)
    if bevel:
        bv = o.modifiers.new('bev', 'BEVEL'); bv.width = 0.025; bv.segments = 3
    return o
ROOM_D = 9.0    # 奥行き
box('floor', (0, ROOM_D * 0.5, 0), (3.4, ROOM_D * 0.5, 0.05), mFloor)
box('ceiling', (0, ROOM_D * 0.5, 3.2), (3.4, ROOM_D * 0.5, 0.05), mWall)
box('back_wall', (0, ROOM_D, 1.6), (3.4, 0.05, 1.6), mWall)
box('left_wall', (-3.4, ROOM_D * 0.5, 1.6), (0.05, ROOM_D * 0.5, 1.6), mWall)
# 右壁は窓を空ける：上下＋左右の枠だけ残し中央を開口（外光を入れる）
box('right_wall_lo', (3.4, ROOM_D * 0.5, 0.5), (0.05, ROOM_D * 0.5, 0.5), mWall)
box('right_wall_hi', (3.4, ROOM_D * 0.5, 2.7), (0.05, ROOM_D * 0.5, 0.5), mWall)
box('right_wall_f', (3.4, 1.2, 1.6), (0.05, 0.4, 1.6), mWall)
box('right_wall_b', (3.4, ROOM_D - 1.2, 1.6), (0.05, 0.4, 1.6), mWall)
# 窓ガラス（開口部を薄板ガラスで塞ぐ＝反射＋屈折）
box('window_glass', (3.4, ROOM_D * 0.5, 1.6), (0.02, ROOM_D * 0.35, 1.05), mGlass, bevel=True)

# ---- カウンター（レジ台）＋空棚（がらんとした店）----
box('counter', (-1.0, 3.0, 0.6), (1.6, 0.5, 0.6), mCounter, bevel=True)
for i in range(4):
    box('shelf_%d' % i, (2.2, 2.0 + i * 1.6, 0.9 + (i % 2) * 0.7), (0.9, 0.06, 0.5), mShelf)
# 椅子（near前景・パララックス層）
for i, xx in enumerate((-2.2, -0.4)):
    box('chair_seat_%d' % i, (xx, 1.4, 0.6), (0.35, 0.35, 0.05), mShelf, bevel=True)
    box('chair_back_%d' % i, (xx, 1.72, 1.0), (0.35, 0.05, 0.4), mShelf, bevel=True)

# ---- "SOLD"札：抽象タグ（文字ではなく発光バー・invariant11）----
# 吊り紐から下がる長方形タグに、太い発光バーを2本＝「掲示」記号として抽象化。
bpy.ops.mesh.primitive_cube_add(location=(-1.0, 2.6, 2.6))
tag = bpy.context.object; tag.name = 'sold_tag'
tag.scale = (0.7, 0.03, 0.45)
mTag = diffuse('tag', (0.9, 0.85, 0.78), rough=0.5)
tag.data.materials.append(mTag)
bv = tag.modifiers.new('bev', 'BEVEL'); bv.width = 0.02; bv.segments = 3
set_mblur_steps(tag)
# タグ上の発光バー2本（抽象の掲示標）
mBar, bb = new_mat('tag_bar'); emissive(bb, WARM, 4.0); set_in(bb, 'Base Color', (*WARM, 1))
for j in range(2):
    bpy.ops.mesh.primitive_cube_add(location=(-1.0, 2.58, 2.7 - j * 0.24))
    bar = bpy.context.object; bar.scale = (0.5, 0.01, 0.05); bar.data.materials.append(mBar)
    bar.parent = tag
    set_mblur_steps(bar)
# 札の落下（キーフレーム・bezier ease＋着地バウンス風・λ0.75 の減衰感）
if FE > FS:
    kb = min(FS + 40, FE)
    tag.location = (-1.0, 2.6, 2.6); tag.keyframe_insert('location', frame=FS)
    tag.location = (-1.0, 2.6, 1.55); tag.keyframe_insert('location', frame=kb)     # レジ上に着地
    # 着地の微バウンス
    kb2 = min(kb + 8, FE)
    tag.location = (-1.0, 2.6, 1.62); tag.keyframe_insert('location', frame=kb2)
    tag.rotation_euler = (0, 0, 0); tag.keyframe_insert('rotation_euler', frame=FS)
    tag.rotation_euler = (math.radians(6), 0, math.radians(-4)); tag.keyframe_insert('rotation_euler', frame=kb)

# ---- 埃/光条パーティクル ~2k（hair＝静止画でも可視・決定論seed・窓光でドリフト風）----
bpy.ops.mesh.primitive_cube_add(location=(1.2, ROOM_D * 0.5, 1.6))
dust_emit = bpy.context.object; dust_emit.name = 'dust_emitter'
dust_emit.scale = (2.0, ROOM_D * 0.4, 1.2)
dust_emit.hide_render = True   # エミッタ自体は不可視
try:
    dust_emit.modifiers.new('dust', 'PARTICLE_SYSTEM')
    dps = dust_emit.particle_systems[0].settings
    dps.type = 'HAIR'
    dps.count = 2000                 # §SH.1 埃/光条 ~2k
    dps.hair_length = 0.02
    dps.use_advanced_hair = True
    dps.render_type = 'PATH'   # HAIR で有効なのは PATH（HALO は emitter 専用）
    try: dps.use_emit_random = True
    except Exception: pass
    try: dust_emit.particle_systems[0].seed = 2035
    except Exception: pass
except Exception as e:
    print('dust particle skip', e)
mDust, du = new_mat('dust'); emissive(du, (1.0, 0.9, 0.75), 2.4); set_in(du, 'Base Color', (1, 1, 1, 1))
dust_emit.data.materials.append(mDust)

# ---- 窓外の強い暖色ライト（開口を通って体積ゴッドレイ）----
sun_d = bpy.data.lights.new('sun', 'AREA'); sun_d.energy = 9000; sun_d.color = WARM; sun_d.size = 3.0
sun = bpy.data.objects.new('sun', sun_d); sun.location = (7.0, ROOM_D * 0.5, 2.0); coll.objects.link(sun)
d = Vector((0, ROOM_D * 0.5, 1.2)) - Vector(sun.location); sun.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

# ---- 補助 area lights / softboxes（bpp_cycles.py 反射規律）----
def area(name, loc, energy, color, size=5):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    d = Vector((0, 3, 1)) - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
area('fill', (-2, -2, 2.4), 500, (0.5, 0.6, 0.9), 6)   # 冷い補助
area('rim', (0, 8, 2.8), 700, ACC_HI, 5)
def softbox(loc, size, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object; m, b = new_mat('sb'); emissive(b, color, strength); o.data.materials.append(m)
    d = Vector((0, 3, 1)) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
softbox((-6, -4, 3), 5, ACC_HI, 1.4)
softbox((-1, -6, 3.5), 6, (0.7, 0.8, 1.0), 0.8)

# ---- camera：奥→手前 dolly 0–72f（Easing風 bezier keyframe）----
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam); scene.camera = cam
cd.lens = 34
cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.2   # DOF f2.2
tgt = bpy.data.objects.new('tgt', None); tgt.location = (-1.0, 3.0, 1.1); coll.objects.link(tgt)  # カウンター＝焦点
cd.dof.focus_object = tgt
set_mblur_steps(cam)
CAM_A = (0.4, ROOM_D - 0.6, 1.6)    # 店の奥
CAM_B = (0.0, 1.0, 1.4)             # 手前（入口側）
def look_from(loc, look):
    d = Vector(look) - Vector(loc)
    return d.to_track_quat('-Z', 'Y').to_euler()
cam.location = CAM_A; cam.rotation_euler = look_from(CAM_A, (-0.6, 3.0, 1.2))
if FE > FS:
    kb = min(FS + 72, FE)   # 0–72f dolly
    cam.location = CAM_A; cam.rotation_euler = look_from(CAM_A, (-0.6, 3.0, 1.2))
    cam.keyframe_insert('location', frame=FS); cam.keyframe_insert('rotation_euler', frame=FS)
    cam.location = CAM_B; cam.rotation_euler = look_from(CAM_B, (-0.8, 2.6, 1.2))
    cam.keyframe_insert('location', frame=kb); cam.keyframe_insert('rotation_euler', frame=kb)

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

# ---- render（物理bake不要＝純Cycles）----
scene.render.image_settings.file_format = 'PNG'
if FE == FS:
    scene.render.filepath = OUT + '_cyc.png'
    bpy.ops.render.render(write_still=True)
    print('WROTE', scene.render.filepath)
else:
    scene.render.filepath = OUT + '/f_'
    bpy.ops.render.render(animation=True)
    print('WROTE SEQ', OUT)
