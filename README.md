# 🧠 Projeto de Geração de Artigos com CrewAI e FastAPI

Este projeto é uma API desenvolvida com **FastAPI** que utiliza a **CrewAI** para gerar artigos baseados em tópicos fornecidos pelo usuário. A aplicação permite enviar um tópico, e a IA retorna um artigo com título, conteúdo e contagem de palavras.

---

## ✨ Tecnologias utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [CrewAI](https://docs.crewai.com/)
- [Uvicorn](https://www.uvicorn.org/) – servidor ASGI para desenvolvimento
- [CORS Middleware](https://fastapi.tiangolo.com/tutorial/cors/) – para integração com frontends externos

---

## 📁 Estrutura do Projeto

- `main.py`  
  Código principal da API.

- `crew_config.py`  
  Função de criação da equipe CrewAI.

- `wikipedia_tool/`  
  Diretório de ferramentas adicionais (ex: busca na Wikipedia).

- `requirements.txt`  
  Dependências do projeto.

- `README.md`  
  Documentação do projeto.

## 🚀 Como executar o projeto

### 1. Clone o repositório

### 2. Instale as dependências

- pip install -r requirements.txt

### 3. Execute o projeto

- uvicorn main:app --reload

A aplicação estará disponível em:
🔗 http://127.0.0.1:8000

Você também pode acessar a documentação interativa da API:
🔍 http://127.0.0.1:8000/docs

📬 Contato
Caso tenha dúvidas, sugestões ou queira contribuir:

💼 Gabriele Soares Quevedo

📧 gsquevedo@inf.ufsm.br