# quit()

# for f in articles_files:
#     article_path = 'database/articles/' + f

#     with open(article_path, encoding='utf-8') as f:
#         data = json.loads(f.read())

#     for item in data:
#         state = item['state']
#         post_type = item['post_type']
#         latin_name = item['latin_name']
#         most_common_name = item['common_name']

#         if 'draft' == state.lower().strip(): continue

#         # TODO: remove
#         # if 'Aloe Vera'.lower() != latin_name.lower(): continue
#         # print(latin_name)

#         entity = item["latin_name"].lower().replace(' ', '-')
#         attribute = item['attribute']

#         try: os.mkdir(f'articles/{entity}')
#         except: pass
#         try: os.mkdir(f'website/{entity}')
#         except: pass

#         folders = [x for x in attribute.split('/')]
#         curr_path = ''
#         for folder in folders:
#             curr_path += folder + '/'
#             try: os.mkdir(f'articles/{entity}/{curr_path}')
#             except: pass
#             try: os.mkdir(f'website/{entity}/{curr_path}')
#             except: pass
#         # try: os.mkdir(f'website/{entity}/{attribute_name}')
#         # except: pass

#         publishing_state = ''
#         for a in articles_master_rows:
#             if a[0].lower().strip() == entity:
#                 publishing_state = a[4].lower().strip()
#                 break

#         article = ''

#         if 'list' == post_type:
#             if 'morphology' in attribute.lower():
#                 # title
#                 title = f'{latin_name.capitalize()} morphology'
#                 article += f'# {title}\n\n'
                
#                 # image
#                 featured_image_filpath = generate_featured_image(entity, attribute)
#                 article += f'![alt]({featured_image_filpath} "title")\n\n'

#                 try: 
#                     with open(f'database/articles/{entity}/botanical/morphology/roots.md', encoding='utf-8') as f: roots_content = f.read()
#                 except: roots_content = ''
#                 try: 
#                     with open(f'database/articles/{entity}/botanical/morphology/stems.md', encoding='utf-8') as f: stems_content = f.read()
#                 except: stems_content = ''
#                 try: 
#                     with open(f'database/articles/{entity}/botanical/morphology/rhizomes.md', encoding='utf-8') as f: rhizomes_content = f.read()
#                 except: rhizomes_content = ''
#                 try: 
#                     with open(f'database/articles/{entity}/botanical/morphology/leaves.md', encoding='utf-8') as f: leaves_content = f.read()
#                 except: leaves_content = ''
#                 try: 
#                     with open(f'database/articles/{entity}/botanical/morphology/flowers.md', encoding='utf-8') as f: flowers_content = f.read()
#                 except: flowers_content = ''
#                 try: 
#                     with open(f'database/articles/{entity}/botanical/morphology/fruits.md', encoding='utf-8') as f: fruits_content = f.read()
#                 except: fruits_content = ''
#                 try: 
#                     with open(f'database/articles/{entity}/botanical/morphology/seeds.md', encoding='utf-8') as f: seeds_content = f.read()
#                 except: seeds_content = ''

