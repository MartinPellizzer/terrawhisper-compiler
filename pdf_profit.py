import os
import json
import random

from oliark_io import json_read
from oliark_llm import llm_reply

from lib import io

llm_reply('').strip()

def llm_gen(prompt, ouput_filepath=''):
    print(prompt)
    reply = llm_reply(prompt).strip()
    if output_filepath != '':
        with open(output_filepath, 'w') as f: f.write(reply)

campaign = 'terrawhisper'
campaign_folderpath = f'market/pdf-profit/{campaign}'
my_method_name = f'medicinal herbal tinctures'
who_selected_slug = ''
try: os.mkdir(campaign_folderpath)
except: pass
try: os.mkdir(f'{campaign_folderpath}/prompts')
except: pass
try: os.mkdir(f'{campaign_folderpath}/init')
except: pass

if 0:
    llm_gen(
        prompt = f'''
            Give me a list of the biggest markets that buy a lot of infoproducts (like ebooks).
        '''
    )

if 0:
    llm_gen(
        prompt = f'''
            Give me a list of the biggest sub markets of the market "health and wellness" that buy a lot of infoproducts (like ebooks). also tell me if "herbal remedies" are one of them.
        '''
    )

def who():
    global who_selected_slug
    with open(f'{campaign_folderpath}/init/market.txt') as f: market = f.read().strip()
    with open(f'{campaign_folderpath}/init/niche.txt') as f: niche = f.read().strip()
    json_output_filepath = f'{campaign_folderpath}/replies/who.json'
    prompt = f'''
        Give me a list of 20 who are most interested audiences in buying a lot of infoproducts (like ebooks, cheatsheets, planners, etc...) in the {niche} niche of the {market} market. 
        Focus on audiences that are considered "mass markets".
        Also, give a score 1-10 to each of them and explanin why. 
        The score is about maximizing profit for my infoproducts, where maximizing should consider both easiness of conversion and size of audience.
        Reply in the following JSON format: 
        [
            {{"who": "who is interested", "score": "10", "why": "why is interested"}}, 
            {{"who": "who is interested", "score": "5", "why": "why is interested"}}, 
            {{"who": "who is interested", "score": "7", "why": "why is interested"}} 
        ]
        Only reply with the JSON, don't add additional info.
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    json_data = {}
    try: json_data = json.loads(reply)
    except: pass 
    if json_data != {}:
        lst = []
        for item in json_data:
            try: who = item['who']
            except: continue
            try: score = item['score']
            except: continue
            try: why = item['why']
            except: continue
            lst.append({
                'who': who,
                'score': score,
                'why': why,
            })
    lst = sorted(lst, key=lambda x: x['score'], reverse=True)
    json_output = {}
    json_output['data'] = lst
    # io.json_write(json_output_filepath, json_output)
    for item_i, item in enumerate(json_output['data']):
        print('######################################')
        print(item_i)
        print('######################################')
        print(item['who'])
        print(item['score'])
        print(item['why'])
        print()
        print()
        print()
    choice = int(input('save number >> '))
    who = json_output['data'][choice]['who']
    who_slug = who.lower().split('(')[0].replace(' ', '-').replace(',', '').strip()
    try: os.mkdir(f'{campaign_folderpath}/{who_slug}')
    except: pass
    with open(f'{campaign_folderpath}/{who_slug}/who-selected.txt', 'w') as f: 
        f.write(who)
    who_selected_slug = who_slug

def who_manual():
    global who_selected_slug
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/who.txt') as f: who = f.read().strip()
    who_slug = who.lower().split('(')[0].replace(' ', '-').replace(',', '').strip()
    try: os.mkdir(f'{campaign_folderpath}/{who_slug}')
    except: pass
    with open(f'{campaign_folderpath}/{who_slug}/who-selected.txt', 'w') as f: 
        f.write(who)
    who_selected_slug = who_slug

def frustration():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    if 0:
        llm_gen(
            prompt = f'''
                Give me a list of frustrations of herbalism students and apprentices in the herbalism niche of the health market that can be solved with infoprodicts (like ebooks, cheatsheets, planners, etc...). Give a score 1-10 to each of them and explanin why. The score is about maximizing profit for my infoproducts, where maximizing should consider both easiness of conversion and size of audience.
            '''
        )
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read().strip()
    json_output_filepath = f'{input_folderpath}/frustrations.json'
    prompt = f'''
        Give me a list of frustrations of {who} in the {niche} niche of the {market} market.
        Also, give a score 1-10 to each of them and explanin why. 
        The score is about maximizing profit for my infoproducts, where maximizing should consider both easiness of conversion and size of audience.
        Reply in the following JSON format: 
        [
            {{"frustration": "write frustration 1 here", "score": "10", "why": "why is interested"}}, 
            {{"frustration": "write frustration 2 here", "score": "5", "why": "why is interested"}}, 
            {{"frustration": "write frustration 3 here", "score": "7", "why": "why is interested"}} 
        ]
        Only reply with the JSON, don't add additional info.
        Make sure you end the JSON with the character "]".
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    json_data = {}
    try: json_data = json.loads(reply)
    except: pass 
    if json_data != {}:
        lst = []
        for item in json_data:
            try: frustration = item['frustration']
            except: continue
            try: score = int(item['score'])
            except: continue
            try: why = item['why']
            except: continue
            lst.append({
                'frustration': frustration,
                'score': score,
                'why': why,
            })
    lst = sorted(lst, key=lambda x: x['score'], reverse=True)
    json_output = {}
    json_output['data'] = lst
    io.json_write(json_output_filepath, json_output)
    for item in json_output['data']:
        print(item)

