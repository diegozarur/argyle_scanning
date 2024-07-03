from abc import abstractmethod
from typing import List, Dict, Any


class Scanner:

    @abstractmethod
    def run(self) -> List[Dict[str, Any]]:
        pass
