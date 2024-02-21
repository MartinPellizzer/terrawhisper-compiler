import csv


def is_row_not_empty(row):
    found = False
    for cell in row:
        if cell.strip() != '':
            found = True
            break
    return found

    
def csv_to_llst(filepath, delimeter='\\'):
    llst = []
    with open(filepath, newline='') as f:
        reader = csv.reader(f, delimiter='\\')
        for row in reader:
            if is_row_not_empty(row):
                llst.append(row)
    return llst

    
def csv_get_rows_by_entity(filepath, entity):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter="|")
        for i, line in enumerate(reader):
            rows.append(line)
    
    filtered_rows = [] 
    for row in rows:
        if row[0].strip() == entity.strip():
            filtered_rows.append(row)
            
    return filtered_rows


def csv_get_rows_by_entity_with_header(filepath, entity):
    rows = []
    with open(filepath, encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter="|")
        for i, line in enumerate(reader):
            rows.append(line)
    
    filtered_rows = [] 
    filtered_rows.append(rows[0])
    for row in rows:
        if row[0].strip() == entity.strip():
            filtered_rows.append(row)
            
    return filtered_rows


def csv_to_llst_2(filepath):
    llst = []
    with open(filepath, newline='') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            if is_row_not_empty(row):
                llst.append(row)
    return llst
