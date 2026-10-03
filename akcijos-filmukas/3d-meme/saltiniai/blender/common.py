"""Shared Blender helpers for the Beribus 3D ads: studio, materials, text, logo, render setup."""
import math
import os
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_XB = os.path.join(HERE, "Inter-ExtraBold.ttf")
FONT_SB = os.path.join(HERE, "Inter-SemiBold.ttf")
MARK_SVG = os.path.join(HERE, "mark.svg")
FPS = 24


def srgb(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((x + 0.055) / 1.055) ** 2.4 if x > 0.04045 else x / 12.92 for x in c) + (1.0,)


NAVY, NAVY2, DEEP, WARM, WARM2, PEACH, CREAM, WHITE = (srgb(x) for x in ("#16304F", "#2C5079", "#0B1626", "#B4532A", "#E08A62", "#F0C3AD", "#F5F5F2", "#FFFFFF"))


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.fps = FPS
    return sc


def mat(name, color, rough=0.35, metal=0.0, coat=0.0, emit=None, emit_strength=1.0, trans=0.0, ior=1.45):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = color
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Transmission Weight"].default_value = trans
    b.inputs["IOR"].default_value = ior
    if emit is not None:
        b.inputs["Emission Color"].default_value = emit
        b.inputs["Emission Strength"].default_value = emit_strength
    return m


def assign(obj, m):
    obj.data.materials.clear()
    obj.data.materials.append(m)


