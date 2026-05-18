
import time
import random
import logging
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

class EthicalComplianceGate:
    def __init__(self, user_agent: str = "VeritasCleanScraper/1.0"):
        """Initializes the compliance gate with an honest bot identity descriptor."""
        self.user_agent = user_agent
        self.parsers = {}

    def _get_robots_url(self, target_url: str) -> str:
        """Extracts the base domain and points to its root robots.txt path."""
        parsed_url = urlparse(target_url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

    def is_scraping_allowed(self, target_url: str) -> bool:
        """Downloads and checks robots.txt rules to ensure compliance."""
        robots_url = self._get_robots_url(target_url)
        
        # Cache the rule file so we don't spam the server downloading it repeatedly
        if robots_url not in self.parsers:
            logging.info(f"Compliance Check: Fetching rules from {robots_url}")
            parser = RobotFileParser()
            try:
                parser.set_url(robots_url)
                parser.read()
                self.parsers[robots_url] = parser
            except Exception as e:
                logging.warning(f"Compliance Warning: Unable to parse robots.txt ({e}). Defaulting to cautious entry.")
                return True

        # Test our specific URL against their rules
        allowed = self.parsers[robots_url].can_fetch(self.user_agent, target_url)
        if not allowed:
            logging.error(f"ETHICAL VIOLATION BLOCKED: Target path [{target_url}] is restricted by robots.txt!")
        else:
            logging.info(f"ETHICAL CLEARANCE GRANTED: Path [{target_url}] is safe to process.")
        return allowed

    def enforce_politeness_delay(self):
        """Introduces a randomized throttling delay to prevent server overload."""
        delay = random.uniform(2.0, 4.5)
        logging.info(f"Politeness Gate: Throttling request. Sleeping for {delay:.2f} seconds...")
        time.sleep(delay)


