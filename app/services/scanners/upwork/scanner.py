from typing import Dict, Any
from app.services.scanners.scanner import Scanner
from .scraper import UpworkScraper


class UpworkScanner(Scanner):

    def __init__(self, scrapper: UpworkScraper):
        self._scrapper = scrapper

    def run(self) -> Dict[str, Any]:
        return self._scrapper.start_searching()
