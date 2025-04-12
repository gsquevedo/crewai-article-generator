from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel
import requests

class WikipediaInput(BaseModel):
    topic: str

class WikipediaTool(BaseTool):
    name: str = "wikipedia_search"
    description: str = "Procura um tópico na Wikipedia e retorna um resumo."
    args_schema: Type[BaseModel] = WikipediaInput

    def _run(self, topic: str):
        """Executa a busca e retorna o resumo."""
        url = f"https://pt.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={topic}&utf8=1"
        response = requests.get(url)
        data = response.json()

        if 'query' in data and 'search' in data['query']:
            search_results = data['query']['search']
            if search_results:
                page_id = search_results[0]['pageid']
                summary_url = f"https://pt.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=&explaintext=&pageids={page_id}"
                summary_response = requests.get(summary_url)
                summary_data = summary_response.json()
                if 'query' in summary_data and 'pages' in summary_data['query']:
                    page_content = summary_data['query']['pages'][str(page_id)]['extract']
                    return page_content
        return "Nenhuma informação encontrada na Wikipedia."

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Execução assíncrona não implementada.")
