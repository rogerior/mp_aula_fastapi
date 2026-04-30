from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Numeros(BaseModel):
    numero1: int
    numero2: int


@app.get(path="/teste")
def hello_world():
    # Lógico de processamento
    return {"message": "Hello World 123"}


# Passando o número 1 e 2 na URL
# http://127.0.0.1:8000/soma/3/2
@app.get(path="/soma/{numero1}/{numero2}")
def soma(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


# Passando o número 1 e 2 no corpo da requisição
# http://127.0.0.1:8000/soma_formato2?numero1=3&numero2=2
@app.post(path="/soma_formato2")
def soma_formato2(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


# Formato 3
@app.post(path="/soma_formato3")
def soma_formato3(numeros: Numeros):
    total = numeros.numero1 + numeros.numero2
    return {"resultado": total}
