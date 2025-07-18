from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///db.sqlite3", echo=True)
SessionLocal = sessionmaker(bind=engine)

JWT_SETTINGS = {
    "secret_key": "strongKey",
    "algorithm": "HS256",
    "access_exp_minutes": 180,
    "refresh_exp_days": 7,
}

Base = declarative_base()
