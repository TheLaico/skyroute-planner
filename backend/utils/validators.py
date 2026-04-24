def within_budget(current_cost, budget):
    """
    Retorna True si el costo actual está dentro del presupuesto.
    """
    return current_cost <= budget

def within_time(current_time_min, max_time_min):
    """
    Retorna True si el tiempo actual está dentro del máximo permitido.
    """
    return current_time_min <= max_time_min

def not_visited(node_id, visited_set):
    """
    Retorna True si el nodo no ha sido visitado.
    """
    return node_id not in visited_set

def subsidized_limit_ok(subsidized_distance, total_distance, limit_pct=0.20):
    """
    Retorna True si la distancia subsidiada no supera el porcentaje límite.
    """
    return subsidized_distance <= total_distance * limit_pct

def budget_below_threshold(current_budget, initial_budget, threshold_pct=0.35):
    """
    Retorna True si el presupuesto actual está por debajo del umbral.
    """
    return current_budget <= initial_budget * threshold_pct
