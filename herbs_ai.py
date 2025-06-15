import os
import json
import random

from oliark_llm import llm_reply

import llm
from lib import g
from lib import io
from lib import data
from lib import utils
from lib import components

model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'

def medicine_poison_ai(json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    herb_name_scientific = json_article['herb_name_scientific']
    key = 'medicine_or_poison'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if clear: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '':
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            prompt = f'''
                Tell me if the following herb is considered medicinal, poisonous, or inert: {herb_name_scientific}.
                Also, tell give a confidence score from 1 to 10, indicating how sure you are about your answer.
                Reply in the following JSON format: 
                [
                    {{"answer": <write "medicine", "poison", or "inert" here>, "score": 8}} 
                ]
                Only reply with the JSON, don't add additional info.
                Don't include notes, reply ONLY with the JSON.
                /no_think
            '''
            reply = llm_reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                _objs = []
                for item in json_data:
                    try: answer = item['answer']
                    except: continue
                    try: score = item['score']
                    except: continue
                    _objs.append({
                        "answer": answer, 
                        "score": score,
                    })
                for _obj in _objs:
                    answer = _obj['answer']
                    score = _obj['score']
                    found = False
                    for output in outputs:
                        if answer in output['answer']: 
                            output['mentions'] += 1
                            output['confidence_score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'answer': answer, 
                            'mentions': 1, 
                            'confidence_score': int(score), 
                        })
        outputs_final = []
        for output in outputs:
            outputs_final.append({
                'answer': output['answer'],
                'mentions': int(output['mentions']),
                'confidence_score': int(output['confidence_score']),
                'total_score': int(output['mentions']) * int(output['confidence_score']),
            })
        outputs_final = sorted(outputs_final, key=lambda x: x['total_score'], reverse=True)
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs_final:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        json_article[key] = outputs_final
        io.json_write(json_article_filepath, json_article)

def benefits_ai(json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    key = 'benefits'
    if key not in json_article: json_article[key] = []
    if regen: json_article[key] = []
    if clear: 
        json_article[key] = []
        io.json_write(json_article_filepath, json_article)
        return
    outputs = []
    if json_article[key] == []:
        output_plants = []
        reply_valid = False
        for i in range(3):
            rnd = random.randint(17, 23)
            prompt = f'''
                List the {rnd} best health benefits of the {herb_name_scientific} plant.
                Also, for each health benefit give a confidence score from 1 to 10, indicating how sure you are that {herb_name_scientific} has that benefit.
                Write each benefits in 3 words or less.
                Make the first word in each benefit a third-person singular action verb.
                Reply in the following JSON format: 
                [
                    {{"answer": "write benefit 1 here", "score": "10"}}, 
                    {{"answer": "write benefit 2 here", "score": "5"}}, 
                    {{"answer": "write benefit 3 here", "score": "7"}} 
                ]
                Only reply with the JSON, don't add additional info.
                /no_think
            '''
            reply = llm_reply(prompt, model_path=model_filepath).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                objects = []
                for item in json_data:
                    try: answer = item['answer']
                    except: continue
                    try: score = item['score']
                    except: continue
                    objects.append({
                        "answer": answer, 
                        "score": score,
                    })
                for obj in objects:
                    answer = obj['answer']
                    score = obj['score']
                    found = False
                    for output in outputs:
                        print(output)
                        print(answer, '->', output['answer'])
                        if answer in output['answer']: 
                            output['mentions'] += 1
                            output['score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'answer': answer, 
                            'mentions': 1, 
                            'score': int(score), 
                        })
            if outputs != []:
                reply_valid = True
                break
        outputs_final = []
        for output in outputs:
            outputs_final.append({
                'answer': output['answer'],
                'mentions': int(output['mentions']),
                'score': int(output['score']),
                'grade': int(output['mentions']) * int(output['score']),
            })
        outputs_final = sorted(outputs_final, key=lambda x: x['grade'], reverse=True)
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs_final:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        if outputs_final != []:
            json_article[key] = outputs_final[:20]
            io.json_write(json_article_filepath, json_article)
        else:
            json_article[key] = 'FAILED'
            io.json_write(json_article_filepath, json_article)

