from dataclasses import dataclass, field
from typing import List

@dataclass
class Aeropuerto:
    """
    Representa un aeropuerto con su información básica y costos.
    """
    codigo_iata: str
    nombre: str
    ciudad: str
    pais: str
    zona_horaria: str
    es_centro: bool
    costo_hospedaje: float
    costo_comida: float
    actividades: List[str] = field(default_factory=list)
    trabajos: List[str] = field(default_factory=list)
    aerolineas: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.codigo_iata or len(self.codigo_iata) != 3:
            raise ValueError("codigo_iata debe ser una cadena de 3 letras.")
        if self.costo_hospedaje < 0:
            raise ValueError("costo_hospedaje debe ser no negativo.")
        if self.costo_comida < 0:
            raise ValueError("costo_comida debe ser no negativo.")
