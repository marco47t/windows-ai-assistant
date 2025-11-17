from duckduckgo_search import DDGS

def search_duckduckgo(query, max_results=5):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
        return [{"title": r['title'], "link": r['href'], "snippet": r['body']} for r in results]

if __name__ == "__main__":
    for result in search_duckduckgo('Python programming', 3):
        print(f"{result['title']}
{result['link']}
{result['snippet']}
---")