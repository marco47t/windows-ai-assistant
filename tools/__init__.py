"""Tools for the AI assistant."""

from tools.web_search import search_web, format_search_results
from tools.web_navigator import scrape_webpage

__all__ = [
    'search_web',
    'format_search_results',
    'scrape_webpage',
]
