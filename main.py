from fastapi import FastAPI,Form
from pydantic import BaseModel,Field,HttpUrl
from typing import Set,List
from uuid import UUID
from datetime import date,datetime,time, timedelta

class Event(BaseModel):
    event_id: UUID
    start_date: date
    start_time: datetime
    end_time: datetime
    expire_time: time
    delta: timedelta

class Profile(BaseModel):
    name: str
    email: str
    age: int

''' Nest inside another model'''
class Image(BaseModel):
    url: HttpUrl #Accepts URL
    name: str

class Product(BaseModel):
    name: str = Field(example="phone")
    price: int = Field(title="This is the price of the product", description="This would be the price of the product being added",gt=0)
    discount: int
    discounted_price: float
    tags: Set[str] = [] # Accepts only unique strings
    image: List[Image] # Accepts list of images

    ''' Add example for referance'''
    # class Config:
    #     schema_extra={
    #         "example":{
    #                     "name": "Phone",
    #                     "price": 100,
    #                     "discount": 10,
    #                     "discounted_price": 0,
    #                     "tags": ["electronic","computers"],
    #                     "image": [
    #                             {
    #                             "url": "https://image1.com",
    #                             "name": "Phone"
    #                             },
    #                             {
    #                             "url": "https://image2.com",
    #                             "name": "Phone side view"
    #                             }
    #                         ]
    #                     }
    #     }

class Offers(BaseModel):
    name: str
    prodcuts: List[Product]

class User(BaseModel):
    name: str
    email: str

app = FastAPI()

''' Use form to take input '''
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"Username": username}

@app.post("/addevent")
def addevent(event: Event):
    return {event}

''' Deeply nested models '''
@app.post("/addproduct")
def addproduct(offers: Offers):
    return {offers}


'''Passing multiple models'''
@app.post("/purchase")
def purchase(user: User, product: Product):
    return{"User": user, "Product": product}

''' Passing qurey parameters, pydantic model, path parameter'''
@app.post("/addprodcut/{product_id}")
def addProduct(product: Product, product_id: int, category: str):
    product.discounted_price = product.price - (product.price*product.discount)/100
    return {"product_id":product_id, "Product":product, "Category":category}

@app.get("/")
def index():
    return "Hello World!!"


''' Path parameter with type '''
@app.get("/property/{id}")
def property(id: int):
    return f"property {id}"

''' Static Path '''
@app.get("/profile/admin")
def admin():
    return "This is admin page"

''' Path parameter, Dynamic Path '''
@app.get("/profile/{username}")
def profile(username: str):
    return f"Username: {username}"


''' Query parameter
Eg: /product?id=1&price=10'''
@app.get("/product")
def product(id:int = None,price:int = None):
    return f"The product id: {id} and price: {price}"

@app.post("/adduser")
def adduser(profile:Profile):
    return profile

''' Using path and query parameters '''
# @app.get("/profile/{userid}/comment")
# def profile(userid:int , commentid:int):
#     return f"User Id:{userid} and Comment Id:{commentid}"