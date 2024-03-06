import mysql.connector
import dotenv
import os

class Connector_dataBase():
    def __init__(self) -> None:
        dotenv.load_dotenv('.env')

        self.host = os.getenv('host')
        self.database = os.getenv('database')
        self.user = os.getenv('user')
        self.password = os.getenv('password')
        self.connection = None

        

    def connection_dataBase(self):
        if self.connection and self.connection.is_connected():
            print('Previamente conectado')
        else:
            self.connection = mysql.connector.connect(host = self.host,
                                             database = self.database,
                                             user = self.user,
                                             password = self.password)
        if self.connection.is_connected():
            db_info = self.connection.get_server_info()
            print(f'Conexão bem sucessida ao MySql Server: {db_info}')
            

        #self.connection.close()


    
# connection = Connector_dataBase()
# connection.connection_dataBase()