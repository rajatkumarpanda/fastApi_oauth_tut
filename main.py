from fastapi import FastAPI

app = FastAPI()

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

''' Using path and query parameters '''
@app.get("/profile/{userid}/comment")
def profile(userid:int , commentid:int):
    return f"User Id:{userid} and Comment Id:{commentid}"