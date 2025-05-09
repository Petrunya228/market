from fastapi import FastAPI
from app.routers import user, order, admin, market
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(order.router)
app.include_router(admin.router)
app.include_router(market.router)
