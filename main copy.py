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





    # medicine
    elif 'medicine' in attribute_1.lower() and attribute_2.strip() == '':
        title = f'{common_name.capitalize()} ({latin_name.capitalize()}) Medicinal Guide: Benefits, Constituents, and Preparations'
        article += f'# {title}\n\n'

        attribute_lst = ['medicine', 'overview']
        image_title = f'{common_name.capitalize()} Medicinal Guide'
        image_filepath = generate_featured_image(entity, attribute_lst, image_title)
        try:
            article += f'![{image_title}]({image_filepath} "{image_title}")\n\n'
        except: 
            print(f'WARNING: missing image ({entity})')

        article += get_content('medicine/_intro', f'database/articles/{entity}')
        article += f'This article explains in details the medicinal properties of {common_name} and how to use this plant to boost your health.' + '\n\n'



        # benefits
        title_section = f'## What are the health benefits and medicinal properties of {common_name}?\n\n'

        content_paragraphs = get_content('medicine/benefits', f'database/articles/{entity}').strip().split('\n')

        tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']].strip() == entity]
        tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'benefits']
        if tmp_rows: image_intro = f'\n\nThe following illustration shows the most important [health benefits of {common_name}](/{entity}/{attribute_1.lower()}/benefits.html).\n\n'
        else: image_intro = f'\n\nThe following illustration shows the most important health benefits of {common_name}.\n\n'

        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]

        image_title = f'{latin_name.capitalize()} Medicinal Benefits'
        image_filepath = generate_image_template_1(
            entity, 
            ['medicine', 'benefits'], 
            rows_filtered,
        )

        lst_intro = f'The following list summarizes the 10 most important health benefits of {common_name}.\n\n'
        lst_filtered = [f'{x[1]}: {x[2]}' for x in rows[:10]]
        lst_formatted = lst_to_blt(bold_blt(lst_filtered))

        article += title_section + content_paragraphs[0] + image_intro + f'\n\n![{image_title}]({image_filepath} "{image_title}")\n\n' + '\n'.join(content_paragraphs[1:]) + '\n\n' + lst_intro + '\n\n' + lst_formatted + '\n\n'



        # constituents
        title_section = f'## What are the key constituents of {common_name} for health purposes?\n\n'
        
        content_paragraphs = get_content('medicine/constituents', f'database/articles/{entity}').strip().split('\n')

        tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
        tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'constituents']
        if tmp_rows: image_intro = f'\n\nThe following illustration shows the most important [active constituents of {common_name}](/{entity}/{attribute_1.lower()}/constituents.html) for medicinal purposes.\n\n'
        else: image_intro = f'\n\nThe following illustration shows the most important active constituents of {common_name} for medicinal purposes.\n\n'

        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/constituents.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]

        image_title = f'{latin_name.capitalize()} Medicinal Constituents'
        image_filepath = generate_image_template_1(
            entity, 
            ['medicine', 'constituents'], 
            rows_filtered,
        )

        lst_intro = f'The following list summarizes the 10 most important active constituents of {common_name} for medicinal purposes.\n\n'
        lst_filtered = [f'{x[1]}: {x[2]}' for x in rows[:10]]
        lst_formatted = lst_to_blt(bold_blt(lst_filtered))
        
        article += title_section + content_paragraphs[0] + image_intro + f'\n\n![{image_title}]({image_filepath} "{image_title}")\n\n' + '\n'.join(content_paragraphs[1:]) + '\n\n' + lst_intro + '\n\n' + lst_formatted + '\n\n'



        # preparations
        title_section = f'## What are the medicinal preparations of {common_name} for health purposes?\n\n'
        
        content_paragraphs = get_content('medicine/preparations', f'database/articles/{entity}').strip().split('\n')

        tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
        tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'preparations']
        if tmp_rows: image_intro = f'\n\nThe following illustration shows the most important [medicinal preparations of {common_name}](/{entity}/{attribute_1.lower()}/preparations.html).\n\n'
        else: image_intro = f'\n\nThe following illustration shows the most important medicinal preparations of {common_name}.\n\n'

        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/preparations.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]

        image_title = f'{latin_name.capitalize()} Medicinal Preparations'
        image_filepath = generate_image_template_1(
            entity, 
            ['medicine', 'preparations'], 
            rows_filtered,
        )

        lst_intro = f'The following list summarizes the 10 most important preparations of {common_name} to boost your health.\n\n'
        lst_filtered = [f'{x[1]}: {x[2]}' for x in rows[:10]]
        lst_formatted = lst_to_blt(bold_blt(lst_filtered))
        
        article += title_section + content_paragraphs[0] + image_intro + f'\n\n![{image_title}]({image_filepath} "{image_title}")\n\n' + '\n'.join(content_paragraphs[1:]) + '\n\n' + lst_intro + '\n\n' + lst_formatted + '\n\n'


        # side-effects
        
        try:
            title_section = f'## What are the possible health side effects of {common_name}?\n\n'
            content_paragraphs = get_content('medicine/side-effects', f'database/articles/{entity}').strip().split('\n')

            tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
            tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'side-effects']
            if tmp_rows: image_intro = f'\n\nThe following illustration shows some possible [health side effects of {common_name}](/{entity}/{attribute_1.lower()}/side-effects.html).\n\n'
            else: image_intro = f'\n\nThe following illustration shows some possible health side effects of {common_name}.\n\n'

            rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/side-effects.csv', entity)
            rows_filtered = [f'{x[1]}' for x in rows[:10]]

            image_title = f'{latin_name.capitalize()} Health Side Effects'
            image_filepath = generate_image_template_1(
                entity, 
                ['medicine', 'side-effects'], 
                rows_filtered,
            )

            lst_intro = f'The following list summarizes the 10 most common health side effects of {common_name} if misused.\n\n'
            lst_filtered = [f'{x[1]}: {x[2]}' for x in rows[:10]]
            lst_formatted = lst_to_blt(bold_blt(lst_filtered))
            
            article += title_section + content_paragraphs[0] + image_intro + f'\n\n![{image_title}]({image_filepath} "{image_title}")\n\n' + '\n'.join(content_paragraphs[1:]) + '\n\n' + lst_intro + '\n\n' + lst_formatted + '\n\n'


            # precautions
            title_section = f'## What precautions should you take when using {common_name} as a medicine?\n\n'
            
            content_paragraphs = get_content('medicine/precautions', f'database/articles/{entity}').strip().split('\n')

            image_intro = f'\n\nThe following illustration shows the most important precautions you must take when you use {common_name} as a medicine.\n\n'

            rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/precautions.csv', entity)
            rows_filtered = [f'{x[1]}' for x in rows[:10]]

            image_title = f'{latin_name.capitalize()} Medicinal Precautions'
            image_filepath = generate_image_template_1(
                entity, 
                ['medicine', 'precautions'], 
                rows_filtered,
            )

            lst_intro = f'The following list summarizes the 10 most important precautions you must take when you use {common_name} as a medicine.\n\n'
            lst_filtered = [f'{x[1]}: {x[2]}' for x in rows[:10]]
            lst_formatted = lst_to_blt(bold_blt(lst_filtered))
            
            article += title_section + content_paragraphs[0] + image_intro + f'\n\n![{image_title}]({image_filepath} "{image_title}")\n\n' + '\n'.join(content_paragraphs[1:]) + '\n\n' + lst_intro + '\n\n' + lst_formatted + '\n\n'
        except:
            pass



  
    elif 'cuisine' in attribute_1.lower() and attribute_2.strip() == '':

        title = f'{common_name} ({latin_name.capitalize()}) Culinary Guide: Uses, Flavor Profile, and Tips'
        article += f'# {title}\n\n'

        attribute_lst = ['cuisine']
        image_title = f'{latin_name.capitalize()} Culinary Guide'
        image_filepath = generate_featured_image(entity, attribute_lst, image_title)
        try:
            article += f'![{image_title}]({image_filepath} "{image_title}")\n\n'
        except: 
            print(f'WARNING: missing image ({entity})')

        article += get_content('cuisine/_intro', f'database/articles/{entity}')



        # uses
        title_section = f'## What are the culinary uses of {common_name}?\n\n'

        content_paragraphs = get_content('cuisine/uses', f'database/articles/{entity}').split('\n')

        image_intro = f'\n\nThe following illustration shows the most common culinary uses of yarrow.\n\n'

        rows = utils.csv_get_rows_by_entity(f'database/tables/cuisine/uses.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]

        image_title = f'{latin_name.capitalize()} Culinary Uses'
        image_filepath = generate_image_template_1(
            entity, 
            ['cuisine', 'uses'], 
            rows_filtered,
        )

        lst_intro = f'The following list summarizes the 10 most common culinary uses of {latin_name}.\n\n'
        lst_filtered = [f'{x[1]}: {x[2]}' for x in rows[:10]]
        lst_formatted = lst_to_blt(bold_blt(lst_filtered))

        article += title_section + content_paragraphs[0] + image_intro + f'\n\n![{image_title}]({image_filepath} "{image_title}")\n\n' + '\n'.join(content_paragraphs[1:]) + '\n\n' + lst_intro + '\n\n' + lst_formatted + '\n\n'


    elif 'botany' in attribute_1.lower() and attribute_2.strip() == '':
        title = f'{common_name.title()} ({latin_name.capitalize()}) Botanical Profile: Taxonomy, Morphology, and Distribution'
        article += f'# {title}\n\n'
        
        try:
            attribute_lst = ['botany']
            image_title = f'{latin_name.capitalize()} Botany'
            featured_image_filpath = generate_featured_image(entity, attribute_lst, image_title)
            article += f'![{title}]({featured_image_filpath} "{title}")\n\n'
        except: 
            print(f'WARNING: missing image ({entity})')

        article_folderpath = f'database/articles/{entity}/{attribute_1}'
        table_folderpath = f'database/tables/{attribute_1}'



        # try: 
        #     with open(f'{article_folderpath}/_intro.md', encoding='utf-8') as f: section_content = f.read()
        #     article += section_content + '\n\n'
        # except: 
        #     print(f'WARNING: missing intro ({entity}/{attribute_1}/{attribute_2})')

        section = 'taxonomy'
        try: 
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What is the taxonomy and classification of {latin_name}?'
            article += f'## {title}\n\n'
            article += section_content + '\n\n'
        except: 
            print(f'WARNING: missing {section} text ({filepath})')

        try: 
            filepath = f'{table_folderpath}/{section}.csv'
            lines = csv_get_table_data(f'{filepath}')
            article += generate_table(lines)
        except: 
            print(f'WARNING: missing {section} table ({filepath})')



        section = 'common-names'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What are the common names of {latin_name}?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        try:
            filepath = f'{table_folderpath}/{section}.csv'
            rows = csv_get_rows(f'{filepath}')
            article += f'Here\'s a list of the most common names of {latin_name} with a brief description for each name.\n\n'
            rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
            article += lst_to_blt(bold_blt(rows_filtered))
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')



        section = 'varieties'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What are the varieties of {latin_name}?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        try:
            filepath = f'{table_folderpath}/{section}.csv'
            rows = csv_get_rows(f'{filepath}')
            article += f'Here\'s a list of the most common varieties of {latin_name} with a brief description for each variety.\n\n'
            rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
            article += lst_to_blt(bold_blt(rows_filtered))
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')

            

        section = 'morphology'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What is the morphology of {latin_name}?'
            article += f'## {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')



        section = 'distribution'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What is the geographical distribution of {latin_name}?'
            article += f'## {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        try:
            filepath = f'{table_folderpath}/{section}.csv'
            article += f'The following table gives list of continents and the distribution of {latin_name} for each continent.\n\n'
            rows = utils.csv_get_rows_by_entity(f'{filepath}', entity)
            article += generate_table_simple(rows)
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')



        section = 'native'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What is the native range of {latin_name}?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        
        try:
            filepath = f'{table_folderpath}/{section}.csv'
            article += f'The following table gives a detailed list of continents and states where {latin_name} is native, according to the United States Department of Agriculture (USDA) and other governative resources around the world.\n\n'
            rows = utils.csv_get_rows_by_entity(f'{filepath}', entity)
            article += generate_table_grouped(rows)
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')



        section = 'habitat'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What is the habitat of {latin_name}?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        try:
            filepath = f'{table_folderpath}/{section}.csv'
            rows = csv_get_rows(f'{filepath}')
            article += f'Here\'s a list of the most common habitats of {latin_name} with a brief description for each one.\n\n'
            rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
            article += lst_to_blt(bold_blt(rows_filtered))
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')



        # invasive --------------------------------------------------------------------
        section = 'invasive'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'Is {latin_name} invasive?'
            article += f'## {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        try:
            filepath = f'{table_folderpath}/{section}.csv'
            rows = csv_get_rows(f'{filepath}')
            article += f'Here\'s a list of the most common habitats of {latin_name} with a brief description for each one.\n\n'
            rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
            article += lst_to_blt(bold_blt(rows_filtered))
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')



        section = 'invasive-impact'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What\'s the impact of {latin_name} as an invasive species?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')



        section = 'invasive-control'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'How to manage and control invasive {latin_name}?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

            

        # life-cycle --------------------------------------------------------------------
        section = 'life-cycle'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'What is the life cycle of {latin_name}?'
            article += f'## {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')

        try:
            filepath = f'{table_folderpath}/{section}.csv'
            rows = csv_get_rows(f'{filepath}')
            article += f'The following list gives a detailed step-by-step description of the life-cycle of {latin_name}.\n\n'
            rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
            article += lst_to_blt(bold_blt(rows_filtered))
            article += '\n\n'
        except:
            print(f'WARNING: missing {section} table ({filepath})')
            


        section = 'perennial'
        try:
            filepath = f'{article_folderpath}/{section}.md'
            with open(f'{filepath}', encoding='utf-8') as f: section_content = f.read()
            title = f'Is {common_name.lower()} annual or perennial?'
            article += f'### {title}\n\n'
            article += section_content + '\n\n'
        except:
            print(f'WARNING: missing {section} text ({filepath})')
            

    else:
        if 'morphology' in attribute_2.lower():
            title = f'{latin_name.capitalize()} morphology'
            article += f'# {title}\n\n'

            try:
                attribute_lst = ['botany', 'morphology']
                image_title = f'{latin_name.capitalize()} Morphology'
                featured_image_filpath = generate_featured_image(entity, attribute_lst, image_title)
                article += f'![{title}]({featured_image_filpath} "{title}")\n\n'
            except:
                print(f'WARNING: missing image ({entity})')

            path = f'database/articles/{entity}/botany/morphology'

            with open(f'{path}/_intro.md', encoding='utf-8') as f:  
                section_content = f.read()
            article += section_content + '\n\n'
            
            article += f'In this article you will learn about the morphology of {latin_name} by analyzing the main parts of this plant and their characteristics.' + '\n\n'

            files = ['roots', 'stems', 'leaves', 'flowers', 'fruits', 'seeds']
            for file in files:
                with open(f'{path}/{file}.md', encoding='utf-8') as f: 
                    section_content = f.read()
                
                if section_content.strip() != '':
                    section_title = file.split('.')[0].capitalize()
                    article += f'## {section_title}\n\n'
                    article += '\n\n' + section_content + '\n\n'
                    article += f'The following table shows in detail the morphological characteristics of {latin_name} {file}.\n\n'
                    lines = csv_get_table_data(f'database/tables/morphology/{section_title.lower()}.csv')
                    article += generate_table(lines)

                if file.strip() == 'roots':
                    filepath = img_morphology_roots(lines[1], latin_name, attribute_1, attribute_2, file)
                    article += f'![none]({filepath} "none")\n\n'
                elif file.strip() == 'stems':
                    filepath = img_morphology_stems(lines[1], latin_name, attribute_1, attribute_2, file)
                    article += f'![none]({filepath} "none")\n\n'
                elif file.strip() == 'leaves':
                    filepath = img_morphology_leaves(lines[1], latin_name, attribute_1, attribute_2, file)
                    article += f'![none]({filepath} "none")\n\n'

        elif 'taxonomy' in attribute_2.lower():

            title = f'{latin_name.capitalize()} taxonomy'
            article += f'# {title}\n\n'
            
            try: 
                attribute_lst = ['botany', 'taxonomy']
                image_title = f'{latin_name.capitalize()} Taxonomy'
                featured_image_filpath = generate_featured_image(entity, attribute_lst, image_title)
                article += f'![alt]({featured_image_filpath} "title")\n\n'
            except:
                print(f'WARNING: missing image ({entity} -> {attribute_1}/{attribute_2})')

            # intro
            path = f'database/articles/{entity}/botany/{attribute_2}'
            with open(f'{path}/_intro.md', encoding='utf-8') as f: 
                section_content = f.read()
            article += section_content + '\n\n'

            article += f'This article gives a detailed explanation of the taxonomy, common names, and varieties of {latin_name}.' + '\n\n'

            try:
                path = f'database/articles/{entity}/botany/taxonomy'
                files = ['taxonomy']

                for file in files:
                    with open(f'{path}/{file}.md', encoding='utf-8') as f: 
                        section_content = f.read()
                    
                    if section_content.strip() != '':
                        section_title = file.split('.')[0].capitalize()
                        article += f'## {section_title}\n\n'
                        article += '\n\n' + section_content + '\n\n'
                        lines = csv_get_table_data(f'database/tables/taxonomy/{section_title.lower()}.csv')
                        article += generate_table(lines)
            except:
                print(f'WARNING: missing taxonomy stuff')
            
            
            # common names section
            try:
                article += f'## Common Names\n\n'
                filepath = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/common-names.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'
                
                rows = csv_get_rows('database/tables/common-names/common-names.csv')
                # rows_filtered = [f'{row[1]}' for row in rows if entity == row[0].strip()]
                # article += lst_to_blt(rows_filtered)
                article += f'Here\'s a list of the most common names of {latin_name} with a brief description for each name.\n\n'
                rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
                article += lst_to_blt(bold_blt(rows_filtered))
                article += '\n\n'
            except:
                print(f'WARNING: missing common names stuff')


            
            # varieties
            try:
                article += f'## Varieties\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/varieties.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'
                
                rows = csv_get_rows('database/tables/varieties/varieties.csv')
                article += f'Here\'s a list of the most common varieties of {latin_name} with a brief description for each variety.\n\n'
                rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
                article += lst_to_blt(bold_blt(rows_filtered))
                article += '\n\n'
            except:
                print(f'WARNING: missing varieties stuff')

            
            # morphology
            try:
                article += f'## Morphology\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/morphology.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'
            except:
                print(f'WARNING: missing morphology stuff')
            
        elif 'distribution' in attribute_2.lower():

            title = f'{latin_name.capitalize()} distribution'
            article += f'# {title}\n\n'
            
            try:
                attribute_lst = ['botany', 'distribution']
                image_title = f'{latin_name.capitalize()} Distribution'
                featured_image_filpath = generate_featured_image(entity, attribute_lst, image_title)
                article += f'![alt]({featured_image_filpath} "title")\n\n'
            except: 
                print(f'WARNING: missing image ({entity} -> {attribute_1}/{attribute_2})')

            # intro
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/_intro.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'

            # article += f'This article gives a detailed explanation of the taxonomy, common names, and varieties of {latin_name}.' + '\n\n'
            
            # habitat
            try:
                article += f'## What is the natural habitat of {latin_name}?\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/habitat.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'

                rows = csv_get_rows('database/tables/habitat/habitat.csv')
                article += f'Here\'s a list of the most common habitats of {latin_name} with a brief description for each one.\n\n'
                rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
                article += lst_to_blt(bold_blt(rows_filtered))
                article += '\n\n'
            except:
                print(f'WARNING: missing habitat stuff')

            # native
            try:
                section = 'native'
                article += f'## In which regions {latin_name} is native?\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/{section}.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'

                article += f'The following table gives a detailed list of continents and states where {latin_name} is native, according to the United States Department of Agriculture (USDA) and other governative resources around the world.\n\n'

                lines = csv_get_table_data(f'database/tables/botany/{section}.csv')
                rows = utils.csv_get_rows_by_entity(f'database/tables/botany/{section}.csv', entity)
                article += generate_table_grouped(rows)
                article += '\n\n'
            except:
                print(f'WARNING: missing native stuff')
            
            # distribution
            try:
                section = 'distribution'
                article += f'## What is the global distribution of {latin_name}?\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/{section}.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'

                article += f'The following table gives list of continents and the distribution of {latin_name} for each continent.\n\n'
                lines = csv_get_table_data(f'database/tables/botany/{section}.csv')
                rows = utils.csv_get_rows_by_entity(f'database/tables/botany/{section}.csv', entity)
                article += generate_table_simple(rows)
                article += '\n\n'
            except:
                print(f'WARNING: missing distribution stuff')

            
            # invasive
            try:
                section = 'invasive'
                article += f'## Is {latin_name} invasive?\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/{section}.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'
                
                article += f'Here\'s a list of the most common habitats of {latin_name} with a brief description for each one.\n\n'
                rows = csv_get_rows(f'database/tables/botany/{section}.csv')
                rows_filtered = [f'{x[1]}: {x[2]}' for x in rows if entity == x[0].strip()]
                article += lst_to_blt(bold_blt(rows_filtered))
                article += '\n\n'
            except:
                print(f'WARNING: missing distribution stuff')

            # invasive impact
            try:
                section = 'invasive-impact'
                article += f'### What\'s the impact of {latin_name} as an invasive species?\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/{section}.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'
                article += '\n\n'
            except:
                print(f'WARNING: missing distribution stuff')

            # invasive control
            try:
                section = 'invasive-control'
                article += f'### How to manage and control invasive {latin_name}?\n\n'
                path = f'database/articles/{entity}/botany/{attribute_2}'
                with open(f'{path}/{section}.md', encoding='utf-8') as f: 
                    section_content = f.read()
                article += section_content + '\n\n'
            except:
                print(f'WARNING: missing distribution stuff')


            # article += f'The following table gives list of continents and the distribution of {latin_name} for each continent.\n\n'
            # lines = csv_get_table_data(f'database/tables/botany/{section}.csv')
            # rows = utils.csv_get_rows_by_entity(f'database/tables/botany/{section}.csv', entity)
            # article += generate_table_simple(rows)
            # article += '\n\n'




        # benefits
        # title_section = f'## What are the health benefits and medicinal properties of {common_name}?\n\n'

        # content_paragraphs = get_content('medicine/benefits', f'database/articles/{entity}').strip().split('\n')

        # # link >> if content exists
        # tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']].strip() == entity]
        # tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'benefits']
        # if tmp_rows: image_intro = f'\n\nThe following illustration shows the most important [health benefits of {common_name}](/{entity}/{attribute_1.lower()}/benefits.html).\n\n'
        # else: image_intro = f'\n\nThe following illustration shows the most important health benefits of {common_name}.\n\n'

        # rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
        # rows_filtered = [f'{x[1]}' for x in rows[:10]]

        # image_title = f'{latin_name.capitalize()} Medicinal Benefits'
        # image_filepath = generate_image_template_1(
        #     entity, 
        #     ['medicine', 'benefits'], 
        #     rows_filtered,
        # )

        # lst_intro = f'The following list summarizes the 10 most important health benefits of {common_name}.\n\n'
        # lst_filtered = [f'{x[1]}' for x in rows[:10]]
        # lst_formatted = lst_to_blt(bold_blt(lst_filtered))

        # article += title_section + content_paragraphs[0] + image_intro + f'\n\n![{image_title}]({image_filepath} "{image_title}")\n\n' + '\n'.join(content_paragraphs[1:]) + '\n\n' + lst_intro + '\n\n' + lst_formatted + '\n\n'

