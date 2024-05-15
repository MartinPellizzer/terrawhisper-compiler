import os
import time
import shutil
import markdown
import random
from PIL import Image, ImageDraw, ImageFont

import g
import util
import utils_ai
import sitemap

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

problems_related_rows = util.csv_get_rows(g.CSV_PROBLEMS_RELATED_FILEPATH)
problems_related_cols = util.csv_get_cols(problems_related_rows)
problems_related_rows = problems_related_rows[1:]


teas_num = 10
ART_ITEMS_NUM = 10


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






# #########################################################
# PREPARATIONS
# #########################################################



# JSONs

def json_preparation_system_problem_intro(json_filepath, data):
    key = 'intro_desc'
    if key not in data:
        problem_id = data['problem_id']
        problem_slug = data['problem_slug']
        problem_name = data['problem_name']
        preparation_name = data['preparation_name']

        herbs_rows_filtered = []
        if preparation_name == 'infusions': herbs_rows_filtered = csv_get_teas_by_problem(problem_id)[:teas_num]
        elif preparation_name == 'tinctures': herbs_rows_filtered = csv_get_tinctures_by_problem(problem_id)[:teas_num]

        herbs_names = [row[herbs_cols['herb_name_common']] for row in herbs_rows_filtered]
        herbs_names_prompt = ', '.join(herbs_names)

        # prompt = f'''
        #     Write 1 paragraph on the best herbal {preparation_name} for {problem_name}.
        #     Write the names of the best herbal {preparation_name} for {problem_name} that are {herbs_names_prompt}.
        #     Explain what are the primary properties of herbal {preparation_name} that help with {problem_name}.
        #     Explain how herbal {preparation_name} can improve the lives of people with {problem_name} and include examples.
        #     Start the reply with the following words: The best herbal {preparation_name} for {problem_name} are .
        #     Never use the following words: can, may, might.
        # '''
        prompt = f'''
            Write 1 detailed paragraph on the herbal {preparation_name} for {problem_name}.
            In the first sentence, give a detailed definition of "herbal {preparation_name} for {problem_name}", including why they help with {problem_name}.
            Explain how herbal {preparation_name} helps with {problem_name}.
            Include many examples of how herbal {preparation_name} for {problem_name} improves lives.
            Don't write the names of the herbs.
            Don't talk about other ailments.
            Start the reply with the following words: Herbal {preparation_name} for {problem_name} are .
            Never use the following words: can, may, might.
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


def json_preparation_system_problem_list(json_filepath, data):
    problem_id = data['problem_id']
    problem_name = data['problem_name']
    problem_slug = data['problem_slug']
    preparation_name = data['preparation_name']

    if preparation_name == 'teas': herbs_rows_filtered = csv_get_teas_by_problem(problem_id)
    if preparation_name == 'tinctures': herbs_rows_filtered = csv_get_tinctures_by_problem(problem_id)

    key = 'remedies_list'
    if key not in data: data[key] = []
    for herb_row in herbs_rows_filtered:
        herb_id = herb_row[herbs_cols['herb_id']].strip()
        herb_slug = herb_row[herbs_cols['herb_slug']].strip()
        herb_name_common = herb_row[herbs_cols['herb_name_common']].strip()
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

    # # del old
    # data_filtered = []
    # for tea_obj in data['teas']: 
    #     found = False
    #     for tea_row in teas_rows[1:]:
    #         tea_condition_id = tea_row[teas_cols['condition_id']].strip().lower()
    #         tea_name = tea_row[teas_cols['tea_name']].strip().lower()
    #         if tea_condition_id != condition_id: continue
    #         if tea_obj['tea_name'] == tea_name: 
    #             found = True
    #             break
    #     if found:
    #         data_filtered.append(tea_obj)

    # data['teas'] = data_filtered
    # util.json_write(json_filepath, data)

    # AI
    for obj in data[key][:teas_num]:
        remedy_name = obj["herb_name_common"].strip().lower()
        if preparation_name == 'teas': remedy_name = f'{remedy_name} tea'.replace(' tea tea', ' tea')
        elif preparation_name == 'tinctures': remedy_name = f'{remedy_name} tincture'

        key = 'remedy_desc'
        if key not in obj or obj[key] == []:
            prompt = f'''
                Explain 1 paragraph on why {remedy_name} helps with {problem_name}.
                Start the reply with the following words: {remedy_name.capitalize()} helps with {problem_name} because .
                Never use the following words: can, may, might.
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = utils_ai.reply_to_paragraphs(reply)
            if len(reply) == 1 and reply != '':
                print('********************************')
                print(reply)
                print('********************************')
                obj[key] = reply[0]
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
            
        # key = 'remedy_constituents'
        # if key not in obj or obj[key] == []:
        #     prompt = f'''
        #         Write a numbered list of the most important medicinal constituents of {remedy_name} that help with {problem_name}.
        #         Include 1 short sentence description for each of these medicinal constituents, explaining why that medicinal contituent is good for {problem_name}.
        #         Include only medicinal constituents that have short names.
        #         Don't include the name of the plant in the constituents names.
        #         Write each list element using the following format: [constituent name]: [constituent description].
        #         Never use the following words: can, may, might.
        #     '''
        #     reply = utils_ai.gen_reply(prompt)
        #     reply = utils_ai.reply_to_list_column(reply)
        #     reply = [line.replace('[', '').replace(']', '') for line in reply]
        #     if reply != '' and reply != []:
        #         print('********************************')
        #         print(reply)
        #         print('********************************')
        #         obj[key] = reply
        #         util.json_write(json_filepath, data)
        #     time.sleep(g.PROMPT_DELAY_TIME)



        key = 'remedy_properties'
        if key not in obj or obj[key] == []:
            prompt = f'''
                Write a numbered list of the most important medicinal properties of {herb_name_common} that help with {problem_name}.
                For each medicinal property, explain in 1 short sentence why that property is important for {problem_name} and what active constituents give that property. 
                Write each list element using the following format: [medicinal propertie]: [property description].
            '''
            reply = utils_ai.gen_reply(prompt)
            reply = utils_ai.reply_to_list_column(reply)
            reply = [line.replace('[', '').replace(']', '') for line in reply]
            if reply != '' and reply != []:
                print('********************************')
                print(reply)
                print('********************************')
                obj[key] = reply
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)
        
        # quit()

        

        

        key = 'remedy_parts'
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
                Never use the following words: can, may, might.
            '''     
            reply = utils_ai.gen_reply(prompt)
            reply = utils_ai.reply_to_list_column(reply)
            if reply != '' and reply != []:
                print('********************************')
                print(reply)
                print('********************************')
                obj[key] = reply
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)

        key = 'remedy_recipe'
        if key not in obj or obj[key] == []:
            prompt = f'''
                Write a 5-step recipe in list format to make {remedy_name} for {problem_name}.
                Include ingredients dosages and preparations times.
                Write only 1 sentence for each step.
                Start each step in the list with an action verb.
                Don't include optional steps.
                Never use the following words: can, may, might.
            '''  
            reply = utils_ai.gen_reply(prompt)
            reply = utils_ai.reply_to_list(reply)
            if reply != '' and reply != [] and len(reply) == 5:
                print('********************************')
                print(reply)
                print('********************************')
                obj[key] = reply
                util.json_write(json_filepath, data)
            time.sleep(g.PROMPT_DELAY_TIME)

        # TODO: gen study


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

    key = 'supplementary_frequency'
    if key not in data:
        prompt = f'''
            How frequently should you drink herbal {preparation_name} for {problem_name}? Explain why in detail.
            Include numbers.
            Don't include names of herbs.
            Don't include side effects.
            Don't include precautions.
            Don't metions sources of informations.
            Reply in a short paragraph of about 60 to 80 words.
            Start the reply with the following words: For {problem_name}, you should drink herbal {preparation_name} .
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



