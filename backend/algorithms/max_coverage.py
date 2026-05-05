"""
Algoritmo de Cobertura Máxima con restricciones de presupuesto y tiempo.
Utiliza DFS con branch and bound para encontrar la ruta con más destinos visitados.
"""
from typing import Dict, List, Set, Tuple, Any
from backend.algorithms.base_algorithm import AlgoritmoBase


class MaxCoverageAlgorithm(AlgoritmoBase):
    """
    Encuentra la ruta que maximiza la cantidad de destinos visitados
    respetando restricciones de presupuesto y/o tiempo.
    
    Utiliza DFS con podas agresivas para exploración eficiente.
    """
    
    def execute(self, 
                origen: str, 
                presupuesto: float, 
                tiempo_max_min: float, 
                tipos_aeronave: List[str], 
                restriccion_tipo: str = "presupuesto",
                excluir_secundarios: bool = False) -> Dict[str, Any]:
        """
        Ejecuta el algoritmo de máxima cobertura.
        
        Args:
            origen: Código IATA de origen
            presupuesto: Presupuesto máximo (USD) o infinito
            tiempo_max_min: Tiempo máximo (minutos) o infinito
            tipos_aeronave: Tipos permitidos de aeronave
            restriccion_tipo: "presupuesto", "tiempo" o "ambos"
            excluir_secundarios: Ignorar nodos no-hub
            
        Returns:
            Dict con path, costos, tiempos y segmentos
        """
        mejor_camino = []
        mejor_segmentos = []
        mejor_costo = 0.0
        mejor_tiempo = 0.0
        max_destinos = 1  # Al menos el origen
        
        # Normalizar tipos de aeronave
        tipos_normalizados = [t.capitalize() for t in tipos_aeronave]
        
        # DFS con memoización
        visitados_global: Set[str] = set()
        
        def dfs(nodo_actual: str, 
                camino: List[str], 
                costo_acum: float, 
                tiempo_acum: float, 
                segmentos: List[Dict]) -> None:
            """
            DFS recursivo con exploración de múltiples caminos.
            """
            nonlocal mejor_camino, mejor_segmentos, mejor_costo, mejor_tiempo, max_destinos
            
            # Actualizar mejor solución si más destinos visitados
            if len(camino) > max_destinos:
                max_destinos = len(camino)
                mejor_camino = camino.copy()
                mejor_segmentos = segmentos.copy()
                mejor_costo = costo_acum
                mejor_tiempo = tiempo_acum
            
            # Obtener nodo actual
            nodo = self.grafo.obtener_nodo(nodo_actual)
            if not nodo:
                return
            
            # Filtro de hubs si aplica
            if excluir_secundarios and not nodo.aeropuerto.es_centro:
                return
            
            # Explorar vecinos
            for arista in nodo.obtener_aristas():
                if arista.esta_bloqueada:
                    continue
                
                vecino = arista.nodo_destino
                
                # Evitar ciclos
                if vecino in camino:
                    continue
                
                # Seleccionar mejor aeronave disponible
                aeronave_usada = None
                costo_segmento = float('inf')
                
                for tipo_norm in tipos_normalizados:
                    if tipo_norm not in arista.ruta.tipos_aeronave:
                        continue
                    
                    try:
                        aeronave = self._get_aircraft(tipo_norm)
                        costo_temp = arista.calcular_costo(aeronave)
                        
                        if costo_temp < costo_segmento:
                            costo_segmento = costo_temp
                            aeronave_usada = aeronave
                    except Exception:
                        continue
                
                if not aeronave_usada:
                    continue
                
                # Calcular nuevos costos
                nuevo_costo = costo_acum + arista.calcular_costo(aeronave_usada)
                nuevo_tiempo = tiempo_acum + arista.calcular_tiempo(aeronave_usada)
                
                # PODA: Verificar restricciones según el tipo
                if restriccion_tipo == "presupuesto":
                    if nuevo_costo > presupuesto:
                        continue
                elif restriccion_tipo == "tiempo":
                    if nuevo_tiempo > tiempo_max_min:
                        continue
                elif restriccion_tipo == "ambos":
                    if nuevo_costo > presupuesto or nuevo_tiempo > tiempo_max_min:
                        continue
                
                # Crear segmento
                segmento = {
                    "origin": arista.nodo_origen,
                    "destination": arista.nodo_destino,
                    "aircraft": aeronave_usada.tipo_nombre,
                    "cost": arista.calcular_costo(aeronave_usada),
                    "time": arista.calcular_tiempo(aeronave_usada),
                    "distance_km": arista.ruta.distancia_km
                }
                
                # Explorar esta rama
                dfs(
                    vecino,
                    camino + [vecino],
                    nuevo_costo,
                    nuevo_tiempo,
                    segmentos + [segmento]
                )
        
        # Iniciar DFS desde el origen
        dfs(origen, [origen], 0.0, 0.0, [])
        
        return {
            "path": mejor_camino,
            "total_cost": mejor_costo,
            "total_time_min": mejor_tiempo,
            "segments": mejor_segmentos,
            "destinations_count": max_destinos,
            "algorithm_used": "dfs_max_coverage"
        }


