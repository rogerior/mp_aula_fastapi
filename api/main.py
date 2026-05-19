from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv
from routers import llm_router, operacoes_router, web_router, health_router
from utils import get_logger
from fastapi_mcp import FastApiMCP


load_dotenv(find_dotenv())

logger = get_logger()


app = FastAPI(
    title="Aula sobre API",
    summary="APIs desenvolvidas durante as aulas",
    description="Essa **API** foi desenvolvida durante as aulas de FastAPI para a turma do MPGO, onde foram abordados os seguintes tópicos: criação de rotas, manipulação de parâmetros, uso de modelos Pydantic e muito mais.",
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
    # dependencies=[Depends(common_api_token)],
)


app.include_router(llm_router.router, prefix="/llm")
app.include_router(
    operacoes_router.router, prefix="/operacoes", tags=["Operações Matemáticas"]
)
app.include_router(web_router.router, prefix="/web", tags=["Pesquisa na Web"])
app.include_router(health_router.router, tags=["Health Check"])


mcp = FastApiMCP(app)
mcp.mount_http()
