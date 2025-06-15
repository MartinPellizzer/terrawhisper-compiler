import json
import random

import chromadb
from chromadb.utils import embedding_functions

from oliark_llm import llm_reply

vault_tmp = '/home/ubuntu/vault-tmp'
collection_name = 'medicinal-plants'

model_validator_filepath = f'{vault_tmp}/llms/Llama-3-Partonus-Lynx-8B-Intstruct-Q4_K_M.gguf'
model_filepath = '/home/ubuntu/vault-tmp/llms/Qwen3-8B-Q4_K_M.gguf'
model_filepath = '/home/ubuntu/vault-tmp/llms/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'

db_path = f'{vault_tmp}/terrawhisper/chroma'
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='all-mpnet-base-v2', 
    device='cuda',
)
chroma_client = chromadb.PersistentClient(path=db_path)

def retrieve_docs(query, n_results):
    collection = chroma_client.get_or_create_collection(
        name=collection_name, 
        embedding_function=sentence_transformer_ef,
    )
    results = collection.query(query_texts=[query], n_results=n_results)
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    return documents, metadatas

def llm_validate(question, context, answer):
    prompt = f'''
    Given the following QUESTION, DOCUMENT and ANSWER you must analyze the provided answer and determine whether it is faithful to the contents of the DOCUMENT. The ANSWER must not offer new information beyond the context provided in the DOCUMENT. The ANSWER also must not contradict information provided in the DOCUMENT. Output your final verdict by strictly following this format: "PASS" if the answer is faithful to the DOCUMENT and "FAIL" if the answer is not faithful to the DOCUMENT. Show your reasoning.

    --
    QUESTION (THIS DOES NOT COUNT AS BACKGROUND INFORMATION):
    {question}

    --
    DOCUMENT:
    {context}

    --
    ANSWER:
    {answer}

    --

    Your output should be in JSON FORMAT with the keys "REASONING" and "SCORE":
    {{"REASONING": <your reasoning as bullet points>, "SCORE": <your final score>}}
    '''
    reply = llm_reply(prompt, model_validator_filepath, max_tokens=1024)
    return reply

def gen_study_snippet(plant_name_scientific):
    n_results = 100
    query = f'{plant_name_scientific.capitalize()} benefits'
    documents, metadatas = retrieve_docs(query, n_results=n_results)
    # use llm to filter the chroma documents and give back the first 10 studies that fit the query
    n_filtered = 5
    documents_filtered = []
    metadatas_filtered = []
    for i in range(n_results):
        if len(documents_filtered) >= n_filtered: break
        document = documents[i]
        metadata = metadatas[i]
        prompt = f'''
            Does the DOCUMENT below mention about the health benefits of {plant_name_scientific}?
            Reply only with "YES" or "NO".
            DOCUMENT: {document}
            /no_think
        '''
        reply = llm_reply(prompt)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        if 'yes' in reply.lower():
            documents_filtered.append(document)
            metadatas_filtered.append(metadata)
    # gen llm replies
    replies = []
    for i in range(len(documents_filtered)):
        for _ in range(3):
            document = documents_filtered[i]
            metadata = metadatas_filtered[i]
            question = f'''
                Write 1 sentence about the health benefits of {plant_name_scientific.capitalize()} using the content in the scientific STUDY below.
            '''
            prompt = f'''
                {question}
                STUDY: {document}
                If you cannot answer for whatever reason, reply only with: 'I can't answer'.
                If you can answer, start with the following words: According to {metadata['journal_title']}, {plant_name_scientific.capitalize()} .
                /no_think
            '''
            reply = llm_reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            if reply.strip().startswith('I can\'t'): 
                continue
            elif reply.strip().startswith('I couldn\'t'): 
                continue
            elif reply.strip().startswith('cannot'): 
                continue
            validator_reply = llm_validate(question, document, reply)
            try: validator_obj = json.loads(validator_reply)
            except: continue
            score = validator_obj['SCORE']
            if score == 'PASS':
                print('pass')
                replies.append(reply)
                break
            elif score == 'FAIL':
                print('fail score')
                continue
            else: 
                print('bad something')
                continue
    if replies == []:
        replies.append('N/A')
    return replies[0]

