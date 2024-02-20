import datetime
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PotholesORM(Base):

    def __init__(self, nametable: str):
        self.__tablename__ = nametable

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    crs4326 = Column(Geometry('POINT'))
    crs3857 = Column(Geometry('POINT'))
    image_path = Column(String("256"))
