import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import re
from db_part import *
from reqResp import *
from manual_start import *


def funcForYaml(tree, big_data):
    tree['columns'] = ()
    tree.column('#0', width=820, stretch=YES)
    yaml_res = yaml.dump(big_data)
    tree.insert('', 0, text=str(yaml_res))


def funcForRaw(tree, big_data):
    tree['columns'] = ()
    tree.column('#0', width=820, stretch=YES)
    json_result = json.dumps(big_data, indent=4)
    tree.insert('', 0, text=str(json_result))


def funcForJson(tree, big_data):
    tree['columns'] = ()
    tree.column('#0', width=820, stretch=YES)
    i = 0
    for data in big_data:
        string = data
        string += " : "
        if isinstance(big_data[data], dict):
            string += "{}"
        elif isinstance(big_data[data], list):
            string += "[]"
        else:
            string += str(big_data[data])
        tree.insert('', i, text=string)
        i = i + 1


def funcForTable(table, container):
    table.column('#0', width=0, stretch=NO)
    table['columns'] = ("id", "value")
    table.column("id", width=210, stretch=YES)
    table.column("value", width=210, stretch=YES)
    table.heading("value", text="value", anchor=CENTER)
    table.heading("id", text="", anchor=CENTER)
    i = 0
    for data in container:
        table.insert(parent='', index=i, iid=i, text='', values=(data, container.get(data)))
        i = i + 1


