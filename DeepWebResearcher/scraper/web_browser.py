from playwright.sync_api import sync_playwright
import html2text
from bs4 import BeautifulSoup
import time
from typing import Dict, Any

class WebBrowser:
    """
    A headless browser scraper using Playwright.
    Capable of rendering JS-heavy websites and extracting main content.
    """

    def __init__(self):
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False
        self.converter.ignore_images = True
        self.converter.ignore_tables = False
        self.converter.body_width = 0  # No wrapping

    def scrape_url(self, url: str) -> str:
        """
        Scrape a single URL using a headless browser.

        Args:
            url: The URL to scrape.

        Returns:
            Markdown formatted text of the page content.
        """
        content = ""

        try:
            with sync_playwright() as p:
                # Launch browser
                # We use chromium, headless=True
                browser = p.chromium.launch(headless=True)

                # specific context with a real user agent to avoid blocking
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                    viewport={"width": 1280, "height": 720}
                )

                page = context.new_page()

                # Navigate
                print(f"Navigating to {url}...")
                try:
                    page.goto(url, timeout=30000, wait_until="domcontentloaded")
                    # Small wait for hydration / dynamic content
                    page.wait_for_timeout(2000)
                except Exception as e:
                    print(f"Navigation error for {url}: {e}")
                    browser.close()
                    return f"Error: Could not load page {url}. {str(e)}"

                # Get content
                html_content = page.content()

                # Clean with BeautifulSoup first (remove scripts, styles, etc)
                soup = BeautifulSoup(html_content, 'html.parser')

                for script in soup(["script", "style", "nav", "footer", "header", "noscript", "iframe", "svg"]):
                    script.decompose()

                # Extract text using html2text for better formatting
                cleaned_html = str(soup)
                content = self.converter.handle(cleaned_html)

                browser.close()

        except Exception as e:
            print(f"Browser error: {str(e)}")
            return f"Error processing {url}: {str(e)}"

        return content

if __name__ == "__main__":
    # Simple test
    browser = WebBrowser()
    url = "https://example.com"
    print(f"Scraping {url}...")
    result = browser.scrape_url(url)
    print("--- RESULT ---")
    print(result[:500])
