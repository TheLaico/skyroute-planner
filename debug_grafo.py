#!/usr/bin/env python3
"""
Script de depuración para validar la construcción del grafo y algoritmos.
Ejecutar: python debug_grafo.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from backend.loaders.json_loader import JSONLoader
from backend.loaders.graph_builder import GraphBuilder
from backend.algorithms.dijkstra import Dijkstra

def debug_grafo():
    print("=" * 70)
    print("DEBUG: Cargando datos del JSON...")
    print("=" * 70)
    
    try:
        data = JSONLoader.load("data/airports_network.json")
        print(f"✓ JSON cargado exitosamente")
        print(f"  - Aeropuertos: {len(data['airports'])}")
        print(f"  - Rutas: {len(data['routes'])}")
    except Exception as e:
        print(f"❌ Error al cargar JSON: {e}")
        return
    
    print("\n" + "=" * 70)
    print("DEBUG: Construyendo grafo...")
    print("=" * 70)
    
    try:
        grafo = GraphBuilder.build(data)
        print(f"✓ Grafo construido exitosamente")
    except Exception as e:
        print(f"❌ Error al construir grafo: {e}")
        return
    
    print("\n" + "=" * 70)
    print("DEBUG: Validando estructura del grafo...")
    print("=" * 70)
    
    # Verificar nodos
    nodos = grafo.obtener_todos_nodos()
    print(f"✓ Total de nodos: {len(nodos)}")
    
    # Verificar aristas
    aristas = grafo.obtener_todas_aristas()
    print(f"✓ Total de aristas: {len(aristas)}")
    
    # Verificar nodo específico
    print("\n" + "-" * 70)
    print("DEBUG: Verificando nodo BOG...")
    print("-" * 70)
    
    nodo_bog = grafo.obtener_nodo("BOG")
    if nodo_bog:
        print(f"✓ Nodo BOG existe")
        aristas_bog = nodo_bog.obtener_aristas()
        print(f"  - Vecinos (aristas salientes): {len(aristas_bog)}")
        for arista in aristas_bog[:5]:  # Mostrar primeras 5
            ruta = arista.ruta
            print(f"    BOG → {ruta.destino}: {ruta.distancia_km} km, "
                  f"tipos: {ruta.tipos_aeronave}, costo_base: ${ruta.costo_base}")
    else:
        print(f"❌ Nodo BOG NO existe en el grafo")
    
    # Verificar BOG → MDE específicamente
    print("\n" + "-" * 70)
    print("DEBUG: Verificando ruta BOG → MDE...")
    print("-" * 70)
    
    encontrada = False
    for arista in aristas_bog:
        if arista.nodo_destino == "MDE":
            encontrada = True
            ruta = arista.ruta
            print(f"✓ Ruta BOG → MDE EXISTE")
            print(f"  - Distancia: {ruta.distancia_km} km")
            print(f"  - Tipos de aeronave permitidos: {ruta.tipos_aeronave}")
            print(f"  - Costo base: ${ruta.costo_base}")
            break
    
    if not encontrada:
        print(f"❌ Ruta BOG → MDE NO EXISTE en el grafo")
    
    # Prueba de Dijkstra
    print("\n" + "=" * 70)
    print("DEBUG: Probando Dijkstra...")
    print("=" * 70)
    
    dijkstra = Dijkstra(grafo)
    print("\nPrueba 1: BOG → MDE con ['Comercial']")
    resultado1 = dijkstra.execute("BOG", "MDE", "distance", ["Comercial"], False)
    print(f"  Resultado: {resultado1}")
    
    print("\nPrueba 2: BOG → MDE con ['comercial'] (minúsculas)")
    resultado2 = dijkstra.execute("BOG", "MDE", "distance", ["comercial"], False)
    print(f"  Resultado: {resultado2}")
    
    print("\nPrueba 3: BOG → EZE (ruta más larga)")
    resultado3 = dijkstra.execute("BOG", "EZE", "distance", ["Comercial"], False)
    if resultado3.get("path"):
        print(f"  ✓ Ruta encontrada: {' → '.join(resultado3['path'])}")
        print(f"    Distancia total: {resultado3.get('total_weight', 0):.0f} km")
    else:
        print(f"  ❌ {resultado3.get('error', 'Error desconocido')}")
    
    print("\n" + "=" * 70)
    print("DEBUG: Verificando tipos de aeronave...")
    print("=" * 70)
    
    # Mostrar tipos disponibles
    from backend.models.aircraft import Aeronave
    aeronaves = Aeronave.con_predeterminados()
    print("Tipos de aeronave disponibles:")
    for aero in aeronaves:
        print(f"  - {aero.tipo_nombre}: ${aero.costo_por_km}/km, {aero.tiempo_por_km} min/km")
    
    print("\n" + "=" * 70)
    print("✓ DEBUG COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    debug_grafo()