def gen_plant_study_intro(plant_name_scientific):
    n_results = 100
    query = f'{plant_name_scientific.capitalize()}'
    documents, metadatas = retrieve_docs(query, n_results=n_results)
    # use llm to filter the chroma documents and give back the first 10 studies that fit the query
    n_filtered = 5
    documents_filtered = []
    metadatas_filtered = []
    for i in range(n_results):
        if len(documents_filtered) >= n_filtered: break
        document = documents[i]
        metadata = metadatas[i]
        prompt = f'''
            Does the DOCUMENT below mention {plant_name_scientific} for medicinal purposes?
            Reply only with "YES" or "NO".
            DOCUMENT: {document}
            /no_think
        '''
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        reply = llm_reply(prompt)
        if 'yes' in reply.lower():
            documents_filtered.append(document)
            metadatas_filtered.append(metadata)
    # gen llm replies
    replies = []
    for i in range(len(documents_filtered)):
        for _ in range(3):
            document = documents_filtered[i]
            metadata = metadatas_filtered[i]
            question = f'''
                Write 1 sentence about the medicinal purposes of {plant_name_scientific.capitalize()} using the content in the scientific STUDY below.
            '''
            prompt = f'''
                {question}
                STUDY: {document}
                If you cannot answer for whatever reason, reply only with: 'I can't answer'.
                If you can answer, start with the following words: According to {metadata['journal_title']}, {plant_name_scientific.capitalize()} .
                /no_think
            '''
            reply = llm_reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            if reply.strip().startswith('I can\'t'): 
                continue
            elif reply.strip().startswith('I couldn\'t'): 
                continue
            elif reply.strip().startswith('cannot'): 
                continue
            validator_reply = llm_validate(question, document, reply)
            try: validator_obj = json.loads(validator_reply)
            except: continue
            score = validator_obj['SCORE']
            if score == 'PASS':
                print('pass')
                replies.append(reply)
                break
            elif score == 'FAIL':
                print('fail score')
                continue
            else: 
                print('bad something')
                continue
    if replies == []:
        replies.append('N/A')
    return replies[0]

###########################################################################
# plants
###########################################################################
def gen_study_plant_intro(plant_name_scientific):
    n_results = 100
    query = f'{plant_name_scientific} benefits'
    documents, metadatas = retrieve_docs(query, n_results=n_results)
    # use llm to filter the chroma documents and give back the first 10 studies that fit the query
    n_filtered = 5
    documents_filtered = []
    metadatas_filtered = []
    for i in range(n_results):
        if len(documents_filtered) >= n_filtered: break
        document = documents[i]
        metadata = metadatas[i]
        document = ' '.join(document.split(' ')[:4000])
        prompt = f'''
            Does the DOCUMENT below talk about {plant_name_scientific} benefits in a positive way?' 
            Reply only with "YES" or "NO".
            DOCUMENT: {document}
            /no_think
        '''
        reply = llm_reply(prompt)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        if 'yes' in reply.lower():
            documents_filtered.append(document)
            metadatas_filtered.append(metadata)
    # gen llm replies
    replies = []
    for i in range(len(documents_filtered)):
        for _ in range(3):
            document = documents_filtered[i]
            metadata = metadatas_filtered[i]
            question = f'''
                Write 1 sentence about {plant_name_scientific} benefits using the content in the scientific STUDY below.
            '''
            prompt = f'''
                {question}
                STUDY: {document}
                If you cannot answer for whatever reason, reply only with: 'I can't answer'.
                If you can answer, start with the following words: According to "{metadata['journal_title']}", {plant_name_scientific} .
                /no_think
            '''
            reply = llm_reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            if reply.strip().startswith('I can\'t'): 
                continue
            elif reply.strip().startswith('I couldn\'t'): 
                continue
            elif reply.strip().startswith('cannot'): 
                continue
            query = f'Does the DOCUMENT below mainly talk about {plant_name_scientific} benefits in a positive way?'
            reply_double_check = reply_double_check_gen(reply, query)
            if 'yes' not in reply_double_check.lower():
                continue
            validator_reply = llm_validate(question, document, reply)
            try: validator_obj = json.loads(validator_reply)
            except: continue
            score = validator_obj['SCORE']
            if score == 'PASS':
                print('pass')
                replies.append(reply)
                break
            elif score == 'FAIL':
                print('fail score')
                continue
            else: 
                print('bad something')
                continue
    if replies == []:
        replies.append('N/A')
    return replies[0]

###########################################################################
# ailment - tea
###########################################################################
def reply_double_check_gen(reply, query):
    prompt = f'''
        {query}
        Reply only with "YES" or "NO".
        DOCUMENT: {reply}
        /no_think
    '''
    reply = llm_reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    return reply