#                 if (roots_content != '' or stems_content != '' or rhizomes_content != '' or leaves_content != '' or 
#                 flowers_content != '' or fruits_content != '' or seeds_content != ''):
#                     if roots_content != '':
#                         section_title = 'Roots'
#                         section_content = roots_content
#                         article += f'## {section_title}\n\n'
#                         article += '\n\n' + section_content + '\n\n'
#                         lines = csv_get_table_data(f'database/tables/morphology/{section_title.lower()}.csv')
#                         article += generate_table(lines)
#                     if stems_content != '':
#                         section_title = 'Stems'
#                         section_content = stems_content
#                         article += f'## {section_title}\n\n'
#                         article += '\n\n' + section_content + '\n\n'
#                         lines = csv_get_table_data(f'database/tables/morphology/{section_title.lower()}.csv')
#                         article += generate_table(lines)
#                     if rhizomes_content != '':
#                         section_title = 'Rhizomes'
#                         section_content = rhizomes_content
#                         article += f'## {section_title}\n\n'
#                         article += '\n\n' + section_content + '\n\n'
#                         lines = csv_get_table_data(f'database/tables/morphology/{section_title.lower()}.csv')
#                         article += generate_table(lines)
#                     if leaves_content != '':
#                         section_title = 'Leaves'
#                         section_content = leaves_content
#                         article += f'## {section_title}\n\n'
#                         article += '\n\n' + section_content + '\n\n'
#                         lines = csv_get_table_data(f'database/tables/morphology/{section_title.lower()}.csv')
#                         article += generate_table(lines)
#                     if flowers_content != '':
#                         section_title = 'Flowers'
#                         section_content = flowers_content
#                         article += f'## {section_title}\n\n'
#                         article += '\n\n' + section_content + '\n\n'
#                         lines = csv_get_table_data(f'database/tables/morphology/{section_title.lower()}.csv')
#                         article += generate_table(lines)
#                     if fruits_content != '':
#                         section_title = 'Fruits'
#                         section_content = fruits_content
#                         article += f'## {section_title}\n\n'
#                         article += '\n\n' + section_content + '\n\n'
#                         lines = csv_get_table_data(f'database/tables/morphology/{section_title.lower()}.csv')
#                         article += generate_table(lines)
#                     if seeds_content != '':
#                         section_title = 'Seeds'
#                         section_content = seeds_content
#                         article += f'## {section_title}\n\n'
#                         article += '\n\n' + section_content + '\n\n'
#                         lines = csv_get_table_data(f'database/tables/morphology/{section_title.lower()}.csv')
#                         article += generate_table(lines)
                    


#                 else:
#                     # sections
#                     main_content = item['main_content']
#                     for section in main_content:
#                         section_title = section["title"]
#                         section_content = section["content"]
#                         article += f'## {section_title}\n\n'
#                         article += '\n\n'.join(section_content) + '\n\n'

#                         # filepath = f'database/articles/{entity}/morphology/{attribute}/flowers.csv'
#                         # print(filepath)

                        
#                         # if 'fruits'.lower() != section_title.lower(): continue
                        
#                         lines = csv_get_table_data(f'database/tables/morphology/{section["title"].lower()}.csv')
#                         article += generate_table(lines)
#                         # for line in lines:
#                         #     print(line)

#                         # subparts
#                         try: subparts = section['subparts']
#                         except: subparts = None
#                         if subparts:
#                             for subpart in subparts:
#                                 subpart_name = subpart['name']
#                                 subpart_desc = subpart['desc']
#                                 article += f'### {subpart_name}\n\n'
#                                 article += '\n\n'.join(subpart_desc) + '\n\n'
#                                 lines = csv_get_table_data(f'database/tables/morphology/{section["title"].lower()}.csv')
#                                 article += generate_table(lines)
#                             # print(subparts)
#             else:
#                 continue

#                 main_content = item['main_content']

#                 title = f'{len(main_content)} Benefits of {latin_name}'
#                 article += f'# {title}\n\n'

#                 for i, section in enumerate(main_content):
#                     article += f'## {i+1}. {section["title"]}\n\n'
#                     article += '\n\n'.join(section['content']) + '\n\n'


#         else:
#             #######################################################################################################
#             #######################################################################################################
#             #######################################################################################################
#             # BOTANICAL
#             #######################################################################################################
#             #######################################################################################################
#             #######################################################################################################
#             if 'botanical' == attribute.lower():
#                 domain = item['domain']
            
#                 domain = item['domain']
#                 kingdom = item['kingdom']
#                 phylum = item['phylum']
#                 _class = item['class']
#                 order = item['order']
#                 family = item['family']
#                 genus = item['genus']
#                 species = item['species']

#                 most_common_name = item['common_names'][0].split(':')[0].lower()
#                 most_common_name_1 = item['common_names'][0].split(':')[0].lower()
#                 most_common_name_2 = item['common_names'][1].split(':')[0].lower()
#                 most_common_name_3 = item['common_names'][2].split(':')[0].lower()
#                 latin_name = f'{genus} {species}'
#                 latin_name_abb = f'{genus[0]}. {species}'