def domino():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- '.join(x['frustration'] for x in json_frustration['data'])
    ###
    json_output_filepath = f'{input_folderpath}/domino.json'
    prompt = f'''
        The Big Domino Statement is the single core belief, the "big domino", I need to knock down that will knock down all teh other dominos and make it so people HAVE to buy my product.
        Create 5 different Big Domino statements for my business given my target audience and what I do. Here is my info:
        Market: {market}
        Niche: {niche}
        Who: {who}
        Frustration: {frustration}
        Use this format: "If I can get [who] to believe that my [NDFE idea] is teh key to [getting their desired result], and they can do it without [frustrations], then all other objections become irrelevant and they have to buy from me."
        Analyze each statement for effectiveness and rank them 1-10 in order of what you feel would work best with the reason why.
        Reply in the following JSON format: 
        [
            {{"domino": "write domino 1 in full here", "score": "10", "why": "reason why 1 here"}}, 
            {{"domino": "write domino 2 in full here", "score": "5", "why": "reason why 1 here"}}, 
            {{"domino": "write domino 3 in full here", "score": "7", "why": "reason why 1 here"}} 
        ]
        Only reply with the JSON, don't add additional info.
        Make sure you end the JSON with the character "]".
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    json_data = {}
    try: json_data = json.loads(reply)
    except: pass 
    if json_data != {}:
        lst = []
        for item in json_data:
            try: domino = item['domino']
            except: continue
            try: score = int(item['score'])
            except: continue
            try: why = item['why']
            except: continue
            lst.append({
                'domino': domino,
                'score': score,
                'why': why,
            })
    lst = sorted(lst, key=lambda x: x['score'], reverse=True)
    json_output = {}
    json_output['data'] = lst
    io.json_write(json_output_filepath, json_output)
    for item_i, item in enumerate(json_output['data']):
        print('######################################')
        print(item_i)
        print('######################################')
        print(item['domino'])
        print(item['score'])
        print(item['why'])
        print()
        print()
        print()
    # choice = int(input('save number >> '))
    choice = 0
    with open(f'{input_folderpath}/domino-selected.txt', 'w') as f: 
        f.write(json_output['data'][choice]['domino'])

def results():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- '.join(x['frustration'] for x in json_frustration['data'])
    with open(f'{input_folderpath}/domino-selected.txt') as f: domino = f.read()
    ###
    json_output_filepath = f'{input_folderpath}/results.json'
    prompt = f'''
        Market: {market}
        Niche: {niche}
        Who: {who}
        Frustrations: {frustration}
        Mission: {domino}
        What are the top 10 specific, measurable results my customers would experience when they do this? 
        Be detailed and focus on tangible outcomes, including specific numbers and timeframes where possible.
        Also, score each answer 1-10 and explain why.
        Reply in the following JSON format: 
        [
            {{"result": "write wanted result 1 here", "score": "10", "why": "reason why 1 here"}}, 
            {{"result": "write wanted result 2 here", "score": "5", "why": "reason why 1 here"}}, 
            {{"result": "write wanted result 3 here", "score": "7", "why": "reason why 1 here"}} 
        ]
        Only reply with the JSON, don't add additional info.
        Make sure you end the JSON with the character "]".
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    json_data = {}
    try: json_data = json.loads(reply)
    except: pass 
    if json_data != {}:
        lst = []
        for item in json_data:
            try: result = item['result']
            except: continue
            try: score = int(item['score'])
            except: continue
            try: why = item['why']
            except: continue
            lst.append({
                'result': result,
                'score': score,
                'why': why,
            })
    lst = sorted(lst, key=lambda x: x['score'], reverse=True)
    json_output = {}
    json_output['data'] = lst
    io.json_write(json_output_filepath, json_output)

