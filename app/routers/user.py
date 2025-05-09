from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app import models, schemas
from app.database import SessionLocal
from app.deps import get_current_user


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/api/v1/public/register", response_model=schemas.UserOut)
def register_user(user: schemas.NewUser, db: Session = Depends(get_db)):
    # Генерация уникального api_key
    api_key = f"key-{uuid4()}"

    # Проверка на существование пользователя с таким же email
    if db.query(models.User).filter(models.User.api_key == api_key).first():
        raise HTTPException(status_code=400, detail="API key collision, please try again")

    # Создание нового пользователя
    db_user = models.User(name=user.name, api_key=api_key)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/api/v1/balance")
def get_balances(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    balances = db.query(models.Balance).filter_by(user_id=user.id).all()

    # Если баланс не найден, возвращаем ошибку
    if not balances:
        raise HTTPException(status_code=404, detail="No balances found for this user")

    result = {b.ticker: b.amount for b in balances}

    # Возвращаем данные баланса пользователя
    return result