#                 common_names = item['common_names']
#                 regional_variations = item['regional_variations']
                
#                 distribution = item['distribution']
                
#                 habitat = item['habitat']
#                 morphology = item['morphology']
#                 life_cycle = item['life_cycle']
#                 reproduction = item['reproduction']

#                 history = item['history']
#                 history_medicinal_uses = item['history_medicinal_uses']
#                 history_culinary_uses = item['history_culinary_uses']
#                 history_spiritual_uses = item['history_spiritual_uses']
                    
#                 culinary_uses = item['culinary_uses']
#                 beverage_uses = item['beverage_uses']
#                 sensory_characteristics = item['sensory_characteristics']
                
#                 horticultural_cultivation = item['horticultural_cultivation']
#                 environmental_requirements = item['environmental_requirements']
#                 pests = item['pests']
#                 diseases = item['diseases']

#                 #######################################################################################################
#                 # TITLE
#                 #######################################################################################################
#                 article += f'# {latin_name.title()} ({most_common_name.title()}) Botanical Guide\n\n'

#                 featured_image_filename = latin_name.lower().replace(' ', '-') + '.jpg'
#                 featured_image_filpath = img_resize(f'articles-images/{featured_image_filename}')
#                 featured_image_filpath = '/' + '/'.join(featured_image_filpath.split('/')[1:])
#                 article += f'![alt]({featured_image_filpath} "title")\n\n'


#                 #######################################################################################################
#                 # TAXONOMY/CLASSIFICATION
#                 #######################################################################################################
#                 # article += f'## What is the classification (taxonomy) of {most_common_name}?\n\n'
#                 article += f'## What is the botanical classification of {most_common_name}?\n\n'
#                 line = f'''
#                     {most_common_name.title()}, with botanical name of **{latin_name}** ({latin_name_abb}), is a plant that belongs to the **{family}** family and the **{genus}** genus.

#                     According to traditional classification (taxonomy), this plant is classified under the **{order}** order, the **{_class}** class, and the **{kingdom}** kingdom (in the {domain} domain).
#                 \n\n'''
#                 article += re.sub(' +', ' ', line)

#                 lst = []
#                 lst_taxonomy = []
#                 lst_taxonomy.append(f'Domain: {domain}')
#                 lst_taxonomy.append(f'Kingdom: {kingdom}')
#                 lst_taxonomy.append(f'Phylum: {phylum}')
#                 lst_taxonomy.append(f'Class: {_class}')
#                 lst_taxonomy.append(f'Order: {order}')
#                 lst_taxonomy.append(f'Family: {family}')
#                 lst_taxonomy.append(f'Genus: {genus}')
#                 lst_taxonomy.append(f'Species: {species}')
#                 lst_taxonomy.insert(0, 'Taxonomy')
#                 lst.append(lst_taxonomy)

#                 lst_common_names = [x.split(':')[0] for x in common_names]
#                 lst_common_names.insert(0, 'Common Names')
#                 lst.append(lst_common_names)

#                 lst_regional_variations = [item.split(':')[0] for item in regional_variations]
#                 lst_regional_variations.insert(0, 'Regional Variations')
#                 lst.append(lst_regional_variations)

#                 # CHEAT SHEET
#                 # img_path = img_cheasheet(latin_name, 'Classification and Variations of', lst, 'taxonomy')
#                 # img_path = '/' + '/'.join(img_path.split('/')[1:])
#                 # article += f'The following illustration shows you this classificaion visually.\n\n'
#                 # article += f'![alt]({img_path} "title")\n\n'

#                 # TAXONOMY
#                 lst_taxonomy.pop(0)
#                 article += f'Here is a list showing the full taxonomy of {latin_name_abb}, in hierarchical order.\n\n'
#                 article += lst_to_blt(lst_taxonomy)
#                 article += '\n\n'

#                 # COMMON NAMES
#                 article += f'### What are the common names of {latin_name}?\n\n'
#                 article += f'The most common name for this plant is **{most_common_name_1.title()}**, but other common names are **{most_common_name_2.title()}** and **{most_common_name_3.title()}**.\n\n'
#                 article += f'Here is a list of the most common names of {latin_name_abb} ordered by popularity, with a brief description of each name.\n\n'
#                 bld = bold_blt(common_names)
#                 article += lst_to_blt(bld)
#                 article += '\n\n'

