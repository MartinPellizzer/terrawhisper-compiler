import subprocess
import datetime
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps



####################################################
# IMAGE
####################################################
def gen_image_title():
    img_w = 880
    px = 130
    py = 50
    line_spacing = 1.2
    offset_fix = 0.1

    font_size = 64
    font_family = "assets/fonts/playfairdisplay/arialbd.ttf"
    font = ImageFont.truetype(font_family, font_size)
    text = 'Is Turmeric Good for Weight Loss?'.upper()
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

    img = Image.new(mode="RGB", size=(max_line_w + px, img_h + py), color='#324030')

    draw = ImageDraw.Draw(img)

    for i, line in enumerate(lines):
        line = line.strip()
        line_w = font.getbbox(line)[2]
        line_h = font.getbbox(line)[3]
        draw.text((max_line_w//2 - line_w//2 + px//2, line_h*line_spacing*i + py//2 - offset_fix - (line_h*offset_fix)), line, '#e7e5e4', font=font)

    img.save(
        f'reels/title.jpg',
        format='JPEG',
        subsampling=0,
        quality=100,
    )

gen_image_title()



####################################################
# SUBTITLES
####################################################
start_time = '00:10:48'
end_time = '00:11:22'
st_hh, st_mm, st_ss = start_time.split('.')[0].split(':')
et_hh, et_mm, et_ss = end_time.split('.')[0].split(':')

start_time_total = int(st_ss) + (int(st_mm) * 60) + (int(st_hh) * 60 * 60)
end_time_total = int(et_ss) + (int(et_mm) * 60) + (int(et_hh) * 60 * 60)

total_time = end_time_total - start_time_total

def gen_subtitles_filtered():
    with open('reels/src/subtitles.srt', 'r', encoding='utf-8') as f:
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

    with open('reels/subtitles-clipped.srt', 'w', encoding='utf-8') as f:
        for line in total_lines:
            f.write(line)

gen_subtitles_filtered()

def gen_clip():
    subprocess.call(f"ffmpeg -y \
    -ss {start_time} \
    -i reels/src/video.mp4 \
    -t {total_time} \
    -c:v libx264 -crf 23 -c:a aac -b:a 192k \
    reels/clipped.mp4", shell=True)

# -c:v libx264 -crf 23 -c:a aac -b:a 192k \
def gen_scale_crop():
    subprocess.call(f"ffmpeg -y \
    -i reels/clipped.mp4 \
    -vf \
    scale=-1:1920,crop=1080:1920 \
    reels/scaled-cropped.mp4", shell=True)

def gen_sub():
    subprocess.call("ffmpeg -y \
    -i reels/scaled-cropped.mp4 \
    -vf \"subtitles=reels/subtitles-clipped.srt:force_style='Alignment=10'\" \
    reels/sub.mp4", shell=True)

def gen_title():
    subprocess.call(f"ffmpeg -y \
    -i reels/sub.mp4 \
    -vf \"movie=reels/title.jpg [title]; [in][title] \
    overlay=main_w/2-overlay_w/2:30 [out]\" \
    reels/title.mp4", shell=True)

def gen_output():
    subprocess.call(f"ffmpeg -y \
    -i reels/title.mp4 \
    -vf drawtext=\"fontfile=assets/fonts/arial.ttf: \
    text='@healerleen': \
    fontcolor=white: \
    x=(w-text_w)/2: \
    y={1920 - 160}: \
    fontsize=36\" \
    reels/output.mp4", shell=True)

gen_clip()
# gen_scale_crop()
# gen_sub()
# gen_title()
# gen_output()

quit()

# # quit()
# i = 0

# font_size = 40
# line_spacing = 1.2
# margin_y = font_size*line_spacing

# subprocess.call(f"ffmpeg -y \
# -i reels/sub.mp4 \
# -vf drawtext=\"fontfile=assets/fonts/arial.ttf: \
# text='Is Turmeric Actually Good for': \
# fontcolor=white: \
# box=1: \
# boxcolor=black@0.8: \
# boxborderw=5: \
# x=(w-text_w)/2: \
# y={font_size*line_spacing*i + margin_y}: \
# fontsize={font_size}\" \
# reels/title-1.mp4", shell=True)
# i += 1

# subprocess.call(f"ffmpeg -y \
# -i reels/title-1.mp4 \
# -vf drawtext=\"fontfile=assets/fonts/arial.ttf: \
# text='Weight Loss? (Honest': \
# fontcolor=white: \
# box=1: \
# boxcolor=black@0.8: \
# boxborderw=5: \
# x=(w-text_w)/2: \
# y={font_size*line_spacing*i + margin_y}: \
# fontsize={font_size}\" \
# reels/title-2.mp4", shell=True)
# i += 1

# subprocess.call(f"ffmpeg -y \
# -i reels/title-2.mp4 \
# -vf drawtext=\"fontfile=assets/fonts/arial.ttf: \
# text='Answer)': \
# fontcolor=white: \
# box=1: \
# boxcolor=black@0.8: \
# boxborderw=5: \
# x=(w-text_w)/2: \
# y={font_size*line_spacing*i + margin_y}: \
# fontsize={font_size}\" \
# reels/title-3.mp4", shell=True)
# i += 1




