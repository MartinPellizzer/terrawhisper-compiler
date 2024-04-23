# ###################################################
# DAILY
# ###################################################

- ARTICLES:
    - gen tea_conditions articles
    - gen 50 trefle plant articles
    - update plants page

- SCRAPE POWO:
    - plants taxonomy
        [1] set N/A if failed scraped
    - fix scraper when elements not found

- PINTEREST:
    just pin (to fix description selenium)

- IMAGES:
    - generate images (especially teas)


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
- copy old articles to new slug if not already present an article
- fix pinterest, take articles from folders

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
