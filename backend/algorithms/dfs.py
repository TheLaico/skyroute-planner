from typing import Dict, List, Set, Any
from backend.algorithms.base_algorithm import AlgoritmoBase
from backend.core.arista import Arista
from backend.core.nodo import Nodo

class DFS(AlgoritmoBase):
    """
    Implementación de búsqueda en profundidad (DFS) recursiva con backtracking.
    DFS con backtracking es apropiado para R3 porque permite explorar exhaustivamente todas las rutas posibles, tomar decisiones dinámicas y retroceder cuando se violan restricciones como el presupuesto.
    """
    def execute(self, origen: str, **kwargs) -> Dict:
        """
        Ejecuta DFS recursivo para encontrar la mejor ruta según el criterio de optimización.
        :param origen: Código IATA de aeropuerto origen.
        :param kwargs: presupuesto (float), tipos_aeronave (List[str]), optimizar (str) - "destinations" o "cost".
        :return: Diccionario con el mejor resultado encontrado.
        """
        presupuesto = kwargs.get('presupuesto', 10000.0)
        tipos_aeronave = kwargs.get('tipos_aeronave', ['Comercial'])
        optimizar = kwargs.get('optimizar', 'destinations')
        
        self._mejor = {
            "best_path": [],
            "total_cost": float('inf') if optimizar == "cost" else 0.0,
            "segments": [],
            "destinations_count": 0,
            "algorithm_used": "dfs",
            "optimize_by": optimizar
        }
        self._dfs(origen, presupuesto, tipos_aeronave, set(), [], 0.0, [], optimizar, 0)
        if not self._mejor["best_path"]:
            self._mejor["total_cost"] = 0.0
        return self._mejor

    def _dfs(self, actual: str, presupuesto: float, tipos_aeronave: List[str], visitados: Set[str], camino: List[str], costo_acum: float, segmentos: List[Dict[str, Any]], optimizar: str, profundidad: int, max_profundidad: int = 15):
        # Depth limit to avoid infinite recursion in large graphs
        if profundidad > max_profundidad:
            return
        visitados.add(actual)
        camino.append(actual)
        nodo_actual = self.grafo.obtener_nodo(actual)
        if not nodo_actual:
            visitados.remove(actual)
            camino.pop()
            return
        # Update best result
        if optimizar == "destinations":
            if len(camino) > self._mejor["destinations_count"]:
                self._mejor["best_path"] = list(camino)
                self._mejor["total_cost"] = costo_acum
                self._mejor["segments"] = list(segmentos)
                self._mejor["destinations_count"] = len(camino)
        elif optimizar == "cost":
            if len(camino) > 1 and costo_acum < self._mejor["total_cost"]:
                self._mejor["best_path"] = list(camino)
                self._mejor["total_cost"] = costo_acum
                self._mejor["segments"] = list(segmentos)
                self._mejor["destinations_count"] = len(camino)
        for arista in nodo_actual.obtener_aristas():
            if arista.esta_bloqueada:
                continue
            vecino = arista.nodo_destino
            if vecino in visitados:
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
            if nuevo_costo > presupuesto:
                continue  # Backtrack if over budget
            segmento = {
                "origin": arista.nodo_origen,
                "destination": arista.nodo_destino,
                "aircraft": aeronave_usada.tipo_nombre,
                "cost": arista.calcular_costo(aeronave_usada),
                "time": arista.calcular_tiempo(aeronave_usada),
                "distance_km": arista.ruta.distancia_km
            }
            self._dfs(vecino, presupuesto, tipos_aeronave, visitados, camino, nuevo_costo, segmentos + [segmento], optimizar, profundidad + 1, max_profundidad)
        visitados.remove(actual)
        camino.pop()

