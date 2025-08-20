from fastapi import FastAPI
from app.routers import customers
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from app.routers import suppliers
from app.routers import auth as auth_router
from app.routers import admin as admin_router
from app.routers import products as products_router
from app.routers import orders as orders_router
from app.routers import order_items as order_items_router

app = FastAPI(title="shoobydo-api")

app.include_router(customers.router)
