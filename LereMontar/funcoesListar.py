def DFS(grafo, v, tempo, adj_list):
    vertice = grafo.vertices[v]
    vertice.cor = 'cinza'
    tempo += 1
    vertice.tempo_descoberta = tempo

    for vizinho in adj_list[v]:
        if isinstance(vizinho, tuple):
            vizinho_id = vizinho[1]  # Acessa o vértice destino na tupla (idAresta, vizinho, peso)
        else:
            vizinho_id = vizinho

        vizinho_obj = grafo.vertices[vizinho_id]
        if vizinho_obj.cor == 'branco':
            vizinho_obj.pai = v
            tempo = DFS(grafo, vizinho_id, tempo, adj_list)

    vertice.cor = 'preto'
    tempo += 1
    vertice.tempo_finalizacao = tempo

    return tempo


# ------- Componentes Conexas
def ComponentesConexas(grafo):
    if grafo.direcionado:
        return -1
    
    componentes = []
    visitados = set()

    def dfs_componente(v, componente_atual):
        visitados.add(v)
        componente_atual.append(v)
        for vizinho in grafo.adj_list[v]:
            if isinstance(vizinho, tuple):  # Arestas como tuplas
                vizinho = vizinho[1]  # Seleciona apenas o vértice de destino
            if vizinho not in visitados:
                dfs_componente(vizinho, componente_atual)

    for vertice in grafo.vertices:
        if vertice not in visitados:
            componente_atual = []
            dfs_componente(vertice, componente_atual)
            componentes.append(sorted(componente_atual))  # Ordena para garantir a ordem correta

    return componentes


# ------- Componentes Fortemente Conexas
def ComponentesFortementeConexas(grafo):
    if not grafo.direcionado:
        return -1

    componentes = []
    visitados = set()
    stack = []

    # Usando sua função DFS para a primeira passagem
    def dfs_primeira_passagem(v):
        if v not in visitados:
            visitados.add(v)
            tempo = 0
            tempo = DFS(grafo, v, tempo, grafo.adj_list)  # Usa DFS para marcar tempos de finalização
            stack.append(v)

    # Primeira passagem: Preencher a pilha com a ordem de finalização dos vértices
    for vertice in grafo.vertices:
        if vertice not in visitados:
            dfs_primeira_passagem(vertice)

    # Inverter as arestas do grafo
    grafo.inverter_arestas()
    visitados.clear()

    # Segunda passagem: DFS na ordem inversa dos tempos de finalização para encontrar componentes
    while stack:
        v = stack.pop()
        if v not in visitados:
            componente_atual = []
            tempo = 0
            tempo = DFS(grafo, v, tempo, grafo.adj_list)  # Usa DFS para marcar os componentes
            for u in grafo.vertices:
                if grafo.vertices[u].cor == 'preto' and u not in visitados:
                    componente_atual.append(u)
                    visitados.add(u)
            componentes.append(componente_atual)

    # Reverter a inversão das arestas para restaurar o grafo original
    grafo.inverter_arestas()

    return componentes



def listarCaminhoEuleriano(grafo):
    grau_saida = {v: 0 for v in grafo.vertices}
    grau_entrada = {v: 0 for v in grafo.vertices}

    def tem_caminho_euleriano_direcionado():
        for v in grafo.vertices:
            for vizinho in grafo.adj_list[v]:
                if isinstance(vizinho, tuple):
                    vizinho = vizinho[0]
                grau_saida[v] += 1
                grau_entrada[vizinho] += 1

        for v in grafo.vertices:
            if grau_saida[v] != grau_entrada[v]:
                return False

        return True

    def tipo_caminho_euleriano_nao_direcionado():
        grau_impar = 0
        for v in grafo.vertices:
            grau = len([vizinho for vizinho in grafo.adj_list[v] if isinstance(vizinho, tuple) or isinstance(vizinho, str)])
            if grau % 2 != 0:
                grau_impar += 1
        if grau_impar == 0:
            return "Euleriano"
        elif grau_impar == 2:
            return "Semi-Euleriano"
        else:
            return "Nenhum"

    if grafo.direcionado:
        if not tem_caminho_euleriano_direcionado():
            return "O grafo não tem um caminho euleriano."
        
        caminho = []
        stack = []
        u = next((v for v in grafo.vertices if grau_saida[v] - grau_entrada[v] == 1), None) or grafo.vertices[0]

        while stack or u is not None:
            if not grafo.adj_list[u]:
                caminho.append(u)
                u = stack.pop() if stack else None
            else:
                stack.append(u)
                u = grafo.adj_list[u].pop()[0] if isinstance(grafo.adj_list[u][-1], tuple) else grafo.adj_list[u].pop()

        return caminho[::-1]

    else:
        tipo_caminho = tipo_caminho_euleriano_nao_direcionado()
        if tipo_caminho == "Nenhum":
            return "O grafo não tem um caminho euleriano."

        caminho = []
        stack = []
        u = next((v for v in grafo.vertices if len(grafo.adj_list[v]) % 2 != 0), None) or grafo.vertices[0]
        arestas_usadas = set()

        while stack or u is not None:
            if not grafo.adj_list[u]:
                caminho.append(u)
                u = stack.pop() if stack else None
            else:
                encontrou_arestas = False
                for vizinho in grafo.adj_list[u]:
                    if isinstance(vizinho, tuple):
                        vizinho = vizinho[0]
                    if (u, vizinho) not in arestas_usadas and (vizinho, u) not in arestas_usadas:
                        stack.append(u)
                        arestas_usadas.add((u, vizinho))
                        arestas_usadas.add((vizinho, u))
                        u = vizinho
                        encontrou_arestas = True
                        break
                if not encontrou_arestas:
                    caminho.append(u)
                    u = stack.pop() if stack else None

        if tipo_caminho == "Euleriano":
            return caminho[::-1]
        elif tipo_caminho == "Semi-Euleriano":
            return "Caminho Semi-Euleriano: " + str(caminho[::-1])
        

