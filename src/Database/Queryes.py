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
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker
import datetime
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
import os

Base: DeclarativeMeta = declarative_base()

class SyncCore():
    __columns = '(geomCRS3857, geomCRS4326, image_path)' #Колонки, в которые ведется запись
    __notTables = '(spatial_ref_sys, raster_columns, raster_overviews, geography_columns, geometry_columns)'
    
    def __init__(self):
        self.isConnect = False

    #Подключение к Базе данных
    def connect_to_bd(self, host, user, password, databaseName, port):
        try:
            self.engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host}:{port}/{databaseName}")
            self.isConnect = True
            self.Session = sessionmaker(bind=self.engine)
            self.metadata = MetaData(bind=self.engine)
            Base.metadata.bind = self.engine
            self.sizeDB, self.tables = self.getTables(self)
            return "Connection to database {} is succesfuly".format(databaseName)
        except Exception as error:
            return "[Info] Error while working with PostgreSQL: {}".format(error)
        
    #Отключение от базы данных
    def disconnect_from_bd(self):
        self.engine.dispose()
        self.isConnect = False

    # Создание таблицы
    def create_table(self, names):
        name_list = names.split()
        for name in name_list:
            if not(self.isInDatabase(self, name)):
                class PotholeTable(Base):
                    __tablename__ = name
                    id = Column(Integer, primary_key=True)
                    created_at = Column(DateTime, default=datetime.utcnow)
                    crs4326 = Column(Geometry('POINT'))
                    crs3857 = Column(Geometry('POINT'))
                    image_path = Column(String("256"))
            PotholeTable.__tablename__.create(bind=self.engine, checkfirst=True)
        self.sizeDB, self.tables = self.getTables(self)

    #Запись данных в таблицу
    def insert_to_table(self, nametable: str, crs3857: dict, crs4326: dict, image_path: str):
        if self.isInDatabase(self, nametable):
            crs3857 = 'Point({} {})'.format(crs3857['x'], crs3857['y'])
            crs4326 = 'Point({} {})'.format(crs4326['lat'], crs4326['lon'])
            self.cursor.execute(f'''INSERT INTO {nametable} {Database.__columns} VALUES (%s, %s, %s)''', (crs3857, crs4326, image_path))

    #Получение количества и списка таблиц
    def getTables(self):
        return len(self.metadata.tables), self.metadata.tables.keys

    #Удаление таблицы
    def drop_table(self, names):
        names_list = names.split()
        for name in names_list:
            Base.metadata.tables[name].drop()
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
                connection.execute(query)
            return True
        return False

