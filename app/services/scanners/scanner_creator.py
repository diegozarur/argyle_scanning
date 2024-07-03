from abc import abstractmethod
from typing import Dict, List, Any, Optional

from app.services.scanners.scanner import Scanner


class ScannerCreator:
    def __init__(self) -> None:
        self._scanner: Optional[Scanner] = None

    @abstractmethod
    def create_scanner(self, scanner_settings: Dict[str, str]) -> Scanner:
        pass

    def run_scanner(self, scanner_settings: Dict[str, str]) -> List[Dict[str, Any]]:
        self._scanner = self.create_scanner(scanner_settings)

        data_to_send = self._scanner.run()

        return data_to_send
