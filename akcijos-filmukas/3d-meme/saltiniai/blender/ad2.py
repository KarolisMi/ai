"""Ad 2 · The meme shatters, revealing a tower of costs. An orange ball wrecks it; one clean €100 block lands."""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = os.path.join(HERE, "out", "ad2")
FRAMES = 192
MEME = os.environ.get("MEME_FRAME", os.path.join(HERE, "..", "v3", "build", "m02_last.png"))
sc = reset()
# high-key cream studio, unlike ad 1
studio(floor_color=srgb("#EDE7DE"), wall_color=srgb("#F6F1EA"), world=(0.6, 0.58, 0.55, 1), floor_rough=0.3)
light("AREA", (-6, -3, 8), (0, 0, 0), 2200, (1.0, 0.9, 0.8), size=6, name="key")
aim(bpy.data.objects["key"], (0, 4, 2))
light("AREA", (6, 0, 5), (0, 0, 0), 900, (0.8, 0.88, 1.0), size=5, name="fill")
aim(bpy.data.objects["fill"], (0, 4, 2))
light("AREA", (0, 10, 9), (0, 0, 0), 1200, (1, 0.95, 0.9), size=6, name="back")
aim(bpy.data.objects["back"], (0, 4, 2))

m_navy = mat("navy", srgb("#16304F"), rough=0.22, coat=1.0)
m_navy2 = mat("navy2", srgb("#2C5079"), rough=0.25, coat=1.0)
m_white = mat("white", srgb("#FFFFFF"), rough=0.4, emit=WHITE, emit_strength=0.15)
m_orange = mat("orange", srgb("#E07A4F"), rough=0.12, coat=1.0)
m_cream = mat("cream", srgb("#FFF8F0"), rough=0.3, coat=0.5)
m_ink = mat("ink", srgb("#16304F"), rough=0.4)
m_warm = mat("warmtxt", srgb("#B4532A"), rough=0.35)

# ---------- tower of costs ----------
bpy.ops.rigidbody.world_add()
rbw = sc.rigidbody_world
rbw.point_cache.frame_start, rbw.point_cache.frame_end = 1, FRAMES
rbw.substeps_per_frame = 20
rbw.solver_iterations = 25
cyc = bpy.data.objects["cyc"]
bpy.context.view_layer.objects.active = cyc
bpy.ops.rigidbody.object_add(type="PASSIVE")
cyc.rigid_body.collision_shape = "MESH"
labels = [("€850", 3.6, 1.5, 0.95, m_navy), ("+ HOSTING", 3.2, 1.0, 0.62, m_navy2), ("+ MONTHLY FEES", 3.0, 1.0, 0.5, m_navy), ("+ HIDDEN COSTS", 2.8, 1.0, 0.5, m_navy2)]
z = 0.0
blocks = []
for i, (s, w, h, ts, mm) in enumerate(labels):
    b = rounded_box(f"blk{i}", (w, 1.3, h), bevel=0.07, m=mm)
    b.location = (0.0 + (0.05 if i % 2 else -0.05), 6.0, z + h / 2)
    t = text(s, size=ts, extrude=0.03, bevel=0.004, name=f"lbl{i}")
    assign(t, m_white)
    t.parent = b
    t.location = (0, -0.68, -ts * 0.36)
    bpy.context.view_layer.objects.active = b
    bpy.ops.rigidbody.object_add(type="ACTIVE")
    b.rigid_body.collision_shape = "BOX"
    b.rigid_body.mass = 2.0 - i * 0.3
    b.rigid_body.friction = 0.7
    b.rigid_body.use_deactivation = True
    b.rigid_body.use_start_deactivated = True
    blocks.append(b)
    z += h + 0.002

# ---------- the wrecking ball ----------
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.75, segments=64, ring_count=32)
ball = bpy.context.object
ball.name = "ball"
bpy.ops.object.shade_smooth()
assign(ball, m_orange)
bpy.context.view_layer.objects.active = ball
bpy.ops.rigidbody.object_add(type="ACTIVE")
ball.rigid_body.collision_shape = "SPHERE"
ball.rigid_body.mass = 30
HIT = 40
key(ball, 1, location=(9.0, 4.0, 2.9))
key(ball, 22, location=(9.0, 4.0, 2.9))
key(ball, HIT, location=(1.75, 5.6, 2.4))
ease(ball, "LINEAR")
ball.rigid_body.kinematic = True
ball.rigid_body.keyframe_insert("kinematic", frame=HIT)
ball.rigid_body.kinematic = False
ball.rigid_body.keyframe_insert("kinematic", frame=HIT + 1)

