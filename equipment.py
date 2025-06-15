import json
from oliark_io import csv_read_rows_to_json
from oliark_io import json_read, json_write
from oliark_llm import llm_reply

model_8b = f'/home/ubuntu/vault-tmp/llms/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf'
model_validator_filepath = f'llms/Llama-3-Partonus-Lynx-8B-Instruct-Q4_K_M.gguf'
model = model_8b

AUTHOR_NAME = 'Martin Pellizzer'

def head_html_generate(title, css_filepath):
    head_html = f'''
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="author" content="{AUTHOR_NAME}">
            <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
            <link rel="stylesheet" href="{css_filepath}">
            <title>{title}</title>
        </head>
    '''
    return head_html

def gen_article(product_slug):
    assets_folderpath = f'equipments/assets'
    jsons_folderpath = f'equipments/jsons'

    jars_assets_folderpath = f'{assets_folderpath}/{product_slug}'
    jars_json_filepath = f'{jsons_folderpath}/{product_slug}.json'

    website_folderpath = 'website-2'
    html_filepath = f'{website_folderpath}/equipments/jars-list.html'

    #####################################################
    # JSON
    #####################################################

    with open(f'{jars_assets_folderpath}/_urls.txt') as f: 
        urls = [x.strip() for x in f.read().strip().split('\n') if x.strip() != '']

    data = json_read(jars_json_filepath, create=True)
    data['product_type'] = 'jars'
    data['title'] = f'product_slug'
    json_write(jars_json_filepath, data)

    # ;json products
    for i, url in enumerate(urls):
        print(url)
        _id = url.split('/')[-1] # amazon asin
        _title_short = url.split('/')[-3] # amazon title short
        
        # init products list
        key = 'products'
        if key not in data: data[key] = []
        found = False
        for obj in data[key]:
            if obj['product_id'] == _id:
                found = True
                break
        if not found:
            product = {'product_id': _id}
            data[key].append(product)
        json_write(jars_json_filepath, data)
        
        # update products data
        key = 'products'
        if key not in data: data[key] = []
        for obj in data[key]:
            if obj['product_id'] == _id:
                obj['product_title_short'] = _title_short

                # ;pros
                if 'product_pros' not in obj: obj['product_pros'] = []
                # if 'product_pros' in obj: obj['product_pros'] = []
                if obj['product_pros'] == []:
                    with open(f'{jars_assets_folderpath}/{_id}-reviews-5star.txt') as f: positive_reviews_text = f.read()
                    outputs = []
                    prompt = f'''
                        Extract a list of the most mentioned and recurring key features from the following CUSTOMERS REVIEWS.
                        Also, follow the GUIDELINES below.
                        CUSTOMERS REVIEWS:
                        {positive_reviews_text}
                        GUIDELINES:
                        Write the features in 7-10 words.
                        Reply in the following JSON format: 
                        [
                            {{"feature": "write feature 1 here"}}, 
                            {{"feature": "write feature 2 here"}}, 
                            {{"feature": "write feature 3 here"}}, 
                            {{"feature": "write feature 4 here"}}, 
                            {{"feature": "write feature 5 here"}} 
                        ]
                        Only reply with the JSON.
                    '''
                    reply = llm_reply(prompt, model).strip()
                    # json_data = json.loads(reply)
                    try: json_data = json.loads(reply)
                    except: json_data = {}
                    if json_data != {}:
                        for item in json_data:
                            try: line = item['feature']
                            except: continue
                            outputs.append(line)
                    obj['product_pros'] = outputs
                    json_write(jars_json_filepath, data)

                # ;cons
                if 'product_cons' not in obj: obj['product_cons'] = []
                # if 'product_cons' in obj: obj['product_cons'] = []
                if obj['product_cons'] == []:
                    with open(f'{jars_assets_folderpath}/{_id}-reviews-1star.txt') as f: negative_reviews_text = f.read()
                    outputs = []
                    if negative_reviews_text.strip() != '':
                        prompt = f'''
                            Extract a list of the most mentioned and recurring complaints from the following CUSTOMERS REVIEWS.
                            Also, follow the GUIDELINES below.
                            CUSTOMERS REVIEWS:
                            {negative_reviews_text}
                            GUIDELINES:
                            Write the features in 7-10 words.
                            Reply in the following JSON format: 
                            [
                                {{"complaint": "write complaint 1 here"}}, 
                                {{"complaint": "write complaint 2 here"}}, 
                                {{"complaint": "write complaint 3 here"}}, 
                                {{"complaint": "write complaint 4 here"}}, 
                                {{"complaint": "write complaint 5 here"}} 
                            ]
                            Only reply with the JSON.
                        '''
                        reply = llm_reply(prompt, model).strip()
                        try: json_data = json.loads(reply)
                        except: json_data = {}
                        if json_data != {}:
                            for item in json_data:
                                try: line = item['complaint']
                                except: continue
                                outputs.append(line)
                    obj['product_cons'] = outputs
                    json_write(jars_json_filepath, data)

                # ;description
                if 'product_desc' not in obj: obj['product_desc'] = ''
                # if 'product_desc' in obj: obj['product_desc'] = ''
                if obj['product_desc'] == '':
                    pros = '\n'.join(obj['product_pros'])
                    cons = '\n'.join(obj['product_cons'])
                    prompt = f'''
                        Write a short 5-sentence paragraph about the following product: jars.
                        The target audience for this product is: herbalists.
                        Use the following PROS and CONS to describe the features, and use the GUIDELINES below.
                        PROS:
                        {pros}
                        CONS:
                        {cons}
                        GUIDELIES:
                        Try to include 1-2 CONS.
                        Reply in paragraph format.
                        Don't write conclusory statements, like sentences that starts with "overall", "in conclusion", "to summarize", etc...
                        Start writing the features from the first sentence.
                        Start with the following words: These jars .
                    '''
                    reply = llm_reply(prompt)
                    obj['product_desc'] = reply
                    json_write(jars_json_filepath, data)

                break

        article_html = ''
        article_html = f'<h1>Best Jars</h1>'

        head_html = head_html_generate(data['title'], '/style.css')

        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {article_html}
            </body>
            </html>
        '''
        with open(html_filepath, 'w') as f: f.write(html)
        
    quit()




    with open(f'{assets_jars_folderpath}/prod-0000-description.txt') as f: description_text = f.read()

    ################################################################################
    # CONTENT
    ################################################################################
        #If there are CONS that contradict the PROS, prioritize the PROS.
        #This product is being used by herbalists, so adapt the data below to an audience of berbalists and write only things that would interest them.
    prompt = f'''
        Write a 5-sentence paragraph about the following product: jars.
        The target audience for this product is: herbalists.
        Use the following PROS and CONS to describe the features, and use the GUIDELINES below.
        PROS:
        {pros}
        CONS:
        {cons}
        GUIDELIES:
        Try to include 1-2 CONS.
        Reply in paragraph format.
        Don't write conclusory statements, like sentences that starts with "overall", "in conclusion", "to summarize", etc...
        Start writing the features from the first sentence.
        Start with the following words: These jars .
    '''
    reply = llm_reply(prompt)
    cons = reply
    quit()


    ################################################################################
    # CONTRADICTIONS
    ################################################################################
    prompt = f'''
        I'm going to give you 2 lists: of PROS and CONS.
        Give me a list of contradictions between the PROS and CONS.
        PROS:
        {pros}
        CONS:
        {cons}
    '''
    reply = llm_reply(prompt)
    contradictions = reply

    ################################################################################
    # CONS (FILTERED)
    ################################################################################
    prompt = f'''
        List the things mentioned in the following CONTENT that are not stated in the following LIST:
        LIST:
        {contradictions}
        CONTENT:
        {negative_reviews_text}
    '''
    reply = llm_reply(prompt)
    print(prompt)

    quit()

    ################################################################################
    # CONTRADICTIONS
    ################################################################################
    prompt = f'''
        Here are 3 pieces of content about a product. 
        CONTENT 1 is what the brand of the product says about the product.
        CONTENT 2 is what happy customers say about the product.
        CONTENT 3 is what unsatisfied customers say about the product.
        I want you to list the contradictions between these pieces of contant.
        Here are the pieces of content.
        CONTENT 1:
        {description_text}
        CONTENT 2:
        {positive_reviews_text}
        CONTENT 3:
        {negative_reviews_text}
    '''
    prompt = f'''
        Here are 2 pieces of content about a product. 
        CONTENT 1 is what happy customers say about the product.
        CONTENT 2 is what unsatisfied customers say about the product.
        I want you to list the contradictions between these pieces of contant.
        Here are the pieces of content.
        CONTENT 1:
        {positive_reviews_text}
        CONTENT 2:
        {negative_reviews_text}
    '''
    prompt = f'''
        Here are 2 pieces of content about a product. 
        CONTENT 1 is what happy customers say about the product.
        CONTENT 2 is what unsatisfied customers say about the product.
        I want you to list all the negative things that are being said in content 2 that don't go against the things said in content 1.
        Here are the pieces of content.
        CONTENT 1:
        {positive_reviews_text}
        CONTENT 2:
        {negative_reviews_text}
    '''
    reply = llm_reply(prompt)
    quit()

    ################################################################################
    # PROS
    ################################################################################
    prompt = f'''
        Extract the 10 most important and recurring pros (positive things) from the AMAZON REVIEWS listed below about the mentioned product.
        Reply in list format.
        Reply only with the list.
        Give me pros that are specific, not general stuff like "good quality" etc.
        Never use the character ":".
        AMAZON REVIEWS:
        {positive_reviews_text}
    '''
    reply = llm_reply(prompt)
    pros = reply

    prompt = f'''
        Write a 200-word short paragraph about a product of mine: jars.
        This product is being used by herbalists, so adapt the data below to an audience of berbalists and write only things that would interest them.
        Write in a simple and direct language.
        Write in a informal and friendly tone.
        Don't use hype, exclamation marks, and other "salesy" expressions.
        Don't repeat yourself.
        Don't allucinate.
        Use the following data: 
        {pros}
        Start with the following words: These jars .
    '''
    reply = llm_reply(prompt)

    quit()

    ################################################################################
    # DESCRIPTION
    ################################################################################
    tone = 'Write in a informal and friendly tone'
    style = 'Write in a concise and direct language'
    words_n = 'Write as few words as possible'

    prompt = f'''
        Write a 200-word short paragraph about a product of mine called: jars.
        Don't use hype, exclamation marks, and other "salesy" expressions.
        Write in a plain and sober way.
        Write in a simple and conversational way.
        Don't mention guarantees.
        Use the following data: 
        {description}
        Start with the following words: These jars .
    '''
    reply = llm_reply(prompt)
    quit()

    ################################################################################
    # STYLE
    ################################################################################
    with open('test/test-review-style.txt') as f: style_review = f.read()
    prompt = f'''
        Extract writing style from the following text:
        {style_review}
    '''
    reply = llm_reply(prompt)
    style = reply






    prompt = f'''
        Extract the 10 most important and recurring cons (negative things) from the AMAZON REVIEWS listed below about the mentioned product.
        Reply in list format.
        Reply only with the list.
        Give me pros that are specific, not general stuff like "good quality" etc.
        Never use the character ":".
        AMAZON REVIEWS:
        {negative_reviews_text}
    '''
    reply = llm_reply(prompt)

    cons = reply


    prompt = f'''
        Write a 200-word short paragraph about a product of mine called: jars.
        Don't use hype, exclamation marks, and other "salesy" expressions.
        Write in a plain and sober way.
        Use the following data: 
        {cons}
        Start with the following words: These jars .
    '''
    reply = llm_reply(prompt)

gen_article('jars')



