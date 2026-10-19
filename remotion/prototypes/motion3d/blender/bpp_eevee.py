import bpy, sys, math
from mathutils import Vector

# ---- args: OUT RX RY FS FE SAMPLES ----
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 1280)), int(A(2, 720))
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 64))
ACC = (0.10, 0.42, 1.0)     # accent (linearish blue ~#4ea1ff)
ACC_HI = (0.35, 0.70, 1.0)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
coll = scene.collection

# ---- engine (EEVEE Next / EEVEE) ----
engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
for cand in ['BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE']:
    if cand in engines:
        scene.render.engine = cand
        break
print('ENGINE =', scene.render.engine, '| available =', engines)

scene.render.resolution_x = RX
scene.render.resolution_y = RY
scene.render.film_transparent = False
scene.render.fps = 30
scene.frame_start, scene.frame_end = FS, FE

ee = scene.eevee
for a, v in [('taa_render_samples', SAMPLES), ('use_raytracing', True),
             ('use_ssr', True), ('use_gtao', True), ('use_shadows', True)]:
    if hasattr(ee, a):
        try: setattr(ee, a, v)
        except Exception as e: print('skip', a, e)
if hasattr(ee, 'ray_tracing_options'):
    try: ee.ray_tracing_options.use_denoise = True
    except Exception: pass

# ---- world: dark with faint blue ambient ----
world = bpy.data.worlds.new('W'); scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
bg.inputs[0].default_value = (0.008, 0.012, 0.025, 1)
bg.inputs[1].default_value = 0.6

# ---- helpers ----
def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree.nodes.get('Principled BSDF')

def set_in(bsdf, name, val):
    if name in bsdf.inputs:
        bsdf.inputs[name].default_value = val
        return True
    return False

def emissive(m, bsdf, color, strength):
    # Blender 4.x/5.x names
    if not set_in(bsdf, 'Emission Color', (*color, 1)):
        set_in(bsdf, 'Emission', (*color, 1))
    set_in(bsdf, 'Emission Strength', strength)

# ---- gem core (dark metallic, faceted) ----
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.15, location=(0, 0, 0))
gem = bpy.context.object; gem.name = 'gem'
for p in gem.data.polygons: p.use_smooth = False
gm, gb = new_mat('gemMetal')
set_in(gb, 'Base Color', (0.015, 0.03, 0.09, 1))
set_in(gb, 'Metallic', 0.88)
set_in(gb, 'Roughness', 0.16)
if not set_in(gb, 'Specular IOR Level', 0.7):
    set_in(gb, 'Specular', 0.7)
set_in(gb, 'Coat Weight', 0.35)      # クリアコートで艶
set_in(gb, 'Coat Roughness', 0.08)
emissive(gm, gb, ACC, 0.25)
gem.data.materials.append(gm)

# ---- glowing wireframe over the gem ----
wire = gem.copy(); wire.data = gem.data.copy(); wire.name = 'gemWire'
coll.objects.link(wire)
wmod = wire.modifiers.new('wf', 'WIREFRAME'); wmod.thickness = 0.03
wm, wb = new_mat('wireGlow')
set_in(wb, 'Base Color', (*ACC, 1))
emissive(wm, wb, ACC_HI, 6.0)
wire.data.materials.clear(); wire.data.materials.append(wm)

# ---- inner emissive core ----
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.5, location=(0, 0, 0))
core = bpy.context.object; core.name = 'core'
cm, cb = new_mat('coreGlow')
emissive(cm, cb, ACC_HI, 14.0)
core.data.materials.append(cm)

# ---- orbiting emissive satellites (parented to an empty for orbit anim) ----
piv = bpy.data.objects.new('pivot', None); coll.objects.link(piv)
sm, sb = new_mat('satGlow'); emissive(sm, sb, (0.9, 0.95, 1.0), 8.0)
set_in(sb, 'Base Color', (1, 1, 1, 1))
import random
random.seed(7)
for i in range(9):
    ang = i / 9 * math.tau
    r = 2.7 + random.random() * 0.5
    z = (random.random() - 0.5) * 1.4
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06 + random.random() * 0.05,
                                         location=(math.cos(ang) * r, math.sin(ang) * r, z))
    s = bpy.context.object; s.data.materials.append(sm)
    s.parent = piv

