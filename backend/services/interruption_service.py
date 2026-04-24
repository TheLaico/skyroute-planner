from backend.interfaces.i_service import IService
from backend.interfaces.i_graph import IGraph
from backend.config import Config
from backend.algorithms.dijkstra import Dijkstra

class InterruptionService(IService):
    """
    Servicio para gestionar interrupciones de rutas y recálculo de trayectorias (R4).
    El flujo de interrupción consiste en bloquear una arista (ruta) en el grafo, lo que simula una interrupción (por clima, mantenimiento, etc). El recálculo busca una nueva ruta óptima desde la posición actual al destino final, respetando los recursos restantes. Si no hay ruta, se busca el hub más cercano como alternativa.
    """
    def __init__(self, grafo: IGraph, config: Config):
        self.grafo = grafo
        self.config = config

    def run(self, origen: str, destino: str) -> dict:
        """
        Bloquea la arista origen→destino en el grafo.
        :return: Confirmación de la operación.
        """
        self.grafo.bloquear_arista(origen, destino)
        return {"status": "bloqueada", "from": origen, "to": destino}

    def unblock(self, origen: str, destino: str) -> dict:
        """
        Desbloquea la arista origen→destino en el grafo.
        :return: Confirmación de la operación.
        """
        self.grafo.desbloquear_arista(origen, destino)
        return {"status": "desbloqueada", "from": origen, "to": destino}

    def recalculate(self, posicion_actual: str, destino_final: str, presupuesto_restante: float, tiempo_restante_min: float, tipos_aeronave: list) -> dict:
        """
        Recalcula la mejor ruta disponible tras una interrupción, usando Dijkstra y los recursos restantes.
        Si no hay camino, busca el hub más cercano como alternativa.
        :return: Diccionario con la nueva ruta o alternativa.
        """
        dijkstra = Dijkstra(self.grafo)
        resultado = dijkstra.execute(posicion_actual, destino_final, "cost", tipos_aeronave)
        if resultado.get("error") or resultado.get("total_weight", float('inf')) > presupuesto_restante or resultado.get("total_weight", float('inf')) > tiempo_restante_min:
            # Buscar el hub más cercano
            hubs = self.grafo.obtener_hubs()
            mejor_hub = None
            mejor_peso = float('inf')
            for hub in hubs:
                if hub.aeropuerto.codigo_iata == posicion_actual:
                    continue
                res = dijkstra.execute(posicion_actual, hub.aeropuerto.codigo_iata, "cost", tipos_aeronave)
                if not res.get("error") and res.get("total_weight", float('inf')) < mejor_peso:
                    mejor_peso = res["total_weight"]
                    mejor_hub = res
            if mejor_hub:
                return {"alternative_hub": mejor_hub}
            return {"error": "No hay rutas disponibles ni hubs alternativos"}
        return {"new_route": resultado}

    def get_blocked_edges(self) -> list:
        """
        Retorna todas las aristas actualmente bloqueadas en el grafo.
        :return: Lista de diccionarios con origen y destino de cada arista bloqueada.
        """
        bloqueadas = []
        for nodo in self.grafo.obtener_todos_nodos():
            for arista in nodo.obtener_aristas():
                if arista.esta_bloqueada:
                    bloqueadas.append({"from": arista.nodo_origen, "to": arista.nodo_destino})
        return bloqueadas
