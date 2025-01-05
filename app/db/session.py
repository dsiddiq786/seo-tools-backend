from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings  # Ensure this matches the actual path
from sqlalchemy.ext.declarative import declarative_base

# Create the database engine
engine = create_engine(settings.DATABASE_URL)

# Session for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define Base for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()