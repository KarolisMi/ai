"""Ad 4 · The meme shatters. Ten glossy tokens on a slowly turning stage light up one by one: only 10 spots."""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = os.path.join(HERE, "out", "ad4")
FRAMES = 180
MEME = os.environ.get("MEME_FRAME", os.path.join(HERE, "..", "v3", "build", "m04_last.png"))
sc = reset()
# deep plum-to-navy stage
studio(floor_color=srgb("#0B0F18"), wall_color=srgb("#1A1430"), world=(0.004, 0.004, 0.01, 1), floor_rough=0.15)
light("SPOT", (0, -1, 9), (0, 0, 0), 5200, (1.0, 0.85, 0.7), name="hero", spot=0.75)
aim(bpy.data.objects["hero"], (0, 4, 0))
light("AREA", (6, 8, 3), (0, 0, 0), 1200, (0.55, 0.45, 1.0), size=4, name="rimL")
aim(bpy.data.objects["rimL"], (0, 4, 1))
light("AREA", (-6, 8, 3), (0, 0, 0), 1200, (1.0, 0.5, 0.35), size=4, name="rimR")
aim(bpy.data.objects["rimR"], (0, 4, 1))

# turntable
bpy.ops.mesh.primitive_cylinder_add(radius=3.4, depth=0.3, vertices=128, location=(0, 4, 0.15))
stage = bpy.context.object
b = stage.modifiers.new("b", "BEVEL")
b.width = 0.06
b.segments = 5
bpy.ops.object.shade_smooth()
assign(stage, mat("stage", srgb("#151A26"), rough=0.2, metal=0.6, coat=1.0))
pivot = bpy.data.objects.new("pivot", None)
bpy.context.collection.objects.link(pivot)
pivot.location = (0, 4, 0.3)
key(pivot, 1, rotation_euler=(0, 0, 0.6))
key(pivot, FRAMES, rotation_euler=(0, 0, -1.4))
ease(pivot, "LINEAR")

m_dim = mat("dim", srgb("#2A3346"), rough=0.25, metal=0.7, coat=1.0)
num_mat = mat("num", WHITE, rough=0.3, emit=WHITE, emit_strength=0.4)
tokens = []
for i in range(10):
    a = -i / 10 * 2 * math.pi
    bpy.ops.mesh.primitive_cylinder_add(radius=0.62, depth=0.16, vertices=96)
    tk = bpy.context.object
    tk.name = f"tok{i}"
    bv = tk.modifiers.new("b", "BEVEL")
    bv.width = 0.05
    bv.segments = 5
    bpy.ops.object.shade_smooth()
    # each token gets its own material so it can light up
    m = mat(f"tokm{i}", srgb("#2A3346"), rough=0.18, metal=0.75, coat=1.0, emit=srgb("#E08A62"), emit_strength=0.0)
    assign(tk, m)
    tk.parent = pivot
    tk.location = (math.sin(a) * 2.5, -math.cos(a) * 2.5, 0.72)
    tk.rotation_euler = (math.pi / 2, 0, a)
    n = text(str(i + 1), size=0.62, extrude=0.03, bevel=0.004, name=f"n{i}")
    assign(n, num_mat)
    n.parent = tk
    n.location = (0, 0.0, 0.085)
    n.rotation_euler = (0, 0, 0)
    n.data.align_y = "CENTER"
    on = 30 + i * 6
    e = m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    e.default_value = 0.0
    e.keyframe_insert("default_value", frame=on)
    e.default_value = 3.0
    e.keyframe_insert("default_value", frame=on + 3)
    e.default_value = 1.2
    e.keyframe_insert("default_value", frame=on + 10)
    key(tk, on, location=tk.location.copy())
    up = tk.location.copy()
    up.z += 0.35
    key(tk, on + 4, location=up)
    key(tk, on + 12, location=(tk.location.x, tk.location.y, 0.72))
    tokens.append(tk)

