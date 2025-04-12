from crewai import Agent, Task, Crew
from langchain.chat_models import ChatLiteLLM
from wikipedia_tool import WikipediaTool
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatLiteLLM(
    model="gemini/gemini-1.5-pro",
    api_key=os.getenv("GOOGLE_API_KEY")
)

wiki_tool = WikipediaTool()

def criar_equipe(topico_usuario: str):
    pesquisador = Agent(
        role='Pesquisador',
        goal='Pesquisar informações detalhadas na Wikipedia sobre um tópico',
        backstory='Especialista em encontrar e resumir informações acadêmicas.',
        tools=[wiki_tool],
        verbose=True,
        llm=llm
    )

    redator = Agent(
        role='Redator',
        goal='Gerar um artigo com pelo menos 300 palavras baseado na pesquisa',
        backstory='Especialista em redigir artigos acadêmicos.',
        tools=[],
        verbose=True,
        llm=llm
    )

    tarefa_pesquisa = Task(
        description=f'Pesquise sobre o tema "{topico_usuario}" e traga um resumo.',
        expected_output='Resumo da pesquisa com informações relevantes',
        agent=pesquisador
    )

    tarefa_redacao = Task(
        description='Utilize o resumo do pesquisador para escrever um artigo de no mínimo 300 palavras.',
        expected_output='Artigo completo baseado na pesquisa',
        agent=redator
    )

    equipe = Crew(
        agents=[pesquisador, redator],
        tasks=[tarefa_pesquisa, tarefa_redacao],
        verbose=True
    )

    return equipe
