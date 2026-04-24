from backend.models.route import Ruta
from backend.models.aircraft import Aeronave

class Arista:
    """
    Clase Arista que envuelve un objeto Ruta y almacena los identificadores de nodo origen y destino.
    """
    def __init__(self, ruta: 'Ruta', nodo_origen: str, nodo_destino: str):
        self.ruta = ruta
        self.nodo_origen = nodo_origen
        self.nodo_destino = nodo_destino

    def calcular_costo(self, aeronave: 'Aeronave') -> float:
        """
        Calcula el costo de recorrer esta arista con una aeronave dada.
        :param aeronave: Aeronave a usar para el cálculo.
        :return: Costo total como float.
        """
        if self.ruta.costo_base == 0:
            return 0.0
        return self.ruta.distancia_km * aeronave.costo_por_km

    def calcular_tiempo(self, aeronave: 'Aeronave') -> float:
        """
        Calcula el tiempo para recorrer esta arista con una aeronave dada.
        :param aeronave: Aeronave a usar para el cálculo.
        :return: Tiempo total como float.
        """
        return self.ruta.distancia_km * aeronave.tiempo_por_km

    @property
    def esta_bloqueada(self) -> bool:
        """
        Indica si la ruta está bloqueada.
        :return: True si está bloqueada, False en caso contrario.
        """
        return self.ruta.esta_bloqueada
