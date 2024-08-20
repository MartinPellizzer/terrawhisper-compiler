import chromadb
from chromadb.utils import embedding_functions

from oliark_llm import llm_reply

vault_path = '/home/ubuntu/vault'
llms_path = f'{vault_path}/llms'
model = f'{llms_path}/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'

PROJ_NAME = 'terrawhisper'
QUERY = 'medicinal-plants'
DB_PATH = f'{PROJ_NAME}-db'
DB_COLLECTION_NAME = QUERY

device = 'cuda'
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='all-mpnet-base-v2', 
    device=device,
)

chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name=DB_COLLECTION_NAME, embedding_function=sentence_transformer_ef)

run = True
while run:
    run = False
    query = 'herbal teas for cough'
    # query = input('>>> ')
    print('***********************')
    print(query)
    print('***********************')

    results = collection.query(query_texts=[query], n_results=5)
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    
    abstracts = []
    for i, document in enumerate(documents):
        document_formatted = f'PARAGRAPH {i+1}: {document}'
        abstracts.append(document_formatted)
        print(document_formatted)
        print()

    prompt = f'''
        From the 5 paragraphs below, pick the one that best proves that herbal teas are good for cough, and that includes the most amount of data, information, details, results and numbers to prove it.
        Reply with the number of the paragraph you select and explain step by step why you selected it.
        If you don't find a good candidate, reply with "0".

        Format the reply as follow: 
        number_selected_paragraph
        step_by_step_explanation

        Below are the 5 paragraphs.
        {abstracts}
    '''
    reply = llm_reply(prompt, model)
    print('***********************')
    print(reply)
    print('***********************')

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
        document = documents[paragraph_num]
        metadata = metadatas[paragraph_num]
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
        reply = llm_reply(prompt, model)
        
