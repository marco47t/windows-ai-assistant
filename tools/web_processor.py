"""Advanced web content processing."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from core.logger import logger
from tools.web_search import search_web
from tools.web_navigator import scrape_webpage
import concurrent.futures


def extract_main_content(html: str) -> str:
    """Extract main content from HTML, removing noise.
    
    Args:
        html: HTML content
        
    Returns:
        Clean main content
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 
                            'aside', 'iframe', 'noscript', 'form']):
            element.decompose()
        
        # Try to find main content
        main_content = None
        
        # Look for common content containers
        for selector in ['article', 'main', '[role="main"]', '.content', 
                        '#content', '.post-content', '.entry-content']:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        # Fallback to body
        if not main_content:
            main_content = soup.find('body')
        
        if not main_content:
            return ""
        
        # Get text
        text = main_content.get_text(separator='\n', strip=True)
        
        # Clean up excessive whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n'.join(lines)
        
        return text
        
    except Exception as e:
        logger.error(f"Content extraction error: {e}")
        return ""


def fetch_and_extract(url: str, max_chars: int = 3000) -> Dict[str, str]:
    """Fetch URL and extract main content.
    
    Args:
        url: URL to fetch
        max_chars: Maximum characters to return
        
    Returns:
        Dict with url, title, and content
    """
    try:
        logger.info(f"Fetching: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get title
        title = soup.find('title')
        title = title.get_text(strip=True) if title else url
        
        # Get content
        content = extract_main_content(response.text)
        
        # Limit content length
        if len(content) > max_chars:
            content = content[:max_chars] + "..."
        
        return {
            'url': url,
            'title': title,
            'content': content,
            'success': True
        }
        
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return {
            'url': url,
            'title': 'Error',
            'content': f"Failed to fetch: {str(e)}",
            'success': False
        }


def search_and_read(query: str, num_results: int = 3, max_chars_per_page: int = 2000) -> Dict:
    """Search web and read top results.
    
    Args:
        query: Search query
        num_results: Number of results to read
        max_chars_per_page: Max characters per page
        
    Returns:
        Dict with search results and page contents
    """
    logger.info(f"Search and read: {query}")
    
    # Step 1: Search
    search_results = search_web(query, max_results=num_results)
    
    if not search_results or not search_results[0].get('link'):
        return {
            'query': query,
            'search_results': search_results,
            'pages': [],
            'error': 'No valid search results'
        }
    
    # Step 2: Fetch pages in parallel (faster)
    urls = [r['link'] for r in search_results if r.get('link')][:num_results]
    
    pages = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {
            executor.submit(fetch_and_extract, url, max_chars_per_page): url 
            for url in urls
        }
        
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                page_data = future.result()
                if page_data['success'] and page_data['content']:
                    pages.append(page_data)
            except Exception as e:
                logger.error(f"Error processing page: {e}")
    
    return {
        'query': query,
        'search_results': search_results,
        'pages': pages,
        'error': None
    }


def format_search_and_read_results(data: Dict) -> str:
    """Format search and read results for AI.
    
    Args:
        data: Result from search_and_read
        
    Returns:
        Formatted text for AI context
    """
    if data.get('error'):
        return f"Search error: {data['error']}"
    
    output = [f"**Search Query:** {data['query']}", ""]
    
    # Add search results overview
    output.append("**Search Results:**")
    for i, result in enumerate(data['search_results'], 1):
        output.append(f"{i}. {result['title']}")
        output.append(f"   {result['link']}")
    output.append("")
    
    # Add page contents
    if data['pages']:
        output.append("**Content from Top Pages:**")
        output.append("")
        
        for i, page in enumerate(data['pages'], 1):
            output.append(f"### Source {i}: {page['title']}")
            output.append(f"URL: {page['url']}")
            output.append("")
            output.append(page['content'])
            output.append("")
            output.append("---")
            output.append("")
    else:
        output.append("*No page content could be extracted.*")
    
    return "\n".join(output)


if __name__ == "__main__":
    # Test
    result = search_and_read("Python programming best practices", num_results=2)
    print(format_search_and_read_results(result))
