from abc import ABC, abstractmethod
from typing import Any, Dict

class IAlgorithm(ABC):
    @abstractmethod
    def execute(self, graph: Any, origin: Any, **kwargs) -> Dict:
        """
        Execute the algorithm on the given graph from the origin node.
        :param graph: The graph to operate on.
        :param origin: The origin node.
        :param kwargs: Additional parameters for the algorithm.
        :return: Dictionary with the result of the algorithm.
        """
        pass
