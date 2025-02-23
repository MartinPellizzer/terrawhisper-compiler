import os
import json

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read
from oliark_llm import llm_reply

vault = '/home/ubuntu/vault'

vertices_plants_filepath = f'/home/ubuntu/vault/herbalism/vertices-plants.json'
vertices_plants = json_read(vertices_plants_filepath)

def json_write(vertices_filepath, vertices):
    j = json.dumps(vertices_plants, indent=4)
    with open(vertices_plants_filepath, 'w') as f:
        print(j, file=f)
    
# get popular teas from ailments preparations articles
def popular_teas():
    output = []
    ailments = csv_read_rows_to_json('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailments):
        system_slug = ailment['system_slug']
        ailment_slug = ailment['ailment_slug']
        url = f'remedies/{system_slug}-system/{ailment_slug}/teas'
        json_filepath = f'database/json/{url}.json'
        if os.path.exists(json_filepath):
            data = json_read(json_filepath, create=True)
            for obj in data['remedies']:
                found = False
                for item in output:
                    if obj['herb_name_scientific'] == item['herb_name_scientific']:
                        item['herb_total_score'] += obj['herb_total_score']
                        found = True
                        break
                if not found:
                    output.append({
                        'herb_name_scientific': obj['herb_name_scientific'],
                        'herb_total_score': obj['herb_total_score'],
                    })
    output = sorted(output, key=lambda x: x['herb_total_score'], reverse=True)
    return output

def gen_vertex_attr_list(vertices_filepath, vertices, vertex, key, prompt):
    if key not in vertex: vertex[key] = []
    # vertex[key] = []
    if vertex[key] == []:
        outputs = []
        for _ in range(1):
            reply = llm_reply(prompt)
            try: json_reply = json.loads(reply)
            except: json_reply = {}
            if json_reply != {}:
                for obj_reply in json_reply:
                    try: name = obj_reply['name'].lower().strip()
                    except: continue
                    try: confidence_score = obj_reply['confidence_score']
                    except: continue
                    outputs.append({
                        'name': name,
                        'confidence_score': confidence_score,
                    })
                outputs = sorted(outputs, key=lambda x: x['confidence_score'], reverse=True)
                print(outputs)
        vertex[key] = outputs
        json_write(vertices_filepath, vertices)

# update knowledge graph -> vertices_plants
def gen_teas_common_names():
    teas_names = [tea['herb_name_scientific'] for tea in popular_teas()]
    for tea_name in teas_names:
        print(tea_name)
        tea_slug = tea_name.strip().lower().replace(' ', '-')
        found = False
        for vertex_plant in vertices_plants:
            if vertex_plant['plant_slug'] == tea_slug:
                print(vertex_plant)
                plant_name_scientific = vertex_plant['plant_name_scientific']
                gen_vertex_attr_list(
                    vertices_filepath = vertices_plants_filepath,
                    vertices = vertices_plants,
                    vertex = vertex_plant,
                    key = 'plant_names_common',
                    prompt = f'''
                        Write a list of the most popular common names of the plant with scientific name: {plant_name_scientific}.
                        Also give a confidence score from 1 to 10 for each list item, indicating how much you are sure about your answer.
                        Use as few words as possible.
                        Reply with the following JSON format:
                        [
                            {{"name": "write name 1 here", "confidence_score": 10}},
                            {{"name": "write name 2 here", "confidence_score": 5}},
                            {{"name": "write name 3 here", "confidence_score": 7}}
                        ]
                        Reply only with the JSON.
                    ''',
                )
                found = True
                break
        if found:
            pass
            # break


teas_names = [tea['herb_name_scientific'] for tea in popular_teas()]
for plant_name in teas_names:
    plant_slug = plant_name.strip().lower().replace(' ', '-')
    found = False
    for vertex_plant in vertices_plants:
        if vertex_plant['plant_slug'] == plant_slug:
            plant_name_scientific = vertex_plant['plant_name_scientific']
            plant_names_common = [item['name'] for item in vertex_plant['plant_names_common']]
            plant_names_common = ', '.join(plant_names_common[:3])
            rows = csv_read_rows_to_json(f'{vault}/amazon/teas.csv')
            found = False
            for row in rows:
                if row['plant_slug'] == plant_slug:
                    found = True
                    break
            if not found:
                with open(f'{vault}/amazon/teas.csv', 'a') as f:
                    f.write(f'{plant_slug}\\{plant_name_scientific}\\{plant_names_common}\\\n')
            print(plant_name_scientific)
            print(plant_names_common)
            print()
            break

