import os
import time
import shutil
import markdown
import random
from PIL import Image, ImageDraw, ImageFont

import g
import util
import utils_ai
import util_image
import sitemap

images_folder = 'C:/terrawhisper-assets/images/'


c_dark = '#030712'
c_bg = '#f5f5f5'

if not os.path.exists('website/images'): os.makedirs('website/images')

conditions_rows = util.csv_get_rows('database/csv/status/conditions.csv')
conditions_cols = util.csv_get_cols(conditions_rows)
conditions_rows = conditions_rows[1:]

problems_rows = util.csv_get_rows(g.CSV_PROBLEMS_FILEPATH)
problems_cols = util.csv_get_cols(problems_rows)
problems_rows = problems_rows[1:]

conditions_rows = util.csv_get_rows(g.CSV_CONDITIONS_FILEPATH)
conditions_cols = util.csv_get_cols(conditions_rows)
conditions_rows = conditions_rows[1:]

systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_NEW_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)
systems_rows = systems_rows[1:]

herbs_rows = util.csv_get_rows(g.CSV_HERBS_FILEPATH)
herbs_cols = util.csv_get_cols(herbs_rows)
herbs_rows = herbs_rows[1:]

preparations_rows = util.csv_get_rows(g.CSV_PREPARATIONS_FILEPATH)
preparations_cols = util.csv_get_cols(preparations_rows)
preparations_rows = preparations_rows[1:]

status_rows = util.csv_get_rows(g.CSV_STATUS_FILEPATH)
status_cols = util.csv_get_cols(status_rows)
status_rows = status_rows[1:]


herbs_auto_rows = util.csv_get_rows(g.CSV_HERBS_AUTO_FILEPATH)
herbs_auto_cols = util.csv_get_cols(herbs_auto_rows)
herbs_auto_rows = herbs_auto_rows[1:]



# JUNCTIONS
problems_herbs_rows = util.csv_get_rows(g.CSV_PROBLEMS_HERBS_FILEPATH)
problems_herbs_cols = util.csv_get_cols(problems_herbs_rows)
problems_herbs_rows = problems_herbs_rows[1:]

problems_systems_rows = util.csv_get_rows(g.CSV_PROBLEMS_SYSTEMS_FILEPATH)
problems_systems_cols = util.csv_get_cols(problems_systems_rows)
problems_systems_rows = problems_systems_rows[1:]

problems_preparations_rows = util.csv_get_rows(g.CSV_PROBLEMS_PREPARATIONS_FILEPATH)
problems_preparations_cols = util.csv_get_cols(problems_preparations_rows)
problems_preparations_rows = problems_preparations_rows[1:]

problems_teas_rows = util.csv_get_rows(g.CSV_PROBLEMS_TEAS_FILEPATH)
problems_teas_cols = util.csv_get_cols(problems_teas_rows)
problems_teas_rows = problems_teas_rows[1:]

problems_tinctures_rows = util.csv_get_rows(g.CSV_PROBLEMS_TINCTURES_FILEPATH)
problems_tinctures_cols = util.csv_get_cols(problems_tinctures_rows)
problems_tinctures_rows = problems_tinctures_rows[1:]

problems_capsules_rows = util.csv_get_rows(g.CSV_PROBLEMS_CAPSULES_FILEPATH)
problems_capsules_cols = util.csv_get_cols(problems_capsules_rows)
problems_capsules_rows = problems_capsules_rows[1:]

problems_related_rows = util.csv_get_rows(g.CSV_PROBLEMS_RELATED_FILEPATH)
problems_related_cols = util.csv_get_cols(problems_related_rows)
problems_related_rows = problems_related_rows[1:]

herbs_benefits_rows = util.csv_get_rows(g.CSV_HERBS_BENEFITS_FILEPATH)
herbs_benefits_cols = util.csv_get_cols(herbs_benefits_rows)
herbs_benefits_rows = herbs_benefits_rows[1:]


status_systems_rows = util.csv_get_rows(g.CSV_STATUS_SYSTEMS_FILEPATH)
status_systems_cols = util.csv_get_cols(status_systems_rows)
status_systems_rows = status_systems_rows[1:]

problems_herbs_auto_rows = util.csv_get_rows(g.CSV_PROBLEMS_HERBS_AUTO_FILEPATH)
problems_herbs_auto_cols = util.csv_get_cols(problems_herbs_auto_rows)
problems_herbs_auto_rows = problems_herbs_auto_rows[1:]

status_herbs_rows = util.csv_get_rows(g.CSV_STATUS_HERBS_FILEPATH)
status_herbs_cols = util.csv_get_cols(status_herbs_rows)
status_herbs_rows = status_herbs_rows[1:]

herbs_names_common_rows = util.csv_get_rows(g.CSV_HERBS_NAMES_COMMON_FILEPATH)
herbs_names_common_cols = util.csv_get_cols(herbs_names_common_rows)
herbs_names_common_rows = herbs_names_common_rows[1:]


status_preparations_teas_rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_TEAS_FILEPATH)
status_preparations_teas_cols = util.csv_get_cols(status_preparations_teas_rows)
status_preparations_teas_rows = status_preparations_teas_rows[1:]

status_preparations_tinctures_rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_TINCTURES_FILEPATH)
status_preparations_tinctures_cols = util.csv_get_cols(status_preparations_tinctures_rows)
status_preparations_tinctures_rows = status_preparations_tinctures_rows[1:]

status_preparations_capsules_rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_CAPSULES_FILEPATH)
status_preparations_capsules_cols = util.csv_get_cols(status_preparations_capsules_rows)
status_preparations_capsules_rows = status_preparations_capsules_rows[1:]

status_preparations_rows = util.csv_get_rows(g.CSV_STATUS_PREPARATIONS_FILEPATH)
status_preparations_cols = util.csv_get_cols(status_preparations_rows)
status_preparations_rows = status_preparations_rows[1:]



teas_num = 10
ART_ITEMS_NUM = 10


# DEBUG

DEBUG_REMEDY_IMG_FOLDER_MISSING = 1
DEBUG_MISS_IMG_KEY_FEATURED = 0
DEBUG_MISS_IMG_KEY_LST = 0
DEBUG_MISS_REMEDY_DESC = 0
DEBUG_MISS_REMEDY_CONSTITUENTS = 0
DEBUG_MISS_REMEDY_PARTS = 0
DEBUG_MISS_REMEDY_RECIPE = 0

DEBUG_PROBLEM_NAME = 0
DEBUG_PROBLEM_SYSTEM = 0
DEBUG_PROBLEM_JSON_FILEPATH = 0
DEBUG_PROBLEM_REDIRECT = 0

DEBUG_PROBLEMS = 0
DEBUG_PLANTS = 0
DEBUG_PLANTS_MEDICINE_BENEFITS = 0

DEBUG_STATUS = 1
DEBUG_STATUS_JSON_FILEPATH = 0


# #########################################################
# CSVs
# #########################################################

def csv_get_herbs_by_problem(problem_id):
    problems_herbs_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_HERBS_FILEPATH, problems_herbs_cols['problem_id'], problem_id,
    )

    problems_herbs_ids = [
        row[problems_herbs_cols['herb_id']] 
        for row in problems_herbs_rows_filtered
        if row[problems_herbs_cols['problem_id']] == problem_id
    ]

    herbs_rows_filtered = []
    for herb_row in herbs_rows:
        herb_id = herb_row[herbs_cols['herb_id']]
        if herb_id in problems_herbs_ids:
            herbs_rows_filtered.append(herb_row)
            
    return herbs_rows_filtered


def csv_get_herbs_auto_by_status(status_id):
    status_herbs_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_STATUS_HERBS_FILEPATH, status_herbs_cols['status_id'], status_id,
    )

    status_herbs_ids = [
        row[status_herbs_cols['herb_id']] 
        for row in status_herbs_rows_filtered
        if row[status_herbs_cols['status_id']] == status_id
    ]

    herbs_auto_rows_filtered = []
    for herb_auto_row in herbs_auto_rows:
        herb_auto_id = herb_auto_row[herbs_auto_cols['herb_id']]
        if herb_auto_id in status_herbs_ids:
            herbs_auto_rows_filtered.append(herb_auto_row)
            
    return herbs_auto_rows_filtered


def csv_get_teas_by_problem(problem_id):
    problems_teas_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_TEAS_FILEPATH, problems_teas_cols['problem_id'], problem_id,
    )

    herbs_rows_filtered = []
    for problem_tea_row in problems_teas_rows_filtered:
        jun_tea_id = problem_tea_row[problems_teas_cols['tea_id']]

        for herb_row in herbs_rows:
            herb_id = herb_row[herbs_cols['herb_id']]

            if herb_id == jun_tea_id:
                herbs_rows_filtered.append(herb_row)

            
    return herbs_rows_filtered



def get_herbs_names_common_by_status(status_id, preparation_slug):
    # get rows of specific preparation for status
    status_remedies_rows_filtered = []
    if preparation_slug == 'teas':
        status_remedies_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_STATUS_PREPARATIONS_TEAS_FILEPATH, status_preparations_teas_cols['status_id'], status_id,
        )
    elif preparation_slug == 'tinctures':
        status_remedies_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_STATUS_PREPARATIONS_TINCTURES_FILEPATH, status_preparations_tinctures_cols['status_id'], status_id,
        )
    elif preparation_slug == 'capsules':
        status_remedies_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_STATUS_PREPARATIONS_CAPSULES_FILEPATH, status_preparations_capsules_cols['status_id'], status_id,
        )

    # get first column of common names table
    remedies_rows_filtered = []
    for status_remedy_row in status_remedies_rows_filtered:
        jun_remedy_id = status_remedy_row[status_preparations_teas_cols['remedy_id']]
        for herb_row in herbs_names_common_rows:
            herb_id = herb_row[herbs_cols['herb_id']]
            if herb_id == jun_remedy_id:
                remedies_rows_filtered.append(herb_row)
                break

    return remedies_rows_filtered
    


def csv_get_tinctures_by_problem(problem_id):
    problems_tinctures_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_TINCTURES_FILEPATH, problems_tinctures_cols['problem_id'], problem_id,
    )

    herbs_rows_filtered = []
    for problem_tincture_row in problems_tinctures_rows_filtered:
        jun_tincture_id = problem_tincture_row[problems_tinctures_cols['tincture_id']]

        for herb_row in herbs_rows:
            herb_id = herb_row[herbs_cols['herb_id']]

            if herb_id == jun_tincture_id:
                herbs_rows_filtered.append(herb_row)

            
    return herbs_rows_filtered


def csv_get_capsules_by_problem(problem_id):
    remedies_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_CAPSULES_FILEPATH, problems_capsules_cols['problem_id'], problem_id,
    )

    herbs_rows_filtered = []
    for remedy_row in remedies_rows_filtered:
        jun_remedy_id = remedy_row[problems_capsules_cols['capsule_id']]

        for herb_row in herbs_rows:
            herb_id = herb_row[herbs_cols['herb_id']]

            if herb_id == jun_remedy_id:
                herbs_rows_filtered.append(herb_row)

            
    return herbs_rows_filtered






def csv_get_problems_by_system(system_id):
    problems_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_SYSTEMS_FILEPATH, problems_systems_cols['system_id'], system_id,
    )

    junction_problems_ids = [
        row[problems_systems_cols['problem_id']] 
        for row in problems_systems_rows_filtered
        if row[problems_systems_cols['system_id']] == system_id
    ]

    problems_rows_filtered = []
    for problem_row in problems_rows:
        problem_id = problem_row[problems_cols['problem_id']]
        if problem_id in junction_problems_ids:
            problems_rows_filtered.append(problem_row)
        
    return problems_rows_filtered


def csv_get_status_by_system(system_id):
    status_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_STATUS_SYSTEMS_FILEPATH, status_systems_cols['system_id'], system_id,
    )

    junction_status_ids = [
        row[status_systems_cols['status_id']] 
        for row in status_systems_rows_filtered
        if row[status_systems_cols['system_id']] == system_id
    ]

    status_rows_filtered = []
    for status_row in status_rows:
        status_id = status_row[status_cols['status_id']]
        if status_id in junction_status_ids:
            status_rows_filtered.append(status_row)
        
    return status_rows_filtered


def csv_get_system_by_problem(problem_id):
    system_row = []

    problems_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_SYSTEMS_FILEPATH, problems_systems_cols['problem_id'], problem_id,
    )

    if problems_systems_rows_filtered != []:
        problem_system_row = problems_systems_rows_filtered[0]
        system_id = problem_system_row[problems_systems_cols['system_id']]

        systems_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], system_id,
        )

        if systems_rows_filtered != []:
            system_row = systems_rows_filtered[0]

    return system_row


def get_system_by_status(status_id):
    system_row = []

    status_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_STATUS_SYSTEMS_FILEPATH, status_systems_cols['status_id'], status_id,
    )

    if status_systems_rows_filtered != []:
        status_system_row = status_systems_rows_filtered[0]
        system_id = status_system_row[status_systems_cols['system_id']]

        systems_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], system_id,
        )

        if systems_rows_filtered != []:
            system_row = systems_rows_filtered[0]

    return system_row


def csv_get_preparations_by_problem(problem_id):
    problems_preparations_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_PREPARATIONS_FILEPATH, problems_preparations_cols['problem_id'], problem_id,
    )

    problems_preparations_ids = [
        row[problems_preparations_cols['preparation_id']] 
        for row in problems_preparations_rows_filtered
        if row[problems_preparations_cols['problem_id']] == problem_id
    ]

    preparations_rows_filtered = []
    for herb_row in preparations_rows:
        herb_id = herb_row[preparations_cols['preparation_id']]
        if herb_id in problems_preparations_ids:
            preparations_rows_filtered.append(herb_row)
            
    return preparations_rows_filtered


def get_preparations_by_status(status_id):
    status_preparations_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_STATUS_PREPARATIONS_FILEPATH, status_preparations_cols['status_id'], status_id,
    )

    status_preparations_ids = [
        row[status_preparations_cols['preparation_id']] 
        for row in status_preparations_rows_filtered
        if row[status_preparations_cols['status_id']] == status_id
    ]

    preparations_rows_filtered = []
    for preparation_row in preparations_rows:
        herb_id = preparation_row[preparations_cols['preparation_id']]
        if herb_id in status_preparations_ids:
            preparations_rows_filtered.append(preparation_row)
            
    return preparations_rows_filtered


def csv_get_related_by_problem(problem_id):
    problems_related_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_RELATED_FILEPATH, problems_related_cols['problem_id'], problem_id,
    )

    problems_rows_filtered = []
    for problem_related_row in problems_related_rows_filtered:
        jun_related_id = problem_related_row[problems_related_cols['related_id']]
        jun_related_name = problem_related_row[problems_related_cols['related_name']]
        for problem_row in problems_rows:
            problem_id = problem_row[problems_cols['problem_id']]
            problem_slug = problem_row[problems_cols['problem_slug']]
            problem_names = problem_row[problems_cols['problem_names']]
            if jun_related_id == problem_id:
                problems_rows_filtered.append({
                    'problem_id': problem_id, 
                    'problem_slug': problem_slug, 
                    'problem_names': problem_names, 
                    'related_name': jun_related_name, 
                })
                break
            
    return problems_rows_filtered


def csv_get_herb_common_name_by_id(herb_id):
    herb_name_common = ''
    for herb_name_common_row in herbs_names_common_rows:
        _id = herb_name_common_row[herbs_names_common_cols['herb_id']]
        _name_common = herb_name_common_row[herbs_names_common_cols['herb_name_common']]
        if _id == herb_id:
            herb_name_common = _name_common
            break
    return herb_name_common





# #########################################################
# ;IMAGES
# #########################################################

