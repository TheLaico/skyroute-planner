"""
Script rápido para probar el fix de Dijkstra
"""
import sys
sys.path.insert(0, '.')

from backend.loaders.graph_builder import GraphBuilder
from backend.loaders.json_loader import JSONLoader
from backend.config import Config
from backend.algorithms.dijkstra import Dijkstra

# Cargar grafo
print("Cargando grafo...")
data = JSONLoader.load("data/airports_network.json")
config = Config()
builder = GraphBuilder()
grafo = builder.build(data)
print(f"OK - Grafo cargado: {len(grafo._nodos)} nodos, {sum(len(n.obtener_aristas()) for n in grafo._nodos.values())} aristas")

# Crear Dijkstra
dijkstra = Dijkstra(grafo)

# Test 1: BOG → EZE con criterio en ESPAÑOL (esto fallaría antes)
print("\n" + "="*70)
print("TEST 1: BOG -> EZE con criterio 'distancia' (ESPANOL)")
print("="*70)
resultado = dijkstra.execute("BOG", "EZE", "distancia", ["comercial"])
print(f"\nRuta encontrada: {resultado.get('path', [])}")
if resultado.get('path'):
    print(f"OK - Criterio en espanol ahora funciona")
else:
    print(f"ERROR: {resultado.get('error')}")

# Test 2: Mismo test con criterio en INGLÉS (para compatibilidad)
print("\n" + "="*70)
print("TEST 2: BOG -> EZE con criterio 'distance' (INGLES)")
print("="*70)
resultado = dijkstra.execute("BOG", "EZE", "distance", ["comercial"])
print(f"\nRuta encontrada: {resultado.get('path', [])}")
if resultado.get('path'):
    print(f"OK - Criterio en ingles tambien funciona")
else:
    print(f"ERROR: {resultado.get('error')}")

# Test 3: BOG → MDE (vecino directo)
print("\n" + "="*70)
print("TEST 3: BOG -> MDE (vecino directo) con criterio 'costo'")
print("="*70)
resultado = dijkstra.execute("BOG", "MDE", "costo", ["comercial"])
print(f"\nRuta encontrada: {resultado.get('path', [])}")
if resultado.get('path'):
    print(f"OK - Ruta directa encontrada")
else:
    print(f"ERROR: {resultado.get('error')}")

print("\n" + "="*70)
print("OK - PRUEBAS COMPLETADAS - Revisa los prints de debug arriba")
print("="*70)
