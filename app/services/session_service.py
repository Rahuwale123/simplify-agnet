from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.session_model import SessionModel
from datetime import datetime

class SessionService:
    def __init__(self, db: Session):
        self.db = db

    def create_new_session(self, user_id: str) -> str:
        # Find the last session for this user to determine the next sequence number
        last_session = (
            self.db.query(SessionModel)
            .filter(SessionModel.user_id == user_id)
            .order_by(desc(SessionModel.sequence_number))
            .first()
        )

        if last_session:
            next_seq = last_session.sequence_number + 1
        else:
            next_seq = 1

        # Format: user_id_s1, user_id_s2, etc.
        # Note: User request example was "user_d_s1" possibly meaning "user_id" + "_s1".
        # Assuming user_id is providing the base.
        new_session_id = f"{user_id}_s{next_seq}"

        new_session = SessionModel(
            user_id=user_id,
            session_id=new_session_id,
            sequence_number=next_seq,
            created_at=datetime.utcnow()
        )

        self.db.add(new_session)
        self.db.commit()
        self.db.refresh(new_session)
        
        return new_session_id

    def get_user_sessions(self, user_id: str):
        return (
            self.db.query(SessionModel)
            .filter(SessionModel.user_id == user_id)
            .order_by(SessionModel.sequence_number)
            .all()
        )

    def delete_session(self, session_id: str) -> bool:
        session = (
            self.db.query(SessionModel)
            .filter(SessionModel.session_id == session_id)
            .first()
        )
        if session:
            self.db.delete(session)
            self.db.commit()
            return True
        return False

from app.config.postgres_db import get_session
from app.models.session_model import SessionModel

def ensure_session(session_id: str, user_id: str):
    """Ensures a session exists in the database. If not, creates it."""
    # Using a new DB session since this might be called outside dependency injection context
    # Or strict adherence to dependency injection would be better, but for quick fix:
    db = next(get_session()) 
    try:
        session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
        if not session:
            # Create if missing
            new_session = SessionModel(
                user_id=user_id,
                session_id=session_id,
                sequence_number=0, # Unknown sequence
                created_at=datetime.utcnow()
            )
            db.add(new_session)
            db.commit()
            print(f"Created missing session: {session_id}")
    except Exception as e:
        print(f"Error ensuring session: {e}")
    finally:
        db.close()

