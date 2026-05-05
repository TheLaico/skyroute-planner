from abc import ABC, abstractmethod
from typing import Any, List


class IGraph(ABC):
    @abstractmethod
    def agregar_nodo(self, *args, **kwargs) -> None:
        """
        Agrega un nodo al grafo.
        :param args: Argumentos posicionales.
        :param kwargs: Argumentos nombrados.
        """
        pass

    @abstractmethod
    def agregar_arista(self, *args, **kwargs) -> None:
        """
        Agrega una arista al grafo.
        :param args: Argumentos posicionales.
        :param kwargs: Argumentos nombrados.
        """
        pass

    @abstractmethod
    def obtener_vecinos(self, codigo_iata: str) -> List[Any]:
        """
        Obtiene los vecinos (aristas no bloqueadas) de un nodo.
        :param codigo_iata: Código IATA del nodo.
        :return: Lista de aristas no bloqueadas.
        """
        pass

    @abstractmethod
    def obtener_nodo(self, codigo_iata: str) -> Any:
        """
        Obtiene un nodo por su código IATA.
        :param codigo_iata: Código IATA del nodo.
        :return: El nodo o None.
        """
        pass

    @abstractmethod
    def obtener_todos_nodos(self) -> List[Any]:
        """
        Retorna todos los nodos del grafo.
        :return: Lista de nodos.
        """
        pass

    @abstractmethod
    def obtener_todas_aristas(self) -> List[Any]:
        """
        Retorna todas las aristas del grafo.
        :return: Lista de aristas.
        """
        pass

    @abstractmethod
    def bloquear_arista(self, origen: str, destino: str) -> None:
        """
        Bloquea la arista entre origen y destino.
        :param origen: Código IATA de origen.
        :param destino: Código IATA de destino.
        """
        pass

    @abstractmethod
    def desbloquear_arista(self, origen: str, destino: str) -> None:
        """
        Desbloquea la arista entre origen y destino.
        :param origen: Código IATA de origen.
        :param destino: Código IATA de destino.
        """
        pass