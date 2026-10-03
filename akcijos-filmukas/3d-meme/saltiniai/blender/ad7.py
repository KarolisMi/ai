"""Ad 7 · The meme plays on a tall display; we pull back as gold coins rain down and a €100 tag swings in."""
import math
import os
import random
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = os.path.join(HERE, "out", "ad7")
FRAMES = 186
SEQ = os.environ.get("SEQ", os.path.join(HERE, "..", "v3", "build", "seq07"))
NSEQ = len([f for f in os.listdir(SEQ) if f.endswith(".png")]) if os.path.isdir(SEQ) else 1
sc = reset()
studio(floor_color=srgb("#0C1420"), wall_color=srgb("#14233A"), world=(0.005, 0.008, 0.015, 1), floor_rough=0.18)
light("AREA", (-5, -3, 8), (0, 0, 0), 2000, (1.0, 0.85, 0.65), size=5, name="key")
aim(bpy.data.objects["key"], (0, 4, 1.5))
light("AREA", (5, 9, 4), (0, 0, 0), 1500, (0.5, 0.7, 1.0), size=4, name="rim")
aim(bpy.data.objects["rim"], (0, 4, 1.5))
light("SPOT", (0, 2, 10), (0, 0, 0), 4000, (1.0, 0.85, 0.6), name="top", spot=0.9)
aim(bpy.data.objects["top"], (0, 4, 0))

scr_mat = seq_material("meme", os.path.join(SEQ, "s_0001.png"), NSEQ) if os.path.isdir(SEQ) else mat("blank", srgb("#222222"))
dev, hs = device("totem", scr_mat, hs=3.6, body_color="#20252E")
dev.location = (-1.6, 5.2, 2.55)

bpy.ops.rigidbody.world_add()
rbw = sc.rigidbody_world
rbw.point_cache.frame_start, rbw.point_cache.frame_end = 1, FRAMES
rbw.substeps_per_frame = 15
rbw.solver_iterations = 15
cyc = bpy.data.objects["cyc"]
bpy.context.view_layer.objects.active = cyc
bpy.ops.rigidbody.object_add(type="PASSIVE")
cyc.rigid_body.collision_shape = "MESH"
for o in (dev, [c for c in dev.children if c.name.startswith("stand")][0]):
    bpy.context.view_layer.objects.active = o
    bpy.ops.rigidbody.object_add(type="PASSIVE")
    o.rigid_body.collision_shape = "BOX"

m_gold = mat("gold", srgb("#E8B04A"), rough=0.22, metal=1.0)
bpy.ops.mesh.primitive_cylinder_add(radius=0.32, depth=0.06, vertices=48)
proto = bpy.context.object
bv = proto.modifiers.new("b", "BEVEL")
bv.width = 0.015
bv.segments = 3
bpy.ops.object.modifier_apply(modifier="b")
bpy.ops.object.shade_smooth()
assign(proto, m_gold)
proto.hide_render = True
proto.location = (0, 0, -50)
rnd = random.Random(7)
for i in range(80):
    c = proto.copy()
    c.data = proto.data
    c.hide_render = False
    bpy.context.collection.objects.link(c)
    c.location = (rnd.uniform(-3.2, 3.2), rnd.uniform(2.6, 6.0), rnd.uniform(9, 12))
    c.rotation_euler = (rnd.uniform(0, 3), rnd.uniform(0, 3), rnd.uniform(0, 3))
    bpy.context.view_layer.objects.active = c
    bpy.ops.rigidbody.object_add(type="ACTIVE")
    c.rigid_body.collision_shape = "CYLINDER"
    c.rigid_body.mass = 0.1
    c.rigid_body.restitution = 0.35
    c.rigid_body.friction = 0.6
    c.rigid_body.kinematic = True
    rel = 34 + int(i * 0.75) + rnd.randint(0, 6)
    c.rigid_body.keyframe_insert("kinematic", frame=rel)
    c.rigid_body.kinematic = False
    c.rigid_body.keyframe_insert("kinematic", frame=rel + 1)

