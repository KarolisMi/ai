"""Ad 10 · The meme on a phone. We pull back into darkness: a burst of light and particles forms the Beribus mark."""
import math
import os
import random
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = os.path.join(HERE, "out", "ad10")
FRAMES = 186
SEQ = os.environ.get("SEQ", os.path.join(HERE, "..", "v3", "build", "seq10"))
NSEQ = len([f for f in os.listdir(SEQ) if f.endswith(".png")]) if os.path.isdir(SEQ) else 1
sc = reset()
studio(floor_color=srgb("#05070C"), wall_color=srgb("#080C16"), world=(0.0, 0.0, 0.003, 1), floor_rough=0.12)
light("AREA", (-4, -2, 6), (0, 0, 0), 900, (0.9, 0.85, 1.0), size=5, name="key")
aim(bpy.data.objects["key"], (0, 4, 3))
light("AREA", (4, 9, 4), (0, 0, 0), 1500, (0.4, 0.6, 1.0), size=3, name="rim")
aim(bpy.data.objects["rim"], (0, 4, 3))

scr_mat = seq_material("meme", os.path.join(SEQ, "s_0001.png"), NSEQ) if os.path.isdir(SEQ) else mat("blank", srgb("#222222"))
dev, hs = device("phone", scr_mat, hs=2.4)
dev.location = (0.0, 2.0, 3.0)
# the phone drifts away and down into the dark
key(dev, 1, location=(0.0, 2.0, 3.0), rotation_euler=(0, 0, 0))
key(dev, 24, location=(0.0, 2.0, 3.0), rotation_euler=(0, 0, 0))
key(dev, 60, location=(-3.5, 1.0, 0.6), rotation_euler=(0.5, 0.4, 0.8))
ease(dev)

BURST = 58
# light burst core
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, segments=32, ring_count=16)
core = bpy.context.object
assign(core, mat("core", WHITE, emit=srgb("#FFE2C8"), emit_strength=30))
core.location = (0, 6, 3.4)
key(core, 1, scale=(0.001,) * 3)
key(core, BURST - 4, scale=(0.001,) * 3)
key(core, BURST, scale=(1.4, 1.4, 1.4))
key(core, BURST + 10, scale=(0.001,) * 3)
ease(core)
# light rays
m_ray = mat("ray", WHITE, emit=srgb("#F0C3AD"), emit_strength=6)
rays = bpy.data.objects.new("rays", None)
bpy.context.collection.objects.link(rays)
rays.location = (0, 6.4, 3.4)
rnd = random.Random(5)
for i in range(18):
    r = rounded_box(f"ray{i}", (0.05, 0.02, rnd.uniform(4, 9)), bevel=0.01, m=m_ray)
    r.parent = rays
    a = i / 18 * 2 * math.pi
    r.rotation_euler = (0, a, 0)
    r.location = (math.sin(a) * 2.5, 0, math.cos(a) * 2.5)
key(rays, 1, scale=(0.001,) * 3, rotation_euler=(0, 0, 0))
key(rays, BURST, scale=(0.001,) * 3, rotation_euler=(0, 0, 0))
key(rays, BURST + 8, scale=(1, 1, 1), rotation_euler=(0, 0.3, 0))
key(rays, FRAMES, scale=(0.9, 0.9, 0.9), rotation_euler=(0, 1.2, 0))
ease(rays)
# particles: small glowing sparks exploding outward then slowing
m_sp = mat("spark", WHITE, emit=srgb("#FFD2A8"), emit_strength=12)
from mathutils import Vector
for i in range(90):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=rnd.uniform(0.015, 0.05), subdivisions=1)
    s = bpy.context.object
    assign(s, m_sp)
    d = Vector((rnd.gauss(0, 1), rnd.gauss(0, 0.6) - 0.6, rnd.gauss(0, 1))).normalized() * rnd.uniform(2.5, 6.5)
    o = Vector((0, 6, 3.4))
    key(s, 1, location=o, scale=(0.001,) * 3)
    key(s, BURST, location=o, scale=(0.001,) * 3)
    key(s, BURST + 1, location=o, scale=(1, 1, 1))
    key(s, BURST + 30, location=o + d, scale=(0.8, 0.8, 0.8))
    key(s, BURST + 90, location=o + d * 1.25 + Vector((0, 0, -0.6)), scale=(0.001,) * 3)
    ease(s, "BEZIER")

