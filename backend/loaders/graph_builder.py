from backend.core.grafo import Grafo
from backend.models.airport import Aeropuerto
from backend.models.route import Ruta
from backend.models.aircraft import Aeronave
from typing import Optional

class GraphBuilder:
    """
    Construye un objeto Grafo a partir de datos crudos y permite modificar la configuración de aeronaves.
    """
    @staticmethod
    def build(data: dict, aircraft_overrides: Optional[dict] = None) -> Grafo:
        """
        Construye el grafo a partir de los datos de aeropuertos y rutas.
        :param data: Diccionario con claves 'airports' y 'routes'.
        :param aircraft_overrides: Diccionario para sobrescribir valores de aeronaves.
        :return: Instancia de Grafo.
        """
        grafo = Grafo()
        # Configurar aeronaves si hay overrides
        if aircraft_overrides:
            GraphBuilder.update_aircraft_config(grafo, aircraft_overrides)
        # Crear nodos
        for a in data['airports']:
            # Mapear claves en inglés a español si es necesario
            airport_data = {
                'codigo_iata': a.get('codigo_iata') or a.get('iata_code'),
                'nombre': a.get('nombre') or a.get('name'),
                'ciudad': a.get('ciudad') or a.get('city'),
                'pais': a.get('pais') or a.get('country'),
                'zona_horaria': a.get('zona_horaria') or a.get('timezone'),
                'es_centro': a.get('es_centro') or a.get('is_hub', False),
                'costo_hospedaje': a.get('costo_hospedaje') or a.get('lodging_cost', 0),
                'costo_comida': a.get('costo_comida') or a.get('meal_cost', 0),
                'actividades': a.get('actividades') or a.get('activities', []),
                'trabajos': a.get('trabajos') or a.get('jobs', []),
                'aerolineas': a.get('aerolineas') or a.get('airlines', [])
            }
            aeropuerto = Aeropuerto(**airport_data)
            grafo.agregar_nodo(aeropuerto)
        # Crear aristas
        for r in data['routes']:
            # Mapear claves en inglés a español si es necesario
            route_data = {
                'origen': r.get('origen') or r.get('origin'),
                'destino': r.get('destino') or r.get('destination'),
                'distancia_km': r.get('distancia_km') or r.get('distance_km'),
                'tipos_aeronave': r.get('tipos_aeronave') or r.get('aircraft_types', []),
                'costo_base': r.get('costo_base') or r.get('base_cost', 0),
                'estadia_minima_minutos': r.get('estadia_minima_minutos') or r.get('min_stay_minutes', 0),
                'esta_bloqueada': r.get('esta_bloqueada') or r.get('is_blocked', False)
            }
            ruta = Ruta(**route_data)
            grafo.agregar_arista(ruta)
        return grafo

    @staticmethod
    def update_aircraft_config(grafo: Grafo, overrides: dict):
        """
        Permite modificar el costo y tiempo por km de los tipos de aeronave en caliente.
        :param grafo: Instancia de Grafo.
        :param overrides: Diccionario con nuevos valores para aeronaves.
        """
        for aeronave in Aeronave.con_predeterminados():
            if aeronave.tipo_nombre in overrides:
                config = overrides[aeronave.tipo_nombre]
                if 'costo_por_km' in config:
                    aeronave.costo_por_km = config['costo_por_km']
                if 'tiempo_por_km' in config:
                    aeronave.tiempo_por_km = config['tiempo_por_km']
