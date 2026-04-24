from abc import ABC, abstractmethod
from typing import Dict, Any

class IService(ABC):
    @abstractmethod
    def run(self, **kwargs) -> Dict:
        """
        Run the service with the given parameters.
        :param kwargs: Parameters for the service.
        :return: Dictionary with the result of the service.
        """
        pass
