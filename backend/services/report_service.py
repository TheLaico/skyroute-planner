import json
from backend.interfaces.i_service import IService
from backend.interfaces.i_graph import IGraph
from backend.models.itinerary import Itinerario
from backend.services.budget_manager import BudgetManagerService

class ReportService(IService):
    """
    Servicio para generar y exportar reportes finales de la simulación.
    """
    def __init__(self, grafo: IGraph):
        self.grafo = grafo

    def run(self, itinerary: Itinerario, budget_manager: BudgetManagerService) -> dict:
        """
        Construye el reporte final con información detallada del itinerario y presupuesto.
        """
        report = {
            "visited_airports": [],
            "flown_segments": [],
            "activities_done": [],
            "jobs_done": [],
            "totals": {}
        }
        # Aeropuertos visitados
        for iata in itinerary.aeropuertos_visitados:
            nodo = self.grafo.obtener_nodo(iata)
            if nodo:
                report["visited_airports"].append({
                    "iata": iata,
                    "nombre": getattr(nodo.aeropuerto, "nombre", ""),
                    "ciudad": getattr(nodo.aeropuerto, "ciudad", ""),
                    "pais": getattr(nodo.aeropuerto, "pais", ""),
                    "tiempo_estadia": itinerary.tiempo_total_min,  # simplificado
                    "costo_total": itinerary.costo_total  # simplificado
                })
        # Segmentos volados
        for seg in itinerary.segmentos_volados:
            # Se asume formato "ORIGEN-DESTINO"
            origen, destino = seg.split("-")
            report["flown_segments"].append({
                "origen": origen,
                "destino": destino
                # Se pueden agregar más detalles si se almacenan en el itinerario
            })
        # Actividades realizadas
        for act in itinerary.actividades_realizadas:
            report["activities_done"].append({
                "nombre": act
                # Se pueden agregar más detalles si se almacenan en el itinerario
            })
        # Trabajos realizados
        for job in getattr(itinerary, "trabajos_realizados", []):
            report["jobs_done"].append({
                "nombre": job
                # Se pueden agregar más detalles si se almacenan en el itinerario
            })
        # Totales
        status = budget_manager.get_status()
        report["totals"] = {
            "presupuesto_inicial": status["initial_budget"],
            "total_gastado": status["total_spent"],
            "total_ganado": status["total_earned"],
            "saldo_final": status["current_budget"],
            "tiempo_total_min": itinerary.tiempo_total_min
        }
        return report

    def print_report(self, report: dict):
        """
        Imprime el reporte formateado en consola como tabla ASCII.
        """
        print("--- REPORTE FINAL ---")
        print("Aeropuertos visitados:")
        print("IATA | Nombre | Ciudad | País | Tiempo | Costo")
        print("---" * 10)
        for a in report["visited_airports"]:
            print(f"{a['iata']} | {a['nombre']} | {a['ciudad']} | {a['pais']} | {a['tiempo_estadia']} | {a['costo_total']}")
        print("\nSegmentos volados:")
        print("Origen | Destino")
        print("---" * 5)
        for s in report["flown_segments"]:
            print(f"{s['origen']} | {s['destino']}")
        print("\nActividades realizadas:")
        for act in report["activities_done"]:
            print(f"- {act['nombre']}")
        print("\nTrabajos realizados:")
        for job in report["jobs_done"]:
            print(f"- {job['nombre']}")
        print("\nTotales:")
        for k, v in report["totals"].items():
            print(f"{k}: {v}")

    def export_to_json(self, report: dict, filepath: str):
        """
        Exporta el reporte a un archivo JSON.
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
