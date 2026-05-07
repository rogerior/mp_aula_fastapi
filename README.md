# mp_aula_fastapi

Projeto de estudo de FastAPI desenvolvido durante as aulas.

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Criação do arquivo .env

Faça uma cópia do arquivo `.env.sample` e coloque com o nome `.env` e preencha as variáveis

## Instalação de dependências (bibliotecas)

```bash
uv sync
```

## Executar a aplicação localmente

```bash
uv run fastapi dev api/main.py
```

Caso já esteja com o ambiente virtual ativado:
```bash
fastapi dev api/main.py
```

A aplicação estará disponível em: http://localhost:8000

A documentação interativa (Swagger UI) estará em: http://localhost:8000/docs
