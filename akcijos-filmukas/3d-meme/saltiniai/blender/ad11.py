"""Ad 11 · Creeper blast continues in 3D: voxels fly at the lens, freeze, and the fire blocks assemble into €100."""
import math, os, random, sys
import bpy, bmesh
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = os.path.join(HERE, "out", "ad11")
FRAMES = 150
sc = reset()
sc.render.fps = 25
R = random.Random(11)

world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.16, 0.42, 1.0, 1); bg.inputs[1].default_value = 1.0
sun = light("SUN", (0, 0, 10), (0, 0, 0), 4.2, (1.0, 0.95, 0.86), name="sun"); sun.rotation_euler = (math.radians(50), 0, math.radians(-35)); sun.data.angle = math.radians(3)
fill = light("AREA", (0, -14, 6), (0, 0, 0), 900, (0.8, 0.88, 1.0), size=8, name="fill"); aim(fill, (0, 0, 2.5))

def cube_mesh(name, s, bevel=0.06):
    me = bpy.data.meshes.new(name); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=s)
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=s * bevel, segments=2, affect="EDGES")
    bm.to_mesh(me); bm.free(); return me

M = {k: mat(k, srgb(c), rough=r, emit=srgb(c) if e else None, emit_strength=e) for k, c, r, e in
     [("grass", "#5FA034", 0.8, 0), ("dirt", "#8B5A2B", 0.85, 0), ("stone", "#8A8D91", 0.7, 0), ("fire", "#D9481A", 0.35, 0.35), ("fire2", "#F28A1E", 0.35, 0.5), ("cloud", "#FFFFFF", 0.9, 0.4), ("txt", "#FFFFFF", 0.4, 0.3), ("pill", "#E07A4F", 0.3, 0.6)]}

# ground: 1m voxels with grass tops, a crater in the middle
gme = bpy.data.meshes.new("ground"); bm = bmesh.new()
for ix in range(-24, 25):
    for iy in range(-12, 40):
        z = 0
        r = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.translate(bm, verts=r["verts"], vec=(ix, iy, z - 0.5))
bm.to_mesh(gme); bm.free()
ground = bpy.data.objects.new("ground", gme); bpy.context.collection.objects.link(ground)
gme.materials.append(M["dirt"]); gme.materials.append(M["grass"])
for p in gme.polygons: p.material_index = 1 if p.normal.z > 0.5 else 0
# Minecraft clouds
for i in range(7):
    cme = bpy.data.meshes.new("c"); bm = bmesh.new(); r = bmesh.ops.create_cube(bm, size=1.0); bmesh.ops.scale(bm, vec=(R.uniform(4, 9), R.uniform(2, 4), 0.8), verts=r["verts"]); bm.to_mesh(cme); bm.free()
    c = bpy.data.objects.new("cloud", cme); bpy.context.collection.objects.link(c); cme.materials.append(M["cloud"]); c.location = (R.uniform(-16, 16), R.uniform(14, 30), R.uniform(9, 14))

# pixel font for €100
PIX = {"€": ["00110", "01001", "11100", "01000", "11100", "01001", "00110"], "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"], "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"]}
S = 0.4; word = "€100"; cols = len(word) * 6 - 1
targets = []
for ci, ch in enumerate(word):
    for ry, row in enumerate(PIX[ch]):
        for cx, v in enumerate(row):
            if v == "1": targets.append(Vector(((ci * 6 + cx) * S - cols * S / 2 + S / 2, 0.5, 3.2 + (6 - ry) * S)))
R.shuffle(targets)

O = Vector((0, 1.0, 0.6))
small = cube_mesh("vox", S * 0.95); big = cube_mesh("voxb", 0.7)
def ballistic(p0, v, t):  # t in seconds of "explosion time"
    return p0 + v * t + Vector((0, 0, -4.0)) * t * t
# explosion time is fast at first, then freezes (slow-mo)
FT = [(1, 0.0), (3, 0.06), (6, 0.15), (10, 0.26), (15, 0.36), (21, 0.43), (28, 0.47), (36, 0.49)]
blocks = []
N_FIRE = len(targets); N_OTHER = 150
for i in range(N_FIRE + N_OTHER):
    fire = i < N_FIRE
    o = bpy.data.objects.new("b", small if fire else big); bpy.context.collection.objects.link(o)
    o.data = small.copy() if False else (small if fire else big)
    o.active_material = None
    ms = M["fire2" if fire and R.random() < 0.3 else "fire"] if fire else M[R.choice(["grass", "dirt", "dirt", "stone"])]
    o.material_slots and None
    o.data = o.data  # shared mesh
    o.color = (1, 1, 1, 1)
    # per-object material via object-linked slot
    if not o.data.materials: o.data.materials.append(None)
    o.material_slots[0].link = "OBJECT"; o.material_slots[0].material = ms
    # velocity: many toward the camera (-y)
    th = R.uniform(0, 2 * math.pi); up = R.uniform(0.15, 1.0)
    toward = R.random() < 0.55
    d = Vector((math.cos(th) * R.uniform(0.3, 1.0), -R.uniform(0.6, 1.4) if toward else math.sin(th) * R.uniform(0.3, 1.0), up)).normalized()
    v = d * R.uniform(9, 22)
    rot0 = Vector((R.uniform(-6, 6), R.uniform(-6, 6), R.uniform(-6, 6)))
    for f, tt in FT:
        p = ballistic(O, v, tt)
        if p.z < 0.3 and not fire: p.z = 0.3
        sc_ = 0.2 if f == 1 else 1.0
        key(o, f, location=p, rotation_euler=rot0 * tt * 2.2, scale=(sc_,) * 3)
    if fire:
        tgt = targets[i]; f0 = 40 + int(R.random() * 22); f1 = f0 + 14
        key(o, f0, location=ballistic(O, v, 0.49), rotation_euler=rot0 * 0.49 * 2.2, scale=(1, 1, 1))
        key(o, f1, location=tgt, rotation_euler=(0, 0, 0), scale=(1, 1, 1))
        for fc in fcurves(o.animation_data.action):
            for kp in fc.keyframe_points:
                if kp.co[0] == f1: kp.interpolation, kp.easing = "BACK", "EASE_OUT"
    else:
        # the rest drops out of the frozen moment and falls away
        f0 = 40 + int(R.random() * 10); p = ballistic(O, v, 0.49)
        key(o, f0, location=p, rotation_euler=rot0 * 0.49 * 2.2)
        key(o, f0 + 16, location=(R.uniform(-9, 9), R.uniform(3, 14), 0.35), rotation_euler=(0, 0, rot0.z))
    blocks.append(o)

