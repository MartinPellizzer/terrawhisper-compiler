#######################################################################################
# ENTITY
#######################################################################################

entity_intro = [
    '''
        Write a 5-sentence paragraph about of [latin_name].
        Include the medicinal properties of [latin_name], the horticultural conditions of [latin_name], and the botanical characteristics of [latin_name].
        Don't include lists.
        Don't add empty lines between sentences.
    ''',
    '''
        Write 1 paragraph in 5 sentences about of [latin_name].
        Include the medicinal properties of [latin_name], the horticultural conditions of [latin_name], and the botanical characteristics of [latin_name].
        Don't include lists.
        Don't add empty lines between sentences.
    ''',
] 



# entity_medicine = [
#     '''
#         Write 5 paragraphs about the medicinal aspects of [latin_name].
#         In paragraph 1, write about the benefits of [latin_name].
#         In paragraph 2, write about the constituents of [latin_name].
#         In paragraph 3, write about the preparations of [latin_name].
#         In paragraph 4, write about the side effects of [latin_name].
#         In paragraph 5, write about the precautions of [latin_name].
#     ''',
# ]

entity_medicine = [
    '''
        Write a 5-sentence paragraph about the medicinal uses of [latin_name].
        In sentence 1, write about the benefits of [latin_name].
        In sentence 2, write about the constituents of [latin_name].
        In sentence 3, write about the preparations of [latin_name].
        In sentence 4, write about the side effects of [latin_name].
        In sentence 5, write about the precautions of [latin_name].
        Start with the following words: [latin_name][aka] has several medicinal uses, such as .
    ''',
    '''
        Write 1 paragraph in 5 sentences about the medicinal uses of [latin_name].
        In sentence 1, write about the benefits of [latin_name].
        In sentence 2, write about the constituents of [latin_name].
        In sentence 3, write about the preparations of [latin_name].
        In sentence 4, write about the side effects of [latin_name].
        In sentence 5, write about the precautions of [latin_name].
        Start with the following words: [latin_name][aka] has several medicinal uses, such as .
    ''',
]

entity_medicine_paragraphs = [
    '''
        Write 5 paragraphs in 400 words about the medicinal uses of [latin_name].
        In paragraph 1, write about the health benefits of [latin_name].
        In paragraph 2, write about the medicinal constituents of [latin_name].
        In paragraph 3, write about the medicinal preparations of [latin_name].
        In paragraph 4, write about the possible side effects of [latin_name].
        In paragraph 5, write about the precautions of [latin_name].
        Start with the following words: [latin_name][aka] has several medicinal uses, such as .
    ''',
]

entity_benefits = [
    '''
        Write a detailed 5-sentence paragraph about the health benefits of [latin_name].
        Don't use lists. Don't mention the active constituents of [latin_name].
        Start with the following words: [latin_name], [aka] has many health benefits, such as .
    ''',
]

entity_constituents = [
    '''
        Write a detailed 5-sentence paragraph about the primary medicinal consituents of [latin_name].
        Don't use lists.
        Start with the following words: [latin_name][aka] has many active constituents, such as .
    ''',
]

entity_preparations = [
    '''
        Write a detailed 5-sentence paragraph about the primary medicinal preparations of [latin_name].
        Include the uses of these medicinal preparations and what parts of the plant are used to make these preparations.
        Don't include health benefits.
        Don't include constituents.
        Don't include side effects.
        Don't include precautions.
        Don't use lists.
        Start with the following words: [latin_name][aka] has many medicinal preparations, such as .
    ''',
]

entity_side_effects = [
    '''
        Write a detailed 5-sentence paragraph about the possible side effects of [latin_name] when used medicinally.
        Don't include health benefits.
        Don't include constituents.
        Don't include precautions.
        Don't use lists.
        Start with the following words: [latin_name][aka] can have some side effects if used improperly, such as .
    ''',
]

entity_precautions = [
    '''
        Write a detailed 5-sentence paragraph about the precautions and best practices when using [latin_name] for medicinal purposes.
        Don't include side effects.
        Don't use lists.
        Start with the following words: You should take some precautions when using [latin_name][aka] for medicinal purposes, such as .
    ''',
    '''
        Write 1 paragraph in 5 sentences about the precautions and best practices when using [latin_name] for medicinal purposes.
        Don't include side effects.
        Don't use lists.
        Start with the following words: You should take some precautions when using [latin_name][aka] for medicinal purposes, such as .
    ''',
]



