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

new_vals_lst = []
vals = [x.insert(0, entity) for x in vals_lst]

# for vals in vals_lst:
#     print(vals)

# quit()
    

vals = [x[1].strip() for x in vals_lst]
vals.insert(0, entity)
# print(vals)
# for vals in vals_lst:
#     print(vals)


formatted_lst = []
for row in vals_lst:
    for state in row[2].split(','):
        formatted_lst.append([row[0], row[1], state])

# for row in formatted_lst:
#     print(row)

old_rows = []
with open(filepath, encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f, delimiter="|")
    for row in reader:
        old_rows.append(row)

new_rows = [x for x in old_rows]
for row in formatted_lst:
    # print(row)
    found = False
    for old_row in old_rows:
        # print(row)
        # print(old_row)
        # print()

        if (row[0].strip() == old_row[0].strip() and 
            row[1].strip() == old_row[1].strip() and 
            row[2].strip() == old_row[2].strip()):
            found = True
    if not found:
        new_rows.append(row)

with open(filepath, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='|')
    for row in new_rows:
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