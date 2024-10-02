'''
Class for easy interaction with the database

'''

import MySQLdb as sql

class db:
    def __init__(self):
        self.connection = sql.connect()

    def execute(query,self):
        self.connection.execute()
