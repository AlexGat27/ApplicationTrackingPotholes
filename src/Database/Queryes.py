'''
    Файл с взаимодействием с базой данных, класс имееет функционал:
    1. Подключение - отключение
    2. Создание - удаление таблицы
    3. Добавление записи в таблицу
    4. Получение количества таблиц
    5. Экспорт таблицы
    6. Получение  данных, есть такая таблица в бд или нет
    7. Очистка таблицы

'''
from sqlalchemy import create_engine, text, func, Column, Integer, String, DateTime, MetaData
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
import os

Base: DeclarativeMeta = declarative_base()

class SyncCore():
    __columns = '(created_at, crs3857, crs4326, image_path)' #Колонки, в которые ведется запись
    __notTables = '(spatial_ref_sys, raster_columns, raster_overviews, geography_columns, geometry_columns)'
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        self.isConnect = False
        self.engine = None
        self.sizeDB = 0
        self.tables = []

    #Подключение к Базе данных
    def connect_to_bd(self, host, user, password, databaseName, port):
        if self.isConnect == False:
            try:
                self.engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host}:{port}/{databaseName}")
                self.isConnect = True
                self.Session = sessionmaker(bind=self.engine)
                self.metadata = MetaData()
                self.metadata.reflect(bind=self.engine)
                self.sizeDB, self.tables = self.getTables()
                return "Connection to database {} is succesfuly".format(databaseName)
            except Exception as error:
                return "[Info] Error while working with PostgreSQL: {}".format(error)
        else: return "Подключение уже есть, разорвите соединение"
        
    #Отключение от базы данных
    def disconnect_from_bd(self):
        self.engine.dispose()
        self.isConnect = False

    # Создание таблицы
    def create_table(self, names: str):
        name_list = names.split()
        for name in name_list:
            if not(self.isInDatabase(name)):
                class PotholeTable(Base):
                    __tablename__ = name
                    id = Column(Integer, primary_key=True)
                    created_at = Column(DateTime)
                    crs4326 = Column(Geometry('POINT'))
                    crs3857 = Column(Geometry('POINT'))
                    image_path = Column(String(256))
                PotholeTable.__table__.create(bind=self.engine, checkfirst=True)
        self.metadata.reflect(bind=self.engine)
        self.sizeDB, self.tables = self.getTables()

    #Запись данных в таблицу
    def insert_potholes(self, nametable: str, crs3857: dict, crs4326: dict, image_path: str):
        if self.isInDatabase(nametable):
            session = self.Session()
            crs3857 = "SRID=3857;POINT({} {})".format(crs3857['x'], crs3857['y'])
            crs4326 = "SRID=4326;POINT({} {})".format(crs4326['lat'], crs4326['lon'])
            query = f'''INSERT INTO {nametable} {self.__columns} VALUES ('{datetime.now()}', ST_GeomFromText('{crs3857}'), ST_GeomFromText('{crs4326}'), '{image_path}')'''
            session.execute(text(query))
            session.commit()
            session.close()

    #Получение количества и списка таблиц
    def getTables(self):
        print(self.metadata.tables.keys())
        return len(self.metadata.tables), list(self.metadata.tables.keys())

    #Удаление таблицы
    def drop_table(self, names):
        names_list = names.split()
        for name in names_list:
            self.metadata.tables[name].drop(bind=self.engine)
            self.metadata.remove(self.metadata.tables[name])  # Удаляем таблицу из метаданных
        self.sizeDB, self.tables = self.getTables()

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
            with self.engine.connect() as connection:
                query = f"DELETE FROM {name}"
                connection.execute(text(query))
            return True
        return False

