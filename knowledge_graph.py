import json

from oliark_io import csv_read_rows_to_json
from oliark_io import json_read, json_write
from oliark_llm import llm_reply

vault_tmp = '/home/ubuntu/vault-tmp'

vertices_plants_filepath = 'database/knowledge-graph/vertices-plants.json'
vertices_plants = json_read(vertices_plants_filepath)

vertices_families_filepath = 'database/knowledge-graph/vertices-families.json'
vertices_families = json_read(vertices_families_filepath)

vertices_orders_filepath = 'database/knowledge-graph/vertices-orders.json'
vertices_orders = json_read(vertices_orders_filepath)

vertices_subclasses_filepath = 'database/knowledge-graph/vertices-subclasses.json'
vertices_subclasses = json_read(vertices_subclasses_filepath)

vertices_classes_filepath = 'database/knowledge-graph/vertices-classes.json'
vertices_classes = json_read(vertices_classes_filepath)

vertices_divisions_filepath = 'database/knowledge-graph/vertices-divisions.json'
vertices_divisions = json_read(vertices_divisions_filepath)

edges_families_orders_filepath = 'database/knowledge-graph/edges-families-orders.json'
edges_families_orders = json_read(edges_families_orders_filepath)

edges_orders_subclasses_filepath = 'database/knowledge-graph/edges-orders-subclasses.json'
edges_orders_subclasses = json_read(edges_orders_subclasses_filepath)

edges_subclasses_classes_filepath = 'database/knowledge-graph/edges-subclasses-classes.json'
edges_subclasses_classes = json_read(edges_subclasses_classes_filepath)

edges_classes_divisions_filepath = 'database/knowledge-graph/edges-classes-divisions.json'
edges_classes_divisions = json_read(edges_classes_divisions_filepath)

# WARNING: only run this after mass cleaning for mass reset
if 0:
    plants_wcvp = csv_read_rows_to_json(f'{vault_tmp}/terrawhisper/wcvp_taxon.csv', delimiter = '|')
    for key, val in plants_wcvp[0].items():
        print(f'{key}: {val}')

    # add new plants
    vertices_plants_slugs = [vertex['plant_slug'] for vertex in vertices_plants]
    for i, plant in enumerate(plants_wcvp):
        print(f'{i}/{len(plants_wcvp)}')
        plant_name_scientific = plant['scientfiicname'].lower().strip()
        plant_family = plant['family'].lower().strip()
        plant_genus = plant['genus'].lower().strip()
        plant_references = plant['references'].lower().strip()
        plant_slug = plant_name_scientific.replace(' ', '-').replace('.', '')
        vertices_plants.append({
            'vertex_type': 'plant',
            'plant_slug': plant_slug,
            'plant_name_scientific': plant_name_scientific,
            'plant_family': plant_family,
            'plant_genus': plant_genus,
        })
    j = json.dumps(vertices_plants, indent=4)
    with open(vertices_plants_filepath, 'w') as f:
        print(j, file=f)

if 0:
    # generate vertices families from plants
    for i, vertex_plant in enumerate(vertices_plants):
        print(f'{i}/{len(vertices_plants)}')
        plant_family = vertex_plant['plant_family']
        found = False
        for vertex_family in vertices_families:
            if plant_family == vertex_family['family_name']:
                found = True
                break
        if not found:
            family_name = plant_family
            family_slug = family_name.lower().strip().replace(' ', '-')
            vertices_families.append({
                'vertex_type': 'family',
                'family_slug': family_slug,
                'family_name': family_name,
            })
    j = json.dumps(vertices_families, indent=4)
    with open(vertices_families_filepath, 'w') as f:
        print(j, file=f)

