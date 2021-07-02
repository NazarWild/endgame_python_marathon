import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import re
from db_part import *
from reqResp import *
from manual_start import *


def funcForTable(table, container, type):
    # types list of dicts = 1 || dict of dicts = 2 || list = 3 || dict = 4
    if type == 1:
        # print("list of dicts")
        columns = []
        for k in container:
            for j in k.keys():
                if j not in columns:
                    columns.append(j)
        table['columns'] = columns
        table.column('#0', width=0, stretch=NO)
        for j in columns:
            table.column(j, stretch=YES)
            table.heading(j, text=j, anchor=CENTER)
        i = 0
        for data in container:
            input_v = []
            for key in columns:
                input_v.append(data.get(key))
            table.insert(parent='', index=i, iid=i, text='', values=input_v)
            i = i + 1
    elif type == 2:
        # print("dict of dicts")
        columns = [""]
        for j in container.values():
            for k in j:
                if k not in columns:
                    columns.append(k)
        table['columns'] = columns
        table.column('#0', width=0, stretch=NO)
        for j in columns:
            table.column(j, stretch=YES)
            table.heading(j, text=j, anchor=CENTER)
        i = 0
        for data in container:
            input_v = [data]
            for dic in container[data]:
                input_v.append(container.get(data).get(dic))
            table.insert(parent='', index=i, iid=i, text='', values=input_v)
            i = i + 1
    elif type == 3:
        # print("list")
        table['columns'] = ("id", "value")
        table.column('#0', width=0, stretch=NO)
        table.column("id", stretch=YES)
        table.column("value", stretch=YES)
        table.heading("value", text="value", anchor=CENTER)
        table.heading("id", text="", anchor=CENTER)
        i = 0
        for data in container:
            table.insert(parent='', index=i, iid=i, text='', values=(i, data))
            i = i + 1
    elif type == 4:
        # print("dict")
        table.column('#0', width=0, stretch=NO)
        table['columns'] = ("id", "value")
        table.column("id", stretch=YES)
        table.column("value", stretch=YES)
        table.heading("value", text="value", anchor=CENTER)
        table.heading("id", text="", anchor=CENTER)
        i = 0
        for data in container:
            table.insert(parent='', index=i, iid=i, text='', values=(data, container.get(data)))
            i = i + 1


def recForTree(tree, bId, big_data, type):
    # types list = 1 || dict = 2
    tree['columns'] = ()
    # tree.column('#0', width=800, stretch=YES)
    i = 0
    for data in big_data:
        key = data
        if type == 2:
            key = big_data.get(data)
        if isinstance(key, list):
            string = f'{data}' + ": [" + f'{len(key)}' + "]"
            # print(f'list = {key}, {string}')
            newId = tree.insert(bId, i, text=string)
            recForTree(tree, newId, key, 1)
        elif isinstance(key, dict):
            if type == 1:
                string = f'{i}' + ": {" + f'{len(key)}' + "}"
            elif type == 2:
                string = f'{data}' + ": {" + f'{len(key)}' + "}"
            # print(f'dict = {key}, {string}')
            newId = tree.insert(bId, i, text=string)
            recForTree(tree, newId, key, 2)
        else:
            if type == 1:
                if isinstance(key, str):
                    string = f'{i}: "{key}"'
                else:
                    string = f'{i}: {key}'
            elif type == 2:
                if isinstance(key, str):
                    string = f'{data}: "{key}"'
                else:
                    string = f'{data}: {key}'
            # print(f'else = {key}, {string}')
            tree.insert(bId, i, text=string)
        i = i + 1


def treeFilling(tree, data):
    tree.delete(*tree.get_children())

    if isinstance(data, list):
        dicts = filter(lambda l: isinstance(l, dict), data.copy())
        other_values = filter(lambda l: isinstance(l, (dict, list)) == False, data.copy())
        if len(list(dicts)) == len(data):
            funcForTable(tree, data, 1)
        elif len(list(other_values)) == len(data):
            funcForTable(tree, data, 3)
        else:
            string = "[" + f'{len(data)}' + "]"
            bId = tree.insert('', 0, text=string)
            recForTree(tree, bId, data, 1)
    elif isinstance(data, dict):
        dicts = filter(lambda l: isinstance(l, dict), data.values())
        other_values = filter(lambda l: isinstance(l, (dict, list)) == False, data.values())
        if len(list(dicts)) == len(data):
            funcForTable(tree, data, 2)
        elif len(list(other_values)) == len(data):
            funcForTable(tree, data, 4)
        else:
            string = "{" + f'{len(data)}' + "}"
            bId = tree.insert('', 0, text=string)
            recForTree(tree, bId, data, 2)


def fillingHistory(history, bd):
    history.delete(*history.get_children())
    history['columns'] = ['ID', 'Method', 'URL', 'Request body', 'Params', 'Headers', 'Status']
    history.column('#0', width=0, stretch=NO)
    history.column("ID", width=40, stretch=YES)
    history.column("Method", width=80, stretch=YES)
    history.column("URL", width=300, stretch=YES)
    history.column("Request body", stretch=YES)
    history.column("Params", stretch=YES)
    history.column("Headers", stretch=YES)
    history.column("Status", stretch=YES)
    history.heading("ID", text="ID", anchor=CENTER)
    history.heading("Method", text="Method", anchor=CENTER)
    history.heading("URL", text="URL", anchor=CENTER)
    history.heading("Request body", text="Request body", anchor=CENTER)
    history.heading("Params", text="Params", anchor=CENTER)
    history.heading("Headers", text="Headers", anchor=CENTER)
    history.heading("Status", text="Status", anchor=CENTER)

    bd.req.execute(f"SELECT * FROM Requests")
    container = bd.req.fetchall()
    i = 0
    for data in container:
        history.insert(parent='', index=i, iid=i, text='', values=data)
        i = i + 1