def img_preparations_cheatsheet(data):
    title = data['title']
    status_slug = data['status_slug']
    preparation_name = data['preparation_name']
    preparation_slug = preparation_name.replace(' ', '-')

    image_filepath_out = f'website/images/herbal-{preparation_slug}-for-{status_slug}-cheatsheet.jpg'
    if os.path.exists(image_filepath_out): return

    img_width = 2480
    img_height = 3508
    gap_width = img_width//10

    c_dark = '#030712'
    c_bg = '#f5f5f5'

    img = Image.new(mode="RGB", size=(img_width, img_height), color=c_bg)

    # logo = Image.open("website-new/images/terrawhisper-logo.png")
    # logo.thumbnail((256, 256), Image.Resampling.LANCZOS)
    # img.paste(logo, (gap_width, 80), logo)

    draw = ImageDraw.Draw(img)

    # draw.line((img_width//3 + gap_width//3, 0, img_width//3 + gap_width//3, img_height), fill=(255, 0, 255), width=3)
    # draw.line((img_width - img_width//3 - gap_width//3, 0, img_width - img_width//3 - gap_width//3, img_height), fill=(255, 0, 255), width=3)

    # draw.line((gap_width, 0, gap_width, img_height), fill=(255, 0, 255), width=3)
    # draw.line((img_width - gap_width, 0, img_width - gap_width, img_height), fill=(255, 0, 255), width=3)


    x = gap_width
    y = 80
    w = img_width//3 + gap_width//3 - 32
    h = 64
    col_curr = 0

    # TITLE
    px = 64
    py = 64
    text = title.title()
    font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 72)
    _, _, text_w, text_h = font.getbbox(text)
    draw.rectangle(((x, y), (x + text_w + px*2, y + text_h + py*2)), fill=c_dark)
    draw.text(
        (x + px, y + py), 
        text,
        (255, 255, 255), font=font
    )
    by_line_x = x + text_w + px*2 + 64
    rect_h = text_h + py*2
    y_start = y + text_h + py*2 + 80
    
    # text = 'by Leen Randell'
    # font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 48)
    # _, _, text_w, text_h = font.getbbox(text)
    # draw.text(
    #     (by_line_x, y + rect_h//2 - text_h//2 - 32), 
    #     text,
    #     (0, 0, 0), font=font
    # )

    # text = 'terrawhisper.com'
    # font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 48)
    # _, _, text_w, text_h = font.getbbox(text)
    # draw.text(
    #     (by_line_x, y + rect_h//2 - text_h//2 + 32), 
    #     text,
    #     (0, 0, 0), font=font
    # )

    
    text = 'by Leen Randell -- TerraWhisper.com'
    font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 48)
    draw.text(
        (x, img_height - 128), 
        text, c_dark, font=font
    )

    y = y_start

    remedies_list = data['remedies_list']
    for i, remedy_obj in enumerate(remedies_list[:10]):
        herb_name_common = remedy_obj['herb_name_common']

        if 'remedy_properties' not in remedy_obj: continue
        if 'remedy_parts' not in remedy_obj: continue

        remedy_properties = [item.split(':')[0] for item in remedy_obj['remedy_properties']]
        remedy_parts = [item.split(':')[0] for item in remedy_obj['remedy_parts']]

        random.shuffle(remedy_properties)
        random.shuffle(remedy_parts)

        remedy_properties = remedy_properties[:3]
        remedy_parts = remedy_parts[:3]


        # Calc Needed Height
        y_tmp = y

        y_tmp += h
        y_tmp += h
        for item in remedy_properties: y_tmp += h
        y_tmp += h
        for item in remedy_parts: y_tmp += h
        
        if y_tmp >= img_height:
            col_curr += 1
            if col_curr == 1:
                x = img_width//3 + gap_width//3 + 16
                y = y_start
                w = img_width - img_width//3 - gap_width//3 - 16
                h = 64
            if col_curr == 2:
                x = img_width - img_width//3 - gap_width//3 + 32
                y = y_start
                w = img_width - gap_width
                h = 64
            if col_curr == 3:
                print('ERROR: Not enough space to draw all remedies')
                break




        # Herb
        cell_herb_h = 96
        text_margin_l = 32
        text_margin_t = 20
        draw.rectangle(((x, y), (w, y + cell_herb_h)), fill=c_dark)
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 48)
        draw.text(
            (x + text_margin_l, y + text_margin_t), 
            f'{i+1}. {herb_name_common.upper()}', 
            c_bg, font=font
        )
        y += cell_herb_h

        # Properties Head
        cell_category_h = 96
        text_margin_t = 16
        # draw.rectangle(((x, y), (w, y + cell_category_h)))
        # draw.rectangle(((x, y), (w, y + cell_category_h)), fill="#adbfb9")
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 48)

        text_x, text_y, text_w, text_h = font.getbbox("Properties")
        draw.rectangle(
            (
                (x + text_margin_l + text_w + 32, y + cell_category_h//2), 
                (w, y + cell_category_h//2 + 4)
            ), 
            fill="#737373"
        )

        draw.text(
            (x + text_margin_l, y + text_margin_t), 
            'Properties', 
            c_dark, font=font
        )
        y += cell_category_h

        # Properties Vals
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 36)
        for item in remedy_properties:
            item = item.replace('properties', '')
            draw.rectangle(((x, y), (w, y + h)), fill=c_bg)
            draw.rectangle((
                (x + text_margin_l + 16, y + h//2 - 16), 
                (x + text_margin_l + 32, y + h//2)), fill=c_dark)
            draw.text(
            (x + text_margin_l + 48, y), 
                item, c_dark, font=font
            )
            y += h

        # Parts Head
        cell_category_h = 96
        text_margin_t = 16
        # draw.rectangle(((x, y), (w, y + cell_category_h)))
        # draw.rectangle(((x, y), (w, y + cell_category_h)), fill="#adbfb9")
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 48)

        text_x, text_y, text_w, text_h = font.getbbox("Plant Parts")
        draw.rectangle(
            (
                (x + text_margin_l + text_w + 32, y + cell_category_h//2), 
                (w, y + cell_category_h//2 + 4)
            ), 
            fill="#737373"
        )

        draw.text(
            (x + text_margin_l, y + text_margin_t), 
            'Plant Parts', c_dark, font=font
        )
        y += cell_category_h

        # Parts Vals
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 36)
        for item in remedy_parts:
            draw.rectangle(((x, y), (w, y + h)), fill=c_bg)
            draw.rectangle((
                (x + text_margin_l + 16, y + h//2 - 16), 
                (x + text_margin_l + 32, y + h//2)), fill=c_dark)
            draw.text(
            (x + text_margin_l + 48, y), 
                item, c_dark, font=font
            )
            y += h

        y += h

    img.thumbnail((img_width//3, img_height//3), Image.LANCZOS)
    img.save(image_filepath_out, quality=50) 
    print('SAVED CHEATSHEET:', image_filepath_out)
    # img.show()

    # quit()





# #########################################################
# ;PREPARATIONS
# #########################################################

def json_preparation_system_problem_supplementary(json_filepath, data):
    problem_id = data['problem_id']
    problem_slug = data['problem_slug']
    problem_name = data['problem_name']
    preparation_name = data['preparation_name']

    key = 'supplementary_best_treatment'
    if key not in data:
        prompt = f'''
            How to best treat {problem_name} with herbal {preparation_name}?
            Reply in a short paragraph of about 60 to 80 words.
            Start the reply with the following words: The best way to treat {problem_name} with herbal {preparation_name} is .
            Never use these words: can, may and might.
        '''
        reply = utils_ai.gen_reply(prompt)

        reply = utils_ai.reply_to_paragraphs(reply)

        print(len(reply))
        if len(reply) == 1:
            print('*******************************************')
            print(reply)
            print('*******************************************')
            data[key] = reply[0]
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)

    key = 'supplementary_causes'
    if key not in data:
        prompt = f'''
            What are the most common causes of {problem_name} that are treatable with herbal {preparation_name}?
            Reply in a short paragraph of about 60 to 80 words.
            Don't include names of herbs.
            Don't include examples of herbs.
            Start the reply with the following words: The primary causes of {problem_name} that are treatable with herbal {preparation_name} are .
            Never use these words: can, may and might.
        '''
        reply = utils_ai.gen_reply(prompt)

        reply = utils_ai.reply_to_paragraphs(reply)

        print(len(reply))
        if len(reply) == 1:
            print('*******************************************')
            print(reply)
            print('*******************************************')
            data[key] = reply[0]
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)

    key = 'supplementary_preparations'
    # if key in data: del data[key]
    if key not in data:
        prompt = f'''
            What other herbal preparations to use with herbal {preparation_name} for {problem_name}?
            Reply in a short paragraph of about 60 to 80 words.
            Don't include names of herbs.
            Start the reply with the following words: Other herbal preparations to use with {preparation_name} for {problem_name} are .
            Never use these words: can, may and might.
        '''
        reply = utils_ai.gen_reply(prompt)

        reply = utils_ai.reply_to_paragraphs(reply)

        print(len(reply))
        if len(reply) == 1:
            print('*******************************************')
            print(reply)
            print('*******************************************')
            data[key] = reply[0]
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)

    key = 'supplementary_frequency'
    if key not in data:
        prompt = f'''
            How frequently should you take herbal {preparation_name} for {problem_name}? Explain why in detail.
            Include numbers.
            Don't include names of herbs.
            Don't include side effects.
            Don't include precautions.
            Don't metions sources of informations.
            Reply in a short paragraph of about 60 to 80 words.
            Start the reply with the following words: For {problem_name}, you should take herbal {preparation_name} .
            Never use these words: can, may and might.
        '''
        reply = utils_ai.gen_reply(prompt)

        reply = utils_ai.reply_to_paragraphs(reply)

        print(len(reply))
        if len(reply) == 1:
            print('*******************************************')
            print(reply)
            print('*******************************************')
            data[key] = reply[0]
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)

    key = 'supplementary_side_effects'
    if key not in data:
        prompt = f'''
            What are the possible side effects of herbal {preparation_name} for {problem_name}?
            Reply in a short paragraph of about 60 to 80 words.
            Start the reply with the following words: The possible side effects associated with consuming herbal {preparation_name} for {problem_name} are .
            Never use these words: can, may and might.
        '''
        reply = utils_ai.gen_reply(prompt)

        reply = utils_ai.reply_to_paragraphs(reply)

        print(len(reply))
        if len(reply) == 1:
            print('*******************************************')
            print(reply)
            print('*******************************************')
            data[key] = reply[0]
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)

    # What causes bad breath?
        # and how to best treat it?
    # How effective are herbal teas in combating bad breath?
    # What are the best herbal teas for bad breath?
    # Can herbal teas replace traditional methods like brushing and flossing for combating bad breath?
        # How frequently should one drink herbal teas to see results in fighting bad breath?
        # Are there any side effects associated with consuming herbal teas for bad breath?
    # Can herbal teas interact with medications or other health conditions?
    # Are there any specific herbs to avoid for individuals with certain health conditions?
        # How long does it take to notice an improvement in bad breath after starting to drink herbal teas?
    # Can herbal teas completely eliminate bad breath or just mask it temporarily?
    # Are there any lifestyle changes or additional oral care practices that should be combined with drinking herbal teas for better results?
    # Are there any particular techniques for brewing herbal teas to maximize their effectiveness against bad breath?
    # Can children or pregnant women safely consume herbal teas for bad breath?
    # Are there any contraindications for using herbal teas for bad breath alongside dental treatments or products?
    # How do herbal teas for bad breath compare to commercial mouthwashes in terms of effectiveness and safety?
    # Are there any specific brands or varieties of herbal teas known for their efficacy in combating bad breath?
    # Can herbal teas for bad breath be used as a preventive measure, or are they only effective for treating existing bad breath?
    # Are there any scientific studies supporting the use of herbal teas for bad breath?
    #!!! Can herbal teas address underlying causes of bad breath, such as gum disease or digestive issues?
    # How should herbal teas be incorporated into a daily oral hygiene routine for optimal results in combating bad breath?


def img_preparation_systems_problems_cheatsheet(data):
    title = data['title']
    problem_slug = data['problem_slug']
    preparation_name = data['preparation_name']
    preparation_slug = preparation_name.replace(' ', '-')

    image_filepath_out = f'website/images/herbal-{preparation_slug}-for-{problem_slug}-cheatsheet.jpg'
    if os.path.exists(image_filepath_out): return

    img_width = 2480
    img_height = 3508
    gap_width = img_width//10

    c_dark = '#030712'
    c_bg = '#f5f5f5'

    img = Image.new(mode="RGB", size=(img_width, img_height), color=c_bg)

    # logo = Image.open("website-new/images/terrawhisper-logo.png")
    # logo.thumbnail((256, 256), Image.Resampling.LANCZOS)
    # img.paste(logo, (gap_width, 80), logo)

    draw = ImageDraw.Draw(img)

    # draw.line((img_width//3 + gap_width//3, 0, img_width//3 + gap_width//3, img_height), fill=(255, 0, 255), width=3)
    # draw.line((img_width - img_width//3 - gap_width//3, 0, img_width - img_width//3 - gap_width//3, img_height), fill=(255, 0, 255), width=3)

    # draw.line((gap_width, 0, gap_width, img_height), fill=(255, 0, 255), width=3)
    # draw.line((img_width - gap_width, 0, img_width - gap_width, img_height), fill=(255, 0, 255), width=3)


    x = gap_width
    y = 80
    w = img_width//3 + gap_width//3 - 32
    h = 64
    col_curr = 0

    # TITLE
    px = 64
    py = 64
    text = title.title()
    font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 72)
    _, _, text_w, text_h = font.getbbox(text)
    draw.rectangle(((x, y), (x + text_w + px*2, y + text_h + py*2)), fill=c_dark)
    draw.text(
        (x + px, y + py), 
        text,
        (255, 255, 255), font=font
    )
    by_line_x = x + text_w + px*2 + 64
    rect_h = text_h + py*2
    y_start = y + text_h + py*2 + 80
    
    # text = 'by Leen Randell'
    # font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 48)
    # _, _, text_w, text_h = font.getbbox(text)
    # draw.text(
    #     (by_line_x, y + rect_h//2 - text_h//2 - 32), 
    #     text,
    #     (0, 0, 0), font=font
    # )

    # text = 'terrawhisper.com'
    # font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 48)
    # _, _, text_w, text_h = font.getbbox(text)
    # draw.text(
    #     (by_line_x, y + rect_h//2 - text_h//2 + 32), 
    #     text,
    #     (0, 0, 0), font=font
    # )

    
    text = 'by Leen Randell -- TerraWhisper.com'
    font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 48)
    draw.text(
        (x, img_height - 128), 
        text, c_dark, font=font
    )

    y = y_start

    remedies_list = data['remedies_list']
    for i, remedy_obj in enumerate(remedies_list[:10]):
        herb_name_common = remedy_obj['herb_name_common']

        if 'remedy_properties' not in remedy_obj: continue
        if 'remedy_parts' not in remedy_obj: continue

        remedy_properties = [item.split(':')[0] for item in remedy_obj['remedy_properties']]
        remedy_parts = [item.split(':')[0] for item in remedy_obj['remedy_parts']]

        random.shuffle(remedy_properties)
        random.shuffle(remedy_parts)

        remedy_properties = remedy_properties[:3]
        remedy_parts = remedy_parts[:3]


        # Calc Needed Height
        y_tmp = y

        y_tmp += h
        y_tmp += h
        for item in remedy_properties: y_tmp += h
        y_tmp += h
        for item in remedy_parts: y_tmp += h
        
        if y_tmp >= img_height:
            col_curr += 1
            if col_curr == 1:
                x = img_width//3 + gap_width//3 + 16
                y = y_start
                w = img_width - img_width//3 - gap_width//3 - 16
                h = 64
            if col_curr == 2:
                x = img_width - img_width//3 - gap_width//3 + 32
                y = y_start
                w = img_width - gap_width
                h = 64
            if col_curr == 3:
                print('ERROR: Not enough space to draw all remedies')
                break




        # Herb
        cell_herb_h = 96
        text_margin_l = 32
        text_margin_t = 20
        draw.rectangle(((x, y), (w, y + cell_herb_h)), fill=c_dark)
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 48)
        draw.text(
            (x + text_margin_l, y + text_margin_t), 
            f'{i+1}. {herb_name_common.upper()}', 
            c_bg, font=font
        )
        y += cell_herb_h

        # Properties Head
        cell_category_h = 96
        text_margin_t = 16
        # draw.rectangle(((x, y), (w, y + cell_category_h)))
        # draw.rectangle(((x, y), (w, y + cell_category_h)), fill="#adbfb9")
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 48)

        text_x, text_y, text_w, text_h = font.getbbox("Properties")
        draw.rectangle(
            (
                (x + text_margin_l + text_w + 32, y + cell_category_h//2), 
                (w, y + cell_category_h//2 + 4)
            ), 
            fill="#737373"
        )

        draw.text(
            (x + text_margin_l, y + text_margin_t), 
            'Properties', 
            c_dark, font=font
        )
        y += cell_category_h

        # Properties Vals
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 36)
        for item in remedy_properties:
            item = item.replace('properties', '')
            draw.rectangle(((x, y), (w, y + h)), fill=c_bg)
            draw.rectangle((
                (x + text_margin_l + 16, y + h//2 - 16), 
                (x + text_margin_l + 32, y + h//2)), fill=c_dark)
            draw.text(
            (x + text_margin_l + 48, y), 
                item, c_dark, font=font
            )
            y += h

        # Parts Head
        cell_category_h = 96
        text_margin_t = 16
        # draw.rectangle(((x, y), (w, y + cell_category_h)))
        # draw.rectangle(((x, y), (w, y + cell_category_h)), fill="#adbfb9")
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 48)

        text_x, text_y, text_w, text_h = font.getbbox("Plant Parts")
        draw.rectangle(
            (
                (x + text_margin_l + text_w + 32, y + cell_category_h//2), 
                (w, y + cell_category_h//2 + 4)
            ), 
            fill="#737373"
        )

        draw.text(
            (x + text_margin_l, y + text_margin_t), 
            'Plant Parts', c_dark, font=font
        )
        y += cell_category_h

        # Parts Vals
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 36)
        for item in remedy_parts:
            draw.rectangle(((x, y), (w, y + h)), fill=c_bg)
            draw.rectangle((
                (x + text_margin_l + 16, y + h//2 - 16), 
                (x + text_margin_l + 32, y + h//2)), fill=c_dark)
            draw.text(
            (x + text_margin_l + 48, y), 
                item, c_dark, font=font
            )
            y += h

        y += h

    img.thumbnail((img_width//3, img_height//3), Image.LANCZOS)
    img.save(image_filepath_out, quality=50) 
    print('SAVED CHEATSHEET:', image_filepath_out)
    # img.show()

    # quit()


def html_preparation_system_problem_supplementary(html_filepath, data):
    problem_id = data['problem_id']
    problem_name = data['problem_name']
    problem_slug = data['problem_slug']
    system_slug = data['system_slug']
    preparation_name = data['preparation_name']
    preparation_slug = data['preparation_slug']

    article_html = ''

    key = 'supplementary_best_treatment'
    if key in data:
        article_html += f'<h2>How to best treat {problem_name} with herbal {preparation_name}?</h2>\n'
        text = data[key]
        text = text.replace(problem_name, f'<a href="/{g.CATEGORY_REMEDIES}/{system_slug}/{problem_slug}.html">{problem_name}</a>', 1)

        article_html += f'{util.text_format_1N1_html(text)}\n'

    key = 'supplementary_causes'
    if key in data:
        article_html += f'<h3>What are the most common causes of {problem_name} that are treatable with herbal {preparation_name}?</h3>\n'
        text = data[key]
        for problem_row in problems_rows[:g.ART_NUM]:
            link_problem_id = problem_row[problems_cols['problem_id']]
            link_problem_slug = problem_row[problems_cols['problem_slug']]
            link_problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()
            
            link_system_row = csv_get_system_by_problem(link_problem_id)
            link_system_slug = link_system_row[systems_cols['system_slug']]

            if link_problem_id != problem_id:
                text = text.replace(link_problem_name, f'<a href="/{g.CATEGORY_REMEDIES}/{link_system_slug}/{link_problem_slug}.html">{link_problem_name}</a>', 1)

        article_html += f'{util.text_format_1N1_html(text)}\n'

    key = 'supplementary_preparations'
    if key in data:
        article_html += f'<h3>What other herbal preparations helps with {problem_name}?</h3>\n'
        text = data[key]
        # for problem_row in problems_rows[:g.ART_NUM]:
        #     link_problem_id = problem_row[problems_cols['problem_id']]
        #     link_problem_slug = problem_row[problems_cols['problem_slug']]
        #     link_problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()
            
        #     link_system_row = csv_get_system_by_problem(link_problem_id)
        #     link_system_slug = link_system_row[systems_cols['system_slug']]

        #     if link_problem_id != problem_id:
        #         text = text.replace(link_problem_name, f'<a href="/{g.CATEGORY_REMEDIES}/{link_system_slug}/{link_problem_slug}.html">{link_problem_name}</a>', 1)

        article_html += f'{util.text_format_1N1_html(text)}\n'

    return article_html



# EXE

def remedies_systems_problems_preparations(preparation_slug):
    preparation_name = ''
    preparation_name_singular = ''

    if preparation_slug == 'teas':
        preparation_name = 'teas'
        preparation_name_singular = 'tea'
    elif preparation_slug == 'tinctures':
        preparation_name = 'tinctures'
        preparation_name_singular = 'tincture'
    elif preparation_slug == 'capsules':
        preparation_name = 'capsules'
        preparation_name_singular = 'capsule'
    preparation_slug_singular = preparation_name_singular.replace(' ', '-')

    if preparation_name == '': return
    if preparation_name_singular == '': return

    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        preparations_rows_filtered = csv_get_preparations_by_problem(problem_id)
        preparations_names = [row[preparations_cols['preparation_name']] for row in preparations_rows_filtered]

        if preparation_slug == 'teas':
            if 'infusions' not in preparations_names: continue
        elif preparation_slug == 'tinctures':
            if 'tinctures' not in preparations_names: continue
        elif preparation_slug == 'capsules':
            if 'capsules' not in preparations_names: continue

        if DEBUG_PROBLEM_NAME: print(f'> {problem_name}')

        system_row = csv_get_system_by_problem(problem_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        if DEBUG_PROBLEM_SYSTEM: print(f'  > {system_name}')

        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}/{problem_slug}/{preparation_slug}.json'
        if DEBUG_PROBLEM_JSON_FILEPATH: print(json_filepath)

        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)
        data['problem_id'] = problem_id
        data['problem_slug'] = problem_slug
        data['problem_name'] = problem_name
        data['system_id'] = system_id
        data['system_slug'] = system_slug
        data['system_name'] = system_name
        data['preparation_slug'] = preparation_slug
        data['preparation_name'] = preparation_name
        data['preparation_slug_singular'] = preparation_slug_singular
        data['preparation_name_singular'] = preparation_name_singular

        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 

        data['url'] = f'{g.CATEGORY_REMEDIES}/{system_slug}/{problem_slug}/{preparation_slug}'

        data['remedies_num'] = ART_ITEMS_NUM
        title = f'{ART_ITEMS_NUM} best herbal {preparation_name} for {problem_name}'
        data['title'] = title

        util.json_write(json_filepath, data)
        
        
        article_html = ''

        if 'title':
            article_html += f'<h1>{title}</h1>\n'

        if 'featured_img':
            src = f'/images/herbal-{preparation_slug}-for-{problem_slug}-overview.jpg'
            alt = f'herbal {preparation_name} for {problem_name} overview.jpg'
            article_html += f'<p><img src="{src}" alt="{alt}"></p>\n'

        if 'intro':
            key = 'intro_desc'
            if key not in data:
                prompt = f'''
                    Write 1 detailed paragraph on the herbal {preparation_name} for {problem_name}.
                    In the first sentence, give a detailed definition of "herbal {preparation_name} for {problem_name}", including why herbal {preparation_name} help with {problem_name}.
                    Explain how herbal {preparation_name} helps with {problem_name}.
                    Include many examples of how herbal {preparation_name} for {problem_name} improves lives.
                    Don't write the names of the herbs.
                    Don't talk about other ailments.
                    Start the reply with the following words: Herbal {preparation_name} for {problem_name} are .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply, error = utils_ai.reply_to_paragraph(reply)
                if error == '':
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply
                    util.json_write(json_filepath, data)
                else:
                    print(f'ERROR: {error}')
                    util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'{util.text_format_1N1_html(data["intro_desc"])}\n'
                
            if 'intro_cheatsheet':
                article_html += f'<p>A summary of the 10 best herbal {preparation_name} for {problem_name} is provided in the following cheatsheet.</p>\n'
                src = f'/images/herbal-{preparation_slug}-for-{problem_slug}-cheatsheet.jpg'
                alt = f'herbal {preparation_name} for {problem_name} cheatsheet.jpg'
                article_html += f'<p><img src="{src}" alt="{alt}"></p>\n'
                
            if 'intro_transition':
                article_html += f'<p>The following article describes in detail the most important {preparation_name} for {problem_name}, including medicinal properties, parts of herbs to use, and recipes for preparations.</p>\n'


        if 'remedy_list':
            key = 'remedies_list'
            if key not in data: data[key] = []
            if preparation_name == 'teas': herbs_rows_filtered = csv_get_teas_by_problem(problem_id)
            if preparation_name == 'tinctures': herbs_rows_filtered = csv_get_tinctures_by_problem(problem_id)
            if preparation_name == 'capsules': herbs_rows_filtered = csv_get_capsules_by_problem(problem_id)
            for herb_row in herbs_rows_filtered:
                herb_id = herb_row[herbs_cols['herb_id']].strip()
                herb_slug = herb_row[herbs_cols['herb_slug']].strip()
                herb_name_common = herb_row[herbs_cols['herb_name_common']].split(',')[0].strip()
                herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']].strip()
                if herb_id == '': continue
                if herb_slug == '': continue
                if herb_name_common == '': continue
                if herb_name_scientific == '': continue
                found = False
                for obj in data[key]:
                    if obj['herb_id'] == herb_id: 
                        found = True
                        break
                if not found:
                    data[key].append({
                        'herb_id': herb_id,
                        'herb_slug': herb_slug,
                        'herb_name_common': herb_name_common,
                        'herb_name_scientific': herb_name_scientific,
                    })
            util.json_write(json_filepath, data)

            for obj in data[key][:teas_num]:
                remedy_name = obj["herb_name_common"].strip().lower()
                remedy_name_scientific = obj["herb_name_common"].strip().lower()
                if preparation_name == 'teas': remedy_name = f'{remedy_name} tea'.replace(' tea tea', ' tea')
                else: remedy_name = f'{remedy_name} {preparation_name_singular}'

                key = 'remedy_desc'
                # if key in obj: del obj[key]
                if key not in obj or obj[key] == []:
                    prompt = f'''
                        Write 1 paragraph in about 60 to 80 words on why herbal {remedy_name} helps with {problem_name}.
                        Don't write about side effects and precautions.
                        Start the reply with the following words: {remedy_name.capitalize()} helps with {problem_name} because .
                    '''
                    reply = utils_ai.gen_reply(prompt)
                    reply, error = utils_ai.reply_to_paragraph(reply)
                    if error == '':
                        print('********************************')
                        print(reply)
                        print('********************************')
                        obj[key] = reply
                        util.json_write(json_filepath, data)
                    else:
                        print(f'ERROR: {error}')
                        util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                    time.sleep(g.PROMPT_DELAY_TIME)

                key = 'remedy_properties'
                # if key in obj: del obj[key]
                if key not in obj or obj[key] == []:
                    prompt = f'''
                        Write a numbered list of the 5 most important medicinal properties of {remedy_name} that help with {problem_name}.
                        For each medicinal property, explain in 1 short sentence why that property is important for {problem_name} and what active constituents give that property. 
                        Write each list element using the following format: [medicinal propertie]: [property description].
                    '''
                    reply = utils_ai.gen_reply(prompt)
                    reply, error = utils_ai.reply_to_list_column(reply)
                    if error == '':
                        print('********************************')
                        print(reply)
                        print('********************************')
                        obj[key] = reply
                        util.json_write(json_filepath, data)
                    else:
                        print(f'ERROR: {error}')
                        util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                    time.sleep(g.PROMPT_DELAY_TIME)

                key = 'remedy_parts'
                # if key in obj: del obj[key]
                if key not in obj or obj[key] == []:
                    prompt = f'''
                        Write a numbered list of the most used parts of the {remedy_name} plant that are used to make medicinal tea for {problem_name}.
                        Reply by only selecting parts from the following list:
                        - Roots
                        - Rhyzomes
                        - Stems
                        - Leaves
                        - Flowers
                        - Seeds
                        - Buds
                        - Bark
                        Never include aerial parts.
                        Never repeat the same part twice and never include similar parts.
                        Include 1 short sentence description for each of these part, explaining why that part is good for making medicinal tea for {problem_name}.
                        Write each list element using the following format: [part name]: [part description].
                    '''     
                    reply = utils_ai.gen_reply(prompt)
                    reply, error = utils_ai.reply_to_list_column(reply)
                    if error == '':
                        print('********************************')
                        print(reply)
                        print('********************************')
                        obj[key] = reply
                        util.json_write(json_filepath, data)
                    else:
                        print(f'ERROR: {error}')
                        util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                    time.sleep(g.PROMPT_DELAY_TIME)

                key = 'remedy_recipe'
                # if key in obj: del obj[key]
                if key not in obj or obj[key] == []:
                    prompt = f'''
                        Write a 5-step procedure in list format to make herbal {remedy_name} for {problem_name}.
                        Include ingredients dosages and preparations times.
                        Write only 1 sentence for each step.
                        Start each step in the list with an action verb.
                        Don't include optional steps.
                        
                    '''  
                    reply = utils_ai.gen_reply(prompt)
                    reply, error = utils_ai.reply_to_list_01(reply)
                    if error == '' and len(reply) == 5:
                        print('********************************')
                        print(reply)
                        print('********************************')
                        obj[key] = reply
                        util.json_write(json_filepath, data)
                    else:
                        print(f'ERROR: {error}')
                        util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                    time.sleep(g.PROMPT_DELAY_TIME)

        
        json_preparation_system_problem_supplementary(json_filepath, data)

        # IMG
        # img_preparation_systems_problems_featured(data)
        
        # if 'remedies_list' in data:
        #     problem_name = data['problem_name']
        #     problem_slug = data['problem_slug']
        #     preparation_name = data['preparation_name'].lower()
        #     preparation_name_singular = ''
        #     if preparation_name == 'teas': preparation_name_singular = 'tea'
        #     elif preparation_name == 'tinctures': preparation_name_singular = 'tincture'
        #     else: print(f'MISSING VALID preparation_name: {preparation_name} {problem_slug}')
        #     preparation_slug = preparation_name.replace(' ', '-')
        #     preparation_slug_singular = preparation_name_singular.replace(' ', '-')

        #     for i, obj in enumerate(data['remedies_list'][:teas_num]):
        #         herb_name_common = obj['herb_name_common'].split(',')[0].strip()
        #         herb_name_common_slug = herb_name_common.replace(' ', '-').replace("'", '-').replace(".", '')

        #         image_filepath_out = f'website/images/herbal-{preparation_slug_singular}-for-{problem_slug}-{herb_name_common_slug}.jpg'
        #         if os.path.exists(image_filepath_out): continue

        #         images_folderpath = f'C:/terrawhisper-assets/images/{preparation_slug}/{herb_name_common_slug}'
        #         if os.path.exists(images_folderpath):
        #             images_filepaths = [f'{images_folderpath}/{filename}' for filename in os.listdir(images_folderpath)] 
        #             image_filepath = random.choice(images_filepaths)
        #             if image_filepath != '':
        #                 label = f'{herb_name_common} {preparation_name_singular}\nfor {problem_name}'
        #                 util.image_label(image_filepath, image_filepath_out, label)
        #         else:
        #             if DEBUG_REMEDY_IMG_FOLDER_MISSING: print(f'IMG FOLDER MISSING: {images_folderpath}')
        # else:
        #     if DEBUG_MISS_IMG_KEY_LST: print(f'MISSING KEY remedy_list: {preparation_slug} {problem_slug}')


        img_preparation_systems_problems_cheatsheet(data)
        
        # HTML
        html_filepath = f'website/{g.CATEGORY_REMEDIES}/{system_slug}/{problem_slug}/{preparation_slug}.html'

        data = util.json_read(json_filepath)



        # list
        for i, remedy_obj in enumerate(data['remedies_list'][:teas_num]):
            herb_name_common = remedy_obj['herb_name_common']
            herb_name_common_slug = herb_name_common.replace(' ', '-').replace("'", '-').replace('.', '')
            herb_slug = remedy_obj['herb_slug']
            remedy_name_preparation = herb_name_common

            if preparation_slug == 'tea': remedy_name_preparation = f'{remedy_name_preparation} tea'.replace(' tea tea', ' tea')
            else: remedy_name_preparation = f'{remedy_name_preparation} {preparation_slug_singular}'

            article_html += f'<h2>{i+1}. {remedy_name_preparation.capitalize()}</h2>\n'
            try: article_html += f'<p>{util.text_format_1N1_html(remedy_obj["remedy_desc"])}</p>\n'
            except: 
                if DEBUG_MISS_REMEDY_DESC: print(f'MISSING REMEDY DESC: {html_filepath} >> {problem_name} >> {remedy_name_preparation}')

            # image gen
            image_filepath_src = f'website/images/herbal-{preparation_slug_singular}-for-{problem_slug}-{herb_slug}.jpg'
            image_filepath_web = f'/images/herbal-{preparation_slug_singular}-for-{problem_slug}-{herb_slug}.jpg'
            if not os.path.exists(image_filepath_src): 
                images_folderpath = f'C:/terrawhisper-assets/images/{preparation_slug}/{herb_name_common_slug}'
                if os.path.exists(images_folderpath):
                    images_filepaths = [f'{images_folderpath}/{filename}' for filename in os.listdir(images_folderpath)] 
                    image_filepath = random.choice(images_filepaths)
                    if image_filepath != '':
                        label = f'{herb_name_common} {preparation_name_singular}\nfor {problem_name}'
                        util.image_label(image_filepath, image_filepath_src, label)
                        print(image_filepath, '>>', image_filepath_src)
                else:
                    if DEBUG_REMEDY_IMG_FOLDER_MISSING: print(f'IMG FOLDER MISSING: {images_folderpath}')

            # img html
            img_alt = f'{herb_name_common} {preparation_name_singular} for {problem_name}'
            try: article_html += f'<p><img src="{image_filepath_web}" alt="{img_alt}"><p>\n'
            except: 
                if DEBUG_MISS_REMEDY_IMG: print(f'MISSING REMEDY IMAGE: {problem_name} >> {tea_image_url}')

            # html - remedy_properties 
            key = 'remedy_properties'
            if key in remedy_obj:
                constituents = remedy_obj[key]
                article_html += f'<p>The list below shows the primary active constituents in {herb_name_common} that aid with {problem_name}.</p>\n'
                article_html += '<ul>\n'
                for constituent in constituents:
                    chunk_1 = constituent.split(': ')[0]
                    chunk_2 = ': '.join(constituent.split(': ')[1:])
                    article_html += f'<li><strong>{chunk_1.capitalize()}</strong>: {chunk_2}</li>\n'
                article_html += '</ul>\n'
            else: 
                if DEBUG_MISS_REMEDY_CONSTITUENTS: print(f'MISSING REMEDY CONSTITUENTS: {problem_name} >> {herb_name_common}')

            key = 'remedy_parts'
            if key in remedy_obj:
                parts = remedy_obj[key]
                article_html += f'<p>Right below you will find a list of the most important parts of {herb_name_common} that help with {problem_name}.</p>\n'
                article_html += '<ul>\n'
                for part in parts:
                    chunk_1 = part.split(': ')[0]
                    chunk_2 = ': '.join(part.split(': ')[1:])
                    article_html += f'<li><strong>{chunk_1.capitalize()}</strong>: {chunk_2}</li>\n'
                article_html += '</ul>\n'
            else: 
                if DEBUG_MISS_REMEDY_PARTS: print(f'MISSING REMEDY PARTS: {problem_name} >> {herb_name_common}')

            key = 'remedy_recipe'
            if key in remedy_obj:
                recipe = remedy_obj[key]
                article_html += f'<p>The following recipe gives a procedure to make a basic {remedy_name_preparation} for {problem_name}.</p>\n'
                article_html += '<ol>\n'
                for step in recipe:
                    article_html += f'<li>{step}</li>\n'
                article_html += '</ol>\n'
            else: 
                if DEBUG_MISS_REMEDY_RECIPE: print(f'MISSING REMEDY RECIPE: {problem_name} >> {herb_name_common}')

                    

        # article_html += html_preparation_system_problem_list(html_filepath, data)
        article_html += html_preparation_system_problem_supplementary(html_filepath, data)

        header_html = util.header_default_dark()
        breadcrumbs_html = util.breadcrumbs(html_filepath)
        meta_html = util.article_meta(article_html, lastmod)
        article_html = util.article_toc(article_html)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                {breadcrumbs_html}
                
                <section class="article-section">
                    <div class="container">
                        {meta_html}
                        {article_html}
                    </div>
                </section>

                <footer>
                    <div class="container-lg">
                        <span>© TerraWhisper.com 2024 | All Rights Reserved
                    </div>
                </footer>
            </body>

            </html>
        '''

        util.file_write(html_filepath, html)



        # REDIRECT
        conditions_olds_rows = util.csv_get_rows('database/csv/status/conditions.csv')
        condition_old_slug_system = ''
        for condition_old_row in conditions_olds_rows[1:]:
            condition_old_slug = condition_old_row[1]
            if condition_old_slug.strip() == '': continue
            system_tmp = condition_old_slug.split('/')[0]
            slug_tmp = condition_old_slug.split('/')[1]
            if slug_tmp == problem_slug:
                condition_old_slug_system = system_tmp
                if DEBUG_PROBLEM_REDIRECT: print(system_tmp)
                if DEBUG_PROBLEM_REDIRECT: print(slug_tmp)

        html_filepath_from = f'website/herbalism/{preparation_name_singular}/{condition_old_slug_system}/{problem_slug}.html'
        html_filepath_to = f'{g.CATEGORY_REMEDIES}/{system_slug}/{problem_slug}/{preparation_slug}.html'

        if DEBUG_PROBLEM_REDIRECT: print(html_filepath_from)
        if os.path.exists(html_filepath_from):
            redirect = f'<meta http-equiv="refresh" content="0; url=https://terrawhisper.com/{html_filepath_to}">'

            html = f'''
                <!DOCTYPE html>
                <html lang="en">

                <head>
                    <meta charset="UTF-8">
                    {redirect}
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <meta name="author" content="{g.AUTHOR_NAME}">
                    <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                    <link rel="stylesheet" href="/style.css">
                    <title>{title}</title>
                    {g.GOOGLE_TAG}
                    
                </head>

                <body>
                    {header_html}
                    
                    <section class="article-section">
                        <div class="container">
                            {meta_html}
                            {article_html}
                        </div>
                    </section>

                    <footer>
                        <div class="container-lg">
                            <span>© TerraWhisper.com 2024 | All Rights Reserved
                        </div>
                    </footer>
                </body>

                </html>
            '''

            util.file_write(html_filepath_from, html)
        else:
            if DEBUG_PROBLEM_REDIRECT: print('path dont exists')


def gen_preparations(preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ').strip()

    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']]
        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip()

        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue

        if DEBUG_STATUS: print(f'> {status_name}')

        system_row = get_system_by_status(status_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        if DEBUG_STATUS: print(f'  > {system_name}')

        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}/{status_slug}/{preparation_slug}.json'
        if DEBUG_STATUS_JSON_FILEPATH: print(json_filepath)

        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)
        data['status_id'] = status_id
        data['status_slug'] = status_slug
        data['status_name'] = status_name
        data['system_id'] = system_id
        data['system_slug'] = system_slug
        data['system_name'] = system_name
        data['preparation_slug'] = preparation_slug
        data['preparation_name'] = preparation_name
        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 
        data['url'] = f'{g.CATEGORY_REMEDIES}/{system_slug}/{status_slug}/{preparation_slug}'
        data['remedies_num'] = ART_ITEMS_NUM
        title = f'{ART_ITEMS_NUM} best herbal {preparation_name} for {status_name}'
        data['title'] = title
        util.json_write(json_filepath, data)

        
        
        article_html = ''

        if 'title':
            article_html += f'<h1>{title}</h1>\n'

        if 'featured_img':
            if 'remedies_list' in data:
                obj = data['remedies_list'][0]
                herb_slug = obj['herb_slug'].split(',')[0].strip()

                image_filepath_out = f'website/images/herbal-{preparation_slug}-for-{status_slug}-overview.jpg'
                if not os.path.exists(image_filepath_out):
                    images_folderpath = f'C:/terrawhisper-assets/images/{preparation_slug}/{herb_slug}'
                    if os.path.exists(images_folderpath):
                        images_filepaths = [f'{images_folderpath}/{filename}' for filename in os.listdir(images_folderpath)] 
                        image_filepath = random.choice(images_filepaths)
                        if image_filepath != '':
                            util.image_variate(image_filepath, image_filepath_out)
                    else:
                        if DEBUG_REMEDY_IMG_FOLDER_MISSING: print(f'IMG FOLDER MISSING: {images_folderpath}')
                if os.path.exists(image_filepath_out):
                    src = f'/images/herbal-{preparation_slug}-for-{status_slug}-overview.jpg'
                    alt = f'herbal {preparation_name} for {status_name} overview'
                    article_html += f'<p><img src="{src}" alt="{alt}"></p>\n'
            else:
                if DEBUG_MISS_IMG_KEY_FEATURED: print(f'MISSING KEY "featured": {preparation_slug} {status_slug}')

        if 'intro':

            key = 'intro_desc'
            if key not in data:
                prompt = f'''
                    Write 1 short paragraph in about 60 to 80 words on the herbal {preparation_name} for {status_name}.
                    Define what "herbal {preparation_name} for {status_name}" is and why they help with {status_name}.
                    Include examples of herbal {preparation_name} that help with {status_name} and examples of how this improves lives.
                    Start the reply with the following words: Herbal {preparation_name} for {status_name} are .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply, error = utils_ai.reply_to_paragraph(reply)
                if error == '':
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply
                    util.json_write(json_filepath, data)
                else:
                    print(f'ERROR: {error}')
                    util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'{util.text_format_1N1_html(data[key])}\n'
                
            # if 'intro_cheatsheet':
            #     image_filepath_out = f'website/images/herbal-{preparation_slug}-for-{status_slug}-cheatsheet.jpg'
            #     if not os.path.exists(image_filepath_out):
            #     # if True:
            #         img_width = 2480
            #         img_height = 3508
            #         gap_width = img_width//10
            #         x = gap_width
            #         y = 80
            #         w = img_width//3 + gap_width//3 - 32
            #         h = 64
            #         col_curr = 0
            #         c_dark = '#030712'
            #         c_bg = '#f5f5f5'

            #         img = Image.new(mode="RGB", size=(img_width, img_height), color=c_bg)
            #         draw = ImageDraw.Draw(img)

            #         # TITLE
            #         px = 64
            #         py = 64
            #         text = title.title()
            #         font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 72)
            #         _, _, text_w, text_h = font.getbbox(text)
            #         draw.rectangle(((x, y), (x + text_w + px*2, y + text_h + py*2)), fill=c_dark)
            #         draw.text(
            #             (x + px, y + py), 
            #             text,
            #             (255, 255, 255), font=font
            #         )
            #         by_line_x = x + text_w + px*2 + 64
            #         rect_h = text_h + py*2
            #         y_start = y + text_h + py*2 + 80
                    
            #         # FOOTER
            #         text = 'by Leen Randell -- TerraWhisper.com'
            #         font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 48)
            #         draw.text(
            #             (x, img_height - 128), 
            #             text, c_dark, font=font
            #         )
            #         y = y_start

            #         # remedies
            #         remedies_list = data['remedies_list']
            #         for i, remedy_obj in enumerate(remedies_list[:10]):
            #             herb_name_common = remedy_obj['herb_name_common']
            #             if 'remedy_properties' not in remedy_obj: continue
            #             if 'remedy_parts' not in remedy_obj: continue
            #             remedy_properties = [item.split(':')[0] for item in remedy_obj['remedy_properties']]
            #             remedy_parts = [item.split(':')[0] for item in remedy_obj['remedy_parts']]
            #             random.shuffle(remedy_properties)
            #             random.shuffle(remedy_parts)
            #             remedy_properties = remedy_properties[:3]
            #             remedy_parts = remedy_parts[:3]

            #             # Calc Needed Height
            #             y_tmp = y
            #             y_tmp += h
            #             y_tmp += h
            #             for item in remedy_properties: y_tmp += h
            #             y_tmp += h
            #             for item in remedy_parts: y_tmp += h
                        
            #             if y_tmp >= img_height:
            #                 col_curr += 1
            #                 if col_curr == 1:
            #                     x = img_width//3 + gap_width//3 + 16
            #                     y = y_start
            #                     w = img_width - img_width//3 - gap_width//3 - 16
            #                     h = 64
            #                 if col_curr == 2:
            #                     x = img_width - img_width//3 - gap_width//3 + 32
            #                     y = y_start
            #                     w = img_width - gap_width
            #                     h = 64
            #                 if col_curr == 3:
            #                     print('ERROR: Not enough space to draw all remedies')
            #                     break

            #             # Herb
            #             cell_herb_h = 96
            #             text_margin_l = 32
            #             text_margin_t = 20
            #             draw.rectangle(((x, y), (w, y + cell_herb_h)), fill=c_dark)
            #             font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 48)
            #             draw.text(
            #                 (x + text_margin_l, y + text_margin_t), 
            #                 f'{i+1}. {herb_name_common.upper()}', 
            #                 c_bg, font=font
            #             )
            #             y += cell_herb_h

            #             # Properties Head
            #             cell_category_h = 96
            #             text_margin_t = 16
            #             font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 48)
            #             text_x, text_y, text_w, text_h = font.getbbox("Properties")
            #             draw.rectangle(
            #                 (
            #                     (x + text_margin_l + text_w + 32, y + cell_category_h//2), 
            #                     (w, y + cell_category_h//2 + 4)
            #                 ), 
            #                 fill="#737373"
            #             )
            #             draw.text(
            #                 (x + text_margin_l, y + text_margin_t), 
            #                 'Properties', 
            #                 c_dark, font=font
            #             )
            #             y += cell_category_h

            #             # Properties Vals
            #             font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 36)
            #             for item in remedy_properties:
            #                 item = item.replace('properties', '')
            #                 draw.rectangle(((x, y), (w, y + h)), fill=c_bg)
            #                 draw.rectangle((
            #                     (x + text_margin_l + 16, y + h//2 - 16), 
            #                     (x + text_margin_l + 32, y + h//2)), fill=c_dark)
            #                 draw.text(
            #                 (x + text_margin_l + 48, y), 
            #                     item, c_dark, font=font
            #                 )
            #                 y += h

            #             # Parts Head
            #             cell_category_h = 96
            #             text_margin_t = 16
            #             font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 48)
            #             text_x, text_y, text_w, text_h = font.getbbox("Plant Parts")
            #             draw.rectangle(
            #                 (
            #                     (x + text_margin_l + text_w + 32, y + cell_category_h//2), 
            #                     (w, y + cell_category_h//2 + 4)
            #                 ), 
            #                 fill="#737373"
            #             )
            #             draw.text(
            #                 (x + text_margin_l, y + text_margin_t), 
            #                 'Plant Parts', c_dark, font=font
            #             )
            #             y += cell_category_h

            #             # Parts Vals
            #             font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 36)
            #             for item in remedy_parts:
            #                 draw.rectangle(((x, y), (w, y + h)), fill=c_bg)
            #                 draw.rectangle((
            #                     (x + text_margin_l + 16, y + h//2 - 16), 
            #                     (x + text_margin_l + 32, y + h//2)), fill=c_dark)
            #                 draw.text(
            #                 (x + text_margin_l + 48, y), 
            #                     item, c_dark, font=font
            #                 )
            #                 y += h
            #             y += h

            #         img.thumbnail((img_width//3, img_height//3), Image.LANCZOS)
            #         img.save(image_filepath_out, quality=50) 
            #         print('SAVED CHEATSHEET:', image_filepath_out)
            #     if os.path.exists(image_filepath_out):
            #         article_html += f'<p>A summary of the 10 best herbal {preparation_name} for {status_name} is provided in the following cheatsheet.</p>\n'
            #         src = f'/images/herbal-{preparation_slug}-for-{status_slug}-cheatsheet.jpg'
            #         alt = f'herbal {preparation_name} for {status_name} cheatsheet.jpg'
            #         article_html += f'<p><img src="{src}" alt="{alt}"></p>\n'
                
            if 'intro_transition':
                article_html += f'<p>The following article describes in detail the most important {preparation_name} for {status_name}, including medicinal properties, parts of herbs to use, and recipes for preparations.</p>\n'

        if 'remedy_list':
            key = 'remedies_list'
            # if key in data: del data[key]
            if key not in data: data[key] = []
            herbs_rows_filtered = get_herbs_names_common_by_status(status_id, preparation_slug)
            for herb_row in herbs_rows_filtered:
                herb_id = herb_row[herbs_cols['herb_id']].strip()
                herb_slug = herb_row[herbs_cols['herb_slug']].strip()
                herb_name_common = herb_row[herbs_cols['herb_name_common']].split(',')[0].strip()
                herb_name_scientific = herb_slug.replace('-', ' ').capitalize()
                if herb_id == '': continue
                if herb_slug == '': continue
                if herb_name_common == '': continue
                if herb_name_scientific == '': continue
                found = False
                for obj in data[key]:
                    if obj['herb_id'] == herb_id: 
                        found = True
                        break
                if not found:
                    data[key].append({
                        'herb_id': herb_id,
                        'herb_slug': herb_slug,
                        'herb_name_common': herb_name_common,
                        'herb_name_scientific': herb_name_scientific,
                    })
            util.json_write(json_filepath, data)

            for i, obj in enumerate(data[key][:teas_num]):
                remedy_name_common = obj["herb_name_common"].strip().lower()
                remedy_name_scientific = obj["herb_name_common"].strip().lower()

                if preparation_name == 'teas': remedy_name_common = f'{remedy_name_common} tea'.replace(' tea tea', ' tea')
                elif preparation_name == 'tinctures': remedy_name_common = f'{remedy_name_common} tincture'
                elif preparation_name == 'capsules': remedy_name_common = f'{remedy_name_common} capsule'
                else: remedy_name_common = f'{remedy_name_common} {preparation_name_singular}'

                if 'remedy_desc':
                    key = 'remedy_desc'
                    # if key in obj: del obj[key]
                    if key not in obj:
                        prompt = f'''
                            Write 1 paragraph in about 60 to 80 words on why herbal {remedy_name} helps with {status_name}.
                            Don't write about side effects and precautions.
                            Start the reply with the following words: {remedy_name.capitalize()} helps with {status_name} because .
                        '''
                        reply = utils_ai.gen_reply(prompt)
                        reply, error = utils_ai.reply_to_paragraph(reply)
                        if error == '':
                            print('********************************')
                            print(reply)
                            print('********************************')
                            obj[key] = reply
                            util.json_write(json_filepath, data)
                        else:
                            print(f'ERROR: {error}')
                            util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                        time.sleep(g.PROMPT_DELAY_TIME)               
                    if key in obj:
                        article_html += f'<h2>{i+1}. {remedy_name_common.capitalize()}</h2>\n'
                        article_html += f'<p>{util.text_format_1N1_html(obj[key])}</p>\n'

                        
                # img
                if 'remedy_image':
                    if 'remedy_properties' in obj and 'remedy_parts' in obj:
                        image_filepath_out = f'website/images/herbal-{preparation_name}-for-{status_slug}-{remedy_name_common}.jpg'
                        image_filepath_web = f'/images/herbal-{preparation_name}-for-{status_slug}-{remedy_name_common}.jpg'
                        if not os.path.exists(image_filepath_out): 
                        # if True: 
                            util_image.template_remedy(image_filepath_out, obj, preparation_name)
                            # util_image.image_template_herbs(image_filepath_out, data)
                        article_html += f'<p><img src="{image_filepath_web}" alt="{status_slug} herbs"></p>'
                    

                if 'remedy_properties':
                    key = 'remedy_properties'
                    # if key in obj: del obj[key]
                    if key not in obj:
                        prompt = f'''
                            Write a numbered list of the 5 most important medicinal properties of {remedy_name_common} that help with {status_name}.
                            For each medicinal property, explain in 1 short sentence why that property is important for {status_name} and what active constituents give that property. 
                            Write each list element using the following format: [medicinal propertie]: [property description].
                        '''
                        reply = utils_ai.gen_reply(prompt)
                        reply, error = utils_ai.reply_to_list_column(reply)
                        if error == '':
                            print('********************************')
                            print(reply)
                            print('********************************')
                            obj[key] = reply
                            util.json_write(json_filepath, data)
                        else:
                            print(f'ERROR: {error}')
                            util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                        time.sleep(g.PROMPT_DELAY_TIME)
                    if key in obj:
                        constituents = obj[key]
                        article_html += f'<p>The list below shows the primary active constituents in {remedy_name_common} that aid with {status_name}.</p>\n'
                        article_html += '<ul>\n'
                        for constituent in constituents:
                            chunk_1 = constituent.split(': ')[0]
                            chunk_2 = ': '.join(constituent.split(': ')[1:])
                            article_html += f'<li><strong>{chunk_1.capitalize()}</strong>: {chunk_2}</li>\n'
                        article_html += '</ul>\n'


                if 'remedy_parts':
                    key = 'remedy_parts'
                    # if key in obj: del obj[key]
                    if key not in obj or obj[key] == []:
                        prompt = f'''
                            Write a numbered list of the most used parts of the {remedy_name_common} plant that are used to make medicinal tea for {status_name}.
                            Reply by only selecting parts from the following list:
                            - Roots
                            - Rhyzomes
                            - Stems
                            - Leaves
                            - Flowers
                            - Seeds
                            - Buds
                            - Bark
                            Never include aerial parts.
                            Never repeat the same part twice and never include similar parts.
                            Never include parts that are not used.
                            Include 1 short sentence description for each of these part, explaining why that part is good for making medicinal tea for {status_name}.
                            Write each list element using the following format: [part name]: [part description].
                        '''     
                        reply = utils_ai.gen_reply(prompt)
                        reply, error = utils_ai.reply_herbs_parts_to_list(reply)
                        if error == '':
                            print('********************************')
                            print(reply)
                            print('********************************')
                            obj[key] = reply
                            util.json_write(json_filepath, data)
                        else:
                            print(f'ERROR: {error}')
                            util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                        time.sleep(g.PROMPT_DELAY_TIME)
                    if key in obj:
                        items = obj[key]
                        article_html += f'<p>The list below shows the primary parts of {remedy_name_common} used to make {preparation_name} for {status_name}.</p>\n'
                        article_html += '<ul>\n'
                        for item in items:
                            chunk_1 = item.split(': ')[0]
                            chunk_2 = ': '.join(item.split(': ')[1:])
                            article_html += f'<li><strong>{chunk_1.capitalize()}</strong>: {chunk_2}</li>\n'
                        article_html += '</ul>\n'


                if 'remedy_recipe':
                    key = 'remedy_recipe'
                    # if key in obj: del obj[key]
                    if key not in obj or obj[key] == []:
                        prompt = f'''
                            Write a 5-step procedure in list format to make herbal {remedy_name_common} for {status_name}.
                            Include ingredients dosages and preparations times.
                            Write only 1 sentence for each step.
                            Start each step in the list with an action verb.
                            Don't include optional steps.
                            
                        '''  
                        reply = utils_ai.gen_reply(prompt)
                        reply, error = utils_ai.reply_to_list_01(reply)
                        if error == '' and len(reply) == 5:
                            print('********************************')
                            print(reply)
                            print('********************************')
                            obj[key] = reply
                            util.json_write(json_filepath, data)
                        else:
                            print(f'ERROR: {error}')
                            util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                        time.sleep(g.PROMPT_DELAY_TIME)
                    if key in obj:
                        recipe = obj[key]
                        article_html += f'<p>The following recipe gives a procedure to make a basic {remedy_name_common} for {status_name}.</p>\n'
                        article_html += '<ol>\n'
                        for step in recipe:
                            article_html += f'<li>{step}</li>\n'
                        article_html += '</ol>\n'

        html_filepath = f'website/{g.CATEGORY_REMEDIES}/{system_slug}/{status_slug}/{preparation_slug}.html'

        header_html = util.header_default_dark()
        breadcrumbs_html = util.breadcrumbs(html_filepath)
        meta_html = util.article_meta(article_html, lastmod)
        article_html = util.article_toc(article_html)
        footer_html = util.footer()

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                {breadcrumbs_html}
                
                <section class="article-section">
                    <div class="container">
                        {meta_html}
                        {article_html}
                    </div>
                </section>

                {footer_html}
            </body>

            </html>
        '''

        util.file_write(html_filepath, html)

        # quit()



def demo_gen_preparations_image(image_filepath_out, preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ').strip()

    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']]
        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip()

        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue

        if DEBUG_STATUS: print(f'> {status_name}')

        system_row = get_system_by_status(status_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        if DEBUG_STATUS: print(f'  > {system_name}')

        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}/{status_slug}/{preparation_slug}.json'
        if DEBUG_STATUS_JSON_FILEPATH: print(json_filepath)

        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)

        # img
        key = 'remedies_list'
        if key in data:
            util_image.template_remedy(data[key][0])
        print('done')

        quit()
        
    


# #########################################################
# ;REMEDIES
# #########################################################

def remedies_systems_problems():
    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        if DEBUG_PROBLEMS: print(f'>> {problem_id} - {problem_name}')
        
        system_row = csv_get_system_by_problem(problem_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        if DEBUG_PROBLEMS: print(f'    {system_id} - {system_name}')



        # init
        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}/{problem_slug}.json'
        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)
        data['problem_id'] = problem_id
        data['problem_slug'] = problem_slug
        data['problem_name'] = problem_name
        data['system_id'] = system_id
        data['system_slug'] = system_slug
        data['system_name'] = system_name
        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 
        title = f'What to know about {problem_name} before treating it with medicinal herbs'
        data['title'] = title
        util.json_write(json_filepath, data)



        article_html = ''

        if 'title':
            article_html += f'<h1>{title}</h1>\n'

        if 'featured_image':
            image_filepath_out = f'website/images/{problem_slug}-overview.jpg'
            image_filepath_web = f'/images/{problem_slug}-overview.jpg'
            if not os.path.exists(image_filepath_out): 
            # if True: 
                img_w, img_h = 768, 512
                p_x = 48
                font_size = img_w//12
                img = Image.new(mode="RGB", size=(img_w, img_h), color=c_dark)
                draw = ImageDraw.Draw(img)

                text = problem_name.upper()
                font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)
                line_width_max = img_w - p_x

                lines = util_image.text_to_lines(text, font, line_width_max) 

                text_height_total = 0
                for i, line in enumerate(lines):
                    _, _, text_w, text_h = font.getbbox(line)
                    text_height_total += text_h

                line_h = 1.3
                for i, line in enumerate(lines):
                    _, _, text_w, text_h = font.getbbox(line)
                    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 + (i*text_h*line_h) - text_height_total//4), line, '#ffffff', font=font)
                img.save(image_filepath_out, quality=50) 
            article_html += f'<p><img src="{image_filepath_web}" alt="{problem_name} overview"></p>'

        if 'intro':
            key = 'intro_desc'
            if key not in data:
                prompt = f'''
                    Write 1 paragraph about the best herbs for {problem_name}.
                    Include a brief definition of: {problem_name}.
                    Include the negative impacts of {problem_name} in people lives. 
                    Include the causes of {problem_name}. 
                    Include the medicinal herbs and their preparations for {problem_name}. 
                    Include the precautions when using herbs medicinally for {problem_name}. 
                    
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_paragraphs(reply)
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'{util.text_format_1N1_html(data[key])}\n'
                article_html += f'<p>This article explains in detail what {problem_name} is, how it affects your life and what are its causes. Then, it lists what medicinal herbs to use to relieve this problem and how to prepare these herbs to get the best results. Lastly, it revals what other natural remedies to use in conjunction with herbal medicine to aid with this problem.</p>\n'

        if 'definition':
            key = 'definition'
            if key not in data:
                prompt = f'''
                    Write 1 paragraph explaining what is {problem_name} and include many examples on how it affects negatively your life.
                    Don't mention the casuses of {problem_name}.
                    
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_paragraphs(reply)
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What is {problem_name} and how it affects your life?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'
        
        if 'causes':
            key = 'causes_desc'
            if key not in data:
                prompt = f'''
                    Write 1 paragraph explaining what are the main causes of {problem_name}.
                    Start the reply with the following words: The main causes of {problem_name} are .
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    if line[0].isdigit(): continue
                    if ':' in line: continue
                    lines_formatted.append(line)
                if len(lines_formatted) == 1:
                    print('***************************************')
                    print(lines_formatted[0])
                    print('***************************************')
                    data[key] = lines_formatted[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What are the main causes of {problem_name}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data["causes_desc"])}\n'

            # img
            key = 'causes_list'
            if key in data:
                image_filepath_out = f'website/images/{problem_slug}-causes.jpg'
                image_filepath_web = f'/images/{problem_slug}-causes.jpg'
                if not os.path.exists(image_filepath_out): 
                # if True: 
                    util_image.image_template_causes(image_filepath_out, data)
                article_html += f'<p><img src="{image_filepath_web}" alt="{problem_name} causes"></p>'

            key = 'causes_list'
            if key not in data:
                causes_num = 10
                prompt = f'''
                    Write a numbered list of the {causes_num} most common causes of {problem_name}.
                    Include a short description for each cause.
                    Reply with the following format: [cause name]: [description]. 
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    line = line.replace('*', '')
                    line = line.replace('[', '')
                    line = line.replace(']', '')
                    if not line[0].isdigit(): continue
                    if '.' not in line: continue
                    if ':' not in line: continue
                    line = '.'.join(line.split('.')[1:])
                    line = line.strip()
                    if line == '': continue
                    lines_formatted.append(line)
                if len(lines_formatted) == causes_num:
                    print('***************************************')
                    print(lines_formatted)
                    print('***************************************')
                    data[key] = lines_formatted
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<p>The most common causes of {problem_name} are listed below.</p>\n'
                article_html += f'<ul>\n'
                for item in data['causes_list']:
                    chunks = item.split(':')
                    chunk_1 = f'<strong>{chunks[0]}</strong>\n'
                    chunk_2 = ':'.join(chunks[1:])
                    article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
                article_html += f'</ul>\n'

        if 'herbs':
            key = 'herbs_desc'
            if key not in data:
                herbs_rows_filtered = csv_get_herbs_by_problem(problem_id)
                herbs_common_names = [row[herbs_cols['herb_name_common']] for row in herbs_rows_filtered]
                herbs_common_names_prompt = ', '.join(herbs_common_names[:5])
                prompt = f'''
                    Write 1 paragraph explaining what medicinal herbs helps with {problem_name} and why.
                    Include some of the following herbs: {herbs_common_names_prompt}.
                    Start the reply with the following words: The best medicinal herbs for {problem_name} are .
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    if line[0].isdigit(): continue
                    if ':' in line: continue
                    lines_formatted.append(line)
                if len(lines_formatted) == 1:
                    print('***************************************')
                    print(lines_formatted[0])
                    print('***************************************')
                    data[key] = lines_formatted[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What are the best medicinal herbs for {problem_name}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            # img
            key = 'herbs_list'
            if key in data:
                image_filepath_out = f'website/images/{problem_slug}-herbs.jpg'
                image_filepath_web = f'/images/{problem_slug}-herbs.jpg'
                if not os.path.exists(image_filepath_out): 
                # if True: 
                    util_image.image_template_herbs(image_filepath_out, data)
                article_html += f'<p><img src="{image_filepath_web}" alt="{problem_name} herbs"></p>'
            
            key = 'herbs_list'
            if key not in data:
                herbs_num = 10
                herbs_rows_filtered = csv_get_herbs_by_problem(problem_id)
                herbs_common_names = [row[herbs_cols['herb_name_common']] for row in herbs_rows_filtered]
                herbs_common_names_prompt = ''
                for i, herb_common_name in enumerate(herbs_common_names[:herbs_num]):
                    herbs_common_names_prompt += f'{i+1}. {herb_common_name.capitalize()}\n'

                prompt = f'''
                    Here is a list of medicinal herbs for {problem_name}:
                    {herbs_common_names_prompt}

                    For each medicinal herb in the list above, explain in 1 sentence why that herb helps with {problem_name}.
                    Reply with a numbered list using the following format: [herb name]: [description].
                    
                '''
                reply = utils_ai.gen_reply(prompt)

                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    line = line.replace('*', '')
                    line = line.replace('[', '')
                    line = line.replace(']', '')
                    if not line[0].isdigit(): continue
                    if '.' not in line: continue
                    if ':' not in line: continue
                    line = '.'.join(line.split('.')[1:])
                    line = line.strip()
                    if line == '': continue
                    lines_formatted.append(line)

                if len(lines_formatted) == herbs_num:
                    print('***************************************')
                    print(lines_formatted)
                    print('***************************************')
                    data[key] = lines_formatted
                    util.json_write(json_filepath, data)

                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<p>The most effective medicinal herbs that help with {problem_name} are listed below.</p>\n'
                article_html += f'<ul>\n'
                for item in data[key]:
                    chunks = item.split(':')
                    chunk_1 = chunks[0]
                    chunk_2 = ':'.join(chunks[1:])
                    herb_row_found = []
                    for herb_row in herbs_rows:
                        if chunk_1.lower().strip() in herb_row[herbs_cols['herb_name_common']]:
                            herb_row_found = herb_row
                    if herb_row_found != []:
                        herb_slug = herb_row_found[herbs_cols['herb_slug']]
                        herb_name_scientific = herb_row_found[herbs_cols['herb_name_scientific']]
                        if os.path.exists(f'website/herbs/{herb_slug}.html'):
                            chunk_1 = f'<strong><a href="/herbs/{herb_slug}.html">{chunk_1}</a></strong>'
                        else:
                            chunk_1 = f'<strong>{chunk_1}</strong>'
                    article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
                article_html += f'</ul>\n'

        if 'preparations':
            key = 'preparations_desc'
            if key not in data:
                preparations_rows_filtered = csv_get_preparations_by_problem(problem_id)
                preparations_names = [row[preparations_cols['preparation_name']] for row in preparations_rows_filtered]
                preparations_names_prompt = ', '.join(preparations_names[:5])
                prompt = f'''
                    Write 1 paragraph about the what are the best types of herbal preparations for {problem_name}.
                    Include the following types of herbal preparations: {preparations_names_prompt}.
                    Explain why each preparation helps with {problem_name}.
                    Don't include names of herbs.
                    Don't include definitions for the preparations.
                    Don't include how to make the preparations.
                    Start the reply with the following words: The most effective herbal preparations for {problem_name} are .
                    
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    if line[0].isdigit(): continue
                    if ':' in line: continue
                    lines_formatted.append(line)
                if len(lines_formatted) == 1:
                    print('***************************************')
                    print(lines_formatted[0])
                    print('***************************************')
                    data[key] = lines_formatted[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What are the most effective herbal preparations for {problem_name}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'


            # img
            key = 'preparations_list'
            if key in data:
                image_filepath_out = f'website/images/{problem_slug}-preparations.jpg'
                image_filepath_web = f'/images/{problem_slug}-preparations.jpg'
                # if not os.path.exists(image_filepath_out): 
                if True: 
                    util_image.image_template_preparations(image_filepath_out, data)
                article_html += f'<p><img src="{image_filepath_web}" alt="{problem_name} herbs"></p>'
            

            key = 'preparations_list'
            if key not in data:
                preparations_rows_filtered = csv_get_preparations_by_problem(problem_id)
                preparations_names = [row[preparations_cols['preparation_name']] for row in preparations_rows_filtered]
                preparations_names_prompt = ''
                for i, preparation_name in enumerate(preparations_names[:10]):
                    preparations_names_prompt += f'{i+1}. {preparation_name.capitalize()}\n'
                prompt = f'''
                    Here is a list of the types of herbal preparations for {problem_name}:
                    {preparations_names_prompt}
                    For each type of herbal preparation in the list above, explain in 1 detailed sentence how and why that preparation helps with {problem_name}.
                    Don't include names of herbs.
                    Don't include definitions for the preparations.
                    Don't explain the making process of the preparations.
                    Reply with a numbered list using the following format: [preparation name]: [description].
                    
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    line = line.replace('*', '')
                    line = line.replace('[', '')
                    line = line.replace(']', '')
                    if not line[0].isdigit(): continue
                    if '.' not in line: continue
                    if ':' not in line: continue
                    line = '.'.join(line.split('.')[1:])
                    line = line.strip()
                    if line == '': continue
                    lines_formatted.append(line)
                if len(lines_formatted) >= 4:
                    print('***************************************')
                    print(lines_formatted)
                    print('***************************************')
                    data[key] = lines_formatted
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<p>The most used herbal preparations that help with {problem_name} are listed below.</p>\n'
                article_html += f'<ul>\n'
                for item in data['preparations_list']:
                    chunks = item.split(':')
                    chunk_1 = chunks[0]
                    chunk_2 = ':'.join(chunks[1:])
                    if chunk_1.lower().strip() == 'infusions':
                        chunk_1 = f'<strong><a href="/remedies/{system_slug}/{problem_slug}/teas.html">{chunk_1}</a></strong>'
                    elif chunk_1.lower().strip() == 'tinctures':
                        chunk_1 = f'<strong><a href="/remedies/{system_slug}/{problem_slug}/tinctures.html">{chunk_1}</a></strong>'
                    elif chunk_1.lower().strip() == 'capsules':
                        chunk_1 = f'<strong><a href="/remedies/{system_slug}/{problem_slug}/capsules.html">{chunk_1}</a></strong>'
                    else:
                        chunk_1 = f'<strong>{chunk_1}</strong>'
                    article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
                article_html += f'</ul>\n'

        if 'precautions':
            key = 'precautions_desc'
            if key not in data:
                prompt = f'''
                    Write 1 paragraph about the precautions to take when using herbal remedies for {problem_name}.
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What precautions to take when using herbal remedies for {problem_name}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            key = 'precautions_list'
            if key not in data:
                prompt = f'''
                    Write a numbered list of precautions to take when using herbal remedies for {problem_name}.
                    Start each precaution with an action verb.
                    Don't use the character ":".
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    line = line.replace('*', '')
                    line = line.replace('[', '')
                    line = line.replace(']', '')
                    if not line[0].isdigit(): continue
                    if '.' not in line: continue
                    if ':' in line: continue
                    line = '.'.join(line.split('.')[1:])
                    line = line.strip()
                    if line == '': continue
                    lines_formatted.append(line)
                print(len(lines_formatted))
                if len(lines_formatted) >= 4:
                    print('***************************************')
                    print(lines_formatted)
                    print('***************************************')
                    data[key] = lines_formatted
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<p>The most important precautions to take when using herbal remedies for {problem_name} are listed below.</p>\n'
                article_html += f'<ul>\n'
                for item in data['precautions_list']:
                    article_html += f'<li>{item}</li>\n'
                article_html += f'</ul>\n'
        
        if 'other_remedies':
            key = 'other_remedies_desc'
            if key not in data:
                prompt = f'''
                    Write 1 paragraph about the natural remedies for {problem_name}, without including herbal remedies.
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What natural remedies to use with medicinal herbs for {problem_name}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            key = 'other_remedies_list'
            if key not in data:
                items_num = 10
                prompt = f'''
                    Write a numbered list of the {items_num} most effective natural remedies for {problem_name}, without including herbal remedies.
                    Start each natural remedy with an action verb.
                    Each list item must have the following format: [natural remedy]: [description].
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    line = line.replace('*', '')
                    line = line.replace('[', '')
                    line = line.replace(']', '')
                    if not line[0].isdigit(): continue
                    if '.' not in line: continue
                    if ':' not in line: continue
                    line = '.'.join(line.split('.')[1:])
                    line = line.strip()
                    if line == '': continue
                    lines_formatted.append(line)
                if len(lines_formatted) == items_num:
                    print('***************************************')
                    print(lines_formatted)
                    print('***************************************')
                    data[key] = lines_formatted
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<p>The most effective natural remedies to use in conjunction with herbal medicine that help with {problem_name} are listed below.</p>\n'
                article_html += f'<ul>\n'
                for item in data['other_remedies_list']:
                    chunks = item.split(':')
                    chunk_1 = f'<strong>{chunks[0]}</strong>\n'
                    chunk_2 = ':'.join(chunks[1:])
                    article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
                article_html += f'</ul>\n'

        # html
        html_filepath = f'website/{g.CATEGORY_REMEDIES}/{system_slug}/{problem_slug}.html'

        header_html = util.header_default_dark()
        breadcrumbs_html = util.breadcrumbs(html_filepath)
        meta_html = util.article_meta(article_html, lastmod)
        article_html = util.article_toc(article_html)
        footer_html = util.footer()

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                {breadcrumbs_html}
                
                <section class="article-section">
                    <div class="container">
                        {meta_html}
                        {article_html}
                    </div>
                </section>

                {footer_html}
            </body>

            </html>
        '''

        util.file_write(html_filepath, html)


def remedies_systems():
    for system_row in systems_rows:
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        problems_rows_filtered = csv_get_problems_by_system(system_id)
        problems_num = len(problems_rows_filtered)

        if problems_num == 0: continue

        json_filepath = f'database/json/remedies/{system_slug}.json'

        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)

        data['url'] = system_slug

        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 

        title = f'{system_name.title()} Ailments To Heal With Herbal Remedies'
        data['title'] = title

        util.json_write(json_filepath, data)

        category_title = f'<h1>{title}</h1>'
        category_intro = f'<p></p>'

        content_html = ''
        for problem_row in problems_rows_filtered:
            problem_slug = problem_row[problems_cols['problem_slug']]
            problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

            src = f'/images/{problem_slug}-overview.jpg'
            alt = f'{problem_name} overview'

            json_filepath = f'database/json/remedies/{system_slug}/{problem_slug}.json'
            if os.path.exists(json_filepath):
                data = util.json_read(json_filepath)

                intro_desc_clip = ' '.join(data['intro_desc'].split(' ')[:16]).strip() + '...'
                content_html += f'''
                    <a href="/remedies/{system_slug}/{problem_slug}.html">
                        <div>
                            <img src="{src}" alt="{alt}">
                            <h2>{problem_name.title()}: Causes, Herbal Remedies, and More</h2>
                            <p>{intro_desc_clip}</p>
                        </div>
                    </a>
                '''
    
        page_url = f'remedies/{system_slug}'
        article_filepath_out = f'website/{page_url}.html'

        header = util.header_default_dark()
        breadcrumbs_html = util.breadcrumbs(article_filepath_out)
        
        template = util.file_read('templates/category.html')

        template = template.replace('[title]', f'Herbal Remedies For {system_name.title()} Ailments')
        template = template.replace('[google_tag]', g.GOOGLE_TAG)
        template = template.replace('[author_name]', g.AUTHOR_NAME)
        template = template.replace('[header]', header)
        template = template.replace('[breadcrumbs]', breadcrumbs_html)
        template = template.replace('[category_title]', category_title)
        template = template.replace('[category_intro]', category_intro)
        template = template.replace('[content]', content_html)

        util.file_write(article_filepath_out, template)


def remedies():
    title = f'Herbal Remedies Organized By Body Systems'
    category_title = f'<h1>{title}</h1>'
    category_intro = ''

    content_html = ''
    for system_row in systems_rows:
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]
        
        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        json_filepath = f'database/json/remedies/{system_slug}.json'
        if os.path.exists(json_filepath):
            # featured image
            image_filepath_out = f'website/images/{system_slug}-overview.jpg'
            image_filepath_src = f'/images/{system_slug}-overview.jpg'
            image_filepath_alt = f'{system_name} overview'
            # if not os.path.exists(image_filepath_out): 
            if True: 
                img_w, img_h = 768, 512
                p_x = 48
                font_size = img_w // 12

                img = Image.new(mode="RGB", size=(img_w, img_h), color=c_dark)
                draw = ImageDraw.Draw(img)

                text = system_name.upper()
                font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)

                words = text.split()
                lines = words

                text_height_total = 0
                for i, line in enumerate(lines):
                    _, _, text_w, text_h = font.getbbox(line)
                    text_height_total += text_h

                line_h = 1.3
                for i, line in enumerate(lines):
                    _, _, text_w, text_h = font.getbbox(line)
                    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 + (i*text_h*line_h) - text_height_total//4), line, '#ffffff', font=font)
                img.save(image_filepath_out, quality=50) 

            data = util.json_read(json_filepath)
            if 'intro_desc' in data:
                intro_desc_clip = data['intro_desc'][:100]
                intro_desc_clip = ' '.join(data['intro_desc'].split(' ')[:16]).strip() + '...'
            else: 
                intro_desc_clip = ''
                
            content_html += f'''
                <a href="/remedies/{system_slug}.html">
                    <div>
                        <img src="{image_filepath_src}" alt="{image_filepath_alt}">
                        <h2>Herbal Remedies for the {system_name.title()}</h2>
                        <p>{intro_desc_clip}</p>
                    </div>
                </a>
            '''
    
    page_url = f'remedies'
    article_filepath_out = f'website/{page_url}.html'

    header = util.header_default_dark()
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)
    
    template = util.file_read('templates/category.html')

    template = template.replace('[title]', title)
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[category_title]', category_title)
    template = template.replace('[category_intro]', category_intro)
    template = template.replace('[content]', content_html)

    util.file_write(article_filepath_out, template)





# #########################################################
# ;HERBS
# #########################################################

def herbs_medicine_benefits():
    for herb_row in herbs_rows[:g.HERBS_ART_NUM]:
        herb_id = herb_row[herbs_cols['herb_id']].strip()
        herb_slug = herb_row[herbs_cols['herb_slug']].strip()
        herb_name_common = herb_row[herbs_cols['herb_name_common']].split(',')[0].strip()
        herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']].strip()

        if herb_id == '': continue
        if herb_slug == '': continue
        if herb_name_common == '': continue
        if herb_name_scientific == '': continue

        if DEBUG_PLANTS_MEDICINE_BENEFITS: print(herb_id)
        if DEBUG_PLANTS_MEDICINE_BENEFITS: print(herb_slug)
        if DEBUG_PLANTS_MEDICINE_BENEFITS: print(herb_name_common)
        if DEBUG_PLANTS_MEDICINE_BENEFITS: print(herb_name_scientific)

        url = f'herbs/{herb_slug}/medicine/benefits'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'website/{url}.html'
        if DEBUG_PLANTS_MEDICINE_BENEFITS: print(html_filepath)

        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)
        data['herb_id'] = herb_id
        data['herb_slug'] = herb_slug
        data['herb_name_common'] = herb_name_common
        data['herb_name_scientific'] = herb_name_scientific
        data['url'] = url
        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 
        title = f'10 health benefits of {herb_name_common}'
        data['title'] = title
        util.json_write(json_filepath, data)

        article_html = ''

        if 'title':
            article_html += f'<h1>{title.title()}</h1>\n'

        if 'benefits':
            key = 'benefits_list'
            # if key in data: data[key] = [] # TODO: remove
            if key not in data: data[key] = []
            herbs_benefits_rows_filtered = util.csv_get_rows_filtered(
                g.CSV_HERBS_BENEFITS_FILEPATH, herbs_benefits_cols['herb_id'], herb_id
            )
            for herb_benefit_row in herbs_benefits_rows_filtered:
                print(herb_benefit_row)
                benefit_name = herb_benefit_row[herbs_benefits_cols['benefit_name']]
                found = False
                for obj in data[key]:
                    if obj['benefit_name'] == benefit_name: 
                        found = True
                        break
                if not found:
                    data[key].append({
                        'herb_id': herb_id,
                        'herb_slug': herb_slug,
                        'herb_name_common': herb_name_common,
                        'herb_name_scientific': herb_name_scientific,
                        'benefit_name': benefit_name,
                    })
            util.json_write(json_filepath, data)
            
            for i, obj in enumerate(data[key][:ART_ITEMS_NUM]):
                obj_herb_name_common = obj["herb_name_common"].strip()
                obj_herb_name_scientific = obj["herb_name_scientific"].strip()
                obj_benefit_name = obj["benefit_name"].strip()

                key = 'benefit_desc'
                # if key in obj: del obj[key]
                if key not in obj:
                    aka = f', also known as {herb_name_scientific},'
                    prompt = f'''
                        Write 1 paragraph of 60 to 80 words on why {obj_herb_name_common} ({obj_herb_name_scientific}) {obj_benefit_name}.
                        Start the reply with the following words: {obj_herb_name_common}{aka} {obj_benefit_name} because .
                    '''
                    reply = utils_ai.gen_reply(prompt)
                    reply = reply.replace(aka, '')
                    reply, error = utils_ai.reply_to_paragraph(reply)
                    if error == '':
                        print('********************************')
                        print(reply)
                        print('********************************')
                        obj[key] = reply
                        util.json_write(json_filepath, data)
                    else:
                        print(f'ERROR: {error}')
                        util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                    time.sleep(g.PROMPT_DELAY_TIME)
                if key in obj:
                    article_html += f'<h2>{i+1}. {obj_benefit_name.capitalize()}</h2>\n'
                    article_html += f'<p>{util.text_format_1N1_html(obj[key])}</p>\n'

        header_html = util.header_default_dark()
        breadcrumbs_html = util.breadcrumbs(html_filepath)
        meta_html = util.article_meta(article_html, lastmod)
        article_html = util.article_toc(article_html)
        footer_html = util.footer()

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                {breadcrumbs_html}
                
                <section class="article-section">
                    <div class="container">
                        {meta_html}
                        {article_html}
                    </div>
                </section>

                {footer_html}
            </body>

            </html>
        '''

        util.file_write(html_filepath, html)
        

def herbs_medicine():
    for herb_row in herbs_rows[:g.HERBS_ART_NUM]:
        herb_id = herb_row[herbs_cols['herb_id']].strip()
        herb_slug = herb_row[herbs_cols['herb_slug']].strip()
        herb_name_common = herb_row[herbs_cols['herb_name_common']].split(',')[0].strip()
        herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']].strip()

        if herb_id == '': continue
        if herb_slug == '': continue
        if herb_name_common == '': continue
        if herb_name_scientific == '': continue

        if DEBUG_PLANTS_MEDICINE_BENEFITS: print(herb_id)
        if DEBUG_PLANTS_MEDICINE_BENEFITS: print(herb_slug)
        if DEBUG_PLANTS_MEDICINE_BENEFITS: print(herb_name_common)
        if DEBUG_PLANTS_MEDICINE_BENEFITS: print(herb_name_scientific)

        url = f'herbs/{herb_slug}/medicine'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'website/{url}.html'
        if DEBUG_PLANTS_MEDICINE_BENEFITS: print(html_filepath)

        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)
        data['herb_id'] = herb_id
        data['herb_slug'] = herb_slug
        data['herb_name_common'] = herb_name_common
        data['herb_name_scientific'] = herb_name_scientific
        data['url'] = url
        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 
        title = f'What Are The Medicinal Properties of {herb_name_common} ({herb_name_scientific})?'
        data['title'] = title
        util.json_write(json_filepath, data)

        article_html = ''

        if 'title':
            article_html += f'<h1>{title}</h1>\n'

        if 'benefits':
            key = 'benefits'
            if key not in data:
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    Write 1 paragraph of 60 to 80 words on what are the health benefits of {herb_name_common} ({herb_name_scientific}).
                    Start the reply with the following words: {herb_name_common}{aka} has health benefits such as .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply, error = utils_ai.reply_to_paragraph(reply)
                if error == '':
                    print('********************************')
                    print(reply)
                    print('********************************')
                    data[key] = reply
                    util.json_write(json_filepath, data)
                else:
                    print(f'ERROR: {error}')
                    util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What are the health benefits of {herb_name_common}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'
        
        if 'constituents':
            key = 'constituents'
            if key not in data:
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    Write 1 paragraph of 60 to 80 words on what are the medicinal constituents of {herb_name_common} ({herb_name_scientific}).
                    Start the reply with the following words: The health benefits of {herb_name_common}{aka} comes from its active constituents, such as .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply, error = utils_ai.reply_to_paragraph(reply)
                if error == '':
                    print('********************************')
                    print(reply)
                    print('********************************')
                    data[key] = reply
                    util.json_write(json_filepath, data)
                else:
                    print(f'ERROR: {error}')
                    util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What are the active constituents of {herb_name_common}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'
                
        if 'preparations':
            key = 'preparations'
            # if key in data: del data[key]
            if key not in data:
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    Write 1 paragraph of 60 to 80 words on what are the medicinal preparations of {herb_name_common} ({herb_name_scientific}) and explain the use of each preparation.
                    Start the reply with the following words: {herb_name_common}{aka} has different medicinal preparations, such as .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply, error = utils_ai.reply_to_paragraph(reply)
                if error == '':
                    print('********************************')
                    print(reply)
                    print('********************************')
                    data[key] = reply
                    util.json_write(json_filepath, data)
                else:
                    print(f'ERROR: {error}')
                    util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What are the medicinal preparations of {herb_name_common}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'
        
        if 'side_effects':
            key = 'side_effects'
            if key not in data:
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    Write 1 paragraph of 60 to 80 words on what are the possible side effects of {herb_name_common} ({herb_name_scientific}) on health if used improperly.
                    Don't include precautions. Just make many examples of possible side effects.
                    Start the reply with the following words: Improper use of {herb_name_common}{aka} increases the chances of experiencing side effects such as .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply, error = utils_ai.reply_to_paragraph(reply)
                if error == '':
                    print('********************************')
                    print(reply)
                    print('********************************')
                    data[key] = reply
                    util.json_write(json_filepath, data)
                else:
                    print(f'ERROR: {error}')
                    util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What are the possible side effect of using {herb_name_common} improperly?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

        if 'precautions':
            key = 'precautions'
            # if key in data: del data[key]
            if key not in data:
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    Write 1 paragraph of 60 to 80 words on what are the precautions to take when using {herb_name_common} ({herb_name_scientific}) medicinally.
                    Start the reply with the following words: Before using {herb_name_common}{aka} for medicinal purposes, you must take precautions such as .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply, error = utils_ai.reply_to_paragraph(reply)
                if error == '':
                    print('********************************')
                    print(reply)
                    print('********************************')
                    data[key] = reply
                    util.json_write(json_filepath, data)
                else:
                    print(f'ERROR: {error}')
                    util.file_append('LOG.md', f'\n\n\n\n\n{reply}\n\n\n\n\n')
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What precautions to take when using {herb_name_common} medicinally?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

        header_html = util.header_default_dark()
        breadcrumbs_html = util.breadcrumbs(html_filepath)
        meta_html = util.article_meta(article_html, lastmod)
        article_html = util.article_toc(article_html)
        footer_html = util.footer()

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                {breadcrumbs_html}
                
                <section class="article-section">
                    <div class="container">
                        {meta_html}
                        {article_html}
                    </div>
                </section>

                {footer_html}
            </body>

            </html>
        '''

        util.file_write(html_filepath, html)


def herbs_pages():
    for herb_row in herbs_rows[:g.HERBS_ART_NUM]:
        herb_id = herb_row[herbs_cols['herb_id']].strip()
        herb_slug = herb_row[herbs_cols['herb_slug']].strip()
        herb_name_common = herb_row[herbs_cols['herb_name_common']].split(',')[0].strip()
        herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']].strip()

        if herb_id == '': continue
        if herb_slug == '': continue
        if herb_name_common == '': continue
        if herb_name_scientific == '': continue

        if DEBUG_PLANTS: print(herb_id)
        if DEBUG_PLANTS: print(herb_slug)
        if DEBUG_PLANTS: print(herb_name_common)
        if DEBUG_PLANTS: print(herb_name_scientific)

        url = f'herbs/{herb_slug}'
        json_filepath = f'database/json/{url}.json'
        html_filepath = f'website/{url}.html'
        if DEBUG_PLANTS: print(html_filepath)

        # json
        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)

        data['herb_id'] = herb_id
        data['herb_slug'] = herb_slug
        data['herb_name_common'] = herb_name_common
        data['herb_name_scientific'] = herb_name_scientific
        data['url'] = url
        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 
        title = f'What to know about {herb_name_common} before using it medicinally'
        data['title'] = title
        util.json_write(json_filepath, data)

        # img
        images_folderpath = f'C:/terrawhisper-assets/images/herbs/{herb_slug}'
        if os.path.exists(images_folderpath):
            images_filenames = os.listdir(images_folderpath)

            # image_featured_filename = random.choice(images_filenames)
            image_featured_filename = images_filenames[0]
            image_featured_filepath_in = f'{images_folderpath}/{image_featured_filename}'
            image_featured_filepath_out = f'website/images/{herb_slug}-overview.jpg'
            image_featured_filepath_web = f'/images/{herb_slug}-overview.jpg'

            label = herb_slug

            if not os.path.exists(image_featured_filepath_out):
            # if os.path.exists(image_featured_filepath_out):
                util.image_save_resized(image_featured_filepath_in, image_featured_filepath_out, 768, 512, 50)
            # util.image_save_resized(image_featured_filepath_in, image_featured_filepath_out, 768, 512, 50)

        # html
        data = util.json_read(json_filepath)

        article_html = ''
        article_html += f'<h1>{title}</h1>\n'
        article_html += f'<p><img src="{image_featured_filepath_web}" alt=""></p>\n'

        key = 'intro_desc' 
        if key not in data: data[key] = ''
        # if key in data: data[key] = ''
        if data[key] == '':
            prompt = f'''
                Write 1 intro paragraph in 5 sentences for an article about the {herb_name_common} herb.
                In sentence 1, explain the health properties of {herb_name_common} and how they improve health.
                In sentence 2, explain the main culinary uses of {herb_name_common}.
                In sentence 3, explain the main hortocultural aspects of {herb_name_common}.
                In sentence 4, explain the botanical properties of {herb_name_common}.
                In sentence 5, explain the main historical references of {herb_name_common}.
                Start the reply with the following words: {herb_name_common}, scientifically know as {herb_name_scientific}, is .
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = utils_ai.reply_to_paragraphs(reply)
            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                data[key] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
        if data[key] != '':
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        key = 'section_medicine_ailments' 
        if key not in data: data[key] = ''
        # if key in data: data[key] = ''
        if data[key] == '':
            aka = f', also known as {herb_name_scientific},'
            prompt = f'''
                Write 1 detailed paragraph about what common ailments {herb_name_common} ({herb_name_scientific}) helps heal.
                Start the reply with the following words: {herb_name_common}{aka} helps healing several common ailments, such us .
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = reply.replace(aka, '')
            reply = utils_ai.reply_to_paragraphs(reply)
            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                data[key] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
        if data[key] != '':
            article_html += f'<h2>What ailments {herb_name_common} help heal?</h2>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        key = 'section_medicine_properties' 
        if key not in data: data[key] = ''
        # if key in data: data[key] = ''
        if data[key] == '':
            aka = f', also known as {herb_name_scientific},'
            prompt = f'''
                Write 1 detailed paragraph about the most important medicinal properties of {herb_name_common} ({herb_name_scientific}).
                
                Start the reply with the following words: {herb_name_common}{aka} has several medicinal properties, such us .
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = reply.replace(aka, '')
            reply = utils_ai.reply_to_paragraphs(reply)
            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                data[key] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
        if data[key] != '':
            article_html += f'<h3>What are the medicinal properties of {herb_name_common}?</h3>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        key = 'section_medicine_parts' 
        if key not in data: data[key] = ''
        # if key in data: data[key] = ''
        if data[key] == '':
            aka = f', also known as {herb_name_scientific},'
            prompt = f'''
                Write 1 detailed paragraph about the most important parts of {herb_name_common} ({herb_name_scientific}) used for medicinal purposes.
                
                Start the reply with the following words: The most commonly used parts of {herb_name_common}{aka} for medicinal purposes are .
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = reply.replace(aka, '')
            reply = utils_ai.reply_to_paragraphs(reply)
            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                data[key] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
        if data[key] != '':
            article_html += f'<h3>What parts of {herb_name_common} are used for medicinal purposes?</h3>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'
        
        key = 'section_medicine_side_effects' 
        if key not in data: data[key] = ''
        # if key in data: data[key] = ''
        if data[key] == '':
            aka = f', also known as {herb_name_scientific},'
            prompt = f'''
                Write 1 detailed paragraph about the possible side effects of improperly using {herb_name_common} ({herb_name_scientific}) for medicinal purposes.
                
                Start the reply with the following words: When used improperly, {herb_name_common}{aka} increases the chances of experiencing side effects, such as .
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = reply.replace(aka, '')
            reply = utils_ai.reply_to_paragraphs(reply)
            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                data[key] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
        if data[key] != '':
            article_html += f'<h3>What are the side effects of {herb_name_common} when used improperly?</h3>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        key = 'section_medicine_precautions' 
        if key not in data: data[key] = ''
        # if key in data: data[key] = ''
        if data[key] == '':
            aka = f', also known as {herb_name_scientific},'
            prompt = f'''
                Write 1 detailed paragraph about the most common precautions to take when using {herb_name_common} ({herb_name_scientific}) medicinally.
                
                Start the reply with the following words: The precautions to take before using {herb_name_common}{aka} medicinally are .
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = reply.replace(aka, '')
            reply = utils_ai.reply_to_paragraphs(reply)
            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                data[key] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
        if data[key] != '':
            article_html += f'<h3>What precautions to take before using {herb_name_common} medicinally?</h3>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'
        
        key = 'section_horticulture' 
        if key not in data: data[key] = ''
        # if key in data: data[key] = ''
        if data[key] == '':
            aka = f', also known as {herb_name_scientific},'
            prompt = f'''
                Write 1 detailed paragraph about what are the horticultural conditions of {herb_name_common} ({herb_name_scientific}).
                Start the reply with the following words: {herb_name_common}{aka} .
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = reply.replace(aka, '')
            reply = utils_ai.reply_to_paragraphs(reply)
            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                data[key] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
        if data[key] != '':
            article_html += f'<h2>What are the horticulture conditions of {herb_name_common}?</h2>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        key = 'section_horticulture_growth' 
        if key not in data: data[key] = ''
        # if key in data: data[key] = ''
        if data[key] == '':
            aka = f', also known as {herb_name_scientific},'
            prompt = f'''
                Write 1 detailed paragraph about what are the growth requirements of {herb_name_common} ({herb_name_scientific}).
                
                Start the reply with the following words: {herb_name_common}{aka} .
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = reply.replace(aka, '')
            reply = utils_ai.reply_to_paragraphs(reply)
            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                data[key] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
        if data[key] != '':
            article_html += f'<h3>What are the growth requirements of {herb_name_common}?</h3>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        key = 'section_horticulture_planting' 
        if key not in data: data[key] = ''
        # if key in data: data[key] = ''
        if data[key] == '':
            aka = f', also known as {herb_name_scientific},'
            prompt = f'''
                Write 1 detailed paragraph about what are the planting tips of {herb_name_common} ({herb_name_scientific}).
                
                Start the reply with the following words: {herb_name_common}{aka} .
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = reply.replace(aka, '')
            reply = utils_ai.reply_to_paragraphs(reply)
            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                data[key] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
        if data[key] != '':
            article_html += f'<h3>What are the planting tips of {herb_name_common}?</h3>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        key = 'section_horticulture_caring' 
        if key not in data: data[key] = ''
        # if key in data: data[key] = ''
        if data[key] == '':
            aka = f', also known as {herb_name_scientific},'
            prompt = f'''
                Write 1 detailed paragraph about what are the caring tips of {herb_name_common} ({herb_name_scientific}).
                
                Start the reply with the following words: {herb_name_common}{aka} .
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = reply.replace(aka, '')
            reply = utils_ai.reply_to_paragraphs(reply)
            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                data[key] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
        if data[key] != '':
            article_html += f'<h3>What are the planting tips of {herb_name_common}?</h3>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        key = 'section_horticulture_harvesting' 
        if key not in data: data[key] = ''
        # if key in data: data[key] = ''
        if data[key] == '':
            aka = f', also known as {herb_name_scientific},'
            prompt = f'''
                Write 1 detailed paragraph about what are the harvesting tips of {herb_name_common} ({herb_name_scientific}).
                
                Start the reply with the following words: {herb_name_common}{aka} .
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = reply.replace(aka, '')
            reply = utils_ai.reply_to_paragraphs(reply)
            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                data[key] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
        if data[key] != '':
            article_html += f'<h3>What are the harvesting tips of {herb_name_common}?</h3>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        key = 'section_horticulture_pests_diseases' 
        if key not in data: data[key] = ''
        # if key in data: data[key] = ''
        if data[key] == '':
            aka = f', also known as {herb_name_scientific},'
            prompt = f'''
                Write 1 detailed paragraph about what are the pest and diseases of {herb_name_common} ({herb_name_scientific}).
                
                Start the reply with the following words: {herb_name_common}{aka} .
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = reply.replace(aka, '')
            reply = utils_ai.reply_to_paragraphs(reply)
            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                data[key] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
        if data[key] != '':
            article_html += f'<h3>What are the pest and diseases tips of {herb_name_common}?</h3>\n'
            article_html += f'{util.text_format_1N1_html(data[key])}\n'

        if 'botany':
            key = 'section_botany' 
            if key not in data: data[key] = ''
            # if key in data: data[key] = ''
            if data[key] == '':
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    Write 1 detailed paragraph about what are the botanical characteristics of {herb_name_common} ({herb_name_scientific}).
                    
                    Start the reply with the following words: {herb_name_common}{aka} .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if data[key] != '':
                article_html += f'<h2>What are the botanical characteristics of {herb_name_common}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            key = 'section_botany_taxonomy' 
            if key not in data: data[key] = ''
            # if key in data: data[key] = ''
            if data[key] == '':
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    Write 1 short paragraph of 60 to 80 words about the taxonomical classification of {herb_name_common} ({herb_name_scientific}).
                    Include kingdom, phylum, class, order, family, genus and species.
                    Write only about the taxonomy. Don't include characteristics or distribution of the plant.
                    Start the reply with the following words: {herb_name_common}{aka} belongs to .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if data[key] != '':
                article_html += f'<h3>What is the taxonomy of {herb_name_common}?</h3>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            key = 'section_botany_variants' 
            if key not in data: data[key] = ''
            # if key in data: data[key] = ''
            if data[key] == '':
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    What are the variants of {herb_name_common} ({herb_name_scientific})?
                    Reply in a short paragraph.
                    Start the reply with the following words: {herb_name_common}{aka} has variants, such as .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if data[key] != '':
                article_html += f'<h3>What are the variants of {herb_name_common}?</h3>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            key = 'section_botany_distribution' 
            if key not in data: data[key] = ''
            # if key in data: data[key] = ''
            if data[key] == '':
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    What is the geographic distribution of {herb_name_common} ({herb_name_scientific})?
                    Reply in a short paragraph.
                    Start the reply with the following words: {herb_name_common}{aka} .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if data[key] != '':
                article_html += f'<h3>What is the geographic distribution of {herb_name_common}?</h3>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            key = 'section_botany_life_cycle' 
            if key not in data: data[key] = ''
            # if key in data: data[key] = ''
            if data[key] == '':
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    What is the life-cycle of {herb_name_common} ({herb_name_scientific})?
                    Reply in a short paragraph.
                    Start the reply with the following words: {herb_name_common}{aka} .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if data[key] != '':
                article_html += f'<h3>What is the life cycle of {herb_name_common}?</h3>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

        if 'historical':
            key = 'section_history' 
            if key not in data: data[key] = ''
            # if key in data: data[key] = ''
            if data[key] == '':
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    Write 1 paragraph of 60 to 80 words about what are the historical uses of {herb_name_common} ({herb_name_scientific}).
                    Start the reply with the following words: {herb_name_common}{aka} .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if data[key] != '':
                article_html += f'<h2>What are the historical uses of {herb_name_common}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            key = 'section_history_mythology' 
            if key not in data: data[key] = ''
            # if key in data: data[key] = ''
            if data[key] == '':
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    Write 1 paragraph of 60 to 80 words about what are the mythological references of {herb_name_common} ({herb_name_scientific}).
                    Start the reply with the following words: {herb_name_common}{aka} .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if data[key] != '':
                article_html += f'<h2>What are the mythological referencec of {herb_name_common}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            key = 'section_history_simbology' 
            if key not in data: data[key] = ''
            # if key in data: data[key] = ''
            if data[key] == '':
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    Write 1 paragraph of 60 to 80 words about what are the symbolic meanings of {herb_name_common} ({herb_name_scientific}).
                    Start the reply with the following words: {herb_name_common}{aka} .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if data[key] != '':
                article_html += f'<h2>What are the symbolic meanings of {herb_name_common}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            key = 'section_history_literature' 
            if key not in data: data[key] = ''
            # if key in data: data[key] = ''
            if data[key] == '':
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    Write 1 paragraph of 60 to 80 words about what are the historical texts of {herb_name_common} ({herb_name_scientific}).
                    Start the reply with the following words: {herb_name_common}{aka} .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if data[key] != '':
                article_html += f'<h2>What are the historical texts of {herb_name_common}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            key = 'section_history_artifacts' 
            if key not in data: data[key] = ''
            # if key in data: data[key] = ''
            if data[key] == '':
                aka = f', also known as {herb_name_scientific},'
                prompt = f'''
                    Write 1 paragraph of 60 to 80 words about what are the historical artifacts of {herb_name_common} ({herb_name_scientific}).
                    Start the reply with the following words: {herb_name_common}{aka} .
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = reply.replace(aka, '')
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if data[key] != '':
                article_html += f'<h2>What are the historical artifacts of {herb_name_common}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

        header_html = util.header_default_dark()
        breadcrumbs_html = util.breadcrumbs(html_filepath)
        meta_html = util.article_meta(article_html, lastmod)
        article_html = util.article_toc(article_html)

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                {breadcrumbs_html}
                
                <section class="article-section">
                    <div class="container">
                        {meta_html}
                        {article_html}
                    </div>
                </section>

                <footer>
                    <div class="container-lg">
                        <span>© TerraWhisper.com 2024 | All Rights Reserved
                    </div>
                </footer>
            </body>

            </html>
        '''

        util.file_write(html_filepath, html)

    # category page
    herbs_cards_html = ''
    for herb_row in herbs_rows[:g.HERBS_ART_NUM]:
        herb_slug = herb_row[herbs_cols['herb_slug']]
        herb_name_common = herb_row[herbs_cols['herb_name_common']].split(',')[0].strip()
   
        url = f'herbs/{herb_slug}'
        json_filepath = f'database/json/{url}.json'
        data = util.json_read(json_filepath)
        title = data['title']
        image_featured_filepath_web = f'/images/{herb_slug}-overview.jpg'

        
        # img
        images_folderpath = f'C:/terrawhisper-assets/images/herbs/{herb_slug}'
        if os.path.exists(images_folderpath):
            images_filenames = os.listdir(images_folderpath)

            image_featured_filename = images_filenames[0]
            image_featured_filepath_in = f'{images_folderpath}/{image_featured_filename}'
            image_featured_filepath_out = f'website/images/{herb_slug}-overview-thumbnail.jpg'
            image_featured_filepath_web = f'/images/{herb_slug}-overview-thumbnail.jpg'

            label = herb_name_common

            if not os.path.exists(image_featured_filepath_out):
            # if os.path.exists(image_featured_filepath_out):
                util.image_save_resized(image_featured_filepath_in, image_featured_filepath_out, 768, 512, 50)
                util.image_label_01(image_featured_filepath_out, label)



        herbs_cards_html += f'''
            <div>
                <a href="/herbs/{herb_slug}.html">
                    <img src="{image_featured_filepath_web}" alt="">
                    <h3>{title}</h3>
                </a>
            </div>
        '''

    article_html = herbs_cards_html

    html_filepath = f'website/herbs.html'

    header_html = util.header_default_dark()
    breadcrumbs_html = util.breadcrumbs(html_filepath)

    html = f'''
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="{g.AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="/style.css">
            <title>{title}</title>
            {g.GOOGLE_TAG}
            
        </head>

        <body>
            {header_html}
            {breadcrumbs_html}
            
            <section class="blog-grid">
                <div class="container-lg">
                    <div class="grid grid-3 gap-24">
                        {article_html}
                    </div>
                </div>
            </section>

            <footer>
                <div class="container-lg">
                    <span>© TerraWhisper.com 2024 | All Rights Reserved
                </div>
            </footer>
        </body>

        </html>
    '''

    util.file_write(html_filepath, html)



# #########################################################
# ;GENERAL
# #########################################################

def page_home():
    header = util.header_default()
    header = util.header_default_dark()

    # image_filepath_in = 'C:/terrawhisper-assets/images/home/medicinal-herbs.jpg'
    # image_filepath_out = 'website/images/medicinal-herbs.jpg'

    # util.image_save_resized(
    #     image_filepath_in, 
    #     image_filepath_out, 
    #     768,
    #     768,
    #     50,
    # )
    
    teas_articles_html = ''
    for condition_row in conditions_rows[:6]:
        condition_name = condition_row[conditions_cols['condition_names']].split(',')[0].strip().lower()
        condition_slug = condition_row[conditions_cols['condition_slugs_prev']].split(',')[0].strip().lower()

        if condition_name == '': continue

        condition_system_id = condition_row[conditions_cols['system_id']].split(',')[0].strip().lower()
        condition_system_slug = util.csv_get_rows_filtered(g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], condition_system_id)[0][systems_cols['system_slug']]

        imagepath = f'/images/herbal-tea-for-{condition_slug}-overview.jpg'
        teas_articles_html += f'''
            <a href="/herbalism/tea/{condition_system_slug}/{condition_slug}.html">
                <div class="card">
                    <img class="card-image"
                        src="{imagepath}" alt=""
                        width="400" height="300">
                    <h3 class="px-16 mt-16">10 Best Herbal Teas For {condition_name.title()}</h3>
                    <p class="px-16 mt-16">Boosts the immune system and fights infections.</p>
                </div>
            </a>
        '''


    articles_teas_html = ''
    i = 0
    for status_row in status_rows:
        if i >= 6: break

        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip().lower()

        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue

        system_row = get_system_by_status(status_id)

        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/teas.json'
        if not os.path.exists(json_filepath): continue

        data = util.json_read(json_filepath)

        intro_desc_clip = ' '.join(data['intro_desc'].split(' ')[:20]).strip() + '...'
        year, month, day = data['lastmod'].split('-')
        lastmod = f'{month}/{day}/{year}'

        src = f'/images/herbal-teas-for-{status_slug}-overview.jpg'
        alt = f'herbal teas for {status_slug}'
        articles_teas_html += f'''
            <div>
                <a href="/remedies/{system_slug}/{status_slug}/teas.html">
                    <img src="{src}" alt="{alt}">
                    <h3>10 Best Herbal Teas For {status_name.title()}</h3>
                </a>
                <p class="desc">{intro_desc_clip}</p>
                <p class="author">By <span>Leen Randell</span> - {lastmod}</p>
            </div>
        '''

        i += 1

    articles_tinctures_html = ''
    i = 0
    for status_row in status_rows:
        if i >= 6: break

        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip().lower()

        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue

        system_row = get_system_by_status(status_id)

        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/tinctures.json'
        if not os.path.exists(json_filepath): continue

        data = util.json_read(json_filepath)

        intro_desc_clip = ' '.join(data['intro_desc'].split(' ')[:20]).strip() + '...'
        year, month, day = data['lastmod'].split('-')
        lastmod = f'{month}/{day}/{year}'

        src = f'/images/herbal-tinctures-for-{status_slug}-overview.jpg'
        alt = f'herbal tinctures for {status_slug}'
        articles_tinctures_html += f'''
            <div>
                <a href="/remedies/{system_slug}/{status_slug}/tinctures.html">
                    <img src="{src}" alt="{alt}">
                    <h3>10 Best Herbal Tinctures For {status_name.title()}</h3>
                </a>
                <p class="desc">{intro_desc_clip}</p>
                <p class="author">By <span>Leen Randell</span> - {lastmod}</p>
            </div>
        '''
        i += 1
        
    articles_herbs_html = ''
    i = 0
    for herb_row in herbs_rows[:g.HERBS_ART_NUM]:
        if i >= 6: break

        herb_id = herb_row[herbs_cols['herb_id']]
        herb_slug = herb_row[herbs_cols['herb_slug']]
        herb_name_common = herb_row[herbs_cols['herb_name_common']].split(',')[0].strip().lower()
        herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']].strip()

        if herb_id == '': continue
        if herb_slug == '': continue
        if herb_name_common == '': continue
        if herb_name_scientific == '': continue

        json_filepath = f'database/json/herbs/{herb_slug}.json'
        if not os.path.exists(json_filepath): continue

        data = util.json_read(json_filepath)

        intro_desc_clip = ' '.join(data['intro_desc'].split(' ')[:20]).strip() + '...'
        year, month, day = data['lastmod'].split('-')
        lastmod = f'{month}/{day}/{year}'

        src = f'/images/{herb_slug}-overview.jpg'
        alt = f'{herb_name_scientific} overview'
        articles_herbs_html += f'''
            <div>
                <a href="/herbs/{herb_slug}.html">
                    <img src="{src}" alt="{alt}">
                    <h3>What to know before using {herb_name_common} medicinally</h3>
                </a>
                <p class="desc">{intro_desc_clip}</p>
                <p class="author">By <span>Leen Randell</span> - {lastmod}</p>
            </div>
        '''
        i += 1

        
                    
    slug = 'index'

    template = util.file_read(f'templates/{slug}.html')

    template = template.replace('[meta_title]', 'Herbalism & Natural Healing')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[teas_articles]', teas_articles_html)
    template = template.replace('[articles_teas]', articles_teas_html)
    template = template.replace('[articles_tinctures]', articles_tinctures_html)
    template = template.replace('[articles_herbs]', articles_herbs_html)

    util.file_write(f'website/{slug}.html', template)


def page_privacy_policy():
    slug = 'privacy-policy'
    filepath_in = f'templates/{slug}.html'
    filepath_out = f'website/{slug}.html'

    breadcrumbs_html = util.breadcrumbs(filepath_out)
    header = util.header_default_dark()
    footer = util.footer()

    template = util.file_read(filepath_in)

    template = template.replace('[title]', 'TerraWhisper Privacy Policy')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[footer]', footer)

    util.file_write(filepath_out, template)


def page_cookie_policy():
    slug = 'cookie-policy'
    filepath_in = f'templates/{slug}.html'
    filepath_out = f'website/{slug}.html'

    breadcrumbs_html = util.breadcrumbs(filepath_out)
    header = util.header_default_dark()
    footer = util.footer()

    template = util.file_read(filepath_in)

    template = template.replace('[title]', 'TerraWhisper Cookie Policy')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[footer]', footer)

    util.file_write(filepath_out, template)


def page_herbalism():
    header = util.header_default()
    header = util.header_default_dark()

    page_url = 'herbalism'
    article_filepath_out = f'website/{page_url}.html'

    template = util.file_read(f'templates/{page_url}.html')
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)

    template = template.replace('[meta_title]', 'Herbalism & Natural Healing')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[title]', 'Herbalism: Herbal Medicine and Preparations')
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)

    util.file_write(article_filepath_out, template)


def page_start_here():
    slug = 'start-here'
    filepath_in = f'templates/{slug}.html'
    filepath_out = f'website/{slug}.html'

    header = util.header_default()
    breadcrumbs_html = util.breadcrumbs(filepath_out)

    template = util.file_read(filepath_in)
    template = template.replace('[title]', 'Start Your Herbalism Journey Here At TerraWhisper')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    util.file_write(filepath_out, template)


def page_about():
    page_url = 'about'
    article_filepath_out = f'website/{page_url}.html'

    header = util.header_default()
    header = util.header_default_dark()
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)
    content = util.file_read(f'static/about.md')
    content = markdown.markdown(content, extensions=['markdown.extensions.tables'])
    
    template = util.file_read('templates/about.html')

    template = template.replace('[title]', 'TerraWhisper | About')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[content]', content)

    util.file_write(article_filepath_out, template)


def page_top_herbs():
    articles_folderpath = 'database/articles/plants'
    plants = util.csv_get_rows('database/tables/plants.csv')
    articles_html = ''

    plants_primary = []
    for plant in plants[1:]:
        latin_name = plant[0].strip().capitalize()
        entity = latin_name.lower().replace(' ', '-')
        filepath_in = f'{articles_folderpath}/{entity}.json'
        data = util.json_read(filepath_in)

        title = data['title']
        common_name = data['common_name']

        article_html = f'''
            <a href="/plants/{entity}.html">
                <div>
                    <img src="/images/{entity}-overview.jpg" alt="">
                    <h3 class="mt-0 mb-0">{latin_name} ({common_name})</h3>
                </div>
            </a>
        '''
        plants_primary.append(article_html)

    articles_html += '<div class="articles">' +'\n'.join(plants_primary) + '</div>'

    page_url = 'top-herbs'
    article_filepath_out = f'website/{page_url}.html'

    header = util.header_default()
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)

    template = util.file_read(f'templates/{page_url}.html')
    template = template.replace('[meta_title]', 'Herbs')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[articles]', articles_html)

    util.file_write(article_filepath_out, template)


