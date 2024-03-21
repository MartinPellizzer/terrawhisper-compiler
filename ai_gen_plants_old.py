

# def ai_medicine_main():
#     for index, plant in enumerate(plants):
#         print(index, '-', len(plants))

#         latin_name = plant[cols['latin_name']].strip().capitalize()
#         common_name = plant[cols['common_name']].strip().title()

#         entity = latin_name.lower().replace(' ', '-')
#         filepath = f'database/articles/plants/{entity}/medicine.json'
        
#         data = util.json_read(filepath)
#         data['entity'] = entity
#         data['url'] = f'{entity}/medicine'
#         data['latin_name'] = latin_name
#         data['common_name'] = common_name
#         data['title'] = f'{latin_name} ({common_name}) Medicinal Guide'
#         util.json_write(filepath, data)

#         ai_medicine_intro(filepath)

#         # # BENEFITS
#         # ai_entity_medicine_benefits(filepath, running)

#         # # CONSTITUENTS
#         # ai_entity_medicine_constituents(filepath, running)

#         # # PREPARATIONS
#         # ai_entity_medicine_preparations(filepath, running)

#         # # SIDE EFFECTS
#         # ai_entity_medicine_side_effects(filepath, running)

#         # # PRECAUTIONS
#         # ai_entity_medicine_precautions(filepath, running)








# def ai_medicine_benefits_text(data):
#     entity = data['entity']
#     latin_name = data['latin_name']
#     common_name = data['common_name']

#     filepath = f'database/articles/plants/{entity}/medicine.json'

#     benefits_text = ''
#     try: benefits_text = data['benefits_text']
#     except: data['benefits_text'] = benefits_text
#     if benefits_text != '':  return

#     rows = util.csv_get_rows_by_entity('database/tables/benefits.csv', entity)
#     benefits = [row[1] for row in rows]
#     benefits_formatted = ', '.join(benefits)

#     aka = f', also known as {common_name.lower()},'
#     starting_text = f'{latin_name}{aka} has '
#     prompt = f'''
#         Explain in a 5-sentence paragraph the following health benefits of {latin_name}: {benefits_formatted}.
#         Don't include the common name of the plant.
#         Start with the following words: {starting_text}
#     '''
#     prompt = prompt_normalize(prompt)
#     reply = gen_reply(prompt)
#     reply = reply.replace(aka, '')
#     reply_formatted = reply_to_paragraphs(reply)

#     if len(reply_formatted) == 1:
#         p = reply_formatted[0]
#         print('***************************************')
#         print(p)
#         print('***************************************')

#         data['benefits_text'] = p
#         util.json_write(filepath, data)

#     time.sleep(30)


# def ai_medicine_constituents_text(data):
#     section = 'constituents'

#     entity = data['entity']
#     latin_name = data['latin_name']
#     common_name = data['common_name']

#     data_param = f'{section}_text'
#     data_var = ''
#     try: data_var = data[data_param]
#     except: data[data_param] = data_var

#     if data_var != '':  return

#     rows = util.csv_get_rows_by_entity(f'database/tables/{section}.csv', entity)
#     lst = [row[1] for row in rows]
#     lst_formatted = ', '.join(lst)

#     aka = f', also known as {common_name.lower()},'
#     starting_text = f'{latin_name}{aka} has several active constituents, '
#     prompt = f'''
#         Explain in a 5-sentence paragraph the following active constituents of {latin_name}: {lst_formatted}.
#         Start with these words: {starting_text}
#     '''    
#     prompt = prompt_normalize(prompt)
#     reply = gen_reply(prompt)
#     reply = reply.replace(aka, '')
#     reply_formatted = reply_to_paragraphs(reply)

#     if len(reply_formatted) == 1:
#         p = reply_formatted[0]
#         print('***************************************')
#         print(p)
#         print('***************************************')

#         data[data_param] = p
#         util.json_write(f'database/articles/plants/{entity}/medicine.json', data)

#     time.sleep(30)


# def ai_medicine_preparations_text(data):
#     section = 'preparations'

#     entity = data['entity']
#     latin_name = data['latin_name']
#     common_name = data['common_name']

#     data_param = f'{section}_text'
#     data_var = ''
#     try: data_var = data[data_param]
#     except: data[data_param] = data_var

