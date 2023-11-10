import sys
import csv
import utils

if len(sys.argv) < 2:
    print("ERR: missing arguments (ENTITY, ATTRIBUTES)")
    quit()

entity = sys.argv[1]
latin_name = entity.replace('-', ' ').capitalize()
latin_name_abbreviated = latin_name.split(' ')[0][0] + '. ' + latin_name.split(' ')[1]

attribute_1 = ''
try: attribute_1 = sys.argv[2].lower().strip()
except: pass
attribute_2 = ''
try: attribute_2 = sys.argv[3].lower().strip()
except: pass

def csv_get_table_data(filepath, entity):
    lines = []
    with open(filepath) as f:
        reader = csv.reader(f, delimiter="|")
        for i, line in enumerate(reader):
            if i == 0:
                lines.append(line)
            else:
                if line[0].strip() == entity.strip():
                    lines.append(line)
    return lines

print(entity)
print(latin_name)
print(latin_name_abbreviated)
print(attribute_1)
print(attribute_2)


try:
    common_names_rows = utils.csv_get_rows_by_entity('database/tables/botany/common-names.csv', entity)
    common_name = common_names_rows[0][1]
except:
    common_names_rows = []
    common_name = ''

print(common_name)


print()
print()
print()
print()
print()

format_table = f'''
        For each characteristic in the above list write a precise description, by adding the exact information, numbers, and data. 
        Use as few words as possible for each description. 
        Use primarily the metric system for numbers, and put the imperial system in between parenthesis with data and numbers.

        Put all the data in table format. The table must have only 2 columns.
'''

dtt = f'''
        Using the data from the previous table, write a section for an article in less than 300 words. 
        Don't write in list format. Write in discursive format. 
        Use simple language and a straightforward sentence structure.
        Don't add fluff or opinions, just write facts.

        ---------------------------------------------------------------
'''

