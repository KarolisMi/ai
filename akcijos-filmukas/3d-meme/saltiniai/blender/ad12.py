"""Ad 12 · The rage-quit monitor keeps flying in 3D, dunks into a bin; a new monitor rises with the €100 site."""
import math, os, sys
import bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = os.path.join(HERE, "out", "ad12")
FRAMES = 150
sc = reset(); sc.render.fps = 25
studio(floor_color=srgb("#3A4252"), wall_color=srgb("#2C3A52"), floor_rough=0.6)
light("AREA", (-5, -4, 7), (0, 0, 0), 2400, (1.0, 0.9, 0.8), size=5, name="key"); aim(bpy.data.objects["key"], (0, 3, 1.5))
light("AREA", (6, 6, 4), (0, 0, 0), 1500, (0.55, 0.7, 1.0), size=4, name="rim"); aim(bpy.data.objects["rim"], (0, 3, 1.5))
light("AREA", (0, -2, 10), (0, 0, 0), 400, (1, 1, 1), size=8, name="top"); aim(bpy.data.objects["top"], (0, 3, 0))

def plane(name, w, h, m):
    bpy.ops.mesh.primitive_plane_add(size=1); o = bpy.context.object; o.name = name; o.scale = (w, h, 1); bpy.ops.object.transform_apply(scale=True); assign(o, m); return o

# ---------- old CRT with the ugly site ----------
m_beige = mat("beige", srgb("#CFC4A8"), rough=0.6)
m_dark = mat("dark", srgb("#2A2A2A"), rough=0.5)
old_scr, _ = image_mat("oldscr", os.path.join(HERE, "oldsite.png"), emit=1.4)
crt = rounded_box("crt", (1.7, 1.5, 1.45), bevel=0.12, m=m_beige)
bezel = rounded_box("bezel", (1.45, 0.06, 1.12), bevel=0.04, m=m_dark); bezel.parent = crt; bezel.location = (0, -0.76, 0.06)
scr = plane("scr", 1.3, 0.98, old_scr); scr.rotation_euler = (math.radians(90), 0, 0); scr.parent = crt; scr.location = (0, -0.795, 0.06)
cable = rounded_box("cable", (0.08, 1.2, 0.08), bevel=0.03, m=m_dark); cable.parent = crt; cable.location = (0.4, 1.2, -0.5)
# flight: from beside the lens (where the meme threw it) to the bin, slow-mo tumble
BIN = (3.2, 5.0, 0)
key(crt, 1, location=(-1.6, -3.2, 2.4), rotation_euler=(0.3, -0.6, 0.9))
key(crt, 6, location=(-0.9, -1.6, 2.9), rotation_euler=(0.5, -0.2, 0.6))
key(crt, 30, location=(1.9, 2.6, 3.3), rotation_euler=(1.6, 0.9, -0.6))
key(crt, 40, location=(3.2, 5.0, 1.35), rotation_euler=(2.6, 1.2, -1.1))
key(crt, 44, location=(3.2, 5.0, 0.95), rotation_euler=(2.7, 1.25, -1.15))
for fc in fcurves(crt.animation_data.action):
    for kp in fc.keyframe_points:
        if kp.co[0] in (30, 40): kp.interpolation, kp.easing = "QUAD", "EASE_IN" if kp.co[0] == 40 else "EASE_OUT"
# bin
m_bin = mat("bin", srgb("#4A5260"), rough=0.35, metal=0.7)
bpy.ops.mesh.primitive_cylinder_add(radius=1.25, depth=1.9, location=(BIN[0], BIN[1], 0.95)); b = bpy.context.object; assign(b, m_bin)
s = b.modifiers.new("s", "SOLIDIFY"); s.thickness = 0.06
bpy.ops.object.mode_set(mode="EDIT"); import bmesh
bm = bmesh.from_edit_mesh(b.data)
for f in bm.faces:
    if f.normal.z > 0.9: f.select = True
    else: f.select = False
bpy.ops.mesh.delete(type="FACE"); bpy.ops.object.mode_set(mode="OBJECT")
bin_txt = text("€850 website", size=0.32, extrude=0.02, bevel=0.003, font=FONT_SB, name="bintxt"); assign(bin_txt, mat("bt", srgb("#E8EDF3"), emit=srgb("#E8EDF3"), emit_strength=0.3)); bin_txt.rotation_euler = (math.radians(90), 0, math.radians(-25)); bin_txt.location = (BIN[0] - 0.55, BIN[1] - 1.22, 1.1)
key(b, 1, rotation_euler=(0, 0, 0)); key(b, 40, rotation_euler=(0, 0, 0)); key(b, 43, rotation_euler=(0.12, -0.08, 0)); key(b, 47, rotation_euler=(-0.06, 0.04, 0)); key(b, 52, rotation_euler=(0, 0, 0))

