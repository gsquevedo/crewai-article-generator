## @file
#  @brief Criação de uma equipe de agentes com funções específicas para gerar um artigo baseado em um tópico.
#  @details Este script utiliza a biblioteca CrewAI, modelos LLM do LangChain e uma ferramenta personalizada da Wikipedia
#           para criar uma equipe composta por agentes com funções de pesquisa, redação e revisão de conteúdo.

from crewai import Agent, Task, Crew 
from langchain_community.chat_models import ChatLiteLLM
from wikipedia_tool import WikipediaTool
from dotenv import load_dotenv
import os

## @brief Carrega variáveis de ambiente do arquivo `.env`.
load_dotenv()

## @brief Inicializa o modelo de linguagem LLM com chave da API do Google.
llm = ChatLiteLLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

## @brief Instancia a ferramenta da Wikipedia.
wiki_tool = WikipediaTool()


## @brief Cria uma equipe de agentes para gerar um artigo com base em um tópico fornecido.
#  @param topico_usuario Tópico principal do artigo.
#  @return Instância de Crew contendo os agentes e tarefas.
def criar_equipe(topico_usuario: str):
    
    ## @brief Agente responsável pela pesquisa do conteúdo.
    pesquisador = Agent(
        role='Pesquisador Especializado',
        goal=f'Coletar e resumir informações relevantes sobre "{topico_usuario}" com base na Wikipedia.',
        backstory=(
            'Você é um pesquisador acadêmico com experiência em coleta e organização de informações. '
            'Seu objetivo é fornecer um resumo claro e objetivo do conteúdo da Wikipedia sobre o tema solicitado.'
        ),
        tools=[wiki_tool],
        verbose=True,
        llm=llm,
        examples=[
            {
                "input": "Futebol",
                "output": "O futebol é um esporte coletivo jogado entre dois times de 11 jogadores cada. É o esporte mais popular do mundo..."
            }
        ]
    )

    ## @brief Agente encarregado de redigir o artigo de forma criativa.
    redator = Agent(
        role='Redator Criativo',
        goal=f'Escrever um artigo cativante de no mínimo 300 palavras sobre "{topico_usuario}" para um público de jovens adultos.',
        backstory=(
            'Você é um redator com talento para transformar textos técnicos em artigos envolventes. '
            'Seu estilo deve ser leve, interessante e adaptado para jovens adultos, mantendo a fidelidade ao conteúdo original.'
        ),
        tools=[],
        verbose=True,
        llm=llm,
        examples=[
            {
                "input": "Resumo: O futebol é um esporte coletivo jogado entre dois times de 11 jogadores...",
                "output": "Imagine um jogo que reúne paixão, rivalidade e habilidade em campo. Estamos falando de futebol..."
            }
        ]
    )

    ## @brief Agente responsável por revisar o conteúdo final do artigo.
    revisor = Agent(
        role='Revisor Gramatical',
        goal='Revisar o artigo final, corrigindo erros gramaticais e garantindo coesão e coerência textual.',
        backstory=(
            'Você é um revisor profissional com um olhar aguçado para gramática, ortografia e fluidez textual. '
            'Seu trabalho é garantir que o artigo final esteja impecável antes da publicação.'
        ),
        tools=[],
        verbose=True,
        llm=llm,
        examples=[
            {
                "input": "Imagine um jogo que reúne paixão rivalidade e habilidade em campo",
                "output": "Imagine um jogo que reúne paixão, rivalidade e habilidade em campo."
            }
        ]
    )

    ## @brief Tarefa atribuída ao pesquisador.
    tarefa_pesquisa = Task(
        description=f'Pesquisar e resumir informações relevantes sobre "{topico_usuario}" na Wikipedia.',
        expected_output='Resumo claro e informativo com no mínimo 100 palavras.',
        agent=pesquisador
    )

    ## @brief Tarefa atribuída ao redator.
    tarefa_redacao = Task(
        description='Reescreva o resumo do Pesquisador em um artigo cativante com no mínimo 300 palavras, voltado para jovens adultos.',
        expected_output='Artigo envolvente com base no conteúdo pesquisado, com linguagem acessível.',
        agent=redator
    )

    ## @brief Tarefa atribuída ao revisor.
    tarefa_revisao = Task(
        description='Revise o artigo escrito pelo Redator, corrigindo erros gramaticais e melhorando a fluidez textual.',
        expected_output='Versão final do artigo revisada e pronta para publicação.',
        agent=revisor,
        output_file=f'articles/artigo.md'
    )
    
    ## @brief Criação e retorno da equipe com os agentes e suas respectivas tarefas.
    equipe = Crew(
        agents=[pesquisador, redator, revisor],
        tasks=[tarefa_pesquisa, tarefa_redacao, tarefa_revisao],
        verbose=True
    )

    return equipe