def past_methods():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- ' + '\n- '.join(x['frustration'] for x in json_frustration['data'])
    with open(f'{input_folderpath}/domino-selected.txt') as f: domino = f.read()
    json_results = json_read(f'{input_folderpath}/results.json')
    results = '\n- ' + '\n- '.join(x['result'] for x in json_results['data'])
    ###
    json_output_filepath = f'{input_folderpath}/past-methods.json'
    prompt = f'''
        Market: {market}
        Niche: {niche}
        Who: {who}
        Frustrations: {frustration}
        Mission: {domino}
        Results: {results}
        List out 10 specific methods my target customer is currently using to try and achieve these results. 
        Break down each method with details about time investment, costs, and typical outcomes they're getting.
        Also, give a confidence score for each answer 1-10 and explain why.
        Reply in the following JSON format: 
        [
            {{"method": "write method 1 here", "time": "write time investment here", "cost": "write const here", "outcome": "write outcome here", "score": "10", "why": "reason why 1 here"}}, 
            {{"method": "write method 2 here", "time": "write time investment here", "cost": "write const here", "outcome": "write outcome here", "score": "5", "why": "reason why 1 here"}}, 
            {{"method": "write method 3 here", "time": "write time investment here", "cost": "write const here", "outcome": "write outcome here", "score": "7", "why": "reason why 1 here"}} 
        ]
        Only reply with the JSON, don't add additional info.
        Make sure you end the JSON with the character "]".
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    try: json_data = {}
    except: pass
    try: json_data = json.loads(reply)
    except: pass 
    if json_data != {}:
        lst = []
        for item in json_data:
            try: method = item['method']
            except: continue
            try: time = item['time']
            except: continue
            try: cost = item['cost']
            except: continue
            try: outcome = item['outcome']
            except: continue
            try: score = int(item['score'])
            except: continue
            try: why = item['why']
            except: continue
            lst.append({
                'method': method,
                'time': time,
                'cost': cost,
                'outcome': outcome,
                'score': score,
                'why': why,
            })
    lst = sorted(lst, key=lambda x: x['score'], reverse=True)
    json_output = {}
    json_output['data'] = lst
    io.json_write(json_output_filepath, json_output)

def frustrations_detailed():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- ' + '\n- '.join(x['frustration'] for x in json_frustration['data'])
    with open(f'{input_folderpath}/domino-selected.txt') as f: domino = f.read()
    json_results = json_read(f'{input_folderpath}/results.json')
    results = '\n- ' + '\n- '.join(x['result'] for x in json_results['data'])
    json_past_methods = json_read(f'{input_folderpath}/past-methods.json')
    past_methods = '\n- ' + '\n- '.join(x['method'] for x in json_past_methods['data'])
    ###
    json_output_filepath = f'{input_folderpath}/frustrations-detailed.json'
    prompt = f'''
        Market: {market}
        Niche: {niche}
        Who: {who}
        Frustrations: {frustration}
        Mission: {domino}
        Results: {results}
        Methods: {past_methods}
        List out 10 detailed frustrations my target market experiences with current solutions. 
        Include specific pain points around time, money, technical challenges, and emotional factors. 
        Be as specific as possible with examples.
        Also, give a confidence score for each answer 1-10 and explain why.
        Reply in the following JSON format: 
        [
            {{"method": "write method 1 here", "time": "write time investment here", "cost": "write cost here", "challenges": "write challenges here", "emotions": "write emotional factors here", "score": "10", "why": "reason why 1 here"}}, 
            {{"method": "write method 2 here", "time": "write time investment here", "cost": "write cost here", "challenges": "write challenges here", "emotions": "write emotional factors here", "score": "5", "why": "reason why 1 here"}}, 
            {{"method": "write method 3 here", "time": "write time investment here", "cost": "write cost here", "challenges": "write challenges here", "emotions": "write emotional factors here", "score": "7", "why": "reason why 1 here"}} 
        ]
        Only reply with the JSON, don't add additional info.
        Make sure you end the JSON with the character "]".
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    json_data = {}
    try: json_data = json.loads(reply)
    except: pass 
    if json_data != {}:
        lst = []
        for item in json_data:
            try: method = item['method']
            except: continue
            try: time = item['time']
            except: continue
            try: cost = item['cost']
            except: continue
            try: challenges = item['challenges']
            except: continue
            try: emotions = item['emotions']
            except: continue
            try: score = int(item['score'])
            except: continue
            try: why = item['why']
            except: continue
            lst.append({
                'method': method,
                'time': time,
                'cost': cost,
                'challenges': challenges,
                'emotions': emotions,
                'score': score,
                'why': why,
            })
    lst = sorted(lst, key=lambda x: x['score'], reverse=True)
    json_output = {}
    json_output['data'] = lst
    io.json_write(json_output_filepath, json_output)

