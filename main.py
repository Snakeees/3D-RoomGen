import os
from constants import Config
from gpt_script import gpt_out
from furni_picker import picker, rand_picker
from blend_file_gen import create_blend, run_blender

def main():
    data = gpt_out('Cluttered, unmade bed, dirty laundry, dust, no organization, unwashed dishes.')
    furniture_ids = picker(data)
    for type in furniture_ids:
        id = furniture_ids[type]
        dir = Config.FUTURE_PATH + id
        bed_obj_file = os.path.join(dir, "raw_model.obj")
        bed_mtl_file = os.path.join(dir, "model.mtl")
        texture_file = os.path.join(dir, "texture.png")
        create_blend(bed_obj_file, bed_mtl_file, texture_file)
    run_blender(furniture_ids)


if __name__ == '__main__':
    main()

