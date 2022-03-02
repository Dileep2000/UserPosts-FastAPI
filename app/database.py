from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL) # connect_args={"check_same_thread": False}

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database connection RAW
# while True:
#   try:
#     conn = psycopg2.connect(host=settings.database_host,database=settings.database_name,user=settings.database_username,password=settings.database_password,cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("Database Connection was successfully")
#     break
#   except Exception as Error:
#     print("There is an Error while connecting to Database")
#     print("Error: ",Error)
#     time.sleep(2)