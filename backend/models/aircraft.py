from dataclasses import dataclass
from typing import List

@dataclass
class Aeronave:
    """
    Representa un tipo de aeronave con costo y tiempo por kilómetro.
    """
    tipo_nombre: str
    costo_por_km: float
    tiempo_por_km: float

    @classmethod
    def con_predeterminados(cls) -> List['Aeronave']:
        """
        Devuelve una lista de tipos de aeronave predeterminados.
        :return: Lista de instancias de Aeronave con valores predeterminados.
        """
        return [
            cls("Comercial", 0.18, 0.7),
            cls("Regional", 0.25, 1.1),
            cls("Hélice", 0.12, 2.5)
        ]

    def __post_init__(self):
        if self.costo_por_km < 0:
            raise ValueError("costo_por_km debe ser no negativo.")
        if self.tiempo_por_km <= 0:
            raise ValueError("tiempo_por_km debe ser positivo.")
