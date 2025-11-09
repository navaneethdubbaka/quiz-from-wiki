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
# In production, this should be set via environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quiz_generator.db")

# Log database configuration (without sensitive info)
if DATABASE_URL.startswith("postgresql"):
    # Mask password in logs
    safe_url = DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else DATABASE_URL
    print(f"📊 Database: PostgreSQL - {safe_url}")
elif DATABASE_URL.startswith("sqlite"):
    print(f"📊 Database: SQLite - {DATABASE_URL}")
else:
    print(f"📊 Database: Unknown type - {DATABASE_URL[:20]}...")

# Validate DATABASE_URL is set for production
if not DATABASE_URL or DATABASE_URL == "sqlite:///./quiz_generator.db":
    if os.getenv("RENDER") or os.getenv("DATABASE_URL"):
        print("⚠️ WARNING: DATABASE_URL not set or using SQLite in production!")
        print("   Please set DATABASE_URL environment variable to your PostgreSQL connection string")

# Engine and Session
# Use connect_args for SQLite to handle file creation
connect_args = {}
pool_settings = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
elif DATABASE_URL.startswith("postgresql"):
    # PostgreSQL connection pool settings for long-running processes
    connect_args = {}
    pool_settings = {
        "pool_size": 5,  # Connection pool size
        "max_overflow": 10,  # Maximum overflow connections
        "pool_recycle": 3600,  # Recycle connections after 1 hour
    }

try:
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Disable echo in production to reduce logs
        pool_pre_ping=True,
        connect_args=connect_args,
        **pool_settings
    )
    db_type = "PostgreSQL" if DATABASE_URL.startswith("postgresql") else "SQLite"
    print(f"✅ Database engine created: {db_type}")
except Exception as e:
    print(f"⚠️ Database engine creation warning: {e}")
    # Create a minimal engine even if there's an error
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        connect_args=connect_args,
        **pool_settings
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
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")
        # Don't fail if DB init fails (might be connection issue)