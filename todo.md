# ###################################################
# DAILY
# ###################################################

- ARTICLES:
    - gen tea_conditions articles
    - gen ailments articles
    - gen herbs articles

- PINTEREST:
    just pin

- IMAGES:
    - generate images teas


# ###################################################
# WEEKLY (saturday?)
# ###################################################

- ANALYTICS
    - check pinterest
    - check google analytics
    - check google search console





# ###################################################
# TODO
# ###################################################
fix http://127.0.0.1:5500/herbalism/tincture/nervous-system/stress.html fatigue link not pointing to article
build simulator for content testing?

- SUPPLEMENTARY UMBRELLA:
    - What causes bad breath and how to best treat it?
    - How to best treat bad breath with herbal teas?
        - What are the causes of bad breath that you can treat with herbal teas?
        - How frequently should you drink herbal teas for bad breath?
        - How long does it take to see results with herbal teas for bad breath?
        - What are the possible side effects of herbal teas for bad breath?
        - What herbs to avoid for bad breath?
        - What other herbal preparations treat for bad breath?

- SUPPLEMENTARY (TEA/TINCTURE):
    make related ailments preparations specific
        - ex. ailments related to x [that-teas-can-treat]
        - pointing link to teas articles instead of general ailment article

- HERBALISM/TINCTURE/SYSTEMS:
    - gen page

- HERBALISM/TINCTURE:
    - gen page

- complete supplementary content in teas and tinctures (make h3 related ailments and faq)
- new herbs page from herbs database (create "herbs" url?)
- fix homepage sections (fix plants and add ailments)
- put only herbal teas/tincures + ailments (and herbs when done) in sitemap for now


- other preparations and best herbs/preparations for condition
- move teas_conditions to ailments? and in herbalism talk about specific teas? or talk about specific teas in plants?

- CHECK PINNED ARTICLES
    [!] check database/articles/herbalism/tea jsons and make sure you have the in the tea_conditions csv with "to_process" cells active

- CONDITIONS PAGE:
    [1] do page conditions

    - CONDITIONS ARTICLES:
        [1] to do conditions page, you must generate conditions articles to link to (create template for article)
    
- REDIRECT:
    [!!!] test redirect on terrawhisper website after upload

- TEAS PAGE:
    [1] gen ai 1 sentence each condition in system in herbalism/tea.json
    [1] adjust conditions names using the names from old condition csv file (because pins already linking), or redirect?
    [1] complete other sections in tea page (ex. how to)

    - TEAS ARTICLES:
        [2] complete studies scraper + ai summary generator 

- IMAGES:
    [1] reorganize images in c://...images/teas...

- PAGES:
    [2] should articles links (ex. home page articles) by a <article> tag?

- PAGE TAXONOMY
    [3] generate

- PLANTS:
    [3] scrape_trefle_plant.py - scrape plants data
    [3] scrape_trefle_plant.py - also scrape powo for data (ex. full taxonomy?)

- ARTICLES:
    [3] improve entity articles (culinary, etc...)

- REFACTOR:
    [3] make benefits, constituents, etc... pages similar to side effects pages (main.py function) 
