import bpy
import os

pi = 22.0/7.0

def eulerToDegree(euler):
    return ( (euler) / (2 * pi) ) * 360

def degreeToEuler(degree):
    return ( (degree) / 360 ) * 2 * pi

def render_360(stl_path, output_dir):
    photo_count = 5
    make_video = True
    # in seconds
    video_duration = 5

    # maybe you should use an absolute path
    background_image_path = "background.jpg"

    # estraggo il nome del file senza estensione dal path
    stl_filename = os.path.splitext(os.path.basename(stl_path))[0]

    # Cancella tutti gli oggetti esistenti
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Importa il file STL
    # bpy.ops.import_mesh.stl(filepath=stl_path)
    bpy.ops.wm.stl_import(filepath=stl_path)

    # Ridimensiona la mesh importata a 10 metri di altezza
    imported_object = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = imported_object
    scale_factor = 10 / max(imported_object.dimensions.x, imported_object.dimensions.y, imported_object.dimensions.z)
    imported_object.scale = (scale_factor, scale_factor, scale_factor)
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    # Move the object to have its bottom at z=0 and its center at (0, 0)
    imported_object.location = (0,0,0)

    # ruoto l'oggetto sperando di metterlo frontale
    object_base_rotation = 0
    imported_object.rotation_euler[2] = object_base_rotation

    x_distance = 14
    y_distance = 14
    z_distance = 7

    # Aggiungi una camera
    camera_location = (x_distance, y_distance, z_distance)
    bpy.ops.object.camera_add(location=camera_location)
    camera = bpy.context.object
    camera.rotation_euler = bpy.context.scene.cursor.rotation_euler
    # camera.rotation_euler = camera_rotation
    bpy.context.view_layer.objects.active = camera
    bpy.ops.object.constraint_add(type='TRACK_TO')
    camera.constraints["Track To"].target = imported_object
    camera.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
    camera.constraints["Track To"].up_axis = 'UP_Y'

    bpy.ops.object.constraint_add(type='COPY_LOCATION')
    camera.constraints["Copy Location"].target = imported_object
    camera.constraints["Copy Location"].use_offset = True

    # add lights to the scene
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
    if background_image_path:
        # extract only file name
        image_filename = os.path.basename(background_image_path)
        # extract only directory to the file
        directory_path = os.path.dirname(background_image_path)

        bpy.ops.image.import_as_mesh_planes(relative=False, filepath=background_image_path, files=[{"name":image_filename, "name":image_filename}], directory=directory_path)

        bgimage = bpy.context.selected_objects[0]

        bpy.ops.object.constraint_add(type='COPY_ROTATION')
        bgimage.constraints["Copy Rotation"].target = camera
        bgimage.constraints["Copy Rotation"].use_z = True
        bgimage.constraints["Copy Rotation"].use_x = True
        bgimage.constraints["Copy Rotation"].use_y = True

        bpy.ops.object.constraint_add(type='COPY_LOCATION')
        bgimage.constraints["Copy Location"].target = camera
        bgimage.constraints["Copy Location"].use_offset = True

        # because we set the constraint with an offset we set the location offset
        bgimage.location = (-48, -47.5, -23.5)

        bgimage.scale = (65, 65, 1)
        
        # add Image for background
        bpy.ops.object.light_add(type='AREA', align='WORLD', location=(20, 20, 22.5), scale=(1, 1, 1), rotation=(degreeToEuler(-22), degreeToEuler(16), 0))
        bgimage_light_1 = bpy.context.object
        bgimage_light_1.data.energy = 9e3
        bpy.ops.object.constraint_add(type='COPY_ROTATION')
        bgimage_light_1.constraints["Copy Rotation"].target = bgimage
        bgimage_light_1.constraints["Copy Rotation"].use_z = True
        bgimage_light_1.constraints["Copy Rotation"].use_x = True
        bgimage_light_1.constraints["Copy Rotation"].use_y = True

        bpy.ops.object.constraint_add(type='COPY_LOCATION')
        bgimage_light_1.constraints["Copy Location"].target = bgimage
        bgimage_light_1.constraints["Copy Location"].use_offset = True

    # Cattura screenshot da diverse angolazioni
    for i in range(photo_count):
        angle = object_base_rotation + (i / photo_count) * 6.28319  # 360 degrees in radians
        imported_object.rotation_euler[2] = angle
     
        bpy.context.scene.render.filepath = os.path.join(output_dir, f"{stl_filename:s}-screenshot_{i:03d}.jpg")
        bpy.ops.render.render(write_still=True)

    if make_video:
        # Set the output format to FFMPEG and the codec to MPEG4
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = 'MPEG4'
        bpy.context.scene.render.filepath = os.path.join(output_dir, stl_filename + ".mp4")

        # duration in seconds
        bpy.context.scene.render.fps = 25
        frame_number = int(bpy.context.scene.render.fps * video_duration)

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

    for filename in os.listdir(source_dir):
        print(f"Processing {filename}")
        if filename.endswith(".stl") or filename.endswith(".obj"):
            stl_path = os.path.join(source_dir, filename)

            print(f"{stl_path} - Start")
            result = render_360(stl_path, rendered_dir)
            if result:
                print(f"{stl_path} - Done, moving to completed folder")
                os.rename(stl_path, os.path.join(completed_dir, filename))
            else:
                print(f"{stl_path} - Error")
            
    