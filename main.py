from array import ArrayType
from multiprocessing.dummy import Array
from pickletools import string1
from click import UUID
from fastapi import FastAPI
from pydantic import BaseModel
from mysqlconn import Mysql_utility
import uuid

app = FastAPI()

class Ingredient(BaseModel):
    name: str
    id: int

class Pizza(BaseModel):
    guid: str
    name: str
    price: float
    ingredients: Ingredient


@app.get("/pizza")
async def getPizza():
    #GetPizza
    factory = Mysql_utility('localhost','pizzeria_db','root','Andrea.99')
    factory.open_connection()

    queryGet = 'select pizze.nome from pizze'
    queryRes = factory.query(queryGet).fetchall()

    factory.close_connection()
    return queryRes

@app.post("/pizza/create")
async def createPizza(pizza_id, pizza: Pizza = None):
    #CreazionePizza
    idPizza = uuid.uuid4()
    Mysql_utility.open_connection
    
@app.patch("/pizza/{pizza_id}/update")
async def updatePizza(pizza_id, pizza: Pizza = None):
    #AggiornamentoPizza
    return 1