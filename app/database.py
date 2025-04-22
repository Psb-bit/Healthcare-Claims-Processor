# DB connection config
# DB connection config

from sqlalchemy import create_engine  # to connect to the database
from sqlalchemy.orm import declarative_base
  # base class for models
from sqlalchemy.orm import sessionmaker  # handles DB sessions

# PostgreSQL connection string
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/claims_db"

# Creating the SQLAlchemy engine (connection to the DB)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Each instance of SessionLocal will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models to inherit from
Base = declarative_base()

# ✅ Dependency to get a DB session for FastAPI or testing
def get_db():
    """
    Yields a SQLAlchemy database session.
    Ensures that each session is closed after the request or test is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

