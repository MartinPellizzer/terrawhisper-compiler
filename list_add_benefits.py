import csv
import sys

print(len(sys.argv))
if len(sys.argv) != 4:
    print("err: pass the right arguments (entity, benefit, part)")
    quit()

entity = sys.argv[1].lower().replace(' ', '-')
benefit = sys.argv[2].lower().strip()
part = sys.argv[3].lower().strip()
print(f'entity: {entity}')
print(f'benefit: {benefit}')
print(f'part: {part}')
filepath = f'database/tables/medicine/benefits/benefits.csv'

with open('_tmp_list.csv', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')

vals = [x.strip() for x in lines if x.strip() != '']


rows = []
for val in vals:
    rows.append([entity, benefit, part, val])

csv_rows = []
with open(filepath, encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f, delimiter="|")
    for i, line in enumerate(reader):
        csv_rows.append(line)


output_rows = [x for x in csv_rows]
for row in rows:
    found = False
    for csv_row in csv_rows:
        if row[0] == csv_row[0] and row[1] == csv_row[1] and row[2] == csv_row[2] and row[3] == csv_row[3]:
            found = True
            break
    if not found:
        output_rows.append(row)

with open(filepath, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='|')
    for row in output_rows:
        writer.writerow(row)