#     if data_var != '':  return

#     rows = util.csv_get_rows_by_entity(f'database/tables/{section}.csv', entity)
#     lst = [row[1] for row in rows]
#     lst_formatted = ', '.join(lst)

#     starting_text = f'{latin_name}, also known as {common_name.lower()}, has many medicinal preparations, such as '
#     prompt = f'''
#         Explain in a 5-sentence paragraph the following medicinal preparations of {latin_name}: {lst_formatted}.
#         Start with these words: {starting_text}
#     '''    
#     prompt = prompt_normalize(prompt)
#     reply = gen_reply(prompt)
#     reply = reply.replace(f', also known as {common_name.lower()},', '')
#     reply = reply.replace(f', also known as {common_name.title()},', '')
#     reply = reply.replace(f', also known as {common_name.capitalize()},', '')
#     reply_formatted = reply_to_paragraphs(reply)

#     if len(reply_formatted) == 1:
#         p = reply_formatted[0]
#         print('***************************************')
#         print(p)
#         print('***************************************')

#         data[data_param] = p
#         util.json_write(f'database/articles/plants/{entity}/medicine.json', data)

#     time.sleep(30)


# def ai_medicine_side_effects_text(data):
#     section = 'side-effects'

#     entity = data['entity']
#     latin_name = data['latin_name']
#     common_name = data['common_name']

#     data_param = f'{section}_text'.replace('-', '_')
#     data_var = ''
#     try: data_var = data[data_param]
#     except: data[data_param] = data_var

#     if data_var != '':  return

#     rows = util.csv_get_rows_by_entity(f'database/tables/{section}.csv', entity)
#     lst = [row[1] for row in rows]
#     lst_formatted = ', '.join(lst)

#     starting_text = f'{latin_name}, also known as {common_name.lower()}, can have side effects if used improperly, such as'
#     prompt = f'''
#         Explain in a 5-sentence paragraph the following possible side effects of {latin_name}: {lst}.
#         Start with these words: {starting_text}
#     '''     
#     prompt = prompt_normalize(prompt)
#     reply = gen_reply(prompt)
#     reply = reply.replace(f', also known as {common_name.lower()},', '')
#     reply = reply.replace(f', also known as {common_name.title()},', '')
#     reply = reply.replace(f', also known as {common_name.capitalize()},', '')
#     reply_formatted = reply_to_paragraphs(reply)

#     if len(reply_formatted) == 1:
#         p = reply_formatted[0]
#         print('***************************************')
#         print(p)
#         print('***************************************')

#         data[data_param] = p
#         util.json_write(f'database/articles/plants/{entity}/medicine.json', data)

#     time.sleep(30)


# def ai_medicine_precautions_text(data):
#     section = 'precautions'

#     entity = data['entity']
#     latin_name = data['latin_name']
#     common_name = data['common_name']

#     data_param = f'{section}_text'.replace('-', '_')
#     data_var = ''
#     try: data_var = data[data_param]
#     except: data[data_param] = data_var

#     # if data_var != '':  return

#     rows = util.csv_get_rows_by_entity(f'database/tables/{section}.csv', entity)
#     lst = [row[1] for row in rows]
#     lst_formatted = ', '.join(lst)

#     starting_text = f'It\'s important to take some precautions when using {latin_name} for medicinal purposes, such as'
#     prompt = f'''
#         Explain in a 5-sentence paragraph why is important to take the following precautions when using {latin_name} for medicinal purposes: {lst}.
#         Start with these words: {starting_text}
#     '''     
#     prompt = prompt_normalize(prompt)
#     reply = gen_reply(prompt)
#     reply = reply.replace(f', also known as {common_name.lower()},', '')
#     reply = reply.replace(f', also known as {common_name.title()},', '')
#     reply = reply.replace(f', also known as {common_name.capitalize()},', '')
#     reply_formatted = reply_to_paragraphs(reply)

#     if len(reply_formatted) == 1:
#         p = reply_formatted[0]
#         print('***************************************')
#         print(p)
#         print('***************************************')

#         data[data_param] = p
#         util.json_write(f'database/articles/plants/{entity}/medicine.json', data)

#     time.sleep(30)


