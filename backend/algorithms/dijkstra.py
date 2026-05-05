import heapq
from typing import Dict, List, Tuple, Set, Any
from backend.algorithms.base_algorithm import AlgoritmoBase
from backend.core.arista import Arista
from backend.core.nodo import Nodo

class Dijkstra(AlgoritmoBase):
    """
    Implementación del algoritmo de Dijkstra para encontrar la ruta óptima según un criterio.
    """
    def execute(self, origen: str, destino: str, criterio: str, tipos_aeronave: List[str], excluir_secundarios: bool = False) -> Dict:
        """
        Ejecuta el algoritmo de Dijkstra desde un nodo origen a un destino según el criterio dado.
        :param origen: Código IATA de aeropuerto origen.
        :param destino: Código IATA de aeropuerto destino.
        :param criterio: "costo"/"cost", "tiempo"/"time" o "distancia"/"distance" (acepta español e inglés).
        :param tipos_aeronave: Lista de tipos de aeronave a usar (en orden de preferencia).
        :param excluir_secundarios: Si es True, ignora nodos que no son hubs.
        :return: Diccionario con el camino, peso total, segmentos y metadatos.
        """
        # Normalizar criterio: aceptar español e inglés
        criterio_norm = criterio.lower().strip()
        if criterio_norm in ["costo", "cost"]:
            criterio_norm = "cost"
        elif criterio_norm in ["tiempo", "time"]:
            criterio_norm = "time"
        elif criterio_norm in ["distancia", "distance"]:
            criterio_norm = "distance"
        else:
            return {"path": [], "error": f"Criterio invalido: {criterio}"}
        
        # DEBUG
        DEBUG = True
        if DEBUG:
            print(f"[DIJKSTRA DEBUG] Iniciando busqueda")
            print(f"  Origen: {origen}, Destino: {destino}, Criterio: {criterio_norm}")
            print(f"  Tipos de aeronave: {tipos_aeronave}")
        
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
            
            if DEBUG and len(visitados) <= 5:
                print(f"  [NODO] Visitando: {actual}, peso acum: {peso_actual:.2f}")

            # End condition
            if actual == destino:
                if DEBUG:
                    print(f"  [DESTINO] Alcanzado: {destino} en {len(camino)} hops")
                return {
                    "path": camino,
                    "total_weight": peso_actual,
                    "segments": segs,
                    "algorithm_used": "dijkstra",
                    "criterion": criterio
                }

            nodo_actual = self.grafo.obtener_nodo(actual)
            if not nodo_actual:
                if DEBUG:
                    print(f"  [ERROR] Nodo {actual} no encontrado")
                continue
            
            aristas = nodo_actual.obtener_aristas()
            if DEBUG and len(visitados) <= 3:
                print(f"    [{actual}] tiene {len(aristas)} aristas salientes")

            if excluir_secundarios and not nodo_actual.aeropuerto.es_centro:
                if DEBUG:
                    print(f"    [{actual}] descartado - no es hub")
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
                
                # Aircraft selection - NORMALIZAR Y VALIDAR
                tipos_normalizados = [t.capitalize() for t in tipos_aeronave]
                
                aeronave_usada = None
                for tipo_norm in tipos_normalizados:
                    # VALIDAR que el tipo esté en la ruta
                    if tipo_norm not in arista.ruta.tipos_aeronave:
                        if DEBUG and len(visitados) <= 2:
                            print(f"      {arista.nodo_origen}->{vecino}: tipo {tipo_norm} no en {arista.ruta.tipos_aeronave}")
                        continue
                    
                    try:
                        aeronave_usada = self._get_aircraft(tipo_norm)
                        break
                    except Exception as e:
                        if DEBUG and len(visitados) <= 2:
                            print(f"      {arista.nodo_origen}->{vecino}: error al obtener {tipo_norm}: {e}")
                        continue
                
                if not aeronave_usada:
                    continue
                
                # Weight calculation
                if criterio_norm == "cost":
                    peso = arista.calcular_costo(aeronave_usada)
                elif criterio_norm == "time":
                    peso = arista.calcular_tiempo(aeronave_usada)
                elif criterio_norm == "distance":
                    peso = arista.ruta.distancia_km
                else:
                    continue
                
                nuevo_peso = peso_actual + peso
                if vecino not in mejor_peso or nuevo_peso < mejor_peso[vecino]:
                    mejor_peso[vecino] = nuevo_peso
                    
                    if DEBUG and len(visitados) <= 2:
                        print(f"      {arista.nodo_origen}->{vecino}: PUSH ({aeronave_usada.tipo_nombre}, peso: {peso:.2f})")
                    
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
        if DEBUG:
            print(f"  [NO RUTA] No se encontro: {origen}->{destino}")
            print(f"    Visitados: {visitados}")
        return {"path": [], "error": "No path found"}
