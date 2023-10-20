import os 
import sys


if len(sys.argv) != 2:
    print('ERR: accept only one argument ("Latin name")')
    quit()

latin_name = sys.argv[1].capitalize()
entity = latin_name.lower().replace(' ', '-')
filepath = f'database/articles/{entity}.json'

if os.path.exists(filepath): quit()

text = (f'''
[
    {{
        "state": "publish",
        "date": "",
        "post_type": "list",
        "entity": "{entity}",
        "attribute": "botanical/morphology",
        "latin_name": "{latin_name}",
        "common_name": "",
        "main_content": [
            {{
                "title": "Roots",
                "content": []
            }},
            {{
                "title": "Stems",
                "content": []
            }},
            {{
                "title": "Leaves",
                "content": []
            }},
            {{
                "title": "Flowers",
                "content": []
            }},
            {{
                "title": "Fruits",
                "content": []
            }},
            {{
                "title": "Seeds",
                "content": []
            }}
        ]
    }}
]
''')


with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)
