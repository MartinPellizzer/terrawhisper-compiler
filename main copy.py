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