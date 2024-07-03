import json
from pathlib import Path


class JSONValidator:
    @staticmethod
    def load_json_from_directory(directory: Path) -> dict:
        json_files = list(directory.glob("*.json"))
        if not json_files:
            raise Exception(f"No JSON file found in the directory=[{directory}]!")

        for file_path in json_files:
            try:
                with open(file_path, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                continue

        raise Exception("Error decoding JSON files in the directory=[{directory}]!")
