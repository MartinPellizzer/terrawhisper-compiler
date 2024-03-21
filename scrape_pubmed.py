from pymed import PubMed
import json


pubmed = PubMed(tool="MyTool", email="my@email.address")
results = pubmed.query("chamomile sleep", max_results=10)

print()
print()
print()
print()
print()
i = 0
for article in results:
    # if i == 1:
    # print(article.toJSON())
    content = article.toJSON()
    json_object = json.loads(content)
    print(json_object['abstract'])
    i += 1
    print()
print()
print()
print()
print()