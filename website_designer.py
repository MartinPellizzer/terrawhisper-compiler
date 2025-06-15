import json
import pygame

vault = f'/home/ubuntu/vault'
pipe = None
bg_model = None
pygame.init()

window_w = 1920
window_h = 1080

screen = pygame.display.set_mode([window_w, window_h])
font_arial_16 = pygame.font.SysFont('Arial', 16)
font_arial_64 = pygame.font.SysFont('Arial', 64)
font_header = pygame.font.SysFont('Arial', 0)

a4_w = 2480
a4_h = 3508

mouse = {
    'x': 0,
    'y': 0,
    'left_click_cur': 0,
    'left_click_old': 0,
    'right_click_cur': 0,
    'right_click_old': 0,
}

button_website_style = {
    'x': 0,
    'y': 100,
    'w': 0,
    'h': 0,
    'px': 16,
    'py': 8,
    'text': 'WEBSITE STYLE',
}

button_website_outline = {
    'x': 0,
    'y': 0,
    'w': 100,
    'h': 30,
    'px': 16,
    'py': 8,
    'text': 'WEBSITE PAGES OUTLINE',
}

header = {
    'x': 0,
    'y': 0,
    'text': 'PAGE TITLE',
}

page = {
    'x': 0,
    'y': 0,
    'w': a4_w//4,
    'h': a4_h//4,
}

section = {
    'x': 0,
    'y': 0,
    'w': a4_w//4,
    'h': 300,
}

pages = []

style = {
    'foreground_color': '#000000',
    'background_color': '#ffffff',
    'h1': '0',
    'h2': '0',
    'p': '0',
}

image_filepath = f'website-designer/test-image.jpg'
my_image = pygame.image.load(image_filepath)
my_image = pygame.transform.scale(my_image, (100, 100))

def draw_header():
    component = header
    font = font_header
    ###
    text = component['text']
    text_surface = font.render(text, False, style['foreground_color'])
    text_w = text_surface.get_width()
    text_h = text_surface.get_height()
    x = window_w//2 - page['w']//2 + component['x']
    y = window_h//2 - page['h']//2 + component['y']
    screen.blit(text_surface, (x, y))

def draw_button_website_outline():
    text = button_website_outline['text']
    text_surface = font_arial_16.render(text, False, (255, 255, 255))
    text_w = text_surface.get_width()
    text_h = text_surface.get_height()
    x = button_website_outline['x']
    y = button_website_outline['y']
    w = text_w + button_website_outline['px']*2
    h = text_h + button_website_outline['py']*2
    pygame.draw.rect(screen, '#303030', (x, y, w, h))
    screen.blit(text_surface, (x+button_website_outline['px'], y+button_website_outline['py']))

def draw_button_website_style():
    button = button_website_style
    text = button['text']
    text_surface = font_arial_16.render(text, False, '#ffffff')
    text_w = text_surface.get_width()
    text_h = text_surface.get_height()
    x = button['x']
    y = button['y']
    w = text_w + button['px']*2
    h = text_h + button['py']*2
    pygame.draw.rect(screen, '#303030', (x, y, w, h))
    screen.blit(text_surface, (x+button['px'], y+button['py']))

def draw_page():
    x = window_w//2 - page['w']//2
    y = window_h//2 - page['h']//2
    w = page['w']
    h = page['h']
    pygame.draw.rect(screen, style['background_color'], (x, y, w, h))

def draw_section():
    x = window_w//2 - page['w']//2 + section['x']
    y = window_h//2 - page['h']//2 + section['y']
    w = section['w']
    h = section['h']
    pygame.draw.rect(screen, '#cdcdcd', (x, y, w, h))

def draw_pages():
    for page_i, page in enumerate(pages):
        text = page['name']
        text_surface = font_arial_16.render(text, False, '#ffffff')
        text_w = text_surface.get_width()
        text_h = text_surface.get_height()
        screen.blit(text_surface, (100, 100+page_i*32))

