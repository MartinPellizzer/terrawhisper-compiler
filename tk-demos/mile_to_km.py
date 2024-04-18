import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk

def convert():
    mile_input = entry_int.get()
    km_output = mile_input * 1.61
    output_string.set(km_output)


window = ttk.Window(themename='darkly')
window.title('demo')
window.geometry('300x150')

title_label = ttk.Label(master=window, text='miles to kilometers', font='Calibri 24 bold')
title_label.pack()

input_frame = ttk.Frame(master=window)
input_frame.pack(pady=10)

entry_int = tk.IntVar()
entry = ttk.Entry(master=input_frame, textvariable=entry_int)
entry.pack(side='left', padx=10)

button = ttk.Button(master=input_frame, text='convert', command=convert)
button.pack(side='left')

output_string = tk.StringVar()
output_label = ttk.Label(master=window, text='output', font='Calibri 24', textvariable=output_string)
output_label.pack(pady=5)

window.mainloop()