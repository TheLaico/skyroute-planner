"""
Dijkstra paso a paso con visualización en consola para R3.
"""
from typing import Dict, List, Tuple
from backend.algorithms.base_algorithm import AlgoritmoBase


class DijkstraStepByStep(AlgoritmoBase):
    """Dijkstra con pasos visualizados en consola."""
    
    def execute(self, origen: str, destino: str, tipos_aeronave: List[str], 
                mostrar_pasos: bool = True) -> Dict:
        """
        Ejecuta Dijkstra mostrando cada paso.
        
        Args:
            origen: Código IATA origen
            destino: Código IATA destino
            tipos_aeronave: Tipos permitidos
            mostrar_pasos: Si es True, pausa entre pasos
            
        Returns:
            Dict con path, costo y segmentos
        """
        
        nodo_origen = self.grafo.obtener_nodo(origen)
        if not nodo_origen:
            return {"error": f"Origen '{origen}' no existe"}
        
        nodo_destino = self.grafo.obtener_nodo(destino)
        if not nodo_destino:
            return {"error": f"Destino '{destino}' no existe"}
        
        # Inicializar estructuras
        distancias = {origen: 0.0}
        previos = {}
        no_visitados = {origen}
        todos_nodos = {n.aeropuerto.codigo_iata for n in self.grafo.obtener_todos_nodos()}
        no_visitados.update(todos_nodos - {origen})
        
        paso = 0
        tipos_norm = [t.capitalize() for t in tipos_aeronave]
        
        print("\n" + "="*70)
        print("DIJKSTRA PASO A PASO")
        print("="*70)
        print(f"Origen: {origen} → Destino: {destino}")
        print("="*70)
        
        # Algoritmo
        while no_visitados:
            # Encontrar no visitado con menor distancia
            actual = None
            min_dist = float('inf')
            
            for nodo in no_visitados:
                if nodo in distancias and distancias[nodo] < min_dist:
                    min_dist = distancias[nodo]
                    actual = nodo
            
            if actual is None or actual == destino:
                break
            
            paso += 1
            
            # Mostrar estado actual
            print(f"\n{'─'*70}")
            print(f"PASO {paso}: Procesando nodo {actual}")
            print(f"{'─'*70}")
            print(f"Distancia acumulada: {distancias[actual]:.2f}")
            
            nodo_actual = self.grafo.obtener_nodo(actual)
            aristas = nodo_actual.obtener_aristas()
            
            # Mostrar vecinos
            print(f"\nVecinos accesibles desde {actual}:")
            
            vecinos_validos = []
            for arista in aristas:
                if arista.esta_bloqueada:
                    continue
                
                vecino = arista.nodo_destino
                
                # Seleccionar mejor aeronave
                aeronave_usada = None
                costo_segmento = float('inf')
                
                for tipo_norm in tipos_norm:
                    if tipo_norm not in arista.ruta.tipos_aeronave:
                        continue
                    try:
                        aeronave = self._get_aircraft(tipo_norm)
                        costo = arista.calcular_costo(aeronave)
                        if costo < costo_segmento:
                            costo_segmento = costo
                            aeronave_usada = aeronave
                    except:
                        continue
                
                if not aeronave_usada:
                    continue
                
                distancia_arista = arista.calcular_costo(aeronave_usada)
                nueva_distancia = distancias[actual] + distancia_arista
                
                # Mostrar vecino
                estado = "NO VISITADO"
                if vecino in distancias:
                    if nueva_distancia < distancias[vecino]:
                        estado = "ACTUALIZAR"
                    else:
                        estado = "SIN CAMBIO"
                
                print(f"  {actual} → {vecino}: ${distancia_arista:.2f} "
                      f"(total: ${nueva_distancia:.2f}) [{estado}]")
                
                vecinos_validos.append((vecino, nueva_distancia, aeronave_usada, distancia_arista))
                
                # Actualizar si es mejor
                if vecino not in distancias or nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    previos[vecino] = (actual, aeronave_usada, distancia_arista)
            
            if not vecinos_validos:
                print(f"  (Sin vecinos accesibles)")
            
            # Mostrar estado de no visitados
            print(f"\nEstado de nodos no visitados:")
            print(f"  {', '.join(sorted(no_visitados - {actual}))}")
            
            # Eliminar visitado
            no_visitados.discard(actual)
            
            # Pausa
            if mostrar_pasos and no_visitados:
                input("\n[Presione Enter para continuar...]")
        
        # Reconstruir camino
        print("\n" + "="*70)
        print("RESULTADO")
        print("="*70)
        
        if destino not in distancias:
            print(f"❌ No hay camino desde {origen} a {destino}")
            return {
                "path": [],
                "total_cost": 0.0,
                "segments": [],
                "error": "No existe ruta"
            }
        
        # Reconstruir ruta
        camino = []
        segmentos = []
        nodo_actual = destino
        
        while nodo_actual != origen:
            camino.append(nodo_actual)
            if nodo_actual in previos:
                prev, aeronave, costo = previos[nodo_actual]
                segmentos.append({
                    "origin": prev,
                    "destination": nodo_actual,
                    "aircraft": aeronave.tipo_nombre,
                    "cost": costo
                })
                nodo_actual = prev
            else:
                break
        
        camino.append(origen)
        camino.reverse()
        segmentos.reverse()
        
        # Mostrar resultado final
        print(f"\nRuta encontrada:")
        print(f"  {' → '.join(camino)}")
        print(f"\nCosto total: ${distancias[destino]:.2f}")
        print(f"Escalas: {len(camino) - 2 if len(camino) > 1 else 0}")
        
        if segmentos:
            print(f"\nDetalles:")
            for i, seg in enumerate(segmentos, 1):
                print(f"  {i}. {seg['origin']} → {seg['destination']} "
                      f"({seg['aircraft']}) ${seg['cost']:.2f}")
        
        return {
            "path": camino,
            "total_cost": distancias[destino],
            "segments": segmentos,
            "algorithm": "dijkstra_step_by_step"
        }
