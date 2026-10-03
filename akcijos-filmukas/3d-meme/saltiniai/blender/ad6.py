"""Ad 6 · The meme keeps playing on a phone; we pull back to a desk. Keycaps pop off the keyboard and spell WEBSITE."""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = os.path.join(HERE, "out", "ad6")
FRAMES = 186
SEQ = os.environ.get("SEQ", os.path.join(HERE, "..", "v3", "build", "seq06"))
NSEQ = len([f for f in os.listdir(SEQ) if f.endswith(".png")]) if os.path.isdir(SEQ) else 1
sc = reset()
# warm evening desk: wood top, dark wall
studio(floor_color=srgb("#2A1C14"), wall_color=srgb("#171A22"), world=(0.01, 0.01, 0.015, 1), floor_rough=0.35)
cyc = bpy.data.objects["cyc"]
# wood grain via noise on the floor material
nt = cyc.active_material.node_tree
noise = nt.nodes.new("ShaderNodeTexWave")
noise.inputs["Scale"].default_value = 0.6
noise.inputs["Distortion"].default_value = 6
mixc = nt.nodes.new("ShaderNodeMix")
mixc.data_type = "RGBA"
mixc.inputs["Factor"].default_value = 0.35
nt.links.new(nt.nodes["Color Ramp"].outputs["Color"], mixc.inputs["A"])
mixc.inputs["B"].default_value = srgb("#4A3122")
nt.links.new(noise.outputs["Fac"], mixc.inputs["Factor"])
nt.links.new(mixc.outputs["Result"], nt.nodes["Principled BSDF"].inputs["Base Color"])

light("AREA", (-4, -2, 6), (0, 0, 0), 1500, (1.0, 0.78, 0.55), size=4, name="lamp")
aim(bpy.data.objects["lamp"], (0, 3, 0.5))
light("AREA", (5, 7, 3), (0, 0, 0), 1100, (0.5, 0.65, 1.0), size=3, name="rim")
aim(bpy.data.objects["rim"], (0, 3, 1))
light("POINT", (2.5, 1.5, 0.6), (0, 0, 0), 120, (1.0, 0.5, 0.3), name="glow")

scr_mat = seq_material("meme", os.path.join(SEQ, "s_0001.png"), NSEQ) if os.path.isdir(SEQ) else mat("blank", srgb("#222222"))
dev, hs = device("phone", scr_mat, hs=2.4)
dev.location = (2.0, 4.6, 1.38)
dev.rotation_euler = (0.0, 0, 0)

# keyboard
kb = rounded_box("kb", (6.2, 2.2, 0.28), bevel=0.12, m=mat("kbm", srgb("#1D2129"), rough=0.3, metal=0.6, coat=0.3))
kb.location = (-0.6, 2.2, 0.14)
kb.rotation_euler = (0, 0, 0.05)
m_key = mat("key", srgb("#2B303A"), rough=0.35, coat=0.3)
m_keyw = mat("keyw", srgb("#E07A4F"), rough=0.2, coat=1.0, emit=srgb("#E07A4F"), emit_strength=0.25)
m_leg = mat("leg", WHITE, rough=0.4, emit=WHITE, emit_strength=0.6)
rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
caps = {}
for r, row in enumerate(rows):
    for c, ch in enumerate(row):
        k = rounded_box(f"k_{ch}", (0.5, 0.5, 0.22), bevel=0.07, m=m_key)
        k.parent = kb
        k.location = (-2.6 + c * 0.58 + r * 0.22, 0.6 - r * 0.58, 0.24)
        lg = text(ch, size=0.24, extrude=0.005, bevel=0.0, font=FONT_SB, name=f"l_{ch}")
        assign(lg, m_leg)
        lg.parent = k
        lg.location = (0, 0, 0.112)
        lg.rotation_euler = (0, 0, 0)
        lg.data.align_y = "CENTER"
        caps[ch] = k

