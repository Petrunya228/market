from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import uuid4
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class NewUser(BaseModel):
    name: str = Field(..., min_length=3)

class UserOut(BaseModel):
    id: str  # Заменили UUID на str
    name: str
    api_key: str
    role: UserRole

    class Config:
        orm_mode = True

class Direction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(str, Enum):
    NEW = "NEW"
    EXECUTED = "EXECUTED"
    PARTIALLY_EXECUTED = "PARTIALLY_EXECUTED"
    CANCELLED = "CANCELLED"

class MarketOrderBody(BaseModel):
    direction: Direction
    ticker: str
    qty: int

class LimitOrderBody(MarketOrderBody):
    price: int

class CreateOrderResponse(BaseModel):
    success: bool = True
    order_id: str  # Заменили UUID на str

class OrderOut(BaseModel):
    id: str  # Заменили UUID на str
    timestamp: datetime
    ticker: str
    qty: int
    price: Optional[int]
    direction: Direction
    status: OrderStatus

    class Config:
        orm_mode = True

class BalanceOut(BaseModel):
    ticker: str
    amount: int

class InstrumentIn(BaseModel):
    ticker: str
    name: str

class InstrumentOut(InstrumentIn):
    class Config:
        orm_mode = True

class TradingInstrumentCreate(BaseModel):
    name: str
    symbol: str
