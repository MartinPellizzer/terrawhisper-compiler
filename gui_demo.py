import tkinter as tk
from tkinter import ttk


def calc():
    height = height_var.get()
    width = width_var.get()
    depth = depth_var.get()
    volume_var.set(height*width*depth)

window = tk.Tk()
window.title('window and widgets')
window.geometry('1600x600')

height_label = ttk.Label(master=window, text="Height")
height_label.pack()
height_var = tk.IntVar(value=0)
height_entry = ttk.Entry(master=window, textvariable=height_var)
height_entry.pack()

width_label = ttk.Label(master=window, text="Width")
width_label.pack()
width_var = tk.IntVar(value=0)
width_entry = ttk.Entry(master=window, textvariable=width_var)
width_entry.pack()

depth_label = ttk.Label(master=window, text="Depth")
depth_label.pack()
depth_var = tk.IntVar(value=0)
depth_entry = ttk.Entry(master=window, textvariable=depth_var)
depth_entry.pack()

button = ttk.Button(master=window, text='Calc Vol', command=calc)
button.pack()

volume_var = tk.StringVar()
volume_label = ttk.Label(master=window, text="Volume", textvariable=volume_var)
volume_label.pack()


window.mainloop()