# def page_plants(regen_csv=False):
#     json_filenames_plants_primary_secondary = [filename.lower().strip() for filename in os.listdir('database/articles/plants') if filename.endswith('.json')]
#     # json_filenames_plants_treffle = [filename.lower().strip() for filename in os.listdir('database/articles/plants_trefle') if filename.endswith('.json')]
    
#     json_filepaths_plants = [] 
#     for filename in json_filenames_plants_primary_secondary: json_filepaths_plants.append(f'database/articles/plants/{filename}')
#     # for filename in json_filenames_plants_treffle: json_filepaths_plants.append(f'database/articles/plants_trefle/{filename}')

#     plants_list = []
#     for filepath in json_filepaths_plants:
#         filepath_in = f'{filepath}'
#         data = util.json_read(filepath_in)
#         plant_name = data['latin_name']
#         plant_slug = data['entity']
#         plants_list.append(f'<a href="/plants/{plant_slug}.html">{plant_name}</a>')

#     plants_list = sorted(plants_list)
#     plants_html = ''.join(plants_list)

#     page_url = 'plants'
#     article_filepath_out = f'website/{page_url}.html'
#     breadcrumbs_html = util.breadcrumbs(article_filepath_out)

#     template = util.file_read(f'templates/{page_url}.html')
#     template = template.replace('[title]', 'Plants')
#     template = template.replace('[google_tag]', g.GOOGLE_TAG)
#     template = template.replace('[author_name]', g.AUTHOR_NAME)
#     template = template.replace('[header]', util.header_default())
#     template = template.replace('[breadcrumbs]', breadcrumbs_html)
#     template = template.replace('[plants_num]', str(len(json_filepaths_plants)))
#     template = template.replace('[items]', plants_html)
#     util.file_write(article_filepath_out, template)

