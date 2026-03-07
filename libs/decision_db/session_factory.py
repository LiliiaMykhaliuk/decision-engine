from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_session_factory(database_url: str):
    engine = create_engine(
        database_url,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
    )
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)
