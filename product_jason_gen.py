import os

from lib import io

from oliark_llm import llm_reply

model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'

json_data_filepath = f'products/save-your-herbal-stockpile/data.json'
json_data = io.json_read(json_data_filepath, create=True)
if 'step_list' not in json_data: json_data['step_list'] = []
io.json_write(json_data_filepath, json_data)

def ai_llm_steps():
    prompt = f'''
        Identify the top 6 experts on preventing mold, spoliage, and potency loss when making a herbal remedy as a diy apothecary, and give me their top 5 strategies. Provide it to me in a list.
    '''
    # prompt += '/no_think'
    reply = llm_reply(prompt, model_path=model_filepath).strip()
    if '</think>' in reply: reply = reply.split('</think>')[1].strip()
    prompt = f'''
        Do you see any duplicate answer repeated from one expert to the next?
        {reply}
    '''
    # prompt += '/no_think'
    reply = llm_reply(prompt, model_path=model_filepath).strip()
    if '</think>' in reply: reply = reply.split('</think>')[1].strip()

step_list = [
    'proper drying and curing',
    'airtight dark glass containers',
    'cool, dry, dark storage',
    'clean equipment',
    'regular spoliage checks',
]

def ai_llm_steps(think=False):
    json_data = io.json_read(json_data_filepath, create=True)
    for step_i, step in enumerate(step_list):
        prompt = f'''
            I have a content template that goes like this:
            Why it's important.
            What's involved. Briefly describe the critical components associated with the step/factor. At least 3 components.
            Component 1
            Component 2
            Component 3
            How to do it. Specific advice on what action(s) to take.
            Component 1
            Step 1
            Step 2
            Step 3
            Etc.
            Component 2
            Step 1
            Step 2
            Step 3
            Etc.
            Etc.
            What can happen.
            Good outcome.
            Better outcome.
            Best outcome.
            Can you apply that template to "{step}" when it comes to preventing mold, spoliage, and potency loss when making a herbal remedy as a diy apothecary?
        '''
        if not think:
            prompt += '/no_think'
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply: reply = reply.split('</think>')[1].strip()
        step_slug = step.lower().strip().replace(' ', '-').replace('/', '')
        step_slug = f'{step_i}-{step_slug}'
        json_data['step_list'].append(reply)
        io.json_write(json_data_filepath, json_data)
        # with open(f'products/save-your-herbal-stockpile/{step_slug}.txt', 'w') as f: f.write(reply)

# ai_llm_steps(think=True)

if 1:
    input_folderpath = 'products/save-your-herbal-stockpile/data'
    output_folderpath = 'products/save-your-herbal-stockpile/pages'
    for input_filename in os.listdir(input_folderpath):
        input_filepath = f'{input_folderpath}/{input_filename}'
        output_filepath = f'{output_folderpath}/{input_filename}'
        with open(input_filepath) as f: input_content = f.read()
        with open('assets/prompt/raw-mode.txt') as f: input_guidelines = f.read()
        prompt = f'''
            Write a page for my ebook using the following CONTENT and GUIDELINES:
            CONTENT:
            {input_content}
            GUIDELINES:
            Don't include bold and italic.
            Use the following structure:
            Why it's important
            What's involved (list the steps/factors) 
            How to do it (describe each step/factor)
            What can happen (describe the possible outcomes)
        '''
            # Write in paragraphs using plain text. Don't include bold and italic.
            # {input_guidelines}
        prompt += '/no_think'
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply: reply = reply.split('</think>')[1].strip()
        with open(output_filepath, 'w') as f: f.write(reply)
        # quit()

if 0:
    output_folderpath = 'products/save-your-herbal-stockpile/pages'
    json_data_filepath = 'products/save-your-herbal-stockpile/data.json'
    json_data = io.json_read(json_data_filepath)
    step_list in json_data['step_list']
    for i, step in enumerate(step_list):
        output_filepath = f'{output_folderpath}/{i}.txt'
        input_content = step
        with open('assets/prompt/raw-mode.txt') as f: input_guidelines = f.read()
        prompt = f'''
            Write a page for my ebook using the following CONTENT and GUIDELINES:
            CONTENT:
            {input_content}
            GUIDELINES:
            Don't include bold and italic.
            Use the following structure:
            Why it's important
            What's involved (list the steps/factors) 
            How to do it (describe each step/factor)
            What can happen (describe the possible outcomes)
        '''
        prompt += '/no_think'
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply: reply = reply.split('</think>')[1].strip()
        with open(output_filepath, 'w') as f: f.write(reply)

from fpdf import FPDF

pdf = FPDF('P', 'mm', 'Letter')

pdf.set_auto_page_break(auto=True, margin=15)

input_folderpath = 'products/save-your-herbal-stockpile/pages'
for i, input_filename in enumerate(os.listdir(input_folderpath)):
    input_filepath = f'{input_folderpath}/{input_filename}'
    with open(input_filepath) as f: input_content = f.read()
    input_content = input_content.replace('–', '-')
    input_content = input_content.replace('’', "'")
    input_content = ''.join([i if ord(i) < 128 else '' for i in input_content])
    pdf.add_page()
    pdf.set_font('helvetica', '', 24)
    pdf.cell(0, 24, f'{str(i+1)}. Step/Factor', ln=True)
    lines = input_content.split('\n')
    blocks = []
    block_cur = []
    for line in lines:
        line = line.strip()
        if line == '':
            if block_cur != []:
                blocks.append(block_cur)
            block_cur = []
        else:
            print(line)
            if line.lower() == 'why it\'s important': continue
            if line.lower() == 'what\'s involved': continue
            if line.lower() == 'how to do it':
                blocks.append(['how to do it'])
                block_cur = []
                continue
            if line.lower() == 'what can happen':
                blocks.append(['what can happen'])
                block_cur = []
                continue
            block_cur.append(line)
    blocks.append(block_cur)
    # quit()
    for block in blocks:
        '''
        sub_blocks = []
        sub_block_cur = ''
        for line in block:
            line = line.strip()
            if line.lower() == 'why it\'s important':
                sub_blocks.append(line)
            else:
                sub_block_cur += line + '\n'
        sub_blocks.append(sub_block_cur)
        # content = '\n'.join(block)
        '''
        content = '\n'.join(block)
        if content.strip().lower() == 'how to do it':
            pdf.set_font('helvetica', '', 18)
            pdf.multi_cell(0, 6, content.capitalize() + '\n')
        elif content.strip().lower() == 'what can happen':
            pdf.set_font('helvetica', '', 18)
            pdf.multi_cell(0, 6, content.capitalize() + '\n')
        else:
            pdf.set_font('helvetica', '', 11)
            pdf.multi_cell(0, 6, content + '\n')
        '''
        for sub_block in sub_blocks:
            print(sub_block)
            if sub_block.strip().lower() == 'why it\'s important':
                print('********************')
                pdf.set_font('helvetica', '', 18)
                pdf.multi_cell(0, 6, sub_block + '\n')
            else:
                pdf.set_font('helvetica', '', 11)
                pdf.multi_cell(0, 6, sub_block + '\n')
        '''
        
        '''
        for line in block:
            line = line.strip()
            if line == '': continue
            pdf.multi_cell(0, 6, line + '\n')
        '''
        # pdf.multi_cell(0, 6, content + '\n')
        # pdf.multi_cell(0, 6, '\n')
        

pdf_filepath = 'products/save-your-herbal-stockpile/pdf_1.pdf'
pdf.output(pdf_filepath)
# subprocess.Popen([pdf_filepath], shell=True)