def my_method_auto():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- ' + '\n- '.join(x['frustration'] for x in json_frustration['data'])
    with open(f'{input_folderpath}/domino-selected.txt') as f: domino = f.read()
    json_results = json_read(f'{input_folderpath}/results.json')
    results = '\n- ' + '\n- '.join(x['result'] for x in json_results['data'])
    json_past_methods = json_read(f'{input_folderpath}/past-methods.json')
    past_methods = '\n- ' + '\n- '.join(x['method'] for x in json_past_methods['data'])
    json_frustrations_detailed = json_read(f'{input_folderpath}/frustrations-detailed.json')
    frustrations_detailed = '' 
    for json_frustration_detailed in json_frustrations_detailed['data']:
        _method = json_frustration_detailed['method']
        _time = json_frustration_detailed['time']
        _cost = json_frustration_detailed['cost']
        _challenges = json_frustration_detailed['challenges']
        _emotions = json_frustration_detailed['emotions']
        _why = json_frustration_detailed['why']
        frustrations_detailed += f'- {_method}, {_time}, {_cost}, {_challenges}, {_emotions}, {_why}.\n'
    ###
    output_filepath = f'{input_folderpath}/my-method.txt'
    prompt = f'''
        Market: {market}
        Niche: {niche}
        Who: {who}
        Frustrations: {frustration}
        Mission: {domino}
        Results: {results}
        Other Methods Frustrations: {frustrations_detailed}
        Create a detailed breakdown of how my method works, including:
        - Step-by-step process
        - Key milestones
        - Required tools/resources
        - Typical timeframes
        - Focus on being specific and actionable 
        Design my method to address and solve the frustrations listed above.
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    with open(output_filepath, 'w') as f: 
        f.write(reply)

def my_method_manual(my_method):
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- ' + '\n- '.join(x['frustration'] for x in json_frustration['data'])
    with open(f'{input_folderpath}/domino-selected.txt') as f: domino = f.read()
    json_results = json_read(f'{input_folderpath}/results.json')
    results = '\n- ' + '\n- '.join(x['result'] for x in json_results['data'])
    json_past_methods = json_read(f'{input_folderpath}/past-methods.json')
    past_methods = '\n- ' + '\n- '.join(x['method'] for x in json_past_methods['data'])
    json_frustrations_detailed = json_read(f'{input_folderpath}/frustrations-detailed.json')
    frustrations_detailed = '' 
    for json_frustration_detailed in json_frustrations_detailed['data']:
        _method = json_frustration_detailed['method']
        _time = json_frustration_detailed['time']
        _cost = json_frustration_detailed['cost']
        _challenges = json_frustration_detailed['challenges']
        _emotions = json_frustration_detailed['emotions']
        _why = json_frustration_detailed['why']
        frustrations_detailed += f'- {_method}, {_time}, {_cost}, {_challenges}, {_emotions}, {_why}.\n'
    ###
    output_filepath = f'{input_folderpath}/my-method.txt'
    prompt = f'''
        Market: {market}
        Niche: {niche}
        Who: {who}
        Frustrations: {frustration}
        Mission: {domino}
        Results: {results}
        Other Methods Frustrations: {frustrations_detailed}
        My Method: {my_method}
        Create a detailed breakdown of how my method works, including:
        - Step-by-step process
        - Key milestones
        - Required tools/resources
        - Typical timeframes
        - Focus on being specific and actionable 
        Design my method to address and solve the frustrations listed above.
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    with open(output_filepath, 'w') as f: 
        f.write(reply)

