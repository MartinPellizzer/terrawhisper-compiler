import subprocess
import datetime
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps
import shutil
import random
import os
import sys

x = f'''
-507
1125-1140
5244
10810 reverse diabetes-2
'''

OP = 'all'
if len(sys.argv) == 2:
    OP = sys.argv[1]


CLIP_FOLDERPATH = 'C:/terrawhisper-assets/videos'
TMP_FOLDERPATH = 'C:/terrawhisper-assets/videos/tmp'
TMP_FOLDERPATH_LOCAL = 'social-media/clip/tmp'
VIDEO_NAME = '2024-01-24'

start_time = '00:06:12.000'
end_time = '00:06:39.000'

title_full = "This 1 Recipe Will \"Reset\" Your Gut Health?"
title = "This 1 Recipe Will \"Reset\" Your Gut Health?"
title_line_1 = "This 1 Recipe Will".upper()
title_line_2 = "\\\"Reset\\\" Your Gut Health?".upper()
title_line_3 = "".upper()
output_filename = 'gut-health-cabbage-soup'

# Dr. Rhonda Patrick - This is The Only Supplement that ACTUALLY Increases Lifespan
credit_lst = ['Dr. Steven Gundry']

# cuts = [
#     [start_time, 0.5],
#     ['00:05:25.500', 0.5],
#     ['00:05:30.500', 0.5],
#     [end_time, 0.5],
# ]

clip_timestamps = [
    [start_time, end_time, 0.5],
]

rand_id = VIDEO_NAME

