import os

import chromadb
from chromadb.utils import embedding_functions

from oliark import json_read

# device = 'cpu'
device = 'cuda'

PROJ_NAME = 'terrawhisper'
QUERY = 'medicinal-plants'
DB_PATH = f'{PROJ_NAME}-db'
DB_COLLECTION_NAME = QUERY

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name='all-mpnet-base-v2', 
    device=device,
)

chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name=DB_COLLECTION_NAME, embedding_function=sentence_transformer_ef)

def embed_abstracts():
    documents_folderpath = f'/home/ubuntu/vault/{PROJ_NAME}/studies/pubmed/{QUERY}/json'
    documents_filenames = os.listdir(documents_folderpath)
    for i, document_filename in enumerate(documents_filenames):
        print(f'{i}/{len(documents_filenames)}')
        document_filepath = f'{documents_folderpath}/{document_filename}'
        try: data = json_read(document_filepath)
        except: continue
        try: article = data['PubmedArticle'][0]['MedlineCitation']['Article']
        except: continue
        try: abstract_text = article['Abstract']['AbstractText']
        except: continue
        try: journal_title = article['Journal']['Title']
        except: continue
        abstract_text = ' '.join(abstract_text).replace('  ', ' ')
        pmid = document_filename.split('.')[0]
        metadata = {
            'pmid': pmid,
            'journal_title': journal_title,
        }

        collection.add(
            documents=[abstract_text],
            metadatas=[metadata],
            ids=[pmid],
        )

embed_abstracts()

results = collection.query(query_texts=['test'], n_results=5)
print(results)
documents = results['documents'][0]
