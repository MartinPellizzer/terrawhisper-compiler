import os
import time
import random
import datetime
import shutil

from Bio import Entrez

from oliark import json_write

proj = 'terrawhisper'
query = f'cough'.strip().lower()
query_slug = query.replace(' ', '-')

vault = '/home/ubuntu/vault'
pubmed_folderpath = f'{vault}/{proj}/studies/pubmed'
query_folderpath = f'{pubmed_folderpath}/{query_slug}'

Entrez.email = 'martinpellizzer@gmail.com'
# sort_by = 'pub_date'
sort_by = 'relevance'
datetypes = ['mdat', 'pdat', 'edat']
datetype = datetypes[2]
years = [year for year in range(2024, 1785, -1)]
yesterday = datetime.datetime.now() - datetime.timedelta(1)
yesterday = datetime.datetime.strftime(yesterday, '%Y/%m/%d')

actions_num_total = 0

def create_folder(folderpath):
    chunk_curr = ''
    for chunk in folderpath.split('/'):
        chunk_curr += f'{chunk}/'
        try: os.makedirs(chunk_curr)
        except: continue

def get_ids(query, year=None, date=None, retmax=50):
    if date:
        handle = Entrez.esearch(db='pubmed', term=query, retmax=retmax, sort=sort_by, datetype=datetype, mindate=date, maxdate=date)
    elif year:
        handle = Entrez.esearch(db='pubmed', term=query, retmax=retmax, sort=sort_by, datetype=datetype, mindate=year, maxdate=year)
    else:
        handle = Entrez.esearch(db='pubmed', term=query, retmax=retmax, sort=sort_by)
    record = Entrez.read(handle)
    handle.close()
    return record['IdList']

def fetch_details(pmid):
    handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')
    try: records = Entrez.read(handle)
    except: 
        handle.close()
        return None
    handle.close()
    return records

def scrape_pubmed_jsons(query, year=None, date=None):
    global actions_num_total
    query_slug = query.strip().lower().replace(' ', '-')
    if year:
        pmid_list = get_ids(query, year=year, retmax=9999)
        print(f'{year}')
    else:
        pmid_list = get_ids(query, date=date, retmax=9999)
        print(f'{date}')
    if pmid_list:
        create_folder(f'{query_folderpath}/json')
        for pmid_i, pmid in enumerate(pmid_list):
            done_pmids = []
            for filename in os.listdir(f'{query_folderpath}/json'):
                done_pmid = filename.split('.')[0]
                done_pmids.append(done_pmid)
            print(f'{pmid_i}/{len(pmid_list)} - {date}')
            if pmid in done_pmids: continue
            try: details = fetch_details(pmid)
            except: continue
            json_write(f'{query_folderpath}/json/{pmid}.json', details)
            time.sleep(random.randint(2, 5))
            actions_num_total += 1
            if actions_num_total >= 1000:
                actions_num_total = 0
                time.sleep(random.randint(450, 750))
    else:
        print('no article found')
    time.sleep(random.randint(2, 5))

for year in years:
    for i in range(1, 12):
        month = i
        if month < 10: month = f'0{month}' 
        date = f'{year}/{month}'
        scrape_pubmed_jsons(query, year, f'{year}/{month}')
    
