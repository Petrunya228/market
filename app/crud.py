from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

# Регистрация нового пользователя и выдача токена
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

# Получение баланса пользователя
def get_user_balance(db: Session, user_id: int) -> models.Balance:
    return db.query(models.Balance).filter(models.Balance.user_id == user_id).first()

# Создание рыночной заявки
def create_market_order(db: Session, order: schemas.OrderCreate, user_id: int) -> models.Order:
    db_order = models.Order(
        user_id=user_id,
        order_type="market",
        amount=order.amount,
        price=order.price  # Для рыночной заявки цена может быть динамичной
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# Создание лимитной заявки
def create_limit_order(db: Session, order: schemas.OrderCreate, user_id: int) -> models.Order:
    db_order = models.Order(
        user_id=user_id,
        order_type="limit",
        amount=order.amount,
        price=order.price
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# Получение всех активных заявок
def get_active_orders(db: Session, user_id: int) -> List[models.Order]:
    return db.query(models.Order).filter(models.Order.user_id == user_id, models.Order.status == 'active').all()

# Отмена заявки
def cancel_order(db: Session, order_id: int) -> Optional[models.Order]:
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order and db_order.status == 'active':
        db_order.status = 'cancelled'
        db.commit()
        db.refresh(db_order)
        return db_order
    return None
