import mysql.connector as mysql
from mysql.connector import Error

class Mysql_utility:
    connetion = None

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    @property
    def host(self):
         return self.__host
    @host.setter
    def host(self,host):
        self.__host=host

    @property
    def database(self):
         return self.__database
    @database.setter
    def database(self,database):
        self.__database=database

    @property
    def user(self):
         return self.__user
    @user.setter
    def user(self,user):
        self.__user=user

    @property
    def password(self):
         return self.__password
    @password.setter
    def password(self,password):
        self.__password=password     
    
    def open_connection(self):
        try:
            connection = mysql.connect(host = self.host, database = self.database, user = self.user, password = self.password)
            self.cursor = connection.cursor()
            self.conn = connection
            print('Aperta connessione al db')
            return self.conn, self.cursor
        except Error as e:
            print('Error: ', e)

    def query(self, query):
            self.cursor.execute(query)
            return self.cursor
    
    def commit(self):
            self.conn.commit()
            return self.conn

    def close_connection(self):
        try:
            self.cursor.close()
            self.conn.close()
            print('Chiusa connessione al db')
        except Error as e:
            print('Error: ', e)

    # def create(self):
    #     try:
    #         factory = Mysql_utility('localhost','pizzeria_db','root','Andrea.99')
    #         connection = factory.open_connection()
    #     except Error as e:
    #         print('Error: ', e)
    #     finally:
    #         self.connection = connection