from oliark_io import json_read, json_write
from oliark_llm import llm_reply

def ai_paragraph_gen(filepath, data, obj, key, prompt, reply_start='', regen=False, clear=False, print_prompt=False):
    if key not in obj: obj[key] = ''
    if regen: obj[key] = ''
    if clear: 
        obj[key] = ''
        json_write(filepath, data)
        return
    if obj[key] == '':
        if print_prompt: print(prompt)
        reply = llm_reply(prompt)
        if reply.strip() != '':
            if reply.strip().startswith('I can\'t'): reply = 'CANT'
            elif reply.strip().startswith('I couldn\'t'): reply = 'CANT'
            elif 'cannot' in reply.strip(): reply = 'CANT'
            elif reply_start != '':
                if not reply.strip().startswith(reply_start): 
                    print(f'TARGET REPLY START: {reply_start}')
                    print(f'REPLY:              {reply.strip()[:40]}')
                    reply = 'WRONG START'
            obj[key] = reply
            json_write(filepath, data)