#     # GENERATE CSV TO DOWNLOAD
#     if regen_csv:
#         rows = []
#         for filepath in json_filepaths_plants:
#             slug = filepath.split('/')[-1].split('.')[0].strip().lower()
#             rows.append([slug])

#         csv_plants_primary = util.csv_get_rows('database/tables/plants.csv')
#         csv_plants_secondary = util.csv_get_rows('database/tables/plants-secondary.csv')
#         csv_plants_trefle = util.csv_get_rows('database/tables/plants/trefle.csv')

#         csv_plants = [] 
#         for row in csv_plants_primary: csv_plants.append(row)
#         for row in csv_plants_secondary: csv_plants.append(row)
#         for row in csv_plants_trefle: csv_plants.append(row)

#         rows_final = [['slug', 'scientific_name', 'common_name', 'genus', 'family']]
#         for row in rows:
#             for csv_plant in csv_plants:
#                 if csv_plant[0].strip().lower() == row[0].strip().lower():
#                     rows_final.append(csv_plant)
#                     break

#         util.csv_set_rows('website/plants.csv', rows_final, delimiter=',')



# #########################################################
# JSON CLEANUP
# #########################################################

def json_del_keys_herbalism_tea(key):
    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        print(f'> {problem_name}')

        system_row = csv_get_system_by_problem(problem_id)

        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        print(f'  > {system_name}')

        json_filepath = f'database/json/herbalism/tea/{system_slug}/{problem_slug}.json'

        data = util.json_read(json_filepath)
        if key in data: del data[key]
        util.json_write(json_filepath, data)


