from oliark_llm import llm_reply

def ebook():
    prompt = f'''
        My market is: health.
        My niche is: herbalism.
        My target audience is: women interested in holistic health.
        My product is: ebook.
        Give me a list of ideas on the type of content my product has to have to help my target audience get what they want.
    '''
    reply = llm_reply(prompt).strip()

def objections():
    prompt = f'''
        My market is: health.
        My niche is: herbalism.
        My target audience is: women interested in holistic health.
        My product: ebook to learn how to make medicinal herbal tinctures called "apothecary accelerator".
        Give me a list of objections my target audience have related to my niche that I can solve with my product.
    '''
    reply = llm_reply(prompt).strip()

_objections = [
    "i don't have time to learn about herbalism and tincture-making",
    "i'm not sure which herbs to use and how to use them",
    "i'm worried about making mistakes or using the wrong herbs",
    "i don't have access to a garden or a reliable herb supplier",
    "i'm concerned about the cost and investment required for herbalism",
    "i con't have the necessary equipment or knowledge to create tinctures safely",
    "i'm notsure i'm doing everything correctly, and i'm worried about the quality of my tinctures",
    "i want to use herbal remedies for myself and my family, but i'm not sure where to start",
    "i'm worried about the potential interactions with medications or health conditions",
    "i want to learn more about the spiritual and emotional aspects of herbalism, but i'm not sure where to start",
]

_lead_magnets = [
    "herbal tincture label template: a downloadable pdf that provides a template for creating custom labels for herbal tinctures, including space for ingredint list, instructions, and other important information",
    "the ultimate guide to drying herbs at home (cheatsheet): a step-by-step guide on how to dry herbs at home, including tips and trick for optimal drying and preservation."
]

def lead_magnets():
    prompt = f'''
        My market is: health.
        My niche is: herbalism.
        My target audience is: women interested in holistic health.
        My flagship product: ebook to learn how to make medicinal herbal tinctures called "apothecary accelerator".
        Give me a list of lead magnets that my target audience in my niche would want.
        Each lead magnet must be extremely fast to consume, easy to implement, and give a practical result (quick win).
        Each lead magnet must be a cheatsheet.
        Each lead magnet must be about a practical aspect of the herbal medicine making process.
    '''
    reply = llm_reply(prompt).strip()

# objections()
lead_magnets()
