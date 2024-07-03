import json
from pathlib import Path


class JSONValidator:
    REQUIRED_KEYS = {"username", "password", "secret_answer"}

    @classmethod
    def validate(cls, data: dict) -> None:
        missing_keys = cls.REQUIRED_KEYS - data.keys()
        if missing_keys:
            raise Exception(
                f"Missing required keys in credentials: {', '.join(missing_keys)}"
            )

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
