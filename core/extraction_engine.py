
import logging
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

class AsynchronousExtractor:
    def __init__(self):
        """Initializes settings to standardize browser behaviors."""
        # This removes the automated script marker from the browser
        self.browser_args = ["--disable-blink-features=AutomationControlled"]
        # Standard desktop web browser identity string
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

    def _extract_by_text_density(self, html_content: str) -> str:
        """Finds the main reading text automatically if website tags change."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove junk elements that confuse AI models (like scripts and style styles)
        for junk in soup(["script", "style", "nav", "footer", "header"]):
            junk.extract()
            
        best_block = ""
        max_text_len = 0
        
        # Look through all standard text containers on the page
        for container in soup.find_all(['div', 'main', 'article', 'section']):
            # Count the actual letters inside this specific layout box
            text = container.get_text(separator=" ", strip=True)
            # If this box has the most text, it is likely the main article content
            if len(text) > max_text_len:
                max_text_len = len(text)
                best_block = text
                
        return best_block

    async def fetch_page_content(self, url: str) -> str:
        """Opens a standardized browser window and extracts clean text data."""
        logging.info(f"Extraction Engine: Launching standardized browser session for {url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=self.browser_args)
            
            # Open a browser tab using a normal desktop layout and identity
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent=self.user_agent
            )
            page = await context.new_page()
            
            try:
                logging.info(f"Extraction Engine: Navigating to page node...")
                await page.goto(url, timeout=30000, wait_until="domcontentloaded")
                
                raw_html = await page.content()
                
                # Run our smart text detector tool
                clean_text = self._extract_by_text_density(raw_html)
                logging.info(f"Extraction Engine: Successfully captured {len(clean_text)} characters of pure content.")
                return clean_text
                
            except Exception as e:
                logging.error(f"Extraction Engine Failure: Could not download page elements: {e}")
                return ""
            finally:
                await browser.close()

