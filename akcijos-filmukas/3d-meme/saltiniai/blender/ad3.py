"""Ad 3 · The meme shatters onto ice. A puck slides into a phone; its screen lights up with the site."""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = os.path.join(HERE, "out", "ad3")
FRAMES = 192
MEME = os.environ.get("MEME_FRAME", os.path.join(HERE, "..", "v3", "build", "m03_last.png"))
sc = reset()
studio(floor_color=srgb("#CFE3F2"), wall_color=srgb("#0D1E33"), world=(0.01, 0.02, 0.04, 1), floor_rough=0.06)
light("AREA", (-5, -2, 7), (0, 0, 0), 1500, (0.75, 0.88, 1.0), size=6, name="key")
aim(bpy.data.objects["key"], (0, 4, 1.5))
light("AREA", (5, 9, 4), (0, 0, 0), 2600, (0.45, 0.75, 1.0), size=3, name="rim")
aim(bpy.data.objects["rim"], (0, 4, 1.5))
light("AREA", (-4, 8, 3), (0, 0, 0), 1400, (1.0, 0.6, 0.4), size=2, name="warmrim")
aim(bpy.data.objects["warmrim"], (0, 4, 1.5))

ph, scr_emit = phone(screen_img=os.path.join(HERE, "site.png"))
ph.location = (0, 4.0, 1.62)
ph.rotation_euler = (0, 0, 0)
# screen wakes when the puck hits
HIT = 34
scr_emit.default_value = 0.0
scr_emit.node.inputs["Emission Strength"].keyframe_insert("default_value", frame=HIT)
scr_emit.default_value = 1.3
scr_emit.node.inputs["Emission Strength"].keyframe_insert("default_value", frame=HIT + 6)
scr_emit.default_value = 1.0
scr_emit.node.inputs["Emission Strength"].keyframe_insert("default_value", frame=HIT + 14)
# the screen is black glass until then
base = scr_emit.node.inputs["Base Color"]
# wobble on impact
key(ph, 1, rotation_euler=(0, 0, 0))
key(ph, HIT, rotation_euler=(0, 0, 0))
key(ph, HIT + 4, rotation_euler=(-0.09, 0, 0.02))
key(ph, HIT + 9, rotation_euler=(0.05, 0, -0.01))
key(ph, HIT + 14, rotation_euler=(-0.02, 0, 0))
key(ph, HIT + 20, rotation_euler=(0, 0, 0))
ease(ph)

# puck
bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.25, vertices=64)
puck = bpy.context.object
puck.name = "puck"
bev = puck.modifiers.new("b", "BEVEL")
bev.width = 0.04
bev.segments = 4
bpy.ops.object.shade_smooth()
assign(puck, mat("puck", srgb("#0B0C0F"), rough=0.35, coat=0.4))
# the puck is what broke the screen: it bursts out right in front of the lens,
# drops onto the ice and slides into the phone
key(puck, 1, location=(-0.98, -4.05, 0.42), rotation_euler=(1.2, 0.3, 0))
key(puck, 6, location=(-0.85, -2.6, 0.5), rotation_euler=(0.6, 0.15, 2))
key(puck, 11, location=(-0.6, -1.0, 0.125), rotation_euler=(0, 0, 4))
key(puck, HIT, location=(0.0, 3.55, 0.125), rotation_euler=(0, 0, 9))
key(puck, HIT + 18, location=(0.25, 2.6, 0.125), rotation_euler=(0, 0, 11))
ease(puck, "LINEAR")
for fc in fcurves(puck.animation_data.action):
    for kp in fc.keyframe_points:
        if kp.co[0] == 11 and fc.data_path == "location" and fc.array_index == 2:
            kp.interpolation, kp.easing = "QUAD", "EASE_IN"
for fc in fcurves(puck.animation_data.action):
    for kp in fc.keyframe_points:
        if kp.co[0] == HIT + 18:
            kp.interpolation, kp.easing = "QUAD", "EASE_OUT"

