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



def img_resize(image_path):
    w, h = 768, 578

    img = Image.open(image_path)

    start_size = img.size
    end_size = (w, h)

    if start_size[0] / end_size [0] < start_size[1] / end_size [1]:
        ratio = start_size[0] / end_size[0]
        new_end_size = (end_size[0], int(start_size[1] / ratio))
    else:
        ratio = start_size[1] / end_size[1]
        new_end_size = (int(start_size[0] / ratio), end_size[1])

    img = img.resize(new_end_size)

    w_crop = new_end_size[0] - end_size[0]
    h_crop = new_end_size[1] - end_size[1]
    
    area = (
        w_crop // 2, 
        h_crop // 2,
        new_end_size[0] - w_crop // 2,
        new_end_size[1] - h_crop // 2
    )
    img = img.crop(area)

    output_path = f'{website_img_path}/{"-".join(image_path.split("/")[1:])}'
    img.save(f'{output_path}')

    return output_path


def img_taxonomy(item):
    domain = item['domain']
    kingdom = item['kingdom']
    phylum = item['phylum']
    _class = item['class']
    order = item['order']
    family = item['family']
    genus = item['genus']
    species = item['species']
    latin_name = f'{genus} {species}'

    w, h = 768, 512
    img = Image.new(mode="RGB", size=(w, h), color='#047857')

    draw = ImageDraw.Draw(img)


    font_size = 40
    line_hight = 1.2
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    lines = [f'Taxonomy of {latin_name}']
    for i, line in enumerate(lines):
        line_w = font.getbbox(line)[2]
        draw.text(
            (w//2 - line_w//2, 30 + (font_size * line_hight * i)), 
            line, 
            (255,255,255), 
        font=font)

    cord_list = []    

    list_y = 160 
    list_y_off = 120
    pos_1 = 0.2
    pos_2 = 0.5
    pos_3 = 0.8 
    arrow_offset = 20
    arrow_point_size = 8

    font_size = 24
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)

    line = domain
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((int(w * pos_1) - line_w//2, list_y), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_1) + line_w//2 + arrow_offset, list_y + line_h//2])

    line = kingdom
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_2) - line_w//2, list_y), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_2) - line_w//2 - arrow_offset, list_y + line_h//2])
    cord_list.append([int(w * pos_2) + line_w//2 + arrow_offset, list_y + line_h//2])

    line = phylum
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_3) - line_w//2, list_y), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_3) - line_w//2 - arrow_offset, list_y + line_h//2])
    cord_list.append([int(w * pos_3), list_y + line_h + arrow_offset])

    line = _class
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_3) - line_w//2, list_y + list_y_off), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_3), list_y + list_y_off - arrow_offset])
    cord_list.append([int(w * pos_3) - line_w//2 - arrow_offset, list_y + list_y_off + line_h//2])

    line = order
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_2) - line_w//2, list_y + list_y_off), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_2) + line_w//2 + arrow_offset, list_y + list_y_off + line_h//2])
    cord_list.append([int(w * pos_2) - line_w//2 - arrow_offset, list_y + list_y_off + line_h//2])

    line = family
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_1) - line_w//2, list_y + list_y_off), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_1) + line_w//2 + arrow_offset, list_y + list_y_off + line_h//2])
    cord_list.append([int(w * pos_1), list_y + list_y_off + line_h + arrow_offset])

    line = genus
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_1) - line_w//2, list_y + list_y_off * 2), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_1), list_y + list_y_off + list_y_off - arrow_offset])
    cord_list.append([int(w * pos_1) + line_w//2 + arrow_offset, list_y + list_y_off * 2 + line_h//2])

    line = species
    line_w = font.getbbox(line)[2]
    draw.text((int(w * pos_2) - line_w//2, list_y + list_y_off * 2), line, (255,255,255), font=font)
    cord_list.append([int(w * pos_2) - line_w//2 - arrow_offset, list_y + list_y_off * 2 + line_h//2])

    draw.line(((cord_list[0][0], cord_list[0][1]), (cord_list[1][0], cord_list[1][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[1][0], cord_list[1][1] - arrow_point_size), (cord_list[1][0] + arrow_point_size, cord_list[1][1]), (cord_list[1][0], cord_list[1][1] + arrow_point_size)], fill='#ffffff')
    draw.line(((cord_list[2][0], cord_list[2][1]), (cord_list[3][0], cord_list[3][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[3][0], cord_list[3][1] - arrow_point_size), (cord_list[3][0] + arrow_point_size, cord_list[3][1]), (cord_list[3][0], cord_list[3][1] + arrow_point_size)], fill='#ffffff')
    draw.line(((cord_list[4][0], cord_list[4][1]), (cord_list[5][0], cord_list[5][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[5][0] - arrow_point_size, cord_list[5][1]), (cord_list[5][0], cord_list[5][1] + arrow_point_size), (cord_list[5][0] + arrow_point_size, cord_list[5][1])], fill='#ffffff')
    draw.line(((cord_list[6][0], cord_list[6][1]), (cord_list[7][0], cord_list[7][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[7][0], cord_list[7][1] - arrow_point_size), (cord_list[7][0] - arrow_point_size, cord_list[7][1]), (cord_list[7][0], cord_list[7][1] + arrow_point_size)], fill='#ffffff')
    draw.line(((cord_list[8][0], cord_list[8][1]), (cord_list[9][0], cord_list[9][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[9][0], cord_list[9][1] - arrow_point_size), (cord_list[9][0] - arrow_point_size, cord_list[9][1]), (cord_list[9][0], cord_list[9][1] + arrow_point_size)], fill='#ffffff')
    
    draw.line(((cord_list[10][0], cord_list[10][1]), (cord_list[11][0], cord_list[11][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[11][0] - arrow_point_size, cord_list[11][1]), (cord_list[11][0], cord_list[11][1] + arrow_point_size), (cord_list[11][0] + arrow_point_size, cord_list[11][1])], fill='#ffffff')

    draw.line(((cord_list[12][0], cord_list[12][1]), (cord_list[13][0], cord_list[13][1])), width=2, fill='#ffffff')
    draw.polygon([(cord_list[13][0], cord_list[13][1] - arrow_point_size), (cord_list[13][0] + arrow_point_size, cord_list[13][1]), (cord_list[13][0], cord_list[13][1] + arrow_point_size)], fill='#ffffff')

    output_filename = latin_name.lower().replace(' ', '-')
    output_path = f'{website_img_path}/{output_filename}-taxonomy.jpg'
    
    # img.show()
    img.save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path


def img_cycle_of_life(item):
    genus = item['genus']
    species = item['species']
    latin_name = f'{genus} {species}'

    bg_color = '#ecfdf5'
    fg_color = '#1c1917'

    resampler = 4
    w, h = 768 * resampler, 768 * resampler
    icon_size = (64 * resampler, 64 * resampler)
    img = Image.new(mode="RGBA", size=(w, h), color=bg_color)
    icon = Image.open("assets/icons/seeds.png")

    draw = ImageDraw.Draw(img)

    line_width = 0.02
    outer_circle_size = 0.8
    inner_circle_size = 0.15

    circle_radius = w//2 * outer_circle_size
    draw.ellipse((
        w//2 - circle_radius, h//2 - circle_radius, 
        w//2 + circle_radius, h//2 + circle_radius), 
        fill=fg_color)
    circle_radius = w//2 * (outer_circle_size - line_width)
    draw.ellipse((
        w//2 - circle_radius, h//2 - circle_radius, 
        w//2 + circle_radius, h//2 + circle_radius), 
        fill=bg_color)

    icon_circle_radius = w//2 * inner_circle_size
    draw.ellipse((
        w//2 - icon_circle_radius, h//2 - icon_circle_radius - circle_radius, 
        w//2 + icon_circle_radius, h//2 + icon_circle_radius - circle_radius), 
        fill=fg_color)
    icon_circle_radius = w//2 * (inner_circle_size - line_width)
    draw.ellipse((
        w//2 - icon_circle_radius, h//2 - icon_circle_radius - circle_radius, 
        w//2 + icon_circle_radius, h//2 + icon_circle_radius - circle_radius), 
        fill=bg_color)

    icon.thumbnail(icon_size, Image.Resampling.LANCZOS)
    img.paste(icon, (
        w//2 - icon_size[0]//2,
        h//2 - icon_size[1]//2 - int(circle_radius)
        ), icon)
        
    font_size = 96
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = 'Seed Germination'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((
        w//2 - line_w//2, 
        h//2 - line_h//2 - circle_radius + int(icon_circle_radius*1.6)), line, fg_color, font=font)

    output_filename = latin_name.lower().replace(' ', '-')
    output_path = f'{website_img_path}/{output_filename}-cycle-of-life.jpg'

    img.thumbnail((w//resampler, h//resampler), Image.Resampling.LANCZOS)
    
    img.convert('RGB').save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path


def draw_line(draw, e_x, e_y, t_x, t_y, line_spacing):
    if e_x >= t_x and e_y >= t_y:
        thickness = 6
        draw.line((e_x, e_y, e_x + (t_y - e_y) + line_spacing, e_y + (t_y - e_y) + line_spacing), fill='#ffffff', width=thickness)
        draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
        thickness = 2
        draw.line((e_x, e_y, e_x + (t_y - e_y) + line_spacing, e_y + (t_y - e_y) + line_spacing), fill='#000000', width=thickness)
        draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))
    elif e_x <= t_x and e_y >= t_y:
        thickness = 6
        draw.line((e_x, e_y, e_x - (t_y - e_y) - line_spacing, t_y + line_spacing), fill='#ffffff', width=thickness)
        draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
        thickness = 2
        draw.line((e_x, e_y, e_x - (t_y - e_y) - line_spacing, t_y + line_spacing), fill='#000000', width=thickness)
        draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))
    elif e_x >= t_x and e_y <= t_y:
        thickness = 6
        draw.line((e_x, e_y, e_x - (t_y - e_y), t_y), fill='#ffffff', width=thickness)
        draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
        thickness = 2
        draw.line((e_x, e_y, e_x - (t_y - e_y), t_y), fill='#000000', width=thickness)
        draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))
    elif e_x <= t_x and e_y <= t_y:
        thickness = 6
        draw.line((e_x, e_y, e_x + (t_y - e_y), t_y), fill='#ffffff', width=thickness)
        draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
        thickness = 2
        draw.line((e_x, e_y, e_x + (t_y - e_y), t_y), fill='#000000', width=thickness)
        draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))


def img_morphology_roots(row, latin_name, category, attribute, file):
    # for i, item in enumerate(row):
    #     print(f'{i} - {item}')

    img_w = 1024
    img_h = 1024
    img = Image.new(mode="RGBA", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)
    icon = Image.open("assets/icons/roots.png")

    icon_size = 384
    icon_size = 512
    icon.thumbnail((icon_size, icon_size), Image.Resampling.LANCZOS)
    img.paste(icon, (img_w//2 - icon_size//2, img_h//2 - icon_size//2), icon)
    
    font_size = 48
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'{latin_name} {file} morphology'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((
        img_w//2 - line_w//2, 
        30), line, '#000000', font=font)

    # y = img_h - 130
    # thickness = 8
    # draw.line((img_w//2 - icon_size//2, y, img_w//2 + icon_size//2, y), fill='#000000', width=thickness)
    # draw.line((img_w//2 - icon_size//2, y + 50//2, img_w//2 - icon_size//2, y - 50//2), fill='#000000', width=thickness)
    # draw.line((img_w//2 + icon_size//2, y + 50//2, img_w//2 + icon_size//2, y - 50//2), fill='#000000', width=thickness)

    font_size = 24
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)

    # line = 'Width: ~20 cm'
    # line_w = font.getbbox(line)[2]
    # line_h = font.getbbox(line)[3]
    # draw.text((img_w//2 - line_w//2, y + line_h), line, '#000000', font=font)

    x = img_w - 130
    thickness = 8
    draw.line((x, img_h//2 - icon_size//3, x, img_h//2 + icon_size//3), fill='#000000', width=thickness)
    draw.line((x - 50//2, img_h//2 - icon_size//3, x + 50//2, img_h//2 - icon_size//3), fill='#000000', width=thickness)
    draw.line((x - 50//2, img_h//2 + icon_size//3, x + 50//2, img_h//2 + icon_size//3), fill='#000000', width=thickness)

    val = sanitize(row[8])
    line = f'Length: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    img_v = Image.new(mode="RGBA", size=(line_w, line_h), color='#ffffff')
    draw_v = ImageDraw.Draw(img_v)
    draw_v.text((0, 0), line, '#000000', font=font)
    img_v = img_v.rotate(90, expand=1)
    img.paste(img_v, (x + line_h, img_h//2 - line_w//2), img_v)

    val = sanitize_one_word(row[9])
    line = f'Color: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 200), line, '#000000', font=font)
    thickness = 6
    draw.line((200 + line_h + 10, 200 + line_h + 10, 475, 475), fill='#ffffff', width=thickness)
    draw.ellipse((475-thickness, 475-thickness, 475+thickness, 475+thickness), fill=(255,255,255,255))
    thickness = 2
    draw.line((200 + line_h + 10, 200 + line_h + 10, 475, 475), fill='#000000', width=thickness)
    # draw.line((50, 200 + line_h + 10, 200 + line_h + 10 + thickness//3, 200 + line_h + 10), fill='#000000', width=thickness)
    draw.ellipse((475-thickness-1, 475-thickness-1, 475+thickness+1, 475+thickness+1), fill=(0,0,0,255))


    e_x, e_y = 675, 625
    t_x, t_y = 675, 725
    val = sanitize(row[7])
    line = f'Diameter: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((t_x, t_y), line, '#000000', font=font)
    thickness = 6
    draw.line((e_x, e_y, e_x + (t_y - e_y), t_y), fill='#ffffff', width=thickness)
    draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
    thickness = 2
    draw.line((e_x, e_y, e_x + (t_y - e_y), t_y), fill='#000000', width=thickness)
    draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))

    e_x, e_y = 585, 580
    t_x, t_y = 250, 825
    val = sanitize_one_word(row[10])
    line = f'Texture: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((t_x, t_y), line, '#000000', font=font)
    thickness = 6
    draw.line((e_x, e_y, e_x - (t_y - e_y), t_y), fill='#ffffff', width=thickness)
    draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
    thickness = 2
    draw.line((e_x, e_y, e_x - (t_y - e_y), t_y), fill='#000000', width=thickness)
    draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))

    e_x, e_y = 520, 400
    t_x, t_y = 600, 300
    val = sanitize_one_word(row[1])
    line = f'Type: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((t_x, t_y), line, '#000000', font=font)
    thickness = 6
    draw.line((e_x, e_y, e_x - (t_y - e_y) - line_h, t_y + line_h), fill='#ffffff', width=thickness)
    draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
    thickness = 2
    draw.line((e_x, e_y, e_x - (t_y - e_y) - line_h, t_y + line_h), fill='#000000', width=thickness)
    draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))

    e_x, e_y = 295, 605
    t_x, t_y = 100, 700
    val = sanitize_one_word(row[4])
    line = f'Tips: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((t_x, t_y), line, '#000000', font=font)
    thickness = 6
    draw.line((e_x, e_y, e_x - (t_y - e_y), t_y), fill='#ffffff', width=thickness)
    draw.ellipse((e_x-thickness, e_y-thickness, e_x+thickness, e_y+thickness), fill=(255,255,255,255))
    thickness = 2
    draw.line((e_x, e_y, e_x - (t_y - e_y), t_y), fill='#000000', width=thickness)
    draw.ellipse((e_x-thickness-1, e_y-thickness-1, e_x+thickness+1, e_y+thickness+1), fill=(0,0,0,255))


    attribute = attribute.replace('/', '-')
    featured_image_filename = f'website/images/{entity}-{category}-{attribute}-{file}.jpg'
    
    img = img.convert('RGB')
    # img = img.resize((768, 768))
    img.save(featured_image_filename, format='JPEG', subsampling=0, quality=100)

    # print(featured_image_filpath)
    filepath = '/' + '/'.join(featured_image_filename.split('/')[1:])

    # img.show()
    # quit()

    return filepath


def img_morphology_stems(row, latin_name, category, attribute, file):
    # with open('database/tables/morphology/stems.csv', encoding='utf-8') as f:
    #     rows = f.readlines()

    # for i, item in enumerate(rows[0].split('\\')):
    #     print(f'{i} - {item}')
    # for i, item in enumerate(row):
    #     print(f'{i} - {item}')

    img_w = 1024
    img_h = 1024
    img = Image.new(mode="RGBA", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)
    icon = Image.open("assets/icons/stems.png")

    icon_size = 384
    icon_size = 512
    icon.thumbnail((icon_size, icon_size), Image.Resampling.LANCZOS)
    img.paste(icon, (img_w//2 - icon_size//2, img_h//2 - icon_size//2), icon)
    
    font_size = 48
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'{latin_name} {file} morphology'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2,30), line, '#000000', font=font)
    
    font_size = 24
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)

    y = img_h - 130
    thickness = 8
    div_h = 32
    draw.line((img_w//2 - icon_size//div_h, y, img_w//2 + icon_size//div_h, y), fill='#000000', width=thickness)
    draw.line((img_w//2 - icon_size//div_h, y + 50//2, img_w//2 - icon_size//div_h, y - 50//2), fill='#000000', width=thickness)
    draw.line((img_w//2 + icon_size//div_h, y + 50//2, img_w//2 + icon_size//div_h, y - 50//2), fill='#000000', width=thickness)

    val = sanitize(row[5])
    line = f'Diameter: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, y + line_h * 1.5), line, '#000000', font=font)

    x = img_w - 130
    thickness = 8
    div_h = 2
    draw.line((x, img_h//2 - icon_size//div_h, x, img_h//2 + icon_size//div_h), fill='#000000', width=thickness)
    draw.line((x - 50//2, img_h//2 - icon_size//div_h, x + 50//2, img_h//2 - icon_size//div_h), fill='#000000', width=thickness)
    draw.line((x - 50//2, img_h//2 + icon_size//div_h, x + 50//2, img_h//2 + icon_size//div_h), fill='#000000', width=thickness)


    val = sanitize(row[4])
    line = f'Height: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    img_v = Image.new(mode="RGBA", size=(line_w, line_h), color='#ffffff')
    draw_v = ImageDraw.Draw(img_v)
    draw_v.text((0, 0), line, '#000000', font=font)
    img_v = img_v.rotate(90, expand=1)
    img.paste(img_v, (x + line_h, img_h//2 - line_w//2), img_v)

    # e_x, e_y = 510, 750
    # t_x, t_y = 650, 950
    # val = sanitize(row[5])
    # line = f'Diameter: {val}'
    # line_w = font.getbbox(line)[2]
    # line_h = font.getbbox(line)[3]
    # line_spacing = line_h * 1.5
    # draw.text((t_x, t_y), line, '#000000', font=font)
    # thickness = 6
    # draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 425, 465
    t_x, t_y = 50, 200
    val = sanitize_one_word(row[6])
    line = f'Color: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    thickness = 6
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 600, 285
    t_x, t_y = 601, 150
    val = sanitize_one_word(row[7])
    line = f'Texture: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 510, 450
    t_x, t_y = 50, 700
    val = sanitize_one_word(row[9])
    line = f'Node: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 510, 500
    t_x, t_y = 550, 600
    val = sanitize(row[10])
    line = f'Internode: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)

    e_x, e_y = 510, 650
    t_x, t_y = 200, 800
    val = sanitize_one_word(row[1])
    line = f'Type: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)


    attribute = attribute.replace('/', '-')
    featured_image_filename = f'website/images/{entity}-{category}-{attribute}-{file}.jpg'
    
    img = img.convert('RGB')
    # img = img.resize((768, 768))
    img.save(featured_image_filename, format='JPEG', subsampling=0, quality=100)

    # print(featured_image_filpath)
    filepath = '/' + '/'.join(featured_image_filename.split('/')[1:])

    # img.show()
    # quit()

    return filepath


def img_morphology_leaves(row, latin_name, category, attribute, file):
    # with open('database/tables/morphology/leaves.csv', encoding='utf-8') as f:
    #     rows = f.readlines()

    # for i, item in enumerate(rows[0].split('\\')):
    #     print(f'{i} - {item}')
    # for i, item in enumerate(row):
    #     print(f'{i} - {item}')

    img_w = 1024
    img_h = 1024
    img = Image.new(mode="RGBA", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)
    icon = Image.open("assets/icons/leaves.png")

    icon_size = 384
    icon_size = 384
    icon.thumbnail((icon_size, icon_size), Image.Resampling.LANCZOS)
    img.paste(icon, (img_w//2 - icon_size//2, img_h//2 - icon_size//2), icon)
    
    font_size = 48
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = f'{latin_name} {file} morphology'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2,30), line, '#000000', font=font)
    
    font_size = 24
    line_hight = 1.5
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)

    y = img_h - 130
    thickness = 8
    div_h = 2
    draw.line((img_w//2 - icon_size//div_h, y, img_w//2 + icon_size//div_h, y), fill='#000000', width=thickness)
    draw.line((img_w//2 - icon_size//div_h, y + 50//2, img_w//2 - icon_size//div_h, y - 50//2), fill='#000000', width=thickness)
    draw.line((img_w//2 + icon_size//div_h, y + 50//2, img_w//2 + icon_size//div_h, y - 50//2), fill='#000000', width=thickness)

    val = sanitize(row[6])
    line = f'Width: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((img_w//2 - line_w//2, y + line_h * 1.5), line, '#000000', font=font)

    x = img_w - 130
    thickness = 8
    div_h = 2
    draw.line((x, img_h//2 - icon_size//div_h, x, img_h//2 + icon_size//div_h), fill='#000000', width=thickness)
    draw.line((x - 50//2, img_h//2 - icon_size//div_h, x + 50//2, img_h//2 - icon_size//div_h), fill='#000000', width=thickness)
    draw.line((x - 50//2, img_h//2 + icon_size//div_h, x + 50//2, img_h//2 + icon_size//div_h), fill='#000000', width=thickness)


    val = sanitize(row[5])
    line = f'Lenght: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    img_v = Image.new(mode="RGBA", size=(line_w, line_h), color='#ffffff')
    draw_v = ImageDraw.Draw(img_v)
    draw_v.text((0, 0), line, '#000000', font=font)
    img_v = img_v.rotate(90, expand=1)
    img.paste(img_v, (x + line_h, img_h//2 - line_w//2), img_v)

    e_x, e_y = 450, 490
    t_x, t_y = 50, 150
    val = sanitize_one_word(row[8])
    line = f'Color: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    thickness = 6
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 650, 450
    t_x, t_y = 400, 250
    val = sanitize_one_word(row[9])
    line = f'Texture: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 600, 550
    t_x, t_y = 750, 800
    val = sanitize_one_word(row[2])
    line = f'Shape: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)
    
    e_x, e_y = 535, 630
    t_x, t_y = 400, 700
    val = sanitize_one_word(row[13])
    line = f'Margin: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)

    e_x, e_y = 345, 680
    t_x, t_y = 100, 800
    val = sanitize_one_word(row[17])
    line = f'Attachment: {val}'
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    line_spacing = line_h * 1.5
    draw.text((t_x, t_y), line, '#000000', font=font)
    draw_line(draw, e_x, e_y, t_x, t_y, line_spacing)


    attribute = attribute.replace('/', '-')
    featured_image_filename = f'website/images/{entity}-{category}-{attribute}-{file}.jpg'
    
    img = img.convert('RGB')
    # img = img.resize((768, 768))
    img.save(featured_image_filename, format='JPEG', subsampling=0, quality=100)

    # print(featured_image_filpath)
    filepath = '/' + '/'.join(featured_image_filename.split('/')[1:])

    # img.show()
    # quit()

    return filepath


def generate_image_habitat(entity):
    input_filepath = f'articles-images/{entity}-botany-habitat.jpg'
    outut_filepath = f'website/images/{entity}-botany-habitat.jpg'

    img = Image.open(input_filepath)
    img.save(outut_filepath, format='JPEG', subsampling=0, quality=100)

    image_filpath = '/' + '/'.join(outut_filepath.split('/')[1:])

    return image_filpath


def img_cheasheet(latin_name, title, lst, img_name):
    img_w, img_h = 768, 2000
    bg_dark_1 = "#047857"
    bg_light_1 = "#ecfdf5"
    bg_light_2 = "#d1fae5"
    bg_light_3 = "#a7f3d0"
    fg_light = '#ffffff'
    fg_dark = '#0f172a'

    img = Image.new(mode="RGB", size=(img_w, img_h), color=bg_light_1)
    draw = ImageDraw.Draw(img)

    rect_h = 0
    line_x = 50
    line_y = 20

    font_size = 36
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    lines = [title, latin_name]
    for i, line in enumerate(lines):
        rect_h += font.getbbox('y')[3]
    rect_h += line_y * 2
        
    draw.rectangle(((0, 0), (img_w, rect_h)), fill=bg_dark_1)
    for i, line in enumerate(lines):
        line_w = font.getbbox(line)[2]
        line_h = font.getbbox('y')[3]
        draw.text((img_w//2 - line_w//2, line_y + line_h * i), line, fg_light, font=font)

    font_size = 16
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    
    title_rect_h = rect_h
    line_y = title_rect_h + 50

    rect_h = 0

    full_len = len(lst)
    half_len_1 = math.ceil(full_len/2)
    half_len_2 = full_len - half_len_1
    sublist_1 = lst[:half_len_1]
    sublist_2 = lst[half_len_1:]

    for l in sublist_1:
        bg = 0
        for i, x in enumerate(l):
            line = x
            line_x = 50
            line_y += rect_h
            line_w = font.getbbox(line)[2]
            line_h = font.getbbox('y')[3]
            rect_x = line_x - 20
            rect_y = line_y - 10
            rect_w = img_w//2 - 50
            rect_h = line_h + 20
            if i == 0:
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_dark_1)
                draw.text((line_x, line_y), line, fg_light, font=font)
            elif bg == 0:
                bg = 1
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_light_2)
                draw.text((line_x, line_y), line, fg_dark, font=font)
            else:
                bg = 0
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_light_1)
                draw.text((line_x, line_y), line, fg_dark, font=font)
        line_y += rect_h
        rect_y = line_y - 10
        draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + 6)), fill=bg_dark_1) 

    max_height = line_y
    
    line_y = title_rect_h + 50

    rect_h = 0
    for l in sublist_2:
        bg = 0
        for i, x in enumerate(l):
            line = x
            line_x = img_w//2 + 36
            line_y += rect_h
            line_w = font.getbbox(line)[2]
            line_h = font.getbbox('y')[3]
            rect_x = line_x - 20
            rect_y = line_y - 10
            rect_w = img_w//2 - 50
            rect_h = line_h + 20
            if i == 0:
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_dark_1)
                draw.text((line_x, line_y), line, fg_light, font=font)
            elif bg == 0:
                bg = 1
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_light_2)
                draw.text((line_x, line_y), line, fg_dark, font=font)
            else:
                bg = 0
                draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h)), fill=bg_light_1)
                draw.text((line_x, line_y), line, fg_dark, font=font)
        line_y += rect_h
        rect_y = line_y - 10
        draw.rectangle(((rect_x, rect_y), (rect_x + rect_w, rect_y + 6)), fill=bg_dark_1) 

    if max_height < line_y : max_height = line_y

    area = (0, 0, img_w, max_height + 30)
    img = img.crop(area)

    
    output_filename = latin_name.lower().replace(' ', '-')
    output_path = f'{website_img_path}/{output_filename}-{img_name}.jpg'
    img.save(f'{output_path}', format='JPEG', subsampling=0, quality=100)

    return output_path


# def generate_featured_image(entity, attribute_lst, title):
#     attribute = '/'.join(attribute_lst)
#     attribute_filename = attribute.replace('/', '-')
#     featured_image_filename = f'{entity}-{attribute_filename}.jpg'
#     featured_image_filpath = img_resize(f'articles-images/{featured_image_filename}')

#     img = Image.open(featured_image_filpath)
#     # background  = Image.open("articles-images/acorus-calamus-botany-morphology-old.jpg")

#     w_banner = img.size[0]
#     y_banner = img.size[1] // 2
#     base = Image.new('RGBA', (w_banner, y_banner), (0, 0, 0, 0))
#     top = Image.new('RGBA', (w_banner, y_banner), (0, 0, 0, 255))
#     # base = Image.new('RGBA', (w_banner, y_banner), '#0f766e')
#     # top = Image.new('RGBA', (w_banner, y_banner), '#0f766e')
#     mask = Image.new('L', (w_banner, y_banner))
#     mask_data = []
#     for y in range(y_banner):
#         mask_data.extend([int(255 * (y / y_banner))] * w_banner)
#     mask.putdata(mask_data)
    
#     y_img = img.size[1]
#     base.paste(top, (0, 0), mask)

#     img.paste(base, (0, y_img - y_banner), base)

    
#     latin_name = entity.replace('-', ' ').capitalize()
#     line = f'{title}'
#     draw = ImageDraw.Draw(img)
#     font_size = 36
#     font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
#     line_w = font.getbbox(line)[2]
#     line_h = font.getbbox('y')[3]
#     draw.text((w_banner//2 - line_w//2, y_img - line_h - 30), line, '#ffffff', font=font)

#     img.save(f'{featured_image_filpath}', format='JPEG', subsampling=0, quality=100)

#     # print(featured_image_filpath)
#     featured_image_filpath = '/' + '/'.join(featured_image_filpath.split('/')[1:])

#     return featured_image_filpath



def generate_image_template_4(entity, common_name, image_filepath, attribute, subtitle, rows):
    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    img_background = Image.open(image_filepath)
    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    current_y = 0

    # Title
    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = common_name.title()
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)

    font_size = 48
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    title_tmp = common_name.title()
    title_w = font.getbbox(title_tmp)[2]

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    subtitle_tmp = subtitle
    subtitle_tmp = subtitle_tmp.split('(')[0]
    subtitle_w = font.getbbox(subtitle_tmp)[2]
    if subtitle_w > 475:
        character_len = len(subtitle_tmp)
        font_size = 800 // character_len
        font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
        subtitle_w = font.getbbox(subtitle_tmp)[2]

    if title_w > subtitle_w: divider_w = title_w
    else: divider_w = subtitle_w
    draw.rectangle(((50, 50 + line_h + 10), (50 + divider_w, 50 + line_h + 10 + 2)), '#ffffff')
    current_y += 50 + line_h + 10 + 2
    
    # Subtitle
    line = subtitle_tmp
    line_h = font.getbbox('y')[3]
    draw.text((50, current_y + 10), line, '#ffffff', font=font)
    current_y += 50 + line_h


    # List
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    max_len = 0
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    for item in rows:
        line_w = font.getbbox(item)[2]
        if max_len < line_w: max_len = line_w
    # print(max_len)
    if max_len > 450:
        font_size = 20
        line_spacing = 1.5
    elif max_len > 500:
        font_size = 18
        line_spacing = 1.7
    else:
        line_spacing = 1.3
    

    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_h = font.getbbox('y')[3]
    for i, line in enumerate(rows):
        line = line.split('(')[0]
        draw.text((50, current_y + 10 + line_h * line_spacing * i), line, '#ffffff', font=font)
    current_y += 10 + line_h * line_spacing * i + line_h

    # Copy
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    draw.text((50, img_h - 50 - line_h), 'TerraWhisper.com', '#ffffff', font=font)

    img.thumbnail((768, 576), Image.Resampling.LANCZOS)

    # Export
    attribute = attribute.lower().replace(' ', '-')
    out_filename = f'website/images/{entity}-{attribute}.jpg'
    # img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    img.save(out_filename, format='JPEG', optimize=True, quality=50)
    filepath = f'images/{entity}-{attribute}.jpg'

    return filepath





def gen_image_medicine(entity, common_name, image_filepath, attribute, table_filepath):
    rows = utils.csv_get_rows_by_entity(table_filepath, entity)
    rows = [f'- {x[1].title()}' for x in rows]
    rows = rows[:10]

    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    img_background = Image.open(image_filepath)
    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    current_y = 0

    # Title
    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = common_name.title()
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)

    font_size = 48
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    title_tmp = common_name.title()
    title_w = font.getbbox(title_tmp)[2]

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    subtitle_tmp = attribute.replace('-', ' ').title()
    subtitle_tmp = subtitle_tmp.split('(')[0]
    subtitle_w = font.getbbox(subtitle_tmp)[2]
    if subtitle_w > 475:
        character_len = len(subtitle_tmp)
        font_size = 800 // character_len
        font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
        subtitle_w = font.getbbox(subtitle_tmp)[2]

    if title_w > subtitle_w: divider_w = title_w
    else: divider_w = subtitle_w
    draw.rectangle(((50, 50 + line_h + 10), (50 + divider_w, 50 + line_h + 10 + 2)), '#ffffff')
    current_y += 50 + line_h + 10 + 2
    
    # Subtitle
    line = subtitle_tmp
    line_h = font.getbbox('y')[3]
    draw.text((50, current_y + 10), line, '#ffffff', font=font)
    current_y += 50 + line_h


    # List
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    max_len = 0
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    for item in rows:
        line_w = font.getbbox(item)[2]
        if max_len < line_w: max_len = line_w
    # print(max_len)
    if max_len > 450:
        font_size = 20
        line_spacing = 1.5
    elif max_len > 500:
        font_size = 18
        line_spacing = 1.7
    else:
        line_spacing = 1.3
    

    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_h = font.getbbox('y')[3]
    for i, line in enumerate(rows):
        line = line.split('(')[0]
        draw.text((50, current_y + 10 + line_h * line_spacing * i), line, '#ffffff', font=font)
    current_y += 10 + line_h * line_spacing * i + line_h

    # Copy
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    draw.text((50, img_h - 50 - line_h), 'TerraWhisper.com', '#ffffff', font=font)

    img.thumbnail((768, 576), Image.Resampling.LANCZOS)

    # Export
    out_filename = f'website/images/{entity}-medicine-{attribute}.jpg'
    # img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    img.save(out_filename, format='JPEG', optimize=True, quality=50)
    filepath = f'images/{entity}-medicine-{attribute}.jpg'

    return filepath















    # medicine >> constituents
    elif 'medicine' in attribute_1.lower() and 'constituents' in attribute_2.strip():
        title = f'10 Active Constituents of {common_name.capitalize()} ({latin_name.capitalize()}): Dosage, Benefits, and Side Effects'
        article += f'# {title}\n\n'

        attribute_lst = ['medicine', 'constituents', 'overview']
        image_title = f'{common_name.capitalize()}\'s Active Constituents'
        image_filepath = generate_featured_image(entity, attribute_lst, image_title)
        try:
            article += f'![{image_title}]({image_filepath} "{image_title}")\n\n'
        except: 
            print(f'WARNING: missing image ({entity})')

        article += get_content('medicine/constituents/_intro', f'database/articles/{entity}')
        article += f'This article lists the key constituents of {common_name} and how what are their positive and negative effect on health.' + '\n\n'



        # constituents
        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/constituents.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]
        images_filenames = os.listdir(f'{image_folder_old}/{entity}/medicine/constituents')
        for i, item in enumerate(rows_filtered):
            if i < 10: num = f'0{i}'
            else: num = f'{i}'

            title_section = f'## {i+1}. {item.title()}\n\n'
            item_formatted = item.replace(' ', '-').lower()
            filename = f'{num}-{item_formatted}'
            filepath = f'medicine/constituents/{filename}'

            content_section = get_content(f'{filepath}', f'database/articles/{entity}').strip()

            # image            
            image_filepath = generate_image_template_2(entity, common_name, images_filenames[i], 
                ['medicine', 'constituents', item], 'constituents',
            )
            image_title = f'{item.title()}'
            image_section = f'![{image_title}]({image_filepath} "{image_title}")\n\n'

            item_words = item.split(' ')
            item_no_s = item_words[0][:-1] + ' ' + ' '.join(item_words[1:])
            image_intro_line = f'The following illustration show a list of the health benefits of {item}.'  + '\n\n'

            section_1 = content_section.split('\n')[0]  + '\n\n'
            section_rest = '\n'.join(content_section.split('\n')[1:])  + '\n\n'

            article += title_section + section_1 + image_intro_line + image_section + section_rest
            
        content = get_content_2(f'database/articles/{entity}/medicine/constituents/parts.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What parts of {common_name} have the highest concentration of biochemical compounds?' + '\n\n'
            article += content + '\n\n'

        content = get_content_2(f'database/articles/{entity}/medicine/constituents/preparations.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What medicinal preparations of {common_name} have the most constituents?' + '\n\n'
            tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
            tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'preparations']
            if tmp_rows: content = content.replace(f'medicinal preparations of {common_name.title()}', f'[medicinal preparations of {common_name.title()}](/{entity}/{attribute_1.lower()}/preparations.html)')
            article += content + '\n\n'
            
        content = get_content_2(f'database/articles/{entity}/medicine/constituents/benefits.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What are the most important health benefits {common_name}\'s constituents can give you?' + '\n\n'
            tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
            tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'benefits']
            if tmp_rows: content = content.replace(f'{common_name.title()}\'s constituents bring many health benefits', f'[{common_name.title()}\'s constituents bring many health benefits](/{entity}/{attribute_1.lower()}/benefits.html)')
            article += content + '\n\n'
            
        content = get_content_2(f'database/articles/{entity}/medicine/constituents/side-effects.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What are the possible side effects of an overdose of {common_name}\'s active compounds?' + '\n\n'
            tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
            tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'benefits']
            if tmp_rows: content = content.replace(f'Overdosing {common_name.title()}\'s constituents may cause side effects', f'[Overdosing {common_name.title()}\'s constituents may cause side effects](/{entity}/{attribute_1.lower()}/benefits.html)')
            article += content + '\n\n'
            

    # medicine >> preparations
    elif 'medicine' in attribute_1.lower() and 'preparations' in attribute_2.strip():
        title = f'10 Medicinal Preparations of {common_name.capitalize()} ({latin_name.capitalize()}) and Their Uses to Promote Health'
        article += f'# {title}\n\n'

        attribute_lst = ['medicine', 'preparations', 'overview']
        image_title = f'{common_name.capitalize()}\'s Medicinal Preparations'
        image_filepath = generate_featured_image(entity, attribute_lst, image_title)
        try:
            article += f'![{image_title}]({image_filepath} "{image_title}")\n\n'
        except: 
            print(f'WARNING: missing image ({entity})')

        article += get_content('medicine/preparations/_intro', f'database/articles/{entity}')
        article += f'This article lists the medicinal preparations of {common_name} and how to use them to achieve health benefits without experiencing side-effects.' + '\n\n'



        # preparations
        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/preparations.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]
        images_filenames = os.listdir(f'{image_folder_old}/{entity}/medicine/preparations')
        for i, item in enumerate(rows_filtered):
            if i < 10: num = f'0{i}'
            else: num = f'{i}'

            title_section = f'## {i+1}. {item.title()}\n\n'
            item_formatted = item.replace(' ', '-').lower()
            filename = f'{num}-{item_formatted}'
            filepath = f'medicine/preparations/{filename}'

            content_section = get_content(f'{filepath}', f'database/articles/{entity}').strip()

            # image            
            image_filepath = generate_image_template_2(entity, common_name, images_filenames[i], 
                ['medicine', 'preparations', item], 'preparations',
            )
            image_title = f'{item.title()}'
            image_section = f'![{image_title}]({image_filepath} "{image_title}")\n\n'

            item_words = item.split(' ')
            item_no_s = item_words[0][:-1] + ' ' + ' '.join(item_words[1:])
            image_intro_line = f'The following illustration give a quick overview about the health benefits of {item}, how to prepare it and what precautions to take.'  + '\n\n'

            section_1 = content_section.split('\n')[0]  + '\n\n'
            section_rest = '\n'.join(content_section.split('\n')[1:])  + '\n\n'

            article += title_section + section_1 + image_intro_line + image_section + section_rest

        content = get_content_2(f'database/articles/{entity}/medicine/preparations/combination.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What combination of {common_name} medicinal preparations work the best for general health?' + '\n\n'
            article += content + '\n\n'
            
        content = get_content_2(f'database/articles/{entity}/medicine/preparations/safest.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What\'s the safest {common_name} medicinal preparations to use?' + '\n\n'
            article += content + '\n\n'
            
        content = get_content_2(f'database/articles/{entity}/medicine/preparations/most-dangerous.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## What can be the most dangerous {common_name} medicinal preparations to use?' + '\n\n'
            article += content + '\n\n'
            
        content = get_content_2(f'database/articles/{entity}/medicine/preparations/animals.md')
        content = content.replace(common_name.lower(), common_name.title())
        if content.strip() != '':
            article += f'## Can you use {common_name} medicinal preparations on animals?' + '\n\n'
            article += content + '\n\n'


    # medicine >> effects
    elif 'medicine' in attribute_1.lower() and 'side-effects' in attribute_2.strip():
        title = f'10 Possible Health Side Effects of {common_name.capitalize()} ({latin_name.capitalize()}): Reasons, Dosages, and Precautions'
        article += f'# {title}\n\n'

        attribute_lst = ['medicine', 'side-effects', 'overview']
        image_title = f'{common_name.capitalize()}\'s Health Side Effects'
        image_filepath = generate_featured_image(entity, attribute_lst, image_title)
        try:
            article += f'![{image_title}]({image_filepath} "{image_title}")\n\n'
        except: 
            print(f'WARNING: missing image ({entity})')

        article += get_content('medicine/side-effects/_intro', f'database/articles/{entity}')
        article += f'This article lists the possible health side effects of {common_name} and how to avoid them.' + '\n\n'



        # list
        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/side-effects.csv', entity)
        rows_filtered = [f'{x[1]}' for x in rows[:10]]
        images_filenames = os.listdir(f'{image_folder_old}/{entity}/medicine/side-effects')
        for i, item in enumerate(rows_filtered):
            if i < 10: num = f'0{i}'
            else: num = f'{i}'

            title_section = f'## {i+1}. {item}\n\n'
            item_formatted = item.replace(' ', '-').lower()
            filename = f'{num}-{item_formatted}'
            filepath = f'medicine/side-effects/{filename}'

            content_section = get_content(f'{filepath}', f'database/articles/{entity}').strip()

            # image            
            image_filepath = generate_image_template_2(entity, common_name, images_filenames[i], 
                ['medicine', 'side-effects', item], 'side-effects',
            )
            image_title = f'{common_name.title()} {item.title()}'
            image_section = f'![{image_title}]({image_filepath} "{image_title}")\n\n'

            item_words = item.split(' ')
            item_no_first_word = ' '.join(item_words[1:])
            image_intro_line = f'{common_name.title()}\'s ability to {item_no_first_word.lower()} can aggravate many health conditions, like the ones shown in the illustration below.'  + '\n\n'

            section_1 = content_section.split('\n')[0]  + '\n\n'
            section_rest = '\n'.join(content_section.split('\n')[1:])  + '\n\n'

            article += title_section + section_1 + image_intro_line + image_section + section_rest

        content = get_content_2(f'database/articles/{entity}/medicine/side-effects/benefits.md')
        if content.strip() != '':
            article += f'## What are the benefits of {common_name} if used correctly?' + '\n\n'
            tmp_rows = [r for r in articles_master_rows if r[articles_dict['entity']] == entity]
            tmp_rows = [r for r in tmp_rows if r[articles_dict['attribute_2']] == 'benefits']
            if tmp_rows: 
                if f'health benefits of {common_name.lower()}' in content:
                    content = content.replace(f'health benefits of {common_name.lower()}', f'[health benefits of {common_name.lower()}](/{entity}/{attribute_1.lower()}/benefits.html)')
                else:
                    content = content.replace(f'health benefits of {common_name.title()}', f'[health benefits of {common_name.title()}](/{entity}/{attribute_1.lower()}/benefits.html)')
            article += content + '\n\n'
  



def generate_image_template_2(entity, common_name, image_filename, attribute_lst, table):
    item = attribute_lst[-1]

    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/{table}/{table}.csv', entity)
    rows_constituents = [f'- {x[3].title()}' for x in rows if x[1] == item.lower().replace(' ', '-').strip() and x[2] == 'image']
    lst_constituents = rows_constituents[:10]

    bg_image_path = f'{image_folder_old}/{entity}/medicine/{table}/{image_filename}'

    img_w = 1024
    img_h = 768
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#fafafa')
    draw = ImageDraw.Draw(img)

    attributes_path = '-'.join(attribute_lst)
    img_background = Image.open(bg_image_path)
    img_background_w = 576
    img_background_h = 768
    img_background.thumbnail((img_background_w, img_background_h), Image.Resampling.LANCZOS)
    img.paste(img_background, (img_w - img_background_w, 0))

    xy = [
        (0, 0,),
        (img_background_w, 0,),
        (img_w - img_background_w, img_h,),
        (0, img_h,),
    ]
    draw.polygon(xy, fill ="#0f766e") 

    current_y = 0

    # Title
    font_size = 48
    line_spacing = 1.3
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line = common_name.title()
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox(line)[3]
    draw.text((50, 50), line, '#ffffff', font=font)

    font_size = 48
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    title_tmp = common_name.title()
    title_w = font.getbbox(title_tmp)[2]

    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    subtitle_tmp = attribute_lst[-1].upper()
    subtitle_tmp = subtitle_tmp.split('(')[0]
    subtitle_w = font.getbbox(subtitle_tmp)[2]
    if subtitle_w > 475:
        character_len = len(subtitle_tmp)
        font_size = 800 // character_len
        font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
        subtitle_w = font.getbbox(subtitle_tmp)[2]

    if title_w > subtitle_w: divider_w = title_w
    else: divider_w = subtitle_w
    draw.rectangle(((50, 50 + line_h + 10), (50 + divider_w, 50 + line_h + 10 + 2)), '#ffffff')
    current_y += 50 + line_h + 10 + 2
    
    # Subtitle
    line = subtitle_tmp
    line_h = font.getbbox('y')[3]
    draw.text((50, current_y + 10), line, '#ffffff', font=font)
    current_y += 50 + line_h

    # List
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    max_len = 0
    font_size = 24
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    for item in lst_constituents:
        line_w = font.getbbox(item)[2]
        if max_len < line_w: max_len = line_w
    # print(max_len)
    if max_len > 450:
        font_size = 20
        line_spacing = 1.5
    elif max_len > 500:
        font_size = 18
        line_spacing = 1.7
    else:
        line_spacing = 1.3
    

    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_h = font.getbbox('y')[3]
    for i, line in enumerate(lst_constituents):
        line = line.split('(')[0]
        draw.text((50, current_y + 10 + line_h * line_spacing * i), line, '#ffffff', font=font)
    current_y += 10 + line_h * line_spacing * i + line_h

    # Copy
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    draw.text((50, img_h - 50 - line_h), '© TerraWhisper.com', '#ffffff', font=font)

    img.thumbnail((768, 576), Image.Resampling.LANCZOS)
    
    # Export
    out_attr_lst = '-'.join(attribute_lst).lower().replace(' ', '-')
    out_filename = f'website/images/{entity}-{out_attr_lst}.jpg'
    # img.save(out_filename, format='JPEG', subsampling=0, quality=100)
    img.save(out_filename, format='JPEG', optimize=True, quality=50)
    filepath = '/' + '/'.join(out_filename.split('/')[1:])

    return filepath


def generate_featured_image(entity, attribute_lst, title):
    attribute = '/'.join(attribute_lst)
    attribute_filename = attribute.replace('/', '-')
    featured_image_filpath = img_resize(f'articles-images/{entity}-{attribute_filename}.jpg')

    img = Image.open(featured_image_filpath)
    # background  = Image.open("articles-images/acorus-calamus-botany-morphology-old.jpg")

    w_banner = img.size[0]
    y_banner = img.size[1] // 2
    base = Image.new('RGBA', (w_banner, y_banner), (0, 0, 0, 0))
    top = Image.new('RGBA', (w_banner, y_banner), (0, 0, 0, 255))
    # base = Image.new('RGBA', (w_banner, y_banner), '#0f766e')
    # top = Image.new('RGBA', (w_banner, y_banner), '#0f766e')
    mask = Image.new('L', (w_banner, y_banner))
    mask_data = []
    for y in range(y_banner):
        mask_data.extend([int(255 * (y / y_banner))] * w_banner)
    mask.putdata(mask_data)
    
    y_img = img.size[1]
    base.paste(top, (0, 0), mask)

    img.paste(base, (0, y_img - y_banner), base)

    
    latin_name = entity.replace('-', ' ').capitalize()
    line = f'{title}'
    draw = ImageDraw.Draw(img)
    font_size = 36
    font = ImageFont.truetype("assets/fonts/arial.ttf", font_size)
    line_w = font.getbbox(line)[2]
    line_h = font.getbbox('y')[3]
    draw.text((w_banner//2 - line_w//2, y_img - line_h - 30), line, '#ffffff', font=font)

    # img.save(f'{featured_image_filpath}', format='JPEG', subsampling=0, quality=100)
    img.save(out_filename, format='JPEG', optimize=True, quality=50)

    # print(featured_image_filpath)
    featured_image_filpath = '/' + '/'.join(featured_image_filpath.split('/')[1:])

    return featured_image_filpath



