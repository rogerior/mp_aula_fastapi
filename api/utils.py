from fastapi import status, HTTPException

from groq import Groq

import logging
import os


API_TOKEN = os.environ.get("API_TOKEN")


def get_logger():
    """
    Configura e retorna o logger padrão da aplicação.

    Inicializa o logging com nível INFO e formato padronizado contendo
    timestamp, nível e mensagem. Utiliza o logger nomeado 'fastapi'.

    Returns:
        logging.Logger: Instância do logger configurado.
    """

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
    )
    logger = logging.getLogger("fastapi")
    return logger


logger = get_logger()


def common_api_token(api_token: str):
    """
    Valida o token de autenticação da requisição.

    Compara o token fornecido com o token esperado definido na variável
    de ambiente API_TOKEN. Caso inválido, lança uma exceção HTTP 401.

    Args:
        api_token (str): Token de autenticação enviado pelo cliente.

    Returns:
        dict: Dicionário contendo o token validado no formato {'api_token': api_token}.

    Raises:
        HTTPException: Se o token fornecido não corresponder ao token esperado (HTTP 401).
    """
    if api_token != API_TOKEN:
        logger.warning(f"Token de autenticação inválido. Token enviado: {api_token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido. Tente novamente.",
        )

    logger.info(f"Token de autenticação válido. Token enviado: {api_token}")
    return {"api_token": api_token}


def get_llm_client(client: str):
    """
    Instancia e retorna o cliente de LLM correspondente ao provedor informado.

    Args:
        client (str): Nome do provedor de LLM. Atualmente suporta apenas 'groq'.

    Returns:
        Groq: Instância do cliente Groq configurada com a chave de API.

    Raises:
        ValueError: Se o nome do cliente não for reconhecido.
    """
    logger.info(f"Obtendo cliente de LLM para: {client}")
    if client == "groq":
        return Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )
    else:
        raise ValueError(f"Cliente de LLM desconhecido: {client}")


def execute_prompt(
    prompt: str, client: str = "groq", model: str = "llama-3.1-8b-instant"
) -> str:
    """
    Envia um prompt ao modelo de LLM e retorna a resposta gerada.

    Args:
        prompt (str): Texto do prompt a ser enviado ao modelo.
        client (str): Nome do provedor de LLM a ser utilizado. Padrão: 'groq'.
        model (str): Identificador do modelo de linguagem. Padrão: 'llama-3.1-8b-instant'.

    Returns:
        str: Conteúdo textual da resposta gerada pelo modelo.
    """
    logger.info(
        f"Executando prompt com o cliente '{client}' e modelo '{model}'. Prompt: {prompt}"
    )

    client = get_llm_client(client)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )

    response = chat_completion.choices[0].message.content

    logger.info(f"Tokens utilizados: {chat_completion.usage.total_tokens}")
    logger.debug(f"Resposta da IA: {response}")

    return response
