def books_get():
    herbs_0000 = io.csv_to_dict(f'database/herbs-book-0000.csv')
    with open('database/herbs/books/medical-herbalism.txt') as f: herbs_0001 = f.read().split('\n')
    ###
    herbs = []
    for herb in herbs_0000: herbs.append(herb['latin_name'].strip().lower())
    for herb in herbs_0001: herbs.append(herb.strip().lower())
    herbs = list(set(herbs))
    herbs = sorted(herbs)
    return herbs