def methods_changed(event):
    print(f'New method selected!')


def views_changed(event):
    print(f'New view selected!')


def render_packed(root, db=None):
    notebook = ttk.Notebook(root)
    notebook.grid(row=0, column=0)

    # create frames
    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)

    frame1.grid(row=0, column=0)
    frame2.grid(row=0, column=0)

    # add frames to notebook

    notebook.add(frame1, text='Main')
    notebook.add(frame2, text='History')

    tree = ttk.Treeview(frame1)
    tree.column('#0', width=800, stretch=YES)
    tree.grid(row=0, rowspan=25, column=9, columnspan=8)

    meth = tk.StringVar()
    methods = ttk.Combobox(frame1, textvariable=meth, values=('GET', 'POST', 'PATCH', 'PUT', 'DELETE'))
    methods.current(0)
    methods.bind('<<ComboboxSelected>>', methods_changed)
    methods.grid(row=0, column=0, columnspan=2)

    url = StringVar()
    url_entry = tk.Entry(frame1, text='key', textvariable=url)
    url_entry.grid(row=0, column=3, columnspan=4)

    def send_request():
        data = manual_start(db, url=url_entry.get(), method=methods.get(), params=None,
                            headers=None, auth=None, body=None, trig=False)
        fillingHistory(history, db)
        if res_view.get() == "TreeView":
            tree.delete(*tree.get_children())
            string = "{" + f'{len(data)}' + "}"
            bId = tree.insert('', 0, text=string)
            recForTree(tree, bId, data, 2)


    send_button = tk.Button(frame1, text="SEND", command=send_request)
    send_button.grid(row=0, column=7, columnspan=2)

    history = ttk.Treeview(frame2, height=100)
    history.grid(column=0, row=0, sticky=(N, W, E, S))
    s = ttk.Scrollbar(root, orient=VERTICAL, command=history.yview)
    s.grid(column=1, row=0, sticky=(N, S))
    history.configure(yscrollcommand=s.set)
    fillingHistory(history, db)

    # l = Listbox(frame2, height=5)
    # l.grid(column=0, row=0, sticky=(N, W, E, S))
    # s = ttk.Scrollbar(frame2, orient=VERTICAL, command=l.yview)
    # s.grid(column=1, row=0, sticky=(N, S))
    # l['yscrollcommand'] = s.set
    # for i in range(1, 101):
    #     l.insert('end', 'Line %d of 100' % i)


    #parameters
    f_params = ttk.Frame(frame1)
    f_params.grid(row=4, column=0, columnspan=8)

    def add_line():
        tk.Entry(f_params, text='key').grid(row=2, column=0)
        tk.Entry(f_params, text='value').grid(row=2, column=4)

    tk.Label(f_params, text="Params").grid(row=0, column=0)
    tk.Entry(f_params, text='key').grid(row=1, column=0)
    tk.Entry(f_params, text='value').grid(row=1, column=4)
    tk.Button(f_params, text="+", command=add_line).grid(row=1, column=8)

    #body
    f_body = ttk.Frame(frame1)
    f_body.grid(row=8, column=0, columnspan=8)

    def add_line():
        tk.Entry(f_body, text='key').grid(row=2, column=0)
        tk.Entry(f_body, text='value').grid(row=2, column=4)

    tk.Label(f_body, text="Body").grid(row=0, column=0)
    tk.Entry(f_body, text='key').grid(row=1, column=0)
    tk.Entry(f_body, text='value').grid(row=1, column=4)
    tk.Button(f_body, text="+", command=add_line).grid(row=1, column=8)

    #headers
    f_headers = ttk.Frame(frame1)
    f_headers.grid(row=14, column=0, columnspan=8)

    def add_line():
        tk.Entry(f_headers, text='key').grid(row=2, column=0)
        tk.Entry(f_headers, text='value').grid(row=2, column=4)

    tk.Label(f_headers, text="Headers").grid(row=0, column=0)
    tk.Entry(f_headers, text='key').grid(row=1, column=0)
    tk.Entry(f_headers, text='value').grid(row=1, column=4)
    tk.Button(f_headers, text="+", command=add_line).grid(row=1, column=8)


    #response view
    r_view = tk.StringVar()
    res_view = ttk.Combobox(frame1, textvariable=r_view, values=('TreeView', 'Table', 'Yaml', 'Raw', 'Json'))
    res_view.current(0)
    res_view.bind('<<ComboboxSelected>>', views_changed)
    res_view.grid(row=22, rowspan=3, column=0, columnspan=8)


def visual_start(db):
    root = tk.Tk()
    root.title('Endgame')
    root.geometry('1290x1200')
    root.minsize(800, 800)
    root.eval('tk::PlaceWindow . center')
    root.configure(background='grey')
    root.resizable(False, False)

    s = ttk.Style()
    s.theme_use('default')
    # ('aqua', 'step', 'clam', 'alt', 'default', 'classic')

    render_packed(root, db=db)

    root.mainloop()