def image_ai():
    import torch
    from diffusers import StableDiffusionXLPipeline
    from diffusers import StableDiffusionPipeline
    from diffusers import DPMSolverMultistepScheduler

    global pipe
    model = {
        'checkpoint_filepath': f'{vault}/stable-diffusion/checkpoints/xl/juggernautXL_juggXIByRundiffusion.safetensors',
        'lora_filepath': f'{vault}/stable-diffusion/loras/xl/pixel-art-xl-v1.1.safetensors',
        'prompt': f'''
            a wooden chair,
            minimalist,
            pixel art,
        ''',
    }
    if not pipe:
        pipe = StableDiffusionXLPipeline.from_single_file(
            model['checkpoint_filepath'], 
            torch_dtype=torch.float16, 
            use_safetensors=True, 
            variant="fp16"
        ).to('cuda')
        pipe.load_lora_weights(model['lora_filepath'])
    prompt = model['prompt']
    image = pipe(
        prompt=prompt, 
        cross_attention_kwargs={'scale': 1}, 
        width=1024, 
        height=1024, 
        num_inference_steps=20, 
        guidance_scale=7.0
    ).images[0]
    image.save(image_filepath)

def mouse_click_button_website_pages_outline():
    text = button_website_outline['text']
    text_surface = font_arial_16.render(text, False, (255, 255, 255))
    text_w = text_surface.get_width()
    text_h = text_surface.get_height()
    x1 = button_website_outline['x']
    y1 = button_website_outline['y']
    x2 = text_w + button_website_outline['px']*2
    y2 = text_h + button_website_outline['py']*2
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        from oliark_llm import llm_reply
        prompt = f'''
            Write me an outline for a website about herbalism.
            Reply only with the name of the pages.
            Reply in the following JSON format: 
            [
                {{"name": "write name of page 1 here"}}, 
                {{"name": "write name of page 2 here"}}, 
                {{"name": "write name of page 3 here"}} 
            ]
            Only reply with the JSON, don't add additional info.
        '''
        reply = llm_reply(prompt).strip()
        json_data = {}
        try: json_data = json.loads(reply)
        except: pass 
        if json_data != {}:
            lst = []
            for item in json_data:
                try: name = item['name']
                except: continue
                lst.append({
                    'name': name,
                })
        global pages
        pages = lst

def mouse_click_button_website_style():
    button = button_website_style
    text = button['text']
    text_surface = font_arial_16.render(text, False, '#ffffff')
    text_w = text_surface.get_width()
    text_h = text_surface.get_height()
    x1 = button['x']
    y1 = button['y']
    x2 = button['x'] + text_w + button['px']*2
    y2 = button['y'] + text_h + button['py']*2
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        from oliark_llm import llm_reply
        prompt = f'''
            Give me the style of a website about herbalism.
            In specific, give me the hex color code for the text elements, the background color for the html body, the size of the h1 header, the size of the h2 header, and the size of the paragraph element.
            For each element, explain why you choose that style.
            Write me the hex codes for the foreground color and background color for a website about herbalism.
            Reply in the following JSON format: 
            {{
                "foreground": "write hex code of foreground color here",
                "background": "write hex code of background color here",
                "h1": "write size in pixels of h1 header here",
                "h2": "write size in pixels of h2 header here",
                "p": "write size in pixels of paragraph  here",
            }} 
            Only reply with the JSON, don't add additional info.
        '''
        reply = llm_reply(prompt).strip()
        json_data = {}
        try: json_data = json.loads(reply)
        except: pass 
        if json_data != {}:
            foreground = json_data['foreground']
            background = json_data['background']
            h1 = int(json_data['h1'].replace('px', ''))
            h2 = json_data['h2']
            p = json_data['p']
            global style
            global font_header
            style['foreground_color'] = foreground
            style['background_color'] = background
            style['h1'] = h1
            style['h2'] = h2
            style['p'] = p
            font_header = pygame.font.SysFont('Arial', h1)
            print(style)

def mouse_pos():
    mouse['x'], mouse['y'] = pygame.mouse.get_pos()

def mouse_left():
    mouse['left_click_cur'] = pygame.mouse.get_pressed()[0]
    if mouse['left_click_cur'] == 1:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            mouse_click_button_website_pages_outline()
            mouse_click_button_website_style()
    else:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                # image_ai()
                pass

    mouse_pos()
    mouse_left()

    screen.fill('#101010')

    draw_page()
    # draw_section()

    draw_pages()
    draw_header()
    draw_button_website_outline()
    draw_button_website_style()

    # screen.blit(my_image, (0, 0))
    pygame.display.flip()

pygame.quit()
