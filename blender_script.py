import bpy
import os
import sys
from math import cos, sin, tan

def render_360(stl_path, output_dir):
    # estraggo il nome del file senza estensione dal path
    file_name = os.path.splitext(os.path.basename(stl_path))[0]

    # Cancella tutti gli oggetti esistenti
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Importa il file STL
    # bpy.ops.import_mesh.stl(filepath=stl_path)
    bpy.ops.wm.stl_import(filepath=stl_path)

    # Ridimensiona la mesh importata a 10 metri di altezza
    imported_object = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = imported_object
    scale_factor = 10 / imported_object.dimensions.z
    imported_object.scale = (scale_factor, scale_factor, scale_factor)
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    # ruoto l'oggetto sperando di metterlo frontale
    object_base_rotation = 6.28319 / 2.75
    imported_object.rotation_euler[2] = object_base_rotation

    # recupera le coordinate boundary XYZ dell'oggetto
    min_x = imported_object.bound_box[0][0]
    max_x = imported_object.bound_box[0][0]
    min_y = imported_object.bound_box[0][1]
    max_y = imported_object.bound_box[0][1]
    min_z = imported_object.bound_box[0][2]
    max_z = imported_object.bound_box[0][2]

    for i in range(1, 8):
        if imported_object.bound_box[i][0] < min_x:
            min_x = imported_object.bound_box[i][0]
        if imported_object.bound_box[i][0] > max_x:
            max_x = imported_object.bound_box[i][0]
        if imported_object.bound_box[i][1] < min_y:
            min_y = imported_object.bound_box[i][1]
        if imported_object.bound_box[i][1] > max_y:
            max_y = imported_object.bound_box[i][1]
        if imported_object.bound_box[i][2] < min_z:
            min_z = imported_object.bound_box[i][2]
        if imported_object.bound_box[i][2] > max_z:
            max_z = imported_object.bound_box[i][2]

    x_distance = 10
    y_distance = 10
    z_distance = 5

    # Aggiungi una camera
    camera_location = (max_x + x_distance, max_y + x_distance, max_z + z_distance)
    # camera_look_at = ((min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2)
    # direction = [camera_look_at[i] - camera_location[i] for i in range(3)]
    bpy.ops.object.camera_add(location=camera_location)
    camera = bpy.context.object
    camera.rotation_euler = bpy.context.scene.cursor.rotation_euler
    bpy.context.view_layer.objects.active = camera
    bpy.ops.object.constraint_add(type='TRACK_TO')
    camera.constraints["Track To"].target = imported_object
    camera.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
    camera.constraints["Track To"].up_axis = 'UP_Y'

    color_nerdify_pink = (1, 0.0202883, 0.346704)
    color_nerdify_green = (0.283147, 0.887924, 0.03434)

    # front right (from obj perspective)
    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(-3, -8, 13), scale=(1, 1, 1), rotation=(-4, -3.7, -6.6))
    area_light_1 = bpy.context.object
    area_light_1.data.energy = 500


    # front left (from obj perspective)
    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(12, -6, 14), scale=(1, 1, 1), rotation=(-3.3, -2.1, -6.6))
    area_light_2 = bpy.context.object
    area_light_2.data.energy = 500
    # at same position add a colored light
    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(12, -6, 14), scale=(1, 1, 1), rotation=(-3.3, -2.1, -6.6))
    area_light_2 = bpy.context.object
    area_light_2.data.energy = 800
    area_light_2.data.color = color_nerdify_green

    
    # back center (from obj perspective)
    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(0.9, 14, 9.7), scale=(1, 1, 1), rotation=(-3.9, -2, -3.9))
    area_light_3 = bpy.context.object
    area_light_3.data.energy = 300
    # at same position add a colored light
    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(0.9, 14, 9.7), scale=(1, 1, 1), rotation=(-3.9, -2, -3.9))
    area_light_3 = bpy.context.object
    area_light_3.data.energy = 500
    area_light_3.data.color = color_nerdify_pink
    
    # front bottom center (from obj perspective)
    bpy.ops.object.light_add(type='AREA', align='WORLD', location=(0, -14, 6), scale=(1, 1, 1), rotation=(-4.6, 0, 0))
    area_light_4 = bpy.context.object
    area_light_4.data.energy = 500

    # Imposta la scena
    bpy.context.scene.camera = camera
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.file_format = 'PNG'

    # Aggiungi un'immagine di background
    if True:
        # maybe here you need the abs path
        filepath = "background.jpg"
        # extract only file name
        planeimagefilename = os.path.basename(filepath)
        # extract only directory to the file
        filepath = os.path.dirname(filepath)

        bpy.ops.image.import_as_mesh_planes(relative=False, filepath=filepath, files=[{"name":planeimagefilename, "name":planeimagefilename}], directory=filepath)

        empty = bpy.context.selected_objects[0]
        bpy.context.object.scale = (88, 88, 1)
        bpy.context.object.rotation_euler[2] = 2.35619
        empty.location = (-60, -60, -15)
        
        # add Image for background
        bpy.ops.object.light_add(type='AREA', align='WORLD', location=(-30, -30, -2), scale=(1, 1, 1), rotation=(-0.785, 1.5, 0))
        area_light_1 = bpy.context.object
        area_light_1.data.energy = 9e3

    # capture screenshot while object rotates
    num_screenshots = 5
    for i in range(num_screenshots):
        angle = object_base_rotation + (i / num_screenshots) * 6.28319  # 360 degrees in radians
        imported_object.rotation_euler[2] = angle
     
        bpy.context.scene.render.filepath = os.path.join(output_dir, f"{file_name:s}-screenshot_{i:03d}.jpg")
        bpy.ops.render.render(write_still=True)


    # Set the output format to FFMPEG and the codec to MPEG4
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.filepath = os.path.join(output_dir, file_name + ".mp4")

    # duration in seconds
    duration = 5
    bpy.context.scene.render.fps = 25
    frame_number = int(bpy.context.scene.render.fps * duration)

    # Animate the rotation of the camera
    imported_object.rotation_mode = 'XYZ'
    imported_object.rotation_euler[2] = object_base_rotation
    imported_object.keyframe_insert(data_path="rotation_euler", frame=i)
    imported_object.rotation_euler[2] = object_base_rotation + 6.28319  # 360 gradi
    imported_object.keyframe_insert(data_path="rotation_euler", frame=frame_number)

    # Set the start and end frames
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = frame_number

    # Render the animation
    bpy.ops.render.render(animation=True)

    return True

if __name__ == "__main__":
    # maybe here you need the abs path
    base_dir = ".\\"
    source_dir = os.path.join(base_dir, "source")
    completed_dir = os.path.join(base_dir, "completed")
    rendered_dir = os.path.join(base_dir, "rendered")
    print ("I will search all stl and obj files in the source directory (%s)" % source_dir)

    if not os.path.exists(completed_dir):
        os.makedirs(completed_dir)
    if not os.path.exists(rendered_dir):
        os.makedirs(rendered_dir)

    print("Starting processing")

    for file_name in os.listdir(source_dir):
        print(f"Processing {file_name}")
        if file_name.endswith(".stl") or file_name.endswith(".obj"):
            stl_path = os.path.join(source_dir, file_name)

            print(f"{stl_path} - Start")
            result = render_360(stl_path, rendered_dir)
            if result:
                print(f"{stl_path} - Done, moving to completed folder")
                # os.rename(stl_path, os.path.join(completed_dir, file_name))
            else:
                print(f"{stl_path} - Error")
            
    