#                 # REGIONAL VARIATIONS
#                 names = [item.split(':')[0] for item in regional_variations]
#                 intro = ''
#                 intro += f'**{names[0].split("(")[0].strip()}**, **{names[1].split("(")[0].strip()}**, and **{names[2].split("(")[0].strip()}**'
#                 article += f'### What are the regional variations of {latin_name}?\n\n'
#                 article += f'The most common regional variations (subspecies) of this plant are {intro}.\n\n'
#                 article += f'In the following list, you can find a more extensive list of common variations of {latin_name_abb}, with a brief description of their unique characteristics and their main regional location.\n\n'
#                 regional_variations = [variation for variation in regional_variations]
#                 bld = bold_blt(regional_variations)
#                 article += lst_to_blt(bld)
#                 article += '\n\n'


#                 #######################################################################################################
#                 # MORPHOLOGY
#                 #######################################################################################################
#                 article += f'## What is the morphology of {latin_name_abb}?\n\n'
#                 article += '\n\n'.join([x for x in item['botanical_morphology_intro']]) + '\n\n'
#                 article += f'### Roots\n\n'
#                 article += lst_to_blt(bold_blt(item['botanical_morphology_roots'])) + '\n\n'
#                 article += f'### Stems\n\n'
#                 article += lst_to_blt(bold_blt(item['botanical_morphology_stems'])) + '\n\n'
#                 article += f'### Leaves\n\n'
#                 article += lst_to_blt(bold_blt(item['botanical_morphology_leaves'])) + '\n\n'
#                 article += f'### Flowers\n\n'
#                 article += lst_to_blt(bold_blt(item['botanical_morphology_flowers'])) + '\n\n'
#                 article += f'### Fruits\n\n'
#                 article += lst_to_blt(bold_blt(item['botanical_morphology_fruits'])) + '\n\n'
#                 article += f'### Seeds\n\n'
#                 article += lst_to_blt(bold_blt(item['botanical_morphology_seeds'])) + '\n\n'

                
#                 #######################################################################################################
#                 # DISTRIBUTION
#                 #######################################################################################################
#                 article += f'## What is the geographic distribution of {latin_name}?\n\n'
#                 article += lst_to_blt(bold_blt(item['botanical_geographic_distribution'])) + '\n\n'

#                 #######################################################################################################
#                 # HABITAT TYPES
#                 #######################################################################################################
#                 article += f'## What are the habitat types for {latin_name}?\n\n'
#                 article += lst_to_blt(bold_blt(item['botanical_habitat_types'])) + '\n\n'

#                 #######################################################################################################
#                 # CLIMATE
#                 #######################################################################################################
#                 article += f'## What are the climate preferences of {latin_name}?\n\n'
#                 article += lst_to_blt(bold_blt(item['botanical_climate'])) + '\n\n'

                


#                 # GROWING ZONES
#                 # growing_zones = item['growing_zones']
#                 # gz_range = growing_zones.split('-')
#                 # gz_lst = [i for i in range(int(gz_range[0]), int(gz_range[1])+1)]
#                 # lst = []
#                 # for gz in gz_lst:
#                 #     for x in growing_zones_data:
#                 #         if x['zone'] == gz:
#                 #             zone = x['zone']
#                 #             temp_fahrenheit_from = x["temperature_from"]
#                 #             temp_fahrenheit_to = x["temperature_to"]
#                 #             temp_celsius_from = round((temp_fahrenheit_from - 32) * 5/9, 1)
#                 #             temp_celsius_to = round((temp_fahrenheit_to - 32) * 5/9, 1)
#                 #             lst.append(f'Zone {zone}: Minimum temperature of {temp_fahrenheit_from}°F to {temp_fahrenheit_to}°F ({temp_celsius_from}°C to {temp_celsius_to}°C)')
#                 #             break