def benefits():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- ' + '\n- '.join(x['frustration'] for x in json_frustration['data'])
    with open(f'{input_folderpath}/domino-selected.txt') as f: domino = f.read()
    json_results = json_read(f'{input_folderpath}/results.json')
    results = '\n- ' + '\n- '.join(x['result'] for x in json_results['data'])
    json_past_methods = json_read(f'{input_folderpath}/past-methods.json')
    past_methods = '\n- ' + '\n- '.join(x['method'] for x in json_past_methods['data'])
    json_frustrations_detailed = json_read(f'{input_folderpath}/frustrations-detailed.json')
    frustrations_detailed = '' 
    for json_frustration_detailed in json_frustrations_detailed['data']:
        _method = json_frustration_detailed['method']
        _time = json_frustration_detailed['time']
        _cost = json_frustration_detailed['cost']
        _challenges = json_frustration_detailed['challenges']
        _emotions = json_frustration_detailed['emotions']
        _why = json_frustration_detailed['why']
        frustrations_detailed += f'- {_method}, {_time}, {_cost}, {_challenges}, {_emotions}, {_why}.\n'
    with open(f'{input_folderpath}/my-method.txt') as f: my_method = f.read()
    ###
    output_filepath = f'{input_folderpath}/benefits.txt'
    prompt = f'''
        Market: {market}
        Niche: {niche}
        Who: {who}
        Frustrations: {frustration}
        Mission: {domino}
        Results: {results}
        Other Methods: {past_methods}
        My Method: {my_method}
        Analyze my method of helping [who][get result]. Explain specifically:
        - What makes it NEW compared to existing solutions
        - What makes it DIFFERENT from other options
        - What makes it FASTER than current approaches
        - What makes it EASIER than traditional methods
        - Be specific with comparisons and examples
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    with open(output_filepath, 'w') as f: 
        f.write(reply)

def external_benefits():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- ' + '\n- '.join(x['frustration'] for x in json_frustration['data'])
    with open(f'{input_folderpath}/domino-selected.txt') as f: domino = f.read()
    json_results = json_read(f'{input_folderpath}/results.json')
    results = '\n- ' + '\n- '.join(x['result'] for x in json_results['data'])
    json_past_methods = json_read(f'{input_folderpath}/past-methods.json')
    past_methods = '\n- ' + '\n- '.join(x['method'] for x in json_past_methods['data'])
    json_frustrations_detailed = json_read(f'{input_folderpath}/frustrations-detailed.json')
    frustrations_detailed = '' 
    for json_frustration_detailed in json_frustrations_detailed['data']:
        _method = json_frustration_detailed['method']
        _time = json_frustration_detailed['time']
        _cost = json_frustration_detailed['cost']
        _challenges = json_frustration_detailed['challenges']
        _emotions = json_frustration_detailed['emotions']
        _why = json_frustration_detailed['why']
        frustrations_detailed += f'- {_method}, {_time}, {_cost}, {_challenges}, {_emotions}, {_why}.\n'
    with open(f'{input_folderpath}/my-method.txt') as f: my_method = f.read()
    with open(f'{input_folderpath}/benefits.txt') as f: benefits = f.read()
    ### 
    output_filepath = f'{input_folderpath}/external-benefits.txt'
    prompt = f'''
        Market: {market}
        Niche: {niche}
        Who: {who}
        Frustrations: {frustration}
        Mission: {domino}
        Results: {results}
        Other Methods: {past_methods}
        My Method: {my_method}
        Benefits: {benefits}
        List 5 external benefits my target market will experience when they achieve the result.
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    with open(output_filepath, 'w') as f: 
        f.write(reply)

def internal_benefits():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- ' + '\n- '.join(x['frustration'] for x in json_frustration['data'])
    with open(f'{input_folderpath}/domino-selected.txt') as f: domino = f.read()
    json_results = json_read(f'{input_folderpath}/results.json')
    results = '\n- ' + '\n- '.join(x['result'] for x in json_results['data'])
    json_past_methods = json_read(f'{input_folderpath}/past-methods.json')
    past_methods = '\n- ' + '\n- '.join(x['method'] for x in json_past_methods['data'])
    json_frustrations_detailed = json_read(f'{input_folderpath}/frustrations-detailed.json')
    frustrations_detailed = '' 
    for json_frustration_detailed in json_frustrations_detailed['data']:
        _method = json_frustration_detailed['method']
        _time = json_frustration_detailed['time']
        _cost = json_frustration_detailed['cost']
        _challenges = json_frustration_detailed['challenges']
        _emotions = json_frustration_detailed['emotions']
        _why = json_frustration_detailed['why']
        frustrations_detailed += f'- {_method}, {_time}, {_cost}, {_challenges}, {_emotions}, {_why}.\n'
    with open(f'{input_folderpath}/my-method.txt') as f: my_method = f.read()
    with open(f'{input_folderpath}/benefits.txt') as f: benefits = f.read()
    ### 
    output_filepath = f'{input_folderpath}/internal-benefits.txt'
    prompt = f'''
        Market: {market}
        Niche: {niche}
        Who: {who}
        Frustrations: {frustration}
        Mission: {domino}
        Results: {results}
        Other Methods: {past_methods}
        My Method: {my_method}
        Benefits: {benefits}
        List 5 internal benefits my target market will experience when they achieve the result.
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    with open(output_filepath, 'w') as f: 
        f.write(reply)

def expertise():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- ' + '\n- '.join(x['frustration'] for x in json_frustration['data'])
    with open(f'{input_folderpath}/domino-selected.txt') as f: domino = f.read()
    json_results = json_read(f'{input_folderpath}/results.json')
    results = '\n- ' + '\n- '.join(x['result'] for x in json_results['data'])
    json_past_methods = json_read(f'{input_folderpath}/past-methods.json')
    past_methods = '\n- ' + '\n- '.join(x['method'] for x in json_past_methods['data'])
    json_frustrations_detailed = json_read(f'{input_folderpath}/frustrations-detailed.json')
    frustrations_detailed = '' 
    for json_frustration_detailed in json_frustrations_detailed['data']:
        _method = json_frustration_detailed['method']
        _time = json_frustration_detailed['time']
        _cost = json_frustration_detailed['cost']
        _challenges = json_frustration_detailed['challenges']
        _emotions = json_frustration_detailed['emotions']
        _why = json_frustration_detailed['why']
        frustrations_detailed += f'- {_method}, {_time}, {_cost}, {_challenges}, {_emotions}, {_why}.\n'
    with open(f'{input_folderpath}/my-method.txt') as f: my_method = f.read()
    with open(f'{input_folderpath}/benefits.txt') as f: benefits = f.read()
    with open(f'{input_folderpath}/internal-benefits.txt') as f: internal_benefits = f.read()
    with open(f'{input_folderpath}/external-benefits.txt') as f: external_benefits = f.read()
    ### 
    output_filepath = f'{input_folderpath}/expertise.txt'
    prompt = f'''
        market: {market}
        niche: {niche}
        who: {who}
        frustrations: {frustration}
        mission: {domino}
        results: {results}
        other methods: {past_methods}
        my method: {my_method}
        benefits: {benefits}
        external benefits: {external_benefits}
        internal benefits: {internal_benefits}
        i have been making herbal medicines since 2009 with this method. 
        i made 1000+ remedies and tested more than 100+ medicinal herbs on my own skin. 
        what makes me the best person to help potential customers with this method?
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    with open(output_filepath, 'w') as f: 
        f.write(reply)

