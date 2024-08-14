def dfs(grafo, v, tempo):
    vertice = grafo.vertices[v]
    vertice.cor = 'cinza'
    tempo += 1
    vertice.tempo_descoberta = tempo

    for vizinho in grafo.adj_list[v]:
        if isinstance(vizinho, tuple):
            vizinho = vizinho[0]
        vizinho_obj = grafo.vertices[vizinho]
        if vizinho_obj.cor == 'branco':
            vizinho_obj.pai = v
            tempo = dfs(grafo, vizinho, tempo)

    vertice.cor = 'preto'
    tempo += 1
    vertice.tempo_finalizacao = tempo

    return tempo


def Conexo(grafo):
    # Inicializa o tempo
    tempo = 0

    # Inicializa as propriedades dos vértices
    for vertice in grafo.vertices:
        grafo.vertices[vertice].cor = 'branco'
        grafo.vertices[vertice].pai = None
        grafo.vertices[vertice].tempo_descoberta = None
        grafo.vertices[vertice].tempo_finalizacao = None

    # Escolhe um vértice arbitrário para começar a DFS
    vertice_inicial = next(iter(grafo.vertices.keys()))

    # Realiza a DFS a partir do vértice inicial
    tempo = dfs(grafo, vertice_inicial, tempo)

    # Verifica se todos os vértices foram alcançados
    if all(grafo.vertices[vertice].cor == 'preto' for vertice in grafo.vertices):
        return True
    else:
        return False


def Bipartido(grafo):
    def verificar_bipartido(grafo, v, visitado, cor, current_color):
        cor[v] = current_color
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho = vizinho[0]
            if cor[vizinho] == -1:
                if not verificar_bipartido(grafo, vizinho, visitado, cor, 1 - current_color):
                    return False
            elif cor[vizinho] == cor[v]:
                return False
        return True

    cor = {v: -1 for v in grafo.vertices}

    for vertice in grafo.vertices:
        if cor[vertice] == -1:
            if not verificar_bipartido(grafo, vertice, set(), cor, 0):
                return "0"

    return "1"


def Euleriano(grafo):
    if not Conexo(grafo):
        return "não é euleriano"
    
    if grafo.direcionado:
        # Verifique se o grafo direcionado é euleriano
        grau_entrada = {v: 0 for v in grafo.vertices}
        grau_saida = {v: 0 for v in grafo.vertices}
        
        for v in grafo.vertices:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                grau_saida[v] += 1
                grau_entrada[vizinho] += 1
        
        # Verifique se os graus de entrada e saída são iguais para todos os vértices
        for v in grafo.vertices:
            if grau_entrada[v] != grau_saida[v]:
                return "0"
            
        return "1"

    else:
        # Verifique se o grafo não direcionado é euleriano
        grau = {v: 0 for v in grafo.vertices}
        
        for v in grafo.vertices:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                grau[v] += 1
        
        # Verifique se o grau de todos os vértices é par
        for v in grafo.vertices:
            if grau[v] % 2 != 0:
                return "0"
            
        return "1"


def Cíclico(grafo):
    def verificar_ciclo(grafo, v, visitado, pai):
        visitado.add(v)
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho = vizinho[0]
            if vizinho not in visitado:
                if verificar_ciclo(grafo, vizinho, visitado, v):
                    return True
            elif vizinho != pai:
                return True
        return False

    visitado = set()
    
    for vertice in grafo.vertices:
        if vertice not in visitado:
            if verificar_ciclo(grafo, vertice, visitado, None):
                return "1"
    return "0"