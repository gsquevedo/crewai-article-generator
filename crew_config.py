from crewai import Agent, Task, Crew
from langchain_community.chat_models import ChatLiteLLM
from wikipedia_tool import WikipediaTool
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente a partir do arquivo .env.
load_dotenv()

# Cria o modelo de linguagem LLM (Large Language Model) com uma chave API do Google.
llm = ChatLiteLLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Instancia a ferramenta do Wikipedia, que será usada pelo agente.
wiki_tool = WikipediaTool()

"""
Cria uma equipe composta por três agentes (pesquisador, redator e revisor) com tarefas específicas
para coletar, redigir e revisar um artigo baseado em um tópico fornecido.

Este método configura os agentes para interagir com a Wikipedia e gerar um artigo sobre o tópico do usuário.

@param topico_usuario: O tópico do artigo a ser gerado.
@return: Instância da classe Crew que contém os agentes e tarefas configuradas.
"""
def criar_equipe(topico_usuario: str):
    
    # Criação do agente de pesquisa, que buscará informações na Wikipedia sobre o tópico.
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

    # Criação do agente redator, responsável por transformar o resumo em um artigo cativante.
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

    # Criação do agente revisor, que será responsável pela revisão gramatical e fluidez do artigo.
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

    # Criação das tarefas para a equipe: pesquisa, redação e revisão.
    tarefa_pesquisa = Task(
        description=f'Pesquisar e resumir informações relevantes sobre "{topico_usuario}" na Wikipedia.',
        expected_output='Resumo claro e informativo com no mínimo 100 palavras.',
        agent=pesquisador
    )

    tarefa_redacao = Task(
        description='Reescreva o resumo do Pesquisador em um artigo cativante com no mínimo 300 palavras, voltado para jovens adultos.',
        expected_output='Artigo envolvente com base no conteúdo pesquisado, com linguagem acessível.',
        agent=redator
    )

    tarefa_revisao = Task(
        description='Revise o artigo escrito pelo Redator, corrigindo erros gramaticais e melhorando a fluidez textual.',
        expected_output='Versão final do artigo revisada e pronta para publicação.',
        agent=revisor,
        output_file=f'articles/artigo.md'
    )
    
    # Criação da equipe, composta pelos agentes e tarefas configuradas.
    equipe = Crew(
        agents=[pesquisador, redator, revisor],
        tasks=[tarefa_pesquisa, tarefa_redacao, tarefa_revisao],
        verbose=True
    )

    return equipe
