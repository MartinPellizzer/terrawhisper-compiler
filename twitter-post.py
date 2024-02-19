from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps





img_w, img_h = 1080, 1080
img = Image.new(mode="RGBA", size=(img_w, img_h), color='#324030')
avatar = Image.open("social-media/leen-avatar.png")

avatar.thumbnail((128, 128), Image.Resampling.LANCZOS)
img.paste(avatar, (100, 100), avatar)



draw = ImageDraw.Draw(img)

font_size = 36
font_family = "assets/fonts/playfairdisplay/arialbd.ttf"
font = ImageFont.truetype(font_family, font_size)

text = 'Leen | Herbal Healer'
draw.text((100+128+30, 128-5), text, '#e7e5e4', font=font)



font_size = 30
font_family = "assets/fonts/playfairdisplay/arial.ttf"
font = ImageFont.truetype(font_family, font_size)

text = '@healerleen'
draw.text((100+128+30, 128+30+5), text, (192, 192, 192), font=font)



text = '''
When I felt anxious, I used to:
- Journal
- Meditate
- Take deep breaths

Now, I:
- Brew valerian teas
- Inhale lavender essential oil
- Infuse holy basil in bathwater

Sometimes, the only way to alleviate anxiety is to 
fix the messed-up chemicals in your body.
'''

font_size = 36
font_family = "assets/fonts/playfairdisplay/arial.ttf"
font = ImageFont.truetype(font_family, font_size)

text = text.strip()
lines = text.split('\n')



line_h = 0
for line in lines:
    tmp_line_h = font.getbbox(line)[3]
    if line_h <= tmp_line_h: line_h = tmp_line_h

line_spacing = 1.2
for i, line in enumerate(lines):
    line = line.strip()
    line_w = font.getbbox(line)[2]
    draw.text((100, 100 + 128 + 80 + line_h*line_spacing*i), line, '#e7e5e4', font=font)


# img.show()

img = img.convert('RGB')

img.save(
    f'social-media/content/herbs-benefits-anxienty.jpg',
    format='JPEG',
    subsampling=0,
    quality=100,
)