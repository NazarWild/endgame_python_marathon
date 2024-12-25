# import mysql.connector
import sqlite3
from parser import *
from prettytable import PrettyTable

def addTab(first, second):
    print(first, end='')
    for i in range(0, 22 - len(first)):
        print(" ", end='')
    if second:
        print(second)
    else:
        print("")


class workWithDb:
    def __init__(self, title, user=None, password=None):
        # self.dbName = title
        # self.myDb = mysql.connector.connect(
        #     host="localhost",
        #     password=password,
        #     user=user
        # )
        # self.myCursor = self.myDb.cursor()
        # self.myCursor.execute(f"CREATE DATABASE {self.dbName}")
        self.conn = sqlite3.connect(title)
        self.req = self.conn.cursor()
        self.req.execute("CREATE TABLE IF NOT EXISTS Requests ("
                         "id INTEGER NOT NULL PRIMARY KEY autoincrement, h_method VARCHAR, url VARCHAR,"
                         "body VARCHAR, params VARCHAR, headers VARCHAR, status INTEGER)")
        self.req.execute("CREATE TABLE IF NOT EXISTS Responses ("
                         "req_id INTEGER, resp_code INTEGER, result VARCHAR)")

    def insertIntoRequests(self, url, h_method, status, params=None, body=None, headers=None):
        sql = 'INSERT INTO Requests (h_method, url, body, params, headers, status) ' \
              f'VALUES ("{h_method}", "{url}", "{body}", "{params}", "{headers}", {status})'
        self.req.execute(sql)
        self.conn.commit()
        return self.req.lastrowid

    def updateRequests(self, req_id, url, h_method, status, params=None, body=None, headers=None):
        self.req.execute(f"UPDATE Requests SET "
                         f'h_method = "{h_method}", url = "{url}", body = "{body}",'
                         f'params = "{params}", headers = "{headers}, status = {status}" '
                         f"WHERE id = {req_id};")
        self.conn.commit()

    def selectRequests(self, req_id):
        self.req.execute(f"SELECT * FROM Requests WHERE id = {req_id}")
        self.conn.commit()
        data = self.req.fetchall()
        x = PrettyTable()
        if data:
            if data[0]:
                data = data[0]
            x.add_column('..', ['Method', 'URL', 'Params', 'Headers', 'Request body', 'Status'])
            x.add_column('Request info', [data[1], data[2], data[4], data[5], data[3], data[6]])
        print(x)
        print("---Response---")
        self.req.execute(f"SELECT * FROM Responses WHERE req_id = {req_id}")
        self.conn.commit()
        data = self.req.fetchall()
        if data:
            if data[0][2]:
                print(data[0][2])
            else:
                print(f"Response code = {data[0][1]}")

    def deleteFromRequests(self, req_id):
        self.req.execute(f"DELETE FROM Requests WHERE id = {req_id};")
        self.conn.commit()
        print(self.req.rowcount, "record deleted.")

    def insertIntoResponses(self, req_id, resp_code, result={}):
        self.req.execute("INSERT INTO Responses (req_id, resp_code, result)"
                         f'VALUES({req_id}, {resp_code}, "{result}")')
        self.conn.commit()

    def updateResponses(self, req_id, resp_code, result):
        self.req.execute(f"UPDATE Responses SET "
                         f'resp_code = {resp_code}, result = "{result}" '
                         f"WHERE id = {req_id}")
        self.conn.commit()

    def deleteFromResponses(self, req_id):
        self.req.execute(f"DELETE FROM Responses WHERE id = {req_id};")
        self.conn.commit()

    def history_show(self):
        print('---Request history---')
        self.req.execute(f"SELECT * FROM Requests")
        x = PrettyTable()
        x.field_names = ['..', 'Method', 'URL', 'Request body', 'Params', 'Headers', 'Status']
        selected = self.req.fetchall()
        num = len(selected)
        if num > 10:
            num = 10
        print(selected)
        for i in range(0, num):
            x.add_row(selected[i])
        print(x.get_string(fields=['..', 'Method', 'URL', 'Request body', 'Params', 'Status']))
        req_id = input('Enter request index to view full info, or "q" to quit: ')
        while req_id != 'q':
            self.selectRequests(int(req_id))
            req_id = input('Enter request index to view full info, or "q" to quit: ')

    def history_clear(self):
        print('---Request history cleared---')
        self.req.execute("DELETE FROM Responses")
        self.req.execute("DELETE FROM Requests")
        self.conn.commit()
