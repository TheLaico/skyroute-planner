from collections import deque
from typing import Dict, List, Set, Any
from backend.algorithms.base_algorithm import AlgoritmoBase
from backend.core.arista import Arista
from backend.core.nodo import Nodo

class BFS(AlgoritmoBase):
    """
    Implementación de búsqueda en anchura (BFS) para maximizar destinos visitados bajo restricciones.
    """
    def execute(self, origen: str, presupuesto: float, tiempo_max_min: float, tipos_aeronave: List[str], excluir_secundarios: bool = False) -> Dict:
        """
        Ejecuta BFS desde el nodo origen, acumulando costo y tiempo, y deteniendo ramas que exceden restricciones.
        :param origen: Código IATA de aeropuerto origen.
        :param presupuesto: Presupuesto máximo permitido.
        :param tiempo_max_min: Tiempo máximo permitido en minutos.
        :param tipos_aeronave: Lista de tipos de aeronave a usar (en orden de preferencia).
        :param excluir_secundarios: Si es True, ignora nodos que no son hubs.
        :return: Diccionario con el mejor camino y métricas.
        """
        # BFS justification: level-by-level guarantees minimum number of hops
        cola = deque()
        cola.append((origen, [origen], 0.0, 0.0, []))  # (current, path, cost, time, segments)
        mejor_camino = []
        mejor_segmentos = []
        mejor_costo = 0.0
        mejor_tiempo = 0.0
        max_destinos = 0
        visitados_global: Set[str] = set()

        while cola:
            # Queue structure: (current, path, cost, time, segments)
            actual, camino, costo_acum, tiempo_acum, segmentos = cola.popleft()
            visitados_global.add(actual)
            nodo_actual = self.grafo.obtener_nodo(actual)
            if not nodo_actual:
                continue
            if excluir_secundarios and not nodo_actual.aeropuerto.es_centro:
                continue
            # Update best if more destinations
            if len(camino) > max_destinos:
                mejor_camino = camino
                mejor_segmentos = segmentos
                mejor_costo = costo_acum
                mejor_tiempo = tiempo_acum
                max_destinos = len(camino)
            for arista in nodo_actual.obtener_aristas():
                if arista.esta_bloqueada:
                    continue
                vecino = arista.nodo_destino
                # Never visit the same airport twice in a route
                if vecino in camino:
                    continue
                # Aircraft selection: use the cheapest available
                aeronave_usada = None
                menor_costo = float('inf')
                for tipo in tipos_aeronave:
                    try:
                        aeronave = self._get_aircraft(tipo)
                        costo = arista.calcular_costo(aeronave)
                        if costo < menor_costo:
                            menor_costo = costo
                            aeronave_usada = aeronave
                    except Exception:
                        continue
                if not aeronave_usada:
                    continue
                nuevo_costo = costo_acum + arista.calcular_costo(aeronave_usada)
                nuevo_tiempo = tiempo_acum + arista.calcular_tiempo(aeronave_usada)
                # Stop expanding branch if over budget or time
                if nuevo_costo > presupuesto or nuevo_tiempo > tiempo_max_min:
                    continue
                segmento = {
                    "origin": arista.nodo_origen,
                    "destination": arista.nodo_destino,
                    "aircraft": aeronave_usada.tipo_nombre,
                    "cost": arista.calcular_costo(aeronave_usada),
                    "time": arista.calcular_tiempo(aeronave_usada),
                    "distance_km": arista.ruta.distancia_km
                }
                cola.append((vecino, camino + [vecino], nuevo_costo, nuevo_tiempo, segmentos + [segmento]))
        return {
            "path": mejor_camino,
            "total_cost": mejor_costo,
            "total_time_min": mejor_tiempo,
            "segments": mejor_segmentos,
            "destinations_count": max_destinos,
            "algorithm_used": "bfs"
        }

