from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from app import models, schemas
from app.deps import get_current_user, get_db
from typing import Union

router = APIRouter()

@router.post("/api/v1/order", response_model=schemas.CreateOrderResponse)
def create_order(
    body: Union[schemas.MarketOrderBody, schemas.LimitOrderBody],
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    is_limit = hasattr(body, "price")
    order = models.Order(
        id=uuid4(),
        user_id=user.id,
        ticker=body.ticker,
        qty=body.qty,
        price=getattr(body, "price", None),
        direction=body.direction,
        status=models.OrderStatus.NEW,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    if not is_limit:
        # Выполнение рыночной заявки (упрощённо)
        opposite = models.Direction.SELL if body.direction == models.Direction.BUY else models.Direction.BUY
        orders = db.query(models.Order).filter_by(ticker=body.ticker, direction=opposite, status=models.OrderStatus.NEW)
        if body.direction == models.Direction.BUY:
            orders = orders.order_by(models.Order.price.asc())
        else:
            orders = orders.order_by(models.Order.price.desc())

        for match in orders:
            if match.qty >= body.qty:
                match.qty -= body.qty
                match.status = models.OrderStatus.EXECUTED if match.qty == 0 else models.OrderStatus.PARTIALLY_EXECUTED
                order.status = models.OrderStatus.EXECUTED
                db.commit()
                break

    return schemas.CreateOrderResponse(order_id=order.id)

@router.get("/api/v1/order")
def list_orders(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter_by(user_id=user.id).all()
    return orders

@router.get("/api/v1/order/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: str, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(models.Order).filter_by(id=order_id, user_id=user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.delete("/api/v1/order/{order_id}")
def cancel_order(order_id: str, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(models.Order).filter_by(id=order_id, user_id=user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = models.OrderStatus.CANCELLED
    db.commit()
    return {"success": True}
