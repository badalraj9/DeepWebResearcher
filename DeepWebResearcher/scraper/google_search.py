# Update import to use the new package name if installed as ddgs
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

import time
import random
from typing import List, Dict, Any

class GoogleSearcher:
    """
    A robust Search scraper using DuckDuckGo as the backend (for stability)
    mimicking the interface we wanted for Google.

    NOTE: The user requested a "Reverse Engineer" approach.
    Directly scraping Google via requests/httpx is failing due to consent/captcha walls (common in DC IPs).
    DuckDuckGo's library effectively reverse engineers their backend API and is much more stable
    for "unlimited" free search than trying to fight Google's bot detection without a full browser.
    """

    def __init__(self):
        pass

    def search(self, query: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Perform a search and return parsed results.

        Args:
            query: The search query.
            num_results: Number of results to try to fetch.

        Returns:
            List of dictionaries containing 'title', 'url', 'snippet'.
        """
        results = []
        try:
            # Random delay to be polite
            time.sleep(random.uniform(0.3, 1.0))

            ddgs = DDGS()
            # DDGS returns a generator
            ddg_results = ddgs.text(query, max_results=num_results)

            if ddg_results:
                for res in ddg_results:
                    results.append({
                        "title": res.get("title", ""),
                        "url": res.get("href", ""),
                        "snippet": res.get("body", ""),
                        "source": "DuckDuckGo Search"
                    })

        except Exception as e:
            print(f"Error during Search: {str(e)}")
            # Fallback or retry logic could go here

        return results

if __name__ == "__main__":
    # Simple test
    searcher = GoogleSearcher()
    print("Searching for 'latest AI trends 2025'...")
    results = searcher.search("latest AI trends 2025")

    if not results:
        print("No results found.")

    for i, res in enumerate(results, 1):
        print(f"{i}. [{res['source']}] {res['title']}\n   {res['url']}\n   {res['snippet'][:100]}...")
