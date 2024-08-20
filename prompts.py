def preparation__intro(preparation_name, status_name):
    return f'''
        Write 1 short paragraph in about 60 to 80 words on the herbal {preparation_name} for {status_name}.
        Define what "herbal {preparation_name} for {status_name}" is and why they help with {status_name}.
        Include examples of herbal {preparation_name} that help with {status_name} and examples of how this improves lives.
        Start the reply with the following words: Herbal {preparation_name} for {status_name} are .
    '''

def preparation__intro_study__select(n_results, preparation_name, status_name, abstracts):
    return f'''
        From the {n_results} paragraphs below, pick the one that best proves that herbal {preparation_name} are good for {status_name}, and that includes the most amount of data, information, details, results and numbers to prove it.
        Only select a study that explicitly mention {preparation_name} and {status_name}.
        Reply with only the number of the paragraph you select, don't explain why you selected it.
        If you don't find a good candidate, reply with "0".
        Below are the {n_results} paragraphs.
        {abstracts}
    '''

def preparation__intro_study__generate(preparation_name, status_name, document, journal_title):
    return f'''
        Explain in a 3-sentence short paragraph why herbal {preparation_name} are good for {status_name}.
        To explain that, use the information, data and numbers provided by the study below. 
        In the reply include an introduction, the methods used, and the results found in the study.
        If the study below doesn't have enough information to justify your argument, reply with only "I can't do that" and nothing else.
        If you have enough information to reply, start the reply with the following words: "For example, according to a study published by {journal_title}, ".
        Below is the study.
        {document}
    '''

def preparation__remedy_desc(preparation_name, status_name, herb_name_scientific, aka):
    return f'''
        Write a 60-80 words paragraph on why herbal {herb_name_scientific} {preparation_name} helps with {status_name}.
        Don't write about side effects and precautions.
        Start the reply with the following words: {herb_name_scientific}{aka} {preparation_name} helps with {status_name} because .
    '''

def preparation__remedy_properties(preparation_name, status_name, herb_name_scientific):
    return f'''
        Write a numbered list of the 2-3 most important medicinal properties of herbal {herb_name_scientific} {preparation_name} that help with {status_name} and explain in 1 breif sentence why.
    '''

def preparation__remedy_constituents(preparation_name, status_name, herb_name_scientific):
    return f'''
        Write a numbered list of the 2-3 most important medicinal constituents of herbal {herb_name_scientific} {preparation_name} that help with {status_name}.
        Examples of medicinal constituents are: terpenes, phenolics, alkaloids, etc.
        For each element in the list, describe in a short sentence why it help with {status_name}.
        Write each element in the list using the following format: [name]: [description].
    '''

def preparation__remedy_parts(preparation_name, status_name, herb_name_scientific):
    return f'''
        Write a numbered list of the 2-3 most used parts of {herb_name_scientific} that are used to make {preparation_name} for {status_name} and explain in 1 brief sentence why.
        Pick only parts from the following list:
        - Roots
        - Rhyzomes
        - Stems
        - Leaves
        - Flowers
        - Seeds
        - Buds
        - Barks
        - Fruits
        Write only 1 part per list item.
        Write each element in the list using the following format: [part name]: [description].
    '''     

def preparation__remedy_parts__old(preparation_name, status_name, herb_name_scientific):
    return f'''
        Write a numbered list of the most used parts of the {herb_name_scientific} plant that are used to make medicinal {preparation_name} for {status_name}.
        Reply by only selecting parts from the following list:
        - Roots
        - Rhyzomes
        - Stems
        - Leaves
        - Flowers
        - Seeds
        - Buds
        - Barks
        - Fruits
        Never include "aerial parts".
        Never repeat the same part twice and never include similar parts.
        Never include parts that are not used.
        Include 1 short sentence description for each of these part, explaining why that part is good for making medicinal {preparation_name} for {status_name}.
        Write each list element using the following format: [part name]: [part description].
    '''     

def preparation__remedy_recipe(preparation_name, herb_name_scientific):
    return f'''
        Write a 5-step recipe on how to make herbal {herb_name_scientific} {preparation_name}.
        Reply with a numbered list.
        Don't include the character ":".
        Write only 1 sentence for each step.
        Each sentence must be 10 to 20 words long.
        Start each step in the list with an action verb.
        Include ingredients dosages and preparations times for each step when applicable.
        Don't name other plants in the list items.
        Don't include optional steps.
    '''

