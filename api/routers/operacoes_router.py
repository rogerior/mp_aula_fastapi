from fastapi import status, HTTPException, APIRouter

from models import Resultado, Numeros, TipoOperacao
from utils import get_logger

logger = get_logger()


router = APIRouter()


# Passando o número 1 e 2 na URL
# http://127.0.0.1:8000/soma/3/2
@router.get(
    path="/v1/soma/{numero1}/{numero2}",
    summary="Soma de dois números",
    description="Essa rota recebe dois números inteiros e retorna a soma deles. Será descontinuado em 30/05/2026.",
    deprecated=True,
)
def soma(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


# Passando o número 1 e 2 no corpo da requisição
# http://127.0.0.1:8000/soma_formato2?numero1=3&numero2=2
@router.post(path="/v2/soma")
def soma_formato2(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


# Formato 3
@router.post(
    path="/v3/soma",
    response_model=Resultado,
    status_code=status.HTTP_201_CREATED,
    response_description="A soma foi realizada com sucesso",
    summary="Soma de dois números",
    description="Essa rota recebe dois números inteiros e retorna a soma deles.",
)
def soma_formato3(numeros: Numeros):

    # Verificando se os números são maior ou igual a 0
    if numeros.numero1 < 0 or numeros.numero2 < 0:
        logger.warning(
            f"Números inválidos. Número 1: {numeros.numero1}, Número 2: {numeros.numero2}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Os números devem ser maiores ou iguais a zero.",
        )

    total = numeros.numero1 + numeros.numero2

    if total < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O resultado da soma não pode ser negativo.",
        )

    return Resultado(resultado=total)


@router.post(
    path="/v1/operacao_matematica",
    summary="Realiza uma operação matemática",
    description="Essa rota recebe dois números inteiros e o tipo da operação matemática (soma, subtração, multiplicação ou divisão) e retorna o resultado da operação.",
)
def operacao_matematica(numeros: Numeros, operacao: TipoOperacao):

    if operacao == TipoOperacao.soma:
        resultado = numeros.numero1 + numeros.numero2

    elif operacao == TipoOperacao.subtracao:
        resultado = numeros.numero1 - numeros.numero2

    elif operacao == TipoOperacao.multiplicacao:
        resultado = numeros.numero1 * numeros.numero2

    elif operacao == TipoOperacao.divisao:
        resultado = numeros.numero1 / numeros.numero2

    return {"resultado": resultado}
