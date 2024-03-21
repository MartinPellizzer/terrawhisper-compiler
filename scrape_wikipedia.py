import wikipediaapi
wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')

page_py = wiki_wiki.page('achillea_millefolium')

print(page_py.title)
print(page_py.summary)
print(page_py.text)