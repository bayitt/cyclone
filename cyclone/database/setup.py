from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

SQLALCHEMY_DATABASE_URL = f'postgresql://{environ.get("DATABASE_USER")}:{environ.get("DATABASE_PASSWORD")}@{environ.get("DATABASE_HOST")}:{environ.get("DATABASE_PORT")}/{environ.get("DATABASE_NAME")}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
