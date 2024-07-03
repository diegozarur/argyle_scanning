from pathlib import Path
from flask import current_app as flask_app
from typing import Optional, Dict, Any

from app.services.scanners.scanner_creator import ScannerCreator
from app.services.scanners.upwork.creator import UpworkCreator
from app.services.scanners.service import ScannerService
from app.views.scanner.json_validator import JSONValidator
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

_scanner_selector: Dict[str, ScannerCreator] = {
    "upwork": UpworkCreator(),
}


@shared_task(bind=True, max_retries=3)
def scanner_task(self, scanner_name: Optional[str] = None, *args: Any, **kwargs: Any) -> Any:
    logger.info(f"Task {self.name} started with scanner_name: {scanner_name}")
    try:
        return _run(scanner_name)
    except Exception as e:
        logger.exception(f"Exception in task {self.name}: {e}")
        raise self.retry(exc=e, countdown=5)
    finally:
        logger.info(f"Task {self.name} ended")


def _run(scanner_name: Optional[str] = None) -> list:
    if scanner_name is None:
        raise ValueError("scanner_name must be provided")

    scanner_creator = _select_scanner(scanner_name)
    scanner_settings = _load_scanner_settings(scanner_name)

    scanner_service = ScannerService(scanner_creator)

    return scanner_service.boot(scanner_settings)


def _select_scanner(scanner_name: str) -> ScannerCreator:
    try:
        return _scanner_selector[scanner_name]
    except KeyError:
        raise Exception("Scanner not found!")


def _load_scanner_settings(scanner_name: str) -> dict:
    scanner_settings_directory = Path(
        f"{flask_app.root_path}/{flask_app.config['SCANNER_SETTINGS']}"
    )
    settings = JSONValidator.load_json_from_directory(scanner_settings_directory)
    scanner_settings = settings.get(scanner_name, {})

    JSONValidator.validate(scanner_settings)

    return scanner_settings

# class ScannerTasks(BaseTask):
#     name = __name__
#
#     _scanner_selector: Dict[str, ScannerCreator] = {
#         "upwork": UpworkCreator(),
#     }
#
#     def run(self, scanner_name: Optional[str] = None) -> str:
#         if scanner_name is None:
#             raise ValueError("scanner_name must be provided")
#
#         scanner_creator = self._select_scanner(scanner_name)
#         scanner_settings = self._load_scanner_settings(scanner_name)
#
#         scanner_service = ScannerService(scanner_creator)
#
#         return json.dumps(
#             scanner_service.boot(scanner_settings)
#         )  # Assuming the result needs to be serialized to a string
#
#     def _select_scanner(self, scanner_name: str) -> ScannerCreator:
#         try:
#             return self._scanner_selector[scanner_name]
#         except KeyError:
#             raise Exception("Scanner not found!")
#
#     def _load_scanner_settings(self, scanner_name: str) -> dict:
#         scanner_settings_directory = Path(
#             f"{flask_app.root_path}/{flask_app.config['SCANNER_SETTINGS']}"
#         )
#         settings = JSONValidator.load_json_from_directory(scanner_settings_directory)
#         scanner_settings = settings.get(scanner_name, {})
#
#         JSONValidator.validate(scanner_settings)
#
#         return scanner_settings
#
#
# current_app.register_task(ScannerTasks)
