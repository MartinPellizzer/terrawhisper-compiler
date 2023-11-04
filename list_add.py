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

with open('_tmp_list.csv', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')

# print(filepath)
# for line in lines:
#     print(line)

# vals.insert(0, entity)

vals = [x.strip() for x in lines if x.strip() != '']

rows = []
for val in vals:
    common_name, description = val.split(':')
    rows.append([entity, common_name, description])

csv_rows = []
with open(filepath, encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f, delimiter="|")
    for i, line in enumerate(reader):
        csv_rows.append(line)


# output_lines = []
# for item in lst:
#     found = False
#     for csv_item in csv_lines:    
#         if item[0].strip() == csv_item[0].strip() and item[1].strip() == csv_item[1].strip():
#             found = True
#             output_lines.append(item)
#             print('replaced')
#             break
#         else:
#             output_lines.append(csv_item)
#     if found == False:
#         output_lines.append(item)
#         print('added')


output_rows = [x for x in csv_rows]
for row in rows:
    found = False
    for csv_row in csv_rows:
        if row[0] == csv_row[0] and row[1] == csv_row[1]:
            found = True
            break
    if not found:
        output_rows.append(row)


    # found = False
    # for row in rows:
    #     if row[0] == csv_row[0] and row[1] == csv_row[1]:
    #         found = True
    #         output_rows.append(row)
    #         break
    #     else: 
    #         output_rows.append(csv_row)
    # if not found:
    #     output_rows.append(row)


with open(filepath, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='|')
    for row in output_rows:
        writer.writerow(row)
