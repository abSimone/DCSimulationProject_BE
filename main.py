from array import ArrayType
from multiprocessing.dummy import Array
from pickletools import string1
from click import UUID
from fastapi import FastAPI
from pydantic import BaseModel
from db_utilities.singleton_db import DBConnection
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
    db = DBConnection()

    queryGet = 'select pizze.nome, pizze.costo from pizze'
    queryRes = db.query(queryGet).fetchall()

    return queryRes

@app.get("/pizza/{pizza_id}")
async def getPizza(pizza_id):
    #GetPizza
    db = DBConnection()

    queryGet = f'select pizze.nome, pizze.costo from pizze where pizze.ID_pizza = {pizza_id}'
    queryRes = db.query(queryGet).fetchall()

    return queryRes

@app.post("/pizza/create")
async def createPizza(pizza_id, pizza: Pizza = None):
    #CreazionePizza
    #idPizza = uuid.uuid4()
    #Mysql_utility.open_connection
    return 1
    
@app.patch("/pizza/{pizza_id}/update")
async def updatePizza(pizza_id, pizza: Pizza = None):
    #AggiornamentoPizza
    return 1