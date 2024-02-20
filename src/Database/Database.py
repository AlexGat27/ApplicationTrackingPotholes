from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
)

class Base(DeclarativeBase):
    pass