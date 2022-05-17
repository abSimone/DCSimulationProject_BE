from array import ArrayType
import json
from multiprocessing.dummy import Array
from pickletools import string1
from click import UUID
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from db_utilities.singleton_db import DBConnection
from fastapi.middleware.cors import CORSMiddleware
import uuid

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Ingredient(BaseModel):
    name: str
    id: int

class Pizza(BaseModel):
    guid: str
    name: str
    price: float
    ingredients: Ingredient

class create_dict(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value

@app.get("/pizza")
async def getPizza():
    #GetPizza
    db = DBConnection()

    queryGet = 'select * from pizze' #aggiungere alias
    queryRes = db.query(queryGet).fetchall()

    res = []
    for row in queryRes:
        toReturnDict = create_dict()
        toReturnDict.add("id_pizza",row[0])
        toReturnDict.add("nome",row[1])
        toReturnDict.add("costo",row[2])
        res.append(toReturnDict)

    return JSONResponse({"data" : res})

@app.get("/pizza/{pizza_id}")
async def getSomePizza(pizza_id):
    #GetCertainPizza
    db = DBConnection()

    query = f'select i.ID_ingrediente ,i.nome from pizze p,ingredienti i, pizza_ingrediente pi where i.ID_ingrediente = pi.FK_ingrediente and pi.FK_pizza = p.ID_pizza and p.ID_pizza = {pizza_id}'
    queryIngr = db.query(query).fetchall()
    
    ingredienti = []
    
    for el in queryIngr:
        ingredienti.append(
            {'id': el[0],
            'nome': el[1]}
        )

    queryGet = f'select pizze.nome, pizze.costo, i.nome from pizze, ingredienti i where pizze.ID_pizza = {pizza_id}' #aggiungere alias
    queryRes = db.query(queryGet).fetchall()
    res = {
        "data":{
            "nome" : queryRes[0][0],
            "costo" : queryRes[0][1],
            "ingredienti" : ingredienti
        }
    }
    
    return JSONResponse(res)

@app.get("/ingrediente/{pizza_id}")
async def getIngredienti(pizza_id):
    #GetPizzaIngredients
    db = DBConnection()

    queryGet = f'select i.nome from ingredienti as i inner join pizza_ingrediente as pi on i.ID_ingrediente = pi.FK_ingrediente inner join pizze as p on pi.FK_pizza = p.ID_pizza where ID_pizza = {pizza_id}'
    queryRes = db.query(queryGet).fetchall()

    json_compatible_item_data = jsonable_encoder(queryRes)
    return JSONResponse(content=json_compatible_item_data)

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