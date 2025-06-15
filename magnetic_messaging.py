import json

from oliark_llm import llm_reply

'''

result -> vehicle -> product -> framework piece -> problem/solution -> headline/subheadline -> content -> salespage -> $$$

result: alleviate everyday stress and axiety
vehicle: healing herbs
product: ebook on how to make tinctures
framework: tinctures, herbs, solvents, storage, dosage
problem: tinctures are expensive
headline: here's why everyone says that herbal remedies are too expensive (and why they actually should cost almost $0).
content:
    - you got to the pharacy
    - all you see are huge numbers (you pay for the brand)
    - instead DIY
    - a jar of tincture for less than $1 that lasts for more than 30 days
    - this is how i usually recommend to start (fast, sloppy, inexpensive)
    - give it a try
    - cta
salespage: buy the offer
$$$
'''


# My product is an ebook and its title is: "The fastest way to make potent medicinal herbal tinctues".

def json_ai(prompt):
    prompt += f'''
        Also, for each list item, explain why.
        Reply in the following JSON format: 
        [
            {{"item": "insert list item 1 here", "why": "insert why for list item 1 here"}}, 
            {{"item": "insert list item 2 here", "why": "insert why for list item 2 here"}}, 
            {{"item": "insert list item 3 here", "why": "insert why for list item 3 here"}} 
        ]
        Only reply with the JSON, don't add additional info.
        Always end the JSON with the character "]".
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    if reply[-1] != ']': reply += ']'
    json_data = {}
    try: json_data = json.loads(reply)
    except: pass 
    if json_data != {}:
        lst = []
        for item in json_data:
            try: _item = item['item']
            except: continue
            try: _why = item['why']
            except: continue
            lst.append({
                'item': _item,
                'why': _why,
            })

    for e in lst:
        print(e['item'])


product = [
    'Apothecary Accelerator: The fastest way to make potent medicinal herbal tictures to alleviate everyday stress and anxiety.',
    'Ozone generators',
]

vehicles = [
    'herbal tinctures',
    'ozone',
]

audiences = [
    'diy herbalists',
    'industrial facilities',
]

objections = [
    'herbal remedies are expensive',
]

promises = [
    'how to alleviate 60-70% of everyday stress and anxiety within 4-6 weeks with DIY herbal tinctures',
]



objections_prompt = f'''
    I sell {product[1]} to {audiences[1]}.
    Give me several list items about the objections my audience has.
'''

audiences_prompt = f'''
    I sell ozone generators.
    Give me several list items about the audiences that are most interested in buying this product.
'''

promises_prompt = f'''
    I teach people how to make medicinal herbal tinctures.
    Give me several list items about tangible results I can promise they will get.
    Make the promises measurable and include a time frame (numbers).
'''


# json_ai(objections_prompt)
# json_ai(audiences_prompt)
json_ai(promises_prompt)


