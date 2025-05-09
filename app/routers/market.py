from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models
from app.deps import get_db

router = APIRouter()

@router.get("/api/v1/public/orderbook/{ticker}")
def get_orderbook(ticker: str, limit: int = 10, db: Session = Depends(get_db)):
    buy_orders = db.query(models.Order).filter_by(ticker=ticker, direction=models.Direction.BUY, status=models.OrderStatus.NEW).order_by(models.Order.price.desc()).limit(limit).all()
    sell_orders = db.query(models.Order).filter_by(ticker=ticker, direction=models.Direction.SELL, status=models.OrderStatus.NEW).order_by(models.Order.price.asc()).limit(limit).all()

    def serialize(orders):
        return [{"price": o.price, "qty": o.qty} for o in orders if o.price is not None]

    return {
        "bid_levels": serialize(buy_orders),
        "ask_levels": serialize(sell_orders)
    }