def json_del_keys_herbalism_tincture(key):
    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        print(f'> {problem_name}')

        system_row = csv_get_system_by_problem(problem_id)

        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        print(f'  > {system_name}')

        json_filepath = f'database/json/herbalism/tincture/{system_slug}/{problem_slug}.json'

        if os.path.exists(json_filepath):
            data = util.json_read(json_filepath)
            if key in data: del data[key]
            util.json_write(json_filepath, data)
        else: print(f'file not exists: {json_filepath}')



# json_del_keys_herbalism_tea(key='intro_desc')
# json_del_keys_herbalism_tincture(key='intro_desc')

# json_del_keys_herbalism_tea(key='supplementary_causes')
# json_del_keys_herbalism_tincture(key='supplementary_causes')

# quit()




# #########################################################
# ;REMEDIES NEW
# #########################################################

def remedies_systems_problems_new():
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']]
        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip()

        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue

        if DEBUG_STATUS: print(f'>> {status_id} - {status_name}')

        system_row = get_system_by_status(status_id)

        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        if DEBUG_STATUS: print(f'    {system_id} - {system_name}')

        # init
        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}/{status_slug}.json'
        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)
        data['status_id'] = status_id
        data['status_slug'] = status_slug
        data['status_name'] = status_name
        data['system_id'] = system_id
        data['system_slug'] = system_slug
        data['system_name'] = system_name
        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 
        title = f'What to know about {status_name} before treating it with medicinal herbs'
        data['title'] = title
        util.json_write(json_filepath, data)

        article_html = ''

        if 'title':
            article_html += f'<h1>{title}</h1>\n'
            
        if 'featured_image':
            image_filepath_out = f'website/images/{status_slug}-overview.jpg'
            image_filepath_web = f'/images/{status_slug}-overview.jpg'
            if not os.path.exists(image_filepath_out): 
            # if True: 
                img_w, img_h = 768, 512
                p_x = 48
                font_size = img_w//12
                img = Image.new(mode="RGB", size=(img_w, img_h), color=c_dark)
                draw = ImageDraw.Draw(img)

                text = status_name.upper()
                font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)
                line_width_max = img_w - p_x

                lines = util_image.text_to_lines(text, font, line_width_max) 

                text_height_total = 0
                for i, line in enumerate(lines):
                    _, _, text_w, text_h = font.getbbox(line)
                    text_height_total += text_h

                line_h = 1.3
                for i, line in enumerate(lines):
                    _, _, text_w, text_h = font.getbbox(line)
                    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 + (i*text_h*line_h) - text_height_total//4), line, '#ffffff', font=font)
                img.save(image_filepath_out, quality=50) 
            article_html += f'<p><img src="{image_filepath_web}" alt="{status_name} overview"></p>'

        if 'intro':
            key = 'intro_desc'
            if key not in data:
                prompt = f'''
                    Write 1 short paragraph of about 60 to 80 words on the best herbs for {status_name}.
                    Include a brief definition of: {status_name}.
                    Include the negative impacts of {status_name} in people lives. 
                    Include the causes of {status_name}. 
                    Include the medicinal herbs and their preparations for {status_name}. 
                    Include the precautions when using herbs medicinally for {status_name}. 
                    
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_paragraphs(reply)
                if len(reply) <= 3:
                    reply = ' '.join(reply)
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'{util.text_format_1N1_html(data[key])}\n'
                article_html += f'<p>This article explains in detail what {status_name} is, how it affects your life and what are its causes. Then, it lists what medicinal herbs to use to relieve this problem and how to prepare these herbs to get the best results. Lastly, it revals what other natural remedies to use in conjunction with herbal medicine to aid with this problem.</p>\n'

        if 'definition':
            key = 'definition'
            if key not in data:
                prompt = f'''
                    Write 1 paragraph explaining what is {status_name} and include many examples on how it affects negatively your life.
                    Don't mention the casuses of {status_name}.
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_paragraphs(reply)
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What is {status_name} and how it affects your life?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

        if 'causes':
            key = 'causes_desc'
            if key not in data:
                prompt = f'''
                    Write 1 paragraph explaining what are the main causes of {status_name}.
                    Start the reply with the following words: The main causes of {status_name} are .
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    if line[0].isdigit(): continue
                    if ':' in line: continue
                    lines_formatted.append(line)
                if len(lines_formatted) == 1:
                    print('***************************************')
                    print(lines_formatted[0])
                    print('***************************************')
                    data[key] = lines_formatted[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What are the main causes of {status_name}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data["causes_desc"])}\n'

            # img
            key = 'causes_list'
            if key in data:
                image_filepath_out = f'website/images/{status_slug}-causes.jpg'
                image_filepath_web = f'/images/{status_slug}-causes.jpg'
                if not os.path.exists(image_filepath_out): 
                # if True: 
                    util_image.image_template_causes(image_filepath_out, data)
                article_html += f'<p><img src="{image_filepath_web}" alt="{status_name} causes"></p>'

            key = 'causes_list'
            if key not in data:
                causes_num = 10
                prompt = f'''
                    Write a numbered list of the {causes_num} most common causes of {status_name}.
                    Include a short description for each cause.
                    Reply with the following format: [cause name]: [description]. 
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    line = line.replace('*', '')
                    line = line.replace('[', '')
                    line = line.replace(']', '')
                    if 'http' in line: continue
                    if not line[0].isdigit(): continue
                    if '.' not in line: continue
                    if ':' not in line: continue
                    line = '.'.join(line.split('.')[1:])
                    line = line.strip()
                    if line == '': continue
                    lines_formatted.append(line)
                if len(lines_formatted) == causes_num:
                    print('***************************************')
                    print(lines_formatted)
                    print('***************************************')
                    data[key] = lines_formatted
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<p>The most common causes of {status_name} are listed below.</p>\n'
                article_html += f'<ul>\n'
                for item in data['causes_list']:
                    chunks = item.split(':')
                    chunk_1 = f'<strong>{chunks[0]}</strong>\n'
                    chunk_2 = ':'.join(chunks[1:])
                    article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
                article_html += f'</ul>\n'

        if 'herbs':
            herbs_rows_filtered = csv_get_herbs_auto_by_status(status_id)

            # get common names
            herbs_names_common_list = []
            for herb_row_filtered in herbs_rows_filtered:
                herb_id = herb_row_filtered[herbs_auto_cols['herb_id']]
                herb_name_common = csv_get_herb_common_name_by_id(herb_id)
                herbs_names_common_list.append(herb_name_common)

            key = 'herbs_desc'
            if key not in data:
                herbs_names_common_prompt = ', '.join(herbs_names_common_list[:5])
                prompt = f'''
                    Write 1 paragraph of about 60 to 80 words on what medicinal herbs helps with {status_name} and why.
                    Include some of the following herbs: {herbs_names_common_prompt}.
                    Start the reply with the following words: The best medicinal herbs for {status_name} are .
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    if line[0].isdigit(): continue
                    if ':' in line: continue
                    lines_formatted.append(line)
                if len(lines_formatted) == 1:
                    print('***************************************')
                    print(lines_formatted[0])
                    print('***************************************')
                    data[key] = lines_formatted[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What are the best medicinal herbs for {status_name}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            # img
            key = 'herbs_list'
            if key in data:
                image_filepath_out = f'website/images/{status_slug}-herbs.jpg'
                image_filepath_web = f'/images/{status_slug}-herbs.jpg'
                if not os.path.exists(image_filepath_out): 
                # if True: 
                    util_image.image_template_herbs(image_filepath_out, data)
                article_html += f'<p><img src="{image_filepath_web}" alt="{status_slug} herbs"></p>'
            
            key = 'herbs_list'
            # if key in data: del data[key]
            if key not in data:
                herbs_num = 10
                herbs_names_common_prompt = ''
                for i, herb_common_name in enumerate(herbs_names_common_list[:herbs_num]):
                    herbs_names_common_prompt += f'{i+1}. {herb_common_name.capitalize()}\n'
                prompt = f'''
                    Here is a list of medicinal herbs for {status_name}:
                    {herbs_names_common_prompt}
                    For each medicinal herb in the list above, explain in 1 sentence why that herb helps with {status_name}.
                    Reply with a numbered list using the following format: [herb name]: [description].
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    line = line.replace('*', '')
                    line = line.replace('[', '')
                    line = line.replace(']', '')
                    if not line[0].isdigit(): continue
                    if '.' not in line: continue
                    if ':' not in line: continue
                    line = '.'.join(line.split('.')[1:])
                    line = line.strip()
                    if line == '': continue
                    lines_formatted.append(line)
                if len(lines_formatted) == herbs_num:
                    print('***************************************')
                    print(lines_formatted)
                    print('***************************************')
                    data[key] = lines_formatted
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<p>The most effective medicinal herbs that help with {status_name} are listed below.</p>\n'
                article_html += f'<ul>\n'
                for item in data[key]:
                    chunks = item.split(':')
                    chunk_1 = chunks[0]
                    chunk_2 = ':'.join(chunks[1:])
                    # herb_row_found = []
                    # for herb_row in herbs_rows:
                    #     if chunk_1.lower().strip() in herb_row[herbs_cols['herb_name_common']]:
                    #         herb_row_found = herb_row
                    # if herb_row_found != []:
                    #     herb_slug = herb_row_found[herbs_cols['herb_slug']]
                    #     herb_name_scientific = herb_row_found[herbs_cols['herb_name_scientific']]
                    #     if os.path.exists(f'website/herbs/{herb_slug}.html'):
                    #         chunk_1 = f'<strong><a href="/herbs/{herb_slug}.html">{chunk_1}</a></strong>'
                    #     else:
                    #         chunk_1 = f'<strong>{chunk_1}</strong>'
                    article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
                article_html += f'</ul>\n'

        if 'preparations':
            preparations_rows_filtered = get_preparations_by_status(status_id)
            preparations_names = [row[preparations_cols['preparation_name']] for row in preparations_rows_filtered]
                
            key = 'preparations_desc'
            # if key in data: del data[key]
            if key not in data:
                preparations_names_prompt = ', '.join(preparations_names[:5])
                prompt = f'''
                    Write 1 paragraph about the what are the best types of herbal preparations for {status_name}.
                    Include the following types of herbal preparations: {preparations_names_prompt}.
                    Explain why each preparation helps with {status_name}.
                    Don't include names of herbs.
                    Don't include definitions for the preparations.
                    Don't include how to make the preparations.
                    Start the reply with the following words: The most effective herbal preparations for {status_name} are .
                    
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    if line[0].isdigit(): continue
                    if ':' in line: continue
                    lines_formatted.append(line)
                if len(lines_formatted) == 1:
                    print('***************************************')
                    print(lines_formatted[0])
                    print('***************************************')
                    data[key] = lines_formatted[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What are the most effective herbal preparations for {status_name}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'
                
            # img
            key = 'preparations_list'
            if key in data:
                image_filepath_out = f'website/images/{status_slug}-preparations.jpg'
                image_filepath_web = f'/images/{status_slug}-preparations.jpg'
                if not os.path.exists(image_filepath_out): 
                # if True: 
                    util_image.image_template_preparations(image_filepath_out, data)
                article_html += f'<p><img src="{image_filepath_web}" alt="{status_name} herbs"></p>'

            key = 'preparations_list'
            if key not in data:
                preparations_names_prompt = ''
                for i, preparation_name in enumerate(preparations_names[:10]):
                    preparations_names_prompt += f'{i+1}. {preparation_name.capitalize()}\n'
                prompt = f'''
                    Here is a list of the types of herbal preparations for {status_name}:
                    {preparations_names_prompt}
                    For each type of herbal preparation in the list above, explain in 1 detailed sentence how and why that preparation helps with {status_name}.
                    Don't include names of herbs.
                    Don't include definitions for the preparations.
                    Don't explain the making process of the preparations.
                    Reply with a numbered list using the following format: [preparation name]: [description].
                    
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    line = line.replace('*', '')
                    line = line.replace('[', '')
                    line = line.replace(']', '')
                    if not line[0].isdigit(): continue
                    if '.' not in line: continue
                    if ':' not in line: continue
                    line = '.'.join(line.split('.')[1:])
                    line = line.strip()
                    if line == '': continue
                    lines_formatted.append(line)
                if len(lines_formatted) >= 4:
                    print('***************************************')
                    print(lines_formatted)
                    print('***************************************')
                    data[key] = lines_formatted
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<p>The most used herbal preparations that help with {status_name} are listed below.</p>\n'
                article_html += f'<ul>\n'
                for item in data['preparations_list']:
                    chunks = item.split(':')
                    chunk_1 = chunks[0]
                    chunk_2 = ':'.join(chunks[1:])
                    # TODO: link only if href page exist
                    if chunk_1.lower().strip() == 'teas':
                        chunk_1 = f'<strong><a href="/remedies/{system_slug}/{status_slug}/teas.html">{chunk_1}</a></strong>'
                    elif chunk_1.lower().strip() == 'tinctures':
                        chunk_1 = f'<strong><a href="/remedies/{system_slug}/{status_slug}/tinctures.html">{chunk_1}</a></strong>'
                    elif chunk_1.lower().strip() == 'capsules':
                        chunk_1 = f'<strong><a href="/remedies/{system_slug}/{status_slug}/capsules.html">{chunk_1}</a></strong>'
                    else:
                        chunk_1 = f'<strong>{chunk_1}</strong>'
                    article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
                article_html += f'</ul>\n'

        if 'precautions':
            key = 'precautions_desc'
            if key not in data:
                prompt = f'''
                    Write 1 paragraph about the precautions to take when using herbal remedies for {status_name}.
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What precautions to take when using herbal remedies for {status_name}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            key = 'precautions_list'
            if key not in data:
                prompt = f'''
                    Write a numbered list of precautions to take when using herbal remedies for {status_name}.
                    Start each precaution with an action verb.
                    Don't use the character ":".
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    line = line.replace('*', '')
                    line = line.replace('[', '')
                    line = line.replace(']', '')
                    if not line[0].isdigit(): continue
                    if '.' not in line: continue
                    if ':' in line: continue
                    line = '.'.join(line.split('.')[1:])
                    line = line.strip()
                    if line == '': continue
                    lines_formatted.append(line)
                print(len(lines_formatted))
                if len(lines_formatted) >= 4:
                    print('***************************************')
                    print(lines_formatted)
                    print('***************************************')
                    data[key] = lines_formatted
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<p>The most important precautions to take when using herbal remedies for {status_name} are listed below.</p>\n'
                article_html += f'<ul>\n'
                for item in data['precautions_list']:
                    article_html += f'<li>{item}</li>\n'
                article_html += f'</ul>\n'



        # html
        html_filepath = f'website/{g.CATEGORY_REMEDIES}/{system_slug}/{status_slug}.html'

        header_html = util.header_default_dark()
        breadcrumbs_html = util.breadcrumbs(html_filepath)
        meta_html = util.article_meta(article_html, lastmod)
        article_html = util.article_toc(article_html)
        footer_html = util.footer()

        html = f'''
            <!DOCTYPE html>
            <html lang="en">

            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta name="author" content="{g.AUTHOR_NAME}">
                <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
                <link rel="stylesheet" href="/style.css">
                <title>{title}</title>
                {g.GOOGLE_TAG}
                
            </head>

            <body>
                {header_html}
                {breadcrumbs_html}
                
                <section class="article-section">
                    <div class="container">
                        {meta_html}
                        {article_html}
                    </div>
                </section>

                {footer_html}
            </body>

            </html>
        '''

        util.file_write(html_filepath, html)

        continue

        
        
        if 'other_remedies':
            key = 'other_remedies_desc'
            if key not in data:
                prompt = f'''
                    Write 1 paragraph about the natural remedies for {problem_name}, without including herbal remedies.
                '''
                reply = utils_ai.gen_reply(prompt)
                reply = utils_ai.reply_to_paragraphs(reply)
                print(len(reply))
                if len(reply) == 1:
                    print('*******************************************')
                    print(reply)
                    print('*******************************************')
                    data[key] = reply[0]
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<h2>What natural remedies to use with medicinal herbs for {problem_name}?</h2>\n'
                article_html += f'{util.text_format_1N1_html(data[key])}\n'

            key = 'other_remedies_list'
            if key not in data:
                items_num = 10
                prompt = f'''
                    Write a numbered list of the {items_num} most effective natural remedies for {problem_name}, without including herbal remedies.
                    Start each natural remedy with an action verb.
                    Each list item must have the following format: [natural remedy]: [description].
                '''
                reply = utils_ai.gen_reply(prompt)
                lines = reply.split('\n')
                lines_formatted = []
                for line in lines:
                    line = line.strip()
                    if line == '': continue
                    line = line.replace('*', '')
                    line = line.replace('[', '')
                    line = line.replace(']', '')
                    if not line[0].isdigit(): continue
                    if '.' not in line: continue
                    if ':' not in line: continue
                    line = '.'.join(line.split('.')[1:])
                    line = line.strip()
                    if line == '': continue
                    lines_formatted.append(line)
                if len(lines_formatted) == items_num:
                    print('***************************************')
                    print(lines_formatted)
                    print('***************************************')
                    data[key] = lines_formatted
                    util.json_write(json_filepath, data)
                time.sleep(g.PROMPT_DELAY_TIME)
            if key in data:
                article_html += f'<p>The most effective natural remedies to use in conjunction with herbal medicine that help with {problem_name} are listed below.</p>\n'
                article_html += f'<ul>\n'
                for item in data['other_remedies_list']:
                    chunks = item.split(':')
                    chunk_1 = f'<strong>{chunks[0]}</strong>\n'
                    chunk_2 = ':'.join(chunks[1:])
                    article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
                article_html += f'</ul>\n'