def listarVerticesArticulacao(grafo):
    vertices = grafo.vertices
    visitados = {v: False for v in vertices}
    descoberta = {v: float("inf") for v in vertices}
    baixo = {v: float("inf") for v in vertices}
    pai = {v: None for v in vertices}
    tempo = [0]
    articulacoes = []

    def dfs(v):
        visitados[v] = True
        tempo[0] += 1
        descoberta[v] = tempo[0]
        baixo[v] = tempo[0]
        filhos = 0

        for vizinho, peso in grafo.adj_list[v]:
            if not visitados[vizinho]:
                pai[vizinho] = v
                filhos += 1
                dfs(vizinho)

                baixo[v] = min(baixo[v], baixo[vizinho])

                # Verifica se v é articulação
                if pai[v] is None and filhos > 1:
                    articulacoes.append(v)
                if pai[v] is not None and baixo[vizinho] >= descoberta[v]:
                    articulacoes.append(v)

            elif vizinho != pai[v]:
                baixo[v] = min(baixo[v], descoberta[vizinho])

    for v in vertices:
        if not visitados[v]:
            dfs(v)

    if not articulacoes:
        return "O grafo não possui vértices de articulação."
    else:
        return articulacoes
    

def listarArestasPonte(grafo):
    # Inicializa os dicionários
    vertices = grafo.vertices
    visitados = {v: False for v in vertices}
    descoberta = {v: float("inf") for v in vertices}
    baixo = {v: float("inf") for v in vertices}
    pai = {v: None for v in vertices}
    tempo = [0]
    pontes = []

    # Função de busca em profundidade com Algoritmo de Tarjan
    def dfs(v):
        visitados[v] = True
        tempo[0] += 1
        descoberta[v] = baixo[v] = tempo[0]

        for aresta in grafo.adj_list[v]:
            if isinstance(aresta, tuple):
                id_aresta, vizinho, peso = aresta
            else:
                id_aresta = None
                vizinho = aresta
                peso = None

            if not visitados[vizinho]:
                pai[vizinho] = v
                dfs(vizinho)

                baixo[v] = min(baixo[v], baixo[vizinho])

                # Verifica se (v, vizinho) é uma ponte
                if baixo[vizinho] > descoberta[v]:
                    pontes.append(id_aresta)  # Adiciona apenas o id_aresta

            elif vizinho != pai[v]:
                baixo[v] = min(baixo[v], descoberta[vizinho])

    for v in vertices:
        if not visitados[v]:
            dfs(v)

    if not pontes:
        return "O grafo não possui arestas de ponte."
    else:
        return pontes

def dfs_lexicografica(v, grafo, visitados, arestas_usadas):
    visitados[v] = True
    for aresta in sorted(grafo.adj_list[v], key=lambda x: (x[1], x[0])):  # Ordena por vizinho e id_aresta
        id_aresta, vizinho = aresta[0], aresta[1]
        
        if not visitados[vizinho]:
            arestas_usadas.append(id_aresta)  # Adiciona o identificador da aresta
            dfs_lexicografica(vizinho, grafo, visitados, arestas_usadas)

def arvore_lexicografica(grafo):
    visitados = {v: False for v in grafo.vertices}
    arestas_usadas = []
    dfs_lexicografica(0, grafo, visitados, arestas_usadas)
    return arestas_usadas

from collections import deque

