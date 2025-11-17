"""Web navigation and scraping using requests and BeautifulSoup."""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from core.logger import logger


def fetch_webpage(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch webpage content.
    
    Args:
        url: URL to fetch
        timeout: Request timeout in seconds
        
    Returns:
        HTML content or None if error
    """
    try:
        logger.info(f"Fetching: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        return response.text
        
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None


def extract_text(html: str) -> str:
    """Extract clean text from HTML.
    
    Args:
        html: HTML content
        
    Returns:
        Cleaned text
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
        
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        return ""


def extract_links(html: str, base_url: str) -> List[Dict[str, str]]:
    """Extract all links from HTML.
    
    Args:
        html: HTML content
        base_url: Base URL for resolving relative links
        
    Returns:
        List of links with text and href
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True)
            
            # Resolve relative URLs
            if href.startswith('/'):
                href = base_url.rstrip('/') + href
            elif not href.startswith('http'):
                continue
            
            if text and href:
                links.append({
                    'text': text,
                    'url': href
                })
        
        return links
        
    except Exception as e:
        logger.error(f"Error extracting links: {e}")
        return []


def scrape_webpage(url: str) -> Dict[str, any]:
    """Scrape webpage for text and links.
    
    Args:
        url: URL to scrape
        
    Returns:
        Dict with url, text, and links
    """
    html = fetch_webpage(url)
    
    if not html:
        return {
            'url': url,
            'text': '',
            'links': [],
            'error': 'Failed to fetch webpage'
        }
    
    text = extract_text(html)
    links = extract_links(html, url)
    
    return {
        'url': url,
        'text': text[:5000],  # Limit text to 5000 chars
        'links': links[:20],   # Limit to 20 links
        'error': None
    }


if __name__ == "__main__":
    # Test scraping
    result = scrape_webpage("https://python.org")
    
    print(f"URL: {result['url']}")
    print(f"\nText preview (first 500 chars):")
    print(result['text'][:500])
    print(f"\nFound {len(result['links'])} links")
    print("\nFirst 5 links:")
    for link in result['links'][:5]:
        print(f"  - {link['text']}: {link['url']}")
