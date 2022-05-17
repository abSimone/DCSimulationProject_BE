from array import ArrayType
from ast import Str
from multiprocessing.dummy import Array
from pickletools import string1
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Integer

app = FastAPI()

class Ingredient(BaseModel):
    name: str
    id: Integer

class Pizza(BaseModel):
    name: str
    price: float
    ingredients: Ingredient


@app.get("/pizza")
async def getPizza():
    #GetPizza
    return 1

@app.patch("/pizza/{pizza_id}/update")
async def updatePizza(pizza_id, pizza: Pizza = None):
    #AggiornamentoPizza
    return 1