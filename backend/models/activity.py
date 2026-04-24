from dataclasses import dataclass

@dataclass
class Actividad:
    """
    Representa una actividad que se puede realizar en un aeropuerto.
    """
    nombre: str
    tipo: str  # "obligatoria" o "opcional"
    duracion_min: int
    costo_usd: float

    def __post_init__(self):
        if self.tipo not in ("obligatoria", "opcional"):
            raise ValueError('tipo debe ser "obligatoria" o "opcional".')
        if self.duracion_min < 0:
            raise ValueError("duracion_min debe ser no negativa.")
        if self.costo_usd < 0:
            raise ValueError("costo_usd debe ser no negativo.")
