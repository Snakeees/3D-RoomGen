import bpy
import math
import os
from random import randint

from constants import Config

a = 5
b = 2.5
c = 0.01


def create_blend(obj_file_path, mtl_file_path, texture_file_path):
    bpy.ops.scene.new()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.window.scene = bpy.data.scenes[-1]
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    bpy.ops.import_scene.obj(
        filepath=obj_file_path,
        use_split_objects=True,
        use_split_groups=True,
        use_image_search=True
    )

    if os.path.exists(mtl_file_path):
        bpy.ops.import_scene.obj(
            filepath=mtl_file_path,
            use_split_objects=True,
            use_split_groups=True,
            use_image_search=True
        )

    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.join()

    if os.path.exists(texture_file_path):
        texture = bpy.data.images.load(texture_file_path)
        material = bpy.data.materials.new(name="TextureMaterial")
        material.use_nodes = True
        bsdf = material.node_tree.nodes["Principled BSDF"]
        tex_image = material.node_tree.nodes.new("ShaderNodeTexImage")
        tex_image.image = texture
        material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

        for obj in bpy.data.objects:
            obj.data.materials.append(material)

    blend_file_path = os.path.splitext(os.path.abspath(obj_file_path))[0] + '.blend'

    try:
        os.remove(blend_file_path)
    except OSError:
        pass

    bpy.ops.wm.save_as_mainfile(filepath=blend_file_path)
    print(blend_file_path)
    bpy.ops.object.delete(use_global=False)
    bpy.ops.wm.quit_blender()


def create_walls():
    bpy.ops.scene.new()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.window.scene = bpy.data.scenes[-1]
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    floor_vertices = [(c, c, c), (a, c, c), (a, a, c), (c, a, c)]
    floor_faces = [(0, 1, 2, 3)]
    wall1_vertices = [(c, c, c), (a, c, c), (a, c, b), (c, c, b)]
    wall1_faces = [(0, 1, 2, 3)]
    wall2_vertices = [(a, c, c), (a, a, c), (a, a, b), (a, c, b)]
    wall2_faces = [(0, 1, 2, 3)]
    wall3_vertices = [(a, a, c), (c, a, c), (c, a, b), (a, a, b)]
    wall3_faces = [(0, 1, 2, 3)]
    wall4_vertices = [(c, a, c), (c, c, c), (c, c, b), (c, a, b)]
    wall4_faces = [(0, 1, 2, 3)]

    def create_object(vertices, faces, name):
        mesh = bpy.data.meshes.new(name)
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        mesh.from_pydata(vertices, [], faces)

    def add_floor_texture(texture_file_path):
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.join()

        if os.path.exists(texture_file_path):
            texture = bpy.data.images.load(texture_file_path)
            material = bpy.data.materials.new(name="TextureMaterial")
            material.use_nodes = True
            bsdf = material.node_tree.nodes["Principled BSDF"]
            tex_image = material.node_tree.nodes.new("ShaderNodeTexImage")
            tex_image.image = texture
            material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

            for obj in bpy.data.objects:
                obj.data.materials.append(material)

    create_object(floor_vertices, floor_faces, 'Floor')
    add_floor_texture(f"{os.getcwd()}/floor_textures/{randint(1,4)}.jpg")
    create_object(wall1_vertices, wall1_faces, 'Wall1')
    create_object(wall2_vertices, wall2_faces, 'Wall2')
    create_object(wall3_vertices, wall3_faces, 'Wall3')
    create_object(wall4_vertices, wall4_faces, 'Wall4')

def add_bed(dir):
    bed_blend_file = next((os.path.join(dir, f) for f in os.listdir(dir) if f.endswith('.blend')), None)

    with bpy.data.libraries.load(bed_blend_file) as (data_from, data_to):
        data_to.objects = data_from.objects

    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)

    object_name = 'model'
    obj = bpy.data.objects.get(object_name)

    if obj is not None:
        obj.name = 'Bed'
        dim = obj.dimensions
        wall3_center = (a / 2, 5 - (dim.z / 2), 0 / 2)
        obj.location = wall3_center
    else:
        print("Object 'model' not found in the scene.")

def add_table(dir):
    bed_blend_file = next((os.path.join(dir, f) for f in os.listdir(dir) if f.endswith('.blend')), None)

    with bpy.data.libraries.load(bed_blend_file) as (data_from, data_to):
        data_to.objects = data_from.objects

    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)

    object_name = 'model'
    obj = bpy.data.objects.get(object_name)

    if obj is not None:
        obj.name = 'Table'
        rotation_angle_degrees = 90.0
        rotation_angle_radians = math.radians(rotation_angle_degrees)
        obj.rotation_euler.z = rotation_angle_radians
        dim = obj.dimensions
        wall3_center = (dim.z/2, a/2, 0)
        obj.location = wall3_center
        return dim.z
    else:
        print("Object 'model' not found in the scene.")

