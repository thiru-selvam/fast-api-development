from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base

from ..config import settings

url_object = URL.create(drivername=settings.database_driver,
                        username=settings.database_username,
                        password=settings.database_password,
                        host=settings.database_hostname,
                        port=settings.database_port,
                        database=settings.database_name)

# SQLALCHEMY_DATABASE_URL = 'postgresql://root:Selva@14599@localhost/fast_api_dev'

engine = create_engine(url_object)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
