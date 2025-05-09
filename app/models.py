from sqlalchemy import Column, String, Integer, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
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
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
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
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    ticker = Column(String, nullable=False)
    qty = Column(Integer, nullable=False)
    price = Column(Integer, nullable=True)  # Если None — это рыночная заявка
    direction = Column(SQLEnum(Direction), nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.NEW)

class Balance(Base):
    __tablename__ = "balances"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    ticker = Column(String, nullable=False)
    amount = Column(Integer, default=0)

class Instrument(Base):
    __tablename__ = "instruments"
    ticker = Column(String, primary_key=True)
    name = Column(String, nullable=False)
