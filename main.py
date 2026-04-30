from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Aula sobre API",
    summary="APIs desenvolvidas durante as aulas",
    description="Essa **API** foi desenvolvida durante as aulas de FastAPI, onde foram abordados os seguintes tópicos: criação de rotas, manipulação de parâmetros, uso de modelos Pydantic e muito mais.",
    version="0.2",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Rogério Rodrigues Carvalho",
        "url": "http://github.com/rogerior/",
        "email": "rogerior@ufg.br",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


class Numeros(BaseModel):
    numero1: int
    numero2: int


class Resultado(BaseModel):
    resultado: int


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
@app.post(path="/soma_formato3", response_model=Resultado)
def soma_formato3(numeros: Numeros):
    total = numeros.numero1 + numeros.numero2
    return Resultado(resultado=total)