entity_horticulture = [
    '''
        Write 5 paragraphs in 400 words about the horticultural aspects of [latin_name].
        In paragraph 1, write about the growth requirements of [latin_name].
        In paragraph 2, write about the planting tips of [latin_name].
        In paragraph 3, write about the caring tips of [latin_name].
        In paragraph 4, write about the harvesting tips of [latin_name].
        In paragraph 5, write about the pests and diseases of [latin_name].
    ''',
    '''
        Write 5 paragraphs about the horticultural aspects of [latin_name].
        In paragraph 1, write about the growth requirements of [latin_name].
        In paragraph 2, write about the planting tips of [latin_name].
        In paragraph 3, write about the caring tips of [latin_name].
        In paragraph 4, write about the harvesting tips of [latin_name].
        In paragraph 5, write about the pests of [latin_name].
    ''',
    '''
        Write 5 paragraphs in 400 words about the horticultural aspects of [latin_name].
        In paragraph 1, write about the growth requirements of [latin_name].
        In paragraph 2, write about the planting tips of [latin_name].
        In paragraph 3, write about the caring tips of [latin_name].
        In paragraph 4, write about the harvesting tips of [latin_name].
        In paragraph 5, write about the pests and diseases of [latin_name].
        Don't add conclusions.
    ''',
    '''
        Write 5 paragraphs in 400 words about the horticultural aspects of [latin_name].
        In paragraph 1, write about the growth requirements of [latin_name].
        In paragraph 2, write about the planting tips of [latin_name].
        In paragraph 3, write about the caring tips of [latin_name].
        In paragraph 4, write about the harvesting tips of [latin_name].
        In paragraph 5, write about the pests and diseases of [latin_name].
        Don't add conclusions. Don't add introductions.
    ''',
]

entity_botany = [
    '''
        Write 5 paragraphs in 400 words about the botanical aspects of [latin_name].
        In paragraph 1, write about the taxonomy of [latin_name].
        In paragraph 2, write about the morphology of [latin_name].
        In paragraph 3, write about the variants names and differences of [latin_name].
        In paragraph 4, write about the geographic distribution and natural habitats of [latin_name].
        In paragraph 5, write about the life-cycle of [latin_name].
    ''',
    '''
        Write 5 paragraphs in 400 words about the botanical aspects of [latin_name].
        In paragraph 1, write about the taxonomy of [latin_name].
        In paragraph 2, write about the morphology of [latin_name].
        In paragraph 3, write about the variants names and differences of [latin_name].
        In paragraph 4, write about the geographic distribution and natural habitats of [latin_name].
        In paragraph 5, write about the life-cycle of [latin_name].
        Don't add conclusions.
    ''',
    '''
        Write 5 paragraphs in 400 words about the botanical aspects of [latin_name].
        In paragraph 1, write about the taxonomy of [latin_name].
        In paragraph 2, write about the morphology of [latin_name].
        In paragraph 3, write about the variants names and differences of [latin_name].
        In paragraph 4, write about the geographic distribution and natural habitats of [latin_name].
        In paragraph 5, write about the life-cycle of [latin_name].
        Don't add conclusions. Don't add introductions.
    ''',
]


entity_history = [
    '''
        Write 5 paragraphs in 400 words about the historical aspects of [latin_name].
        In paragraph 1, write about the historical medicinal uses of [latin_name].
        In paragraph 2, write about the mythology of [latin_name].
        In paragraph 4, write about the ancient rituals of [latin_name].
        In paragraph 5, write about the literature of [latin_name].
        In paragraph 3, write about the symbolism of [latin_name].
    ''',
    '''
        Write 5 paragraphs in 400 words about the historical aspects of [latin_name].
        In paragraph 1, write about the historical medicinal uses of [latin_name].
        In paragraph 2, write about the mythology of [latin_name].
        In paragraph 4, write about the ancient rituals of [latin_name].
        In paragraph 5, write about the literature of [latin_name].
        In paragraph 3, write about the symbolism of [latin_name].
        Don't add conclusions.
    ''',
    '''
        Write 5 paragraphs in 400 words about the historical aspects of [latin_name].
        In paragraph 1, write about the historical medicinal uses of [latin_name].
        In paragraph 2, write about the mythology of [latin_name].
        In paragraph 4, write about the ancient rituals of [latin_name].
        In paragraph 5, write about the literature of [latin_name].
        In paragraph 3, write about the symbolism of [latin_name].
        Don't add conclusions. Don't add introductions.
    ''',
]



entity_taxonomy = [
    '''
        Give me a ordered list with the Linnaean Taxonomy of [latin_name]. Include:
        1. Kingdom
        2. Phylum
        3. Class
        4. Order
        5. Family
        6. Genus
        7. Species
    ''',
    '''
        Give me the Linnaean Taxonomy of [latin_name] in ordered list. Include:
        1. Kingdom
        2. Phylum
        3. Class
        4. Order
        5. Family
        6. Genus
        7. Species
    ''',
]

#######################################################################################
# ENTITY >> MEDICINE
#######################################################################################

entity_medicine_intro = [
    '''
        Write a 5-sentence paragraph about the medicinal aspects of [latin_name].
        In sentence 1, write the benefits of [latin_name].
        In sentence 2, write the constituents of [latin_name].
        In sentence 3, write the preparations of [latin_name].
        In sentence 4, write the side effects of [latin_name].
        In sentence 5, write the precautions of [latin_name].
    ''',
]