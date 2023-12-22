'''
    Файл с взаимодействием с базой данных, класс имееет функционал:
    1. Подключение - отключение
    2. Создание - удаление таблицы
    3. Добавление записи в таблицу
    4. Получение количества таблиц
    5. Экспорт таблицы
    6. Получение  данных, есть такая таблица в бд или нет
    7. Очистка таблицы

    Оформлен с применением паттерна Singleton
'''
import psycopg2
from psycopg2 import Error
import os
import numpy as np

class Database():
    #Класс базы данных, откуда осуществялется все взаимодействие с ней
    instance = None
    __columns = '(geometry, adress, pothole_class)' #Колонки, в которые ведется запись
    __notTables = '(spatial_ref_sys, raster_columns, raster_overviews, geography_columns, geometry_columns)'

    #Переопределение метода __new__ для создания только одного объекта класса
    def __new__(cls):
        if Database.instance == None:
            Database.instance = super().__new__(cls)
        return Database.instance
    
    def __init__(self):
        self.isConnect = False

    #Подключение к Базе данных
    def connect_to_bd(self, host, user, password, database, port):
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
        
    #Отключение от базы данных
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
                    adress text COLLATE pg_catalog."default" NOT NULL,
                    geometry geometry(Point, 3857),
                    pothole_class SMALLINT);'''
                )
        self.sizeDB, self.tables = Database._getTables(self)

    #Запись данных в таблицу
    def insert_to_table(self, nametable, time_detect, adress='0', latitude=0, longitude=0, pothole_class=1):
        if Database.isInDatabase(self, nametable):
            coordinates = 'Point({} {})'.format(latitude, longitude)
            self.cursor.execute(f'''INSERT INTO {nametable} {Database.__columns} VALUES (%s, %s, %s)''', (coordinates, adress, pothole_class))

    #Получение количества и списка таблиц
    def _getTables(self):
        self.cursor.execute("""SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'""")
        tables = [table[0] for table in self.cursor.fetchall() if not(table[0] in self.__notTables)]
        count = len(tables)
        return count, tables
    
    def getInfoFromTable(self, nameTable):
        self.cursor.execute('''SELECT time_detect, time_add, adress, 
                            ST_AsText(ST_CollectionExtract(geometry)), pothole_class
                             FROM {}
                            ORDER BY adress, pothole_class'''.format(nameTable))
        return self.cursor.fetchall()

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
        
    #Экспорт таблицы 
    def export_table(self, path, name):
        if self.isInDatabase(name):
            query = "SELECT * FROM {}".format(name)
            outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
            with open(os.path.join(path, name + ".csv"), 'w') as f:
                self.cursor.copy_expert(outputquery, f)

    #Очистка таблицы
    def clear_table(self, name):
        if self.isInDatabase(name):
            query = "DELETE FROM {}".format(name)
            self.cursor.execute(query)
            return True
        return False

