from datetime import datetime
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Boolean

DATABASE_URL = "sqlite:///mydatabase.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("firstname", sqlalchemy.String(50)),
    sqlalchemy.Column("lastname", sqlalchemy.String(50)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
)

products = sqlalchemy.Table(
    "products", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50)),
    sqlalchemy.Column("description", sqlalchemy.String(1000)),
    sqlalchemy.Column("price", sqlalchemy.Float),
)

orders = sqlalchemy.Table(
    "orders", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id')),
    sqlalchemy.Column("date", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.Boolean),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

metadata.create_all(engine)

app = FastAPI()

class UserIn(BaseModel):
    firstname: str = Field(title="First Name", max_length=50)
    lastname: str = Field(title="Last Name", max_length=50)
    email: str = Field(itle="Email", max_length=128)
    password: str = Field(title="Password", max_length=255)

class User(BaseModel):
    id: int
    firstname: str = Field(title="First Name", max_length=50)
    lastname: str = Field(title="Last Name", max_length=50)
    email: str = Field(itle="Email", max_length=128)
    # password: str = Field(title="Password", max_length=255)

class ProductIn(BaseModel):
    name: str = Field(title="Name", max_length=50)
    description: str = Field(default=None, title="Description", max_length=1000)
    price: float = Field(title="Price", gt=0, le=1000000)

class Product(BaseModel):
    id: int
    name: str = Field(title="Name", max_length=50)
    description: str = Field(default=None, title="Description", max_length=1000)
    price: float = Field(title="Price", gt=0, le=1000000)

class OrderIn(BaseModel):
    user_id: int
    product_id: int
    date: datetime = None
    status: bool = Field(title="Status")

class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    date: datetime = None
    status: bool = Field(title="Status")

# Users
@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}

@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(firstname=user.firstname,
                                  lastname=user.lastname,
                                  email=user.email,
                                  password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}

# Products
@app.get("/products/", response_model=List[Product])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)

@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**new_product.dict())
    await database.execute(query)
    return {**new_product.dict(), "id": product_id}

@app.post("/products/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(name=product.name,
                                     description=product.description,
                                     price=product.price)
    last_record_id = await database.execute(query)
    return {**products.dict(), "id": last_record_id}

@app.delete("/products/{product_id}")
async def delete_order(product_id: int):
    query = products.delete().where(products.c.id == product_id,)
    await database.execute(query)
    return {'message': 'Product deleted'}

# Orders
@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)

@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}

@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(user_id=order.user_id,
                                   product_id=order.product_id,
                                   date=order.date,
                                   status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id,)
    await database.execute(query)
    return {'message': 'Order deleted'}

#
# @app.get("/fake_users/{count}")
# async def create_user(count: int):
#     for i in range(count):
#         query = users.insert().values(firstname=f'firstname{i}',
#                                       lastname=f'lastname{i}',
#                                       email=f'mail{i}@gmail.com',
#                                       password=f'password{i}', )
#         await database.execute(query)
#     return {'message': f'{count} fake users create'}
#
# @app.get("/fake_products/{count}")
# async def create_prod(count: int):
#     for i in range(count):
#         query = products.insert().values(name=f'name{i}',
#                                       description=f'description{i}',
#                                       price=count-i,)
#         await database.execute(query)
#     return {'message': f'{count} fake products create'}
#
# @app.get("/fake_orders/{count}")
# async def create_ord(count: int):
#     for i in range(count):
#         query = orders.insert().values(user_id=i,
#                                        product_id=i,
#                                        date=datetime.today(),
#                                        status=True,)
#         await database.execute(query)
#     return {'message': f'{count} fake orders create'}