# def ai_medicine_main():
#     for plant in plants:
#         latin_name = plant[cols['latin_name']].strip()
#         common_name = plant[cols['common_name']].strip()

#         entity = latin_name.lower().replace(' ', '-')
#         filepath = f'database/articles/plants/{entity}/medicine.json'

#         data = util.json_read(filepath)
#         data['entity'] = entity
#         data['url'] = f'{entity}/medicine'
#         data['latin_name'] = latin_name
#         data['common_name'] = common_name
#         data['title'] = f'{latin_name} ({common_name}) Medicinal Properties and Uses'
#         util.json_write(filepath, data)

#         ai_medicine_benefits_text(data)
#         ai_medicine_constituents_text(data)
#         ai_medicine_preparations_text(data)
#         ai_medicine_side_effects_text(data)
#         ai_medicine_precautions_text(data)






def ai_medicine_benefits_text(entity):
    var_val = ''
    var_name = 'benefits_text'

    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '':  return

    rows = util.csv_get_rows_by_entity('database/tables/benefits.csv', entity)
    lst = [row[1] for row in rows]
    lst = ', '.join(lst)

    starting_text = f'{latin_name}, also known as {common_name.lower()}, has several health benefits, such as '
    prompt = f'''
        Explain in a 5-sentence paragraph the following health benefits of {latin_name}: {lst}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = reply.replace(f', also known as {common_name.lower()},', '')
    reply = reply.replace(f', also known as {common_name.title()},', '')
    reply = reply.replace(f', also known as {common_name.capitalize()},', '')
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_medicine_benefits_list(entity):
    filepath_in = 'database/tables/benefits.csv'
    filepath_out = f'database/articles/plants/{entity}/medicine.json'
    benefits_csv = [row[1] for row in util.csv_get_rows_by_entity(filepath_in, entity)]
    
    data = util.json_read(filepath_out)

    benefits_list = []
    try: benefits_list = data['benefits_list']
    except: data['benefits_list'] = benefits_list
    if benefits_list != []: return
    
    benefits_num = 10
    latin_name = entity.replace('-', ' ').strip().capitalize()
    lst = ''.join(f'{i+1}. {benefit}\n' for i, benefit in enumerate(benefits_csv[:benefits_num]))
    prompt = f'''
        Write a 1 sentence description for each benefit of {latin_name} in the following list:
        {lst}
        Answer in a ordered list using the following format. benefit: description.
    '''     
    prompt = prompt_normalize(prompt)
    reply = utils_ai.gen_reply(prompt)
    
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if ':' not in line: continue
        if '. 'not in line: continue
        if not reply.endswith('.'): reply += '.'
        line = line.strip()
        reply_formatted.append(line)

    if len(reply_formatted) == benefits_num:
        print('***************************************')
        for paragraph in reply_formatted:
            print(paragraph)
        print('***************************************')

        data['benefits_list'] = reply_formatted
        util.json_write(filepath_out, data)

    time.sleep(30)





def ai_medicine_constituents_text(entity):
    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    constituents_text = ''
    try: constituents_text = data['constituents_text']
    except: data['constituents_text'] = ''
    if constituents_text != '':  return

    rows = util.csv_get_rows_by_entity('database/tables/constituents.csv', entity)
    lst = [row[1] for row in rows]
    lst = ', '.join(lst)

    starting_text = f'{latin_name}, also known as {common_name.lower()}, has several active constituents, such as '
    prompt = f'''
        Explain in a 5-sentence paragraph the following medicinal constituents of {latin_name}: {lst}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = reply.replace(f', also known as {common_name.lower()},', '')
    reply = reply.replace(f', also known as {common_name.title()},', '')
    reply = reply.replace(f', also known as {common_name.capitalize()},', '')
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data['constituents_text'] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_medicine_constituents_list(entity):
    filepath_in = 'database/tables/constituents.csv'
    filepath_out = f'database/articles/plants/{entity}/medicine.json'
    rows = [row[1] for row in util.csv_get_rows_by_entity(filepath_in, entity)]
    
    data = util.json_read(filepath_out)

    lst = []
    try: lst = data['constituents_list']
    except: data['constituents_list'] = lst
    if lst != []: return
    
    lst_num = 10
    latin_name = entity.replace('-', ' ').strip().capitalize()
    lst = ''.join(f'{i+1}. {benefit}\n' for i, benefit in enumerate(rows[:lst_num]))
    prompt = f'''
        Write a 1 sentence description for each medicinal constituent of {latin_name} in the following list:
        {lst}
        Answer in a ordered list using the following format. constituent: description.
    '''     
    prompt = prompt_normalize(prompt)
    reply = utils_ai.gen_reply(prompt)
    
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if ':' not in line: continue
        if '. 'not in line: continue
        if not reply.endswith('.'): reply += '.'
        line = line.strip()
        reply_formatted.append(line)

    if len(reply_formatted) == lst_num:
        print('***************************************')
        for paragraph in reply_formatted:
            print(paragraph)
        print('***************************************')

        data['constituents_list'] = reply_formatted
        util.json_write(filepath_out, data)

    time.sleep(30)