# linnaean system -> order
if 0:
    for i, vertex_plant in enumerate(vertices_plants):
        print(f'{i}/{len(vertices_plants)}')
        plant_name_scientific = vertex_plant['plant_name_scientific']
        family = vertex_plant['plant_family']
        genus = vertex_plant['plant_genus']
        species = plant_name_scientific
        if edges_families_orders:
            edges_families = [edge['vertex_1'] for edge in edges_families_orders if edge['edge_type'] == 'family_order']
        else:
            edges_families = []
        if family not in edges_families: 
            outputs = []
            for _ in range(1):
                prompt = f'''
                    Write the Linnaean system of classification for the plant: {plant_name_scientific}.
                    The Linnaean system is classified by: Kingdom, Division, Class, Subclass, Order, Family, Genus, Species.
                    I will give you the Species, Genus, Family of this plant and you have to fill the rest. 
                    Use as few words as possible.
                    Reply with the following JSON format:
                    [
                        {{"Kingdom": "write the kingdom name here"}},
                        {{"Division": "write the division name here"}},
                        {{"Class": "write the class name here"}},
                        {{"Subclass": "write the subclass name here"}},
                        {{"Order": "write the order name here"}},
                        {{"Family": "{family}"}},
                        {{"Genus": "{genus}"}},
                        {{"Species": "{species}"}}
                    ]
                    Reply only with the JSON.
                '''
                reply = llm_reply(prompt)
                try: json_reply = json.loads(reply)
                except: json_reply = {}
                if json_reply != {}:
                    try: plant_kingdom = json_reply[0]['Kingdom']
                    except: continue
                    try: plant_division = json_reply[1]['Division']
                    except: continue
                    try: plant_class = json_reply[2]['Class']
                    except: continue
                    try: plant_subclass = json_reply[3]['Subclass']
                    except: continue
                    try: plant_order = json_reply[4]['Order'].strip().lower()
                    except: continue
                    try: plant_family = json_reply[5]['Family'].strip().lower()
                    except: continue
                    print('***************************************')
                    edge_new = {
                        'edge_type': 'family_order',
                        'vertex_1': family,
                        'vertex_2': plant_order,
                    }
                    edges_families_orders.append(edge_new)
                    j = json.dumps(edges_families_orders, indent=4)
                    with open(edges_families_orders_filepath, 'w') as f:
                        print(j, file=f)
                    orders_slugs = [vertex['order_slug'] for vertex in vertices_orders if vertex['vertex_type'] == 'order']
                    if plant_order not in orders_slugs:
                        order_name = plant_order
                        order_slug = order_name.strip().lower().replace(' ', '-')
                        vertex_new = {
                            'vertex_type': 'order',
                            'order_slug': order_slug,
                            'order_name': order_name
                        }
                        vertices_orders.append(vertex_new)
                        j = json.dumps(vertices_orders, indent=4)
                        with open(vertices_orders_filepath, 'w') as f:
                            print(j, file=f)

# linnaean system -> subclass
if 0:
    for i, vertex_plant in enumerate(vertices_plants):
        print(f'{i}/{len(vertices_plants)}')
        plant_name_scientific = vertex_plant['plant_name_scientific']
        
        species = plant_name_scientific
        genus = vertex_plant['plant_genus']
        family = vertex_plant['plant_family']
        order = [edge['vertex_2'] for edge in edges_families_orders if edge['vertex_1'] == family][0]
        subclass_found = False
        edges_orders = [edge['vertex_2'] for edge in edges_families_orders if (edge['edge_type'] == 'family_order' and edge['vertex_1'] == family)]
        if edges_orders != []:
            plant_order = edges_orders[0]
            edges_subclasses = [edge['vertex_2'] for edge in edges_orders_subclasses if (edge['edge_type'] == 'order_subclass' and edge['vertex_1'] == plant_order)]
            if edges_subclasses != []:
                plant_subclass = edges_subclasses[0]
                subclass_found = True
        if not subclass_found:
            outputs = []
            for _ in range(1):
                prompt = f'''
                    Write the Linnaean system of classification for the plant: {plant_name_scientific}.
                    The Linnaean system is classified by: Kingdom, Division, Class, Subclass, Order, Family, Genus, Species.
                    I will give you the Species, Genus, Family, Order of this plant and you have to fill the rest. 
                    Use as few words as possible.
                    Reply with the following JSON format:
                    [
                        {{"Kingdom": "write the kingdom name here"}},
                        {{"Division": "write the division name here"}},
                        {{"Class": "write the class name here"}},
                        {{"Subclass": "write the class name here"}},
                        {{"Order": "{order}"}},
                        {{"Family": "{family}"}},
                        {{"Genus": "{genus}"}},
                        {{"Species": "{species}"}}
                    ]
                    Reply only with the JSON.
                '''
                reply = llm_reply(prompt)
                try: json_reply = json.loads(reply)
                except: json_reply = {}
                if json_reply != {}:
                    try: plant_kingdom = json_reply[0]['Kingdom'].strip().lower()
                    except: continue
                    try: plant_division = json_reply[1]['Division'].strip().lower()
                    except: continue
                    try: plant_class = json_reply[2]['Class'].strip().lower()
                    except: continue
                    try: plant_subclass = json_reply[3]['Subclass'].strip().lower()
                    except: continue
                    try: plant_order = json_reply[4]['Order'].strip().lower()
                    except: continue
                    try: plant_family = json_reply[5]['Family'].strip().lower()
                    except: continue
                    print('***************************************')
                    edge_new = {
                        'edge_type': 'order_subclass',
                        'vertex_1': order,
                        'vertex_2': plant_subclass,
                    }
                    edges_orders_subclasses.append(edge_new)
                    j = json.dumps(edges_orders_subclasses, indent=4)
                    with open(edges_orders_subclasses_filepath, 'w') as f:
                        print(j, file=f)
                    subclasses_slugs = [vertex['subclass_slug'] for vertex in vertices_subclasses if vertex['vertex_type'] == 'subclass']
                    if plant_subclass not in subclasses_slugs:
                        subclass_name = plant_subclass
                        subclass_slug = subclass_name.strip().lower().replace(' ', '-')
                        vertex_new = {
                            'vertex_type': 'subclass',
                            'subclass_slug': subclass_slug,
                            'subclass_name': subclass_name
                        }
                        print(vertex_new)
                        vertices_subclasses.append(vertex_new)
                        j = json.dumps(vertices_subclasses, indent=4)
                        with open(vertices_subclasses_filepath, 'w') as f:
                            print(j, file=f)

