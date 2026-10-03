"""Ad 1 · Price smash. A baseball flies out of the lens, blows a giant €850 apart, €100 lands."""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = os.path.join(HERE, "out", "ad1")
FRAMES = 204  # 8.5 s @ 24 fps
sc = reset()
studio()

# ---------- lights ----------
light("AREA", (-5, -4, 7), (0, 0, 0), 2600, (1.0, 0.86, 0.74), size=5, name="key")
aim(bpy.data.objects["key"], (0, 4, 1.5))
light("AREA", (6, 8, 4), (0, 0, 0), 1800, (0.55, 0.7, 1.0), size=4, name="rim")
aim(bpy.data.objects["rim"], (0, 4, 1.5))
light("AREA", (0, -2, 11), (0, 0, 0), 350, (1, 1, 1), size=8, name="top")
aim(bpy.data.objects["top"], (0, 4, 0))
light("SPOT", (0, 0, 9), (0, 0, 0), 9000, (0.35, 0.5, 0.9), name="wallglow", spot=1.2)
aim(bpy.data.objects["wallglow"], (0, 16, 6))

# ---------- materials ----------
m_white = mat("white", srgb("#F2EFEA"), rough=0.28, coat=0.6)
m_old = mat("old", srgb("#C9CED8"), rough=0.35, coat=0.3)
m_price = mat("price", srgb("#E07A4F"), rough=0.18, coat=1.0)
m_txt = mat("txt", WHITE, rough=0.4, emit=WHITE, emit_strength=0.25)
m_peach = mat("peach", PEACH, rough=0.3, emit=PEACH, emit_strength=0.2)
m_leather = mat("leather", srgb("#F4F1EA"), rough=0.55)
m_seam = mat("seam", srgb("#C2312B"), rough=0.5)
m_logo = mat("logo", srgb("#2C5079"), rough=0.12, metal=0.6, coat=1.0)
m_pill = mat("pill", srgb("#B4532A"), rough=0.25, coat=1.0, emit=srgb("#B4532A"), emit_strength=0.6)

# ---------- €850, to be smashed ----------
old = to_mesh(text("€850", size=3.0, extrude=0.35, bevel=0.03, name="old"))
old.location = (0, 6.5, 0)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)
assign(old, m_old)
letters = split_loose(old)

# ---------- floor collider + rigid bodies ----------
bpy.ops.rigidbody.world_add()
rbw = sc.rigidbody_world
rbw.point_cache.frame_start, rbw.point_cache.frame_end = 1, FRAMES
rbw.substeps_per_frame = 20
rbw.solver_iterations = 20
cyc = bpy.data.objects["cyc"]
bpy.context.view_layer.objects.active = cyc
bpy.ops.rigidbody.object_add(type="PASSIVE")
cyc.rigid_body.collision_shape = "MESH"
cyc.rigid_body.friction = 0.6
for L in letters:
    bpy.context.view_layer.objects.active = L
    bpy.ops.rigidbody.object_add(type="ACTIVE")
    L.rigid_body.collision_shape = "CONVEX_HULL"
    L.rigid_body.mass = 0.5
    L.rigid_body.friction = 0.5
    L.rigid_body.restitution = 0.2
    L.rigid_body.use_deactivation = True
    L.rigid_body.use_start_deactivated = True

# ---------- baseball ----------
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.42, segments=64, ring_count=32)
ball = bpy.context.object
ball.name = "ball"
bpy.ops.object.shade_smooth()
assign(ball, m_leather)
pts = []
for i in range(241):
    t = i / 240 * 2 * math.pi
    lat = 0.9 * math.sin(2 * t)
    pts.append((math.cos(lat) * math.cos(t) * 0.425, math.cos(lat) * math.sin(t) * 0.425, math.sin(lat) * 0.425))
cu = bpy.data.curves.new("seam", "CURVE")
cu.dimensions = "3D"
sp = cu.splines.new("POLY")
sp.points.add(len(pts) - 1)
for p, (x, y, z) in zip(sp.points, pts):
    p.co = (x, y, z, 1)
sp.use_cyclic_u = True
cu.bevel_depth = 0.022
cu.bevel_resolution = 2
seam = bpy.data.objects.new("seam", cu)
bpy.context.collection.objects.link(seam)
seam.data.materials.append(m_seam)
seam.parent = ball
bpy.context.view_layer.objects.active = ball
bpy.ops.rigidbody.object_add(type="ACTIVE")
ball.rigid_body.collision_shape = "SPHERE"
ball.rigid_body.mass = 6
ball.rigid_body.restitution = 0.3
HIT = 16
key(ball, 1, location=(0.25, -8.7, 1.75), rotation_euler=(0, 0, 0))
key(ball, HIT, location=(0.35, 6.0, 1.6), rotation_euler=(4.0, 2.0, 1.0))
ball.rigid_body.kinematic = True
ball.rigid_body.keyframe_insert("kinematic", frame=HIT)
ball.rigid_body.kinematic = False
ball.rigid_body.keyframe_insert("kinematic", frame=HIT + 1)
ease(ball, "LINEAR")