def ai_medicine_preparations_text(entity):
    var_val = ''
    var_name = 'preparations_text'

    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '':  return

    rows = util.csv_get_rows_by_entity('database/tables/constituents.csv', entity)
    lst = [row[1] for row in rows]
    lst = ', '.join(lst)

    starting_text = f'{latin_name}, also known as {common_name.lower()}, has several medicinal preparations, such as '
    prompt = f'''
        Explain in a 5-sentence paragraph the following medicinal preparations of {latin_name}: {lst}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = reply.replace(f', also known as {common_name.lower()},', '')
    reply = reply.replace(f', also known as {common_name.title()},', '')
    reply = reply.replace(f', also known as {common_name.capitalize()},', '')
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_medicine_preparations_list(entity):
    var_val = []
    var_name = 'preparations_list'

    filepath_in = 'database/tables/preparations.csv'
    filepath_out = f'database/articles/plants/{entity}/medicine.json'
    rows = [row[1] for row in util.csv_get_rows_by_entity(filepath_in, entity)]
    
    data = util.json_read(filepath_out)

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != []: return
    
    lst_num = 10
    latin_name = entity.replace('-', ' ').strip().capitalize()
    lst = ''.join(f'{i+1}. {benefit}\n' for i, benefit in enumerate(rows[:lst_num]))
    prompt = f'''
        Write a 1 sentence description for each medicinal preparation of {latin_name} in the following list:
        {lst}
        Answer in a ordered list using the following format. preparation: description.
    '''     
    prompt = prompt_normalize(prompt)
    reply = utils_ai.gen_reply(prompt)
    
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if ':' not in line: continue
        if '. 'not in line: continue
        if not reply.endswith('.'): reply += '.'
        line = line.strip()
        reply_formatted.append(line)

    if len(reply_formatted) == lst_num:
        print('***************************************')
        for paragraph in reply_formatted:
            print(paragraph)
        print('***************************************')

        data[var_name] = reply_formatted
        util.json_write(filepath_out, data)

    time.sleep(30)





def ai_medicine_side_effects_text(entity):
    var_val = ''
    var_name = 'side_effects_text'

    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '':  return

    rows = util.csv_get_rows_by_entity('database/tables/side-effects.csv', entity)
    lst = [row[1] for row in rows]
    lst = ', '.join(lst)

    starting_text = f'{latin_name}, also known as {common_name.lower()}, can have side effects if used improperly, '
    prompt = f'''
        Explain in a 5-sentence paragraph the following possible side effects of {latin_name}: {lst}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = reply.replace(f', also known as {common_name.lower()},', '')
    reply = reply.replace(f', also known as {common_name.title()},', '')
    reply = reply.replace(f', also known as {common_name.capitalize()},', '')
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_medicine_side_effects_list(entity):
    var_val = []
    var_name = 'side_effects_list'

    filepath_in = 'database/tables/side-effects.csv'
    filepath_out = f'database/articles/plants/{entity}/medicine.json'
    rows = [row[1] for row in util.csv_get_rows_by_entity(filepath_in, entity)]
    
    data = util.json_read(filepath_out)

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != []: return
    
    lst_num = 10
    latin_name = entity.replace('-', ' ').strip().capitalize()
    lst = ''.join(f'{i+1}. {item}\n' for i, item in enumerate(rows[:lst_num]))
    prompt = f'''
        Write a 1 sentence description for each possible side effect of {latin_name} in the following list:
        {lst}
        Answer in a ordered list using the following format. side effect: description.
    '''     
    prompt = prompt_normalize(prompt)
    reply = utils_ai.gen_reply(prompt)
    
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if ':' not in line: continue
        if '. 'not in line: continue
        if not reply.endswith('.'): reply += '.'
        line = line.strip()
        reply_formatted.append(line)

    if len(reply_formatted) == lst_num:
        print('***************************************')
        for paragraph in reply_formatted:
            print(paragraph)
        print('***************************************')

        data[var_name] = reply_formatted
        util.json_write(filepath_out, data)

    time.sleep(30)


    


