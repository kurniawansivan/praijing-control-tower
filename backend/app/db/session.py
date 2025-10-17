from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# SQLAlchemy Database URL
SQLALCHEMY_DATABASE_URL = settings.database_url

# Create engine and session maker
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "option": "-csearch_path=public"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()
