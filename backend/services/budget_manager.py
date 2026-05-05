from backend.interfaces.i_service import IService
from backend.config import Config
from backend.models.job import Trabajo
from backend.utils import validators
from backend.algorithms.dfs import DFS
from typing import Optional


class BudgetManagerService(IService):
    """
    Servicio para gestionar el presupuesto, ingresos y egresos de la simulación.
    """
    def __init__(self, config: Config, initial_budget: float = 0.0):
        self.initial_budget = initial_budget
        self.current_budget = initial_budget
        self.total_spent = 0.0
        self.total_earned = 0.0
        self.config = config
        self._jobs_done = []
        self.threshold_pct = config.budget_threshold_pct

    def run(self, **kwargs) -> dict:
        """
        No aplica directamente. Usar los métodos específicos de gestión de presupuesto.
        :return: Estado actual del presupuesto.
        """
        return self.get_status()

    def spend(self, amount: float) -> dict:
        """
        Descuenta un monto del presupuesto. Lanza error si queda negativo.
        """
        if self.current_budget - amount < 0:
            raise ValueError("Presupuesto insuficiente.")
        self.current_budget -= amount
        self.total_spent += amount
        return self.get_status()

    def earn(self, job: Trabajo, hours: int) -> dict:
        """
        Suma ingreso por trabajo, validando el máximo de horas.
        """
        if hours > job.max_horas:
            raise ValueError("No se pueden trabajar más horas que el máximo permitido.")
        ingreso = job.tarifa_hora * hours
        self.current_budget += ingreso
        self.total_earned += ingreso
        self._jobs_done.append({"job": job.nombre, "hours": hours, "earned": ingreso})
        return self.get_status()

    def is_below_threshold(self) -> bool:
        """
        Retorna True si el presupuesto está por debajo del umbral.
        """
        return validators.budget_below_threshold(self.current_budget, self.initial_budget, self.threshold_pct)

    def get_status(self) -> dict:
        """
        Retorna el estado actual del presupuesto.
        """
        return {
            "current_budget": self.current_budget,
            "total_spent": self.total_spent,
            "total_earned": self.total_earned,
            "initial_budget": self.initial_budget,
            "threshold_pct": self.threshold_pct
        }

    def reset(self, new_budget: float):
        """
        Reinicia el presupuesto para una nueva simulación.
        """
        self.initial_budget = new_budget
        self.current_budget = new_budget
        self.total_spent = 0.0
        self.total_earned = 0.0
        self._jobs_done = []


class AdvancedPlannerService(IService):
    """
    Servicio avanzado de planificación que integra DFS y gestión de presupuesto.
    """
    def __init__(self, grafo, config: Config, budget_manager: BudgetManagerService):
        self.grafo = grafo
        self.config = config
        self.budget_manager = budget_manager
        self.dfs = DFS(grafo)

    def run(self, origen: str, initial_budget: float, tipos_aeronave: Optional[list] = None) -> dict:
        """
        Ejecuta DFS para encontrar la ruta de mayor cobertura con menor gasto y retorna el estado de presupuesto.
        """
        if tipos_aeronave is None:
            tipos_aeronave = []
        resultado = self.dfs.execute(origen, initial_budget, tipos_aeronave, optimizar="cost")
        status = self.budget_manager.get_status()
        return {"dfs_result": resultado, "budget_status": status}