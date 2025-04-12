from fastapi import FastAPI
from pydantic import BaseModel
from crew_config import criar_equipe

app = FastAPI()

class TarefaInput(BaseModel):
    topico: str

@app.post("/executar")
async def executar_crew(input_data: TarefaInput):
    try:
        equipe = criar_equipe(input_data.topico)
        resultado = equipe.kickoff()
        return {"resultado": str(resultado.output)}
    except Exception as e:
        return {"erro": str(e)}