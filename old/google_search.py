from googlesearch import search

lst = search("best herbal teas for colds", num=3, stop=3)
for item in lst:
    print(item)