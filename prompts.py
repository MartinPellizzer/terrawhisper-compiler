import sys
import csv

if len(sys.argv) < 2:
    print("ERR: missing arguments (ENTITY, ATTRIBUTES)")
    quit()

entity = sys.argv[1]
latin_name = entity.replace('-', ' ').capitalize()
attribute_1 = ''
try: sys.argv[2].lower().strip()
except: pass
attribute_2 = ''
try: sys.argv[3].lower().strip()
except: pass

def csv_get_table_data(filepath, entity):
    lines = []
    with open(filepath) as f:
        reader = csv.reader(f, delimiter="\\")
        for i, line in enumerate(reader):
            if i == 0:
                lines.append(line)
            else:
                if line[0].strip() == entity.strip():
                    lines.append(line)
    return lines


def csv_get_rows_by_entity(filepath, entity):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter="|")
        for i, line in enumerate(reader):
            rows.append(line)
    
    filtered_rows = [] 
    for row in rows:
        if row[0].strip() == entity[0].strip():
            filtered_rows.append(row)
    return rows


try:
    common_names = csv_get_rows_by_entity('database/tables/botany/common-names.csv', 'achillea-millefolium')
    common_name = common_names[0][1]
except:
    common_names = []
    common_name = ''



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
    rows = csv_get_table_data(filepath, entity)
    rows = [f'-{row}' for row in rows[1][1:]]
    rows = '\n'.join(rows)
    print(f'''BOTANICAL PROFILE

        Write a paragraph about the taxonomy of {latin_name}. 
        Include as many details as possible in as few words as possible.
        Include all the data from the following list for the taxonomy:

        {rows}

        Also, start the paragraph with the following words:

        {common_name} ({latin_name})

        --------------------------------------------------------------------


        
        ''')


# give me 2 lists:

# in the first list write the native regions where yarrow is found.
# in the second list write the naturalized regions where yarrow is found.






if attribute_2 == 'morphology': morphology()
elif attribute_2 == 'taxonomy': taxonomy()
elif attribute_2 == 'distribution': distribution()
elif attribute_1 == 'botany': botany()
elif attribute_1 == '': main()


