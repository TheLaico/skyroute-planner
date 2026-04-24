from abc import ABC, abstractmethod
from typing import Dict, Any, Set
from backend.interfaces.i_algorithm import IAlgorithm
from backend.interfaces.i_graph import IGraph
from backend.models.aircraft import Aeronave
from backend.core.edge import Arista

class AlgoritmoBase(IAlgorithm, ABC):
    """
    Clase abstracta base para algoritmos de rutas.
    """
    def __init__(self, grafo: IGraph):
        """
        Constructor que recibe el grafo sobre el cual se ejecutará el algoritmo.
        Requerimiento: El algoritmo debe operar sobre una estructura de grafo.
        """
        self.grafo = grafo

    @abstractmethod
    def execute(self, origen: str, **kwargs) -> Dict:
        """
        Método abstracto para ejecutar el algoritmo desde un nodo origen.
        Requerimiento: Permitir diferentes algoritmos de búsqueda de rutas.
        :param origen: Código IATA de aeropuerto origen.
        :param kwargs: Otros parámetros del algoritmo.
        :return: Diccionario con los resultados del algoritmo.
        """
        pass

    def _get_aircraft(self, tipo_aeronave: str) -> Aeronave:
        """
        Método protegido que retorna la Aeronave correspondiente al tipo solicitado.
        Requerimiento: Permitir seleccionar el tipo de aeronave para el cálculo de costos y tiempos.
        :param tipo_aeronave: Nombre del tipo de aeronave.
        :return: Instancia de Aeronave.
        """
        for aeronave in Aeronave.con_predeterminados():
            if aeronave.tipo_nombre == tipo_aeronave:
                return aeronave
        raise ValueError(f"Tipo de aeronave no válido: {tipo_aeronave}")

    def _visited_check(self, visitados: Set[str], nodo: str) -> bool:
        """
        Método protegido que verifica si un nodo ya fue visitado.
        Requerimiento: No repetir escalas en la ruta.
        :param visitados: Conjunto de nodos visitados.
        :param nodo: Código IATA del nodo a verificar.
        :return: True si ya fue visitado, False en caso contrario.
        """
        return nodo in visitados

    def _edge_cost(self, arista: Arista, tipo_aeronave: str) -> float:
        """
        Calcula el costo de una arista para un tipo de aeronave.
        Requerimiento: Calcular el costo total de la ruta.
        :param arista: Instancia de Arista.
        :param tipo_aeronave: Tipo de aeronave.
        :return: Costo como float.
        """
        aeronave = self._get_aircraft(tipo_aeronave)
        return arista.calcular_costo(aeronave)

    def _edge_time(self, arista: Arista, tipo_aeronave: str) -> float:
        """
        Calcula el tiempo de una arista para un tipo de aeronave.
        Requerimiento: Calcular el tiempo total de la ruta.
        :param arista: Instancia de Arista.
        :param tipo_aeronave: Tipo de aeronave.
        :return: Tiempo como float.
        """
        aeronave = self._get_aircraft(tipo_aeronave)
        return arista.calcular_tiempo(aeronave)
