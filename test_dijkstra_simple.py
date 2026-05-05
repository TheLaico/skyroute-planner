"""Test simple de Dijkstra para debug"""
import sys
sys.path.insert(0, '.')

# Forzar recarga de módulos
import importlib
if 'backend' in sys.modules:
    del sys.modules['backend']
if 'backend.algorithms' in sys.modules:
    del sys.modules['backend.algorithms']
if 'backend.algorithms.dijkstra' in sys.modules:
    del sys.modules['backend.algorithms.dijkstra']
if 'backend.algorithms.base_algorithm' in sys.modules:
    del sys.modules['backend.algorithms.base_algorithm']

# Importar directamente
from backend.algorithms.dijkstra import Dijkstra
import backend.algorithms.dijkstra as dijkstra_module

print("1. Dijkstra importado")
print(f"   Archivo del módulo: {dijkstra_module.__file__}")

# Test sin cargar grafo, solo ver si entra a la función
class MockGrafo:
    def obtener_nodo(self, codigo):
        print(f"   [MOCK] obtener_nodo({codigo}) llamado")
        return None

mock_grafo = MockGrafo()
dijkstra = Dijkstra(mock_grafo)

print("2. Dijkstra instanciado")
print(f"   execute method: {dijkstra.execute}")
print("3. Llamando execute() con criterio 'distancia'...")

resultado = dijkstra.execute("BOG", "EZE", "distancia", ["comercial"])

print(f"4. Resultado: {resultado}")