#                 # article += f'### What are the growing zones for {most_common_name}?\n\n'
#                 # article += f'The best growing zones for {most_common_name} are **USDA Hardiness Zones {growing_zones}**.\n\n'
#                 # article += f'Here is a breakdown of these zones and their minimum temperatures.\n\n'
#                 # bld = bold_blt(lst)
#                 # article += lst_to_blt(bld)
#                 # article += '\n\n'
                

#                 # LIFE CYCLE
#                 article += f'### Life cycle\n\n'
#                 lst = [item.split(':')[0].lower() for item in life_cycle]
#                 intro = lst_to_txt(lst)
#                 article += f'The life cycle phases of this plant are {intro}.\n\n'
#                 article += f'Here\'s a brief description of each phase.\n\n'
#                 bld = bold_blt(life_cycle)
#                 article += lst_to_blt(bld)
#                 article += '\n\n'

#                 # REPRODUCTION
#                 article += f'### Reproduction\n\n'
#                 article += f'Here\'s listed the different ways {most_common_name} reproduce and propagate.\n\n'
#                 bld = bold_blt(reproduction)
#                 article += lst_to_blt(bld)
#                 article += '\n\n'

#             # TODO: redo achillea millefolium to delete this section
#             elif 'morphology' in attribute.lower():
#                 #######################################################################################################
#                 # MORPHOLOGY
#                 #######################################################################################################
#                 title = f'What is the morphology of {latin_name}?'
#                 article += f'# {title}\n\n'

#                 featured_image_filpath = generate_featured_image(entity, attribute)
#                 article += f'![alt]({featured_image_filpath} "title")\n\n'
#                 article += '\n\n'.join([x for x in item['botanical_morphology_intro']]) + '\n\n'

#                 article += f'## {latin_name} roots morphology\n\n'.title()
#                 article += '\n\n'.join(item['botanical_morphology_roots_intro']) + '\n\n'
#                 article += f'The full description of the {latin_name} root morphology is given in the following list.' + '\n\n'
#                 article += lst_to_blt(bold_blt(item['botanical_morphology_roots'])) + '\n\n'

#                 try:
#                     intro = item['botanical_morphology_rhizomes_intro']
#                     article += f'## {latin_name} rhizomes morphology\n\n'.title()
#                     article += '\n\n'.join(intro) + '\n\n'
#                     article += f'The full description of the {latin_name} rhizomes morphology is given in the following list.' + '\n\n'
#                     article += lst_to_blt(bold_blt(item['botanical_morphology_rhizomes'])) + '\n\n'
#                 except: pass

#                 try:
#                     intro = item['botanical_morphology_stems_intro']
#                     article += f'## {latin_name} stems morphology\n\n'.title()
#                     article += '\n\n'.join(intro) + '\n\n'
#                     article += f'The full description of the {latin_name} stems morphology is given in the following list.' + '\n\n'
#                     article += lst_to_blt(bold_blt(item['botanical_morphology_stems'])) + '\n\n'
#                 except: pass
                
#                 try:
#                     intro = item['botanical_morphology_leaves_intro']
#                     article += f'## {latin_name} leaves morphology\n\n'.title()
#                     article += '\n\n'.join(intro) + '\n\n'
#                     article += f'The full description of the {latin_name} leaves morphology is given in the following list.' + '\n\n'
#                     article += lst_to_blt(bold_blt(item['botanical_morphology_leaves'])) + '\n\n'
#                 except: pass

#                 try:
#                     intro = item['botanical_morphology_inflorescence_intro']
#                     article += f'## {latin_name} inflorescence morphology\n\n'.title()
#                     article += '\n\n'.join(intro) + '\n\n'
#                     article += f'The full description of the {latin_name} inflorescence morphology is given in the following list.' + '\n\n'
#                     article += lst_to_blt(bold_blt(item['botanical_morphology_inflorescence'])) + '\n\n'
#                 except: pass
                
#                 # try:
#                 #     intro = item['botanical_morphology_spadix_intro']
#                 #     article += f'## spadix morphology\n\n'.title()
#                 #     article += '\n\n'.join(intro) + '\n\n'
#                 #     article += f'The full description of the {latin_name} spadix morphology is given in the following list.' + '\n\n'
#                 #     article += lst_to_blt(bold_blt(item['botanical_morphology_spadix'])) + '\n\n'
#                 # except: pass
                