# IMGs

def img_preparation_systems_problems_featured(data):
    if 'remedies_list' in data:
        problem_slug = data['problem_slug']
        preparation_name = data['preparation_name'].lower()
        preparation_slug = preparation_name.replace(' ', '-')
        obj = data['remedies_list'][0]
        herb_name_common = obj['herb_name_common'].split(',')[0].strip()
        herb_name_common_slug = herb_name_common.replace(' ', '-').replace("'", '-').replace(".", '')

        image_filepath_out = f'website/images/herbal-{preparation_slug}-for-{problem_slug}-overview.jpg'
        if not os.path.exists(image_filepath_out):
            images_folderpath = f'C:/terrawhisper-assets/images/{preparation_slug}/{herb_name_common_slug}'
            if os.path.exists(images_folderpath):
                images_filepaths = [f'{images_folderpath}/{filename}' for filename in os.listdir(images_folderpath)] 
                image_filepath = random.choice(images_filepaths)
                if image_filepath != '':
                    util.image_variate(image_filepath, image_filepath_out)
            else:
                print(f'IMG FOLDER MISSING: {images_folderpath}')
    else:
        print(f'MISSING KEY remedy_list: {preparation_slug} {problem_slug}')


def img_preparation_systems_problems_list(data):
    if 'remedies_list' in data:
        problem_slug = data['problem_slug']
        preparation_name = data['preparation_name'].lower()
        preparation_name_singular = ''
        if preparation_name == 'teas': preparation_name_singular = 'tea'
        elif preparation_name == 'tinctures': preparation_name_singular = 'tincture'
        else: print(f'MISSING VALID preparation_name: {preparation_name} {problem_slug}')
        preparation_slug = preparation_name.replace(' ', '-')
        preparation_slug_singular = preparation_name_singular.replace(' ', '-')

        for i, obj in enumerate(data['remedies_list'][:teas_num]):
            herb_name_common = obj['herb_name_common'].split(',')[0].strip()
            herb_name_common_slug = herb_name_common.replace(' ', '-').replace("'", '-').replace(".", '')

            image_filepath_out = f'website/images/{herb_name_common_slug}-{preparation_slug_singular}-for-{problem_slug}.jpg'
            if not os.path.exists(image_filepath_out):
                images_folderpath = f'C:/terrawhisper-assets/images/{preparation_slug}/{herb_name_common_slug}'
                if os.path.exists(images_folderpath):
                    images_filepaths = [f'{images_folderpath}/{filename}' for filename in os.listdir(images_folderpath)] 
                    image_filepath = random.choice(images_filepaths)
                    if image_filepath != '':
                        util.image_variate(image_filepath, image_filepath_out)
                else:
                    print(f'IMG FOLDER MISSING: {images_folderpath}')
    else:
        print(f'MISSING KEY remedy_list: {preparation_slug} {problem_slug}')


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

    img = Image.new(mode="RGB", size=(img_width, img_height), color='#ece3d8')

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
    draw.rectangle(((x, y), (x + text_w + px*2, y + text_h + py*2)), fill="#4c5e58")
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
        text,
        (0, 0, 0), font=font
    )

    y = y_start

    remedies_list = data['remedies_list']
    for i, remedy_obj in enumerate(remedies_list[:10]):
        herb_name_common = remedy_obj['herb_name_common']
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
        draw.rectangle(((x, y), (w, y + cell_herb_h)), fill="#4c5e58")
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Bold.ttf", 48)
        draw.text(
            (x + text_margin_l, y + text_margin_t), 
            f'{i+1}. {herb_name_common.upper()}', 
            (255, 255, 255), font=font
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
            '#000000', font=font
        )
        y += cell_category_h

        # Properties Vals
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 36)
        for item in remedy_properties:
            item = item.replace('properties', '')
            draw.rectangle(((x, y), (w, y + h)), fill="#ece3d8")
            draw.rectangle((
                (x + text_margin_l + 16, y + h//2 - 16), 
                (x + text_margin_l + 32, y + h//2)), fill="#000000")
            draw.text(
            (x + text_margin_l + 48, y), 
                item, 
                '#000000', font=font
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
            'Plant Parts', 
            '#000000', font=font
        )
        y += cell_category_h

        # Parts Vals
        font = ImageFont.truetype("assets/fonts/Lato/Lato-Regular.ttf", 36)
        for item in remedy_parts:
            draw.rectangle(((x, y), (w, y + h)), fill="#ece3d8")
            draw.rectangle((
                (x + text_margin_l + 16, y + h//2 - 16), 
                (x + text_margin_l + 32, y + h//2)), fill="#000000")
            draw.text(
            (x + text_margin_l + 48, y), 
                item, 
                '#000000', font=font
            )
            y += h

        y += h
        
        
    
    img.save(image_filepath_out, quality=50) 
    print(image_filepath_out)
    # img.show()

    # quit()



# HTMLs

def html_preparation_system_problem_intro(html_filepath, data):
    key = 'intro_desc'
    article_html = ''

    title = data['title'].title()
    problem_slug = data['problem_slug']
    problem_name = data['problem_name']
    preparation_name = data['preparation_name']
    preparation_slug = preparation_name.replace(' ', '-')

    article_html += f'<h1>{title}</h1>\n'

    img_src = f'/images/herbal-{preparation_slug}-for-{problem_slug}-overview.jpg'
    img_alt = f'herbal {preparation_name} for {problem_name} overview.jpg'
    try: article_html += f'<p><img src="{img_src}" alt="{img_alt}"></p>\n'
    except: print(f'MISSING TEA IMAGE: {problem_name} >> {tea_image_url}')

    if key in data:
        intro = data[key]
        article_html += f'{util.text_format_1N1_html(intro)}\n'
    else: 
        print(f'MISSING INTRO: {html_filepath} >> {problem_name}')
    
    article_html += f'<p>A summary of the 10 best herbal {preparation_name} for {problem_name} is provided in the following cheatsheet.</p>\n'

    img_src = f'/images/herbal-{preparation_slug}-for-{problem_slug}-cheatsheet.jpg'
    img_alt = f'herbal {preparation_name} for {problem_name} cheatsheet.jpg'
    article_html += f'<p><img src="{img_src}" alt="{img_alt}"></p>\n'

    article_html += f'<p>The following article describes in detail the most important teas for {problem_name}, including medicinal properties, parts of herbs to use, and recipes for preparations.</p>\n'

    return article_html


# adjust it for tincures
def html_preparation_system_problem_list(html_filepath, data):
    article_html = ''
    problem_slug = data['problem_slug']
    problem_name = data['problem_name']
    preparation_name = data['preparation_name']
    preparation_name_singular = data['preparation_name_singular']
    preparation_slug = data['preparation_slug']

    for i, remedy_obj in enumerate(data['remedies_list'][:teas_num]):
        herb_slug = remedy_obj['herb_slug'].strip().lower()
        herb_name_common = remedy_obj['herb_name_common'].strip().lower()
        herb_name_common_slug = herb_name_common.replace(' ', '-').replace("'", '-')

        remedy_name = remedy_obj["herb_name_common"].strip().lower()
        remedy_name_preparation = remedy_name
        if preparation_slug == 'tea': remedy_name_preparation = f'{remedy_name_preparation} tea'.replace(' tea tea', ' tea')
        elif preparation_slug == 'tincture': remedy_name_preparation = f'{remedy_name_preparation} tincture'

        article_html += f'<h2>{i+1}. {remedy_name_preparation.capitalize()}</h2>\n'
        try: article_html += f'<p>{util.text_format_1N1_html(remedy_obj["remedy_desc"])}</p>\n'
        except: print(f'MISSING REMEDY DESC: {html_filepath} >> {problem_name} >> {remedy_name_preparation}')

        img_src = f'/images/{herb_name_common_slug}-{preparation_slug}-for-{problem_slug}.jpg'
        img_alt = f'{herb_name_common} {preparation_name_singular} for {problem_name}.jpg'
        try: article_html += f'<p><img src="{img_src}" alt="{img_alt}"><p>\n'
        except: print(f'MISSING REMEDY IMAGE: {problem_name} >> {tea_image_url}')
            
        try:
            tea_constituents = remedy_obj['remedy_properties']
            article_html += f'<p>The list below shows the primary active constituents in {remedy_name} that aid with {problem_name}.</p>\n'
            article_html += '<ul>\n'
            for tea_constituent in tea_constituents:
                chunk_1 = tea_constituent.split(': ')[0]
                chunk_2 = ': '.join(tea_constituent.split(': ')[1:])
                article_html += f'<li><strong>{chunk_1.capitalize()}</strong>: {chunk_2}</li>\n'
            article_html += '</ul>\n'
        except: print(f'MISSING REMEDY CONSTITUENTS: {problem_name} >> {remedy_name}')

        try:
            tea_parts = remedy_obj['remedy_parts']
            article_html += f'<p>Right below you will find a list of the most important parts in {remedy_name} that help with {problem_name}.</p>\n'
            article_html += '<ul>\n'
            for tea_part in tea_parts:
                chunk_1 = tea_part.split(': ')[0]
                chunk_2 = ': '.join(tea_part.split(': ')[1:])
                article_html += f'<li><strong>{chunk_1.capitalize()}</strong>: {chunk_2}</li>\n'
            article_html += '</ul>\n'
        except: print(f'MISSING REMEDY PARTS: {problem_name} >> {remedy_name}')

        try:
            tea_recipe = remedy_obj['remedy_recipe']
            article_html += f'<p>The following recipe gives a procedure to make a basic {remedy_name_preparation} for {problem_name}.</p>\n'
            article_html += '<ol>\n'
            for step in tea_recipe:
                article_html += f'<li>{step}</li>\n'
            article_html += '</ol>\n'
        except: print(f'MISSING REMEDY RECIPE: {problem_name} >> {remedy_name}')

    return article_html


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
        text = text.replace(problem_name, f'<a href="/ailments/{system_slug}/{problem_slug}.html">{problem_name}</a>', 1)

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
                text = text.replace(link_problem_name, f'<a href="/herbalism/{preparation_slug}/{link_system_slug}/{link_problem_slug}.html">{link_problem_name}</a>', 1)

        article_html += f'{util.text_format_1N1_html(text)}\n'

    return article_html

# EXE

def art_tea_systems_problems():
    preparation_name = 'teas'
    preparation_name_singular = 'tea'
    preparation_slug = 'tea'
    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        preparations_rows_filtered = csv_get_preparations_by_problem(problem_id)
        preparations_names = [row[preparations_cols['preparation_name']] for row in preparations_rows_filtered]
        if 'infusions' not in preparations_names: continue

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

        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)
        data['problem_id'] = problem_id
        data['problem_slug'] = problem_slug
        data['problem_name'] = problem_name
        data['system_id'] = system_id
        data['system_slug'] = system_slug
        data['system_name'] = system_name
        data['preparation_name'] = preparation_name
        data['preparation_name_singular'] = preparation_name_singular
        data['preparation_slug'] = preparation_slug

        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 

        data['url'] = f'herbalism/tea/{system_slug}/{problem_slug}'
        
        data['remedy_num'] = teas_num
        title = f'{teas_num} Best herbal teas for {problem_name}'
        data['title'] = title

        util.json_write(json_filepath, data)

        # JSON
        json_preparation_system_problem_intro(json_filepath, data)
        json_preparation_system_problem_list(json_filepath, data)
        json_preparation_system_problem_supplementary(json_filepath, data)

        # IMG
        img_preparation_systems_problems_featured(data)
        img_preparation_systems_problems_list(data)
        img_preparation_systems_problems_cheatsheet(data)

        # HTML
        html_filepath = f'website/herbalism/tea/{system_slug}/{problem_slug}.html'

        data = util.json_read(json_filepath)

        article_html = ''
        article_html += html_preparation_system_problem_intro(html_filepath, data)
        article_html += html_preparation_system_problem_list(html_filepath, data)
        article_html += html_preparation_system_problem_supplementary(html_filepath, data)

        header_html = util.header_default()
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

        # # GEN TEAS HTML TOO FOR OLD REDIRECTS
        # condition_slug_old = condition_slug.split('/')[-1].strip()
        # html_filepath = f'website/herbalism/teas/{condition_slug_old}.html'

        # header_html = util.header_default()
        # breadcrumbs_html = util.breadcrumbs(html_filepath)
        # meta_html = util.article_meta(article_html, lastmod)
        # article_html = util.article_toc(article_html)

        # html = f'''
        #     <!DOCTYPE html>
        #     <html lang="en">

        #     <head>
        #         <head>\n<meta http-equiv="refresh" content="0; url=https://terrawhisper.com/herbalism/tea/{condition_slug}.html">
        #         <meta charset="UTF-8">
        #         <meta name="viewport" content="width=device-width, initial-scale=1.0">
        #         <meta name="author" content="{g.AUTHOR_NAME}">
        #         <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
        #         <link rel="stylesheet" href="/style.css">
        #         <title>{title}</title>
        #         {g.GOOGLE_TAG}
                
        #     </head>

        #     <body>
        #         {header_html}
        #         {breadcrumbs_html}
                
        #         <section class="article-section">
        #             <div class="container">
        #                 {meta_html}
        #                 {article_html}
        #             </div>
        #         </section>

        #         <footer>
        #             <div class="container-lg">
        #                 <span>© TerraWhisper.com 2024 | All Rights Reserved
        #             </div>
        #         </footer>
        #     </body>

        #     </html>
        # '''
        # util.file_write(html_filepath, html)


        # # REDIRECTS
        # condition_slugs_prev_list = condition_slugs_prev.split(',')
        # for condition_slug_prev in condition_slugs_prev_list:
        #     print(condition_slug_prev)
        #     if condition_slug_prev == condition_slug: continue
        #     html_filepath_out = f'website/herbalism/tea/{condition_slug_prev}.html'
        #     html_filepath_web = f'https://terrawhisper.com/herbalism/tea/{condition_slug}.html'
        #     html = util.file_read(html_filepath_out)
        #     if os.path.exists(html_filepath_out):
        #         if f'<meta http-equiv="refresh" content="0; url={html_filepath_web}">' not in html:
        #             html = html.replace(
        #                 '<head>',
        #                 f'<head>\n<meta http-equiv="refresh" content="0; url={html_filepath_web}">'
        #             )
        #     util.file_write(html_filepath_out, html)



# TODO: fast - all tea instances to tinctures, including images
def art_tincture_systems_problems():
    preparation_name = 'tinctures'
    preparation_name_singular = 'tincture'
    preparation_slug = 'tincture'
    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue
        
        preparations_rows_filtered = csv_get_preparations_by_problem(problem_id)
        preparations_names = [row[preparations_cols['preparation_name']] for row in preparations_rows_filtered]
        if 'tinctures' not in preparations_names: continue

        print(f'> {problem_name}')

        system_row = csv_get_system_by_problem(problem_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        print(f'  > {system_name}')

        json_filepath = f'database/json/herbalism/{preparation_slug}/{system_slug}/{problem_slug}.json'

        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)
        data['problem_id'] = problem_id
        data['problem_slug'] = problem_slug
        data['problem_name'] = problem_name
        data['system_id'] = system_id
        data['system_slug'] = system_slug
        data['system_name'] = system_name
        data['preparation_name'] = preparation_name
        data['preparation_name_singular'] = preparation_name_singular
        data['preparation_slug'] = preparation_slug

        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 

        data['url'] = f'herbalism/tincture/{system_slug}/{problem_slug}'

        data['remedies_num'] = ART_ITEMS_NUM
        title = f'{ART_ITEMS_NUM} best herbal tinctures for {problem_name}'
        data['title'] = title

        util.json_write(json_filepath, data)

        # JSON
        json_preparation_system_problem_intro(json_filepath, data)
        json_preparation_system_problem_list(json_filepath, data)
        json_preparation_system_problem_supplementary(json_filepath, data)

        # IMG
        img_preparation_systems_problems_featured(data)
        img_preparation_systems_problems_list(data)
        img_preparation_systems_problems_cheatsheet(data)
        
        # HTML
        html_filepath = f'website/herbalism/{preparation_slug}/{system_slug}/{problem_slug}.html'

        data = util.json_read(json_filepath)

        
        html_filepath = f'website/herbalism/{preparation_slug}/{system_slug}/{problem_slug}.html'

        data = util.json_read(json_filepath)

        article_html = ''
        article_html += html_preparation_system_problem_intro(html_filepath, data)
        article_html += html_preparation_system_problem_list(html_filepath, data)
        article_html += html_preparation_system_problem_supplementary(html_filepath, data)


        
        header_html = util.header_default()
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





# #########################################################
# ARTICLES - PROBLEMS
# #########################################################

def json_ailments_systems_problems_intro(json_filepath, data):
    key = 'intro'
    if key not in data:
        problem_name = data['problem_name']
        prompt = f'''
            Write 1 paragraph about the best herbal teas for {problem_name}.
            Include a brief definition of: {problem_name}.
            Include the negative impacts of {problem_name} in people lives. 
            Include the causes of {problem_name}. 
            Include the medicinal herbs and they preparations for {problem_name}. 
            Include the precautions when using herbs medicinally for {problem_name}. 
            Never use the following words: can, may, might.
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


def json_ailments_systems_problems_definition(json_filepath, data):
    key = 'definition'
    if key not in data:
        problem_name = data['problem_name']
        prompt = f'''
            Write 1 paragraph explaining what is {problem_name} and include many examples on how it affects negatively your life.
            Don't mention the casuses of {problem_name}.
            Never use the following words: can, may, might.
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


def json_ailments_systems_problems_causes(json_filepath, data):
    key = 'causes_desc'
    if key not in data:
        problem_name = data['problem_name']
        prompt = f'''
            Write 1 paragraph explaining what are the main causes of {problem_name}.
            Start the reply with the following words: The main causes of {problem_name} are .
            Never use the following words: can, may, might.
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
        
    causes_num = 10
    key = 'causes_list'
    if key not in data:
        problem_name = data['problem_name']

        prompt = f'''
            Write a numbered list of the {causes_num} most common causes of {problem_name}.
            Include a short description for each cause.
            Reply with the following format: [cause name]: [description].
            Never use the following words: can, may, might.
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


def json_ailments_systems_problems_herbs(json_filepath, data):
    herbs_num = 10

    key = 'herbs_desc'
    if key not in data:
        problem_id = data['problem_id']
        problem_name = data['problem_name']

        herbs_rows_filtered = csv_get_herbs_by_problem(problem_id)
        herbs_common_names = [row[herbs_cols['herb_name_common']] for row in herbs_rows_filtered]
        herbs_common_names_prompt = ', '.join(herbs_common_names[:5])

        prompt = f'''
            Write 1 paragraph explaining what medicinal herbs helps with {problem_name} and why.
            Include some of the following herbs: {herbs_common_names_prompt}.
            Start the reply with the following words: The best medicinal herbs for {problem_name} are .
            Never use the following words: can, may, might.
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

    key = 'herbs_list'
    if key not in data:
        problem_id = data['problem_id']
        problem_name = data['problem_name']

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
            Never use the following words: can, may, might.
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


def json_ailments_systems_problems_preparations(json_filepath, data):
    key = 'preparations_desc'
    if key not in data:
        problem_id = data['problem_id']
        problem_name = data['problem_name']

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
            Never use the following words: can, may, might.
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

    key = 'preparations_list'
    if key not in data:
        problem_id = data['problem_id']
        problem_name = data['problem_name']

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
            Never use the following words: can, may, might.
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


def json_ailments_systems_problems_precautions(json_filepath, data):
    key = 'precautions_desc'
    if key not in data:
        problem_name = data['problem_name']
        prompt = f'''
            Write 1 paragraph about the precautions to take when using herbal remedies for {problem_name}.
            Never use the following words: can, may, might.
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

    key = 'precautions_list'
    if key not in data:
        problem_id = data['problem_id']
        problem_name = data['problem_name']

        prompt = f'''
            Write a numbered list of precautions to take when using herbal remedies for {problem_name}.
            Start each precaution with an action verb.
            Never use the following words: can, may, might.
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

        if len(lines_formatted) >= 4:
            print('***************************************')
            print(lines_formatted)
            print('***************************************')
            data[key] = lines_formatted
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)
        

def json_ailments_systems_problems_other_remedies(json_filepath, data):
    key = 'other_remedies_desc'
    if key not in data:
        problem_name = data['problem_name']
        prompt = f'''
            Write 1 paragraph about the natural remedies for {problem_name}, without including herbal remedies.
            Never use the following words: can, may, might.
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

    items_num = 10
    key = 'other_remedies_list'
    if key not in data:
        problem_id = data['problem_id']
        problem_name = data['problem_name']

        prompt = f'''
            Write a numbered list of the {items_num} most effective natural remedies for {problem_name}, without including herbal remedies.
            Start each natural remedy with an action verb.
            Each list item must have the following format: [natural remedy]: [description].
            Never use the following words: can, may, might.
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

        print(f'num lines formatted in reply >> {len(lines_formatted)}')
        if len(lines_formatted) == items_num:
            print('***************************************')
            print(lines_formatted)
            print('***************************************')
            data[key] = lines_formatted
            util.json_write(json_filepath, data)

        time.sleep(g.PROMPT_DELAY_TIME)


def html_ailments_systems_problems_other_remedies(data):
    problem_name = data['problem_name']
    other_remedies_desc = data['other_remedies_desc']

    article_html = ''
    
    article_html += f'<h2>What natural remedies to use with medicinal herbs for {problem_name}?</h2>\n'
    article_html += f'{util.text_format_1N1_html(other_remedies_desc)}\n'
    article_html += f'<p>The most effective natural remedies to use in conjunction with herbal medicine that help with {problem_name} are listed below.</p>\n'
    article_html += f'<ul>\n'
    for item in data['other_remedies_list']:
        chunks = item.split(':')
        chunk_1 = f'<strong>{chunks[0]}</strong>\n'
        chunk_2 = ':'.join(chunks[1:])
        article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
    article_html += f'</ul>\n'

    return article_html


def html_ailments_systems_problems_intro(data):
    title = ''
    intro = ''
    problem_name = ''

    if 'title' in data: title = data['title']
    else: print(f'MISSING TITLE: ailments_systems_problems -- {problem_name}')
    if 'intro' in data: intro = data['intro']
    else: print(f'MISSING INTRO: ailments_systems_problems -- {problem_name}')
    if 'problem_name' in data: problem_name = data['problem_name']
    else: print(f'MISSING PROBLEM_NAME: ailments_systems_problems -- {problem_name}')

    article_html = ''

    article_html += f'<h1>{title}</h1>\n'
    article_html += f'{util.text_format_1N1_html(intro)}\n'
    article_html += f'<p>This article explains in detail what {problem_name} is, how it affects your life and what are its causes. Then, it lists what medicinal herbs to use to relieve this problem and how to prepare these herbs to get the best results. Lastly, it revals what other natural remedies to use in conjunction with herbal medicine to aid with this problem.</p>\n'

    return article_html


def art_ailments_systems_problems():
    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        print(f'>> {problem_id} - {problem_name}')
        
        problem_system_row = util.csv_get_rows_filtered(
            g.CSV_PROBLEMS_SYSTEMS_FILEPATH, 
            problems_systems_cols['problem_id'], 
            problem_id
        )[0]

        system_row = util.csv_get_rows_filtered(
            g.CSV_SYSTEMS_NEW_FILEPATH, 
            systems_cols['system_id'], 
            problem_system_row[problems_systems_cols['system_id']]
        )[0]

        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        print(f'    {system_id} - {system_name}')



        # json
        json_filepath = f'database/json/problems/{system_slug}/{problem_slug}.json'
        print(json_filepath)

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



        # sections
        json_ailments_systems_problems_intro(json_filepath, data)
        json_ailments_systems_problems_definition(json_filepath, data)
        json_ailments_systems_problems_causes(json_filepath, data)
        json_ailments_systems_problems_herbs(json_filepath, data)

        json_ailments_systems_problems_preparations(json_filepath, data)
        json_ailments_systems_problems_precautions(json_filepath, data)
        json_ailments_systems_problems_other_remedies(json_filepath, data)



        # html
        html_filepath = f'website/ailments/{system_slug}/{problem_slug}.html'

        data = util.json_read(json_filepath)

        article_html = ''
        article_html += html_ailments_systems_problems_intro(data)

        article_html += f'<h2>What is {problem_name} and how it affects your life?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["definition"])}\n'
        
        article_html += f'<h2>What are the main causes of {problem_name}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["causes_desc"])}\n'
        if 'causes_list' in data:
            article_html += f'<p>The most common causes of {problem_name} are listed below.</p>\n'
            article_html += f'<ul>\n'
            for item in data['causes_list']:
                chunks = item.split(':')
                chunk_1 = f'<strong>{chunks[0]}</strong>\n'
                chunk_2 = ':'.join(chunks[1:])
                article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
            article_html += f'</ul>\n'
        else: print(f'MISSING cause_list >> {json_filepath}')
        
        article_html += f'<h2>What are the best medicinal herbs for {problem_name}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["herbs_desc"])}\n'
        if 'causes_list' in data:
            article_html += f'<p>The most effective medicinal herbs that help with {problem_name} are listed below.</p>\n'
            article_html += f'<ul>\n'
            if 'herbs_list' in data:
                for item in data['herbs_list']:
                    chunks = item.split(':')
                    chunk_1 = f'<strong>{chunks[0]}</strong>\n'
                    chunk_2 = ':'.join(chunks[1:])
                    article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
                article_html += f'</ul>\n'
        else: print(f'MISSING causes_list >> {json_filepath}')
        
        article_html += f'<h2>What are the most effective herbal preparations for {problem_name}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["preparations_desc"])}\n'
        if 'preparations_list' in data:
            article_html += f'<p>The most used herbal preparations that help with {problem_name} are listed below.</p>\n'
            article_html += f'<ul>\n'
            for item in data['preparations_list']:
                chunks = item.split(':')
                chunk_1 = chunks[0]
                chunk_2 = ':'.join(chunks[1:])
                if chunk_1.lower().strip() == 'infusions':
                    chunk_1 = f'<strong><a href="/herbalism/tea/{system_slug}/{problem_slug}.html">{chunk_1}</a></strong>'
                elif chunk_1.lower().strip() == 'tinctures':
                    chunk_1 = f'<strong><a href="/herbalism/tincture/{system_slug}/{problem_slug}.html">{chunk_1}</a></strong>'
                else:
                    chunk_1 = f'<strong>{chunk_1}</strong>'
                article_html += f'<li>{chunk_1}: {chunk_2}</li>\n'
            article_html += f'</ul>\n'
        else: print(f'MISSING preparations_list >> {json_filepath}')


        article_html += f'<h2>What precautions to take when using herbal remedies for {problem_name}?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["precautions_desc"])}\n'
        if 'precautions_list' in data:
            article_html += f'<p>The most important precautions to take when using herbal remedies for {problem_name} are listed below.</p>\n'
            article_html += f'<ul>\n'
            for item in data['precautions_list']:
                article_html += f'<li>{item}</li>\n'
            article_html += f'</ul>\n'
        else: print(f'MISSING precautions_list >> {json_filepath}')

        article_html += html_ailments_systems_problems_other_remedies(data)

        header_html = util.header_default()
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





def json_ailments_intro(json_filepath, data):
    key = 'intro_desc'
    if key not in data:
        prompt = f'''
            Write 1 intro paragraph for an article about ailments an healing herbs.
            Start by explaining what are the impacts of ailments on people lives.
            Then explain why healing herbs can help with the most common ailments. 
            Finally explain that the rest of the article will reveal the most common ailments for each body system and what are the best herbs to get rid of those ailments.
            Never use the following words: can, may, might.
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


def json_ailments_definition(json_filepath, data):
    key = 'definition_desc'
    if key not in data:
        prompt = f'''
            Write 1 paragraph explaining what are ailments.
            Include a detailed definition of the word "ailments".
            Include an explanation on how ailments can affect your life.
            Include examples.
            Never use the following words: can, may, might.
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


def json_ailments_systems(json_filepath, data):
    key = 'systems'
    if key not in data: data[key] = []
    for system_row in systems_rows:
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        found = False
        for system_obj in data[key]:
            if system_obj['system_id'] == system_id:
                found = True
                break
        
        if not found:
            data[key].append({'system_id': system_id, 'system_slug': system_slug, 'system_name': system_name})

    util.json_write(json_filepath, data)

    key = 'system_desc'
    for system_obj in data['systems']:
        if key not in system_obj:
            system_id = system_obj['system_id']
            system_name = system_obj['system_name']

            problems_rows_filtered = csv_get_problems_by_system(system_id)
            if len(problems_rows_filtered) > 0:
                problems_names = [row[problems_cols['problem_names']].split(',')[0].strip() for row in problems_rows_filtered]
                problems_names_prompt = ', '.join(problems_names)
                problems_names_prompt = f'Include the following common ailments: {problems_names_prompt}'
            else:
                problems_names_prompt = ''

            prompt = f'''
                Write 1 paragraph about the most common ailments of the {system_name} and how they affect your life.
                {problems_names_prompt}.
                Include what herbs and herbal remedies to use to help the {system_name}.
                Start the reply with the following words: The most common ailments of the {system_name} are .
                Never use the following words: can, may, might.
            '''
            reply = utils_ai.gen_reply(prompt)

            reply = utils_ai.reply_to_paragraphs(reply)

            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                system_obj[key] = reply[0]
                util.json_write(json_filepath, data)

            time.sleep(g.PROMPT_DELAY_TIME)


def art_ailments():
    json_filepath = f'database/json/ailments.json'

    util.create_folder_for_filepath(json_filepath)
    util.json_generate_if_not_exists(json_filepath)
    data = util.json_read(json_filepath)

    lastmod = util.date_now()
    if 'lastmod' not in data: data['lastmod'] = lastmod
    else: lastmod = data['lastmod'] 

    title = f'What are the most common ailments and how to cure them with medicinal herbs'
    data['title'] = title

    util.json_write(json_filepath, data)

    # json art sections
    json_ailments_intro(json_filepath, data)
    json_ailments_definition(json_filepath, data)
    json_ailments_systems(json_filepath, data)



    html_filepath = 'website/ailments.html'

    data = util.json_read(json_filepath)

    article_html = ''

    article_html += f'<h1>{title}</h1>\n'
    article_html += f'{util.text_format_1N1_html(data["intro_desc"])}\n'

    article_html += f'<h2>What are ailments and how they affect your life?</h2>\n'
    article_html += f'{util.text_format_1N1_html(data["definition_desc"])}\n'

    for system_obj in data['systems']:
        system_id = system_obj['system_id']
        system_slug = system_obj['system_slug']
        system_name = system_obj['system_name']
        system_desc = system_obj['system_desc']

        article_html += f'<h2>{system_name.capitalize()} ailments</h2>\n'
        article_html += f'{util.text_format_1N1_html(system_desc)}\n'

        problems_rows_filtered = csv_get_problems_by_system(system_id)
        if len(problems_rows_filtered) > 0:
            article_html += f'The following link shows the <a href="/ailments/{system_slug}.html">most common ailments of the {system_name}</a> that you can alleviate with medicinal herbs.\n'

    header_html = util.header_default()
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
            <link rel="stylesheet" href="/util.css">
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





def json_ailments_systems_intro(json_filepath, data):
    key = 'intro_desc'
    if key not in data:
        system_name = data['system_name']
        prompt = f'''
            Write 1 intro paragraph for an article about {system_name} ailments an healing herbs.
            Start by explaining what are the impacts of the {system_name} ailments on people lives.
            Then explain why healing herbs can help with the most common {system_name} ailments. 
            Finally explain that the rest of the article will reveal the most common {system_name} ailments and what are the best herbs to get rid of those ailments.
            Never use the following words: can, may, might.
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


def json_ailments_systems_definition(json_filepath, data):
    key = 'definition_desc'
    if key not in data:
        system_name = data['system_name']
        prompt = f'''
            Write 1 paragraph explaining what are {system_name} ailments.
            Include a detailed definition of "{system_name} ailments".
            Include an explanation on how {system_name} ailments can affect your life.
            Include examples of {system_name} ailments.
            Never use the following words: can, may, might.
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


def json_ailments_systems_problems(json_filepath, data):
    key = 'problems'
    if key not in data: data[key] = []
    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue
        
        system_row = csv_get_system_by_problem(problem_id)
        if system_row[systems_cols['system_id']] != data['system_id']: continue

        found = False
        for problem_obj in data[key]:
            if problem_obj['problem_id'] == problem_id:
                found = True
                break
        
        if not found:
            data[key].append({'problem_id': problem_id, 'problem_slug': problem_slug, 'problem_name': problem_name})

    util.json_write(json_filepath, data)
        
    key = 'problem_desc'
    for problem_obj in data['problems']:
        # if key in problem_obj: del problem_obj[key]
        if key not in problem_obj:
            problem_id = problem_obj['problem_id']
            problem_name = problem_obj['problem_name']

            prompt = f'''
                Write 1 paragraph about what is {problem_name}, how it affects your life, and what are the medicinal herbs for {problem_name}.
                Start the reply with the following words: {problem_name.capitalize()} is .
                Never use the words "can", "may", and "might".
            '''
            reply = utils_ai.gen_reply(prompt)

            reply = utils_ai.reply_to_paragraphs(reply)

            print(len(reply))
            if len(reply) == 1:
                print('*******************************************')
                print(reply)
                print('*******************************************')
                problem_obj[key] = reply[0]
                util.json_write(json_filepath, data)

            time.sleep(g.PROMPT_DELAY_TIME)


def art_ailments_systems():
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

        # json
        json_filepath = f'database/json/problems/{system_slug}.json'

        util.create_folder_for_filepath(json_filepath)
        util.json_generate_if_not_exists(json_filepath)
        data = util.json_read(json_filepath)

        data['system_id'] = system_id
        data['system_slug'] = system_slug
        data['system_name'] = system_name

        lastmod = util.date_now()
        if 'lastmod' not in data: data['lastmod'] = lastmod
        else: lastmod = data['lastmod'] 

        title = f'{problems_num} Most common {system_name} ailments and how to treat them with herbal medicine'
        data['title'] = title

        util.json_write(json_filepath, data)

        # ai
        json_ailments_systems_intro(json_filepath, data)
        json_ailments_systems_definition(json_filepath, data)
        json_ailments_systems_problems(json_filepath, data)



        # html
        html_filepath = f'website/ailments/{system_slug}.html'

        data = util.json_read(json_filepath)

        article_html = ''
        article_html += f'<h1>{title}</h1>\n'
        article_html += f'{util.text_format_1N1_html(data["intro_desc"])}\n'

        for i, problem_obj in enumerate(data['problems']):
            problem_id = problem_obj['problem_id']
            problem_slug = problem_obj['problem_slug']
            problem_name = problem_obj['problem_name']
            problem_desc = problem_obj['problem_desc']

            problem_desc = problem_desc.replace(
                problem_name.capitalize(),
                f'<a href="/ailments/{system_slug}/{problem_slug}.html">{problem_name.capitalize()}</a>',
                1
            )

            article_html += f'<h2>{i+1}. {problem_name.capitalize()}</h2>\n'
            article_html += f'{util.text_format_1N1_html(problem_desc)}\n'


        article_html += f'<h2>What are {system_name} ailments and how they affect your life?</h2>\n'
        article_html += f'{util.text_format_1N1_html(data["definition_desc"])}\n'

        header_html = util.header_default()
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






# #########################################################
# PAGES
# #########################################################

def page_home():
    header = util.header_default()

    image_filepath_in = 'C:/terrawhisper-assets/images/home/medicinal-herbs.jpg'
    image_filepath_out = 'website/images/medicinal-herbs.jpg'

    util.image_save_resized(
        image_filepath_in, 
        image_filepath_out, 
        768,
        768,
        50,
    )
    
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

    

    slug = 'index'

    template = util.file_read(f'templates/{slug}.html')

    template = template.replace('[meta_title]', 'Herbalism & Natural Healing')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', header)
    template = template.replace('[teas_articles]', teas_articles_html)

    util.file_write(f'website/{slug}.html', template)


def page_herbalism():
    header = util.header_default()

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


def page_plants(regen_csv=False):
    json_filenames_plants_primary_secondary = [filename.lower().strip() for filename in os.listdir('database/articles/plants') if filename.endswith('.json')]
    # json_filenames_plants_treffle = [filename.lower().strip() for filename in os.listdir('database/articles/plants_trefle') if filename.endswith('.json')]
    
    json_filepaths_plants = [] 
    for filename in json_filenames_plants_primary_secondary: json_filepaths_plants.append(f'database/articles/plants/{filename}')
    # for filename in json_filenames_plants_treffle: json_filepaths_plants.append(f'database/articles/plants_trefle/{filename}')

    plants_list = []
    for filepath in json_filepaths_plants:
        filepath_in = f'{filepath}'
        data = util.json_read(filepath_in)
        plant_name = data['latin_name']
        plant_slug = data['entity']
        plants_list.append(f'<a href="/plants/{plant_slug}.html">{plant_name}</a>')

    plants_list = sorted(plants_list)
    plants_html = ''.join(plants_list)

    page_url = 'plants'
    article_filepath_out = f'website/{page_url}.html'
    breadcrumbs_html = util.breadcrumbs(article_filepath_out)

    template = util.file_read(f'templates/{page_url}.html')
    template = template.replace('[title]', 'Plants')
    template = template.replace('[google_tag]', g.GOOGLE_TAG)
    template = template.replace('[author_name]', g.AUTHOR_NAME)
    template = template.replace('[header]', util.header_default())
    template = template.replace('[breadcrumbs]', breadcrumbs_html)
    template = template.replace('[plants_num]', str(len(json_filepaths_plants)))
    template = template.replace('[items]', plants_html)
    util.file_write(article_filepath_out, template)

    # GENERATE CSV TO DOWNLOAD
    if regen_csv:
        rows = []
        for filepath in json_filepaths_plants:
            slug = filepath.split('/')[-1].split('.')[0].strip().lower()
            rows.append([slug])

        csv_plants_primary = util.csv_get_rows('database/tables/plants.csv')
        csv_plants_secondary = util.csv_get_rows('database/tables/plants-secondary.csv')
        csv_plants_trefle = util.csv_get_rows('database/tables/plants/trefle.csv')

        csv_plants = [] 
        for row in csv_plants_primary: csv_plants.append(row)
        for row in csv_plants_secondary: csv_plants.append(row)
        for row in csv_plants_trefle: csv_plants.append(row)

        rows_final = [['slug', 'scientific_name', 'common_name', 'genus', 'family']]
        for row in rows:
            for csv_plant in csv_plants:
                if csv_plant[0].strip().lower() == row[0].strip().lower():
                    rows_final.append(csv_plant)
                    break

        util.csv_set_rows('website/plants.csv', rows_final, delimiter=',')





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
# SIMULATE
# #########################################################


# #########################################################
# EXE
# #########################################################

page_home()
page_herbalism()
page_top_herbs()
page_plants(regen_csv=False)
page_about()
page_start_here()

art_ailments_systems_problems()
art_ailments_systems()
art_ailments()

art_tea_systems_problems()
art_tincture_systems_problems()


# sitemap.sitemap_all()
# shutil.copy2('sitemap.xml', 'website/sitemap.xml')



shutil.copy2('style.css', 'website/style.css')
shutil.copy2('util.css', 'website/util.css')
# shutil.copy2('assets/images/healing-herbs.jpg', 'website/images/healing-herbs.jpg')