def remedies_systems_new():
    for system_row in systems_rows:
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        status_rows_filtered = csv_get_status_by_system(system_id)
        status_num = len(status_rows_filtered)

        if status_num == 0: continue

        json_filepath = f'database/json/remedies/{system_slug}.json'
        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)
        data['url'] = system_slug
        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 
        title = f'{system_name.title()} Ailments To Heal With Herbal Remedies'
        data['title'] = title
        util.json_write(json_filepath, data)

        category_title = f'<h1>{title}</h1>'
        category_intro = f'<p></p>'

        content_html = ''
        for status_row in status_rows_filtered:
            status_slug = status_row[status_cols['status_slug']]
            status_name = status_row[status_cols['status_names']].split(',')[0].strip()

            src = f'/images/{status_slug}-overview.jpg'
            alt = f'{status_name} overview'

            json_filepath = f'database/json/remedies/{system_slug}/{status_slug}.json'
            if os.path.exists(json_filepath):
                data = util.json_read(json_filepath)

                intro_desc_clip = ' '.join(data['intro_desc'].split(' ')[:16]).strip() + '...'
                content_html += f'''
                    <a href="/remedies/{system_slug}/{status_slug}.html">
                        <div>
                            <img src="{src}" alt="{alt}">
                            <h2>{status_name.title()}: Causes, Herbal Remedies, and More</h2>
                            <p>{intro_desc_clip}</p>
                        </div>
                    </a>
                '''
    
        page_url = f'remedies/{system_slug}'
        article_filepath_out = f'website/{page_url}.html'

        header = util.header_default_dark()
        breadcrumbs_html = util.breadcrumbs(article_filepath_out)
        
        template = util.file_read('templates/category.html')

        template = template.replace('[title]', f'Herbal Remedies For {system_name.title()} Ailments')
        template = template.replace('[google_tag]', g.GOOGLE_TAG)
        template = template.replace('[author_name]', g.AUTHOR_NAME)
        template = template.replace('[header]', header)
        template = template.replace('[breadcrumbs]', breadcrumbs_html)
        template = template.replace('[category_title]', category_title)
        template = template.replace('[category_intro]', category_intro)
        template = template.replace('[content]', content_html)

        util.file_write(article_filepath_out, template)


