import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///./debate_system.db")
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread:False"})
else:
    engine=create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,autocommit = False, autoflush=False)

Base = declarative_base()
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()