# ---------- the €100 block lands ----------
nb = rounded_box("new", (3.4, 1.4, 1.7), bevel=0.12, m=m_cream)
nt = text("€100", size=1.25, extrude=0.06, bevel=0.01, name="newt")
assign(nt, m_warm)
nt.parent = nb
nt.location = (0, -0.74, -0.42)
tag = text("ALL-IN", size=0.34, extrude=0.02, bevel=0.003, font=FONT_SB, spacing=1.2, name="tag")
assign(tag, m_ink)
tag.parent = nb
tag.location = (0, -0.74, 0.5)
L = 92
key(nb, 1, location=(0, 3.0, 18), rotation_euler=(0, 0, 0.5))
key(nb, L - 14, location=(0, 3.0, 12), rotation_euler=(0, 0, 0.4))
key(nb, L, location=(0, 3.0, 0.85), rotation_euler=(0, 0, -0.04))
key(nb, L + 5, location=(0, 3.0, 1.25), rotation_euler=(0, 0, 0.02))
key(nb, L + 10, location=(0, 3.0, 0.85), rotation_euler=(0, 0, 0.0))
ease(nb)
for fc in fcurves(nb.animation_data.action):
    for kp in fc.keyframe_points:
        if kp.co[0] in (L, L + 10):
            kp.interpolation = "QUAD"
            kp.easing = "EASE_IN"


def rise_in(o, f, loc, out=None):
    x, y, zz = loc
    key(o, 1, location=(x, y, zz - 0.5), scale=(0.001,) * 3)
    key(o, f, location=(x, y, zz - 0.5), scale=(0.001,) * 3)
    key(o, f + 9, location=(x, y, zz), scale=(1, 1, 1))
    for fc in fcurves(o.animation_data.action):
        for kp in fc.keyframe_points:
            if kp.co[0] == f + 9:
                kp.interpolation, kp.easing = "BACK", "EASE_OUT"
    if out:
        key(o, out, location=(x, y, zz), scale=(1, 1, 1))
        key(o, out + 7, location=(x, y, zz + 0.4), scale=(0.001,) * 3)


a1 = text("No monthly fees.", size=0.62, extrude=0.04, bevel=0.005, name="a1")
assign(a1, m_ink)
rise_in(a1, 108, (0, 2.6, 4.35), out=146)
a2 = text("No hidden costs.", size=0.62, extrude=0.04, bevel=0.005, name="a2")
assign(a2, m_ink)
rise_in(a2, 116, (0, 2.6, 3.5), out=146)
pill = rounded_box("pill", (5.0, 0.3, 1.15), bevel=0.5, m=mat("pillm", srgb("#16304F"), rough=0.2, coat=1.0, emit=srgb("#16304F"), emit_strength=0.2))
ct = text("Comment “WEBSITE”", size=0.62, extrude=0.04, bevel=0.005, name="ct")
assign(ct, m_white)
ct.parent = pill
ct.location = (0, -0.18, -0.22)
rise_in(pill, 152, (0, 2.6, 4.0))
lg = logo(height=1.0, depth=0.14, m=m_navy)
url = text("beribus.com", size=0.6, extrude=0.04, bevel=0.005, font=FONT_SB, align="LEFT", name="url")
assign(url, m_ink)
grp = bpy.data.objects.new("brand", None)
bpy.context.collection.objects.link(grp)
lg.parent = grp
lg.location = (-1.75, 0, 0)
url.parent = grp
url.location = (-1.1, 0, 0.27)
rise_in(grp, 162, (0, 2.6, 5.35))

# ---------- camera + shatter ----------
cam, tgt = camera((0.0, -6.5, 2.4), (0.0, 6.0, 2.2), lens=30)
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 3.2
focus = bpy.data.objects.new("focus", None)
bpy.context.collection.objects.link(focus)
cam.data.dof.focus_object = focus
key(focus, 1, location=(0, 6.0, 2.2))
key(focus, L, location=(0, 3.0, 1.5))
key(focus, FRAMES, location=(0, 2.8, 2.5))
key(cam, 1, location=(0.0, -2.5, 2.3))
key(cam, 16, location=(0.0, -3.4, 2.5))
key(cam, HIT - 4, location=(1.6, -3.6, 2.8))
key(cam, 70, location=(-0.6, -5.0, 3.0))
key(cam, L + 8, location=(0.0, -4.6, 2.6))
key(cam, FRAMES, location=(0.0, -4.4, 2.9))
key(tgt, 1, location=(0.0, 6.0, 2.3))
key(tgt, HIT, location=(0.3, 6.0, 2.2))
key(tgt, L, location=(0.0, 3.0, 2.0))
key(tgt, FRAMES, location=(0.0, 2.8, 3.2))
ease(cam)
ease(tgt)
if os.path.exists(MEME):
    shatter(cam, MEME, f0=2, impact=(float(os.environ.get("IMPX", 0.5)), float(os.environ.get("IMPY", 0.45))), dist=0.6, power=0.9)

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
