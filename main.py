from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crew_config import criar_equipe
from crewai import Agent, Crew, Task
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

## @brief Instancia o aplicativo FastAPI.
app = FastAPI()

## @brief Adiciona o middleware CORS (Cross-Origin Resource Sharing) à aplicação FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## @class TópicoRequest
#  @brief Modelo de dados para a requisição de geração de artigo.
#
#  Define o formato da requisição que inclui o 'topico', 
#  o qual será usado para gerar o conteúdo do artigo.
class TópicoRequest(BaseModel):
    ## @var topico
    #  @brief O tópico do artigo a ser gerado.
    topico: str


## @class ArtigoData
#  @brief Modelo de dados para o artigo gerado.
#
#  Define a estrutura de um artigo gerado, que inclui o 
#  título, o conteúdo e a contagem de palavras.
class ArtigoData(BaseModel):
    ## @var titulo
    #  @brief O título do artigo.
    titulo: str

    ## @var conteudo
    #  @brief O conteúdo do artigo.
    conteudo: str

    ## @var palavras
    #  @brief A quantidade de palavras no artigo.
    palavras: int


## @class ResultadoArtigo
#  @brief Modelo de dados para o resultado da geração do artigo.
#
#  Encapsula o status da operação de geração do artigo, 
#  os dados do artigo e detalhes adicionais.
class ResultadoArtigo(BaseModel):
    ## @var status
    #  @brief O status da operação de geração do artigo (ex: 'sucesso').
    status: str

    ## @var artigo
    #  @brief O artigo gerado.
    artigo: ArtigoData

    ## @var detalhes
    #  @brief Detalhes adicionais sobre o erro, se houver (pode ser None).
    detalhes: Optional[str] = None


## @brief Endpoint para gerar um artigo baseado em um tópico fornecido.
#
#  Este endpoint recebe uma requisição com um tópico e gera um artigo com base nesse tópico. O artigo 
#  gerado é retornado com o título, conteúdo e a quantidade de palavras.
#
#  @param request O objeto que contém o tópico fornecido pelo usuário.
#  @return ResultadoArtigo O resultado da geração do artigo, incluindo o artigo gerado, status e detalhes.
#  @exception HTTPException Se ocorrer um erro ao gerar o artigo, uma exceção HTTP será levantada com status 500.
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

    except Exception as e:
        # Se ocorrer um erro, lança uma exceção HTTP com status 500.
        raise HTTPException(status_code=500, detail=f"Erro ao gerar o artigo: {str(e)}")