####################################################
# IMAGE
####################################################
def gen_image_title():
    img_w = 980
    px = 130
    py = 80
    line_spacing = 1.3
    offset_fix = 0.1

    font_size = 64
    font_family = "assets/fonts/arial/ARIAL.ttf"
    font = ImageFont.truetype(font_family, font_size)
    text = title.upper()
    words = text.split(' ')

    lines = []
    curr_line = ''
    for word in words:
        curr_line_w = font.getbbox(curr_line)[2]
        word_w = font.getbbox(word)[2]
        if curr_line_w + word_w < img_w - px:
            curr_line += f'{word} '
        else:
            lines.append(curr_line)
            curr_line = f'{word} '
    lines.append(curr_line)

    max_line_w = 0
    for i, line in enumerate(lines):
        line = line.strip()
        line_w = font.getbbox(line)[2]
        line_h = font.getbbox(line)[3]
        if max_line_w < line_w: max_line_w = line_w
        # draw.text((img_w//2 - line_w//2, line_h*i), line, '#e7e5e4', font=font)

    img_h = int(line_h*(i+1)) + int((line_h*line_spacing-line_h)*i) 

    img = Image.new(mode="RGBA", size=(1080, img_h + py), color='#324030')

    draw = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        line = line.strip()
        line_w = font.getbbox(line)[2]
        line_h = font.getbbox(line)[3]
        draw.text((1080//2 - line_w//2, line_h*line_spacing*i + py//2 - offset_fix - (line_h*offset_fix)), line, '#e7e5e4', font=font)

    img.save(
        f'{CLIP_FOLDERPATH}/tmp/title.png',
        format='PNG',
        subsampling=0,
        quality=100,
    )




####################################################
# SUBTITLES
####################################################
def get_total_time(start_time, end_time):

    st_hh, st_mm, st_ss_ms = start_time.split('.')[0].split(':')
    et_hh, et_mm, et_ss_ms = end_time.split('.')[0].split(':')

    st_hh, st_mm, st_ss_ms = start_time.split(':')
    et_hh, et_mm, et_ss_ms = end_time.split(':')

    st_ms = '0'
    et_ms = '0'
    try: st_ss, st_ms = st_ss_ms.split('.')
    except: st_ss = st_ss_ms
    try: et_ss, et_ms = et_ss_ms.split('.')
    except: et_ss = et_ss_ms

    start_time_total = int(st_ss) + (int(st_mm) * 60) + (int(st_hh) * 60 * 60)
    end_time_total = int(et_ss) + (int(et_mm) * 60) + (int(et_hh) * 60 * 60)

    total_time = end_time_total - start_time_total
    total_time = f'{total_time}.{et_ms}'

    return total_time

st_hh, st_mm, st_ss_ms = start_time.split('.')[0].split(':')
et_hh, et_mm, et_ss_ms = end_time.split('.')[0].split(':')

st_hh, st_mm, st_ss_ms = start_time.split(':')
et_hh, et_mm, et_ss_ms = end_time.split(':')

st_ms = '0'
et_ms = '0'
try: st_ss, st_ms = st_ss_ms.split('.')
except: st_ss = st_ss_ms
try: et_ss, et_ms = et_ss_ms.split('.')
except: et_ss = et_ss_ms

start_time_total = int(st_ss) + (int(st_mm) * 60) + (int(st_hh) * 60 * 60)
end_time_total = int(et_ss) + (int(et_mm) * 60) + (int(et_hh) * 60 * 60)

total_time = end_time_total - start_time_total
total_time = f'{total_time}.{et_ms}'

def gen_subtitles_filtered():
    with open(f'{CLIP_FOLDERPATH}/src/{VIDEO_NAME}/sub.srt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_lines = []
    current_lines = []
    time_line = ''
    for line in lines:
        current_lines.append(line)
        if '-->' in line: time_line = line

        if line.strip() == '':
            curr_start_time = time_line.split('-->')[0].strip()
            curr_end_time = time_line.split('-->')[1].strip()
            cst_hh, cst_mm, cst_ss = curr_start_time.split(':')
            cet_hh, cet_mm, cet_ss = curr_end_time.split(':')
            cst_ss, cst_ms = cst_ss.split(',')
            cet_ss, cet_ms = cet_ss.split(',')

            curr_start_time_total = int(cst_ss) + (int(cst_mm) * 60) + (int(cst_hh) * 60 * 60)
            curr_end_time_total = int(cet_ss) + (int(cet_mm) * 60) + (int(cet_hh) * 60 * 60)

            # print(curr_start_time_total)
            # print(curr_end_time_total)
            # quit()

            new_start_time = curr_start_time_total - start_time_total
            new_end_time = curr_end_time_total - start_time_total

            m, s = divmod(new_start_time, 60)
            h, _ = divmod(m, 60)
            new_start_time_formatted = f'{h:02d}:{m:02d}:{s:02d},{cst_ms}'

            m, s = divmod(new_end_time, 60)
            h, _ = divmod(m, 60)
            new_end_time_formatted = f'{h:02d}:{m:02d}:{s:02d},{cet_ms}'

            if start_time_total <= curr_start_time_total and end_time_total >= curr_end_time_total:
                current_lines[1] = f'{new_start_time_formatted} --> {new_end_time_formatted}\n'
                for l in current_lines:
                    total_lines.append(l)
            current_lines = []

    with open(f'{TMP_FOLDERPATH}/subtitles-clipped.srt', 'w', encoding='utf-8') as f:
        for line in total_lines:
            f.write(line)



####################################################
# VIDEOS
####################################################
def gen_clip(start_time, end_time, x, y, out_filename):
    total_time = get_total_time(start_time, end_time)

    command = f"ffmpeg -y \
    -ss {start_time} \
    -i {CLIP_FOLDERPATH}/src/{VIDEO_NAME}/video.mp4 \
    -t {total_time} \
    -vf scale=-1:1920,crop=1080:1920:{x}:{y},hflip \
    -c:v libx264 -crf 23 -c:a aac -b:a 192k \
    {out_filename}"

    subprocess.call(command, shell=True)
    print(command)


def gen_sub(part='clip'):
    subprocess.call(f"ffmpeg -y \
    -i {TMP_FOLDERPATH}/image.mp4 \
    -vf \"subtitles={TMP_FOLDERPATH_LOCAL}/subtitles-clipped.srt:force_style='Alignment=2,OutlineColour=&H100000000,BorderStyle=3,Outline=1,Shadow=0,Fontsize=14,MarginV=80'\" \
    {TMP_FOLDERPATH}/sub.mp4", shell=True)


def gen_copy():
    font_size = 64
    line_spacing = 80
    font_file = 'assets/fonts/Lato/Lato-Black.ttf'
    mt = 250
    command = f"ffmpeg -y \
    -i {TMP_FOLDERPATH}/sub.mp4 \
    -vf \"[in] \
        drawtext=fontsize={font_size}:fontcolor=White: \
        fontfile='{font_file}': \
        text='{title_line_1}':x=(w-text_w)/2:y={mt}+{line_spacing*0}: \
        bordercolor=black:borderw=5 \
        , \
        drawtext=fontsize={font_size}:fontcolor=White: \
        fontfile='{font_file}': \
        text='{title_line_2}':x=(w-text_w)/2:y={mt}+{line_spacing*1}: \
        box=1:boxborderw=16:boxcolor=#22c55e \
        , \
        drawtext=fontsize={font_size}:fontcolor=White: \
        fontfile='{font_file}': \
        text='{title_line_3}':x=(w-text_w)/2:y={mt}+{line_spacing*2}: \
        bordercolor=black:borderw=5 \
        , \
        drawtext=fontsize=36:fontcolor=white: \
        fontfile='assets/fonts/Lato/Lato-Regular.ttf': \
        x=(w-text_w)/2:y={1920 - 80}: \
        text='@healerleen': \
        [out] \
        \" \
    {TMP_FOLDERPATH}/copy.mp4"
    subprocess.call(command, shell=True)




def gen_concat(in_filename_1, in_filename_2):
    subprocess.call(f"ffmpeg -y \
    -i {TMP_FOLDERPATH}/{in_filename_1}.mp4 \
    -i {TMP_FOLDERPATH}/{in_filename_2}.mp4 \
    -filter_complex concat=n=2:v=1:a=1 \
    {TMP_FOLDERPATH}/clip_full.mp4", shell=True)




# def gen_concat_2():
#     subprocess.call(f"ffmpeg -y \
#     -safe 0 -f concat -segment_time_metadata 1 \
#     -i concat.txt \
#     -vf select=concatdec_select \
#     -af aselect=concatdec_select,aresample=async=1 \
#     {TMP_FOLDERPATH}/clip_full.mp4", shell=True)
    
def gen_concat_2():
    subprocess.call(f"ffmpeg -y \
    -safe 0 -f concat -segment_time_metadata 1 \
    -i concat.txt \
    -vf select=concatdec_select \
    -af aselect=concatdec_select,aresample=async=1 \
    {TMP_FOLDERPATH}/clip_full.mp4", shell=True)


def gen_random_id():
    rand_id = ''
    for i in range(8):
        rand_id += str(random.randint(0, 9))
    return rand_id


def gen_instagram_post():
    try: os.makedirs(f'social-media/content/{rand_id}')
    except: pass
    try: os.makedirs(f'social-media/content/{rand_id}/instagram')
    except: pass
    try: os.makedirs(f'social-media/content/{rand_id}/instagram/video')
    except: pass

    shutil.copy2(f'{TMP_FOLDERPATH}/output.mp4', f'social-media/content/{rand_id}/instagram/video/{output_filename}.mp4')

    credit_txt = ', '.join(credit_lst).title()
    with open(f'social-media/content/{rand_id}/instagram/video/caption.txt', 'w', encoding='utf-8') as f:
        f.write(f'''        
{title_full.title()} What's your thought on this?

Share this post with someone who needs to see this.

Follow @healerleen for more daily content about holistic health, natural remedies, and medicinal herbs. 

Credits: {credit_txt}
'''.strip())
    

def gen_tiktok_post():
    try: os.makedirs(f'social-media/content/{rand_id}')
    except: pass
    try: os.makedirs(f'social-media/content/{rand_id}/tiktok')
    except: pass
    try: os.makedirs(f'social-media/content/{rand_id}/tiktok/video')
    except: pass

    shutil.copy2(f'{TMP_FOLDERPATH}/output.mp4', f'social-media/content/{rand_id}/tiktok/video/{output_filename}.mp4')

    credit_txt = ', '.join(credit_lst).title()
    with open(f'social-media/content/{rand_id}/tiktok/video/caption.txt', 'w', encoding='utf-8') as f:
        f.write(f'''
{title_full.title()} What's your thought on this?

Share this post with someone who needs to see this.

Follow @healerleen for more daily content about holistic health, natural remedies, and medicinal herbs. 

Credits: {credit_txt}
'''.strip())


def gen_twitter_post():
    try: os.makedirs(f'social-media/content/{rand_id}')
    except: pass
    try: os.makedirs(f'social-media/content/{rand_id}/twitter')
    except: pass
    try: os.makedirs(f'social-media/content/{rand_id}/twitter/video')
    except: pass

    shutil.copy2(f'{TMP_FOLDERPATH}/output.mp4', f'social-media/content/{rand_id}/twitter/video/{output_filename}.mp4')

    credit_txt = ', '.join(credit_lst).title()
    with open(f'social-media/content/{rand_id}/twitter/video/caption.txt', 'w', encoding='utf-8') as f:
        f.write(f'''
{title_full} 

What's your thought on this? 👇
'''.strip())


# rand_id = 0
# random.seed(datetime.datetime.now().timestamp())
# while True:
#     rand_id = gen_random_id()
#     if rand_id not in os.listdir('social-media/content/new'):
#         break

# TODO: dinamically gen concat from variable len list
if OP == 'clip':
    try: shutil.rmtree(TMP_FOLDERPATH)
    except: pass
    try: os.makedirs(TMP_FOLDERPATH)
    except: pass

    with open('concat.txt', 'w') as f: pass
    for i, timestamp in enumerate(clip_timestamps):
        filename = str(i).zfill(4)
        gen_clip(
            timestamp[0], timestamp[1], int(1920*timestamp[2]), 0, 
            f'{TMP_FOLDERPATH}/{filename}.mp4'
        )
        
        with open('concat.txt', 'a') as f: 
            f.write(f"file '{TMP_FOLDERPATH}/{filename}.mp4'\n")

    if len(clip_timestamps) != 1: 
        gen_concat_2()
    else:
        shutil.copy2(f'{TMP_FOLDERPATH}/0000.mp4', f'{TMP_FOLDERPATH}/clip_full.mp4')

else:
    pass

if OP == 'concat':
    # gen_concat('clipped-0', 'clipped-1')
    gen_concat_2()

if OP == 'sub_file':
    gen_subtitles_filtered()

if OP == 'sub_vid':
    gen_sub()

if OP == 'copy':
    gen_copy()
    shutil.copy2(f'{TMP_FOLDERPATH}/copy.mp4', f'{TMP_FOLDERPATH}/output.mp4')



if OP == 'export':
    gen_instagram_post()
    gen_tiktok_post()
    gen_twitter_post()



def add_image(input_filename, output_path):
    input_path = f'{CLIP_FOLDERPATH}/tmp/{input_filename}.mp4'
    image_1_path = f'{CLIP_FOLDERPATH}/src/{VIDEO_NAME}/images/102.png'
    image_2_path = f'{CLIP_FOLDERPATH}/src/{VIDEO_NAME}/images/104.png'
    image_3_path = f'{CLIP_FOLDERPATH}/src/{VIDEO_NAME}/images/106.png'
    command = f"ffmpeg -y \
    -i {input_path} \
    -i {image_1_path} \
    -i {image_2_path} \
    -i {image_3_path} \
    -filter_complex \
    \" \
    [1:v]scale=-1:1920[img_1], \
    [2:v]scale=-1:1920[img_2], \
    [3:v]scale=-1:1920[img_3], \
    [v:0][img_1]overlay=0:0:enable='between(t,3.502,6.630)'[v1]; \
    [v1][img_2]overlay=0:0:enable='between(t,10.587,15.587)'[v2]; \
    [v2][img_3]overlay=0:0:enable='between(t,18.000,21.717)'[v3]; \
    \" \
    -map \"[v3]\" -map 0:a \
    {TMP_FOLDERPATH}/{output_path}.mp4"
    subprocess.call(command, shell=True)
    print(command)


if OP == 'image':
    add_image('clip_full', 'image')



def zoom(input_filename, output_path):
    command = f"ffmpeg -y \
    -i {input_path} \
    -vf \
    \" \
    zoompan=z=pzoom+0.001:d=700:s=1080x1920:fps=30 \
    \" \
    {TMP_FOLDERPATH}/{output_path}.mp4"
    subprocess.call(command, shell=True)
    print(command)

if OP == 'zoom':
    add_image('clip_full', 'zoom')