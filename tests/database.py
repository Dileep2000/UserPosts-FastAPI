# import alembic
# from fastapi.testclient import TestClient
# from app.database import get_db, Base
# from app.main import app
# from app.config import settings
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import pytest
# from alembic import command


# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}_test"

# engine = create_engine(SQLALCHEMY_DATABASE_URL) # connect_args={"check_same_thread": False}

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # def overide_get_db():
# #   db = TestingSessionLocal()
# #   try:
# #     yield db
# #   finally:
# #     db.close()

# # app.dependency_overrides[get_db] = overide_get_db

# @pytest.fixture()
# def session():
#   Base.metadata.drop_all(bind=engine)
#   Base.metadata.create_all(bind=engine)
#   db = TestingSessionLocal()
#   try:
#     yield db
#   finally:
#     db.close()

# @pytest.fixture()
# def client(session):
#   def overide_get_db():
#     try:
#       yield session
#     finally:
#       session.close()
#   app.dependency_overrides[get_db] = overide_get_db
#   # command.upgrade("head")
#   #before the code runs
#   yield TestClient(app)
#   #after the code runs
#   # command.downgrade("base")