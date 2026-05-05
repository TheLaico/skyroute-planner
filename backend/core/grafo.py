from typing import Dict, List, Optional
from backend.models.airport import Aeropuerto
from backend.models.route import Ruta
from backend.core.nodo import Nodo
from backend.core.arista import Arista
from backend.interfaces.i_graph import IGraph

class Grafo(IGraph):
    """
    Implementación de un grafo dirigido de aeropuertos y rutas.
    """
    def __init__(self):
        """
        Inicializa el grafo con un diccionario vacío de nodos.
        """
        self._nodos: Dict[str, Nodo] = {}

    def agregar_nodo(self, aeropuerto: Aeropuerto):
        """
        Agrega un nodo al grafo a partir de un aeropuerto.
        :param aeropuerto: Instancia de Aeropuerto.
        """
        self._nodos[aeropuerto.codigo_iata] = Nodo(aeropuerto)

    def agregar_arista(self, ruta: Ruta):
        """
        Agrega una arista al grafo a partir de una ruta.
        :param ruta: Instancia de Ruta.
        """
        origen = ruta.origen
        destino = ruta.destino
        if origen in self._nodos and destino in self._nodos:
            arista = Arista(ruta, origen, destino)
            self._nodos[origen].agregar_arista(arista)

    def obtener_vecinos(self, codigo_iata: str) -> List[Arista]:
        """
        Obtiene las aristas no bloqueadas del nodo especificado.
        :param codigo_iata: Código IATA del aeropuerto.
        :return: Lista de aristas no bloqueadas.
        """
        nodo = self._nodos.get(codigo_iata)
        if nodo:
            return [a for a in nodo.obtener_aristas() if not a.esta_bloqueada]
        return []

    def obtener_nodo(self, codigo_iata: str) -> Optional[Nodo]:
        """
        Obtiene el nodo correspondiente al código IATA.
        :param codigo_iata: Código IATA del aeropuerto.
        :return: Nodo o None si no existe.
        """
        return self._nodos.get(codigo_iata)

    def obtener_todos_nodos(self) -> List[Nodo]:
        """
        Retorna todos los nodos del grafo.
        :return: Lista de nodos.
        """
        return list(self._nodos.values())

    def obtener_todas_aristas(self) -> List[Arista]:
        """
        Retorna todas las aristas del grafo.
        :return: Lista de aristas.
        """
        aristas = []
        for nodo in self._nodos.values():
            aristas.extend(nodo.obtener_aristas())
        return aristas

    def bloquear_arista(self, origen: str, destino: str):
        """
        Marca la arista entre origen y destino como bloqueada.
        :param origen: Código IATA de origen.
        :param destino: Código IATA de destino.
        """
        nodo = self._nodos.get(origen)
        if nodo:
            for arista in nodo.obtener_aristas():
                if arista.nodo_destino == destino:
                    arista.ruta.esta_bloqueada = True

    def desbloquear_arista(self, origen: str, destino: str):
        """
        Desbloquea la arista entre origen y destino.
        :param origen: Código IATA de origen.
        :param destino: Código IATA de destino.
        """
        nodo = self._nodos.get(origen)
        if nodo:
            for arista in nodo.obtener_aristas():
                if arista.nodo_destino == destino:
                    arista.ruta.esta_bloqueada = False

    def obtener_hubs(self) -> List[Nodo]:
        """
        Retorna los nodos que son hubs (es_centro == True).
        :return: Lista de nodos hubs.
        """
        return [n for n in self._nodos.values() if n.aeropuerto.es_centro]