def value_statement():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- ' + '\n- '.join(x['frustration'] for x in json_frustration['data'])
    with open(f'{input_folderpath}/domino-selected.txt') as f: domino = f.read()
    json_results = json_read(f'{input_folderpath}/results.json')
    results = '\n- ' + '\n- '.join(x['result'] for x in json_results['data'])
    json_past_methods = json_read(f'{input_folderpath}/past-methods.json')
    past_methods = '\n- ' + '\n- '.join(x['method'] for x in json_past_methods['data'])
    json_frustrations_detailed = json_read(f'{input_folderpath}/frustrations-detailed.json')
    frustrations_detailed = '' 
    for json_frustration_detailed in json_frustrations_detailed['data']:
        _method = json_frustration_detailed['method']
        _time = json_frustration_detailed['time']
        _cost = json_frustration_detailed['cost']
        _challenges = json_frustration_detailed['challenges']
        _emotions = json_frustration_detailed['emotions']
        _why = json_frustration_detailed['why']
        frustrations_detailed += f'- {_method}, {_time}, {_cost}, {_challenges}, {_emotions}, {_why}.\n'
    with open(f'{input_folderpath}/my-method.txt') as f: my_method = f.read()
    with open(f'{input_folderpath}/benefits.txt') as f: benefits = f.read()
    with open(f'{input_folderpath}/internal-benefits.txt') as f: internal_benefits = f.read()
    with open(f'{input_folderpath}/external-benefits.txt') as f: external_benefits = f.read()
    with open(f'{input_folderpath}/expertise.txt') as f: expertise = f.read()
    ### 
    output_filepath = f'{input_folderpath}/value-statement.txt'
    prompt = f'''
        market: {market}
        niche: {niche}
        who: {who}
        frustrations: {frustration}
        mission: {domino}
        results: {results}
        other methods: {past_methods}
        my method: {my_method}
        benefits: {benefits}
        external benefits: {external_benefits}
        internal benefits: {internal_benefits}
        expertise: {expertise}
        Can you help finalize my Value Statement given this info? 
        I want to create a PDF ebook that shows my target customer how to [get result][using my method] without [frustrations].
        Here is the value statement framework:
        Helping [who] get [dream result] without [things they hate] in [specific timeframe].
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    with open(output_filepath, 'w') as f: 
        f.write(reply)

def doc():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- ' + '\n- '.join(x['frustration'] for x in json_frustration['data'])
    with open(f'{input_folderpath}/domino-selected.txt') as f: domino = f.read()
    json_results = json_read(f'{input_folderpath}/results.json')
    results = '\n- ' + '\n- '.join(x['result'] for x in json_results['data'])
    json_past_methods = json_read(f'{input_folderpath}/past-methods.json')
    past_methods = '\n- ' + '\n- '.join(x['method'] for x in json_past_methods['data'])
    json_frustrations_detailed = json_read(f'{input_folderpath}/frustrations-detailed.json')
    frustrations_detailed = '' 
    for json_frustration_detailed in json_frustrations_detailed['data']:
        _method = json_frustration_detailed['method']
        _time = json_frustration_detailed['time']
        _cost = json_frustration_detailed['cost']
        _challenges = json_frustration_detailed['challenges']
        _emotions = json_frustration_detailed['emotions']
        _why = json_frustration_detailed['why']
        frustrations_detailed += f'- {_method}, {_time}, {_cost}, {_challenges}, {_emotions}, {_why}.\n'
    with open(f'{input_folderpath}/my-method.txt') as f: my_method = f.read()
    with open(f'{input_folderpath}/benefits.txt') as f: benefits = f.read()
    with open(f'{input_folderpath}/internal-benefits.txt') as f: internal_benefits = f.read()
    with open(f'{input_folderpath}/external-benefits.txt') as f: external_benefits = f.read()
    with open(f'{input_folderpath}/expertise.txt') as f: expertise = f.read()
    with open(f'{input_folderpath}/value-statement.txt') as f: value_statement = f.read()
    ### 
    output_filepath = f'{input_folderpath}/doc.txt'
    prompt = f'''
        market: {market}
        niche: {niche}
        who: {who}
        frustrations: {frustration}
        mission: {domino}
        results: {results}
        other methods: {past_methods}
        my method: {my_method}
        benefits: {benefits}
        external benefits: {external_benefits}
        internal benefits: {internal_benefits}
        expertise: {expertise}
        value statement: {value_statement}
        Please organize and compile all of the questions and answers from above so that I can copy and paste it into Google Docs. It should include the following:
        - The Big Domino Statement
        - 10 tangible results I help people get
        - 10 current solutions
        - 10 frustrations
        - My method
        - NDFE
        - 5 external benefits
        - 5 internal benefits
        - Why me (track record)
        - Value statement
        Be sure to add all of it without leaving any details out.
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    with open(output_filepath, 'w') as f: 
        f.write(reply)