# ---------- desk + new monitor ----------
m_desk = mat("desk", srgb("#E9E4DA"), rough=0.45)
m_alu = mat("alu", srgb("#C9CED6"), rough=0.25, metal=0.85)
m_black = mat("black", srgb("#0C0F14"), rough=0.2, coat=1.0)
DX = -2.4
desk = rounded_box("desk", (4.6, 2.2, 0.14), bevel=0.04, m=m_desk); desk.location = (DX, 3.2, 1.3)
for lx in (-2.1, 2.1):
    leg = rounded_box("leg", (0.12, 1.9, 1.3), bevel=0.03, m=m_alu); leg.location = (DX + lx, 3.2, 0.65)
new_scr, scr_tex = image_mat("newscr", os.path.join(HERE, "sitewide.png"), emit=0.0)
mon = rounded_box("mon", (3.2, 0.09, 2.15), bevel=0.05, m=m_black)
ns = plane("ns", 3.02, 2.0, new_scr); ns.rotation_euler = (math.radians(90), 0, 0); ns.parent = mon; ns.location = (0, -0.05, 0.02)
stand = rounded_box("stand", (0.34, 0.12, 1.0), bevel=0.04, m=m_alu); stand.parent = mon; stand.location = (0, 0.12, -1.35)
foot = rounded_box("foot", (1.1, 0.75, 0.06), bevel=0.03, m=m_alu); foot.parent = mon; foot.location = (0, 0.15, -1.86)
key(mon, 1, location=(DX, 3.0, 9.0)); key(mon, 50, location=(DX, 3.0, 9.0)); key(mon, 60, location=(DX, 3.0, 3.29)); key(mon, 63, location=(DX, 3.0, 3.45)); key(mon, 66, location=(DX, 3.0, 3.29))
for fc in fcurves(mon.animation_data.action):
    for kp in fc.keyframe_points:
        if kp.co[0] == 60: kp.interpolation, kp.easing = "QUAD", "EASE_IN"
em = new_scr.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
for f, v in ((1, 0.0), (68, 0.0), (72, 1.6), (76, 0.75)): em.default_value = v; em.keyframe_insert("default_value", frame=f)
bc = new_scr.node_tree.nodes["Principled BSDF"].inputs["Base Color"]

# ---------- copy ----------
m_price = mat("price", srgb("#E07A4F"), rough=0.2, coat=1.0, emit=srgb("#E07A4F"), emit_strength=0.25)
m_txt = mat("txt", srgb("#FFFFFF"), rough=0.4, emit=srgb("#FFFFFF"), emit_strength=0.3)
def rise(o, f, loc):
    key(o, 1, location=(loc[0], loc[1], loc[2] - 0.6), scale=(0.001,) * 3); key(o, f, location=(loc[0], loc[1], loc[2] - 0.6), scale=(0.001,) * 3); key(o, f + 10, location=loc, scale=(1, 1, 1))
    for fc in fcurves(o.animation_data.action):
        for kp in fc.keyframe_points:
            if kp.co[0] == f + 10: kp.interpolation, kp.easing = "BACK", "EASE_OUT"
p = text("€100", size=1.6, extrude=0.25, bevel=0.025, name="p"); assign(p, m_price); p.rotation_euler = (math.radians(90), 0, 0); rise(p, 84, (DX, 3.0, 5.0))
l = text("New website · live in 5 days", size=0.4, extrude=0.04, bevel=0.005, name="l"); assign(l, m_txt); l.rotation_euler = (math.radians(90), 0, 0); rise(l, 94, (DX, 1.9, 1.0))
pill = rounded_box("pill", (4.4, 0.4, 0.82), bevel=0.36, m=mat("pillm", srgb("#16304F"), rough=0.2, coat=1.0, emit=srgb("#16304F"), emit_strength=0.2))
ct = text("Comment “WEBSITE”", size=0.45, extrude=0.04, bevel=0.005, name="ct"); assign(ct, m_txt); ct.rotation_euler = (math.radians(90), 0, 0); ct.parent = pill; ct.location = (0, -0.22, -0.16)
rise(pill, 108, (DX, 1.5, 0.3))

# ---------- camera ----------
cam, tgt = camera((-0.6, -3.8, 2.6), (0.6, 2.0, 2.6), lens=24)
key(cam, 1, location=(-0.6, -3.8, 2.6)); key(cam, 40, location=(0.6, -3.2, 2.4)); key(cam, 62, location=(-1.4, -4.2, 3.0)); key(cam, 110, location=(-2.3, -4.6, 3.2)); key(cam, FRAMES, location=(-2.1, -4.9, 3.1))
key(tgt, 1, location=(-0.4, 0.5, 2.7)); key(tgt, 30, location=(2.4, 4.0, 2.0)); key(tgt, 44, location=(3.0, 5.0, 1.2)); key(tgt, 62, location=(-2.0, 3.2, 2.8)); key(tgt, 110, location=(-2.4, 3.0, 2.8)); key(tgt, FRAMES, location=(-2.4, 3.0, 2.75))
ease(cam); ease(tgt)

render_setup(sc, OUT, FRAMES, samples=int(os.environ.get("SAMPLES", 10)))
sc.render.fps = 25
frames = os.environ.get("ONLY")
if frames:
    for f in [int(x) for x in frames.split(",")]:
        sc.frame_set(f); sc.render.filepath = os.path.join(OUT, f"test_{f:04d}"); bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(animation=True)
