from typing import Any, Dict, List


class BaseRepository:
    def create(self, data: Dict[str, Any]) -> None:
        raise NotImplementedError

    def read(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def update(self, query: Dict[str, Any], data: Dict[str, Any]) -> None:
        raise NotImplementedError

    def delete(self, query: Dict[str, Any]) -> None:
        raise NotImplementedError
