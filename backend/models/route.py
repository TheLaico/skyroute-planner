from dataclasses import dataclass, field
from typing import List

@dataclass
class Ruta:
    """
    Representa una ruta entre dos aeropuertos.
    """
    origen: str
    destino: str
    distancia_km: float
    tipos_aeronave: List[str] = field(default_factory=list)
    costo_base: float = 0.0
    estadia_minima_minutos: int = 0
    esta_bloqueada: bool = False

    def __post_init__(self):
        if self.distancia_km < 0:
            raise ValueError("distancia_km debe ser no negativa.")
        if self.costo_base < 0:
            raise ValueError("costo_base debe ser no negativo.")
        if self.estadia_minima_minutos < 0:
            raise ValueError("estadia_minima_minutos debe ser no negativo.")
