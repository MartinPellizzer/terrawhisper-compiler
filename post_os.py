import os
import json
import random

from oliark_io import json_read
from oliark_llm import llm_reply

from lib import io

llm_reply('').strip()

campaign = 'terrawhisper'
campaign_folderpath = f'market/post-os/{campaign}'
my_method_name = f'medicinal herbal tinctures'
try: os.mkdir(f'market/post-os')
except: pass
try: os.mkdir(campaign_folderpath)
except: pass

def business_profile():
    output_filepath = f'{campaign_folderpath}/business_profile.txt'
    content = f'I am an herbalist selling info products to help DIY herbalists and apothecaries produce potent herbal remedies'
    with open(f'{campaign_folderpath}/business-profile.txt', 'w') as f: f.write(content)
    
def customer_profile():
    with open(f'{campaign_folderpath}/business-profile.txt') as f: business_profile = f.read().strip()
    output_filepath = f'{campaign_folderpath}/customer-profile.txt'
    prompt = f'''
        {business_profile}

        Provide a list of actionable insights for each customer component:

        Goals: what they aim to achieve.
        Pains: what frustrates or stops them.
        Objections: beliefs or doubts that create resistance.
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    with open(output_filepath, 'w') as f: f.write(reply)

def content_table():
    with open(f'{campaign_folderpath}/business-profile.txt') as f: business_profile = f.read().strip()
    with open(f'{campaign_folderpath}/customer-profile.txt') as f: customer_profile = f.read().strip()
    output_filepath = f'{campaign_folderpath}/content-table.txt'
    prompt = f'''
        MY BUSINESS PROFILE:
        {business_profile}
        MY CUSTOMER PROFILE:
        {customer_profile}
        Based on my business profile and customer profile, generate a list with the following data points:
        Struggles - key challenges my audience face.
        Aspirations - what they want to achieve.
        Objections - concerns or doubts they have.
        Tools/Tips - specific methods, tools, or insights to help them reach their goal.
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    with open(output_filepath, 'w') as f: f.write(reply)

# business_profile()
customer_profile()
content_table()
