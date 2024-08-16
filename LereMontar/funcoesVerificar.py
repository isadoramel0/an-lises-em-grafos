def DFS(grafo, v, tempo, adj_list):
    vertice = grafo.vertices[v]
    vertice.cor = 'cinza' # Vértice em processo de exploração
    tempo += 1
    vertice.tempoDescoberta = tempo

    for vizinho in adj_list[v]:
        if isinstance(vizinho, tuple):
            vizinho_id = vizinho[1]  # Acessa o vértice destino na tupla (idAresta, vizinho, peso)
        else:
            vizinho_id = vizinho

        vizinhoObj = grafo.vertices[vizinho_id]
        if vizinhoObj.cor == 'branco':   # Se o vértice não foi visitado
            vizinhoObj.pai = v # Define o pai do vértice
            tempo = DFS(grafo, vizinho_id, tempo, adj_list) 

    vertice.cor = 'preto' # Vértice finalizado
    tempo += 1
    vertice.tempoFinalizacao = tempo # Define o tempo de finalização

    return tempo


# ------- Conexo
def Conexo(grafo):
    # Se o grafo é direcionado, criamos uma lista de adjacência temporária com arestas bidirecionais
    if grafo.direcionado:
        adj_listTemp = {v: [] for v in grafo.vertices}
        for v in grafo.adj_list:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    adj_listTemp[v].append(vizinho) # Adiciona a aresta original
                    adj_listTemp[vizinho[1]].append((v, vizinho[1])) # Adiciona a aresta inversa
                else:
                    adj_listTemp[v].append(vizinho)
                    adj_listTemp[vizinho].append(v)
    else:
        adj_listTemp = grafo.adj_list

    # Escolhe o primeiro vértice da lista de vértices para começar a DFS
    verticeInicial = list(grafo.vertices.keys())[0]

    # Realiza a DFS a partir do vértice inicial usando a lista de adjacência apropriada
    tempo = 0
    DFS(grafo, verticeInicial, tempo, adj_listTemp)

    # Verifica se todos os vértices foram alcançados
    if (all(grafo.vertices[vertice].cor == 'preto' for vertice in grafo.vertices)):
        return 1
    else:
        return 0


# ------- Bipartido
def Bipartido(grafo):

    # A lógica é a mesma da DFS, mas a personalização é feita para colorir os vértices adjacentes com cores diferentes para identificar se o grafo é bipartido
    def verificarBipartido(grafo, v, cor, corAtual):
        cor[v] = corAtual
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho = vizinho[1]
            if cor[vizinho] == -1:
                if not verificarBipartido(grafo, vizinho, cor, 1 - corAtual): # Se o vértice vizinho não foi visitado aplicamos a DFS nele
                    return False
            elif cor[vizinho] == cor[v]: # Se o vértice vizinho tem a mesma cor que o vértice atual
                return False
        return True

    cor = {v: -1 for v in grafo.vertices}

    for vertice in grafo.vertices:
        if cor[vertice] == -1: # Se o vértice ainda não foi visitado 
            if not verificarBipartido(grafo, vertice, cor, 0): 
                return "0"

    return "1"

# ------- Euleriano
def Euleriano(grafo):
    if not Conexo(grafo): # Se o grafo não é conexo, ele não pode ser euleriano
        return "0"
    
    if grafo.direcionado:
        # Verifica se o grafo direcionado é euleriano (grau de entrada = grau de saída)
        grauEntrada = {v: 0 for v in grafo.vertices}
        grauSaida = {v: 0 for v in grafo.vertices}
        
        for v in grafo.vertices:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[1]
                grauSaida[v] += 1
                grauEntrada[vizinho] += 1
        
        # Verifica se os graus de entrada e saída são iguais para todos os vértices
        for v in grafo.vertices:
            if grauEntrada[v] != grauSaida[v]:
                return "0"
            
        return "1"

    else:
        # Verifica se o grafo não direcionado é euleriano
        grau = {v: 0 for v in grafo.vertices}
        
        for v in grafo.vertices:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[1]
                grau[v] += 1
        
        # Verifica se o grau de todos os vértices é par
        for v in grafo.vertices:
            if grau[v] % 2 != 0:
                return "0"
            
        return "1"


# ------- Procura ciclo
def Cíclico(grafo):

    def verificarCiclo(grafo, v, visitado, pai):
        visitado.add(v) # Adiciona o vértice atual à lista de visitados
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho = vizinho[0]
            if vizinho not in visitado:
                if verificarCiclo(grafo, vizinho, visitado, v):
                    return True
            elif vizinho != pai: # Se o vértice vizinho já foi visitado e não é o pai do vértice atual, então encontramos um ciclo 
                return True
        return False

    visitado = set() # Lista de vértices visitados
    
    for vertice in grafo.vertices:
        if vertice not in visitado:
            if verificarCiclo(grafo, vertice, visitado, None):
                return "1"
    return "0"
