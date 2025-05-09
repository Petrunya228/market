from sqlalchemy import Column, String, Integer, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from enum import Enum
from app.database import Base

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))  # Заменили UUID на String(36)
    name = Column(String, nullable=False)
    api_key = Column(String, unique=True, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)

class OrderStatus(str, Enum):
    NEW = "NEW"
    EXECUTED = "EXECUTED"
    PARTIALLY_EXECUTED = "PARTIALLY_EXECUTED"
    CANCELLED = "CANCELLED"

class Direction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class Order(Base):
    __tablename__ = "orders"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))  # Заменили UUID на String(36)
    user_id = Column(String(36), ForeignKey("users.id"))  # Заменили UUID на String(36)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ticker = Column(String, nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Integer, nullable=True)  # Если None — это рыночная заявка
    direction = Column(SQLEnum(Direction), nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.NEW)

class Balance(Base):
    __tablename__ = "balances"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))  # Заменили UUID на String(36)
    user_id = Column(String(36), ForeignKey("users.id"))  # Заменили UUID на String(36)
    ticker = Column(String, nullable=False)
    amount = Column(Integer, default=0)

class Instrument(Base):
    __tablename__ = "instruments"
    ticker = Column(String, primary_key=True)
    name = Column(String, nullable=False)

class TradingInstrument(Base):
    __tablename__ = 'trading_instruments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
