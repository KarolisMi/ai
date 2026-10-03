"""Ad 8 · The meme on a phone. We pull back; a second phone with a real website slides in and the first one topples."""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = os.path.join(HERE, "out", "ad8")
FRAMES = 186
SEQ = os.environ.get("SEQ", os.path.join(HERE, "..", "v3", "build", "seq08"))
NSEQ = len([f for f in os.listdir(SEQ) if f.endswith(".png")]) if os.path.isdir(SEQ) else 1
sc = reset()
# soft peach daylight studio
studio(floor_color=srgb("#F2DCCB"), wall_color=srgb("#F8EADF"), world=(0.7, 0.62, 0.56, 1), floor_rough=0.4)
light("AREA", (-6, -3, 7), (0, 0, 0), 1800, (1.0, 0.92, 0.84), size=7, name="key")
aim(bpy.data.objects["key"], (0, 4, 1.5))
light("AREA", (6, 2, 4), (0, 0, 0), 700, (0.85, 0.9, 1.0), size=5, name="fill")
aim(bpy.data.objects["fill"], (0, 4, 1.5))

scr_mat = seq_material("meme", os.path.join(SEQ, "s_0001.png"), NSEQ) if os.path.isdir(SEQ) else mat("blank", srgb("#222222"))
old, hs = device("phone", scr_mat, hs=2.6, body_color="#8B8F96")
old.location = (0.0, 4.0, 1.42)
# the old phone darkens and falls backwards
dim = scr_mat.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
dim.keyframe_insert("default_value", frame=70)
dim.default_value = 0.15
dim.keyframe_insert("default_value", frame=86)
FALL = 82
pivot = bpy.data.objects.new("oldpivot", None)
bpy.context.collection.objects.link(pivot)
pivot.location = (0.0, 4.1, 0.0)
bpy.context.view_layer.update()
mw = old.matrix_world.copy()
old.parent = pivot
old.matrix_parent_inverse = pivot.matrix_world.inverted()
key(pivot, 1, location=(0.0, 4.1, 0.0), rotation_euler=(0, 0, 0))
key(pivot, 60, location=(0.0, 4.1, 0.0), rotation_euler=(0, 0, 0))
key(pivot, 70, location=(-1.6, 4.1, 0.0), rotation_euler=(0, 0, 0))
key(pivot, FALL, location=(-1.6, 4.1, 0.0), rotation_euler=(-0.08, 0, 0))
key(pivot, FALL + 12, location=(-1.6, 4.4, 0.0), rotation_euler=(-1.48, 0, 0))
key(pivot, FALL + 16, location=(-1.6, 4.4, 0.0), rotation_euler=(-1.40, 0, 0))
key(pivot, FALL + 20, location=(-1.6, 4.4, 0.0), rotation_euler=(-1.48, 0, 0))
ease(pivot)
for fc in fcurves(pivot.animation_data.action):
    for kp in fc.keyframe_points:
        if kp.co[0] == FALL + 12:
            kp.interpolation, kp.easing = "QUAD", "EASE_IN"

new, scr_emit = phone(name="new", h=2.75, screen_img=os.path.join(HERE, "site.png"), body_color="#16304F")
key(new, 1, location=(6.0, 4.0, 1.42), rotation_euler=(0, 0, -0.5))
key(new, 62, location=(6.0, 4.0, 1.42), rotation_euler=(0, 0, -0.5))
key(new, 78, location=(1.1, 3.8, 1.42), rotation_euler=(0, 0, 0.12))
key(new, 90, location=(0.9, 3.8, 1.42), rotation_euler=(0, 0, 0.0))
ease(new)

m_ink = mat("ink", srgb("#16304F"), rough=0.4)
m_warm = mat("warm", srgb("#B4532A"), rough=0.3, coat=0.4)
m_grey = mat("grey", srgb("#8E8A86"), rough=0.5)
m_white = mat("white", WHITE, rough=0.35, emit=WHITE, emit_strength=0.3)


def rise_in(o, f, loc, out=None):
    x, y, zz = loc
    key(o, 1, location=(x, y, zz - 0.3), scale=(0.001,) * 3)
    key(o, f, location=(x, y, zz - 0.3), scale=(0.001,) * 3)
    key(o, f + 9, location=(x, y, zz), scale=(1, 1, 1))
    for fc in fcurves(o.animation_data.action):
        for kp in fc.keyframe_points:
            if kp.co[0] == f + 9:
                kp.interpolation, kp.easing = "BACK", "EASE_OUT"
    if out:
        key(o, out, location=(x, y, zz), scale=(1, 1, 1))
        key(o, out + 7, location=(x, y, zz + 0.3), scale=(0.001,) * 3)


a = text("A Facebook page", size=0.5, extrude=0.03, bevel=0.004, font=FONT_SB, name="a")
assign(a, m_grey)
rise_in(a, 96, (0.5, 3.4, 4.6), out=146)
strike = rounded_box("strike", (3.9, 0.05, 0.07), bevel=0.02, m=m_warm)
key(strike, 1, location=(0.5, 3.3, 4.78), scale=(0.001, 1, 1))
key(strike, 104, location=(0.5, 3.3, 4.78), scale=(0.001, 1, 1))
key(strike, 110, location=(0.5, 3.3, 4.78), scale=(1, 1, 1))
key(strike, 146, location=(0.5, 3.3, 4.78), scale=(1, 1, 1))
key(strike, 150, location=(0.5, 3.3, 4.78), scale=(0.001, 1, 1))
b = text("A real website.", size=0.78, extrude=0.05, bevel=0.006, name="b")
assign(b, m_ink)
rise_in(b, 112, (0.5, 3.4, 3.65), out=146)
c = text("€100 · first 10 clients", size=0.5, extrude=0.03, bevel=0.004, font=FONT_SB, name="c")
assign(c, m_warm)
rise_in(c, 152, (0.5, 3.4, 4.65))
pill = rounded_box("pill", (5.0, 0.3, 1.0), bevel=0.42, m=mat("pillm", srgb("#16304F"), rough=0.2, coat=1.0, emit=srgb("#16304F"), emit_strength=0.2))
ct = text("Comment “WEBSITE”", size=0.6, extrude=0.04, bevel=0.005, name="ct")
assign(ct, m_white)
ct.parent = pill
ct.location = (0, -0.18, -0.21)
rise_in(pill, 160, (0.5, 3.4, 3.7))

cam, tgt, d = pull_out_camera(old, hs, lens=30, fill=0.995)
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 3.0
focus = bpy.data.objects.new("focus", None)
bpy.context.collection.objects.link(focus)
cam.data.dof.focus_object = focus
start = cam.location.copy()
key(focus, 1, location=old.location)
key(focus, 76, location=(1.0, 3.8, 1.5))
key(focus, FRAMES, location=(0.6, 3.5, 3.4))
key(cam, 1, location=start)
key(cam, 8, location=start)
key(cam, 58, location=(0.2, -3.0, 2.0))
key(cam, 100, location=(0.6, -5.0, 2.9))
key(cam, FRAMES, location=(0.6, -5.6, 3.1))
key(tgt, 1, location=(old.location.x, old.location.y + 5, old.location.z))
key(tgt, 8, location=(old.location.x, old.location.y + 5, old.location.z))
key(tgt, 58, location=(0.2, 4.0, 1.5))
key(tgt, 100, location=(0.6, 3.6, 2.7))
key(tgt, FRAMES, location=(0.6, 3.5, 3.1))
ease(cam)
ease(tgt)

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
