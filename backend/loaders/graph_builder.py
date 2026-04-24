from backend.core.graph import Grafo
from backend.models.airport import Aeropuerto
from backend.models.route import Ruta
from backend.models.aircraft import Aeronave

class GraphBuilder:
    """
    Construye un objeto Grafo a partir de datos crudos y permite modificar la configuración de aeronaves.
    """
    @staticmethod
    def build(data: dict, aircraft_overrides: dict = None) -> Grafo:
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
            aeropuerto = Aeropuerto(**a)
            grafo.agregar_nodo(aeropuerto)
        # Crear aristas
        for r in data['routes']:
            ruta = Ruta(**r)
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
