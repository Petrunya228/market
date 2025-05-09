from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)) -> models.User:
    if not authorization.startswith("TOKEN "):
        raise HTTPException(status_code=403, detail="Invalid token format")
    token = authorization.removeprefix("TOKEN ")
    user = db.query(models.User).filter_by(api_key=token).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid token")
    return user