def ai_medicine_precautions_text(entity):
    var_val = ''
    var_name = 'precautions_text'

    filepath = f'database/articles/plants/{entity}/medicine.json'
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != '':  return

    rows = util.csv_get_rows_by_entity('database/tables/precautions.csv', entity)
    lst = [row[1] for row in rows]
    lst = ', '.join(lst)

    starting_text = f'Before using {latin_name} it\'s important to take some precautions, such as '
    prompt = f'''
        Explain in a 5-sentence paragraph the following precautions when using {latin_name} for medicinal purposes: {lst}.
        Start with these words: {starting_text}
    '''     
    prompt = prompt_normalize(prompt)
    reply = gen_reply(prompt)
    reply = reply.replace(f', also known as {common_name.lower()},', '')
    reply = reply.replace(f', also known as {common_name.title()},', '')
    reply = reply.replace(f', also known as {common_name.capitalize()},', '')
    reply_formatted = reply_to_paragraphs(reply)

    if len(reply_formatted) == 1:
        p = reply_formatted[0]
        print('***************************************')
        print(p)
        print('***************************************')

        data[var_name] = p
        util.json_write(filepath, data)

    time.sleep(30)


def ai_medicine_precautions_list(entity):
    var_val = []
    var_name = 'precautions_list'

    filepath_in = 'database/tables/precautions.csv'
    filepath_out = f'database/articles/plants/{entity}/medicine.json'
    rows = [row[1] for row in util.csv_get_rows_by_entity(filepath_in, entity)]
    
    data = util.json_read(filepath_out)

    try: var_val = data[var_name]
    except: data[var_name] = var_val
    if var_val != []: return
    
    lst_num = 10
    latin_name = entity.replace('-', ' ').strip().capitalize()
    lst = ''.join(f'{i+1}. {item}\n' for i, item in enumerate(rows[:lst_num]))
    prompt = f'''
        Write a 1 sentence description for each of the following precaution you should take when using {latin_name} for medicinal purposes:
        {lst}
        Answer in a ordered list using the following format. precaution: description.
    '''     
    prompt = prompt_normalize(prompt)
    reply = utils_ai.gen_reply(prompt)
    
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if ':' not in line: continue
        if '. 'not in line: continue
        if not reply.endswith('.'): reply += '.'
        line = line.strip()
        reply_formatted.append(line)

    if len(reply_formatted) == lst_num:
        print('***************************************')
        for paragraph in reply_formatted:
            print(paragraph)
        print('***************************************')

        data[var_name] = reply_formatted
        util.json_write(filepath_out, data)

    time.sleep(30)


    

    

# def ai_entity_medicine_benefits_list(filepath):
#     running = False

#     data = util.json_read(filepath)
#     latin_name = data['latin_name']
#     common_name = data['common_name']

#     try: benefits = data['benefits']
#     except: data['benefits'] = []

#     if data['benefits'] != []: return running
#     running = True
    
#     prompt_num = 10
#     prompt = f'''
#         Write a numbered list of the {prompt_num} best health benefits of {common_name} ({latin_name}).
#         Include names and descriptions.
#         Start the names with a third-person singular action verb.
#     '''
#     prompt = prompt_normalize(prompt)
#     reply = gen_reply(prompt)
#     reply = reply.strip()

#     reply_formatted = []
#     for line in reply.split('\n'):
#         line_name = ''
#         line_desc = ''
#         line = line.strip()
#         if line == '': continue

#         if ': ' in line: 
#             line_name = line.split(': ')[0].strip()
#             line_desc = ': '.join(line.split(': ')[1:]).strip()
#             if line_name == '': continue
#             if line_desc == '': continue

