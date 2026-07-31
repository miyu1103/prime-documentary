"""EP60 surfside — HERO: PUNCHING SHEAR at a slab-column connection.

WHAT THIS IS: an explanatory diagram, not a reconstruction. It shows the mechanism NIST
described — two connections between garage columns and the pool deck failed, the column
heads punched through the slab, and their load transferred to neighbouring columns that
were not strong enough to carry it. Abstract geometry only: no building likeness, no
debris, no readable text, no seals (invariant 11 / R-39). Nothing here depicts the
collapse of Champlain Towers South; it depicts how a flat-slab connection fails.

WHY IT EXISTS: measured 2026-07-31 — nothing in Remotion, After Effects or the Blender
scene library renders a building section, a slab, a column or a load path, and the archive
shelf has no rebar/spalling/corrosion footage at all (rebar=1, corrosion=0, spalling=0
across 171,597 ledger rows). This shot is the film's central physical idea and it has to
be built.

DETERMINISTIC BY CONSTRUCTION: no random, no physics solver. Every motion is a keyframed
transform, so frame N is identical on every run and the render is resumable frame-by-frame
(scripts/render_rolin_heroes.sh skips frames already on disk).

ARGV: blender -b -P surfside_section.py -- <OUT> <RX> <RY> <FS> <FE> <SAMPLES>
SMOKE (3 frames — a single frame cannot catch a sequence bug):
    blender -b -P surfside_section.py -- out/ep60_smoke 960 540 44 46 48
FULL (6.0s at 30fps):
    blender -b -P surfside_section.py -- out/hero_section 3840 2160 1 180 160

TIMELINE (30fps, 180 frames = 6.0s)
    f1-40    the grid stands. slow camera push. load glow even across all nine columns.
    f40-52   the two front-centre connections brighten and strain (overload).
    f52-88   PUNCH: the two column heads rise through the slab; a shear cone drops around
             each; the ring of slab at the connection separates.
    f88-140  the slab sags between the punched pair; load glow migrates outward to the
             neighbouring columns, which brighten past the level the failed pair ever had.
    f140-180 hold on the redistributed grid, camera still drifting. no resolution.
"""

import bpy, sys, math, os
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def A(i, d): return argv[i] if i < len(argv) else d
OUT = A(0, 'out')
RX, RY = int(A(1, 3840)), int(A(2, 2160))
FS, FE = int(A(3, 1)), int(A(4, 180))
SAMPLES = int(A(5, 160))

CONCRETE = (0.055, 0.060, 0.068, 1.0)   # cold grey, institutional
LOAD_OK = (0.30, 0.62, 0.95)            # calm blue — load being carried
LOAD_HOT = (1.00, 0.55, 0.16)           # amber — load a column should not be carrying
RIM = (0.55, 0.75, 1.00)

# beat frames
F_STRAIN, F_PUNCH, F_PUNCH_END, F_MIGRATE, F_HOLD = 40, 52, 88, 140, 180

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
coll = scene.collection

# ---- engine ---------------------------------------------------------------
_engs = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
for _c in ['BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE']:
    if _c in _engs:
        scene.render.engine = _c
        break
print('ENGINE =', scene.render.engine)
ee = scene.eevee
for _a, _v in [('taa_render_samples', SAMPLES), ('use_raytracing', True), ('use_ssr', True),
               ('use_gtao', True), ('use_shadows', True), ('use_volumetric_shadows', True)]:
    if hasattr(ee, _a):
        try: setattr(ee, _a, _v)
        except Exception as _e: print('eevee skip', _a, _e)
if hasattr(ee, 'volumetric_samples'):
    try: ee.volumetric_samples = 64
    except Exception: pass
if hasattr(ee, 'ray_tracing_options'):
    try: ee.ray_tracing_options.use_denoise = True
    except Exception: pass

scene.render.resolution_x = RX
scene.render.resolution_y = RY
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.frame_start, scene.frame_end = FS, FE
scene.view_settings.view_transform = 'AgX'
scene.render.use_motion_blur = True
scene.render.motion_blur_shutter = 0.5
try:
    _ep = bpy.context.preferences.edit
    _ep.keyframe_new_interpolation_type = 'BEZIER'
    _ep.keyframe_new_handle_type = 'AUTO_CLAMPED'
