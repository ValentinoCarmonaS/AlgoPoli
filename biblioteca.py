from grafo import Grafo
import random
from collections import deque, defaultdict

FACTOR_AMORTIGUACION_PAGERANK = 0.85
FACTOR_DE_ITERACIONES_PAGERANK = 30

def grafo_init(archivo):
    grafo = Grafo(es_dirigido=True)
    with open(archivo, "r") as ar:
        for linea in ar:
            v1, v2 = linea.strip().split('\t')
            grafo.agregar_vertice(v1)
            grafo.agregar_vertice(v2)
            grafo.agregar_arista(v1, v2)
    return grafo

def imprimir_vertices(vertices):
    print(", ".join(vertices))

def imprimir_componentes(componentes):
    for idx, elem in enumerate(componentes, start=1):
        print(f"CFC {idx}: ", end="")
        imprimir_vertices(elem)

def imprimir_comunidades(comunidades, n):
    for idx, (k, vertices) in enumerate(comunidades.items(), start=1):
        if len(vertices) >= n:
            print(f"Comunidad {idx}:", end=" ")
            imprimir_vertices(vertices)

def camino_minimo(grafo, origen, destino): 
    if origen == destino:
        return [origen]
    vertices = grafo.obtener_vertices()
    if origen not in vertices or destino not in vertices:
        return ["Seguimiento imposible"]

    visitados = set([origen])
    padre = {origen: None}
    cola = deque([origen])

    while cola:
        actual = cola.popleft()
        for vecino in grafo.adyacentes(actual):
            if vecino not in visitados:
                visitados.add(vecino)
                padre[vecino] = actual
                cola.append(vecino)
                if vecino == destino:
                    camino = []
                    while vecino is not None:
                        camino.append(vecino)
                        vecino = padre[vecino]
                    return camino[::-1]

    return ["Seguimiento imposible"]


def pagerank(grafo):
    vertices = grafo.obtener_vertices()
    n = len(vertices)
    rank = {}
    gds = {}
    nuevo = {}
    for v in vertices:
        rank[v] = 1 / n
        gds[v] = len(grafo.adyacentes(v))
        nuevo[v] = (1 - FACTOR_AMORTIGUACION_PAGERANK) / n
    for _ in range(FACTOR_DE_ITERACIONES_PAGERANK):
        for v in vertices:
            if gds[v] == 0:
                puntuacion = rank[v] / n
            else:
                puntuacion = rank[v] / gds[v]
            for w in grafo.adyacentes(v):
                nuevo[w] += puntuacion
        rank = nuevo
    return rank


def mas_importantes(grafo):
    page_ranks = pagerank(grafo)
    vertices_ordenados = sorted(page_ranks, key=page_ranks.get, reverse=True)
    return vertices_ordenados

def persecucion_rapida(grafo, vertices, k, importantes):
    k_importantes = importantes[:k]
    return mejor_camino(grafo, vertices, k_importantes)

def mejor_camino(grafo, vertices, k_importantes):
    resultado = None
    for v in vertices:
        for elem in k_importantes:
            cam_min = camino_minimo(grafo, v, elem)
            if cam_min == ["Seguimiento imposible"]:
                continue
            if resultado is None or len(cam_min) < len(resultado):
                resultado = cam_min           
            if len(cam_min) == len(resultado) and k_importantes.index(cam_min[-1]) < k_importantes.index(resultado[-1]):
                resultado = cam_min
    return resultado

def comunidades(grafo):
    etiqueta = {v: v for v in grafo.obtener_vertices()}
    vertices = grafo.obtener_vertices()
    random.shuffle(vertices)
    actualizado = True

    while actualizado:
        actualizado = False
        for v in vertices:
            adyacentes = grafo.adyacentes(v)
            if adyacentes:
                etiqueta_frecuencia = defaultdict(int)
                for w in adyacentes:
                    etiqueta_frecuencia[etiqueta[w]] += 1
                etiqueta_mas_comun = max(etiqueta_frecuencia, key=etiqueta_frecuencia.get)
                if etiqueta[v] != etiqueta_mas_comun:
                    etiqueta[v] = etiqueta_mas_comun
                    actualizado = True

    comunidades = defaultdict(list)
    for vertice, etiq in etiqueta.items():
        comunidades[etiq].append(vertice)
    
    return comunidades

def div_rumor(grafo, origen, limite):
    resultado = []
    visitados = set()
    distancia = {origen: 0}
    q = deque([origen])
    visitados.add(origen)

    while q:
        v = q.popleft()
        if distancia[v] == limite:
            break
        for w in grafo.adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                distancia[w] = distancia[v] + 1
                q.append(w)
                resultado.append(w)
    return resultado


def ciclo(grafo, vertice):
    q = deque([vertice])
    padres = {vertice: None}
    visitados = set([vertice])

    while q:
        v = q.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                padres[w] = v
                visitados.add(w)
                q.append(w)
            elif w == vertice:
                ciclo = [w]
                while v != w:
                    ciclo.append(v)
                    v = padres[v]
                ciclo.append(w)
                return ciclo[::-1]

    return "No se encontro recorrido"

def componentes_fuertemente_conexas(grafo):
    resultados = []
    visitados = set()
    for v in grafo.obtener_vertices():
        if v not in visitados:
            _componentes_fuertemente_conexas(grafo, v, visitados, {}, {}, deque(), set(), resultados, [0])
    return resultados

def _componentes_fuertemente_conexas(grafo, v, visitados, orden, mas_bajo, pila, apilados, cfcs, contador_global):
    orden[v] = contador_global[0]
    mas_bajo[v] = contador_global[0]
    contador_global[0] += 1
    visitados.add(v)
    pila.append(v)
    apilados.add(v)
    for w in grafo.adyacentes(v):
        if w not in visitados:
            _componentes_fuertemente_conexas(grafo, w, visitados, orden, mas_bajo, pila, apilados, cfcs, contador_global)
        if w in apilados:
            mas_bajo[v] = min(mas_bajo[v], mas_bajo[w])
    if orden[v] == mas_bajo[v]:
        nueva_cfc = []
        while True:
            w = pila.pop()
            apilados.remove(w)
            nueva_cfc.append(w)
            if w == v:
                break
        cfcs.append(nueva_cfc)
