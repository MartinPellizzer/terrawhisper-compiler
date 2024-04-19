import tkinter as tk
from tkinter import ttk

# import utils_ai
import util

def func_name():
    # text_in = prompt.get("1.0", 'end-1c')
    # text_out = utils_ai.gen_reply(text_in)
    text.delete(1.0, 'end-1c')
    text.insert('end-1c', conditions_names)

filepath = 'database/csv/status/conditions.csv'
rows = util.csv_get_rows(filepath)
cols = util.csv_get_cols(rows)

conditions_names = ''
for row in rows:
    row_name = row[cols['condition_name']]
    conditions_names += row_name + '\n'

window = tk.Tk()
window.title('window and widgets')
window.geometry('1600x600')

text = tk.Text(master=window)
text.pack(side='left')

button = ttk.Button(master=window, text='click me', command=func_name)
button.pack(side='left')

window.mainloop()