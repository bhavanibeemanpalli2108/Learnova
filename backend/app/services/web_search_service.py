from typing import Dict, List

from langchain_tavily import TavilySearch

from app.core.logger import logger
from app.core.config import settings

class WebSearchService:
    """
    Service responsible for retrieving information from the web using Tavily.
    """

    def __init__(self):

        self.search_tool = TavilySearch(
            tavily_api_key=settings.TAVILY_API_KEY,
            max_results=5,
            search_depth="advanced",
            include_answer=False,
            include_raw_content=True,
        )

    
    def search(self, query: str) -> Dict:
        """
        Search the web and return formatted context.
        """

        logger.info(f"Searching Tavily for: {query}")

        response = self.search_tool.invoke(query)

        logger.info(f"Tavily response type: {type(response)}")

        results = response.get("results", [])

        context = self._format_results(results)

        sources = self._extract_sources(results)

        return {
            "context": context,
            "sources": sources,
        }

    def _format_results(self, results: List[dict]) -> str:

        formatted = []

        for result in results:

            if not isinstance(result, dict):
                continue

            formatted.append(
                f"Title: {result.get('title', '')}\n"
                f"Content: {result.get('content', '')}"
            )

        return "\n\n".join(formatted)

    def _extract_sources(self, results: List[dict]) -> List[dict]:

        sources = []

        for result in results:

            if not isinstance(result, dict):
                continue

            sources.append(
                {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                }
            )

        return sources