# the mark
m_logo = mat("logo", srgb("#F0C3AD"), rough=0.25, metal=0.3, coat=1.0, emit=srgb("#E08A62"), emit_strength=0.35)
lg = logo(height=2.6, depth=0.4, m=m_logo)
lp = bpy.data.objects.new("lp", None)
bpy.context.collection.objects.link(lp)
lg.parent = lp
lg.location = (0, 0, -1.3)
key(lp, 1, location=(0, 6, 3.4), rotation_euler=(0, 0, 3.2), scale=(0.001,) * 3)
key(lp, BURST, location=(0, 6, 3.4), rotation_euler=(0, 0, 3.2), scale=(0.001,) * 3)
key(lp, BURST + 22, location=(0, 6, 3.6), rotation_euler=(0, 0, -0.25), scale=(1, 1, 1))
key(lp, FRAMES, location=(0, 6, 3.6), rotation_euler=(0, 0, 0.25), scale=(1, 1, 1))
ease(lp)

m_white = mat("white", WHITE, rough=0.35, emit=WHITE, emit_strength=0.5)
m_peach = mat("peach", PEACH, rough=0.3, emit=PEACH, emit_strength=0.5)


def rise_in(o, f, loc):
    x, y, zz = loc
    key(o, 1, location=(x, y, zz - 0.3), scale=(0.001,) * 3)
    key(o, f, location=(x, y, zz - 0.3), scale=(0.001,) * 3)
    key(o, f + 9, location=(x, y, zz), scale=(1, 1, 1))
    for fc in fcurves(o.animation_data.action):
        for kp in fc.keyframe_points:
            if kp.co[0] == f + 9:
                kp.interpolation, kp.easing = "BACK", "EASE_OUT"


t1 = text("beribus.com", size=0.75, extrude=0.06, bevel=0.008, name="t1")
assign(t1, m_white)
rise_in(t1, 96, (0, 5.4, 1.45))
t2 = text("Websites for €100 · first 10 clients", size=0.42, extrude=0.02, bevel=0.003, font=FONT_SB, name="t2")
assign(t2, m_peach)
rise_in(t2, 106, (0, 5.4, 0.85))
pill = rounded_box("pill", (5.0, 0.3, 1.0), bevel=0.42, m=mat("pillm", srgb("#E07A4F"), rough=0.2, coat=1.0, emit=srgb("#E07A4F"), emit_strength=0.6))
ct = text("Comment “WEBSITE”", size=0.56, extrude=0.04, bevel=0.005, name="ct")
assign(ct, m_white)
ct.parent = pill
ct.location = (0, -0.18, -0.2)
rise_in(pill, 136, (0, 5.4, 6.1))

cam, tgt, d = pull_out_camera(dev, hs, lens=30, fill=0.995)
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.4
focus = bpy.data.objects.new("focus", None)
bpy.context.collection.objects.link(focus)
cam.data.dof.focus_object = focus
start = cam.location.copy()
key(focus, 1, location=dev.location)
key(focus, 24, location=dev.location)
key(focus, BURST, location=(0, 6, 3.4))
key(focus, FRAMES, location=(0, 5.6, 3.2))
key(cam, 1, location=start)
key(cam, 6, location=start)
key(cam, BURST, location=(0.0, -4.2, 3.4))
key(cam, FRAMES, location=(0.0, -5.2, 3.5))
key(tgt, 1, location=(dev.location.x, dev.location.y + 5, dev.location.z))
key(tgt, BURST, location=(0.0, 6.0, 3.4))
key(tgt, FRAMES, location=(0.0, 5.6, 3.5))
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
