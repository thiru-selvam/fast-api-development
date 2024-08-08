from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url_object = URL.create(drivername="postgresql",
                        username="root",
                        password="Selva@14599",
                        host="127.0.0.1",
                        port=5432,
                        database="fast_api_dev")

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


