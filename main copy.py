# medicine >> benefits
    elif 'medicine' in attribute_1.lower() and 'benefits' in attribute_2.strip():
        title = f'10 Health Benefits of {common_name.capitalize()} ({latin_name.capitalize()})'
        article += f'# {title}\n\n'

        attribute_lst = ['medicine', 'benefits', 'overview']
        image_title = f'{common_name.capitalize()}\'s Medicinal Benefits'
        image_filepath = generate_featured_image(entity, attribute_lst, image_title)
        try:
            article += f'![{image_title}]({image_filepath} "{image_title}")\n\n'
        except: 
            print(f'WARNING: missing image ({entity})')

        article += get_content('medicine/benefits/_intro', f'database/articles/{entity}')
        article += f'This article explains in details the most important and well recognized health benefits of {common_name}, including what constituents are responsible for those benefits and what health condititions they can help.' + '\n\n'


        
        # benefits
        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]
        images_filenames = os.listdir(f'{image_folder_old}/{entity}/medicine/benefits')
        for i, item in enumerate(rows_filtered):
            if i < 10: num = f'0{i}'
            else: num = f'{i}'
        
            title_section = f'## {i+1}. {item.title()}\n\n'
            item_formatted = item.replace(' ', '-').lower()
            filename = f'{num}-{item_formatted}'
            filepath = f'medicine/benefits/{filename}'

            content_section = get_content(f'{filepath}', f'database/articles/{entity}').strip()
            content_section = content_section.replace(common_name.lower(), common_name.title())
            
            # image
            try:
                image_filepath = generate_image_template_medicine_benefits(entity, common_name, images_filenames[i], item,)
            except:
                image_filepath = generate_image_template_medicine_benefits_2(entity, common_name, images_filenames[i], item,)
            image_title = f'{common_name.title()} {item.title()}'
            image_section = f'![{image_title}]({image_filepath} "{image_title}")\n\n'

            item_words = item.split(' ')
            item_no_s = item_words[0][:-1] + ' ' + ' '.join(item_words[1: ])
            image_intro_line = f'The primary constituents and preparations that make {common_name} {item_no_s.lower()} are shown in the following illustration.'  + '\n\n'

            section_1 = content_section.split('\n')[0]  + '\n\n'
            section_rest = '\n'.join(content_section.split('\n')[1:])  + '\n\n'

            article += title_section + section_1 + image_intro_line + image_section + section_rest
            
        content = get_content_2(f'database/articles/{entity}/medicine/benefits/constituents.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## Which biochemical compounds of {common_name} contribute the most to health?' + '\n\n'
            tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
            tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'constituents']
            if tmp_rows: content = content.replace(f'biochemical compounds of {common_name.title()}', f'[biochemical compounds of {common_name.title()}](/{entity}/{attribute_1.lower()}/constituents.html)')
            article += content + '\n\n'

        content = get_content_2(f'database/articles/{entity}/medicine/benefits/preparations.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## How to properly use {common_name} to get its benefits?' + '\n\n'
            tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
            tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'preparations']
            if tmp_rows: content = content.replace(f'preparations of {common_name.title()}', f'[preparations of {common_name.title()}](/{entity}/{attribute_1.lower()}/preparations.html)')
            article += content + '\n\n'

        content = get_content_2(f'database/articles/{entity}/medicine/benefits/side-effects.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What health side effects can {common_name} have if used improperly?' + '\n\n'
            tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
            tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'side-effects']
            if tmp_rows: content = content.replace(f'side effects associated with {common_name.title()}', f'[side effects associated with {common_name.title()}](/{entity}/{attribute_1.lower()}/side-effects.html)')
            article += content + '\n\n'

        content = get_content_2(f'database/articles/{entity}/medicine/benefits/precautions.md')
        if content.strip() != '':
            article += f'## What precautions should you take before using {common_name} for medicinal purposes?' + '\n\n'
            article += content + '\n\n'





        # sections = ['medicine', 'cuisine', 'horticulture', 'botany', 'history']
        # for i, section in enumerate(sections):
        #     with open(f'database/articles/{entity}/{section}.md', encoding='utf-8') as f: content = f.read()
        #     content_paragraphs = content.split('\n')
        #     content_paragraphs = [x for x in content_paragraphs if x.strip() != '']
            
        #     paragraph_1 = content_paragraphs[0]
        #     paragraph_rest = content_paragraphs[1:]

        #     try: filepath = generate_image_template_3(
        #         entity, 
        #         common_name, 
        #         f'{image_folder}/{entity}/000{i}.jpg', 
        #         f'{section}', 
        #         f'database/tables/{section}.csv'
        #     )
        #     except:
        #         print(f'Missing Image: {entity} {section}') 
        #         filepath = ''

        #     section_title = ''
        #     if section == 'medicine': 
        #         section_title = f'What are the medicinal uses of {common_name}?'
        #         try:
        #             with open(f'database/articles/{entity}/medicine/_intro.md') as f: intro_content = f.read()
        #         except: 
        #             intro_content = ''
        #         if intro_content.strip() != '':
        #             image_intro = f'The following illustration lists the most important uses of <a href="/{entity}/medicine.html">{common_name} in medicine</a>.'
        #         else:
        #             image_intro = f'The following illustration lists the most important uses of {common_name} in medicine.'
        #     elif section == 'cuisine': 
        #         section_title = f'What are the culinary uses of {common_name}?'
        #         image_intro = f'The following illustration lists the most common uses of {common_name} for culinary purposes.'
        #     elif section == 'horticulture': 
        #         section_title = f'How to cultivate {common_name} in your garden?'
        #         image_intro = f'The following illustration lists the most important tips to cutlitvate {common_name}.'
        #     elif section == 'botany': 
        #         section_title = f'What is the botanical profile of {common_name}?'
        #         image_intro = f'The following illustration display the botanical profile of {common_name}.'
        #     elif section == 'history': 
        #         section_title = f'What are the historical uses of {common_name}?'
        #         image_intro = f'The following illustration lists the most well known historical uses of {common_name}.'
            
        #     article += f'<h2>{section_title.title()}</h2>'
        #     article += f'<p>{paragraph_1}</p>'
        #     article += f'<p>{image_intro}</p>'
        #     article += f'<img src="images/{entity}-{section}.jpg" alt="{latin_name.title()} {section.title()}">'
        #     for paragraph in paragraph_rest:
        #         article += f'<p>{paragraph}</p>'

        # title = f'What to know before using {common_name} ({latin_name.capitalize()})'.title()
        # article += f'<h1>{title}</h1>'

        # try:
        #     attribute_lst = ['overview']
        #     image_title = f'{common_name.capitalize()} Overview'
        #     filepath = generate_featured_image(entity, attribute_lst, image_title)
        #     article += f'![{image_title}]({filepath} "{image_title}")\n\n'
        # except: 
        #     print(f'WARNING: missing image ({entity})')
            
        # try: article += get_content('intro', f'database/articles/{entity}')
        # except: pass
        # try: article += get_content('_intro', f'database/articles/{entity}')
        # except: pass
        # article += f'This article gives an overview on the many uses of {common_name} and what you need to know before using it.' + '\n\n'

        
        # # benefits
        # title_section = f'## What are the medicinal uses of {common_name}?\n\n'
        # content_paragraphs = get_content_2(f'database/articles/{entity}/medicine.md').strip().split('\n')
        # image_intro = f'\n\nThe following illustration lists the most important uses of [{common_name} in medicine](/{entity}/medicine.html).\n\n'
        
        # rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
        # rows_filtered = [f'{x[1]}' for x in rows[:10]]
        # image_title = f'{latin_name.capitalize()} Medicine'
        # image_filepath = generate_image_template_1(entity, ['medicine'], rows_filtered)

        # p_before = content_paragraphs[0]
        # p_after = "\n\n".join(content_paragraphs[1:])
        # article += title_section + p_before + image_intro + f'![{image_title}]({image_filepath} "{image_title}")' + p_after + '\n\n'


        # # cuisine
        # title_section = f'## What are the culinary uses of {common_name}?\n\n'
        # content_paragraphs = get_content_2(f'database/articles/{entity}/cuisine.md').strip().split('\n')
        
        # if cuisine_col != 'n':
        #     image_intro = f'\n\nThe following illustration lists the most common uses of {common_name} for culinary purposes.\n\n'
            
        #     rows = utils.csv_get_rows_by_entity(f'database/tables/cuisine/uses.csv', entity)
        #     rows_filtered = [f'{x[1]}' for x in rows[:10]]

        #     image_title = f'{latin_name.capitalize()} Cuisine'
        #     try:
        #         image_filepath = ''
        #         image_filepath = generate_image_template_1(
        #             entity, 
        #             ['cuisine'], 
        #             rows_filtered,
        #         )
        #     except: pass
        # else:
        #     image_intro = f'\n\nThe following illustration serves as a reminder that {common_name} is toxic and must not be used for culinary purposes.\n\n'
        #     image_title = f'{latin_name.capitalize()} Cuisine'
        #     try:
        #         image_filepath = ''
        #         image_filepath = generate_image_template_no_cuisine(
        #             entity, 
        #             ['cuisine'], 
        #         )
        #     except: pass
        
        # p_before = content_paragraphs[0]
        # p_after = "\n\n".join(content_paragraphs[1:])
        # article += title_section + p_before + image_intro + f'![{image_title}]({image_filepath} "{image_title}")' + p_after + '\n\n'
        

        # # horticulture
        # title_section = f'## How to cultivate {common_name} in your garden?\n\n'
        # content_paragraphs = get_content_2(f'database/articles/{entity}/horticulture.md').strip().split('\n')
        # image_intro = f'\n\nThe following illustration lists the most important tips to cutlitvate {common_name}.\n\n'
        
        # rows = utils.csv_get_rows_by_entity(f'database/tables/horticulture/tips.csv', entity)
        # rows_filtered = [f'{x[1]}' for x in rows[:10]]
        # image_title = f'{latin_name.capitalize()} Horticulture'
        # image_filepath = generate_image_template_1(entity, ['horticulture'], rows_filtered)

        # p_before = content_paragraphs[0]
        # p_after = "\n\n".join(content_paragraphs[1:])
        # article += title_section + p_before + image_intro + f'![{image_title}]({image_filepath} "{image_title}")' + p_after + '\n\n'
            

        # # botany
        # title_section = f'## What is the botanical profile of {common_name}?\n\n'
        # content_paragraphs = get_content_2(f'database/articles/{entity}/botany.md').strip().split('\n')
        # image_intro = f'\n\nThe following illustration show the traditional taxonomy of {common_name}.\n\n'
        
        # rows = utils.csv_get_rows_by_entity_with_header(f'database/tables/botany/taxonomy.csv', entity)
        # rows_filtered = [f'{rows[0][k].capitalize()}: {rows[1][k]}' for k in range(len(rows[0])) if k != 0]
        # image_title = f'{latin_name.capitalize()} Botany'
        # image_filepath = generate_image_template_1(entity, ['botany'], rows_filtered)

        # p_before = content_paragraphs[0]
        # p_after = "\n\n".join(content_paragraphs[1:])
        # article += title_section + p_before + image_intro + f'![{image_title}]({image_filepath} "{image_title}")' + p_after + '\n\n'


        # # history
        # title_section = f'## What is the history and folklore of {common_name}?\n\n'
        # content_paragraphs = get_content_2(f'database/articles/{entity}/history.md').strip().split('\n')
        # image_intro = f'\n\nThe following illustration lists the most well known historical uses of {common_name}.\n\n'
        
        # rows = utils.csv_get_rows_by_entity(f'database/tables/history/uses.csv', entity)
        # rows_filtered = [f'{x[1]}' for x in rows[:10]]
        # image_title = f'{latin_name.capitalize()} History'
        # image_filepath = generate_image_template_1(entity, ['history'], rows_filtered)

        # p_before = content_paragraphs[0]
        # p_after = "\n\n".join(content_paragraphs[1:])
        # article += title_section + p_before + image_intro + f'![{image_title}]({image_filepath} "{image_title}")' + p_after + '\n\n'



