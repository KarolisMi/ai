"""Ad 5 · The meme shatters. A domino run of steps (Design, Texts, Mobile, SEO) topples into a big LIVE button."""
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = os.path.join(HERE, "out", "ad5")
FRAMES = 186
MEME = os.environ.get("MEME_FRAME", os.path.join(HERE, "..", "v3", "build", "m05_last.png"))
sc = reset()
# clean light-grey/blue studio
studio(floor_color=srgb("#DDE3EC"), wall_color=srgb("#EEF2F7"), world=(0.5, 0.53, 0.58, 1), floor_rough=0.25)
light("AREA", (-6, -2, 8), (0, 0, 0), 2000, (1.0, 0.95, 0.9), size=6, name="key")
aim(bpy.data.objects["key"], (0, 4, 1))
light("AREA", (6, 6, 5), (0, 0, 0), 1000, (0.8, 0.88, 1.0), size=5, name="fill")
aim(bpy.data.objects["fill"], (0, 4, 1))

bpy.ops.rigidbody.world_add()
rbw = sc.rigidbody_world
rbw.point_cache.frame_start, rbw.point_cache.frame_end = 1, FRAMES
rbw.substeps_per_frame = 30
rbw.solver_iterations = 30
cyc = bpy.data.objects["cyc"]
bpy.context.view_layer.objects.active = cyc
bpy.ops.rigidbody.object_add(type="PASSIVE")
cyc.rigid_body.collision_shape = "MESH"

labels = ["DESIGN", "TEXTS", "MOBILE", "SEO", "", "", "", ""]
cols = ["#16304F", "#2C5079", "#16304F", "#2C5079", "#16304F", "#2C5079", "#16304F", "#2C5079"]
m_white = mat("white", WHITE, rough=0.35, emit=WHITE, emit_strength=0.3)
tiles = []
# a gentle S-curve of dominoes leading to the button
pts = []
for i in range(14):
    t = i / 13
    pts.append((math.sin(t * math.pi * 1.2) * 1.6 - 0.6, -0.5 + t * 7.2))
for i, (x, y) in enumerate(pts):
    if i + 1 < len(pts):
        nx, ny = pts[i + 1]
    else:
        nx, ny = x, y + 1
    ang = math.atan2(nx - x, ny - y)
    tl = rounded_box(f"dom{i}", (1.1, 0.2, 2.0), bevel=0.04, m=mat(f"dm{i}", srgb(cols[i % 8]), rough=0.2, coat=1.0))
    tl.location = (x, y, 1.0)
    tl.rotation_euler = (0, 0, -ang)
    if i < 4:
        lb = text(labels[i], size=0.22, extrude=0.01, bevel=0.002, font=FONT_SB, spacing=1.1, name=f"dl{i}")
        assign(lb, m_white)
        lb.parent = tl
        lb.location = (0, -0.105, 0.2)
        lb.rotation_euler = (math.pi / 2, 0, 0)
        lb.data.align_y = "CENTER"
    bpy.context.view_layer.objects.active = tl
    bpy.ops.rigidbody.object_add(type="ACTIVE")
    tl.rigid_body.collision_shape = "BOX"
    tl.rigid_body.mass = 0.4
    tl.rigid_body.friction = 0.5
    tl.rigid_body.use_deactivation = True
    tl.rigid_body.use_start_deactivated = True
    tiles.append(tl)

# pusher nudges the first tile
pusher = rounded_box("pusher", (0.5, 0.5, 0.5), bevel=0.1, m=mat("push", srgb("#E07A4F"), rough=0.15, coat=1.0))
px, py = pts[0]
bpy.context.view_layer.objects.active = pusher
bpy.ops.rigidbody.object_add(type="ACTIVE")
pusher.rigid_body.mass = 2
pusher.rigid_body.kinematic = True
key(pusher, 1, location=(px, py - 3.0, 1.8))
key(pusher, 14, location=(px, py - 3.0, 1.8))
key(pusher, 24, location=(px, py - 0.25, 1.8))
ease(pusher, "LINEAR")
pusher.rigid_body.keyframe_insert("kinematic", frame=24)
pusher.rigid_body.kinematic = False
pusher.rigid_body.keyframe_insert("kinematic", frame=25)

