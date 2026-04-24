class Config:
    """
    Clase de configuración para la aplicación SkyRoute Planner.
    Permite instanciar y modificar los valores de configuración.
    """
    AIRCRAFT_DEFAULTS = {
        "Comercial": {"cost_per_km": 0.18, "time_per_km": 0.7},
        "Regional": {"cost_per_km": 0.25, "time_per_km": 1.1},
        "Hélice": {"cost_per_km": 0.12, "time_per_km": 2.5}
    }
    BUDGET_THRESHOLD_PCT: float = 0.35
    LODGING_INTERVAL_HOURS: int = 20
    MEAL_INTERVAL_HOURS: int = 8
    SUBSIDIZED_ROUTE_MAX_PCT: float = 0.20

    def __init__(self):
        self.aircraft_defaults = dict(Config.AIRCRAFT_DEFAULTS)
        self.budget_threshold_pct = Config.BUDGET_THRESHOLD_PCT
        self.lodging_interval_hours = Config.LODGING_INTERVAL_HOURS
        self.meal_interval_hours = Config.MEAL_INTERVAL_HOURS
        self.subsidized_route_max_pct = Config.SUBSIDIZED_ROUTE_MAX_PCT

    @classmethod
    def from_json(cls, data: dict) -> 'Config':
        """
        Crea una instancia de Config sobrescribiendo los valores por defecto con los del JSON si existen.
        :param data: Diccionario con posibles claves de configuración.
        :return: Instancia de Config.
        """
        config = cls()
        if 'aircraft_defaults' in data:
            config.aircraft_defaults = data['aircraft_defaults']
        if 'budget_threshold_pct' in data:
            config.budget_threshold_pct = data['budget_threshold_pct']
        if 'lodging_interval_hours' in data:
            config.lodging_interval_hours = data['lodging_interval_hours']
        if 'meal_interval_hours' in data:
            config.meal_interval_hours = data['meal_interval_hours']
        if 'subsidized_route_max_pct' in data:
            config.subsidized_route_max_pct = data['subsidized_route_max_pct']
        return config

    def to_dict(self) -> dict:
        """
        Serializa la configuración actual a un diccionario.
        :return: Diccionario con los valores actuales de configuración.
        """
        return {
            "aircraft_defaults": self.aircraft_defaults,
            "budget_threshold_pct": self.budget_threshold_pct,
            "lodging_interval_hours": self.lodging_interval_hours,
            "meal_interval_hours": self.meal_interval_hours,
            "subsidized_route_max_pct": self.subsidized_route_max_pct
        }
