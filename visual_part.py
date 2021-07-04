import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import re
from db_part import *
from reqResp import *
from manual_start import *


def funcForTable(table, container):
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


def widgetsToDict(widgDict):
    dick = {}
    for i in widgDict:
        dick[i.get()] = widgDict[i].get()
    if dick == {} or dick == {'': ''}:
        return None
    return dick


# def methods_changed(event):
#     print(f'New method selected!')
#
#
# def views_changed(event):
#     print(f'New view selected!')


def render_packed(root, db=None):
    notebook = ttk.Notebook(root, height=1170)
    notebook.grid(row=0, column=0)


    # create frames
    frame1 = tk.Frame(notebook, bg="#F0E68C")
    frame2 = tk.Frame(notebook, bg="#F0E68C")

    frame1.grid()
    frame2.grid()

    # add frames to notebook
    notebook.add(frame1, text='MAIN')
    notebook.add(frame2, text='HISTORY')

    tree = ttk.Treeview(frame1, height=100)
    tree.column('#0', width=820, stretch=YES)
    tree.grid(row=0, rowspan=100, column=9, columnspan=8)

    meth = tk.StringVar()
    methods = ttk.Combobox(frame1, textvariable=meth, values=('GET', 'POST', 'PATCH', 'PUT', 'DELETE'))
    methods.current(1)
    # methods.bind('<<ComboboxSelected>>', methods_changed)
    methods.grid(row=0, column=0, columnspan=2)

    url = StringVar()
    url_entry = tk.Entry(frame1, text='key', textvariable=url)
    url_entry.grid(row=0, column=3, columnspan=4)

    #info label
    info = tk.Label(frame1, text="", bg="#F0E68C", width=52)
    info.grid(row=1, rowspan=3, column=0, columnspan=8)

    def send_request():
        data = manual_start(db, url=url_entry.get(), method=methods.get(), params=widgetsToDict(params),
                            headers=widgetsToDict(headers), auth=None, body=widgetsToDict(body), trig=False, label=info)
        fillingHistory(history, db)
        if data:
            if res_view.get() == "TreeView":
                tree.delete(*tree.get_children())
                string = "{" + f'{len(data)}' + "}"
                bId = tree.insert('', 0, text=string)
                recForTree(tree, bId, data, 2)
            # if res_view.get() == "Table":
            #     funcForTable(tree, data)

    send_button = tk.Button(frame1, text="SEND", command=send_request, bg="Gold")
    send_button.grid(row=0, column=7, columnspan=2)

    #parameters
    f_params = tk.Frame(frame1, bg="#BDB76B")
    f_params.grid(row=4, column=0, columnspan=8)

    tk.Label(f_params, text="Params").grid(row=0, column=0)

    def add_params():
        entryKey = tk.Entry(f_params)
        entryKey.grid(row=len(params) + 1, column=0)
        entryValue = tk.Entry(f_params)
        entryValue.grid(row=len(params) + 1, column=4)
        params[entryKey] = entryValue

    params = {}
    entryKey = tk.Entry(f_params)
    entryKey.grid(row=1, column=0)
    entryValue = tk.Entry(f_params)
    entryValue.grid(row=1, column=4)
    params[entryKey] = entryValue

    tk.Button(f_params, text="+", command=add_params).grid(row=1, column=8)

    #body
    f_body = tk.Frame(frame1, bg="#BDB76B")
    f_body.grid(row=10, column=0, columnspan=8)

    tk.Label(f_body, text="Body").grid(row=0, column=0)

    def add_body():
        entryKeybody = tk.Entry(f_body)
        entryKeybody.grid(row=len(body) + 1, column=0)
        entryValuebody = tk.Entry(f_body)
        entryValuebody.grid(row=len(body) + 1, column=4)
        body[entryKeybody] = entryValuebody

    body = {}
    entryKeybody = tk.Entry(f_body)
    entryKeybody.grid(row=1, column=0)
    entryValuebody = tk.Entry(f_body)
    entryValuebody.grid(row=1, column=4)
    body[entryKeybody] = entryValuebody

    tk.Button(f_body, text="+", command=add_body).grid(row=1, column=8)

    #headers
    f_headers = tk.Frame(frame1, bg="#BDB76B")
    f_headers.grid(row=16, column=0, columnspan=8)

    tk.Label(f_headers, text="Headers").grid(row=0, column=0)

    def add_headers():
        entryKeyHeaders = tk.Entry(f_headers)
        entryKeyHeaders.grid(row=len(headers) + 1, column=0)
        entryValueHeaders = tk.Entry(f_headers)
        entryValueHeaders.grid(row=len(headers) + 1, column=4)
        headers[entryKeyHeaders] = entryValueHeaders

    headers = {}
    entryKeyHeaders = tk.Entry(f_headers)
    entryKeyHeaders.grid(row=1, column=0)
    entryValueHeaders = tk.Entry(f_headers)
    entryValueHeaders.grid(row=1, column=4)
    headers[entryKeyHeaders] = entryValueHeaders

    tk.Button(f_headers, text="+", command=add_headers).grid(row=1, column=8)


    #response view
    r_view = tk.StringVar()
    res_view = ttk.Combobox(frame1, textvariable=r_view, values=('TreeView', 'Table', 'Yaml', 'Raw', 'Json'))
    res_view.current(0)
    # res_view.bind('<<ComboboxSelected>>', views_changed)
    res_view.grid(row=22, rowspan=3, column=0, columnspan=8)

    #history tab
    history = ttk.Treeview(frame2, selectmode='browse')
    history.pack(side='left')

    vsb = ttk.Scrollbar(frame2, orient="vertical", command=history.yview)
    vsb.pack(side='right', fill=Y)

    history.configure(yscrollcommand=vsb.set)

    fillingHistory(history, db)


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
