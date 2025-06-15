import os

from lib import g
from lib import io

entities = io.csv_to_dict(f'database/entities/equipment.csv')

pipe = None
def pipe_init():
    import torch
    from diffusers import DiffusionPipeline
    from diffusers import StableDiffusionXLPipeline
    from diffusers import DPMSolverMultistepScheduler
    from PIL import Image, ImageFont, ImageDraw
    global pipe
    if pipe == None:
        pipe = StableDiffusionXLPipeline.from_single_file(
            g.CHECKPOINT_FILEPATH, 
            torch_dtype=torch.float16, 
            use_safetensors=True, 
            variant="fp16"
        ).to('cuda')
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

if 0:
    entity = {
        'entity_slug': 'jar',
        'entity_name_singular': 'jar',
        'entity_name_plural': 'jars',
    }

for entity in entities:
    output_filepath = f'{g.WEBSITE_FOLDERPATH}/images/equipment/{entity["entity_slug"]}.jpg'
    if os.path.exists(output_filepath):
        continue
    prompt = f'''
        {entity['entity_name_singular']},
        dried herbs,
        wooden table, 
        rustic,
        vintage apothecary,
        natural lighting,
        cozy,
        soft shadows,
        boho aesthetic,
    '''
    image_size = [1024, 1024]
    pipe_init()
    image = pipe(
        prompt=prompt, 
        negative_prompt='', 
        width=image_size[0], 
        height=image_size[1], 
        num_inference_steps=20, 
        guidance_scale=5.0
    ).images[0]
    output_filepath_tmp = f'tmp/images/{entity["entity_slug"]}.jpg'
    image.save(output_filepath_tmp, optimize=True, quality=50)
    # image.show()


