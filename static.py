import shutil

import g
import util

css_in ='style.css'
css_out = 'website/style.css'
shutil.copy2(css_in, css_out)

font_in ='assets/fonts/comfortaa/Comfortaa-Regular.ttf'
font_out = 'website/fonts/comfortaa/Comfortaa-Regular.ttf'
util.create_folder_for_filepath(font_out)
shutil.copy2(font_in, font_out)

file_in ='assets/fonts/comfortaa/Comfortaa-Bold.ttf'
file_out = 'website/fonts/comfortaa/Comfortaa-Bold.ttf'
util.create_folder_for_filepath(file_out)
shutil.copy2(file_in, file_out)


def page_home():
    header = util.header_default()

    slug = 'index'
    template = util.file_read(f'templates/{slug}.html')
    template = template.replace('[meta_title]', 'Herbalism & Natural Healing')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    util.file_write(f'website/{slug}.html', template)

page_home()