def recap():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- ' + '\n- '.join(x['frustration'] for x in json_frustration['data'])
    with open(f'{input_folderpath}/domino-selected.txt') as f: domino = f.read()
    json_results = json_read(f'{input_folderpath}/results.json')
    results = '\n- ' + '\n- '.join(x['result'] for x in json_results['data'])
    json_past_methods = json_read(f'{input_folderpath}/past-methods.json')
    past_methods = '\n- ' + '\n- '.join(x['method'] for x in json_past_methods['data'])
    json_frustrations_detailed = json_read(f'{input_folderpath}/frustrations-detailed.json')
    frustrations_detailed = '' 
    for json_frustration_detailed in json_frustrations_detailed['data']:
        _method = json_frustration_detailed['method']
        _time = json_frustration_detailed['time']
        _cost = json_frustration_detailed['cost']
        _challenges = json_frustration_detailed['challenges']
        _emotions = json_frustration_detailed['emotions']
        _why = json_frustration_detailed['why']
        frustrations_detailed += f'- {_method}, {_time}, {_cost}, {_challenges}, {_emotions}, {_why}.\n'
    with open(f'{input_folderpath}/my-method.txt') as f: my_method = f.read()
    with open(f'{input_folderpath}/benefits.txt') as f: benefits = f.read()
    ### 
    output_filepath = f'{input_folderpath}/recap.txt'
    recap_text = f'''
        #################################################################
        Market: 
        #################################################################
        {market}
        #################################################################
        Niche: 
        #################################################################
        {niche}
        #################################################################
        Who: 
        #################################################################
        {who}
        #################################################################
        Frustrations: 
        #################################################################
        {frustration}
        #################################################################
        Mission: 
        #################################################################
        {domino}
        #################################################################
        Results: 
        #################################################################
        {results}
        #################################################################
        Other Methods: 
        #################################################################
        {past_methods}
        #################################################################
        Frustrations Detailed: 
        #################################################################
        {frustrations_detailed}
        #################################################################
        My Method: 
        #################################################################
        {my_method}
        #################################################################
        Benefits: 
        #################################################################
        {benefits}
    '''
    with open(output_filepath, 'w') as f: 
        f.write(recap_text)

