from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Product(BaseModel):
    name:str
    price:float
    in_stock :bool = True

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/hello")
def hello():
    return {"message": "Welcome to Data Engineering"}


@app.post("/products")מנ
def create_product(product: Product):
    return product

@app.get("/divide")
def divide(a: int, b: int):
    result = a / b
    return {"result": result}