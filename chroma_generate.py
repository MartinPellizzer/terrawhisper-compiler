import sys

import chromadb
from chromadb.utils import embedding_functions

from oliark_llm import llm_reply

vault = '/home/ubuntu/vault'
llms_path = f'{vault}/llms'
model = f'{llms_path}/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'

proj_name = 'terrawhisper'
db_path = f'{vault}/{proj_name}/database/{proj_name}'

device = 'cuda'
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='all-mpnet-base-v2', 
    device=device,
)

chroma_client = chromadb.PersistentClient(path=db_path)

collection_name = sys.argv[1]
query = sys.argv[2]

print('***********************')
print(query)
print('***********************')

collection = chroma_client.get_or_create_collection(name=collection_name, embedding_function=sentence_transformer_ef)

results = collection.query(query_texts=[query], n_results=10)
documents = results['documents'][0]
metadatas = results['metadatas'][0]

abstracts = []
for i, document in enumerate(documents):
    # document_formatted = f'PARAGRAPH {i+1}: {document}'
    document_formatted = f'SOURCE \"{metadatas[i]["journal_title"]}\": {document}'
    abstracts.append(document_formatted)
    print(document_formatted)
    print()

prompt = f'''
    From the 5 paragraphs below, pick the one that best answer with the most amount of data, information, details, results and numbers the following question: {query}.
    Reply with only the number of the paragraph you select, don't add additional content.
    If you don't find a good candidate, reply with "0".

    Format the reply as follow: 
    number_selected_paragraph

    Below are the 5 paragraphs.
    {abstracts}
'''
prompt = f'''
    Reply to the following QUESTION using the following DOCUMENTS as context:
    Reply in 1 detailed sentence.
    Cite the source of the document you used to answer by ending the reply with the following words: ", according to the ".
    QUESTION: {query}
    DOCUMENTS:
    {abstracts}
'''
reply = llm_reply(prompt, model)
print('***********************')
print(reply)
print('***********************')

quit()
paragraph_num = 0
for line in reply.split('\n'):
    line = line.strip()
    if line == '': continue
    if line[0].isdigit():
        if line[0] == 0:
            break
        else:
            paragraph_num = int(line.split(' ')[0])
            break

print(paragraph_num)
if paragraph_num == 0:
    print('not valid paragraph')
else:
    document = documents[paragraph_num-1]
    metadata = metadatas[paragraph_num-1]
    print(document)
    print()

    prompt = f'''
        Explain why herbal teas are good for cough using the information and data provided by the study below. 
        Reply with a short paragraph of 3 sentences.
        In sentence 1, write an introduction, which starts with the following words: "For example, according to a study published by <em>{metadata}<em>, ".
        In sentence 2, write the methods.
        In sentence 3, write the results.
        Below is the study.
        {document}
    '''
    prompt = f'''
        Reply to the following QUESTION using the information and data provided by the CONTEXT below. 
        Use only the data from the study to reply, don't make up an answer.
        If you are confident about the reply, start the reply with the following text: "According to a study published by {metadata['journal_title']}, there are ".
        If you are not 100% confident you can answer with the context below, reply with "NA", don't make up an answer.
        QUESTION: {query}
        CONTEXT: {document}
    '''
    reply = llm_reply(prompt, model)
    print('***********************')
    print(reply)
    print('***********************')
    
