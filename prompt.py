import sys

if len(sys.argv) != 3:
    print("ERR: missing arguments (ENTITY, ATTRIBUTE)")
    quit()

entity = sys.argv[1].replace('-', ' ').capitalize()
attribute = sys.argv[2].lower().strip()
# print(entity)

print()
print()
print()
print()
print()

def morphology():
    i = 1
    print(f'''
    {i}. ALL PARTS

    Give me a complete list of all the parts of {entity} in terms of morphology. 
    Don't add descriptions.
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')
    i += 1

    print(f'''
    {i}. ROOTS

    Give me a complete list of all the parts of STEMS of the {entity}. 
    Don't add descriptions.
    ''')
    print(f'''
    {i}. STEMS

    Give me a complete list of all the parts of STEMS of the {entity}. 
    Don't add descriptions.
    ''')
    print(f'''
    {i}. RHIZOME

    Give me a complete list of all the parts of RHIZOME of the {entity}. 
    Don't add descriptions.
    ''')
    print(f'''
    {i}. LEAVES

    Give me a complete list of all the parts of LEAVES of the {entity}. 
    Don't add descriptions.
    ''')
    print(f'''
    {i}. FLOWERS

    Give me a complete list of all the parts of FLOWERS of the {entity}. 
    Don't add descriptions.
    ''')
    print(f'''
    {i}. FRUITS

    Give me a complete list of all the parts of FRUITS of the {entity}. 
    Don't add descriptions.
    ''')
    print(f'''
    {i}. SEEDS

    Give me a complete list of all the parts of SEEDS of the {entity}. 
    Don't add descriptions.
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')
    i += 1



    print(f'''
    {i}. ROOTS CHARACTERISTICS

    Here's a list of morphological characteristics of roots of {entity}:

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

    For each characteristic in the above list write a precise description, by adding the exact information, numbers, and data. 
    Use as few words as possible for each description. 
    use primarily the metric system and put the imperial system in between parenthesis with data and numbers.

    Put all the data in table format. The table must have only 2 columns.
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')


    print(f'''
    {i}. STEMS CHARACTERISTICS

    Here's a list of morphological characteristics of stems of {entity}:

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

    For each characteristic in the above list write a precise description, by adding the exact information, numbers, and data. 
    Use as few words as possible for each description. 
    use primarily the metric system and put the imperial system in between parenthesis with data and numbers.

    Put all the data in table format. The table must have only 2 columns.
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')


    print(f'''
    {i}. RHIZOMES CHARACTERISTICS

    Here's a list of morphological characteristics of rhizomes of {entity}:

    - Rhizome Arrangement
    - Rhizome Shape
    - Rhizome Height
    - Rhizome Diameter
    - Rhizome Color
    - Rhizome Surface Texture
    - Rhizome Nodes
    - Rhizome Internodes

    For each characteristic in the above list write a precise description, by adding the exact information, numbers, and data. 
    Use as few words as possible for each description. 
    use primarily the metric system and put the imperial system in between parenthesis with data and numbers.

    Put all the data in table format. The table must have only 2 columns.
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')


    print(f'''
    {i}. LEAVES CHARACTERISTICS

    Here's a list of morphological characteristics of leaves of {entity}:

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

    For each characteristic in the above list write a precise description, by adding the exact information, numbers, and data. 
    Use as few words as possible for each description. 
    use primarily the metric system and put the imperial system in between parenthesis with data and numbers.

    Put all the data in table format. The table must have only 2 columns.
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')



    print(f'''
    {i}. FLOWERS CHARACTERISTICS

    Here's a list of morphological characteristics of flowers of {entity}:

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

    For each characteristic in the above list write a precise description, by adding the exact information, numbers, and data. 
    Use as few words as possible for each description. 
    use primarily the metric system and put the imperial system in between parenthesis with data and numbers.

    Put all the data in table format. The table must have only 2 columns.
    ''')

    print(f'''
    --------------------------------------------------------------------
    ''')



    print(f'''
    {i}. FRUITS CHARACTERISTICS

    Here's a list of morphological characteristics of fruits of {entity}:

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

    For each characteristic in the above list write a precise description, by adding the exact information, numbers, and data. 
    Use as few words as possible for each description. 
    use primarily the metric system and put the imperial system in between parenthesis with data and numbers.

    Put all the data in table format. The table must have only 2 columns.
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')




    print(f'''
    {i}. SEEDS CHARACTERISTICS

    Here's a list of morphological characteristics of seeds of {entity}:

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

    For each characteristic in the above list write a precise description, by adding the exact information, numbers, and data. 
    Use as few words as possible for each description. 
    use primarily the metric system and put the imperial system in between parenthesis with data and numbers.

    Put all the data in table format. The table must have only 2 columns.
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')
    i += 1


    print(f'''
    {i}. DATA TO TEXT

    Using the data from the previous table, write a section for an article in less than 300 words. 
    Don't write in list format. Write in discursive format. 
    Use simple language and a straightforward sentence structure.
    Don't add fluff or opinions, just write facts.
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')
    i += 1

def taxonomy():
    i = 1
    print(f'''
    {i}. TAXONOMY

    Give me the taxonomy of {entity}.

    Include:

    - Domain
    - Kingdom
    - Phylum
    - Class
    - Order
    - Family
    - Genus
    - Species

    Format the data in a 2 column table.
    In the first column of the table, write the elements in the list.
    In the second column of the table, write the answer. 
    ''')
    print(f'''
    --------------------------------------------------------------------
    ''')
    i += 1

if attribute == 'morphology': morphology()
elif attribute == 'taxonomy': taxonomy()


