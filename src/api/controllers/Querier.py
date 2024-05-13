from abc import ABC, abstractmethod

class Querier(ABC):
    
    @abstractmethod
    def fetch(self) -> str:
        pass