# with open('database/articles/achillea-millefolium/medicine/benefits/data.json') as json_file:
        #     data = json.load(json_file)

        # for i, section in enumerate(data['benefits']):
        #     benefit = section['benefit']
        #     definition = section['definition']
        #     constituent_list = section['constituent_list']
        #     constituent_text = section['constituent_text']

        #     article += f'## {i+1}. {benefit.title()}' + '\n\n'
        #     article += definition + '\n\n'
        #     article += 'The following list includes the main medicinal constituents that give A. millefolium this benefit.' + '\n\n'
        #     article += lst_to_blt(constituent_list) + '\n\n'
        #     article += constituent_text + '\n\n'

        #     # image
        #     images_filenames = os.listdir(f'{image_folder_old}/{entity}/medicine/benefits')
            
        #     image_filepath = generate_image_template_medicine_benefits_2(
        #         entity, 
        #         common_name, 
        #         images_filenames[i], 
        #         benefit,
        #     )
        #     image_title = f'{common_name.title()} {item.title()}'
        #     image_section = f'![{image_title}]({image_filepath} "{image_title}")\n\n'

        #     article += image_section


        # rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
        # rows_filtered = [f'{x[1]}' for x in rows[:10]]
        # images_filenames = os.listdir(f'{image_folder_old}/{entity}/medicine/benefits')
        # for i, item in enumerate(rows_filtered):
        #     if i < 10: num = f'0{i}'
        #     else: num = f'{i}'
        
        #     title_section = f'## {i+1}. {item.title()}\n\n'
        #     item_formatted = item.replace(' ', '-').lower()
        #     filename = f'{num}-{item_formatted}'
        #     filepath = f'medicine/benefits/{filename}'

        #     content_section = get_content(f'{filepath}', f'database/articles/{entity}').strip()
        #     content_section = content_section.replace(common_name.lower(), common_name.title())
            
        #     # image
        #     try:
        #         image_filepath = generate_image_template_medicine_benefits(entity, common_name, images_filenames[i], item,)
        #     except:
        #         image_filepath = generate_image_template_medicine_benefits_2(entity, common_name, images_filenames[i], item,)
        #     image_title = f'{common_name.title()} {item.title()}'
        #     image_section = f'![{image_title}]({image_filepath} "{image_title}")\n\n'

        #     item_words = item.split(' ')
        #     item_no_s = item_words[0][:-1] + ' ' + ' '.join(item_words[1: ])
        #     image_intro_line = f'The primary constituents and preparations that make {common_name} {item_no_s.lower()} are shown in the following illustration.'  + '\n\n'

        #     section_1 = content_section.split('\n')[0]  + '\n\n'
        #     section_rest = '\n'.join(content_section.split('\n')[1:])  + '\n\n'

        #     article += title_section + section_1 + image_intro_line + image_section + section_rest
            
        # content = get_content_2(f'database/articles/{entity}/medicine/benefits/constituents.md')
        # content = content.replace(common_name.lower(), common_name.title())
        # if content.strip() != '':
        #     article += f'## Which biochemical compounds of {common_name} contribute the most to health?' + '\n\n'
        #     tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
        #     tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'constituents']
        #     if tmp_rows: content = content.replace(f'biochemical compounds of {common_name.title()}', f'[biochemical compounds of {common_name.title()}](/{entity}/{attribute_1.lower()}/constituents.html)')
        #     article += content + '\n\n'

        # content = get_content_2(f'database/articles/{entity}/medicine/benefits/preparations.md')
        # content = content.replace(common_name.lower(), common_name.title())
        # if content.strip() != '':
        #     article += f'## How to properly use {common_name} to get its benefits?' + '\n\n'
        #     tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
        #     tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'preparations']
        #     if tmp_rows: content = content.replace(f'preparations of {common_name.title()}', f'[preparations of {common_name.title()}](/{entity}/{attribute_1.lower()}/preparations.html)')
        #     article += content + '\n\n'

        # content = get_content_2(f'database/articles/{entity}/medicine/benefits/side-effects.md')
        # content = content.replace(common_name.lower(), common_name.title())
        # if content.strip() != '':
        #     article += f'## What health side effects can {common_name} have if used improperly?' + '\n\n'
        #     tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
        #     tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'side-effects']
        #     if tmp_rows: content = content.replace(f'side effects associated with {common_name.title()}', f'[side effects associated with {common_name.title()}](/{entity}/{attribute_1.lower()}/side-effects.html)')
        #     article += content + '\n\n'

        # content = get_content_2(f'database/articles/{entity}/medicine/benefits/precautions.md')
        # if content.strip() != '':
        #     article += f'## What precautions should you take before using {common_name} for medicinal purposes?' + '\n\n'
        #     article += content + '\n\n'