# ---------- €100 drops in ----------
new = text("€100", size=3.4, extrude=0.42, bevel=0.045, name="price")
assign(new, m_price)
DROP = 62
key(new, 1, location=(0, 2.6, 16), rotation_euler=(math.pi / 2, 0, 0.0), scale=(1, 1, 1))
key(new, DROP, location=(0, 2.6, 9), rotation_euler=(math.pi / 2, 0, 0.35))
key(new, DROP + 12, location=(0, 2.6, 0.0), rotation_euler=(math.pi / 2, 0, -0.06))
key(new, DROP + 17, location=(0, 2.6, 0.55), rotation_euler=(math.pi / 2, 0, 0.03))
key(new, DROP + 22, location=(0, 2.6, 0.0), rotation_euler=(math.pi / 2, 0, 0.0))
key(new, DROP + 25, location=(0, 2.6, 0.12))
key(new, DROP + 28, location=(0, 2.6, 0.0))
ease(new, "BEZIER")
for fc in fcurves(new.animation_data.action):
    for kp in fc.keyframe_points:
        if kp.co[0] in (DROP + 12, DROP + 22, DROP + 28):
            kp.interpolation = "QUAD"
            kp.easing = "EASE_IN"

# ---------- copy, slides in after the landing ----------
def slide_in(o, f, z, dx=0.0, out=None):
    key(o, 1, location=(dx, 3.0, z - 0.6), scale=(0.001, 0.001, 0.001))
    key(o, f, location=(dx, 3.0, z - 0.6), scale=(0.001, 0.001, 0.001))
    key(o, f + 10, location=(dx, 3.0, z), scale=(1, 1, 1))
    for fc in fcurves(o.animation_data.action):
        for kp in fc.keyframe_points:
            if kp.co[0] == f + 10:
                kp.interpolation = "BACK"
                kp.easing = "EASE_OUT"
    if out:
        key(o, out, location=(dx, 3.0, z), scale=(1, 1, 1))
        key(o, out + 8, location=(dx, 3.0, z + 0.5), scale=(0.001, 0.001, 0.001))

t1 = text("FIRST 10 CLIENTS ONLY", size=0.6, extrude=0.04, bevel=0.006, font=FONT_SB, spacing=1.15, name="t1")
assign(t1, m_peach)
slide_in(t1, 98, 5.35, out=150)
t2 = text("Your website in 5 days", size=0.86, extrude=0.06, bevel=0.008, name="t2")
assign(t2, m_txt)
slide_in(t2, 108, 4.2, out=150)

# CTA: pill + text, then logo + url
bpy.ops.mesh.primitive_cube_add(size=1)
pill = bpy.context.object
pill.name = "pill"
pill.scale = (5.4, 0.3, 1.3)
bpy.ops.object.transform_apply(scale=True)
bev = pill.modifiers.new("bev", "BEVEL")
bev.width = 0.45
bev.segments = 12
bev.limit_method = "NONE"
assign(pill, m_pill)
cta = text("DM “WEBSITE”", size=0.86, extrude=0.05, bevel=0.006, name="cta")
assign(cta, m_txt)
cta.parent = pill
cta.location = (0, -0.19, -0.32)
cta.rotation_euler = (math.pi / 2, 0, 0)
slide_in(pill, 156, 4.5)
lg = logo(height=1.25, depth=0.16, m=m_logo)
url = text("beribus.com", size=0.72, extrude=0.04, bevel=0.005, font=FONT_SB, align="LEFT", name="url")
assign(url, m_txt)
grp = bpy.data.objects.new("brand", None)
bpy.context.collection.objects.link(grp)
lg.parent = grp
lg.location = (-2.05, 0, 0.0)
url.parent = grp
url.location = (-1.15, 0, 0.36)
slide_in(grp, 166, 6.0)

# ---------- camera ----------
cam, tgt = camera((0.2, -9.0, 1.7), (0.3, 6.0, 1.6), lens=28, dof=None)
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.8
focus = bpy.data.objects.new("focus", None)
bpy.context.collection.objects.link(focus)
cam.data.dof.focus_object = focus
key(focus, 1, location=(0.3, -6, 1.6))
key(focus, HIT, location=(0.3, 6.0, 1.6))
key(focus, DROP, location=(0, 3.6, 1.5))
key(focus, FRAMES, location=(0, 3.2, 2.0))
key(cam, 1, location=(0.2, -9.0, 1.7))
key(cam, HIT + 2, location=(0.0, -7.6, 1.8))
key(cam, 46, location=(2.2, -8.0, 2.6))
key(cam, DROP + 10, location=(0.0, -8.6, 2.6))
key(cam, 120, location=(0.0, -7.9, 2.3))
key(cam, FRAMES, location=(0.0, -7.4, 2.2))
key(tgt, 1, location=(0.3, 6.0, 1.6))
key(tgt, HIT + 2, location=(0.3, 6.0, 1.5))
key(tgt, 46, location=(0.0, 6.0, 1.2))
key(tgt, DROP + 10, location=(0.0, 3.4, 2.6))
key(tgt, FRAMES, location=(0.0, 3.4, 3.2))
ease(cam)
ease(tgt)

render_setup(sc, OUT, FRAMES, samples=int(os.environ.get("SAMPLES", 16)), blur=os.environ.get("BLUR", "1") == "1")
sc.cycles.adaptive_threshold = 0.03
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