#             if line_name[0].isdigit():
#                 if '. ' in line_name: line_name = line_name.split('. ')[1].strip()
#                 if line_name == '': continue
#                 reply_formatted.append({"name": line_name, "desc": line_desc})

#     if prompt_num == len(reply_formatted):
#         for paragraph in reply_formatted:
#             print('***************************************')
#             print(paragraph)
#             print('***************************************')

#         data['benefits'] = reply_formatted
#         util.json_write(filepath, data)

#     return running




# RESETS
def entity_medicine_benefits_init():
    for index, plant in enumerate(plants):
        latin_name = plant[cols['latin_name']].strip().capitalize()
        common_name = plant[cols['common_name']].strip().title()
        entity = latin_name.lower().replace(' ', '-')
        url = f'{entity}/medicine/benefits'
        filepath = f'database/articles/plants/{url}.json'
        folder_create(filepath)

        data = util.json_read(filepath)
        if not data: continue
        data['benefits'] = []
        util.json_write(filepath, data)
    
# entity_medicine_benefits_init()

# ---------------------------------------------------------------------




def ai_benefits_definition(filepath):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    benefits = []
    try: benefits = data['benefits']
    except: return

    for benefit in benefits[:10]:
        benefit_name = benefit['benefit_name']
        
        benefit_definition = ''
        try: benefit_definition = benefit['definition']
        except: benefit['definition'] = benefit_definition
        if benefit_definition != '': continue

        starting_text = f'"{common_name.title()} {benefit_name.lower()}" refers to its ability to '
        prompt = f'''
                Define in detail in 1 sentence what "{common_name} {benefit_name}" means. 
                Start the sentence with these words: {starting_text}
            '''
        prompt = prompt_normalize(prompt)
        reply = gen_reply(prompt)
        reply = reply.strip()
        if starting_text.lower().strip() not in reply.lower():
            reply = starting_text + reply 

        paragraphs = reply.split('\n')
        paragraphs_filtered = []
        for paragraph in paragraphs:
            if ":" in paragraph: continue
            if paragraph[0].isdigit(): continue
            if len(paragraph.split('. ')) != 1: continue
            paragraphs_filtered.append(paragraph)
        
        if len(paragraphs_filtered) == 1:
            print('***************************************')
            print(reply)
            print('***************************************')

            benefit['definition'] = paragraphs_filtered[0]
            util.json_write(filepath, data)
        
        time.sleep(30)













# def ai_entity_medicine_benefits_constituents_list(filepath, running):
#     data = util.json_read(filepath)
#     latin_name = data['latin_name']
#     common_name = data['common_name']

#     # benefits = []
#     # try: benefits = data['benefits']
#     # except: return

#     for benefit in benefits[:10]:
#         # TODO: UNIFY WHEN POSSIBLE
#         try: benefit_name = benefit['name']
#         except: benefit_name = benefit['benefit']

#         benefit_constituents = []
#         try: benefit_constituents = benefit['constituents']
#         except: benefit['constituents'] = []

#         if benefit_constituents != []: continue
#         running = True
        
#         prompt_num = 10
#         prompt = f'''
#             Write a numbered list of the {prompt_num} most important medicinal constituents of {latin_name} that help with this benefit: {benefit_name}. 
#             Write only the names of the constituents, not the descriptions.
#         '''        
#         prompt = prompt_normalize(prompt)
#         reply = gen_reply(prompt)

#         reply = reply.strip()
#         reply_formatted = []
#         for line in reply.split('\n'):
#             line = line.strip()
#             if line == '': continue
#             if line[0].isdigit() and '. ' in line:
#                 line = '. '.join(line.split('. ')[1:]).strip()
#                 if line == '': continue
#                 if ':' in line: line = line.split(':')[0].strip()
#                 if '(' in line: line = line.split('(')[0].strip()
#                 if line.endswith('.'): line = line[0:-1]
#                 if len(line.split(' ')) > 3: continue
#                 reply_formatted.append(line)
        
#         print('***************************************')
#         print(reply_formatted)
#         print('***************************************')

#         if prompt_num == len(reply_formatted):
#             benefit['constituents'] = reply_formatted
#             util.json_write(filepath, data)

#     return running


