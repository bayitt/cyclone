from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

from ..utilities.env import load_env

load_env()

SQLALCHEMY_DATABASE_URL = f'postgresql://{environ.get("DATABASE_USER")}:{environ.get("DATABASE_PASSWORD")}@{environ.get("DATABASE_HOST")}:{int(environ.get("DATABASE_PORT"))}/{environ.get("DATABASE_NAME")}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=3, pool_recycle=1800)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
