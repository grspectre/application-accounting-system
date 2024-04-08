from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
import os
import sys

api_dir = os.path.join(os.path.dirname(__file__), '..')
env_path = os.path.join(os.path.abspath(api_dir), '.env')
config = dotenv_values(env_path)

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}/{}".format(
    config.get('POSTGRES_USER', 'postgres'),
    config.get('POSTGRES_PWD', 'postgres'),
    config.get('POSTGRES_DOMAIN', 'localhost'),
    config.get('POSTGRES_DB', 'postgres')
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
