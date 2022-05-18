import mysql.connector as mysql
from mysql.connector import Error
from .config import config

class DBConnection:
    instance = None
    con = None
    cursor = None

    def __new__(cls):
        if DBConnection.instance is None:
            DBConnection.instance = object.__new__(cls)
        return DBConnection.instance

    def __init__(self):
        if DBConnection.con is None:
            try:
                __db_config = config['mysql']
                DBConnection.con = mysql.connect(host = __db_config['host'], database = __db_config['db'], user = __db_config['user'], password = __db_config['password'])
                self.cursor = DBConnection.con.cursor()
                #print('aperta connessione')
            except Error as e:
                print('Error: ', e)
    
    def query(self, query):
            self.cursor.execute(query)
            return self.cursor
    
    def commit(self):
        self.con.commit()
    

    def __del__(self):
        if DBConnection.con is not None:
            DBConnection.con.close()
            #print('chiusa connessione')