import os
import shutil
import utils

# PATHS
ARTICLES_CSV = 'articles.csv'

# INITS
articles = utils.csv_to_llst(ARTICLES_CSV)

# index col with dict
articles_dict = {}
for i, item in enumerate(articles[0]):
    articles_dict[item] = i

articles = articles[1:]


google_tag = '''
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-9086LN3SRR"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-9086LN3SRR');
    </script>
'''


def normalize(text):
    return text.strip().lower()


all_plants_grid = []
for i, plant_row in enumerate(articles[1:]):
    print(f'{i+1}/{len(articles[1:])} - {plant_row}')
    entity = plant_row[articles_dict['entity']].strip()
    common_name = plant_row[articles_dict['common_name']].strip().lower()
    latin_name = entity.capitalize().replace('-', ' ')

    root = plant_row[articles_dict['root']].strip().lower()

    if root == '': continue

    if os.path.exists(f'website/{entity}.html'):
        all_plants_grid.append(
            [
                entity,
                common_name,
                latin_name,
                f'images/{entity}-introduction.jpg',
            ]
        )

articles_html = ''
for home_article in all_plants_grid:
    title = f'{home_article[1]} ({home_article[2]}) Guide'.title()
    articles_html += f'''
        <div>
            <img src="{home_article[3]}">
            <h2 class="grid-articles-title"><a href="{home_article[0]}.html">{title}</a></h2>
        </div>
    '''

html = f'''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="author" content="Martin Pellizzer">
        <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042" />
        <link rel="stylesheet" href="style.css">
        <title>All Plant | TerraWhisper</title>
        {google_tag}
    </head>

    <body>
        <section class="header-divider">
            <div class="container-lg">
                <header>
                    <a class="text-stone-700" href="/">TerraWhisper</a>
                    <nav>
                        <a class="text-stone-700" href="/plants.html">All Plants</a>
                    </nav>
                </header>
            </div>
        </section>

        <section class="container-lg mt-96 grid gap-48 grid-3">
            {articles_html}
        </section>

        
        <footer>
            <div class="container-lg">
                <span>© TerraWhisper.com 2023 | All Rights Reserved
            </div>
        </footer>
    </body>
    

    </html>
'''


with open(f'website/plants.html', 'w', encoding='utf-8') as f:
    f.write(html)



##################################################################################################
# ABOUT
##################################################################################################

shutil.copy2('static/about.html', 'website/about.html')


# articles_html = ''
# for home_article in articles_benefits:
#     title = f'10 health benefits of {home_article[1]} ({home_article[2]})'.title()
#     articles_html += f'''
#         <div>
#             <img src="{home_article[3]}">
#             <h2 class="grid-articles-title"><a href="{home_article[0]}/medicine/benefits.html">{title}</a></h2>
#         </div>
#     '''

# html = f'''
#     <!DOCTYPE html>
#     <html lang="en">

#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <meta name="author" content="Martin Pellizzer">
#         <meta name="p:domain_verify" content="b3cb3dbe613e3700596c8f50c5208042"/>
#         <link rel="stylesheet" href="style.css">
#         <title>Medicinal Plants | TerraWhisper</title>
#         {google_tag}
        
#     </head>

#     <body>
#         <section class="hero-section">
#             <div class="container-lg h-full">

#                 <section>
#                     <div class="container-lg">
#                         <header>
#                             <a class="fg-white" href="/">TerraWhisper</a>
#                             <nav>
#                                 <a class="fg-white" href="/plants.html">All Plants</a>
#                             </nav>
#                         </header>
#                     </div>
#                 </section>

#                 <div class="flex flex-col justify-center items-center h-90">
#                     <h1 class="fg-white text-center size-72 weight-400">Learn how to improve your health using medicinal plants</h1>

#                     <div class="container">
#                         <p class="fg-white text-center">If you are interested in healing herbs and natural remedies, welcome
#                             to the tribe. Here you will find out what are the best plants to boost your health and how to
#                             use them correctly to improve results.</p>
#                     </div>
#                 </div>
#             </div>
#         </section>

#         <section class="my-96">
#             <div class="container">
#                 <h2 class="text-center mb-16">Embrace Scientific Herbalism</h2>
#                 <p class="text-center mb-16">The medicinal properties of herbs are well recognized by science and 1000+ new
#                     scientific studies are conducted every year to document it. In fact, more than 75% of modern medicinals
#                     are made by synthesizing and extracting biochemical compounds from plants all around the world, and the
#                     number is increasing day by day.</p>
#                 <p class="text-center mb-16">If you are looking for a science-based approach to herbalism, and not a
#                     "magical" one, enjoy our articles packed with tons of scientific data on plants' healing effects.</p>
#             </div>
#         </section>

#         <section class="container-lg mt-96 grid gap-48 grid-3">
#             {articles_html}
#         </section>
        
#         <footer>
#             <div class="container-lg">
#                 <span>© TerraWhisper.com 2023 | All Rights Reserved
#             </div>
#         </footer>

#     </body>

#     </html>
# '''

# with open(f'website/index.html', 'w', encoding='utf-8') as f:
#     f.write(html)




shutil.copy2('style.css', 'website/style.css')
shutil.copy2('index.html', 'website/index.html')