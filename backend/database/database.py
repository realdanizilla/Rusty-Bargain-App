import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import declarative_base - qual das declarative_base é a correta?
from dotenv import load_dotenv


# Loading environment variables
load_dotenv()

# Reading variables from .env file
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Database URL setup
# DATABASE_URL = (
#    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
#    f"@{POSTGRES_HOST}/{POSTGRES_DB}"
# )
DATABASE_URL = 'postgresql://user:password@postgres/rusty_bargain'

print(DATABASE_URL)
# Creating the engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating the declarative base class for the database
Base = declarative_base()

# funcion to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





 