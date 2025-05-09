from sqlalchemy.orm import Session
from .. import models, schemas
from typing import Optional
from fastapi import APIRouter

from typing import List


router = APIRouter()


# Удаление пользователя
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None

# Пополнение баланса пользователя
def top_up_balance(db: Session, user_id: int, amount: float):
    db_balance = db.query(models.Balance).filter(models.Balance.user_id == user_id).first()
    if db_balance:
        db_balance.amount += amount
        db.commit()
        db.refresh(db_balance)
        return db_balance
    return None

# Списание с баланса пользователя
def withdraw_balance(db: Session, user_id: int, amount: float):
    db_balance = db.query(models.Balance).filter(models.Balance.user_id == user_id).first()
    if db_balance and db_balance.amount >= amount:
        db_balance.amount -= amount
        db.commit()
        db.refresh(db_balance)
        return db_balance
    return None

# Добавление нового торгового инструмента
def add_trading_instrument(db: Session, instrument: schemas.TradingInstrumentCreate) -> models.TradingInstrument:
    db_instrument = models.TradingInstrument(
        name=instrument.name,
        symbol=instrument.symbol,
        type=instrument.type
    )
    db.add(db_instrument)
    db.commit()
    db.refresh(db_instrument)
    return db_instrument

# Делистинг (удаление) торгового инструмента
def delist_trading_instrument(db: Session, instrument_id: int) -> Optional[models.TradingInstrument]:
    db_instrument = db.query(models.TradingInstrument).filter(models.TradingInstrument.id == instrument_id).first()
    if db_instrument:
        db.delete(db_instrument)
        db.commit()
        return db_instrument
    return None