def recForTree(tree, bId, big_data, type):
    # types list = 1 || dict = 2
    tree['columns'] = ()
    tree.column('#0', width=820, stretch=YES)
    i = 0
    for data in big_data:
        key = data
        if type == 2:
            key = big_data.get(data)
        if isinstance(key, list):
            string = f'{data}' + ": [" + f'{len(key)}' + "]"
            # print(f'list = {key}, {string}')
            newId = tree.insert(bId, i, text=string, background="#5F9EA0")
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
    history.column("ID", width=50, stretch=YES)
    history.column("Method", width=80, stretch=YES)
    history.column("URL", width=300, stretch=YES)
    history.column("Request body", width=250, stretch=YES)
    history.column("Params", width=250, stretch=YES)
    history.column("Headers", width=250, stretch=YES)
    history.column("Status", width=100, stretch=YES)
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
    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)

    frame1.grid()
    frame2.grid()

    # add frames to notebook
    notebook.add(frame1, text='MAIN')
    notebook.add(frame2, text='HISTORY')

    tree = ttk.Treeview(frame1, height=100, style="mystyle.Treeview", selectmode='none')
    tree.column('#0', width=820, stretch=YES)
    tree.grid(row=4, rowspan=100, column=0, columnspan=8)

    # hsb = ttk.Scrollbar(frame1, orient="horizontal", command=tree.yview)
    # hsb.grid(row=3, column=0, columnspan=8)
    #
    # tree.configure(yscrollcommand=hsb.set)

    #response view
    res_view = ttk.Combobox(frame1, values=('TreeView', 'Yaml', 'Raw', 'Json', 'Table'),
                            state='readonly', justify="center")
    # res_view = ttk.Combobox(frame1, values=('TreeView', 'Json'), state='readonly', justify="center")
    res_view.set('TreeView')
    # res_view.bind('<<ComboboxSelected>>', views_changed)
    res_view.grid(row=0, rowspan=3, column=0, columnspan=8)

    methods = ttk.Combobox(frame1, values=('GET', 'POST', 'PATCH', 'PUT', 'DELETE'), state='readonly', justify="center")
    methods.set('GET')
    # methods.bind('<<ComboboxSelected>>', methods_changed)
    methods.grid(row=0, column=9, columnspan=2)

    url = StringVar()
    url_entry = ttk.Entry(frame1, text='key', textvariable=url)
    url_entry.grid(row=0, column=12, columnspan=4)

    #info label
    info = tk.Label(frame1, text="", width=52, bg="#6495ED")
    info.grid(row=1, rowspan=3, column=9, columnspan=8)

    def send_request():
        t = False
        if res_view.get() == "Yaml":
            t = True

        data = manual_start(db, url=url_entry.get(), method=methods.get(), params=widgetsToDict(params),
                            headers=widgetsToDict(headers), auth=None, body=widgetsToDict(body), trig=t, label=info)
        fillingHistory(history, db)
        if data:
            tree.delete(*tree.get_children())
            tree['columns'] = ()
            tree.column('#0', width=820, stretch=YES)
            if res_view.get() == "TreeView":
                string = "{" + f'{len(data)}' + "}"
                bId = tree.insert('', 0, text=string)
                recForTree(tree, bId, data, 2)
            elif res_view.get() == "Table":
                funcForTable(tree, data)
            elif res_view.get() == "Json":
                funcForJson(tree, data)
            elif res_view.get() == "Raw":
                funcForRaw(tree, data)
            elif res_view.get() == "Yaml":
                funcForYaml(tree, data)

    send_button = ttk.Button(frame1, text="SEND", command=send_request)
    send_button.grid(row=0, column=16, columnspan=2)

    #parameters
    f_params = ttk.Frame(frame1)
    f_params.grid(row=4, column=10, columnspan=8)

    ttk.Label(f_params, text="Params").grid(row=0, column=0)

    def add_params():
        entryKey = ttk.Entry(f_params)
        entryKey.grid(row=len(params) + 1, column=0)
        entryValue = ttk.Entry(f_params)
        entryValue.grid(row=len(params) + 1, column=4)
        params[entryKey] = entryValue

    def del_params():
        if len(params) > 1:
            x = params.popitem()
            x[0].destroy()
            x[1].destroy()

    params = {}
    entryKey = ttk.Entry(f_params)
    entryKey.grid(row=1, column=0)
    entryValue = ttk.Entry(f_params)
    entryValue.grid(row=1, column=4)
    params[entryKey] = entryValue

    ttk.Button(f_params, text="+", command=add_params).grid(row=1, column=8)
    ttk.Button(f_params, text="-", command=del_params).grid(row=2, column=8)

    #body
    f_body = ttk.Frame(frame1)
    f_body.grid(row=10, column=10, columnspan=8)

    ttk.Label(f_body, text="Body").grid(row=0, column=0)

    def add_body():
        entryKeybody = ttk.Entry(f_body)
        entryKeybody.grid(row=len(body) + 1, column=0)
        entryValuebody = ttk.Entry(f_body)
        entryValuebody.grid(row=len(body) + 1, column=4)
        body[entryKeybody] = entryValuebody

    def del_body():
        if len(body) > 1:
            b = body.popitem()
            b[0].destroy()
            b[1].destroy()

    body = {}
    entryKeybody = ttk.Entry(f_body)
    entryKeybody.grid(row=1, column=0)
    entryValuebody = ttk.Entry(f_body)
    entryValuebody.grid(row=1, column=4)
    body[entryKeybody] = entryValuebody

    ttk.Button(f_body, text="+", command=add_body).grid(row=1, column=8)
    ttk.Button(f_body, text="-", command=del_body).grid(row=2, column=8)

    #headers
    f_headers = ttk.Frame(frame1)
    f_headers.grid(row=16, column=10, columnspan=8)

    ttk.Label(f_headers, text="Headers").grid(row=0, column=0)

    def add_headers():
        entryKeyHeaders = ttk.Entry(f_headers)
        entryKeyHeaders.grid(row=len(headers) + 1, column=0)
        entryValueHeaders = ttk.Entry(f_headers)
        entryValueHeaders.grid(row=len(headers) + 1, column=4)
        headers[entryKeyHeaders] = entryValueHeaders

    def del_headers():
        if len(headers) > 1:
            h = headers.popitem()
            h[0].destroy()
            h[1].destroy()

    headers = {}
    entryKeyHeaders = ttk.Entry(f_headers)
    entryKeyHeaders.grid(row=1, column=0)
    entryValueHeaders = ttk.Entry(f_headers)
    entryValueHeaders.grid(row=1, column=4)
    headers[entryKeyHeaders] = entryValueHeaders

    ttk.Button(f_headers, text="+", command=add_headers).grid(row=1, column=8)
    ttk.Button(f_headers, text="-", command=del_headers).grid(row=2, column=8)

    #history tab
    history = ttk.Treeview(frame2, selectmode='browse', style="mystyle.Treeview", height=1200)
    history.pack(side='left')

    vsb = ttk.Scrollbar(frame2, orient="vertical", command=history.yview)
    vsb.pack(side='right', fill=Y)

    history.configure(yscrollcommand=vsb.set)
    # history.tag_configure('odd', background='#E8E8E8')
    # history.tag_configure('even', background='#DFDFDF')

    fillingHistory(history, db)


def visual_start(db):
    root = tk.Tk()
    root.title('Endgame')
    root.geometry('1300x1200')
    root.minsize(800, 800)
    root.eval('tk::PlaceWindow . center')
    root.configure(background='grey')
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use('default')
    style.configure('TLabel', background='#6495ED', foreground="#F0FFF0")
    style.configure('TButton', background='#BC8F8F', foreground='#191970', activebackground='#F4A460')
    style.configure('TEntry', fieldbackground='#AFEEEE')
    style.configure('TFrame', background='#6495ED')
    # style.configure('TCombobox', background='#87CEFA', , foreground="#F0FFF0")
    style.configure('TNotebook', background='#4682B4')
    style.configure("TNotebook.Tab", borderwidth=2, background='#FDF5E6', foreground='#191970')
    style.configure("Vertical.TScrollbar", background='#BC8F8F', borderwidth=2)

    #https://httpbin.org/get
    #SUNKEN, RAISED, GROOVE, RIDGE
    style.configure("mystyle.Treeview", font=('Calibri', 14), background="#B0C4DE", fieldbackground="#B0C4DE")  # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 18, 'bold'), foreground='#000080')  # Modify the font of the headings

    render_packed(root, db=db)

    root.mainloop()
