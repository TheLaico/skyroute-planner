from abc import ABC, abstractmethod
from typing import Dict, Any

class IService(ABC):
    @abstractmethod
    def run(self, *args, **kwargs) -> Dict:
        """
        Run the service with the given parameters.
        :param args: Positional arguments for the service.
        :param kwargs: Keyword arguments for the service.
        :return: Dictionary with the result of the service.
        """
        pass
