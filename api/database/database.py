from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

config = dotenv_values('../.env')

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