# linnaean system -> class
if 0:
    for i, vertex_plant in enumerate(vertices_plants):
        print(f'{i}/{len(vertices_plants)}')
        plant_name_scientific = vertex_plant['plant_name_scientific']
        plant_species = plant_name_scientific
        plant_genus = plant_name_scientific.split(' ')[0]
        plant_family = vertex_plant['plant_family']
        plant_order = [edge['vertex_2'] for edge in edges_families_orders if edge['vertex_1'] == plant_family][0]
        plant_subclass = [edge['vertex_2'] for edge in edges_orders_subclasses if edge['vertex_1'] == plant_order][0]
        class_found = False
        try: plant_order = [edge['vertex_2'] for edge in edges_families_orders if (edge['edge_type'] == 'family_order' and edge['vertex_1'] == plant_family)][0]
        except: continue
        edges_subclasses = [edge['vertex_2'] for edge in edges_orders_subclasses if (edge['edge_type'] == 'order_subclass' and edge['vertex_1'] == plant_order)]
        if edges_subclasses != []:
            plant_subclass = edges_subclasses[0]
            edges_classes = [edge['vertex_2'] for edge in edges_subclasses_classes if (edge['edge_type'] == 'subclass_class' and edge['vertex_1'] == plant_subclass)]
            if edges_classes != []:
                plant_class = edges_classes[0]
                class_found = True
        print('***************************************************')
        print(class_found)
        if not class_found:
            outputs = []
            for _ in range(1):
                prompt = f'''
                    Write the Linnaean system of classification for the plant: {plant_name_scientific}.
                    The Linnaean system is classified by: Kingdom, Division, Class, Subclass, Order, Family, Genus, Species.
                    I will give you the Species, Genus, Family, Order, Subclass of this plant and you have to fill the rest. 
                    Use as few words as possible.
                    Reply with the following JSON format:
                    [
                        {{"Kingdom": "write the kingdom name here"}},
                        {{"Division": "write the division name here"}},
                        {{"Class": "write the class name here"}},
                        {{"Subclass": "{plant_subclass}"}},
                        {{"Order": "{plant_order}"}},
                        {{"Family": "{plant_family}"}},
                        {{"Genus": "{plant_genus}"}},
                        {{"Species": "{plant_species}"}}
                    ]
                    Reply only with the JSON.
                    Insert in the reply all the items listed in the JSON above, even the ones already given to you.
                '''
                reply = llm_reply(prompt)
                try: json_reply = json.loads(reply)
                except: json_reply = {}
                if json_reply != {}:
                    try: plant_kingdom = json_reply[0]['Kingdom'].strip().lower()
                    except: continue
                    try: plant_division = json_reply[1]['Division'].strip().lower()
                    except: continue
                    try: plant_class = json_reply[2]['Class'].strip().lower()
                    except: continue
                    try: plant_subclass = json_reply[3]['Subclass'].strip().lower()
                    except: continue
                    try: plant_order = json_reply[4]['Order'].strip().lower()
                    except: continue
                    try: plant_family = json_reply[5]['Family'].strip().lower()
                    except: continue
                    if 1:
                        edge_new = {
                            'edge_type': 'subclass_class',
                            'vertex_1': plant_subclass,
                            'vertex_2': plant_class,
                        }
                        edges_subclasses_classes.append(edge_new)
                        j = json.dumps(edges_subclasses_classes, indent=4)
                        with open(edges_subclasses_classes_filepath, 'w') as f:
                            print(j, file=f)
                        vertices_slugs = [vertex['class_slug'] for vertex in vertices_classes if vertex['vertex_type'] == 'class']
                        if plant_class not in vertices_slugs:
                            vertex_new = {
                                'vertex_type': 'class',
                                'class_slug': plant_class,
                            }
                            vertices_classes.append(vertex_new)
                            j = json.dumps(vertices_classes, indent=4)
                            with open(vertices_classes_filepath, 'w') as f:
                                print(j, file=f)

