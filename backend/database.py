# database.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables
load_dotenv()

# Database configuration
# DB_USER = os.getenv("DB_USER", "postgres")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "")
# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_PORT = os.getenv("DB_PORT", "5432")
# DB_NAME = os.getenv("DB_NAME", "quiz_generator_db")

# # Database URL
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Default to SQLite if DATABASE_URL is not set (for local dev)
# In production/Vercel, this should be set via environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quiz_generator.db")

# Engine and Session
# Use connect_args for SQLite to handle file creation
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

try:
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Disable echo in production to reduce logs
        pool_pre_ping=True,
        connect_args=connect_args
    )
except Exception as e:
    print(f"⚠️ Database engine creation warning: {e}")
    # Create a minimal engine even if there's an error
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        connect_args=connect_args
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Quiz Model
class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    url = Column(String(500), nullable=False, unique=True)
    title = Column(String(300), nullable=False)
    date_generated = Column(DateTime, default=datetime.utcnow, nullable=False)
    scraped_content = Column(Text, nullable=True)
    full_quiz_data = Column(Text, nullable=False)
    
    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}', url='{self.url}')>"


# Initialize database
def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")