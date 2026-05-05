"""
Punto de entrada principal para la consola de SkyRoute Planner.
Menú interactivo para cargar red, ver aeropuertos, planificar rutas, simular interrupciones y generar reportes.

"""
import sys
import json
from typing import Union
from pathlib import Path

# Agregar el directorio padre (raíz del proyecto) al sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.loaders.json_loader import JSONLoader
from backend.loaders.graph_builder import GraphBuilder
from backend.core.grafo import Grafo
from backend.services.route_planner import RoutePlannerService
from backend.services.itinerary_service import ItineraryService
from backend.services.budget_manager import BudgetManagerService
from backend.services.interruption_service import InterruptionService
from backend.services.report_service import ReportService
from backend.config import Config
from backend.algorithms.dijkstra_step_by_step import DijkstraStepByStep




def mostrar_menu():
    print("\n=== SkyRoute Planner — Menú Principal ===")
    print("[1] Cargar red aérea desde JSON")
    print("[2] Ver aeropuertos (indica hubs con *)")
    print("[3] Ver rutas de un aeropuerto")
    print("[4] Planificación básica — R2")
    print("[5] Planificación avanzada — R3 (paso a paso)")
    print("[6] Simular interrupción de ruta — R4")
    print("[7] Ver rutas bloqueadas")
    print("[8] Recalcular ruta tras interrupción")
    print("[9] Generar reporte final — R5")
    print("[10] Ver grafo completo")
    print("[0] Salir")



def pedir_input(mensaje: str, tipo: type = str, opciones=None) -> Union[int, float, str]:
    max_intentos = 3
    intentos = 0
    
    while intentos < max_intentos:
        try:
            valor = input(mensaje).strip()
            if not valor:
                print("Por favor ingrese un valor.")
                intentos += 1
                continue
            
            if tipo is int:
                valor = int(valor)
            elif tipo is float:
                valor = float(valor)
            elif tipo is str:
                valor = str(valor)
            
            if opciones is not None and valor not in opciones:
                print(f"Opción inválida. Opciones válidas: {opciones}")
                intentos += 1
                continue
            
            return valor
        
        except ValueError as e:
            print(f"Entrada inválida: {e}. Intente nuevamente.")
            intentos += 1
        except TypeError as e:
            print(f"Entrada inválida: {e}. Intente nuevamente.")
            intentos += 1
        except EOFError:
            print("\nSesión terminada.")
            raise SystemExit(0)
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            raise SystemExit(0)
        except Exception as e:
            print(f"Error inesperado: {e}")
            intentos += 1
    
    print("Demasiados intentos fallidos. Cancelando operación.")
    return None




def visualizar_grafo(grafo):
    """Visualiza el grafo mostrando nodos y aristas."""
    print("\n=== Estructura del Grafo ===")
    print(f"Total de aeropuertos: {len(grafo.obtener_todos_nodos())}")
    print("\nNodos (Aeropuertos):")
    for nodo in grafo.obtener_todos_nodos():
        aeropuerto = nodo.aeropuerto
        hub = " (HUB)" if getattr(aeropuerto, 'es_centro', False) else ""
        print(f"  {getattr(aeropuerto, 'codigo_iata', '')}: {getattr(aeropuerto, 'nombre', '')}{hub}")
    
    print("\nAristas (Rutas) - Muestra origen → destino (distancia km):")
    aristas_mostradas = set()
    for nodo in grafo.obtener_todos_nodos():
        for arista in nodo.obtener_aristas():
            ruta = arista.ruta
            clave = (ruta.origen, ruta.destino)
            if clave not in aristas_mostradas:
                bloqueada = " [BLOQUEADA]" if arista.esta_bloqueada else ""
                print(f"  {clave[0]} → {clave[1]} ({getattr(ruta, 'distancia_km', 0)} km){bloqueada}")
                aristas_mostradas.add(clave)




