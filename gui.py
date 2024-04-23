import tkinter as tk
from tkinter import ttk
import random

import g
import util

conditions_rows = util.csv_get_rows(g.CSV_CONDITIONS_FILEPATH)
conditions_cols = util.csv_get_cols(conditions_rows)

table_data = []
for condition_row in conditions_rows[1:]:
    condition_id = condition_row[conditions_cols['condition_id']]
    condition_name = condition_row[conditions_cols['condition_name']]
    condition_slug = condition_row[conditions_cols['condition_slug']]

    if condition_id == '': continue

    table_data.append((condition_id, condition_name, condition_slug))

window = tk.Tk()
window.geometry('800x600')

table = ttk.Treeview(window, columns=('id', 'name', 'slug'), show='headings')
table.heading('id', text='ID')
table.heading('name', text='Name')
table.heading('slug', text='Slug')
table.pack(fill='both', expand=True)

# for i in range(100):
#     r1 = random.randint(1, 100)
#     r2 = random.randint(1, 100)
#     r3 = random.randint(1, 100)
#     table.insert(parent='', index=0, values=(r1, r2, r3))

for values in table_data:
    table.insert(parent='', index=tk.END, values=values)


# table.insert(parent='', index=tk.END, values = ('xxxxx', 'yyyyy', 'zzzzz'))

def item_select(_):
    for i in table.selection():
        print(table.item(i)['values'])

def delete_items(_):
    for i in table.selection():
        table.delete(i)

table.bind('<<TreeviewSelect>>', item_select)
table.bind('<Delete>', delete_items)

window.mainloop()