except Exception: pass

world = bpy.data.worlds.new('W'); scene.world = world; world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
bg.inputs[0].default_value = (0.008, 0.011, 0.018, 1)
bg.inputs[1].default_value = 0.45


# ---- helpers --------------------------------------------------------------
def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree.nodes.get('Principled BSDF')


def set_in(b, n, v):
    if n in b.inputs:
        b.inputs[n].default_value = v
        return True
    return False


def emissive(b, color, strength):
    if not set_in(b, 'Emission Color', (*color, 1)):
        set_in(b, 'Emission', (*color, 1))
    set_in(b, 'Emission Strength', strength)


def emit_socket(b):
    """The socket to keyframe for emission strength, or None."""
    return b.inputs['Emission Strength'] if 'Emission Strength' in b.inputs else None


def key_emit(b, frame, strength, color=None):
    s = emit_socket(b)
    if s is None:
        return
    if color is not None:
        if not set_in(b, 'Emission Color', (*color, 1)):
            set_in(b, 'Emission', (*color, 1))
        c = b.inputs.get('Emission Color') or b.inputs.get('Emission')
        if c is not None:
            c.keyframe_insert('default_value', frame=frame)
    s.default_value = strength
    s.keyframe_insert('default_value', frame=frame)


def act_fcurves(ad):
    """Blender 5.x removed Action.fcurves. Walk layers->strips->channelbags instead.

    Returns every fcurve on the action, on 4.x and 5.x alike. Getting this wrong is silent:
    `getattr(action, 'fcurves', [])` yields [] on 5.1, so an interpolation-fixing loop
    written the old way does nothing at all and the motion ships linear.
    """
    if ad is None or ad.action is None:
        return []
    act = ad.action
    fcs = list(getattr(act, 'fcurves', []) or [])
    if fcs:
        return fcs
    for layer in getattr(act, 'layers', []) or []:
        for strip in getattr(layer, 'strips', []) or []:
            for bag in getattr(strip, 'channelbags', []) or []:
                fcs.extend(list(getattr(bag, 'fcurves', []) or []))
    return fcs


def ease(obj_or_data):
    """Force bezier/auto-clamped on everything this object animates (no linear motion)."""
    ad = getattr(obj_or_data, 'animation_data', None)
    n = 0
    for fc in act_fcurves(ad):
        for kp in fc.keyframe_points:
            kp.interpolation = 'BEZIER'
            kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
            n += 1
    return n


# ---- geometry: the flat-slab grid -----------------------------------------
SLAB_Z = 0.0
SLAB_T = 0.34            # slab thickness
COL_R = 0.42             # column radius
COL_H = 3.2              # storey height below the slab
PITCH = 4.2              # column spacing
GRID = [-1, 0, 1]

slab_mat, slab_b = new_mat('slab')
set_in(slab_b, 'Base Color', (0.105, 0.112, 0.124, 1))
set_in(slab_b, 'Roughness', 0.80)
set_in(slab_b, 'Metallic', 0.0)

# the deck slab, with the two failing bays cut out as separate shear cones below
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, SLAB_Z))
slab = bpy.context.object
slab.name = 'slab'
slab.scale = (PITCH * 3.4 / 2, PITCH * 3.4 / 2, SLAB_T / 2)
slab.data.materials.append(slab_mat)
bev = slab.modifiers.new('bev', 'BEVEL'); bev.width = 0.012; bev.segments = 2

# garage floor — the columns must stand on something or the shot reads as floating shapes
bpy.ops.mesh.primitive_plane_add(size=46, location=(0, 0, SLAB_Z - SLAB_T / 2 - COL_H))
garage_floor = bpy.context.object
garage_floor.name = 'garage_floor'
gm, gb = new_mat('garage_floor')
set_in(gb, 'Base Color', (0.030, 0.033, 0.038, 1))
set_in(gb, 'Roughness', 0.62)
set_in(gb, 'Metallic', 0.0)
garage_floor.data.materials.append(gm)

