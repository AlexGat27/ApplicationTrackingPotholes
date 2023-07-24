from ultralytics import YOLO
import psycopg2
from psycopg2 import Error
from datetime import datetime, timezone
import random
import os

#Осуществялется с паттерном "Одиночка"
class Database():
    instance = None
    default_parametres_BD = {'host':'127.0.0.1', 'user':'postgres', 'password':'Shurikgat2704', 'database':'postgres', 'port':'5432'}
    __columns = '(time_detect, time_add, adress, latitude, longitude, pothole_class)' #Колонки, в которые ведется запись

    def __new__(cls):
        if Database.instance == None:
            Database.instance = super().__new__(cls)
        return Database.instance
    
    def __init__(self):
        self.isConnect = False

    #Подключение к Базе данных
    def connect_to_bd(self, host='127.0.0.1', user='postgres', password='Shurikgat2704', database='postgres', port='5432'):
        try:
            self.connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.sizeDB, self.tables = Database._getTables(self)
            self.isConnect = True
            return "Connection to database {} is succesfuly".format(database)
        except (Exception, Error) as error:
            return "[Info] Error while working with PostgreSQL: {}".format(error)
        
    def disconnect_from_bd(self):
        self.cursor.close()
        self.connection.close()
        self.isConnect = False

    # Создание таблицы
    def create_table(self, names):
        name_list = names.split()
        for name in name_list:
            if not(Database.isInDatabase(self, name)):
                self.cursor.execute(
                    f'''create table {name}
                    (id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
                    time_detect TIMESTAMP,
                    time_add TIMESTAMP,
                    adress text COLLATE pg_catalog."default" NOT NULL,
                    latitude numeric NOT NULL,
                    longitude numeric NOT NULL,
                    pothole_class integer NOT NULL);'''
                )
        self.sizeDB, self.tables = Database._getTables(self)

    #Запись данных в таблицу
    def insert_to_table(self, nametable, adress='0', latitude=0, longitude=0, pothole_class=0):
        if Database.isInDatabase(self, nametable):
            today = datetime.now()
            time_detect = datetime.today()
            self.cursor.execute(f'''INSERT INTO {nametable} {Database.__columns} VALUES (%s, %s, %s, %s, %s, %s)''', (time_detect, today, adress, latitude, longitude, pothole_class))

    #Получение количества и списка таблиц
    def _getTables(self):
        self.cursor.execute("""SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'""")
        tables = [table[0] for table in self.cursor.fetchall()]
        count = len(tables)
        return count, tables

    #Удаление таблицы
    def drop_table(self, names):
        names_list = names.split()
        for name in names_list:
            if name in self.tables:
                query = "drop table {}".format(name)
                self.cursor.execute(query)
        self.sizeDB, self.tables = self._getTables()

    #Проверка существования таблицы в БД
    def isInDatabase(self, nametable):
        if nametable in self.tables:
            return True
        else:
            return False
        
    def export_table(self, path, name):
        if self.isInDatabase(name):
            query = "SELECT * FROM {}".format(name)
            outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
            with open(os.path.join(path, name + ".csv"), 'w') as f:
                self.cursor.copy_expert(outputquery, f)


