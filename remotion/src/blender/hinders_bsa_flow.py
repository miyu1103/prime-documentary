# hinders_bsa_flow.py — EP35 F2 BSAOriginFlow ★ (SUPER-HEAVY / L3 ceiling)
#
# 3D手法: Blender Mantaflow **liquid(FLIP)** 流体シム。1970 BSA 由来の「汚れた資金」が
#         上流ドメインから小店ROIへ流下・分岐・滴下する抽象流体。
# 基準ソース: bpp_cycles.py（CYCLES/OPTIX→CPU・AgX・caustics OFF・softbox・DOF・bloom）
#           ＋ bpp_physics.py（bake→render animation 規律）。
# 引数規約: blender -b -P hinders_bsa_flow.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
#   FS==FE → テスト静止画 <OUT>_cyc.png（シムは進まない＝フォールバック静的geoで1枚出す）
#   else   → PNG連番 <OUT>/f_0001.png…（bake_all→render animation）
# invariant11: 実在肖像/判読テキスト/実ロゴ/実通貨なし＝抽象の濁った液体のみ。
# 決定論: random.seed 固定。
import bpy, sys, math, random
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 1920)), int(A(2, 1080))
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 200))   # §SH.1 Cycles ceiling 200 samples
random.seed(35)            # EP35 決定論

ACC = (0.10, 0.42, 1.0)          # Federal=冷スチール系アクセント
ACC_HI = (0.35, 0.70, 1.0)
GRIME = (0.16, 0.11, 0.045)      # 汚れた資金の暖い濁り（抽象色・実通貨は描かない）

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
coll = scene.collection

# ---- CYCLES + GPU（bpp_cycles.py の試行→CPUフォールバックを踏襲）----
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
# NOTE: caustics OFF on purpose — 液体ガラス＋caustics は一部フレームでレンダ時間爆発。
# Glare bloom がグローを供給するので、アニメレンダで再有効化しない（bpp_cycles.py と同方針）。
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
# Cycles の motion "steps" はオブジェクト単位（motion_steps）。値N→2^N サブステップ。
# N=4 → 2^4 = 16 サブステップ＝§SH.1 の motion blur steps=16 に対応。
def set_mblur_steps(obj, n=4):
    try: obj.cycles.motion_steps = n
    except Exception: pass

# ---- world: 薄霧ボリューム（体積ゴッドレイの下地）----
world = bpy.data.worlds.new('W'); scene.world = world
world.use_nodes = True
wn = world.node_tree
bg = wn.nodes.get('Background')
bg.inputs[0].default_value = (0.010, 0.016, 0.032, 1)
bg.inputs[1].default_value = 0.4
try:
    vs = wn.nodes.new('ShaderNodeVolumeScatter')
    vs.inputs['Density'].default_value = 0.020     # 薄霧＝key/rim光で流体に体積ゴッドレイ
    if 'Anisotropy' in vs.inputs:
        vs.inputs['Anisotropy'].default_value = 0.30
    wout = wn.nodes.get('World Output')
    wn.links.new(vs.outputs['Volume'], wout.inputs['Volume'])
except Exception as e:
    print('world volume skip', e)

# ---- material helpers（bpp_cycles.py 準拠）----
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

# 汚れた資金の液体＝濁ったガラス質（低IORの水寄り＋グライム着色）
mLiquid, lb = new_mat('dirtyLiquid')
set_in(lb, 'Base Color', (*GRIME, 1))
set_in(lb, 'Transmission Weight', 1.0)
set_in(lb, 'Roughness', 0.06)
set_in(lb, 'IOR', 1.33)

# 静的フォールバック用のメタル（上流の樋・下流の小店バット）
mMetal, mb = new_mat('metal')
set_in(mb, 'Base Color', (0.02, 0.03, 0.06, 1)); set_in(mb, 'Metallic', 0.9); set_in(mb, 'Roughness', 0.28)

# ---- Mantaflow liquid domain（res=192・adaptive・secondary・low viscosity）----
DOM_LOC = (0, 0, 1.0)
bpy.ops.mesh.primitive_cube_add(location=DOM_LOC)
domain = bpy.context.object; domain.name = 'fluid_domain'
domain.scale = (3.2, 2.2, 3.0)   # 上流(上)→小店(下) の縦長ドメイン
domain.data.materials.append(mLiquid)
fmod = domain.modifiers.new('Fluid', 'FLUID')
fmod.fluid_type = 'DOMAIN'
ds = fmod.domain_settings
ds.domain_type = 'LIQUID'
for attr, val in [
    ('resolution_max', 192),           # §SH.1 res=192（super-heavy）
    ('use_adaptive_domain', True),     # adaptive domain
    ('use_mesh', True),                # 滑らかな液体メッシュ生成
    ('use_spray_particles', True),     # secondary: spray
    ('use_foam_particles', True),      # secondary: foam
    ('use_bubble_particles', True),    # secondary: bubble
    ('use_viscosity', True),
    ('viscosity_value', 0.05),         # 低粘度＝よく流れて滴下する
    ('cache_frame_start', FS),
    ('cache_frame_end', FE),
]:
    try: setattr(ds, attr, val)
    except Exception as e: print('domain attr skip', attr, e)
set_mblur_steps(domain)

# ---- inflow（上流ドメイン＝資金の湧出口）----
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 2.4))
inflow = bpy.context.object; inflow.name = 'bsa_inflow'
inflow.scale = (0.5, 0.5, 0.25)
inflow.data.materials.append(mLiquid)
ifmod = inflow.modifiers.new('Fluid', 'FLUID')
ifmod.fluid_type = 'FLOW'
fl = ifmod.flow_settings
fl.flow_type = 'LIQUID'
fl.flow_behavior = 'INFLOW'
try: fl.use_inflow = True
except Exception: pass

