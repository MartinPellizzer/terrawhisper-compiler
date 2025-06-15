from oliark_llm import llm_reply

if 0:
    with open('market/keep-it-real-mode.txt') as f: keep_it_real_mode = f.read()

    prompt = f'''
        write me an email to sell a herbal tincture to my newsletter.
        {keep_it_real_mode}
    '''
    reply = llm_reply(prompt).strip()

campaign = 'terrawhisper'
campaign_folderpath = f'market/content'
try: os.mkdir(campaign_folderpath)
except: pass

def ailments_seasonal_list():
    json_output_filepath = f'{campaign_folderpath}/ailments-seasonal-list.json'
    prompt = f'''
        Write a list of the most common seasonal ailments for each month of the year. 
        Write 4 ailments per month.
        Don't repeat illnesses between months, write an illness only once.
        Write only illnesses experienced by a mass audence each year.
        Write only illnesses that can be relieved with medicinal herbs.
        Reply in the following JSON format: 
        [
            {{"month": "write month name 1 here", "illnesses": "[illness 1, illness 2, illness 3, illness 4]"}}, 
            {{"month": "write month name 2 here", "illnesses": "[illness 1, illness 2, illness 3, illness 4]"}}, 
            {{"month": "write month name 3 here", "illnesses": "[illness 1, illness 2, illness 3, illness 4]"}} 
        ]
        Only reply with the JSON, don't add additional info.
        Make sure you end the JSON with the character "]".
    '''
    print(prompt)
    reply = llm_reply(prompt).strip()
    json_data = {}
    try: json_data = json.loads(reply)
    except: pass 
    if json_data != {}:
        lst = []
        for item in json_data:
            try: month = item['month']
            except: continue
            try: illnesses = item['illnesses']
            except: continue
            lst.append({
                'month': month,
                'illnesses': illnesses,
            })
    json_output = {}
    json_output['data'] = lst
    io.json_write(json_output_filepath, json_output)

ailments_seasonal_list()
