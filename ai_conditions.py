import util
import utils_ai
import time

outline = [
    'definition',
    'causes',
    'herbal remedies',
    'other natural remedies and lifestyle changes',
    'other lifestyle remedies',
    'associated conditions (linking)',
    'Diagnostic Approaches??',
]

csv_filepath = 'database/tables/conditions/conditions.csv'
conditions_rows = util.csv_get_rows(csv_filepath)
conditions_cols = util.csv_get_header_dict(conditions_rows)

def ai_paragraph(condition_slug, section_name, prompt):
    json_filepath = f'database/articles/conditions/{condition_slug}.json'
    util.json_generate_if_not_exists(json_filepath)
    data = util.json_read(json_filepath)

    var_val = []
    try: var_val = data[section_name]
    except: data[section_name] = var_val
    if var_val == []:
        reply = utils_ai.gen_reply(prompt)
        reply = utils_ai.reply_to_paragraphs(reply)

        if len(reply) == 1:
            print('--------------------------------------------------')
            print(reply)
            print('--------------------------------------------------')
            data[section_name] = reply
            util.json_write(json_filepath, data)

        time.sleep(30)



for condition_row in conditions_rows[1:]:
    condition_name = condition_row[conditions_cols['condition']].lower().strip()
    condition_slug = condition_row[conditions_cols['slug']].lower().strip()
    system_id = condition_row[conditions_cols['system_id']].strip()
    condition_classification = condition_row[conditions_cols['classification']].lower().strip()

    # TODO: remove the next 2 lines, they are used for prompt testing
    if system_id != '0': continue
    if condition_classification != 'symptom': continue
    print(condition_name)


    ai_paragraph(condition_slug, 'definition_desc',
        f'''
            Write a 5-sentence paragraph about {condition_name}.
            Include a detailed definition of what {condition_name} is.
            Include a description about the impact that {condition_name} has on human health.
        '''
    )
    ai_paragraph(condition_slug, 'causes_desc',
        f'''
            Write a 5-sentence paragraph explaing what are the causes of {condition_name}.
        '''
    )
    ai_paragraph(condition_slug, 'herbal_remedies_desc',
        f'''
            Write a 5-sentence paragraph explaing what are the herbal remedies for {condition_name}.
        '''
    )
    ai_paragraph(condition_slug, 'other_remedies_desc',
        f'''
            Write a 5-sentence paragraph explaing what are the natural remedies and lifestyle changes to help reduce {condition_name}.
            Don't include herbs and herbal remedies.
        '''
    )

    ai_paragraph(condition_slug, 'associated_symptoms_desc',
        f'''
            Write a 5-sentence paragraph explaing what are other symptoms associated with {condition_name}.
        '''
    )

    # json_filepath = f'database/articles/conditions/{condition_slug}.json'
    # util.json_generate_if_not_exists(json_filepath)
    # data = util.json_read(json_filepath)

    # definition_desc = []
    # try: definition_desc = data['definition_desc']
    # except: data['definition_desc'] = definition_desc
    # if definition_desc != []:
    #     if 'can' in definition_desc or 'may' in definition_desc or 'might' in definition_desc: 
    #         prompt = f'''
    #             Remove every occurence of the words "can", "may", and "might" from the following text: A cough is a forceful expulsion of air from the lungs that occurs when the respiratory system detects irritants or foreign substances. This reflex action helps protect the airways by clearing them of mucus, phlegm, and other irritants. Prolonged or chronic coughing, however, can lead to significant health issues. It can cause fatigue, sleep disturbances, and even broken ribs in severe cases. Additionally, coughing can spread viruses and other contagions, posing a risk to public health. Ultimately, coughing is a necessary and vital function for maintaining lung health, but it can also have detrimental effects on one's overall well-being.
    #         '''
            
    #         reply = utils_ai.gen_reply(prompt)
    #         reply = utils_ai.reply_to_paragraphs(reply)

    #         if len(reply) == 1:
    #             print('--------------------------------------------------')
    #             print(reply)
    #             print('--------------------------------------------------')
    #             data['definition_desc'] = reply
    #             util.json_write(json_filepath, data)

    # time.sleep(30)
    
quit()