# the LIVE button at the end of the run
bx, by = pts[-1][0], pts[-1][1] + 1.5
bpy.ops.mesh.primitive_cylinder_add(radius=1.25, depth=0.4, vertices=96, location=(bx, by, 0.2))
basep = bpy.context.object
bpy.ops.object.shade_smooth()
assign(basep, mat("base", srgb("#16304F"), rough=0.2, metal=0.5, coat=1.0))
bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=0.35, vertices=96, location=(bx, by, 0.55))
cap = bpy.context.object
bv = cap.modifiers.new("b", "BEVEL")
bv.width = 0.12
bv.segments = 6
bpy.ops.object.shade_smooth()
capm = mat("cap", srgb("#2F9E62"), rough=0.12, coat=1.0, emit=srgb("#3CCB80"), emit_strength=0.0)
assign(cap, capm)
PRESS = int(os.environ.get("PRESS", 112))
key(cap, PRESS - 1, location=(bx, by, 0.55))
key(cap, PRESS + 2, location=(bx, by, 0.42))
key(cap, PRESS + 10, location=(bx, by, 0.5))
e = capm.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
e.default_value = 0
e.keyframe_insert("default_value", frame=PRESS)
e.default_value = 6
e.keyframe_insert("default_value", frame=PRESS + 3)
e.default_value = 2.5
e.keyframe_insert("default_value", frame=PRESS + 14)
lv = text("LIVE", size=0.55, extrude=0.03, bevel=0.004, name="live")
assign(lv, m_white)
lv.parent = cap
lv.location = (0, 0, 0.18)
lv.rotation_euler = (0, 0, 0)
lv.data.align_y = "CENTER"
bpy.context.view_layer.objects.active = basep
bpy.ops.rigidbody.object_add(type="PASSIVE")
bpy.context.view_layer.objects.active = cap
bpy.ops.rigidbody.object_add(type="PASSIVE")
cap.rigid_body.kinematic = True

m_ink = mat("ink", srgb("#16304F"), rough=0.4)
m_warm = mat("warm", srgb("#B4532A"), rough=0.3, coat=0.5)


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


ty = by + 0.2
t1 = text("Push one button.", size=0.6, extrude=0.04, bevel=0.005, name="t1")
assign(t1, m_ink)
rise_in(t1, PRESS + 6, (bx, ty, 3.5), out=150)
t2 = text("We do the rest.", size=0.6, extrude=0.04, bevel=0.005, name="t2")
assign(t2, m_warm)
rise_in(t2, PRESS + 12, (bx, ty, 2.7), out=150)
pill = rounded_box("pill", (4.4, 0.3, 1.0), bevel=0.45, m=mat("pillm", srgb("#16304F"), rough=0.2, coat=1.0, emit=srgb("#16304F"), emit_strength=0.2))
ct = text("Comment “WEBSITE”", size=0.52, extrude=0.04, bevel=0.005, name="ct")
assign(ct, m_white)
ct.parent = pill
ct.location = (0, -0.18, -0.21)
rise_in(pill, 156, (bx, ty, 3.1))
t3 = text("€100 · first 10 clients · beribus.com", size=0.3, extrude=0.02, bevel=0.003, font=FONT_SB, name="t3")
assign(t3, m_ink)
rise_in(t3, 164, (bx, ty, 2.35))

cam, tgt = camera((0, -6, 3), (0, 2, 1), lens=30)
cam.data.dof.use_dof = True
cam.data.dof.aperture_fstop = 2.8
focus = bpy.data.objects.new("focus", None)
bpy.context.collection.objects.link(focus)
cam.data.dof.focus_object = focus
# tracking shot along the run
key(cam, 1, location=(px - 1.5, py - 4.0, 2.0))
key(cam, 30, location=(px - 2.5, py - 3.2, 2.4))
key(cam, 70, location=(-3.2, 3.0, 2.8))
key(cam, PRESS, location=(bx - 2.5, by - 4.5, 3.0))
key(cam, FRAMES, location=(bx, by - 9.0, 3.2))
key(tgt, 1, location=(px, py + 1.0, 1.0))
key(tgt, 30, location=(px, py + 1.5, 1.0))
key(tgt, 70, location=(pts[8][0], pts[8][1], 0.8))
key(tgt, PRESS, location=(bx, by, 0.8))
key(tgt, FRAMES, location=(bx, by, 2.4))
key(focus, 1, location=(px, py, 1.0))
key(focus, 70, location=(pts[8][0], pts[8][1], 0.8))
key(focus, PRESS, location=(bx, by, 0.8))
key(focus, FRAMES, location=(bx, ty, 2.8))
ease(cam)
ease(tgt)
if os.path.exists(MEME):
    shatter(cam, MEME, f0=2, impact=(float(os.environ.get("IMPX", 0.5)), float(os.environ.get("IMPY", 0.5))), dist=0.6, power=1.0)

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
