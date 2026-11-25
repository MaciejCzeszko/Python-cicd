from sqlalchemy import create_engine
import os
from sqlalchemy.orm import DeclarativeBase, sessionmaker
DB_URL = os.environ["DATABASE_URL"]

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

Base.metadata.create_all(engine)