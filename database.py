from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql://avnadmin:AVNS_sTQnwTygOzaybZx10dr@pg-5787341-musicly-6d03.i.aivencloud.com:26653/defaultdb?sslmode=require"
print("Подключение к:", DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()