# def ai_entity_medicine_benefits_constituents_text(filepath, running):
#     data = util.json_read(filepath)
#     latin_name = data['latin_name']
#     common_name = data['common_name']

#     benefits = []
#     try: benefits = data['benefits']
#     except: return

#     for benefit in benefits[:10]:
#         # TODO: UNIFY WHEN POSSIBLE
#         try: benefit_name = benefit['name']
#         except: benefit_name = benefit['benefit']
        
#         benefit_constituents = []
#         try: benefit_constituents = benefit['constituents']
#         except: benefit['constituents'] = []
        
#         benefit_constituents_text = ''
#         try: benefit_constituents_text = benefit['constituents_text']
#         except: benefit['constituents_text'] = ''

#         if benefit_constituents == []: continue
#         if benefit_constituents_text != '': continue
#         running = True

#         constituents = ', '.join(benefit_constituents[:7])
#         prompt = f'''
#             Write a 60-word paragraph explaining how these constituents contained in the {common_name} plant {benefit_name}: {constituents}.
#         '''

#         prompt = prompt_normalize(prompt)
#         reply = gen_reply(prompt)
#         reply = reply.strip()
        
#         paragraphs = reply.split('\n')
#         paragraphs_filtered = []
#         for paragraph in paragraphs:
#             if ":" in paragraph: continue
#             if paragraph[0].isdigit(): continue
#             if len(paragraph.split('. ')) < 2: continue
#             paragraphs_filtered.append(paragraph)

#         if len(paragraphs_filtered) == 1:            
#             print('***************************************')
#             print(paragraphs_filtered[0])
#             print('***************************************')

#             benefit['constituents_text'] = paragraphs_filtered[0]
#             util.json_write(filepath, data)

#     return running


# def ai_entity_medicine_benefits_conditions_list(filepath, running):
#     data = util.json_read(filepath)
#     latin_name = data['latin_name']
#     common_name = data['common_name']

#     benefits = []
#     try: benefits = data['benefits']
#     except: return

#     for benefit in benefits[:10]:
#         # TODO: UNIFY WHEN POSSIBLE
#         try: benefit_name = benefit['name']
#         except: benefit_name = benefit['benefit']

#         benefit_conditions = []
#         try: benefit_conditions = benefit['conditions']
#         except: benefit['conditions'] = []

#         if benefit_conditions != []: continue
#         running = True

#         prompt_paragraphs_num = 10
#         prompt = f'''
#             Write a numbered list of the {prompt_paragraphs_num} most common health conditions helped by this benefit of {common_name}: {benefit_name}.
#             Give me just the names of the conditions, not the descriptions.
#         '''        
#         prompt = prompt_normalize(prompt)
#         reply = gen_reply(prompt)

#         reply = reply.strip()
#         reply_formatted = []
#         for line in reply.split('\n'):
#             line = line.strip()
#             if line == '': continue
#             if ':' in line: continue
#             if line[0].isdigit() and '. ' in line:
#                 line = '. '.join(line.split('. ')[1:]).strip()
#                 line = line.split('(')[0].strip()
#                 if line == '': continue
#                 if len(line.split(' ')) > 5: continue
#                 reply_formatted.append(line)
        
#         print('***************************************')
#         print(reply_formatted)
#         print('***************************************')

#         if prompt_paragraphs_num == len(reply_formatted):
#             benefit['conditions'] = reply_formatted
#             util.json_write(filepath, data)

#     return running


# def ai_entity_medicine_benefits_conditions_text(filepath, running):
#     data = util.json_read(filepath)
#     latin_name = data['latin_name']
#     common_name = data['common_name']

#     benefits = []
#     try: benefits = data['benefits']
#     except: return

#     for benefit in benefits[:10]:
#         # TODO: UNIFY WHEN POSSIBLE
#         try: benefit_name = benefit['name']
#         except: benefit_name = benefit['benefit']
        
#         benefit_conditions = []
#         try: benefit_conditions = benefit['conditions']
#         except: benefit['conditions'] = []
        
#         benefit_conditions_text = ''
#         try: benefit_conditions_text = benefit['conditions_text']
#         except: benefit['conditions_text'] = ''

#         if benefit_conditions == []: continue
#         if benefit_conditions_text != '': continue
#         running = True

