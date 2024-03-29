import pathlib

path = pathlib.Path('database\\articles\\plants')
filepaths = path.rglob("*.json")

for filepath in filepaths: 
    print(filepath) 