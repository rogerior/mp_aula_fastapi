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


class PesquisaInput(BaseModel):
    termo: str
    max_results: int = 5


class PesquisaResult(BaseModel):
    title: str
    url: str
    body: str


class PesquisaOutput(BaseModel):
    resultados: list[PesquisaResult]


class ExtracaoInput(BaseModel):
    url: str


class ExtracaoOutput(BaseModel):
    url: str
    content: str


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"
