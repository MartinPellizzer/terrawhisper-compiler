
def write_plant_medicine_benefits():
    rows = csv_get_rows(f'plants.csv') 
    for i, row in enumerate(rows[1:num_articles+1]):
        entity = row[0].strip()
        common_name = row[1].strip()
        latin_name = get_latin_name(entity)

        try: os.makedirs(f'database')
        except: pass
        try: os.makedirs(f'database/articles')
        except: pass
        try: os.makedirs(f'database/articles/{entity}')
        except: pass

        rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
        benefits = [f'{x[1]}' for x in rows[:10]]
        images_text = ''

        for i, benefit in enumerate(benefits):

            # check if benefit already exists
            with open(f'database/articles/{entity}/medicine/benefits/data.json', encoding='utf-8') as json_file:
                data = json.load(json_file)

            found = False
            for obj in data['benefits']:
                if obj['benefit'].lower() == benefit.lower():
                    found = True
                    print(found)
                    break

            # if benefit not exists -> add new obj
            if not found:
                data['benefits'].append(
                    {
                        "benefit": f"{benefit.lower()}",
                        "definition": "",
                        "constituent_list": [],
                        "constituent_text": ""
                    }
                )

            with open('database/articles/achillea-millefolium/medicine/benefits/data.json', "w", encoding='utf-8') as outfile: 
                json.dump(data, outfile)

            # generate definition if not exists
            for obj in data['benefits']:
                if obj['benefit'].lower() == benefit.lower():

                    if obj['definition'].strip() != '': continue

                    prompt = f'''
                        {SYSTEM_PROMPT}
                        Define in 1 sentence what "{common_name} {benefit}" means. 
                        Start the sentence with these words: "{common_name.title()}'s ability to {benefit.lower()} refers to ".
                        Fix grammatical errors.
                    '''

                    print()
                    print(f"Q: {i+1}/{num_articles}")
                    print()
                    print(prompt)
                    print()
                    print("A:")
                    print()
                    reply = ''
                    for text in llm(prompt, stream=True):
                        reply += text
                        print(text, end="", flush=True)
                    print()
                    print()

                    if reply.strip().startswith(f"{common_name.title()}'s"):
                        obj['definition'] = reply.strip()

                        with open('database/articles/achillea-millefolium/medicine/benefits/data.json', "w", encoding='utf-8') as outfile: 
                            json.dump(data, outfile)

write_plant_medicine_benefits()
