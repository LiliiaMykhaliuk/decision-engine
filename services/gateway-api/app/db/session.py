from libs.decision_db.session_factory import create_session_factory
from app.core.config import settings

SessionLocal = create_session_factory(settings.database_url)

def get_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
