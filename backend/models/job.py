from dataclasses import dataclass

@dataclass
class Trabajo:
    """
    Representa un trabajo que se puede realizar en un aeropuerto.
    """
    nombre: str
    tarifa_hora: float
    max_horas: int

    def __post_init__(self):
        if self.tarifa_hora < 0:
            raise ValueError("tarifa_hora debe ser no negativa.")
        if self.max_horas < 0:
            raise ValueError("max_horas debe ser no negativo.")