def planificacion_avanzada_r3(grafo):
    """Implementa Planificación Avanzada R3 (Dijkstra paso a paso)."""
    
    print("\n" + "="*50)
    print("=== PLANIFICACIÓN AVANZADA (R3) - PASO A PASO ===")
    print("="*50)
    
    origen = pedir_input("\nAeropuerto de origen (IATA): ").upper()
    if not grafo.obtener_nodo(origen):
        print(f"❌ Error: '{origen}' no existe.")
        return
    
    destino = pedir_input("Aeropuerto de destino (IATA): ").upper()
    if not grafo.obtener_nodo(destino):
        print(f"❌ Error: '{destino}' no existe.")
        return
    
    tipos_entrada = pedir_input("Tipos de aeronave (coma separados, ej: comercial,regional): ")
    tipos_aeronave = [t.strip().capitalize() for t in tipos_entrada.split(",")]
    
    pausa = pedir_input("¿Pausar entre pasos? (s/n): ").lower() == 's'
    
    try:
        dijkstra = DijkstraStepByStep(grafo)
        resultado = dijkstra.execute(origen, destino, tipos_aeronave, mostrar_pasos=pausa)
        
        if resultado.get("error"):
            print(f"\n❌ {resultado['error']}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def planificacion_basica_r2(grafo, route_planner, bfs_service):
    """Implementa la funcionalidad completa de Planificación Básica (R2)."""
    
    print("\n" + "="*50)
    print("=== PLANIFICACIÓN BÁSICA (R2) ===")
    print("="*50)
    
    # 1. Solicitar parámetros básicos
    origen = pedir_input("\nAeropuerto de origen (código IATA): ").upper()
    
    # Verificar que el aeropuerto existe
    nodo_origen = grafo.obtener_nodo(origen)
    if not nodo_origen:
        print(f"❌ Error: aeropuerto '{origen}' no existe en la red.")
        return
    
    presupuesto = pedir_input("Presupuesto máximo (USD): ", float)
    tiempo_max = pedir_input("Tiempo máximo disponible (minutos): ", int)
    
    # Tipos de aeronave permitidos (para el BFS)
    tipos_entrada = pedir_input("Tipos de aeronave permitidos (coma separados, ej: comercial,regional): ")
    tipos_aeronave = [t.strip().capitalize() for t in tipos_entrada.split(",")]
    
    # IMPORTANTE: Llamar a route_planner.run() para obtener resultados del BFS
    # Esto ejecuta tanto Dijkstra como los algoritmos de máxima cobertura
    if not route_planner:
        print("❌ Error: el servicio de planificación no está disponible.")
        return
    
    print("\n⏳ Calculando itinerarios automáticos...")
    try:
        # Ejecutar route_planner con un destino dummy (no importa para máxima cobertura)
        # Usamos el mismo origen como destino temporal
        resultados = route_planner.run(
            origen=origen, 
            destino=origen,  # No importa para máxima cobertura
            presupuesto=presupuesto, 
            tiempo_max_min=tiempo_max, 
            criterios=["costo"],
            tipos_aeronave=tipos_aeronave, 
            excluir_secundarios=False
        )
    except Exception as e:
        print(f"⚠️ Error al calcular itinerarios: {e}")
        return
    
    print("\n" + "-"*50)
    print("ITINERARIO 1: Maximizar destinos por PRESUPUESTO")
    print("-"*50)
    
    # 2A. Mostrar resultados del BFS por presupuesto
    try:
        bfs_presupuesto = resultados.get("max_destinations_by_budget", {})
        
        if bfs_presupuesto.get("error"):
            print(f"⚠️ Aviso: {bfs_presupuesto['error']}")
        
        ruta = bfs_presupuesto.get("path", [origen])
        costo_total = bfs_presupuesto.get("total_cost", 0.0)
        destinos = bfs_presupuesto.get("destinations_count", len(ruta))
        segmentos = bfs_presupuesto.get("segments", [])
        
        print(f"Origen: {origen}")
        print(f"Presupuesto disponible: ${presupuesto:.2f}")
        print(f"Ruta: {' → '.join(ruta)}")
        print(f"Destinos visitados: {destinos}")
        print(f"Costo total: ${costo_total:.2f}")
        
        if segmentos:
            print(f"\n  Detalles de tramos:")
            for i, seg in enumerate(segmentos, 1):
                print(f"    {i}. {seg.get('origin')} → {seg.get('destination')}")
                print(f"       Aeronave: {seg.get('aircraft')} | "
                      f"Costo: ${seg.get('cost', 0):.2f} | "
                      f"Tiempo: {seg.get('time', 0):.0f} min")
    except Exception as e:
        print(f"⚠️ Error al mostrar itinerario por presupuesto: {e}")
    
    print("\n" + "-"*50)
    print("ITINERARIO 2: Maximizar destinos por TIEMPO")
    print("-"*50)
    
    # 2B. Mostrar resultados del BFS por tiempo
    try:
        bfs_tiempo = resultados.get("max_destinations_by_time", {})
        
        if bfs_tiempo.get("error"):
            print(f"⚠️ Aviso: {bfs_tiempo['error']}")
        
        ruta = bfs_tiempo.get("path", [origen])
        tiempo_total = bfs_tiempo.get("total_time_min", 0.0)
        destinos = bfs_tiempo.get("destinations_count", len(ruta))
        segmentos = bfs_tiempo.get("segments", [])
        
        print(f"Origen: {origen}")
        print(f"Tiempo disponible: {tiempo_max} minutos")
        print(f"Ruta: {' → '.join(ruta)}")
        print(f"Destinos visitados: {destinos}")
        print(f"Tiempo total: {tiempo_total:.0f} minutos")
        
        if segmentos:
            print(f"\n  Detalles de tramos:")
            for i, seg in enumerate(segmentos, 1):
                print(f"    {i}. {seg.get('origin')} → {seg.get('destination')}")
                print(f"       Aeronave: {seg.get('aircraft')} | "
                      f"Tiempo: {seg.get('time', 0):.0f} min | "
                      f"Distancia: {seg.get('distance_km', 0):.0f} km")
    except Exception as e:
        print(f"⚠️ Error al mostrar itinerario por tiempo: {e}")
    
    # 3. Segunda parte: Calcular mejor ruta según criterio
    print("\n" + "="*50)
    print("--- Cálculo de mejor ruta ---")
    print("="*50)
    
    destino = pedir_input("\nAeropuerto destino (código IATA): ").upper()
    
    # Verificar que el destino existe
    if not grafo.obtener_nodo(destino):
        print(f"❌ Error: aeropuerto '{destino}' no existe en la red.")
        return
    
    criterio = pedir_input("Criterio de optimización (costo/tiempo/distancia): ", str, 
                          opciones=["costo", "tiempo", "distancia"])
    
    tipos_entrada = pedir_input("Tipos de aeronave permitidos (coma separados, ej: comercial,regional): ")
    # Normalizar a mayúsculas para comparación
    tipos_aeronave = [t.strip().capitalize() for t in tipos_entrada.split(",")]
    
    # 4. Calcular mejor ruta con Dijkstra
    try:
        if not route_planner:
            print("❌ Error: el servicio de planificación no está disponible.")
            return
        
        resultados = route_planner.run(origen, destino, presupuesto, tiempo_max, [criterio], tipos_aeronave, False)
        
        print("\n" + "-"*50)
        print(f"MEJOR RUTA (Criterio: {criterio})")
        print("-"*50)
        
        ruta_resultado = resultados.get("by_criteria", {}).get(criterio, {})
        
        if ruta_resultado.get("error"):
            print(f"❌ {ruta_resultado['error']}")
        else:
            camino = ruta_resultado.get("path", [])
            if camino:
                print(f"\n✓ Ruta encontrada:")
                print(f"  {' → '.join(camino)}")
                print(f"\n  Número de escalas: {len(camino) - 2 if len(camino) > 1 else 0}")
                
                segmentos = ruta_resultado.get("segments", [])
                if segmentos:
                    print(f"\n  Tramos:")
                    costo_total = 0
                    tiempo_total = 0
                    distancia_total = 0
                    
                    for i, seg in enumerate(segmentos, 1):
                        costo = seg.get("cost", 0)
                        tiempo = seg.get("time", 0)
                        distancia = seg.get("distance_km", 0)
                        aeronave = seg.get("aircraft", "N/A")
                        
                        print(f"    {i}. {seg.get('origin')} → {seg.get('destination')}")
                        print(f"       Aeronave: {aeronave}")
                        print(f"       Costo: ${costo:.2f} | Tiempo: {tiempo:.0f} min | Distancia: {distancia:.0f} km")
                        
                        costo_total += costo
                        tiempo_total += tiempo
                        distancia_total += distancia
                    
                    print(f"\n  TOTALES:")
                    print(f"    Costo total: ${costo_total:.2f}")
                    print(f"    Tiempo total: {tiempo_total:.0f} minutos")
                    print(f"    Distancia total: {distancia_total:.0f} km")
                else:
                    print("  (Sin segmentos registrados)")
            else:
                print("❌ No se encontró una ruta que cumpla con las restricciones.")
    
    except Exception as e:
        print(f"❌ Error al calcular ruta: {e}")



def main():
    # Instanciar servicios (se inicializan con None, se asignan tras cargar red)
    grafo = None
    config = None
    route_planner = None
    itinerary_service = None
    budget_manager = None
    interruption_service = None
    report_service = None
    itinerario_actual = None
    rutas_bloqueadas = set()

    while True:
        mostrar_menu()
        opcion = pedir_input("Seleccione una opción: ", tipo = int, opciones=[0,1,2,3,4,5,6,7,8,9,10])

        try:
            if opcion == 1:
                ruta = pedir_input("Ruta del archivo JSON: ")
                try:
                    data = JSONLoader.load(ruta)
                    config_data = JSONLoader.get_global_config(data)
                    config = Config.from_json(config_data)
                    grafo = GraphBuilder.build(data)
                    route_planner = RoutePlannerService(grafo, config)
                    itinerary_service = ItineraryService(grafo, config)
                    budget_manager = BudgetManagerService(config, 0.0)
                    interruption_service = InterruptionService(grafo, config)
                    report_service = ReportService(grafo)
                    itinerario_actual = None
                    rutas_bloqueadas = set()
                    print("Red aérea cargada correctamente.")
                except Exception as e:
                    print(f"Error al cargar la red: {e}")

            elif opcion == 2:
                if not grafo:
                    print("Primero debe cargar la red aérea.")
                    continue
                print("\nAeropuertos disponibles:")
                for nodo in grafo.obtener_todos_nodos():
                    aeropuerto = nodo.aeropuerto
                    hub = "*" if getattr(aeropuerto, 'es_centro', False) else ""
                    print(f"{getattr(aeropuerto, 'codigo_iata', '')} - {getattr(aeropuerto, 'nombre', '')} {hub}")

            elif opcion == 3:
                if not grafo:
                    print("Primero debe cargar la red aérea.")
                    continue
                codigo = pedir_input("Código IATA del aeropuerto: ").upper()
                nodo = grafo.obtener_nodo(codigo)
                if not nodo:
                    print("No se encontró el aeropuerto.")
                    continue
                aristas = nodo.obtener_aristas()
                if not aristas:
                    print("No se encontraron rutas para ese aeropuerto.")
                else:
                    print(f"Rutas desde {codigo}:")
                    for arista in aristas:
                        ruta = arista.ruta
                        print(f"→ {ruta.destino} ({getattr(ruta, 'transporte', 'avion')}) — Costo: {getattr(ruta, 'costo_base', 0)}, Tiempo: {getattr(ruta, 'tiempo_min', 0)}")

            elif opcion == 4:
                if not route_planner:
                    print("Primero debe cargar la red aérea.")
                    continue
                planificacion_basica_r2(grafo, route_planner, None)

            elif opcion == 5:
                if not grafo:
                    print("Primero debe cargar la red aérea.")
                    continue
                planificacion_avanzada_r3(grafo)

            elif opcion == 6:
                if not interruption_service:
                    print("Primero debe cargar la red aérea.")
                    continue
                origen = pedir_input("Origen de la ruta a bloquear (IATA): ").upper()
                destino = pedir_input("Destino de la ruta a bloquear (IATA): ").upper()
                try:
                    grafo.bloquear_arista(origen, destino)
                    rutas_bloqueadas.add((origen, destino))
                    print(f"Ruta {origen} → {destino} bloqueada.")
                except Exception as e:
                    print(f"Error al bloquear ruta: {e}")

            elif opcion == 7:
                if not grafo:
                    print("Primero debe cargar la red aérea.")
                    continue
                
                # Buscar todas las rutas bloqueadas en el grafo
                rutas_bloqueadas_json = []
                for nodo in grafo.obtener_todos_nodos():
                    for arista in nodo.obtener_aristas():
                        if arista.esta_bloqueada:
                            rutas_bloqueadas_json.append((arista.ruta.origen, arista.ruta.destino))
                
                if not rutas_bloqueadas_json:
                    print("No hay rutas bloqueadas.")
                else:
                    print(f"\nRutas bloqueadas ({len(rutas_bloqueadas_json)}):")
                    for origen, destino in sorted(rutas_bloqueadas_json):
                        print(f"  {origen} → {destino}")

            elif opcion == 8:
                print("Funcionalidad de recálculo tras interrupción no implementada completamente en este ejemplo.")

            elif opcion == 9:
                print("Funcionalidad de generación de reporte final requiere integración con el itinerario y budget manager.")

            elif opcion == 10:
                if not grafo:
                    print("Primero debe cargar la red aérea.")
                    continue
                visualizar_grafo(grafo)

            elif opcion == 0:
                print("¡Hasta luego!")
                sys.exit(0)

        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
