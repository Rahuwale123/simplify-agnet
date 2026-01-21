from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from app.config.postgres_db import Base

class SessionModel(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    session_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # We might want to store the sequence number explicitly to make it easier to find the next one
    sequence_number = Column(Integer)