def preparation__supplementary_best_treatment(status_name, preparation_name):
    return f'''
        Write a 60-80 words paragraph on the best combination of herbal {preparation_name} to heal {status_name}.
        Start the reply with the following words: The best combination of herbal {preparation_name} that help with {status_name} is .
    '''

###################################################################################################
# ;status
###################################################################################################

def status__intro(status_name):
    return f'''
        Write 1 short paragraph of about 60 to 80 words on the best herbs for {status_name}.
        Include a brief definition of: {status_name}.
        Also, explain negative health impacts, causes, medicinal herbs and precautions.
        Reply in paragraph format, not in list format.
    '''

def status__definition(status_name):
    return f'''
        Write 1 paragraph explaining what is {status_name}.
        Also include many examples on how it affects negatively your life.
        Don't mention the casuses of {status_name}.
    '''

def status__causes(status_name):
    return f'''
        Write 1 paragraph explaining what are the main causes of {status_name}.
        Start the reply with the following words: The main causes of {status_name} are .
    '''

def status__herbs(status_name, herbs_names_common_prompt):
    return f'''
        Write 1 paragraph of about 60 to 80 words on what medicinal herbs helps with {status_name} and why.
        Include some of the following herbs: {herbs_names_common_prompt}.
        Start the reply with the following words: The best medicinal herbs for {status_name} are .
    '''

def status__herbs_list(status_name, herbs_names_common_prompt):
    return f'''
        Write a numbered list explaining why the HERBS below are good for {status_name}.
        Follow the GUIDELINES below.
        ## GUIDELINES
        Reply with only the numbered list, no additional content or notes.
        Use the following structure for each item in the list: "herb_name: explanation".
        ## HERBS
        {herbs_names_common_prompt}
    '''

def status__preparations(status_name, preparations_names_prompt):
    return f'''
        Write 1 paragraph about what are the best types of herbal preparations for {status_name}.
        Include the following types of herbal preparations: {preparations_names_prompt}.
        Explain why each preparation helps with {status_name}.
        Don't include names of herbs.
        Don't include definitions for the preparations.
        Don't include how to make the preparations.
        Start the reply with the following words: The most effective herbal preparations for {status_name} are .
    '''

def status__preparations_list(status_name, preparations_names_prompt):
    return f'''
        Write a numbered list explaining why the HERBS below are good for {status_name}.
        Follow the GUIDELINES below.
        ## GUIDELINES
        Reply with only the numbered list, no additional content or notes.
        Use the following structure for each item in the list: "preparation_name: explanation".
        ## HERBS
        {preparations_names_prompt}
    '''

###################################################################################################
# ;herbs
###################################################################################################

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

