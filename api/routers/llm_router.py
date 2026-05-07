from fastapi import APIRouter

from models import HistoriaInput, HistoriaOutput
from utils import get_logger, execute_prompt


logger = get_logger()

router = APIRouter()


@router.post(
    path="/gerar_historia/v1",
    tags=["Criação de Textos"],
    summary="Gera uma história a partir de um tema",
    description="Essa rota recebe um tema e gera uma história, utilizando IA, relacionada a esse tema.",
    response_model=HistoriaOutput,
)
def gerar_historia(tema: HistoriaInput):

    logger.info(f"Gerando história para o tema: {tema.tema}")

    prompt = f"Gere uma história relacionada ao seguinte tema: {tema.tema}"

    historia = execute_prompt(prompt)

    logger.info("História gerada com sucesso")

    return HistoriaOutput(historia=historia)
