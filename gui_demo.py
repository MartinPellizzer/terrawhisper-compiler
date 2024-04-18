import tkinter as tk
from tkinter import ttk

import utils_ai

def func_name():
    text_in = prompt.get("1.0", 'end-1c')
    text_out = utils_ai.gen_reply(text_in)
    reply.delete(1.0, 'end-1c')
    reply.insert('end-1c', text_out)

window = tk.Tk()
window.title('window and widgets')
window.geometry('1600x600')

prompt = tk.Text(master=window)
prompt.pack(side='left')

reply = tk.Text(master=window)
reply.pack(side='left')

button = ttk.Button(master=window, text='click me', command=func_name)
button.pack(side='left')

window.mainloop()