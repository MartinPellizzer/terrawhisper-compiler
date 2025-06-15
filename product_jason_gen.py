from oliark_llm import llm_reply

model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'

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
    'avoid moisture with dessicants',
    'regular spoliage checks',
]

step_list = [
    'proper drying',
    'airtight storage',
    'avoid moisture sources',
    'cool, dark storage',
    'clean equipment / contamination control',
    'use of preservatives',
    'high-quality herbs',
    'proper extraction',
]

for step_i, step in enumerate(step_list):
    prompt = f'''
        I have a content template that goes like this:
        Why it's important.
        What's involved. Briefly describe the critica components associated with the step/factor. At least 3 components.
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
    # prompt += '/no_think'
    reply = llm_reply(prompt, model_path=model_filepath).strip()
    if '</think>' in reply: reply = reply.split('</think>')[1].strip()
    step_slug = step.lower().strip().replace(' ', '').replace('/', '')
    step_slug = f'{step_i}-{step_slug}'
    with open(f'products/save-your-herbal-stockpile/{step_slug}.txt', 'w') as f: f.write(reply)