def constituents_ai(json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    #
    key = 'constituents'
    if key not in json_article: json_article[key] = []
    if regen: json_article[key] = []
    if clear: 
        json_article[key] = []
        io.json_write(json_article_filepath, json_article)
        return
    outputs = []
    if json_article[key] == []:
        output_plants = []
        reply_valid = False
        for i in range(3):
            rnd = random.randint(17, 23)
            prompt = f'''
                List the {rnd} best medicinal constituents of the {herb_name_scientific} plant.
                By medicinal constituents, I mean things like types of carbohydrates, lipids, terpenes, polyphenols, alkaloids, etc... 
                Also, for each item in the list give a confidence score from 1 to 10, indicating how sure you are about that answer.
                Reply in the following JSON format: 
                [
                    {{"answer": "write constituent 1 here", "score": "10"}}, 
                    {{"answer": "write constituent 2 here", "score": "5"}}, 
                    {{"answer": "write constituent 3 here", "score": "7"}} 
                ]
                Only reply with the JSON, don't add additional info.
                Answer in as few words as possible.
                /no_think
            '''
            reply = llm_reply(prompt, model_path=model_filepath).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                objects = []
                for item in json_data:
                    try: answer = item['answer']
                    except: continue
                    try: score = item['score']
                    except: continue
                    answer = answer.split('(')[0].strip().lower()
                    objects.append({
                        "answer": answer, 
                        "score": score,
                    })
                for obj in objects:
                    answer = obj['answer']
                    score = obj['score']
                    found = False
                    for output in outputs:
                        print(output)
                        print(answer, '->', output['answer'])
                        if answer in output['answer']: 
                            output['mentions'] += 1
                            output['score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'answer': answer, 
                            'mentions': 1, 
                            'score': int(score), 
                        })
            if outputs != []:
                reply_valid = True
                break
        outputs_final = []
        for output in outputs:
            outputs_final.append({
                'answer': output['answer'],
                'mentions': int(output['mentions']),
                'score': int(output['score']),
                'grade': int(output['mentions']) * int(output['score']),
            })
        outputs_final = sorted(outputs_final, key=lambda x: x['grade'], reverse=True)
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs_final:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        if outputs_final != []:
            json_article[key] = outputs_final[:20]
            io.json_write(json_article_filepath, json_article)
        else:
            json_article[key] = 'FAILED'
            io.json_write(json_article_filepath, json_article)

def parts_ai(json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    #
    key = 'parts'
    if key not in json_article: json_article[key] = []
    if regen: json_article[key] = []
    if clear: 
        json_article[key] = []
        io.json_write(json_article_filepath, json_article)
        return
    outputs = []
    if json_article[key] == []:
        parts = ['root', 'stem', 'leaf', 'flower', 'fruit', 'seed']
        parts_prompt = ', '.join(parts)
        parts_prompt_json = [f'{{"answer": "{part}", "score": "write score here"}}' for part in parts]
        parts_prompt_json = ',\n'.join(parts_prompt_json)[:-1] + '\n'
        output_plants = []
        reply_valid = False
        for i in range(3):
            # rnd = random.randint(17, 23)
            prompt = f'''
                For each of the following parts of the {herb_name_scientific} plant, give me a confidence score from 1 to 10 indicating how much this part is used for medicinal purposes: {parts_prompt}.
                Reply in the following JSON format: 
                [{parts_prompt_json}]
                Only reply with the JSON, don't add additional info.
                Answer in as few words as possible.
                /no_think
            '''
            reply = llm_reply(prompt, model_path=model_filepath).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                objects = []
                for item in json_data:
                    try: answer = item['answer']
                    except: continue
                    try: score = item['score']
                    except: continue
                    answer = answer.split('(')[0].strip().lower()
                    part_found = False
                    part = ''
                    for _part in parts:
                        if _part.lower().strip() == answer.lower().strip():
                            part = _part
                            part_found = True
                            break
                    if part_found:
                        objects.append({
                            "answer": answer, 
                            "score": score,
                        })
                for obj in objects:
                    answer = obj['answer']
                    score = obj['score']
                    found = False
                    for output in outputs:
                        print(output)
                        print(answer, '->', output['answer'])
                        if answer in output['answer']: 
                            output['mentions'] += 1
                            output['score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'answer': answer, 
                            'mentions': 1, 
                            'score': int(score), 
                        })
            if outputs != []:
                reply_valid = True
                break
        outputs_final = []
        for output in outputs:
            outputs_final.append({
                'answer': output['answer'],
                'mentions': int(output['mentions']),
                'score': int(output['score']),
                'grade': int(output['mentions']) * int(output['score']),
            })
        outputs_final = sorted(outputs_final, key=lambda x: x['grade'], reverse=True)
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs_final:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        if outputs_final != []:
            json_article[key] = outputs_final[:20]
            io.json_write(json_article_filepath, json_article)
        else:
            json_article[key] = 'FAILED'
            io.json_write(json_article_filepath, json_article)

