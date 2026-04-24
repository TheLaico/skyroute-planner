from typing import List
from backend.models.airport import Aeropuerto
# Evitar import circular para Arista

class Nodo:
    """
    Clase Nodo que envuelve un objeto Aeropuerto y gestiona su lista de adyacencia.
    """
    def __init__(self, aeropuerto: 'Aeropuerto'):
        self.aeropuerto = aeropuerto
        self.lista_adyacencia: List['Arista'] = []

    def agregar_arista(self, arista: 'Arista'):
        """
        Agrega una arista a la lista de adyacencia.
        :param arista: Arista a agregar.
        """
        self.lista_adyacencia.append(arista)

    def obtener_aristas(self) -> List['Arista']:
        """
        Obtiene todas las aristas de la lista de adyacencia.
        :return: Lista de aristas.
        """
        return self.lista_adyacencia

    def __repr__(self):
        return f"Nodo({self.aeropuerto.codigo_iata})"