# columns
FAIL = [(0, -1), (1, -1)]   # the two front connections that fail (NIST: two connections)
columns = {}
col_bsdf = {}
for gx in GRID:
    for gy in GRID:
        x, y = gx * PITCH, gy * PITCH
        bpy.ops.mesh.primitive_cylinder_add(radius=COL_R, depth=COL_H, vertices=32,
                                            location=(x, y, SLAB_Z - SLAB_T / 2 - COL_H / 2))
        c = bpy.context.object
        c.name = 'col_%d_%d' % (gx, gy)
        m, b = new_mat(c.name)
        set_in(b, 'Base Color', CONCRETE)
        set_in(b, 'Roughness', 0.8)
        hot = (gx, gy) in FAIL
        emissive(b, LOAD_HOT if hot else LOAD_OK, 0.12 if hot else 0.07)
        c.data.materials.append(m)
        columns[(gx, gy)] = c
        col_bsdf[(gx, gy)] = b

# capitals: a short flare at each column head, so the connection reads as a connection
for (gx, gy), c in columns.items():
    bpy.ops.mesh.primitive_cone_add(radius1=COL_R * 1.05, radius2=COL_R * 1.9, depth=0.42,
                                    vertices=32,
                                    location=(gx * PITCH, gy * PITCH, SLAB_Z - SLAB_T / 2 - 0.21))
    cap = bpy.context.object
    cap.name = 'cap_%d_%d' % (gx, gy)
    cap.data.materials.append(slab_mat)

# ---- the punch: a shear cone per failing connection ------------------------
# A truncated cone of slab, wider at the top, that drops away as the column head rises
# through it. This IS punching shear: the column punches up, the cone drops out.
cones = []
for (gx, gy) in FAIL:
    x, y = gx * PITCH, gy * PITCH
    bpy.ops.mesh.primitive_cone_add(radius1=COL_R * 1.15, radius2=COL_R * 3.4,
                                    depth=SLAB_T * 1.02, vertices=40,
                                    location=(x, y, SLAB_Z))
    cone = bpy.context.object
    cone.name = 'shearcone_%d_%d' % (gx, gy)
    m, b = new_mat(cone.name)
    set_in(b, 'Base Color', (0.075, 0.078, 0.086, 1))
    set_in(b, 'Roughness', 0.9)
    emissive(b, LOAD_HOT, 0.0)
    cone.data.materials.append(m)
    cones.append((cone, b, Vector((x, y, SLAB_Z))))

# fracture ring: eight wedges around each failing connection that separate outward
ring_parts = []
for (gx, gy) in FAIL:
    x, y = gx * PITCH, gy * PITCH
    for i in range(8):
        a = i * math.pi / 4
        r = COL_R * 3.1
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x + math.cos(a) * r, y + math.sin(a) * r, SLAB_Z))
        w = bpy.context.object
        w.name = 'frag_%d_%d_%02d' % (gx, gy, i)
        w.scale = (0.34, 0.20, SLAB_T / 2 * 0.96)
        w.rotation_euler = (0, 0, a)
        w.data.materials.append(slab_mat)
        ring_parts.append((w, Vector((math.cos(a), math.sin(a), 0.0))))

