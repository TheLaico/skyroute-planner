from backend.interfaces.i_service import IService
from backend.interfaces.i_graph import IGraph
from backend.config import Config
from backend.models.itinerary import Itinerario
from backend.models.activity import Actividad
from backend.models.job import Trabajo
from backend.utils import cost_calculator, time_calculator

class ItineraryService(IService):
    """
    Servicio para construir y actualizar itinerarios de viaje.
    """
    def __init__(self, grafo: IGraph, config: Config):
        self.grafo = grafo
        self.config = config

    def run(self, path: list, tipo_aeronave: str) -> Itinerario:
        """
        Construye un itinerario a partir de un camino y tipo de aeronave.
        :param path: Lista de códigos IATA.
        :param tipo_aeronave: Tipo de aeronave a usar.
        :return: Instancia de Itinerario.
        """
        itinerary = Itinerario()
        tiempo_acumulado = 0.0
        for i in range(len(path) - 1):
            origen = path[i]
            destino = path[i + 1]
            nodo = self.grafo.obtener_nodo(origen)
            if not nodo:
                continue
            arista = next((a for a in nodo.obtener_aristas() if a.nodo_destino == destino), None)
            if not arista:
                continue
            aeronave = self._get_aircraft(tipo_aeronave)
            costo = cost_calculator.segment_cost(arista.ruta.distancia_km, aeronave)
            tiempo = time_calculator.flight_time_min(arista.ruta.distancia_km, aeronave)
            tiempo_acumulado += tiempo
            # Cobro de alojamiento
            if time_calculator.lodging_interval_exceeded(tiempo_acumulado, self.config.lodging_interval_hours):
                costo += cost_calculator.lodging_cost(nodo.aeropuerto)
                tiempo_acumulado = 0  # Reinicia el contador tras cobrar alojamiento
            # Cobro de alimentación
            if time_calculator.meal_interval_exceeded(tiempo_acumulado, self.config.meal_interval_hours):
                costo += cost_calculator.meal_cost(nodo.aeropuerto)
            segmento = f"{origen}-{destino}"
            itinerary.segmentos_volados.append(segmento)
            itinerary.costo_total += costo
            itinerary.tiempo_total_min += tiempo
            itinerary.aeropuertos_visitados.append(origen)
        if path:
            itinerary.aeropuertos_visitados.append(path[-1])
        return itinerary

    def add_activity(self, itinerary: Itinerario, airport_iata: str, activity_name: str) -> Itinerario:
        """
        Agrega una actividad al itinerario y suma su costo y tiempo.
        :param itinerary: Instancia de Itinerario.
        :param airport_iata: Código IATA del aeropuerto.
        :param activity_name: Nombre de la actividad.
        :return: Itinerario actualizado.
        """
        nodo = self.grafo.obtener_nodo(airport_iata)
        if not nodo:
            return itinerary
        actividad = next((a for a in getattr(nodo.aeropuerto, 'actividades', []) if getattr(a, 'nombre', None) == activity_name), None)
        if actividad:
            itinerary.actividades_realizadas.append(activity_name)
            itinerary.costo_total += getattr(actividad, 'costo_usd', 0)
            itinerary.tiempo_total_min += getattr(actividad, 'duracion_min', 0)
        return itinerary

    def get_available_activities(self, airport_iata: str) -> list:
        """
        Retorna la lista de actividades disponibles en un aeropuerto.
        :param airport_iata: Código IATA del aeropuerto.
        :return: Lista de instancias de Actividad.
        """
        nodo = self.grafo.obtener_nodo(airport_iata)
        if nodo:
            return getattr(nodo.aeropuerto, 'actividades', [])
        return []

    def get_available_jobs(self, airport_iata: str) -> list:
        """
        Retorna la lista de trabajos disponibles en un aeropuerto.
        :param airport_iata: Código IATA del aeropuerto.
        :return: Lista de instancias de Trabajo.
        """
        nodo = self.grafo.obtener_nodo(airport_iata)
        if nodo:
            return getattr(nodo.aeropuerto, 'trabajos', [])
        return []

    def _get_aircraft(self, tipo_aeronave: str):
        from backend.models.aircraft import Aeronave
        for aeronave in Aeronave.con_predeterminados():
            if aeronave.tipo_nombre == tipo_aeronave:
                return aeronave
        raise ValueError(f"Tipo de aeronave no válido: {tipo_aeronave}")
