import random

class Grafo:
    def __init__(self, es_dirigido=False, vertices_init=None):
        self._es_dirigido = es_dirigido
        self._vertices = {}
        if vertices_init:
            for vertice in vertices_init:
                self.agregar_vertice(vertice)

    def es_dirigido(self) -> bool:
        return self._es_dirigido

    def agregar_vertice(self, vertice: str):
        if vertice not in self._vertices:
            self._vertices[vertice] = {}

    def borrar_vertice(self, vertice: str):
        if vertice in self._vertices:
            del self._vertices[vertice]
            for v in self._vertices:
                if vertice in self._vertices[v]:
                    del self._vertices[v][vertice]

    def agregar_arista(self, v1: str, v2: str, peso: int = 1):
        if v1 in self._vertices and v2 in self._vertices:
            self._vertices[v1][v2] = peso
            if not self._es_dirigido:
                self._vertices[v2][v1] = peso

    def borrar_arista(self, v1: str, v2: str):
        if v1 in self._vertices and v2 in self._vertices[v1]:
            del self._vertices[v1][v2]
        if not self._es_dirigido and v2 in self._vertices and v1 in self._vertices[v2]:
            del self._vertices[v2][v1]

    def estan_unidos(self, v1: str, v2: str) -> bool:
        return v1 in self._vertices and v2 in self._vertices[v1]

    def peso_arista(self, v1: str, v2: str) -> int:
        if v1 in self._vertices and v2 in self._vertices[v1]:
            return self._vertices[v1][v2]
        else:
            raise ValueError(f"No existe una arista entre {v1} y {v2}")

    def obtener_vertices(self) -> list:
        return list(self._vertices.keys())

    def vertice_aleatorio(self) -> str:
        if self._vertices:
            return random.choice(list(self._vertices.keys()))

    def adyacentes(self, v: str) -> list:
        return list(self._vertices[v].keys()) if v in self._vertices else []

    def __str__(self):
        resultado = "Vertices:\n"
        for v in self.vertices:
            resultado += f"{v}: {self.vertices[v]}\n"
        return resultado