# ---- reflective floor ----
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -1.7))
fl = bpy.context.object
fm, fb = new_mat('floor')
set_in(fb, 'Base Color', (0.01, 0.015, 0.03, 1))
set_in(fb, 'Metallic', 0.9)
set_in(fb, 'Roughness', 0.28)
fl.data.materials.append(fm)

# ---- lights ----
def area(name, loc, energy, color, size=5):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    d = Vector((0, 0, 0)) - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob
area('key', (5, -4, 6), 1400, (1, 1, 1), 6)
area('fill', (-6, -2, 2), 700, ACC_HI, 7)
area('rim', (-2, 5, 4), 1100, (0.6, 0.8, 1.0), 5)

# 反射用ソフトボックス（画面外の発光板。金属面に映り込んで質感UP）
def softbox(loc, size, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object
    m, b = new_mat('sb'); emissive(m, b, color, strength)
    o.data.materials.append(m)
    d = Vector((0, 0, 0)) - Vector(loc)
    o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
softbox((-8, -5, 3), 5, ACC_HI, 3.2)
softbox((8, -5, 2.5), 5, (0.75, 0.88, 1.0), 2.4)
softbox((0, -9, 5), 6, (0.55, 0.72, 1.0), 1.8)

# ---- camera + DOF ----
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam); scene.camera = cam
cam.location = (2.6, -6.2, 1.7)
cd.lens = 55
cd.dof.use_dof = True
cd.dof.focus_object = gem
cd.dof.aperture_fstop = 2.2
d = Vector((0, 0, 0.1)) - Vector(cam.location)
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

# ---- animation (only if a range) ----
if FE > FS:
    gem.rotation_mode = wire.rotation_mode = 'XYZ'
    for ob, turns in [(gem, 0.25), (wire, 0.25), (piv, 0.5), (core, -0.15)]:
        ob.rotation_euler = (0, 0, 0); ob.keyframe_insert('rotation_euler', frame=FS)
        ob.rotation_euler = (0, 0, math.tau * turns); ob.keyframe_insert('rotation_euler', frame=FE)
    # camera slow dolly in
    cam.location = (2.6, -6.2, 1.7); cam.keyframe_insert('location', frame=FS)
    cam.location = (1.6, -5.2, 1.4); cam.keyframe_insert('location', frame=FE)

# ---- compositor bloom (Glare Fog Glow) — robust across Blender 4.x/5.x ----
def setup_bloom(scene):
    nt = None
    try:
        scene.use_nodes = True
        nt = scene.node_tree
    except Exception:
        nt = None
    if nt is None and hasattr(scene, 'compositing_node_group'):
        ng = bpy.data.node_groups.new('comp', 'CompositorNodeTree')
        scene.compositing_node_group = ng
        nt = ng
    if nt is None:
        print('BLOOM: no compositor API, skipping'); return
    for n in list(nt.nodes): nt.nodes.remove(n)
    rl = nt.nodes.new('CompositorNodeRLayers')
    gl = nt.nodes.new('CompositorNodeGlare')
    # Blender 5.x: Glare controls are INPUT SOCKETS, set via default_value
    def sock(name, val):
        if name in gl.inputs:
            try: gl.inputs[name].default_value = val; return True
            except Exception as e: print('sock fail', name, e)
        return False
    if not sock('Type', 'Bloom'):
        sock('Type', 'Fog Glow')
    sock('Quality', 'High')
    sock('Highlights Threshold', 0.75)
    sock('Highlights Smoothness', 0.3)
    sock('Strength', 1.0)
    sock('Size', 0.8)
    # Fallback for 4.x property API
    for attr, val in [('glare_type', 'FOG_GLOW')]:
        try: setattr(gl, attr, val)
        except Exception: pass
    # output node: Composite (4.x) or Group Output (5.x node group)
    out = None
    try:
        out = nt.nodes.new('CompositorNodeComposite')
    except Exception:
        pass
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
if FE == FS:
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = OUT + '_test.png'
    bpy.ops.render.render(write_still=True)
    print('WROTE', scene.render.filepath)
else:
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = OUT + '/f_'
    bpy.ops.render.render(animation=True)
    print('WROTE SEQ', OUT)