def summary():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    json_frustration = json_read(f'{input_folderpath}/frustrations.json')
    frustration = '\n- ' + '\n- '.join(x['frustration'] for x in json_frustration['data'])
    with open(f'{input_folderpath}/domino-selected.txt') as f: domino = f.read()
    json_results = json_read(f'{input_folderpath}/results.json')
    results = '\n- ' + '\n- '.join(x['result'] for x in json_results['data'])
    json_past_methods = json_read(f'{input_folderpath}/past-methods.json')
    past_methods = '\n- ' + '\n- '.join(x['method'] for x in json_past_methods['data'])
    json_frustrations_detailed = json_read(f'{input_folderpath}/frustrations-detailed.json')
    frustrations_detailed = '' 
    for json_frustration_detailed in json_frustrations_detailed['data']:
        _method = json_frustration_detailed['method']
        _time = json_frustration_detailed['time']
        _cost = json_frustration_detailed['cost']
        _challenges = json_frustration_detailed['challenges']
        _emotions = json_frustration_detailed['emotions']
        _why = json_frustration_detailed['why']
        frustrations_detailed += f'- {_method}, {_time}, {_cost}, {_challenges}, {_emotions}, {_why}.\n'
    with open(f'{input_folderpath}/my-method.txt') as f: my_method = f.read()
    with open(f'{input_folderpath}/benefits.txt') as f: benefits = f.read()
    ### 
    output_filepath = f'{input_folderpath}/summary.txt'
    prompt = f'''
        Summarize the following content.
        #################################################################
        Market: 
        #################################################################
        {market}
        #################################################################
        Niche: 
        #################################################################
        {niche}
        #################################################################
        Who: 
        #################################################################
        {who}
        #################################################################
        Frustrations: 
        #################################################################
        {frustration}
        #################################################################
        Mission: 
        #################################################################
        {domino}
        #################################################################
        Results: 
        #################################################################
        {results}
        #################################################################
        Other Methods: 
        #################################################################
        {past_methods}
        #################################################################
        Frustrations Detailed: 
        #################################################################
        {frustrations_detailed}
        #################################################################
        My Method: 
        #################################################################
        {my_method}
        #################################################################
        Benefits: 
        #################################################################
        {benefits}
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    with open(output_filepath, 'w') as f: 
        f.write(reply)

who_manual()

if 0:
    # who()
    who_manual()
    frustration()
    domino()
    results()
    past_methods()
    frustrations_detailed()
    my_method_manual(my_method_name)
    benefits()
    external_benefits()
    internal_benefits()
    expertise()
    value_statement()
    doc()

    recap()
    summary()

def market_research():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    with open(f'{input_folderpath}/value-statement-one-liner.txt') as f: value_statement_one_liner = f.read()
    with open(f'{input_folderpath}/doc.txt') as f: doc = f.read()
    ### 
    output_filepath = f'{input_folderpath}/market-research.txt'
    prompt = f'''
        I need you to do deep research on my target customer and business. 
        I am creating an ebook that "{value_statement_one_liner}".
        This research doc will be crucial to helping us create the right PDF, products, sales pages, content, and marketing that converts.
        Analyze the current market opportunity for {niche}. 
        Include:
        Current market size and growth projections
        Key trends driving growth
        Major pain points being solved
        Consumer demand and behavior shifts
        Current gaps & pain points in existing solutions
        Unique aspects making this timely
        Emerging tools or technologies making this easier
        The financial potential for new entrants (provide statistics, sources, and insights on why this is a lucrative opportunity)
        Target audience overview
        Format as 3-5 concise paragraphs with specific numbers, sources, and links to all sources.
        Please ensure you include all links to research, stats, studies, and articles.
        I have also attached my Business Info doc below that will tell you more about my business and target audience.
        {doc}        
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    with open(output_filepath, 'w') as f: 
        f.write(reply)




def market_method():
    input_folderpath = f'{campaign_folderpath}/{who_selected_slug}'
    init_folderpath = f'{campaign_folderpath}/init'
    with open(f'{init_folderpath}/market.txt') as f: market = f.read().strip()
    with open(f'{init_folderpath}/niche.txt') as f: niche = f.read().strip()
    with open(f'{input_folderpath}/who-selected.txt') as f: who = f.read()
    with open(f'{input_folderpath}/value-statement-one-liner.txt') as f: value_statement_one_liner = f.read()
    with open(f'{input_folderpath}/doc.txt') as f: doc = f.read()
    ### 
    output_filepath = f'{input_folderpath}/market-method.txt'
    prompt = f'''
        I need you to do deep research on my target customer and business. 
        I am creating an ebook that "{value_statement_one_liner}".
        This research doc will be crucial to helping us create the right PDF, products, sales pages, content, and marketing that converts.
        For my method, provide:
        What key problems it solves
        Why it's uniquely positioned to succeed
        How it differs from traditional approaches
        Why this solution is timely now
        Include specific benefits and metrics where possible.
        Format as 3-5 concise paragraphs with specific numbers, sources, and links to all sources.
        Please ensure you include all links to research, stats, studies, and articles.
        I have also attached my Business Info doc below that will tell you more about my business and target audience.
        {doc}        
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    with open(output_filepath, 'w') as f: 
        f.write(reply)



# market_research()
market_method()