#         conditions = ', '.join(benefit_conditions[:7])
#         prompt = f'''
#             Write a 60-word paragraph explaining how the fact that {common_name} {benefit_name.lower()} helps with the following conditions: {conditions}.
#         '''

#         prompt = prompt_normalize(prompt)
#         reply = gen_reply(prompt)
#         reply = reply.strip()
        
#         paragraphs = reply.split('\n')
#         paragraphs_filtered = []
#         for paragraph in paragraphs:
#             if ":" in paragraph: continue
#             if paragraph.strip() == '': continue
#             if paragraph[0].isdigit(): continue
#             if len(paragraph.split('. ')) < 2: continue
#             paragraphs_filtered.append(paragraph)

#         if len(paragraphs_filtered) == 1:            
#             print('***************************************')
#             print(paragraphs_filtered[0])
#             print('***************************************')

#             benefit['conditions_text'] = paragraphs_filtered[0]
#             util.json_write(filepath, data)

#     return running








#######################################################################
# MEDICINE
#######################################################################

def ai_medicine_constituents(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    constituents_list = ''
    try: constituents_list = data['constituents_list']
    except: data['constituents_list'] = constituents_list
    if constituents_list != '': return
    running = True

    prompt_paragraphs_num = 10
    prompt = f'''
        Write a numbered list of the {prompt_paragraphs_num} best active constituents of {latin_name} ({common_name}) for health.
        Add descriptions to the active constituents.
    '''     
    
    reply = utils_ai.gen_reply(prompt)

    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if ':' not in line: continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
            reply_formatted.append(line)

    if prompt_paragraphs_num == len(reply_formatted):
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')
        data['constituents_list'] = reply_formatted
        util.json_write(filepath, data)

    return running


def ai_medicine_preparations(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    preparations_list = []
    try: preparations_list = data['preparations_list']
    except: data['preparations_list'] = []

    if preparations_list != []: return
    running = True

    prompt_paragraphs_num = 10
    prompt = f'''
        Write a numbered list of the {prompt_paragraphs_num} best medicinal preparations of {latin_name} ({common_name}).
        Add descriptions to the medicinal preparations.
        Examples of medicinal preparations are infusions and tincures.
    '''     
    
    reply = utils_ai.gen_reply(prompt)

    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if ':' not in line: continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
            reply_formatted.append(line)

    if prompt_paragraphs_num == len(reply_formatted):
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')
        data['preparations_list'] = reply_formatted
        util.json_write(filepath, data)
        
    return running


def ai_medicine_side_effects(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    side_effects_list = []
    try: side_effects_list = data['side_effects_list']
    except: data['side_effects_list'] = []

    if side_effects_list != []: return
    running = True

    prompt_paragraphs_num = 10
    prompt = f'''
        Write a numbered list of the {prompt_paragraphs_num} possible side effects of using {latin_name} ({common_name}) for medicinal purposes.
        Add descriptions to the side effects.
    '''     
    
    reply = utils_ai.gen_reply(prompt)

    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if ':' not in line: continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
            reply_formatted.append(line)

    if prompt_paragraphs_num == len(reply_formatted):
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')
        data['side_effects_list'] = reply_formatted
        util.json_write(filepath, data)
        
    return running


def ai_medicine_precautions(filepath, running):
    data = util.json_read(filepath)
    latin_name = data['latin_name']
    common_name = data['common_name']

    precautions_list = []
    try: precautions_list = data['precautions_list']
    except: data['precautions_list'] = []

    if precautions_list != []: return
    running = True

    prompt_paragraphs_num = 10
    prompt = f'''
        Write a numbered list of the {prompt_paragraphs_num} precautions to take when of using {latin_name} ({common_name}) for medicinal purposes.
        Include the names of the precautions and add descriptions.
    '''     
    
    reply = utils_ai.gen_reply(prompt)

    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if ':' not in line: continue
        if line[0].isdigit():
            line = '. '.join(line.split('. ')[1:]).strip()
            if line == '': continue
            reply_formatted.append(line)

    if prompt_paragraphs_num == len(reply_formatted):
        for paragraph in reply_formatted:
            print('***************************************')
            print(paragraph)
            print('***************************************')
        data['precautions_list'] = reply_formatted
        util.json_write(filepath, data)
        
    return running