# linnaean system -> division
if 1:
    for i, vertex_plant in enumerate(vertices_plants):
        print(f'{i}/{len(vertices_plants)}')
        plant_name_scientific = vertex_plant['plant_name_scientific']
        plant_species = plant_name_scientific
        plant_genus = plant_name_scientific.split(' ')[0]
        plant_family = vertex_plant['plant_family']
        plant_order = [edge['vertex_2'] for edge in edges_families_orders if edge['vertex_1'] == plant_family][0]
        plant_subclass = [edge['vertex_2'] for edge in edges_orders_subclasses if edge['vertex_1'] == plant_order][0]
        plant_class = [edge['vertex_2'] for edge in edges_subclasses_classes if edge['vertex_1'] == plant_subclass][0]
        try: plant_order = [edge['vertex_2'] for edge in edges_families_orders if (edge['edge_type'] == 'family_order' and edge['vertex_1'] == plant_family)][0]
        except: continue
        try: plant_subclass = [edge['vertex_2'] for edge in edges_orders_subclasses if (edge['edge_type'] == 'order_subclass' and edge['vertex_1'] == plant_order)][0]
        except: continue
        try: plant_class = [edge['vertex_2'] for edge in edges_subclasses_classes if (edge['edge_type'] == 'subclass_class' and edge['vertex_1'] == plant_subclass)][0]
        except: continue
        
        plant_divisions = [edge['vertex_2'] for edge in edges_classes_divisions if (edge['edge_type'] == 'class_division' and edge['vertex_1'] == plant_class)]
        if plant_divisions != []: continue
        print('***************************************************')
        outputs = []
        for _ in range(1):
            prompt = f'''
                Write the Linnaean system of classification for the plant: {plant_name_scientific}.
                The Linnaean system is classified by: Kingdom, Division, Class, Subclass, Order, Family, Genus, Species.
                I will give you the Species, Genus, Family, Order, Subclass, Class of this plant and you have to fill the rest. 
                Use as few words as possible.
                Reply with the following JSON format:
                [
                    {{"Kingdom": "write the kingdom name here"}},
                    {{"Division": "write the division name here"}},
                    {{"Class": "{plant_class}"}},
                    {{"Subclass": "{plant_subclass}"}},
                    {{"Order": "{plant_order}"}},
                    {{"Family": "{plant_family}"}},
                    {{"Genus": "{plant_genus}"}},
                    {{"Species": "{plant_species}"}}
                ]
                Reply only with the JSON.
                Insert in the reply all the items listed in the JSON above, even the ones already given to you.
            '''
            reply = llm_reply(prompt)
            try: json_reply = json.loads(reply)
            except: json_reply = {}
            if json_reply != {}:
                try: plant_kingdom = json_reply[0]['Kingdom'].strip().lower()
                except: continue
                try: plant_division = json_reply[1]['Division'].strip().lower()
                except: continue
                try: plant_class = json_reply[2]['Class'].strip().lower()
                except: continue
                try: plant_subclass = json_reply[3]['Subclass'].strip().lower()
                except: continue
                try: plant_order = json_reply[4]['Order'].strip().lower()
                except: continue
                try: plant_family = json_reply[5]['Family'].strip().lower()
                except: continue
                if 1:
                    edge_new = {
                        'edge_type': 'class_division',
                        'vertex_1': plant_class,
                        'vertex_2': plant_division,
                    }
                    edges_classes_divisions.append(edge_new)
                    j = json.dumps(edges_classes_divisions, indent=4)
                    with open(edges_classes_divisions_filepath, 'w') as f:
                        print(j, file=f)
                    vertices_slugs = [vertex['division_slug'] for vertex in vertices_divisions if vertex['vertex_type'] == 'division']
                    if plant_division not in vertices_slugs:
                        vertex_new = {
                            'vertex_type': 'division',
                            'division_slug': plant_division,
                        }
                        vertices_divisions.append(vertex_new)
                        j = json.dumps(vertices_divisions, indent=4)
                        with open(vertices_divisions_filepath, 'w') as f:
                            print(j, file=f)

