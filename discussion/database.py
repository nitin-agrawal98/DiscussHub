from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config_parser.config import config
from models.base import Base

engine = create_engine(config["db"]["uri"])
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
session = Session()


def init_db():
    Base.metadata.create_all(bind=engine)
