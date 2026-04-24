def segment_cost(distance_km, aircraft):
    """
    Calcula el costo de un segmento de vuelo. Si aircraft tiene base_cost==0, retorna 0 (subsidiado).
    """
    if hasattr(aircraft, 'costo_base') and getattr(aircraft, 'costo_base', 0) == 0:
        return 0.0
    return distance_km * aircraft.costo_por_km

def lodging_cost(airport, nights=1):
    """
    Calcula el costo de hospedaje en un aeropuerto.
    """
    return nights * airport.costo_hospedaje

def meal_cost(airport, meals=1):
    """
    Calcula el costo de comidas en un aeropuerto.
    """
    return meals * airport.costo_comida

def job_income(job, hours):
    """
    Calcula el ingreso por trabajo, respetando el máximo de horas.
    """
    return min(hours, job.max_horas) * job.tarifa_hora