# white flash continuing from the meme
fl_m = mat("flash", srgb("#FFFFFF"), emit=srgb("#FFF6E0"), emit_strength=30)
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=O); flash = bpy.context.object; assign(flash, fl_m)
key(flash, 1, scale=(2.5, 2.5, 2.5)); key(flash, 5, scale=(5, 5, 5)); key(flash, 9, scale=(0.01, 0.01, 0.01))
es = fl_m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
for f, v in ((1, 60), (5, 20), (9, 0)): es.default_value = v; es.keyframe_insert("default_value", frame=f)
pl = light("POINT", tuple(O), (0, 0, 0), 0, (1, 0.7, 0.4), size=0.5, name="boom")
for f, v in ((1, 80000), (6, 20000), (18, 0)): pl.data.energy = v; pl.data.keyframe_insert("energy", frame=f)

# copy and CTA
t1 = text("WEBSITE · LIVE IN 5 DAYS", size=0.85, extrude=0.08, bevel=0.01, name="t1"); assign(t1, M["txt"]); t1.rotation_euler = (math.radians(90), 0, 0)
key(t1, 1, location=(0, 0.4, 1.0), scale=(0.001,) * 3); key(t1, 82, location=(0, 0.4, 1.0), scale=(0.001,) * 3); key(t1, 94, location=(0, 0.4, 2.05), scale=(1, 1, 1))
pill = rounded_box("pill", (8.2, 0.5, 1.5), bevel=0.6, m=M["pill"])
ct = text("Comment “WEBSITE”", size=0.82, extrude=0.06, bevel=0.008, name="ct"); assign(ct, M["txt"]); ct.rotation_euler = (math.radians(90), 0, 0); ct.parent = pill; ct.location = (0, -0.3, -0.29)
key(pill, 1, location=(0, -0.6, -2), scale=(0.001,) * 3); key(pill, 100, location=(0, -0.6, -2), scale=(0.001,) * 3); key(pill, 112, location=(0, -0.6, 0.95), scale=(1, 1, 1))
for o in (t1, pill):
    for fc in fcurves(o.animation_data.action):
        for kp in fc.keyframe_points:
            if kp.co[0] in (94, 112): kp.interpolation, kp.easing = "BACK", "EASE_OUT"
lg = logo(height=0.7, m=M["txt"]) if "logo" in globals() else None
if lg:
    lg.rotation_euler = (math.radians(90), 0, 0); key(lg, 1, location=(0, 0.6, 9.0), scale=(0.001,) * 3); key(lg, 120, location=(0, 0.6, 9.0), scale=(0.001,) * 3); key(lg, 130, location=(0, 0.6, 7.6), scale=(1.4, 1.4, 1.4))

cam, tgt = camera((0, -4.5, 2.0), (0, 1, 1.2), lens=26)
shake = [(1, (0.25, -4.5, 2.2)), (2, (-0.2, -4.5, 1.8)), (3, (0.18, -4.6, 2.15)), (4, (-0.12, -4.7, 1.9)), (6, (0.06, -5.0, 2.05))]
for f, p in shake: key(cam, f, location=p)
key(cam, 30, location=(0, -12.0, 3.0)); key(cam, 70, location=(0, -14.5, 3.8)); key(cam, FRAMES, location=(1.2, -13.6, 3.5))
key(tgt, 1, location=(0, 1, 1.2)); key(tgt, 30, location=(0, 0.5, 2.8)); key(tgt, 70, location=(0, 0.5, 4.4)); key(tgt, FRAMES, location=(0, 0.5, 4.3))
ease(cam); ease(tgt)

render_setup(sc, OUT, FRAMES, samples=int(os.environ.get("SAMPLES", 10)))
sc.render.fps = 25
frames = os.environ.get("ONLY")
if frames:
    for f in [int(x) for x in frames.split(",")]:
        sc.frame_set(f); sc.render.filepath = os.path.join(OUT, f"test_{f:04d}"); bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
