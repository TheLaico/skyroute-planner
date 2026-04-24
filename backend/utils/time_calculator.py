def flight_time_min(distance_km, aircraft):
    """
    Calcula el tiempo de vuelo en minutos para una distancia y aeronave.
    """
    return distance_km * aircraft.tiempo_por_km

def hours_to_minutes(hours):
    """
    Convierte horas a minutos.
    """
    return hours * 60

def minutes_to_hours(minutes):
    """
    Convierte minutos a horas.
    """
    return minutes / 60

def lodging_interval_exceeded(elapsed_min, interval_hours=20):
    """
    Verifica si se excedió el intervalo de hospedaje.
    """
    return elapsed_min >= interval_hours * 60

def meal_interval_exceeded(elapsed_min, interval_hours=8):
    """
    Verifica si se excedió el intervalo de comida.
    """
    return elapsed_min >= interval_hours * 60
