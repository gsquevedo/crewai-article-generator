from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crew_config import criar_equipe
from crewai import Agent, Crew, Task
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

# Instancia o aplicativo FastAPI.
app = FastAPI()

# Adiciona o middleware CORS (Cross-Origin Resource Sharing) à aplicação FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Modelo de dados para a requisição de geração de artigo.

A classe define o formato da requisição que inclui o 'topico', 
o qual será usado para gerar o conteúdo do artigo.

Atributos:
    topico (str): O tópico do artigo a ser gerado.
"""
class TópicoRequest(BaseModel):
    topico: str

"""
Modelo de dados para o artigo gerado.

A classe define a estrutura de um artigo gerado, que inclui o 
título, o conteúdo e a contagem de palavras.

Atributos:
    titulo (str): O título do artigo.
    conteudo (str): O conteúdo do artigo.
    palavras (int): A quantidade de palavras no artigo.
"""
class ArtigoData(BaseModel):
    titulo: str
    conteudo: str
    palavras: int

"""
Modelo de dados para o resultado da geração do artigo.

A classe encapsula o status da operação de geração do artigo, 
os dados do artigo e detalhes adicionais.

Atributos:
    status (str): O status da operação de geração do artigo (ex: 'sucesso').
    artigo (ArtigoData): O artigo gerado.
    detalhes (Optional[str]): Detalhes adicionais sobre o erro, se houver (pode ser None).
"""
class ResultadoArtigo(BaseModel):
    status: str
    artigo: ArtigoData
    detalhes: Optional[str] = None

"""
Endpoint para gerar um artigo baseado em um tópico fornecido.

Este endpoint recebe uma requisição com um tópico e gera um artigo com base nesse tópico. O artigo 
gerado é retornado com o título, conteúdo e a quantidade de palavras.

Parametros:
    request (TópicoRequest): O objeto que contém o tópico fornecido pelo usuário.

Retorno:
    ResultadoArtigo: O resultado da geração do artigo, incluindo o artigo gerado, status e detalhes.

Raises:
    HTTPException: Se ocorrer um erro ao gerar o artigo, uma exceção HTTP será levantada com status 500.
"""
@app.post("/gerar_artigo/", response_model=ResultadoArtigo)
async def gerar_artigo(request: TópicoRequest):
    try:
        # Obtém o tópico fornecido na requisição.
        topico_usuario = request.topico

        # Executa a função de criação de equipe para gerar o artigo.
        equipe = criar_equipe(topico_usuario)
        resultado = equipe.kickoff()

       # Transforma o resultado em uma string e calcula o número de palavras.
        artigo_str = str(resultado).strip()
        titulo = f"Artigo sobre {topico_usuario.capitalize()}"
        palavras = len(artigo_str.split())

        # Cria o objeto de dados do artigo formatado.
        artigo_formatado = ArtigoData(
            titulo=titulo,
            conteudo=artigo_str,
            palavras=palavras
        )

        # Retorna o resultado com status 'sucesso'.
        return ResultadoArtigo(
            status="sucesso",
            artigo=artigo_formatado
        )

    # Se ocorrer um erro, lança uma exceção HTTP com status 500.
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar o artigo: {str(e)}")

