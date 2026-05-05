from fastapi import Depends, FastAPI, status, HTTPException


from groq import Groq

import logging
import os

from dotenv import load_dotenv

from models import Resultado, Numeros, TipoOperacao, HistoriaInput, HistoriaOutput


load_dotenv()


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("fastapi")


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

API_TOKEN = "123"


def common_api_token(api_token: str):
    if api_token != API_TOKEN:
        logger.warning(f"Token de autenticação inválido. Token enviado: {api_token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido. Tente novamente.",
        )

    logger.info(f"Token de autenticação válido. Token enviado: {api_token}")
    return {"api_token": api_token}


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
    dependencies=[Depends(common_api_token)],
)


@app.get(path="/teste")
def hello_world():
    # Lógico de processamento
    return {"message": "Hello World 123"}


# Passando o número 1 e 2 na URL
# http://127.0.0.1:8000/soma/3/2
@app.get(
    path="/v1/soma/{numero1}/{numero2}",
    summary="Soma de dois números",
    description="Essa rota recebe dois números inteiros e retorna a soma deles. Será descontinuado em 30/05/2026.",
    tags=["Operações Matemáticas"],
    deprecated=True,
)
def soma(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


# Passando o número 1 e 2 no corpo da requisição
# http://127.0.0.1:8000/soma_formato2?numero1=3&numero2=2
@app.post(path="/v2/soma", tags=["Operações Matemáticas"])
def soma_formato2(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


# Formato 3
@app.post(
    path="/v3/soma",
    response_model=Resultado,
    tags=["Operações Matemáticas"],
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


@app.post(
    path="/v1/operacao_matematica",
    tags=["Operações Matemáticas"],
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


@app.post(
    path="/gerar_historia/v1",
    tags=["Criação de Textos"],
    summary="Gera uma história a partir de um tema",
    description="Essa rota recebe um tema e gera uma história, utilizando IA, relacionada a esse tema.",
    response_model=HistoriaOutput,
)
def gerar_historia(tema: HistoriaInput):

    logger.info(f"Gerando história para o tema: {tema.tema}")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Gere uma história relacionada ao seguinte tema: {tema.tema}",
            }
        ],
        model="llama-3.1-8b-instant",
    )

    logger.info("História gerada com sucesso.")
    logger.info(f"Tokens utilizados: {chat_completion.usage.total_tokens}")
    logger.debug(f"Resposta da IA: {chat_completion.choices[0].message.content}")

    historia = chat_completion.choices[0].message.content

    return HistoriaOutput(historia=historia)