# ---- effector（中段の分岐障害物＝流れを枝分かれ・滴下させる）----
bpy.ops.mesh.primitive_cube_add(location=(0.4, 0, 0.9), rotation=(0, math.radians(28), 0))
baffle = bpy.context.object; baffle.name = 'branch_baffle'
baffle.scale = (0.9, 1.4, 0.06)
baffle.data.materials.append(mMetal)
efmod = baffle.modifiers.new('Fluid', 'FLUID')
efmod.fluid_type = 'EFFECTOR'
try: efmod.effector_settings.effector_type = 'COLLISION'
except Exception: pass

# ---- 小店ROI の受けバット（下流・静的可視geo：静止画でも黒にしない保険）----
bpy.ops.mesh.primitive_cube_add(location=(0, 0, -1.15))
basin = bpy.context.object; basin.name = 'small_store_basin'
basin.scale = (1.6, 1.1, 0.12)
basin.data.materials.append(mMetal)
bfmod = basin.modifiers.new('Fluid', 'FLUID')
bfmod.fluid_type = 'EFFECTOR'
try: bfmod.effector_settings.effector_type = 'COLLISION'
except Exception: pass

# 上流の樋（静的可視geo）＋ フォールバック滴（静止画で液体を必ず1つ見せる）
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 2.05))
spout = bpy.context.object; spout.name = 'upstream_spout'
spout.scale = (0.55, 0.55, 0.08); spout.data.materials.append(mMetal)
for i in range(7):
    z = 1.7 - i * 0.42
    x = (random.random() - 0.5) * 0.5
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.10 + random.random() * 0.06, location=(x, 0, z))
    drp = bpy.context.object
    for p in drp.data.polygons: p.use_smooth = True
    drp.data.materials.append(mLiquid)
    set_mblur_steps(drp)

# ---- lights / softboxes（bpp_cycles.py 準拠・霧で体積化）----
def area(name, loc, energy, color, size=6):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    d = Vector((0, 0, 0)) - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
area('key', (5, -5, 7), 2000, (1, 1, 1), 7)
area('fill', (-6, -3, 3), 900, ACC_HI, 7)
area('rim', (-2, 6, 6), 1500, (0.6, 0.8, 1.0), 6)   # 冷色rim＝流体に体積ゴッドレイ
def softbox(loc, size, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object; m, b = new_mat('sb'); emissive(b, color, strength); o.data.materials.append(m)
    d = Vector((0, 0, 0)) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
softbox((-8, -5, 4), 5, ACC_HI, 1.4)     # §SH bpp_cycles softbox 1.4/1.1/0.8
softbox((8, -5, 3), 5, (0.75, 0.88, 1.0), 1.1)
softbox((0, -9, 6), 6, (0.55, 0.72, 1.0), 0.8)

# ---- camera：上流→小店へ 0–48f dolly＋見下ろしtilt（keyframe=bezier default）----
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam); scene.camera = cam
cd.lens = 42
cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.2   # §SH DOF f2.2
tgt = bpy.data.objects.new('tgt', None); tgt.location = (0, 0, 0.4); coll.objects.link(tgt)
cd.dof.focus_object = tgt
set_mblur_steps(cam)
CAM_A = (2.6, -8.2, 3.2)   # 上流寄り・やや高所
CAM_B = (1.6, -6.6, 1.6)   # 小店へ寄り・見下ろし解消（tilt）
def look_from(loc, look=(0, 0, 0.4)):
    d = Vector(look) - Vector(loc)
    return d.to_track_quat('-Z', 'Y').to_euler()
cam.location = CAM_A; cam.rotation_euler = look_from(CAM_A, (0, 0, 1.6))
if FE > FS:
    kb = min(FS + 48, FE)   # 0–48f dolly
    cam.location = CAM_A; cam.rotation_euler = look_from(CAM_A, (0, 0, 1.6))
    cam.keyframe_insert('location', frame=FS); cam.keyframe_insert('rotation_euler', frame=FS)
    cam.location = CAM_B; cam.rotation_euler = look_from(CAM_B, (0, 0, -0.6))  # 見下ろしtilt
    cam.keyframe_insert('location', frame=kb); cam.keyframe_insert('rotation_euler', frame=kb)

# ---- compositor bloom（Blender 5.x node group + socket API・bpp_cycles.py 準拠）----
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

# ---- bake（bpp_physics.py 規律：アニメ時のみ bake→render animation）----
scene.render.image_settings.file_format = 'PNG'
if FE == FS:
    # 静止画テスト：Mantaflow はシムが進まない＝静的フォールバックgeoで1枚出す。
    scene.render.filepath = OUT + '_cyc.png'
    bpy.ops.render.render(write_still=True)
    print('WROTE', scene.render.filepath)
else:
    # 流体キャッシュを bake（headless Mantaflow は重い／モーダル問題あり＝try保護）。
    bpy.context.view_layer.objects.active = domain
    for o in bpy.context.selected_objects: o.select_set(False)
    domain.select_set(True)
    try:
        if hasattr(bpy.context, 'temp_override'):
            with bpy.context.temp_override(scene=scene, active_object=domain,
                                           object=domain, selected_objects=[domain]):
                bpy.ops.fluid.bake_all()
        else:
            bpy.ops.fluid.bake_all()
        print('FLUID BAKED')
    except Exception as e:
        print('fluid bake err (headless Mantaflow heavy/may need GUI bake):', e)
    scene.render.filepath = OUT + '/f_'
    bpy.ops.render.render(animation=True)
    print('WROTE SEQ', OUT)