def studio(floor_color=None, wall_color=None, world=(0.01, 0.015, 0.03, 1), floor_rough=0.22):
    """Dark seamless cyclorama: floor curving into a back wall."""
    fc = floor_color or srgb("#0E1B2D")
    wc = wall_color or srgb("#122440")
    # cyclorama from a bent plane
    verts, faces = [], []
    xs = [-30, 30]
    prof = []
    for i in range(0, 40):
        y = -30 + i * 1.0
        prof.append((y, 0.0))
    r = 6.0
    for i in range(1, 17):
        a = i / 16 * math.pi / 2
        prof.append((10 + r * math.sin(a), r - r * math.cos(a)))
    for z in range(1, 12):
        prof.append((10 + r, r + z * 2.0))
    for j, (y, z) in enumerate(prof):
        for x in xs:
            verts.append((x, y, z))
    for j in range(len(prof) - 1):
        a, b, c, d = j * 2, j * 2 + 1, j * 2 + 3, j * 2 + 2
        faces.append((a, b, c, d))
    me = bpy.data.meshes.new("cyc")
    me.from_pydata(verts, [], faces)
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new("cyc", me)
    bpy.context.collection.objects.link(ob)
    m = mat("cyc", fc, rough=floor_rough)
    # gradient: floor to wall color by height
    nt = m.node_tree
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = fc
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = wc
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Max"].default_value = 14
    nt.links.new(geo.outputs["Position"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
    assign(ob, m)
    w = bpy.data.worlds.new("w")
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = world
    w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
    return ob


def light(kind, loc, rot, power, color=(1, 1, 1), size=2.0, name=None, spot=None):
    d = bpy.data.lights.new(name or kind, kind)
    d.energy = power
    d.color = color
    if kind == "AREA":
        d.size = size
        d.shape = "DISK"
    if kind == "SPOT" and spot:
        d.spot_size = spot
        d.spot_blend = 0.6
    o = bpy.data.objects.new(name or kind, d)
    o.location = loc
    o.rotation_euler = rot
    bpy.context.collection.objects.link(o)
    return o


def aim(obj, target):
    """Point an object's -Z axis at a target location."""
    from mathutils import Vector
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def camera(loc, target, lens=30, dof=None, fstop=2.0):
    cd = bpy.data.cameras.new("cam")
    cd.lens = lens
    cd.sensor_fit = "AUTO"
    o = bpy.data.objects.new("cam", cd)
    bpy.context.collection.objects.link(o)
    o.location = loc
    tgt = bpy.data.objects.new("cam_target", None)
    bpy.context.collection.objects.link(tgt)
    tgt.location = target
    c = o.constraints.new("TRACK_TO")
    c.target = tgt
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    if dof:
        cd.dof.use_dof = True
        cd.dof.focus_object = dof
        cd.dof.aperture_fstop = fstop
    bpy.context.scene.camera = o
    return o, tgt


def text(body, size=1.0, extrude=0.12, bevel=0.015, font=FONT_XB, align="CENTER", spacing=1.0, name=None):
    cu = bpy.data.curves.new(name or "txt", "FONT")
    cu.body = body
    cu.font = bpy.data.fonts.load(font, check_existing=True)
    cu.size = size
    cu.extrude = extrude
    cu.bevel_depth = bevel
    cu.bevel_resolution = 3
    cu.align_x = align
    cu.align_y = "BOTTOM_BASELINE"
    cu.space_character = spacing
    cu.resolution_u = 6
    o = bpy.data.objects.new(name or "txt", cu)
    bpy.context.collection.objects.link(o)
    o.rotation_euler = (math.pi / 2, 0, 0)  # stand upright, facing -Y
    return o


def to_mesh(o):
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.convert(target="MESH")
    return bpy.context.view_layer.objects.active


def split_loose(o):
    """Separate a mesh into loose parts; returns the new objects sorted left to right."""
    bpy.ops.object.select_all(action="DESELECT")
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.separate(type="LOOSE")
    bpy.ops.object.mode_set(mode="OBJECT")
    parts = list(bpy.context.selected_objects)
    for p in parts:
        bpy.ops.object.select_all(action="DESELECT")
        p.select_set(True)
        bpy.context.view_layer.objects.active = p
        bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    return sorted(parts, key=lambda p: p.location.x)


def logo(height=1.0, depth=0.18, m=None, name="logo"):
    """Extruded, bevelled Beribus mark (traced outline) standing upright, base at origin."""
    import json
    d = json.load(open(os.path.join(HERE, "mark.json")))
    sc_ = height / d["h"]
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "2D"
    cu.fill_mode = "BOTH"
    P = lambda q: ((q[0] - d["w"] / 2) * sc_, (d["h"] - q[1]) * sc_)
    for c in d["curves"]:
        if len(c["segs"]) <= 4:
            continue  # potrace frame, not part of the mark
        pts = []  # (co, handle_left, handle_right)
        cur = P(c["start"])
        nodes = [[cur, cur, cur]]
        for sg in c["segs"]:
            if sg[0] == "L":
                a, b = P(sg[1]), P(sg[2])
                nodes.append([a, a, a]); nodes.append([b, b, b])
            else:
                c1, c2, e = P(sg[1]), P(sg[2]), P(sg[3])
                nodes[-1][2] = c1
                nodes.append([e, c2, e])
        # closing: last node coincides with first
        first, last = nodes[0], nodes[-1]
        first[1] = last[1]
        nodes = nodes[:-1]
        sp = cu.splines.new("BEZIER")
        sp.bezier_points.add(len(nodes) - 1)
        for bp, (co, hl, hr) in zip(sp.bezier_points, nodes):
            bp.co = (co[0], co[1], 0)
            bp.handle_left_type = bp.handle_right_type = "FREE"
            bp.handle_left = (hl[0], hl[1], 0)
            bp.handle_right = (hr[0], hr[1], 0)
        sp.use_cyclic_u = True
    cu.extrude = depth
    cu.bevel_depth = depth * 0.12
    cu.bevel_resolution = 4
    cu.resolution_u = 24
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    o.rotation_euler = (math.pi / 2, 0, 0)
    if m:
        cu.materials.append(m)
    return o


def key(obj, frame, **props):
    for k, v in props.items():
        setattr(obj, k, v)
        obj.keyframe_insert(data_path=k, frame=frame)


def ease(obj, kind="BEZIER", easing="AUTO", path=None):
    ad = obj.animation_data
    if not ad or not ad.action:
        return
    for fc in fcurves(ad.action):
        if path and fc.data_path != path:
            continue
        for kp in fc.keyframe_points:
            kp.interpolation = kind
            kp.easing = easing


def fcurves(action):
    if hasattr(action, "fcurves") and action.fcurves is not None:
        try:
            return list(action.fcurves)
        except TypeError:
            pass
    out = []
    for layer in getattr(action, "layers", []):
        for strip in layer.strips:
            for bag in strip.channelbags:
                out += list(bag.fcurves)
    return out


def render_setup(sc, out_dir, frames, res=(576, 1024), samples=10, blur=True):
    sc.frame_start, sc.frame_end = 1, frames
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.denoising_quality = "BALANCED"
    sc.cycles.denoising_prefilter = "NONE"
    sc.cycles.max_bounces = 4
    sc.cycles.diffuse_bounces = 1
    sc.cycles.glossy_bounces = 2
    sc.cycles.transmission_bounces = 2
    sc.cycles.transparent_max_bounces = 4
    sc.cycles.caustics_reflective = False
    sc.cycles.caustics_refractive = False
    sc.cycles.blur_glossy = 1.0
    sc.cycles.adaptive_threshold = 0.04
    sc.cycles.use_auto_tile = False
    sc.render.use_persistent_data = True
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.use_motion_blur = blur
    sc.render.motion_blur_shutter = 0.5
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = os.path.join(out_dir, "f_")
    try:
        sc.view_settings.view_transform = "AgX"
        sc.view_settings.look = "AgX - Medium High Contrast"
    except TypeError:
        pass


def image_mat(name, path, emit=1.0, rough=0.12):
    """Screen-like material: the image shows at its own brightness, with a glassy sheen on top."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(path, check_existing=True)
    tex.extension = "EXTEND"
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(tex.outputs["Color"], b.inputs["Emission Color"])
    b.inputs["Emission Strength"].default_value = emit
    b.inputs["Roughness"].default_value = rough
    b.inputs["Coat Weight"].default_value = 0.6
    return m, tex


def view_size(cam, dist):
    """Width/height of the camera's view at a distance (portrait, sensor fit on height)."""
    sc = bpy.context.scene
    h = 2 * dist * (cam.data.sensor_width / 2) / cam.data.lens
    return h * sc.render.resolution_x / sc.render.resolution_y, h


def shatter(cam, img_path, f0, impact=(0.5, 0.5), dist=1.2, cols=9, rows=16, seed=4, power=1.0):
    """The meme's last frame as a pane right in front of the lens that cracks, then bursts past the camera.
    impact is in image UV (0..1, origin top-left)."""
    import random
    from mathutils import Vector
    rnd = random.Random(seed)
    W, H = view_size(cam, dist)
    m, _ = image_mat("pane", img_path, emit=1.0)
    m.node_tree.nodes["Principled BSDF"].inputs["Coat Weight"].default_value = 1.0
    # jittered grid
    P = {}
    for j in range(rows + 1):
        for i in range(cols + 1):
            u, v = i / cols, j / rows
            if 0 < i < cols:
                u += rnd.uniform(-0.38, 0.38) / cols
            if 0 < j < rows:
                v += rnd.uniform(-0.38, 0.38) / rows
            P[i, j] = (u, v)
    tris = []
    for j in range(rows):
        for i in range(cols):
            a, b, c, d = P[i, j], P[i + 1, j], P[i + 1, j + 1], P[i, j + 1]
            tris += [(a, b, c), (a, c, d)] if rnd.random() < 0.5 else [(a, b, d), (b, c, d)]
    ix, iy = impact
    shards = []
    for k, tri in enumerate(tris):
        cu = sum(p[0] for p in tri) / 3
        cv = sum(p[1] for p in tri) / 3
        verts = [((p[0] - cu) * W, -(p[1] - cv) * H, 0) for p in tri]
        me = bpy.data.meshes.new(f"sh{k}")
        me.from_pydata(verts, [], [(0, 1, 2)])
        uv = me.uv_layers.new()
        for li, loop in enumerate(me.loops):
            p = tri[loop.vertex_index]
            uv.data[li].uv = (p[0], 1 - p[1])
        me.materials.append(m)
        ob = bpy.data.objects.new(f"sh{k}", me)
        bpy.context.collection.objects.link(ob)
        sol = ob.modifiers.new("s", "SOLIDIFY")
        sol.thickness = 0.006
        ob.parent = cam
        home = Vector(((cu - 0.5) * W, -(cv - 0.5) * H, -dist))
        dx, dy = cu - ix, (cv - iy) * H / W
        r = math.hypot(dx, dy) + 1e-3
        delay = r * 7
        out = Vector((dx / r, -dy / r, 0)) * rnd.uniform(0.6, 1.4) * power
        fly = out * 1.6 + Vector((0, 0, rnd.uniform(1.0, 2.2) * power))  # toward/past the lens
        rot = Vector((rnd.uniform(-3, 3), rnd.uniform(-3, 3), rnd.uniform(-2, 2)))
        ob.location = home
        ob.keyframe_insert("location", frame=1)
        ob.keyframe_insert("location", frame=f0)
        # hairline crack: tiny inward nudge
        ob.location = home + Vector((0, 0, rnd.uniform(-0.004, 0.004)))
        ob.rotation_euler = (rnd.uniform(-0.03, 0.03), rnd.uniform(-0.03, 0.03), 0)
        ob.keyframe_insert("location", frame=f0 + 1 + int(delay * 0.3))
        ob.keyframe_insert("rotation_euler", frame=f0 + 1 + int(delay * 0.3))
        st = f0 + 2 + int(delay)
        ob.keyframe_insert("location", frame=st)
        ob.keyframe_insert("rotation_euler", frame=st)
        ob.location = home + fly
        ob.rotation_euler = rot
        ob.keyframe_insert("location", frame=st + 12)
        ob.keyframe_insert("rotation_euler", frame=st + 12)
        for fc in fcurves(ob.animation_data.action):
            for kp in fc.keyframe_points:
                kp.interpolation = "QUAD" if kp.co[0] >= st else "CONSTANT"
                kp.easing = "EASE_IN"
        # hide once well past the lens
        ob.hide_render = False
        ob.keyframe_insert("hide_render", frame=st + 11)
        ob.hide_render = True
        ob.keyframe_insert("hide_render", frame=st + 12)
        shards.append(ob)
    return shards


def rounded_box(name, size, bevel=0.08, m=None):
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    b = o.modifiers.new("bev", "BEVEL")
    b.width = bevel
    b.segments = 6
    b.limit_method = "NONE"
    bpy.ops.object.shade_smooth()
    if m:
        assign(o, m)
    return o


def phone(name="phone", h=3.2, screen_img=None, body_color="#1B1F26"):
    """A modern phone: rounded titanium body, glass screen with an image, standing upright facing -Y.
    Returns (body, screen_material_emission_input)."""
    w, d = h * 0.47, h * 0.055
    body = rounded_box(name, (w, d, h), bevel=w * 0.16, m=mat(name + "_m", srgb(body_color), rough=0.28, metal=0.85, coat=0.3))
    sm = None
    if screen_img:
        bpy.ops.mesh.primitive_plane_add(size=1)
        scr = bpy.context.object
        scr.name = name + "_screen"
        scr.scale = (w * 0.92, h * 0.955, 1)
        bpy.ops.object.transform_apply(scale=True)
        # round the screen corners
        b = scr.modifiers.new("bev", "BEVEL")
        b.affect = "VERTICES"
        b.width = w * 0.12
        b.segments = 10
        scr.rotation_euler = (math.pi / 2, 0, 0)
        scr.location = (0, -d / 2 - 0.002, 0)
        scr.parent = body
        m, tex = image_mat(name + "_scr", screen_img, emit=1.0, rough=0.05)
        assign(scr, m)
        sm = m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    return body, sm


def seq_material(name, first_frame, nframes, emit=1.0):
    """Emissive screen material playing a PNG sequence (the meme keeps running on the device)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new("ShaderNodeTexImage")
    img = bpy.data.images.load(first_frame)
    img.source = "SEQUENCE"
    tex.image = img
    tex.image_user.frame_duration = nframes
    tex.image_user.frame_start = 1
    tex.image_user.frame_offset = 0
    tex.image_user.use_auto_refresh = True
    tex.image_user.use_cyclic = True
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(tex.outputs["Color"], b.inputs["Emission Color"])
    b.inputs["Emission Strength"].default_value = emit
    b.inputs["Roughness"].default_value = 0.05
    b.inputs["Coat Weight"].default_value = 0.8
    return m


def device(kind, screen_mat, hs=3.0, body_color="#15181E"):
    """A device with an exact 9:16 screen facing -Y, centred on its screen.
    kind: phone | totem. Returns the root object and the screen height."""
    ws = hs * 9 / 16
    if kind == "phone":
        body = rounded_box("dev", (ws * 1.08, hs * 0.06, hs * 1.06), bevel=ws * 0.14, m=mat("devm", srgb(body_color), rough=0.25, metal=0.85, coat=0.4))
    else:  # tall free-standing display on a base
        body = rounded_box("dev", (ws * 1.06, hs * 0.08, hs * 1.04), bevel=0.06, m=mat("devm", srgb(body_color), rough=0.3, metal=0.6, coat=0.3))
        stand = rounded_box("stand", (ws * 0.5, hs * 0.3, hs * 0.12), bevel=0.05, m=mat("standm", srgb(body_color), rough=0.3, metal=0.6))
        stand.parent = body
        stand.location = (0, 0, -hs * 0.58)
    bpy.ops.mesh.primitive_plane_add(size=1)
    scr = bpy.context.object
    scr.name = "screen"
    scr.scale = (ws, hs, 1)
    bpy.ops.object.transform_apply(scale=True)
    scr.rotation_euler = (math.pi / 2, 0, 0)
    scr.location = (0, -(hs * (0.03 if kind == "phone" else 0.04)) - 0.003, 0)
    scr.parent = body
    assign(scr, screen_mat)
    return body, hs


def pull_out_camera(dev, hs, lens=30, fill=1.0):
    """Camera square-on to the device screen so the screen exactly fills the frame."""
    d = hs * lens / 36 * fill
    from mathutils import Vector
    bpy.context.view_layer.update()
    scr = [c for c in dev.children if c.name.startswith("screen")][0]
    sy = scr.matrix_world.translation.y
    cam, tgt = camera((dev.location.x, sy - d, dev.location.z), (dev.location.x, sy + 5, dev.location.z), lens=lens)
    return cam, tgt, d