class GreedyMaxCoverageAlgorithm(AlgoritmoBase):
    """
    Alternativa greedy más rápida: en cada paso elige el vecino más "barato"
    en términos de la restricción (presupuesto o tiempo).
    """
    
    def execute(self, 
                origen: str, 
                presupuesto: float, 
                tiempo_max_min: float, 
                tipos_aeronave: List[str], 
                restriccion_tipo: str = "presupuesto",
                excluir_secundarios: bool = False) -> Dict[str, Any]:
        """
        Versión greedy para máxima cobertura.
        """
        camino = [origen]
        segmentos = []
        costo_acum = 0.0
        tiempo_acum = 0.0
        
        tipos_normalizados = [t.capitalize() for t in tipos_aeronave]
        visitados: Set[str] = {origen}
        
        while True:
            nodo_actual = self.grafo.obtener_nodo(camino[-1])
            if not nodo_actual:
                break
            
            mejor_vecino = None
            mejor_costo = float('inf')
            mejor_tiempo = float('inf')
            mejor_arista = None
            mejor_aeronave = None
            
            # Buscar el mejor siguiente nodo
            for arista in nodo_actual.obtener_aristas():
                if arista.esta_bloqueada:
                    continue
                
                vecino = arista.nodo_destino
                if vecino in visitados:
                    continue
                
                if excluir_secundarios:
                    nodo_vecino = self.grafo.obtener_nodo(vecino)
                    if nodo_vecino and not nodo_vecino.aeropuerto.es_centro:
                        continue
                
                # Seleccionar aeronave más barata
                aeronave_usada = None
                costo_segmento = float('inf')
                
                for tipo_norm in tipos_normalizados:
                    if tipo_norm not in arista.ruta.tipos_aeronave:
                        continue
                    
                    try:
                        aeronave = self._get_aircraft(tipo_norm)
                        costo_temp = arista.calcular_costo(aeronave)
                        
                        if costo_temp < costo_segmento:
                            costo_segmento = costo_temp
                            aeronave_usada = aeronave
                    except Exception:
                        continue
                
                if not aeronave_usada:
                    continue
                
                nuevo_costo = costo_acum + costo_segmento
                nuevo_tiempo = tiempo_acum + arista.calcular_tiempo(aeronave_usada)
                
                # Poda por restricciones
                if restriccion_tipo == "presupuesto":
                    if nuevo_costo > presupuesto:
                        continue
                elif restriccion_tipo == "tiempo":
                    if nuevo_tiempo > tiempo_max_min:
                        continue
                elif restriccion_tipo == "ambos":
                    if nuevo_costo > presupuesto or nuevo_tiempo > tiempo_max_min:
                        continue
                
                # Seleccionar por criterio: costo si es presupuesto, tiempo si es tiempo
                if restriccion_tipo == "presupuesto":
                    criterio = costo_segmento
                else:
                    criterio = nuevo_tiempo
                
                if criterio < mejor_costo:
                    mejor_vecino = vecino
                    mejor_costo = costo_segmento
                    mejor_tiempo = nuevo_tiempo
                    mejor_arista = arista
                    mejor_aeronave = aeronave_usada
            
            # Si no hay vecino válido, terminar
            if not mejor_vecino:
                break
            
            # Agregar al camino
            camino.append(mejor_vecino)
            visitados.add(mejor_vecino)
            costo_acum += mejor_costo
            tiempo_acum += mejor_tiempo
            
            segmentos.append({
                "origin": mejor_arista.nodo_origen,
                "destination": mejor_arista.nodo_destino,
                "aircraft": mejor_aeronave.tipo_nombre,
                "cost": mejor_costo,
                "time": mejor_aeronave.tiempo_por_km * mejor_arista.ruta.distancia_km,
                "distance_km": mejor_arista.ruta.distancia_km
            })
        
        return {
            "path": camino,
            "total_cost": costo_acum,
            "total_time_min": tiempo_acum,
            "segments": segmentos,
            "destinations_count": len(camino),
            "algorithm_used": "greedy_max_coverage"
        }