# ---- animation -------------------------------------------------------------
# Authored ALWAYS, never `if FE > FS`. With the old guard a single-frame preview
# skipped this block entirely and rendered the end state, so frames 30, 70 and 150
# came out pixel-identical. Measured before the fix: 0 changed pixels between them.
if True:
    # 1. the failing columns strain, then punch UP through the slab
    for (gx, gy) in FAIL:
        c = columns[(gx, gy)]
        z0 = c.location.z
        c.location.z = z0
        c.keyframe_insert('location', frame=F_STRAIN)
        c.location.z = z0 + 0.06                 # strain: the head presses into the slab
        c.keyframe_insert('location', frame=F_PUNCH)
        c.location.z = z0 + SLAB_T * 1.5         # punch through
        c.keyframe_insert('location', frame=F_PUNCH_END)
        c.keyframe_insert('location', frame=F_HOLD)
        ease(c)

    # 2. the shear cones drop out of the slab
    for cone, b, base in cones:
        cone.location = base
        cone.keyframe_insert('location', frame=F_PUNCH)
        cone.location = Vector((base.x, base.y, base.z - 1.15))
        cone.keyframe_insert('location', frame=F_PUNCH_END)
        cone.location = Vector((base.x, base.y, base.z - 1.35))
        cone.keyframe_insert('location', frame=F_HOLD)
        # the fracture surface flares as it separates, then cools
        key_emit(b, F_PUNCH, 0.0)
        key_emit(b, F_PUNCH + 8, 1.1)
        key_emit(b, F_PUNCH_END, 0.12)
        ease(cone)
        ease(cone.data.materials[0].node_tree)

    # 3. the fracture ring separates outward and tips
    for w, outward in ring_parts:
        p0 = w.location.copy()
        w.location = p0
        w.keyframe_insert('location', frame=F_PUNCH)
        w.rotation_euler = w.rotation_euler.copy()
        w.keyframe_insert('rotation_euler', frame=F_PUNCH)
        w.location = p0 + outward * 0.22 + Vector((0, 0, -0.16))
        w.keyframe_insert('location', frame=F_PUNCH_END)
        w.rotation_euler = (w.rotation_euler.x + 0.14, w.rotation_euler.y - 0.10, w.rotation_euler.z)
        w.keyframe_insert('rotation_euler', frame=F_PUNCH_END)
        w.keyframe_insert('location', frame=F_HOLD)
        ease(w)

    # 4. load migrates: the failed pair goes dark, the neighbours take the amber
    for (gx, gy), b in col_bsdf.items():
        failing = (gx, gy) in FAIL
        neighbour = (not failing) and any(abs(gx - fx) <= 1 and abs(gy - fy) <= 1 for fx, fy in FAIL)
        key_emit(b, F_STRAIN, 0.12 if failing else 0.07, LOAD_HOT if failing else LOAD_OK)
        if failing:
            key_emit(b, F_PUNCH, 0.85, LOAD_HOT)          # overload flare
            key_emit(b, F_PUNCH_END, 0.02, LOAD_HOT)     # then it carries nothing
            key_emit(b, F_HOLD, 0.02, LOAD_HOT)
        elif neighbour:
            key_emit(b, F_PUNCH_END, 0.10, LOAD_OK)
            key_emit(b, F_MIGRATE, 0.55, LOAD_HOT)       # brighter than the pair ever was
            key_emit(b, F_HOLD, 0.65, LOAD_HOT)
        else:
            key_emit(b, F_MIGRATE, 0.14, LOAD_OK)
            key_emit(b, F_HOLD, 0.16, LOAD_OK)
        ease(b.id_data)

    # 5. the slab sags between the punched pair
    slab.scale = slab.scale.copy(); slab.keyframe_insert('scale', frame=F_PUNCH)
    slab.location = Vector((0, 0, SLAB_Z)); slab.keyframe_insert('location', frame=F_PUNCH)
    slab.location = Vector((0, 0, SLAB_Z - 0.10)); slab.keyframe_insert('location', frame=F_MIGRATE)
    slab.location = Vector((0, 0, SLAB_Z - 0.13)); slab.keyframe_insert('location', frame=F_HOLD)
    ease(slab)

