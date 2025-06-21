import shutil

from lib import g

shutil.copy2('style.css', f'{g.WEBSITE_FOLDERPATH}/style.css')

# herbs
if 0:
    if 1:
        from lib import art_herbs_preparations
        art_herbs_preparations.gen()
    if 0:
        from lib import art_herbs_benefits
        art_herbs_benefits.gen()
    if 1:
        from lib import art_herbs
        art_herbs.gen()
    if 0:
        from lib import cat_herbs
        cat_herbs.gen()

# ailments
if 0:
    if 1:
        from lib import art_ailments_preparations
        art_ailments_preparations.gen()
    if 1:
        from lib import art_ailments
        art_ailments.gen()
    if 1:
        from lib import cat_ailments
        cat_ailments.gen()

# preparations
if 1:
    if 0:
        from lib import art_preparations_herbs
        art_preparations_herbs.gen()
    if 0:
        from lib import art_preparations_best
        art_preparations_best.gen()
    if 1:
        from lib import art_preparations
        art_preparations.gen()
    if 1:
        from lib import cat_preparations
        cat_preparations.gen()

# equipment
if 0:
    if 1:
        from lib import art_equipment_best
        art_equipment_best.gen()
    if 1:
        from lib import art_equipment
        art_equipment.gen()
    if 1:
        from lib import cat_equipment
        cat_equipment.gen()

# shop
if 0:
    if 1:
        from lib import pag_shop_herb_drying_checklist_download
        from lib import pag_shop_herb_drying_checklist_subscribe
        pag_shop_herb_drying_checklist_download.gen()
        pag_shop_herb_drying_checklist_subscribe.gen()
    if 1:
        from lib import pag_shop_infusion_cheatsheet
        pag_shop_infusion_cheatsheet.gen()
    if 1:
        from lib import pag_shop
        pag_shop.gen()

if 0: 
    if 1:
        from page_home import page_home_gen
        page_home_gen()


# TODO:
# complete pages herbs (and link to benefits)
# complete pages herbs benefits

# write equipment best pages
# complete equipment pages

# complete shop
# complete ailments
# complete home
