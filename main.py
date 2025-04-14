from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crew_config import criar_equipe
from crewai import Agent, Crew, Task
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TópicoRequest(BaseModel):
    topico: str

class ResultadoArtigo(BaseModel):
    status: str
    artigo: str
    detalhes: Optional[str] = None

@app.post("/gerar_artigo/")
async def gerar_artigo(request: TópicoRequest):
    try:
        topico_usuario = request.topico
        equipe = criar_equipe(topico_usuario)
        resultado = equipe.kickoff()
        artigo_str = str(resultado)

        return ResultadoArtigo(
            status="sucesso",
            artigo=artigo_str,
            # detalhes=f"Arquivos salvos: {caminho_md}, {caminho_json}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar o artigo: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