# ---- lights ---------------------------------------------------------------
def area(name, loc, energy, color, size=6, target=Vector((0, 0, SLAB_Z - 1.0))):
    ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color; ld.size = size
    ob = bpy.data.objects.new(name, ld); ob.location = loc; coll.objects.link(ob)
    ob.rotation_euler = (target - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()

area('key', (8, -12, SLAB_Z - 0.95), 1500, (1.0, 0.97, 0.93), 8)
area('fill', (-12, -7, SLAB_Z - 1.9), 380, RIM, 10)
area('rim', (-6, 10, SLAB_Z - 1.35), 620, (0.55, 0.72, 1.0), 8)
area('under', (0, -4, SLAB_Z - COL_H + 0.4), 520, LOAD_OK, 14, target=Vector((0, 0, SLAB_Z - 0.5)))

area('soffit', (0.6, -PITCH * 1.15, SLAB_Z - 1.05), 780, (0.80, 0.86, 1.0), 13,
     target=Vector((0, 0, SLAB_Z + 0.4)))

# faint haze so the depth of the grid reads
bpy.ops.mesh.primitive_cube_add(size=34, location=(0, 0, SLAB_Z - 1.4))
vol = bpy.context.object
vm = bpy.data.materials.new('haze'); vm.use_nodes = True
vnt = vm.node_tree
for n in list(vnt.nodes):
    if n.type == 'BSDF_PRINCIPLED':
        vnt.nodes.remove(n)
pv = vnt.nodes.new('ShaderNodeVolumePrincipled')
pv.inputs['Density'].default_value = 0.006
vnt.links.new(pv.outputs['Volume'], vnt.nodes.get('Material Output').inputs['Volume'])
vol.data.materials.append(vm)

# ---- camera: low, under the deck, drifting in on the failing pair ----------
LOOK = Vector((PITCH * 0.28, -PITCH * 0.05, SLAB_Z - 0.50))
CAM_START = Vector((PITCH * 1.75, -PITCH * 3.35, SLAB_Z - COL_H * 0.80))
CAM_END = Vector((PITCH * 1.35, -PITCH * 2.60, SLAB_Z - COL_H * 0.66))
cd = bpy.data.cameras.new('cam')
cam = bpy.data.objects.new('cam', cd)
coll.objects.link(cam)
scene.camera = cam
cd.lens = 30
cd.dof.use_dof = True
cd.dof.aperture_fstop = 3.4
cam.location = CAM_START
cam.rotation_euler = (LOOK - CAM_START).to_track_quat('-Z', 'Y').to_euler()
cd.dof.focus_distance = (CAM_START - LOOK).length
if True:
    cam.location = CAM_START; cam.keyframe_insert('location', frame=FS)
    cam.location = CAM_END; cam.keyframe_insert('location', frame=FE)
    cam.rotation_euler = (LOOK - CAM_START).to_track_quat('-Z', 'Y').to_euler()
    cam.keyframe_insert('rotation_euler', frame=FS)
    cam.rotation_euler = (LOOK - CAM_END).to_track_quat('-Z', 'Y').to_euler()
    cam.keyframe_insert('rotation_euler', frame=FE)
    cd.dof.focus_distance = (CAM_START - LOOK).length; cd.dof.keyframe_insert('focus_distance', frame=FS)
    cd.dof.focus_distance = (CAM_END - LOOK).length; cd.dof.keyframe_insert('focus_distance', frame=FE)
    n = ease(cam) + ease(cd)
    print('EASED camera keyframes =', n)

# ---- bloom ----------------------------------------------------------------
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
        print('BLOOM: skip'); return
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    rl = nt.nodes.new('CompositorNodeRLayers')
    gl = nt.nodes.new('CompositorNodeGlare')
    def sock(name, val):
        if name in gl.inputs:
            try: gl.inputs[name].default_value = val
            except Exception as e: print('sock', name, e)
    if 'Type' in gl.inputs:
        try: gl.inputs['Type'].default_value = 'Bloom'
        except Exception: sock('Type', 'Fog Glow')
    sock('Quality', 'High'); sock('Highlights Threshold', 0.85); sock('Strength', 0.9); sock('Size', 0.75)
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

scene.render.image_settings.file_format = 'PNG'
os.makedirs(OUT if FE > FS else (os.path.dirname(OUT) or '.'), exist_ok=True)
if FE == FS:
    # scene.frame_set() is MANDATORY here. render(write_still=True) renders frame_current,
    # which is 1 on a fresh file, and without a frame_set the depsgraph has never evaluated
    # the animation at all — so the still comes out showing every object at its AUTHORED
    # (end-state) transform. That defect produced four consecutive "frame 30" previews of
    # this scene that were really the finished collapse. Inherited from the tyler template.
    scene.frame_set(FS)
    scene.render.filepath = OUT + '_test.png'
    bpy.ops.render.render(write_still=True)
    print('WROTE', scene.render.filepath, 'at frame', scene.frame_current)
else:
    scene.render.filepath = OUT + '/f_'
    bpy.ops.render.render(animation=True)
    print('WROTE SEQ', OUT, FS, '..', FE)
