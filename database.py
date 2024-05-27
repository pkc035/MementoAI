from sqlalchemy                 import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm             import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime                   import datetime

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    short_key = Column(String, unique=True, index=True, nullable=False)
    original_url = Column(String, nullable=False)
    expiration_date = Column(DateTime, nullable=True)
    visit_counts = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
