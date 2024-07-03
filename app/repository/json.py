import json
import os
from typing import List, Dict, Any
from flask import current_app
from .base import BaseRepository


class JSONRepository(BaseRepository):
    def __init__(self) -> None:
        self.directory: str = current_app.config["SCANNER_SETTINGS"]

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def _list_all_files(self) -> List[str]:
        return [f for f in os.listdir(self.directory) if f.endswith(".json")]

    def _read_all_data(self) -> List[Dict[str, Any]]:
        all_data: List[Dict[str, Any]] = []
        for file_name in self._list_all_files():
            file_path = os.path.join(self.directory, file_name)
            with open(file_path, "r") as f:
                all_data.extend(json.load(f))
        return all_data

    def _write_all_data(
        self, data: List[Dict[str, Any]], file_name: str = "data.json"
    ) -> None:
        file_path = os.path.join(self.directory, file_name)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def create(self, data: Dict[str, Any], file_name: str = "data.json") -> None:
        all_data = self._read_all_data()
        all_data.append(data)
        self._write_all_data(all_data, file_name)

    def read(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        all_data = self._read_all_data()
        return [
            item for item in all_data if all(item.get(k) == v for k, v in query.items())
        ]

    def update(
        self, query: Dict[str, Any], data: Dict[str, Any], file_name: str = "data.json"
    ) -> None:
        all_data = self._read_all_data()
        updated = False
        for index, item in enumerate(all_data):
            if all(item.get(k) == v for k, v in query.items()):
                all_data[index].update(data)
                updated = True
        if updated:
            self._write_all_data(all_data, file_name)

    def delete(self, query: Dict[str, Any], file_name: str = "data.json") -> None:
        all_data = self._read_all_data()
        all_data = [
            item
            for item in all_data
            if not all(item.get(k) == v for k, v in query.items())
        ]
        self._write_all_data(all_data, file_name)
