import json

import util
import utils_ai

import data_csv

import g

from oliark import csv_read_rows, csv_read_rows_to_json
from oliark_llm import llm_reply

vault_folderpath = '/home/ubuntu/vault'
model = f'{vault_folderpath}/llms/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'

# model = 'Mistral-Nemo-Instruct-2407.Q8_0.gguf'
# model = 'Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'
# model = 'Meta-Llama-3.1-8B-Instruct-Q8_0.gguf'

status_rows, status_cols = data_csv.status()

def gen_ailments_form_keywords():
    content = util.file_read('database/keywords.txt')
    prompt = f'''
        Extract from the following list of KEYWORDS all the ailments.
        Follow the GUIDELINES below.
        GUIDELINES:
        - write only the ailments
        - don't repeat the same ailment twice
        - write each ailment using as few words as possible
        KEYWORDS:
        {content}
    '''
    reply = utils_ai.gen_reply(prompt, model=model)


def find_similar():
    reply = utils_ai.gen_reply('test', model=model)

    with open('database/ailments.txt') as f: content = f.read()
    ailments = content.split('\n')
    status_names = [status_row[status_cols['status_names']] for status_row in status_rows]

    for ailment in ailments:
        ailment = ailment.strip()
        if ailment == '': continue
        status_names_prompt = '\n'.join(status_names)
        print()
        print()
        print()
        print('***********************')
        print(ailment)
        print('***********************')
        prompt = f'''
            Extract the items from the following LIST that are the most similar to the following QUERY.
            Follow the GUIDELINES below.
            ## QUERY
            {ailment}
            ## LIST
            {status_names_prompt}
            ## GUIDELINES
            Write only the list items
            Order the list items from the most similar to the least
            Write as few words as possible
        '''
        reply = utils_ai.gen_reply(prompt, model=model)
        lines = []
        for line in reply.split('\n'):
            line = line.strip()
            if line == '': continue
            line = line.replace('-', '')
            line = line.strip()
            lines.append(line)
        print()
        print(f'## {ailment}')
        print('-----------------------')
        for line in lines:
            print(f'    - {line}')
        print('-----------------------')
        cmd = input('>>> ')
        if cmd == 'q': break


def llm_similar_ailments_from_ailment(ailment_name):
    prompt = f'''
        Statistically speaking, what other ailments can experience people who suffer from {ailment_name}.
        Reply in numbered list format.
        Write only 1 ailment per list item.
        Write only the list of correlated ailments and nothing else.
        Order the list by the most probable and common ailments.
        Don't include acronyms and content in between brackets.
    '''
    reply = utils_ai.gen_reply(prompt, model=model)
    items = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if '. ' not in line: continue
        line = '. '.join(line.split('. ')[1:])
        line = line.replace('.', '')
        line = line.strip()
        items.append(line)
    print('***********************')
    for item in items:
        print(item)
    print('***********************')

    ailments = '\n- '.join(items)
    prompt = f'''
        For each of the AILMENTS listed below, write what's the main body organ and body system that's most affected by the ailment.
        Reply with a numbered list in the format: [ailment_name] - [body_organ_name] - [body_sytem_name].
        Example of list item: bronchitis - lungs - respiratory system
        Write only 1 organ and 1 system per ailment.
        Don't include acronyms.
        Don't content in between brackets.
        AILMENTS:
        {ailments}
    '''
    print(prompt)
    reply = utils_ai.gen_reply(prompt, model=model)
    items = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        if '. ' not in line: continue
        line = '. '.join(line.split('. ')[1:])
        line = line.replace('.', '')
        line = line.strip()
        items.append(line)
    print('***********************')
    for item in items:
        print(item)
    print('***********************')
    
def llm_csv_gen_ailments_body_parts():
    status_rows = csv_read_rows(g.CSV_STATUS_FILEPATH)
    for status_row in status_rows[1:]:
        print(status_row[5])
        if status_row[5] == '':            
            prompt = f'''
                What is the body part most affectect by the ailment {status_row[3]}?
                Select only 1 body part, the most interested one by this ailment.
                Reply with the following json format: {{"ailment_name": name_of_ailment, "body_part_name": name_of_body_part}}
                Example of reply = {{"ailment_name": "bronchitis", "body_part_name": "lungs"}}
                Reply only with the json, don't add additional info.
            '''
            reply = llm_reply(prompt, model).strip().lower()
            reply_json = json.loads(reply)
            print(reply_json)
            body_part_name = reply_json["body_part_name"]
            status_row[5] = body_part_name
        print(status_row)
        
        util.csv_set_rows(g.CSV_STATUS_FILEPATH, status_rows)
            
llm_csv_gen_ailments_body_parts()

