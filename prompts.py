
def herb__intro(herb_name_scientific, herb_name_common):
    return f'''
        Write 1 intro paragraph in 4 sentences for an article about the {herb_name_scientific} herb.
        Follow the STRUCTURE and the GUIDELINES below.
        ## STRUCTURE
        In sentence 1, explain the health properties of this herb and how they improve health.
        In sentence 2, explain the main hortocultural aspects of this herb.
        In sentence 3, explain the botanical properties of this herb.
        In sentence 4, explain the main historical references of this herb.
        ## GUIDELINES
        Include only the paragraph in the reply, no additional info.
        Start the reply with the following words: {herb_name_scientific}, commonly know as {herb_name_common}, is .
    '''

def herb__medicine(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 5 paragraph of the medicinal aspects of {herb_name_scientific} ({herb_name_common}).
        Follow the GUIDELINES below.
        ## GUIDELINES
        - in paragraph 1, write about the medicinal uses and benefits of this plant.
        - in paragraph 2, write about the active constituents of this plant that gives its medicinal properties.
        - in paragraph 3, write about the parts of the plants that are most used for medicinal purposes.
        - in paragraph 4, write about the possible side effects of this plant when used improperly.
        - in paragraph 5, write about the most common precautions to take when using this plant medicinally.
        - all paragraphs must contains only facts and not opinions or speculations.
        - each paragraph should be about 40 words long.
        - pack as much info as possible in as few words as possible.
        - start the reply with the following words: {herb_name_scientific}{aka} helps with .
    '''

def herb__horticulture(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 4 paragraph of the horticulture aspects of {herb_name_scientific} ({herb_name_common}).
        Follow the GUIDELINES below.
        ## GUIDELINES
        - in paragraph 1, write about the growth requirements this plant.
        - in paragraph 2, write about the planting tips of this plant.
        - in paragraph 3, write about the harvesting tips of this plant.
        - in paragraph 4, write about the pests and diseases that most commonly affect of this plant.
        - all paragraphs must contains only facts and not opinions or speculations.
        - each paragraph should be about 40 words long.
        - pack as much info as possible in as few words as possible.
        - don't repeate the same piece of information or facts multiple times.
        - start the reply with the following words: {herb_name_scientific}{aka} grow .
    '''

herb_medicine__intro = f'''
    Write 1 paragraph of 60 to 80 words about the medicinal aspects of [herb_name_scientific] ([herb_name_common]).
    Follow the GUIDELINES below.
    ## GUIDELINES
    In sentence 1, write about the benefits of this herb.
    In sentence 2, write about the medicinal constituents of this herb.
    In sentence 3, write about the medicinal preparations of this herb.
    In sentence 4, write about the possible side effects of this herb.
    In sentence 5, write about the precautions to take when using this herb.
    Start the reply with the following words: [herb_name_scientific][aka] has health benefits such as .
'''


def herb_medicine_benefits__intro(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 1 paragraph of 60-80 words about the medicinal benefits of {herb_name_scientific} ({herb_name_common}).
        Follow the GUIDELINES below.
        ## GUIDELINES
        Include the benefits of this plant.
        Include what are the medicinal properties this plant has that give these benefits.
        Include examples on how this benefits can improve people lives.
        Start the reply with the following words: {herb_name_scientific}{aka} has health benefits such as .
    '''
