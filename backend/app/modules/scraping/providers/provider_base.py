from abc import ABC, abstractmethod
from typing import Iterable, Dict, Any


class ProviderBase(ABC):
    @abstractmethod
    def search_companies(self, query: str) -> Iterable[Dict[str, Any]]:
        pass
