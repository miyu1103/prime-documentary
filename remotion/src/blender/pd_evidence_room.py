"""PD Visual System P09 — PD EVIDENCE ROOM (reusable procedural set, C1 minimum).

One reusable set (NOT rebuilt per episode): records desk, evidence board (blank
paste-slots for Remotion overlays), verdict monitor (emissive), map table. Brand
lighting: navy/black/silver + electric-blue emission (no flat wash, no readable
text baked — invariant 11). Camera chosen by ARGV. C1 = 3 fixed/near-frontal
cams. EEVEE Next, AgX, Glare bloom. Follows remotion/prototypes/motion3d/blender/
bpp_eevee.py (engine/lights/bloom/render) + aircash_cashstack.py (_act_fcurves).

ARGV CONTRACT:
    blender -b -P pd_evidence_room.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES> [CAMERA]
    FS==FE -> single test still <OUT>_test.png ; FS<FE -> PNG seq <OUT>/f_0001.png
    CAMERA in {cam1_enter_room, cam2_push_desk, cam3_pan_board} (default cam2).
SMOKE (3-frame sequence catches anim bugs a single still hides):
    blender -b -P remotion/src/blender/pd_evidence_room.py -- out/evroom/_smoke 1920 1080 1 3 48 cam2_push_desk
"""
import bpy, sys, math
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out/evroom')
RX, RY = int(A(1, 1920)), int(A(2, 1080))
FS, FE = int(A(3, 1)), int(A(4, 1))
SAMPLES = int(A(5, 96))
CAMERA = str(A(6, 'cam2_push_desk'))

# brand tokens (linear-ish RGB)
NAVY = (0.017, 0.040, 0.075)
ELEC = (0.043, 0.176, 1.0)
ELEC_HI = (0.12, 0.42, 1.0)
SILVER = (0.60, 0.63, 0.69)
GOLD = (0.78, 0.46, 0.05)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
coll = scene.collection

# ---- engine ----
engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
for cand in ['BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE']:
    if cand in engines:
        scene.render.engine = cand; break
print('ENGINE =', scene.render.engine)
scene.render.resolution_x, scene.render.resolution_y = RX, RY
scene.render.fps = 30
scene.frame_start, scene.frame_end = FS, FE
try:
    scene.view_settings.view_transform = 'AgX'
except Exception as e:
    print('AgX skip', e)
ee = scene.eevee
for a, v in [('taa_render_samples', SAMPLES), ('use_raytracing', True),
             ('use_ssr', True), ('use_gtao', True), ('use_shadows', True)]:
    if hasattr(ee, a):
        try: setattr(ee, a, v)
        except Exception as e: print('skip', a, e)

world = bpy.data.worlds.new('W'); scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
bg.inputs[0].default_value = (0.006, 0.010, 0.020, 1); bg.inputs[1].default_value = 0.35

def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree.nodes.get('Principled BSDF')
def set_in(b, name, val):
    if name in b.inputs:
        b.inputs[name].default_value = val; return True
    return False
def emissive(m, b, color, strength):
    if not set_in(b, 'Emission Color', (*color, 1)):
        set_in(b, 'Emission', (*color, 1))
    set_in(b, 'Emission Strength', strength)
def box(name, loc, scale, color, metallic=0.0, rough=0.6):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    m, b = new_mat(name)
    set_in(b, 'Base Color', (*color, 1)); set_in(b, 'Metallic', metallic); set_in(b, 'Roughness', rough)
    o.data.materials.append(m); return o
def panel(name, loc, scale, color, strength):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    o.rotation_euler = (math.radians(90), 0, 0)  # face -Y (toward cameras)
    m, b = new_mat(name); emissive(m, b, color, strength)
    o.data.materials.append(m); return o

# ---- room shell ----
box('floor', (0, 1, 0), (16, 16, 0.1), (0.010, 0.016, 0.030), metallic=0.85, rough=0.32)
box('backwall', (0, 5, 3), (16, 0.2, 8), NAVY, rough=0.75)
box('leftwall', (-7, 1, 3), (0.2, 12, 8), NAVY, rough=0.8)
box('rightwall', (7, 1, 3), (0.2, 12, 8), NAVY, rough=0.8)
# records desk (silver metallic slab)
box('records_desk', (0, 1.2, 0.9), (3.4, 1.6, 0.18), SILVER, metallic=0.85, rough=0.25)
box('desk_leg1', (-1.4, 1.2, 0.45), (0.16, 0.16, 0.9), (0.05, 0.06, 0.08), metallic=0.7, rough=0.4)
box('desk_leg2', (1.4, 1.2, 0.45), (0.16, 0.16, 0.9), (0.05, 0.06, 0.08), metallic=0.7, rough=0.4)
# evidence board on back wall + 3 blank paste slots (lighter = Remotion overlay targets)
box('evidence_board', (0, 4.88, 3.2), (5.2, 0.12, 2.6), (0.02, 0.03, 0.05), rough=0.8)
for i, x in enumerate((-1.6, 0.0, 1.6)):
    p = panel(f'board_slot_{i}', (x, 4.80, 3.3), (1.3, 1.5, 1), (0.06, 0.09, 0.16), 0.4)
