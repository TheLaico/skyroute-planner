"""
Punto de entrada principal para la consola de SkyRoute Planner.
Menú interactivo para cargar red, ver aeropuertos, planificar rutas, simular interrupciones y generar reportes.
Todo el código y mensajes están en español.
"""
import sys
import json
from backend.loaders.json_loader import JSONLoader
from backend.loaders.graph_builder import GraphBuilder
from backend.core.graph import Grafo
from backend.services.route_planner import RoutePlannerService
from backend.services.itinerary_service import ItineraryService
from backend.services.budget_manager import BudgetManagerService
from backend.services.interruption_service import InterruptionService
from backend.services.report_service import ReportService
from backend.config import Config


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
    print("[0] Salir")

def pedir_input(mensaje, tipo=str, opciones=None):
    while True:
        try:
            valor = input(mensaje)
            if tipo is int:
                valor = int(valor)
            elif tipo is float:
                valor = float(valor)
            elif tipo is str:
                valor = str(valor)
            if opciones is not None and valor not in opciones:
                print(f"Opción inválida. Opciones válidas: {opciones}")
                continue
            return valor
        except Exception as e:
            print(f"Entrada inválida: {e}")

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
        opcion = pedir_input("Seleccione una opción: ", tipo=int, opciones=[0,1,2,3,4,5,6,7,8,9])

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
                    budget_manager = BudgetManagerService(config)
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
                origen = pedir_input("Aeropuerto origen (IATA): ").upper()
                destino = pedir_input("Aeropuerto destino (IATA): ").upper()
                presupuesto = pedir_input("Presupuesto máximo (USD): ", float)
                tiempo = pedir_input("Tiempo máximo (min): ", int)
                criterios = pedir_input("Criterios (costo/tiempo/distancia): ", str, opciones=["costo","tiempo","distancia"])
                tipos = pedir_input("Tipos de aeronave (coma separados, ej: Comercial,Regional): ").split(",")
                try:
                    resultados = route_planner.run(origen, destino, presupuesto, tiempo, [criterios], tipos, False)
                    print("\nResultados de planificación:")
                    for crit, res in resultados.get("by_criteria", {}).items():
                        print(f"Criterio: {crit}")
                        print(res)
                    itinerario_actual = None  # Aquí deberías construir el itinerario si lo deseas
                except Exception as e:
                    print(f"Error en planificación: {e}")

            elif opcion == 5:
                print("Funcionalidad avanzada paso a paso no implementada completamente en este ejemplo. (Requiere lógica adicional para interacción de usuario y actualización de itinerario)")

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
                if not rutas_bloqueadas:
                    print("No hay rutas bloqueadas.")
                else:
                    print("Rutas bloqueadas:")
                    for o, d in rutas_bloqueadas:
                        print(f"{o} → {d}")

            elif opcion == 8:
                print("Funcionalidad de recálculo tras interrupción no implementada completamente en este ejemplo.")

            elif opcion == 9:
                print("Funcionalidad de generación de reporte final requiere integración con el itinerario y budget manager.")

            elif opcion == 0:
                print("¡Hasta luego!")
                sys.exit(0)

        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
