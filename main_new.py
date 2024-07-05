import time

from llama_cpp import Llama

import prompts_components

llm = Llama(
      model_path="/home/ubuntu/llm/Meta-Llama-3-8B-Instruct.Q8_0.gguf",
      n_gpu_layers=-1,
)

herb_name_common = 'chamomile'
herb_name_scientific = 'Martiarca chamomilla'
status = 'insomnia'

prompt = f'''
    write a list of parts of the herb {herb_name_common} ({herb_name_scientific}) that helps with insomnia.
    you must follow the GUIDELINES.
    respond only in JSON format following the EXAMPLE_STRUCTURE.

    ## GUIDELINES
    only choose the parts from the following list: root, stem, leaf, flower, fruit, seed, rhizome, bark, bud.
    try to include at least 3 parts.

    ## EXAMPLE_STRUCTURE
    [
        {{
            "part_name": "name of the plant's part",
            "part_description": "description on why this part helps"
        }}
    ]
    
'''

prompt = f'''
    # GENERATE LIST 

    write a numbered list of parts of the herb {herb_name_common} ({herb_name_scientific}) that helps with insomnia.
    follow the GUIDELINES below.

    ## GUIDELINES

    - only choose the parts from the following list: root, stem, leaf, flower, fruit, seed, rhizome, bark, bud.
    - try to include at least 2-3 parts.

'''

# prompt = f'''
#     write a list of parts of the herb {{herb_name_common}} ({{herb_name_scientific}}) that helps with insomnia and explain why.
# '''

stream = llm.create_chat_completion(
    messages = [
        {
            'role': 'user',
            'content': prompt,
        }
    ],
    stream = True,
    temperature = 0.7,
    # response_format = {
        # "type": "json_object",
        # "schema": {
            # "type": "object",
            # "properties": {
                # "part_name": {"type": "string"},
                # "description": {"type": "string"},
            # },
            # "required": ["part_name"],
        # },
    # }
)

start_time = time.time()

reply = ''
for chunk in stream:
    if 'content' in chunk['choices'][0]['delta'].keys():
        token = chunk['choices'][0]['delta']['content']
        reply += token
        print(token, end='', flush=True)
    
end_time = time.time()

print(f'execution time: {end_time - start_time}')
