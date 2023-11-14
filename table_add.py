import csv
import sys

print(len(sys.argv))
if len(sys.argv) != 4:
    print("err: pass the right arguments (entity, attribute, table)")
    quit()

entity = sys.argv[1].lower().replace(' ', '-')
attribute = sys.argv[2].lower().strip()
table = sys.argv[3].lower().strip()
print(f'entity: {entity}')
print(f'attribute: {attribute}')
print(f'table: {table}')
filepath = f'database/tables/{attribute}/{table}.csv'

with open('_tmp_table.csv', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
lines = [x for x in lines if x.startswith('|')]
# for line in lines:
#     print(line)

# quit()

vals_lst = []
for line in lines[2:]:
    # vals = [val.strip() for val in line.split('|')[1: -1]]
    tmp_vals = line.split('|')[1: -1]
    vals_lst.append(tmp_vals)
    

vals = [x[1].strip() for x in vals_lst]
vals.insert(0, entity)
# print(vals)
# for vals in vals_lst:
#     print(vals)

found = False
csv_lines = []
with open(filepath, encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f, delimiter="|")
    for i, line in enumerate(reader):
        if entity.strip() == line[0].strip():
            found = True
            csv_lines.append(vals)
            print('replaced')
        else:
            csv_lines.append(line)
    if found == False:
        csv_lines.append(vals)
        print('added')

with open(filepath, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='|')
    for row in csv_lines:
        writer.writerow(row)

# lines = []
# with open(filepath) as f:
#     reader = csv.reader(f, delimiter="\\")
#     for i, line in enumerate(reader):
#         if i == 0:
#             lines.append(line)
#         else:
#             if line[0].strip() == entity.strip():
#                 lines.append(line)