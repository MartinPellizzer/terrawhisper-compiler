import os
import time

from Bio import Entrez

import util
import util_data
import data_csv

vault = '/home/ubuntu/vault'

status_rows, status_cols = data_csv.status()
systems_rows, systems_cols = data_csv.systems()
status_preparations_rows, status_preparations_cols = data_csv.status_preparations()

Entrez.email = 'leenrandell@gmail.com'
sort_by = 'relevance'
proj = 'terrawhisper'
pubmed_folderpath = f'{vault}/{proj}/studies/pubmed'

def create_folder(folderpath):
    chunk_curr = ''
    for chunk in folderpath.split('/'):
        chunk_curr += f'{chunk}/'
        try: os.makedirs(chunk_curr)
        except: continue
create_folder(pubmed_folderpath)

def get_ids(query, year=None, retmax=50):
    if year:
        handle = Entrez.esearch(db='pubmed', term=query, retmax=retmax, sort=sort_by, datetype='edat', mindate=year, maxdate=year)
    else:
        handle = Entrez.esearch(db='pubmed', term=query, retmax=retmax, sort=sort_by)
    record = Entrez.read(handle)
    handle.close()
    return record['IdList']

def fetch_details(pmid):
    handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')
    records = Entrez.read(handle)
    handle.close()
    return records

def scrape_pubmed(query, year=None):
    query_slug = query.strip().lower().replace(' ', '-')
    pmid_list = get_ids(query, year)
    citation_arr = []
    abstract_arr = []
    if pmid_list:
        create_folder(f'{pubmed_folderpath}/{query_slug}')
        for pmid_i, pmid in enumerate(pmid_list):
            print(f'{pmid_i}/{len(pmid_list)}')
            pmid_csv = util.csv_get_rows_by_entity(f'{vault}/ozonogroup/studies/pubmed/master.csv', pmid, col_num=0)
            if pmid_csv != []: continue
            abstract_text = ''
            title = ''
            authors = ''
            authors_str = ''
            journal_title = ''
            journal_volume = ''
            journal_issue = ''
            pub_date = ''
            pub_year = ''
            pub_month = ''
            pub_day = ''
            pages = ''
            details = fetch_details(pmid)
            try:
                abstract_text = details['PubmedArticle'][0]['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
            except:
                continue
            article = details['PubmedArticle'][0]['MedlineCitation']['Article']
            journal = article['Journal']
            pubmed_data = details['PubmedArticle'][0]['PubmedData']
            title = article.get('ArticleTitle', 'No title available')
            try:
                authors = article['AuthorList']
            except: pass
            try:
                author_str = ', '.join([f"{a['LastName']} {a['ForeName'][0]}" for a in authors])
            except: pass
            try:
                journal_title = journal.get('Title', 'No journal title available')
            except: pass
            try:
                journal_volume = journal['JournalIssue'].get('Volume', 'No volume')
            except: pass
            try:
                journal_issue = journal['JournalIssue'].get('Issue', 'No issue')
            except: pass
            try:
                pub_date = article.get('ArticleDate', [{'Year': 'No year', 'Month': 'No month', 'Day': 'No day'}])[0]
            except: pass
            try:
                pub_year = pub_date['Year']
            except: pass
            try:
                pub_month = pub_date['Month']
            except: pass
            try:
                pub_day = pub_date['Day']
            except: pass
            try:
                pages = article['Pagination'].get('StartPage', 'No pages')
            except: pass
            try:
                citation = f'{author_str}. {title}. {journal_title}. {pub_year}. {pub_month}. {pub_day};{journal_volume}({journal_issue}):{pages}. PMID: {pmid}.'
            except:
                citation = f'{title}. {journal_title}. PMID: {pmid}.'
            citation_arr.append(citation)
            abstract_arr.append(abstract_text)
            print(citation)
            print(abstract_text)
            print()
            print()
            print()
            create_folder(f'{pubmed_folderpath}/{query_slug}/{pmid}')
            with open(f'{pubmed_folderpath}/{query_slug}/{pmid}/abstract.txt', 'w') as f: f.write(abstract_text)
            row = [
                pmid,
                pub_year,
                pub_month,
                pub_day,
                journal_title,
                journal_volume,
                journal_issue,
                pages,
                title,
                author_str
            ]
            util.csv_add_rows(f'{pubmed_folderpath}/{query_slug}/ids.csv', [row])
            time.sleep(1)
    else:
        print('no article found')
    print(f'number of abstracts: {len(abstract_arr)}')
    print(f'number of citations: {len(citation_arr)}')
    abstracts_text = '\n\n'.join(abstract_arr)

preparation_name_sin = 'tea'
for status_row in status_rows:
    status_exe = status_row[status_cols['status_exe']]
    status_id = status_row[status_cols['status_id']]
    status_slug = status_row[status_cols['status_slug']]
    status_name = status_row[status_cols['status_names']].split(',')[0].strip()
    if status_exe == '': continue
    if status_id == '': continue
    if status_slug == '': continue
    if status_name == '': continue
    print(f'>> {status_id} - {status_name}')
    system_row = util_data.get_system_by_status(status_id)
    system_id = system_row[systems_cols['system_id']]
    system_slug = system_row[systems_cols['system_slug']]
    system_name = system_row[systems_cols['system_name']]
    if system_id == '': continue
    if system_slug == '': continue
    if system_name == '': continue
    print(f'    {system_id} - {system_name}')
    found = False
    for status_preparation_row in status_preparations_rows:
        j_status_id = status_preparation_row[status_preparations_cols['status_id']] 
        j_preparation_name = status_preparation_row[status_preparations_cols['preparation_name']] 
        if status_id.strip().lower() == j_status_id.strip().lower():
            if j_preparation_name.strip().lower().startswith(preparation_name_sin):
                found = True
                break
    if found:
        query = f'{preparation_name_sin} {status_name}'
        scrape_pubmed(query)
        quit()
    
