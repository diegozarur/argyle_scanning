from typing import Dict, Optional

from app.services.scanners.scanner_creator import ScannerCreator


class ScannerService:

    def __init__(self, scanner: ScannerCreator):
        self._service = scanner

    def boot(self, scanner_settings: Dict[str, str]) -> list:
        data_extracted = self._service.run_scanner(scanner_settings)

        return data_extracted