def preparations_ai(json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    ###
    key = 'preparations'
    if key not in json_article: json_article[key] = []
    if regen: json_article[key] = []
    if clear: 
        json_article[key] = []
        io.json_write(json_article_filepath, json_article)
        return
    outputs = []
    if json_article[key] == []:
        preparations_names_plural = ['teas', 'decoctions', 'tinctures', 'essential olis', 'creams', 'syrups', 'juices', 'linctuses', 'mucillages', 'capsules', 'lozenges', 'baths', 'oinments', 'suppositories', 'liniments', 'gargles', 'oils', 'poultices']
        preparations_prompt = ', '.join(preparations_names_plural)
        preparations_prompt_json = [f'{{"answer": "{part}", "score": "write score here"}}' for part in preparations_names_plural]
        preparations_prompt_json = ',\n'.join(preparations_prompt_json)[:-1] + '\n'
        output_plants = []
        reply_valid = False
        for i in range(3):
            # rnd = random.randint(17, 23)
            prompt = f'''
                For each of the following herbal preparations of the {herb_name_scientific} plant, give me a confidence score from 1 to 10 indicating how much this preparation is used for medicinal purposes: {preparations_prompt}.
                Reply in the following JSON format: 
                [{preparations_prompt_json}]
                Only reply with the JSON, don't add additional info.
                Answer in as few words as possible.
                /no_think
            '''
            reply = llm_reply(prompt, model_path=model_filepath).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                objects = []
                for item in json_data:
                    try: answer = item['answer']
                    except: continue
                    try: score = item['score']
                    except: continue
                    answer = answer.split('(')[0].strip().lower()
                    preparation_found = False
                    preparation = ''
                    for _preparation in preparations_names_plural:
                        if _preparation.lower().strip() == answer.lower().strip():
                            preparation = _preparation
                            preparation_found = True
                            break
                    if preparation_found:
                        objects.append({
                            "answer": answer, 
                            "score": score,
                        })
                for obj in objects:
                    answer = obj['answer']
                    score = obj['score']
                    found = False
                    for output in outputs:
                        print(output)
                        print(answer, '->', output['answer'])
                        if answer in output['answer']: 
                            output['mentions'] += 1
                            output['score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'answer': answer, 
                            'mentions': 1, 
                            'score': int(score), 
                        })
            if outputs != []:
                reply_valid = True
                break
        outputs_final = []
        for output in outputs:
            outputs_final.append({
                'answer': output['answer'],
                'mentions': int(output['mentions']),
                'score': int(output['score']),
                'grade': int(output['mentions']) * int(output['score']),
            })
        outputs_final = sorted(outputs_final, key=lambda x: x['grade'], reverse=True)
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs_final:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        if outputs_final != []:
            json_article[key] = outputs_final[:20]
            io.json_write(json_article_filepath, json_article)
        else:
            json_article[key] = 'FAILED'
            io.json_write(json_article_filepath, json_article)

def side_effects_ai(json_article_filepath, regen=False, clear=False):
    json_article = io.json_read(json_article_filepath)
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    key = 'side_effects'
    if key not in json_article: json_article[key] = []
    if regen: json_article[key] = []
    if clear: 
        json_article[key] = []
        io.json_write(json_article_filepath, json_article)
        return
    outputs = []
    if json_article[key] == []:
        output_plants = []
        reply_valid = False
        for i in range(3):
            rnd = random.randint(17, 23)
            prompt = f'''
                List the {rnd} most common health side effects of the {herb_name_scientific} plant.
                Also, for each side effect give a confidence score from 1 to 10, indicating how sure you are that answer.
                Write each side effect in 3 words or less.
                Make the first word in each side effect a third-person singular action verb.
                Reply in the following JSON format: 
                [
                    {{"answer": "write side effect 1 here", "score": "10"}}, 
                    {{"answer": "write side effect 2 here", "score": "5"}}, 
                    {{"answer": "write side effect 3 here", "score": "7"}} 
                ]
                Only reply with the JSON, don't add additional info.
                /no_think
            '''
            reply = llm_reply(prompt, model_path=model_filepath).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                objects = []
                for item in json_data:
                    try: answer = item['answer']
                    except: continue
                    try: score = item['score']
                    except: continue
                    objects.append({
                        "answer": answer, 
                        "score": score,
                    })
                for obj in objects:
                    answer = obj['answer']
                    score = obj['score']
                    found = False
                    for output in outputs:
                        print(output)
                        print(answer, '->', output['answer'])
                        if answer in output['answer']: 
                            output['mentions'] += 1
                            output['score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'answer': answer, 
                            'mentions': 1, 
                            'score': int(score), 
                        })
            if outputs != []:
                reply_valid = True
                break
        outputs_final = []
        for output in outputs:
            outputs_final.append({
                'answer': output['answer'],
                'mentions': int(output['mentions']),
                'score': int(output['score']),
                'grade': int(output['mentions']) * int(output['score']),
            })
        outputs_final = sorted(outputs_final, key=lambda x: x['grade'], reverse=True)
        print('***********************')
        print('***********************')
        print('***********************')
        for output in outputs_final:
            print(output)
        print('***********************')
        print('***********************')
        print('***********************')
        if outputs_final != []:
            json_article[key] = outputs_final[:20]
            io.json_write(json_article_filepath, json_article)
        else:
            json_article[key] = 'FAILED'
            io.json_write(json_article_filepath, json_article)

