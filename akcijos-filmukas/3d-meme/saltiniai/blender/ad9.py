"""Ad 9 · The meme on a tall display. We pull back; four 3D question marks flip into green checks."""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = os.path.join(HERE, "out", "ad9")
FRAMES = 186
SEQ = os.environ.get("SEQ", os.path.join(HERE, "..", "v3", "build", "seq09"))
NSEQ = len([f for f in os.listdir(SEQ) if f.endswith(".png")]) if os.path.isdir(SEQ) else 1
sc = reset()
# teal-navy gallery
studio(floor_color=srgb("#0B1F24"), wall_color=srgb("#0F2E35"), world=(0.004, 0.012, 0.014, 1), floor_rough=0.2)
light("AREA", (-5, -3, 7), (0, 0, 0), 1700, (1.0, 0.9, 0.8), size=5, name="key")
aim(bpy.data.objects["key"], (0, 4, 2.5))
light("AREA", (5, 9, 5), (0, 0, 0), 1600, (0.35, 0.9, 0.85), size=4, name="rim")
aim(bpy.data.objects["rim"], (0, 4, 2.5))

scr_mat = seq_material("meme", os.path.join(SEQ, "s_0001.png"), NSEQ) if os.path.isdir(SEQ) else mat("blank", srgb("#222222"))
dev, hs = device("totem", scr_mat, hs=3.4, body_color="#1B2A30")
dev.location = (0.0, 7.5, 2.45)
key(dev, 1, location=(0.0, 7.5, 2.45))
key(dev, 20, location=(0.0, 7.5, 2.45))
key(dev, 50, location=(0.0, 9.5, -4.5))
ease(dev)