def morphology():
    i = 1
    print(f'''
    {i}. ALL PARTS

    Give me a complete list of all the parts of {latin_name} in terms of morphology. 
    Don't add descriptions.
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')
    i += 1

    print(f'''
    {i}. ROOTS

    Give me a complete list of all the parts of STEMS of the {latin_name}. 
    Don't add descriptions.
    ''')
    print(f'''
    {i}. STEMS

    Give me a complete list of all the parts of STEMS of the {latin_name}. 
    Don't add descriptions.
    ''')
    print(f'''
    {i}. RHIZOME

    Give me a complete list of all the parts of RHIZOME of the {latin_name}. 
    Don't add descriptions.
    ''')
    print(f'''
    {i}. LEAVES

    Give me a complete list of all the parts of LEAVES of the {latin_name}. 
    Don't add descriptions.
    ''')
    print(f'''
    {i}. FLOWERS

    Give me a complete list of all the parts of FLOWERS of the {latin_name}. 
    Don't add descriptions.
    ''')
    print(f'''
    {i}. FRUITS

    Give me a complete list of all the parts of FRUITS of the {latin_name}. 
    Don't add descriptions.
    ''')
    print(f'''
    {i}. SEEDS

    Give me a complete list of all the parts of SEEDS of the {latin_name}. 
    Don't add descriptions.
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')
    i += 1



    print(f'''{i}. ROOTS CHARACTERISTICS

        Here's a list of morphological characteristics of roots of {latin_name}:

        - Root System Type
        - Root Structure
        - Root Branching
        - Root Tips
        - Root Density
        - Root Depth
        - Root Diameter
        - Root Length
        - Root Color
        - Root Surface Texture
        - Root Nodules
        - Root Hairs

        {format_table}

        ----------------------------------------------------------------

        {dtt}
    ''')


    print(f'''{i}. STEMS CHARACTERISTICS

        Here's a list of morphological characteristics of stems of {latin_name}:

        - Stem Type
        - Stem Arrangement
        - Stem Shape
        - Stem Height
        - Stem Diameter
        - Stem Color
        - Stem Texture
        - Stem Surface
        - Stem Nodes
        - Stem Internodes

        {format_table}
        
        ----------------------------------------------------------------

        {dtt}
    ''')


    # print(f'''{i}. RHIZOMES CHARACTERISTICS

    #     Here's a list of morphological characteristics of rhizomes of {latin_name}:

    #     - Rhizome Arrangement
    #     - Rhizome Shape
    #     - Rhizome Height
    #     - Rhizome Diameter
    #     - Rhizome Color
    #     - Rhizome Surface Texture
    #     - Rhizome Nodes
    #     - Rhizome Internodes

    #     {format_table}
        
    #     ----------------------------------------------------------------

    #     {dtt}
    # ''')
    # print(f'''
    # --------------------------------------------------------------------
    # ''')


    print(f'''{i}. LEAVES CHARACTERISTICS

        Here's a list of morphological characteristics of leaves of {latin_name}:

        - Leaf Complexity
        - Leaf Shape
        - Leaf Arrangement
        - Leaf Orientation
        - Leaf Length
        - Leaf Width
        - Leaf Thickness
        - Leaf Color
        - Leaf Texture
        - Leaf Surface
        - Leaf Apex
        - Leaf Base
        - Leaf Margin
        - Leaf Venation
        - Leaf Lamina
        - Leaf Midrib
        - Leaf Attachment
        - Leaf Petiole
        - Leaf Stipules

        {format_table}
        
        ----------------------------------------------------------------

        {dtt}
    ''')


    print(f''' {i}. FLOWERS CHARACTERISTICS

        Here's a list of morphological characteristics of flowers of {latin_name}:

        - Inflorescence Type
        - Flower Complexity
        - Flower Symmetry
        - Flower Structure
        - Flower Attachment
        - Flower Shape
        - Flower Length
        - Flower Width 
        - Flower Color
        - Flower Texture
        - Flower Surface
        - Number of Floral Parts
        - Flower Sepals
        - Flower Petals
        - Flower Perianth
        - Flower Stamen
        - Flower Pistil
        - Flower Ovary
        - Flower Style
        - Flower Stigma
        - Flower Stipules
        - Flower Bracts
        - Flower Peduncle 
        - Flower Pedicel

        {format_table}
        
        ----------------------------------------------------------------

        {dtt}
    ''')


    print(f'''{i}. FRUITS CHARACTERISTICS

        Here's a list of morphological characteristics of fruits of {latin_name}:

        - Fruit Type
        - Fruit Arrangement
        - Fruit Distribution
        - Fruit Attachment
        - Fruit Shape
        - Fruit Length
        - Fruit Width
        - Fruit Thickness
        - Fruit Color
        - Fruit Texture
        - Fruit Surface
        - Fruit Marking
        - Fruit Dehiscence

        {format_table}
        
        ----------------------------------------------------------------

        {dtt}
    ''')


    print(f'''{i}. SEEDS CHARACTERISTICS

        Here's a list of morphological characteristics of seeds of {latin_name}:

        - Seed Type
        - Seed Arrangement
        - Seed Shape
        - Seed Appendages
        - Seed Number
        - Seed Length
        - Seed Width
        - Seed Thickness
        - Seed Hardness
        - Seed Coat Color
        - Seed Coat Surface
        - Seed Coat Texture
        - Seed Coat Thickness
        - Seed Coat Permeability
        - Seed Hilum
        - Seed Embryo
        - Seed Cotyledon
        - Seed Radicle

        {format_table}
        
        ----------------------------------------------------------------

        {dtt}
    ''')
    i += 1


    print(f''' {i}. INTRO
        Summarize the following text in less than 200 words, without using lists, only discursive text:
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')
    i += 1

##################################################################
# taxonomy 
##################################################################
def taxonomy():

    print(f'''TAXONOMY

        Give me the taxonomy of {latin_name}.

        Include:

        - Domain
        - Kingdom
        - Phylum
        - Class
        - Order
        - Family
        - Genus
        - Species

        Format the data in a 2-column table.
        In the first column of the table, write the elements in the list.
        In the second column of the table, write the answer. 

        --------------------------------------------------------------------

        Using the data from the previous table, write a section for an article in less than 300 words. 
        Don't write in list format. Write in discursive format. 
        Use simple language and a straightforward sentence structure.
        Don't add fluff or opinions, just write facts.
        
        



        ''')

    print(f'''COMMON NAMES

        Write a list of 10 common names of {latin_name}. Add a description for each name.

        --------------------------------------------------------------------

        Using the data from the previous table, write a section for an article in less than 300 words. 
        Don't write in list format. Write in discursive format. 
        Use simple language and a straightforward sentence structure.
        Don't add fluff or opinions, just write facts.




        
        ''')
    
    print(f'''VARIETIES

        Give me a list of 10 varieties of {latin_name}. Add a description for each name.

        --------------------------------------------------------------------
    
        Using the data from the previous table, write a section for an article in less than 300 words. 
        Don't write in list format. Write in discursive format. 
        Use simple language and a straightforward sentence structure.
        Don't add fluff or opinions, just write facts.





        ''')
    
    text = ''

    filenames = ['roots', 'stems', 'leaves', 'flowers', 'fruits', 'seeds',]
    for filename in filenames:
        filepath = f'database/tables/morphology/{filename}.csv'
        tmp_header = []
        tmp_values = []
        with open(filepath, encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter="\\")
            for k, row in enumerate(reader):
                if k == 0:
                    tmp_header = row
                    continue
                if entity == row[0].strip():
                    tmp_values = row
                    break
        
        lst = []
        for k in range(len(tmp_values)):
            if k == 0: continue
            if tmp_values[k].strip() != '':
                lst.append(f'- {tmp_header[k]}: ' + tmp_values[k])
        text += '\n'.join(lst)


    print(f'''SECONDARY-CONTENT (MORPHOLOGY)

        Write an overall description of the appearance of {latin_name} by using the data in the following tables:
        
        {text}

        Use less than 100 words in your answer.
        Start the reply with the following sentence:

        Knowing the Morphology of {latin_name} is useful if you want to be able to classify this plant.
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')

    print(f'''INTRO HIGHLIGHTS

       Give me 3 highlights about the following text in less than 100 words:
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')

    print(f'''INTRO TEXT

       Write an intro paragraph about {latin_name} using the highlights from your previous reply.
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')


##################################################################
# DISTRIBUTION 
##################################################################
def distribution():

    print(f'''NATURAL HABITAT

        Give me a list of the natural habitats of {latin_name} ordered by most frequent. Just give me the names, don't give me descriptions.

        --------------------------------------------------------------------

        Give me a description for each name in the previous list. Use a scientific style of writing but use a simple and straightforward sentence structure.

        --------------------------------------------------------------------

        Using the data from the previous list, write a section for an article in less than 300 words. 
        Don't write in list format. Write in discursive format. 
        Use a scientific style of writing but use a simple and straightforward sentence structure.
        Don't add fluff or opinions, just write facts.


        ''')

    print(f'''NATIVE

        Give me a list of continents where {latin_name} is native and not imported. Give me only the names, not the descriptions.

        --------------------------------------------------------------------

        For each of the above continents, give me a list of states where {latin_name} is native and not imported.

        --------------------------------------------------------------------

        Generate a table with 2 columns.

        In the first column, write the list of continents from the last reply.
        In the second column, write the corresponding list of states from the last reply.

        The title of the first column is "Continent".
        The title of the second column is "States".

        --------------------------------------------------------------------

        Using the data from the previous list, write a section for an article in less than 300 words. 
        Don't write in list format. Write in discursive format. 
        Use a scientific style of writing but use a simple and straightforward sentence structure.
        Don't add fluff or opinions, just write facts.



        ''')
        
    print(f'''DISTRIBUTION

        Generate a table with 2 columns.

        In the first column, list the continents in this order: Europe, Asia, Africa, North America, South America, Australia, Antarctica
        In the second column, write an estimate of the distribution of {latin_name} with a word that can be "Abundant", "Moderate", "Scarce", or "Absent".

        --------------------------------------------------------------------

        Using the data from the previous table, write a section for an article in less than 300 words without mentioning the numbers in the second column. 
        Don't write in list format. Write in discursive format. 
        Use a scientific style of writing but use a simple and straightforward sentence structure.
        Don't add fluff or opinions, just write facts.
        
        --------------------------------------------------------------------



        ''')
        
    print(f'''INVASIVE

        List of regions where {latin_name} is considered invasive?

        --------------------------------------------------------------------

        Using the data from the previous list, write a section for an article in less than 300 words about the invasiveness of {latin_name}.
        Don't write in list format. Write in discursive format.
        Use a scientific style of writing but use a simple and straightforward sentence structure.
        Don't add fluff or opinions, just write facts.

        The title of the section (h2) is:

        "Is {latin_name} invasive?"

        --------------------------------------------------------------------



        ''')    

    print(f'''INVASIVE IMPACT

        List of regions where {latin_name} is considered invasive?

        --------------------------------------------------------------------

        Using the data from the previous list, write a section for an article in less than 200 words about the impact of {latin_name} as an invasive species.
        Don't write in list format. Write in discursive format.
        Use a scientific style of writing but use a simple and straightforward sentence structure.
        Don't add fluff or opinions, just write facts.

        The title of the section is:

        "What's the impact of {latin_name} as an invasive species"

        --------------------------------------------------------------------



        ''')


def botany():
    text = ''
    filenames = ['roots', 'stems', 'leaves', 'flowers', 'fruits', 'seeds',]
    for filename in filenames:
        filepath = f'database/tables/morphology/{filename}.csv'
        tmp_header = []
        tmp_values = []
        with open(filepath, encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter="\\")
            for k, row in enumerate(reader):
                if k == 0:
                    tmp_header = row
                    continue
                if entity == row[0].strip():
                    tmp_values = row
                    break
        
        lst = []
        for k in range(len(tmp_values)):
            if k == 0: continue
            if tmp_values[k].strip() != '':
                lst.append(f'- {tmp_header[k]}: ' + tmp_values[k])
        text += '\n'.join(lst)

    print(f'''MORPHOLOGY

        Write me the morphology of Achillea millefolium. Include the following parts:

        Roots
        Stems
        Leaves
        Flowers
        Fruits
        Seeds

        Give me as much data, info, and numbers as possible for each part. Use the metric system for the numbers. Write using a discursive format, not lists.

        Reference the following list to extract the data, info, and numbers:

        {text}

        
        
        Also, start the reply with the following sentence:

        Knowing the Morphology of {latin_name} is useful if you want to be able to classify this plant.
    
        --------------------------------------------------------------------
        

        
        ''')

    print(f'''LIFE-CYCLE

        Write a detailed description of the life cycle of Achillea millefolium. 
        Compress as many details, numbers, and data in as few words as possible. 
        Use a scientific writing style, with a simple and straightforward sentence structure in active voice 
        ({latin_name} must always be the subject in every sentence).
        Don't add fluff or opinions, only facts.
    
        --------------------------------------------------------------------

        Is yarrow perennial? If so, give me details about why it is.

        --------------------------------------------------------------------


        
        ''')


# Achillea millefolium, commonly known as yarrow, belongs to the domain Eukaryota and the kingdom Plantae. It is classified under the Angiosperms (or Magnoliophyta) as a Eudicot, placing it within the order Asterales. This plant is a member of the family Asteraceae and is specifically categorized under the genus Achillea. Its full scientific name is Achillea millefolium, encompassing its various taxonomic levels within the plant kingdom.

def main():

    filepath = f'database/tables/botany/taxonomy.csv'
    taxonomy_rows = csv_get_table_data(filepath, entity)
    taxonomy_rows = [f'-{x}' for x in taxonomy_rows[1][1:]]
    taxonomy_rows = '\n'.join(taxonomy_rows)

    common_names_lst = [f'- {x[1]}' for x in common_names_rows]
    common_names_lst = '\n'.join(common_names_lst)

    varieties_rows = utils.csv_get_rows_by_entity('database/tables/botany/varieties.csv', 'achillea-millefolium')
    varieties_rows = [f'- {x[1]}' for x in varieties_rows]
    varieties_rows = '\n'.join(varieties_rows)

    morphology_rows = ''
    filenames = ['roots', 'stems', 'leaves', 'flowers', 'fruits', 'seeds',]
    for filename in filenames:
        filepath = f'database/tables/morphology/{filename}.csv'
        tmp_header = []
        tmp_values = []
        with open(filepath, encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f, delimiter="\\")
            for k, row in enumerate(reader):
                if k == 0:
                    tmp_header = row
                    continue
                if entity == row[0].strip():
                    tmp_values = row
                    break
        
        lst = []
        for k in range(len(tmp_values)):
            if k == 0: continue
            if tmp_values[k].strip() != '':
                lst.append(f'- {tmp_header[k]}: ' + tmp_values[k])
        morphology_rows += '\n'.join(lst)

    print(f'''BOTANICAL
        Write a paragraph about the taxonomy of {latin_name}. 
        Include as many details as possible in as few words as possible.
        Include all the data from the following list for the taxonomy:

        {taxonomy_rows}

        Also, start the paragraph with the following words:

        {common_name} ({latin_name})

        --------------------------------------------------------------------

        Write a paragraph about the common names of {latin_name}. 
        Include as many details as possible in as few words as possible.
        Include all the names in the following list:

        {common_names_lst}

        Also, start the paragraph with the following words:

        {latin_name} has many common names, but the most common is {common_name}. Other common names are

        --------------------------------------------------------------------
        
        Write a paragraph about the variants of {latin_name}. 
        Include as many details as possible in as few words as possible.
        Include all the variants in the following list:

        {varieties_rows}

        Also, start the paragraph with the following words:

        {latin_name_abbreviated} also has many varieties, such as

        --------------------------------------------------------------------

        Write a paragraph about the morphology of {latin_name}. 
        Include as many details as possible in as few words as possible.
        Make sure that that what you write doesn't conflict with the data given in the following list:

        {morphology_rows}

        Also, start the paragraph with the following words:
        
        In terms of morphology, this plant

        --------------------------------------------------------------------
        
        Write a paragraph about the regions where {latin_name} is native, naturalized, or both.
        Don't talk about the habitats, just talk about the regional distribution around the world.
        Include as many details as possible in as few words as possible.
        Include if this plant is invasive at the end of the paragraph.

        Also, start the paragraph with the following words:
        
        About {common_name}'s geographic distribution, it is
        
        --------------------------------------------------------------------

        Write a paragraph about the habitat of {latin_name}.
        Don't mention its geographical distribution, write only about the habitat.
        Don't mention its morphological characteristics, write only about the habitat.
        Include as many details as possible in as few words as possible.
        Also include if this plant is annual or perennial at the beginning of paragraph.




        
        ''')

    print(f'''MEDICINAL

        Write a paragraph about the medicinal uses of {common_name} ({latin_name}). 
        Include as many details as possible in as few words as possible.

        --------------------------------------------------------------------

        Write a paragraph about the active compounds of {common_name} ({latin_name}). 
        Include as many details as possible in as few words as possible.

        --------------------------------------------------------------------
        
        Write a paragraph about the traditional and modern uses of {common_name} ({latin_name}) for medicinal purposes.
        Include as many details as possible in as few words as possible.
        Don't include the native range of this plant.
        Don't include the morphology of this plant.
        Don't include the common names or the varieties of this plant.
        Don't include the constituents of this plant.

        --------------------------------------------------------------------

        Write a paragraph about the precautions of using {common_name} ({latin_name}) for medicinal purposes.
        Include as many details as possible in as few words as possible.

        --------------------------------------------------------------------

        Write a section of an article on the medicinal uses of {common_name} ({latin_name}) in about 400 words.
        
        This section must have 4 paragraphs.

        In the first paragraph, write about the modern medicinal applications of this plant.
        In the second paragraph, write about the active compounds of this plant.
        In the third paragraph, write about the different types of preparations of this plant.
        In the fourth paragraph, write about the safety and precautions of this plant.

        Include as many details, data, and numbers as possible in as few words as possible.
        Use the metric system as the primary measuring system.

        --------------------------------------------------------------------
        
        Write 4 paragraphs about {common_name} ({latin_name}).

        In the first paragraph, write about the modern medicinal applications of this plant.
        In the second paragraph, write about the active compounds of this plant for medicinal purposes.
        In the third paragraph, write about the different types of preparations of this plant for medicinal purposes.
        In the fourth paragraph, write about the safety and precautions of this plant for medicinal pusposes.

        Include as many details, data, and numbers as possible in as few words as possible.
        Use the metric system as the primary measuring system.

        --------------------------------------------------------------------

        Write me a list of the 10 most important health benefits of {common_name} ({latin_name}). 
        Start each benefit with a verb.





        ''')

    print(f'''CULINARY

        Write a paragraph about the culinary uses of {common_name} ({latin_name}). 
        Include as many details as possible in as few words as possible.

        --------------------------------------------------------------------

        Write a paragraph about the flavor profile of {common_name} ({latin_name}). 
        Include as many details as possible in as few words as possible.
        Don't mention its botanical aspects.
        Don't mention its medicinal uses.
        Don't mention its herbal preparations.
        Don't mention its culinary uses.

        --------------------------------------------------------------------
        
        Write 3 paragraphs about {common_name} ({latin_name}).

        In the first paragraph, write about the culinary uses of this plant (if edible).
        In the second paragraph, write about the flavor profile of this plant.
        In the third paragraph, write about the culinary tips when using this plant (if edible).

        Include as many details, data, and numbers as possible in as few words as possible.
        Use the metric system as the primary measuring system.

        --------------------------------------------------------------------

        Write me a list of the 10 most important culinary uses of {common_name} ({latin_name}).





        ''')

    print(f'''CULTIVATION

        Write 3 paragraphs about {common_name} ({latin_name}).

        In the first paragraph, write about how to grow this plant in your garden or landscape.
        In the second paragraph, write about the ideal growing conditions and soil requirements for this plant.
        In the third paragraph, write about pruning and maintenance tips to keep this plant healthy

        Include as many details as possible in as few words as possible.
        Use the metric system as the primary measuring system.

        --------------------------------------------------------------------

        Write me a list of the 10 most important cultivation tips for {common_name} ({latin_name}). 
        Give me just the tips, don't add descriptions. 
        Every tip must be less than 5 words. 
        Every tip must start with a verb.
        Use the metric system as the primary measuring system.





        ''')
        
    print(f'''BOTANICAL 2

        Write 4 paragraphs about {common_name} ({latin_name}).

        In the first paragraph, write about how the traditional taxonomy of this plant (include domain, kingdom, phylum, class, order, family, genus, species).
        In the second paragraph, write about the common name and variants of this plant.
        In the third paragraph, write about the general morphology of this plant.
        In the fourth paragraph, write about the geographic distribution and habitat of this plant.

        Include as many details as possible in as few words as possible.
        Use the metric system as the primary measuring system.
        Write each paragraph in discursive format, don't use lists.
        Don't mention this plant's culinary uses.
        Don't mention this plant's medicinal uses.

        Make sure that what you write doesn't contradict with the data given in the following list:

        {morphology_rows}

        --------------------------------------------------------------------

        Write me a list of the 10 most important cultivation tips for {common_name} ({latin_name}). 
        Give me just the tips, don't add descriptions. 
        Every tip must be less than 5 words. 
        Every tip must start with a verb.
        Use the metric system as the primary measuring system.

        --------------------------------------------------------------------


        Write a paragraph about the regional distribution and habitat of {common_name} ({latin_name})
        Include as many details as possible in as few words as possible.
        Don't mention the uses of this plant.
        Don't mention the morphology of this plant.

        Also, start the paragraph with the following words:
        
        About {common_name}'s geographic distribution, it is





        ''')

    print(f'''HISTORY FOLKLORE
    
        Write 3 paragraphs about {common_name} ({latin_name}).

        In the first paragraph, write about this plant in traditional folk medicine and its role in different cultures.
        In the second paragraph, write about the ancient uses of this plant in divination.
        In the third paragraph, write about the legends and myths surrounding this plant.

        Include as many details as possible in as few words as possible.
        Use the metric system as the primary measuring system.

        --------------------------------------------------------------------

        Write me a list of the 10 most well known historical folkloristic uses of {common_name} ({latin_name}). 
        Give me just the uses, don't add descriptions. 
        Every item in the list must be less than 5 words.

        --------------------------------------------------------------------

        Ok, rewrite the items in the previous list using less than 5 words for each item.

        --------------------------------------------------------------------
        
        Ok, now add a brief description to each element in the previous list.





        ''')


# give me 2 lists:

# in the first list write the native regions where yarrow is found.
# in the second list write the naturalized regions where yarrow is found.



def medicine():

    print(f'''MEDICINAL PROPERTIES

        Write me a list of the 10 major health benefits of {common_name} ({latin_name}). 
        Start each benefit with a verb.

        --------------------------------------------------------------------

        Write a paragraph about the health benefits and medicinal properties of {common_name} ({latin_name}).
        Include the elements in the list above.
        Pack as much data as possible in as few words as possible.

        --------------------------------------------------------------------

        Using the data from the list above, write about 300 words on the medicinal benefits of {common_name} ({latin_name}).
        Pack as much data, info, and numbers as possible.
        Use the metric system when expressing numbers.
        Don't add subjective fluff or opinions, just objective facts. 

        --------------------------------------------------------------------
        
        Ok, now include some numbers to back up your claims.

        --------------------------------------------------------------------

        Ok, now use the data from the list above to write a section about the benefits of {common_name} ({latin_name}) in about 300 words.
        This section must not use a list format. 

        --------------------------------------------------------------------





        ''')

    print(f'''KEY CONSTITUENTS

        Write me a list of the 10 key constituents of {common_name} ({latin_name}) for health purposes. 

        --------------------------------------------------------------------

        Write a paragraph about the key constituents of {common_name} ({latin_name}).
        Include the elements in the list above.
        Pack as much data as possible in as few words as possible.

        --------------------------------------------------------------------
        
        Using the data from the list above, write about 300 words on the key constituents of {common_name} ({latin_name}).
        Pack as much data, info, and numbers as possible.
        Use the metric system when expressing numbers.
        Don't add subjective fluff or opinions, just objective facts. 

        --------------------------------------------------------------------

        Ok, now include some numbers to back up your claims.

        --------------------------------------------------------------------

        Ok, now use the data from the list above to write a section about the key constituents of {common_name} ({latin_name}) in about 300 words.
        Write in a discursive way, do not use a list format.

        --------------------------------------------------------------------





        ''')

    print(f'''KEY PREPARATIONS

        Write me a list of key preparations of {common_name} ({latin_name}) for health purposes. Use a flat list style, don't put lists inside lists.

        --------------------------------------------------------------------

        Write a paragraph about the key preparations of {common_name} ({latin_name}).
        Include the elements in the list above.
        Pack as much data as possible in as few words as possible.

        --------------------------------------------------------------------
        
        Using the list above, write about 300 words on the key preparations of {common_name} ({latin_name}).
        Pack as much data, info, and numbers as possible.
        Use the metric system when expressing numbers.
        Don't add subjective fluff or opinions, just objective facts. 

        --------------------------------------------------------------------

        Ok, now include some numbers to back up your claims.

        --------------------------------------------------------------------

        Ok, now use the data from the list above to write a section about the key preparations of {common_name} ({latin_name}) in about 300 words.
        Write in a discursive way, do not use a list format.

        --------------------------------------------------------------------





        ''')
        
    print(f'''SAFETY AND PRECAUTIONS

        Write me a list of precautions when using {common_name} ({latin_name}) as a medicine. 
        Use a flat list style, don't put lists inside lists.

        --------------------------------------------------------------------

        Write a paragraph about the precautions of {common_name} ({latin_name}).
        Include the elements in the list above.
        Pack as much data as possible in as few words as possible.

        --------------------------------------------------------------------
        
        Using the list above, write about 300 words on the precautions of {common_name} ({latin_name}).
        Pack as much data, info, and numbers as possible.
        Use the metric system when expressing numbers.
        Don't add subjective fluff or opinions, just objective facts. 

        --------------------------------------------------------------------

        Ok, now include some numbers to back up your claims.

        --------------------------------------------------------------------

        Ok, now use the data from the list above to write a section about the precautions of {common_name} ({latin_name}) in about 300 words.
        Write in a discursive way, do not use a list format.

        --------------------------------------------------------------------





        ''')


def medicine_benefits():
    
    rows = utils.csv_get_rows_by_entity(f'database/tables/medicine/benefits.csv', entity)
    benefits = [f'{x[1]}' for x in rows[:10]]
    images_text = ''
    for i, item in enumerate(benefits):
        images_text += f'''{i}.
        Write me a list of constituents of {common_name} ({latin_name}) that help {item}.
        Write just the names, don't write descriptions.
        Order the list from the most helpful item to the least helpful.
        
        Write me a list of preparations of {common_name} ({latin_name}) that help {item}.
        Write just the names, don't write descriptions.
        Order the list from the most helpful item to the least helpful.

        --------------------------------------------------------------------
        
        '''


    print(f'''10 BENEFITS
    
        Write 3 paragraphs about {common_name} ({latin_name}).

        In the first paragraph, write about this plant's ability to ___, and what constituents this plant has to get this health benefit. Also, include numbers and data about the quantities of these constituents in this plant.
        In the second paragraph, write about examples of health conditions that can benefit from the beneficial property described in the first paragraph.
        In the third paragraph, write about which parts of this plant can be used to get the benefit described in the first paragraph and which preparations can be made for that.

        Include as many details, data, and numbers as possible in as few words as possible.
        Use the metric system as the primary measuring system.

        The first paragraph must start with the following words:

        {common_name} ___ thanks to

        --------------------------------------------------------------------

        Write 3 paragraphs about {common_name} ({latin_name}) about the following health benefit: ___.

        In the first paragraph, write about this plant's ability to get this health benefit, and what constituents this plant has to get this health benefit. Also, include numbers and data about the quantities of these constituents in this plant.
        In the second paragraph, write about examples of health conditions that can benefit from this health benefit. Don't talk about health conditions unrelated to this health benefit.
        In the third paragraph, write about which parts of this plant can be used to get this health benefit and which preparations can be made.

        Include as many details, data, and numbers as possible in as few words as possible.
        Use the metric system as the primary measuring system.

        The first paragraph must start with the following words:

        {common_name} ___ thanks to

        --------------------------------------------------------------------

        {images_text}


        ''')

        # give me 3 lists.

        # in the first list, give me 3 items about the constituents of yarrow to relieve inflammation.
        # in the second list, give me 3 items about the health conditions related to inflammation that yarrow helps to relieve.
        # in the third list, give me 3 items about the preparations of yarrow to help relieve inflammation.

        # give me just the names, don't add descriptions.

        # write this lists as a list of lists in python code.

        # These lists must not contradict the info contained in the following text:






def cuisine():

    print(f'''CULINARY USES

        Write me a list of the 10 culinary uses of {common_name} ({latin_name}). 

        --------------------------------------------------------------------

        Write a paragraph about the culinary uses of {common_name} ({latin_name}).
        Include the elements in the list above.
        Pack as much data as possible in as few words as possible.

        --------------------------------------------------------------------

        Using the data from the list above, write about 300 words on the culinary uses of {common_name} ({latin_name}).
        Pack as much data, info, and numbers as possible.
        Use the metric system when expressing numbers.
        Don't add subjective fluff or opinions, just objective facts. 

        --------------------------------------------------------------------
        
        Ok, now include some numbers to back up your claims.

        --------------------------------------------------------------------

        Ok, now use the data from the list above to write a section for an article about the culinary uses of {common_name} ({latin_name}) in about 300 words.
        This section must not use a list format. 

        --------------------------------------------------------------------





        ''')


def horticultural():

    print(f'''CULTIVATION TIPS

        Write me a list of the 10 tips to cultivate {common_name} ({latin_name}). 
        Give me just the tips, don't add descriptions.

        --------------------------------------------------------------------

        Ok, now rewrite each tip in less than 5 words. Keep as much data and numbers as possible.
        
        --------------------------------------------------------------------

        Ok, now add a description for each tip.

        --------------------------------------------------------------------





        ''')
        

def botany():

    print(f'''TAXONOMY 





        ''')


def history():

    print(f'''HISTORY 

        Write me a list of historical uses of {common_name} ({latin_name}). 
        Give me just the tips, don't add descriptions.

        --------------------------------------------------------------------

        Ok, now rewrite each item in the list above in less than 5 words.
        Keep as much data and numbers as possible.
        
        --------------------------------------------------------------------

        Ok, now add a description for each item in the list.

        --------------------------------------------------------------------





        ''')



if attribute_2 == 'morphology': morphology()
elif attribute_2 == 'taxonomy': taxonomy()
elif attribute_2 == 'distribution': distribution()
elif attribute_1 == 'botany': botany()
elif attribute_1 == 'medicine': medicine()
elif attribute_1 == 'medicine_benefits': medicine_benefits()
elif attribute_1 == 'cuisine': cuisine()
elif attribute_1 == 'horticultural': horticultural()
elif attribute_1 == 'botany': botany()
elif attribute_1 == 'history': history()
elif attribute_1 == '': main()


