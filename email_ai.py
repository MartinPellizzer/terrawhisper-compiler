import os
import json
import random

from oliark_llm import llm_reply

from lib import io

model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'

#######################################################
# outline
#######################################################
# problem
# story
# failed solution (what/why)
# working solution (what/why/how)
# cta

#######################################################
# problem
#######################################################
problem = 'heat rash'

#######################################################
# story
#######################################################
prompt = f'''
    today i want to write an email about the following seasonal ailment: {problem}.
    i want to start the email with a story, so give me 10 ideas of story plots i can write to start this email.
    the story ideas must be about someone i know, be relatable, and be a real story, not a fiction story.
    reply in the following JSON format: 
    [
        {{"answer": "write story plot idea 1 here"}}, 
        {{"answer": "write story plot idea 2 here"}}, 
        {{"answer": "write story plot idea 3 here"}} 
    ]
    only reply with the JSON, don't add additional info.
    /no_think
'''
print(prompt)
reply = llm_reply(prompt, model_path=model_filepath).strip()
if '</think>' in reply:
    reply = reply.split('</think>')[1].strip()
json_data = {}
try: json_data = json.loads(reply)
except: pass 
if json_data != {}:
    lst = []
    for item in json_data:
        try: answer = item['answer']
        except: continue
        lst.append(answer)
# for i, e in enumerate(lst):
    # print(f'{i} - {e}')
# index = int(input('choose story >> '))
story = random.choice(lst)
# story = lst[index]

#######################################################
# failed solution
#######################################################
if 0:
    prompt = f'''
        today i want to write an email about the following seasonal ailment: {problem}.
        i want you to list the 10 most common solution people use for this ailment, and why they are not enough.
        don't include herbal remedies as solutions.
        reply in the following JSON format: 
        [
            {{"answer": "write the solution 1 here", "why": "write why solution 1 is not enough"}}, 
            {{"answer": "write the solution 2 here", "why": "write why solution 1 is not enough"}}, 
            {{"answer": "write the solution 3 here", "why": "write why solution 1 is not enough"}} 
        ]
        only reply with the JSON, don't add additional info.
        /no_think
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    json_data = {}
    try: json_data = json.loads(reply)
    except: pass 
    if json_data != {}:
        lst = []
        for item in json_data:
            try: answer = item['answer']
            except: continue
            try: why = item['why']
            except: continue
            lst.append(f'{answer} {why}')
    failed_solution = random.choice(lst)

#######################################################
# working solution
#######################################################
prompt = f'''
    today i want to write an email about the following seasonal ailment: {problem}.
    i want you to give me the 10 best herbal remedies to use for this ailment, why they works, and how to use them.
    reply in the following JSON format: 
    [
        {{"answer": "write the herbal remedy 1 here", "why": "write why herbal remedy 1 works here", "how": "write how to use herbal remedy 1 here"}}, 
        {{"answer": "write the herbal remedy 2 here", "why": "write why herbal remedy 2 works here", "how": "write how to use herbal remedy 2 here"}}, 
        {{"answer": "write the herbal remedy 3 here", "why": "write why herbal remedy 3 works here", "how": "write how to use herbal remedy 3 here"}}, 
        {{"answer": "write the herbal remedy 4 here", "why": "write why herbal remedy 4 works here", "how": "write how to use herbal remedy 4 here"}}, 
        {{"answer": "write the herbal remedy 5 here", "why": "write why herbal remedy 5 works here", "how": "write how to use herbal remedy 5 here"}}, 
        {{"answer": "write the herbal remedy 6 here", "why": "write why herbal remedy 6 works here", "how": "write how to use herbal remedy 6 here"}}, 
        {{"answer": "write the herbal remedy 7 here", "why": "write why herbal remedy 7 works here", "how": "write how to use herbal remedy 7 here"}}, 
        {{"answer": "write the herbal remedy 8 here", "why": "write why herbal remedy 8 works here", "how": "write how to use herbal remedy 8 here"}}, 
        {{"answer": "write the herbal remedy 9 here", "why": "write why herbal remedy 9 works here", "how": "write how to use herbal remedy 9 here"}}, 
        {{"answer": "write the herbal remedy 10 here", "why": "write why herbal remedy 10 works here", "how": "write how to use herbal remedy 10 here"}} 
    ]
    only reply with the JSON, don't add additional info.
    /no_think
'''
print(prompt)
reply = llm_reply(prompt).strip()
if '</think>' in reply:
    reply = reply.split('</think>')[1].strip()
json_data = {}
try: json_data = json.loads(reply)
except: pass 
if json_data != {}:
    lst = []
    for item in json_data:
        try: answer = item['answer']
        except: continue
        try: why = item['why']
        except: continue
        try: how = item['how']
        except: continue
        lst.append(f'{answer} {why} {how}')
working_solution = random.choice(lst)

#######################################################
# email
#######################################################
    # Failed solution:
    # {failed_solution}
prompt = f'''
    Write a short email for my newsletter with the following STRUCTURE and GUIDELINES:
    <STRUCTURE>
    Introduction: 
    {story}
    Working solution:
    {working_solution}
    Conclusion:
    Encourage them to make this herbal remedy, in case they need it.
    Start the email with the words "Dear Apothecary, " and end it with the words "Stay Grounded, Leen".
    Add a P.S. section.
    </STRUCTURE>
    <GUIDELINES>
    Write this in my personal voice. Make it raw, honest, and unfiltered. Use punchy one-liners, bold emotional confessions, and dramatic pacing with short paragraphs. Don’t polish the language too much—I want it real. It should feel like I’m talking directly to a friend over a drink, not giving a TED Talk.
    Use casual slang where it fits. Curse if it serves the point. Use ellipses, parentheses, and capitalization for rhythm and emphasis. Balance vulnerability with wit. Show that I’m not afraid to admit mistakes, but I’m also not afraid to laugh at them.
    Think: Gary Vee meets Brene Brown with a little Dave Chappelle spice.
    Never swear.
    Never use acronym.
    </GUIDELINES>
    /no_think

'''
print(prompt)
'''
reply = llm_reply(prompt).strip()
if '</think>' in reply:
    reply = reply.split('</think>')[1].strip()
email = reply

print(reply)

'''
'''
print(story)
print(failed_solution)
print(working_solution)
print(email)
'''