m_q = mat("q", srgb("#F0C3AD"), rough=0.2, coat=1.0, emit=srgb("#F0C3AD"), emit_strength=0.2)
m_ok = mat("ok", srgb("#2F9E62"), rough=0.15, coat=1.0, emit=srgb("#3CCB80"), emit_strength=0.5)
m_white = mat("white", WHITE, rough=0.35, emit=WHITE, emit_strength=0.4)
labels = ["Design", "Texts", "Mobile", "No monthly fee"]
pos = [(-1.3, 3.0, 4.2), (1.3, 3.0, 4.2), (-1.3, 3.0, 2.0), (1.3, 3.0, 2.0)]
for i, (lab, p) in enumerate(zip(labels, pos)):
    piv = bpy.data.objects.new(f"piv{i}", None)
    bpy.context.collection.objects.link(piv)
    q = text("?", size=1.4, extrude=0.18, bevel=0.03, name=f"q{i}")
    assign(q, m_q)
    q.parent = piv
    q.location = (0, -0.12, -0.45)
    q.rotation_euler = (math.pi / 2, 0, 0)
    # check mark built from two rounded bars, on the back side
    chk = bpy.data.objects.new(f"chk{i}", None)
    bpy.context.collection.objects.link(chk)
    chk.parent = piv
    chk.rotation_euler = (0, 0, math.pi)
    chk.location = (0, 0.22, 0)
    chk.scale = (0.8, 0.8, 0.8)
    for j, (sx, sz, ang, ox, oz) in enumerate(((0.52, 0.2, 0.817, -0.30, -0.16), (1.02, 0.2, -0.824, 0.165, 0.02))):
        bar = rounded_box(f"bar{i}{j}", (sx, 0.22, sz), bevel=0.09, m=m_ok)
        bar.parent = chk
        bar.location = (ox, 0, oz)
        bar.rotation_euler = (0, ang, 0)
    lb = text(lab, size=0.36, extrude=0.03, bevel=0.004, font=FONT_SB, name=f"lb{i}")
    assign(lb, m_white)
    F = 70 + i * 10
    key(piv, 1, location=(p[0], p[1], p[2] + 0.4), rotation_euler=(0, 0, 0), scale=(0.001,) * 3)
    key(piv, 24 + i * 4, location=(p[0], p[1], p[2] + 0.4), rotation_euler=(0, 0, 0), scale=(0.001,) * 3)
    key(piv, 34 + i * 4, location=p, rotation_euler=(0, 0, 0.3), scale=(1, 1, 1))
    key(piv, F, location=p, rotation_euler=(0, 0, -0.15), scale=(1, 1, 1))
    key(piv, F + 10, location=p, rotation_euler=(0, 0, math.pi), scale=(1, 1, 1))
    ease(piv)
    for fc in fcurves(piv.animation_data.action):
        for kp in fc.keyframe_points:
            if kp.co[0] == F + 10:
                kp.interpolation, kp.easing = "BACK", "EASE_OUT"
    # swap faces at the middle of the flip so the ? and the check never show together
    key(q, 1, scale=(1, 1, 1)); key(q, F + 4, scale=(1, 1, 1)); key(q, F + 5, scale=(0.001,) * 3)
    key(chk, 1, scale=(0.001,) * 3); key(chk, F + 4, scale=(0.001,) * 3); key(chk, F + 5, scale=(0.8, 0.8, 0.8))
    for o in (q, chk):
        for fc in fcurves(o.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"
    key(lb, 1, location=(p[0], p[1], p[2] - 1.15), scale=(0.001,) * 3)
    key(lb, F + 6, location=(p[0], p[1], p[2] - 1.15), scale=(0.001,) * 3)
    key(lb, F + 14, location=(p[0], p[1], p[2] - 0.95), scale=(1, 1, 1))
    ease(lb)


def rise_in(o, f, loc):
    x, y, zz = loc
    key(o, 1, location=(x, y, zz - 0.3), scale=(0.001,) * 3)
    key(o, f, location=(x, y, zz - 0.3), scale=(0.001,) * 3)
    key(o, f + 9, location=(x, y, zz), scale=(1, 1, 1))
    for fc in fcurves(o.animation_data.action):
        for kp in fc.keyframe_points:
            if kp.co[0] == f + 9:
                kp.interpolation, kp.easing = "BACK", "EASE_OUT"


h1 = text("What do you get for €100?", size=0.44, extrude=0.03, bevel=0.004, font=FONT_SB, name="h1")
assign(h1, m_white)
rise_in(h1, 30, (0, 3.0, 5.85))
key(h1, 136, location=(0, 3.0, 5.85), scale=(1, 1, 1))
key(h1, 143, location=(0, 3.0, 6.2), scale=(0.001,) * 3)
h2 = text("Everything.", size=0.8, extrude=0.06, bevel=0.008, name="h2")
assign(h2, m_q)
rise_in(h2, 118, (0, 3.0, 0.35))
pill = rounded_box("pill", (4.3, 0.3, 0.95), bevel=0.4, m=mat("pillm", srgb("#E07A4F"), rough=0.2, coat=1.0, emit=srgb("#E07A4F"), emit_strength=0.6))
ct = text("DM “WEBSITE”", size=0.56, extrude=0.04, bevel=0.005, name="ct")
assign(ct, m_white)
ct.parent = pill
ct.location = (0, -0.18, -0.2)
rise_in(pill, 146, (0, 2.9, 6.9))
url = text("beribus.com · first 10 clients", size=0.32, extrude=0.02, bevel=0.003, font=FONT_SB, name="url")
assign(url, m_white)
rise_in(url, 154, (0, 2.9, 6.05))

cam, tgt, d = pull_out_camera(dev, hs, lens=30, fill=0.995)
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.8
focus = bpy.data.objects.new("focus", None)
bpy.context.collection.objects.link(focus)
cam.data.dof.focus_object = focus
start = cam.location.copy()
key(focus, 1, location=dev.location)
key(focus, 40, location=(0, 3.0, 3.2))
key(focus, FRAMES, location=(0, 3.0, 3.6))
key(cam, 1, location=start)
key(cam, 6, location=start)
key(cam, 44, location=(0.0, -4.4, 3.3))
key(cam, 120, location=(0.4, -5.6, 3.4))
key(cam, FRAMES, location=(0.0, -6.4, 3.6))
key(tgt, 1, location=(dev.location.x, dev.location.y + 5, dev.location.z))
key(tgt, 6, location=(dev.location.x, dev.location.y + 5, dev.location.z))
key(tgt, 44, location=(0.0, 3.0, 3.3))
key(tgt, FRAMES, location=(0.0, 3.0, 3.6))
ease(cam)
ease(tgt)

render_setup(sc, OUT, FRAMES, samples=int(os.environ.get("SAMPLES", 10)))
if os.environ.get("END"):
    sc.frame_end = int(os.environ["END"])
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
