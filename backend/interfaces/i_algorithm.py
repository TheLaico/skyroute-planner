from abc import ABC, abstractmethod
from typing import Any, Dict

class IAlgorithm(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> Dict:
        """
        Execute the algorithm from the origin node.
        :param args: Positional arguments for the algorithm.
        :param kwargs: Additional keyword arguments for the algorithm.
        :return: Dictionary with the result of the algorithm.
        """
        pass