def gen_study_ailment_tea_intro(preparation_name, ailment_name):
    n_results = 100
    query = f'{preparation_name} for {ailment_name}'
    documents, metadatas = retrieve_docs(query, n_results=n_results)
    # use llm to filter the chroma documents and give back the first 10 studies that fit the query
    n_filtered = 5
    documents_filtered = []
    metadatas_filtered = []
    for i in range(n_results):
        if len(documents_filtered) >= n_filtered: break
        document = documents[i]
        metadata = metadatas[i]
        prompt = f'''
            Does the DOCUMENT below talk about {preparation_name} for {ailment_name} in a positive way?
            Reply only with "YES" or "NO".
            DOCUMENT: {document}
            /no_think
        '''
        reply = llm_reply(prompt)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        if 'yes' in reply.lower():
            documents_filtered.append(document)
            metadatas_filtered.append(metadata)
    # gen llm replies
    replies = []
    for i in range(len(documents_filtered)):
        for _ in range(3):
            document = documents_filtered[i]
            metadata = metadatas_filtered[i]
            question = f'''
                Write 1 sentence about {preparation_name} for {ailment_name} using the content in the scientific STUDY below.
            '''
            prompt = f'''
                {question}
                STUDY: {document}
                If you cannot answer for whatever reason, reply only with: 'I can't answer'.
                If you can answer, start with the following words: According to "{metadata['journal_title']}", {preparation_name} for {ailment_name} .
                /no_think
            '''
            reply = llm_reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            if reply.strip().startswith('I can\'t'): 
                continue
            elif reply.strip().startswith('I couldn\'t'): 
                continue
            elif reply.strip().startswith('cannot'): 
                continue
            query = f'Does the DOCUMENT below mainly talk about {preparation_name} for {ailment_name} in a positive way?'
            reply_double_check = reply_double_check_gen(reply, query)
            if 'yes' not in reply_double_check.lower(): continue
            validator_reply = llm_validate(question, document, reply)
            try: validator_obj = json.loads(validator_reply)
            except: continue
            score = validator_obj['SCORE']
            if score == 'PASS':
                print('pass')
                replies.append(reply)
                break
            elif score == 'FAIL':
                print('fail score')
                continue
            else: 
                print('bad something')
                continue
    if replies == []:
        replies.append('N/A')
    return replies[0]

def gen_study_ailment_tea_list(plant_name_scientific, preparation_name, ailment_name):
    n_results = 100
    query = f'{plant_name_scientific.capitalize()} {preparation_name} for {ailment_name}'
    query = f'{plant_name_scientific.capitalize()} for {ailment_name}'
    documents, metadatas = retrieve_docs(query, n_results=n_results)
    # use llm to filter the chroma documents and give back the first 10 studies that fit the query
    n_filtered = 5
    documents_filtered = []
    metadatas_filtered = []
    for i in range(n_results):
        if len(documents_filtered) >= n_filtered: break
        document = documents[i]
        metadata = metadatas[i]
        prompt = f'''
            Does the DOCUMENT below talk about {plant_name_scientific} {preparation_name} for {ailment_name} in a positive way?
            Reply only with "YES" or "NO".
            DOCUMENT: {document}
            /no_think
        '''
        reply = llm_reply(prompt)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        if 'yes' in reply.lower():
            documents_filtered.append(document)
            metadatas_filtered.append(metadata)
    # gen llm replies
    replies = []
    for i in range(len(documents_filtered)):
        for _ in range(3):
            document = documents_filtered[i]
            metadata = metadatas_filtered[i]
            question = f'''
                Write 1 sentence about the {plant_name_scientific.capitalize()} {preparation_name} for {ailment_name} using the content in the scientific STUDY below.
            '''
            prompt = f'''
                {question}
                STUDY: {document}
                If you cannot answer for whatever reason, reply only with: 'I can't answer'.
                If you can answer, start with the following words: According to "{metadata['journal_title']}", {plant_name_scientific.capitalize()} {preparation_name} for {ailment_name} .
                /no_think
            '''
            reply = llm_reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            if reply.strip().startswith('I can\'t'): 
                continue
            elif reply.strip().startswith('I couldn\'t'): 
                continue
            elif reply.strip().startswith('cannot'): 
                continue
            elif not reply.strip().startswith('According to '): 
                continue
            query = f'Does the DOCUMENT below mainly talk about {plant_name_scientific.capitalize()} {preparation_name} for {ailment_name} in a positive way?'
            reply_double_check = reply_double_check_gen(reply, query)
            if 'yes' not in reply_double_check.lower():
                print('#############################################################################')
                print('double check fail')
                print('#############################################################################')
                continue
            validator_reply = llm_validate(question, document, reply)
            try: validator_obj = json.loads(validator_reply)
            except: continue
            score = validator_obj['SCORE']
            if score == 'PASS':
                print('pass')
                replies.append(reply)
                break
            elif score == 'FAIL':
                print('fail score')
                continue
            else: 
                print('bad something')
                continue
    if replies == []:
        replies.append('N/A')
    return replies[0]

