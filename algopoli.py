#!/usr/bin/python3

from grafo import Grafo
import sys
import biblioteca

delincuentes_mas_importantes = None

def init_mas_importantes(grafo):
    global delincuentes_mas_importantes
    if delincuentes_mas_importantes is None:
        delincuentes_mas_importantes = biblioteca.mas_importantes(grafo)

def min_seguimientos(grafo, comandos):
    if len(comandos) != 3:
        return
    min_camino = biblioteca.camino_minimo(grafo, comandos[1], comandos[2])
    print(" -> ".join(min_camino))

def mas_imp(grafo, comandos):
    if len(comandos) != 2:
        return  
    init_mas_importantes(grafo)
    k = int(comandos[1])
    biblioteca.imprimir_vertices(delincuentes_mas_importantes[:k])

def persecucion(grafo, comandos): 
    if len(comandos) != 3:
        return
    vertices = comandos[1].split(",")
    k = int(comandos[2])
    init_mas_importantes(grafo)
    mejor_camino = biblioteca.persecucion_rapida(grafo, vertices, k, delincuentes_mas_importantes)
    print(" -> ".join(mejor_camino))

def comunidades(grafo, comandos): 
    if len(comandos) != 2:
        return
    k = int(comandos[1])
    comunidades = biblioteca.comunidades(grafo)
    biblioteca.imprimir_comunidades(comunidades, k)

def divulgar(grafo, comandos): 
    if len(comandos) != 3:
        return
    k = int(comandos[2]) 
    rumor = biblioteca.div_rumor(grafo, comandos[1], k)
    biblioteca.imprimir_vertices(rumor)

def divulgar_ciclo(grafo, comandos):    
    if len(comandos) != 2:
        return
    ciclo = biblioteca.ciclo(grafo, comandos[1])
    if isinstance(ciclo, list):
        print(" -> ".join(ciclo))
    else:
        print(ciclo)

def cfc(grafo, comandos):
    if len(comandos) != 1:
        return
    cfc = biblioteca.componentes_fuertemente_conexas(grafo)
    biblioteca.imprimir_componentes(cfc)

ENTRADAS = {
    "min_seguimientos": min_seguimientos,
    "mas_imp": mas_imp,
    "persecucion": persecucion,
    "comunidades": comunidades,
    "divulgar": divulgar,
    "divulgar_ciclo": divulgar_ciclo,
    "cfc": cfc
}

def main():
    if len(sys.argv) != 2:
        print("Cantidad de parametros invalida")
        return
    grafo = biblioteca.grafo_init(sys.argv[1])
    if 764 in grafo.obtener_vertices():
        print('existe')
    for line in sys.stdin:
        if not line.strip():
            continue
        comandos = line.split() 
        accion = comandos[0]
        if accion in ENTRADAS:
            ENTRADAS[accion](grafo, comandos)

if __name__ == "__main__":
    main()