word = "WEBSITE"
used = {}
from mathutils import Vector
fly = []
for i, ch in enumerate(word):
    if ch in used:
        # second E: duplicate the key so both can fly
        src = caps[ch]
        k = src.copy()
        k.data = src.data
        bpy.context.collection.objects.link(k)
        for chd in src.children:
            c2 = chd.copy()
            bpy.context.collection.objects.link(c2)
            c2.parent = k
        k.location = src.location.copy()
    else:
        k = caps[ch]
    used[ch] = True
    fly.append(k)
F0 = 70
for i, k in enumerate(fly):
    bpy.context.view_layer.update()
    w = k.matrix_world.translation.copy()
    k.parent = None
    k.location = w
    k.rotation_euler = (0, 0, 0.05)
    assign(k, m_keyw)
    s0 = F0 + i * 4
    target = Vector((-2.2 + i * 0.7, 3.4, 3.5))
    key(k, 1, location=w, rotation_euler=(0, 0, 0.05), scale=(1, 1, 1))
    key(k, s0, location=w, rotation_euler=(0, 0, 0.05), scale=(1, 1, 1))
    key(k, s0 + 6, location=w + Vector((0, 0, 1.2)), rotation_euler=(1.0, 0.4, 0.3), scale=(1.2, 1.2, 1.2))
    key(k, s0 + 16, location=target, rotation_euler=(math.pi / 2, 0, 0), scale=(1.2, 1.2, 1.2))
    ease(k)
    for fc in fcurves(k.animation_data.action):
        for kp in fc.keyframe_points:
            if kp.co[0] == s0 + 16:
                kp.interpolation, kp.easing = "BACK", "EASE_OUT"

m_white = mat("white", WHITE, rough=0.35, emit=WHITE, emit_strength=0.4)
m_peach = mat("peach", PEACH, rough=0.3, emit=PEACH, emit_strength=0.4)


def rise_in(o, f, loc, out=None):
    x, y, zz = loc
    key(o, 1, location=(x, y, zz - 0.3), scale=(0.001,) * 3)
    key(o, f, location=(x, y, zz - 0.3), scale=(0.001,) * 3)
    key(o, f + 9, location=(x, y, zz), scale=(1, 1, 1))
    for fc in fcurves(o.animation_data.action):
        for kp in fc.keyframe_points:
            if kp.co[0] == f + 9:
                kp.interpolation, kp.easing = "BACK", "EASE_OUT"


t1 = text("DM us", size=0.6, extrude=0.04, bevel=0.005, font=FONT_SB, name="t1")
assign(t1, m_white)
rise_in(t1, 104, (-0.1, 3.4, 4.45))
t2 = text("€100 website · first 10 clients", size=0.34, extrude=0.02, bevel=0.003, font=FONT_SB, name="t2")
assign(t2, m_peach)
rise_in(t2, 118, (-0.1, 3.4, 2.75))
t3 = text("beribus.com", size=0.4, extrude=0.03, bevel=0.004, font=FONT_SB, name="t3")
assign(t3, m_white)
rise_in(t3, 128, (-0.1, 3.4, 2.15))

cam, tgt, d = pull_out_camera(dev, hs, lens=30, fill=0.995)
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.8
focus = bpy.data.objects.new("focus", None)
bpy.context.collection.objects.link(focus)
cam.data.dof.focus_object = focus
start = cam.location.copy()
key(focus, 1, location=dev.location)
key(focus, 60, location=dev.location)
key(focus, 90, location=(-0.1, 3.4, 3.0))
key(focus, FRAMES, location=(-0.1, 3.4, 3.2))
key(cam, 1, location=start)
key(cam, 6, location=start)
key(cam, 40, location=(1.6, 0.4, 2.0))
key(cam, 70, location=(0.6, -2.4, 3.0))
key(cam, 110, location=(-0.1, -5.6, 3.3))
key(cam, FRAMES, location=(-0.1, -6.0, 3.4))
key(tgt, 1, location=(dev.location.x, dev.location.y + 5, dev.location.z))
key(tgt, 6, location=(dev.location.x, dev.location.y + 5, dev.location.z))
key(tgt, 40, location=(1.2, 4.0, 1.2))
key(tgt, 70, location=(0.0, 3.0, 1.6))
key(tgt, FRAMES, location=(-0.1, 3.4, 3.2))
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