# verdict monitor (emissive electric screen) — corner-export target for later
mon = panel('MONITOR_SCREEN', (-3.4, 4.80, 3.0), (2.4, 1.5, 1), ELEC, 1.6)
box('monitor_bezel', (-3.4, 4.9, 3.0), (2.7, 0.1, 1.75), (0.05, 0.06, 0.08), metallic=0.6, rough=0.3)
# map table (emissive slab on desk)
maptab = panel('map_table', (0, 1.2, 1.02), (2.6, 1.2, 1), ELEC_HI, 0.7)
maptab.rotation_euler = (0, 0, 0)  # lay flat

# ---- lights (brand) ----
def area(name, loc, energy, color, size=6, target=(0, 2, 1.5)):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    d = Vector(target) - Vector(loc); ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob
area('key', (5, -4, 6.5), 1400, (0.85, 0.9, 1.0), 8)
area('fill', (-6, -2, 3), 700, ELEC_HI, 8)
area('rim', (-2, 6.5, 5), 1000, GOLD, 5)
def softbox(loc, size, color, strength, target=(0, 2, 1.5)):
    bpy.ops.mesh.primitive_plane_add(size=size, location=loc)
    o = bpy.context.object
    m, b = new_mat('sb'); emissive(m, b, color, strength); o.data.materials.append(m)
    d = Vector(target) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
softbox((-8, -5, 4), 5, ELEC_HI, 3.0)
softbox((8, -5, 3), 5, (0.75, 0.88, 1.0), 2.2)

# ---- cameras (C1: fixed / near-frontal) ----
CAMS = {
    # more dramatic travels so the 3D space reads as space (bigger dolly + lateral + descent)
    'cam1_enter_room': dict(a=(-3.2, -10.5, 3.8), b=(0.6, -5.2, 1.8), lens=30, look=(0, 2.4, 1.6)),
    'cam2_push_desk':  dict(a=(2.6, -7.4, 3.0), b=(-0.4, -2.9, 1.15), lens=42, look=(0, 1.4, 1.0)),
    'cam3_pan_board':  dict(a=(-3.6, -3.4, 3.2), b=(3.6, -3.4, 3.0), lens=38, look=(0, 4.85, 3.2)),
}
cfg = CAMS.get(CAMERA, CAMS['cam2_push_desk'])
cd = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new(CAMERA, cd)
coll.objects.link(cam); scene.camera = cam
cd.lens = cfg['lens']
def aim(loc, look):
    return (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
if FE > FS:
    cam.location = cfg['a']; cam.rotation_euler = aim(cfg['a'], cfg['look'])
    cam.keyframe_insert('location', frame=FS); cam.keyframe_insert('rotation_euler', frame=FS)
    cam.location = cfg['b']; cam.rotation_euler = aim(cfg['b'], cfg['look'])
    cam.keyframe_insert('location', frame=FE); cam.keyframe_insert('rotation_euler', frame=FE)
else:
    cam.location = cfg['a']; cam.rotation_euler = aim(cfg['a'], cfg['look'])

# ---- bloom (Glare) ----
def setup_bloom(scene):
    try:
        scene.use_nodes = True; nt = scene.node_tree
    except Exception:
        nt = None
    if nt is None and hasattr(scene, 'compositing_node_group'):
        ng = bpy.data.node_groups.new('comp', 'CompositorNodeTree'); scene.compositing_node_group = ng; nt = ng
    if nt is None:
        print('BLOOM skip'); return
    for n in list(nt.nodes): nt.nodes.remove(n)
    rl = nt.nodes.new('CompositorNodeRLayers'); gl = nt.nodes.new('CompositorNodeGlare')
    def sock(name, val):
        if name in gl.inputs:
            try: gl.inputs[name].default_value = val; return True
            except Exception: return False
        return False
    if not sock('Type', 'Bloom'): sock('Type', 'Fog Glow')
    sock('Quality', 'High'); sock('Highlights Threshold', 0.8); sock('Strength', 0.9); sock('Size', 0.8)
    try: setattr(gl, 'glare_type', 'FOG_GLOW')
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
    print('BLOOM ok')
setup_bloom(scene)

# ---- render ----
scene.render.image_settings.file_format = 'PNG'
if FE == FS:
    scene.render.filepath = OUT + '_test.png'
    bpy.ops.render.render(write_still=True); print('WROTE', scene.render.filepath)
else:
    scene.render.filepath = OUT + '/f_'
    bpy.ops.render.render(animation=True); print('WROTE SEQ', OUT)
