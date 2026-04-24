from abc import ABC, abstractmethod
from typing import Any, List, Dict

class IGraph(ABC):
    @abstractmethod
    def add_node(self, node: Any) -> None:
        """
        Add a node to the graph.
        :param node: The node to add.
        :return: None
        """
        pass

    @abstractmethod
    def add_edge(self, node1: Any, node2: Any, **kwargs) -> None:
        """
        Add an edge between two nodes.
        :param node1: The first node.
        :param node2: The second node.
        :param kwargs: Additional edge attributes.
        :return: None
        """
        pass

    @abstractmethod
    def get_neighbors(self, node: Any) -> List[Any]:
        """
        Get the neighbors of a node.
        :param node: The node to get neighbors for.
        :return: List of neighboring nodes.
        """
        pass

    @abstractmethod
    def get_node(self, node_id: Any) -> Any:
        """
        Get a node by its identifier.
        :param node_id: The identifier of the node.
        :return: The node object.
        """
        pass

    @abstractmethod
    def get_all_nodes(self) -> List[Any]:
        """
        Get all nodes in the graph.
        :return: List of all nodes.
        """
        pass

    @abstractmethod
    def get_all_edges(self) -> List[Any]:
        """
        Get all edges in the graph.
        :return: List of all edges.
        """
        pass

    @abstractmethod
    def block_edge(self, node1: Any, node2: Any) -> None:
        """
        Block the edge between two nodes.
        :param node1: The first node.
        :param node2: The second node.
        :return: None
        """
        pass

    @abstractmethod
    def unblock_edge(self, node1: Any, node2: Any) -> None:
        """
        Unblock the edge between two nodes.
        :param node1: The first node.
        :param node2: The second node.
        :return: None
        """
        pass
