import json

from pdfminer.high_level import extract_pages, extract_text

from oliark_io import csv_read_rows_to_json
from oliark_llm import llm_reply

from lib import g

pdf_filepath = f'/home/ubuntu/books/herbalism/medical-herbalism.pdf'
plants_wcvp = csv_read_rows_to_json(f'{g.VAULT_TMP}/terrawhisper/wcvp_taxon.csv', delimiter = '|')

reply = llm_reply('').strip()

output = []

i = 0
for page_i, page_layout in enumerate(extract_pages(pdf_filepath)):
    text = extract_text(pdf_filepath, page_numbers=[page_i, page_i])
    prompt = f'''
        Does the following text contains scientific names of plants? Reply only with "YES" or "NO".
        TEXT:
        {text}
    '''
    print(prompt)
    print('########################################')
    reply = llm_reply(prompt).strip()
    print('########################################')
    if reply.lower() == 'yes':
        prompt = f'''
            List the names of the plants mentioned in the SNIPPET below.
            Reply only in the following JSON format: 
            [
                {{"herb_name_scientific": "scientific name of herb 1 used for preparation"}}, 
                {{"herb_name_scientific": "scientific name of herb 2 used for preparation"}}, 
                {{"herb_name_scientific": "scientific name of herb 3 used for preparation"}} 
            ]
            SNIPPET:
            {text}
        '''
        print('########################################')
        reply = llm_reply(prompt).strip()
        print('########################################')
        json_data = {}
        try: json_data = json.loads(reply)
        except: pass 
        print(json_data)
        if json_data != []:
            names_scientific = []
            for item in json_data:
                try: line = item['herb_name_scientific']
                except: continue
                for plant in plants_wcvp:
                    name_scientific = plant['scientfiicname']
                    if name_scientific.lower().strip() in line.lower().strip():
                        if len(name_scientific.split(' ')) > 1:
                            print('++++++++++++++++++++++++++++++++++++++++')
                            print(name_scientific)
                            print('++++++++++++++++++++++++++++++++++++++++')
                            names_scientific.append({
                                "name": name_scientific, 
                            })
                            break
            for name in names_scientific:
                output.append(name)
    i += 1
    # if i > 50: break

herb_names_scientific = [item['name'] for item in output]
print(herb_names_scientific)
herb_names_scientific = list(set(herb_names_scientific))
print(herb_names_scientific)
herb_names_scientific = '\n'.join(herb_names_scientific)
print(herb_names_scientific)
with open('database/herbs/books/medical-herbalism.txt', 'w') as f:
    f.write(herb_names_scientific)
