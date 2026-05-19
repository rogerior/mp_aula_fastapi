"""
Biblioteca cliente para a API de aulas de FastAPI.

Exemplo de uso::

    from biblioteca_api import BibliotecaAPI, TipoOperacao

    api = BibliotecaAPI(base_url="http://localhost:8000", api_token="meu-token")

    resultado = api.soma_v3(10, 5)
    print(resultado.resultado)  # 15

    historia = api.gerar_historia("dinossauros no espaço")
    print(historia.historia)
"""

import warnings
from dataclasses import dataclass
from enum import Enum

import requests


# ---------------------------------------------------------------------------
# Enums e modelos de dados
# ---------------------------------------------------------------------------


class TipoOperacao(str, Enum):
    """Tipos de operação matemática disponíveis."""

    SOMA = "soma"
    SUBTRACAO = "subtracao"
    MULTIPLICACAO = "multiplicacao"
    DIVISAO = "divisao"


@dataclass
class HistoriaOutput:
    """Resposta do endpoint de geração de histórias."""

    historia: str


@dataclass
class Resultado:
    """Resposta dos endpoints de soma (v3) e operação matemática."""

    resultado: int


# ---------------------------------------------------------------------------
# Exceções da biblioteca
# ---------------------------------------------------------------------------


class APIError(Exception):
    """Levantada quando a API retorna um status HTTP de erro."""

    def __init__(self, status_code: int, detail: object) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


# ---------------------------------------------------------------------------
# Cliente principal
# ---------------------------------------------------------------------------


class BibliotecaAPI:
    """Cliente para todos os endpoints da API.

    Args:
        base_url: URL base da API, por exemplo ``"http://localhost:8000"``.
        api_token: Token de autenticação exigido por todos os endpoints.
        timeout: Timeout em segundos para cada requisição (padrão: 30).
    """

    def __init__(self, base_url: str, api_token: str, timeout: float = 30) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_token = api_token
        self._timeout = timeout
        self._session = requests.Session()

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    def _url(self, path: str) -> str:
        return f"{self._base_url}{path}"

    def _check_response(self, response: requests.Response) -> None:
        if response.status_code >= 400:
            try:
                detail = response.json()
            except Exception:
                detail = response.text
            raise APIError(response.status_code, detail)

    # ------------------------------------------------------------------
    # Tag: Criação de Textos
    # ------------------------------------------------------------------

    def gerar_historia(self, tema: str) -> HistoriaOutput:
        """Gera uma história relacionada ao *tema* fornecido usando IA.

        Corresponde a ``POST /llm/gerar_historia/v1``.

        Args:
            tema: Tema sobre o qual a história será gerada.

        Returns:
            :class:`HistoriaOutput` contendo o texto gerado.
        """
        response = self._session.post(
            self._url("/llm/gerar_historia/v1"),
            params={"api_token": self._api_token},
            json={"tema": tema},
            timeout=self._timeout,
        )
        self._check_response(response)
        return HistoriaOutput(**response.json())

    # ------------------------------------------------------------------
    # Tag: Operações Matemáticas
    # ------------------------------------------------------------------

    def soma_v1(self, numero1: int, numero2: int) -> dict:
        """Soma dois números inteiros via parâmetros de rota.

        Corresponde a ``GET /operacoes/v1/soma/{numero1}/{numero2}``.

        .. deprecated::
            Este endpoint será descontinuado em 30/05/2026.
            Prefira :meth:`soma_v3`.

        Args:
            numero1: Primeiro operando.
            numero2: Segundo operando.

        Returns:
            Dicionário com o resultado retornado pela API.
        """
        warnings.warn(
            "soma_v1 está depreciado e será removido em 30/05/2026. Use soma_v3.",
            DeprecationWarning,
            stacklevel=2,
        )
        response = self._session.get(
            self._url(f"/operacoes/v1/soma/{numero1}/{numero2}"),
            params={"api_token": self._api_token},
            timeout=self._timeout,
        )
        self._check_response(response)
        return response.json()

    def soma_v2(self, numero1: int, numero2: int) -> dict:
        """Soma dois números inteiros via parâmetros de query.

        Corresponde a ``POST /operacoes/v2/soma``.

        Args:
            numero1: Primeiro operando.
            numero2: Segundo operando.

        Returns:
            Dicionário com o resultado retornado pela API.
        """
        response = self._session.post(
            self._url("/operacoes/v2/soma"),
            params={
                "numero1": numero1,
                "numero2": numero2,
                "api_token": self._api_token,
            },
            timeout=self._timeout,
        )
        self._check_response(response)
        return response.json()

    def soma_v3(self, numero1: int, numero2: int) -> Resultado:
        """Soma dois números inteiros via corpo da requisição.

        Corresponde a ``POST /operacoes/v3/soma``.

        Args:
            numero1: Primeiro operando.
            numero2: Segundo operando.

        Returns:
            :class:`Resultado` com o valor da soma.
        """
        response = self._session.post(
            self._url("/operacoes/v3/soma"),
            params={"api_token": self._api_token},
            json={"numero1": numero1, "numero2": numero2},
            timeout=self._timeout,
        )
        self._check_response(response)
        return Resultado(**response.json())

    def operacao_matematica(
        self,
        numero1: int,
        numero2: int,
        operacao: TipoOperacao,
    ) -> dict:
        """Realiza uma operação matemática entre dois números.

        Corresponde a ``POST /operacoes/v1/operacao_matematica``.

        Args:
            numero1: Primeiro operando.
            numero2: Segundo operando.
            operacao: Tipo da operação (:class:`TipoOperacao`).

        Returns:
            Dicionário com o resultado retornado pela API.

        Example::

            api.operacao_matematica(10, 2, TipoOperacao.DIVISAO)
        """
        response = self._session.post(
            self._url("/operacoes/v1/operacao_matematica"),
            params={
                "operacao": operacao.value,
                "api_token": self._api_token,
            },
            json={"numero1": numero1, "numero2": numero2},
            timeout=self._timeout,
        )
        self._check_response(response)
        return response.json()