def remedies():
    title = f'Herbal Remedies Organized By Body Systems'
    category_title = f'<h1>{title}</h1>'
    category_intro = ''

    content_html = ''
    for system_row in systems_rows:
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]
        
        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        json_filepath = f'database/json/remedies/{system_slug}.json'
        if os.path.exists(json_filepath):
            # featured image
            image_filepath_out = f'website/images/{system_slug}-overview.jpg'
            image_filepath_src = f'/images/{system_slug}-overview.jpg'
            image_filepath_alt = f'{system_name} overview'
            # if not os.path.exists(image_filepath_out): 
            if True: 
                img_w, img_h = 768, 512
                p_x = 48
                font_size = img_w // 12

                img = Image.new(mode="RGB", size=(img_w, img_h), color=c_dark)
                draw = ImageDraw.Draw(img)

                text = system_name.upper()
                font = ImageFont.truetype("assets/fonts/arial/ARIAL.TTF", font_size)

                words = text.split()
                lines = words

                text_height_total = 0
                for i, line in enumerate(lines):
                    _, _, text_w, text_h = font.getbbox(line)
                    text_height_total += text_h

                line_h = 1.3
                for i, line in enumerate(lines):
                    _, _, text_w, text_h = font.getbbox(line)
                    draw.text((img_w//2 - text_w//2, img_h//2 - text_h//2 + (i*text_h*line_h) - text_height_total//4), line, '#ffffff', font=font)
                img.save(image_filepath_out, quality=50) 

            data = util.json_read(json_filepath)
            if 'intro_desc' in data:
                intro_desc_clip = data['intro_desc'][:100]
                intro_desc_clip = ' '.join(data['intro_desc'].split(' ')[:16]).strip() + '...'
            else: 
                intro_desc_clip = ''
                
            content_html += f'''
                <a href="/remedies/{system_slug}.html">
                    <div>
                        <img src="{image_filepath_src}" alt="{image_filepath_alt}">
                        <h2>Herbal Remedies for the {system_name.title()}</h2>
                        <p>{intro_desc_clip}</p>
                    </div>
                </a>
            '''
    
    page_url = f'remedies'
    article_filepath_out = f'website/{page_url}.html'

    header = util.header_default_dark()
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)
    
    template = util.file_read('templates/category.html')

    template = template.replace('[title]', title)
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[category_title]', category_title)
    template = template.replace('[category_intro]', category_intro)
    template = template.replace('[content]', content_html)

    util.file_write(article_filepath_out, template)





# #########################################################
# EXE
# #########################################################

page_home()
# page_privacy_policy()
# page_cookie_policy()
# page_herbalism()
# page_top_herbs()
# page_plants(regen_csv=False)
# page_about()

# if 'remedies':
#     remedies_systems_problems()
#     remedies_systems()
#     remedies()

if 'remedies':
    remedies_systems_problems_new()
    remedies_systems_new()
    remedies()


if 'preparations':
    gen_preparations('teas')
    gen_preparations('tinctures')
    gen_preparations('capsules')


# if 'preparations':
#     remedies_systems_problems_preparations('teas')
#     remedies_systems_problems_preparations('tinctures')
#     remedies_systems_problems_preparations('capsules')

# if 'herbs':
#     herbs_medicine_benefits()
#     herbs_medicine()
#     herbs_pages()


# sitemap.sitemap_all()
# shutil.copy2('sitemap.xml', 'website/sitemap.xml')


shutil.copy2('style.css', 'website/style.css')
shutil.copy2('util.css', 'website/util.css')
shutil.copy2('assets/images/healing-herbs.jpg', 'website/images/healing-herbs.jpg')
shutil.copy2('pinterest-3e4f1.html', 'website/pinterest-3e4f1.html')
