import util
import utils_ai

import data_csv

model = 'Mistral-Nemo-Instruct-2407.Q8_0.gguf'
# model = 'Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'
# model = 'Meta-Llama-3.1-8B-Instruct-Q8_0.gguf'

status_rows, status_cols = data_csv.status()

def gen_ailments():
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