#                 # try:
#                 #     intro = item['botanical_morphology_spathe_intro']
#                 #     article += f'## spathe morphology\n\n'.title()
#                 #     article += '\n\n'.join(intro) + '\n\n'
#                 #     article += f'The full description of the {latin_name} spathe morphology is given in the following list.' + '\n\n'
#                 #     article += lst_to_blt(bold_blt(item['botanical_morphology_spathe'])) + '\n\n'
#                 # except: pass
                
#                 try:
#                     intro = item['botanical_morphology_flowers_intro']
#                     article += f'## {latin_name} flowers morphology\n\n'.title()
#                     article += '\n\n'.join(intro) + '\n\n'
#                     article += f'The full description of the {latin_name} flowers morphology is given in the following list.' + '\n\n'
#                     article += lst_to_blt(bold_blt(item['botanical_morphology_flowers'])) + '\n\n'
#                 except: pass
                
#                 article += f'## {latin_name} fruits morphology\n\n'.title()
#                 article += '\n\n'.join(item['botanical_morphology_fruits_intro']) + '\n\n'
#                 article += f'The full description of the {latin_name} fruits morphology is given in the following list.' + '\n\n'
#                 article += lst_to_blt(bold_blt(item['botanical_morphology_fruits'])) + '\n\n'
                
#                 article += f'## {latin_name} seeds morphology\n\n'.title()
#                 article += '\n\n'.join(item['botanical_morphology_seeds_intro']) + '\n\n'
#                 article += f'The full description of the {latin_name} seeds morphology is given in the following list.' + '\n\n'
#                 article += lst_to_blt(bold_blt(item['botanical_morphology_seeds'])) + '\n\n'


#         article_filepath = generate_html(title, article, entity, attribute)

#         if publishing_state == 'published':
#             articles_home.append(
#                 {
#                     'img': featured_image_filpath,
#                     'url': article_filepath,
#                     'name': most_common_name.title(),
#                     'title': title,
#                 }
#             )




        

        


##################################################################################################
# PLANTS PAGE
##################################################################################################
# taxonomy = {}

# for article in articles_home:
#     article_folders = article['url'].split('/')

#     full_path_curr = ''
#     for i in range(len(article_folders)-1):
#         folder_curr = article_folders[i]
#         folder_next = article_folders[i+1]

#         full_path_curr += f'{folder_curr}/'

#         if full_path_curr not in taxonomy: 
#             taxonomy[full_path_curr] = [folder_next]
#         else: 
#             if folder_next not in taxonomy[full_path_curr]:
#                 taxonomy[full_path_curr].append(folder_next)

# for key, lst in taxonomy.items():
#     for val in lst:
#         if not os.path.exists(f'website/{key}/index.html'):
#             with open(f'website/{key}/index.html', 'w') as f:
#                 f.write(f'<p><a href="{val}">{val}</a></p>')
#         else: 
#             with open(f'website/{key}/index.html', 'a') as f:
#                 f.write(f'<p><a href="{val}">{val}</a></p>')





##################################################################################################
# HOME PAGE
##################################################################################################



# articles = ''
# for article in articles_home:
#     img = article['img']
#     url = article['url']
#     title = article['title']
#     name = article['name']
#     articles += f'''
#         <div class="flex gap-32">
#             <div class="flex-1">
#                 <img src="{img}" alt="">
#             </div>
#             <div class="flex-1">
#                 <h2 class="mt-0">{title}</h2>
#                 <p>
#                     Lorem ipsum, dolor sit amet consectetur adipisicing elit. Porro beatae consequatur ad
#                     quod,
#                     accusamus numquam velit nisi sint. Rerum eaque animi, enim ipsam laborum rem vitae
#                     repellendus
#                     vero
#                     quod corporis.
#                 </p>
#                 <a
#                     href="{url}">{name} Guide</a>
#             </div>
#         </div>
#         \n
#     '''