# ice spray particles at impact
m_snow = mat("snow", srgb("#F3FAFF"), rough=0.6, emit=srgb("#E8F4FF"), emit_strength=0.4)
import random
rnd = random.Random(2)
for i in range(46):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=rnd.uniform(0.015, 0.045), subdivisions=1)
    s = bpy.context.object
    assign(s, m_snow)
    a = rnd.uniform(-2.6, -0.5)
    sp = rnd.uniform(0.8, 2.2)
    start = (rnd.uniform(-0.3, 0.3), 3.5, 0.1)
    key(s, 1, location=start, scale=(0.001,) * 3)
    key(s, HIT, location=start, scale=(0.001,) * 3)
    for k in range(1, 6):
        tt = k * 3 / 24
        key(s, HIT + k * 3, location=(start[0] + math.cos(a) * sp * tt * 3, start[1] + math.sin(a) * sp * tt * 2, max(0.02, 0.1 + 3.2 * tt - 9 * tt * tt)), scale=(1,) * 3 if k < 5 else (0.001,) * 3)
    ease(s, "LINEAR")

m_white = mat("white", WHITE, rough=0.35, emit=WHITE, emit_strength=0.35)
m_ice = mat("icetxt", srgb("#9FD3FF"), rough=0.3, emit=srgb("#9FD3FF"), emit_strength=0.5)


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


t1 = text("YOUR SITE, LIVE IN", size=0.36, extrude=0.03, bevel=0.004, font=FONT_SB, spacing=1.2, name="t1")
assign(t1, m_ice)
rise_in(t1, 92, (0, 3.6, 5.55), out=140)
t2 = text("5 days", size=1.3, extrude=0.1, bevel=0.012, name="t2")
assign(t2, m_white)
rise_in(t2, 98, (0, 3.6, 4.15), out=140)
t3 = text("€100 · first 10 clients", size=0.46, extrude=0.03, bevel=0.004, font=FONT_SB, name="t3")
assign(t3, m_ice)
rise_in(t3, 146, (0, 3.6, 5.5))
pill = rounded_box("pill", (4.4, 0.3, 1.05), bevel=0.45, m=mat("pillm", srgb("#E07A4F"), rough=0.2, coat=1.0, emit=srgb("#E07A4F"), emit_strength=0.5))
ct = text("DM “WEBSITE”", size=0.62, extrude=0.04, bevel=0.005, name="ct")
assign(ct, m_white)
ct.parent = pill
ct.location = (0, -0.18, -0.22)
rise_in(pill, 154, (0, 3.6, 4.35))
url = text("beribus.com", size=0.42, extrude=0.03, bevel=0.004, font=FONT_SB, name="url")
assign(url, m_white)
rise_in(url, 162, (0, 3.6, 3.6))

# camera: low ice-level chase, then orbit up to the phone
cam, tgt = camera((-1.2, -6.0, 0.5), (0.0, 4.0, 0.6), lens=28)
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.2
focus = bpy.data.objects.new("focus", None)
bpy.context.collection.objects.link(focus)
cam.data.dof.focus_object = focus
key(focus, 1, location=(-1.2, -2.0, 0.2))
key(focus, HIT, location=(0, 3.6, 0.6))
key(focus, FRAMES, location=(0, 3.8, 2.5))
key(cam, 1, location=(-1.0, -4.7, 0.42))
key(cam, HIT, location=(-0.6, -1.2, 0.45))
key(cam, 64, location=(2.8, -1.8, 1.6))
key(cam, 100, location=(0.5, -2.2, 2.9))
key(cam, FRAMES, location=(0.0, -2.6, 3.4))
key(tgt, 1, location=(-1.0, 2.0, 0.3))
key(tgt, HIT, location=(0.0, 3.6, 0.8))
key(tgt, 64, location=(0.0, 4.0, 1.7))
key(tgt, FRAMES, location=(0.0, 3.8, 3.4))
ease(cam)
ease(tgt)
if os.path.exists(MEME):
    shatter(cam, MEME, f0=2, impact=(float(os.environ.get("IMPX", 0.5)), float(os.environ.get("IMPY", 0.5))), dist=0.6, power=1.0)

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