def herb__botany(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 5 paragraph of the botanical aspects of {herb_name_scientific} ({herb_name_common}).
        Follow the GUIDELINES below.
        ## GUIDELINES
        - in paragraph 1, write about the botanical characteristics of this plant.
        - in paragraph 2, write about the taxonomical classification of this plant.
        - in paragraph 3, write about the variants of this plant.
        - in paragraph 4, write about the geographical distribution of this plant.
        - in paragraph 5, write about the life cycle of this plant.
        - all paragraphs must contains only facts and not opinions or speculations.
        - each paragraph should be about 40 words long.
        - pack as much info as possible in as few words as possible.
        - don't repeate the same piece of information or facts multiple times.
        - start the reply with the following words: {herb_name_scientific}{aka} is .
    '''

def herb__history(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 5 paragraph of the historical aspects of {herb_name_scientific} ({herb_name_common}).
        Follow the GUIDELINES below.
        ## GUIDELINES
        - in paragraph 1, write about the historical uses of this plant.
        - in paragraph 2, write about the mythological references of this plant.
        - in paragraph 3, write about the symbolic meanings of this plant.
        - in paragraph 4, write about the historical texts of this plant.
        - in paragraph 5, write about the historical artifacts of this plant.
        - all paragraphs must contains only facts and not opinions or speculations.
        - each paragraph should be about 40 words long.
        - pack as much info as possible in as few words as possible.
        - don't repeate the same piece of information or facts multiple times.
        - start the reply with the following words: {herb_name_scientific}{aka} is .
    '''

def herb_medicine__intro(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 1 paragraph of 60 to 80 words about the medicinal aspects of {herb_name_scientific} ({herb_name_common}).
        Follow the GUIDELINES below.
        ## GUIDELINES
        In sentence 1, write about the benefits of this herb.
        In sentence 2, write about the medicinal constituents of this herb.
        In sentence 3, write about the medicinal preparations of this herb.
        In sentence 4, write about the possible side effects of this herb.
        In sentence 5, write about the precautions to take when using this herb.
        Start the reply with the following words: {herb_name_scientific}{aka} has health benefits such as .
    '''

def herb_medicine__benefits(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 1 paragraph of 60-80 words on the health benefits of {herb_name_scientific} ({herb_name_common}).
        Start the reply with the following words: {herb_name_scientific}{aka} has health benefits such as .
    '''

def herb_medicine__constituents(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 1 paragraph of 60-80 words on the medicinal constituents of {herb_name_scientific} ({herb_name_common}).
        Start the reply with the following words: {herb_name_scientific}{aka} has active constituents such as .
    '''

def herb_medicine__preparations(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 1 paragraph of 60-80 words on the medicinal preparations of {herb_name_scientific} ({herb_name_common}).
        Start the reply with the following words: {herb_name_scientific}{aka} has medicinal preparations such as .
    '''

def herb_medicine__side_effects(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 1 paragraph of 60-80 words on the side effects of {herb_name_scientific} ({herb_name_common}) on health.
        Start the reply with the following words: Improper use of {herb_name_scientific}{aka} increases the chances of experiencing side effects such as .
    '''

def herb_medicine__precautions(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 1 paragraph of 60-80 words on the precautions to take when using {herb_name_scientific} ({herb_name_common}) medicinally.
        Start the reply with the following words: Before using {herb_name_scientific}{aka} for medicinal purposes, you must take precautions such as .
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

def herb_medicine_benefits__benefit_desc(herb_name_scientific, herb_name_common, benefit_name, aka):
    return f'''
        Write 1 paragraph of 60 to 80 words on why {herb_name_scientific} ({herb_name_common}) {benefit_name}.
        Start the reply with the following words: {herb_name_scientific}{aka} {benefit_name} because .
    '''

def herb_medicine_constituents__intro(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 1 paragraph of 60 to 80 words about the medicinal constituents of {herb_name_scientific} ({herb_name_common}).
        Follow the GUIDELINES below.
        GUIDELINES:
        Include the constituents of this plant.
        Include what are the medicinal properties this plant has that are given by these constituents.
        Include examples on how these constituents can improve people lives.
        Start the reply with the following words: {herb_name_scientific}{aka} has active constituents such as .
    '''

def herb_medicine_preparations__intro(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 1 paragraph of 60 to 80 words about the medicinal preparations of {herb_name_scientific}.
        Follow the GUIDELINES below.
        GUIDELINES
        Include the medicinal preparations of this plant (ex. teas, tinctures, etc...).
        Include what are the these medicinal preparations useful for.
        Start the reply with the following words: {herb_name_scientific}{aka} has several medicinal preparations, such as .
    '''

def herb_medicine_side_effects__intro(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 1 paragraph of 60 to 80 words about the possible side effects of {herb_name_scientific}.
        Follow the GUIDELINES below.
        GUIDELINES
        Include the side effects of this herb.
        Include what are the causes of these possible side effects.
        Include examples on how these side effects can worsen people lives.
        Start the reply with the following words: {herb_name_scientific}{aka} has some side effects when used improperly, such as .
    '''

def herb_medicine_precautions__intro(herb_name_scientific, herb_name_common, aka):
    return f'''
        Write 1 paragraph of 60 to 80 words about the most common precautions to take when using {herb_name_scientific} medicinally.
        Follow the GUIDELINES below.
        ## GUIDELINES
        Include the precautions to take for this herb.
        Include why it's important to take these precautions.
        Include examples on how not taking this precaution may give you side effects.
        Start the reply with the following words: {herb_name_scientific}{aka} has some precautions to consider before using it medicinally, such as .
    '''