# swinging price tag
tag = rounded_box("tag", (2.6, 0.12, 1.5), bevel=0.25, m=mat("tagm", srgb("#FFF6EC"), rough=0.35, coat=0.6))
tt = text("€100", size=1.0, extrude=0.04, bevel=0.006, name="tt")
assign(tt, mat("tagt", srgb("#B4532A"), rough=0.3))
tt.parent = tag
tt.location = (0, -0.07, -0.42)
hole = text("THE WHOLE PRICE", size=0.17, extrude=0.01, bevel=0.0, font=FONT_SB, spacing=1.2, name="ht")
assign(hole, mat("ink", srgb("#16304F"), rough=0.4))
hole.parent = tag
hole.location = (0, -0.07, 0.42)
pivot = bpy.data.objects.new("tagpivot", None)
bpy.context.collection.objects.link(pivot)
tag.parent = pivot
tag.location = (0, 0, -1.6)
string = rounded_box("string", (0.03, 0.03, 1.0), bevel=0.01, m=mat("str", srgb("#C9CED8"), rough=0.5))
string.parent = pivot
string.location = (0, 0, -0.42)
T0 = 92
key(pivot, 1, location=(1.6, 3.2, 12), rotation_euler=(0, 0, 0))
key(pivot, T0, location=(1.6, 3.2, 12), rotation_euler=(0, 0.4, 0))
key(pivot, T0 + 12, location=(1.6, 3.2, 5.0), rotation_euler=(0, -0.35, 0))
for k, ang in enumerate((0.22, -0.13, 0.07, -0.03, 0.0)):
    key(pivot, T0 + 20 + k * 9, rotation_euler=(0, ang, 0))
ease(pivot)

m_white = mat("white", WHITE, rough=0.35, emit=WHITE, emit_strength=0.4)
m_gold_t = mat("goldt", srgb("#F2C66D"), rough=0.25, metal=0.8, emit=srgb("#F2C66D"), emit_strength=0.25)


def rise_in(o, f, loc):
    x, y, zz = loc
    key(o, 1, location=(x, y, zz - 0.3), scale=(0.001,) * 3)
    key(o, f, location=(x, y, zz - 0.3), scale=(0.001,) * 3)
    key(o, f + 9, location=(x, y, zz), scale=(1, 1, 1))
    for fc in fcurves(o.animation_data.action):
        for kp in fc.keyframe_points:
            if kp.co[0] == f + 9:
                kp.interpolation, kp.easing = "BACK", "EASE_OUT"


t1 = text("No monthly fees.", size=0.5, extrude=0.04, bevel=0.005, font=FONT_SB, name="t1")
assign(t1, m_white)
rise_in(t1, 132, (0.0, 2.4, 6.55))
pill = rounded_box("pill", (4.3, 0.3, 1.0), bevel=0.42, m=mat("pillm", srgb("#E07A4F"), rough=0.2, coat=1.0, emit=srgb("#E07A4F"), emit_strength=0.6))
ct = text("DM “WEBSITE”", size=0.6, extrude=0.04, bevel=0.005, name="ct")
assign(ct, m_white)
ct.parent = pill
ct.location = (0, -0.18, -0.21)
rise_in(pill, 142, (0.0, 2.4, 5.55))
url = text("beribus.com · first 10 clients", size=0.36, extrude=0.03, bevel=0.004, font=FONT_SB, name="url")
assign(url, m_gold_t)
rise_in(url, 152, (0.0, 2.4, 4.75))

cam, tgt, d = pull_out_camera(dev, hs, lens=30, fill=0.995)
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.6
focus = bpy.data.objects.new("focus", None)
bpy.context.collection.objects.link(focus)
cam.data.dof.focus_object = focus
start = cam.location.copy()
key(focus, 1, location=dev.location)
key(focus, 90, location=(0, 4.0, 2.0))
key(focus, FRAMES, location=(0.5, 3.0, 4.0))
key(cam, 1, location=start)
key(cam, 6, location=start)
key(cam, 50, location=(-0.4, -2.6, 3.0))
key(cam, 100, location=(0.6, -6.6, 3.6))
key(cam, FRAMES, location=(0.3, -7.4, 4.2))
key(tgt, 1, location=(dev.location.x, dev.location.y + 5, dev.location.z))
key(tgt, 6, location=(dev.location.x, dev.location.y + 5, dev.location.z))
key(tgt, 50, location=(-0.6, 5.0, 2.4))
key(tgt, 100, location=(0.4, 4.0, 3.2))
key(tgt, FRAMES, location=(0.3, 3.0, 4.3))
ease(cam)
ease(tgt)

render_setup(sc, OUT, FRAMES, samples=int(os.environ.get("SAMPLES", 10)))
bpy.ops.ptcache.bake_all(bake=True)
if os.environ.get("START"):
    sc.frame_start = int(os.environ["START"])
frames = os.environ.get("ONLY")
if frames:
    for f in [int(x) for x in frames.split(",")]:
        sc.frame_set(f)
        sc.render.filepath = os.path.join(OUT, f"test_{f:04d}")
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