def html_plant_medicine(url):
    json_article_filepath = f'{g.ENTITIES_FOLDERPATH}/{url}.json'
    html_article_filepath = f'{g.WEBSITE_FOLDERPATH}/{url}/benefits.html'
    print(f'    >> JSON: {json_article_filepath}')
    print(f'    >> HTML: {html_article_filepath}')
    json_article = io.json_read(json_article_filepath)
    print(json_article)
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    benefits = json_article['benefits']
    benefits_num = json_article['benefits_num']
    benefits_title = json_article['benefits_title']
    benefits_intro = json_article['benefits_intro']
    ###
    html_article = ''
    html_article += f'<h1>{benefits_title}</h1>\n'
    html_article += f'''
        <img style="margin-bottom: 16px;" 
        src="/images/herbs/{herb_slug}.jpg" 
        alt="{herb_name_scientific}">
    '''
    html_article += f'{utils.text_format_sentences_html(json_article["benefits_intro"])}\n'
    html_article += f'<p>Below there\'s a list of the {benefits_num} best health benefits of {herb_name_scientific}.</p>\n'
    html_article += f'[html_intro_toc]\n'
    for i, benefit in enumerate(benefits[:benefits_num]):
        benefit_answer = benefit['answer']
        benefit_description = benefit['description']
        html_article += f'<h2>{i+1}. {benefit_answer.capitalize()}</h2>\n'
        html_article += f'{utils.text_format_sentences_html(benefit_description)}\n'
    ###
    html_article, json_toc = components.toc(html_article)
    html_intro_toc = components.toc_json_to_html_article(json_toc)
    html_article = html_article.replace('[html_intro_toc]', html_intro_toc)
    html_toc_sidebar = components.toc_json_to_html_sidebar(json_toc)
    html_breadcrumbs = components.breadcrumbs(f'{url}/benefits.html')
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(benefits_title)}
        <body>
            {components.html_header()}
            <main style="margin-top: 24px;" class="container-md mob-flex gap-48">
                <article class="article">
                    {html_breadcrumbs}
                    {html_article}
                </article>
            </main>
            {components.html_footer()}
        </body>
        </html>
    '''
    html_article_folderpath = '/'.join(html_article_filepath.split('/')[:-1])
    if not os.path.exists(html_article_folderpath): os.mkdir(html_article_folderpath)
    with open(html_article_filepath, 'w') as f: f.write(html)
    print('here')
    print(html_article)

def gen():
    herbs = data.herbs_books_get()
    herbs = herbs[:]
    for herb_i, herb in enumerate(herbs):
        print(f'{herb_i}/{len(herbs)} - {herb}')
        herb_name_scientific = herb.strip().lower()
        herb_slug = utils.sluggify(herb_name_scientific)
        url_relative = f'herbs/{herb_slug}'
        ###
        json_article_filepath = f'{g.ENTITIES_FOLDERPATH}/{url_relative}.json'
        print(f'    >> JSON: {json_article_filepath}')
        ###
        json_article = io.json_read(json_article_filepath, create=True)
        json_article['url'] = url_relative
        json_article['herb_slug'] = herb_slug
        json_article['herb_name_scientific'] = herb_name_scientific
        if 'lastmod' not in json_article: json_article['lastmod'] = utils.today()
        lastmod = json_article['lastmod']
        if 'benefits_num' not in json_article: json_article['benefits_num'] = random.choice([7, 9, 11, 13])
        if 'constituents_num' not in json_article: json_article['constituents_num'] = random.choice([7, 9, 11, 13])
        if 'preparations_num' not in json_article: json_article['preparations_num'] = random.choice([7, 9, 11, 13])
        if 'side_effects_num' not in json_article: json_article['side_effects_num'] = random.choice([7, 9, 11, 13])
        io.json_write(json_article_filepath, json_article)
        ###
        medicine_poison_ai(json_article_filepath, regen=False, clear=False)
        if data.herb_medicine_poison_get(url_relative) == 'medicine':
            benefits_ai(json_article_filepath, regen=False, clear=False)
            constituents_ai(json_article_filepath, regen=False, clear=False)
            parts_ai(json_article_filepath, regen=False, clear=False)
            preparations_ai(json_article_filepath, regen=False, clear=False)
            side_effects_ai(json_article_filepath, regen=False, clear=False)
            pass

gen()
