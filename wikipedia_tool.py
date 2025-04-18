from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel
import requests

"""
Modelo de entrada para a busca de tópicos na Wikipedia.

@param topic: O tópico a ser pesquisado na Wikipedia.
"""
class WikipediaInput(BaseModel):
    topic: str

"""
Ferramenta para procurar um tópico na Wikipedia e retornar um resumo.

A ferramenta consulta a API da Wikipedia para buscar um tópico e retornar um resumo extraído da introdução da página correspondente.

@param name: O nome da ferramenta (padrão: "wikipedia_search").
@param description: Descrição da funcionalidade da ferramenta (padrão: "Procura um tópico na Wikipedia e retorna um resumo.").
@param args_schema: O modelo de entrada esperado pela ferramenta (padrão: `WikipediaInput`).
"""
class WikipediaTool(BaseTool):
    name: str = "wikipedia_search"
    description: str = "Procura um tópico na Wikipedia e retorna um resumo."
    args_schema: Type[BaseModel] = WikipediaInput

    """
    Executa a busca no tópico da Wikipedia e retorna o resumo extraído.

    Este método realiza uma requisição para a API da Wikipedia, procurando pelo tópico solicitado e retornando o resumo
    extraído da página principal.

    @param topic: O tópico a ser pesquisado na Wikipedia.
    @return: Resumo do tópico ou uma mensagem de erro caso não haja resultados.
    """
    def _run(self, topic: str):
        # Constrói a URL para a busca na Wikipedia
        url = f"https://pt.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={topic}&utf8=1"
        response = requests.get(url)
        data = response.json()

        # Verifica se a resposta contém resultados da busca
        if 'query' in data and 'search' in data['query']:
            search_results = data['query']['search']
            if search_results:
                page_id = search_results[0]['pageid']
                # Constrói a URL para obter o resumo da página
                summary_url = f"https://pt.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=&explaintext=&pageids={page_id}"
                summary_response = requests.get(summary_url)
                summary_data = summary_response.json()
                # Verifica se os dados de resumo estão disponíveis e retorna o conteúdo
                if 'query' in summary_data and 'pages' in summary_data['query']:
                    page_content = summary_data['query']['pages'][str(page_id)]['extract']
                    return page_content
        return "Nenhuma informação encontrada na Wikipedia."