def study_plant_intro_ai(herb_name_scientific):
    n_results = 100
    query = f'{herb_name_scientific.capitalize()}'
    documents, metadatas = retrieve_docs(query, n_results=n_results)
    # use llm to filter the chroma documents and give back the first N ones
    n_filtered = 5
    documents_filtered = []
    metadatas_filtered = []
    for i in range(n_results):
        if len(documents_filtered) >= n_filtered: break
        document = documents[i]
        metadata = metadatas[i]
        document = ' '.join(document.split()[:4000])
        prompt = f'''
            Does the DOCUMENT below talk about {herb_name_scientific} benefits in a positive way?
            Reply only with "YES" or "NO".
            DOCUMENT: {document}
            /no_think
        '''
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        if 'yes' in reply.lower():
            documents_filtered.append(document)
            metadatas_filtered.append(metadata)
    # gen llm replies
    replies = []
    for i in range(len(documents_filtered)):
        for _ in range(3):
            document = documents_filtered[i]
            metadata = metadatas_filtered[i]
            question = f'''
                Write 1 sentence about the {herb_name_scientific.capitalize()} benefits using the content in the scientific STUDY below.
            '''
            prompt = f'''
                {question}
                STUDY: {document}
                If you cannot answer for whatever reason, reply only with: 'I can't answer'.
                If you can answer, start with the following words: According to "{metadata['journal_title']}", {herb_name_scientific.capitalize()} .
                /no_think
            '''
            reply = llm_reply(prompt, model_path=model_filepath).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            if reply.strip().startswith('I can\'t'): continue
            elif reply.strip().startswith('I couldn\'t'): continue
            elif reply.strip().startswith('cannot'): continue
            elif not reply.strip().startswith('According to '): continue
            query = f'Does the DOCUMENT below mainly talk about {herb_name_scientific.capitalize()} benefits in a positive way?'
            reply_double_check = reply_double_check_gen(reply, query)
            if 'yes' not in reply_double_check.lower():
                print('#############################################################################')
                print('double check fail')
                print('#############################################################################')
                continue
            document = f'{document} Source: {metadata["journal_title"]}'
            validator_reply = llm_validate(question, document, reply)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            try: validator_obj = json.loads(validator_reply)
            except: continue
            score = validator_obj['SCORE']
            if score == 'PASS':
                print('pass')
                replies.append(reply)
                break
            elif score == 'FAIL':
                print('fail score')
                continue
            else: 
                print('bad something')
                continue
    if replies == []:
        replies.append('[N/A]')
    return replies[0]

def ai_study_plant_benefit(herb_name_scientific, benefit):
    n_results = 100
    query = f'{herb_name_scientific.capitalize()} {benefit}'
    documents, metadatas = retrieve_docs(query, n_results=n_results)
    # use llm to filter the chroma documents and give back the first N ones
    n_filtered = 5
    documents_filtered = []
    metadatas_filtered = []
    for i in range(n_results):
        if len(documents_filtered) >= n_filtered: break
        document = documents[i]
        metadata = metadatas[i]
        document = ' '.join(document.split()[:4000])
        prompt = f'''
            Does the DOCUMENT below talk about the fact that {query} in a positive way?
            Reply only with "YES" or "NO".
            DOCUMENT: {document}
            /no_think
        '''
        reply = llm_reply(prompt, model_path=model_filepath).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        if 'yes' in reply.lower():
            documents_filtered.append(document)
            metadatas_filtered.append(metadata)
    # gen llm replies
    replies = []
    for i in range(len(documents_filtered)):
        for _ in range(3):
            document = documents_filtered[i]
            metadata = metadatas_filtered[i]
            question = f'''
                Write 1 sentence about the fact that {query} using the content in the scientific STUDY below.
            '''
            prompt = f'''
                {question}
                STUDY: {document}
                If you cannot answer for whatever reason, reply only with: 'I can't answer'.
                If you can answer, start with the following words: According to "{metadata['journal_title']}", {herb_name_scientific.capitalize()} .
                /no_think
            '''
            reply = llm_reply(prompt, model_path=model_filepath).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            if reply.strip().startswith('I can\'t'): continue
            elif reply.strip().startswith('I couldn\'t'): continue
            elif reply.strip().startswith('cannot'): continue
            elif not reply.strip().startswith('According to '): continue
            query = f'Does the DOCUMENT below mainly talk about the fact that {query.capitalize()} in a positive way?'
            reply_double_check = reply_double_check_gen(reply, query)
            if 'yes' not in reply_double_check.lower():
                print('#############################################################################')
                print('double check fail')
                print('#############################################################################')
                continue
            document = f'{document} Source: {metadata["journal_title"]}'
            validator_reply = llm_validate(question, document, reply)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            try: validator_obj = json.loads(validator_reply)
            except: continue
            score = validator_obj['SCORE']
            if score == 'PASS':
                print('pass')
                replies.append(reply)
                break
            elif score == 'FAIL':
                print('fail score')
                continue
            else: 
                print('bad something')
                continue
    if replies == []:
        replies.append('N/A')
    return replies[0]

