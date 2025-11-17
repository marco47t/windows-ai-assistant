"""Web search using DuckDuckGo."""

from duckduckgo_search import DDGS
from typing import List, Dict
from core.logger import logger


def search_web(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Search the web using DuckDuckGo.
    
    Args:
        query: Search query
        max_results: Maximum number of results to return
        
    Returns:
        List of search results with title, link, and snippet
    """
    try:
        logger.info(f"Searching web for: {query}")
        
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            
        formatted_results = [
            {
                "title": r['title'],
                "link": r['href'],
                "snippet": r['body']
            }
            for r in results
        ]
        
        logger.info(f"Found {len(formatted_results)} results")
        return formatted_results
        
    except Exception as e:
        logger.error(f"Web search error: {e}")
        return []


def format_search_results(results: List[Dict[str, str]]) -> str:
    """Format search results for display.
    
    Args:
        results: List of search results
        
    Returns:
        Formatted string
    """
    if not results:
        return "No results found."
    
    output = []
    for i, result in enumerate(results, 1):
        output.append(f"{i}. **{result['title']}**")
        output.append(f"   {result['link']}")
        output.append(f"   {result['snippet']}")
        output.append("")
    
    return "\n".join(output)


if __name__ == "__main__":
    # Test the search
    results = search_web("Python programming", 3)
    print(format_search_results(results))
