
def quantVertices(grafo):
    return len(grafo.vertices)

def quantArestas(grafo):
    return len(grafo.arestas)

def Conexo(grafo):
    def dfs(v, visited):
        visited.add(v)
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple): # Se o grafo for ponderado, vizinho será uma tupla (v2, peso)
                vizinho = vizinho[0]
            if vizinho not in visited:
                dfs(vizinho, visited)

    visited = set()
    comecarVertice = next(iter(grafo.vertices))  # Começa a DFS a partir de um vértice qualquer
    dfs(comecarVertice, visited)
    
    if len(visited) == len(grafo.vertices):
        return "é"
    else:
        return "não é"

def Bipartido(grafo):
    def dfs(v, cor, current_color):
        cor[v] = current_color # Define a cor do vértice atual
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho = vizinho[0]
            if cor[vizinho] == -1:
                if not dfs(vizinho, cor, 1 - current_color): # Inverte a cor
                    return False
            elif cor[vizinho] == cor[v]:
                return False
        return True

    cor = {v: -1 for v in grafo.vertices}  # Inicializa todas as cores como -1 (não colorido)

    for vertice in grafo.vertices:
        if cor[vertice] == -1:  
            if not dfs(vertice, cor, 0 ):  # Inicia a DFS com a cor 0
                return "não é bipartido"

    return "é bipartido"

def Euleriano(grafo):
    if Conexo(grafo) == "não é":
        return "não é euleriano"
    else:
        graus = {v: 0 for v in grafo.vertices} # Inicializa o dicionário de graus de cada vértice
        for v in grafo.vertices:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                graus[v] += 1 # Incrementa o grau do vértice
        for v in graus:
            if graus[v] % 2 != 0:
                return "não é euleriano"
        return "é euleriano"

def Hamiltoniano(grafo):
    if Conexo(grafo) == "não é":
        return "não é hamiltoniano"
    else:
        if len(grafo.vertices) < 3:
            return "não é hamiltoniano"
        graus = {v: 0 for v in grafo.vertices} # Inicializa o dicionário de graus de cada vértice
        for v in grafo.vertices:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                graus[v] += 1 
            if graus[v] < len(grafo.vertices) // 2: # Se o grau de um vértice for menor que a metade do número de vértices, não é hamiltoniano (TEOREMA DE DIRAC)
                return "não é hamiltoniano"
            else:
                return "é hamiltoniano"
            
def Cíclico(grafo):
    
    if grafo.direcionado:
        visited = set()   # Marca o nó atual como visitado
        rec_stack = set() # Adiciona o nó atual à pilha de recursão
    
        def dfs(v):
            visited.add(v)
            rec_stack.add(v)
        
            for vizinho in grafo.adj_list[v]:
                if vizinho not in visited:
                    if dfs(vizinho):
                        return True
                elif vizinho in rec_stack:
                    return True
        
            rec_stack.remove(v)
            return False
    
        for vertice in grafo.vertices:
            if vertice not in visited:
                if dfs(vertice):
                    return "é cíclico"
        return "não é cíclico"
    
    else:
        visited = set()
    
        def dfs(v, parent):
            visited.add(v)
            for vizinho in grafo.adj_list[v]:
                if vizinho not in visited:
                    if dfs(vizinho, v):
                        return True
                elif parent != vizinho:
                    return True
            return False
    
    for vertice in grafo.vertices:
        if vertice not in visited:
            if dfs(vertice, None):
                return "é cíclico"
    return "não é cíclico"

import networkx as nx
def converter_para_networkx(grafo):
    G = nx.Graph()
    for v in grafo.adj_list:
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):
                G.add_edge(v, vizinho[0], weight=vizinho[1])  # Para grafos ponderados
            else:
                G.add_edge(v, vizinho)  # Para grafos não ponderados
    return G

def VerificaPlanar(grafo):
    # Verifica se o grafo é planar
    G = converter_para_networkx(grafo)
    planar = nx.check_planarity(G)
    return planar
    
def Planar(grafo):
    if VerificaPlanar(grafo):
        return "é planar"
    else:
        return "não é planar"


        




        
    