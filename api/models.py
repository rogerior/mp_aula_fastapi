from pydantic import BaseModel
from enum import Enum


class Numeros(BaseModel):
    numero1: int
    numero2: int


class Resultado(BaseModel):
    resultado: int


class TipoOperacao(str, Enum):
    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"


class HistoriaInput(BaseModel):
    tema: str


class HistoriaOutput(BaseModel):
    historia: str
