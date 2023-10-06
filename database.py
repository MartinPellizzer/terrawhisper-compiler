import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog

database_name = 'database.db'

db_plants_fields = {
    'oid': 'integer',
	'latin_name': "text", 
	'common_name': "text", 
}
plants_fields = [f'{f}' for f in db_plants_fields]


def db_plants_create_table():
    fields_lst = [f'{f} {db_plants_fields[f]}' for f in db_plants_fields]
    fields = ', '.join(fields_lst)
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute(f'create table if not exists plants ({fields})')


def db_plants_get_rows():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute(f'select oid, * from plants')
    records = c.fetchall()	
    conn.commit()
    conn.close()
    return records


def db_plants_insert_rows(rows):
    fields_lst = [f'{f}' for f in db_plants_fields]
    fields = ':' + ', :'.join(fields_lst)

    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    for row in rows:
        fields_dict = {}
        for i, key in enumerate(db_plants_fields):
            fields_dict[key] = row[i]
        c.execute(f'insert into plants values ({fields})', fields_dict)
    conn.commit()
    conn.close()


def db_plants_update_by_oid(values):
    values.append(values[0])
    fields = ' = ?, '.join(db_plants_fields) + ' = ?'
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    sql = f'''update plants set {fields} where oid = ?'''
    c.execute(sql, values)
    conn.commit()
    conn.close()





def tk_plants_tree_refresh(rows):
    main_tree.delete(*main_tree.get_children())
    for index, row in enumerate(rows):
        main_tree.insert(parent='', index=index, iid=index, text='', values=row, tags=(row[1],))


# def tk_plants_add():
#     entries_vals = [entry.get() for entry in entries]
#     db_plants_insert_rows([entries_vals])
#     tk_plants_tree_refresh(db_plants_get_rows())
#     print(entries_vals)



##############################################################
# TKINTER ADD PLANT
##############################################################
def tk_plants_add():
	add_window = Toplevel(root)
	add_window.title('Add Client')
	add_window.geometry('270x500')
	add_window.grab_set()

	add_frame = LabelFrame(add_window, text='Add Plants', padx=20, pady=10)
	add_frame.pack(side=LEFT, fill=Y)

	add_labels = []
	add_entries = []
	for i, field in enumerate(plants_fields):
		add_labels.append(Label(add_frame, text=field).grid(row=i, column=0, sticky=W))
		tmp_entry = Entry(add_frame)
		tmp_entry.grid(row=i, column=1, sticky=W)
		add_entries.append(tmp_entry)
	i += 1

	def tk_plants_add_to_db():
		entries_vals = [entry.get() for entry in add_entries]
		db_plants_insert_rows([entries_vals])

		for i, field in enumerate(plants_fields):
			add_entries[i].delete(0, END)

		tk_plants_tree_refresh(db_plants_get_rows())

	curr_add_button = Button(add_frame, text='Add', command=tk_plants_add_to_db)
	curr_add_button.grid(row=i, column=0, sticky=W)


##############################################################
# TKINTER UPDATE PLANT
##############################################################
def tk_plants_update(e):
    update_window = Toplevel(root)
    update_window.title('Update Client')
    update_window.geometry('270x500')
    update_window.grab_set()

    update_frame = LabelFrame(update_window, text='Update Plants', padx=20, pady=10)
    update_frame.pack(side=LEFT, fill=Y)

    selected_row = main_tree.focus()
    selected_values = main_tree.item(selected_row, 'values')

    update_labels = []
    update_entries = []
    for i, field in enumerate(plants_fields):
        tmp_label = Label(update_frame, text=field)
        tmp_label.grid(row=i, column=0, sticky=W)
        update_labels.append(tmp_label)

        tmp_entry = Entry(update_frame)
        tmp_entry.grid(row=i, column=1, sticky=W)
        update_entries.append(tmp_entry)
        update_entries[i].insert(0, selected_values[i])
    i += 1        

    def tk_plants_update_by_oid():
        entries_vals = [entry.get() for entry in update_entries]
        db_plants_update_by_oid(entries_vals)

        # for i, field in enumerate(plants_fields):
        #     update_entries[i].delete(0, END)

        tk_plants_tree_refresh(db_plants_get_rows())

    curr_add_button = Button(update_frame, text='Update', command=tk_plants_update_by_oid)
    curr_add_button.grid(row=i, column=0, sticky=W)

# db_plants_create_table()
# rows = db_plants_get_rows()


root = Tk()
root.title('Botanist')
root.geometry('800x600')

frame_fields = Frame(root, padx=20, pady=10)
frame_fields.pack(side=LEFT, fill=Y)

i = 0
add_button = Button(frame_fields, text='Add', command=tk_plants_add)
add_button.grid(row=i, column=0, sticky=W)
i += 1


# CENTER
frame_center = Frame(root, padx=20, pady=10)
frame_center.pack(side=LEFT, expand=True, fill=BOTH)


# TREEVIEW
frame_tree = Frame(frame_center)
frame_tree.pack(side=TOP, expand=True, fill=BOTH)

main_tree = ttk.Treeview(frame_tree)
main_tree.pack(expand=True, fill=Y)

total_width = 640
column_width = total_width // len(plants_fields)

main_tree['columns'] = plants_fields
main_tree.column('#0', width=0, stretch=NO)
main_tree.heading('#0', text='', anchor=W)
for field in plants_fields:
	main_tree.column(field, width=column_width, anchor=W)
	main_tree.heading(field, text=field, anchor=W)
    


##############################################################
# KEY BINDING
##############################################################
main_tree.bind("<Double-1>", tk_plants_update)



##############################################################
# INIT
##############################################################
tk_plants_tree_refresh(db_plants_get_rows())

root.mainloop()