m_white = mat("white", WHITE, rough=0.35, emit=WHITE, emit_strength=0.35)
m_peach = mat("peach", PEACH, rough=0.3, emit=PEACH, emit_strength=0.5)


def rise_in(o, f, loc, out=None):
    x, y, zz = loc
    key(o, 1, location=(x, y, zz - 0.4), scale=(0.001,) * 3)
    key(o, f, location=(x, y, zz - 0.4), scale=(0.001,) * 3)
    key(o, f + 9, location=(x, y, zz), scale=(1, 1, 1))
    for fc in fcurves(o.animation_data.action):
        for kp in fc.keyframe_points:
            if kp.co[0] == f + 9:
                kp.interpolation, kp.easing = "BACK", "EASE_OUT"
    if out:
        key(o, out, location=(x, y, zz), scale=(1, 1, 1))
        key(o, out + 7, location=(x, y, zz + 0.3), scale=(0.001,) * 3)


t1 = text("Only", size=0.7, extrude=0.05, bevel=0.006, font=FONT_SB, name="t1")
assign(t1, m_white)
rise_in(t1, 26, (0, 4.0, 6.3), out=128)
t2 = text("10 spots", size=1.35, extrude=0.1, bevel=0.012, name="t2")
assign(t2, m_peach)
rise_in(t2, 32, (0, 4.0, 4.85), out=128)
t3 = text("€100 website · 5 days", size=0.55, extrude=0.04, bevel=0.005, font=FONT_SB, name="t3")
assign(t3, m_white)
rise_in(t3, 134, (0, 4.0, 6.2))
pill = rounded_box("pill", (4.4, 0.3, 1.05), bevel=0.45, m=mat("pillm", srgb("#E07A4F"), rough=0.2, coat=1.0, emit=srgb("#E07A4F"), emit_strength=0.6))
ct = text("DM “WEBSITE”", size=0.62, extrude=0.04, bevel=0.005, name="ct")
assign(ct, m_white)
ct.parent = pill
ct.location = (0, -0.18, -0.22)
rise_in(pill, 142, (0, 4.0, 4.95))
lg = logo(height=0.8, depth=0.12, m=mat("logo", srgb("#F0C3AD"), rough=0.15, metal=0.8))
url = text("beribus.com", size=0.5, extrude=0.03, bevel=0.004, font=FONT_SB, align="LEFT", name="url")
assign(url, m_white)
grp = bpy.data.objects.new("brand", None)
bpy.context.collection.objects.link(grp)
lg.parent = grp
lg.location = (-1.45, 0, 0)
url.parent = grp
url.location = (-0.9, 0, 0.18)
rise_in(grp, 150, (0, 4.0, 3.95))

cam, tgt = camera((0, -4.0, 4.5), (0, 4.0, 1.0), lens=32)
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.4
focus = bpy.data.objects.new("focus", None)
bpy.context.collection.objects.link(focus)
cam.data.dof.focus_object = focus
key(focus, 1, location=(0, 1.5, 0.8))
key(focus, FRAMES, location=(0, 1.6, 1.5))
key(cam, 1, location=(0, -1.5, 1.6))
key(cam, 26, location=(0, -4.2, 3.6))
key(cam, 120, location=(0, -4.8, 4.4))
key(cam, FRAMES, location=(0, -5.2, 4.2))
key(tgt, 1, location=(0, 4.0, 1.2))
key(tgt, 26, location=(0, 4.0, 2.4))
key(tgt, FRAMES, location=(0, 4.0, 3.6))
ease(cam)
ease(tgt)
if os.path.exists(MEME):
    shatter(cam, MEME, f0=2, impact=(float(os.environ.get("IMPX", 0.5)), float(os.environ.get("IMPY", 0.45))), dist=0.6, power=1.1)

render_setup(sc, OUT, FRAMES, samples=int(os.environ.get("SAMPLES", 10)))
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
