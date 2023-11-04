import csv

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