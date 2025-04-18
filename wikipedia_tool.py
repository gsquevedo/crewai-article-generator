from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel
import requests

## @class WikipediaInput
#  @brief Modelo de entrada para a busca de tópicos na Wikipedia.
#
#  Representa os dados necessários para realizar uma busca na Wikipedia.
class WikipediaInput(BaseModel):
    ## @var topic
    #  @brief O tópico a ser pesquisado na Wikipedia.
    topic: str


## @class WikipediaTool
#  @brief Ferramenta para procurar um tópico na Wikipedia e retornar um resumo.
#
#  Esta ferramenta consulta a API da Wikipedia para buscar um tópico e retornar
#  um resumo extraído da introdução da página correspondente.
class WikipediaTool(BaseTool):
    ## @var name
    #  @brief Nome da ferramenta.
    name: str = "wikipedia_search"

    ## @var description
    #  @brief Descrição da funcionalidade da ferramenta.
    description: str = "Procura um tópico na Wikipedia e retorna um resumo."

    ## @var args_schema
    #  @brief Modelo de entrada esperado pela ferramenta.
    args_schema: Type[BaseModel] = WikipediaInput

    ## @brief Executa a busca do tópico na Wikipedia.
    #
    #  Este método realiza uma requisição para a API da Wikipedia, procurando pelo tópico
    #  solicitado e retornando o resumo da introdução da página principal correspondente.
    #
    #  @param topic O tópico a ser pesquisado na Wikipedia.
    #  @return Um resumo textual do tópico encontrado ou uma mensagem de erro caso nada seja encontrado.
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
