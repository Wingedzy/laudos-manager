from sqlalchemy.orm import sessionmaker
from app.config import engine

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()