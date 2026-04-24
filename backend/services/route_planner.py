from backend.interfaces.i_service import IService
from backend.interfaces.i_graph import IGraph
from backend.config import Config
from backend.algorithms.dijkstra import Dijkstra
from backend.algorithms.bfs import BFS
from backend.utils import validators

class RoutePlannerService(IService):
    """
    Servicio para planificación de rutas usando Dijkstra (R2) y BFS (máxima cobertura).
    Dijkstra resuelve R2 porque encuentra la ruta óptima según un criterio (costo, tiempo, distancia).
    BFS resuelve la cobertura máxima porque explora nivel a nivel y maximiza la cantidad de destinos visitados bajo restricciones.
    """
    def __init__(self, grafo: IGraph, config: Config):
        self.grafo = grafo
        self.config = config
        self.dijkstra = Dijkstra(grafo)
        self.bfs = BFS(grafo)

    def run(self, origen, destino, presupuesto, tiempo_max_min, criterios: list, tipos_aeronave: list, excluir_secundarios: bool):
        """
        Ejecuta los algoritmos de rutas según los criterios y restricciones dadas.
        :param origen: Código IATA de origen.
        :param destino: Código IATA de destino.
        :param presupuesto: Presupuesto máximo permitido.
        :param tiempo_max_min: Tiempo máximo permitido en minutos.
        :param criterios: Lista de criterios ("cost", "time", "distance").
        :param tipos_aeronave: Lista de tipos de aeronave.
        :param excluir_secundarios: Si es True, ignora nodos que no son hubs.
        :return: Diccionario con resultados por criterio y máxima cobertura.
        """
        resultados = {"by_criteria": {}}
        # Ejecutar Dijkstra para cada criterio (R2)
        for criterio in criterios:
            resultado = self.dijkstra.execute(origen, destino, criterio, tipos_aeronave, excluir_secundarios)
            # Validar restricciones
            if not resultado.get("error"):
                if not validators.within_budget(resultado.get("total_weight", 0), presupuesto):
                    resultado["error"] = "Excede el presupuesto"
                if not validators.within_time(resultado.get("total_weight", 0), tiempo_max_min) and criterio == "time":
                    resultado["error"] = "Excede el tiempo máximo"
            resultados["by_criteria"][criterio] = resultado
        # Ejecutar BFS para máxima cobertura por presupuesto
        bfs_budget = self.bfs.execute(origen, presupuesto, tiempo_max_min, tipos_aeronave, excluir_secundarios)
        if not validators.within_budget(bfs_budget.get("total_cost", 0), presupuesto):
            bfs_budget["error"] = "Excede el presupuesto"
        resultados["max_destinations_by_budget"] = bfs_budget
        # Ejecutar BFS para máxima cobertura por tiempo
        bfs_time = self.bfs.execute(origen, float('inf'), tiempo_max_min, tipos_aeronave, excluir_secundarios)
        if not validators.within_time(bfs_time.get("total_time_min", 0), tiempo_max_min):
            bfs_time["error"] = "Excede el tiempo máximo"
        resultados["max_destinations_by_time"] = bfs_time
        return resultados
