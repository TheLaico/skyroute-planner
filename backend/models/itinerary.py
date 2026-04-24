from dataclasses import dataclass, field
from typing import List

@dataclass
class Itinerario:
    """
    Representa un itinerario de viaje, acumulando aeropuertos visitados, segmentos, actividades, trabajos y totales.
    """
    aeropuertos_visitados: List[str] = field(default_factory=list)
    segmentos_volados: List[str] = field(default_factory=list)
    actividades_realizadas: List[str] = field(default_factory=list)
    trabajos_realizados: List[str] = field(default_factory=list)
    costo_total: float = 0.0
    tiempo_total_min: int = 0
    total_ganado: float = 0.0

    def __post_init__(self):
        if self.costo_total < 0:
            raise ValueError("costo_total debe ser no negativo.")
        if self.tiempo_total_min < 0:
            raise ValueError("tiempo_total_min debe ser no negativo.")
        if self.total_ganado < 0:
            raise ValueError("total_ganado debe ser no negativo.")