def add_chair(dir, tablez):
    bed_blend_file = next((os.path.join(dir, f) for f in os.listdir(dir) if f.endswith('.blend')), None)

    with bpy.data.libraries.load(bed_blend_file) as (data_from, data_to):
        data_to.objects = data_from.objects

    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)

    object_name = 'model'
    obj = bpy.data.objects.get(object_name)

    if obj is not None:
        obj.name = 'Chair'
        rotation_angle_degrees = 270.0
        rotation_angle_radians = math.radians(rotation_angle_degrees)
        obj.rotation_euler.z = rotation_angle_radians
        dim = obj.dimensions
        wall3_center = ((tablez/2)+(dim.z/2)+0.1, a/2, 0)
        obj.location = wall3_center
    else:
        print("Object 'model' not found in the scene.")

def add_wardrobe(dir):
    bed_blend_file = next((os.path.join(dir, f) for f in os.listdir(dir) if f.endswith('.blend')), None)

    with bpy.data.libraries.load(bed_blend_file) as (data_from, data_to):
        data_to.objects = data_from.objects

    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)

    object_name = 'model'
    obj = bpy.data.objects.get(object_name)

    if obj is not None:
        obj.name = 'Wardrobe'
        rotation_angle_degrees = 270.0
        rotation_angle_radians = math.radians(rotation_angle_degrees)
        obj.rotation_euler.z = rotation_angle_radians
        dim = obj.dimensions
        wall3_center = (5-(dim.z/2), 5-(dim.x/2), 0)
        obj.location = wall3_center
    else:
        print("Object 'model' not found in the scene.")

def add_tv_stand(dir):
    bed_blend_file = next((os.path.join(dir, f) for f in os.listdir(dir) if f.endswith('.blend')), None)

    with bpy.data.libraries.load(bed_blend_file) as (data_from, data_to):
        data_to.objects = data_from.objects

    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)

    object_name = 'model'
    obj = bpy.data.objects.get(object_name)

    if obj is not None:
        obj.name = 'TV-Stand'
        rotation_angle_degrees = 180.0
        rotation_angle_radians = math.radians(rotation_angle_degrees)
        obj.rotation_euler.z = rotation_angle_radians
        dim = obj.dimensions
        wall3_center = (a/2, (dim.z/2), 0)
        obj.location = wall3_center
    else:
        print("Object 'model' not found in the scene.")

def add_light(dir):
    bed_blend_file = next((os.path.join(dir, f) for f in os.listdir(dir) if f.endswith('.blend')), None)

    with bpy.data.libraries.load(bed_blend_file) as (data_from, data_to):
        data_to.objects = data_from.objects

    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)

    object_name = 'model'
    obj = bpy.data.objects.get(object_name)

    if obj is not None:
        obj.name = 'Light'
        dim = obj.dimensions
        wall3_center = (a/2, a/2, b-dim.y)
        obj.location = wall3_center
    else:
        print("Object 'model' not found in the scene.")

def center():
    for obj in bpy.context.scene.objects:
        obj.location.x -= 2.5
        obj.location.y -= 2.5

def area_light():
    light_location = (0, 0, 3)
    bpy.ops.object.light_add(type='AREA', location=light_location)
    light_object = bpy.context.object
    light_object.data.energy = 1000.0
    light_object.data.size = 6.0


def save_file():
    cur_dir = os.getcwd()
    blend_files = [file for file in os.listdir(cur_dir) if file.lower().endswith('.blend')]
    path = f'{cur_dir}/out-{len(blend_files)+1}.blend'
    bpy.ops.wm.save_as_mainfile(filepath=path)

def run_blender(furniture_ids):
    create_walls()
    add_bed(Config.FUTURE_PATH+furniture_ids['Bed'])
    tablez = add_table(Config.FUTURE_PATH+furniture_ids['Table'])
    add_chair(Config.FUTURE_PATH+furniture_ids['Chair'], tablez)
    add_wardrobe(Config.FUTURE_PATH+furniture_ids['Wardrobe'])
    add_tv_stand(Config.FUTURE_PATH+furniture_ids['TV Stand'])
    add_light(Config.FUTURE_PATH+furniture_ids['Light'])
    center()
    area_light()
    bpy.context.scene.cycles.samples = 1024
    save_file()

