import heapq
from typing import Dict, List, Tuple, Set, Any
from backend.algorithms.base_algorithm import AlgoritmoBase
from backend.core.edge import Arista
from backend.core.node import Nodo

class Dijkstra(AlgoritmoBase):
    """
    Implementación del algoritmo de Dijkstra para encontrar la ruta óptima según un criterio.
    """
    def execute(self, origen: str, destino: str, criterio: str, tipos_aeronave: List[str], excluir_secundarios: bool = False) -> Dict:
        """
        Ejecuta el algoritmo de Dijkstra desde un nodo origen a un destino según el criterio dado.
        :param origen: Código IATA de aeropuerto origen.
        :param destino: Código IATA de aeropuerto destino.
        :param criterio: "cost", "time" o "distance".
        :param tipos_aeronave: Lista de tipos de aeronave a usar (en orden de preferencia).
        :param excluir_secundarios: Si es True, ignora nodos que no son hubs.
        :return: Diccionario con el camino, peso total, segmentos y metadatos.
        """
        # Initialization
        heap: List[Tuple[float, str, List[str], List[Dict[str, Any]]]] = []
        heapq.heappush(heap, (0.0, origen, [], []))
        visitados: Set[str] = set()
        mejor_peso: Dict[str, float] = {origen: 0.0}
        caminos: Dict[str, List[str]] = {origen: [origen]}
        segmentos: Dict[str, List[Dict[str, Any]]] = {origen: []}

        while heap:
            # Extract minimum
            peso_actual, actual, camino, segs = heapq.heappop(heap)
            if actual in visitados:
                continue
            visitados.add(actual)
            camino = camino + [actual]

            # End condition
            if actual == destino:
                return {
                    "path": camino,
                    "total_weight": peso_actual,
                    "segments": segs,
                    "algorithm_used": "dijkstra",
                    "criterion": criterio
                }

            nodo_actual = self.grafo.obtener_nodo(actual)
            if not nodo_actual:
                continue
            if excluir_secundarios and not nodo_actual.aeropuerto.es_centro:
                continue

            for arista in nodo_actual.obtener_aristas():
                if arista.esta_bloqueada:
                    continue
                vecino = arista.nodo_destino
                if vecino in visitados:
                    continue
                # Node repetition restriction
                if vecino in camino:
                    continue
                # Aircraft selection (first available)
                aeronave_usada = None
                for tipo in tipos_aeronave:
                    try:
                        aeronave_usada = self._get_aircraft(tipo)
                        break
                    except Exception:
                        continue
                if not aeronave_usada:
                    continue
                # Weight calculation
                if criterio == "cost":
                    peso = arista.calcular_costo(aeronave_usada)
                elif criterio == "time":
                    peso = arista.calcular_tiempo(aeronave_usada)
                elif criterio == "distance":
                    peso = arista.ruta.distancia_km
                else:
                    continue
                nuevo_peso = peso_actual + peso
                if vecino not in mejor_peso or nuevo_peso < mejor_peso[vecino]:
                    mejor_peso[vecino] = nuevo_peso
                    # Segment info
                    segmento = {
                        "origin": arista.nodo_origen,
                        "destination": arista.nodo_destino,
                        "aircraft": aeronave_usada.tipo_nombre,
                        "cost": arista.calcular_costo(aeronave_usada),
                        "time": arista.calcular_tiempo(aeronave_usada),
                        "distance_km": arista.ruta.distancia_km
                    }
                    heapq.heappush(heap, (nuevo_peso, vecino, camino, segs + [segmento]))
        # No path found
        return {"path": [], "error": "No path found"}
