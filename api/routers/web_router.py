from models import (
    ExtracaoInput,
    ExtracaoOutput,
    PesquisaInput,
    PesquisaOutput,
)
from utils import get_logger
from fastapi import APIRouter
from ddgs import DDGS


logger = get_logger()

router = APIRouter()


@router.post(
    path="/web_search/v1",
    response_model=PesquisaOutput,
    tags=["Pesquisa na Web"],
    summary="Realiza uma pesquisa na web utilizando DuckDuckGo",
    description="Essa rota recebe um termo de pesquisa e retorna os resultados encontrados utilizando o mecanismo de busca DuckDuckGo.",
)
def web_search(termo: PesquisaInput):
    logger.info(f"Realizando pesquisa para o termo: {termo}")

    results = DDGS().news(termo.termo, max_results=termo.max_results, region="pt-br")

    return PesquisaOutput(resultados=results)


@router.post(
    path="/extract_content/v1",
    tags=["Pesquisa na Web"],
    summary="Extrai o conteúdo de uma página web",
    description="Essa rota recebe uma URL e retorna o conteúdo extraído dessa página web.",
    response_model=ExtracaoOutput,
)
def extract_content(url: ExtracaoInput):
    logger.info(f"Extraindo conteúdo da URL: {url.url}")

    content = DDGS().extract(url.url)

    return ExtracaoOutput(url=content["url"], content=content["content"])