def bfs_lexicografica(v, grafo):
    visitados = {v: False for v in grafo.vertices}
    arestas_usadas = []
    fila = deque([v])
    visitados[v] = True

    while fila:
        atual = fila.popleft()
        for aresta in sorted(grafo.adj_list[atual], key=lambda x: (x[1])):  # Ordena os vizinhos por ordem lexicográfica
            id_aresta, vizinho, *peso = aresta
            
            if not visitados[vizinho]:
                visitados[vizinho] = True
                fila.append(vizinho)
                arestas_usadas.append(id_aresta)

    return arestas_usadas

def arvore_largura(grafo):
    if 0 not in grafo.vertices:
        return []  # Se não há vértice 0 no grafo, não pode gerar a árvore de largura
    
    return bfs_lexicografica(0, grafo)

import heapq
# Algoritmo de Prim para árvore geradora mínima
def prim_lexicografico(grafo):
    visitados = {v: False for v in grafo.vertices}
    mst = []
    min_heap = []
    inicial = 0

    visitados[inicial] = True
    for aresta in grafo.adj_list[inicial]:
        id_aresta, vizinho, peso = aresta
        heapq.heappush(min_heap, (peso, id_aresta, inicial, vizinho))

    while min_heap:
        peso, id_aresta, u, v = heapq.heappop(min_heap)
        if not visitados[v]:
            visitados[v] = True
            mst.append(id_aresta)

            for aresta in grafo.adj_list[v]:
                id_aresta, vizinho, peso = aresta
                if not visitados[vizinho]:
                    heapq.heappush(min_heap, (peso, id_aresta, v, vizinho))

    return mst

def arvore_geradora_minima(grafo):
    if len(grafo.arestas) == 0:
        return []  # Não há arestas para gerar uma árvore
    return prim_lexicografico(grafo)

from collections import defaultdict

def ordem_topologica(grafo):
    # Verifica se o grafo é direcionado
    if grafo.direcionado == False:
        return -1

    adj_list = grafo.adj_list
    pilha = []
    visitado = set()

    def dfs_pilha(grafo, v, tempo, adj_list, visitado, pilha):
        vertice = grafo.vertices[v]
        vertice.cor = 'cinza'
        tempo += 1
        vertice.tempo_descoberta = tempo

        for vizinho in adj_list[v]:
            if isinstance(vizinho, tuple):
                vizinho_id = vizinho[1]  # Acessa o vértice destino na tupla (idAresta, vizinho, peso)
            else:
                vizinho_id = vizinho

            if vizinho_id not in visitado:
                visitado.add(vizinho_id)
                tempo = dfs_pilha(grafo, vizinho_id, tempo, adj_list, visitado, pilha)

        vertice.cor = 'preto'
        tempo += 1
        vertice.tempo_finalizacao = tempo

        pilha.append(v)
        return tempo

    for vertice in grafo.vertices:
        if vertice not in visitado:
            visitado.add(vertice)
            dfs_pilha(grafo, vertice, 0, adj_list, visitado, pilha)

    # A pilha contém os vértices na ordem inversa da ordem topológica
    return pilha[::-1]

import heapq

def caminho_minimo(grafo):
    # Verifica se todos os pesos das arestas são iguais
    pesos = set()
    for arestas in grafo.adj_list.values():
        for aresta in arestas:
            if isinstance(aresta, tuple):
                peso = aresta[2]  # O peso está no terceiro índice (índice 2)
            else:
                peso = 1  # Peso padrão para arestas não ponderadas
            pesos.add(peso)
            if len(pesos) > 1:  # Se encontrar mais de um peso, podemos parar
                break
        if len(pesos) > 1:
            break
    
    # Se todos os pesos forem iguais, retorna -1
    if len(pesos) == 1:
        return -1
    if grafo.direcionado:
        return -1

    origem = 0
    destino = len(grafo.vertices) - 1
    distancias = {v: float('inf') for v in grafo.vertices}
    distancias[origem] = 0
    heap = [(0, origem)]  # (distância, vértice)
    
    while heap:
        distancia_atual, vertice_atual = heapq.heappop(heap)
        
        if distancia_atual > distancias[vertice_atual]:
            continue
        
        for aresta in grafo.adj_list[vertice_atual]:
            if isinstance(aresta, tuple):
                vizinho = aresta[1]
                peso = aresta[2]  # O peso está no terceiro índice (índice 2)
            else:
                vizinho = aresta
                peso = 1  # Peso padrão para arestas não ponderadas
            
            nova_distancia = distancia_atual + peso
            
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                heapq.heappush(heap, (nova_distancia, vizinho))
    
    return distancias[destino] if distancias[destino] != float('inf') else -1

