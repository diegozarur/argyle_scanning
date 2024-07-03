from app.services.scanners.scanner_creator import ScannerCreator
from typing import Dict
from .scanner import UpworkScanner
from .scraper import UpworkScraper
from app.services.scanners.scanner import Scanner


class UpworkCreator(ScannerCreator):
    def create_scanner(self, scanner_settings: Dict[str, str]) -> Scanner:
        scrapper = UpworkScraper(scanner_settings)
        return UpworkScanner(scrapper)
