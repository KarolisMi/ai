import bpy, time, sys
eng = sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=64, ring_count=32); bpy.ops.object.shade_smooth()
m = bpy.data.materials.new("m"); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (0.8, 0.3, 0.1, 1); b.inputs["Roughness"].default_value = 0.25
bpy.context.object.data.materials.append(m)
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -1))
bpy.ops.object.light_add(type='AREA', location=(3, -3, 5)); bpy.context.object.data.energy = 800; bpy.context.object.data.size = 3
bpy.ops.object.camera_add(location=(0, -6, 1.5), rotation=(1.35, 0, 0)); sc.camera = bpy.context.object
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.08, 0.15, 1)
sc.render.resolution_x, sc.render.resolution_y = 720, 1280
sc.render.filepath = f"/tmp/claude-0/-home-user-ai/032b34d0-ed06-5306-99df-beee661f300d/scratchpad/b3d/test_{eng}.png"
if eng == 'CYCLES':
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 24; sc.cycles.use_denoising = True; sc.render.threads_mode = 'AUTO'
else:
    sc.render.engine = 'BLENDER_EEVEE'
t = time.time(); bpy.ops.render.render(write_still=True); print("RENDER", eng, round(time.time() - t, 2))
