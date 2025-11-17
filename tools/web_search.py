"""Web search with Google Custom Search API."""

import os
import requests
from typing import List, Dict
from core.logger import logger


def search_google(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Search using Google Custom Search API.
    
    Args:
        query: Search query
        max_results: Maximum results (max 10)
        
    Returns:
        List of search results
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    
    if not api_key or not search_engine_id:
        logger.error("GOOGLE_API_KEY or GOOGLE_SEARCH_ENGINE_ID not found in .env")
        return [{
            "title": "Google Search Not Configured",
            "link": "",
            "snippet": "Please add GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID to your .env file"
        }]
    
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": query,
            "num": min(max_results, 10)  # Google allows max 10 per request
        }
        
        logger.info(f"Google Custom Search: {query}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        for item in data.get("items", []):
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", "")
            })
        
        logger.info(f"Google Search: Found {len(results)} results")
        return results
        
    except Exception as e:
        logger.error(f"Google Search error: {e}")
        return [{
            "title": "Search Error",
            "link": "",
            "snippet": f"Error: {str(e)}"
        }]


def search_web(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Search the web using Google Custom Search.
    
    Args:
        query: Search query
        max_results: Maximum results
        
    Returns:
        List of search results
    """
    return search_google(query, max_results)


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
        if result['link']:
            output.append(f"   🔗 {result['link']}")
        output.append(f"   {result['snippet']}")
        output.append("")
    
    return "\n".join(output)


if __name__ == "__main__":
    # Test
    results = search_web("Python programming", 3)
    print(format_search_results(results))
