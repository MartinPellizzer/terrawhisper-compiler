from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

PAGE_WIDTH, PAGE_HEIGHT = 2480, 3508

img = Image.new(mode="RGB", size=(PAGE_WIDTH, PAGE_HEIGHT), color='#ffffff')
draw = ImageDraw.Draw(img)

checklist_input_filepath = 'checklists/checklist-input.txt'
checklist_output_filepath = 'checklists/checklist-output.jpg'

def multiline(line, width=800):
    lines = []
    line_cur = ''
    for word in line.split():
        _, _, line_w, _ = font.getbbox(line_cur)
        _, _, word_w, _ = font.getbbox(word)
        if line_w + word_w < width:
            line_cur += f'{word} '
        else:
            lines.append(line_cur)
            line_cur = f'{word} '
    if line_cur.strip() != '':
        lines.append(line_cur)
    return lines

page_px = 128
y_start = 80
y_cur = y_start

with open(checklist_input_filepath) as f: lines = f.read().strip().split('\n')

# title
lines = lines[0].replace('# ', '').strip().split('<br>')
font_size = 160
font_family, font_weight = 'Lato', 'Black'
font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
font = ImageFont.truetype(font_path, font_size)
_, _, line_w, line_h = font.getbbox(lines[0])
draw.text((PAGE_WIDTH//2 - line_w//2, y_cur), lines[0], '#000000', font=font)
y_cur += font_size
_, _, line_w, line_h = font.getbbox(lines[1])
draw.text((PAGE_WIDTH//2 - line_w//2, y_cur), lines[1], '#000000', font=font)
y_cur += font_size
y_cur += 50

# subtitle
with open(checklist_input_filepath) as f: lines = f.read().strip().split('\n')
text = lines[1].replace('## ', '').strip()
font_size = 64
font_family, font_weight = 'Lato', 'Regular'
font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
font = ImageFont.truetype(font_path, font_size)
lines = multiline(text, width=1600)
for line in lines:
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((PAGE_WIDTH//2 - line_w//2, y_cur), line, '#000000', font=font)
    y_cur += font_size*1.3
y_cur += 130

# copyright
with open(checklist_input_filepath) as f: lines = f.read().strip().split('\n')
line = lines[2].replace('@ ', '').strip()
font_size = 36
font_family, font_weight = 'Lato', 'Regular'
font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
font = ImageFont.truetype(font_path, font_size)
_, _, line_w, line_h = font.getbbox(line)
x1 = PAGE_WIDTH - line_w - page_px
y1 = PAGE_HEIGHT - 80 - font_size
draw.text((x1, y1), line, '#000000', font=font)


# items
with open(checklist_input_filepath) as f: lines = f.read().strip().split('\n')

print(lines)


font_size = 36
font_family, font_weight = 'Lato', 'Regular'
font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
font = ImageFont.truetype(font_path, font_size)

checklist_px = 128
columns_gap = 128
columns_width = (PAGE_WIDTH - checklist_px*2 - columns_gap)//2

col_cur = 1
x_start = columns_gap
y_start = y_cur
x_cur = x_start
for line in lines:
    if line.strip().startswith('# '): continue
    if line.strip().startswith('## '): continue
    # if line.strip().startswith('### '): continue
    if line.strip().startswith('@ '): continue
    if line.strip().startswith('---'): continue


    py = 64
    pl = 32
    rectangle_size = 64
    cell_outline_width = 4

    font_size = 36
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    item_pl = rectangle_size + pl + 32
    
    # multiline
    if line.strip() != '': item_lines = multiline(line, columns_width-pl*2-rectangle_size-32)
    else: item_lines = ['']

    print(columns_width)
    print(item_lines)
    # empty line
    if item_lines[0] == '':
        y_cur += cell_h - cell_outline_width
        continue

    # title
    if item_lines[0].strip().startswith('### '):
        check_present = False
        item_lines[0] = item_lines[0].replace('### ', '').upper()
        title_y_off = 0
        font_size = 48
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        item_pl = pl
    else:
        check_present = True
        title_y_off = 8
        item_pl = rectangle_size + pl + 32


    # calc 
    cell_h = rectangle_size + py + font_size * (len(item_lines)-1)
    x1 = x_cur
    y1 = y_cur
    x2 = x_cur+columns_width
    y2 = y_cur+cell_h
    cell_shape = [(x1, y1), (x2, y2)]

    check_shape = [(x_cur + pl, y_cur + py/2), (x_cur + pl + rectangle_size, y_cur + rectangle_size + py/2)]

    # draw
    draw.rectangle(cell_shape, fill='#ffffff', outline='#000000', width=cell_outline_width)
    if check_present:
        draw.rectangle(check_shape, fill='#ffffff', outline='#000000', width=cell_outline_width)

    if len(item_lines) > 1: 
        for item_line_i, item_line in enumerate(item_lines):
            draw.text((x_cur + item_pl, y_cur + py/2 + font_size*item_line_i - 8), item_line, '#000000', font=font)
        y_cur -= font_size
    else:
        draw.text((x_cur + item_pl, y_cur + py/2 + title_y_off), item_lines[0], '#000000', font=font)

    y_cur += cell_h - cell_outline_width

    if y_cur > 3000:
        y_cur = y_start
        x_cur = checklist_px + columns_width + columns_gap
        col_cur += 1
        if col_cur > 2:
            break

img.show()
img.save(checklist_output_filepath)
