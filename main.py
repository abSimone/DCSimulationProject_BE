from array import ArrayType
import json
from multiprocessing.dummy import Array
from pickletools import string1
from typing import List
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


class Ingrediente(BaseModel):
    nome: str
    id: int


class Pizza(BaseModel):
    nome: str
    costo: float
    ingredienti: List[Ingrediente]


class create_dict(dict):

    # __init__ function
    def __init__(self):
        self = dict()

    # Function to add key:value
    def add(self, key, value):
        self[key] = value


@app.get("/pizza")
async def getPizza():
    # GetPizza
    db = DBConnection()

    queryGet = 'select * from pizze'  # aggiungere alias
    queryRes = db.query(queryGet).fetchall()

    res = []
    for row in queryRes:
        toReturnDict = create_dict()
        toReturnDict.add("id_pizza", row[0])
        toReturnDict.add("nome", row[1])
        toReturnDict.add("costo", row[2])
        res.append(toReturnDict)

    return JSONResponse({"data": res})


@app.get("/pizza/{pizza_id}")
async def getSomePizza(pizza_id):
    # GetCertainPizza
    db = DBConnection()

    query = f'select i.ID_ingrediente ,i.nome from pizze p,ingredienti i, pizza_ingrediente pi where i.ID_ingrediente = pi.FK_ingrediente and pi.FK_pizza = p.ID_pizza and p.ID_pizza = {pizza_id}'
    queryIngr = db.query(query).fetchall()

    ingredienti = []

    for el in queryIngr:
        ingredienti.append(
            {'id': el[0],
             'nome': el[1]}
        )

    # aggiungere alias
    queryGet = f'select pizze.nome, pizze.costo, i.nome from pizze, ingredienti i where pizze.ID_pizza = {pizza_id}'
    queryRes = db.query(queryGet).fetchall()
    res = {
        "data": {
            "nome": queryRes[0][0],
            "costo": queryRes[0][1],
            "ingredienti": ingredienti
        }
    }

    return JSONResponse(res)


@app.get("/ingrediente")
async def getIngredienti():
    # getIngredients
    db = DBConnection()

    queryGet = 'select * from ingredienti'
    queryRes = db.query(queryGet).fetchall()

    ingredienti = []
    for tuple in queryRes:
        ingredienti.append({"id": tuple[0], "nome": tuple[1]})

    res = {
        "data": ingredienti
    }

    return JSONResponse(res)


@app.get("/ingrediente/{pizza_id}")
async def getIngredientiPizza(pizza_id):
    # GetPizzaIngredients
    db = DBConnection()

    queryGet = f'select i.nome from ingredienti as i inner join pizza_ingrediente as pi on i.ID_ingrediente = pi.FK_ingrediente inner join pizze as p on pi.FK_pizza = p.ID_pizza where ID_pizza = {pizza_id}'
    queryRes = db.query(queryGet).fetchall()

    json_compatible_item_data = jsonable_encoder(queryRes)
    return JSONResponse(content=json_compatible_item_data)


@app.post("/pizza/aggiungi")
async def createPizza(pizza: Pizza):
    db = DBConnection()
    queryPost = f'insert into pizze(nome, costo) values("{pizza.nome}", {pizza.costo})'
    db.query(queryPost)
    db.commit()
    queryGet = f'select id_pizza from pizze where nome = "{pizza.nome}"'
    nuovaPizzaId = db.query(queryGet).fetchone()
    relazionaPizzaIngredienti = f'insert into pizza_ingrediente values'
    for i in pizza.ingredienti:
        relazionaPizzaIngredienti += f'({nuovaPizzaId[0]}, {i.id}),'

    relazionaPizzaIngredienti = relazionaPizzaIngredienti[0: len(
        relazionaPizzaIngredienti)-1]

    db.query(relazionaPizzaIngredienti).fetchall()
    db.commit()

    return 1


@app.patch("/pizza/{pizza_id}/update")
async def updatePizza(pizza_id, pizza: Pizza = None):
    db = DBConnection()
    queryUpdate = f'update pizze set nome = "{pizza.nome}", costo = {pizza.costo} where id_pizza = {pizza_id}'
    db.query(queryUpdate).fetchall()
    db.commit()
    getRelazione = f'select fk_ingrediente from pizza_ingrediente where fk_pizza = {pizza_id}'
    print(db.query(getRelazione).fetchall())
    queryDelete = f'delete from pizza_ingrediente where FK_pizza = {pizza_id}'
    db.query(queryDelete)
    db.commit()
    relazionaPizzaIngredienti = f'insert into pizza_ingrediente values'
    for i in pizza.ingredienti:
        relazionaPizzaIngredienti += f'({pizza_id}, {i.id}),'
    relazionaPizzaIngredienti = relazionaPizzaIngredienti[0: len(
        relazionaPizzaIngredienti)-1]

    db.query(relazionaPizzaIngredienti).fetchall()
    db.commit()

    return 1

@app.delete("/pizza/{pizza_id}/delete")
async def deletePizza(pizza_id):

    db = DBConnection()
    delete = f'delete from pizza_ingrediente where fk_pizza={pizza_id}'
    db.query(delete)
    db.commit()
    delete = f'delete from pizze where id_pizza={pizza_id}'
    db.query(delete)
    db.commit()
    return 1
