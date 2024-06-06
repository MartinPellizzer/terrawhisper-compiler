from groq import Groq
from ctransformers import AutoModelForCausalLM
import time


with open('C:/api/groq.txt', 'r', encoding='utf-8') as f:
    api = f.read()


client = Groq(
    api_key=api,
)


MODELS = [
    'C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.1.Q8_0.gguf',
    'C:\\Users\\admin\\Desktop\\models\\mistral-7b-instruct-v0.2.Q8_0.gguf',
    'C:\\Users\\admin\\Desktop\\models\\neural-chat-7b-v3-3.Q8_0.gguf',
    'C:\\Users\\admin\\.cache\\lm-studio\\models\\TheBloke\\Starling-LM-7B-alpha-GGUF\\starling-lm-7b-alpha.Q8_0.gguf',
]
MODEL = MODELS[1]

llm = AutoModelForCausalLM.from_pretrained(
    MODEL,
    model_type="mistral", 
    context_length=2048, 
    max_new_tokens=2048,
    )


def gen_reply_api(prompt):
    completion = client.chat.completions.create(
        # model="llama2-70b-4096",
        model="mixtral-8x7b-32768",
        # model="llama3-70b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.5,
    )

    reply = completion.choices[0].message.content
    print()
    print()
    print()
    print("Q:")
    print()
    print(prompt)
    print()
    print("A:")
    print()
    print(reply)
    print()
    return reply


def gen_reply_local(prompt):
    print()
    print("Q:")
    print()
    print(prompt)
    print()
    print("A:")
    print()
    reply = ''
    for text in llm(prompt, stream=True):
        reply += text
        print(text, end="", flush=True)
    print()
    print()
    return reply


def gen_reply(prompt):
    reply = ''
    try: reply = gen_reply_api(prompt)
    except: 
        print(
            '''
            ********************************************************************
            ERROR API: WAITING FOR SOME MINUTES... THEN RETRY...
            ********************************************************************
            '''
        )
        time.sleep(600)
    # reply = gen_reply_local(prompt)

    return reply



# #################################################################################
# FORMAT REPLY
# #################################################################################
def reply_to_paragraphs(reply):
    reply = reply.strip()
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if ':' in line: continue
        # if ':' in line: 
        #     tmp_line = line.split(':')[1]
        #     if tmp_line.strip() == '': continue
        if len(line.strip().split(' ')) <= 16: continue
        reply_formatted.append(line)
    return reply_formatted

def reply_to_paragraph(reply):
    reply = reply.strip()
    if '\n' in reply: return [reply, 'too many paragraphs']
    if ':' in reply: return [reply, 'found : in text']
    if reply[-1] != '.': return [reply, 'text not ending with .']
    return [reply, '']
    

def reply_to_list_column(reply):
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): return [reply, 'list item don\'t start with number']
        if line[-1] != '.': return [reply, 'missing ending .']
        
        line = '.'.join(line.split('.')[1:]).strip()
        if line == '': return [reply, 'missing text after number']

        # if len(line.split(' ')) < 10: continue

        line = line.replace('*', '')
        line = line.replace('[', '')
        line = line.replace(']', '')

        if ':' not in line: return [reply, 'missing :']
        line_chunks = line.split(':')
        chunk_1 = line_chunks[0].split('(')[0].strip()
        chunk_2 = line_chunks[1].strip()
        line = f'{chunk_1}: {chunk_2}'

        reply_formatted.append(line)

    return [reply_formatted, '']



def reply_herbs_parts_to_list(reply):
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): return [reply, 'list item don\'t start with number']
        if line[-1] != '.': return [reply, 'missing ending .']
        
        line = '.'.join(line.split('.')[1:]).strip()
        if line == '': return [reply, 'missing text after number']

        # if len(line.split(' ')) < 10: continue

        line = line.replace('*', '')
        line = line.replace('[', '')
        line = line.replace(']', '')


        if ':' not in line: return [reply, 'missing :']
        line_chunks = line.split(':')
        chunk_1 = line_chunks[0].split('(')[0].strip()
        if 'aerial' in chunk_1: continue
        chunk_2 = line_chunks[1].strip()
        line = f'{chunk_1}: {chunk_2}'

        reply_formatted.append(line)

    return [reply_formatted, '']


    

def reply_to_list(reply):
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if not line[0].isdigit(): continue
        
        line = '. '.join(line.split('. ')[1:]).strip()
        if line == '': continue

        # if len(line.split(' ')) < 10: continue

        reply_formatted.append(line)

    return reply_formatted

    

def reply_to_list_01(reply):
    reply_formatted = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue

        if not line[0].isdigit(): return [reply, 'list item don\'t start with number']
        if line[-1] != '.': return [reply, 'missing ending .']
        
        line = '. '.join(line.split('. ')[1:]).strip()
        if line == '': [reply, 'missing text after number']

        # if len(line.split(' ')) < 10: continue

        reply_formatted.append(line)

    return [reply_formatted, '']
