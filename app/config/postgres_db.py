from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

# Optimized engine to handle low connection limits on the server
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=5,
    max_overflow=0,
    pool_recycle=300,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_postgres_db():
    Base.metadata.create_all(bind=engine)
